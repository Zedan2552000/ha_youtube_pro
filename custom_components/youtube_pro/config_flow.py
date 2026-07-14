import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import os

from .const import DOMAIN, CONF_COOKIE_PATH, DEFAULT_COOKIE_PATH

class YouTubeProConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for YouTube Pro."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            cookie_path = self.hass.config.path(user_input[CONF_COOKIE_PATH].replace("/config/", ""))
            if not os.path.exists(cookie_path):
                errors["base"] = "invalid_path"
            else:
                return self.async_create_entry(title="YouTube Pro", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_COOKIE_PATH, default=DEFAULT_COOKIE_PATH): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )