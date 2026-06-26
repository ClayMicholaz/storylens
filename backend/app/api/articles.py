from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal, get_db
from app.models.article import Article

router = APIRouter()

@router.get("/articles")
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).order_by(Article.published_date.desc()).limit(50).all()

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