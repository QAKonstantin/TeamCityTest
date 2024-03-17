from http import HTTPStatus

from custom_requester.custom_requester import CustomRequester


class ProjectApi(CustomRequester):

    def create_project(self, project_data, expected_status=HTTPStatus.OK, need_verify_status=True):
        return self.send_request("POST", "/app/rest/projects", data=project_data,
                                 expected_status=expected_status,
                                 need_verify_status=need_verify_status)

    def get_projects(self):
        return self.send_request("GET", "/app/rest/projects")

    def get_project_by_locator(self, locator):
        return self.send_request("GET", f"/app/rest/projects/{locator}")

    def delete_project(self, project_id, expected_status=HTTPStatus.NO_CONTENT):
        return self.send_request("DELETE", f"/app/rest/projects/id:{project_id}",
                                 expected_status=expected_status)

    def clean_up_project(self, created_project_id):
        try:
            self.delete_project(created_project_id)
            get_projects_response = self.get_projects().json()
            project_ids = [project.get('id', {}) for project in get_projects_response.get('project', [])]
            assert created_project_id not in project_ids, "ID созданного проекта найден в списке проектов после удаления"
        except ValueError:
            raise ValueError(f"Проект с id {created_project_id} не был создан")
