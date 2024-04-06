import allure
import pytest

from data.build_conf_data import BuildConfResponseModel
from data.project_data import ProjectResponseModel
from pages.build_conf_page import RunBuildPage


class TestBuildE2E:
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.parent_suite("UI тесты")
    @allure.suite("Управление запусками билдов")
    @allure.sub_suite("Запуск билда")
    @allure.title("Cоздание проекта, билд конфигурации, шага и запуск билда")
    @allure.description(
        "Авторизация Администратором, создание проекта, билд конфигурации, шага в командной строке и запуск билда")
    @pytest.mark.build_run
    @pytest.mark.ui
    def test_e2e_run_build(self, project_data, build_conf_data, random_description, browser, super_admin, login):
        with allure.step('Подготовка данных для создания проекта и билд конфигурации'):
            project_data_1 = project_data()
            build_conf_data_1 = build_conf_data(project_data_1.id)

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

        with allure.step("Запуск билда"):
            run_build_browser = RunBuildPage(browser, build_conf_data_1.id)
            run_build_browser.run_build()

        with allure.step("Проверка, что билд завершился успешно"):
            run_build_browser.check_last_status_running_build()
