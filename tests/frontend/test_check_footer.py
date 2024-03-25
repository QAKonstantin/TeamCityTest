import allure
import pytest

from enums.roles import Roles
from pages.auth_page import AuthLoginForm


@pytest.mark.parametrize("role", [
    Roles.SYSTEM_ADMIN.value,
    Roles.PROJECT_ADMIN.value,
    Roles.AGENT_MANAGER.value,
], ids=["By system admin",
        "By project admin",
        "By agent manager"])
@allure.severity(allure.severity_level.NORMAL)
@allure.parent_suite("UI тесты")
@allure.suite("Проверка футера")
@allure.sub_suite("Футер")
@allure.title("Авторизация под разными ролями и проверка ссылок в футере")
@pytest.mark.ui
@pytest.mark.footer
def test_e2e_check_footer_by_roles(browser, user_create, role):
    with allure.step(f'Создание пользователя с ролью {role}'):
        role_user = user_create(role)

    with allure.step(f"Авторизация под ролью {role}"):
        main_page = AuthLoginForm(browser)
        main_page.login(*role_user.creds)

    with allure.step(f"Проверка ссылок в футере"):
        main_page.footer.go_to_about_teamcity(close_tab=True)
        main_page.footer.go_to_license_agreement(close_tab=True)

    with allure.step(f"Проверка версии системы"):
        main_page.footer.check_version()

    with allure.step(f"Проверка копирайта"):
        main_page.footer.check_copyright()
