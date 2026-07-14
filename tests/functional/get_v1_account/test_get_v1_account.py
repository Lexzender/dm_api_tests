import allure

from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http

@allure.suite("Тесты на проверку метода GET v1/account/account")
class TestsGetV1Account:
    @allure.title("Получение авторизованного пользователя")
    def test_get_v1_account(self,auth_account_helper):
        with check_status_code_http():
            response = auth_account_helper.dm_account_api.account_api.get_v1_account()
            GetV1Account.check_response_values(response)

    @allure.title("Получение  не авторизованного пользователя")
    def test_get_v1_account_no_auth(self,account_helper):
        with check_status_code_http(401,"User must be authenticated"):
            account_helper.dm_account_api.account_api.get_v1_account()