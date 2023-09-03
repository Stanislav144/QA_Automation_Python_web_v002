from requests import JSONDecodeError

from BaseApp import BasePage, BaseRestSession
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
import logging
import yaml


class TestSearchLocators:
    """Класс для хранения локаторов"""
    ids = dict()
    with open('locators.yaml') as f:
        locators = yaml.safe_load(f)

    for locator in locators['xpath'].keys():
        ids[locator] = (By.XPATH, locators['xpath'][locator])

    for locator in locators['css'].keys():
        ids[locator] = (By.CSS_SELECTOR, locators['css'][locator])


class OperationsHelper(BasePage):
    """Класс, содержащий методы для работы с элементами на веб-страницах"""

    #  EXCEPTIONS
    def enter_text_into_field(self, locator, word, description=None):
        """Вспомогательный метод для методов ввода в поля текста"""
        if description:
            element_name = description
        else:
            element_name = locator
        logging.info(f'Send {word} to element {element_name}')

        field = self.find_element(locator)
        if not field:
            logging.debug(f'Element {locator} not found')
            return False
        try:
            field.clear()
            field.send_keys(word)
        except TimeoutException:
            logging.exception(f'Exception while operation with {locator}')
            return False

        return True

    def click_button(self, locator, description):
        """Вспомогательный метод для методов нажатия на кнопку"""
        if description:
            element_name = description
        else:
            element_name = locator

        button = self.find_element(locator)
        if not button:
            return False

        try:
            button.click()
        except TimeoutException:
            logging.exception('Exception with click')

        logging.debug(f'Clicked {element_name}')
        return True

    def get_text_from_element(self, locator, description=None):
        """Вспомогательный метод для методов возврата текста из элемента"""
        if description:
            element_name = description
        else:
            element_name = locator

        field = self.find_element(locator, time=3)
        if not field:
            return None

        try:
            text = field.text
        except TimeoutException:
            logging.exception(f'Exception while getting a test from {element_name}')
            return None

        logging.debug(f'Founded text {text} in field {element_name}')
        return text

    # ENTER TEXT
    def enter_login(self, word):
        """Ввод логина в поле ввода username страницы авторизации"""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_LOGIN_FIELD'], word,
                                   description='Enter a login on an authorisation page')

    def enter_pass(self, word):
        """Ввод пароля в поле ввода password страницы авторизации"""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_PASS_FIELD'], word,
                                   description='Enter a password on  an authorisation page')

    def enter_post_title(self, word):
        """Ввод заголовка поста в поле ввода Title формы создания поста"""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_FORM_POST_TITLE'], word,
                                   description='Enter a title in a creating post form')

    def enter_post_description(self, word):
        """Ввод описания поста в поле ввода Description формы создания поста"""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_FORM_POST_DESCRIPTION'], word,
                                   description='Enter a description in a creating post form')

    def enter_post_content(self, word):
        """Ввод поста в поле ввода Content формы создания поста"""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_FORM_POST_CONTENT'], word,
                                   description='Enter a content in a creating post form')

    def enter_username_contact_us_form(self, word):
        """Ввод имени пользователя в поле ввода 'Your name' формы 'Contact us!'"""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_USERNAME_FIELD_CONTACT_US_FORM'], word,
                                   description='Enter an username in a contact us form')

    def enter_email_contact_us_form(self, word):
        """Ввод электронной почты в поле ввода 'Your email' формы 'Contact us!'"""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_EMAIL_FIELD_CONTACT_US_FORM'], word,
                                   description='Enter an email in a contact us form')

    def enter_content_contact_us_form(self, word):
        """Ввод текста обращения в поле ввода 'Content' формы 'Contact us!'"""
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_CONTENT_FIELD_CONTACT_US_FORM'], word,
                                   description='Enter a content in a contact us form')

    #  GET TEXT
    def get_error_text(self):
        """Возврат текста из блока ошибки страницы авторизации"""
        return self.get_text_from_element(TestSearchLocators.ids['LOCATOR_ERROR_FIELD'],
                                          description='Get error text')

    def get_login_text(self):
        """Возврат имени пользователя"""
        return self.get_text_from_element(TestSearchLocators.ids['LOCATOR_USER_PROFILE_LINK'],
                                          description='Get login text')

    def get_post_title(self):
        """Возврат названия поста пользователя"""
        return self.get_text_from_element(TestSearchLocators.ids['LOCATOR_POST_NAME'],
                                          description='Get post name')

    def get_alert(self):
        """Возврат текста alert при отправке формы обратной связи"""
        logging.info('Get alert text')
        text = self.get_alert_text()
        logging.info(text)
        return text

    #  CLICK BUTTON
    def click_login_button(self):
        """Нажатие кнопки Login страницы авторизации"""
        self.click_button(TestSearchLocators.ids['LOCATOR_LOGIN_BTN'],
                          description='Login button')

    def click_create_post_button(self):
        """Нажатие кнопки создания поста"""
        self.click_button(TestSearchLocators.ids['LOCATOR_CREATE_POST_BTN'],
                          description='Create post button')

    def click_save_post_button(self):
        """Нажатие кнопки сохранения поста"""
        self.click_button(TestSearchLocators.ids['LOCATOR_SAVE_POST_BTN'],
                          description='Save post button')

    def click_contact_us_button(self):
        """Нажатие кнопки открытия формы обратной связи на главной странице"""
        self.click_button(TestSearchLocators.ids['LOCATOR_CONTACT_FORM_BTN'],
                          description='Contact Us button')

    def click_send_contact_us_form(self):
        """Нажатие кнопки отправки формы обратной связи"""
        self.click_button(TestSearchLocators.ids['LOCATOR_SEND_CONTACT_US_FORM_BTN'],
                          description='Save Contact Us form')


class RestHelper(BaseRestSession):
    """Класс, содержащий методы для работы с REST запросами"""

    def get_user_token(self):
        """Вспомогательный метод авторизации с проверкой, возвращающий токен"""
        token = ''
        try:
            token = self.login()
        except KeyError:
            logging.exception(f'Failed user {self.user_name} login')
        except JSONDecodeError:
            logging.exception(f'404 not found!')

        return token

    def get_post(self, url_posts):
        """Возврат списка постов всех пользователей"""
        logging.info('Getting list of posts...')

        token = self.get_user_token()
        results = []

        try:
            data = self.session.get(url=url_posts,
                                    headers={'X-Auth-Token': token},
                                    params={'owner': 'notMe'}).json()['data']
            results = [i['title'] for i in data]
        except KeyError:
            logging.exception('Wrong token in GET request')

        if len(results) > 0:
            logging.info('Success')
        else:
            logging.info('Posts list is empty!')

        return results

    def new_post(self, url_posts, title, description, content):
        """Создание нового поста"""
        logging.info('Creating a new post...')

        token = self.get_user_token()
        descriptions = []

        try:
            self.session.post(url=url_posts,
                              headers={'X-Auth-Token': token},
                              data={'title': title, 'description': description, 'content': content})
            posts_info = self.session.get(url=url_posts,
                                          headers={'X-Auth-Token': token}).json()['data']
            descriptions = [i['description'] for i in posts_info]
        except KeyError:
            logging.exception('Wrong data in requests')

        if len(descriptions) > 0:
            logging.info('Success')
        else:
            logging.info("Post creating failed!")

        return descriptions