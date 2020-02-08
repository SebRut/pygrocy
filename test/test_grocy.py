from unittest import TestCase
from unittest.mock import patch, mock_open
import unittest

import os
from datetime import datetime
from typing import List
import responses
from pygrocy import Grocy
from pygrocy.grocy import Product
from pygrocy.grocy import Group
from pygrocy.grocy import ShoppingListProduct
from pygrocy.grocy import Chore
from pygrocy.grocy_api_client import CurrentStockResponse, ProductData, GrocyApiClient, UserDto
from test.test_const import CONST_BASE_URL, CONST_PORT, CONST_SSL, SKIP_REAL


class TestGrocy(TestCase):

    def setUp(self):
        self.grocy = Grocy(CONST_BASE_URL, "api_key")
        self.grocy = None
        self.grocy = Grocy(CONST_BASE_URL, "demo_mode",  verify_ssl = CONST_SSL, port = CONST_PORT)

    def test_init(self):
        assert isinstance(self.grocy, Grocy)

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
    def test_get_chores_valid(self):
        chores = self.grocy.chores(get_details=True)
        
        assert isinstance(chores, list)
        assert len(chores) >=1
        for chore in chores:
            assert isinstance(chore, Chore)
            assert isinstance(chore.chore_id, int)
            assert isinstance(chore.last_tracked_time, datetime)
            assert isinstance(chore.next_estimated_execution_time, datetime)
            assert isinstance(chore.name, str)
            assert isinstance(chore.last_done_by, UserDto)

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
    def test_product_get_details_valid(self):
        product = self.grocy.product(5)

        assert isinstance(product.product.name, str)
        assert isinstance(product.product.product_group_id, int)

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

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
    def test_get_stock_valid(self):
        stock = self.grocy.stock(True)

        assert isinstance(stock, list)
        assert len(stock) >= 10
        for prod in stock:
            assert isinstance(prod, Product)
            assert isinstance(prod.available_amount, float)
            assert isinstance(prod.best_before_date, datetime)
            assert isinstance(prod.barcodes, List) or prod.barcodes is None
            assert isinstance(prod.product_group_id, int)

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

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
    def test_get_shopping_list_valid(self):
        shopping_list = self.grocy.shopping_list(True)
        
        assert isinstance(shopping_list, list)
        assert len(shopping_list) >= 1
        for item in shopping_list:
            assert isinstance(item, ShoppingListProduct)
            assert isinstance(item.id, int)
            assert isinstance(item.product_id, int) or item.product_id is None
            assert isinstance(item.note, str) or item.note is None
            assert isinstance(item.amount, float)
            if item.product:
                assert isinstance(item.product, ProductData)
                assert isinstance(item.product.id, int)
            
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

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
    def test_add_missing_product_to_shopping_list_valid(self):
        assert self.grocy.add_missing_product_to_shopping_list().status_code == 204
        
    @responses.activate
    def test_add_missing_product_to_shopping_list_error(self):
        responses.add(responses.POST, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/shoppinglist/add-missing-products", status=400)
        assert self.grocy.add_missing_product_to_shopping_list().status_code != 204

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
    def test_add_product_to_shopping_list_valid(self):
        assert self.grocy.add_product_to_shopping_list(22).status_code == 204

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
    def test_add_product_to_shopping_list_error(self):
        assert self.grocy.add_product_to_shopping_list(3000).status_code != 204

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
    def test_add_product_valid(self):
        assert self.grocy.add_product(22, 1, 1.5, datetime.now()).status_code == 200

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
    def test_add_product_error(self):
        assert self.grocy.add_product(3000, 1, 1.5, datetime.now()).status_code != 200

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
    def test_consume_product_valid(self):
        assert self.grocy.consume_product(22).status_code == 200

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
    def test_consume_product_error(self):
        assert self.grocy.consume_product(3000).status_code != 200

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
    def test_execute_chore_valid(self):
        assert self.grocy.execute_chore(1, 1, datetime.now()).status_code == 200

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
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

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
    def test_get_product_groups_valid(self):
        product_groups_list = self.grocy.product_groups()
        
        assert isinstance(product_groups_list, list)
        assert len(product_groups_list) >= 1
        for item in product_groups_list:
            assert isinstance(item, Group)
            assert isinstance(item.id, int)
            assert isinstance(item.name, str)
            assert isinstance(item.description, str) or item.description is None
            
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
        
    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
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

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
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

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
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

    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
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
        
    @unittest.skipIf(SKIP_REAL == 'True', 'Skipping tests that hit the real API server.')
    def test_get_last_db_changed_valid(self):

        timestamp = self.grocy.get_last_db_changed()

        assert isinstance(timestamp, datetime)

    @responses.activate
    def test_get_last_db_changed_invalid_no_data(self):
        resp = {}
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/system/db-changed-time", json=resp ,status=200)

        assert self.grocy.get_last_db_changed() is None

    @unittest.skipUnless(SKIP_REAL == 'True', 'Skipping mock tests.')
    @responses.activate
    def test_get_chores_valid_no_details_mock(self):
        resp = [
            {
                "chore_id": "1",
                "last_tracked_time": "2019-11-18 00:00:00",
                "next_estimated_execution_time": "2019-11-25 00:00:00",
                "track_date_only": "1"
            },
            {
                "chore_id": "2",
                "last_tracked_time": "2019-11-16 00:00:00",
                "next_estimated_execution_time": "2019-11-23 00:00:00",
                "track_date_only": "1"
            },
            {
                "chore_id": "3",
                "last_tracked_time": "2019-11-10 00:00:00",
                "next_estimated_execution_time": "2019-12-10 00:00:00",
                "track_date_only": "1"
            },
            {
                "chore_id": "4",
                "last_tracked_time": "2019-11-18 00:00:00",
                "next_estimated_execution_time": "2019-11-25 00:00:00",
                "track_date_only": "1",
            }
        ]
        
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/chores", json=resp, status=200)
        chores = self.grocy.chores(get_details=False)
        
        assert isinstance(chores, list)
        assert len(chores) == 4
        assert chores[0].chore_id == 1
        assert chores[1].chore_id == 2
        assert chores[2].chore_id == 3
        assert chores[3].chore_id == 4
        
    @unittest.skipUnless(SKIP_REAL == 'True', 'Skipping mock tests.')
    @responses.activate
    def test_product_get_details_valid_mock(self):
        current_stock_response = CurrentStockResponse({
            "product_id": 0,
            "amount": "0.33",
            "best_before_date": "2019-05-02"
        })
        product = Product(current_stock_response)

        api_client = GrocyApiClient(CONST_BASE_URL, "demo_mode", port = CONST_PORT, verify_ssl = CONST_SSL)

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
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/products/0", json=resp, status=200)

        product.get_details(api_client)

        assert product.name == "string"
        assert product.product_group_id == 0

    @unittest.skipUnless(SKIP_REAL == 'True', 'Skipping mock tests.')
    @responses.activate
    def test_get_stock_valid_mock(self):
        resp = [
            {
                "product_id": 0,
                "amount": "0.33",
                "best_before_date": "2019-05-02"
            }
        ]
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock", json=resp, status=200)

        stock = self.grocy.stock()

        assert isinstance(stock, list)
        assert len(stock) == 1
        for prod in stock:
            assert isinstance(prod, Product)

    @unittest.skipUnless(SKIP_REAL == 'True', 'Skipping mock tests.')
    @responses.activate
    def test_get_shopping_list_valid_mock(self):
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
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/objects/shopping_list", json=resp, status=200)

        shopping_list = self.grocy.shopping_list()
        
        assert isinstance(shopping_list, list)
        assert len(shopping_list) == 1
        for item in shopping_list:
            assert isinstance(item, ShoppingListProduct)
            
    @unittest.skipUnless(SKIP_REAL == 'True', 'Skipping mock tests.')
    @responses.activate
    def test_add_missing_product_to_shopping_list_valid_mock(self):
        responses.add(responses.POST, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/shoppinglist/add-missing-products", status=204)
        assert self.grocy.add_missing_product_to_shopping_list().status_code == 204
        
    @unittest.skipUnless(SKIP_REAL == 'True', 'Skipping mock tests.')
    @responses.activate
    def test_add_product_to_shopping_list_valid_mock(self):
        responses.add(responses.POST, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/shoppinglist/add-product", status=204)
        assert self.grocy.add_product_to_shopping_list(1).status_code == 204

    @unittest.skipUnless(SKIP_REAL == 'True', 'Skipping mock tests.')
    @responses.activate
    def test_add_product_to_shopping_list_error_mock(self):
        responses.add(responses.POST, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/shoppinglist/add-product", status=400)
        assert self.grocy.add_product_to_shopping_list(1).status_code != 204

    @unittest.skipUnless(SKIP_REAL == 'True', 'Skipping mock tests.')
    @responses.activate
    def test_get_product_groups_valid_mock(self):
        resp = [
            {
                "id": 1,
                "name": "string",
                "description": "string",
                "row_created_timestamp": "2019-04-17 10:30:00",
            }
        ]
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/objects/product_groups", json=resp, status=200)
        product_groups_list = self.grocy.product_groups()
        
        assert isinstance(product_groups_list, list)
        assert len(product_groups_list) == 1
        for item in product_groups_list:
            assert isinstance(item, Group)
            
    @unittest.skipUnless(SKIP_REAL == 'True', 'Skipping mock tests.')
    @responses.activate
    def test_get_expiring_products_valid_mock(self):
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
        
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/volatile", json=resp, status=200)

        expiring_product = self.grocy.expiring_products()

        assert isinstance(expiring_product, list)
        assert len(expiring_product) == 1
        for prod in expiring_product:
            assert isinstance(prod, Product)

    @unittest.skipUnless(SKIP_REAL == 'True', 'Skipping mock tests.')
    @responses.activate
    def test_get_expired_products_valid_mock(self):
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
        
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/volatile", json=resp, status=200)

        expired_product = self.grocy.expired_products()

        assert isinstance(expired_product, list)
        assert len(expired_product) == 1
        for prod in expired_product:
            assert isinstance(prod, Product)

    @unittest.skipUnless(SKIP_REAL == 'True', 'Skipping mock tests.')
    @responses.activate
    def test_get_missing_products_valid_mock(self):
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
        
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/stock/volatile", json=resp, status=200)

        missing_product = self.grocy.missing_products()

        assert isinstance(missing_product, list)
        assert len(missing_product) == 1
        for prod in missing_product:
            assert isinstance(prod, Product)


    @unittest.skipUnless(SKIP_REAL == 'True', 'Skipping mock tests.')
    @responses.activate
    def test_get_userfields_invalid_no_data_mock(self):
        resp = []
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/userfields/chores/1", json=resp ,status=200)

        assert not self.grocy.get_userfields("chores",1) 


    @unittest.skipUnless(SKIP_REAL == 'True', 'Skipping mock tests.')
    @responses.activate
    def test_get_last_db_changed_valid_mock(self):
        resp =  { "changed_time": "2019-09-18T05:30:58.598Z" }
        
        responses.add(responses.GET, '{}:{}'.format(CONST_BASE_URL,CONST_PORT) + "/api/system/db-changed-time", json=resp, status=200)

        timestamp = self.grocy.get_last_db_changed()

        assert isinstance(timestamp, datetime)
