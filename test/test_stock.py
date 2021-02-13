import pytest

from pygrocy.data_models.product import Product


class TestStock:
    @pytest.mark.vcr
    def test_get_stock_valid(self, grocy):
        stock = grocy.stock()

        assert isinstance(stock, list)
        assert len(stock) == 19
        for prod in stock:
            assert isinstance(prod, Product)
