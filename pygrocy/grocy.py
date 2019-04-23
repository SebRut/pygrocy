from .grocy_api_client import GrocyApiClient


class Grocy(object):
    def __init__(self, base_url, api_key):
        self._api_client = GrocyApiClient(base_url, api_key)

    def stock(self):
        return [Stock(self._api_client, resp) for resp in self._api_client.get_stock()]

    def volatile_stock(self):
        return self._api_client.get_volatile_stock()

    def expiring_products(self):
        return self.volatile_stock().expiring_products

    def expired_products(self):
        return self.volatile_stock().expired_products

    def missing_products(self):
        return self.volatile_stock().missing_products

    def product(self, product_id):
        return self._api_client.get_product(product_id)


class Stock(object):
    def __init__(self, api_client, stock_response):
        self._api_client = api_client

        self._product_id = stock_response.product_id
        self._available_amount = stock_response.amount
        self._best_before_date = stock_response.best_before_date

    def update(self):
        product_response = self._api_client.get_product(self.product_id)
        self._available_amount = product_response.stock_amount
        self._best_before_date = product_response.next_best_before_date

    @property
    def product_id(self):
        return self._product_id

    @property
    def available_amount(self):
        return self._available_amount

    @property
    def best_before_date(self):
        return self._best_before_date
