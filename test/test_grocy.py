from unittest import TestCase

from pygrocy import Grocy


class TestGrocy(TestCase):
    def test_init(self):
        grocy = Grocy("http://example.com", "api_key")
        assert isinstance(grocy, Grocy)
