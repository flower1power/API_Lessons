from faker import Faker


def test_put_v1_account_email(account_helper, prepare_user):
    faker = Faker()
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_email = f'{prepare_user.login}{faker.text(5)}@mail.ru'
    expected_error_text = 'Пользователь не смог авторизоваться'

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.change_email(login=login, password=password, new_email=new_email)

    try:
        account_helper.user_login(login=login, password=password)
    except AssertionError as error:
        assert expected_error_text == str(error), f'Ожидалась ошибка: {expected_error_text}'

    token = account_helper.get_activation_token_by_login(login=login)
    account_helper.activate_user(token=token)
    account_helper.user_login(login=login, password=password)
