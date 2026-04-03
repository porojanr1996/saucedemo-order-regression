"""Login and session gates — you cannot place an order without a valid account."""

from __future__ import annotations

import pytest

from config.test_data import LOCKED_OUT_USER, MSG_LOGIN_MISMATCH, STANDARD_USER, User
from pages.login_page import LoginPage

pytestmark = [pytest.mark.regression, pytest.mark.auth]


@pytest.mark.parametrize(
    "credentials",
    [
        User("wrong_user", STANDARD_USER.password),
        User(STANDARD_USER.username, "wrong_password"),
    ],
    ids=["AUTH-NEG-01-bad-username", "AUTH-NEG-02-bad-password"],
)
def test_invalid_credentials_show_generic_error(page, credentials: User):
    login = LoginPage(page)
    login.open()
    login.login(credentials)
    login.assert_error_contains(MSG_LOGIN_MISMATCH)


def test_locked_out_user_cannot_start_session(page):
    login = LoginPage(page)
    login.open()
    login.login(LOCKED_OUT_USER)
    banner = login.by_test_id("error")
    text = banner.inner_text().lower()
    assert "locked out" in text, f"Expected locked-out copy, got: {text!r}"
