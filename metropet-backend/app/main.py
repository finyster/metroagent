from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .routers import chat, health

app = FastAPI(title="MetroPet Backend")
app.include_router(chat)
app.include_router(health)

BASE_DIR = Path(__file__).resolve().parent
app.mount("/demo", StaticFiles(directory=BASE_DIR.parent / "web", html=True), name="demo")

@app.get("/")
def read_root():
    return {"message": "MetroPet API"}
