from .grocy_api_client import GrocyApiClient

class Grocy(object):
    def __init__(self, base_url, api_key):
        self._api_client = GrocyApiClient(base_url, api_key)

    def stock(self, volatile_only = False):
        if(volatile_only):
            return self._api_client.get_volatile_stock()
        else:
            return self._api_client.get_stock()

    def product(self, product_id):
        return self._api_client.get_product(product_id)