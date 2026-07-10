import time
from json import loads

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_pasword import ResetPassword
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount


def retrier(
        function
):
    def wrapper(
            *args,
            **kwargs
    ):
        token = None
        count = 0
        while token is None:
            print(f"Попытка получения токена номер {count}!")
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError("Превышено количество попыток получения активационного токена!")
            if token:
                return token
            time.sleep(1)

    return wrapper


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(
            self,
            login: str,
            password: str,
    ):
        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=LoginCredentials(
                login=login,
                password=password
            ),
            validate_response=False
        )

        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        registration = Registration(
            login=login,
            email=email,
            password=password
        )

        response = self.dm_account_api.account_api.post_v1_account(
            registration=registration
        )

        assert response.status_code == 201, f"Пользователь не был создан {response.json()}"

        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f'Токен для пользователя {login}, не был получен'

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response: bool = False
    ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )

        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response
        )
        return response

    def change_email(
            self,
            login: str,
            password: str,
            new_email: str,
            activate: bool = False,
    ):

        change_email = ChangeEmail(
            login=login,
            password=password,
            email=new_email
        )

        self.dm_account_api.account_api.put_v1_account_email(change_email=change_email)

        if activate:
            response = self.mailhog.mailhog_api.get_api_v2_messages()

            assert response.status_code == 200, "Письма не были получены"

            token = self.get_activation_token_by_login(
                login,
                response
            )
            assert token is not None, f'Токен для пользователя {login}, не был получен'

            response = self.dm_account_api.account_api.put_v1_account_token(token=token)

            assert response.status_code == 200, "Пользователь не был активирован"

    def activate_user(
            self,
            login
    ):

        token = self.get_activation_token_by_login(
            login,
        )
        assert token is not None, f'Токен для пользователя {login}, не был получен'

        self.dm_account_api.account_api.put_v1_account_token(token=token)

    def reset_password(
            self,
            login,
            email
    ):
        reset_password = ResetPassword(
            login=login,
            email=email
        )
        response = self.dm_account_api.account_api.post_v1_password(reset_password=reset_password)


    def change_password(
            self,
            login,
            email,
            old_password,
            new_password,
    ):
        self.reset_password(login, email)
        token = self.get_activation_token_by_login(
            login, change_password=True
        )
        assert token is not None, f'Токен для пользователя {login}, не был получен'

        chanhe_password = ChangePassword(
            login=login,
            token=token,
            oldPassword= old_password,
            newPassword= new_password)


        self.dm_account_api.account_api.put_v1_password(chanhe_password=chanhe_password)


    def logout_current_user(
            self
    ):
        response = self.dm_account_api.account_api.delete_v1_account_login()
        assert response.status_code == 204, "Не удалось выйти из текущей УЗ"

    def logout_all_device(
            self
    ):
        response = self.dm_account_api.account_api.delete_v1_account_login_all()
        assert response.status_code == 204, "Не удалось выйти со всех устройств"

    @retrier
    def get_activation_token_by_login(
            self,
            login,
            change_password=False
    ):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"

        for item in response.json()["items"]:
            user_data = loads(item["Content"]["Body"])
            user_login = user_data['Login']
            if user_login == login and change_password == False:
                token = user_data["ConfirmationLinkUrl"].split('/')[-1]

            if user_login == login and change_password == True:
                token = user_data["ConfirmationLinkUri"].split('/')[-1]
            print(
                f"Токен для логина {user_login}:",
                token
            )
            break
        return token
