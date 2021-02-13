from datetime import datetime

import iso8601
import pytz
from tzlocal import get_localzone


def parse_date(input_value):
    if input_value == "" or input_value is None:
        return None
    return iso8601.parse_date(input_value)


def parse_int(input_value, default_value=None):
    if input_value is None:
        return default_value
    try:
        return int(input_value)
    except ValueError:
        return default_value


def parse_float(input_value, default_value=None):
    if input_value is None:
        return default_value
    try:
        return float(input_value)
    except ValueError:
        return default_value


def parse_bool_int(input_value):
    if input_value is None:
        return False
    try:
        num = int(input_value)
        return bool(num)
    except ValueError:
        return False


def localize_datetime(timestamp: datetime) -> datetime:
    if timestamp.tzinfo is not None:
        return timestamp

    local_tz = get_localzone()
    return local_tz.localize(timestamp).astimezone(pytz.utc)
