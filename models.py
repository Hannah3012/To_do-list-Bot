from datetime import datetime, timezone
from sqlalchemy import Column, Integer, BigInteger,String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column,relationship
from typing import List
from database import Base

class User(Base):
    __tablename__= "users"
    tg_id:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120))
    todos: Mapped[list["Todo"]] = relationship("Todo", back_populates="user", cascade="all, delete-orphan")

class Todo(Base):
    __tablename__ = "todos"
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="CASCADE"))
    task:Mapped[str] = mapped_column(String, nullable=False)
    is_done:Mapped[bool] = mapped_column(default=False, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="todos") 
