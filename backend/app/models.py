from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .db import Base


class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default='open')
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(50))
    content = Column(Text)
    session_id = Column(String(255), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
