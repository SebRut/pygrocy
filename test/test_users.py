import pytest

from pygrocy.data_models.user import User


class TestUsers:
    @pytest.mark.vcr
    def test_get_user_by_id_valid(self, grocy):
        user = grocy.user(user_id=1)
        assert isinstance(user, User)
        assert user.id == 1
        assert user.display_name == "Demo User"
        assert user.username == "Demo User"

    @pytest.mark.vcr
    def test_get_users_valid(self, grocy):
        users = grocy.users()

        assert len(users) == 4
        user = users[0]
        assert isinstance(user, User)
