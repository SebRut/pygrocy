import datetime

import pytest

from pygrocy.errors import GrocyError


class TestMealPlanSections:
    @pytest.mark.vcr
    def test_get_sections_valid(self, grocy):
        sections = grocy.meal_plan_sections()

        assert len(sections) == 4
        section = sections[1]
        assert section.id == 1
        assert section.name == "Breakfast"
        assert section.sort_number == 10
        assert isinstance(section.row_created_timestamp, datetime.datetime)

    @pytest.mark.vcr
    def test_get_section_by_id_valid(self, grocy):
        section = grocy.meal_plan_section(1)

        assert section.id == 1

    @pytest.mark.vcr
    def test_get_section_by_id_invalid(self, grocy):
        section = grocy.meal_plan_section(1000)
        assert section is None

    @pytest.mark.vcr
    def test_get_sections_filters_valid(self, grocy):
        query_filter = ["name=Breakfast"]
        sections = grocy.meal_plan_sections(query_filters=query_filter)

        for item in sections:
            assert item.name == "Breakfast"

    @pytest.mark.vcr
    def test_get_sections_filters_invalid(self, grocy, invalid_query_filter):
        with pytest.raises(GrocyError) as exc_info:
            grocy.meal_plan_sections(query_filters=invalid_query_filter)

        error = exc_info.value
        assert error.status_code == 500
