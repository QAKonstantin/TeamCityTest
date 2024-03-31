import allure
import pytest
import requests

from api.api_manager import ApiManager
from data.build_conf_data import BuildConfData
from data.build_run_data import BuildRunData
from data.project_data import ProjectData
from data.user_data import UserData
from entities.user import User, Role
from enums.browser import BROWSERS
from pages.auth_page import AuthLoginForm, AuthLoginBySuperAdmin
from resources.user_creds import SuperAdminCreds
from utils.browser_setup import BrowserSetup
from utils.data_generator import DataGenerator


@pytest.fixture(params=BROWSERS)
def browser(request):
    playwright, browser, context, page = BrowserSetup.setup(browser_type=request.param)
    yield page
    BrowserSetup.teardown(context, browser, playwright)


@pytest.fixture
def browser_for_setup():
    playwright, browser, context, page = BrowserSetup.setup()
    yield page
    BrowserSetup.teardown(context, browser, playwright)


@pytest.fixture
def login(browser):
    with allure.step("Авторизация под Администратором"):
        login_browser = AuthLoginForm(browser)
        login_browser.login(username="admin", password="admin")
        login_browser.header.check_user_avatar()


@pytest.fixture
def login_by_super_admin(browser):
    with allure.step("Авторизация под Супер Администратором"):
        login_super_admin_browser = AuthLoginBySuperAdmin(browser)
        login_super_admin_browser.login_by_super_admin()
        login_super_admin_browser.header.check_user_avatar()


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()
    super_admin = User(SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD, None, new_session,
                       ["SUPER_ADMIN"])
    super_admin.api_manager.auth_api.auth_and_get_csrf(super_admin.creds)
    return super_admin


@pytest.fixture
def super_admin_creds():
    return SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD


@pytest.fixture
def user_create(user_session, super_admin):
    created_user_pool = []

    def _user_create(role):
        user_data = UserData.create_user_data(role, scope="g")
        super_admin.api_manager.user_api.create_user(user_data)
        new_session = user_session()
        created_user_pool.append(user_data["username"])
        return User(user_data['username'], user_data['password'], user_data['email'], new_session, [Role(role)])

    yield _user_create

    for username in created_user_pool:
        super_admin.api_manager.user_api.delete_user(username)


@pytest.fixture
def project_data(super_admin):
    project_id_pool = []

    def _create_project_data():
        project = ProjectData.create_project_data()
        project_id_pool.append(project.id)
        return project

    yield _create_project_data

    for project_id in project_id_pool:
        super_admin.api_manager.auth_api.auth_and_get_csrf(super_admin.creds)
        super_admin.api_manager.project_api.clean_up_project(project_id)


@pytest.fixture
def build_conf_data(super_admin):
    build_conf_id_pool = []

    def _create_build_conf_data(project_id):
        build_conf = BuildConfData.create_build_conf_data(project_id)
        build_conf_id_pool.append(build_conf.id)
        return build_conf

    yield _create_build_conf_data

    for build_conf_id in build_conf_id_pool:
        super_admin.api_manager.auth_api.auth_and_get_csrf(super_admin.creds)
        super_admin.api_manager.build_conf_api.clean_up_build_conf(build_conf_id)


@pytest.fixture
def build_run_data():
    def _create_build_run_data(build_conf_id):
        build_run_data = BuildRunData.build_run_data(build_conf_id)
        return build_run_data

    yield _create_build_run_data


@pytest.fixture
def random_description():
    return DataGenerator.fake_description()
