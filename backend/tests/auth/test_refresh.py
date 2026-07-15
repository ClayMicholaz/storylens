from uuid import uuid4

from fastapi.testclient import TestClient

from tests.conftest import make_user_dict
from app.users.models import User
from app.core.auth import create_refresh_token


class TestRefresh:
    REFRESH_PATH = "/api/auth/refresh"

    def _create_user_with_tokens(self, db_session, token_version: int = 0):
        """Insert a user and return a refresh token for them."""
        user_data = make_user_dict(email="refresh@example.com", token_version=token_version)
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        refresh_token = create_refresh_token(user.id, user.email, user.token_version)
        return user, refresh_token

    def test_refresh_success(self, client: TestClient, db_session):
        """Valid refresh token returns 200 with a new token pair."""
        _, token = self._create_user_with_tokens(db_session)

        response = client.post(
            self.REFRESH_PATH,
            json={"refresh_token": token},
        )
        assert response.status_code == 200, response.text
        body = response.json()
        assert "access_token" in body
        assert "refresh_token" in body
        assert body["token_type"] == "bearer"
        # Verify we got a new access token (access tokens have different 'type' claim)
        # Decode and verify the access token is valid
        from app.core.auth import decode_token
        access_data = decode_token(body["access_token"])
        assert access_data["type"] == "access"

    def test_refresh_revoked_token(self, client: TestClient, db_session):
        """A refresh token from a user with a bumped token_version is rejected (401)."""
        user, token = self._create_user_with_tokens(db_session, token_version=0)

        # Bump the token_version (simulating password change / logout-all-devices)
        user.token_version = 1
        db_session.commit()

        response = client.post(
            self.REFRESH_PATH,
            json={"refresh_token": token},
        )
        assert response.status_code == 401, response.text

    def test_refresh_invalid_token(self, client: TestClient):
        """A garbage/nonsense token is rejected (401)."""
        response = client.post(
            self.REFRESH_PATH,
            json={"refresh_token": "this-is-not-a-valid-jwt-token"},
        )
        assert response.status_code == 401, response.text

    def test_refresh_access_token_fails(self, client: TestClient, db_session):
        """Using an access token on the refresh endpoint should fail (401)."""
        from app.core.auth import create_access_token

        user, _ = self._create_user_with_tokens(db_session)
        access_token = create_access_token(user.id, user.email, user.token_version)

        response = client.post(
            self.REFRESH_PATH,
            json={"refresh_token": access_token},
        )
        assert response.status_code == 401, response.text

    def test_refresh_deleted_user(self, client: TestClient, db_session):
        """Refresh token from a deleted user (no longer in DB) returns 401."""
        from app.core.auth import create_refresh_token

        # Create a token for a user ID that doesn't exist in the DB
        ghost_token = create_refresh_token(uuid4(), "ghost@example.com", 0)

        response = client.post(
            self.REFRESH_PATH,
            json={"refresh_token": ghost_token},
        )
        assert response.status_code == 401, response.text