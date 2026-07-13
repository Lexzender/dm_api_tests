from datetime import datetime

import pytest
from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    instance_of,
    has_properties,
    equal_to
)

from checkers.http_checkers import check_status_code_http


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

    assert_that(
        response, all_of(
            has_property("resource", has_property("login", starts_with("Kostromin"))),
            has_property("resource", has_property("registration", instance_of(datetime))),
            has_property(
                "resource", has_properties(
                    {
                        "rating":has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0),
                            }
                        )
                    }
                )
            )
        )
    )



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