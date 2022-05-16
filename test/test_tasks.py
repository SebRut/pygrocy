from datetime import datetime

import pytest

from pygrocy.data_models.task import TaskCategory
from pygrocy.data_models.user import User
from pygrocy.errors import GrocyError


class TestTasks:
    @pytest.mark.vcr
    def test_get_tasks_valid(self, grocy):
        tasks = grocy.tasks()

        assert len(tasks) == 5
        task = tasks[1]
        assert task.id == 2
        assert task.name == "Task2"
        assert isinstance(task.assigned_to_user, User)
        assert isinstance(task.category, TaskCategory)
        assert task.category.id == 1
        assert task.category.name == "Category1"

    @pytest.mark.vcr
    def test_get_task_valid(self, grocy):
        task = grocy.task(2)

        assert task.id == 2
        assert task.name == "Task2"
        assert isinstance(task.assigned_to_user, User)
        assert isinstance(task.category, TaskCategory)
        assert task.category.id == 1
        assert task.category.name == "Category1"

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
