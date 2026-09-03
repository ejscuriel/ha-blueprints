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
```

Para actualizar un blueprint ya importado, vuelve a importarlo desde su misma URL
y recarga las automatizaciones que lo utilizan.

---

## 🔍 Diagnóstico

Los tres blueprints recomendados usan las **trazas nativas de cada
automatización**. En Home Assistant abre la automatización concreta y selecciona
**Trazas**. Al existir una instancia por pareja, la traza muestra directamente
qué habitación y qué temporizador produjeron el resultado.

Los estados `unknown` y `unavailable` no se convierten en órdenes de encendido o
apagado. Esto evita sincronizaciones no deseadas después de una desconexión o
del reinicio de Home Assistant.

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
