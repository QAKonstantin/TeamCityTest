import allure

from enums.hosts import NEW_BUILD_STEP_COMMAND_LINE, EDIT_BUILD_RUNNERS, GENERAL_SETTING_EDIT_BUILD, \
    BUILD_CONF_AFTER_REMOVED
from pages.base_page import BasePage


class AdminSideBarBuildConf(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.general_settings_selector = "ul.tabs:has-text('General Settings')"
        self.version_control_settings_selector = "ul.tabs:has-text('Version Control Settings')"
        self.build_steps_selector = "ul.tabs:has-text('Build Steps')"
        self.suggestions_selector = "ul.tabs:has-text('Suggestions')"

    def go_to_general_settings(self):
        with allure.step("Переход к общим настройкам билд конфигурации"):
            self.actions.click_button(self.general_settings_selector)

    def go_to_version_control_settings(self):
        with allure.step("Переход к настройкам VCS"):
            self.actions.click_button(self.version_control_settings_selector)

    def go_to_build_steps(self):
        with allure.step("Переход к настройкам шагов билд конфигурации"):
            self.actions.click_button(self.build_steps_selector)

    def go_to_suggestions(self):
        with allure.step("Переход к рекомендациям"):
            self.actions.click_button(self.suggestions_selector)


class BuildStepsFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_build_step_selector = "span.addNew:has-text('Add build step')"

    def go_to_build_steps(self):
        with allure.step("Переход к созданию шагов билда"):
            self.actions.click_button(self.add_build_step_selector)


class ListRunnerParamsBuild(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.command_line_selector = "td.SelectBuildRunners__title--Vf:has-text('Command Line')"

    def go_to_command_line_build_step(self):
        with allure.step("Переход к созданию шага билда на основе командной строки"):
            self.actions.click_button(self.command_line_selector)


class CreateNewBuildStepCommandLine(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.build_step_name_selector = "input#buildStepName"
        self.build_step_id_selector = "input#newRunnerId"
        self.build_custom_script_selector = ".CodeMirror >> textarea"
        self.create_build_step_button = "#saveButtons .submitButton"
        self.cancel_build_step_button = "#saveButtons .cancel"

    def input_build_step_details(self, step_id, custom_script):
        with allure.step("Ввод данных для создания проекта"):
            self.actions.wait_for_selector(self.build_step_id_selector)
            self.actions.input_text(self.build_step_id_selector, step_id)
            self.actions.input_text(self.build_custom_script_selector, custom_script)

    def click_create_button(self):
        with allure.step("Нажатие кнопки создания шага билда"):
            self.actions.click_button(self.create_build_step_button)


class EditBuildPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.admin_sidebar_build_conf = AdminSideBarBuildConf(page)
        self.list_runner_params = ListRunnerParamsBuild(page)
        self.menu_list_actions = MenuListActionsFragment(page)
        self.create_build_step_by_command_line = CreateNewBuildStepCommandLine(page)

    def go_to_general_settings_page(self, build_conf_id):
        with allure.step("Переход на страницу редактирования билд конфигурации"):
            self.page_url = GENERAL_SETTING_EDIT_BUILD
            self.actions.navigate(self.page_url.format(build_conf_id=build_conf_id))
            self.actions.wait_for_page_load()

    def go_to_creation_build_step_page(self, build_conf_id):
        with allure.step("Переход на страницу создания шага билда"):
            self.page_url = NEW_BUILD_STEP_COMMAND_LINE
            self.actions.navigate(self.page_url.format(build_conf_id=build_conf_id))
            self.actions.wait_for_page_load()

    def create_build_step(self, step_name, custom_script, build_conf_id):
        self.go_to_creation_build_step_page(build_conf_id)
        self.list_runner_params.go_to_command_line_build_step()
        self.create_build_step_by_command_line.input_build_step_details(step_name, custom_script)
        self.create_build_step_by_command_line.click_create_button()
        self.page_url = EDIT_BUILD_RUNNERS.format(build_conf_id=build_conf_id)
        self.actions.wait_for_url_changed(self.page_url)

    def delete_build_conf(self, project_id, build_conf):
        self.go_to_general_settings_page(build_conf)

        self.page.on("dialog", lambda dialog: dialog.accept())
        self.menu_list_actions.click_on_delete_build_conf()

        self.page_url = BUILD_CONF_AFTER_REMOVED.format(project_id=project_id)
        self.actions.wait_for_url_changed(self.page_url)


class MenuListActionsFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.delete_build_conf_selector = ".menuItem a:has-text('Delete...')"
        self.popup = "div.quickLinksMenuPopup"
        self.quick_links = QuickLinksFragment(page)

    def click_on_delete_build_conf(self):
        with allure.step("Нажать на кнопку удаления билд конфигурации"):
            self.quick_links.expand_list_actions()
            self.actions.click_button(self.delete_build_conf_selector)


class QuickLinksFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.actions_selector = "div[data-hint-container-id='build-configuration-admin-actions']"
        self.go_to_build_conf_page_selector = "div#homeLink"
        self.run_build_conf_selector = "div[data-hint-container-id='build-configuration-admin-run-button']"

    def go_to_build_conf_main_page(self):
        with allure.step("Переход на страницу подробной информации по билд конфигурации"):
            self.actions.click_button(self.go_to_build_conf_page_selector)

    def expand_list_actions(self):
        with allure.step("Открыть меню действий с билд конфигурацией"):
            self.actions.click_button(self.actions_selector)
