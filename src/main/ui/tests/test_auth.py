from main.ui.pages.catalog_page import CatalogPage
from main.ui.pages.login_page import LoginPage
from main.ui.steps.catalog_steps import CatalogSteps
from main.ui.steps.login_steps import LoginSteps


def test_auth(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")

    catalog_page = CatalogPage(page)
    assert catalog_page.get_products_count() > 0, "Ожидаем товары на странице каталога"


def test_auth_invalid(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("locked_out_user", "secret_sauce")

    error = steps.login_page.get_error_test()
    assert "locked out" in error, "Ожидаем сообщение о заблокированном пользователе"


def test_logout(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    login.open_login_page().login("standard_user", "secret_sauce")

    assert  catalog.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

    catalog.logout()
    assert page.url == LoginPage.URL, "Ожидаем возврат на страницу логина"

def test_logout_visual_user(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)

    login.open_login_page().login("visual_user", "secret_sauce")
    assert  catalog.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

    catalog.logout()
    assert page.url == LoginPage.URL, "Ожидаем возврат на страницу логина"