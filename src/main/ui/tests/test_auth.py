from playwright.sync_api import expect
from main.ui.pages.catalog_page import CatalogPage
from main.ui.pages.login_page import LoginPage


def test_auth(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    assert page.url == "https://www.saucedemo.com/inventory.html", "Ожидаем редирект на страницу каталога"


def test_auth_invalid(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("locked_out_user", "secret_sauce")

    assert page.url == LoginPage.URL, "Ожидаем остаться на странице логина"

    error = login_page.get_error_test()
    assert "locked out" in error, "Ожидаем сообщение о заблокированном пользователе"


def test_logout(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    catalog_page = CatalogPage(page)
    assert  catalog_page.get_product_count() > 0

    catalog_page.logout()

    expect(page).to_have_url(LoginPage.URL)

def test_logout_visual_user(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("visual_user", "secret_sauce")

    catalog_page = CatalogPage(page)
    assert catalog_page.get_product_count() > 0

    catalog_page.logout()

    expect(page).to_have_url(LoginPage.URL)