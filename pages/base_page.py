from __future__ import annotations

from playwright.sync_api import Locator, Page

from config.settings import NAVIGATION_TIMEOUT_MS


class BasePage:
    """Thin wrapper: one place for timeouts and data-test locator helper."""

    path_glob: str | None = None

    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_navigation_timeout(NAVIGATION_TIMEOUT_MS)
        self.page.set_default_timeout(NAVIGATION_TIMEOUT_MS)

    def by_test_id(self, value: str) -> Locator:
        return self.page.locator(f'[data-test="{value}"]')

    def wait_url(self, glob_pattern: str) -> None:
        """Playwright glob (e.g. **/cart.html); prefer over expect().to_have_url for path wildcards."""
        self.page.wait_for_url(glob_pattern, timeout=NAVIGATION_TIMEOUT_MS)

    def expect_loaded(self) -> None:
        if self.path_glob:
            self.wait_url(self.path_glob)

