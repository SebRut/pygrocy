from unittest import TestCase
from unittest.mock import patch, mock_open

import json
from datetime import datetime
from requests.exceptions import HTTPError
import responses
from pygrocy import Grocy
from pygrocy.grocy import Chore, Product, Group, ShoppingListProduct

from pygrocy.grocy_api_client import CurrentStockResponse, GrocyApiClient, TransactionType, UserDto, ChoreDetailsResponse, ProductData
from test.test_const import CONST_BASE_URL, CONST_PORT, CONST_SSL

class TestGrocy(TestCase):

    def setUp(self):
        self.grocy_regular = Grocy(CONST_BASE_URL, "api_key")
        self.grocy = Grocy(CONST_BASE_URL, "demo_mode",  verify_ssl = CONST_SSL, port = CONST_PORT)
        self.base_url = f"{CONST_BASE_URL}:{CONST_PORT}/api"
        self.date_test = datetime.strptime("2019-05-04 11:31:04", '%Y-%m-%d %H:%M:%S')

    def test_init(self):
        self.assertIsInstance(self.grocy, Grocy)
        
    def test_get_chores_valid(self):
        chores = self.grocy.chores()
        
        self.assertIsInstance(chores, list)
        self.assertGreaterEqual(len(chores), 1)
        for chore in chores:
            self.assertIsInstance(chore, Chore)
            self.assertIsInstance(chore.id, int)
            self.assertIsInstance(chore.last_tracked_time, datetime)
            self.assertIsInstance(chore.next_estimated_execution_time, datetime)
            self.assertIsInstance(chore.name, str)
            self.assertIsInstance(chore.last_done_by, UserDto)

    @responses.activate
    def test_get_chore_details_valid(self):
        details_json = """{
            "chore": {
                "id": "1",
                "name": "Changed towels in the bathroom",
                "description": null,
                "period_type": "manually",
                "period_days": "5",
                "row_created_timestamp": "2020-03-16 00:50:14",
                "period_config": null,
                "track_date_only": "0",
                "rollover": "0",
                "assignment_type": null,
                "assignment_config": null,
                "next_execution_assigned_to_user_id": null,
                "consume_product_on_execution": "0",
                "product_id": null,
                "product_amount": null,
                "period_interval": "1"
            },
            "last_tracked": "2020-03-11 00:50:15",
            "tracked_count": 3,
            "last_done_by": {
                "id": "1",
                "username": "Demo User",
                "first_name": null,
                "last_name": null,
                "row_created_timestamp": "2020-03-16 00:50:13",
                "display_name": "Demo User"
            },
            "next_estimated_execution_time": "2999-12-31 23:59:59",
            "next_execution_assigned_user": null
        }"""
        details_json = json.loads(details_json)
        responses.add(responses.GET, f"{self.base_url}/chores/1", json=details_json, status=200)
        chore_details = self.grocy.chore(1)
        self.assertIsInstance(chore_details, ChoreDetailsResponse)

    def test_get_stock_valid(self):
        stock = self.grocy.stock().products_list

        self.assertIsInstance(stock, list)
        self.assertGreaterEqual(len(stock), 10)
        for prod in stock:
            self.assertIsInstance(prod, Product)

    @responses.activate
    def test_get_stock_invalid_missing_data(self):
        resp = []
        responses.add(responses.GET, f"{self.base_url}/stock", json=resp, status=200)
        self.assertEqual(len(self.grocy.stock().products_list) ,0)
        
    def test_get_shopping_list_valid(self):
        shopping_list = self.grocy.shopping_list().list
        
        self.assertIsInstance(shopping_list, list)
        self.assertGreaterEqual(len(shopping_list), 1)
        for item in shopping_list:
            self.assertIsInstance(item, ShoppingListProduct)
            self.assertIsInstance(item.id, int)
            if item.product_id:
                self.assertIsInstance(item.product_id, int)
                self.assertIsInstance(item.product, ProductData)
                self.assertIsInstance(item.product.id, int)
            self.assertIsInstance(item.amount, float)
            if item.note:
                self.assertIsInstance(item.note, str)

    @responses.activate
    def test_get_shopping_list_invalid_no_data(self):
        responses.add(responses.GET, f"{self.base_url}/objects/shopping_list", status=400)
        self.assertRaises(HTTPError, self.grocy.shopping_list)
        
    @responses.activate
    def test_get_shopping_list_invalid_missing_data(self):
        resp = []
        responses.add(responses.GET, f"{self.base_url}/objects/shopping_list", json=resp, status=200)
        self.assertEqual(len(self.grocy.shopping_list().list), 0)
        
    def test_add_missing_product_to_shopping_list_valid(self):
         self.assertIsNone(self.grocy.shopping_list().add_missing_product_to_shopping_list())
        
    @responses.activate
    def test_add_missing_product_to_shopping_list_error(self):
        responses.add_passthru(f"{self.base_url}/objects/shopping_list")
        responses.add(responses.POST, f"{self.base_url}/stock/shoppinglist/add-missing-products", status=400)

    def test_add_product_to_shopping_list_valid(self):
        self.grocy.shopping_list().add_product_to_shopping_list(22)
        
    def test_add_product_to_shopping_list_error(self):
        self.assertRaises(HTTPError, self.grocy.shopping_list().add_product_to_shopping_list, 3000)
        
    @responses.activate
    def test_clear_shopping_list_valid(self):
        responses.add_passthru(f"{self.base_url}/objects/shopping_list")
        responses.add(responses.POST, f"{self.base_url}/stock/shoppinglist/clear", status=204)
        self.grocy.shopping_list().clear_shopping_list()
        
    @responses.activate
    def test_clear_shopping_list_error(self):
        responses.add_passthru(f"{self.base_url}/objects/shopping_list")
        responses.add(responses.POST, f"{self.base_url}/stock/shoppinglist/clear", status=400)
        self.assertRaises(HTTPError, self.grocy.shopping_list().clear_shopping_list)
        
    @responses.activate
    def test_remove_product_in_shopping_list_valid(self):
        responses.add_passthru(f"{self.base_url}/objects/shopping_list")
        responses.add(responses.POST, f"{self.base_url}/stock/shoppinglist/remove-product", status=204)
        self.grocy.shopping_list().remove_product_in_shopping_list(1)
        
    @responses.activate
    def test_remove_product_in_shopping_list_error(self):
        responses.add_passthru(f"{self.base_url}/objects/shopping_list")
        responses.add(responses.POST, f"{self.base_url}/stock/shoppinglist/remove-product", status=400)
        self.assertRaises(HTTPError, self.grocy.shopping_list().remove_product_in_shopping_list, 1)
        
    def test_get_product_groups_valid(self):
        product_groups_list = self.grocy.product_groups()
        
        self.assertIsInstance(product_groups_list, list)
        self.assertGreaterEqual(len(product_groups_list), 1)
        for group in product_groups_list:
            self.assertIsInstance(group, Group)
            self.assertIsInstance(group.id, int)
            self.assertIsInstance(group.name, str)
            if group.description:
                self.assertIsInstance(group.description, str)
            
    @responses.activate
    def test_get_product_groups_invalid_no_data(self):
        responses.add(responses.GET, f"{self.base_url}/objects/product_groups", status=400)
        self.assertRaises(HTTPError, self.grocy.product_groups)
        
    @responses.activate
    def test_get_product_groups_invalid_missing_data(self):
        resp = []
        responses.add(responses.GET, f"{self.base_url}/objects/product_groups", json=resp, status=200)
        self.assertEqual(len(self.grocy.product_groups()), 0)

    @responses.activate
    def test_add_product_pic_valid(self):
        with patch("os.path.exists" ) as m_exist:
            with patch("builtins.open", mock_open()) as m_open:
                m_exist.return_value = True
                responses.add(responses.PUT, f"{self.base_url}/files/productpictures/MS5qcGc=", status=204)
                responses.add(responses.PUT, f"{self.base_url}/objects/products/1", status=204)
                resp = self.grocy.add_product_pic(1,"/somepath/pic.jpg")
                self.assertIsNone(resp)

    @responses.activate
    def test_add_product_pic_invalid_missing_data(self):
        with patch("os.path.exists" ) as m_exist:
            m_exist.return_value = False
            self.assertRaises(FileNotFoundError, self.grocy.add_product_pic,1,"/somepath/pic.jpg")

    @responses.activate
    def test_upload_product_picture_error(self):
        with patch("os.path.exists" ) as m_exist:
            with patch("builtins.open", mock_open()) as m_open:
                m_exist.return_value = True
                api_client = GrocyApiClient(CONST_BASE_URL, "demo_mode", port = CONST_PORT, verify_ssl = CONST_SSL)
                responses.add(responses.PUT, f"{self.base_url}/files/productpictures/MS5qcGc=", status=400)
                self.assertRaises(HTTPError, api_client.upload_product_picture, 1,"/somepath/pic.jpg")
                
        
    @responses.activate
    def test_update_product_pic_error(self):
        api_client = GrocyApiClient(CONST_BASE_URL, "demo_mode", port = CONST_PORT, verify_ssl = CONST_SSL)
        responses.add(responses.PUT, f"{self.base_url}/objects/products/1", status=400)
        self.assertRaises(HTTPError, api_client.update_product_pic, 1)        
    
    def test_get_expiring_products_valid(self):
        
        expiring_product = self.grocy.stock().expiring_products

        self.assertIsInstance(expiring_product, list)
        self.assertGreaterEqual(len(expiring_product), 1)
        for prod in expiring_product:
            self.assertIsInstance(prod, Product)

    @responses.activate
    def test_get_expiring_invalid_no_data(self):
        resp = {
            "expiring_products": [],
            "expired_products": [],
            "missing_products": []
        }
        responses.add_passthru(f"{self.base_url}/stock")
        responses.add(responses.GET, f"{self.base_url}/stock/volatile", json=resp, status=200)

        expiring_product = self.grocy.stock().expiring_products
        self.assertEqual(len(expiring_product), 0)

    @responses.activate
    def test_get_expiring_invalid_missing_data(self):
        resp = {}
        responses.add_passthru(f"{self.base_url}/stock")
        responses.add(responses.GET, f"{self.base_url}/stock/volatile", json=resp, status=200)
        
    def test_get_expired_products_valid(self):
        
        expired_product = self.grocy.stock().expired_products

        self.assertIsInstance(expired_product, list)
        self.assertGreaterEqual(len(expired_product), 1)
        for prod in expired_product:
            self.assertIsInstance(prod, Product)

    @responses.activate
    def test_get_expired_invalid_no_data(self):
        resp = {
            "expiring_products": [],
            "expired_products": [],
            "missing_products": []
        }
        responses.add_passthru(f"{self.base_url}/stock")
        responses.add(responses.GET, f"{self.base_url}/stock/volatile", json=resp, status=200)

        expired_products = self.grocy.stock().expired_products
        self.assertEqual(len(expired_products), 0)

    @responses.activate
    def test_get_expired_invalid_missing_data(self):
        resp = {}
        responses.add_passthru(f"{self.base_url}/stock")
        responses.add(responses.GET, f"{self.base_url}/stock/volatile", json=resp, status=200)
        
    def test_get_missing_products_valid(self):

        missing_product = self.grocy.stock().missing_products

        self.assertIsInstance(missing_product, list)
        self.assertGreaterEqual(len(missing_product), 1)
        for prod in missing_product:
            self.assertIsInstance(prod, Product)
            self.assertIsInstance(prod.amount_missing, float)
            self.assertIsInstance(prod.is_partly_in_stock, bool)

    @responses.activate
    def test_get_missing_invalid_no_data(self):
        resp = {
            "expiring_products": [],
            "expired_products": [],
            "missing_products": []
        }
        responses.add_passthru(f"{self.base_url}/stock")
        responses.add(responses.GET, f"{self.base_url}/stock/volatile", json=resp, status=200)

        missing_products = self.grocy.stock().missing_products
        self.assertEqual(len(missing_products), 0)

    @responses.activate
    def test_get_missing_invalid_missing_data(self):
        resp = {}
        responses.add_passthru(f"{self.base_url}/stock")
        responses.add(responses.GET, f"{self.base_url}/stock/volatile", json=resp, status=200)
        
    @responses.activate
    def test_get_userfields_valid(self):
        resp =  {
                "uf1": 0,
                "uf2": "string"
            }
        
        responses.add(responses.GET, f"{self.base_url}/userfields/chores/1", json=resp, status=200)

        a_chore_uf = self.grocy.get_userfields("chores",1)

        self.assertEqual(a_chore_uf['uf1'], 0)

    def test_get_userfields_invalid_no_data(self):
        self.grocy.get_userfields("chores",1)

    @responses.activate
    def test_set_userfields_valid(self):
        responses.add(responses.PUT, f"{self.base_url}/userfields/chores/1", status=204)
        self.grocy.set_userfields("chores",1,"auserfield", "value")
        
    @responses.activate
    def test_set_userfields_error(self):
        responses.add(responses.PUT, f"{self.base_url}/userfields/chores/1", status=400)
        self.assertRaises(HTTPError, self.grocy.set_userfields, "chores",1,"auserfield","value")

    def test_get_last_db_changed_valid(self):

        timestamp = self.grocy.get_last_db_changed()

        self.assertIsInstance(timestamp, datetime)


    @responses.activate
    def test_get_last_db_changed_invalid_no_data(self):
        resp = {}
        responses.add(responses.GET, f"{self.base_url}/system/db-changed-time", json=resp ,status=200)

        self.assertIsNone(self.grocy.get_last_db_changed())

    @responses.activate
    def test_add_product_valid(self):
        responses.add_passthru(f"{self.base_url}/stock")
        responses.add(responses.POST, f"{self.base_url}/stock/products/1/add", status=200)
        self.assertIsNone(self.grocy.stock().add_product(1, 1.3, 2.44, self.date_test))

    @responses.activate
    def test_add_product_error(self):
        responses.add_passthru(f"{self.base_url}/stock")
        responses.add(responses.POST, f"{self.base_url}/stock/products/1/add", status=400)
        self.assertRaises(HTTPError, self.grocy.stock().add_product, 1, 1.3, 2.44, self.date_test)

    @responses.activate
    def test_consume_product_valid(self):
        responses.add_passthru(f"{self.base_url}/stock")
        responses.add(responses.POST, f"{self.base_url}/stock/products/1/consume", status=200)
        self.assertIsNone(self.grocy.stock().consume_product(1, 1.3, self.date_test))

    @responses.activate
    def test_consume_product_error(self):
        responses.add_passthru(f"{self.base_url}/stock")
        responses.add(responses.POST, f"{self.base_url}/stock/products/1/consume", status=400)
        self.assertRaises(HTTPError, self.grocy.stock().consume_product, 1, 1.3, self.date_test)

    @responses.activate
    def test_execute_chore_valid(self):
        responses.add_passthru(f"{self.base_url}/chores")
        responses.add(responses.POST, f"{self.base_url}/chores/1/execute", status=200)
        self.assertIsNone(self.grocy.chores()[0].execute_chore(1, self.date_test))

    @responses.activate
    def test_execute_chore_error(self):
        responses.add_passthru(f"{self.base_url}/chores")
        responses.add(responses.POST, f"{self.base_url}/chores/1/execute", status=400)
        self.assertRaises(HTTPError, self.grocy.chores()[0].execute_chore, 1, self.date_test)
