"""Checkout step one (Your information) — field validation is cheap to automate and expensive when it breaks."""

from __future__ import annotations

import pytest

from config.test_data import (
    MSG_FIRST_NAME_REQUIRED,
    MSG_LAST_NAME_REQUIRED,
    MSG_POSTAL_REQUIRED,
    PRODUCT_BACKPACK,
)
from pages.cart_page import CartPage
from pages.checkout_information_page import CheckoutInformationPage
from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.regression


def _open_checkout_step_one_with_one_item(page) -> CheckoutInformationPage:
    inv = InventoryPage(page)
    inv.add_to_cart(PRODUCT_BACKPACK)
    inv.open_cart()
    CartPage(page).checkout()
    return CheckoutInformationPage(page)


def test_first_name_required(authenticated_page):
    step_one = _open_checkout_step_one_with_one_item(authenticated_page)
    step_one.by_test_id("lastName").fill("Doe")
    step_one.by_test_id("postalCode").fill("12345")
    step_one.attempt_continue_expecting_inline_error()
    step_one.assert_inline_error(MSG_FIRST_NAME_REQUIRED)


def test_last_name_required(authenticated_page):
    step_one = _open_checkout_step_one_with_one_item(authenticated_page)
    step_one.by_test_id("firstName").fill("Jane")
    step_one.by_test_id("postalCode").fill("12345")
    step_one.attempt_continue_expecting_inline_error()
    step_one.assert_inline_error(MSG_LAST_NAME_REQUIRED)


def test_postal_code_required(authenticated_page):
    step_one = _open_checkout_step_one_with_one_item(authenticated_page)
    step_one.by_test_id("firstName").fill("Jane")
    step_one.by_test_id("lastName").fill("Doe")
    step_one.attempt_continue_expecting_inline_error()
    step_one.assert_inline_error(MSG_POSTAL_REQUIRED)
