from __future__ import annotations

from playwright.sync_api import Page, expect

from config.settings import EXPECT_TIMEOUT_MS
from config.test_data import MSG_ORDER_THANK_YOU
from pages.base_page import BasePage


class OrderCompletePage(BasePage):
    path_glob = "**/checkout-complete.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def assert_success(self) -> None:
        expect(self.by_test_id("complete-header")).to_have_text(
            MSG_ORDER_THANK_YOU,
            timeout=EXPECT_TIMEOUT_MS,
        )
        expect(self.by_test_id("complete-text")).to_be_visible(timeout=EXPECT_TIMEOUT_MS)
