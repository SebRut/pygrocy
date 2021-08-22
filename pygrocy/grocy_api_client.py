import base64
import json
import logging
from datetime import datetime
from enum import Enum
from typing import List
from urllib.parse import urljoin

import requests

from pygrocy.utils import (
    localize_datetime,
    parse_bool_int,
    parse_date,
    parse_float,
    parse_int,
)

from .errors import GrocyError

DEFAULT_PORT_NUMBER = 9192

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


class ShoppingListItem(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json.get("id"))
        self._product_id = parse_int(parsed_json.get("product_id", None))
        self._note = parsed_json.get("note", None)
        self._amount = parse_float(parsed_json.get("amount"), 0)
        self._row_created_timestamp = parse_date(
            parsed_json.get("row_created_timestamp", None)
        )
        self._shopping_list_id = parse_int(parsed_json.get("shopping_list_id"))
        self._done = parse_int(parsed_json.get("done"))

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


class MealPlanResponse(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json.get("id"))
        self._day = parse_date(parsed_json.get("day"))
        self._type = parsed_json.get("type")
        self._recipe_id = parse_int(parsed_json.get("recipe_id"))
        self._recipe_servings = parse_int(parsed_json.get("recipe_servings"))
        self._note = parsed_json.get("note", None)
        self._product_id = parsed_json.get("product_id")
        self._product_amount = parse_float(parsed_json.get("product_amount"), 0)
        self._product_qu_id = parsed_json.get("product_qu_id")
        self._row_created_timestamp = parse_date(
            parsed_json.get("row_created_timestamp")
        )
        self._userfields = parsed_json.get("userfields")

    @property
    def id(self) -> int:
        return self._id

    @property
    def day(self) -> datetime:
        return self._day

    @property
    def recipe_id(self) -> int:
        return self._recipe_id

    @property
    def recipe_servings(self) -> int:
        return self._recipe_servings

    @property
    def note(self) -> str:
        return self._note


class RecipeDetailsResponse(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json.get("id"))
        self._name = parsed_json.get("name")
        self._description = parsed_json.get("description")
        self._base_servings = parse_int(parsed_json.get("base_servings"))
        self._desired_servings = parse_int(parsed_json.get("desired_servings"))
        self._picture_file_name = parsed_json.get("picture_file_name")
        self._row_created_timestamp = parse_date(
            parsed_json.get("row_created_timestamp")
        )
        self._userfields = parsed_json.get("userfields")

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def base_servings(self) -> int:
        return self._base_servings

    @property
    def desired_servings(self) -> int:
        return self._desired_servings

    @property
    def picture_file_name(self) -> str:
        return self._picture_file_name


class QuantityUnitData(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json.get("id"))
        self._name = parsed_json.get("name")
        self._name_plural = parsed_json.get("name_plural")
        self._description = parsed_json.get("description")
        self._row_created_timestamp = parse_date(
            parsed_json.get("row_created_timestamp")
        )


class LocationData(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json.get("id"))
        self._name = parsed_json.get("name")
        self._description = parsed_json.get("description")
        self._row_created_timestamp = parse_date(
            parsed_json.get("row_created_timestamp")
        )

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description


class ProductData(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json.get("id"))
        self._name = parsed_json.get("name")
        self._description = parsed_json.get("description", None)
        self._location_id = parse_int(parsed_json.get("location_id", None))
        self._product_group_id = parse_int(parsed_json.get("product_group_id", None))
        self._qu_id_stock = parse_int(parsed_json.get("qu_id_stock", None))
        self._qu_id_purchase = parse_int(parsed_json.get("qu_id_purchsase", None))
        self._qu_factor_purchase_to_stock = parse_float(
            parsed_json.get("qu_factor_purchase_to_stock", None)
        )
        self._picture_file_name = parsed_json.get("picture_file_name", None)
        self._allow_partial_units_in_stock = bool(
            parsed_json.get("allow_partial_units_in_stock", None) == "true"
        )
        self._row_created_timestamp = parse_date(
            parsed_json.get("row_created_timestamp", None)
        )
        self._min_stock_amount = parse_int(parsed_json.get("min_stock_amount", None), 0)
        self._default_best_before_days = parse_int(
            parsed_json.get("default_best_before_days", None)
        )

    @property
    def id(self) -> int:
        return self._id

    @property
    def product_group_id(self) -> int:
        return self._product_group_id

    @property
    def name(self) -> str:
        return self._name


class ChoreData(object):
    def __init__(self, parsed_json):
        self.id = parse_int(parsed_json.get("id"))
        self.name = parsed_json.get("name")
        self.description = parsed_json.get("description")
        self.period_type = parsed_json.get("period_type")
        self.period_config = parsed_json.get("period_config")
        self.period_days = parse_int(parsed_json.get("period_days"))
        self.track_date_only = parse_bool_int(parsed_json.get("track_date_only"))
        self.rollover = parse_bool_int(parsed_json.get("rollover"))
        self.assignment_type = parsed_json.get("assignment_type")
        self.assignment_config = parsed_json.get("assignment_config")
        self.next_execution_assigned_to_user_id = parse_int(
            parsed_json.get("next_execution_assigned_to_user_id")
        )
        self.userfields = parsed_json.get("userfields")


class UserDto(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json.get("id"))

        self._username = parsed_json.get("username")
        self._first_name = parsed_json.get("first_name")
        self._last_name = parsed_json.get("last_name")
        self._display_name = parsed_json.get("display_name")

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
        self._chore_id = parse_int(parsed_json.get("chore_id"), None)
        self._last_tracked_time = parse_date(parsed_json.get("last_tracked_time"))
        self._next_estimated_execution_time = parse_date(
            parsed_json.get("next_estimated_execution_time")
        )

    @property
    def chore_id(self) -> int:
        return self._chore_id

    @property
    def last_tracked_time(self) -> datetime:
        return self._last_tracked_time

    @property
    def next_estimated_execution_time(self) -> datetime:
        return self._next_estimated_execution_time


class CurrentStockResponse(object):
    def __init__(self, parsed_json):
        self._product_id = parse_int(parsed_json.get("product_id"))
        self._amount = parse_float(parsed_json.get("amount"))
        self._best_before_date = parse_date(parsed_json.get("best_before_date"))
        self._amount_opened = parse_float(parsed_json.get("amount_opened"))
        self._product = ProductData(parsed_json.get("product"))

    @property
    def product_id(self) -> int:
        return self._product_id

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def best_before_date(self) -> datetime:
        return self._best_before_date

    @property
    def amount_opened(self) -> float:
        return self._amount_opened

    @property
    def product(self) -> ProductData:
        return self._product


class MissingProductResponse(object):
    def __init__(self, parsed_json):
        self._product_id = parse_int(parsed_json.get("id"))
        self._name = parsed_json.get("name")
        self._amount_missing = parse_float(parsed_json.get("amount_missing"))
        self._is_partly_in_stock = bool(
            parse_int(parsed_json.get("is_partly_in_stock"))
        )

    @property
    def product_id(self) -> int:
        return self._product_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def amount_missing(self) -> float:
        return self._amount_missing

    @property
    def is_partly_in_stock(self) -> bool:
        return self._is_partly_in_stock


class CurrentVolatilStockResponse(object):
    def __init__(self, parsed_json):
        self._due_products = []
        if "due_products" in parsed_json:
            self._due_products = [
                CurrentStockResponse(product)
                for product in parsed_json.get("due_products")
            ]

        self._overdue_products = []
        if "overdue_products" in parsed_json:
            self._overdue_products = [
                CurrentStockResponse(product)
                for product in parsed_json.get("overdue_products")
            ]

        self._expired_products = []
        if "expired_products" in parsed_json:
            self._expired_products = [
                CurrentStockResponse(product)
                for product in parsed_json.get("expired_products")
            ]

        self._missing_products = []
        if "missing_products" in parsed_json:
            self._missing_products = [
                MissingProductResponse(product)
                for product in parsed_json.get("missing_products")
            ]

    @property
    def due_products(self) -> List[CurrentStockResponse]:
        return self._due_products

    @property
    def overdue_products(self) -> List[CurrentStockResponse]:
        return self._overdue_products

    @property
    def expired_products(self) -> List[CurrentStockResponse]:
        return self._expired_products

    @property
    def missing_products(self) -> List[MissingProductResponse]:
        return self._missing_products


class ProductBarcodeData(object):
    def __init__(self, parsed_json):
        self._barcode = str(parsed_json.get("barcode"))

    @property
    def barcode(self) -> str:
        return self._barcode


class ProductDetailsResponse(object):
    def __init__(self, parsed_json):
        self._last_purchased = parse_date(parsed_json.get("last_purchased"))
        self._last_used = parse_date(parsed_json.get("last_used"))
        self._stock_amount = parse_int(parsed_json.get("stock_amount"))
        self._stock_amount_opened = parse_int(parsed_json.get("stock_amount_opened"))
        self._next_best_before_date = parse_date(
            parsed_json.get("next_best_before_date")
        )
        self._last_price = parse_float(parsed_json.get("last_price"))

        self._product = ProductData(parsed_json.get("product"))

        self._quantity_unit_stock = QuantityUnitData(
            parsed_json.get("quantity_unit_stock")
        )

        self._parse_location(parsed_json)

        self._parse_barcodes(parsed_json)

    def _parse_barcodes(self, parsed_json):
        barcodes_raw = parsed_json.get("product_barcodes", "")
        if barcodes_raw is not None:
            self._barcodes = [ProductBarcodeData(barcode) for barcode in barcodes_raw]

    def _parse_location(self, parsed_json):
        raw_location = parsed_json.get("location")
        if raw_location is None:
            self._location = None
        else:
            self._location = LocationData(raw_location)

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
    def barcodes(self) -> List[ProductBarcodeData]:
        return self._barcodes

    @property
    def product(self) -> ProductData:
        return self._product


class ChoreDetailsResponse(object):
    def __init__(self, parsed_json):
        self._chore = ChoreData(parsed_json.get("chore"))
        self._last_tracked = parse_date(parsed_json.get("last_tracked"))
        self._next_estimated_execution_time = parse_date(
            parsed_json.get("next_estimated_execution_time")
        )
        self._track_count = parse_int(parsed_json.get("track_count"))

        next_user = parsed_json.get("next_execution_assigned_user")
        if next_user is not None:
            self._next_execution_assigned_user = UserDto(next_user)
        else:
            self._next_execution_assigned_user = None

        if self._last_tracked is None:
            self._last_done_by = None
        else:
            self._last_done_by = UserDto(parsed_json.get("last_done_by"))

    @property
    def chore(self) -> ChoreData:
        return self._chore

    @property
    def last_done_by(self) -> UserDto:
        return self._last_done_by

    @property
    def last_tracked(self) -> datetime:
        return self._last_tracked

    @property
    def next_estimated_execution_time(self) -> datetime:
        return self._next_estimated_execution_time

    @property
    def track_count(self) -> int:
        return self._track_count

    @property
    def next_execution_assigned_user(self) -> UserDto:
        return self._next_execution_assigned_user


class TransactionType(Enum):
    PURCHASE = "purchase"
    CONSUME = "consume"
    INVENTORY_CORRECTION = "inventory-correction"
    PRODUCT_OPENED = "product-opened"


class TaskResponse(object):
    def __init__(self, parsed_json):
        self.id = parse_int(parsed_json.get("id"))
        self.name = parsed_json.get("name")
        self.description = parsed_json.get("description")
        self.due_date = parse_date(parsed_json.get("due_date"))
        self.done = parse_int(parsed_json.get("done"))
        self.done_timestamp = parse_date(parsed_json.get("done_timestamp"))
        self.category_id = parse_int(parsed_json.get("category_id"))
        self.assigned_to_user_id = parse_int(parsed_json.get("assigned_to_user_id"))
        self.userfields = parsed_json.get("userfields")


class CurrentBatteryResponse(object):
    def __init__(self, parsed_json):
        self.id = parse_int(parsed_json.get("battery_id"))
        self.last_tracked_time = parse_date(parsed_json.get("last_tracked_time"))
        self.next_estimated_charge_time = parse_date(
            parsed_json.get("'next_estimated_charge_time")
        )


class BatteryData(object):
    def __init__(self, parsed_json):
        self.id = parse_int(parsed_json.get("id"))
        self.name = parsed_json.get("name")
        self.description = parsed_json.get("description")
        self.used_in = parsed_json.get("used_in")
        self.charge_interval_days = parse_int(parsed_json.get("charge_interval_days"))
        self.created_timestamp = parse_date(parsed_json.get("row_created_timestamp"))
        self.userfields = parsed_json.get("userfields")


class BatteryDetailsResponse(object):
    def __init__(self, parsed_json):
        self.battery = BatteryData(parsed_json.get("battery"))
        self.charge_cycles_count = parse_int(parsed_json.get("charge_cycles_count"))
        self.last_charged = parse_date(parsed_json.get("last_charged"))
        self.next_estimated_charge_time = parse_date(
            parsed_json.get("'next_estimated_charge_time")
        )


def _enable_debug_mode():
    _LOGGER.setLevel(logging.DEBUG)


class GrocyApiClient(object):
    def __init__(
        self,
        base_url,
        api_key,
        port: int = DEFAULT_PORT_NUMBER,
        verify_ssl=True,
        debug=False,
    ):
        if debug:
            _enable_debug_mode()

        self._base_url = "{}:{}/api/".format(base_url, port)
        _LOGGER.debug(f"generated base url: {self._base_url}")

        self._api_key = api_key
        self._verify_ssl = verify_ssl
        if self._api_key == "demo_mode":
            self._headers = {"accept": "application/json"}
        else:
            self._headers = {"accept": "application/json", "GROCY-API-KEY": api_key}

    def _do_get_request(self, end_url: str):
        req_url = urljoin(self._base_url, end_url)
        resp = requests.get(req_url, verify=self._verify_ssl, headers=self._headers)

        _LOGGER.debug("-->\tGET /%s", end_url)
        _LOGGER.debug("<--\t%d for /%s", resp.status_code, end_url)
        _LOGGER.debug("\t\t%s", resp.content)

        if resp.status_code >= 400:
            raise GrocyError(resp)

        if len(resp.content) > 0:
            return resp.json()

    def _do_post_request(self, end_url: str, data: dict):
        req_url = urljoin(self._base_url, end_url)
        resp = requests.post(
            req_url, verify=self._verify_ssl, headers=self._headers, json=data
        )

        _LOGGER.debug("-->\tPOST /%s", end_url)
        _LOGGER.debug("\t\t%s", data)
        _LOGGER.debug("<--\t%d for /%s", resp.status_code, end_url)
        _LOGGER.debug("\t\t%s", resp.content)

        if resp.status_code >= 400:
            raise GrocyError(resp)
        if len(resp.content) > 0:
            return resp.json()

    def _do_put_request(self, end_url: str, data):
        req_url = urljoin(self._base_url, end_url)
        up_header = self._headers.copy()
        up_header["accept"] = "*/*"
        if isinstance(data, dict):
            up_header["Content-Type"] = "application/json"
            data = json.dumps(data)
        else:
            up_header["Content-Type"] = "application/octet-stream"
        resp = requests.put(
            req_url, verify=self._verify_ssl, headers=up_header, data=data
        )

        _LOGGER.debug("-->\tPUT /%s", end_url)
        _LOGGER.debug("\t\t%s", data)
        _LOGGER.debug("<--\t%d for /%s", resp.status_code, end_url)
        _LOGGER.debug("\t\t%s", resp.content)

        if resp.status_code >= 400:
            raise GrocyError(resp)

        if len(resp.content) > 0:
            return resp.json()

    def _do_delete_request(self, end_url: str):
        req_url = urljoin(self._base_url, end_url)
        resp = requests.get(req_url, verify=self._verify_ssl, headers=self._headers)

        _LOGGER.debug("-->\tDELETE /%s", end_url)
        _LOGGER.debug("<--\t%d for /%s", resp.status_code, end_url)
        _LOGGER.debug("\t\t%s", resp.content)

        if resp.status_code >= 400:
            raise GrocyError(resp)

        if len(resp.content) > 0:
            return resp.json()

    def get_stock(self) -> List[CurrentStockResponse]:
        parsed_json = self._do_get_request("stock")
        return [CurrentStockResponse(response) for response in parsed_json]

    def get_volatile_stock(self) -> CurrentVolatilStockResponse:
        parsed_json = self._do_get_request("stock/volatile")
        return CurrentVolatilStockResponse(parsed_json)

    def get_product(self, product_id) -> ProductDetailsResponse:
        url = f"stock/products/{product_id}"
        parsed_json = self._do_get_request(url)
        if parsed_json:
            return ProductDetailsResponse(parsed_json)

    def get_chores(self) -> List[CurrentChoreResponse]:
        parsed_json = self._do_get_request("chores")
        return [CurrentChoreResponse(chore) for chore in parsed_json]

    def get_chore(self, chore_id: int) -> ChoreDetailsResponse:
        url = f"chores/{chore_id}"
        parsed_json = self._do_get_request(url)
        if parsed_json:
            return ChoreDetailsResponse(parsed_json)

    def execute_chore(
        self,
        chore_id: int,
        done_by: int = None,
        tracked_time: datetime = datetime.now(),
    ):
        localized_tracked_time = localize_datetime(tracked_time)

        data = {"tracked_time": localized_tracked_time.isoformat()}

        if done_by is not None:
            data["done_by"] = done_by

        return self._do_post_request(f"chores/{chore_id}/execute", data)

    def add_product(
        self,
        product_id,
        amount: float,
        price: float,
        best_before_date: datetime = None,
        transaction_type: TransactionType = TransactionType.PURCHASE,
    ):
        data = {
            "amount": amount,
            "transaction_type": transaction_type.value,
            "price": price,
        }

        if best_before_date is not None:
            data["best_before_date"] = best_before_date.strftime("%Y-%m-%d")

        return self._do_post_request(f"stock/products/{product_id}/add", data)

    def consume_product(
        self,
        product_id: int,
        amount: float = 1,
        spoiled: bool = False,
        transaction_type: TransactionType = TransactionType.CONSUME,
    ):
        data = {
            "amount": amount,
            "spoiled": spoiled,
            "transaction_type": transaction_type.value,
        }

        self._do_post_request(f"stock/products/{product_id}/consume", data)

    def get_shopping_list(self) -> List[ShoppingListItem]:
        parsed_json = self._do_get_request("objects/shopping_list")
        return [ShoppingListItem(response) for response in parsed_json]

    def add_missing_product_to_shopping_list(self, shopping_list_id: int = None):
        data = None
        if shopping_list_id:
            data = {"list_id": shopping_list_id}

        self._do_post_request("stock/shoppinglist/add-missing-products", data)

    def add_product_to_shopping_list(
        self, product_id: int, shopping_list_id: int = 1, amount: int = 1
    ):
        data = {
            "product_id": product_id,
            "list_id": shopping_list_id,
            "product_amount": amount,
        }
        self._do_post_request("stock/shoppinglist/add-product", data)

    def clear_shopping_list(self, shopping_list_id: int = 1):
        data = {"list_id": shopping_list_id}

        self._do_post_request("stock/shoppinglist/clear", data)

    def remove_product_in_shopping_list(
        self, product_id: int, shopping_list_id: int = 1, amount: int = 1
    ):
        data = {
            "product_id": product_id,
            "list_id": shopping_list_id,
            "product_amount": amount,
        }
        self._do_post_request("stock/shoppinglist/remove-product", data)

    def get_product_groups(self) -> List[LocationData]:
        parsed_json = self._do_get_request("objects/product_groups")
        return [LocationData(response) for response in parsed_json]

    def upload_product_picture(self, product_id: int, pic_path: str):
        b64fn = base64.b64encode("{}.jpg".format(product_id).encode("ascii"))
        req_url = "files/productpictures/" + str(b64fn, "utf-8")
        with open(pic_path, "rb") as pic:
            self._do_put_request(req_url, pic)

    def update_product_pic(self, product_id: int):
        pic_name = f"{product_id}.jpg"
        data = {"picture_file_name": pic_name}
        self._do_put_request(f"objects/products/{product_id}", data)

    def get_userfields(self, entity: str, object_id: int):
        url = f"userfields/{entity}/{object_id}"
        return self._do_get_request(url)

    def set_userfields(self, entity: str, object_id: int, key: str, value):
        data = {key: value}
        self._do_put_request(f"userfields/{entity}/{object_id}", data)

    def get_last_db_changed(self):
        resp = self._do_get_request("system/db-changed-time")
        last_change_timestamp = parse_date(resp.get("changed_time"))
        return last_change_timestamp

    def get_tasks(self) -> List[TaskResponse]:
        parsed_json = self._do_get_request("tasks")
        return [TaskResponse(data) for data in parsed_json]

    def complete_task(self, task_id: int, done_time: datetime = datetime.now()):
        url = f"tasks/{task_id}/complete"

        localized_done_time = localize_datetime(done_time)

        data = {"done_time": localized_done_time.isoformat()}
        self._do_post_request(url, data)

    def get_meal_plan(self) -> List[MealPlanResponse]:
        parsed_json = self._do_get_request("objects/meal_plan")
        return [MealPlanResponse(data) for data in parsed_json]

    def get_recipe(self, object_id: int) -> RecipeDetailsResponse:
        parsed_json = self._do_get_request(f"objects/recipes/{object_id}")
        if parsed_json:
            return RecipeDetailsResponse(parsed_json)

    def get_batteries(self) -> List[CurrentBatteryResponse]:
        parsed_json = self._do_get_request(f"batteries")
        if parsed_json:
            return [CurrentBatteryResponse(data) for data in parsed_json]

    def get_battery(self, battery_id: int) -> BatteryDetailsResponse:
        parsed_json = self._do_get_request(f"batteries/{battery_id}")
        if parsed_json:
            return BatteryDetailsResponse(parsed_json)

    def charge_battery(self, battery_id: int, tracked_time: datetime = datetime.now()):
        localized_tracked_time = localize_datetime(tracked_time)
        data = {"tracked_time": localized_tracked_time.isoformat()}

        return self._do_post_request(f"batteries/{battery_id}/charge", data)

    def add_generic(self, entity_type: str, data):
        return self._do_post_request(f"objects/{entity_type}", data)

    def update_generic(self, entity_type: str, object_id: int, data):
        return self._do_put_request(f"objects/{entity_type}/{object_id}", data)

    def delete_generic(self, entity_type: str, object_id: int):
        return self._do_delete_request(f"objects/{entity_type}/{object_id}")

    def get_generic_objects_for_type(self, entity_type: str):
        return self._do_get_request(f"objects/{entity_type}")
