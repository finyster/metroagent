import openai, json
from .tools import get_route, get_fare, get_station_exit
from ..schemas.tools import RouteQuery, FareQuery, StationExitInfo
FUNCTION_MAP = {
    "get_route": (RouteQuery, get_route),
    "get_fare": (FareQuery, get_fare),
    "get_station_exit": (StationExitInfo, get_station_exit)
}

openai.api_key = os.getenv("OPENAI_API_KEY")
model_name = "gpt-4o-mini"  # 或企業專案限定版本

async def chat(messages: list[dict], user_id: str):
    """主入口：把使用者訊息送 LLM，並按需求呼叫工具。"""
    # 1st  call – 讓 LLM 判斷要不要下 function
    resp = await openai.ChatCompletion.acreate(
        model=model_name,
        messages=messages,
        tools=[{"type": "function", "function": {"name": k, "parameters": v.model_json_schema()}}
               for k, (v, _) in FUNCTION_MAP.items()],
        tool_choice="auto",
        stream=False
    )
    msg = resp.choices[0].message
    if msg.tool_calls:
        # 2nd  call – 實際執行 function 後把結果塞回去
        results = []
        for call in msg.tool_calls:
            fn_name = call.function.name
            args = json.loads(call.function.arguments)
            model_cls, func = FUNCTION_MAP[fn_name]
            validated = model_cls(**args)
            res = await func(validated)
            results.append({"tool_call_id": call.id, "role": "tool", "name": fn_name,
                            "content": json.dumps(res, ensure_ascii=False)})
        # 再送一次 LLM 生成最終 user‑visible 回答
        full_messages = messages + [msg] + results
        final = await openai.ChatCompletion.acreate(
            model=model_name,
            messages=full_messages,
            stream=False
        )
        return final.choices[0].message.content
    else:
        # 無需 function 時就回傳
        return msg.content

async def chat_stream(messages: list[dict], user_id: str):
    resp = await openai.ChatCompletion.acreate(
        model=model_name,
        messages=messages,
        stream=True
    )
    async for chunk in resp:
        yield chunk
