from __future__ import annotations

import os
import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, sync_playwright

from pages.login_page import LoginPage

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser_type_launch_args():
    headed = os.environ.get("HEADED", "").lower() in ("1", "true", "yes")
    return {"headless": not headed}


@pytest.fixture(scope="session")
def browser(playwright_instance, browser_type_launch_args):
    chromium = playwright_instance.chromium.launch(**browser_type_launch_args)
    yield chromium
    chromium.close()


@pytest.fixture
def browser_context(browser, base_url):
    video_dir = os.environ.get("PW_VIDEO_DIR")
    context_kwargs = {
        "base_url": base_url,
        "viewport": {"width": 1280, "height": 720},
    }
    if video_dir:
        path = Path(video_dir)
        path.mkdir(parents=True, exist_ok=True)
        context_kwargs["record_video_dir"] = str(path)

    context = browser.new_context(**context_kwargs)
    yield context
    context.close()


@pytest.fixture
def page(browser_context) -> Page:
    new_page = browser_context.new_page()
    yield new_page
    if not new_page.is_closed():
        new_page.close()


@pytest.fixture
def authenticated_page(page: Page) -> Page:
    """New session: `standard_user` on inventory."""
    login = LoginPage(page)
    login.open()
    login.login_as_standard_user()
    page.wait_for_url("**/inventory.html")
    return page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    pg: Page | None = item.funcargs.get("page")
    if pg is None or pg.is_closed():
        return

    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^\w.\-]+", "_", item.nodeid)[:180]
    target = SCREENSHOTS_DIR / f"{safe}.png"
    try:
        pg.screenshot(path=str(target), full_page=True)
    except Exception:
        pass
