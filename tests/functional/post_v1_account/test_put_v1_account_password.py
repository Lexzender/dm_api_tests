def test_put_v1_password(account_helper,prepare_user):

    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_password = "new" + password

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

    account_helper.change_password(
        login=login,
        email=email,
        old_password=password,
        new_password=new_password
    )
    response = account_helper.user_login(
        login=login,
        password=new_password
    )

    assert response.status_code == 200, "Пользователь не смог авторизоваться с новым паролем "
