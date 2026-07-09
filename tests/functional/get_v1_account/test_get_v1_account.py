from hamcrest import (
    assert_that,
    all_of,
    has_property,
    starts_with,
    has_properties,
    equal_to
)


def test_get_v1_account(auth_account_helper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    assert_that(response, all_of(
        has_property("resource", has_property("login", starts_with("Kostromin"))),
        has_property(
            "resource", has_properties("roles", ["Guest","Player"])
        )

    ))