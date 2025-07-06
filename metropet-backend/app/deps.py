#metropet-backend/app/deps.py
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
import jwt

security = HTTPBearer()

JWT_SECRET = os.getenv('JWT_SECRET', 'secret')

def verify_jwt(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

async def get_current_user(credentials=Depends(security)):
    return verify_jwt(credentials.credentials)
