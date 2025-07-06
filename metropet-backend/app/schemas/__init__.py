# metropet-backend/app/schemas/__init__.py
from .chat import ChatMessage, ChatRequest
from .tools import (
    RouteQuery,
    FareQuery,
    StationExitInfo,
    NextTrainQuery,
    TimetableQuery,
    ServiceHoursQuery,
)

__all__ = [
    'ChatMessage', 'ChatRequest',
    'RouteQuery', 'FareQuery', 'StationExitInfo',
    'NextTrainQuery', 'TimetableQuery', 'ServiceHoursQuery'
]
