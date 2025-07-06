from fastapi import FastAPI
from .routers import chat, health

app = FastAPI(title="MetroPet Backend")
app.include_router(chat)
app.include_router(health)

@app.get("/")
def read_root():
    return {"message": "MetroPet API"}
