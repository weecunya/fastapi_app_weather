import secrets

from fastapi import Depends, APIRouter, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import rate_limit
from app.schemas import UserCreate, LoginRequest
from app.utils import hash_password,verify_password
from app.models import User, UserSession
from database import get_db
from app.redis_client import redis_client


router = APIRouter(prefix="/auth",tags=["authentification"])

@router.post('/register',dependencies=[Depends(rate_limit)])
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    if user_data.password != user_data.password2:
        raise HTTPException(status_code=400,detail='Incorrect password')
    existing_user = await db.execute(select(User).where(User.email == user_data.email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400,detail='User already exists')
    user = User(email=user_data.email,hashed_password=hash_password(user_data.password),first_name=user_data.first_name,
last_name=user_data.last_name, is_active=True)
    db.add(user)
    await db.commit()
    return {'message': 'User created successfully'}


@router.post('/login',dependencies=[Depends(rate_limit)])
async def login(request: LoginRequest,response: Response ,db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(User).where(User.email == request.email))
    results = results.scalar_one_or_none()
    if not results:
        raise HTTPException(status_code=401,detail='User does not exist')
    result = verify_password(request.password, results.hashed_password)
    if not result:
        raise HTTPException(status_code=400,detail='Incorrect password')
    session_token = secrets.token_urlsafe(32)
    await redis_client.setex(f"session:{session_token}", 7*24*3600, str(results.id))
    db.add(UserSession(session_token=session_token,user_id=results.id))
    response.set_cookie(key='session_id',value=session_token,httponly=True,secure=False,samesite='lax',max_age=7*24*3600)
    results.is_active = True
    await db.commit()
    return {'status': "logged in"}


