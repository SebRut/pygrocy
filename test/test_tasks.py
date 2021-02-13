import pytest


class TestTasks:
    @pytest.mark.vcr
    def test_get_tasks_valid(self, grocy):
        tasks = grocy.tasks()

        assert len(tasks) == 6
        assert tasks[0].id == 1
        assert tasks[0].name == "Repair the garage door"
