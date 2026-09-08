[CmdletBinding()]
param(
    [Parameter()]
    [ValidatePattern('^https?://')]
    [string]$BaseUrl = 'http://homeassistant.local:8123',

    [Parameter()]
    [string]$Token = $env:HOME_ASSISTANT_TOKEN,

    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string]$Platform = 'dahua',

    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string[]]$KeepNames = @(
        'Main',
        'Motion Alarm',
        'Motion Detection',
        'Reboot',
        'Smart Motion Detection',
        'Smart Motion Human',
        'Sub'
    ),

    [Parameter()]
    [switch]$Apply,

    [Parameter()]
    [ValidateRange(5, 120)]
    [int]$TimeoutSeconds = 15
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function ConvertTo-HaWebSocketUri {
    param([Parameter(Mandatory)][string]$Url)

    $httpUri = [Uri]$Url.TrimEnd('/')
    $socketScheme = switch ($httpUri.Scheme) {
        'http' { 'ws' }
        'https' { 'wss' }
        default { throw "El esquema '$($httpUri.Scheme)' no es compatible." }
    }

    $builder = [UriBuilder]$httpUri
    $builder.Scheme = $socketScheme
    $builder.Path = "$($httpUri.AbsolutePath.TrimEnd('/'))/api/websocket"
    $builder.Query = ''
    $builder.Fragment = ''
    return $builder.Uri
}

function Send-HaWebSocketMessage {
    param(
        [Parameter(Mandatory)][System.Net.WebSockets.ClientWebSocket]$Socket,
        [Parameter(Mandatory)][hashtable]$Message,
        [Parameter(Mandatory)][int]$Timeout
    )

    $json = $Message | ConvertTo-Json -Compress -Depth 20
    $bytes = [Text.Encoding]::UTF8.GetBytes($json)
    $segment = [ArraySegment[byte]]::new($bytes)
    $timeoutSource = [Threading.CancellationTokenSource]::new($Timeout * 1000)
    try {
        $null = $Socket.SendAsync(
            $segment,
            [System.Net.WebSockets.WebSocketMessageType]::Text,
            $true,
            $timeoutSource.Token
        ).GetAwaiter().GetResult()
    }
    finally {
        $timeoutSource.Dispose()
    }
}

function Receive-HaWebSocketMessage {
    param(
        [Parameter(Mandatory)][System.Net.WebSockets.ClientWebSocket]$Socket,
        [Parameter(Mandatory)][int]$Timeout
    )

    $memory = [IO.MemoryStream]::new()
    $timeoutSource = [Threading.CancellationTokenSource]::new($Timeout * 1000)
    try {
        do {
            $buffer = [byte[]]::new(8192)
            $segment = [ArraySegment[byte]]::new($buffer)
            $result = $Socket.ReceiveAsync(
                $segment,
                $timeoutSource.Token
            ).GetAwaiter().GetResult()

            if ($result.MessageType -eq [System.Net.WebSockets.WebSocketMessageType]::Close) {
                throw 'Home Assistant cerró la conexión WebSocket.'
            }

            $memory.Write($buffer, 0, $result.Count)
        } until ($result.EndOfMessage)

        $text = [Text.Encoding]::UTF8.GetString($memory.ToArray())
        return $text | ConvertFrom-Json
    }
    finally {
        $timeoutSource.Dispose()
        $memory.Dispose()
    }
}

function Invoke-HaWebSocketCommand {
    param(
        [Parameter(Mandatory)][System.Net.WebSockets.ClientWebSocket]$Socket,
        [Parameter(Mandatory)][int]$Id,
        [Parameter(Mandatory)][hashtable]$Command,
        [Parameter(Mandatory)][int]$Timeout
    )

    $message = @{} + $Command
    $message.id = $Id
    Send-HaWebSocketMessage -Socket $Socket -Message $message -Timeout $Timeout

    do {
        $response = Receive-HaWebSocketMessage -Socket $Socket -Timeout $Timeout
    } until ($null -ne $response.id -and [int]$response.id -eq $Id)

    if (-not $response.success) {
        $details = if ($response.error.message) { $response.error.message } else { 'Error desconocido' }
        throw "Falló '$($Command.type)': $details"
    }

    return $response.result
}

function Test-IsKeptDahuaEntity {
    param(
        [Parameter(Mandatory)]$Entity,
        [Parameter(Mandatory)][string[]]$AllowedNames
    )

    $sourceName = if ($Entity.original_name) {
        [string]$Entity.original_name
    }
    else {
        ([string]$Entity.entity_id).Split('.', 2)[1] -replace '_', ' '
    }

    foreach ($allowedName in $AllowedNames) {
        if ($sourceName -match "(?:^| )$([Regex]::Escape($allowedName))$") {
            return $true
        }
    }
    return $false
}

$socket = [System.Net.WebSockets.ClientWebSocket]::new()
$secureToken = $null
$tokenPointer = [IntPtr]::Zero

try {
    if ([string]::IsNullOrWhiteSpace($Token)) {
        $secureToken = Read-Host 'Token de acceso de larga duración de un administrador' -AsSecureString
        $tokenPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureToken)
        $Token = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($tokenPointer)
    }

    if ([string]::IsNullOrWhiteSpace($Token)) {
        throw 'No se recibió un token de acceso.'
    }

    $socketUri = ConvertTo-HaWebSocketUri -Url $BaseUrl
    Write-Host "Conectando a $socketUri ..."
    $connectTimeout = [Threading.CancellationTokenSource]::new($TimeoutSeconds * 1000)
    try {
        $null = $socket.ConnectAsync($socketUri, $connectTimeout.Token).GetAwaiter().GetResult()
    }
    finally {
        $connectTimeout.Dispose()
    }

    $authRequired = Receive-HaWebSocketMessage -Socket $socket -Timeout $TimeoutSeconds
    if ($authRequired.type -ne 'auth_required') {
        throw "Respuesta inicial inesperada: $($authRequired.type)"
    }

    Send-HaWebSocketMessage -Socket $socket -Timeout $TimeoutSeconds -Message @{
        type = 'auth'
        access_token = $Token
    }
    $authResult = Receive-HaWebSocketMessage -Socket $socket -Timeout $TimeoutSeconds
    if ($authResult.type -ne 'auth_ok') {
        throw 'Home Assistant rechazó el token. Debe pertenecer a un administrador.'
    }

    $messageId = 1
    $allEntities = @(Invoke-HaWebSocketCommand -Socket $socket -Id $messageId -Timeout $TimeoutSeconds -Command @{
        type = 'config/entity_registry/list'
    })

    $platformEntities = @($allEntities | Where-Object { $_.platform -eq $Platform })
    if ($platformEntities.Count -eq 0) {
        throw "No se encontraron entidades de la plataforma '$Platform'."
    }

    $plan = foreach ($entity in $platformEntities) {
        $keep = Test-IsKeptDahuaEntity -Entity $entity -AllowedNames $KeepNames
        $disabledBy = if ($null -eq $entity.disabled_by) { '' } else { [string]$entity.disabled_by }
        $desiredState = if ($keep) { 'Habilitada' } else { 'Deshabilitada' }
        $action = if ($keep -and $disabledBy) {
            'Habilitar'
        }
        elseif (-not $keep -and -not $disabledBy) {
            'Deshabilitar'
        }
        else {
            'Sin cambio'
        }

        [pscustomobject]@{
            EntityId = [string]$entity.entity_id
            NombreOriginal = [string]$entity.original_name
            EstadoDeseado = $desiredState
            Accion = $action
            DeshabilitadaPor = $disabledBy
        }
    }

    $changes = @($plan | Where-Object { $_.Accion -ne 'Sin cambio' })
    $keepCount = @($plan | Where-Object { $_.EstadoDeseado -eq 'Habilitada' }).Count
    $disableCount = @($plan | Where-Object { $_.EstadoDeseado -eq 'Deshabilitada' }).Count

    Write-Host ''
    Write-Host "Plataforma: $Platform"
    Write-Host "Entidades encontradas: $($platformEntities.Count)"
    Write-Host "Perfil final: $keepCount habilitadas / $disableCount deshabilitadas"
    Write-Host "Cambios pendientes: $($changes.Count)"

    if ($changes.Count -gt 0) {
        $changes | Sort-Object EntityId | Format-Table Accion, EntityId, NombreOriginal -AutoSize
    }

    if (-not $Apply) {
        Write-Host ''
        Write-Host 'Modo auditoría: no se realizó ningún cambio.'
        Write-Host 'Ejecuta nuevamente con -Apply para aplicar este plan.'
        return
    }

    $failures = [System.Collections.Generic.List[object]]::new()
    foreach ($change in $changes) {
        $messageId += 1
        $disabledBy = if ($change.Accion -eq 'Deshabilitar') { 'user' } else { $null }
        try {
            $null = Invoke-HaWebSocketCommand -Socket $socket -Id $messageId -Timeout $TimeoutSeconds -Command @{
                type = 'config/entity_registry/update'
                entity_id = $change.EntityId
                disabled_by = $disabledBy
            }
            Write-Host "OK  $($change.Accion): $($change.EntityId)"
        }
        catch {
            $failures.Add([pscustomobject]@{
                EntityId = $change.EntityId
                Error = $_.Exception.Message
            })
        }
    }

    Write-Host ''
    Write-Host "Resultado: $($changes.Count - $failures.Count) cambios correctos; $($failures.Count) errores."
    if ($failures.Count -gt 0) {
        $failures | Format-Table EntityId, Error -Wrap
        throw 'El perfil terminó con errores. Revisa la tabla anterior.'
    }
}
finally {
    $Token = $null
    if ($tokenPointer -ne [IntPtr]::Zero) {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($tokenPointer)
    }
    if ($socket.State -eq [System.Net.WebSockets.WebSocketState]::Open) {
        $closeTimeout = [Threading.CancellationTokenSource]::new($TimeoutSeconds * 1000)
        try {
            $null = $socket.CloseAsync(
                [System.Net.WebSockets.WebSocketCloseStatus]::NormalClosure,
                'Finished',
                $closeTimeout.Token
            ).GetAwaiter().GetResult()
        }
        catch {
            $socket.Abort()
        }
        finally {
            $closeTimeout.Dispose()
        }
    }
    $socket.Dispose()
}
