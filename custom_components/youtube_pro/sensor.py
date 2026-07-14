from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities([
        YouTubeProSensor(coordinator, "account_name", "YouTube Account", "mdi:account"),
        YouTubeProSensor(coordinator, "watching_now", "YouTube Watching", "mdi:youtube"),
        YouTubeProSensor(coordinator, "notifications_count", "YouTube Notifications", "mdi:bell"),
        YouTubeProSensor(coordinator, "live_now_count", "YouTube Live Channels", "mdi:access-point"),
        YouTubeProSensor(coordinator, "watch_later_count", "YouTube Watch Later", "mdi:clock-time-four"),
        YouTubeProSensor(coordinator, "subscriptions_count", "YouTube Subscriptions", "mdi:youtube-subscription"),
        YouTubeProSensor(coordinator, "recent_history", "YouTube History", "mdi:history"),
    ], True)

class YouTubeProSensor(SensorEntity):
    def __init__(self, coordinator, data_key, name, icon):
        self.coordinator = coordinator
        self.data_key = data_key
        self._name = name
        self._icon = icon
        self._attr_unique_id = f"youtube_pro_{data_key}"

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def state(self):
        val = self.coordinator.data.get(self.data_key)
        if isinstance(val, list):
            return len(val) if val else "Empty"
        return val

    @property
    def extra_state_attributes(self):
        attrs = {}
        if self.data_key == "live_now_count":
            attrs["live_channels"] = self.coordinator.data.get("live_channels", [])
        if self.data_key == "recent_history":
            attrs["last_5_videos"] = self.coordinator.data.get("recent_history", [])
        return attrs

    @property
    def should_poll(self):
        return False

    async def async_added_to_hass(self):
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
    async def async_update(self):
        await self.coordinator.async_request_refresh()