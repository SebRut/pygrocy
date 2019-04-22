import json
from urllib.parse import urljoin

import requests

from pygrocy.utils import parse_date, parse_int, parse_float


class GrocyApiClient(object):
    def __init__(self, base_url, api_key):
        self._base_url = base_url
        self._api_key = api_key
        self._headers = {
            "accept": "application/json",
            "GROCY-API-KEY": api_key
        }

    def get_stock(self):
        req_url = urljoin(self._base_url, "stock")
        resp = requests.get(req_url, headers=self._headers)
        parsed_json = json.loads(resp.text)
        return [CurrentStockResponse(response) for response in parsed_json]

    def get_volatile_stock(self):
        req_url = urljoin(self._base_url, "stock/volatile")
        resp = requests.get(req_url, headers=self._headers)
        parsed_json = json.loads(resp.text)
        return CurrentVolatilStockResponse(parsed_json)

    def get_product(self, product_id):
        req_url = urljoin(urljoin(self._base_url, "stock/products/"), str(product_id))
        resp = requests.get(req_url, headers=self._headers)
        parsed_json = json.loads(resp.text)
        return ProductDetailsResponse(parsed_json)


class CurrentVolatilStockResponse(object):
    def __init__(self, parsed_json):
        from pygrocy.grocy import Product
        self._expiring_products = [Product(product) for product in parsed_json['expiring_products']]
        self._expired_products = [Product(product) for product in parsed_json['expired_products']]
        self._missing_products = [Product(product) for product in parsed_json['missing_products']]

    @property
    def expiring_products(self):
        return self._expiring_products

    @property
    def expired_products(self):
        return self._expired_products

    @property
    def missing_products(self):
        return self._missing_products


class CurrentStockResponse(object):
    def __init__(self, parsed_json):
        self._product_id = int(parsed_json['product_id'])
        self._amount = float(parsed_json['amount'])
        self._best_before_date = parse_date(parsed_json['best_before_date'])

    @property
    def product_id(self):
        return self._product_id

    @property
    def amount(self):
        return self._amount

    @property
    def best_before_date(self):
        return self._best_before_date


class ProductDetailsResponse(object):
    def __init__(self, parsed_json):
        self._last_purchased = parse_date(parsed_json['last_purchased'])
        self._last_used = parse_date(parsed_json['last_used'])
        self._stock_amount = int(parsed_json['stock_amount'])
        self._stock_amount_opened = parse_int(parsed_json['stock_amount_opened'])
        self._next_best_before_date = parse_date(parsed_json['next_best_before_date'])
        self._last_price = parse_float(parsed_json['last_price'])

        from pygrocy.grocy import Product
        self._product = Product(parsed_json['product'])

        from pygrocy.grocy import QuantityUnit
        self._quantity_unit_purchase = QuantityUnit(parsed_json['quantity_unit_purchase'])
        self._quantity_unit_stock = QuantityUnit(parsed_json['quantity_unit_stock'])

        from pygrocy.grocy import Location
        self._location = Location(parsed_json['location'])

    @property
    def last_purchased(self):
        return self._last_purchased

    @property
    def last_used(self):
        return self._last_used

    @property
    def stock_amount(self):
        return self._stock_amount

    @property
    def stock_amount_opened(self):
        return self._stock_amount_opened

    @property
    def next_best_before_date(self):
        return self._next_best_before_date

    @property
    def last_price(self):
        return self._last_price
