import pytest

from pygrocy.data_models.product import Group
from pygrocy.errors import GrocyError


class TestProductGroups:
    @pytest.mark.vcr
    def test_get_product_groups_valid(self, grocy):
        product_groups_list = grocy.product_groups()

        assert isinstance(product_groups_list, list)
        assert len(product_groups_list) == 6
        for group in product_groups_list:
            assert isinstance(group, Group)
            assert isinstance(group.id, int)
            assert isinstance(group.name, str)
            if group.description:
                assert isinstance(group.description, str)

        group = next(group for group in product_groups_list if group.id == 1)
        assert group.name == "01 Sweets"
        assert group.description is None

    @pytest.mark.vcr
    def test_get_product_groups_filters_valid(self, grocy):
        query_filter = ["id=6"]
        product_groups = grocy.product_groups(query_filters=query_filter)

        for item in product_groups:
            assert item.id == 6

    @pytest.mark.vcr
    def test_get_product_groups_filters_invalid(self, grocy, invalid_query_filter):
        with pytest.raises(GrocyError) as exc_info:
            grocy.product_groups(query_filters=invalid_query_filter)

        error = exc_info.value
        assert error.status_code == 500
