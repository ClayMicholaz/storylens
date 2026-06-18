from fastapi import FastAPI
from app.api.articles import router as articles_router

app = FastAPI(title="StoryLens API")

@app.get("/")
def root():
    return {"message": "StoryLens API Running"}

app.include_router(articles_router, prefix="/api")