import pytest
from main.ui.pages.basket_page import BasketPage
from main.ui.pages.catalog_page import CatalogPage
from main.ui.pages.checkout_page import CheckoutPage
from main.ui.steps.basket_steps import BasketSteps
from main.ui.steps.catalog_steps import CatalogSteps
from main.ui.steps.checkout_steps import CheckoutSteps


def test_add_item_and_check_in_cart(page):
    basket = BasketSteps(page)
    catalog = CatalogSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Backpack")
    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Backpack")

def test_add_item_and_check_in_cart_fleece_jacket(page):
    basket = BasketSteps(page)
    catalog = CatalogSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")


    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")

def test_remove_item_from_cart(page):
    basket = BasketSteps(page)
    catalog = CatalogSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")

    basket.remove_item("Sauce Labs Fleece Jacket")
    basket.remove_item("Sauce Labs Bolt T-Shirt")
    basket.expect_item_not_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_not_in_cart("Sauce Labs Bolt T-Shirt")


def test_checkout_multiple_items(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")

    basket_total = basket.get_items_total_price()
    basket.checkout()

    checkout.start_checkout(first_name="Test", last_name="User", postal_code="12345")
    checkout_total = checkout.get_item_total_after_continue()
    assert checkout_total == basket_total, "Сумма товаров в Checkout не совпадает с корзиной"


def test_checkout_without_items(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.checkout()
    checkout.start_checkout(first_name="Test", last_name="User", postal_code="")
    error_text = checkout.get_error_text()
    assert error_text != "", "Ожидалась ошибка при оформлении пустой корзины"