# Blueprints de Home Assistant

Catálogo de automatizaciones reutilizables desarrolladas por EVOTECH LTDA.
Cada blueprint vive en su propia carpeta y contiene su archivo YAML junto con
un `README.md` dedicado.

El blueprint se importa una sola vez en Home Assistant. Después se crea una
automatización independiente por habitación, pareja, zona o unidad.

## Recomendados

| Blueprint | Versión | Documentación | Estado |
|---|---:|---|---|
| Interruptor ↔ Luz — una pareja | 2.0.0 | [Abrir](automation/switch_light_single/README.md) | Recomendado |
| Puerta → Luz / Interruptor — una pareja | 3.0.0 | [Abrir](automation/door_light_single/README.md) | Recomendado |
| Presencia + horario + clima | 0.2.1 BETA | [Abrir](automation/presence_climate/README.md) | Beta controlada |
| Aire acondicionado — perfil y horarios | 1.4.1 | [Abrir](automation/climate_fixed_schedule/README.md) | Recomendado |

## Heredados

| Blueprint | Versión | Documentación |
|---|---:|---|
| Interruptores ↔ luces — hasta 10 parejas | 1.2.0 | [Abrir](automation/switch_light/README.md) |
| Puertas → luces — hasta 10 parejas | 2.1.0 | [Abrir](automation/door_light/README.md) |

Las versiones heredadas se mantienen para instalaciones existentes. Para una
instalación nueva se recomiendan las variantes de una sola pareja, porque sus
trazas, temporizadores y reinicios son independientes.

[Volver a la portada](../README.md)
