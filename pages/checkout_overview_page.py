from __future__ import annotations

import re

from playwright.sync_api import Page
from pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    path_glob = "**/checkout-step-two.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def finish(self) -> None:
        self.by_test_id("finish").click()
        self.wait_url("**/checkout-complete.html")

    def line_item_count(self) -> int:
        return self.by_test_id("inventory-item").count()

    def assert_money_line_present(self) -> None:
        subtotal = self.by_test_id("subtotal-label").inner_text()
        assert re.search(r"\$\d+\.\d{2}", subtotal), f"Unexpected subtotal line: {subtotal!r}"

    def assert_summary_lines_match_pattern(self) -> None:
        subtotal = self.by_test_id("subtotal-label").inner_text()
        tax = self.by_test_id("tax-label").inner_text()
        total = self.by_test_id("total-label").inner_text()
        assert re.search(r"Item total: \$\d+\.\d{2}", subtotal), subtotal
        assert re.search(r"Tax: \$\d+\.\d{2}", tax), tax
        assert re.search(r"Total: \$\d+\.\d{2}", total), total
