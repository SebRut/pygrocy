from datetime import datetime
from typing import List

from pygrocy.base import DataModel
from pygrocy.grocy_api_client import (
    CurrentStockResponse,
    GrocyApiClient,
    LocationData,
    MissingProductResponse,
    ProductBarcode,
    ProductDetailsResponse,
    ShoppingListItem,
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

        self._barcodes = []
        self._product_group_id = None

    def _init_from_CurrentStockResponse(self, response: CurrentStockResponse):
        self._id = response.product_id
        self._available_amount = response.amount
        self._best_before_date = response.best_before_date
        if response.product:
            self._name = response.product.name
            self._product_group_id = response.product.product_group_id

    def _init_from_MissingProductResponse(self, response: MissingProductResponse):
        self._id = response.product_id
        self._name = response.name
        self._amount_missing = response.amount_missing
        self._is_partly_in_stock = response.is_partly_in_stock

    def _init_from_ProductDetailsResponse(self, response: ProductDetailsResponse):
        self._id = response.product.id
        self._product_group_id = response.product.product_group_id
        self._available_amount = response.stock_amount
        self._best_before_date = response.next_best_before_date
        self._name = response.product.name
        self._barcodes = response.barcodes

    def get_details(self, api_client: GrocyApiClient):
        details = api_client.get_product(self.id)
        if details:
            self._name = details.product.name
            self._barcodes = details.barcodes
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
        return [barcode.barcode for barcode in self.product_barcodes]

    @property
    def product_barcodes(self) -> List[ProductBarcode]:
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
