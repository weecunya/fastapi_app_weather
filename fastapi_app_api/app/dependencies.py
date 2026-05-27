from fastapi import Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from app.models import User
from app.redis_client import redis_client



async def get_current_user(request:Request,db : AsyncSession = Depends(get_db)):
    session_token = request.cookies.get('session_id')
    print(session_token)
    if session_token is None:
        raise HTTPException(status_code=401,detail='not authenticated')
    user_id = await redis_client.get(f'session:{session_token}')
    if not user_id:
        raise HTTPException(status_code=401,detail='session expired')
    user = await db.get(User,int(user_id))
    if not user:
        raise HTTPException(status_code=401,detail='user not found')
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400,detail='Inactive user')
    return current_user

async def rate_limit(request: Request,limit:int = 5, window:int = 0):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"
    current = await redis_client.incr(key)

    if current == 1:
        await redis_client.expire(key,window)
    else:
        current = int(current)
    if current > limit:
        raise HTTPException(status_code=429,detail='too many requests')

