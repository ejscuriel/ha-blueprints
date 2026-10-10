# Acciones opcionales en puerta, presencia e interruptor/luz

Actualización del 10 de octubre de 2026.

## Versiones

| Blueprint | Versión anterior | Versión nueva |
|---|---:|---:|
| Puerta → Luz / Interruptor — una pareja | 3.0.0 | 3.1.0 |
| Presencia + Interruptor con horario, clima y temporizadores | 0.2.1 BETA | 0.3.0 BETA |
| Interruptor ↔ Luz — una pareja | 2.0.0 | 2.1.0 |

## Configuración

En cada automatización abre **🧩 Acciones opcionales (avanzado)**:

1. Configura **Acciones adicionales** con el editor visual de Home Assistant.
2. En **Cuándo ejecutar las acciones adicionales**, selecciona encendido, apagado o ambos.
3. Activa **Ejecutar acciones adicionales** y guarda.

El check empieza desactivado, el bloque de acciones vacío y el evento propuesto
es encendido. Configurar acciones o marcar eventos NO activa el check. Desmarcarlo
suspende el bloque sin borrar su configuración. Sin eventos seleccionados o sin
acciones configuradas, no se realiza ninguna acción adicional.

| Campo interno | Valor predeterminado |
|---|---|
| `habilitar_acciones_adicionales` | `false` |
| `acciones_adicionales` | `[]` |
| `ejecutar_acciones_adicionales_en` | Encendido del dispositivo o pareja |

Se ejecuta el mismo bloque en cada evento elegido. Para acciones distintas al
encender y apagar, usa un bloque visual **Elegir** que compruebe el estado del
dispositivo, o crea un script con esa lógica.

## Momento de ejecución

| Blueprint | Encendido | Apagado |
|---|---|---|
| Puerta | Transición real de la carga de `off` a `on`, sea automática o manual. | Transición real de la carga de `on` a `off`, sea por temporizador o externa. |
| Presencia | Transición real de la carga de `off` a `on`, sea automática o manual. | Transición real de la carga de `on` a `off`, sea por ausencia, máximo, validación o externa. |
| Interruptor ↔ Luz | Cuando ambos extremos pasan a estar encendidos. | Cuando ambos extremos pasan a estar apagados. |

En puerta y presencia, abrir/cerrar la puerta o detectar presencia sin cambio
real de la carga no repite las acciones adicionales. Recuperar la carga desde
`unknown`/`unavailable` tampoco ejecuta el bloque; el control original conserva
su propio tratamiento de esos estados.

En interruptor/luz se observa el resultado de la sincronización, no cada uno de
los dos cambios por separado. Esto evita duplicar el bloque por el eco normal
entre entidades. Si una entidad no responde y la pareja no queda sincronizada,
no hay evento adicional. Recuperar una entidad puede generar este evento cuando
ambas vuelven a quedar en el mismo estado válido; no se dan órdenes nuevas de
sincronización por esa recuperación.

## Compatibilidad con automatizaciones existentes

Se conservan las rutas de archivos y `source_url`, los nombres del blueprint y
de sus inputs anteriores, sus selectores y valores predeterminados, las condiciones,
las órdenes, los tiempos y los modos de ejecución. Los tres campos nuevos tienen
valores predeterminados: las automatizaciones ya creadas no necesitan incorporarlos
manualmente ni recrearse. Se mantiene el requisito mínimo declarado en estos
archivos, Home Assistant 2026.1.0.

Con el check desactivado:

- Puerta y presencia usan la secuencia original completa, sin abrir las ramas de
  acciones adicionales.
- Interruptor/luz conserva su secuencia de sincronización; omite el bloque añadido.
- Los disparadores nuevos de apagado en presencia y pareja sincronizada en
  interruptor/luz permanecen deshabilitados.
- No se requieren helpers, otras automatizaciones ni scripts externos.

La implementación conserva `mode: restart` en puerta e interruptor/luz y
`mode: parallel`, `max: 5` en presencia.

## Temporizadores, reinicios y errores al activar la extensión

En puerta y presencia se usa un bloque paralelo **solo cuando corresponde un
evento adicional habilitado**. Una rama conserva el control original y otra
ejecuta las acciones del usuario. Así, una espera del bloque adicional no se
inserta antes de la validación, la espera de ausencia ni el temporizador de apagado.
No se añade otra automatización.

En interruptor/luz las acciones adicionales siguen al control original, en una
ejecución propia del evento de pareja sincronizada. No se añade un bloque paralelo.

Se conserva el reinicio de la ejecución en puerta e interruptor/luz: un nuevo
evento puede cancelar acciones adicionales que aún estén esperando. En presencia,
el bloque adicional puede continuar después del apagado y mantiene ocupada una
ejecución hasta terminar; las ejecuciones siguen limitadas a cinco. Para trabajos
largos, utiliza `script.turn_on` dentro del editor de acciones: inicia un script
sin esperar a que termine.

Los errores de ejecución manejables del bloque adicional usan
`continue_on_error: true`; en puerta y presencia el control está además en una
rama separada. Esto no vuelve válido un YAML mal formado, una plantilla rota ni
una configuración que Home Assistant rechace al cargar.

Las acciones configuradas por el usuario sí pueden modificar dispositivos.
Evita controlar desde ellas la misma carga o los sensores de entrada si no buscas
crear nuevos eventos de encendido/apagado. El check desactivado conserva el
comportamiento anterior; activarlo permite los efectos elegidos expresamente.

## Actualización en Home Assistant

1. En **Ajustes → Automatizaciones y escenas → Blueprints**, abre el menú del
   blueprint existente y utiliza **Reimportar blueprint**.
2. Conserva el blueprint y las automatizaciones existentes; no crees otra copia
   con una ruta diferente. Todas las automatizaciones que lo usan comparten esa
   definición.
3. Comprueba la versión en la descripción. El check nuevo debe aparecer apagado.
4. Si tu instalación no refleja el cambio, recarga las automatizaciones. Hazlo
   cuando no haya un ciclo que necesites conservar: una recarga puede interrumpir
   esperas en curso.
5. Activa la extensión solo en las automatizaciones donde quieras usarla.

Actualizar GitHub no actualiza automáticamente la copia local de Home Assistant.

## Verificación de esta entrega

Se comprobó el análisis sintáctico YAML, la resolución de `!input`, los valores
predeterminados de los campos nuevos y la comparación estructural del control
original frente a la versión anterior de GitHub
(`070fc5e4084792f890848c8d5b01fbe2f245e561`).

La comprobación de regresión verifica que los inputs anteriores, disparadores
originales, condiciones, acciones de control y modos de ejecución se mantienen,
y que los disparadores nuevos no se habilitan por defecto. Se verificaron los
casos de check apagado, selección vacía, encendido y apagado seleccionados.

Esta es una validación estática del código; no se ejecutó en la instalación de
Home Assistant ni se accionaron dispositivos físicos.

## Referencias

- [Esquema y valores predeterminados de blueprints](https://www.home-assistant.io/docs/blueprint/schema/)
- [Selectores de acciones y booleanos](https://www.home-assistant.io/docs/blueprint/selectors/)
- [Bloques de acciones, paralelo y errores](https://www.home-assistant.io/docs/scripts/)
