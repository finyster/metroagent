import httpx, os
from ..schemas.tools import RouteQuery, FareQuery, StationExitInfo

API_KEY = os.getenv("METRO_OPEN_API_KEY")
BASE = "https://tdx.transportdata.tw/api/basic/v2"

async def get_route(query: RouteQuery):
    async with httpx.AsyncClient(timeout=5) as client:
        url = f"{BASE}/Rail/Metro/ODFare/Taipei?$filter=OriginStationID eq '{query.origin}' and DestinationStationID eq '{query.destination}'"
        r = await client.get(url, headers={"authorization": f"Bearer {API_KEY}"})
    r.raise_for_status()
    data = r.json()
    # 回傳轉乘節點、行車時間等自訂格式
    return {
        "duration_min": data[0]["TravelTime"],
        "transfers": data[0]["RouteName"]["Zh_tw"],
        "recommend_board_car": "中段第3車廂"
    }

async def get_fare(query: FareQuery):
    async with httpx.AsyncClient(timeout=5) as client:
        url = f"{BASE}/Rail/Metro/ODFare/Taipei?$filter=OriginStationID eq '{query.origin}' and DestinationStationID eq '{query.destination}'"
        r = await client.get(url, headers={"authorization": f"Bearer {API_KEY}"})
    r.raise_for_status()
    data = r.json()
    return {"fare": data[0]["Fares"][0]["Price"]}

async def get_station_exit(query: StationExitInfo):
    async with httpx.AsyncClient(timeout=5) as client:
        url = f"{BASE}/Rail/Metro/StationExit/Taipei/{query.station}"
        r = await client.get(url, headers={"authorization": f"Bearer {API_KEY}"})
    r.raise_for_status()
    data = r.json()
    return data
