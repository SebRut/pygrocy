import iso8601


def parse_date(input):
    if input == None:
        return None
    else:
        return iso8601.parse_date(input)


def parse_int(input, default_value=None):
    if input == None:
        return default_value
    else:
        try:
            return int(input)
        except ValueError:
            return default_value


def parse_float(input, default_value=None):
    if input == None:
        return default_value
    else:
        try:
            return float(input)
        except ValueError:
            return default_value
