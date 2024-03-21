import allure

from pages.auth_page import AuthLoginBySuperAdmin
from pages.setup_page import SetupPage


@allure.title("Сетап")
@allure.description(
    "Сетап для проверки правильности настройки тестовой среды:"
    "принятие пользовательского соглашения,"
    "инициализация БД,"
    "создание пользователя с ролью Администратор")
def test_setup(browser):
    with allure.step("Сетап"):
        setup_page = SetupPage(browser)
        setup_page.setup()
