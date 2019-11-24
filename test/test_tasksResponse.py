import json
from unittest import TestCase

from pygrocy.grocy_api_client import TasksResponse


class TestTasksResponse(TestCase):
    def test_parse(self):
        input_json = """{
            "id": 0,
            "category_id": 0,
            "name": "string",
            "description": "string",
            "due_date": "2019-05-04T11:31:04.563Z",
            "done": 0,
            "done_timestamp": ,
            "assigned_to_user_id": 0
        }"""

        response = TasksResponse(json.loads(input_json))

        assert response.task_id == 0
        assert response.name == "string"
        assert response.done_timestamp is None
        