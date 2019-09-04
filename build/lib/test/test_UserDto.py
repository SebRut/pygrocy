import json
from unittest import TestCase

from pygrocy.grocy_api_client import UserDto


class TestUserDto(TestCase):
    def test_parse(self):
        input_json = """{
            "id": "1",
            "username": "user",
            "first_name": "Guz",
            "last_name": "Userman",
            "row_created_timestamp": "2019-04-17 10:30:00",
            "display_name": "Guzzboy"
        }"""

        response = UserDto(json.loads(input_json))

        assert response.display_name == "Guzzboy"
        assert response.id == 1
        assert response.first_name == "Guz"
        assert response.last_name == "Userman"
        assert response.username == "user"
