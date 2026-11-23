import os

import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    headless = os.getenv("HEADLESS_MODE", "true").lower() == "true"
    slow_mo = int(os.getenv("SLOW_MO", "0"))

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=headless,
            slow_mo=slow_mo
        )

        yield browser

        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()

    yield page

    context.close()
