from .grocy_api_client import GrocyApiClient


class Grocy(object):
    def __init__(self, base_url, api_key):
        self._api_client = GrocyApiClient(base_url, api_key)

    def stock(self):
            return self._api_client.get_stock()

    def volatile_stock(self):
        return self._api_client.get_volatile_stock()

    def product(self, product_id):
        return self._api_client.get_product(product_id)
