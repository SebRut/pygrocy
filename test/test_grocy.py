from unittest import TestCase
from unittest.mock import patch, mock_open
from io import FileIO
import responses
from pygrocy import Grocy
from pygrocy.grocy import Product
from pygrocy.grocy import Group
from pygrocy.grocy import ShoppingListProduct
from pygrocy.grocy_api_client import CurrentStockResponse, GrocyApiClient


class TestGrocy(TestCase):
    def setUp(self):
        self.grocy = Grocy("https://example.com/api/", "api_key")

    def test_init(self):
        assert isinstance(self.grocy, Grocy)

    @responses.activate
    def test_product_get_details_valid(self):
        current_stock_response = CurrentStockResponse({
            "product_id": 0,
            "amount": "0.33",
            "best_before_date": "2019-05-02"
        })
        product = Product(current_stock_response)

        api_client = GrocyApiClient("https://example.com/api/", "api_key")

        resp = {
            "product": {
                "id": 0,
                "name": "string",
                "description": "string",
                "location_id": 0,
                "qu_id_purchase": 0,
                "qu_id_stock": 0,
                "qu_factor_purchase_to_stock": 0,
                "barcode": "string",
                "product_group_id": 0,
                "min_stock_amount": 0,
                "default_best_before_days": 0,
                "picture_file_name": "string",
                "allow_partial_units_in_stock": True,
                "row_created_timestamp": "2019-05-02T18:30:48.041Z"
            },
            "quantity_unit_purchase": {
                "id": 0,
                "name": "string",
                "name_plural": "string",
                "description": "string",
                "row_created_timestamp": "2019-05-02T18:30:48.041Z"
            },
            "quantity_unit_stock": {
                "id": 0,
                "name": "string",
                "name_plural": "string",
                "description": "string",
                "row_created_timestamp": "2019-05-02T18:30:48.041Z"
            },
            "last_purchased": "2019-05-02",
            "last_used": "2019-05-02T18:30:48.041Z",
            "stock_amount": 0,
            "stock_amount_opened": 0,
            "next_best_before_date": "2019-05-02T18:30:48.041Z",
            "last_price": 0,
            "location": {
                "id": 0,
                "name": "string",
                "description": "string",
                "row_created_timestamp": "2019-05-02T18:30:48.041Z"
            }
        }
        responses.add(responses.GET, "https://example.com/api/stock/products/0", json=resp, status=200)

        product.get_details(api_client)

        assert product.name == "string"
        assert product.product_group_id == 0

    @responses.activate
    def test_product_get_details_invalid_no_data(self):
        current_stock_response = CurrentStockResponse({
            "product_id": 0,
            "amount": "0.33",
            "best_before_date": "2019-05-02"
        })
        product = Product(current_stock_response)

        api_client = GrocyApiClient("https://example.com/api/", "api_key")

        responses.add(responses.GET, "https://example.com/api/stock/products/0", status=200)

        product.get_details(api_client)

        assert product.name is None

    @responses.activate
    def test_get_stock_valid(self):
        resp = [
            {
                "product_id": 0,
                "amount": "0.33",
                "best_before_date": "2019-05-02"
            }
        ]
        responses.add(responses.GET, "https://example.com/api/stock", json=resp, status=200)

        stock = self.grocy.stock()

        assert isinstance(stock, list)
        assert len(stock) == 1
        for prod in stock:
            assert isinstance(prod, Product)

    @responses.activate
    def test_get_stock_invalid_no_data(self):
        responses.add(responses.GET, "https://example.com/api/stock", status=200)

        assert self.grocy.stock() is None

    @responses.activate
    def test_get_stock_invalid_missing_data(self):
        resp = [
            {
            }
        ]
        responses.add(responses.GET, "https://example.com/api/stock", json=resp, status=200)
        
    @responses.activate
    def test_get_shopping_list_valid(self):
        resp = [
            {
                "id": 1,
                "product_id": 6,
                "note": "string",
                "amount": 2,
                "row_created_timestamp": "2019-04-17 10:30:00",
                "shopping_list_id": 1,
                "done": 0
            }
        ]
        responses.add(responses.GET, "https://example.com/api/objects/shopping_list", json=resp, status=200)

        shopping_list = self.grocy.shopping_list()
        
        assert isinstance(shopping_list, list)
        assert len(shopping_list) == 1
        for item in shopping_list:
            assert isinstance(item, ShoppingListProduct)
            
    @responses.activate
    def test_get_shopping_list_invalid_no_data(self):
        responses.add(responses.GET, "https://example.com/api/objects/shopping_list", status=400)
        assert self.grocy.shopping_list() is None
        
    @responses.activate
    def test_get_shopping_list_invalid_missing_data(self):
        resp = [
            {
            }
        ]
        responses.add(responses.GET, "https://example.com/api/objects/shopping_list", json=resp, status=200)
        
    @responses.activate
    def test_add_missing_product_to_shopping_list_valid(self):
        responses.add(responses.POST, "https://example.com/api/stock/shoppinglist/add-missing-products", status=204)
        assert self.grocy.add_missing_product_to_shopping_list().status_code == 204
        
    @responses.activate
    def test_add_missing_product_to_shopping_list_error(self):
        responses.add(responses.POST, "https://example.com/api/stock/shoppinglist/add-missing-products", status=400)
        assert self.grocy.add_missing_product_to_shopping_list().status_code != 204
        
    @responses.activate
    def test_clear_shopping_list_valid(self):
        responses.add(responses.POST, "https://example.com/api/stock/shoppinglist/clear", status=204)
        assert self.grocy.clear_shopping_list().status_code == 204
        
    @responses.activate
    def test_clear_shopping_list_error(self):
        responses.add(responses.POST, "https://example.com/api/stock/shoppinglist/clear", status=400)
        assert self.grocy.clear_shopping_list().status_code != 204
        
    @responses.activate
    def test_remove_product_in_shopping_list_valid(self):
        responses.add(responses.DELETE, "https://example.com/api/objects/shopping_list/1", status=204)
        assert self.grocy.remove_product_in_shopping_list(1).status_code == 204
        
    @responses.activate
    def test_remove_product_in_shopping_list_error(self):
        responses.add(responses.DELETE, "https://example.com/api/objects/shopping_list/1", status=400)
        assert self.grocy.remove_product_in_shopping_list(1).status_code != 204
        
    @responses.activate
    def test_get_product_groups_valid(self):
        resp = [
            {
                "id": 1,
                "name": "string",
                "description": "string",
                "row_created_timestamp": "2019-04-17 10:30:00",
            }
        ]
        responses.add(responses.GET, "https://example.com/api/objects/product_groups", json=resp, status=200)
        product_groups_list = self.grocy.product_groups()
        
        assert isinstance(product_groups_list, list)
        assert len(product_groups_list) == 1
        for item in product_groups_list:
            assert isinstance(item, Group)
            
    @responses.activate
    def test_get_product_groups_invalid_no_data(self):
        responses.add(responses.GET, "https://example.com/api/objects/product_groups", status=400)
        assert self.grocy.product_groups() is None
        
    @responses.activate
    def test_get_product_groups_invalid_missing_data(self):
        resp = [
            {
            }
        ]
        responses.add(responses.GET, "https://example.com/api/objects/product_groups", json=resp, status=200)
        
    @responses.activate
    def test_upload_product_picture_valid(self):
        with patch("os.path.exists" ) as m_exist:
            with patch("builtins.open", mock_open()) as m_open:
                m_exist.return_value = True
                api_client = GrocyApiClient("https://example.com/api/", "api_key")
                responses.add(responses.PUT, "https://example.com/api/files/productpictures/MS5qcGc=", status=204)
                assert api_client.upload_product_picture(1,"/somepath/pic.jpg").status_code == 204
            
    @responses.activate
    def test_upload_product_picture_invalid_missing_data(self):
        with patch("os.path.exists" ) as m_exist:
            m_exist.return_value = False
            api_client = GrocyApiClient("https://example.com/api/", "api_key")
            responses.add(responses.PUT, "https://example.com/api/files/productpictures/MS5qcGc=", status=204)
            assert api_client.upload_product_picture(1,"/somepath/pic.jpg") is None
        
    @responses.activate
    def test_upload_product_picture_error(self):
        with patch("os.path.exists" ) as m_exist:
            with patch("builtins.open", mock_open()) as m_open:
                m_exist.return_value = True
                api_client = GrocyApiClient("https://example.com/api/", "api_key")
                responses.add(responses.PUT, "https://example.com/api/files/productpictures/MS5qcGc=", status=400)
                assert api_client.upload_product_picture(1,"/somepath/pic.jpg").status_code != 204
                
    @responses.activate
    def test_update_product_pic_valid(self):
        api_client = GrocyApiClient("https://example.com/api/", "api_key")
        responses.add(responses.PUT, "https://example.com/api/objects/products/1", status=204)
        assert api_client.update_product_pic(1).status_code == 204
        
    @responses.activate
    def test_update_product_pic_error(self):
        api_client = GrocyApiClient("https://example.com/api/", "api_key")
        responses.add(responses.PUT, "https://example.com/api/objects/products/1", status=400)
        assert api_client.update_product_pic(1).status_code != 204
        
    @responses.activate
    def test_get_expiring_products_valid(self):
        resp = {
            "expiring_products" : [
                {
                    "product_id": 0,
                    "amount": "0.33",
                    "best_before_date": "2019-05-02",
                    "amount_opened": "0"
                }
            ],
            "expired_products": [],
            "missing_products": []
        }
        
        responses.add(responses.GET, "https://example.com/api/stock/volatile", json=resp, status=200)

        eg_product = self.grocy.expiring_products()

        assert isinstance(eg_product, list)
        assert len(eg_product) == 1
        for prod in eg_product:
            assert isinstance(prod, Product)

    @responses.activate
    def test_get_expiring_invalid_no_data(self):
        resp = {
            "expiring_products": [],
            "expired_products": [],
            "missing_products": []
        }
        responses.add(responses.GET, "https://example.com/api/stock/volatile", json=resp, status=200)

        assert not self.grocy.expiring_products()

    @responses.activate
    def test_get_expiring_invalid_missing_data(self):
        resp = {}
        responses.add(responses.GET, "https://example.com/api/stock/volatile", json=resp, status=200)
        
    @responses.activate
    def test_get_expired_products_valid(self):
        resp = {
            "expired_products" : [
                {
                    "product_id": 0,
                    "amount": "0.33",
                    "best_before_date": "2019-05-02",
                    "amount_opened": "0"
                }
            ],
            "expiring_products": [],
            "missing_products": []
        }
        
        responses.add(responses.GET, "https://example.com/api/stock/volatile", json=resp, status=200)

        ed_product = self.grocy.expired_products()

        assert isinstance(ed_product, list)
        assert len(ed_product) == 1
        for prod in ed_product:
            assert isinstance(prod, Product)

    @responses.activate
    def test_get_expired_invalid_no_data(self):
        resp = {
            "expiring_products": [],
            "expired_products": [],
            "missing_products": []
        }
        responses.add(responses.GET, "https://example.com/api/stock/volatile", json=resp, status=200)

        assert not self.grocy.expired_products()

    @responses.activate
    def test_get_expired_invalid_missing_data(self):
        resp = {}
        responses.add(responses.GET, "https://example.com/api/stock/volatile", json=resp, status=200)
        
    @responses.activate
    def test_get_missing_products_valid(self):
        resp = {
            "missing_products" : [
                {
                    "product_id": 0,
                    "amount": "0.33",
                    "best_before_date": "2019-05-02",
                    "amount_opened": "0"
                }
            ],
            "expired_products": [],
            "expiring_products": []
        }
        
        responses.add(responses.GET, "https://example.com/api/stock/volatile", json=resp, status=200)

        m_product = self.grocy.missing_products()

        assert isinstance(m_product, list)
        assert len(m_product) == 1
        for prod in m_product:
            assert isinstance(prod, Product)

    @responses.activate
    def test_get_missing_invalid_no_data(self):
        resp = {
            "expiring_products": [],
            "expired_products": [],
            "missing_products": []
        }
        responses.add(responses.GET, "https://example.com/api/stock/volatile", json=resp, status=200)

        assert not self.grocy.missing_products()

    @responses.activate
    def test_get_stock_invalid_missing_data(self):
        resp = {}
        responses.add(responses.GET, "https://example.com/api/stock/volatile", json=resp, status=200)
        
        