from pydantic import BaseModel
from typing import List, Literal

class ChatMessage(BaseModel):
    role: Literal['system', 'user', 'assistant']
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
