from fastapi import FastAPI

app = FastAPI(title="StoryLens API")

@app.get("/")
def root():
    return {"message": "StoryLens API Running"}