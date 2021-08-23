from datetime import datetime

import pytest

from pygrocy.errors import GrocyError


class TestTasks:
    @pytest.mark.vcr
    def test_get_tasks_valid(self, grocy):
        tasks = grocy.tasks()

        assert len(tasks) == 6
        assert tasks[0].id == 1
        assert tasks[0].name == "Repair the garage door"

    @pytest.mark.vcr
    def test_complete_task_valid_with_defaults(self, grocy):
        grocy.complete_task(3)

    @pytest.mark.vcr
    def test_complete_task_valid(self, grocy):
        grocy.complete_task(4, done_time=datetime.now())

    @pytest.mark.vcr
    def test_complete_task_invalid(self, grocy):
        with pytest.raises(GrocyError) as exc_info:
            grocy.complete_task(1000)

        error = exc_info.value
        assert error.status_code == 400
