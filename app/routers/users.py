from fastapi import Depends, APIRouter, Request, Response, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.dependencies import get_current_active_user
from app.redis_client import redis_client
from app.schemas import MessageResponse, UserUpdate
from app.models import User, UserSession
from database import get_db

router = APIRouter(prefix="/users",tags=["users"])

@router.get('/me')
async def me(current_user:User = Depends(get_current_active_user)):
    return current_user

@router.put('/update',response_model=MessageResponse)
async def update_me(user: UserUpdate, current_user:User = Depends(get_current_active_user),db: AsyncSession = Depends(get_db)):
    if current_user.is_active is None and current_user.last_name is None:
        raise HTTPException(status_code=400,detail="Invalid Credentials")
    if current_user.first_name is not None:
        current_user.first_name=user.first_name
    if user.last_name is not None:
        current_user.last_name=user.last_name
    await db.commit()
    return {"message":"User successfully updated"}

@router.delete('/delete',response_model=MessageResponse)
async def delete_me(response: Response,request: Request,current_user:User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    current_user.is_active=False
    session = await db.execute(select(UserSession).where(UserSession.user_id == current_user.id))
    user_sessions = session.scalars().all()
    for user_session in user_sessions:
        await db.delete(user_session)
    await db.commit()
    session_token = request.cookies.get('session_token')
    if session_token:
        await redis_client.delete_cookie(f'session: {session_token}')
    response.delete_cookie('session_id')
    return {"message":"User successfully deleted"}






