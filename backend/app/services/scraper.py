import os
import feedparser
from datetime import datetime, timezone
import time
from dotenv import load_dotenv

# Load database environment variables just in case we need them later
load_dotenv()

# 🎯 Target Feed Registry broken down by category
NEWS_FEEDS = {
    "tech": [
        {
            "name": "TechCrunch",
            "url": "https://techcrunch.com/feed/"
        },
        {
            "name": "The Verge",
            "url": "https://www.theverge.com/rss/index.xml"
        },
        {
            "name": "Ars Technica",
            "url": "https://feeds.arstechnica.com/arstechnica/index"
        }
    ],
    "world": [
        {
            "name": "BBC World News",
            "url": "http://feeds.bbci.co.uk/news/world/rss.xml"
        },
        {
            "name": "Reuters World",
            "url": "https://www.reutersagency.com/feed/?best-topics=world-news"
        }
    ],
    "science": [
        {
            "name": "NASA Breaking News",
            "url": "https://www.nasa.gov/news-release/feed/"
        },
        {
            "name": "New Scientist",
            "url": "https://www.newscientist.com/feed/home/"
        }
    ]
}

def parse_feed(category, source_name, url):
    """Parses a single RSS feed and normalizes the output format."""
    print(f"📡 Fetching {source_name} ({category.upper()})...")
    
    # feedparser automatically handles downloading and parsing the raw XML
    feed = feedparser.parse(url)
    
    parsed_articles = []
    
    for entry in feed.entries:
        # Extract the title and link safely
        title = entry.get("title", "")
        link = entry.get("link", "")
        
        # Summaries can sometimes be missing or nested under 'summary' or 'description'
        summary = entry.get("summary", entry.get("description", ""))
        
        # RSS dates can be notoriously messy. feedparser tries to convert them into a structured time tuple.
        published_parsed = entry.get("published_parsed", None)
        if published_parsed:
            published_date = datetime.fromtimestamp(time.mktime(published_parsed), tz=timezone.utc)
        else:
            published_date = datetime.now(timezone.utc) # Fallback to current time if feed layout is broken
            
        article_data = {
            "title": title,
            "url": link,
            "summary": summary,
            "content": None,  # Placeholder for potential future content extraction
            "source": source_name,
            "category": category,
            "published_date": published_date
        }
        parsed_articles.append(article_data)
        
    print(f"✅ Successfully extracted {len(parsed_articles)} articles from {source_name}.\n")
    return parsed_articles

def run_collector():
    """Loops through all registered categories and pulls articles."""
    all_collected_data = []
    
    print("🚀 Starting StoryLens RSS Collection Engine...")
    print("==================================================")
    
    for category, feeds in NEWS_FEEDS.items():
        for feed in feeds:
            try:
                articles = parse_feed(category, feed["name"], feed["url"])
                all_collected_data.extend(articles)
            except Exception as e:
                print(f"❌ Error pulling from {feed['name']}: {str(e)}\n")
                
    print("==================================================")
    print(f"🎉 Engine Finished! Collected {len(all_collected_data)} total articles across all channels.")
    
    # Quick visual preview of the first article collected
    if all_collected_data:
        print("\n👀 Quick Sample Preview:")
        sample = all_collected_data[0]
        print(f"   Title:    {sample['title']}")
        print(f"   Source:   [{sample['source'].upper()}] - Category: ({sample['category']})")
        print(f"   Link:     {sample['url']}")
        print(f"   Date:     {sample['published_date']}")

if __name__ == "__main__":
    run_collector()