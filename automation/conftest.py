import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import pytest

from api_client import WebCalcClient


@pytest.fixture(scope="session")
def api():
    return WebCalcClient()
