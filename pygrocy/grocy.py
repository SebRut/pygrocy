import logging
from datetime import datetime
from typing import List

import deprecation

from .base import DataModel  # noqa: F401
from .data_models.battery import Battery
from .data_models.chore import Chore
from .data_models.generic import EntityType
from .data_models.meal_items import MealPlanItem, RecipeItem
from .data_models.product import Group, Product, ShoppingListProduct
from .data_models.task import Task
from .data_models.user import User  # noqa: F401
from .errors import GrocyError  # noqa: F401
from .grocy_api_client import ChoreDetailsResponse  # noqa: F401
from .grocy_api_client import CurrentChoreResponse  # noqa: F401
from .grocy_api_client import CurrentStockResponse  # noqa: F401
from .grocy_api_client import LocationData  # noqa: F401
from .grocy_api_client import MealPlanResponse  # noqa: F401
from .grocy_api_client import MissingProductResponse  # noqa: F401
from .grocy_api_client import ProductDetailsResponse  # noqa: F401
from .grocy_api_client import RecipeDetailsResponse  # noqa: F401
from .grocy_api_client import ShoppingListItem  # noqa: F401
from .grocy_api_client import TaskResponse  # noqa: F401
from .grocy_api_client import UserDto  # noqa: F401
from .grocy_api_client import DEFAULT_PORT_NUMBER, GrocyApiClient, TransactionType

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


class Grocy(object):
    def __init__(
        self,
        base_url,
        api_key,
        port: int = DEFAULT_PORT_NUMBER,
        verify_ssl=True,
        debug=False,
    ):
        self._api_client = GrocyApiClient(base_url, api_key, port, verify_ssl, debug)

        if debug:
            _LOGGER.setLevel(logging.DEBUG)

    def stock(self) -> List[Product]:
        raw_stock = self._api_client.get_stock()
        stock = [Product(resp) for resp in raw_stock]
        return stock

    @deprecation.deprecated(details="Use due_products instead")
    def expiring_products(self, get_details: bool = False) -> List[Product]:
        return self.due_products(get_details)

    def due_products(self, get_details: bool = False) -> List[Product]:
        raw_due_products = self._api_client.get_volatile_stock().due_products
        due_products = [Product(resp) for resp in raw_due_products]

        if get_details:
            for item in due_products:
                item.get_details(self._api_client)
        return due_products

    def overdue_products(self, get_details: bool = False) -> List[Product]:
        raw_overdue_products = self._api_client.get_volatile_stock().overdue_products
        overdue_products = [Product(resp) for resp in raw_overdue_products]

        if get_details:
            for item in overdue_products:
                item.get_details(self._api_client)
        return overdue_products

    def expired_products(self, get_details: bool = False) -> List[Product]:
        raw_expired_products = self._api_client.get_volatile_stock().expired_products
        expired_products = [Product(resp) for resp in raw_expired_products]

        if get_details:
            for item in expired_products:
                item.get_details(self._api_client)
        return expired_products

    def missing_products(self, get_details: bool = False) -> List[Product]:
        raw_missing_products = self._api_client.get_volatile_stock().missing_products
        missing_products = [Product(resp) for resp in raw_missing_products]

        if get_details:
            for item in missing_products:
                item.get_details(self._api_client)
        return missing_products

    def product(self, product_id: int) -> Product:
        resp = self._api_client.get_product(product_id)
        if resp:
            return Product(resp)

    def all_products(self) -> List[Product]:
        raw_products = self.get_generic_objects_for_type(EntityType.PRODUCTS)
        from pygrocy.grocy_api_client import ProductData

        product_datas = [ProductData(product) for product in raw_products]
        return [Product(product) for product in product_datas]

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

    def complete_task(self, task_id, done_time: datetime = datetime.now()):
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

    def batteries(self) -> List[Battery]:
        raw_batteries = self._api_client.get_batteries()
        return [Battery(bat) for bat in raw_batteries]

    def battery(self, battery_id: int) -> Battery:
        battery = self._api_client.get_battery(battery_id)
        if battery:
            return Battery(battery)

    def charge_battery(self, battery_id: int, tracked_time: datetime = datetime.now()):
        return self._api_client.charge_battery(battery_id, tracked_time)

    def add_generic(self, entity_type: EntityType, data):
        return self._api_client.add_generic(entity_type.value, data)

    def update_generic(self, entity_type: EntityType, object_id: int, updated_data):
        return self._api_client.update_generic(
            entity_type.value, object_id, updated_data
        )

    def delete_generic(self, entity_type: EntityType, object_id: int):
        return self._api_client.delete_generic(entity_type, object_id)

    def get_generic_objects_for_type(self, entity_type: EntityType):
        return self._api_client.get_generic_objects_for_type(entity_type.value)
