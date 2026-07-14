import logging
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, CONF_COOKIE_PATH, UPDATE_INTERVAL
from .api import YouTubeAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up YouTube Pro from a config entry."""
    cookie_path = hass.config.path(entry.data[CONF_COOKIE_PATH].replace("/config/", ""))

    api = YouTubeAPI(cookie_path)

    async def async_update_data():
        try:
            return await hass.async_add_executor_job(api.fetch_data)
        except Exception as err:
            raise UpdateFailed(f"Error fetching YouTube data: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="YouTube Pro Sensor",
        update_method=async_update_data,
        update_interval=timedelta(seconds=UPDATE_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok