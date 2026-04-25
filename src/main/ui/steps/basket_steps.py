import allure
from main.ui.pages.basket_page import BasketPage
from playwright.sync_api import Page, expect


class BasketSteps:
    def __init__(self, page: Page):
        self.page = page
        self.basket = BasketPage(page)

    @allure.step("Открываем корзину")
    def open_cart(self):
        self.basket.open_cart()
        return self

    @allure.step("Переход к оформлению заказа")
    def checkout(self):
        self.basket.checkout()
        return self

    @allure.step("Удалить {product_name} из корзины")
    def remove_item(self, product_name: str):
        self.basket.remove_item(product_name)
        return self

    @allure.step("Ожидание отображения {product_name} в корзине")
    def expect_item_in_cart(self, product_name: str):
        self.basket.expect_item_in_cart(product_name)
        return self

    @allure.step("Проверить отсутствие {product_name} в корзине")
    def expect_item_not_in_cart(self, product_name: str):
        self.basket.expect_item_not_in_cart(product_name)
        return self

    @allure.step("Получить список названий товаров в корзине")
    def get_item_names(self) -> list[str]:
        return self.basket.get_item_names()

    @allure.step("Получить цены всех товаров в корзине")
    def get_item_prices(self) -> list[float]:
        return self.basket.get_item_prices()

    @allure.step("Расчет итоговой суммы заказа")
    def get_items_total_price(self) -> float:
        return self.basket.get_items_total_price()
