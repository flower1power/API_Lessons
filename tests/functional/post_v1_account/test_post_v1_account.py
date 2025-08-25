from datetime import datetime

import pytest
from faker import Faker

from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account

faker = Faker()
now = datetime.now()
data = now.strftime("%d_%m_%Y_%H_%M_%S")


def test_post_v1_account(account_helper, prepare_user):
    account_helper.register_new_user(login=prepare_user.login, password=prepare_user.password, email=prepare_user.email)
    response = account_helper.user_login(
        login=prepare_user.login,
        password=prepare_user.password,
        validate_response=True
    )
    
    PostV1Account.check_response_values(prepare_user=prepare_user, response=response)


@pytest.mark.parametrize(
    "login, password, email", [
        (
                f"{faker.name().replace(' ', '')}_{data}",
                f"{faker.password(5)}",
                f"{faker.email()}",
        ),
        (
                f"{faker.name().replace(' ', '')}_{data}",
                f"{faker.password(10)}",
                f"{faker.email().replace('@', '')}",
        ),
        (
                f"{faker.name()[0]}",
                f"{faker.password(10)}",
                f"{faker.email()}",
        )

    ]
)
def test_post_v1_account_invalid_credentials(account_helper, login, password, email):
    with check_status_code_http(400, "Validation failed"):
        account_helper.register_new_user(login=login, password=password, email=email)
