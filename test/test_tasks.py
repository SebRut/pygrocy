from datetime import datetime

import pytest


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
