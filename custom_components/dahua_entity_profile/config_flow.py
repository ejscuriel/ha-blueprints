"""Config flow for Dahua Entity Profile."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlowResult,
    OptionsFlowWithReload,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from . import ATTR_KEEP_NAMES, DEFAULT_KEEP_NAMES, DEFAULT_PLATFORM, DOMAIN


def _remove_shared_name_prefix(names: list[str]) -> list[str]:
    """Remove a device-name prefix shared by all entities in one config entry."""
    if len(names) < 2:
        return names

    tokenized = [name.split() for name in names]
    shared_count = 0
    for tokens in zip(*tokenized, strict=False):
        if len({token.casefold() for token in tokens}) != 1:
            break
        shared_count += 1

    if shared_count == 0 or any(len(tokens) == shared_count for tokens in tokenized):
        return names
    return [" ".join(tokens[shared_count:]) for tokens in tokenized]


def _available_profile_names(
    hass: HomeAssistant,
    selected_names: list[str] | tuple[str, ...],
) -> list[str]:
    """Build reusable entity-type names from the installed Dahua entries."""
    candidates = {
        name.casefold(): name for name in (*DEFAULT_KEEP_NAMES, *selected_names)
    }
    grouped_names: dict[str, list[str]] = defaultdict(list)
    registry = er.async_get(hass)

    for entity_entry in registry.entities.values():
        if (
            entity_entry.platform != DEFAULT_PLATFORM
            or not entity_entry.config_entry_id
            or not entity_entry.original_name
        ):
            continue
        grouped_names[entity_entry.config_entry_id].append(entity_entry.original_name)

    for names in grouped_names.values():
        for profile_name in _remove_shared_name_prefix(names):
            cleaned_name = profile_name.strip()
            if cleaned_name:
                candidates.setdefault(cleaned_name.casefold(), cleaned_name)

    return sorted(candidates.values(), key=str.casefold)


def _selection_schema(hass: HomeAssistant, selected_names: list[str]) -> vol.Schema:
    """Build the multi-select schema with the available entity types."""
    return vol.Schema(
        {
            vol.Required(ATTR_KEEP_NAMES, default=selected_names): SelectSelector(
                SelectSelectorConfig(
                    options=_available_profile_names(hass, selected_names),
                    multiple=True,
                    mode=SelectSelectorMode.DROPDOWN,
                )
            )
        }
    )


class DahuaEntityProfileConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Dahua Entity Profile."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> DahuaEntityProfileOptionsFlow:
        """Create the options flow."""
        return DahuaEntityProfileOptionsFlow()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial setup step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        errors: dict[str, str] = {}
        if user_input is not None:
            selected_names = user_input[ATTR_KEEP_NAMES]
            if selected_names:
                return self.async_create_entry(
                    title="Dahua Entity Profile",
                    data={ATTR_KEEP_NAMES: selected_names},
                )
            errors["base"] = "empty_selection"

        return self.async_show_form(
            step_id="user",
            data_schema=_selection_schema(self.hass, list(DEFAULT_KEEP_NAMES)),
            errors=errors,
        )


class DahuaEntityProfileOptionsFlow(OptionsFlowWithReload):
    """Let the user choose which Dahua entity types remain enabled."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the retained entity types."""
        errors: dict[str, str] = {}
        if user_input is not None:
            selected_names = user_input[ATTR_KEEP_NAMES]
            if selected_names:
                return self.async_create_entry(
                    title="",
                    data={ATTR_KEEP_NAMES: selected_names},
                )
            errors["base"] = "empty_selection"

        selected_names = list(
            self.config_entry.options.get(
                ATTR_KEEP_NAMES,
                self.config_entry.data.get(ATTR_KEEP_NAMES, DEFAULT_KEEP_NAMES),
            )
        )
        return self.async_show_form(
            step_id="init",
            data_schema=_selection_schema(self.hass, selected_names),
            errors=errors,
        )
