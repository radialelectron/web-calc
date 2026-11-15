import os

# Webcalc is a runtime dependency: this service calls its HTTP API.
WEBCALC_BASE_URL = os.environ.get("WEBCALC_BASE_URL", "http://localhost:8000")

# Contract this consumer was written against (path relative to repo root).
WEBCALC_CONTRACT = "contracts/webcalc-openapi.json"
