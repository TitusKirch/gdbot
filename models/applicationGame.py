import json
import os

from typing import List

from sqlalchemy import Column, String, Boolean, Text, Integer, ForeignKey

from db import db_session
from models.base import Base


class ApplicationGame(Base):
    __tablename__ = 'applications_games'

    applicationID = Column(Integer, ForeignKey(
        "applications.applicationID"), primary_key=True)
    gameID = Column(Integer, ForeignKey("games.gameID"), primary_key=True)
