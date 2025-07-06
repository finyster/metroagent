#metropet-backend/app/routers/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get('/healthz')
async def healthcheck():
    return {'status': 'ok'}
