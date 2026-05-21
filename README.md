# 🏠 Home Assistant Blueprints — EVOTECH LTDA

Colección de blueprints para Home Assistant desarrollados por **EVOTECH LTDA**.

> **Autor:** Eduardo Sánchez Curiel  
> **País:** Colombia 🇨🇴  
> **Web:** [www.evotechltda.com](https://www.evotechltda.com)  
> **Contacto:** admin@evotechltda.com  
> **Licencia:** MIT — libre uso con crédito al autor  

---

## 📦 Blueprints disponibles

---

### 💡 Vincular Interruptores con Luces (hasta 10 parejas)

En muchas instalaciones domóticas modernas conviven interruptores WiFi o Zigbee
con tiras LED controladas por un controlador WiFi independiente. Aunque físicamente
el interruptor **no está cableado** a la tira LED, con este blueprint logramos
una sincronización **lógica** bidireccional: el interruptor actúa como si estuviera
directamente conectado a la luz, y viceversa.

Es ideal cuando tienes varios de estos casos repartidos por la casa — sala, cuarto,
cocina, pasillo — y no quieres crear una automatización separada para cada uno.
Con una sola instancia de este blueprint gestionas hasta **10 parejas** interruptor↔luz,
cada una con sus propios ajustes de brillo y temperatura de color.

**¿Qué hace?**
- Interruptor `ON/OFF` → enciende/apaga la tira LED con brillo y temperatura definidos
- Tira LED `ON/OFF` → enciende/apaga el interruptor para mantener ambos sincronizados
- Compatible con interruptores **WiFi** (Sonoff, Tuya, Shelly) y **Zigbee** (IKEA, Aqara, Sonoff ZB)
- Compatible con controladores LED **WiFi CCT** (temperatura de color fría/cálida)
- Cada pareja puede tener su propio brillo y temperatura, o usar los valores globales por defecto
- Protección ante dispositivos desconectados o no disponibles
- Registro detallado en el log de HA con nombre de automatización y número de pareja

**Requisitos**
- Home Assistant **2024.4** o superior
- Dispositivos integrados nativamente en HA (eWeLink, Tuya, MQTT, ESPHome, etc.)

**Importar directamente en Home Assistant:**

[![Importar Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/sync_switch_luz/blueprint_multi_switch_luz.yaml)

> Enlace directo al archivo raw en GitHub.

**Configuración**

| Parámetro | Descripción | Por defecto |
|---|---|---|
| Brillo por defecto | % de brillo al encender (1–100) | 55% |
| Temperatura por defecto | Kelvin: 2700 cálido · 6500 frío | 6500 K |
| Pareja N → Interruptor | Entity ID del switch | — |
| Pareja N → Luz | Entity ID de la luz | — |
| Pareja N → Brillo | Brillo individual (0 = usar defecto) | 0 |
| Pareja N → Temperatura | Temperatura individual (0 = usar defecto) | 0 |

**Log de seguimiento**

Los eventos quedan registrados bajo el logger `blueprint.sync_switch_luz`:

```
INFO  [Sala principal] Pareja 1 — Switch→Luz:
      'switch.sonoff_sala' → ON → 'light.led_sala' encendida (brillo=55%, CT=6500K)

WARN  [Sala principal] Pareja 1 — OMITIDO Switch→Luz:
      'light.led_sala' no disponible. Verifica la conexión del dispositivo.
```

**Versiones**

| Versión | Fecha | Cambios |
|---|---|---|
| 1.2.0 | 2025-05-20 | Logs con nombre de automatización y nº de pareja |
| 1.1.0 | 2025-05-20 | Ampliado a 10 parejas |
| 1.0.0 | 2025-05-20 | Versión inicial |

---

## 🛠 Instalación manual

Si prefieres instalar sin el botón de importación:

1. Descarga el archivo `blueprint.yaml`
2. Cópialo a tu carpeta de HA:
```
config/blueprints/automation/sync_switch_luz/blueprint_multi_switch_luz.yaml
```
3. En HA: **Configuración → Automatizaciones → Planos → ⋮ → Recargar planos**
4. Crea una nueva automatización desde el plano

---

## 📄 Licencia

MIT License — Copyright (c) 2025 EVOTECH LTDA — Eduardo Sánchez Curiel

Se permite el uso, copia y modificación libre con crédito al autor original.
