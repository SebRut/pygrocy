from datetime import date, datetime
from typing import List

from pygrocy.base import DataModel
from pygrocy.grocy_api_client import SystemConfigDto, SystemInfoDto, SystemTimeDto


class SystemInfo(DataModel):
    def __init__(self, system_info_dto: SystemInfoDto):
        self._grocy_version = system_info_dto.grocy_version_info.version
        self._grocy_release_date = system_info_dto.grocy_version_info.release_date
        self._php_version = system_info_dto.php_version
        self._sqlite_version = system_info_dto.sqlite_version
        self._os = system_info_dto.os
        self._client = system_info_dto.client

    @property
    def grocy_version(self) -> str:
        return self._grocy_version

    @property
    def grocy_release_date(self) -> date:
        return self._grocy_release_date

    @property
    def php_version(self) -> str:
        return self._php_version

    @property
    def sqlite_version(self) -> str:
        return self._sqlite_version

    @property
    def os(self) -> str:
        return self._os

    @property
    def client(self) -> str:
        return self._client


class SystemTime(DataModel):
    def __init__(self, system_time_dto: SystemTimeDto):
        self._timezone = system_time_dto.timezone
        self._time_local = system_time_dto.time_local
        self._time_local_sqlite3 = system_time_dto.time_local_sqlite3
        self._time_utc = system_time_dto.time_utc
        self._timestamp = system_time_dto.timestamp

    @property
    def timezone(self) -> str:
        return self._timezone

    @property
    def time_local(self) -> datetime:
        return self._time_local

    @property
    def time_local_sqlite3(self) -> datetime:
        return self._time_local_sqlite3

    @property
    def time_utc(self) -> datetime:
        return self._time_utc

    @property
    def timestamp(self) -> int:
        return self._timestamp


class SystemConfig(DataModel):
    def __init__(self, system_config_dto: SystemConfigDto):
        self._username = system_config_dto.username
        self._base_path = system_config_dto.base_path
        self._base_url = system_config_dto.base_url
        self._mode = system_config_dto.mode
        self._default_locale = system_config_dto.default_locale
        self._locale = system_config_dto.locale
        self._currency = system_config_dto.currency

        self._enabled_features = []
        for feature, value in system_config_dto.feature_flags.items():
            if bool(value):
                self._enabled_features.append(feature)

    @property
    def username(self) -> str:
        return self._username

    @property
    def base_path(self) -> str:
        return self._base_path

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def default_locale(self) -> str:
        return self._default_locale

    @property
    def locale(self) -> str:
        return self._locale

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def enabled_features(self) -> List[str]:
        return self._enabled_features
