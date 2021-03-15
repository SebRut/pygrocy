import json

from pygrocy.data_models.product import ProductBarcode
from pygrocy.grocy_api_client import ProductBarcodeData


class TestMisc:
    def test_158_productbarcode_deserialization(self):
        parsed_data = {"barcode": "123"}
        data = ProductBarcodeData(parsed_data)

        obj = ProductBarcode(data)
        result = json.dumps(obj)

        assert result is not None
