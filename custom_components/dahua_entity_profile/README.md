# Dahua Entity Profile

Servicio local para aplicar manualmente una lista blanca al registro de
entidades de la integración Dahua. No elimina entidades ni cambia la
configuración interna de las cámaras.

## Instalación nueva mediante HACS

[![Abrir el repositorio en HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ejscuriel&repository=ha-blueprints&category=integration)

1. Usar el botón anterior o, en HACS, agregar
   `https://github.com/ejscuriel/ha-blueprints` como repositorio personalizado
   de tipo **Integración**.
2. Instalar **Dahua Entity Profile** y reiniciar Home Assistant.
3. Abrir **Configuración → Dispositivos y servicios → Añadir integración**.
4. Buscar **Dahua Entity Profile**, seleccionar los tipos de entidad que se
   conservarán y completar la instalación.
5. En el dispositivo creado, pulsar **Aplicar perfil mínimo de entidades** cada
   vez que se agregue una cámara Dahua.

No se edita `configuration.yaml`, no se necesita token y no es obligatorio crear
una automatización. La acción `dahua_entity_profile.apply` queda disponible para
usuarios que prefieran llamarla desde una automatización manual.

La selección puede modificarse después desde **Configuración → Dispositivos y
servicios → Perfil de entidades Dahua → Configurar**. La lista muestra los tipos
detectados en las cámaras Dahua instaladas. Por defecto conserva `Main`, `Sub`,
`Motion Alarm`, `Smart Motion Human`, `Motion Detection`,
`Smart Motion Detection` y `Reboot`.

Cambiar la selección no modifica inmediatamente el registro. El nuevo perfil se
aplica únicamente cuando se pulsa el botón o se llama la acción. Si la acción no
incluye `keep_names`, utiliza automáticamente la selección guardada.

También se admite instalación manual copiando la carpeta
`custom_components/dahua_entity_profile`, reiniciando Home Assistant y añadiendo
la integración desde la interfaz.

## Comportamiento

- Recorre solo las entidades cuya plataforma coincide con `platform`.
- Habilita las entidades cuyos nombres originales coinciden con `keep_names`.
- Deshabilita las demás mediante `RegistryEntryDisabler.USER`.
- No vuelve a escribir entidades que ya tienen el estado correcto.
- Recarga en serie solamente las entradas de configuración modificadas.
- Continúa ante errores individuales y publica un resumen final en el log y en
  una notificación persistente.
- Usa un bloqueo interno para impedir dos ejecuciones simultáneas.

La operación es idempotente y puede repetirse después de agregar cada cámara.

[Volver al catálogo de Custom Components](../README.md)
