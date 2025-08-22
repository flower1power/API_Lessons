from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http


def test_get_v1_account_auth(auth_account_helper):
    with check_status_code_http():
        response = auth_account_helper.dm_account.account_api.get_v1_account()

        GetV1Account.check_response_values(response=response)


def test_get_v1_account(account_helper):
    with check_status_code_http(expected_status_code=401, expected_message='User must be authenticated'):
        account_helper.dm_account.account_api.get_v1_account()
