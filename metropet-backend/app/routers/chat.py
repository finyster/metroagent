# routers/chat.py
@router.post("/v1/chat")
async def chat_endpoint(req: ChatRequest, user=Depends(get_current_user)):
    answer = await orchestrator.chat(req.messages, user_id=user.sub)
    return {"reply": answer}

@router.websocket("/v1/chat/stream")
async def ws_endpoint(websocket: WebSocket, token: str = Query(...)):
    user = verify_jwt(token)
    await websocket.accept()
    async for data in websocket.iter_text():
        req = ChatRequest.parse_raw(data)
        async for chunk in orchestrator.chat_stream(req.messages, user_id=user.sub):
            await websocket.send_json(chunk)
