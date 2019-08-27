import json
from unittest import TestCase

from pygrocy.grocy_api_client import ShoppingListItem


class TestShoppingListItem(TestCase):
    def test_parse(self):
        input_json = """{
            "id": "1",
            "product_id": "6",
            "note": "string",
            "amount": "2",
            "row_created_timestamp": "2019-04-17 10:30:00",
            "shopping_list_id": "1",
            "done": "0"
        }"""

        response = ShoppingListItem(json.loads(input_json))

        assert response.product_id == 6
        assert response.id == 1
        assert response.note == "string"
        assert response.amount == 2
        