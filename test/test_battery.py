from datetime import datetime

import pytest


class TestBattery:
    @pytest.mark.vcr
    def test_get_batteries_valid(self, grocy):
        batteries = grocy.batteries()

        assert len(batteries) == 4
        assert isinstance(batteries[0].last_tracked_time, datetime)

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
