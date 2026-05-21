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

## ✨ ¿Por qué estos blueprints?

En instalaciones domóticas modernas conviven dispositivos de distintos fabricantes
(Sonoff, Tuya, Zigbee, ESPHome) que necesitan trabajar juntos sin cableado físico.
Estos blueprints cubren los casos más comunes con una sola instancia configurable,
registro detallado en el log y protección ante fallos de conectividad.

**Características comunes a todos los blueprints:**
- ✅ Hasta **10 parejas** de dispositivos en una sola instancia
- ✅ Secciones **plegables** — expande solo lo que necesitas
- ✅ **Protección** ante dispositivos desconectados o no disponibles
- ✅ **Log detallado** con nombre de automatización, número de pareja y causa del fallo
- ✅ Compatible con **WiFi** (Tuya, Sonoff, Shelly) y **Zigbee** (IKEA, Aqara, Sonoff ZB)
- ✅ Requiere Home Assistant **2024.4** o superior

---

## 📦 Blueprints disponibles

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

🔗 [Ver código fuente](blueprints/automation/switch_light/switch_light.yaml)

---

### 🚪 2. Puerta → Luz / Interruptor con Temporización

> **Control automático de iluminación por apertura de puertas con timers configurables**

Vincula sensores de puerta o ventana con luces o interruptores de forma **lógica**.
Al abrir la puerta enciende la luz; al cerrarla la mantiene encendida un tiempo
adicional antes de apagarla — como un interruptor automático de escalera o pasillo,
pero totalmente configurable por pareja.

Ideal para **entradas, pasillos, closets, bodegas, baños y garajes**.

**Comportamiento:**
| Evento | Resultado |
|---|---|
| Puerta `ABRE` | Enciende la luz. Timer de apertura activo si ≠ -1 |
| Tiempo apertura vence (puerta aún abierta) | Apaga la luz automáticamente |
| Puerta `CIERRA` | Inicia timer de cierre si ≠ -1 |
| Tiempo cierre vence | Apaga la luz automáticamente |
| Switch `ON` manual + puerta **abierta** | Reinicia el timer de apertura como si la puerta se abriera |
| Switch `ON` manual + puerta **cerrada** | Aplica timer específico `t_mc` (parámetro independiente) |
| Cualquier tiempo = `-1` | Encendido **indefinido**, sin apagado automático |

**Parámetros configurables:**
| Parámetro | Descripción | Por defecto |
|---|---|---|
| Tiempo puerta abierta | Segundos encendida con puerta abierta (-1 = ilimitado) | 300 s |
| Tiempo tras cierre | Segundos encendida tras cerrar (-1 = ilimitado) | 60 s |
| Tiempo switch manual + puerta cerrada | Timer cuando se enciende manualmente con puerta cerrada (-1 = ilimitado) | 120 s |
| Pareja N → Sensor | Binary sensor de puerta/ventana/apertura | — |
| Pareja N → Luz/Switch | Target (acepta light.* y switch.*) | — |
| Pareja N → Tiempo apertura | Individual (0 = usar defecto, -1 = ilimitado) | 0 |
| Pareja N → Tiempo cierre | Individual (0 = usar defecto, -1 = ilimitado) | 0 |
| Pareja N → Tiempo manual cerrada | Timer cuando switch se activa manualmente con puerta cerrada (0 = defecto, -1 = ilimitado) | 0 |

**Log de seguimiento** (`blueprint.puerta_luz`):
```
INFO  [Entrada principal] Pareja 1 — Puerta ABIERTA → Luz encendida. Tiempo máximo: 300s
INFO  [Entrada principal] Pareja 1 — Puerta CERRADA. Apagado programado en: 60s
INFO  [Entrada principal] Pareja 1 — Tiempo tras cierre agotado (60s) → Luz apagada
INFO  [Entrada principal] Pareja 1 — Timer cancelado: la puerta volvió a abrirse
WARN  [Entrada principal] Pareja 1 — OMITIDO: Sensor no disponible (unavailable)
      Acción requerida: revisar batería o conectividad del sensor.
```

**Versiones:**
| Versión | Fecha | Cambios |
|---|---|---|
| 1.1.0 | 2025-05-20 | Nuevo parámetro: tiempo switch manual + puerta cerrada |
| 1.0.0 | 2025-05-20 | Versión inicial: 10 parejas, temporización y logging |

[![Importar Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/door_light/BP_Multi_Door_Light.yaml)

🔗 [Ver código fuente](blueprints/automation/door_light/door_light.yaml)

---

## 🛠 Instalación manual

Si prefieres instalar sin el botón de importación:

1. Descarga el archivo `.yaml` del blueprint que necesitas
2. Cópialo a tu instalación de HA en la ruta correspondiente:

```
# Blueprint 1 — Interruptores con luces
config/blueprints/automation/switch_light/switch_light.yaml

# Blueprint 2 — Puertas con luces
config/blueprints/automation/door_light/door_light.yaml
```

3. En HA: **Configuración → Automatizaciones → Planos → ⋮ → Recargar planos**
4. Crea una nueva automatización desde el plano deseado

---

## 🔍 Ver logs en Home Assistant

Los eventos quedan registrados en **Configuración → Registros**.
Filtra por el logger de cada blueprint:

| Blueprint | Logger |
|---|---|
| Interruptores ↔ Luces | `blueprint.sync_switch_luz` |
| Puertas → Luces | `blueprint.puerta_luz` |

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
