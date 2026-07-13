
from hamcrest import (
    assert_that,
    all_of,
    has_property,
    starts_with,
    has_properties
)

from checkers.http_checkers import check_status_code_http


def test_get_v1_account(auth_account_helper):
    with check_status_code_http():
        response = auth_account_helper.dm_account_api.account_api.get_v1_account()
        assert_that(response, all_of(
        has_property("resource", has_property("login", starts_with("Kostromin"))),
            has_property(
            "resource", has_properties("roles", ["Guest","Player"])
        )

    ))

def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401,"User must be authenticated"):
        account_helper.dm_account_api.account_api.get_v1_account()