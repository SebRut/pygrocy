import json
from unittest import TestCase

from pygrocy.grocy_api_client import LocationData


class TestLocationData(TestCase):
    def test_parse(self):
        input_json = """{
            "id": "1",
            "name": "string",
            "description": "string",
            "row_created_timestamp": "2019-04-17 10:30:00"
        }"""

        response = LocationData(json.loads(input_json))

        assert response.id == 1
        assert response.name == "string"
        assert response.description == "string"
        