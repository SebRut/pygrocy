import base64
from datetime import datetime
from enum import Enum
from typing import List, Dict

from .base import DataModel
from .grocy_api_client import (
    DEFAULT_PORT_NUMBER,
    ChoreDetailsResponse,
    CurrentChoreResponse,
    CurrentStockResponse,
    GrocyApiClient,
    LocationData,
    MissingProductResponse,
    ProductDetailsResponse,
    MealPlanResponse,
    RecipeDetailsResponse,
    ShoppingListItem,
    TransactionType,
    UserDto,
    TaskResponse,
)


class Product(DataModel):
    def __init__(self, response):
        self._init_empty()
        if isinstance(response, CurrentStockResponse):
            self._init_from_CurrentStockResponse(response)
        elif isinstance(response, MissingProductResponse):
            self._init_from_MissingProductResponse(response)
        elif isinstance(response, ProductDetailsResponse):
            self._init_from_ProductDetailsResponse(response)

    def _init_empty(self):
        self._name = None
        self._id = None
        self._amount_missing = None
        self._is_partly_in_stock = None

        self._available_amount = None
        self._best_before_date = None

        self._barcodes = None
        self._product_group_id = None

    def _init_from_CurrentStockResponse(self, response: CurrentStockResponse):
        self._id = response.product_id
        self._available_amount = response.amount
        self._best_before_date = response.best_before_date
        if response.product:
            self._name = response.product.name
            self._barcodes = response.product.barcodes
            self._product_group_id = response.product.product_group_id

    def _init_from_MissingProductResponse(self, response: MissingProductResponse):
        self._id = response.product_id
        self._name = response.name
        self._amount_missing = response.amount_missing
        self._is_partly_in_stock = response.is_partly_in_stock

    def _init_from_ProductDetailsResponse(self, response: ProductDetailsResponse):
        self._id = response.product.id
        self._available_amount = response.stock_amount
        self._best_before_date = response.next_best_before_date
        self._name = response.product.name
        self._barcodes = response.product.barcodes

    def get_details(self, api_client: GrocyApiClient):
        details = api_client.get_product(self.id)
        if details:
            self._name = details.product.name
            self._barcodes = details.product.barcodes
            self._product_group_id = details.product.product_group_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> int:
        return self._id

    @property
    def product_group_id(self) -> int:
        return self._product_group_id

    @property
    def available_amount(self) -> float:
        return self._available_amount

    @property
    def best_before_date(self) -> datetime:
        return self._best_before_date

    @property
    def barcodes(self) -> List[str]:
        return self._barcodes

    @property
    def amount_missing(self) -> float:
        return self._amount_missing

    @property
    def is_partly_in_stock(self) -> int:
        return self._is_partly_in_stock


class Group(DataModel):
    def __init__(self, raw_product_group: LocationData):
        self._id = raw_product_group.id
        self._name = raw_product_group.name
        self._description = raw_product_group.description

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description


class ShoppingListProduct(DataModel):
    def __init__(self, raw_shopping_list: ShoppingListItem):
        self._id = raw_shopping_list.id
        self._product_id = raw_shopping_list.product_id
        self._note = raw_shopping_list.note
        self._amount = raw_shopping_list.amount
        self._product = None

    def get_details(self, api_client: GrocyApiClient):
        if self._product_id:
            self._product = Product(api_client.get_product(self._product_id))

    @property
    def id(self) -> int:
        return self._id

    @property
    def product_id(self) -> int:
        return self._product_id

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def note(self) -> str:
        return self._note

    @property
    def product(self) -> Product:
        return self._product


class User(DataModel):
    def __init__(self, user_dto: UserDto):
        self._id = user_dto.id
        self._username = user_dto.username
        self._first_name = user_dto.first_name
        self._last_name = user_dto.last_name
        self._display_name = user_dto.display_name

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


class PeriodType(str, Enum):
    MANUALLY = "manually"
    DYNAMIC_REGULAR = "dynamic-regular"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class AssignmentType(str, Enum):
    NO_ASSIGNMENT = "no-assignment"
    WHO_LEAST_DID_FIRST = "who-least-did-first"
    RANDOM = "random"
    IN_ALPHABETICAL_ORDER = "in-alphabetical-order"


class Chore(DataModel):
    def __init__(self, response):
        if isinstance(response, CurrentChoreResponse):
            self._init_from_CurrentChoreResponse(response)
        elif isinstance(response, ChoreDetailsResponse):
            self._init_from_ChoreDetailsResponse(response)

    # noinspection PyPep8Naming
    def _init_from_CurrentChoreResponse(self, response: CurrentChoreResponse):
        self._id = response.chore_id
        self._last_tracked_time = response.last_tracked_time
        self._next_estimated_execution_time = response.next_estimated_execution_time
        self._name = None
        self._last_done_by = None

    # noinspection PyPep8Naming
    def _init_from_ChoreDetailsResponse(self, response: ChoreDetailsResponse):
        chore_data = response.chore
        self._id = chore_data.id
        self._name = chore_data.name
        self._description = chore_data.description

        if chore_data.period_type is not None:
            self._period_type = PeriodType(chore_data.period_type)
        else:
            self._period_type = None

        self._period_config = chore_data.period_config
        self._period_days = chore_data.period_days
        self._track_date_only = chore_data.track_date_only
        self._rollover = chore_data.rollover

        if chore_data.assignment_type is not None:
            self._assignment_type = AssignmentType(chore_data.assignment_type)
        else:
            self._assignment_type = None

        self._assignment_config = chore_data.assignment_config
        self._next_execution_assigned_to_user_id = (
            chore_data.next_execution_assigned_to_user_id
        )
        self._userfields = chore_data.userfields

        self._last_tracked_time = response.last_tracked
        self._next_estimated_execution_time = response.next_estimated_execution_time
        if response.last_done_by is not None:
            self._last_done_by = User(response.last_done_by)
        else:
            self._last_done_by = None
        self._track_count = response.track_count
        if response.next_execution_assigned_user is not None:
            self._next_execution_assigned_user = User(
                response.next_execution_assigned_user
            )
        else:
            self._next_execution_assigned_user = None

    def get_details(self, api_client: GrocyApiClient):
        details = api_client.get_chore(self.id)
        self._init_from_ChoreDetailsResponse(details)

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
    def period_type(self) -> PeriodType:
        return self._period_type

    @property
    def period_config(self) -> str:
        return self._period_config

    @property
    def period_days(self) -> int:
        return self._period_days

    @property
    def track_date_only(self) -> bool:
        return self._track_date_only

    @property
    def rollover(self) -> bool:
        return self._rollover

    @property
    def assignment_type(self) -> AssignmentType:
        return self._assignment_type

    @property
    def assignment_config(self) -> str:
        return self._assignment_config

    @property
    def next_execution_assigned_to_user_id(self) -> int:
        return self._next_execution_assigned_to_user_id

    @property
    def userfields(self) -> Dict[str, str]:
        return self._userfields

    @property
    def last_tracked_time(self) -> datetime:
        return self._last_tracked_time

    @property
    def next_estimated_execution_time(self) -> datetime:
        return self._next_estimated_execution_time

    @property
    def last_done_by(self) -> User:
        return self._last_done_by

    @property
    def track_count(self) -> int:
        return self._track_count

    @property
    def next_execution_assigned_user(self) -> User:
        return self._next_execution_assigned_user


class Task(DataModel):
    def __init__(self, response: TaskResponse):

        self._id = response.id
        self._name = response.name
        self._description = response.description
        self._due_date = response.due_date
        self._done = response.done
        self._done_timestamp = response.done_timestamp
        self._category_id = response.category_id
        self._assigned_to_user_id = response.assigned_to_user_id
        self._userfields = response.userfields

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def due_date(self) -> datetime:
        return self._due_date

    @property
    def done(self) -> int:
        return self._done

    @property
    def done_timestamp(self) -> datetime:
        return self._done_timestamp

    @property
    def category_id(self) -> int:
        return self._category_id

    @property
    def assigned_to_user_id(self) -> int:
        return self._assigned_to_user_id

    @property
    def userfields(self) -> Dict[str, str]:
        return self._userfields


class RecipeItem(DataModel):
    def __init__(self, response: RecipeDetailsResponse):
        self._id = response.id
        self._name = response.name
        self._description = response.description
        self._base_servings = response.base_servings
        self._desired_servings = response.desired_servings
        self._picture_file_name = response.picture_file_name

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

    def get_picture_url_path(self, width: int = 400):
        if self.picture_file_name:
            b64name = base64.b64encode(self.picture_file_name.encode("ascii"))
            path = "files/recipepictures/" + str(b64name, "utf-8")

            return f"{path}?force_serve_as=picture&best_fit_width={width}"


class MealPlanItem(DataModel):
    def __init__(self, response: MealPlanResponse):
        self._id = response.id
        self._day = response.day
        self._recipe_id = response.recipe_id
        self._recipe_servings = response.recipe_servings
        self._note = response.note

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

    @property
    def recipe(self) -> RecipeItem:
        return self._recipe

    def get_details(self, api_client: GrocyApiClient):
        recipe = api_client.get_recipe(self.recipe_id)
        if recipe:
            self._recipe = RecipeItem(recipe)


class Grocy(object):
    def __init__(
        self, base_url, api_key, port: int = DEFAULT_PORT_NUMBER, verify_ssl=True
    ):
        self._api_client = GrocyApiClient(base_url, api_key, port, verify_ssl)

    def stock(self) -> List[Product]:
        raw_stock = self._api_client.get_stock()
        stock = [Product(resp) for resp in raw_stock]
        return stock

    def expiring_products(self, get_details: bool = False) -> List[Product]:
        raw_expiring_product = self._api_client.get_volatile_stock().expiring_products
        expiring_product = [Product(resp) for resp in raw_expiring_product]

        if get_details:
            for item in expiring_product:
                item.get_details(self._api_client)
        return expiring_product

    def expired_products(self, get_details: bool = False) -> List[Product]:
        raw_expired_product = self._api_client.get_volatile_stock().expired_products
        expired_product = [Product(resp) for resp in raw_expired_product]

        if get_details:
            for item in expired_product:
                item.get_details(self._api_client)
        return expired_product

    def missing_products(self, get_details: bool = False) -> List[Product]:
        raw_missing_product = self._api_client.get_volatile_stock().missing_products
        missing_product = [Product(resp) for resp in raw_missing_product]

        if get_details:
            for item in missing_product:
                item.get_details(self._api_client)
        return missing_product

    def product(self, product_id: int) -> Product:
        resp = self._api_client.get_product(product_id)
        if resp:
            return Product(resp)

    def chores(self, get_details: bool = False) -> List[Chore]:
        raw_chores = self._api_client.get_chores()
        chores = [Chore(chore) for chore in raw_chores]

        if get_details:
            for chore in chores:
                chore.get_details(self._api_client)
        return chores

    def execute_chore(
        self,
        chore_id: int,
        done_by: int = None,
        tracked_time: datetime = datetime.now(),
    ):
        return self._api_client.execute_chore(chore_id, done_by, tracked_time)

    def chore(self, chore_id: int) -> Chore:
        resp = self._api_client.get_chore(chore_id)
        return Chore(resp)

    def add_product(
        self,
        product_id,
        amount: float,
        price: float,
        best_before_date: datetime = None,
        transaction_type: TransactionType = TransactionType.PURCHASE,
    ):
        return self._api_client.add_product(
            product_id, amount, price, best_before_date, transaction_type
        )

    def consume_product(
        self,
        product_id: int,
        amount: float = 1,
        spoiled: bool = False,
        transaction_type: TransactionType = TransactionType.CONSUME,
    ):
        return self._api_client.consume_product(
            product_id, amount, spoiled, transaction_type
        )

    def shopping_list(self, get_details: bool = False) -> List[ShoppingListProduct]:
        raw_shoppinglist = self._api_client.get_shopping_list()
        shopping_list = [ShoppingListProduct(resp) for resp in raw_shoppinglist]

        if get_details:
            for item in shopping_list:
                item.get_details(self._api_client)
        return shopping_list

    def add_missing_product_to_shopping_list(self, shopping_list_id: int = 1):
        return self._api_client.add_missing_product_to_shopping_list(shopping_list_id)

    def add_product_to_shopping_list(
        self, product_id: int, shopping_list_id: int = None, amount: int = None
    ):
        return self._api_client.add_product_to_shopping_list(
            product_id, shopping_list_id, amount
        )

    def clear_shopping_list(self, shopping_list_id: int = 1):
        return self._api_client.clear_shopping_list(shopping_list_id)

    def remove_product_in_shopping_list(
        self, product_id: int, shopping_list_id: int = 1, amount: int = 1
    ):
        return self._api_client.remove_product_in_shopping_list(
            product_id, shopping_list_id, amount
        )

    def product_groups(self) -> List[Group]:
        raw_groups = self._api_client.get_product_groups()
        return [Group(resp) for resp in raw_groups]

    def add_product_pic(self, product_id: int, pic_path: str):
        self._api_client.upload_product_picture(product_id, pic_path)
        return self._api_client.update_product_pic(product_id)

    def get_userfields(self, entity: str, object_id: int):
        return self._api_client.get_userfields(entity, object_id)

    def set_userfields(self, entity: str, object_id: int, key: str, value):
        return self._api_client.set_userfields(entity, object_id, key, value)

    def get_last_db_changed(self):
        return self._api_client.get_last_db_changed()

    def tasks(self) -> List[Task]:
        raw_tasks = self._api_client.get_tasks()
        return [Task(task) for task in raw_tasks]

    def complete_task(self, task_id, done_time):
        return self._api_client.complete_task(task_id, done_time)

    def meal_plan(self, get_details: bool = False) -> List[MealPlanItem]:
        raw_meal_plan = self._api_client.get_meal_plan()
        meal_plan = [MealPlanItem(data) for data in raw_meal_plan]

        if get_details:
            for item in meal_plan:
                item.get_details(self._api_client)
        return meal_plan

    def recipe(self, recipe_id: int) -> RecipeItem:
        recipe = self._api_client.get_recipe(recipe_id)
        if recipe:
            return RecipeItem(recipe)

    def add_generic(self, entity_type, data):
        return self._api_client.add_generic(entity_type, data)
