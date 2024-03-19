import allure
from pages.base_page import BasePage


class VCSFormContainerFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.create_button_selector = "input[value='Create']"
        self.skip_button_selector = "a.cancel:has-text('Skip')"

    def click_skip_vcs_root(self):
        with allure.step("Пропустить настройку VCS"):
            self.actions.click_button(self.skip_button_selector)

    def click_create_vcs_root(self):
        with allure.step("Создать настройку VCS"):
            self.actions.click_button(self.create_button_selector)
