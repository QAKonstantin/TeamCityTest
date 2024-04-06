import time

import allure

from enums.hosts import BUILD_CONF_PAGE
from enums.build_model import BuildStatus
from pages.base_page import BasePage


class RunBuildPage(BasePage):
    def __init__(self, page, build_conf_id):
        super().__init__(page)
        self.page_url = BUILD_CONF_PAGE.format(build_conf_id=build_conf_id)
        self.build_type_header = BuildTypePageHeaderFragment(page)
        self.overview = OverviewFragment(page)

    def go_to_build_conf_page(self):
        with allure.step("Переход на страницу подробной информации о билд конфигурации"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def run_build(self):
        with allure.step("Запуск билда"):
            self.go_to_build_conf_page()
            self.build_type_header.click_run_build()

    def check_last_status_running_build(self, expected_status: str = BuildStatus.BUILD_SUCCESS.value):
        last_build_status = BuildStatus.BUILD_UNKNOWN.value
        timeout = 0
        while last_build_status != expected_status:
            if timeout != 60:
                time.sleep(1)
                last_build_status = self.overview.get_all_running_builds().first.inner_text().upper()
                timeout += 1
            else:
                raise TimeoutError(
                    f"Текущий статус: {last_build_status} не соответствует ожидаемому: {expected_status}")


class BuildTypePageHeaderFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.edit_configuration_selector = "div[data-hint-container-id='edit-entity'] >> .ring-button-content"
        self.run_build_selector = "button[data-test='run-build']"

    def click_edit_configuration(self):
        with allure.step("Нажать на кнопку перехода к настройкам билд конфигурации"):
            self.actions.click_button(self.edit_configuration_selector)

    def click_run_build(self):
        with allure.step("Нажать на кнопку запуска билда"):
            self.actions.click_button(self.run_build_selector)


class OverviewFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.list_builds = "div.Builds__builds--nK >> .Grid__rowGroupsWrapper--_0"
        self.running_builds_statuses = "div.Build__status--bG .MiddleEllipsis__searchable--uZ"

    def get_all_running_builds(self):
        return self.actions.get_element(self.running_builds_statuses)
