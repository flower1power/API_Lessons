from json import loads

from faker import Faker

from dm_api_account.apis.account_api import AccountApi, UserCredentials
from mailhog_api.apis.mailhog_api import MailhogApi


def test_post_v1_account():
    faker = Faker()
    account_api = AccountApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    login = faker.name().replace(' ', '')
    password = faker.password()
    email = f'{login}@mail.ru'
    json_data: UserCredentials = {
        "login": login,
        "email": email,
        "password": password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f'Пользователь не был создан {response.json()}'

    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, 'Письма не были получены'
    #
    token = get_activation_token_by_login(login=login, response=response)
    assert token is not None, f'Токен для пользователя {login}, не был получен'

    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, 'Пользователь не был активирован'


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]

    return token
