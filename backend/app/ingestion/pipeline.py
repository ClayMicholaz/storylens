import os
import hashlib
from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.database.session import SessionLocal
from app.articles.models import Article
from app.ingestion.scraper import run_collector

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


# INSERT USING SQLALCHEMY — bulk fetch + bulk upsert
def insert_articles(session, articles):
    if not articles:
        print("No articles to insert")
        return

    incoming_hashes = [a["article_hash"] for a in articles]

    existing_hashes = {
        row.article_hash
        for row in session.query(Article.article_hash)
        .filter(Article.article_hash.in_(incoming_hashes))
        .all()
    }

    new_articles = [a for a in articles if a["article_hash"] not in existing_hashes]
    skipped = len(articles) - len(new_articles)

    if not new_articles:
        print(f"Inserted: 0")
        print(f"Skipped duplicates: {skipped}")
        return

    rows = [
        {
            "title": a["title"],
            "summary": a.get("summary"),
            "content": a.get("content"),
            "source": a["source"],
            "url": a["url"],
            "category": a["category"],
            "published_date": a["published_date"],
            "article_hash": a["article_hash"],
            "content_hash": a["content_hash"],
        }
        for a in new_articles
    ]

    stmt = pg_insert(Article).values(rows)
    stmt = stmt.on_conflict_do_nothing(index_elements=["article_hash"])
    result = session.execute(stmt)
    session.commit()

    inserted = result.rowcount if result.rowcount is not None else len(rows)
    print(f"Inserted: {inserted}")
    print(f"Skipped duplicates: {skipped + (len(rows) - inserted)}")


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