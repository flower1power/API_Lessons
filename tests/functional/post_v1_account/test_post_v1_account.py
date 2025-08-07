from faker import Faker

from dm_api_account.apis.account_api import AccountApi, UserCredentials


def test_post_v1_account():
    faker = Faker()
    account_api = AccountApi(host='http://5.63.153.31:5051')

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
