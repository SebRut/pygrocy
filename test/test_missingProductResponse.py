import json
from unittest import TestCase

from pygrocy.grocy_api_client import MissingProductResponse


class TestMissingProductResponse(TestCase):
    def test_parse_partly_in_stock_true(self):
        input_json = """{ "id": "7", "name": "XXXX", "amount_missing": "2", "is_partly_in_stock": "1" }"""
        response = MissingProductResponse(json.loads(input_json))

        assert response.product_id == 7
        assert response.name == "XXXX"
        assert response.amount_missing == 2
        assert response.is_partly_in_stock

    def test_parse_partly_in_stock_false(self):
        input_json = """{ "id": "7", "name": "XXXX", "amount_missing": "2", "is_partly_in_stock": "0" }"""
        response = MissingProductResponse(json.loads(input_json))

        assert response.product_id == 7
        assert response.name == "XXXX"
        assert response.amount_missing == 2
        assert not response.is_partly_in_stock
