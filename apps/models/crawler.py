from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from core.database import Base, engine


class Status(PyEnum):
    ON = 1
    OFF = 0


# class CrawlerServer(Base):
#     __tablename__ = "crawl_server"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255), unique=True)
#     ip_address = Column(String(255))
#     port = Column(Integer)
#     status = Column(Integer, default=Status.ON.value)
#     created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CrawlerBot(Base):
    __tablename__ = "crawl_bot"

    class Social(PyEnum):
        YOUTUBE = 1
        FACEBOOK = 2
        TIKTOK = 3

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String(255))
    group_id = Column(String(255), unique=True)
    status = Column(Integer, default=Status.ON.value)
    social_id = Column(Integer, default=Social.YOUTUBE.value)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    server_id = Column(Integer)


Base.metadata.create_all(engine)
