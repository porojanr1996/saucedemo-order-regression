"""Test users, product keys, and UI strings for assertions."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class User:
    username: str
    password: str


@dataclass(frozen=True, slots=True)
class CustomerInfo:
    first_name: str
    last_name: str
    postal_code: str


STANDARD_USER = User("standard_user", "secret_sauce")
LOCKED_OUT_USER = User("locked_out_user", "secret_sauce")

DEFAULT_CUSTOMER = CustomerInfo("Jane", "Doe", "90210")
CUSTOMER_ALT = CustomerInfo("Alex", "Rivera", "10001")

# data-test suffixes after add-to-cart- / remove-
PRODUCT_BACKPACK = "sauce-labs-backpack"
PRODUCT_BIKE_LIGHT = "sauce-labs-bike-light"

# Checkout copy (site is en-US)
MSG_LOGIN_MISMATCH = "Username and password do not match"
MSG_FIRST_NAME_REQUIRED = "Error: First Name is required"
MSG_LAST_NAME_REQUIRED = "Error: Last Name is required"
MSG_POSTAL_REQUIRED = "Error: Postal Code is required"
MSG_ORDER_THANK_YOU = "Thank you for your order!"
