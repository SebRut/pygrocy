import json
from unittest import TestCase

from pygrocy.grocy_api_client import CurrentChoreResponse


class TestCurrentChoreResponse(TestCase):
    def test_parse(self):
        input_json = """{ "chore_id": "4", "last_tracked_time": null, "next_estimated_execution_time": "2999-12-31 23:59:59", "track_date_only": "0", "next_execution_assigned_to_user_id": null }"""

        response = CurrentChoreResponse(json.loads(input_json))

        assert response.chore_id == 4
    
