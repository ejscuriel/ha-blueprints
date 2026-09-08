# Interruptor ↔ Luz — una pareja

Sincroniza de forma bidireccional un interruptor y una luz. Cada pareja crea una
automatización independiente, con trazas y reinicios propios.

[![Importar Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/switch_light_single/BP_Switch_Light.yaml)

## Valores predeterminados

- Brillo: 55 %.
- Temperatura de color: 6500 K.
- Estados `unknown` y `unavailable`: no producen acciones cruzadas.
- Modo de ejecución: `restart`.

## Instalación

1. Importar el blueprint con el botón anterior.
2. Crear una automatización desde el blueprint.
3. Seleccionar un interruptor y una luz.
4. Repetir con una automatización distinta para cada pareja.

[Ver YAML](BP_Switch_Light.yaml) · [Volver al catálogo](../../README.md)
