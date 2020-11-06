from datetime import datetime
from enum import Enum
from typing import List, Dict
from pygrocy.base import DataModel
from pygrocy.data_models.user import User
from pygrocy.grocy_api_client import CurrentChoreResponse, ChoreDetailsResponse, GrocyApiClient


class PeriodType(str, Enum):
    MANUALLY = "manually"
    DYNAMIC_REGULAR = "dynamic-regular"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class AssignmentType(str, Enum):
    NO_ASSIGNMENT = "no-assignment"
    WHO_LEAST_DID_FIRST = "who-least-did-first"
    RANDOM = "random"
    IN_ALPHABETICAL_ORDER = "in-alphabetical-order"


class Chore(DataModel):
    def __init__(self, response):
        if isinstance(response, CurrentChoreResponse):
            self._init_from_CurrentChoreResponse(response)
        elif isinstance(response, ChoreDetailsResponse):
            self._init_from_ChoreDetailsResponse(response)

    # noinspection PyPep8Naming
    def _init_from_CurrentChoreResponse(self, response: CurrentChoreResponse):
        self._id = response.chore_id
        self._last_tracked_time = response.last_tracked_time
        self._next_estimated_execution_time = response.next_estimated_execution_time
        self._name = None
        self._last_done_by = None

    # noinspection PyPep8Naming
    def _init_from_ChoreDetailsResponse(self, response: ChoreDetailsResponse):
        chore_data = response.chore
        self._id = chore_data.id
        self._name = chore_data.name
        self._description = chore_data.description

        if chore_data.period_type is not None:
            self._period_type = PeriodType(chore_data.period_type)
        else:
            self._period_type = None

        self._period_config = chore_data.period_config
        self._period_days = chore_data.period_days
        self._track_date_only = chore_data.track_date_only
        self._rollover = chore_data.rollover

        if chore_data.assignment_type is not None:
            self._assignment_type = AssignmentType(chore_data.assignment_type)
        else:
            self._assignment_type = None

        self._assignment_config = chore_data.assignment_config
        self._next_execution_assigned_to_user_id = (
            chore_data.next_execution_assigned_to_user_id
        )
        self._userfields = chore_data.userfields

        self._last_tracked_time = response.last_tracked
        self._next_estimated_execution_time = response.next_estimated_execution_time
        if response.last_done_by is not None:
            self._last_done_by = User(response.last_done_by)
        else:
            self._last_done_by = None
        self._track_count = response.track_count
        if response.next_execution_assigned_user is not None:
            self._next_execution_assigned_user = User(
                response.next_execution_assigned_user
            )
        else:
            self._next_execution_assigned_user = None

    def get_details(self, api_client: GrocyApiClient):
        details = api_client.get_chore(self.id)
        self._init_from_ChoreDetailsResponse(details)

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
    def period_type(self) -> PeriodType:
        return self._period_type

    @property
    def period_config(self) -> str:
        return self._period_config

    @property
    def period_days(self) -> int:
        return self._period_days

    @property
    def track_date_only(self) -> bool:
        return self._track_date_only

    @property
    def rollover(self) -> bool:
        return self._rollover

    @property
    def assignment_type(self) -> AssignmentType:
        return self._assignment_type

    @property
    def assignment_config(self) -> str:
        return self._assignment_config

    @property
    def next_execution_assigned_to_user_id(self) -> int:
        return self._next_execution_assigned_to_user_id

    @property
    def userfields(self) -> Dict[str, str]:
        return self._userfields

    @property
    def last_tracked_time(self) -> datetime:
        return self._last_tracked_time

    @property
    def next_estimated_execution_time(self) -> datetime:
        return self._next_estimated_execution_time

    @property
    def last_done_by(self) -> User:
        return self._last_done_by

    @property
    def track_count(self) -> int:
        return self._track_count

    @property
    def next_execution_assigned_user(self) -> User:
        return self._next_execution_assigned_user
