from pygrocy.base import DataModel
from pygrocy.grocy_api_client import UserDto


class User(DataModel):
    def __init__(self, user_dto: UserDto):
        self._id = user_dto.id
        self._username = user_dto.username
        self._first_name = user_dto.first_name
        self._last_name = user_dto.last_name
        self._display_name = user_dto.display_name

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self) -> str:
        return self._username

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def display_name(self) -> str:
        return self._display_name