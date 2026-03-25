import requests


class TestDeleteAll:
    def test_delete_all_test(self):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )
        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        delete_all_test_response = requests.delete(
            url="http://localhost:4111/api/admin/users",
            headers={
                "accept": "*/*",
                "Authorization": f"Bearer {token}"
            }
        )

        assert delete_all_test_response.status_code == 200