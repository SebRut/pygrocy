import json
from unittest import TestCase

from pygrocy.grocy_api_client import ChoreDetailsResponse


class TestChoreDetailsResponse(TestCase):
    def test_parse(self):
        input_json = """{
            "chore": {
                "id": 0,
                "name": "string",
                "description": "string",
                "period_type": "manually",
                "period_days": 0,
                "row_created_timestamp": "2019-05-04T11:31:04.563Z"
            },
            "last_tracked": "2019-05-04T11:31:04.563Z",
            "track_count": 0,
            "last_done_by": {
                "id": 0,
                "username": "string",
                "first_name": "string",
                "last_name": "string",
                "display_name": "string",
                "row_created_timestamp": "2019-05-04T11:31:04.564Z"
            },
            "next_estimated_execution_time": "2019-05-04T11:31:04.564Z",
            "next_execution_assigned_user": {
                "id": 42,
                "username": "string",
                "first_name": "string",
                "last_name": "string",
                "display_name": "string",
                "row_created_timestamp": "2019-05-04T11:31:04.564Z"
            }
        }"""

        response = ChoreDetailsResponse(json.loads(input_json))

        assert response.chore.id == 0
        assert response.chore.name == "string"

        assert response.last_done_by.display_name == "string"

        assert response.next_execution_assigned_user.id == 42
        assert response.next_execution_assigned_user.display_name == "string"

    def test_no_last_tracked_data(self):
        input_json = """{
            "chore": {
                "id": 0,
                "name": "string",
                "description": "string",
                "period_type": "manually",
                "period_days": 0,
                "row_created_timestamp": "2019-05-04T11:31:04.563Z"
            },
            "last_tracked": null,
            "track_count": 0,
            "last_done_by": null,
            "next_estimated_execution_time": "2019-05-04T11:31:04.564Z"
        }"""

        response = ChoreDetailsResponse(json.loads(input_json))

        assert response.last_tracked is None
        assert response.last_done_by is None
