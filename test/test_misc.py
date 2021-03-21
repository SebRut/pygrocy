from pygrocy.data_models.product import ProductBarcode
from pygrocy.grocy_api_client import ProductBarcodeData


class TestMisc:
    def test_158_productbarcode_deserialization(self):
        parsed_data = {"barcode": "123"}
        data = ProductBarcodeData(parsed_data)

        barcode = ProductBarcode(data)
        result = barcode.toJson()

        assert result is not None
        assert "barcode" in result
        assert "123" in result
