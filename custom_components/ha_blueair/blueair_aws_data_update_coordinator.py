"""Blueair device object."""
import logging
from datetime import timedelta

from blueair_api import DeviceAws as BlueAirApiDeviceAws, ModelEnum
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.debounce import Debouncer

from .const import DOMAIN, FILTER_EXPIRED_THRESHOLD

_LOGGER = logging.getLogger(__name__)


class BlueairAwsDataUpdateCoordinator(DataUpdateCoordinator):
    """Blueair device object."""

    def __init__(
        self, hass: HomeAssistant, blueair_api_device: BlueAirApiDeviceAws
    ) -> None:
        """Initialize the device."""
        self.hass: HomeAssistant = hass
        self.blueair_api_device: BlueAirApiDeviceAws = blueair_api_device
        self._manufacturer: str = "BlueAir"
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}-{self.blueair_api_device.uuid}",
            update_interval=timedelta(minutes=5),
            request_refresh_debouncer=Debouncer(
                hass, _LOGGER, cooldown=5.0, immediate=False,
            ),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            await self.blueair_api_device.refresh()
            self.name = f"{DOMAIN}-{self.blueair_api_device.name}"
            _LOGGER.info("update called, pm1=%s", self.pm1)
            return {}
        except Exception as error:
            _LOGGER.exception(error)
            raise UpdateFailed(error) from error

    @property
    def id(self) -> str:
        """Return Blueair device id."""
        return self.blueair_api_device.uuid

    @property
    def device_name(self) -> str:
        """Return device name."""
        return self.blueair_api_device.name

    @property
    def manufacturer(self) -> str:
        """Return manufacturer for device."""
        return self._manufacturer

    @property
    def model(self) -> str:
        """Return api package enum of device model."""
        return self.blueair_api_device.model.model_name

    @property
    def fan_speed(self) -> int:
        """Return the current fan speed."""
        return self.blueair_api_device.fan_speed

    @property
    def speed_count(self) -> int:
        """Return the max fan speed."""
        if self.blueair_api_device.model == ModelEnum.HUMIDIFIER_H35I:
            return 64
        elif self.blueair_api_device.model in [
            ModelEnum.MAX_211I,
            ModelEnum.MAX_311I,
            ModelEnum.PROTECT_7440I,
            ModelEnum.PROTECT_7470I
        ]:
            return 91
        elif self.blueair_api_device.model == ModelEnum.T10I:
            return 4
        else:
            return 100

    @property
    def is_on(self) -> bool:
        """Return the current fan state."""
        return self.blueair_api_device.running

    @property
    def brightness(self) -> int:
        return self.blueair_api_device.brightness

    @property
    def child_lock(self) -> bool:
        return self.blueair_api_device.child_lock

    @property
    def night_mode(self) -> bool:
        return self.blueair_api_device.night_mode

    @property
    def temperature(self) -> int:
        return self.blueair_api_device.temperature

    @property
    def humidity(self) -> int:
        return self.blueair_api_device.humidity

    @property
    def voc(self) -> int:
        return self.blueair_api_device.tVOC

    @property
    def pm1(self) -> int:
        return self.blueair_api_device.pm1

    @property
    def pm10(self) -> int:
        return self.blueair_api_device.pm10

    @property
    def pm25(self) -> int:
        # pm25 is the more common name for pm2.5.
        return self.blueair_api_device.pm2_5

    @property
    def co2(self) -> int:
        return NotImplemented

    @property
    def online(self) -> bool:
        return self.blueair_api_device.wifi_working

    @property
    def fan_auto_mode(self) -> bool:
        return self.blueair_api_device.fan_auto_mode

    @property
    def wick_dry_mode(self) -> bool:
        return self.blueair_api_device.wick_dry_mode

    @property
    def water_shortage(self) -> bool:
        return self.blueair_api_device.water_shortage

    @property
    def filter_expired(self) -> bool:
        """Returns the current filter status."""
        if self.blueair_api_device.filter_usage_percentage not in (NotImplemented, None):
                return (self.blueair_api_device.filter_usage_percentage >=
                        FILTER_EXPIRED_THRESHOLD)
        if self.blueair_api_device.wick_usage_percentage not in (NotImplemented, None):
                return (self.blueair_api_device.wick_usage_percentage >=
                        FILTER_EXPIRED_THRESHOLD)

    async def set_fan_speed(self, new_speed) -> None:
        await self.blueair_api_device.set_fan_speed(new_speed)
        await self.async_request_refresh()

    async def set_running(self, running) -> None:
        await self.blueair_api_device.set_running(running)
        await self.async_request_refresh()

    async def set_brightness(self, brightness) -> None:
        await self.blueair_api_device.set_brightness(brightness)
        await self.async_request_refresh()

    async def set_child_lock(self, locked) -> None:
        await self.blueair_api_device.set_child_lock(locked)
        await self.async_request_refresh()

    async def set_night_mode(self, mode) -> None:
        await self.blueair_api_device.set_night_mode(mode)
        await self.async_request_refresh()

    async def set_fan_auto_mode(self, value) -> None:
        await self.blueair_api_device.set_fan_auto_mode(value)
        await self.async_request_refresh()

    async def set_wick_dry_mode(self, value) -> None:
        await self.blueair_api_device.set_wick_dry_mode(value)
        await self.async_request_refresh()
