import json
from unittest import TestCase

from pygrocy.grocy_api_client import CurrentStockResponse


class TestCurrentStockResponse(TestCase):
    def test_parse(self):
        input_json = """{"product_id": 0,"amount": "12.53","best_before_date": "2019-04-22","amount_opened": 0}"""
        response = CurrentStockResponse(json.loads(input_json))

        assert response.product_id == 0
        assert response.amount == 12.53
        assert response.amount_opened == 0
        
        assert response.best_before_date.year == 2019
        assert response.best_before_date.month == 4
        assert response.best_before_date.day == 22
