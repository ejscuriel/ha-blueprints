<div align="center">

# 🏠 Home Assistant Blueprints
### by EVOTECH LTDA

[![HA Version](https://img.shields.io/badge/Home%20Assistant-2026.1%2B-blue?logo=homeassistant)](https://www.home-assistant.io/)
[![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-green)](LICENSE)
[![Colombia](https://img.shields.io/badge/País-Colombia%20🇨🇴-yellow)]()
[![Web](https://img.shields.io/badge/Web-evotechltda.com-orange)](https://www.evotechltda.com)

**Colección de blueprints para desplegar hogares Home Assistant de forma rápida,
legible y repetible.**

Desarrollados por **Eduardo Sánchez Curiel — EVOTECH LTDA**

📧 admin@evotechltda.com · 🌐 www.evotechltda.com

</div>

---

## 📦 Blueprints recomendados

| # | Blueprint | Unidad de configuración | Descripción |
|---|---|---|---|
| 1 | 💡 [Interruptor ↔ Luz](#-1-interruptor--luz--una-pareja) | Una pareja | Sincronización bidireccional |
| 2 | 🚪 [Puerta → Luz / Interruptor](#-2-puerta--luz--interruptor--una-pareja) | Una pareja | Control con tres temporizadores |
| 3 | 🌦 [Presencia → Luz / Interruptor](#-3-presencia--luz--interruptor-con-horario-y-clima) | Una zona | Presencia, horarios, clima y máximo opcional |
| 4 | ❄️ [Aire acondicionado → Perfil fijo](#-4-aire-acondicionado--perfil-obligatorio-y-hasta-5-horarios) | Una unidad | Configuración obligatoria y cinco cambios programados |

Los blueprints se importan **una sola vez**. Después se crea una automatización
por pareja o zona. Esta estructura hace que la interfaz, las trazas, los nombres,
los reinicios y los errores sean independientes y fáciles de entender.

---

### 💡 1. Interruptor ↔ Luz — una pareja

> Sincroniza un interruptor y una luz sin cableado físico.

[![Importar Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/switch_light_single/BP_Switch_Light.yaml)

🔗 [Ver código fuente](blueprints/automation/switch_light_single/BP_Switch_Light.yaml)

**Comportamiento:**

| Evento | Resultado |
|---|---|
| Interruptor `on` | Enciende la luz con el brillo y la temperatura elegidos |
| Interruptor `off` | Apaga la luz |
| Luz `on` | Enciende el interruptor |
| Luz `off` | Apaga el interruptor |
| Estado `unknown` o `unavailable` | No ejecuta una acción cruzada |

**Parámetros:**

| Parámetro | Por defecto |
|---|---|
| Interruptor | Obligatorio |
| Luz | Obligatoria |
| Brillo | 55 % |
| Temperatura de color | 6500 K |

Cada pareja usa `mode: restart` de manera aislada. Si dos interruptores se
asocian deliberadamente con la misma luz, se crean dos automatizaciones y ambos
se sincronizan mediante los cambios de estado de esa luz.

---

### 🚪 2. Puerta → Luz / Interruptor — una pareja

> Controla una carga con un sensor de puerta y tres tiempos independientes.

[![Importar Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/door_light_single/BP_Door_Light.yaml)

🔗 [Ver código fuente](blueprints/automation/door_light_single/BP_Door_Light.yaml)

**Comportamiento:**

| Evento | Temporizador aplicado |
|---|---|
| La puerta abre | Enciende y usa el tiempo de puerta abierta (`t_ab`) |
| La puerta cierra | Usa el tiempo de puerta cerrada (`t_ce`) |
| El dispositivo enciende con la puerta abierta | Usa `t_ab` |
| El dispositivo enciende con la puerta cerrada | Usa el tiempo manual (`t_mc`) |
| El dispositivo se apaga físicamente o externamente | Cancela el tiempo activo |

**Valores especiales para los tres tiempos:**

| Valor | Resultado |
|---|---|
| `-1` | Encendido ilimitado; no hay apagado automático |
| `0` | Apagado inmediato |
| `1…3600` | Espera esa cantidad de segundos antes de apagar |

Antes de apagar, el blueprint confirma que la puerta conserva el estado
esperado y que la carga continúa encendida. Un cambio de estado reinicia solo
la automatización de esa pareja; nunca cancela el temporizador de otra zona.

---

### 🌦 3. Presencia → Luz / Interruptor con horario y clima

> Controla una carga por presencia, horario y clima, con límite máximo opcional.

[![Importar Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/presence_climate/BP_Presencia_Interruptor_Clima.yaml)

🔗 [Ver código fuente](blueprints/automation/presence_climate/BP_Presencia_Interruptor_Clima.yaml)

Controla una luz, interruptor o relé a partir de un sensor binario de presencia.
El encendido automático se autoriza dentro del horario normal o dentro de un
horario alternativo cuando la entidad meteorológica coincide con los estados
seleccionados.

**Comportamiento:**

| Evento | Resultado |
|---|---|
| Nueva presencia dentro de un horario autorizado | Solicita el encendido |
| Encendido automático o manual | Inicia un ciclo de control |
| Encendido sin presencia | Espera la validación; apaga si la presencia no aparece |
| Ausencia continua | Apaga después del tiempo configurado |
| Máximo habilitado y agotado | Apaga aunque el sensor continúe en `on` |
| Máximo deshabilitado | No limita el ciclo mientras exista presencia |
| Apagado físico o externo | Finaliza inmediatamente el ciclo |

**Valores predeterminados:**

| Parámetro | Valor |
|---|---|
| Validación inicial | 5 s |
| Ausencia antes de apagar | 5 s |
| Aplicar tiempo máximo | Activado |
| Tiempo máximo | 5 min |
| Horario normal | 17:30–06:40 |
| Horario climático | 06:40–17:30 |
| Clima habilitante | Nublado, lluvia, lluvia fuerte y tormenta con lluvia |

Los horarios predeterminados son complementarios. El normal cubre la tarde,
la noche y la madrugada; el climático cubre el resto del día solamente cuando
el clima lo justifica.

El máximo es útil en lavanderías o áreas de trabajo donde una lavadora o
secadora puede producir falsas presencias por vibración. Puede desactivarse en
cocina, estudio u otras zonas en las que la ausencia sea suficiente para apagar.

**Reglas de tiempo:**

- El máximo comienza en el encendido real del dispositivo.
- Durante la validación vence el plazo más corto entre validación y máximo restante.
- Cuando se alcanza el máximo, no se enciende otra vez hasta una nueva presencia.
- Un encendido manual posterior inicia un ciclo nuevo.
- La ausencia y el apagado físico conservan prioridad aunque el máximo esté desactivado.

---

### ❄️ 4. Aire acondicionado — perfil obligatorio y hasta 5 horarios

> Normaliza la configuración de una unidad sin importar cómo fue encendida.

[![Importar Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/climate_fixed_schedule/BP_Climate_Fixed_Schedule.yaml)

🔗 [Ver código fuente](blueprints/automation/climate_fixed_schedule/BP_Climate_Fixed_Schedule.yaml)

Se crea una automatización por cada entidad `climate.*`. Después de permanecer
encendida durante un minuto en **cualquier modo activo**, la unidad recibe el
perfil inicial. Esto incluye encendidos en `dry`, `auto`, `fan_only`, `cool`,
`heat` y cualquier otro modo publicado por la integración.

El minuto pendiente pertenece al disparador de Home Assistant. Si el servidor
se reinicia o se recargan las automatizaciones durante ese minuto, el conteo no
se conserva; el siguiente encendido normal vuelve a iniciar el proceso completo.

**Comportamiento:**

| Evento | Resultado |
|---|---|
| La unidad completa un minuto encendida | Aplica modo obligatorio, temperatura, ventilador y oscilaciones |
| Llega una de las cinco horas habilitadas | Aplica ese perfil si la unidad continúa encendida |
| Llega una hora deshabilitada | No hace nada |
| La unidad se apaga antes de cumplir el minuto | No genera el evento inicial |
| Otro evento llega mientras se aplica un perfil | `mode: single` conserva la primera ejecución y registra la superposición |
| La entidad está `unknown` o `unavailable` | No envía órdenes; registra el perfil omitido |
| Una orden falla o un valor no se aplica | Continúa con las demás órdenes y registra un resumen final |
| Un parámetro ya tiene el valor solicitado | No lo reenvía y evita ese pitido |
| Reenvío obligatorio activado para el perfil | Envía todos sus parámetros configurados aunque ya coincidan |

Cada horario puede configurar temperatura, ventilador, oscilación vertical y
oscilación horizontal. La opción **No modificar** permite que un horario cambie
solo los valores necesarios. Para usar uno, dos o tres horarios, se dejan los
restantes desactivados.

El perfil inicial precargado reproduce la configuración vigente de la unidad de
Eduardo: `cool / 21 / low / Bottom / MiddleRight`. Las cinco horas propuestas
son 23:00, 00:00, 01:00, 02:00 y 03:00. Por seguridad, todos los horarios vienen
desactivados; cada usuario habilita únicamente los que necesite.

Cada perfil incluye **Reenviar aunque ya coincida**, desactivado de forma
predeterminada. Así se evitan órdenes y pitidos innecesarios. Al activarlo, el
modo, la temperatura y cada opción distinta de **No modificar** se consideran
obligatorios y se transmiten incluso si el estado publicado ya es igual.

La sección avanzada **Acciones opcionales** permite conservar funciones que no
son propias del clima. Su selector solo decide después de cuáles perfiles se
ejecutan esas acciones: marcar allí un horario **no lo activa**. Cada horario se
habilita exclusivamente con **Ejecutar el perfil horario N** dentro de su propia
sección. En la unidad de Eduardo se usa para encender
`switch.aire_edu_display_light` solo después del perfil inicial, 22:00 y 00:00.

Al finalizar, el blueprint espera cinco segundos y compara el modo HVAC, la
temperatura, el ventilador y las oscilaciones con el perfil solicitado. Solo
escribe un error si detecta diferencias, valores no soportados, apagado durante
la ejecución o pérdida de disponibilidad. Los errores individuales de las
órdenes no cancelan la comprobación final.

Los nombres de ventilador y oscilación no son universales. El selector incluye
los valores observados en las unidades EVOTECH y permite escribir valores
personalizados para otras marcas e integraciones.

**Migración desde `SETTING A.A.`:**

1. Importa el blueprint y crea primero una instancia para una sola unidad.
2. Copia al perfil inicial los valores que hoy recibe el script.
3. Convierte las llamadas horarias de esa unidad en los horarios 1–5 y activa
   solamente los que realmente utilice.
4. Prueba encendiendo desde `off` en `cool`, `dry`, `auto` y `fan_only`, y espera
   un minuto completo en cada prueba.
5. Cuando las trazas confirmen el resultado, desactiva las automatizaciones
   antiguas de configuración inicial y horarios de esa unidad para evitar que
   dos lógicas envíen órdenes simultáneas.
6. Repite el proceso unidad por unidad. El script compartido se elimina al final,
   cuando ninguna automatización antigua lo siga llamando.

---

## ✨ Criterios de diseño

- Home Assistant **2026.1.0 o superior**; no se mantiene compatibilidad con versiones antiguas.
- Sintaxis moderna: `triggers`, `conditions`, `actions` y llamadas mediante `action`.
- Una automatización por pareja o zona para trazas y reinicios independientes.
- YAML explícito y visible en el editor; Jinja se reserva para cálculos de tiempo inevitables.
- Entradas agrupadas en secciones plegables y con selectores actuales.
- Comentarios dentro del código para explicar decisiones y estados límite.
- GitHub `main` es la fuente canónica para importar y desplegar los blueprints.

---

## 🧭 Instalación y despliegue

1. Usa el botón **Importar Blueprint** del blueprint deseado.
2. En Home Assistant abre **Configuración → Automatizaciones y escenas → Planos**.
3. Crea una automatización desde el plano importado.
4. Repite el paso anterior por cada pareja o zona; no vuelvas a importar el archivo.
5. Asigna un alias que identifique claramente el espacio y los dispositivos.

Las rutas canónicas son:

```text
blueprints/automation/switch_light_single/BP_Switch_Light.yaml
blueprints/automation/door_light_single/BP_Door_Light.yaml
blueprints/automation/presence_climate/BP_Presencia_Interruptor_Clima.yaml
blueprints/automation/climate_fixed_schedule/BP_Climate_Fixed_Schedule.yaml
```

Para actualizar un blueprint ya importado, vuelve a importarlo desde su misma URL
y recarga las automatizaciones que lo utilizan.

---

## 🔍 Diagnóstico

Los cuatro blueprints recomendados usan las **trazas nativas de cada
automatización**. En Home Assistant abre la automatización concreta y selecciona
**Trazas**. Al existir una instancia por pareja, zona o unidad, la traza muestra
directamente qué habitación y qué temporizador produjeron el resultado.

Los estados `unknown` y `unavailable` no se convierten en órdenes de encendido o
apagado. Esto evita sincronizaciones no deseadas después de una desconexión o
del reinicio de Home Assistant.

---

## 🛠 Herramientas de mantenimiento

### Perfil mínimo de entidades Dahua

[`tools/Set-DahuaEntityProfile.ps1`](tools/Set-DahuaEntityProfile.ps1) audita o
aplica una lista blanca después de agregar una cámara Dahua. Conserva solamente
`Main`, `Sub`, `Motion Alarm`, `Smart Motion Human`, `Motion Detection` y
`Smart Motion Detection` por dispositivo; el resto se deshabilita de forma
reversible en el registro de entidades.

La ejecución sin `-Apply` es una simulación. Las instrucciones completas y las
precauciones para el token están en [`tools/README.md`](tools/README.md).

---

## 🗃 Blueprints multipareja heredados

Las versiones anteriores se conservan para consulta y reversión. Siguen siendo
válidas para las instalaciones existentes, pero no son la estructura recomendada
para despliegues nuevos porque una sola ejecución puede mezclar trazas o reiniciar
temporizadores de parejas distintas.

| Blueprint heredado | Código | Importar |
|---|---|---|
| Switch ↔ Light — hasta 10 parejas | [Fuente](blueprints/automation/switch_light/BP_Multi_Switch_Light.yaml) | [Importar](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/switch_light/BP_Multi_Switch_Light.yaml) |
| Door → Light — hasta 10 parejas | [Fuente](blueprints/automation/door_light/BP_Multi_Door_Light.yaml) | [Importar](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/door_light/BP_Multi_Door_Light.yaml) |

No es necesario borrar estas versiones al migrar: basta con que las nuevas
automatizaciones apunten a los blueprints de una pareja.

---

## 🧾 Versiones

| Blueprint | Versión | Fecha | Estado |
|---|---:|---:|---|
| Interruptor ↔ Luz — una pareja | 2.0.0 | 2026-09-02 | Recomendado |
| Puerta → Luz / Interruptor — una pareja | 3.0.0 | 2026-09-02 | Recomendado |
| Presencia → Luz / Interruptor | 0.2.1 BETA | 2026-09-02 | Beta controlada |
| Aire acondicionado → Perfil fijo | 1.4.1 | 2026-09-07 | Nueva versión para pruebas |
| Switch ↔ Light — multipareja | 1.2.0 | 2025-05-20 | Heredado |
| Door → Light — multipareja | 2.1.0 | 2025-05-20 | Heredado |

---

## 🤝 Contribuciones

¿Encontraste un problema o tienes una mejora? Abre un **Issue** o un **Pull Request**.
Para casos de uso distintos, escribe a admin@evotechltda.com.

---

## 📄 Licencia

MIT License — Copyright (c) 2025–2026 EVOTECH LTDA — Eduardo Sánchez Curiel.

Se permite el uso, copia y modificación libre con crédito al autor original.

---

<div align="center">

Hecho con ❤️ en Colombia 🇨🇴 por **EVOTECH LTDA**

[www.evotechltda.com](https://www.evotechltda.com) · admin@evotechltda.com

</div>
