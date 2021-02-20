import pytest

from pygrocy.data_models.product import Product, ShoppingListProduct
from pygrocy.errors import GrocyError


class TestShoppingList:
    @pytest.mark.vcr
    def test_get_shopping_list_valid(self, grocy):
        shopping_list = grocy.shopping_list(True)

        assert isinstance(shopping_list, list)
        assert len(shopping_list) == 7
        for item in shopping_list:
            assert isinstance(item, ShoppingListProduct)
            assert isinstance(item.id, int)
            if item.product_id:
                assert isinstance(item.product_id, int)
                assert isinstance(item.product, Product)
                assert isinstance(item.product.id, int)
            assert isinstance(item.amount, float)
            if item.note:
                assert isinstance(item.note, str)

        item = next(item for item in shopping_list if item.id == 2)
        assert item.note is None
        assert item.amount == 1.0
        assert item.product_id == 20

    @pytest.mark.vcr
    def test_add_missing_product_to_shopping_list_valid(self, grocy):
        assert grocy.add_missing_product_to_shopping_list() is None

    @pytest.mark.vcr
    def test_add_product_to_shopping_list_valid(self, grocy):
        grocy.add_product_to_shopping_list(19)

    @pytest.mark.vcr
    def test_add_nonexistant_product_to_shopping_list(self, grocy):
        with pytest.raises(GrocyError) as exc_info:
            grocy.add_product_to_shopping_list(3000)

        error = exc_info.value
        assert error.status_code == 400
        assert error.message == "Product does not exist or is inactive"

    @pytest.mark.vcr
    def test_add_missing_products_to_nonexistant_shopping_list(self, grocy):
        with pytest.raises(GrocyError) as exc_info:
            grocy.add_missing_product_to_shopping_list(3000)

        error = exc_info.value
        assert error.status_code == 400
        assert error.message == "Shopping list does not exist"

    @pytest.mark.vcr
    def test_clear_shopping_list_valid(self, grocy):
        grocy.clear_shopping_list()

    @pytest.mark.vcr
    def test_remove_product_in_shopping_list_valid(self, grocy):
        grocy.remove_product_in_shopping_list(20)
