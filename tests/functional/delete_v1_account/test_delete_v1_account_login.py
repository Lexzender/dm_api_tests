def test_v1_delete_login(auth_account_helper):
    auth_account_helper.logout_current_user()

def test_v1_delete_account_all(auth_account_helper):
    auth_account_helper.logout_all_device()