import os

BASE_URL = os.environ.get("WEB_CALC_BASE_URL", "http://127.0.0.1:8000")
TIMEOUT = float(os.environ.get("WEB_CALC_TIMEOUT", "5"))
