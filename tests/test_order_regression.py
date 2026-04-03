"""
Regression coverage for the Sauce Demo order placement flow (browse → cart → checkout → complete).

Selectors use stable data-test attributes from https://www.saucedemo.com/
"""

import re

import pytest

pytestmark = pytest.mark.regression


def _add_backpack(page):
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()


def _add_bike_light(page):
    page.locator('[data-test="add-to-cart-sauce-labs-bike-light"]').click()


def _open_cart(page):
    page.locator('[data-test="shopping-cart-link"]').click()
    page.wait_for_url("**/cart.html")


def _start_checkout(page):
    page.locator('[data-test="checkout"]').click()
    page.wait_for_url("**/checkout-step-one.html")


def _fill_shipping(page, first="Jane", last="Doe", postal="90210"):
    page.locator('[data-test="firstName"]').fill(first)
    page.locator('[data-test="lastName"]').fill(last)
    page.locator('[data-test="postalCode"]').fill(postal)


def _continue_to_overview(page):
    page.locator('[data-test="continue"]').click()
    page.wait_for_url("**/checkout-step-two.html")


def _finish_order(page):
    page.locator('[data-test="finish"]').click()
    page.wait_for_url("**/checkout-complete.html")


@pytest.mark.parametrize(
    "username,password,expected_substring",
    [
        ("wrong_user", "secret_sauce", "Username and password do not match"),
        ("standard_user", "wrong_password", "Username and password do not match"),
    ],
)
def test_login_rejects_invalid_credentials(page_context, base_url, username, password, expected_substring):
    """Users cannot reach checkout without a valid session."""
    page = page_context
    page.goto("/")
    page.locator('[data-test="username"]').fill(username)
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()
    error = page.locator('[data-test="error"]')
    error.wait_for(state="visible")
    assert expected_substring in error.inner_text()


def test_login_blocks_locked_out_user(page_context, base_url):
    page = page_context
    page.goto("/")
    page.locator('[data-test="username"]').fill("locked_out_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()
    error = page.locator('[data-test="error"]')
    error.wait_for(state="visible")
    assert "locked out" in error.inner_text().lower()


def test_happy_path_place_order_single_item(logged_in):
    """Standard successful purchase from inventory through confirmation."""
    page = logged_in
    _add_backpack(page)
    assert page.locator('[data-test="shopping-cart-badge"]').inner_text() == "1"
    _open_cart(page)
    assert page.locator('[data-test="inventory-item"]').count() == 1
    _start_checkout(page)
    _fill_shipping(page)
    _continue_to_overview(page)
    assert page.locator('[data-test="inventory-item"]').count() == 1
    assert re.search(r"\$\d+\.\d{2}", page.locator('[data-test="subtotal-label"]').inner_text())
    _finish_order(page)
    header = page.locator('[data-test="complete-header"]')
    assert header.inner_text() == "Thank you for your order!"
    assert page.locator('[data-test="complete-text"]').is_visible()


def test_place_order_multiple_items_cart_totals(logged_in):
    page = logged_in
    _add_backpack(page)
    _add_bike_light(page)
    badge = page.locator('[data-test="shopping-cart-badge"]')
    assert badge.inner_text() == "2"
    _open_cart(page)
    assert page.locator('[data-test="inventory-item"]').count() == 2
    _start_checkout(page)
    _fill_shipping(page, first="Alex", last="Rivera", postal="10001")
    _continue_to_overview(page)
    subtotal = page.locator('[data-test="subtotal-label"]').inner_text()
    tax = page.locator('[data-test="tax-label"]').inner_text()
    total = page.locator('[data-test="total-label"]').inner_text()
    assert re.search(r"Item total: \$\d+\.\d{2}", subtotal)
    assert re.search(r"Tax: \$\d+\.\d{2}", tax)
    assert re.search(r"Total: \$\d+\.\d{2}", total)
    _finish_order(page)
    assert page.locator('[data-test="complete-header"]').inner_text() == "Thank you for your order!"


def test_checkout_step_one_requires_first_name(logged_in):
    page = logged_in
    _add_backpack(page)
    _open_cart(page)
    _start_checkout(page)
    page.locator('[data-test="lastName"]').fill("Doe")
    page.locator('[data-test="postalCode"]').fill("12345")
    page.locator('[data-test="continue"]').click()
    err = page.locator('[data-test="error"]')
    err.wait_for(state="visible")
    assert "First Name is required" in err.inner_text()


def test_checkout_step_one_requires_last_name(logged_in):
    page = logged_in
    _add_backpack(page)
    _open_cart(page)
    _start_checkout(page)
    page.locator('[data-test="firstName"]').fill("Jane")
    page.locator('[data-test="postalCode"]').fill("12345")
    page.locator('[data-test="continue"]').click()
    err = page.locator('[data-test="error"]')
    err.wait_for(state="visible")
    assert "Last Name is required" in err.inner_text()


def test_checkout_step_one_requires_postal_code(logged_in):
    page = logged_in
    _add_backpack(page)
    _open_cart(page)
    _start_checkout(page)
    page.locator('[data-test="firstName"]').fill("Jane")
    page.locator('[data-test="lastName"]').fill("Doe")
    page.locator('[data-test="continue"]').click()
    err = page.locator('[data-test="error"]')
    err.wait_for(state="visible")
    assert "Postal Code is required" in err.inner_text()


def test_cancel_from_checkout_step_one_returns_to_cart(logged_in):
    page = logged_in
    _add_backpack(page)
    _open_cart(page)
    _start_checkout(page)
    page.locator('[data-test="cancel"]').click()
    page.wait_for_url("**/cart.html")
    assert page.locator('[data-test="inventory-item"]').count() == 1


def test_remove_item_from_cart_updates_badge_and_list(logged_in):
    page = logged_in
    _add_backpack(page)
    _add_bike_light(page)
    assert page.locator('[data-test="shopping-cart-badge"]').inner_text() == "2"
    _open_cart(page)
    page.locator('[data-test="remove-sauce-labs-backpack"]').click()
    assert page.locator('[data-test="shopping-cart-badge"]').inner_text() == "1"
    assert page.locator('[data-test="inventory-item"]').count() == 1


def test_continue_shopping_from_cart_returns_to_inventory(logged_in):
    page = logged_in
    _add_backpack(page)
    _open_cart(page)
    page.locator('[data-test="continue-shopping"]').click()
    page.wait_for_url("**/inventory.html")
    assert page.locator('[data-test="inventory-container"]').is_visible()


def test_empty_cart_checkout_current_site_behavior(logged_in):
    """
    Documents current behavior: checkout remains available with an empty cart,
    and the flow can complete with zero line items (useful regression signal if this changes).
    """
    page = logged_in
    _open_cart(page)
    assert page.locator('[data-test="inventory-item"]').count() == 0
    assert page.locator('[data-test="checkout"]').is_enabled()
    _start_checkout(page)
    _fill_shipping(page)
    _continue_to_overview(page)
    assert page.locator('[data-test="inventory-item"]').count() == 0
    _finish_order(page)
    assert page.locator('[data-test="complete-header"]').inner_text() == "Thank you for your order!"
