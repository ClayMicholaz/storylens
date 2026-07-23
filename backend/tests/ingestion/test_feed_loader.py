import json
import os
import tempfile
from pathlib import Path

import pytest

from app.ingestion.feed_loader import (
    load_feeds_config,
    validate_feed,
    validate_feeds_config,
    DEFAULT_FEEDS,
)


class TestValidateFeed:
    def test_valid_feed(self):
        """Test that a valid feed passes validation."""
        feed = {"name": "Test Feed", "url": "https://example.com/feed"}
        assert validate_feed(feed) is True

    def test_missing_name(self):
        """Test that feed without name fails."""
        feed = {"url": "https://example.com/feed"}
        assert validate_feed(feed) is False

    def test_missing_url(self):
        """Test that feed without url fails."""
        feed = {"name": "Test Feed"}
        assert validate_feed(feed) is False

    def test_empty_feed(self):
        """Test that empty feed fails."""
        assert validate_feed({}) is False

    def test_non_dict_feed(self):
        """Test that non-dict feed fails."""
        assert validate_feed("not a dict") is False
        assert validate_feed(None) is False


class TestValidateFeedsConfig:
    def test_valid_config(self):
        """Test that valid config passes validation."""
        config = {
            "tech": [{"name": "Test", "url": "https://example.com"}]
        }
        assert validate_feeds_config(config) is True

    def test_invalid_category_feeds(self):
        """Test that non-list feeds for category fails."""
        config = {"tech": "not a list"}
        assert validate_feeds_config(config) is False

    def test_invalid_feed_in_config(self):
        """Test that config with invalid feed fails."""
        config = {
            "tech": [{"url": "https://example.com"}]  # missing name
        }
        assert validate_feeds_config(config) is False

    def test_non_dict_config(self):
        """Test that non-dict config fails."""
        assert validate_feeds_config([]) is False
        assert validate_feeds_config("not a dict") is False


class TestLoadFeedsConfig:
    def test_loads_valid_config(self):
        """Test loading a valid config file."""
        config_content = {
            "tech": [
                {"name": "Custom Feed", "url": "https://custom.com/feed"}
            ]
        }
        
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        ) as f:
            json.dump(config_content, f)
            temp_path = f.name
        
        try:
            result = load_feeds_config(temp_path)
            assert result == config_content
        finally:
            os.unlink(temp_path)

    def test_fallback_on_missing_file(self):
        """Test fallback to defaults when file doesn't exist."""
        result = load_feeds_config("/nonexistent/path/config.json")
        assert result == DEFAULT_FEEDS

    def test_fallback_on_invalid_json(self):
        """Test fallback to defaults on invalid JSON."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        ) as f:
            f.write("not valid json {{{")
            temp_path = f.name
        
        try:
            result = load_feeds_config(temp_path)
            assert result == DEFAULT_FEEDS
        finally:
            os.unlink(temp_path)

    def test_fallback_on_invalid_struct(self):
        """Test fallback to defaults on invalid structure."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        ) as f:
            json.dump({"tech": [{"url": "missing name"}]}, f)
            temp_path = f.name
        
        try:
            result = load_feeds_config(temp_path)
            assert result == DEFAULT_FEEDS
        finally:
            os.unlink(temp_path)