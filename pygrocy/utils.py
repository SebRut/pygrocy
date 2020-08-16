import iso8601
import pytz
from tzlocal import get_localzone
from datetime import datetime


def parse_date(input_value):
    if input_value is "" or input_value is None:
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


def localize_datetime(timestamp: datetime) -> datetime:
    if timestamp.tzinfo is not None:
        return timestamp

    local_tz = get_localzone()
    return local_tz.localize(timestamp).astimezone(pytz.utc)
