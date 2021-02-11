from datetime import datetime

import pytest

from pygrocy.data_models.chore import AssignmentType, Chore, PeriodType
from pygrocy.data_models.user import User


class TestChores:
    @pytest.mark.vcr
    def test_get_chores_valid(self, grocy):
        chores = grocy.chores(get_details=True)

        assert isinstance(chores, list)
        assert len(chores) == 6
        for chore in chores:
            assert isinstance(chore, Chore)
            assert isinstance(chore.id, int)
            assert isinstance(chore.last_tracked_time, datetime)
            assert isinstance(chore.next_estimated_execution_time, datetime)
            assert isinstance(chore.name, str)
            assert isinstance(chore.last_done_by, User)

        chore = next(chore for chore in chores if chore.id == 6)
        assert chore.name == "The thing which happens on Mondays and Wednesdays"
        assert chore.period_type == PeriodType.WEEKLY
        assert chore.last_done_by.id == 1

    @pytest.mark.vcr
    def test_get_chore_details(self, grocy):
        chore_details = grocy.chore(3)
        assert isinstance(chore_details, Chore)

        assert chore_details.name == "Lawn mowed in the garden"
        assert chore_details.period_type == PeriodType.DYNAMIC_REGULAR
        assert chore_details.last_done_by.id == 1
        assert chore_details.assignment_type == AssignmentType.RANDOM
