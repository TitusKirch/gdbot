import json
import os

from typing import List

from sqlalchemy import Column, String, Boolean, Text, Integer, ForeignKey, BigInteger

from db import db_session
from models.base import Base


class ApplicationGame(Base):
    __tablename__ = 'applications_games'

    applicationID = Column(BigInteger, ForeignKey(
        "applications.applicationID"), primary_key=True)
    gameID = Column(BigInteger, ForeignKey("games.gameID"), primary_key=True)

    @classmethod
    def getByID(cls, applicationID: int, gameID: int) -> 'Application':
        return db_session.query(Application).filter(Application.applicationID == applicationID).filter(Application.gameID == gameID).first()
