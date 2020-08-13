import json
from datetime import datetime
from unittest import TestCase

from pygrocy.grocy_api_client import MealPlanResponse


class TestMealPlanResponse(TestCase):
    def test_parse(self):
        input_json = """{
            "id": "7",
            "day": "2020-08-16",
            "type": "recipe",
            "recipe_id": "4",
            "recipe_servings": "3",
            "note": null,
            "product_id": null,
            "product_amount": "0.0",
            "product_qu_id": null,
            "row_created_timestamp": "2020-08-12 14:37:06",
            "userfields": null
        }"""

        response = MealPlanResponse(json.loads(input_json))

        assert response.id == 7
        assert response.recipe_id == 4
        assert response.recipe_servings == 3
        self.assertIsInstance(response.day, datetime)
