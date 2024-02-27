from http import HTTPStatus

from custom_requester.custom_requester import CustomRequester


class BuildRunApi(CustomRequester):

    def run_build(self, build_run_data, expected_status=HTTPStatus.OK, need_verify_status=True):
        return self.send_request("POST", "/app/rest/buildQueue", data=build_run_data,
                                 expected_status=expected_status,
                                 need_verify_status=need_verify_status)

    def get_running_build_by_id(self, build_id, expected_status=HTTPStatus.OK):
        return self.send_request("GET", f"/app/rest/builds?locator=id:{build_id}",
                                 expected_status=expected_status)

    def get_builds_from_build_conf(self, build_conf, expected_status=HTTPStatus.OK):
        return self.send_request("GET", f"/app/rest/builds/?locator=buildType:{build_conf}",
                                 expected_status=expected_status)
