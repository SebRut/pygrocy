from datetime import datetime
from enum import Enum
from typing import List
from urllib.parse import urljoin

import requests

from pygrocy.utils import parse_date, parse_float, parse_int

class ShoppingListItem(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json.get('id'))
        self._product_id = parse_int(parsed_json.get('product_id'))
        self._note = parsed_json.get('note',None)
        self._amount = parse_float(parsed_json.get('amount'),0)
        self._row_created_timestamp = parse_date(parsed_json.get('row_created_timestamp', None))
        self._shopping_list_id = parse_int(parsed_json.get('shopping_list_id'))
        self._done = parse_int(parsed_json.get('done'))


    @property
    def id(self) -> int:
        return self._id
    
    @property
    def product_id(self) -> int:
        return self._product_id

    @property
    def note(self) -> str:
        return self._note

    @property
    def amount(self) -> float:
        return self._amount

class QuantityUnitData(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json.get('id'))
        self._name = parsed_json.get('name')
        self._name_plural = parsed_json.get('name_plural')
        self._description = parsed_json.get('description')
        self._row_created_timestamp = parse_date(parsed_json.get('row_created_timestamp'))


class LocationData(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json.get('id'))
        self._name = parsed_json.get('name')
        self._description = parsed_json.get('description')
        self._row_created_timestamp = parse_date(parsed_json.get('row_created_timestamp'))


class ProductData(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json.get('id'))
        self._name = parsed_json.get('name')
        self._description = parsed_json.get('description', None)
        self._location_id = parse_int(parsed_json.get('location_id', None))
        self._qu_id_stock = parse_int(parsed_json.get('qu_id_stock', None))
        self._qu_id_purchase = parse_int(parsed_json.get('qu_id_purchsase', None))
        self._qu_factor_purchase_to_stock = parse_float(parsed_json.get('qu_factor_purchase_to_stock', None))
        self._picture_file_name = parsed_json.get('picture_file_name', None)
        self._allow_partial_units_in_stock = bool(parsed_json.get('allow_partial_units_in_stock', None) == "true")
        self._row_created_timestamp = parse_date(parsed_json.get('row_created_timestamp', None))
        self._min_stock_amount = parse_int(parsed_json.get('min_stock_amount', None), 0)
        self._default_best_before_days = parse_int(parsed_json.get('default_best_before_days', None))

        barcodes_raw = parsed_json.get('barcode', "")
        if barcodes_raw is None:
            self._barcodes = None
        else:
            self._barcodes = barcodes_raw.split(",")


    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def barcodes(self) -> List[str]:
        return self._barcodes


class ChoreData(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json.get('id'))
        self._name = parsed_json.get('name')

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name


class UserDto(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json.get('id'))

        self._username = parsed_json.get('username')
        self._first_name = parsed_json.get('first_name')
        self._last_name = parsed_json.get('last_name')
        self._display_name = parsed_json.get('display_name')

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self) -> str:
        return self._username

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def display_name(self) -> str:
        return self._display_name


class CurrentChoreResponse(object):
    def __init__(self, parsed_json):
        self._chore_id = parse_int(parsed_json.get('chore_id'), None)
        self._last_tracked_time = parse_date(parsed_json.get('last_tracked_time'))
        self._next_estimated_execution_time = parse_date(parsed_json.get('next_estimated_execution_time'))

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
        self._expiring_products = [ProductData(product) for product in parsed_json.get('expiring_products')]
        self._expired_products = [ProductData(product) for product in parsed_json.get('expired_products')]
        self._missing_products = [ProductData(product) for product in parsed_json.get('missing_products')]

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
        self._product_id = parse_int(parsed_json.get('product_id'))
        self._amount = parse_float(parsed_json.get('amount'))
        self._best_before_date = parse_date(parsed_json.get('best_before_date'))

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
        self._last_purchased = parse_date(parsed_json.get('last_purchased'))
        self._last_used = parse_date(parsed_json.get('last_used'))
        self._stock_amount = parse_int(parsed_json.get('stock_amount'))
        self._stock_amount_opened = parse_int(parsed_json.get('stock_amount_opened'))
        self._next_best_before_date = parse_date(parsed_json.get('next_best_before_date'))
        self._last_price = parse_float(parsed_json.get('last_price'))

        self._product = ProductData(parsed_json.get('product'))

        self._quantity_unit_purchase = QuantityUnitData(parsed_json.get('quantity_unit_purchase'))
        self._quantity_unit_stock = QuantityUnitData(parsed_json.get('quantity_unit_stock'))

        self._location = LocationData(parsed_json.get('location'))

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
        self._chore = ChoreData(parsed_json.get('chore'))
        self._last_tracked = parse_date(parsed_json.get('last_tracked'))

        if self._last_tracked is None:
            self._last_done_by = None
        else:
            self._last_done_by = UserDto(parsed_json.get('last_done_by'))

    @property
    def chore(self) -> ChoreData:
        return self._chore

    @property
    def last_done_by(self) -> UserDto:
        return self._last_done_by

    @property
    def last_tracked(self) -> datetime:
        return self._last_tracked


class TransactionType(Enum):
    PURCHASE = "purchase"
    CONSUME = "consume"
    INVENTORY_CORRECTION = "inventory-correction"
    PRODUCT_OPENED = "product-opened"


class GrocyApiClient(object):
    def __init__(self, base_url, api_key, verify_ssl = True):
        self._base_url = base_url
        self._api_key = api_key
        self._verify_ssl = verify_ssl
        self._headers = {
            "accept": "application/json",
            "GROCY-API-KEY": api_key
        }

    def get_stock(self) -> List[CurrentStockResponse]:
        req_url = urljoin(self._base_url, "stock")
        resp = requests.get(req_url, verify=self._verify_ssl, headers=self._headers)
        if resp.status_code != 200 or not resp.text:
            return
        parsed_json = resp.json()
        return [CurrentStockResponse(response) for response in parsed_json]

    def get_volatile_stock(self) -> CurrentVolatilStockResponse:
        req_url = urljoin(self._base_url, "stock/volatile")
        resp = requests.get(req_url, verify=self._verify_ssl, headers=self._headers)
        parsed_json = resp.json()
        return CurrentVolatilStockResponse(parsed_json)

    def get_product(self, product_id) -> ProductDetailsResponse:
        req_url = urljoin(urljoin(self._base_url, "stock/products/"), str(product_id))
        resp = requests.get(req_url, verify=self._verify_ssl, headers=self._headers)
        if resp.status_code != 200 or not resp.text:
            return
        parsed_json = resp.json()
        return ProductDetailsResponse(parsed_json)

    def get_chores(self) -> List[CurrentChoreResponse]:
        req_url = urljoin(self._base_url, "chores")
        resp = requests.get(req_url, verify=self._verify_ssl, headers=self._headers)
        parsed_json = resp.json()
        return [CurrentChoreResponse(chore) for chore in parsed_json]

    def get_chore(self, chore_id: int) -> ChoreDetailsResponse:
        req_url = urljoin(urljoin(self._base_url, "chores/"), str(chore_id))
        resp = requests.get(req_url, verify=self._verify_ssl, headers=self._headers)
        parsed_json = resp.json()
        return ChoreDetailsResponse(parsed_json)

    def execute_chore(self, chore_id: int, done_by: int = None, tracked_time: datetime = datetime.now()):
        data = {
            "tracked_time": tracked_time.isoformat()
        }

        if done_by is not None:
            data["done_by"] = done_by

        req_url = urljoin(urljoin(urljoin(self._base_url, "chores/"), str(chore_id) + "/"), "execute")
        requests.post(req_url, verify=self._verify_ssl, headers=self._headers, data=data)

    def add_product(self, product_id, amount: float, price: float, best_before_date: datetime = None,
                    transaction_type: TransactionType = TransactionType.PURCHASE):
        data = {
            "amount": amount,
            "transaction_type": transaction_type.value,
            "price": price
        }

        if best_before_date is not None:
            data["best_before_date"] = best_before_date.strftime('%Y-%m-%d')

        req_url = urljoin(urljoin(urljoin(self._base_url, "stock/products/"), str(product_id) + "/"), "add")
        requests.post(req_url, verify=self._verify_ssl, headers=self._headers, data=data)

    def consume_product(self, product_id: int, amount: float = 1, spoiled: bool = False,
                        transaction_type: TransactionType = TransactionType.CONSUME):
        data = {
            "amount": amount,
            "spoiled": spoiled,
            "transaction_type": transaction_type.value
        }

        req_url = urljoin(urljoin(urljoin(self._base_url, "stock/products/"), str(product_id) + "/"), "consume")
        requests.post(req_url, verify=self._verify_ssl, headers=self._headers, data=data)

        
    def get_shopping_list(self) -> List[ShoppingListItem]:
        req_url = urljoin(self._base_url, "objects/shopping_list")
        resp = requests.get(req_url, verify=self._verify_ssl, headers=self._headers)
        if resp.status_code != 200:
            return
        parsed_json = resp.json()
        return [ShoppingListItem(response) for response in parsed_json]

    def add_missing_product_to_shopping_list(self, shopping_list_id: int = 1):
        data = {
            "list_id": shopping_list_id
        }

        req_url = urljoin(self._base_url, "stock/shoppinglist/add-missing-products")
        resp = requests.post(req_url, verify=self._verify_ssl, headers=self._headers, data=data)
        return resp
            
    def clear_shopping_list(self, shopping_list_id: int = 1):
        data = {
            "list_id": shopping_list_id
        }

        req_url = urljoin(self._base_url, "stock/shoppinglist/clear")
        resp = requests.post(req_url, verify=self._verify_ssl, headers=self._headers, data=data)
        return resp
            
    def remove_product_in_sl(self, sl_product_id: int):
        
        req_url = urljoin(urljoin(self._base_url, "objects/shopping_list/"), str(sl_product_id))
        resp = requests.delete(req_url, verify=self._verify_ssl, headers=self._headers)
        return resp
        
    str(sl_product_id))
        resp = requests.delete(req_url, verify=self._verify_ssl, headers=self._headers)
        if resp.status_code == 204:
            return True
        else:
            return False
            
        