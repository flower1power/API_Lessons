import structlog
from faker import Faker

from helpers.account_helper import AccountHelper
from rest_client.configuration import Configuration as DmApiConfiguration
from rest_client.configuration import Configuration as MailhogConfiguration
from services.api_dm_account import ApiDmAccount
from services.api_mailhog import ApiMailhog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True)
    ]
)


def test_post_v1_account():
    faker = Faker()
    api_mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025', disable_log=True)
    api_dm_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')

    account = ApiDmAccount(configuration=api_dm_configuration)
    mailhog = ApiMailhog(configuration=api_mailhog_configuration)

    account_helper = AccountHelper(api_dm_account=account, api_mailhog=mailhog)

    login = faker.name().replace(' ', '')
    password = faker.password()
    email = f'{login}@mail.ru'

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
