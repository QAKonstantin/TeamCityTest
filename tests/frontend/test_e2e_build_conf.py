import allure
import pytest

from data.build_conf_data import BuildConfResponseModel, BuildConfData
from data.project_data import ProjectResponseModel
from pages.create_build_conf_page import BuildConfCreationPage
from pages.edit_build_conf_page import EditBuildPage


class TestBuildConfE2E:
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.parent_suite("UI тесты")
    @allure.suite("Управление билд конфигурациями")
    @allure.sub_suite("Cоздание билд конфигурации")
    @allure.title("Cоздание билд конфигурации и шага в билде Супер Администратором")
    @allure.description(
        "Авторизация Супер Администратором, создание проекта, билд конфигурации и шага в командной строке")
    @pytest.mark.build_conf
    @pytest.mark.ui
    def test_e2e_create_build_conf(self, project_data, build_conf_data, random_description, browser, super_admin,
                                   login):
        with allure.step('Подготовка данных для создания проекта и билд конфигурации'):
            project_data_1 = project_data()
            build_conf_data_1 = build_conf_data(project_data_1.id)
            custom_script = build_conf_data_1.steps['step'][0]['properties']['property'][0]['value']

        with allure.step('Отправка запроса на создание проекта'):
            created_project_response = super_admin.api_manager.project_api.create_project(
                project_data_1.model_dump()).text
            created_project_model = ProjectResponseModel.model_validate_json(created_project_response)
            assert created_project_model.id == project_data_1.id, \
                f"Ожидался project_id= {project_data_1.id}, но был получен {created_project_model.id}"

        with allure.step("Создание билд конфигурации"):
            build_conf_creation_browser = BuildConfCreationPage(browser, project_data_1.id)
            build_conf_creation_browser.create_build_conf(project_data_1.id, build_conf_data_1.name,
                                                          build_conf_data_1.id,
                                                          random_description)

        with allure.step("Добавление шага"):
            build_step_creation_browser = EditBuildPage(browser)
            build_step_creation_browser.create_build_step(build_conf_data_1.name, custom_script,
                                                          build_conf_data_1.id)

        with allure.step(
                'Отправка запроса на получение информации по созданной билд конфигурации и наличию шага в билде'):
            data_build_conf_response = super_admin.api_manager.build_conf_api.get_build_conf_by_locator(
                build_conf_data_1.id).text
            created_build_conf = BuildConfResponseModel.model_validate_json(data_build_conf_response)
            assert created_build_conf.id == build_conf_data_1.id, \
                f"Не найден созданный build_conf_id={created_build_conf.id} среди существующих билд конфигураций"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.parent_suite("UI тесты")
    @allure.suite("Управление билд конфигурациями")
    @allure.sub_suite("Удаление билд конфигурации")
    @allure.title("Удаление билд конфигурации под Супер Администратором")
    @allure.description("Авторизация Супер Администратором, создание проекта, билда и удаление билда")
    @pytest.mark.build_conf
    @pytest.mark.ui
    def test_e2e_delete_build_conf(self, project_data, browser, super_admin, login):
        with allure.step('Подготовка данных для создания проекта и билд конфигурации'):
            project_data_1 = project_data()
            build_conf_data_1 = BuildConfData.create_build_conf_data(project_data_1.id)

        with allure.step('Отправка запроса на создание проекта'):
            created_project_response = super_admin.api_manager.project_api.create_project(
                project_data_1.model_dump()).text
            created_project_model = ProjectResponseModel.model_validate_json(created_project_response)
            assert created_project_model.id == project_data_1.id, \
                f"Ожидался project_id= {project_data_1.id}, но был получен {created_project_model.id}"

        with allure.step('Отправка запроса на создание билд конфигурации'):
            create_build_conf_response = super_admin.api_manager.build_conf_api.create_build_conf(
                build_conf_data_1.model_dump()).text
            build_conf_model = BuildConfResponseModel.model_validate_json(create_build_conf_response)
            with pytest.assume:
                assert build_conf_model.id == build_conf_data_1.id, \
                    f"Ожидался build_conf_id={build_conf_data_1.id}, но был получен {build_conf_model.id}"

        with allure.step("Удаление билд конфигурации"):
            build_conf_edit_page_browser = EditBuildPage(browser)
            build_conf_edit_page_browser.delete_build_conf(project_data_1.id, build_conf_data_1.id)

        with (allure.step('Отправка запроса на проверку, что билд конфигурация действительно удалена')):
            get_builds_response = super_admin.api_manager.build_conf_api.get_builds().json()
            build_ids = [build.get('id', {}) for build in get_builds_response.get('buildType', [])]
            assert build_conf_data_1.id not in build_ids, \
                "ID созданной билд конфигурации найден в списке билдов после удаления"
