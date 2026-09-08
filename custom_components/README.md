# Custom Components de Home Assistant

Catálogo de integraciones personalizadas desarrolladas por EVOTECH LTDA.
Cada integración tiene una carpeta propia con su código, manifiesto,
traducciones, recursos visuales y documentación individual.

| Integración | Versión | Propósito | Documentación |
|---|---:|---|---|
| Dahua Entity Profile | 1.1.0 | Conserva únicamente los tipos de entidad Dahua seleccionados | [Abrir](dahua_entity_profile/README.md) |

[![Instalar Dahua Entity Profile con HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ejscuriel&repository=ha-blueprints&category=integration)

## Regla para futuros componentes

Dentro de una instalación de Home Assistant, cada integración se copia como:

```text
/config/custom_components/<dominio_de_la_integración>/
```

Para distribución mediante HACS, cada nuevo custom component tendrá su propio
repositorio instalable, siguiendo la
[estructura requerida para integraciones](https://www.hacs.xyz/docs/publish/integration/).
Este catálogo servirá como índice común y enlazará cada repositorio. Así HACS
puede actualizar cada integración de manera independiente.

[Volver a la portada](../README.md)
