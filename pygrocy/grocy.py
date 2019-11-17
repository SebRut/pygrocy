from datetime import datetime
from typing import List

from .grocy_api_client import (TasksResponse, ChoreDetailsResponse, CurrentChoreResponse,
                               CurrentStockResponse,
                               ShoppingListItem,
                               LocationData,
                               CurrentVolatilStockResponse, GrocyApiClient,
                               ProductData, ProductDetailsResponse,
                               TransactionType, UserDto, DEFAULT_PORT_NUMBER)


class Product(object):
    def __init__(self, stock_response: CurrentStockResponse):
        self._product_id = stock_response.product_id
        self._available_amount = stock_response.amount
        self._best_before_date = stock_response.best_before_date

        self._name = None
        self._barcodes = None
        self._product_group_id = None

    def get_details(self, api_client: GrocyApiClient):
        details = api_client.get_product(self.product_id)
        if details is None:
            return
        self._name = details.product.name
        self._barcodes = details.product.barcodes
        self._product_group_id = details.product.product_group_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def product_id(self) -> int:
        return self._product_id
        
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

class Group(object):
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

class ShoppingListProduct(object):
    def __init__(self, raw_shopping_list: ShoppingListItem):
        self._id = raw_shopping_list.id
        self._product_id = raw_shopping_list.product_id
        self._note = raw_shopping_list.note
        self._amount = raw_shopping_list.amount
        self._product = None
        
    def get_details(self, api_client: GrocyApiClient):
        self._product = api_client.get_product(self._product_id).product
        
    @property
    def id(self) -> int:
        return self._id
        
    @property
    def product_id(self) -> int:
        return self._product_id
        
    @property
    def amount(self) -> int:
        return self._amount
        
    @property
    def note(self) -> str:
        return self._note
        
    @property
    def product(self) -> Product:
        if self._product_id is None:
            self.get_details()
        return self._product
    
class Chore(object):
    def __init__(self, raw_chore: CurrentChoreResponse):
        self._chore_id = raw_chore.chore_id
        self._last_tracked_time = raw_chore.last_tracked_time
        self._next_estimated_execution_time = raw_chore.next_estimated_execution_time

        self._name = None
        self._last_done_by = None

    def get_details(self, api_client: GrocyApiClient):
        details = api_client.get_chore(self.chore_id)
        self._name = details.chore.name
        self._last_tracked_time = details.last_tracked
        self._last_done_by = details.last_done_by

    @property
    def chore_id(self) -> int:
        return self._chore_id

    @property
    def last_tracked_time(self) -> datetime:
        return self._last_tracked_time

    @property
    def next_estimated_execution_time(self) -> datetime:
        return self._next_estimated_execution_time

    @property
    def name(self) -> str:
        return self._name

    @property
    def last_done_by(self) -> UserDto:
        return self._last_done_by

class Task(object):
    def __init__(self, task: TasksResponse):
        self._id = task.task_id
        self._category_id = task.category_id
        self._assigned_to_user_id = task.assigned_to_user_id
        self._due_date = task.due_date
        self._done_timestamp = task.done_timestamp
        self._name = task.name
        self._description = task.description
        self._done = task.done

    @property
    def task_id(self) -> int:
        return self._id

    @property
    def category_id(self) -> int:
        return self._category_id

    @property
    def assigned_to_user_id(self) -> int:
        return self._assigned_to_user_id

    @property
    def done(self) -> int:
        return self._done

    @property
    def due_date(self) -> datetime:
        return self._due_date

    @property
    def done_timestamp(self) -> datetime:
        return self._done_timestamp

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

class Grocy(object):
    def __init__(self, base_url, api_key, port: int = DEFAULT_PORT_NUMBER, verify_ssl = True):
        self._api_client = GrocyApiClient(base_url, api_key, port, verify_ssl)

    def stock(self, get_details: bool = False) -> List[Product]:
        raw_stock = self._api_client.get_stock()
        if raw_stock is None:
            return
        stock = [Product(resp) for resp in raw_stock]

        if get_details:
            for item in stock:
                item.get_details(self._api_client)
        return stock

    def volatile_stock(self) -> CurrentVolatilStockResponse:
        return self._api_client.get_volatile_stock()

    def expiring_products(self, get_details: bool = False) -> List[Product]:
        raw_expiring_product = self.volatile_stock().expiring_products
        if raw_expiring_product is None:
            return
        expiring_product = [Product(resp) for resp in raw_expiring_product]

        if get_details:
            for item in expiring_product:
                item.get_details(self._api_client)
        return expiring_product

    def expired_products(self, get_details: bool = False) -> List[Product]:
        raw_expired_product = self.volatile_stock().expired_products
        if raw_expired_product is None:
            return
        expired_product = [Product(resp) for resp in raw_expired_product]

        if get_details:
            for item in expired_product:
                item.get_details(self._api_client)
        return expired_product


    def missing_products(self, get_details: bool = False) -> List[Product]:
        raw_missing_product = self.volatile_stock().missing_products
        if raw_missing_product is None:
            return
        missing_product = [Product(resp) for resp in raw_missing_product]

        if get_details:
            for item in missing_product:
                item.get_details(self._api_client)
        return missing_product


    def product(self, product_id: int) -> ProductDetailsResponse:
        return self._api_client.get_product(product_id)

    def chores(self, get_details: bool = False) -> List[Chore]:
        raw_chores = self._api_client.get_chores()
        chores = [Chore(chore) for chore in raw_chores]

        if get_details:
            for chore in chores:
                chore.get_details(self._api_client)
        return chores

    def execute_chore(self, chore_id: int, done_by: int = None, tracked_time: datetime = datetime.now()):
        return self._api_client.execute_chore(chore_id, done_by, tracked_time)

    def chore(self, chore_id: int) -> ChoreDetailsResponse:
        return self._api_client.get_chore(chore_id)

    def tasks(self) -> List[Task]:
        raw_tasks = self._api_client.get_tasks()
        tasks = [Task(task) for task in raw_tasks]

        return tasks

    def mark_task_complete(self, task_id: int, done_time: datetime = datetime.now()):
        return self._api_client.mark_task_complete(task_id, done_time)

    def undo_task_complete(self, task_id: int):
        return self._api_client.undo_task_complete(task_id)

    def add_product(self, product_id, amount: float, price: float, best_before_date: datetime = None,
                    transaction_type: TransactionType = TransactionType.PURCHASE):
        return self._api_client.add_product(product_id, amount, price, best_before_date, transaction_type)

    def consume_product(self, product_id: int, amount: float = 1, spoiled: bool = False,
                        transaction_type: TransactionType = TransactionType.CONSUME):
        return self._api_client.consume_product(product_id, amount, spoiled, transaction_type)
    
    def shopping_list(self, get_details: bool = False) -> List[ShoppingListProduct]:
        raw_shoppinglist = self._api_client.get_shopping_list()
        if raw_shoppinglist is None:
            return
        shopping_list = [ShoppingListProduct(resp) for resp in raw_shoppinglist]

        if get_details:
            for item in shopping_list:
                item.get_details(self._api_client)
        return shopping_list
        
    def add_missing_product_to_shopping_list(self, shopping_list_id: int = 1):
        return self._api_client.add_missing_product_to_shopping_list(shopping_list_id)
        
    def clear_shopping_list(self, shopping_list_id: int = 1):
        return self._api_client.clear_shopping_list(shopping_list_id)

    def remove_product_in_shopping_list(self, shopping_list_product_id: int):
        return self._api_client.remove_product_in_sl(shopping_list_product_id)
        
    def product_groups(self) -> List[Group]:
        raw_groups = self._api_client.get_product_groups()
        if raw_groups is None:
            return
        return [Group(resp) for resp in raw_groups]
        
    def add_product_pic(self, product_id: int, pic_path: str):
        if self._api_client.upload_product_picture(product_id, pic_path).status_code != 204:
            return
        return self._api_client.update_product_pic(product_id)
        
    def get_userfields(self, entity: str, object_id: int):
        return self._api_client.get_userfields(entity, object_id)
        
    def set_userfields(self, entity: str, object_id: int, key: str, value):
        return self._api_client.set_userfields(entity, object_id, key, value)
        
    def get_last_db_changed(self):
        return self._api_client.get_last_db_changed()
        