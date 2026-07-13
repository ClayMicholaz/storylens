from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.auth.router import router as auth_router
from app.articles.router import router as articles_router
from app.preferences.router import router as preferences_router
from app.users.router import router as users_router

app = FastAPI(title="StoryLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    detail = exc.detail
    body = detail if isinstance(detail, dict) else {"error": "http_error", "message": str(detail)}
    return JSONResponse(status_code=exc.status_code, content={"error": body})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": {"error": "validation_error", "details": exc.errors()}},
    )

@app.get("/")
def root():
    return {"message": "StoryLens API Running"}

@app.get("/debug")
async def debug(request: Request):
    return {
        "path": request.url.path
    }

app.include_router(articles_router, prefix="/api", tags=["Articles"])
app.include_router(auth_router, prefix="/api", tags=["Auth"])
app.include_router(preferences_router, prefix="/api", tags=["Preferences"])
app.include_router(users_router, prefix="/api", tags=["Users"])