from __future__ import annotations

from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    path_glob = "**/cart.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def line_items(self):
        return self.by_test_id("inventory-item")

    def line_item_count(self) -> int:
        return self.line_items().count()

    def checkout(self) -> None:
        self.by_test_id("checkout").click()
        self.wait_url("**/checkout-step-one.html")

    def remove_item(self, product_slug: str) -> None:
        self.by_test_id(f"remove-{product_slug}").click()

    def continue_shopping(self) -> None:
        self.by_test_id("continue-shopping").click()
        self.wait_url("**/inventory.html")
