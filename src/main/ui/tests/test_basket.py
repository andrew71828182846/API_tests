import pytest
from main.ui.pages.basket_page import BasketPage
from main.ui.pages.catalog_page import CatalogPage
from main.ui.pages.checkout_page import CheckoutPage


def test_add_item_and_check_in_cart(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Backpack")
    basket.open_cart()
    assert "Sauce Labs Backpack" in basket.get_item_names()

def test_add_item_and_check_in_cart_fleece_jacket(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")


    basket.open_cart()
    items = basket.get_item_names()
    assert "Sauce Labs Fleece Jacket" in items
    assert "Sauce Labs Bolt T-Shirt" in items

def test_remove_item_from_cart(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

    basket.open_cart()
    items = basket.get_item_names()
    assert "Sauce Labs Fleece Jacket" in items
    assert "Sauce Labs Bolt T-Shirt" in items

    basket.remove_item("Sauce Labs Fleece Jacket")
    basket.remove_item("Sauce Labs Bolt T-Shirt")

    items = basket.get_item_names()
    assert "Sauce Labs Fleece Jacket" not in items
    assert "Sauce Labs Bolt T-Shirt" not in items


def test_checkout_multiple_items(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)
    checkout = CheckoutPage(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

    basket.open_cart()
    items = basket.get_item_names()
    assert "Sauce Labs Fleece Jacket" in items
    assert "Sauce Labs Bolt T-Shirt" in items

    basket_total = basket.get_items_total_price()
    basket.checkout()

    checkout.start_checkout(first_name="Test", last_name="User", postal_code="12345")
    assert checkout.get_item_total_after_continue() == pytest.approx(basket_total, 0.01)

    checkout.finish_checkout()
    assert checkout.get_success_text() == "Thank you for your order!"


def test_checkout_without_items(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)
    checkout = CheckoutPage(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")


    basket.open_cart()
    assert "Sauce Labs Fleece Jacket" in basket.get_item_names()
    basket.checkout()
    checkout.start_checkout(first_name="Test", last_name="User", postal_code="")
    assert checkout.get_error_text() == "Error: Postal Code is required"