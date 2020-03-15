from unittest import TestCase
from unittest.mock import patch, mock_open

from datetime import datetime
from requests.exceptions import HTTPError
import responses
from pygrocy import Grocy
from pygrocy.grocy import Product
from pygrocy.grocy import Group
from pygrocy.grocy import ShoppingListProduct
from pygrocy.grocy_api_client import CurrentStockResponse, GrocyApiClient
from test.test_const import CONST_BASE_URL, CONST_PORT, CONST_SSL

class TestGrocy(TestCase):

    def setUp(self):
        self.grocy = Grocy(CONST_BASE_URL, "api_key")
        self.grocy = None
        self.grocy = Grocy(CONST_BASE_URL, "demo_mode",  verify_ssl = CONST_SSL, port = CONST_PORT)

    def test_init(self):
        self.assertIsInstance(self.grocy, Grocy)
        
    def test_get_chores_valid(self):
        chores = self.grocy.chores(get_details=True)
        
        self.assertIsInstance(chores, list)
        self.assertEqual(len(chores), 6)
        self.assertEqual(chores[0].id, 1)

    def test_product_get_details_valid(self):
        stock = self.grocy.stock()

        product = stock[0]

        api_client = GrocyApiClient(CONST_BASE_URL, "demo_mode", port = CONST_PORT, verify_ssl = CONST_SSL)
        product.get_details(api_client)

        self.assertIsInstance(product.name, str)
        self.assertIsInstance(product.id, int)
        self.assertIsInstance(product.available_amount, float)
        self.assertIsInstance(product.best_before_date, datetime)
        if product.barcodes:
            self.assertIsInstance(product.barcodes, (list, str))
        self.assertIsInstance(product.product_group_id, int)

    @responses.activate
    def test_product_get_details_invalid_no_data(self):
        current_stock_response = CurrentStockResponse({
            "product_id": 0,
            "amount": "0.33",
            "best_before_date": "2019-05-02"
        })

        product = Product(current_stock_response)

        api_client = GrocyApiClient(CONST_BASE_URL, "demo_mode", port = CONST_PORT, verify_ssl = CONST_SSL)

        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/products/0", status=200)

        product.get_details(api_client)

        self.assertIsNone(product.name)

    def test_get_stock_valid(self):
        stock = self.grocy.stock()

        self.assertIsInstance(stock, list)
        self.assertGreaterEqual(len(stock), 10)
        for prod in stock:
            self.assertIsInstance(prod, Product)

    @responses.activate
    def test_get_stock_invalid_missing_data(self):
        resp = []
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock", json=resp, status=200)
        self.assertEqual(len(self.grocy.stock()) ,0)
        
    def test_get_shopping_list_valid(self):
        shopping_list = self.grocy.shopping_list(True)
        
        self.assertIsInstance(shopping_list, list)
        self.assertGreaterEqual(len(shopping_list), 1)
        for item in shopping_list:
            self.assertIsInstance(item, ShoppingListProduct)
            
    @responses.activate
    def test_get_shopping_list_invalid_no_data(self):
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/objects/shopping_list", status=400)
        self.assertRaises(HTTPError, self.grocy.shopping_list)
        
    @responses.activate
    def test_get_shopping_list_invalid_missing_data(self):
        resp = []
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/objects/shopping_list", json=resp, status=200)
        self.assertEqual(len(self.grocy.shopping_list()), 0)
        
    def test_add_missing_product_to_shopping_list_valid(self):
         self.assertIsNone(self.grocy.add_missing_product_to_shopping_list())
        
    @responses.activate
    def test_add_missing_product_to_shopping_list_error(self):
        responses.add(responses.POST, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/shoppinglist/add-missing-products", status=400)
        self.assertRaises(HTTPError, self.grocy.add_missing_product_to_shopping_list)
        
    def test_add_product_to_shopping_list_valid(self):
        self.grocy.add_product_to_shopping_list(22)
        
    def test_add_product_to_shopping_list_error(self):
        self.assertRaises(HTTPError, self.grocy.add_product_to_shopping_list, 3000)
        
    @responses.activate
    def test_clear_shopping_list_valid(self):
        responses.add(responses.POST, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/shoppinglist/clear", status=204)
        self.grocy.clear_shopping_list()
        
    @responses.activate
    def test_clear_shopping_list_error(self):
        responses.add(responses.POST, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/shoppinglist/clear", status=400)
        self.assertRaises(HTTPError, self.grocy.clear_shopping_list)
        
    @responses.activate
    def test_remove_product_in_shopping_list_valid(self):
        responses.add(responses.POST, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/shoppinglist/remove-product", status=204)
        self.grocy.remove_product_in_shopping_list(1)
        
    @responses.activate
    def test_remove_product_in_shopping_list_error(self):
        responses.add(responses.POST, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/shoppinglist/remove-product", status=400)
        self.assertRaises(HTTPError, self.grocy.remove_product_in_shopping_list, 1)
        
    def test_get_product_groups_valid(self):
        product_groups_list = self.grocy.product_groups()
        
        self.assertIsInstance(product_groups_list, list)
        self.assertGreaterEqual(len(product_groups_list), 1)
        for item in product_groups_list:
            self.assertIsInstance(item, Group)
            
    @responses.activate
    def test_get_product_groups_invalid_no_data(self):
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/objects/product_groups", status=400)
        self.assertRaises(HTTPError, self.grocy.product_groups)
        
    @responses.activate
    def test_get_product_groups_invalid_missing_data(self):
        resp = []
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/objects/product_groups", json=resp, status=200)
        self.assertEqual(len(self.grocy.product_groups()), 0)
        
    @responses.activate
    def test_upload_product_picture_valid(self):
        with patch("os.path.exists" ) as m_exist:
            with patch("builtins.open", mock_open()) as m_open:
                m_exist.return_value = True
                api_client = GrocyApiClient(CONST_BASE_URL, "demo_mode", port = CONST_PORT, verify_ssl = CONST_SSL)
                responses.add(responses.PUT, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/files/productpictures/MS5qcGc=", status=204)
                api_client.upload_product_picture(1,"/somepath/pic.jpg")
            
    @responses.activate
    def test_upload_product_picture_invalid_missing_data(self):
        with patch("os.path.exists" ) as m_exist:
            m_exist.return_value = False
            api_client = GrocyApiClient(CONST_BASE_URL, "demo_mode", port = CONST_PORT, verify_ssl = CONST_SSL)
            responses.add(responses.PUT, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/files/productpictures/MS5qcGc=", status=204)
            self.assertIsNone(api_client.upload_product_picture(1,"/somepath/pic.jpg"))
        
    @responses.activate
    def test_upload_product_picture_error(self):
        with patch("os.path.exists" ) as m_exist:
            with patch("builtins.open", mock_open()) as m_open:
                m_exist.return_value = True
                api_client = GrocyApiClient(CONST_BASE_URL, "demo_mode", port = CONST_PORT, verify_ssl = CONST_SSL)
                responses.add(responses.PUT, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/files/productpictures/MS5qcGc=", status=400)
                self.assertRaises(HTTPError, api_client.upload_product_picture, 1,"/somepath/pic.jpg")
                
    @responses.activate
    def test_update_product_pic_valid(self):
        api_client = GrocyApiClient(CONST_BASE_URL, "demo_mode", port = CONST_PORT, verify_ssl = CONST_SSL)
        responses.add(responses.PUT, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/objects/products/1", status=204)
        api_client.update_product_pic(1)
        
    @responses.activate
    def test_update_product_pic_error(self):
        api_client = GrocyApiClient(CONST_BASE_URL, "demo_mode", port = CONST_PORT, verify_ssl = CONST_SSL)
        responses.add(responses.PUT, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/objects/products/1", status=400)
        self.assertRaises(HTTPError, api_client.update_product_pic, 1)        
    
    def test_get_expiring_products_valid(self):
        
        expiring_product = self.grocy.expiring_products(True)

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
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/volatile", json=resp, status=200)

        self.grocy.expiring_products(True)

    @responses.activate
    def test_get_expiring_invalid_missing_data(self):
        resp = {}
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/volatile", json=resp, status=200)
        
    def test_get_expired_products_valid(self):
        
        expired_product = self.grocy.expired_products(True)

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
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/volatile", json=resp, status=200)

        self.grocy.expired_products(True)

    @responses.activate
    def test_get_expired_invalid_missing_data(self):
        resp = {}
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/volatile", json=resp, status=200)
        
    def test_get_missing_products_valid(self):

        missing_product = self.grocy.missing_products(True)

        self.assertIsInstance(missing_product, list)
        self.assertGreaterEqual(len(missing_product), 1)
        for prod in missing_product:
            self.assertIsInstance(prod, Product)

    @responses.activate
    def test_get_missing_invalid_no_data(self):
        resp = {
            "expiring_products": [],
            "expired_products": [],
            "missing_products": []
        }
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/volatile", json=resp, status=200)

        self.grocy.missing_products(True)

    @responses.activate
    def test_get_missing_invalid_missing_data(self):
        resp = {}
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/volatile", json=resp, status=200)
        
    @responses.activate
    def test_get_userfields_valid(self):
        resp =  {
                "uf1": 0,
                "uf2": "string"
            }
        
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/userfields/chores/1", json=resp, status=200)

        a_chore_uf = self.grocy.get_userfields("chores",1)

        self.assertEqual(a_chore_uf['uf1'], 0)

    def test_get_userfields_invalid_no_data(self):
        self.grocy.get_userfields("chores",1)

    @responses.activate
    def test_set_userfields_valid(self):
        responses.add(responses.PUT, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/userfields/chores/1", status=204)
        self.grocy.set_userfields("chores",1,"auserfield", "value")
        
    @responses.activate
    def test_set_userfields_error(self):
        responses.add(responses.PUT, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/userfields/chores/1", status=400)
        self.assertRaises(HTTPError, self.grocy.set_userfields, "chores",1,"auserfield","value")

    def test_get_last_db_changed_valid(self):

        timestamp = self.grocy.get_last_db_changed()

        self.assertIsInstance(timestamp, datetime)


    @responses.activate
    def test_get_last_db_changed_invalid_no_data(self):
        resp = {}
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/system/db-changed-time", json=resp ,status=200)

        self.assertIsNone(self.grocy.get_last_db_changed())
