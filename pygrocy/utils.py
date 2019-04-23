import iso8601


def parse_date(input):
    if input is None:
        return None
    return iso8601.parse_date(input)


def parse_int(input, default_value=None):
    if input is None:
        return default_value
    try:
        return int(input)
    except ValueError:
        return default_value


def parse_float(input, default_value=None):
    if input is None:
        return default_value
    try:
        return float(input)
    except ValueError:
        return default_value
