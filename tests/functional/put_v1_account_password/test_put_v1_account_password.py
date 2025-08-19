from faker import Faker


def test_put_v1_account_password(account_helper, prepare_user):
    faker = Faker()
    user = prepare_user
    new_password = faker.password(length=10, special_chars=False)

    account_helper.register_new_user(login=user.login, password=user.password, email=user.email)
    account_helper.auth_user(login=user.login, password=user.password)
    account_helper.change_password(
        login=user.login,
        email=user.email,
        old_password=user.password,
        new_password=new_password
    )
    account_helper.auth_user(login=user.login, password=new_password)
