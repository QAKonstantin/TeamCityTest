from playwright.sync_api import Page, expect
import allure


class PageAction:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url):
        with allure.step(f"Переход на URL: {url}"):
            self.page.goto(url)

    def check_url(self, expected_url: str, timeout=10000):
        with allure.step(f"Проверка URL: ожидаемый URL - {expected_url}"):
            expect(self.page).to_have_url(expected_url, timeout=timeout)

    def check_open_in_new_tab(self, expected_url: str):
        with allure.step(f"Проверка, что ссылка открылась в новой вкладке"):
            try:
                with self.page.context.expect_page() as new_page:
                    expect(new_page.value).to_have_url(expected_url)
            except Exception:
                raise AssertionError(
                    f"Некорректная ссылка: {new_page.value} \n ОР: {expected_url} \n"
                    f"или ссылка должна открываться в новой вкладке")

    def close_tab(self, n=-1):
        """
        :param n: Номер вкладки, которую необходимо закрыть. По умолчанию закрывается последняя вкладка
        """
        with allure.step(f"Закрыть вкладку"):
            all_tabs = self.page.context.pages
            all_tabs[n].close()

    def wait_for_url_changed(self, expected_url: str):
        with allure.step(f"Ожидание изменения URL на {expected_url}"):
            self.page.wait_for_url(expected_url)

    def wait_for_page_load(self):
        with allure.step(f"Ожидание загрузки страницы"):
            self.page.wait_for_load_state('load')

    def click_button(self, selector, timeout=30000):
        with allure.step(f"Клик по элементу: {selector}"):
            self.page.click(selector, timeout=timeout)

    def activate_inactive_checkbox(self, selector):
        with allure.step(f"Активация чекбокса {selector}"):
            if not self.page.is_checked(selector):
                self.click_button(selector)
                assert self.page.is_checked(selector), f"Чекбокс {selector} остался неактивен"

    def is_element_present(self, selector):
        with allure.step(f"Проверка видимости элемента: {selector}"):
            expect(self.page.locator(selector)).to_be_visible()

    def is_button_active(self, selector):
        with allure.step(f"Проверка активности кнопки: {selector}"):
            expect(self.page.locator(selector)).to_be_enabled(timeout=10000)

    def get_element(self, selector):
        with allure.step(f"Получить элемент по локатору: {selector}"):
            return self.page.locator(selector)

    def get_text(self, selector) -> str:
        with allure.step(f"Получить текст по локатору: {selector}"):
            return self.page.locator(selector).inner_html()

    def input_text(self, selector, text):
        with allure.step(f"Ввод текста {text} в элемент: {selector}"):
            self.page.fill(selector, text)

    def input_filtered_text(self, selector, text):
        with allure.step(f"Ввод текста 'FILTERED' в элемент: {selector}"):
            self.page.fill(selector, text)

    def wait_for_selector(self, selector, timeout=60000):
        with allure.step(f"Ожидаем появления элемента: {selector}"):
            self.page.wait_for_selector(selector, state="attached", timeout=timeout)

    def wait_for_disappear_selector(self, selector, timeout=30000):
        with allure.step(f"Ожидаем исчезновения элемента: {selector}"):
            self.page.wait_for_selector(selector, state='detached', timeout=timeout)

    def assert_text_present_on_page(self, text):
        with allure.step(f"Проверка наличия текста '{text}' на странице"):
            expect(self.page).to_have_text(text)

    def assert_text_in_element(self, selector, text):
        with allure.step(f"Проверка наличия текста '{text}' в элементе: {selector}"):
            expect(self.page.locator(selector)).to_have_text()

    def assert_element_attribute(self, selector, attribute, value):
        with allure.step(f"Проверка значения {value} атрибута {attribute} элемента {selector}"):
            expect(self.page.locator(selector)).to_have_attribute(attribute, value)

    def assert_element_hidden(self, selector):
        with allure.step(f"Проверка, что элемент {selector} скрыт"):
            expect(self.page.locator(selector)).to_be_hidden()

    def assert_count_elements(self, selector, n: int):
        with allure.step(f"Проверка на количество элементов {selector}"):
            expect(self.page.locator(selector)).to_have_count(n)
