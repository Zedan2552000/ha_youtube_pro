from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    coordinator = hass.data[DOMAIN]
    async_add_entities([
        YouTubeProSensor(coordinator, "watching_now", "YouTube Watching", "mdi:youtube"),
        YouTubeProSensor(coordinator, "notifications_count", "YouTube Notifications", "mdi:bell"),
        YouTubeProSensor(coordinator, "live_now_count", "YouTube Live Channels", "mdi:access-point"),
    ], True)

class YouTubeProSensor(SensorEntity):
    def __init__(self, coordinator, data_key, name, icon):
        self.coordinator = coordinator
        self.data_key = data_key
        self._name = name
        self._icon = icon

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def state(self):
        return self.coordinator.data.get(self.data_key)

    @property
    def extra_state_attributes(self):
        if self.data_key == "live_now_count":
            return {"live_channels": self.coordinator.data.get("live_channels", [])}
        if self.data_key == "watching_now":
            return {"account": self.coordinator.data.get("account_name", "Unknown")}
        return {}

    @property
    def should_poll(self):
        return False

    async def async_added_to_hass(self):
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
    async def async_update(self):
        await self.coordinator.async_request_refresh()
