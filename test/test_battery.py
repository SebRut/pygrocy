from datetime import datetime

import pytest

from pygrocy.errors import GrocyError


class TestBattery:
    @pytest.mark.vcr
    def test_get_batteries_valid(self, grocy):
        batteries = grocy.batteries(get_details=False)

        assert len(batteries) == 4
        assert isinstance(batteries[0].last_tracked_time, datetime)

    @pytest.mark.vcr
    def test_get_batteries_with_details_valid(self, grocy):
        batteries = grocy.batteries(get_details=True)

        assert len(batteries) == 4
        assert isinstance(batteries[0].last_tracked_time, datetime)
        assert batteries[0].last_charged == batteries[0].last_tracked_time
        assert batteries[0].id == 1
        assert batteries[0].name == "Battery1"

    @pytest.mark.vcr
    def test_get_battery_details_valid(self, grocy):
        battery = grocy.battery(1)

        assert battery.id == 1
        assert battery.name == "Battery1"
        assert battery.description == "Warranty ends 2023"
        assert battery.used_in == "TV remote control"
        assert battery.charge_interval_days == 180
        assert isinstance(battery.created_timestamp, datetime)
        assert isinstance(battery.last_charged, datetime)
        assert isinstance(battery.next_estimated_charge_time, datetime)
        assert battery.userfields is None
        assert battery.charge_cycles_count == 4

    @pytest.mark.vcr
    def test_charge_battery(self, grocy):
        assert grocy.charge_battery(1)

    @pytest.mark.vcr
    def test_get_batteries_filters_valid(self, grocy):
        query_filter = ["next_estimated_charge_time<2022-06-20"]
        batteries = grocy.batteries(query_filters=query_filter)

        for item in batteries:
            assert item.next_estimated_charge_time < datetime(2022, 6, 20)

    @pytest.mark.vcr
    def test_get_batteries_filters_invalid(self, grocy, invalid_query_filter):
        with pytest.raises(GrocyError) as exc_info:
            grocy.batteries(query_filters=invalid_query_filter)

        error = exc_info.value
        assert error.status_code == 500
