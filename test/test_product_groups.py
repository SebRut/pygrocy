import pytest

from pygrocy.data_models.product import Group


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
