# metropet-backend/app/llm/tools.py

import json
import os
from pathlib import Path
from ..schemas.tools import (
    RouteQuery,
    FareQuery,
    StationExitInfo,
    NextTrainQuery,
    TimetableQuery,
    ServiceHoursQuery,
)

# --- Configuration for the TDX API ---
# The real API is currently unavailable. Instead we load sample data
API_KEY = os.getenv("METRO_OPEN_API_KEY")
BASE_URL = "https://tdx.transportdata.tw/api/basic/v2"

# Load dummy metro data for offline use
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "dummy_metro.json"
with DATA_FILE.open(encoding="utf-8") as f:
    DUMMY_DATA = json.load(f)

# --- Tool Functions ---

async def get_route(query: RouteQuery):
    """Return example travel time information between two stations."""
    key = f"{query.origin}-{query.destination}"
    route = DUMMY_DATA.get("routes", {}).get(key)
    if not route:
        route = {"duration_min": 5, "transfers": 0}
    route.setdefault("recommend_board_car", "中間車廂較為舒適")
    return route

async def get_fare(query: FareQuery):
    """Return example fare between two stations."""
    key = f"{query.origin}-{query.destination}"
    fare = DUMMY_DATA.get("fares", {}).get(key)
    if fare is None:
        fare = 20
    return {"fare": fare}

async def get_station_exit(query: StationExitInfo):
    """Return station exit information from sample data."""
    return DUMMY_DATA.get("station_exits", {}).get(query.station, [])

async def get_next_train(query: NextTrainQuery):
    """Return the next train arrival information."""
    info = DUMMY_DATA.get("next_trains", {}).get(query.station)
    if not info:
        return {"error": "station not found"}
    return info

async def get_timetable(query: TimetableQuery):
    """Return a simple timetable for a station."""
    times = DUMMY_DATA.get("schedules", {}).get(query.station)
    if not times:
        return {"error": "schedule not found"}
    return {"times": times}

async def get_service_hours(query: ServiceHoursQuery):
    """Return first and last train times for a station."""
    hours = DUMMY_DATA.get("service_hours", {}).get(query.station)
    if not hours:
        return {"error": "no data"}
    return hours

# --- ✨ ADD THIS MAP: Defines all available tools for the orchestrator ---
FUNCTION_MAP = {
    "get_route": (RouteQuery, get_route),
    "get_fare": (FareQuery, get_fare),
    "get_station_exit": (StationExitInfo, get_station_exit),
    "get_next_train": (NextTrainQuery, get_next_train),
    "get_timetable": (TimetableQuery, get_timetable),
    "get_service_hours": (ServiceHoursQuery, get_service_hours),
}
