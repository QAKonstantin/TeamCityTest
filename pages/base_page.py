from playwright.sync_api import Page

from actions.page_actions import PageAction
from components.footer import Footer
from components.header import Header
from enums.hosts import BASE_URL


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self._base_url = BASE_URL
        self._endpoint = ""
        self.actions = PageAction(page)
        self.header = Header(self.actions)
        self.footer = Footer(self.actions)

    @property
    def page_url(self):
        return self._base_url + self._endpoint

    @page_url.setter
    def page_url(self, endpoint: str):
        self._endpoint = endpoint
