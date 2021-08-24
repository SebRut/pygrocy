import datetime

import pytest


class TestMealPlanSections:
    @pytest.mark.vcr
    def test_get_sections_valid(self, grocy):
        sections = grocy.meal_plan_sections()

        assert len(sections) == 2
        section = sections[1]
        assert section.id == 1
        assert section.name == "Breakfast"
        assert section.sort_number == 3
        assert isinstance(section.row_created_timestamp, datetime.datetime)

    @pytest.mark.vcr
    def test_get_section_by_id_valid(self, grocy):
        section = grocy.meal_plan_section(1)

        assert section.id == 1

    @pytest.mark.vcr
    def test_get_section_by_id_invalid(self, grocy):
        section = grocy.meal_plan_section(1000)
        assert section is None
