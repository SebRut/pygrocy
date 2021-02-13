import pytest


class TestBattery:
    @pytest.mark.vcr
    def test_get_batteries_valid(self, grocy):
        batteries = grocy.batteries()

        assert len(batteries) == 4

    @pytest.mark.vcr
    def test_get_battery_details_valid(self, grocy):
        battery = grocy.battery(1)

        assert battery.id == 1
        assert battery.name == "Battery1"
        assert battery.description == "Warranty ends 2023"
        assert battery.used_in == "TV remote control"
        assert battery.charge_interval_days == 0
        assert battery.created_timestamp.year == 2021
        assert battery.created_timestamp.month == 2
        assert battery.created_timestamp.day == 13
        assert battery.userfields is None
        assert battery.charge_cycles_count == 4
