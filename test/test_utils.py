from datetime import datetime

try:
    import zoneinfo
except ImportError:
    # backports can be removed when python 3.8 support is dropped
    from backports import zoneinfo

import pygrocy.utils as utils


class TestUtils:
    def test_parse_date_valid(self):
        date_str = "2022-07-10 21:10:53"
        date_obj = utils.parse_date(date_str)

        assert isinstance(date_obj, datetime)

    def test_parse_date_no_data(self):
        date_str = None
        date_obj = utils.parse_date(date_str)

        assert date_obj is None

    def test_parse_date_empty_string(self):
        date_str = ""
        date_obj = utils.parse_date(date_str)

        assert date_obj is None

    def test_parse_int_valid(self):
        int_str = "2"
        int_number = utils.parse_int(int_str)

        assert isinstance(int_number, int)

    def test_parse_int_no_data(self):
        int_str = None
        int_number = utils.parse_int(int_str, -1)

        assert int_number == -1

    def test_parse_int_error(self):
        int_str = "string"
        int_number = utils.parse_int(int_str, -1)

        assert int_number == -1

    def test_parse_float_valid(self):
        float_str = "2.01"
        float_number = utils.parse_float(float_str)

        assert isinstance(float_number, float)

    def test_parse_float_no_data(self):
        float_str = None
        float_number = utils.parse_float(float_str, -1)

        assert float_number == -1

    def test_parse_float_error(self):
        float_str = "string"
        float_number = utils.parse_float(float_str, -1)

        assert float_number == -1

    def test_localize_datetime_input_timezone_unaware(self):
        date = datetime(2022, 7, 10, 21, 17, 34, 633809, tzinfo=None)

        localized_datetime = utils.localize_datetime(date)

        assert localized_datetime == datetime(
            2022, 7, 10, 21, 17, 34, 633809, tzinfo=zoneinfo.ZoneInfo("localtime")
        )

    def test_localize_datetime_input_timezone_aware(self):
        date = datetime(
            2022,
            7,
            10,
            13,
            17,
            34,
            633809,
            tzinfo=zoneinfo.ZoneInfo("America/Los_Angeles"),
        )

        localized_datetime = utils.localize_datetime(date)

        assert localized_datetime == datetime(
            2022,
            7,
            10,
            13,
            17,
            34,
            633809,
            tzinfo=zoneinfo.ZoneInfo("America/Los_Angeles"),
        )

    def test_grocy_datetime_str(self):
        date = datetime(2022, 7, 10, 21, 17, 34, 633809, tzinfo=None)
        date_str = utils.grocy_datetime_str(date)

        assert date_str == "2022-07-10 21:17:34"
