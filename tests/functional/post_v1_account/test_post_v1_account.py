import pytest

from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account



def test_post_v1_account(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(
        login=login,
        email=email,
        password=password
    )
    response = account_helper.user_login(
        login=login,
        password=password,
        validate_response=True
    )

    PostV1Account.check_response_values(response)




@pytest.mark.parametrize("login, password, email", [
    pytest.param("test_user", "short", "test@mail.com", id="Short_password"),
    pytest.param("test_user", "123456789", "testmail.com", id="invalid_email"),
    pytest.param("u", "123456789", "test@mail.com", id="invalid_login")
])
def test_not_create_user_with_invalid_params(
        account_helper,
        prepare_user,
        login,
        password,
        email
):

    with check_status_code_http(400, "Validation failed"):
        account_helper.register_new_user(
            login=login,
            email=email,
            password=password
    )