import time
from http import HTTPStatus

import allure
import pytest
from data.build_conf_data import BuildConfResponseModel
from data.build_run_data import BuildRunResponseModel, BuildGetResponseModel, BuildRunData
from data.project_data import ProjectResponseModel
from enums.build_model import BuildStatus, BuildState
from enums.roles import Roles


class TestRunBuild:

    @pytest.mark.parametrize("role", [
        Roles.SYSTEM_ADMIN.value
    ], ids=["By system admin"])
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.parent_suite("API тесты")
    @allure.suite("Управление запусками билдов")
    @allure.sub_suite("Запуск билда")
    @allure.title('Проверка запуска билда')
    @allure.description('Проверяется запуск и успешная работа билда')
    @pytest.mark.build_run
    @pytest.mark.api
    @pytest.mark.additional
    def test_run_build_by_all_roles(self, project_data, build_conf_data, build_run_data, super_admin, user_create,
                                    role):
        with allure.step('Подготовка данных для создания проекта, билд конфигурации и запуска билда'):
            project_data_1 = project_data()
            build_conf_data_1 = build_conf_data(project_data_1.id)
            build_run_1 = build_run_data(build_conf_data_1.id)

        with allure.step(f'Создание и авторизация пользователя с ролью {role}'):
            role_user = user_create(role)
            role_user.api_manager.auth_api.auth_and_get_csrf(role_user.creds)

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

        with allure.step('Отправка запроса на запуск билда'):
            run_build_response = role_user.api_manager.build_run_api.run_build(build_run_1.model_dump()).text
            run_build_model = BuildRunResponseModel.model_validate_json(run_build_response)

        with allure.step('Ожидание получения успешного статуса после запуска билда'):
            get_build_data = role_user.api_manager.build_run_api.get_running_build_by_id(run_build_model.id).text
            get_build_data_model = BuildGetResponseModel.model_validate_json(get_build_data)

            build_state = get_build_data_model.build[0].state
            timeout = 0
            while build_state != BuildState.BUILD_FINISHED.value:
                if timeout != 30:
                    time.sleep(1)
                    get_build_data = role_user.api_manager.build_run_api.get_running_build_by_id(
                        run_build_model.id).json()
                    print(f"get_build_data: \n + {get_build_data}")
                    build_state = get_build_data['build'][0]['state']
                    timeout += 1
                    print(f"build_state_new:  {build_state}")
                else:
                    raise TimeoutError(f"Билд с id: {run_build_model.id} не был завершён в течение отведённого времени")

            with pytest.assume:
                build_status = get_build_data['build'][0]['status']
                assert build_status == BuildStatus.BUILD_SUCCESS.value, \
                    f"Ожидался статус {BuildStatus.BUILD_SUCCESS.value}, но был получен {build_status}"

            with pytest.assume:
                assert run_build_model.buildType.id == build_conf_data_1.id, \
                    f"Ожидался build_conf_id={build_conf_data_1.id}, но был получен {run_build_model.buildType.id}"

            with pytest.assume:
                assert run_build_model.buildType.projectId == project_data_1.id, \
                    f"Ожидался project_id={project_data_1.id}, но был получен {run_build_model.buildType.projectId}"

            with pytest.assume:
                assert run_build_model.triggered.user.username == role_user.username, \
                    f"Ожидался username={role_user.username}, но был получен {run_build_model.triggered.user.username}"

    @pytest.mark.parametrize(("attribute", "status_code", "text_error"), [
        ('', HTTPStatus.NOT_FOUND, "NotFoundException: Nothing is found by locator 'count:1,id:'."),
        ('3_tywwerttr_1', HTTPStatus.NOT_FOUND,
         "NotFoundException: No build type nor template is found by id '3_tywwerttr_1'.")
    ], ids=["empty value",
            "non-existent value"])
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.parent_suite("API тесты")
    @allure.suite("Управление запусками билдов")
    @allure.sub_suite("Запуск билда")
    @allure.sub_suite("Негативные сценарии")
    @allure.title('Проверка невозможности запуска билда с невалидным id билд конфигурации')
    @pytest.mark.build_run
    def test_negative_run_build(self, project_data, build_conf_data, super_admin, attribute, status_code, text_error):
        with allure.step('Подготовка данных для создания проекта, билд конфигурации и запуска билда'):
            project_data_1 = project_data()
            build_conf_data_1 = build_conf_data(project_data_1.id)
            build_run_1 = BuildRunData.build_run_data(attribute)

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

        with allure.step(f'Отправка запроса на запуск билда со значением build_conf_id: {attribute}'):
            run_build_response = super_admin.api_manager.build_run_api.run_build(build_run_1.model_dump(),
                                                                                 expected_status=status_code).text
            assert text_error in run_build_response, \
                f'Ожидаемое сообщение об ошибке не соответствует фактическому: {run_build_response}'
