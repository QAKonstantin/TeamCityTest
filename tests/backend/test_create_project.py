from http import HTTPStatus

import allure
import pytest

from data.project_data import ProjectResponseModel, ProjectData
from enums.roles import Roles


class TestProjectCreate:

    @pytest.mark.parametrize("role", [
        Roles.SYSTEM_ADMIN.value,
        Roles.PROJECT_ADMIN.value,
        Roles.AGENT_MANAGER.value,
    ], ids=["By system admin",
            "By project admin",
            "By agent manager"])
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.parent_suite("API тесты")
    @allure.suite("Управление проектами")
    @allure.sub_suite("Создание проекта")
    @allure.title('Проверка создания проекта')
    @allure.description('Проверяется создание проекта и пополнение в общем списке проектов')
    @pytest.mark.projects
    @pytest.mark.api
    def test_positive_creating_project_by_roles(self, project_data, user_create, role):
        with allure.step('Подготовка данных для создания проекта'):
            project_data_1 = project_data()

        with allure.step(f'Создание и авторизация пользователя с ролью {role}'):
            role_user = user_create(role)
            role_user.api_manager.auth_api.auth_and_get_csrf(role_user.creds)

        with allure.step('Отправка запроса на создание проекта'):
            created_project_response = role_user.api_manager.project_api.create_project(
                project_data_1.model_dump()).text
            created_project_model = ProjectResponseModel.model_validate_json(created_project_response)
        with pytest.assume:
            assert created_project_model.id == project_data_1.id, \
                f"Ожидался project_id= {project_data_1.id}, но был получен {created_project_model.id}"
        with pytest.assume:
            assert created_project_model.parentProjectId == project_data_1.parentProject["locator"], \
                (f"Ожидался parent project_id= {project_data_1.parentProject['locator']},"
                 f" но был получен {created_project_model.parentProjectId}")

        with allure.step('Отправка запроса на получение информации по созданному проекту'):
            data_project_response = role_user.api_manager.project_api.get_project_by_locator(
                project_data_1.id).text
            data_project_model = ProjectResponseModel.model_validate_json(data_project_response)

        with pytest.assume:
            assert data_project_model.id == project_data_1.id, \
                f"Не найден созданный project_id={project_data_1.id} среди существующих проектов"

    @pytest.mark.parametrize("role", [
        Roles.PROJECT_DEVELOPER.value,
        Roles.PROJECT_VIEWER.value,
    ], ids=["By developer",
            "By viewer"])
    @allure.severity(allure.severity_level.NORMAL)
    @allure.parent_suite("API тесты")
    @allure.suite("Управление проектами")
    @allure.sub_suite("Создание проекта")
    @allure.sub_suite("Негативные сценарии")
    @allure.title('Проверка отсутствия прав на создание проекта')
    @allure.description('Проверяется невозможность создания проекта под определенными ролями')
    @pytest.mark.projects
    def test_negative_creating_project_by_roles(self, user_create, role):
        with allure.step('Подготовка данных для создания проекта'):
            project_data_1 = ProjectData.create_project_data()

        with allure.step(f'Создание и авторизация пользователя с ролью {role}'):
            role_user = user_create(role)
            role_user.api_manager.auth_api.auth_and_get_csrf(role_user.creds)

        with allure.step(f'Проверка на отсутствие доступа для создания проекта под ролью {role}'):
            created_project_response = role_user.api_manager.project_api.create_project(project_data_1.model_dump(),
                                                                                        need_verify_status=False)
        assert "AccessDeniedException" in created_project_response.text, \
            f"У пользователя с ролью {role} не должно быть доступа к созданию проекта"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.parent_suite("API тесты")
    @allure.suite("Управление проектами")
    @allure.sub_suite("Создание проекта")
    @allure.sub_suite("Негативные сценарии")
    @allure.title('Проверка невозможности создания проектов с одинаковыми данными')
    @allure.description(
        'Проверяется валидация DuplicateProjectNameException при повторном создании проекта с существующими данными')
    @pytest.mark.projects
    def test_create_existing_project(self, project_data, super_admin):
        with allure.step('Подготовка данных для создания проекта'):
            project_data_1 = project_data()

        with allure.step('Отправка запроса на создание проекта'):
            created_project_response = super_admin.api_manager.project_api.create_project(
                project_data_1.model_dump()).text
            created_project_model = ProjectResponseModel.model_validate_json(created_project_response)
        with pytest.assume:
            assert created_project_model.id == project_data_1.id, \
                f"Ожидался project_id= {project_data_1.id}, но был получен {created_project_model.id}"

        with allure.step('Отправка повторного запроса на создание такого же проекта'):
            created_project_response = super_admin.api_manager.project_api.create_project(
                project_data_1.model_dump(), expected_status=HTTPStatus.BAD_REQUEST).text
            assert "DuplicateProjectNameException: Project with this name already exists" in created_project_response

    @pytest.mark.parametrize(("attribute", "status_code", "text_error", "value"), [
        ("name", HTTPStatus.BAD_REQUEST, "BadRequestException: Project name cannot be empty", ''),
        ("id", HTTPStatus.INTERNAL_SERVER_ERROR, "InvalidIdentifierException: Project ID must not be empty", ''),
        ("parentProject", HTTPStatus.BAD_REQUEST,
         "BadRequestException: No project specified. Either 'id', 'internalId' "
         "or 'locator' attribute should be present.", {})
    ], ids=["name",
            "id",
            "parentProject"])
    @allure.severity(allure.severity_level.NORMAL)
    @allure.parent_suite("API тесты")
    @allure.suite("Управление проектами")
    @allure.sub_suite("Создание проекта")
    @allure.sub_suite("Негативные сценарии")
    @allure.title('Невозможность создания проекта с пустыми атрибутами')
    @allure.description(
        'Проверяется валидация с пустыми атрибутами проекта')
    @pytest.mark.projects
    def test_create_project_with_empty_attributes(self, super_admin, attribute, status_code, text_error, value):
        with allure.step('Подготовка данных для создания проекта'):
            project_data_1 = dict(ProjectData.create_project_data())
            project_data_1[attribute] = value

        with (allure.step(f'Отправка запроса на создание проекта с пустым {attribute}')):
            created_project_response = super_admin.api_manager.project_api.create_project(
                project_data_1, expected_status=status_code).text
            assert text_error in created_project_response, \
                f'Ожидаемое сообщение об ошибке не соответствует фактическому: {created_project_response}'
