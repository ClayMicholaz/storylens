from sqlalchemy.orm import Session

from app.articles.repository import get_recent_articles

def get_latest_articles(db: Session):
    articles = get_recent_articles(db)

    return [
        {
            "id": a.id,
            "title": a.title,
            "summary": a.summary,
            "url": a.url,
            "source": a.source,
            "category": a.category,
            "published_date": a.published_date,
        }
        for a in articles
    ]