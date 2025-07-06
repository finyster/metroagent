# metropet-backend/app/llm/orchestrator.py

import os
import json
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
from typing import List, Dict, AsyncGenerator

from .tools import FUNCTION_MAP

# 載入環境變數
load_dotenv()

# --- LLM Client 設定 ---
LLM_MODE = os.getenv("LLM_MODE", "openai")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "breeze-7b-instruct-v1_0:latest")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

# --- 根據 LLM_MODE 初始化 AsyncOpenAI Client (推薦使用異步版本) ---
if LLM_MODE == 'local':
    print(f"🚀 Running in LOCAL mode with Ollama model: {OLLAMA_MODEL}")
    client = AsyncOpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key="ollama",  # Ollama API 金鑰固定為 'ollama'
    )
    model_to_use = OLLAMA_MODEL
else:
    print(f"☁️ Running in OPENAI mode with model: {MODEL_NAME}")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in the .env file")
    client = AsyncOpenAI(api_key=api_key)
    model_to_use = MODEL_NAME


async def chat_stream(messages: List[Dict], user_id: str) -> AsyncGenerator[str, None]:
    """
    統一的流式聊天處理，支援 Tool Calling。
    """
    try:
        # --- 步驟 1: 初次呼叫 LLM，判斷是否需要使用工具 ---
        # 注意：對於本地模型，並非所有模型都完美支援 OpenAI 的 tools 格式，
        # Breeze 和 Llama 3.1 支援度較好。
        tools = [{"type": "function", "function": f.model_json_schema()} for f, _ in FUNCTION_MAP.values()]
        
        first_response = await client.chat.completions.create(
            model=model_to_use,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        response_message = first_response.choices[0].message

        # --- 步驟 2: 檢查 LLM 是否要求執行工具 ---
        tool_calls = response_message.tool_calls
        if not tool_calls:
            # 如果不需要工具，直接以流式方式回傳最終答案
            stream = await client.chat.completions.create(
                model=model_to_use,
                messages=messages + [response_message],
                stream=True
            )
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
            return

        # --- 步驟 3: 如果需要，執行所有工具 ---
        print(f"🛠️ Executing tools: {[call.function.name for call in tool_calls]}")
        tool_outputs = []
        for call in tool_calls:
            fn_name = call.function.name
            args = json.loads(call.function.arguments)
            
            model_cls, func = FUNCTION_MAP[fn_name]
            validated_args = model_cls(**args)
            result = await func(validated_args)
            
            tool_outputs.append({
                "tool_call_id": call.id,
                "role": "tool",
                "name": fn_name,
                "content": json.dumps(result, ensure_ascii=False),
            })

        # --- 步驟 4: 將工具執行結果回傳給 LLM，以流式方式生成最終回答 ---
        messages.append(response_message)
        messages.extend(tool_outputs)

        final_stream = await client.chat.completions.create(
            model=model_to_use,
            messages=messages,
            stream=True
        )
        async for chunk in final_stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    except Exception as e:
        print(f"An error occurred during chat stream: {e}")
        error_message = f"處理請求時發生錯誤：{e}"
        yield error_message