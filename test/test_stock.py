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

    @pytest.mark.vcr
    def test_get_due_products_valid(self, grocy):
        due_products = grocy.due_products(True)

        assert isinstance(due_products, list)
        assert len(due_products) == 3
        for prod in due_products:
            assert isinstance(prod, Product)

    @pytest.mark.vcr
    def test_get_expired_products_valid(self, grocy):
        expired_products = grocy.expired_products(True)

        assert isinstance(expired_products, list)
        assert len(expired_products) == 1
        for prod in expired_products:
            assert isinstance(prod, Product)

    @pytest.mark.vcr
    def test_get_missing_products_valid(self, grocy):
        missing_products = grocy.missing_products(True)

        assert isinstance(missing_products, list)
        assert len(missing_products) == 4
        for prod in missing_products:
            assert isinstance(prod, Product)
            assert isinstance(prod.amount_missing, float)
            assert isinstance(prod.is_partly_in_stock, bool)

        product = next(product for product in missing_products if product.id == 1)
        assert product.is_partly_in_stock is False
        assert product.amount_missing == 8.0

    @pytest.mark.vcr
    def test_get_overdue_products_valid(self, grocy):
        overdue_products = grocy.overdue_products(True)

        assert isinstance(overdue_products, list)
        assert len(overdue_products) == 2
        for prod in overdue_products:
            assert isinstance(prod, Product)
