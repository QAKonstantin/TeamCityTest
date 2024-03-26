import allure
from pages.base_page import BasePage
from pages.create_project_page import MenuListCreateFragment
from pages.create_vcs_root_page import VCSFormContainerFragment
from enums.hosts import CREATE_BUILD_CONF, EDIT_VCS_ROOT, EDIT_BUILD_CONF_VCS_ROOT


class CreateFormContainerFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.build_conf_name_selector = "input#buildTypeName"
        self.build_conf_id_selector = "input#buildTypeExternalId"
        self.build_conf_description_selector = "input#description"
        self.create_build_conf_button = "input[name=createBuildType]"

    def input_build_conf_details(self, name, build_conf_id, description):
        with allure.step("Ввод данных для создания билд конфигурации"):
            self.actions.wait_for_selector(self.build_conf_name_selector)
            self.actions.input_text(self.build_conf_name_selector, name)
            self.actions.input_text(self.build_conf_id_selector, build_conf_id)
            self.actions.input_text(self.build_conf_description_selector, description)

    def click_create_button(self):
        with allure.step("Нажатие кнопки создания билд конфигурации"):
            self.actions.click_button(self.create_build_conf_button)


class BuildConfCreationPage(BasePage):
    def __init__(self, page, project_id):
        super().__init__(page)
        self.page_url = CREATE_BUILD_CONF.format(project_id=project_id)
        self.menu_list_create = MenuListCreateFragment(page)
        self.create_form_container = CreateFormContainerFragment(page)
        self.settings_vcs_root = VCSFormContainerFragment(page)

    def go_to_creation_build_conf_page(self):
        with allure.step("Переход на страницу создания билд конфигурации"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def create_build_conf(self, project_id, name, build_conf_id, description):
        self.go_to_creation_build_conf_page()
        self.menu_list_create.click_create_manually()
        self.create_form_container.input_build_conf_details(name, build_conf_id, description)
        self.create_form_container.click_create_button()
        self.page_url = EDIT_VCS_ROOT.format(project_id=project_id, build_conf_id=build_conf_id)
        self.actions.wait_for_url_changed(self.page_url)
        self.settings_vcs_root.click_skip_vcs_root()
        self.page_url = EDIT_BUILD_CONF_VCS_ROOT.format(project_id=project_id, build_conf_id=build_conf_id)
        self.actions.wait_for_url_changed(self.page_url)
