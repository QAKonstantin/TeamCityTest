import allure

from pages.agent_page import AgentPage
from pages.setup_page import SetupPage


@allure.title("Сетап")
@allure.description(
    "Сетап для проверки правильности настройки тестовой среды:"
    "принятие пользовательского соглашения,"
    "инициализация БД,"
    "создание пользователя с ролью Администратор")
def test_setup(browser_for_setup):
    with allure.step("Инициализация БД и создание пользователя с ролью Администратор"):
        setup_page = SetupPage(browser_for_setup)
        setup_page.first_steps_and_create_user()
    with allure.step("Авторизация агента"):
        auth_agent = AgentPage(browser_for_setup)
        auth_agent.authorize_agent()
