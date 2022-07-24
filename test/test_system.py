from datetime import date, datetime

import pytest
from pygrocy.data_models.system import SystemConfig, SystemInfo, SystemTime


class TestSystem:
    @pytest.mark.vcr
    def test_get_last_db_changed_valid(self, grocy):
        timestamp = grocy.get_last_db_changed()

        assert isinstance(timestamp, datetime)
        assert timestamp.year == 2022
        assert timestamp.month == 4
        assert timestamp.day == 22

    @pytest.mark.vcr
    def test_get_system_info_valid(self, grocy):
        system_info = grocy.get_system_info()

        assert isinstance(system_info, SystemInfo)
        assert isinstance(system_info.grocy_release_date, date)
        assert system_info.grocy_version == "3.3.1"
        assert system_info.php_version == "8.0.20"
        assert system_info.sqlite_version == "3.38.5"

    @pytest.mark.vcr
    def test_get_system_time_valid(self, grocy):
        system_time = grocy.get_system_time()

        assert isinstance(system_time, SystemTime)
        assert isinstance(system_time.time_local, datetime)
        assert isinstance(system_time.time_local_sqlite3, datetime)
        assert isinstance(system_time.time_utc, datetime)

        assert system_time.timezone == "UTC"
        assert system_time.timestamp == 1658679505

    @pytest.mark.vcr
    def test_get_system_config_valid(self, grocy):
        system_config = grocy.get_system_config()

        assert isinstance(system_config, SystemConfig)

        assert system_config.username == "Demo User"
        assert system_config.currency == "USD"
        assert system_config.locale == "en"
        assert "FEATURE_FLAG_TASKS" in system_config.enabled_features
        assert "FEATURE_FLAG_THERMAL_PRINTER" not in system_config.enabled_features
