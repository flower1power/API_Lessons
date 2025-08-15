from collections import namedtuple
from datetime import datetime

import pytest
from faker import Faker

from helpers.account_helper import AccountHelper
from rest_client.configuration import Configuration
from services.api_dm_account import ApiDmAccount
from services.api_mailhog import ApiMailhog


@pytest.fixture()
def mailhog_client():
    mailhog_configuration = Configuration(host='http://5.63.153.31:5025', disable_log=True)
    mailhog_client = ApiMailhog(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture()
def account_client():
    dm_api_configuration = Configuration(host='http://5.63.153.31:5051', disable_log=False)
    account_client = ApiDmAccount(configuration=dm_api_configuration)
    return account_client


@pytest.fixture()
def account_helper(account_client: ApiDmAccount, mailhog_client: ApiMailhog):
    account_helper = AccountHelper(api_dm_account=account_client, api_mailhog=mailhog_client)
    return account_helper


@pytest.fixture()
def auth_account_helper(mailhog_client: ApiMailhog):
    dm_api_configuration = Configuration(host='http://5.63.153.31:5051', disable_log=False)
    account_client = ApiDmAccount(configuration=dm_api_configuration)

    account_helper = AccountHelper(api_dm_account=account_client, api_mailhog=mailhog_client)

    login = "DarrenDalton12_08_2025_22_43_04"
    email = "DarrenDalton12_08_2025_22_43_04@mail.ru"
    password = "C^Uy3BbI8h"

    account_helper.auth_user(login=login, password=password)

    return account_helper


@pytest.fixture
def prepare_user():
    now = datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S")
    faker = Faker()

    login = faker.name().replace(' ', '') + data
    password = faker.password(length=10, special_chars=False)
    email = f'{login}@mail.ru'
    User = namedtuple("user", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)

    return user
