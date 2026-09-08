"""Button platform for Dahua Entity Profile."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import DEFAULT_KEEP_NAMES, DEFAULT_PLATFORM, DOMAIN, async_apply_profile


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the manual profile button."""
    async_add_entities([DahuaApplyProfileButton(entry)])


class DahuaApplyProfileButton(ButtonEntity):
    """Button that applies the default Dahua entity profile."""

    _attr_has_entity_name = True
    _attr_translation_key = "apply_profile"
    _attr_icon = "mdi:filter-cog"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the button."""
        self._attr_unique_id = f"{entry.entry_id}_apply_profile"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Dahua Entity Profile",
            manufacturer="EVOTECH LTDA",
            model="Entity Registry Profile",
        )

    async def async_press(self) -> None:
        """Apply the default profile."""
        await async_apply_profile(
            self.hass,
            platform=DEFAULT_PLATFORM,
            keep_names=DEFAULT_KEEP_NAMES,
            reload_integrations=True,
            notify=True,
        )
