import json
import os

from typing import List

from sqlalchemy import Column, String, Boolean, Text, Integer

from db import db_session
from models.base import Base


class Game(Base):
    __tablename__ = 'games'

    gameID = Column(Integer, autoincrement=True, primary_key=True)
    key = Column(String(length=255))
    name = Column(String(length=255))
