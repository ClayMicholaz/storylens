from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.articles.schemas import ArticleResponse
from app.articles.service import get_latest_articles

router = APIRouter()

@router.get("/articles", response_model=list[ArticleResponse])
def get_articles(db: Session = Depends(get_db)):
    return get_latest_articles(db)