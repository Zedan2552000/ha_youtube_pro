import logging
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import DOMAIN, CONF_COOKIE_PATH, DEFAULT_COOKIE_PATH, UPDATE_INTERVAL
from .api import YouTubeAPI

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_COOKIE_PATH, default=DEFAULT_COOKIE_PATH): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    conf = config.get(DOMAIN, {})
    cookie_path = conf.get(CONF_COOKIE_PATH, DEFAULT_COOKIE_PATH)
    cookie_path = hass.config.path(cookie_path.replace("/config/", ""))

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

    await coordinator.async_refresh()
    hass.data[DOMAIN] = coordinator

    hass.async_create_task(
        hass.helpers.discovery.async_load_platform('sensor', DOMAIN, {}, config)
    )

    return True
