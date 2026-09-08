<div align="center">

# 🏠 Home Assistant — EVOTECH LTDA

[![HA Version](https://img.shields.io/badge/Home%20Assistant-2026.1%2B-blue?logo=homeassistant)](https://www.home-assistant.io/)
[![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-green)](#licencia)
[![Colombia](https://img.shields.io/badge/País-Colombia%20🇨🇴-yellow)]()
[![Web](https://img.shields.io/badge/Web-evotechltda.com-orange)](https://www.evotechltda.com)

**Soluciones reutilizables para desplegar y mantener instalaciones de Home
Assistant de forma clara, segura y repetible.**

Desarrolladas por **Eduardo Sánchez Curiel — EVOTECH LTDA**

📧 admin@evotechltda.com · 🌐 www.evotechltda.com

</div>

---

## Catálogo

| Familia | Introducción | Organización |
|---|---|---|
| 📐 Blueprints | [Abrir catálogo](blueprints/README.md) | Una carpeta por blueprint, con YAML y documentación propia |
| 🧩 Custom Components | [Abrir catálogo](custom_components/README.md) | Una carpeta por integración, con código y documentación propia |

Integración disponible actualmente:
[**Dahua Entity Profile 1.1.0**](https://github.com/ejscuriel/ha-dahua-entity-profile).

## Estructura

```text
ha-blueprints/
├── README.md
├── blueprints/
│   ├── README.md
│   └── automation/
│       └── <blueprint>/
│           ├── README.md
│           └── <blueprint>.yaml
└── custom_components/
    ├── README.md
    └── <integración>/
        ├── README.md
        ├── manifest.json
        └── código y recursos
```

Las rutas `blueprints/` y `custom_components/` son intencionales: corresponden
a las estructuras reconocidas por Home Assistant y HACS. Los enlaces actuales
de importación e instalación se mantienen estables.

## Instalación

### Blueprints

1. Abrir el [catálogo de blueprints](blueprints/README.md).
2. Entrar en la carpeta de la solución deseada.
3. Usar su botón **Importar Blueprint**.
4. Crear una automatización independiente por habitación, zona, pareja o unidad.

### Custom Components

1. Abrir el [catálogo de integraciones](custom_components/README.md).
2. Entrar en la documentación de la integración deseada.
3. Seguir su instalación mediante HACS o el procedimiento manual documentado.

> [HACS administra una integración personalizada por repositorio](https://www.hacs.xyz/docs/publish/integration/).
> Cuando se
> desarrollen nuevos custom components, cada uno tendrá un repositorio instalable
> independiente; este catálogo común conservará los enlaces y la introducción de
> toda la familia.

## Criterios de trabajo

- Documentación junto al código de cada solución.
- Una automatización independiente por pareja, zona o unidad cuando corresponda.
- Manejo explícito de estados `unknown` y `unavailable`.
- Registro de excepciones y resultados para facilitar el diagnóstico.
- Valores predeterminados seguros para instalaciones nuevas.
- GitHub `main` como fuente canónica de publicación.

## Licencia

MIT License — Copyright (c) 2025–2026 EVOTECH LTDA — Eduardo Sánchez Curiel.

Se permite el uso, copia y modificación libre con crédito al autor original.

---

<div align="center">

Hecho con ❤️ en Colombia 🇨🇴 por **EVOTECH LTDA**

[www.evotechltda.com](https://www.evotechltda.com) · admin@evotechltda.com

</div>
