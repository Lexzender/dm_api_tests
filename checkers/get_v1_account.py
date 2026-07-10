from hamcrest import (assert_that)
from assertpy import (
    assert_that,
    soft_assertions
)
from datetime import datetime

from dm_api_account.models.user_envelope import UserRole


class GetV1Account:

    @classmethod
    def check_response_values(
            cls,
            response
            ):
        with soft_assertions():
            assert_that(response.resource.login).is_equal_to('Kostromin_05_07_2026_13_44_28'),
            assert_that(response.resource.online).is_instance_of(datetime),
            assert_that(response.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)
