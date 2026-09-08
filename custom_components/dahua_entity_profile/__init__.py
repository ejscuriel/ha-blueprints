"""Manual entity-registry profile for Dahua cameras."""

from __future__ import annotations

import asyncio
import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from homeassistant.helpers import config_validation as cv, entity_registry as er
from homeassistant.helpers.typing import ConfigType

DOMAIN = "dahua_entity_profile"
SERVICE_APPLY = "apply"

ATTR_PLATFORM = "platform"
ATTR_KEEP_NAMES = "keep_names"
ATTR_RELOAD_INTEGRATIONS = "reload_integrations"
ATTR_NOTIFY = "notify"

DEFAULT_PLATFORM = "dahua"
DEFAULT_KEEP_NAMES = (
    "Main",
    "Sub",
    "Motion Alarm",
    "Smart Motion Human",
    "Motion Detection",
    "Smart Motion Detection",
    "Reboot",
)

NOTIFICATION_ID = "dahua_entity_profile_last_run"
PLATFORMS = (Platform.BUTTON,)
_LOGGER = logging.getLogger(__name__)

SERVICE_APPLY_SCHEMA = vol.Schema(
    {
        vol.Optional(ATTR_PLATFORM, default=DEFAULT_PLATFORM): cv.string,
        vol.Optional(ATTR_KEEP_NAMES): vol.All(
            cv.ensure_list, [cv.string]
        ),
        vol.Optional(ATTR_RELOAD_INTEGRATIONS, default=True): cv.boolean,
        vol.Optional(ATTR_NOTIFY, default=True): cv.boolean,
    }
)


def configured_keep_names(entry: ConfigEntry) -> list[str]:
    """Return the profile saved in the config entry, or the defaults."""
    configured = entry.options.get(
        ATTR_KEEP_NAMES,
        entry.data.get(ATTR_KEEP_NAMES, DEFAULT_KEEP_NAMES),
    )
    return [str(name) for name in configured]


def _service_keep_names(hass: HomeAssistant, call: ServiceCall) -> list[str]:
    """Resolve explicit service data before falling back to integration options."""
    if ATTR_KEEP_NAMES in call.data:
        return call.data[ATTR_KEEP_NAMES]

    entries = hass.config_entries.async_entries(DOMAIN)
    if entries:
        return configured_keep_names(entries[0])
    return list(DEFAULT_KEEP_NAMES)


def _is_kept_entity(entry: er.RegistryEntry, keep_names: list[str]) -> bool:
    """Return whether an entity matches one of the retained integration names."""
    source_name = entry.original_name
    if not source_name:
        source_name = entry.entity_id.split(".", maxsplit=1)[-1].replace("_", " ")

    normalized_source = source_name.strip().casefold()
    return any(
        normalized_source == normalized_keep
        or normalized_source.endswith(f" {normalized_keep}")
        for normalized_keep in (name.strip().casefold() for name in keep_names)
        if normalized_keep
    )


async def _async_notify(hass: HomeAssistant, message: str) -> None:
    """Publish one replaceable result notification."""
    await hass.services.async_call(
        "persistent_notification",
        "create",
        {
            "title": "Perfil de entidades Dahua",
            "message": message,
            "notification_id": NOTIFICATION_ID,
        },
        blocking=True,
    )


async def async_apply_profile(
    hass: HomeAssistant,
    *,
    platform: str = DEFAULT_PLATFORM,
    keep_names: list[str] | tuple[str, ...] = DEFAULT_KEEP_NAMES,
    reload_integrations: bool = True,
    notify: bool = True,
) -> None:
    """Apply the allowlist and report a final summary."""
    async with hass.data[DOMAIN]["run_lock"]:
        platform = platform.strip()
        normalized_keep_names = [name.strip() for name in keep_names if name.strip()]

        if not platform:
            raise ServiceValidationError("La plataforma no puede estar vacía.")
        if not normalized_keep_names:
            raise ServiceValidationError(
                "La lista de entidades que se conservarán no puede estar vacía."
            )

        registry = er.async_get(hass)
        platform_entries = [
            entry for entry in registry.entities.values() if entry.platform == platform
        ]
        if not platform_entries:
            raise ServiceValidationError(
                f"No se encontraron entidades de la plataforma '{platform}'."
            )

        desired_enabled = 0
        desired_disabled = 0
        enabled = 0
        disabled = 0
        unchanged = 0
        failures: list[str] = []
        config_entries_to_reload: set[str] = set()

        for entry in platform_entries:
            keep = _is_kept_entity(entry, normalized_keep_names)
            if keep:
                desired_enabled += 1
                if entry.disabled_by is None:
                    unchanged += 1
                    continue
                disabled_by: er.RegistryEntryDisabler | None = None
                action_name = "habilitar"
            else:
                desired_disabled += 1
                if entry.disabled_by is not None:
                    unchanged += 1
                    continue
                disabled_by = er.RegistryEntryDisabler.USER
                action_name = "deshabilitar"

            try:
                registry.async_update_entity(
                    entry.entity_id,
                    disabled_by=disabled_by,
                )
            except Exception as err:  # noqa: BLE001 - continue and report all entries
                failures.append(
                    f"{entry.entity_id}: no se pudo {action_name} ({err})"
                )
                continue

            if keep:
                enabled += 1
            else:
                disabled += 1
            if entry.config_entry_id:
                config_entries_to_reload.add(entry.config_entry_id)

        reloaded = 0
        if reload_integrations:
            for config_entry_id in sorted(config_entries_to_reload):
                try:
                    if await hass.config_entries.async_reload(config_entry_id):
                        reloaded += 1
                    else:
                        failures.append(
                            f"{config_entry_id}: la integración no confirmó la recarga"
                        )
                except Exception as err:  # noqa: BLE001 - report other reloads too
                    failures.append(
                        f"{config_entry_id}: error al recargar la integración ({err})"
                    )

        summary = (
            f"Plataforma: `{platform}`\n\n"
            f"- Entidades encontradas: **{len(platform_entries)}**\n"
            f"- Perfil esperado: **{desired_enabled} habilitadas / "
            f"{desired_disabled} deshabilitadas**\n"
            f"- Habilitadas en esta ejecución: **{enabled}**\n"
            f"- Deshabilitadas en esta ejecución: **{disabled}**\n"
            f"- Sin cambios: **{unchanged}**\n"
            f"- Integraciones recargadas: **{reloaded}**\n"
            f"- Errores: **{len(failures)}**"
        )
        if failures:
            summary = f"{summary}\n\n" + "\n".join(
                f"- `{failure}`" for failure in failures
            )

        if failures:
            _LOGGER.error("Perfil Dahua terminó con errores:\n%s", summary)
        else:
            _LOGGER.info("Perfil Dahua aplicado correctamente:\n%s", summary)

        if notify:
            try:
                await _async_notify(hass, summary)
            except Exception as err:  # noqa: BLE001 - preserve the main result
                _LOGGER.error("No se pudo crear la notificación final: %s", err)

        if failures:
            raise HomeAssistantError(
                "El perfil Dahua terminó con errores; revisa la notificación y el log."
            )


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Dahua entity-profile integration and service."""
    hass.data.setdefault(DOMAIN, {"run_lock": asyncio.Lock()})

    async def async_handle_apply(call: ServiceCall) -> None:
        """Handle a service request."""
        await async_apply_profile(
            hass,
            platform=call.data[ATTR_PLATFORM],
            keep_names=_service_keep_names(hass, call),
            reload_integrations=call.data[ATTR_RELOAD_INTEGRATIONS],
            notify=call.data[ATTR_NOTIFY],
        )

    hass.services.async_register(
        DOMAIN,
        SERVICE_APPLY,
        async_handle_apply,
        schema=SERVICE_APPLY_SCHEMA,
    )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Dahua Entity Profile from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Dahua Entity Profile config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
