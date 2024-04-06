import allure
import pytest

from data.project_data import ProjectResponseModel, ProjectData
from pages.create_project_page import ProjectCreationPage
from pages.edit_project_page import ProjectEditPage


class TestProjectE2E:
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.parent_suite("UI тесты")
    @allure.suite("Управление проектами")
    @allure.sub_suite("Создание проекта")
    @allure.title("Cоздание проекта под Администратором")
    @allure.description("Авторизация Администратором и создание проекта")
    @pytest.mark.projects
    @pytest.mark.ui
    def test_e2e_create_project(self, project_data, random_description, browser, super_admin, login):
        project_data_1 = project_data()

        with allure.step("Создание проекта"):
            project_creation_browser = ProjectCreationPage(browser)
            project_creation_browser.create_project(project_data_1.name, project_data_1.id, random_description)

        with allure.step('Отправка запроса на получение информации по созданному проекту'):
            response = super_admin.api_manager.project_api.get_project_by_locator(
                project_data_1.id).text
            created_project = ProjectResponseModel.model_validate_json(response)
            assert created_project.id == project_data_1.id, \
                f"Не найден созданный project_id={created_project.id} среди существующих проектов"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.parent_suite("UI тесты")
    @allure.suite("Управление проектами")
    @allure.sub_suite("Удаление проекта")
    @allure.title("Удаление проекта под Супер Администратором")
    @allure.description("Авторизация Администратором, создание проекта и его удаление")
    @pytest.mark.projects
    @pytest.mark.ui
    def test_e2e_delete_project(self, browser, super_admin, login):
        with allure.step('Подготовка данных для создания проекта'):
            project_data_1 = ProjectData.create_project_data()

        with allure.step('Отправка запроса на создание проекта'):
            created_project_response = super_admin.api_manager.project_api.create_project(
                project_data_1.model_dump()).text
            created_project_model = ProjectResponseModel.model_validate_json(created_project_response)
            assert created_project_model.id == project_data_1.id, \
                f"Ожидался project_id= {project_data_1.id}, но был получен {created_project_model.id}"

        with allure.step("Удаление проекта"):
            project_edit_page_browser = ProjectEditPage(browser)
            project_edit_page_browser.delete_project(project_data_1.id)

        with (allure.step('Отправка запроса на проверку, что проект действительно удалён')):
            get_projects_response = super_admin.api_manager.project_api.get_projects().json()
            project_ids = [project.get('id', {}) for project in get_projects_response.get('project', [])]
            assert project_data_1.id not in project_ids, "ID созданного проекта найден в списке проектов после удаления"
