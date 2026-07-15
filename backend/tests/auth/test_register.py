import pytest
from fastapi.testclient import TestClient


class TestRegister:
    REGISTER_PATH = "/api/auth/register"

    def test_register_success(self, client: TestClient):
        """Register a new user returns 201 with tokens."""
        response = client.post(
            self.REGISTER_PATH,
            json={"email": "newuser@example.com", "password": "strongpassword"},
        )
        assert response.status_code == 201, response.text
        body = response.json()
        assert "access_token" in body
        assert "refresh_token" in body
        assert body["token_type"] == "bearer"
        assert body["user"]["email"] == "newuser@example.com"
        assert "id" in body["user"]

    def test_register_duplicate_email(self, client: TestClient):
        """Registering with an existing email returns 409."""
        # First registration
        client.post(
            self.REGISTER_PATH,
            json={"email": "dup@example.com", "password": "strongpassword"},
        )
        # Second registration with same email
        response = client.post(
            self.REGISTER_PATH,
            json={"email": "dup@example.com", "password": "anotherpassword"},
        )
        assert response.status_code == 409, response.text
        body = response.json()
        assert "detail" in body or "error" in body

    @pytest.mark.parametrize(
        "payload, expected_status",
        [
            ({"email": "a@b.com", "password": "short"}, 422),   # password too short (< 8)
            ({"email": "", "password": "longenough123"}, 422),  # empty email
            ({"password": "longenough123"}, 422),                # missing email
            ({"email": "a@b.com"}, 422),                         # missing password
            ({"email": "not-an-email", "password": "longenough"}, 422),  # bad email format
        ],
    )
    def test_register_validation_errors(self, client: TestClient, payload: dict, expected_status: int):
        """Invalid payloads return validation errors."""
        response = client.post(self.REGISTER_PATH, json=payload)
        assert response.status_code == expected_status, response.text