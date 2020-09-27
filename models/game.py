import json
import os

from typing import List

from sqlalchemy import Column, String, Boolean, Text, Integer, BigInteger

from db import db_session
from models.base import Base


class Game(Base):
    __tablename__ = 'games'

    gameID = Column(Integer, autoincrement=True, primary_key=True)
    key = Column(String(length=255))
    name = Column(String(length=255))
    roleID = Column(BigInteger, nullable=True)

    @classmethod
    def getByKey(cls, key: str) -> 'Game':
        return db_session.query(Game).filter(Game.key == key).first()

    @classmethod
    def all(cls) -> List['Game']:
        return db_session.query(Game).all()
