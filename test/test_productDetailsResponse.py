import json
from unittest import TestCase

from pygrocy.grocy_api_client import ProductDetailsResponse


class TestProductDetailsResponse(TestCase):
    def test_barcode_null(self):
        input_json = """{ "product": { "id": 0, "name": "string", "description": "string", "location_id": 0, "qu_id_purchase": 0, "qu_id_stock": 0, "qu_factor_purchase_to_stock": 0, "barcode": null, "min_stock_amount": 0, "default_best_before_days": 0, "picture_file_name": "string", "allow_partial_units_in_stock": true, "row_created_timestamp": "2019-04-22T09:54:15.835Z" }, "quantity_unit_purchase": { "id": 0, "name": "string", "name_plural": "string", "description": "string", "row_created_timestamp": "2019-04-22T09:54:15.835Z" }, "quantity_unit_stock": { "id": 0, "name": "string", "name_plural": "string", "description": "string", "row_created_timestamp": "2019-04-22T09:54:15.835Z" }, "last_purchased": "2019-04-22", "last_used": "2019-04-22T09:54:15.835Z", "stock_amount": 10, "stock_amount_opened": 2, "next_best_before_date": "2019-04-22T09:54:15.835Z", "last_price": 0, "location": { "id": 0, "name": "string", "description": "string", "row_created_timestamp": "2019-04-22T09:54:15.835Z" } }"""
        response = ProductDetailsResponse(json.loads(input_json))

        assert len(response.barcodes) == 0

    def test_parse(self):
        input_json = """{ "product_barcodes": [{"barcode":"string"},{"barcode":"123"}], "product": { "id": 0, "name": "string", "description": "string", "location_id": 0, "product_group_id": 0, "qu_id_purchase": 0, "qu_id_stock": 0, "qu_factor_purchase_to_stock": 0, "barcode": "string,123", "min_stock_amount": 0, "default_best_before_days": 0, "picture_file_name": "string", "allow_partial_units_in_stock": true, "row_created_timestamp": "2019-04-22T09:54:15.835Z" }, "quantity_unit_purchase": { "id": 0, "name": "string", "name_plural": "string", "description": "string", "row_created_timestamp": "2019-04-22T09:54:15.835Z" }, "quantity_unit_stock": { "id": 0, "name": "string", "name_plural": "string", "description": "string", "row_created_timestamp": "2019-04-22T09:54:15.835Z" }, "last_purchased": "2019-04-22", "last_used": "2019-04-22T09:54:15.835Z", "stock_amount": 10, "stock_amount_opened": 2, "next_best_before_date": "2019-04-22T09:54:15.835Z", "last_price": 0, "location": { "id": 0, "name": "string", "description": "string", "row_created_timestamp": "2019-04-22T09:54:15.835Z" } }"""
        response = ProductDetailsResponse(json.loads(input_json))

        assert response.stock_amount == 10
        assert response.stock_amount_opened == 2
        assert response.last_price == 0
        assert response.product.product_group_id == 0

        assert response.next_best_before_date.year == 2019
        assert response.next_best_before_date.month == 4
        assert response.next_best_before_date.day == 22
        assert response.next_best_before_date.hour == 9
        assert response.next_best_before_date.minute == 54
        assert response.next_best_before_date.second == 15

        assert response.last_used.year == 2019
        assert response.last_used.month == 4
        assert response.last_used.day == 22
        assert response.last_used.hour == 9
        assert response.last_used.minute == 54
        assert response.last_used.second == 15

        assert response.last_purchased.year == 2019
        assert response.last_purchased.month == 4
        assert response.last_purchased.day == 22

        assert [barcode.barcode for barcode in response.barcodes] == ["string", "123"]
