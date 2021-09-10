from datetime import datetime
from typing import Dict

from pygrocy.base import DataModel
from pygrocy.data_models.user import User
from pygrocy.grocy_api_client import TaskCategoryDto, TaskResponse


class TaskCategory(DataModel):
    def __init__(self, data: TaskCategoryDto):
        self._id = data.id
        self._name = data.name
        self._description = data.description
        self._row_created_timestamp = data.row_created_timestamp

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def row_created_timestamp(self) -> datetime:
        return self._row_created_timestamp


class Task(DataModel):
    def __init__(self, response: TaskResponse):

        self._id = response.id
        self._name = response.name
        self._description = response.description
        self._due_date = response.due_date
        self._done = response.done
        self._done_timestamp = response.done_timestamp
        self._category_id = response.category_id
        if response.category:
            self._category = TaskCategory(response.category)
        self._assigned_to_user_id = response.assigned_to_user_id
        if response.assigned_to_user:
            self._assigned_to_user = User(response.assigned_to_user)
        self._userfields = response.userfields

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def due_date(self) -> datetime.date:
        return self._due_date

    @property
    def done(self) -> int:
        return self._done

    @property
    def done_timestamp(self) -> datetime:
        return self._done_timestamp

    @property
    def category_id(self) -> int:
        return self._category_id

    @property
    def category(self) -> TaskCategory:
        return self._category

    @property
    def assigned_to_user_id(self) -> int:
        return self._assigned_to_user_id

    @property
    def assigned_to_user(self) -> User:
        return self._assigned_to_user

    @property
    def userfields(self) -> Dict[str, str]:
        return self._userfields
