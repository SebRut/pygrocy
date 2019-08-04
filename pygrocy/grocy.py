from datetime import datetime
from typing import List

from .grocy_api_client import (ChoreDetailsResponse, CurrentChoreResponse,
                               CurrentStockResponse,
                               CurrentVolatilStockResponse, GrocyApiClient,
                               ProductData, ProductDetailsResponse,
                               TransactionType, UserDto)


class Product(object):
    def __init__(self, stock_response: CurrentStockResponse):
        self._product_id = stock_response.product_id
        self._available_amount = stock_response.amount
        self._best_before_date = stock_response.best_before_date

        self._name = None
        self._barcodes = None

    def get_details(self, api_client: GrocyApiClient):
        details = api_client.get_product(self.product_id)
        if details is None:
            return
        self._name = details.product.name
        self._barcodes = details.product.barcodes

    @property
    def name(self) -> str:
        return self._name

    @property
    def product_id(self) -> int:
        return self._product_id

    @property
    def available_amount(self) -> float:
        return self._available_amount

    @property
    def best_before_date(self) -> datetime:
        return self._best_before_date

    @property
    def barcodes(self) -> List[str]:
        return self._barcodes


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


class Grocy(object):
    def __init__(self, base_url, api_key, verify_ssl = True):
        self._api_client = GrocyApiClient(base_url, api_key, verify_ssl)

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

    def expiring_products(self) -> List[ProductData]:
        return self.volatile_stock().expiring_products

    def expired_products(self) -> List[ProductData]:
        return self.volatile_stock().expired_products

    def missing_products(self) -> List[ProductData]:
        return self.volatile_stock().missing_products

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

    def add_product(self, product_id, amount: float, price: float, best_before_date: datetime = None,
                    transaction_type: TransactionType = TransactionType.PURCHASE):
        return self._api_client.add_product(product_id, amount, price, best_before_date, transaction_type)

    def consume_product(self, product_id: int, amount: float = 1, spoiled: bool = False,
                        transaction_type: TransactionType = TransactionType.CONSUME):
        return self._api_client.consume_product(product_id, amount, spoiled, transaction_type)
