import pytest

from pygrocy.data_models.product import Product, ProductBarcode
from pygrocy.errors.grocy_error import GrocyError


class TestProduct:
    @pytest.mark.vcr
    def test_get_all_products(self, grocy):
        products = grocy.all_products()

        assert len(products) == 26

        product = products[0]
        assert product.id == 1
        assert product.name == "Cookies"

    @pytest.mark.vcr
    def test_product_get_details_valid(self, grocy):
        product = grocy.product(8)

        assert isinstance(product, Product)
        assert product.name == "Gulash soup"
        assert product.available_amount == 5
        assert product.product_group_id == 3
        assert product.qu_factor_purchase_to_stock == 1.0
        assert product.default_quantity_unit_purchase.id == 5
        assert product.default_quantity_unit_purchase.name == "Tin"
        assert product.default_quantity_unit_purchase.description is None
        assert product.default_quantity_unit_purchase.name_plural == "Tins"

        assert len(product.product_barcodes) == 2
        barcode = product.product_barcodes[0]
        assert isinstance(barcode, ProductBarcode)
        assert barcode.barcode == "22111968"

    @pytest.mark.vcr
    def test_product_no_barcodes(self, grocy):
        stock = grocy.stock()
        product = next(prod for prod in stock if prod.id == 2)

        assert product.name == "Chocolate"
        assert product.product_barcodes is not None
        assert isinstance(product.product_barcodes, list)
        assert len(product.product_barcodes) == 0

    @pytest.mark.vcr
    def test_product_get_details_non_existant(self, grocy):
        with pytest.raises(GrocyError) as exc_info:
            grocy.product(200)

        error = exc_info.value
        assert error.status_code == 400
        assert error.message == "Product does not exist or is inactive"

    @pytest.mark.vcr
    def test_add_product_pic_valid(self, grocy, mocker):
        mocked_exists = mocker.patch("os.path.exists")
        mocked_exists.return_value = True

        mocker.patch("builtins.open", mocker.mock_open())

        assert grocy.add_product_pic(20, "/somepath/pic.jpg") is None

    @pytest.mark.vcr
    def test_get_product_by_barcode(self, grocy):
        product = grocy.product_by_barcode("42141099")

        assert isinstance(product, Product)
        assert product.name == "Crisps"
        assert product.available_amount == 25
        assert product.product_group_id == 1

        assert len(product.product_barcodes) == 1
        barcode = product.product_barcodes[0]
        assert isinstance(barcode, ProductBarcode)
        assert barcode.barcode == "42141099"

    @pytest.mark.vcr
    def test_product_by_barcode_get_details_non_existant(self, grocy):
        with pytest.raises(GrocyError) as exc_info:
            grocy.product_by_barcode(200)

        error = exc_info.value
        assert error.status_code == 400
        assert error.message == "No product with barcode 200 found"
