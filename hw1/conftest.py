import pytest
import yaml
import requests

with open('config.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)
    username, password, address_login = data['username'], data['password'], data['url_login']

S = requests.Session()


@pytest.fixture()
def user_login():
    rest1 = S.post(url=address_login, data={'username': username, 'password': password})
    return rest1.json()['token']


@pytest.fixture()
def post_title():
    return 'рпрпоалвовсиарар2git commit -m "first commit"'


@pytest.fixture()
def new_post():
    title = 'Беловодье'
    description = ('"Белово́дье'
                   'Белово́дье 002')
    content = ('Белово́дье — в старообрядческих преданиях легендарная страна на востоке от России, где во всей полноте сохранилось «древлеправославное» (дораскольное, «дониконовское»)' 
               'священство, где нет и не может быть антихриста. Легенда сформировалась в конце XVIII — начале XIX века. Легенда не была связана с деятельностью определённого' 
               'старообрядческого согласия, она развивалась среди поморцев, часовенных, беглопоповцев и др.[1] В Словаре Даля беловодье определяется как не заселённая, вольная земля[2].')
    return title, description, content