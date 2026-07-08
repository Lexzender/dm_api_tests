from collections import namedtuple
from datetime import datetime

import pytest
import structlog

from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount
from helpers.account_helper import AccountHelper

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)


@pytest.fixture
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(
        host="http://185.185.143.231:5025"
    )
    mailhog_client = MailHogApi(
        configuration=mailhog_configuration
    )
    return mailhog_client


@pytest.fixture
def account_api():
    dm_api_configuration = DmApiConfiguration(
        host="http://185.185.143.231:5051",
        disable_log=False
    )
    account = DMApiAccount(
        configuration=dm_api_configuration
    )
    return account


@pytest.fixture
def account_helper(
        account_api,
        mailhog_api
        ):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)

    return account_helper

@pytest.fixture
def auth_account_helper(mailhog_api):
    dm_api_configuration = DmApiConfiguration(
        host="http://185.185.143.231:5051",
        disable_log=False
    )
    account = DMApiAccount(
        configuration=dm_api_configuration
    )
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.auth_client(login="Kostromin_05_07_2026_13_44_28", password="123456789")

    return account_helper

@pytest.fixture
def prepare_user():
    now = datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S_%f")
    login = f"Kostromin_{data}"
    password = "123456789"
    email = f"{login}@mail.ru"
    User = namedtuple("User", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)
    return user
