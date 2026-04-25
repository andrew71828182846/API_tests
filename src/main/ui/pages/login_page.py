from playwright.sync_api import Page
from main.ui.pages.base_page import BasePage
from main.ui.utils.constants import Urls


class LoginPage(BasePage):
    URL = Urls.BASE

    def __init__(self, page: Page):
        super().__init__(page)
        self.open_login_page = None
        self.page = page
        self.error_message = page.locator("h3[data-test='error']")

    def open(self):
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_test(self) -> str:
        return self.error_message.inner_text()
