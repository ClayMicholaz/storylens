import os
import feedparser
from datetime import datetime, timezone
import time
from dotenv import load_dotenv

from .feed_loader import NEWS_FEEDS


# Load database environment variables just in case we need them later
load_dotenv()

def parse_feed(category, source_name, url):
    print(f"Fetching {source_name} ({category.upper()})...")

    feed = feedparser.parse(url)

    parsed_articles = []

    for entry in feed.entries:
        title = entry.get("title", "")
        link = entry.get("link", "")

        if not title or not link:
            continue

        summary = entry.get("summary", entry.get("description", ""))

        content = entry.get("content", "")

        if isinstance(content, list):
            content = content[0].get("value", "") if content else ""

        if not content:
            content = summary

        published_parsed = entry.get("published_parsed", None)
        if published_parsed:
            published_date = datetime.fromtimestamp(
                time.mktime(published_parsed),
                tz=timezone.utc
            )
        else:
            published_date = datetime.now(timezone.utc)

        article_data = {
            "title": title,
            "url": link,
            "summary": summary,
            "content": content,
            "source": source_name,
            "category": category,
            "published_date": published_date
        }

        parsed_articles.append(article_data)

    print(f"Successfully extracted {len(parsed_articles)} articles from {source_name}.\n")

    return parsed_articles

def run_collector():
    """Loops through all registered categories and pulls articles."""
    all_collected_data = []

    print("Starting StoryLens RSS Collection Engine...")
    print("==================================================")

    for category, feeds in NEWS_FEEDS.items():
        for feed in feeds:
            try:
                articles = parse_feed(category, feed["name"], feed["url"])
                all_collected_data.extend(articles)
            except Exception as e:
                print(f"Error pulling from {feed['name']}: {str(e)}")

    print("==================================================")
    print(f"Engine Finished! Collected {len(all_collected_data)} articles.")

    return all_collected_data

if __name__ == "__main__":
    run_collector()