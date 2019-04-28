from datetime import datetime
from typing import List

from .grocy_api_client import (ChoreDetailsResponse, CurrentChoreResponse,
                               CurrentVolatilStockResponse, GrocyApiClient,
                               ProductData, ProductDetailsResponse, CurrentStockResponse)


class Stock(object):
    def __init__(self, api_client: GrocyApiClient, stock_response: CurrentStockResponse):
        self._api_client = api_client

        self._product_id = stock_response.product_id
        self._available_amount = stock_response.amount
        self._best_before_date = stock_response.best_before_date

    def update(self):
        product_response = self._api_client.get_product(self.product_id)
        self._available_amount = product_response.stock_amount
        self._best_before_date = product_response.next_best_before_date

    @property
    def product_id(self) -> int:
        return self._product_id

    @property
    def available_amount(self) -> float:
        return self._available_amount

    @property
    def best_before_date(self) -> datetime:
        return self._best_before_date


class Chore(object):
    def __init__(self, api_client: GrocyApiClient, raw_chore: CurrentChoreResponse):
        self._api_client = api_client
        self._chore_id = raw_chore.chore_id
        self._last_tracked_time = raw_chore.last_tracked_time
        self._next_estimated_execution_time = raw_chore.next_estimated_execution_time
        self._name = None

    def get_details(self):
        details = self._api_client.get_chore(self.chore_id)
        self._name = details.chore.name


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



class Grocy(object):
    def __init__(self, base_url, api_key):
        self._api_client = GrocyApiClient(base_url, api_key)

    def stock(self) -> List[Stock]:
        return [Stock(self._api_client, resp) for resp in self._api_client.get_stock()]

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
        chores = [Chore(self._api_client, chore) for chore in raw_chores]

        if get_details:
            for chore in chores:
                chore.get_details()
        return chores

    def chore(self, chore_id: int) -> ChoreDetailsResponse:
        return self._api_client.get_chore(chore_id)
