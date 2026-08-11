"""Automates TC-09 and TC-17 from the Confluence Test Cases page: full-stack
E2E checks driven through the actual calculator buttons in a real browser.
"""
import pathlib

import pytest
from playwright.sync_api import sync_playwright

from config import BASE_URL

FRONTEND_INDEX = pathlib.Path(__file__).resolve().parents[1] / "frontend" / "index.html"


@pytest.fixture()
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page()
        pg.add_init_script(f"window.WEB_CALC_API_BASE = '{BASE_URL}';")
        pg.goto(f"file://{FRONTEND_INDEX}")
        yield pg
        browser.close()


def test_tc09_standard_calculation_e2e(page):
    page.click("[data-digit='1']")
    page.click("[data-digit='2']")
    page.click("[data-action='add']")
    page.click("[data-digit='8']")
    page.click("[data-action='equals']")
    page.wait_for_function("document.getElementById('result').textContent !== '...'")
    assert page.inner_text("#result") == "20"


def test_tc17_scientific_calculation_e2e(page):
    page.click("#mode-scientific")
    page.click("[data-digit='9']")
    page.click("[data-digit='0']")
    page.click("[data-sci='sin']")
    page.click("[data-action='equals']")
    page.wait_for_function("document.getElementById('result').textContent !== '...'")
    assert page.inner_text("#result") == "1"
