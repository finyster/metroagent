from pydantic import BaseModel, Field
from typing import List, Literal

class RouteQuery(BaseModel):
    origin: str = Field(..., description="起站英文或中文名稱")
    destination: str = Field(..., description="迄站英文或中文名稱")
    depart_at: str | None = Field(None, description="ISO‑8601 時間字串，若為 None 則預設現在出發")

class FareQuery(BaseModel):
    origin: str
    destination: str
    ticket_type: Literal["single", "return", "daypass"] = "single"

class StationExitInfo(BaseModel):
    station: str
    facility: Literal["elevator", "restroom", "atm", "parking"] | None = None
