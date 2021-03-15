import json

from pygrocy.grocy_api_client import ProductBarcode


class TestMisc:
    def test_158_productbarcode_deserialization(self):
        parsed_data = {"barcode": "123"}
        obj = ProductBarcode(parsed_data)
        result = json.dumps(obj)
        assert result is not None
