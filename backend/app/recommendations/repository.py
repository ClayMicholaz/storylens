from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.articles.models import Article


def get_similar_articles(
    db: Session,
    article_id: UUID,
    limit: int = 5,
):
    """Get articles most semantically similar to the given article."""

    article = (
        db.query(Article)
        .filter(Article.id == article_id)
        .first()
    )

    if article is None:
        return None, []

    if article.embedding is None:
        return article, []

    cosine_distance = Article.embedding.cosine_distance(article.embedding)

    recommendations = (
        db.query(
            Article,
            (1 - cosine_distance).label("similarity"),
        )
        .filter(
            Article.id != article_id,
            Article.embedding.is_not(None),
        )
        .order_by(cosine_distance)
        .limit(limit)
        .all()
    )

    return article, recommendations