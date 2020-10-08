from datetime import datetime
from typing import Dict
from pygrocy.base import DataModel
from pygrocy.grocy_api_client import TaskResponse


class Task(DataModel):
    def __init__(self, response: TaskResponse):

        self._id = response.id
        self._name = response.name
        self._description = response.description
        self._due_date = response.due_date
        self._done = response.done
        self._done_timestamp = response.done_timestamp
        self._category_id = response.category_id
        self._assigned_to_user_id = response.assigned_to_user_id
        self._userfields = response.userfields

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def due_date(self) -> datetime:
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
    def assigned_to_user_id(self) -> int:
        return self._assigned_to_user_id

    @property
    def userfields(self) -> Dict[str, str]:
        return self._userfields