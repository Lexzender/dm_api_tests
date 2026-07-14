import allure


@allure.suite("Тесты на проверку метода POST v1/account/login")
class TestPostV1AccountLogin:
    @allure.title("Проверка авторизации нового пользователя")
    def test_post_v1_login(self,account_helper, prepare_user):
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
            password=password
        )

        assert response.status_code == 200, "Пользователь не смог авторизоваться"
