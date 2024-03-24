import allure

from pages.base_page import BasePage
from pages.agent_page import AgentPage


class FirstPageContent(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.nested_page_content = "#nestedPageContent"
        self.proceed_button_selector = "#proceedButton"
        self.restore_button_selector = "#restoreButton"

    def proceed_first_page(self):
        with allure.step("Нажать кнопку proceed на первой странице"):
            self.actions.click_button(self.proceed_button_selector)

    def restore(self):
        with allure.step(f"Нажать кнопку restore"):
            self.actions.click_button(self.restore_button_selector)


class LoadingPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.loading_icon_selector = ".icon-refresh"

    def wait_loading(self, timeout=999999):
        with allure.step("Ожидание начала загрузки"):
            self.actions.wait_for_selector(self.loading_icon_selector)
        with allure.step("Ожидание завершения загрузки"):
            self.actions.wait_for_disappear_selector(self.loading_icon_selector, timeout)


class DatabaseConnectionSetup(FirstPageContent):

    def proceed_database(self):
        with allure.step("Нажать кнопку proceed на странице инициализации БД"):
            self.actions.click_button(self.proceed_button_selector)


class AgreementPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = "/showAgreement.html"
        self.accept_checkbox_agreement_selector = "input#accept"
        self.anonymous_statistics_checkbox_selector = "input#sendUsageStatistics"
        self.continue_button_selector = "input[name='Continue']"

    def accept_agreement(self):
        with allure.step("Активировать чекбокс принятия Соглашения"):
            self.actions.activate_inactive_checkbox(self.accept_checkbox_agreement_selector)

    def continue_agreement(self):
        with allure.step("Нажать кнопку Продолжить на странице с Соглашением"):
            self.actions.click_button(self.continue_button_selector)


class SetupUserPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = "/setupAdmin.html"
        self.username_selector = "#input_teamcityUsername"
        self.password_selector = "#password1"
        self.confirm_password_selector = '#retypedPassword'
        self.create_account_button_selector = ".loginButton"

    def fill_user_details(self, username, password):
        with allure.step("Заполнить данные пользователя"):
            self.actions.input_text(self.username_selector, username)
            self.actions.input_text(self.password_selector, password)
            self.actions.input_text(self.confirm_password_selector, password)

    def create_user(self):
        with allure.step("Создать пользователя с ролью Администратор"):
            self.actions.click_button(self.create_account_button_selector)


class SetupPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_page_content = FirstPageContent(page)
        self.loading = LoadingPage(page)
        self.database_setup = DatabaseConnectionSetup(page)
        self.agreement = AgreementPage(page)
        self.setup_user = SetupUserPage(page)
        self.agent_page = AgentPage(page)

    def setup(self, username="admin", password="admin"):
        self.actions.navigate(self.page_url)
        self.actions.wait_for_page_load()
        self.first_page_content.proceed_first_page()
        self.loading.wait_loading()
        self.database_setup.proceed_database()
        self.loading.wait_loading()
        self.agreement.accept_agreement()
        self.agreement.continue_agreement()
        self.actions.wait_for_page_load()
        self.actions.check_url(self.setup_user.page_url)
        self.setup_user.fill_user_details(username, password)
        self.setup_user.create_user()
        self.actions.wait_for_page_load()
        self.page_url = "/favorite/projects"
        self.actions.check_url(self.page_url, timeout=30000)
        self.agent_page.authorize_agent()
