from urllib.parse import urljoin
import requests


class GrocyApiClient(object):
    def __init__(self, base_url, api_key):
        self._base_url = base_url
        self._api_key = api_key
        self._headers = {
            "accept": "application/json",
            "GROCY-API-KEY": api_key
        }

    def get_stock(self):
        req_url = urljoin(self._base_url, "stock")
        resp = requests.get(req_url, headers=self._headers)
        return resp.text

    def get_volatile_stock(self):
        req_url = urljoin(self._base_url, "stock/volatile")
        resp = requests.get(req_url, headers=self._headers)
        return resp.text

    def get_product(self, product_id):
        req_url = urljoin(urljoin(self._base_url, "stock/products/"), product_id)
        print(req_url)
        resp = requests.get(req_url, headers=self._headers)
        return resp.text
