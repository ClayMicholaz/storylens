import json
import os
from pathlib import Path
from typing import Dict, List

# Default feeds as fallback
DEFAULT_FEEDS = {
    "tech": [
        {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
        {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml"},
        {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index"}
    ],
    "world": [
        {"name": "BBC World News", "url": "http://feeds.bbci.co.uk/news/world/rss.xml"},
        {"name": "Reuters World", "url": "https://www.reutersagency.com/feed/?best-topics=world-news"}
    ],
    "science": [
        {"name": "NASA Breaking News", "url": "https://www.nasa.gov/news-release/feed/"},
        {"name": "New Scientist", "url": "https://www.newscientist.com/feed/home/"}
    ]
}


def validate_feed(feed: dict) -> bool:
    """Validate that a feed entry has required fields."""
    return isinstance(feed, dict) and "name" in feed and "url" in feed


def validate_feeds_config(config: dict) -> bool:
    """Validate the entire feeds configuration structure."""
    if not isinstance(config, dict):
        return False
    for category, feeds in config.items():
        if not isinstance(feeds, list):
            return False
        for feed in feeds:
            if not validate_feed(feed):
                return False
    return True


def load_feeds_config(config_path: str = None) -> Dict[str, List[dict]]:
    """
    Load RSS feeds configuration from JSON file.
    
    Args:
        config_path: Optional path to config file. Defaults to backend/feed_config.json
    
    Returns:
        Dictionary mapping categories to feed lists
    """
    if config_path is None:
        # Default to feed_config.json in backend directory
        config_path = str(Path(__file__).resolve().parents[2] / "feed_config.json")
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if validate_feeds_config(config):
                return config
            else:
                print(f"Warning: Invalid feeds config at {config_path}, using defaults")
        else:
            print(f"Warning: Config file not found at {config_path}, using defaults")
    except json.JSONDecodeError as e:
        print(f"Warning: Error parsing feeds config: {e}, using defaults")
    except Exception as e:
        print(f"Warning: Unexpected error loading feeds config: {e}, using defaults")
    
    return DEFAULT_FEEDS.copy()


# Load feeds at module level for backward compatibility
NEWS_FEEDS = load_feeds_config()