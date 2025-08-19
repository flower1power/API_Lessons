def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.dm_account.account_api.get_v1_account()


def test_get_v1_account(account_helper):
    response = account_helper.dm_account.account_api.get_v1_account(validate_response=False)
    assert response.status_code == 401, 'Удалось получить данные не авторизованного клиента'
