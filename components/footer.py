import os

from actions.page_actions import PageAction
from enums.hosts import BASE_URL, JETBRAINS_URL
from dotenv import load_dotenv

load_dotenv()


class Footer:
    def __init__(self, actions: PageAction):
        self.actions = actions
        self.page_url = None
        self.teamcity_version = "div.Footer__version--YW"
        self.copyright = "div.Footer__copyright--Pt"
        self.about_teamcity = "span.ring-link-inner:has-text('About TeamCity')"
        self.license_agreement = "span.ring-link-inner:has-text('License Agreement')"
        self.version = "div[title='Node id: MAIN_SERVER']"

    def go_to_about_teamcity(self, close_tab=False):
        """
        Переход по ссылке о Teamcity
        :param close_tab: Флаг для закрытия текущей вкладки. По умолчанию вкладка не закрывается
        """
        self.actions.is_button_active(self.about_teamcity, timeout=30000)
        self.actions.click_button(self.about_teamcity)
        self.page_url = f"{JETBRAINS_URL}/teamcity/?fromServer"
        self.actions.check_open_in_new_tab(self.page_url)
        if close_tab:
            self.actions.close_tab()

    def go_to_license_agreement(self, close_tab=False):
        """
        Переход по ссылке с лицензионным соглашением
        :param close_tab: Флаг для закрытия текущей вкладки. По умолчанию вкладка не закрывается
        """
        self.actions.is_button_active(self.license_agreement, timeout=30000)
        self.actions.click_button(self.license_agreement)
        self.page_url = f"{BASE_URL}/showAgreement.html"
        self.actions.check_open_in_new_tab(self.page_url)
        if close_tab:
            self.actions.close_tab()

    def check_version(self):
        current_version = self.actions.get_text(self.version).replace("&nbsp;", " ")
        expected_version = os.getenv("SYSTEM_VERSION")
        assert current_version == expected_version, (f"Текущая версия системы: {current_version},"
                                                     f" ожидаемая версия: {expected_version}")

    def check_copyright(self):
        current_copyright = self.actions.get_text(self.copyright)
        expected_copyright = os.getenv("COPYRIGHT_TEXT")
        assert current_copyright == expected_copyright, (f"Текущий копирайт: {current_copyright},"
                                                         f"ожидаемый копирайт: {expected_copyright}")
