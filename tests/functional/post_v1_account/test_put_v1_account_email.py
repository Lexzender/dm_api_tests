def test_change_email(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_email = "new"+email

    account_helper.register_new_user(
        login=login,
        email=email,
        password=password
    )
    response = account_helper.user_login(
        login=login,
        password=password
    )
    assert response.status_code == 200, "Пользователь не смог авторизоваться"
    # сменить email
    account_helper.change_email(
        login=login,
        new_email=new_email,
        password=password
    )

    response = account_helper.user_login(
        login=login,
        password=password
    )
    assert response.status_code == 403, "Пользователь смог авторизоваться"

    account_helper.activate_user(login=login)

    account_helper.user_login(
        login=login,
        password=password
    )
