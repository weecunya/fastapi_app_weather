import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings
from app.models import Base

# создание таблиц


connect_args = {"check_same_thread": False}
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True, connect_args=connect_args)

AsyncSessionLocal = async_sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)



async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    print('start')
    new_engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True, connect_args=connect_args)
    async with new_engine.begin() as conn:
        print('Connected')
        await conn.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    asyncio.run(init_db())