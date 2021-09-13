from pygrocy.grocy_api_client import GrocyApiClient


class TestGrocyApiClient:
    def test_url_only(self):
        client = GrocyApiClient(api_key="", base_url="http://grocy.de")
        assert client._base_url == "http://grocy.de:9192/api/"

    def test_url_and_port(self):
        client = GrocyApiClient(api_key="", base_url="http://grocy.de", port=1234)
        assert client._base_url == "http://grocy.de:1234/api/"
