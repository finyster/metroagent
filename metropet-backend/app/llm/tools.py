# metropet-backend/app/llm/tools.py

import httpx
import os
from ..schemas.tools import RouteQuery, FareQuery, StationExitInfo

# --- Configuration for the TDX API ---
API_KEY = os.getenv("METRO_OPEN_API_KEY")
BASE_URL = "https://tdx.transportdata.tw/api/basic/v2"

# --- Tool Functions ---

async def get_route(query: RouteQuery):
    """Fetches travel route and time between two Taipei Metro stations."""
    async with httpx.AsyncClient(timeout=10) as client:
        url = f"{BASE_URL}/Rail/Metro/ODFare/Taipei?$filter=OriginStationID eq '{query.origin}' and DestinationStationID eq '{query.destination}'"
        headers = {"authorization": f"Bearer {API_KEY}"} if API_KEY else {}
        r = await client.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        if not data:
            return {"error": "Could not find a route for the given stations."}
        # Return a custom format for travel time, transfers, etc.
        return {
            "duration_min": data[0].get("TravelTime"),
            "transfers": data[0].get("RouteName", {}).get("Zh_tw"),
            "recommend_board_car": "The middle cars are generally recommended."
        }

async def get_fare(query: FareQuery):
    """Fetches the fare between two Taipei Metro stations."""
    async with httpx.AsyncClient(timeout=10) as client:
        url = f"{BASE_URL}/Rail/Metro/ODFare/Taipei?$filter=OriginStationID eq '{query.origin}' and DestinationStationID eq '{query.destination}'"
        headers = {"authorization": f"Bearer {API_KEY}"} if API_KEY else {}
        r = await client.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        if not data or not data[0].get("Fares"):
            return {"error": "Could not find fare information."}
        return {"fare": data[0]["Fares"][0].get("Price")}

async def get_station_exit(query: StationExitInfo):
    """Fetches information about a specific metro station's exits."""
    async with httpx.AsyncClient(timeout=10) as client:
        # Note: The API endpoint might need adjustment depending on the exact query structure.
        # This is a general structure.
        url = f"{BASE_URL}/Rail/Metro/StationExit/TRTC?$filter=StationID eq '{query.station}'"
        headers = {"authorization": f"Bearer {API_KEY}"} if API_KEY else {}
        r = await client.get(url, headers=headers)
        r.raise_for_status()
        return r.json()

# --- ✨ ADD THIS MAP: Defines all available tools for the orchestrator ---
FUNCTION_MAP = {
    "get_route": (RouteQuery, get_route),
    "get_fare": (FareQuery, get_fare),
    "get_station_exit": (StationExitInfo, get_station_exit),
}