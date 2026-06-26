from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import articles, auth
from app.api.articles import router as articles_router

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

app.include_router(articles_router, prefix="/api")
app.include_router(auth.router, prefix="/api")