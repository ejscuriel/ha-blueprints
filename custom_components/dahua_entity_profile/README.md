# Dahua Entity Profile

Servicio local para aplicar manualmente una lista blanca al registro de
entidades de la integración Dahua. No elimina entidades ni cambia la
configuración interna de las cámaras.

## Instalación nueva mediante HACS

1. En HACS, agregar `https://github.com/ejscuriel/ha-blueprints` como repositorio
   personalizado de tipo **Integración**.
2. Instalar **Dahua Entity Profile** y reiniciar Home Assistant.
3. Abrir **Configuración → Dispositivos y servicios → Añadir integración**.
4. Buscar **Dahua Entity Profile** y completar su único paso.
5. En el dispositivo creado, pulsar **Aplicar perfil mínimo de entidades** cada
   vez que se agregue una cámara Dahua.

No se edita `configuration.yaml`, no se necesita token y no es obligatorio crear
una automatización. La acción `dahua_entity_profile.apply` queda disponible para
usuarios que prefieran llamarla desde una automatización manual.

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
