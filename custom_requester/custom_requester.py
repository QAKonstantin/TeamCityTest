import logging
import os
from http import HTTPStatus
from requests import Response
from swagger_coverage_py.listener import CoverageListener

from enums.hosts import BASE_URL


class CustomRequester:
    base_headers = dict({"Content-Type": "application/json", "Accept": "application/json"})

    def __init__(self, session):
        self.session = session
        self.base_url = BASE_URL
        self.logger = logging.getLogger(__name__)

    def send_request(self, method, endpoint, data=None, expected_status=HTTPStatus.OK, need_logging=True,
                     need_verify_status=True):
        """
        Врапер для запросов. Позволяет прикручивать дополнительную логику
        :param method: Метод запроса
        :param endpoint: Ендпоинт для склейки с BASE_URL
        :param data: Тело запроса. По умолчанию пустое, чтобы пропускало no-content запросы
        :param expected_status: Ожидаемый статус код
        :param need_logging: Флаг для логирования. По умолчанию = True
        :param need_verify_status: Флаг для проверки статус кода в ответе. По умолчанию = True
        :return: Возвращает объект ответа
        """
        if endpoint == "/authenticationTest.html?csrf":
            url = f"{self.base_url}{endpoint}"
            response = self.session.request(method=method, url=url, json=data)
        else:
            kwargs = {"json": data}
            response: Response = CoverageListener(
                method=method,
                base_url=self.base_url,
                raw_path=endpoint,
                uri_params={},
                session=self.session,
                **kwargs
            ).response
            if need_logging:
                self.log_request_and_response(response, expected_status, need_verify_status)
            if need_verify_status:
                if response.status_code != expected_status:
                    raise ValueError(f"Unexpected status code: {response.status_code}, expected: {expected_status}")
        return response

    def _update_session_headers(self, **kwargs):
        self.headers = self.base_headers.copy()
        self.headers.update(kwargs)
        self.session.headers.update(self.headers)

    def log_request_and_response(self, response, expected_status, need_verify_status):
        """
        Логирование запросов и ответов. Настройки логирования описаны в pytest.ini
        Преобразует вывод в curl-like (-H хэдеры), (-d тело)

        :param expected_status: Ожидаемый статус код
        :param need_verify_status: Флаг для проверки статус кода в ответе при логировании
        :param response: Объект response, получаемый из метода "send_request"
        """
        try:
            request = response.request
            GREEN = '\033[32m'
            RED = '\033[31m'
            RESET = '\033[0m'
            headers = "\n".join([f"-H '{headers}:{value}'" for headers, value in request.headers.items()])
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace('(call)', '')}"

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
            body = f"-d '{body}' \n" if body != '{}' else ''

            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl - X {request.method} '{request.url}' \n"''
                f"{headers} \n"
                f"{body} \n"
            )
            if need_verify_status:
                response_status = response.status_code
                is_success = expected_status.value
                response_data = response.text

                if response_status != is_success:
                    self.logger.info(
                        f"\tRESPONSE:"
                        f"\nSTATUS_CODE: {RED}{response_status}{RESET}"
                        f"\nDATA: {RED}{response_data}{RESET}"
                    )
        except Exception as e:
            self.logger.info(f"\nLogging went wrong: {type(e)} - {e}")
