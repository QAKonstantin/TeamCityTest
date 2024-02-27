from api.auth_api import AuthAPI
from api.build_conf_api import BuildConfAPI
from api.build_run_api import BuildRunApi
from api.project_api import ProjectApi
from api.user_api import UserApi


class ApiManager:
    """
    Используется с целью создания экземпляров классов для тестов в рамках одной сессии
    """

    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.project_api = ProjectApi(session)
        self.build_conf_api = BuildConfAPI(session)
        self.build_run_api = BuildRunApi(session)
        self.user_api = UserApi(session)

    def close_session(self):
        self.session.close()
