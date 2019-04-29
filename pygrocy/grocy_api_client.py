from datetime import datetime
from enum import Enum
from typing import List
from urllib.parse import urljoin

import requests

from pygrocy.utils import parse_date, parse_float, parse_int


class QuantityUnitData(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json['id'])
        self._name = parsed_json['name']
        self._name_plural = parsed_json['name_plural']
        self._description = parsed_json['description']
        self._row_created_timestamp = parse_date(parsed_json['row_created_timestamp'])


class LocationData(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json['id'])
        self._name = parsed_json['name']
        self._description = parsed_json['description']
        self._row_created_timestamp = parse_date(parsed_json['row_created_timestamp'])


class ProductData(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json['id'])
        self._name = parsed_json['name']
        self._description = parsed_json.get('description', None)
        self._location_id = parse_int(parsed_json.get('location_id', None))
        self._qu_id_stock = parse_int(parsed_json.get('qu_id_stock', None))
        self._qu_id_purchase = parse_int(parsed_json.get('qu_id_purchsase', None))
        self._qu_factor_purchase_to_stock = parse_float(parsed_json.get('qu_factor_purchase_to_stock', None))
        self._barcodes = parsed_json.get('barcode', "").split(",")
        self._picture_file_name = parsed_json.get('picture_file_name', None)
        self._allow_partial_units_in_stock = bool(parsed_json.get('allow_partial_units_in_stock', None) == "true")
        self._row_created_timestamp = parse_date(parsed_json.get('row_created_timestamp', None))
        self._min_stock_amount = parse_int(parsed_json.get('min_stock_amount', None), 0)
        self._default_best_before_days = parse_int(parsed_json.get('default_best_before_days', None))

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name


class ChoreData(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json['id'])
        self._name = parsed_json['name']

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name


class UserDto(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json['id'])

        self._username = parsed_json['username']


class CurrentChoreResponse(object):
    def __init__(self, parsed_json):
        self._chore_id = parse_int(parsed_json['chore_id'], None)
        self._last_tracked_time = parse_date(parsed_json['last_tracked_time'])
        self._next_estimated_execution_time = parse_date(parsed_json['next_estimated_execution_time'])

    @property
    def chore_id(self) -> int:
        return self._chore_id

    @property
    def last_tracked_time(self) -> datetime:
        return self._last_tracked_time

    @property
    def next_estimated_execution_time(self) -> datetime:
        return self._next_estimated_execution_time


class CurrentVolatilStockResponse(object):
    def __init__(self, parsed_json):
        self._expiring_products = [ProductData(product) for product in parsed_json['expiring_products']]
        self._expired_products = [ProductData(product) for product in parsed_json['expired_products']]
        self._missing_products = [ProductData(product) for product in parsed_json['missing_products']]

    @property
    def expiring_products(self) -> List[ProductData]:
        return self._expiring_products

    @property
    def expired_products(self) -> List[ProductData]:
        return self._expired_products

    @property
    def missing_products(self) -> List[ProductData]:
        return self._missing_products


class CurrentStockResponse(object):
    def __init__(self, parsed_json):
        self._product_id = int(parsed_json['product_id'])
        self._amount = float(parsed_json['amount'])
        self._best_before_date = parse_date(parsed_json['best_before_date'])

    @property
    def product_id(self) -> int:
        return self._product_id

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def best_before_date(self) -> datetime:
        return self._best_before_date


class ProductDetailsResponse(object):
    def __init__(self, parsed_json):
        self._last_purchased = parse_date(parsed_json['last_purchased'])
        self._last_used = parse_date(parsed_json['last_used'])
        self._stock_amount = int(parsed_json['stock_amount'])
        self._stock_amount_opened = parse_int(parsed_json['stock_amount_opened'])
        self._next_best_before_date = parse_date(parsed_json['next_best_before_date'])
        self._last_price = parse_float(parsed_json['last_price'])

        self._product = ProductData(parsed_json['product'])

        self._quantity_unit_purchase = QuantityUnitData(parsed_json['quantity_unit_purchase'])
        self._quantity_unit_stock = QuantityUnitData(parsed_json['quantity_unit_stock'])

        self._location = LocationData(parsed_json['location'])

    @property
    def last_purchased(self) -> datetime:
        return self._last_purchased

    @property
    def last_used(self) -> datetime:
        return self._last_used

    @property
    def stock_amount(self) -> int:
        return self._stock_amount

    @property
    def stock_amount_opened(self) -> int:
        return self._stock_amount_opened

    @property
    def next_best_before_date(self) -> datetime:
        return self._next_best_before_date

    @property
    def last_price(self) -> float:
        return self._last_price

    @property
    def product(self) -> ProductData:
        return self._product


class ChoreDetailsResponse(object):
    def __init__(self, parsed_json):
        self._chore = ChoreData(parsed_json['chore'])
        self._last_done_by = UserDto(parsed_json['last_done_by'])

    @property
    def chore(self) -> ChoreData:
        return self._chore


class TransactionType(Enum):
    PURCHASE = "purchase"
    CONSUME = "consume"
    INVENTORY_CORRECTION = "inventory-correction"
    PRODUCT_OPENED = "product-opened"


class GrocyApiClient(object):
    def __init__(self, base_url, api_key):
        self._base_url = base_url
        self._api_key = api_key
        self._headers = {
            "accept": "application/json",
            "GROCY-API-KEY": api_key
        }

    def get_stock(self) -> List[CurrentStockResponse]:
        req_url = urljoin(self._base_url, "stock")
        resp = requests.get(req_url, headers=self._headers)
        parsed_json = resp.json()
        return [CurrentStockResponse(response) for response in parsed_json]

    def get_volatile_stock(self) -> CurrentVolatilStockResponse:
        req_url = urljoin(self._base_url, "stock/volatile")
        resp = requests.get(req_url, headers=self._headers)
        parsed_json = resp.json()
        return CurrentVolatilStockResponse(parsed_json)

    def get_product(self, product_id) -> ProductDetailsResponse:
        req_url = urljoin(urljoin(self._base_url, "stock/products/"), str(product_id))
        resp = requests.get(req_url, headers=self._headers)
        parsed_json = resp.json()
        return ProductDetailsResponse(parsed_json)

    def get_chores(self) -> List[CurrentChoreResponse]:
        req_url = urljoin(self._base_url, "chores")
        resp = requests.get(req_url, headers=self._headers)
        parsed_json = resp.json()
        return [CurrentChoreResponse(chore) for chore in parsed_json]

    def get_chore(self, chore_id: int) -> ChoreDetailsResponse:
        req_url = urljoin(urljoin(self._base_url, "chores/"), str(chore_id))
        resp = requests.get(req_url, headers=self._headers)
        parsed_json = resp.json()
        return ChoreDetailsResponse(parsed_json)

    def add_product(self, product_id, amount: float, price: float, best_before_date: datetime = None,
                    transaction_type: TransactionType = TransactionType.PURCHASE):
        data = {
            "amount": amount,
            "transaction_type": transaction_type.value,
            "price": price
        }

        if best_before_date is not None:
            data["best_before_date"] = best_before_date.isoformat()

        req_url = urljoin(urljoin(urljoin(self._base_url, "stock/products/"), str(product_id) + "/"), "add")
        requests.post(req_url, headers=self._headers, data=data)

    def consume_product(self, product_id: int, amount: float = 1, spoiled: bool = False,
                        transaction_type: TransactionType = TransactionType.CONSUME):
        data = {
            "amount": amount,
            "spoiled": spoiled,
            "transaction_type": transaction_type.value
        }

        req_url = urljoin(urljoin(urljoin(self._base_url, "stock/products/"), str(product_id) + "/"), "consume")
        requests.post(req_url, headers=self._headers, data=data)
