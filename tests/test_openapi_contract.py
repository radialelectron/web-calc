import json
import os

from main import app

CONTRACT = os.path.join(
    os.path.dirname(__file__), "..", "contracts", "webcalc-openapi.json"
)


def test_committed_openapi_contract_matches_app():
    """Fails when the API changes without regenerating contracts/webcalc-openapi.json
    (run `python contracts/export_openapi.py`)."""
    with open(CONTRACT) as f:
        committed = json.load(f)
    assert committed == json.loads(json.dumps(app.openapi()))
