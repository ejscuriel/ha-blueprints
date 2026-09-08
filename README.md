<div align="center">

# 📐 Home Assistant Blueprints — EVOTECH LTDA

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2026.1%2B-blue?logo=homeassistant)](https://www.home-assistant.io/)
[![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-green)](#licencia)
[![Web](https://img.shields.io/badge/Web-evotechltda.com-orange)](https://www.evotechltda.com)

Colección de automatizaciones reutilizables para instalaciones nuevas de Home
Assistant.

Desarrolladas por **Eduardo Sánchez Curiel — EVOTECH LTDA**.

</div>

## Catálogo

[Abrir la introducción y el catálogo completo de blueprints](blueprints/README.md).

| Blueprint recomendado | Versión | Documentación |
|---|---:|---|
| Interruptor ↔ Luz — una pareja | 2.0.0 | [Abrir](blueprints/automation/switch_light_single/README.md) |
| Puerta → Luz / Interruptor — una pareja | 3.0.0 | [Abrir](blueprints/automation/door_light_single/README.md) |
| Presencia + horario + clima | 0.2.1 BETA | [Abrir](blueprints/automation/presence_climate/README.md) |
| Aire acondicionado — perfil y horarios | 1.4.1 | [Abrir](blueprints/automation/climate_fixed_schedule/README.md) |

## Estructura

```text
ha-blueprints/
├── README.md
└── blueprints/
    ├── README.md
    └── automation/
        └── <blueprint>/
            ├── README.md
            └── <blueprint>.yaml
```

Cada blueprint se importa una sola vez. Después se crea una automatización
independiente por habitación, pareja, zona o unidad.

## Otras colecciones

- [Catálogo principal de Home Assistant](https://github.com/ejscuriel/home-assistant)
- [Custom Components](https://github.com/ejscuriel/ha-custom-components)

El código de las integraciones personalizadas no se duplica en este repositorio.

## Licencia

MIT License — Copyright (c) 2025–2026 EVOTECH LTDA — Eduardo Sánchez Curiel.

Se permite el uso, copia y modificación libre con crédito al autor original.
