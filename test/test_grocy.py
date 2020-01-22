from unittest import TestCase
from unittest.mock import patch, mock_open

from datetime import datetime
import responses
from pygrocy import Grocy
from pygrocy.grocy import Product
from pygrocy.grocy import Group
from pygrocy.grocy import ShoppingListProduct
from pygrocy.grocy_api_client import CurrentStockResponse, ProductData, GrocyApiClient
from test.test_const import CONST_BASE_URL, CONST_PORT, CONST_SSL

class TestGrocy(TestCase):

    def setUp(self):
        self.grocy = Grocy(CONST_BASE_URL, "api_key")
        self.grocy = None
        self.grocy = Grocy(CONST_BASE_URL, "demo_mode",  verify_ssl = CONST_SSL, port = CONST_PORT)

    def test_init(self):
        assert isinstance(self.grocy, Grocy)
        
    def test_get_chores_valid(self):
        chores = self.grocy.chores(get_details=True)
        
        assert isinstance(chores, list)
        assert len(chores) >=1
        assert isinstance(chores[0].chore_id, int)

    def test_product_get_details_valid(self):
        stock = self.grocy.stock()

        product = stock[0]

        api_client = GrocyApiClient(CONST_BASE_URL, "demo_mode", port = CONST_PORT, verify_ssl = CONST_SSL)
        product.get_details(api_client)

        assert isinstance(product.name, str)
        assert isinstance(product.product_group_id, int)

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

        assert product.name is None

    def test_get_stock_valid(self):
        stock = self.grocy.stock(True)

        assert isinstance(stock, list)
        assert len(stock) >= 10
        for prod in stock:
            assert isinstance(prod, Product)

    @responses.activate
    def test_get_stock_invalid_no_data(self):
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock", status=200)

        assert self.grocy.stock() is None

    @responses.activate
    def test_get_stock_invalid_missing_data(self):
        resp = [
            {
            }
        ]
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock", json=resp, status=200)
        
    def test_get_shopping_list_valid(self):
        shopping_list = self.grocy.shopping_list(True)
        
        assert isinstance(shopping_list, list)
        assert len(shopping_list) >= 1
        for item in shopping_list:
            assert isinstance(item, ShoppingListProduct)
            assert isinstance(item.id, int)
            assert isinstance(item.product_id, int) or item.product_id is None
            assert isinstance(item.amount, float)
            if item.product:
                assert isinstance(item.product, ProductData)
            
    @responses.activate
    def test_get_shopping_list_invalid_no_data(self):
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/objects/shopping_list", status=400)
        assert self.grocy.shopping_list() is None
        
    @responses.activate
    def test_get_shopping_list_invalid_missing_data(self):
        resp = [
            {
            }
        ]
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/objects/shopping_list", json=resp, status=200)
        
    def test_add_missing_product_to_shopping_list_valid(self):
        assert self.grocy.add_missing_product_to_shopping_list().status_code == 204
        
    @responses.activate
    def test_add_missing_product_to_shopping_list_error(self):
        responses.add(responses.POST, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/shoppinglist/add-missing-products", status=400)
        assert self.grocy.add_missing_product_to_shopping_list().status_code != 204

    def test_add_product_to_shopping_list_valid(self):
        assert self.grocy.add_product_to_shopping_list(22).status_code == 204

    def test_add_product_to_shopping_list_error(self):
        assert self.grocy.add_product_to_shopping_list(3000).status_code != 204

    def test_add_product_valid(self):
        assert self.grocy.add_product(22, 1, 1.5, datetime.now()).status_code == 200

    def test_add_product_error(self):
        assert self.grocy.add_product(3000, 1, 1.5, datetime.now()).status_code != 200

    def test_consume_product_valid(self):
        assert self.grocy.consume_product(22).status_code == 200

    def test_consume_product_error(self):
        assert self.grocy.consume_product(3000).status_code != 200

    def test_execute_chore_valid(self):
        assert self.grocy.execute_chore(1, 1, datetime.now()).status_code == 200

    def test_execute_chore_error(self):
        assert self.grocy.execute_chore(3000).status_code != 200
        
    @responses.activate
    def test_clear_shopping_list_valid(self):
        responses.add(responses.POST, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/shoppinglist/clear", status=204)
        assert self.grocy.clear_shopping_list().status_code == 204
        
    @responses.activate
    def test_clear_shopping_list_error(self):
        responses.add(responses.POST, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/shoppinglist/clear", status=400)
        assert self.grocy.clear_shopping_list().status_code != 204
        
    @responses.activate
    def test_remove_product_in_shopping_list_valid(self):
        responses.add(responses.POST, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/shoppinglist/remove-product", status=204)
        assert self.grocy.remove_product_in_shopping_list(1).status_code == 204
        
    @responses.activate
    def test_remove_product_in_shopping_list_error(self):
        responses.add(responses.POST, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/shoppinglist/remove-product", status=400)
        assert self.grocy.remove_product_in_shopping_list(1).status_code != 204
        
    def test_get_product_groups_valid(self):
        product_groups_list = self.grocy.product_groups()
        
        assert isinstance(product_groups_list, list)
        assert len(product_groups_list) >= 1
        for item in product_groups_list:
            assert isinstance(item, Group)
            
    @responses.activate
    def test_get_product_groups_invalid_no_data(self):
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/objects/product_groups", status=400)
        assert self.grocy.product_groups() is None
        
    @responses.activate
    def test_get_product_groups_invalid_missing_data(self):
        resp = [
            {
            }
        ]
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/objects/product_groups", json=resp, status=200)
        
    @responses.activate
    def test_upload_product_picture_valid(self):
        with patch("os.path.exists" ) as m_exist:
            with patch("builtins.open", mock_open()) as m_open:
                m_exist.return_value = True
                api_client = GrocyApiClient(CONST_BASE_URL, "demo_mode", port = CONST_PORT, verify_ssl = CONST_SSL)
                responses.add(responses.PUT, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/files/productpictures/MS5qcGc=", status=204)
                assert api_client.upload_product_picture(1,"/somepath/pic.jpg").status_code == 204
            
    @responses.activate
    def test_upload_product_picture_invalid_missing_data(self):
        with patch("os.path.exists" ) as m_exist:
            m_exist.return_value = False
            api_client = GrocyApiClient(CONST_BASE_URL, "demo_mode", port = CONST_PORT, verify_ssl = CONST_SSL)
            responses.add(responses.PUT, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/files/productpictures/MS5qcGc=", status=204)
            assert api_client.upload_product_picture(1,"/somepath/pic.jpg") is None
        
    @responses.activate
    def test_upload_product_picture_error(self):
        with patch("os.path.exists" ) as m_exist:
            with patch("builtins.open", mock_open()) as m_open:
                m_exist.return_value = True
                api_client = GrocyApiClient(CONST_BASE_URL, "demo_mode", port = CONST_PORT, verify_ssl = CONST_SSL)
                responses.add(responses.PUT, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/files/productpictures/MS5qcGc=", status=400)
                assert api_client.upload_product_picture(1,"/somepath/pic.jpg").status_code != 204
                
    @responses.activate
    def test_update_product_pic_valid(self):
        api_client = GrocyApiClient(CONST_BASE_URL, "demo_mode", port = CONST_PORT, verify_ssl = CONST_SSL)
        responses.add(responses.PUT, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/objects/products/1", status=204)
        assert api_client.update_product_pic(1).status_code == 204
        
    @responses.activate
    def test_update_product_pic_error(self):
        api_client = GrocyApiClient(CONST_BASE_URL, "demo_mode", port = CONST_PORT, verify_ssl = CONST_SSL)
        responses.add(responses.PUT, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/objects/products/1", status=400)
        assert api_client.update_product_pic(1).status_code != 204
        
    
    def test_get_expiring_products_valid(self):
        
        expiring_product = self.grocy.expiring_products(True)

        assert isinstance(expiring_product, list)
        assert len(expiring_product) >= 1
        for prod in expiring_product:
            assert isinstance(prod, Product)

    @responses.activate
    def test_get_expiring_invalid_no_data(self):
        resp = {
            "expiring_products": [],
            "expired_products": [],
            "missing_products": []
        }
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/volatile", json=resp, status=200)

        assert not self.grocy.expiring_products(True)

    @responses.activate
    def test_get_expiring_invalid_missing_data(self):
        resp = {}
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/volatile", json=resp, status=200)
        
    def test_get_expired_products_valid(self):
        
        expired_product = self.grocy.expired_products(True)

        assert isinstance(expired_product, list)
        assert len(expired_product) >= 1
        for prod in expired_product:
            assert isinstance(prod, Product)

    @responses.activate
    def test_get_expired_invalid_no_data(self):
        resp = {
            "expiring_products": [],
            "expired_products": [],
            "missing_products": []
        }
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/volatile", json=resp, status=200)

        assert not self.grocy.expired_products(True)

    @responses.activate
    def test_get_expired_invalid_missing_data(self):
        resp = {}
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/volatile", json=resp, status=200)
        
    def test_get_missing_products_valid(self):

        missing_product = self.grocy.missing_products(True)

        assert isinstance(missing_product, list)
        assert len(missing_product) >= 1
        for prod in missing_product:
            assert isinstance(prod, Product)

    @responses.activate
    def test_get_missing_invalid_no_data(self):
        resp = {
            "expiring_products": [],
            "expired_products": [],
            "missing_products": []
        }
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/volatile", json=resp, status=200)

        assert not self.grocy.missing_products(True)

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

        assert a_chore_uf['uf1'] == 0

    def test_get_userfields_invalid_no_data(self):
        assert not self.grocy.get_userfields("chores",1) 

    @responses.activate
    def test_set_userfields_valid(self):
        responses.add(responses.PUT, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/userfields/chores/1", status=204)
        assert self.grocy.set_userfields("chores",1,"auserfield","value").status_code == 204
        
    @responses.activate
    def test_set_userfields_error(self):
        responses.add(responses.PUT, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/userfields/chores/1", status=400)
        assert self.grocy.set_userfields("chores",1,"auserfield","value").status_code != 204
        

    def test_get_last_db_changed_valid(self):

        timestamp = self.grocy.get_last_db_changed()

        assert isinstance(timestamp, datetime)


    @responses.activate
    def test_get_last_db_changed_invalid_no_data(self):
        resp = {}
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/system/db-changed-time", json=resp ,status=200)

        assert self.grocy.get_last_db_changed() is None
