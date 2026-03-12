import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import String, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    username: Mapped[str] = mapped_column(String(20))
    hashed_password: Mapped[str] = mapped_column(String(255))
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    tasks: Mapped[list["Task"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    sessions: Mapped[list["AuthSessions"]] = relationship(foreign_keys="AuthSessions.user_id", back_populates="user",
                                                          cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="tasks" )
    task: Mapped[str] = mapped_column(String(50))
    comlite: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class AuthSessions(Base):
    __tablename__ = "auth_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="sessions")
    jti: Mapped[str] = mapped_column(String(50), unique=True)
    revoked: Mapped[bool] = mapped_column(Boolean)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


