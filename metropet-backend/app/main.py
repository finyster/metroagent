# metropet-backend/app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .routers import chat, health

app = FastAPI(title="MetroPet Backend")

# --- 關鍵改動 1 ---
# 為了避免 API 路徑 (如 /v1/chat) 被當成靜態檔案處理，
# 我們必須在掛載靜態檔案「之前」，先註冊所有的 API Router。
app.include_router(chat.router)
app.include_router(health.router)


# --- 關鍵改動 2 ---
# 我們將移除原本的 @app.get("/") 函式，
# 並將靜態檔案的掛載路徑從 "/demo" 改為 "/"。
# 'html=True' 會自動將根目錄的請求導向到 index.html。

BASE_DIR = Path(__file__).resolve().parent
app.mount("/", StaticFiles(directory=BASE_DIR.parent / "web", html=True), name="web-ui")

# 原本的 @app.get("/") 已被上面的 app.mount 取代，因此可以安全地移除。
# def read_root():
#     return {"message": "MetroPet API"}
