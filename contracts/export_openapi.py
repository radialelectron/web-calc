"""Regenerate contracts/webcalc-openapi.json from the FastAPI app."""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "backend"))

from main import app  # noqa: E402

if __name__ == "__main__":
    with open(os.path.join(HERE, "webcalc-openapi.json"), "w") as f:
        json.dump(app.openapi(), f, indent=2, sort_keys=True)
        f.write("\n")
