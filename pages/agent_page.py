import time

import allure

from pages.base_page import BasePage


class AgentSideBar(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.unauthorized_agents_selector = "a[data-test-sidebar-link='base']:has-text('UNAUTHORIZED AGENTS')"

    def expand_unauthorized_agents(self):
        with allure.step("Открыть список неавторизованных агентов"):
            self.actions.click_button(self.unauthorized_agents_selector)


class UnauthorizedAgentsContent(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.show_popup_authorize_button_selector = "button[data-test-authorize-agent='true']"

    def click_authorize_button(self):
        with allure.step("Открыть попап для авторизации агента"):
            self.actions.click_button(self.show_popup_authorize_button_selector)


class PopupAuthorizeAgent(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.authorize_agent_button_selector = "button.CommonForm__button--Nb"

    def click_authorize_button_in_popup(self):
        with allure.step("Нажать на кнопку Authorize"):
            self.actions.click_button(self.authorize_agent_button_selector)


class AgentPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = "/agents/overview"
        self.agent_side_bar = AgentSideBar(page)
        self.unauthorized_agents_content = UnauthorizedAgentsContent(page)
        self.popup_authorize_agent = PopupAuthorizeAgent(page)
        self.test_test = "span[data-hint-container-id='header-agents-active']"

    def go_to_agent_page(self):
        with allure.step("Переход на страницу с агентами"):
            self.actions.navigate(self.page_url)

    def authorize_agent(self):
        with allure.step("Авторизация агента"):
            self.go_to_agent_page()
            self.actions.wait_for_page_load()
            self.agent_side_bar.expand_unauthorized_agents()
            self.unauthorized_agents_content.click_authorize_button()
            self.popup_authorize_agent.click_authorize_button_in_popup()
            self.actions.wait_for_disappear_selector(self.agent_side_bar.unauthorized_agents_selector)
            self.go_to_agent_page()
            self.actions.wait_for_page_load()
