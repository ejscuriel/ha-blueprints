"""Config flow for Dahua Entity Profile."""

from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult

from . import DOMAIN


class DahuaEntityProfileConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Dahua Entity Profile."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial setup step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="Dahua Entity Profile", data={})

        return self.async_show_form(step_id="user")
