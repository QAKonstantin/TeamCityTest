from actions.page_actions import PageAction


class Header:
    def __init__(self, actions: PageAction):
        self.page_url = None
        self.actions = actions
        self.logo_button = '.ring-header-logo'
        self.project_button = 'a[title="Projects"] >> text="Projects"'
        self.add_project_button = 'a[title="Create subproject"][data-test-link-with-icon="add"]'

    def go_to_projects_throw_header_button(self):
        self.actions.is_button_active(self.project_button)
        self.actions.click_button(self.project_button)
        self.actions.wait_for_page_load()

    def go_to_create_projects_throw_header_button(self):
        self.actions.is_button_active(self.add_project_button)
        self.actions.click_button(self.add_project_button)
        self.actions.wait_for_page_load()
