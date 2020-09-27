import json
import os

from typing import List

from sqlalchemy import Column, String, Boolean, Text, Integer, BigInteger

from db import db_session
from models.base import Base


class Application(Base):
    __tablename__ = 'applications'

    applicationID = Column(BigInteger, autoincrement=True, primary_key=True)
    name = Column(String(length=255))

    @classmethod
    def getByID(cls, id: int) -> 'Application':
        return db_session.query(Application).filter(Application.id == id).first()
