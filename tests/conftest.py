import os
from collections import namedtuple
from datetime import datetime
from pathlib import Path

import pytest
from faker import Faker
from swagger_coverage_py.reporter import CoverageReporter
from vyper import v

from helpers.account_helper import AccountHelper
from packages.notifier.bot import send_file
from packages.rest_client.configuration import Configuration
from services.api_dm_account import ApiDmAccount
from services.api_mailhog import ApiMailhog

options = (
    'service.dm_api_account',
    'service.mailhog',
    'user.login',
    'user.password',
    'telegram.chat_id',
    'telegram.token'
)


@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    reporter = CoverageReporter(api_name="dm-api-account", host=v.get('service.dm_api_account'))
    reporter.cleanup_input_files()
    reporter.setup("/swagger/Account/swagger.json")

    yield
    reporter.generate_report()
    send_file()


@pytest.fixture(scope="session", autouse=True)
def set_config(request):
    config = Path(__file__).joinpath("../../").joinpath("config")
    config_name = request.config.getoption("--env")
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f"{option}", request.config.getoption(f"--{option}"))
        os.environ["TELEGRAM_BOT_CHAT_ID"] = v.get('telegram.chat_id')
        os.environ["TELEGRAM_BOT_ACCESS_TOKEN"] = v.get('telegram.token')
        request.config.stash['telegram-notifier-addfields']['enviroment'] = config_name
        request.config.stash['telegram-notifier-addfields']['report'] = 'https://flower1power.github.io/API_Lessons/'


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", help="run dev")

    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)


@pytest.fixture()
def mailhog_client():
    mailhog_configuration = Configuration(host=v.get('service.mailhog'), disable_log=True)
    mailhog_client = ApiMailhog(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture()
def account_client():
    dm_api_configuration = Configuration(host=v.get('service.dm_api_account'), disable_log=False)
    account_client = ApiDmAccount(configuration=dm_api_configuration)
    return account_client


@pytest.fixture()
def account_helper(account_client: ApiDmAccount, mailhog_client: ApiMailhog):
    account_helper = AccountHelper(api_dm_account=account_client, api_mailhog=mailhog_client)
    return account_helper


@pytest.fixture()
def auth_account_helper(mailhog_client: ApiMailhog):
    dm_api_configuration = Configuration(host=v.get('service.dm_api_account'), disable_log=False)
    account_client = ApiDmAccount(configuration=dm_api_configuration)

    account_helper = AccountHelper(api_dm_account=account_client, api_mailhog=mailhog_client)

    login = v.get('user.login')
    password = v.get('user.password')

    account_helper.auth_user(login=login, password=password)

    return account_helper


@pytest.fixture
def prepare_user():
    now = datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S")
    faker = Faker()

    login = faker.name().replace(' ', '') + "_" + data
    password = faker.password(length=10, special_chars=False)
    email = f'{login}@mail.ru'
    User = namedtuple("user", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)

    return user
