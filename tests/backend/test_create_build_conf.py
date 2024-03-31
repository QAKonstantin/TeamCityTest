from http import HTTPStatus

import allure
import pytest

from data.build_conf_data import BuildConfResponseModel, BuildConfData
from data.project_data import ProjectResponseModel
from enums.roles import Roles


class TestBuildConfCreate:

    @pytest.mark.parametrize("role", [
        Roles.SYSTEM_ADMIN.value,
        Roles.PROJECT_ADMIN.value,
        Roles.AGENT_MANAGER.value,
    ], ids=["By system admin",
            "By project admin",
            "By agent manager"])
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.parent_suite("API тесты")
    @allure.suite("Управление билд конфигурациями")
    @allure.sub_suite("Создание билд конфигурации")
    @allure.title('Проверка создания билд конфигурации')
    @allure.description('Проверяется создание билд конфигурации')
    @pytest.mark.build_conf
    def test_positive_creating_build_conf(self, project_data, build_conf_data, user_create, role):
        with allure.step('Подготовка данных для создания проекта и билд конфигурации'):
            project_data_1 = project_data()
            build_conf_data_1 = build_conf_data(project_data_1.id)

        with allure.step(f'Создание и авторизация пользователя с ролью {role}'):
            role_user = user_create(role)
            role_user.api_manager.auth_api.auth_and_get_csrf(role_user.creds)

        with allure.step('Отправка запроса на создание проекта'):
            created_project_response = role_user.api_manager.project_api.create_project(
                project_data_1.model_dump()).text
            project_model = ProjectResponseModel.model_validate_json(created_project_response)
            assert project_model.id == project_data_1.id, \
                f"Ожидался project_id={project_data_1.id}, но был получен {project_model.id}"

        with allure.step('Отправка запроса на создание билд конфигурации'):
            create_build_conf_response = role_user.api_manager.build_conf_api.create_build_conf(
                build_conf_data_1.model_dump()).text
            build_conf_model = BuildConfResponseModel.model_validate_json(create_build_conf_response)
            with pytest.assume:
                assert build_conf_model.id == build_conf_data_1.id, \
                    f"Ожидался build_conf_id={build_conf_data_1.id}, но был получен {build_conf_model.id}"

        with allure.step('Отправка запроса на получение информации по созданной билд конфигурации'):
            data_build_conf_response = role_user.api_manager.build_conf_api.get_build_conf_by_locator(
                build_conf_data_1.id).text
            data_build_conf_model = BuildConfResponseModel.model_validate_json(data_build_conf_response)
        with pytest.assume:
            assert data_build_conf_model.id == build_conf_data_1.id, \
                f"Не найден созданный build_conf_id={build_conf_data_1.id} среди существующих билд конфигураций"

    @pytest.mark.parametrize("role", [
        Roles.PROJECT_DEVELOPER.value,
        Roles.PROJECT_VIEWER.value,
    ], ids=["By developer",
            "By viewer"])
    @allure.severity(allure.severity_level.NORMAL)
    @allure.parent_suite("API тесты")
    @allure.suite("Управление билд конфигурациями")
    @allure.sub_suite("Создание билд конфигурации")
    @allure.sub_suite("Негативные сценарии")
    @allure.title('Проверка отсутствия прав на создание билд конфигурации')
    @allure.description('Проверяется невозможность создания билд конфигурации под определёнными ролями')
    @pytest.mark.build_conf
    def test_negative_creating_build_conf(self, project_data, build_conf_data, super_admin, user_create, role):
        with allure.step('Подготовка данных для создания проекта и билд конфигурации'):
            project_data_1 = project_data()
            build_conf_data_1 = BuildConfData.create_build_conf_data(project_data_1.id)

        with allure.step(f'Создание и авторизация пользователя с ролью {role}'):
            role_user = user_create(role)
            role_user.api_manager.auth_api.auth_and_get_csrf(role_user.creds)

        with allure.step('Отправка запроса на создание проекта под супер администратором'):
            project_response = super_admin.api_manager.project_api.create_project(
                project_data_1.model_dump()).text
            ProjectResponseModel.model_validate_json(project_response)

        with allure.step(f'Проверка на отсутствие доступа для создания билд конфигурации под ролью {role}'):
            build_conf_response = role_user.api_manager.build_conf_api.create_build_conf(
                build_conf_data_1.model_dump(), need_verify_status=False)

        assert "AccessDeniedException" in build_conf_response.text

    @pytest.mark.parametrize(("attribute", "status_code", "text_error", "value"), [
        ("name", HTTPStatus.BAD_REQUEST,
         "BadRequestException: When creating a build type, non empty name should be provided.", ''),
        ("id", HTTPStatus.INTERNAL_SERVER_ERROR,
         "InvalidIdentifierException: Build configuration or template ID must not be empty", ''),
        ("project_id", HTTPStatus.NOT_FOUND,
         "NotFoundException: No project found by locator 'count:1,id:", '')
    ], ids=["name",
            "id",
            "project_id"])
    @allure.severity(allure.severity_level.NORMAL)
    @allure.parent_suite("API тесты")
    @allure.suite("Управление билд конфигурациями")
    @allure.sub_suite("Создание билд конфигурации")
    @allure.sub_suite("Негативные сценарии")
    @allure.title('Проверка невозможности создания билд конфигурации')
    @allure.description('Проверяется валидация с пустыми атрибутами билд конфигурации')
    @pytest.mark.build_conf
    @pytest.mark.api
    def test_create_build_conf_with_empty_attributes(self, project_data, build_conf_data, super_admin, attribute,
                                                     status_code, text_error, value):
        with (allure.step('Подготовка данных для создания проекта и билд конфигурации')):
            project_data_1 = project_data()
            build_conf_data_1 = dict(BuildConfData.create_build_conf_data(project_data_1.id))
            if attribute == "project_id":
                build_conf_data_1["project"]["id"] = ''
            else:
                build_conf_data_1[attribute] = value

        with allure.step('Отправка запроса на создание проекта'):
            created_project_response = super_admin.api_manager.project_api.create_project(
                project_data_1.model_dump()).text
            project_model = ProjectResponseModel.model_validate_json(created_project_response)
            assert project_model.id == project_data_1.id, \
                f"Ожидался project_id={project_data_1.id}, но был получен {project_model.id}"

        with allure.step('Отправка запроса на создание билд конфигурации'):
            create_build_conf_response = super_admin.api_manager.build_conf_api.create_build_conf(
                build_conf_data_1, expected_status=status_code).text
            assert text_error in create_build_conf_response, \
                f'Ожидаемое сообщение об ошибке не соответствует фактическому: {create_build_conf_response}'

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.parent_suite("API тесты")
    @allure.suite("Управление билд конфигурациями")
    @allure.sub_suite("Создание билд конфигурации")
    @allure.sub_suite("Негативные сценарии")
    @allure.title('Невозможность создания билд конфигурации с одинаковыми данными')
    @allure.description(
        'Проверяется валидация DuplicateExternalIdException при повторном создании билд конфигурации с существующими '
        'данными')
    @pytest.mark.build_conf
    def test_create_existing_build_conf(self, project_data, build_conf_data, super_admin):

        with allure.step('Подготовка данных для создания проекта и билд конфигурации'):
            project_data_1 = project_data()
            build_conf_data_1 = build_conf_data(project_data_1.id)

        with allure.step('Отправка запроса на создание проекта'):
            created_project_response = super_admin.api_manager.project_api.create_project(
                project_data_1.model_dump()).text
            project_model = ProjectResponseModel.model_validate_json(created_project_response)
            assert project_model.id == project_data_1.id, \
                f"Ожидался project_id={project_data_1.id}, но был получен {project_model.id}"

        with allure.step('Отправка запроса на создание билд конфигурации'):
            create_build_conf_response = super_admin.api_manager.build_conf_api.create_build_conf(
                build_conf_data_1.model_dump()).text
            build_conf_model = BuildConfResponseModel.model_validate_json(create_build_conf_response)
            with pytest.assume:
                assert build_conf_model.id == build_conf_data_1.id, \
                    f"Ожидался build_conf_id={build_conf_data_1.id}, но был получен {build_conf_model.id}"

        with allure.step('Отправка повторного запроса на создание такой же билд конфигурации'):
            create_build_conf_response = super_admin.api_manager.build_conf_api.create_build_conf(
                build_conf_data_1.model_dump(), expected_status=HTTPStatus.BAD_REQUEST, need_verify_status=False).text
            assert (f'DuplicateExternalIdException: The build configuration / template ID "{build_conf_data_1.id}" '
                    f'is already used by another configuration or template') in create_build_conf_response
