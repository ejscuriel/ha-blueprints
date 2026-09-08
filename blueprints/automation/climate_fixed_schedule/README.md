# Aire acondicionado — perfil obligatorio y hasta 5 horarios

Normaliza la configuración de una unidad de aire acondicionado sin importar el
método o modo usado para encenderla. Cada unidad utiliza una automatización
independiente.

[![Importar Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/climate_fixed_schedule/BP_Climate_Fixed_Schedule.yaml)

## Funcionamiento

- Un minuto después del encendido aplica el perfil inicial obligatorio.
- Reconoce cualquier modo activo, incluido `dry`.
- Permite hasta cinco perfiles horarios independientes.
- Horas propuestas: 23:00, 00:00, 01:00, 02:00 y 03:00.
- No reenvía un parámetro que ya coincide, salvo que se active su reenvío
  obligatorio para producir el `beep`.
- Si la entidad está `unknown` o `unavailable`, no envía órdenes.
- Al terminar verifica el resultado y registra las excepciones.

## Perfil inicial predeterminado

`cool / 21 °C / low / Bottom / MiddleRight`

Los cinco horarios vienen desactivados. Cada usuario habilita solamente los que
necesite y configura sus valores.

## Instalación

1. Importar el blueprint.
2. Crear una automatización para una sola entidad `climate.*`.
3. Revisar el perfil inicial y habilitar los horarios necesarios.
4. Probar la unidad y revisar las trazas antes de desactivar la automatización
   antigua.

[Ver YAML](BP_Climate_Fixed_Schedule.yaml) · [Volver al catálogo](../../README.md)
