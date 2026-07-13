import allure


@allure.suite("Тесты на проверку метода GET v1/account/account")
class TestDeleteV1Login:
    @allure.title("Проверка выхода из текущей сессии")
    def test_v1_delete_login(self,auth_account_helper):
        auth_account_helper.logout_current_user()

    @allure.title("Проверка выхода из всех сессий")
    def test_v1_delete_account_all(self,auth_account_helper):
        auth_account_helper.logout_all_device()