import os
import hashlib
from dotenv import load_dotenv
from app.database.session import SessionLocal
from app.models.article import Article
from app.services.scraper import run_collector

load_dotenv()

# ARTICLE IDENTITY HASH
def make_article_hash(url: str, title: str) -> str:
    raw = f"{url.strip()}::{title.strip()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# TRUE CONTENT HASH
def make_content_hash(content: str) -> str:
    content = content or ""
    return hashlib.sha256(content.strip().encode("utf-8")).hexdigest()

# NORMALIZATION
def normalize_articles(articles):
    cleaned = []
    for a in articles:
        if not a.get("url") or not a.get("title"):
            continue
        a["article_hash"] = make_article_hash(a["url"], a["title"])
        a["content_hash"] = make_content_hash(a.get("content") or "")
        cleaned.append(a)

    return cleaned


# INSERT USING SQLALCHEMY
def insert_articles(session, articles):
    inserted = 0
    skipped = 0

    for a in articles:
        exists = session.query(Article).filter_by(article_hash=a["article_hash"]).first()
        print("Checking:", a["title"][:40], exists is not None)

        if exists:
            skipped += 1
            continue

        article = Article(
            title=a["title"],
            summary=a.get("summary"),
            content=a.get("content"),
            source=a["source"],
            url=a["url"],
            category=a["category"],
            published_date=a["published_date"],
            article_hash=a["article_hash"],
            content_hash=a["content_hash"],
        )

        session.add(article)
        inserted += 1

    session.commit()

    print(f"Inserted: {inserted}")
    print(f"Skipped duplicates: {skipped}")


# PIPELINE
def run_ingestion():
    print("\nStarting SQLAlchemy News Ingestion")
    print("====================================")

    raw_articles = run_collector()
    print(f"Scraped {len(raw_articles)} articles")

    articles = normalize_articles(raw_articles)
    print(f"Normalized {len(articles)} articles")

    session = SessionLocal()

    try:
        insert_articles(session, articles)
    except Exception as e:
        session.rollback()
        print(f"Database error: {e}")
    finally:
        session.close()

    print("====================================")
    print("Ingestion finished\n")


if __name__ == "__main__":
    run_ingestion()