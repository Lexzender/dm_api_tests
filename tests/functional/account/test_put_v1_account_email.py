from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from tests.functional.account.test_post_v1_account import (
    get_activation_token_by_login,
    fake
)


def test_change_email():
    account_api = AccountApi(
        host='http://185.185.143.231:5051'
    )
    login_api = LoginApi(
        host='http://185.185.143.231:5051'
    )
    mailhog_api = MailhogApi(
        'http://185.185.143.231:5025'
    )

    login = fake.user_name()
    password = "123456789"
    email = f'{login}@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password
    }

    response = account_api.post_v1_account(
        json_data=json_data
    )
    print(response.status_code)
    print(response.text)

    assert response.status_code == 201, f"Пользователь не был создан {response.json()}"

    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены"

    token = get_activation_token_by_login(login,response)
    assert token is not None, f'Токен для пользователя {login}, не был получен'

    response = account_api.put_v1_account_token(token=token)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был активирован"

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"

    #сменить email
    json_data = {
        'login': login,
        'password': password,
        'email': f'R{email}'
    }

    response = account_api.put_v1_account_email(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Не удалось сменить email"

    #НЕ успешная авторизация со старыми кредами
    response = login_api.post_v1_account_login(json_data=json_data)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 403, "Пользователь смог авторизоваться"

    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены"

    token = get_activation_token_by_login(login,
                                          response
                                          )
    assert token is not None, f'Токен для пользователя {login}, не был получен'

    response = account_api.put_v1_account_token(token=token)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был активирован"

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"
