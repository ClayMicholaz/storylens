import pytest
from fastapi.testclient import TestClient

from tests.conftest import make_user_dict
from app.users.models import User


class TestLogin:
    LOGIN_PATH = "/api/auth/login"

    def _register_user(self, db_session, email: str = "test@example.com", password: str = "password123"):
        """Helper to insert a user directly into the DB (bypasses the API)."""
        user_data = make_user_dict(email=email)
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    def test_login_success(self, client: TestClient, db_session):
        """Login with valid credentials returns 200 with tokens."""
        email = "logintest@example.com"
        self._register_user(db_session, email=email)

        response = client.post(
            self.LOGIN_PATH,
            json={"email": email, "password": "password123"},
        )
        assert response.status_code == 200, response.text
        body = response.json()
        assert "access_token" in body
        assert "refresh_token" in body
        assert body["token_type"] == "bearer"
        assert body["user"]["email"] == email

    def test_login_wrong_password(self, client: TestClient, db_session):
        """Login with wrong password returns 401."""
        email = "wrongpw@example.com"
        self._register_user(db_session, email=email)

        response = client.post(
            self.LOGIN_PATH,
            json={"email": email, "password": "wrongpassword"},
        )
        assert response.status_code == 401, response.text

    def test_login_nonexistent_user(self, client: TestClient, db_session):
        """Login with an unregistered email returns 401."""
        response = client.post(
            self.LOGIN_PATH,
            json={"email": "nobody@example.com", "password": "password123"},
        )
        assert response.status_code == 401, response.text

    def test_login_disabled_user(self, client: TestClient, db_session):
        """Login with a disabled user account returns 403."""
        user_data = make_user_dict(email="disabled@example.com", is_active=False)
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()

        response = client.post(
            self.LOGIN_PATH,
            json={"email": "disabled@example.com", "password": "password123"},
        )
        assert response.status_code == 403, response.text

    @pytest.mark.parametrize(
        "payload, expected_status",
        [
            ({"email": "a@b.com", "password": "short"}, 422),   # password too short
            ({"email": "", "password": "longenough123"}, 422),  # empty email
            ({"password": "longenough123"}, 422),                # missing email
            ({"email": "a@b.com"}, 422),                         # missing password
        ],
    )
    def test_login_validation_errors(self, client: TestClient, payload: dict, expected_status: int):
        """Invalid payloads return validation errors."""
        response = client.post(self.LOGIN_PATH, json=payload)
        assert response.status_code == expected_status, response.text