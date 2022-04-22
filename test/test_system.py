from datetime import datetime

import pytest


class TestSystem:
    @pytest.mark.vcr
    def test_get_last_db_changed_valid(self, grocy):
        timestamp = grocy.get_last_db_changed()

        assert isinstance(timestamp, datetime)
        assert timestamp.year == 2022
        assert timestamp.month == 4
        assert timestamp.day == 22
