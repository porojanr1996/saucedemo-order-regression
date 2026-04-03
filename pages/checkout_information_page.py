from __future__ import annotations

from playwright.sync_api import Page, expect

from config.settings import EXPECT_TIMEOUT_MS
from config.test_data import CustomerInfo
from pages.base_page import BasePage


class CheckoutInformationPage(BasePage):
    path_glob = "**/checkout-step-one.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def fill(self, info: CustomerInfo) -> None:
        self.by_test_id("firstName").fill(info.first_name)
        self.by_test_id("lastName").fill(info.last_name)
        self.by_test_id("postalCode").fill(info.postal_code)

    def continue_to_overview(self) -> None:
        self.by_test_id("continue").click()
        self.wait_url("**/checkout-step-two.html")

    def attempt_continue_expecting_inline_error(self) -> None:
        """Submit an invalid form; page stays on step one and shows [data-test=error]."""
        self.by_test_id("continue").click()

    def cancel(self) -> None:
        self.by_test_id("cancel").click()
        self.wait_url("**/cart.html")

    def assert_inline_error(self, full_message: str) -> None:
        err = self.by_test_id("error")
        expect(err).to_be_visible(timeout=EXPECT_TIMEOUT_MS)
        expect(err).to_have_text(full_message, timeout=EXPECT_TIMEOUT_MS)
