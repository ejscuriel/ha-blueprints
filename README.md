<div align="center">

# 🏠 Home Assistant Blueprints
### by EVOTECH LTDA

[![HA Version](https://img.shields.io/badge/Home%20Assistant-2024.4%2B-blue?logo=homeassistant)](https://www.home-assistant.io/)
[![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-green)](LICENSE)
[![Colombia](https://img.shields.io/badge/País-Colombia%20🇨🇴-yellow)]()
[![Web](https://img.shields.io/badge/Web-evotechltda.com-orange)](https://www.evotechltda.com)

**Colección de blueprints profesionales para Home Assistant**
desarrollados por **Eduardo Sánchez Curiel — EVOTECH LTDA**

📧 admin@evotechltda.com · 🌐 www.evotechltda.com

</div>

---

## 📦 Blueprints disponibles

| # | Blueprint | Descripción rápida |
|---|---|---|
| 1 | 💡 [Switch ↔ Light](#-1-vincular-interruptores-con-luces-cct) | Sincroniza interruptor y luz bidireccionalmente |
| 2 | 🚪 [Door → Light](#-2-puerta--luz--interruptor-con-temporización) | Controla luz por apertura de puerta con timers |
| 3 | 🌦 [Presence → Light / Switch](#-3-presencia--luz--interruptor-con-horario-y-clima) | Controla una carga por presencia, horario y clima |

---

### 💡 1. Switch ↔ Light (WiFi / Zigbee)

> Sincroniza interruptor y luz sin cableado físico — hasta 10 parejas

[![Importar Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/switch_light/BP_Multi_Switch_Light.yaml)
🔗 [Ver código fuente](blueprints/automation/switch_light/BP_Multi_Switch_Light.yaml)

---

### 🚪 2. Door → Light / Switch

> Enciende/apaga luz al abrir/cerrar una puerta con timers configurables — hasta 10 parejas

[![Importar Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/door_light/BP_Multi_Door_Light.yaml)
🔗 [Ver código fuente](blueprints/automation/door_light/BP_Multi_Door_Light.yaml)

---

### 🌦 3. Presence → Light / Switch

> Controla una luz, interruptor o relé por presencia, horario y clima, con límite máximo opcional

[![Importar Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/presence_climate/BP_Presencia_Interruptor_Clima.yaml)
🔗 [Ver código fuente](blueprints/automation/presence_climate/BP_Presencia_Interruptor_Clima.yaml)

---

## ✨ Características de la colección

- ✅ Los blueprints multipareja admiten hasta **10 parejas** por instancia
- ✅ Entradas organizadas en secciones **plegables** cuando corresponde
- ✅ Protección ante estados no disponibles y trazabilidad según cada blueprint
- ✅ Compatible con **WiFi** (Tuya, Sonoff, Shelly) y **Zigbee** (IKEA, Aqara, Sonoff ZB)
- ✅ Cada blueprint declara y documenta su versión mínima de Home Assistant

---

## 📖 Documentación detallada

---

### 💡 1. Vincular Interruptores con Luces CCT

> **Sincronización bidireccional interruptor ↔ luz sin cableado físico**

En muchas instalaciones conviven interruptores WiFi o Zigbee con tiras LED
controladas por un controlador WiFi independiente. Aunque físicamente el
interruptor **no está cableado** a la tira LED, este blueprint logra una
sincronización **lógica** bidireccional: el interruptor actúa como si estuviera
directamente conectado a la luz, y viceversa.

**Comportamiento:**
| Evento | Resultado |
|---|---|
| Interruptor `ON` | Enciende la luz con brillo y temperatura definidos |
| Interruptor `OFF` | Apaga la luz |
| Luz `ON` | Enciende el interruptor |
| Luz `OFF` | Apaga el interruptor |

**Parámetros configurables:**
| Parámetro | Descripción | Por defecto |
|---|---|---|
| Brillo por defecto | % de brillo al encender (1–100) | 55% |
| Temperatura por defecto | Kelvin: 2700 cálido · 6500 frío | 6500 K |
| Pareja N → Interruptor | Entity ID del switch | — |
| Pareja N → Luz | Entity ID de la luz CCT | — |
| Pareja N → Brillo | Individual (0 = usar defecto) | 0 |
| Pareja N → Temperatura | Individual (0 = usar defecto) | 0 |

**Log de seguimiento** (`blueprint.sync_switch_luz`):
```
INFO  [Sala principal] Pareja 1 — Switch→Luz: 'switch.sonoff_sala' → ON
      → 'light.led_sala' encendida (brillo=55%, CT=6500K)
WARN  [Sala principal] Pareja 1 — OMITIDO: 'light.led_sala' no disponible
      Verifica la conexión del dispositivo.
```

**Versiones:**
| Versión | Fecha | Cambios |
|---|---|---|
| 1.2.0 | 2025-05-20 | Logs con nombre de automatización y nº de pareja |
| 1.1.0 | 2025-05-20 | Ampliado a 10 parejas |
| 1.0.0 | 2025-05-20 | Versión inicial |

[![Importar Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/switch_light/BP_Multi_Switch_Light.yaml)
🔗 [Ver código fuente](blueprints/automation/switch_light/BP_Multi_Switch_Light.yaml)

---

### 🚪 2. Puerta → Luz / Interruptor con Temporización

> **Control automático de iluminación por apertura de puertas con 3 timers independientes**

Vincula hasta 10 sensores de puerta con luces o interruptores de forma **lógica**,
sin cableado físico. Cada pareja gestiona sus propios timers de forma independiente.
Compatible con sensores **WiFi y Zigbee** y cualquier luz o switch integrado en HA.

Ideal para **entradas, pasillos, closets, bodegas, baños y garajes**.

**Comportamiento:**
| Evento | Timer | Resultado |
|---|---|---|
| Puerta `ABRE` | `t_ab` | Enciende + apaga tras t_ab segundos |
| Puerta `CIERRA` | `t_ce` | Apaga tras t_ce segundos |
| Switch `ON` manual + puerta **abierta** | `t_ab` | Reinicia el timer t_ab |
| Switch `ON` manual + puerta **cerrada** | `t_mc` | Apaga tras t_mc segundos |
| Cualquier timer = `0` | — | Apaga **inmediatamente** |
| Cualquier timer = `-1` | — | Sin apagado automático (**ilimitado**) |

**Parámetros por pareja (cada pareja es independiente):**
| Parámetro | Descripción | Sugerido |
|---|---|---|
| Sensor de puerta | Binary sensor (door, window, opening) | — |
| Luz o interruptor | Acepta light.* y switch.* | — |
| `t_ab` | Tiempo tras abrir puerta. 0=inmediato, -1=ilimitado | 300 s |
| `t_ce` | Tiempo tras cerrar puerta. 0=inmediato, -1=ilimitado | 60 s |
| `t_mc` | Tiempo encendido manual + puerta cerrada. 0=inmediato, -1=ilimitado | 120 s |

**Log de seguimiento** (`blueprint.door_light`):
```
INFO  [Entrada] Pareja 1 — Puerta ABIERTA → 'light.led_entrada' encendido. t_ab: 300s
INFO  [Entrada] Pareja 1 — t_ab agotado (300s), puerta aún abierta → apagado
INFO  [Entrada] Pareja 1 — Puerta CERRADA. t_ce: 60s
INFO  [Entrada] Pareja 1 — t_ce agotado (60s) → 'light.led_entrada' apagado
INFO  [Entrada] Pareja 1 — Encendido MANUAL. Puerta: off. Timer (t_mc): 120s
INFO  [Entrada] Pareja 1 — t_ce cancelado: puerta volvió a abrirse → control a t_ab
WARN  [Entrada] Pareja 1 — OMITIDO: Sensor no disponible (unavailable)
WARN  [Entrada] Pareja 1 — OMITIDO: Dispositivo no disponible (unavailable)
```

**Versiones:**
| Versión | Fecha | Cambios |
|---|---|---|
| 2.1.0 | 2025-05-20 | Lógica definitiva: t_ab al abrir, -1=ilimitado en todos los timers |
| 2.0.0 | 2025-05-20 | Selector entity para detección de encendido manual |
| 1.2.0 | 2025-05-20 | Eliminados valores globales por defecto |
| 1.1.0 | 2025-05-20 | Parámetro t_mc: encendido manual + puerta cerrada |
| 1.0.0 | 2025-05-20 | Versión inicial |

[![Importar Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/door_light/BP_Multi_Door_Light.yaml)
🔗 [Ver código fuente](blueprints/automation/door_light/BP_Multi_Door_Light.yaml)

---

### 🌦 3. Presencia → Luz / Interruptor con Horario y Clima

> **Control de una carga por presencia, con horarios, clima y temporizadores**

Controla una luz, interruptor o relé a partir de un sensor binario de presencia.
El encendido automático se limita por día y horario, pero también puede habilitarse
durante un horario alternativo cuando la entidad meteorológica indique lluvia o
nubosidad. Requiere **Home Assistant 2026.1.0 o superior**.

El tiempo máximo es opcional: resulta útil en zonas de lavandería o trabajo donde
la vibración puede mantener un sensor activo por error. En cocina, estudio u otras
zonas donde ese límite no interesa, se puede desactivar y el ciclo queda sin tiempo
máximo mientras exista presencia.

**Comportamiento:**

| Evento | Resultado |
|---|---|
| Nueva presencia dentro del horario autorizado | Solicita el encendido |
| Encendido automático o manual | Inicia un único ciclo de control |
| Encendido sin presencia | Espera la validación; si no aparece presencia, apaga |
| Ausencia continua | Apaga tras el tiempo de ausencia |
| Tiempo máximo habilitado y agotado | Apaga aunque el sensor continúe en `on` |
| Tiempo máximo deshabilitado | Mantiene el ciclo sin límite mientras haya presencia |
| Apagado físico o externo | Termina inmediatamente el ciclo activo |

**Parámetros principales:**

| Parámetro | Descripción | Por defecto |
|---|---|---|
| Sensor de presencia | `binary_sensor.*`: `on` = presencia, `off` = ausencia | — |
| Luz, interruptor o relé | Entidad `light.*` o `switch.*` | — |
| Espera inicial por presencia | Validación tras encender sin presencia | 5 s |
| Ausencia antes de apagar | Ausencia continua necesaria para apagar | 5 s |
| Aplicar tiempo máximo | Activa o desactiva el límite absoluto del ciclo | Activado |
| Tiempo máximo | Se cuenta desde el encendido real | 5 min |
| Horario normal | Puede atravesar la medianoche | 17:30–06:40 |
| Horario climático | Cubre el tramo restante si el clima coincide | 06:40–17:30 |
| Estados climáticos | Condiciones que habilitan el horario alternativo | Nublado, lluvia, lluvia fuerte y tormenta con lluvia |

Los horarios predeterminados son complementarios: el normal cubre
`17:30–06:40` y el climático cubre `06:40–17:30`. Así, el clima adverso puede
autorizar el tramo diurno que no cubre el horario normal.

**Reglas de temporización importantes:**

- El tiempo máximo se cuenta desde el encendido real del dispositivo.
- Durante la validación se usa el plazo más corto entre la validación y el máximo restante.
- Al alcanzar el máximo no se vuelve a encender mientras el sensor continúe en `on`.
- Un nuevo encendido manual inicia un ciclo completo nuevo.
- Aunque el máximo esté deshabilitado, la ausencia y el apagado físico siguen teniendo prioridad.

**Versiones:**

| Versión | Fecha | Cambios |
|---|---|---|
| 0.2.1 BETA | 2026-09-02 | Horario climático predeterminado complementario: 06:40–17:30 |
| 0.2.0 BETA | 2026-09-02 | Tiempo máximo opcional y límite absoluto desde el encendido |
| 0.1.0 BETA | 2026-09-02 | Primera versión beta |

[![Importar Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/presence_climate/BP_Presencia_Interruptor_Clima.yaml)
🔗 [Ver código fuente](blueprints/automation/presence_climate/BP_Presencia_Interruptor_Clima.yaml)

---

## 🛠 Instalación manual

Si prefieres instalar sin el botón de importación:

1. Descarga el archivo `.yaml` del blueprint que necesitas
2. Cópialo a tu instalación de HA:

```
config/blueprints/automation/switch_light/BP_Multi_Switch_Light.yaml
config/blueprints/automation/door_light/BP_Multi_Door_Light.yaml
config/blueprints/automation/presence_climate/BP_Presencia_Interruptor_Clima.yaml
```

3. En HA: **Configuración → Automatizaciones → Planos → ⋮ → Recargar planos**
4. Crea una nueva automatización desde el plano deseado

---

## 🔍 Logs y trazas en Home Assistant

Los blueprints con logger dedicado se consultan en **Configuración → Registros**.
El blueprint de presencia utiliza las trazas nativas de la automatización:

| Blueprint | Diagnóstico |
|---|---|
| Switch ↔ Light | `blueprint.sync_switch_luz` |
| Door → Light | `blueprint.door_light` |
| Presence → Light / Switch | Trazas de la automatización, sin logger dedicado |

---

## 🤝 Contribuciones

¿Encontraste un bug o tienes una mejora? Abre un **Issue** o un **Pull Request**.
¿Tienes un caso de uso diferente? Escríbenos a admin@evotechltda.com

---

## 📄 Licencia

MIT License — Copyright (c) 2025 EVOTECH LTDA — Eduardo Sánchez Curiel

Se permite el uso, copia y modificación libre con crédito al autor original.

---

<div align="center">

Hecho con ❤️ en Colombia 🇨🇴 por **EVOTECH LTDA**

[www.evotechltda.com](https://www.evotechltda.com) · admin@evotechltda.com

</div>
