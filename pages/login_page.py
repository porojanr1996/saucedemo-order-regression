from __future__ import annotations

from playwright.sync_api import Page, expect

from config.settings import EXPECT_TIMEOUT_MS
from config.test_data import STANDARD_USER, User
from pages.base_page import BasePage


class LoginPage(BasePage):
    path_glob = "**/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> None:
        self.page.goto("/")

    def login(self, user: User) -> None:
        self.by_test_id("username").fill(user.username)
        self.by_test_id("password").fill(user.password)
        self.by_test_id("login-button").click()

    def login_as_standard_user(self) -> None:
        self.login(STANDARD_USER)

    def assert_error_contains(self, substring: str) -> None:
        banner = self.by_test_id("error")
        expect(banner).to_be_visible(timeout=EXPECT_TIMEOUT_MS)
        expect(banner).to_contain_text(substring, timeout=EXPECT_TIMEOUT_MS)
