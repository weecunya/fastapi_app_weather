from typing import List

from pydantic import BaseModel
from sqlalchemy import String, Boolean, ForeignKey, DateTime
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email:Mapped[str] = mapped_column(String(255),unique=True, index=True)
    hashed_password:Mapped[str] = mapped_column(String(255))
    first_name:Mapped[str] = mapped_column(String(100))
    last_name:Mapped[str] = mapped_column(String(100))
    is_active:Mapped[bool] = mapped_column(Boolean,default=True)
    created_at:Mapped[datetime] = mapped_column(DateTime,default=datetime.now,onupdate=datetime.now,nullable=True)

class UserSession(Base):
    __tablename__ = "user_sessions"
    id : Mapped[int] = mapped_column(primary_key=True)
    session_token : Mapped[str] = mapped_column(String, unique=True)
    user_id : Mapped[int] = mapped_column(ForeignKey('users.id'))
    is_active : Mapped[bool] = mapped_column(Boolean,default=True)


# creating roles (in development)

# class Role(Base):
#     __tablename__ = "roles"
#     id:Mapped[int] = mapped_column(primary_key=True)
#     name:Mapped[str] = mapped_column(String(255),unique=True)
#
#
# class UserRole(Base):
#     __tablename__ = "user_role"
#     user_id:Mapped[int] = mapped_column(ForeignKey("users.id"),primary_key=True)
#     role_id:Mapped[int] = mapped_column(ForeignKey("roles.id"),primary_key=True)

#
# class UserSession(Base):
#     __tablename__ = 'user_sessions'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     session_id: Mapped[str] = mapped_column(String(255),unique=True)
#     user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
#     expires_at: Mapped[datetime] = mapped_column(DateTime)
#     created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.now)
#     user : Mapped['User'] = relationship(back_populates='sessions')


