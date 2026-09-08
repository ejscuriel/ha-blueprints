# Perfil mínimo de entidades Dahua

`Set-DahuaEntityProfile.ps1` aplica una lista blanca a todas las entidades de la
plataforma `dahua`. Es idempotente: puede ejecutarse nuevamente después de
agregar una cámara y solo modifica lo que no coincide con el perfil.

## Entidades que permanecen habilitadas

Por cada cámara se conservan:

- `Main`
- `Sub`
- `Motion Alarm`
- `Smart Motion Human`
- `Motion Detection`
- `Smart Motion Detection`

Todas las demás se marcan como deshabilitadas por el usuario. La utilidad no
elimina entidades ni modifica parámetros internos de las cámaras.

## Uso

Requiere PowerShell 5.1 o superior y un token de acceso de larga duración de un
usuario administrador de Home Assistant. El token se solicita de forma oculta
si no se proporciona mediante `HOME_ASSISTANT_TOKEN`; nunca se guarda en disco.
Cada operación tiene un límite de espera de 15 segundos, configurable mediante
`-TimeoutSeconds`.

Primero se ejecuta la auditoría, que no cambia nada:

```powershell
.\tools\Set-DahuaEntityProfile.ps1 -BaseUrl http://homeassistant.local:8123
```

Después de revisar la tabla, se aplica el perfil:

```powershell
.\tools\Set-DahuaEntityProfile.ps1 -BaseUrl http://homeassistant.local:8123 -Apply
```

Para una instalación que publique la integración bajo otro identificador o que
necesite una lista distinta:

```powershell
.\tools\Set-DahuaEntityProfile.ps1 `
  -BaseUrl https://ha.example.com `
  -Platform dahua `
  -KeepNames Main,Sub,'Motion Alarm' `
  -Apply
```

La cuenta debe ser administradora porque el cambio se realiza mediante el
registro de entidades de la API WebSocket de Home Assistant. Si una operación
falla, la utilidad continúa con las restantes y termina mostrando un resumen de
errores. El token no debe incluirse en Git, documentación ni capturas.

## Alcance

Deshabilitar entidades reduce estados, historial y ruido visual dentro de Home
Assistant. No evita por sí solo que la integración Dahua haga consultas internas
a la cámara; los problemas de sesiones o solicitudes agotadas deben medirse de
nuevo después de esta limpieza.
