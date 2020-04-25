from datetime import datetime
from typing import List

from .grocy_api_client import (DEFAULT_PORT_NUMBER, ChoreDetailsResponse,
                               CurrentChoreResponse, CurrentStockResponse,
                               GrocyApiClient,
                               LocationData, MissingProductResponse,
                               ProductDetailsResponse,
                               ShoppingListItem, TransactionType, UserDto)


class Product(object):
    def __init__(self, response):
        if isinstance(response, CurrentStockResponse):
            self._init_from_CurrentStockResponse(response)
        elif isinstance(response, MissingProductResponse):
            self._init_from_MissingProductResponse(response)
        elif isinstance(response, ProductDetailsResponse):
            self._init_from_ProductDetailsResponse(response)

    def _init_from_CurrentStockResponse(self, response: CurrentStockResponse):
        self._id = response.product_id
        self._available_amount = response.amount
        self._best_before_date = response.best_before_date
        self._amount_missing = None
        self._is_partly_in_stock = None
        if response.product:
            self._name = response.product.name
            self._barcodes = response.product.barcodes
            self._product_group_id = response.product.product_group_id

    def _init_from_MissingProductResponse(self, response: MissingProductResponse):
        self._id = response.product_id
        self._name = response.name
        self._available_amount = None
        self._best_before_date = None
        self._amount_missing = response.amount_missing
        self._is_partly_in_stock = response.is_partly_in_stock
        self._barcodes = None
        self._product_group_id = None

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
        if self._product_id:
            self._product = api_client.get_product(self._product_id).product

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


class Chore(object):
    def __init__(self, response):
        if isinstance(response, CurrentChoreResponse):
            self._init_from_CurrentChoreResponse(response)
        elif isinstance(response, ChoreDetailsResponse):
            self._init_from_ChoreDetailsResponse(response)

    def _init_from_CurrentChoreResponse(self, response: CurrentChoreResponse):
        self._id = response.chore_id
        self._last_tracked_time = response.last_tracked_time
        self._next_estimated_execution_time = response.next_estimated_execution_time
        self._name = None
        self._last_done_by = None

    def _init_from_ChoreDetailsResponse(self, response):
        self._id = response.chore.id
        self._last_tracked_time = response.last_tracked
        self._next_estimated_execution_time = response.next_estimated_execution_time
        self._name = response.chore.name
        self._last_done_by = response.last_done_by

    def get_details(self, api_client: GrocyApiClient):
        details = api_client.get_chore(self.id)
        self._name = details.chore.name
        self._last_tracked_time = details.last_tracked
        self._last_done_by = details.last_done_by

    @property
    def id(self) -> int:
        return self._id

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


class Grocy(object):
    def __init__(self, base_url, api_key, port: int = DEFAULT_PORT_NUMBER, verify_ssl=True):
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

    def execute_chore(self, chore_id: int, done_by: int = None, tracked_time: datetime = datetime.now()):
        return self._api_client.execute_chore(chore_id, done_by, tracked_time)

    def chore(self, chore_id: int) -> Chore:
        resp = self._api_client.get_chore(chore_id)
        return Chore(resp)

    def add_product(self, product_id, amount: float, price: float, best_before_date: datetime = None,
                    transaction_type: TransactionType = TransactionType.PURCHASE):
        return self._api_client.add_product(product_id, amount, price, best_before_date, transaction_type)

    def consume_product(self, product_id: int, amount: float = 1, spoiled: bool = False,
                        transaction_type: TransactionType = TransactionType.CONSUME):
        return self._api_client.consume_product(product_id, amount, spoiled, transaction_type)

    def shopping_list(self, get_details: bool = False) -> List[ShoppingListProduct]:
        raw_shoppinglist = self._api_client.get_shopping_list()
        shopping_list = [ShoppingListProduct(resp) for resp in raw_shoppinglist]

        if get_details:
            for item in shopping_list:
                item.get_details(self._api_client)
        return shopping_list

    def add_missing_product_to_shopping_list(self, shopping_list_id: int = 1):
        return self._api_client.add_missing_product_to_shopping_list(shopping_list_id)

    def add_product_to_shopping_list(self, product_id: int, shopping_list_id: int = None, amount: int = None):
        return self._api_client.add_product_to_shopping_list(product_id, shopping_list_id, amount)

    def clear_shopping_list(self, shopping_list_id: int = 1):
        return self._api_client.clear_shopping_list(shopping_list_id)

    def remove_product_in_shopping_list(self, product_id: int, shopping_list_id: int = 1, amount: int = 1):
        return self._api_client.remove_product_in_shopping_list(product_id, shopping_list_id, amount)

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
