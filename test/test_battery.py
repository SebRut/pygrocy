import pytest


class TestBattery:
    @pytest.mark.vcr
    def test_get_batteries_valid(self, grocy):
        batteries = grocy.batteries()

        assert len(batteries) == 4
