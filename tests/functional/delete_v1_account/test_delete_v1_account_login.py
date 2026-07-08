def test_get_v1_account(auth_account_helper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    assert response.status_code == 200
