from datetime import datetime
from enum import Enum
from typing import List, Dict

from .base import DataModel
from .data_models.chore import Chore
from .data_models.meal_items import RecipeItem, MealPlanItem
from .data_models.product import Product, Group, ShoppingListProduct
from .data_models.task import Task
from .data_models.user import User
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
