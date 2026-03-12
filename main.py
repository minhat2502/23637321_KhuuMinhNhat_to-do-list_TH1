from fastapi import FastAPI
from core.config import settings
from routers.todo_router import router as todo_router
from routers.auth_router import router as auth_router

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
app.include_router(todo_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    return {"message": f"Chào mừng đến với {settings.APP_NAME}!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
