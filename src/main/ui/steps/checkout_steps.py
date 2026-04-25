import allure
from playwright.sync_api import Page
from main.ui.pages.checkout_page import CheckoutPage


class CheckoutSteps:
    def __init__(self, page: Page):
        self.page = page
        self.checkout = CheckoutPage(page)

    @allure.step("Заполнить данные клиента и продолжить оформление: {first_name} {last_name}")
    def start_checkout(self, first_name: str, last_name: str, postal_code: str):
        self.checkout.start_checkout(first_name, last_name, postal_code)
        return self

    @allure.step("Завершить оформление заказа")
    def finish_checkout(self):
        self.checkout.finish_checkout()
        return self

    @allure.step("Получить текст сообщения об ошибке")
    def get_error_text(self) -> str:
        return self.checkout.get_error_text()

    @allure.step("Получить текст подтверждения заказа")
    def get_success_text(self) -> str:
        return self.checkout.get_success_text()

    @allure.step("Получить итоговую сумму после перехода к подтверждению")
    def get_item_total(self) -> float:
        return self.checkout.get_item_total()

    @allure.step("Открываем корзину")
    def get_item_total_after_continue(self) -> float:
        return self.checkout.get_item_total_after_continue()
