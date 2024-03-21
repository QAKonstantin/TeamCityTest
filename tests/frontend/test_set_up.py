import allure

from enums.hosts import BASE_URL
from pages.setup_page import SetupPage


@allure.title("Сетап")
@allure.description(
    "Сетап для проверки правильности настройки тестовой среды:"
    "принятие пользовательского соглашения,"
    "инициализация БД,"
    "создание пользователя с ролью Администратор")
def test_setup(browser):
    with allure.step("Сетап"):
        print(BASE_URL)
        setup_page = SetupPage(browser)
        setup_page.setup()
