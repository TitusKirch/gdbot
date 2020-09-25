import json
import os

from typing import List

from sqlalchemy import Column, String, Boolean, Text

from db import db_session
from models.base import Base


class Extension(Base):
    __tablename__ = 'extensions'

    name = Column(String(length=255), primary_key=True)
    isLoaded = Column(Boolean, server_default="0")
    description = Column(Text)
    author = Column(String(length=255), nullable=True)

    def __init__(self, name, is_loaded: bool):
        self.name = name
        self.isLoaded = is_loaded

    def loadMeta(self):
        # try:
        metaPath = 'extensions/meta/' + self.name + '.json'
        if os.path.isfile(metaPath):
            with open(metaPath) as json_file:
                metaData = json.load(json_file)

                if 'description' in metaData:
                    self.description = metaData['description']

                if 'author' in metaData:
                    self.author = metaData['author']
        # except:
        #    pass

    @classmethod
    def get(cls, name: str) -> 'Extension':
        return db_session.query(Extension).filter(Extension.name == name).first()

    @classmethod
    def loaded(cls) -> List['Extension']:
        return db_session.query(Extension).filter(Extension.isLoaded == 1).all()

    @classmethod
    def unloaded(cls) -> List['Extension']:
        return db_session.query(Extension).filter(Extension.isLoaded == 0).all()
