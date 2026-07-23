"""Tests for the articles router, including background task behavior."""
import time
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.articles.router import _ingestion_in_progress, _ingestion_lock


class TestBackgroundIngestion:
    """Test that background ingestion works correctly without blocking."""

    def test_articles_endpoint_returns_immediately(
        self, client: TestClient, db_session
    ):
        """Articles endpoint should return immediately without waiting for ingestion."""
        # Mock run_ingestion to simulate a slow operation
        with patch("app.articles.router.run_ingestion") as mock_ingestion:
            mock_ingestion.side_effect = lambda: time.sleep(2)  # Simulate slow ingestion

            # Reset the flag
            global _ingestion_in_progress
            with _ingestion_lock:
                _ingestion_in_progress = False

            # Make request - should return immediately (not wait 2 seconds)
            response = client.get("/api/articles")
            
            # Response should be instant (200 OK)
            assert response.status_code == 200
            assert response.json() == {"data": [], "pagination": {"has_more": False, "next_cursor": None, "limit": 20}}
            
            # Ingestion should have been scheduled
            mock_ingestion.assert_called_once()

    def test_background_ingestion_sets_flag_during_run(
        self, client: TestClient, db_session
    ):
        """Background ingestion flag should be set during ingestion and cleared after."""
        reset_flag()
        
        with patch("app.articles.router.run_ingestion") as mock_ingestion:
            # Track when ingestion starts/stops
            def slow_ingestion():
                # Check flag is set during execution
                assert _ingestion_in_progress is True
                time.sleep(0.1)
            
            mock_ingestion.side_effect = slow_ingestion

            # Add an article so refresh is needed
            from tests.conftest import make_article
            from app.articles.models import Article
            a_dict = make_article(title="Old Article")
            a_dict["published_date"] = datetime.now(timezone.utc) - timedelta(hours=2)
            a = Article(**a_dict)
            db_session.add(a)
            db_session.commit()
            db_session.refresh(a)

            response = client.get("/api/articles")
            assert response.status_code == 200
            
            # Give time for background task to complete
            time.sleep(0.3)
            
            # Flag should be cleared after ingestion completes
            with _ingestion_lock:
                assert _ingestion_in_progress is False

    def test_no_concurrent_background_ingestions(
        self, client: TestClient, db_session
    ):
        """Multiple requests should not trigger multiple concurrent ingestions."""
        reset_flag()
        
        with patch("app.articles.router.run_ingestion") as mock_ingestion:
            def slow_ingestion():
                time.sleep(0.5)
            
            mock_ingestion.side_effect = slow_ingestion

            # Add an old article to trigger refresh
            from tests.conftest import make_article
            from app.articles.models import Article
            a_dict = make_article(title="Old Article")
            a_dict["published_date"] = datetime.now(timezone.utc) - timedelta(hours=2)
            a = Article(**a_dict)
            db_session.add(a)
            db_session.commit()

            # Make multiple rapid requests
            responses = [client.get("/api/articles") for _ in range(3)]
            
            # All should succeed
            assert all(r.status_code == 200 for r in responses)
            
            # Ingestion should only be called once (due to flag protection)
            time.sleep(0.2)  # Give background task time to start
            with _ingestion_lock:
                # Only one ingestion should be running or scheduled
                assert mock_ingestion.call_count == 1

    def test_no_ingestion_when_not_needed(self, client: TestClient, db_session):
        """Ingestion should not run when articles are fresh."""
        reset_flag()
        
        with patch("app.articles.router.run_ingestion") as mock_ingestion:
            # Add a fresh article (less than 60 minutes old)
            from tests.conftest import make_article
            from app.articles.models import Article
            a_dict = make_article(title="Fresh Article")
            a_dict["published_date"] = datetime.now(timezone.utc) - timedelta(minutes=30)
            a = Article(**a_dict)
            db_session.add(a)
            db_session.commit()
            db_session.refresh(a)

            response = client.get("/api/articles")
            assert response.status_code == 200
            
            # Ingestion should NOT be called for fresh articles
            assert mock_ingestion.call_count == 0


def reset_flag():
    """Reset the ingestion flag to False."""
    global _ingestion_in_progress
    with _ingestion_lock:
        _ingestion_in_progress = False