import pytest
from payload.json_usercreation import userCreation
from utils.request import request_call
from utils.logger import log_request_response
from utils.excel import get_test_data

call_method = request_call()

# ------------------ DYNAMIC SHEET READS ------------------
headers_create_user, data_create_user = get_test_data("Create_user")
headers_update_password, data_update_password = get_test_data("update_password")
headers_login, data_login = get_test_data("Login_data")


class TestUserCreation:
    name_user = None
    user_password = None

    @pytest.mark.parametrize(",".join(headers_create_user), data_create_user, ids=[f"{row[0]}" for row in data_create_user])
    def test_create_user(self, testcasename, name, username, email, roleId, expected_statuscode):
        body = userCreation.create_user_payload(name, username, email, roleId)
        createuser_response = call_method.test_post_method("v1/user", json=body)
        assert createuser_response.status_code == expected_statuscode
        log_request_response(createuser_response, request_body=body)

        if createuser_response.status_code == 200 and username.lower() == "admin":
            TestUserCreation.name_user = username
            print(f"'admin' user created and assigned to name_user: {TestUserCreation.name_user}")


    def test_get_user(self):
        expected_username = TestUserCreation.name_user
        if expected_username is None:
            print("Expected username is None — create_user may not have run.")
            return

        response = call_method.test_get_method("v1/users")
        assert response.status_code == 200
        log_request_response(response)

        data = response.json().get("detail", {}).get("data", [])
        for user in data:
            print(f"Checking user: {user.get('username')}")
            print(f"Expected username: {expected_username}")
            if user.get("username") == expected_username:
                password = user.get("psswrd")
                if password:
                    print(f"Password found: {password}")
                    TestUserCreation.user_password = password
                    return password

        print("Password not found in the response.")
        return None

    @pytest.mark.parametrize(",".join(headers_update_password), data_update_password, ids=[f"{row[0]}" for row in data_update_password])
    def test_update_password(self, testcasename, username, newpsswrd, expected_statuscode):
        old_password = TestUserCreation.user_password
        if old_password is None:
            pytest.skip("Password not found. Skipping test.")

        body = userCreation.update_password(username, newpsswrd)
        body["oldpsswrd"] = old_password
        response = call_method.test_put_method("v1/psswrd-reset", json=body)
        assert response.status_code == expected_statuscode
        log_request_response(response, request_body=body)

    @pytest.mark.parametrize(",".join(headers_login), data_login, ids=[f"{row[0]}" for row in data_login])
    def test_login(self, testcasename, username, psswrd, expected_statuscode):
        body = userCreation.login_data(username, psswrd)
        response = call_method.test_post_method("v1/login", json=body)
        assert response.status_code == expected_statuscode
        log_request_response(response, request_body=body)

        if response.status_code == 200:
            token = response.json().get("detail", {}).get("data", {}).get("access_token")
            if token:
                with open("utils/Auth.txt", "w", encoding="utf-8") as f:
                    f.write(f"Bearer {token}")
