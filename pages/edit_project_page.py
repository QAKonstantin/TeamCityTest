import allure
from pages.base_page import BasePage
from enums.hosts import EDIT_PROJECT, EDIT_PROJECT_ROOT


class MenuListActionsFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.delete_project_selector = "a[title='Delete project']"
        self.quick_links = QuickLinksFragment(page)

    def click_on_delete_project(self):
        with allure.step("Нажать на кнопку Delete project"):
            self.quick_links.expand_list_actions()
            self.actions.click_button(self.delete_project_selector)


class QuickLinksFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.actions_selector = "div[data-hint-container-id='project-admin-actions']"
        self.go_to_project_page_selector = "div#homeLink"

    def go_to_project_main_page(self):
        with allure.step("Переход на страницу проекта"):
            self.actions.click_button(self.go_to_project_page_selector)

    def expand_list_actions(self):
        with allure.step("Открыть меню действий с проектом"):
            self.actions.click_button(self.actions_selector)


class ProjectEditPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = EDIT_PROJECT
        self.menu_list_actions = MenuListActionsFragment(page)

    def go_to_project_edit_page(self, project_id):
        with allure.step("Переход на страницу редактирования проекта"):
            self.actions.navigate(self.page_url.format(project_id=project_id))
            self.actions.wait_for_page_load()

    def delete_project(self, project_id):
        self.go_to_project_edit_page(project_id)
        self.menu_list_actions.click_on_delete_project()
        self.page_url = EDIT_PROJECT_ROOT
        self.actions.wait_for_url_changed(self.page_url)
