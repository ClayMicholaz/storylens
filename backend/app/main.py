from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.articles.router import router as articles_router
from app.preferences.router import router as preferences_router

app = FastAPI(title="StoryLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "StoryLens API Running"}

app.include_router(articles_router, prefix="/api", tags=["Articles"])
app.include_router(preferences_router, prefix="/api", tags=["Preferences"])