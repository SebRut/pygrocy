import json
from datetime import datetime
from test.test_const import CONST_BASE_URL, CONST_PORT, CONST_SSL
from unittest import TestCase
from unittest.mock import mock_open, patch

import responses

from pygrocy import Grocy
from pygrocy.errors import GrocyError
from pygrocy.grocy_api_client import GrocyApiClient


class TestGrocy(TestCase):
    def setUp(self):
        self.grocy_regular = Grocy(CONST_BASE_URL, "api_key")
        self.grocy = Grocy(
            CONST_BASE_URL, "demo_mode", verify_ssl=CONST_SSL, port=CONST_PORT
        )
        self.base_url = f"{CONST_BASE_URL}:{CONST_PORT}/api"
        self.date_test = datetime.strptime("2019-05-04 11:31:04", "%Y-%m-%d %H:%M:%S")
        self.add_generic_data = {"name": "This is a task"}

    @responses.activate
    def test_get_shopping_list_invalid_no_data(self):
        responses.add(
            responses.GET, f"{self.base_url}/objects/shopping_list", status=400
        )
        self.assertRaises(GrocyError, self.grocy.shopping_list)

    @responses.activate
    def test_get_shopping_list_invalid_missing_data(self):
        resp = []
        responses.add(
            responses.GET,
            f"{self.base_url}/objects/shopping_list",
            json=resp,
            status=200,
        )
        self.assertEqual(len(self.grocy.shopping_list()), 0)

    @responses.activate
    def test_clear_shopping_list_error(self):
        responses.add(
            responses.POST, f"{self.base_url}/stock/shoppinglist/clear", status=400
        )
        self.assertRaises(GrocyError, self.grocy.clear_shopping_list)

    @responses.activate
    def test_remove_product_in_shopping_list_error(self):
        responses.add(
            responses.POST,
            f"{self.base_url}/stock/shoppinglist/remove-product",
            status=400,
        )
        self.assertRaises(GrocyError, self.grocy.remove_product_in_shopping_list, 1)

    @responses.activate
    def test_get_product_groups_invalid_no_data(self):
        responses.add(
            responses.GET, f"{self.base_url}/objects/product_groups", status=400
        )
        self.assertRaises(GrocyError, self.grocy.product_groups)

    @responses.activate
    def test_get_product_groups_invalid_missing_data(self):
        resp = []
        responses.add(
            responses.GET,
            f"{self.base_url}/objects/product_groups",
            json=resp,
            status=200,
        )
        self.assertEqual(len(self.grocy.product_groups()), 0)

    @responses.activate
    def test_add_product_pic_invalid_missing_data(self):
        with patch("os.path.exists") as m_exist:
            m_exist.return_value = False
            self.assertRaises(
                FileNotFoundError, self.grocy.add_product_pic, 1, "/somepath/pic.jpg"
            )

    @responses.activate
    def test_upload_product_picture_error(self):
        with patch("os.path.exists") as m_exist:
            with patch("builtins.open", mock_open()):
                m_exist.return_value = True
                api_client = GrocyApiClient(
                    CONST_BASE_URL, "demo_mode", port=CONST_PORT, verify_ssl=CONST_SSL
                )
                responses.add(
                    responses.PUT,
                    f"{self.base_url}/files/productpictures/MS5qcGc=",
                    status=400,
                )
                self.assertRaises(
                    GrocyError,
                    api_client.upload_product_picture,
                    1,
                    "/somepath/pic.jpg",
                )

    @responses.activate
    def test_update_product_pic_error(self):
        api_client = GrocyApiClient(
            CONST_BASE_URL, "demo_mode", port=CONST_PORT, verify_ssl=CONST_SSL
        )
        responses.add(responses.PUT, f"{self.base_url}/objects/products/1", status=400)
        self.assertRaises(GrocyError, api_client.update_product_pic, 1)

    @responses.activate
    def test_get_due_invalid_no_data(self):
        resp = {"due_products": [], "expired_products": [], "missing_products": []}
        responses.add(
            responses.GET, f"{self.base_url}/stock/volatile", json=resp, status=200
        )

        self.grocy.due_products(True)

    @responses.activate
    def test_get_expired_invalid_no_data(self):
        resp = {"expiring_products": [], "expired_products": [], "missing_products": []}
        responses.add(
            responses.GET, f"{self.base_url}/stock/volatile", json=resp, status=200
        )

        self.grocy.expired_products(True)

    @responses.activate
    def test_get_expired_invalid_missing_data(self):
        resp = {}
        responses.add(
            responses.GET, f"{self.base_url}/stock/volatile", json=resp, status=200
        )

    @responses.activate
    def test_get_missing_invalid_no_data(self):
        resp = {"expiring_products": [], "expired_products": [], "missing_products": []}
        responses.add(
            responses.GET, f"{self.base_url}/stock/volatile", json=resp, status=200
        )

        self.grocy.missing_products(True)

    @responses.activate
    def test_get_missing_invalid_missing_data(self):
        resp = {}
        responses.add(
            responses.GET, f"{self.base_url}/stock/volatile", json=resp, status=200
        )

    @responses.activate
    def test_get_userfields_valid(self):
        resp = {"uf1": 0, "uf2": "string"}

        responses.add(
            responses.GET, f"{self.base_url}/userfields/chores/1", json=resp, status=200
        )

        a_chore_uf = self.grocy.get_userfields("chores", 1)

        self.assertEqual(a_chore_uf["uf1"], 0)

    @responses.activate
    def test_set_userfields_valid(self):
        responses.add(responses.PUT, f"{self.base_url}/userfields/chores/1", status=204)
        self.grocy.set_userfields("chores", 1, "auserfield", "value")

    @responses.activate
    def test_set_userfields_error(self):
        responses.add(responses.PUT, f"{self.base_url}/userfields/chores/1", status=400)
        self.assertRaises(
            GrocyError, self.grocy.set_userfields, "chores", 1, "auserfield", "value"
        )

    @responses.activate
    def test_get_last_db_changed_invalid_no_data(self):
        resp = {}
        responses.add(
            responses.GET,
            f"{self.base_url}/system/db-changed-time",
            json=resp,
            status=200,
        )

        self.assertIsNone(self.grocy.get_last_db_changed())

    @responses.activate
    def test_add_product_valid(self):
        responses.add(
            responses.POST, f"{self.base_url}/stock/products/1/add", status=200
        )
        self.assertIsNone(self.grocy.add_product(1, 1.3, 2.44, self.date_test))

    @responses.activate
    def test_add_product_error(self):
        responses.add(
            responses.POST, f"{self.base_url}/stock/products/1/add", status=400
        )
        self.assertRaises(
            GrocyError, self.grocy.add_product, 1, 1.3, 2.44, self.date_test
        )

    @responses.activate
    def test_consume_product_valid(self):
        responses.add(
            responses.POST, f"{self.base_url}/stock/products/1/consume", status=200
        )
        self.assertIsNone(self.grocy.consume_product(1, 1.3))

    @responses.activate
    def test_consume_product_error(self):
        responses.add(
            responses.POST, f"{self.base_url}/stock/products/1/consume", status=400
        )
        self.assertRaises(GrocyError, self.grocy.consume_product, 1, 1.3)

    @responses.activate
    def test_execute_chore_valid(self):
        responses.add(responses.POST, f"{self.base_url}/chores/1/execute", status=200)
        self.assertIsNone(self.grocy.execute_chore(1, 1, self.date_test))

    @responses.activate
    def test_execute_chore_error(self):
        responses.add(responses.POST, f"{self.base_url}/chores/1/execute", status=400)
        self.assertRaises(GrocyError, self.grocy.execute_chore, 1, 1, self.date_test)

    @responses.activate
    def test_get_meal_plan(self):
        resp_json = json.loads(
            """[
              {
                "id": "1",
                "day": "2020-08-10",
                "type": "recipe",
                "recipe_id": "1",
                "recipe_servings": "1",
                "note": null,
                "product_id": null,
                "product_amount": "0.0",
                "product_qu_id": null,
                "row_created_timestamp": "2020-08-12 19:59:30",
                "userfields": null
              }
          ]"""
        )
        responses.add(
            responses.GET,
            f"{self.base_url}/objects/meal_plan",
            json=resp_json,
            status=200,
        )
        meal_plan = self.grocy.meal_plan()
        self.assertEqual(len(meal_plan), 1)
        self.assertEqual(meal_plan[0].id, 1)
        self.assertEqual(meal_plan[0].recipe_id, 1)

    @responses.activate
    def test_get_recipe(self):
        resp_json = json.loads(
            """{
          "id": "1",
          "name": "Pizza",
          "description": "<p>Mix everything</p>",
          "row_created_timestamp": "2020-08-12 11:37:34",
          "picture_file_name": "51si0q0wsiq5imo4f8wbIMG_5709.jpeg",
          "base_servings": "4",
          "desired_servings": "4",
          "not_check_shoppinglist": "0",
          "type": "normal",
          "product_id": "",
          "userfields": null
        }"""
        )
        responses.add(
            responses.GET,
            f"{self.base_url}/objects/recipes/1",
            json=resp_json,
            status=200,
        )
        recipe = self.grocy.recipe(1)
        self.assertEqual(recipe.id, 1)
        self.assertEqual(recipe.name, "Pizza")
        self.assertEqual(recipe.base_servings, 4)
        self.assertIsInstance(recipe.get_picture_url_path(400), str)
