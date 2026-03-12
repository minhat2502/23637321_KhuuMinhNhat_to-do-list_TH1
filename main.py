from fastapi import FastAPI

app = FastAPI(title="To-Do List API", version="0.1.0")


@app.get("/")
def root():
    return {"message": "Chào mừng đến với To-Do List API!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
