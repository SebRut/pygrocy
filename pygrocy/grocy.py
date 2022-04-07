import logging
from datetime import datetime
from typing import List

import deprecation

from .base import DataModel  # noqa: F401
from .data_models.battery import Battery
from .data_models.chore import Chore
from .data_models.generic import EntityType
from .data_models.meal_items import MealPlanItem, MealPlanSection, RecipeItem
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
        path: str = None,
        verify_ssl=True,
        debug=False,
    ):
        self._api_client = GrocyApiClient(
            base_url, api_key, port, path, verify_ssl, debug
        )

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

    def product_by_barcode(self, barcode: str) -> Product:
        resp = self._api_client.get_product_by_barcode(barcode)
        if resp:
            return Product(resp)

    def all_products(self) -> List[Product]:
        raw_products = self.get_generic_objects_for_type(EntityType.PRODUCTS)
        from pygrocy.grocy_api_client import ProductData

        product_datas = [ProductData(**product) for product in raw_products]
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
        allow_subproduct_substitution: bool = False,
    ):
        return self._api_client.consume_product(
            product_id, amount, spoiled, transaction_type, allow_subproduct_substitution
        )

    def inventory_product(
        self,
        product_id: int,
        new_amount: int,
        best_before_date: datetime = None,
        shopping_location_id: int = None,
        location_id: int = None,
        price: int = None,
        get_details: bool = True,
    ) -> Product:
        product = Product(
            self._api_client.inventory_product(
                product_id,
                new_amount,
                best_before_date,
                shopping_location_id,
                location_id,
                price,
            )
        )

        if get_details:
            product.get_details(self._api_client)
        return product

    def add_product_by_barcode(
        self,
        barcode: str,
        amount: float,
        price: float,
        best_before_date: datetime = None,
        get_details: bool = True,
    ) -> Product:
        product = Product(
            self._api_client.add_product_by_barcode(
                barcode, amount, price, best_before_date
            )
        )

        if get_details:
            product.get_details(self._api_client)
        return product

    def consume_product_by_barcode(
        self,
        barcode: str,
        amount: float = 1,
        spoiled: bool = False,
        get_details: bool = True,
    ) -> Product:
        product = Product(
            self._api_client.consume_product_by_barcode(barcode, amount, spoiled)
        )

        if get_details:
            product.get_details(self._api_client)
        return product

    def inventory_product_by_barcode(
        self,
        barcode: str,
        new_amount: int,
        best_before_date: datetime = None,
        location_id: int = None,
        price: int = None,
        get_details: bool = True,
    ) -> Product:
        product = Product(
            self._api_client.inventory_product_by_barcode(
                barcode, new_amount, best_before_date, location_id, price
            )
        )

        if get_details:
            product.get_details(self._api_client)
        return product

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
        self,
        product_id: int,
        shopping_list_id: int = None,
        amount: int = None,
        quantity_unit_id: int = None,
    ):
        return self._api_client.add_product_to_shopping_list(
            product_id, shopping_list_id, amount, quantity_unit_id
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

    def task(self, task_id: int) -> Task:
        resp = self._api_client.get_task(task_id)
        return Task(resp)

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

    def meal_plan_sections(self) -> List[MealPlanSection]:
        raw_sections = self._api_client.get_meal_plan_sections()
        return [MealPlanSection(section) for section in raw_sections]

    def meal_plan_section(self, meal_plan_section_id: int) -> MealPlanSection:
        section = self._api_client.get_meal_plan_section(meal_plan_section_id)

        if section:
            return MealPlanSection(section)

    def users(self) -> List[User]:
        user_dtos = self._api_client.get_users()
        return [User(user) for user in user_dtos]

    def user(self, user_id: int = None) -> User:
        user = self._api_client.get_user(user_id=user_id)
        if user:
            return User(user)
