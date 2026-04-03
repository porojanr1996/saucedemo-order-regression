from __future__ import annotations

from playwright.sync_api import Page

from config.test_data import PRODUCT_BACKPACK, CustomerInfo
from pages.cart_page import CartPage
from pages.checkout_information_page import CheckoutInformationPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from pages.order_complete_page import OrderCompletePage


def add_product_and_open_cart(page: Page, product_slug: str = PRODUCT_BACKPACK) -> CartPage:
    inv = InventoryPage(page)
    inv.add_to_cart(product_slug)
    inv.open_cart()
    return CartPage(page)


def complete_checkout_from_cart(page: Page, shipping: CustomerInfo) -> OrderCompletePage:
    """Cart → Your information → Overview → Complete."""
    cart = CartPage(page)
    cart.checkout()
    info = CheckoutInformationPage(page)
    info.fill(shipping)
    info.continue_to_overview()
    overview = CheckoutOverviewPage(page)
    overview.finish()
    return OrderCompletePage(page)
