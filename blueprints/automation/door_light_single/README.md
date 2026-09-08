# Puerta → Luz / Interruptor — una pareja

Controla una luz, interruptor o relé mediante un sensor de puerta. Maneja tiempos
independientes para puerta abierta, puerta cerrada y encendido manual.

[![Importar Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/door_light_single/BP_Door_Light.yaml)

## Reglas de tiempo

- `-1`: encendido ilimitado.
- `0`: apagado inmediato.
- `1…3600`: espera en segundos antes de apagar.
- El apagado físico o externo cancela el temporizador activo.

## Instalación

1. Importar el blueprint.
2. Crear una automatización para una sola puerta y una sola carga.
3. Configurar los tres tiempos.
4. Crear otra automatización para cada nueva pareja.

[Ver YAML](BP_Door_Light.yaml) · [Volver al catálogo](../../README.md)
