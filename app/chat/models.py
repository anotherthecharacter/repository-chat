from sqlalchemy import (
    Boolean, Column, 
    DateTime, ForeignKey,
    Integer, SmallInteger,
    String, UUID,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, nullable=False, unique=True, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    photo_url = Column(String(255))


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    name = Column(String(255), nullable=False)
    status = Column(SmallInteger, nullable=False)
    updated_at = Column(SmallInteger, nullable=False)


class UserChat(Base):
    __tablename__ = "user_chats"

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    user = Column(ForeignKey("users.id"), nullable=False)
    chat = Column(ForeignKey("chats.id"), nullable=False)


class UserMessage(Base):
    __tablename__ = "user_messages"
    
    id = Column(Integer, autoincrement=True, nullable=False, unique=True, primary_key=True)
    sender = Column(ForeignKey("users.id"))
    receiver = Column(ForeignKey("users.id"))
    text = Column(String(255), nullable=False)
    time_delivered = Column(DateTime, default=func.now(), nullable=False)
    time_seen = Column(DateTime, nullable=True)
    is_delivered = Column(Boolean, default=False, nullable=False)
