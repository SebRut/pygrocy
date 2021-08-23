import pytest

from pygrocy.data_models.generic import EntityType
from pygrocy.errors.grocy_error import GrocyError


class TestGeneric:
    @pytest.mark.vcr
    def test_generic_add_valid(self, grocy):
        data = {"name": "Testbattery"}

        grocy.add_generic(EntityType.BATTERIES, data)

    @pytest.mark.vcr
    def test_generic_add_invalid(self, grocy):
        data = {"eman": "Testbattery"}

        with pytest.raises(GrocyError) as exc_info:
            grocy.add_generic(EntityType.BATTERIES, data)

        error = exc_info.value
        assert error.status_code == 400

    @pytest.mark.vcr
    def test_generic_update_valid(self, grocy):
        updated_data = {"name": "Le new battery"}

        grocy.update_generic(EntityType.BATTERIES, 1, updated_data)

    @pytest.mark.vcr
    def test_generic_update_invalid_id(self, grocy):
        updated_data = {"name": "Le new battery"}

        with pytest.raises(GrocyError) as exc_info:
            grocy.update_generic(EntityType.BATTERIES, 1000, updated_data)

        error = exc_info.value
        assert error.status_code == 400
        assert error.message == "Object not found"

    @pytest.mark.vcr
    def test_generic_update_invalid_data(self, grocy):
        with pytest.raises(GrocyError) as exc_info:
            grocy.update_generic(EntityType.BATTERIES, 1, None)

        error = exc_info.value
        assert error.status_code == 400
        assert error.message[:7] == "Request"

    @pytest.mark.vcr
    def test_delete_generic_success(self, grocy):
        grocy.delete_generic(EntityType.TASKS, 3)

    @pytest.mark.vcr
    def test_delete_generic_error(self, grocy):
        with pytest.raises(GrocyError) as exc_info:
            grocy.delete_generic(EntityType.TASKS, 30000)

        error = exc_info.value
        assert error.status_code == 404
