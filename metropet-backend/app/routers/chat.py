# metropet-backend/app/routers/chat.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from ..schemas.chat import ChatRequest
from ..llm import orchestrator

router = APIRouter()

@router.post('/v1/chat')
async def chat_endpoint(req: ChatRequest):
    """
    這個端點接收聊天訊息，並以流式方式回傳 LLM 的回覆。
    """
    # 直接呼叫更新後的流式 orchestrator
    return StreamingResponse(
        orchestrator.chat_stream(req.messages, user_id="local-user"),
        media_type="text/plain; charset=utf-8"
    )