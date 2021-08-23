from datetime import datetime

import pytest

from pygrocy.data_models.chore import AssignmentType, Chore, PeriodType
from pygrocy.data_models.user import User
from pygrocy.errors.grocy_error import GrocyError


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
        assert chore.period_config == "monday,wednesday"

    @pytest.mark.vcr
    def test_get_chore_details(self, grocy):
        chore_details = grocy.chore(3)
        assert isinstance(chore_details, Chore)

        assert chore_details.name == "Lawn mowed in the garden"
        assert chore_details.assignment_type == AssignmentType.RANDOM
        assert chore_details.last_done_by.id == 1
        assert chore_details.period_type == PeriodType.DYNAMIC_REGULAR
        assert chore_details.period_days == 21
        assert chore_details.period_config is None
        assert chore_details.track_date_only is False
        assert chore_details.rollover is False
        assert chore_details.assignment_config == "1,2,3,4"
        assert chore_details.next_execution_assigned_user.id == 2
        assert chore_details.next_execution_assigned_to_user_id == 2
        assert chore_details.userfields is None

    @pytest.mark.vcr
    def test_execute_chore_valid(self, grocy):
        result = grocy.execute_chore(1)
        assert not isinstance(result, GrocyError)

    @pytest.mark.vcr
    def test_execute_chore_valid_with_data(self, grocy):
        result = grocy.execute_chore(1, done_by=1, tracked_time=datetime.now())
        assert not isinstance(result, GrocyError)

    @pytest.mark.vcr
    def test_execute_chore_invalid(self, grocy):
        with pytest.raises(GrocyError) as exc_info:
            grocy.execute_chore(1000)

        error = exc_info.value
        assert error.status_code == 400
