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


## Acciones opcionales — versión 2.1.0

La sección **🧩 Acciones opcionales (avanzado)** incluye:

- **Ejecutar acciones adicionales:** check desactivado por defecto.
- **Acciones adicionales:** editor visual, vacío por defecto.
- **Cuándo ejecutar las acciones adicionales:** encendido, apagado o ambos;
  propone encendido, pero no se ejecuta hasta activar el check.

El bloque se ejecuta cuando ambos extremos quedan sincronizados en el estado
seleccionado, evitando duplicarlo por el eco entre interruptor y luz. También
puede ejecutarse al recuperar una entidad si la pareja vuelve a coincidir.

Las automatizaciones existentes conservan sus inputs y funcionamiento con el
check apagado. Reimporta el blueprint en su misma ruta; no necesitas recrearlas.

[Guía completa: actualización, eventos, temporizadores y límites](../../../docs/acciones_opcionales.md).

[Ver YAML](BP_Switch_Light.yaml) · [Volver al catálogo](../../README.md)
