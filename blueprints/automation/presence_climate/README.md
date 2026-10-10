# Presencia + horario + clima

Controla una luz, interruptor o relé según presencia, horario y condiciones
meteorológicas. Incluye validación inicial, espera de ausencia y tiempo máximo
opcional.

> Estado: **0.3.0 BETA**. Probar primero en una sola zona.

[![Importar Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/ejscuriel/ha-blueprints/main/blueprints/automation/presence_climate/BP_Presencia_Interruptor_Clima.yaml)

## Valores predeterminados

- Validación inicial: 5 segundos.
- Ausencia antes de apagar: 5 segundos.
- Tiempo máximo: 5 minutos, activado.
- Horario normal: 17:30–06:40.
- Horario condicionado por clima: 06:40–17:30.

## Instalación

1. Importar el blueprint.
2. Crear una automatización para una zona.
3. Seleccionar presencia, carga y entidad meteorológica.
4. Revisar las trazas durante la prueba controlada.


## Acciones opcionales — versión 0.3.0 BETA

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

[Ver YAML](BP_Presencia_Interruptor_Clima.yaml) · [Volver al catálogo](../../README.md)
