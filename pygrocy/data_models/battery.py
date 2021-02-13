from datetime import datetime

from pygrocy.base import DataModel
from pygrocy.grocy_api_client import BatteryDetailsResponse, CurrentBatteryResponse


class Battery(DataModel):
    def __init__(self, response):
        self._init_empty()

        self._next_estimated_charge_time = response.next_estimated_charge_time

        if isinstance(response, CurrentBatteryResponse):
            self._init_from_CurrentBatteryResponse(response)
        elif isinstance(response, BatteryDetailsResponse):
            self._init_from_BatteryDetailsResponse(response)

    def _init_from_CurrentBatteryResponse(self, response: CurrentBatteryResponse):
        self._id = response.id
        self._last_tracked_time = response.last_tracked_time

    def _init_from_BatteryDetailsResponse(self, response: BatteryDetailsResponse):
        self._charge_cycles_count = response.charge_cycles_count
        self._last_charged = response.last_charged
        self._id = response.battery.id
        self._name = response.battery.name
        self._description = response.battery.description
        self._used_in = response.battery.used_in
        self._charge_interval_days = response.battery.charge_interval_days
        self._created_timestamp = response.battery.created_timestamp
        self._userfields = response.battery.userfields

    def _init_empty(self):
        self._last_tracked_time = None
        self._charge_cycles_count = None
        self._last_charged = None
        self._name = None
        self._description = None
        self._used_in = None
        self._charge_interval_days = None
        self._created_timestamp = None
        self._userfields = None

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def used_in(self) -> str:
        return self._used_in

    @property
    def charge_interval_days(self) -> int:
        return self._charge_interval_days

    @property
    def created_timestamp(self) -> datetime:
        return self._created_timestamp

    @property
    def charge_cycles_count(self) -> int:
        return self._charge_cycles_count

    @property
    def userfields(self):
        return self._userfields

    @property
    def last_charged(self) -> datetime:
        return self._last_charged

    @property
    def last_tracked_time(self) -> datetime:
        return self._last_tracked_time

    @property
    def next_estimated_charge_time(self) -> datetime:
        return self._next_estimated_charge_time
