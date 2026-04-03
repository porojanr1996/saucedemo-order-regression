"""End-to-end purchase journeys — what release sign-off usually hinges on."""

from __future__ import annotations

import pytest

from config.test_data import CUSTOMER_ALT, DEFAULT_CUSTOMER, PRODUCT_BACKPACK, PRODUCT_BIKE_LIGHT
from flows.order_flow import complete_checkout_from_cart
from pages.cart_page import CartPage
from pages.checkout_information_page import CheckoutInformationPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from pages.order_complete_page import OrderCompletePage

pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_smoke_single_item_happy_path(authenticated_page):
    inv = InventoryPage(authenticated_page)
    inv.add_to_cart(PRODUCT_BACKPACK)
    inv.expect_cart_badge("1")
    inv.open_cart()
    done = complete_checkout_from_cart(authenticated_page, DEFAULT_CUSTOMER)
    done.assert_success()


def test_single_item_line_count_and_subtotal_on_overview(authenticated_page):
    inv = InventoryPage(authenticated_page)
    inv.add_to_cart(PRODUCT_BACKPACK)
    inv.open_cart()

    cart = CartPage(authenticated_page)
    assert cart.line_item_count() == 1
    cart.checkout()

    step_one = CheckoutInformationPage(authenticated_page)
    step_one.fill(DEFAULT_CUSTOMER)
    step_one.continue_to_overview()

    overview = CheckoutOverviewPage(authenticated_page)
    assert overview.line_item_count() == 1
    overview.assert_money_line_present()
    overview.finish()

    OrderCompletePage(authenticated_page).assert_success()


def test_multi_item_cart_totals_match_expected_pattern(authenticated_page):
    inv = InventoryPage(authenticated_page)
    inv.add_to_cart(PRODUCT_BACKPACK)
    inv.add_to_cart(PRODUCT_BIKE_LIGHT)
    inv.expect_cart_badge("2")
    inv.open_cart()

    cart = CartPage(authenticated_page)
    assert cart.line_item_count() == 2
    cart.checkout()

    step_one = CheckoutInformationPage(authenticated_page)
    step_one.fill(CUSTOMER_ALT)
    step_one.continue_to_overview()

    overview = CheckoutOverviewPage(authenticated_page)
    overview.assert_summary_lines_match_pattern()
    overview.finish()

    OrderCompletePage(authenticated_page).assert_success()
