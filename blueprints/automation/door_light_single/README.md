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


## Acciones opcionales — versión 3.1.0

La sección **🧩 Acciones opcionales (avanzado)** incluye:

- **Ejecutar acciones adicionales:** check desactivado por defecto.
- **Acciones adicionales:** editor visual, vacío por defecto.
- **Cuándo ejecutar las acciones adicionales:** encendido, apagado o ambos;
  propone encendido, pero no se ejecuta hasta activar el check.

El bloque se ejecuta con el cambio real de la carga, automático o manual. Se
separa del control de tiempos para que una espera adicional no retrase el
apagado. La recuperación desde unknown/unavailable no ejecuta el bloque.

Las automatizaciones existentes conservan sus inputs y funcionamiento con el
check apagado. Reimporta el blueprint en su misma ruta; no necesitas recrearlas.

[Guía completa: actualización, eventos, temporizadores y límites](../../../docs/acciones_opcionales.md).

[Ver YAML](BP_Door_Light.yaml) · [Volver al catálogo](../../README.md)
