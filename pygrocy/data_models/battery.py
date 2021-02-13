from datetime import datetime

from grocy_api_client import CurrentBatteryResponse

from pygrocy.base import DataModel


class Battery(DataModel):
    def __init__(self, response: CurrentBatteryResponse):
        self._id = response.id
        self._last_tracked_time = response.last_tracked_time
        self._next_estimated_charge_time = response.next_estimated_charge_time

    @property
    def id(self) -> int:
        return self._id

    @property
    def last_tracked_time(self) -> datetime:
        return self._last_tracked_time

    @property
    def next_estimated_charge_time(self) -> datetime:
        return self._next_estimated_charge_time
