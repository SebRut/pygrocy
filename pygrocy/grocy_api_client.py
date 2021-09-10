import base64
import json
import logging
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from pydantic import BaseModel, Field
from pydantic.schema import date

from pygrocy import EntityType
from pygrocy.utils import localize_datetime, parse_date

from .errors import GrocyError

DEFAULT_PORT_NUMBER = 9192

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


class ShoppingListItem(BaseModel):
    id: int
    product_id: Optional[int] = None
    note: Optional[str] = None
    amount: float
    row_created_timestamp: datetime
    shopping_list_id: int
    done: int


class MealPlanResponse(BaseModel):
    id: int
    day: date
    type: str
    recipe_id: Optional[int] = None
    recipe_servings: Optional[int] = None
    note: Optional[str] = None
    product_id: Optional[int] = None
    product_amount: Optional[float] = None
    product_qu_id: Optional[str] = None
    row_created_timestamp: datetime
    userfields: Optional[Dict] = None
    section_id: Optional[int] = None


class RecipeDetailsResponse(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    base_servings: int
    desired_servings: int
    picture_file_name: Optional[str]
    row_created_timestamp: datetime
    userfields: Optional[Dict] = None


class QuantityUnitData(BaseModel):
    id: int
    name: str
    name_plural: str
    description: Optional[str] = None
    row_created_timestamp: datetime


class LocationData(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    row_created_timestamp: datetime


class ProductData(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    location_id: int
    product_group_id: Optional[int] = None
    qu_id_stock: int
    qu_id_purchase: int
    qu_factor_purchase_to_stock: float
    picture_file_name: Optional[str] = None
    allow_partial_units_in_stock: Optional[bool] = False
    row_created_timestamp: datetime
    min_stock_amount: Optional[int]
    default_best_before_days: int


class ChoreData(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    period_type: str
    period_config: Optional[str] = None
    period_days: Optional[int] = 0
    track_date_only: bool
    rollover: bool
    assignment_type: Optional[str] = None
    assignment_config: Optional[str] = None
    next_execution_assigned_to_user_id: Optional[int] = None
    userfields: Optional[Dict]


class UserDto(BaseModel):
    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None


class CurrentChoreResponse(BaseModel):
    chore_id: int
    last_tracked_time: Optional[datetime]
    next_estimated_execution_time: datetime


class CurrentStockResponse(BaseModel):
    product_id: int
    amount: float
    best_before_date: date
    amount_opened: float
    product: ProductData


class MissingProductResponse(BaseModel):
    id: int
    name: str
    amount_missing: float
    is_partly_in_stock: bool


class CurrentVolatilStockResponse(BaseModel):
    due_products: Optional[List[CurrentStockResponse]] = None
    overdue_products: Optional[List[CurrentStockResponse]] = None
    expired_products: Optional[List[CurrentStockResponse]] = None
    missing_products: Optional[List[MissingProductResponse]] = None


class ProductBarcodeData(BaseModel):
    barcode: str


class ProductDetailsResponse(BaseModel):
    last_purchased: Optional[date] = None
    last_used: Optional[datetime] = None
    stock_amount: int
    stock_amount_opened: int
    next_best_before_date: Optional[date] = None
    last_price: Optional[float] = None
    product: ProductData
    quantity_unit_stock: QuantityUnitData
    barcodes: Optional[List[ProductBarcodeData]] = Field(alias="product_barcodes")
    location: Optional[LocationData] = None


class ChoreDetailsResponse(BaseModel):
    chore: ChoreData
    last_tracked: Optional[datetime] = None
    next_estimated_execution_time: datetime
    track_count: int = 0
    next_execution_assigned_user: Optional[UserDto] = None
    last_done_by: Optional[UserDto] = None


class TransactionType(Enum):
    PURCHASE = "purchase"
    CONSUME = "consume"
    INVENTORY_CORRECTION = "inventory-correction"
    PRODUCT_OPENED = "product-opened"


class TaskCategoryDto(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    row_created_timestamp: datetime


class TaskResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    due_date: date
    done: int
    done_timestamp: Optional[datetime] = None
    category_id: Optional[int] = None
    category: Optional[TaskCategoryDto] = None
    assigned_to_user_id: Optional[int] = None
    assigned_to_user: Optional[UserDto] = None
    userfields: Optional[Dict] = None


class CurrentBatteryResponse(BaseModel):
    id: int
    last_tracked_time: Optional[datetime] = None
    next_estimated_charge_time: datetime


class BatteryData(BaseModel):
    id: int
    name: str
    description: str
    used_in: str
    charge_interval_days: int
    created_timestamp: datetime = Field(alias="row_created_timestamp")
    userfields: Optional[Dict] = None


class BatteryDetailsResponse(BaseModel):
    battery: BatteryData
    charge_cycles_count: int
    last_charged: Optional[datetime] = None
    next_estimated_charge_time: datetime


class MealPlanSectionResponse(BaseModel):
    id: Optional[int] = None
    name: str
    sort_number: Optional[int] = None
    row_created_timestamp: datetime


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
        return [CurrentStockResponse(**response) for response in parsed_json]

    def get_volatile_stock(self) -> CurrentVolatilStockResponse:
        parsed_json = self._do_get_request("stock/volatile")
        return CurrentVolatilStockResponse(**parsed_json)

    def get_product(self, product_id) -> ProductDetailsResponse:
        url = f"stock/products/{product_id}"
        parsed_json = self._do_get_request(url)
        if parsed_json:
            return ProductDetailsResponse(**parsed_json)

    def get_chores(self) -> List[CurrentChoreResponse]:
        parsed_json = self._do_get_request("chores")
        return [CurrentChoreResponse(**chore) for chore in parsed_json]

    def get_chore(self, chore_id: int) -> ChoreDetailsResponse:
        url = f"chores/{chore_id}"
        parsed_json = self._do_get_request(url)
        if parsed_json:
            return ChoreDetailsResponse(**parsed_json)

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
        return [ShoppingListItem(**response) for response in parsed_json]

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
        return [LocationData(**response) for response in parsed_json]

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
        return [TaskResponse(**data) for data in parsed_json]

    def complete_task(self, task_id: int, done_time: datetime = datetime.now()):
        url = f"tasks/{task_id}/complete"

        localized_done_time = localize_datetime(done_time)

        data = {"done_time": localized_done_time.isoformat()}
        self._do_post_request(url, data)

    def get_meal_plan(self) -> List[MealPlanResponse]:
        parsed_json = self._do_get_request("objects/meal_plan")
        return [MealPlanResponse(**data) for data in parsed_json]

    def get_recipe(self, object_id: int) -> RecipeDetailsResponse:
        parsed_json = self._do_get_request(f"objects/recipes/{object_id}")
        if parsed_json:
            return RecipeDetailsResponse(**parsed_json)

    def get_batteries(self) -> List[CurrentBatteryResponse]:
        parsed_json = self._do_get_request(f"batteries")
        if parsed_json:
            return [CurrentBatteryResponse(**data) for data in parsed_json]

    def get_battery(self, battery_id: int) -> BatteryDetailsResponse:
        parsed_json = self._do_get_request(f"batteries/{battery_id}")
        if parsed_json:
            return BatteryDetailsResponse(**parsed_json)

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

    def get_meal_plan_sections(self) -> List[MealPlanSectionResponse]:
        parsed_json = self.get_generic_objects_for_type(EntityType.MEAL_PLAN_SECTIONS)
        if parsed_json:
            return [MealPlanSectionResponse(**resp) for resp in parsed_json]

    def get_meal_plan_section(self, meal_plan_section_id) -> MealPlanSectionResponse:
        parsed_json = self._do_get_request(
            f"objects/meal_plan_sections?query%5B%5D=id%3D{meal_plan_section_id}"
        )
        if parsed_json and len(parsed_json) == 1:
            return MealPlanSectionResponse(**parsed_json[0])

    def get_users(self) -> List[UserDto]:
        parsed_json = self._do_get_request("users")
        if parsed_json:
            return [UserDto(**user) for user in parsed_json]

    def get_user(self, user_id: int) -> UserDto:
        query_params = []
        if user_id:
            query_params.append(f"id={user_id}")
        parsed_json = self._do_get_request("users")
        if parsed_json:
            return UserDto(**parsed_json[0])
