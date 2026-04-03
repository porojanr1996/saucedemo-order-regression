from __future__ import annotations

from playwright.sync_api import Page, expect

from config.settings import EXPECT_TIMEOUT_MS
from pages.base_page import BasePage


class InventoryPage(BasePage):
    path_glob = "**/inventory.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def add_to_cart(self, product_slug: str) -> None:
        self.by_test_id(f"add-to-cart-{product_slug}").click()

    def open_cart(self) -> None:
        self.by_test_id("shopping-cart-link").click()
        self.wait_url("**/cart.html")

    def cart_badge_count(self) -> str:
        return self.by_test_id("shopping-cart-badge").inner_text()

    def expect_cart_badge(self, count: str) -> None:
        expect(self.by_test_id("shopping-cart-badge")).to_have_text(count, timeout=EXPECT_TIMEOUT_MS)
