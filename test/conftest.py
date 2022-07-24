from test.test_const import CONST_BASE_URL, CONST_PORT, CONST_SSL
from typing import List

import pytest

from pygrocy import Grocy


@pytest.fixture
def grocy():
    yield Grocy(CONST_BASE_URL, "demo_mode", verify_ssl=CONST_SSL, port=CONST_PORT)


# noinspection PyProtectedMember
@pytest.fixture
def grocy_api_client(grocy):
    yield grocy._api_client


@pytest.fixture
def vcr_config():
    yield {"record_mode": "once", "decode_compressed_response": True}


@pytest.fixture
def invalid_query_filter() -> List[str]:
    yield ["invalid"]
