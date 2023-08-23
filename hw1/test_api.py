import yaml
import requests

S = requests.Session()

with open('config.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)
    url_posts = data['url_posts']


def test_rest_get_post(user_login, post_title):
    res = S.get(url=url_posts, headers={'X-Auth-Token': user_login}, params={'owner': 'notMe'}).json()['data']
    r = [i['title'] for i in res]
    assert post_title in r, 'Test 1 FAILED'


def test_rest_new_post(user_login, new_post):
    S.post(url=url_posts, headers={'X-Auth-Token': user_login}, data={'title': new_post[0],
                                                                      'description': new_post[1],
                                                                      'content': new_post[2]})
    posts_info = S.get(url=url_posts, headers={'X-Auth-Token': user_login}).json()['data']
    descriptions = [i['description'] for i in posts_info]
    assert new_post[1] in descriptions, 'Test 2 FAILED'