from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger,String, Boolean,DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    text = Column(String, nullable=False)
    is_done = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        status = "✅" if self.is_done else "◻️"
        return f"{status} [{self.id}] {self.text}"
