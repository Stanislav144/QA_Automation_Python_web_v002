import logging
import yaml

from testpage import RestHelper

with open('testdata.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)
    user_login = data['login']
    user_passwd = data['password']
    url_login = data['url_login']
    url_posts = data['url_posts']
    not_owner_post_title = data['another_user_post_title']
    post_title = data['post_title']
    post_description = data['post_description']
    post_content = data['post_content']


def test_rest_get_post():
    """Позитивный тест получения списка постов"""
    logging.info('_____________REST test 1 is starting_____________')
    rest_session = RestHelper(url_login, user_login, user_passwd)
    posts = rest_session.get_post(url_posts)
    assert not_owner_post_title in posts, '!!!REST test 1 FAILED!!!'


def test_rest_new_post():
    logging.info('_____________REST test 2 is starting_____________')
    rest_session = RestHelper(url_login, user_login, user_passwd)
    new_post = rest_session.new_post(url_posts, post_title, post_description, post_content)
    assert post_description in new_post, '!!!REST test 2 FAILED!!!'