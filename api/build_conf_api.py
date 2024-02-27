from http import HTTPStatus

from custom_requester.custom_requester import CustomRequester


class BuildConfAPI(CustomRequester):

    def create_build_conf(self, build_data, expected_status=HTTPStatus.OK, need_verify_status=True):
        return self.send_request("POST", "/app/rest/buildTypes", data=build_data,
                                 expected_status=expected_status,
                                 need_verify_status=need_verify_status)

    def get_build_conf_by_locator(self, locator):
        return self.send_request("GET", f"/app/rest/buildTypes/id:{locator}")

    def get_builds(self):
        return self.send_request("GET", "/app/rest/buildTypes")

    def delete_build_conf(self, create_build_id, expected_status=HTTPStatus.NO_CONTENT):
        return self.send_request("DELETE", f"/app/rest/buildTypes/id:{create_build_id}",
                                 expected_status=expected_status)

    def clean_up_build_conf(self, create_build_id):
        try:
            self.delete_build_conf(create_build_id)
            get_builds_response = self.get_builds().json()
            build_ids = [build.get('id', {}) for build in get_builds_response.get('buildType', [])]
            assert create_build_id not in build_ids, \
                "ID созданной билд конфигурации найден в списке билдов после удаления"
        except ValueError:
            raise ValueError(f"Билд конфигурации с id {create_build_id} не был создан")
