import logging
import requests

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class BasePage:
    """Класс, содержащий необходимые методы для работы с webdriver"""

    def __init__(self, driver):
        self.driver = driver
        self.base_url = 'https://test-stand.gb.ru'

    def find_element(self, locator, time=10):
        """Метод, осуществляющий поиск одного элемента и возвращающий его"""
        try:
            element = WebDriverWait(self.driver, time).until(ec.presence_of_element_located(locator),
                                                             message=f"Can't find element by locator {locator}")
        except TimeoutException:
            logging.exception('Find element exception:')
            element = None
        return element

    def get_element_property(self, locator, el_property):
        """Метод, возвращающий свойство одного элемента"""
        element = self.find_element(locator)
        if element:
            return element.value_of_css_property(el_property)
        logging.exception(f'Property {el_property} not found in element with locator {locator}')
        return None

    def go_to_site(self):
        """Переход на указанную страницу"""
        try:
            start_browsing = self.driver.get(self.base_url)
        except TimeoutException:
            logging.exception('Exception while open the site')
            start_browsing = None
        return start_browsing

    def get_alert_text(self):
        """Получение текста alert"""
        try:
            alert = self.driver.switch_to.alert
            return alert.text
        except TimeoutException:
            logging.exception('Exception with alert')
            return None


class BaseRestSession:
    """Класс, содержащий необходимые методы для работы с REST запросами"""

    def __init__(self, url, name, passwd):
        self.url_login = url
        self.user_name = name
        self.user_pass = passwd
        self.session = requests.Session()

    def login(self):
        """Вход в аккаунт и возврат токена"""
        rest = self.session.post(url=self.url_login, data={'username': self.user_name, 'password': self.user_pass})
        return rest.json()['token']