"""Cart, checkout navigation, and empty-cart behavior."""

from __future__ import annotations

import pytest

from config.test_data import DEFAULT_CUSTOMER, PRODUCT_BACKPACK, PRODUCT_BIKE_LIGHT
from flows.order_flow import complete_checkout_from_cart
from pages.cart_page import CartPage
from pages.checkout_information_page import CheckoutInformationPage
from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.regression


def test_cancel_from_checkout_returns_to_cart_with_items_intact(authenticated_page):
    inv = InventoryPage(authenticated_page)
    inv.add_to_cart(PRODUCT_BACKPACK)
    inv.open_cart()
    CartPage(authenticated_page).checkout()

    CheckoutInformationPage(authenticated_page).cancel()

    cart = CartPage(authenticated_page)
    assert cart.line_item_count() == 1


def test_remove_line_updates_badge_and_cart(authenticated_page):
    inv = InventoryPage(authenticated_page)
    inv.add_to_cart(PRODUCT_BACKPACK)
    inv.add_to_cart(PRODUCT_BIKE_LIGHT)
    inv.expect_cart_badge("2")
    inv.open_cart()

    cart = CartPage(authenticated_page)
    cart.remove_item(PRODUCT_BACKPACK)
    inv.expect_cart_badge("1")
    assert cart.line_item_count() == 1


def test_continue_shopping_returns_to_product_grid(authenticated_page):
    inv = InventoryPage(authenticated_page)
    inv.add_to_cart(PRODUCT_BACKPACK)
    inv.open_cart()
    CartPage(authenticated_page).continue_shopping()

    assert InventoryPage(authenticated_page).by_test_id("inventory-container").is_visible()


def test_empty_cart_still_allows_checkout_today(authenticated_page):
    """Sauce Demo currently allows checkout with zero cart lines; update if product rules change."""
    inv = InventoryPage(authenticated_page)
    inv.open_cart()
    cart = CartPage(authenticated_page)
    assert cart.line_item_count() == 0
    assert cart.by_test_id("checkout").is_enabled()

    done = complete_checkout_from_cart(authenticated_page, DEFAULT_CUSTOMER)
    done.assert_success()
