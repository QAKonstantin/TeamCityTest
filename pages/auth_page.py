import os

import allure
from pages.base_page import BasePage
from dotenv import load_dotenv

load_dotenv()


class AuthLoginForm(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.username_input = "#username"
        self.password_input = "#password"
        self.login_btn = ".loginButton"
        self.page_url = "/login.html"

    def input_credentials(self, username, password):
        with allure.step("Ввод данных для авторизации"):
            self.actions.wait_for_selector(self.username_input)
            self.actions.input_text(self.username_input, username)
            self.actions.input_text(self.password_input, password)

    def click_login(self):
        with allure.step("Авторизация пользователя"):
            self.actions.click_button(self.login_btn)

    def go_to_login_page(self):
        with allure.step("Переход на страницу авторизации"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def login(self, username, password):
        self.go_to_login_page()
        self.input_credentials(username, password)
        self.click_login()
        self.page_url = '/favorite/projects'
        self.actions.wait_for_url_changed(self.page_url)


class AuthLoginBySuperAdmin(AuthLoginForm):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.page_url = "/login.html?super=1"

    def input_token(self, token):
        with allure.step("Ввод токена для авторизации под Супер Администратором"):
            self.actions.wait_for_selector(self.password_input)
            self.actions.input_text(self.password_input, token)

    def login_by_super_admin(self, token=os.getenv('SUPER_USER_TOKEN')):
        self.go_to_login_page()
        self.input_token(token)
        self.click_login()
        # self.actions.contain_uri('/favorite/projects')
