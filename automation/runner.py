"""Single entry point for the automation suite: boots the backend on a
dedicated port, waits for it to be healthy, runs pytest against this
directory, then tears the backend down. Usage: python automation/runner.py
"""
import os
import subprocess
import sys
import time

import requests

AUTOMATION_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(AUTOMATION_DIR, "..", "backend")
PORT = 8010
BASE_URL = f"http://127.0.0.1:{PORT}"


def wait_for_health(url, timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        try:
            if requests.get(f"{url}/api/health", timeout=1).status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.3)
    return False


def main():
    env = os.environ.copy()
    env["WEB_CALC_BASE_URL"] = BASE_URL

    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", str(PORT)],
        cwd=BACKEND_DIR,
        env=env,
    )
    try:
        if not wait_for_health(BASE_URL):
            print("Backend did not become healthy in time")
            sys.exit(1)

        result = subprocess.run(
            [sys.executable, "-m", "pytest", AUTOMATION_DIR, "-v"],
            env=env,
        )
        sys.exit(result.returncode)
    finally:
        proc.terminate()
        proc.wait()


if __name__ == "__main__":
    main()
