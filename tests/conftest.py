import pytest
from playwright.sync_api import Page, sync_playwright


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture
def page_context(playwright_instance, base_url):
    browser = playwright_instance.chromium.launch(headless=True)
    context = browser.new_context(
        base_url=base_url,
        viewport={"width": 1280, "height": 720},
    )
    page = context.new_page()
    yield page
    context.close()
    browser.close()


@pytest.fixture
def logged_in(page_context: Page, base_url) -> Page:
    page = page_context
    page.goto("/")
    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()
    page.wait_for_url("**/inventory.html")
    return page
