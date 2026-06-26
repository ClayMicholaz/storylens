from sqlalchemy.orm import Session

from app.articles.models import Article

def get_recent_articles(db: Session):
    return (
        db.query(Article)
        .order_by(Article.published_date.desc())
        .limit(50)
        .all()
    )