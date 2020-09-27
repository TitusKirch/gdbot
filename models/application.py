import json
import os

from typing import List

from sqlalchemy import Column, String, Boolean, Text, Integer

from db import db_session
from models.base import Base


class Application(Base):
    __tablename__ = 'applications'

    applicationID = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(length=255))
