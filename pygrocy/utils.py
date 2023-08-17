from datetime import datetime


def parse_date(input_value):
    if input_value == "" or input_value is None:
        return None
    return datetime.fromisoformat(input_value)


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
    return timestamp.astimezone()


def grocy_datetime_str(timestamp: datetime) -> str:
    if timestamp is None:
        return ""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")
