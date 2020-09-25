import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# setup database engine, create tables and setup session
db_engine = create_engine('mysql+mysqldb://' + os.getenv('DATABASE_USER') + ':' + os.getenv('DATABASE_PASSWORD') +
                          '@' + os.getenv('DATABASE_HOST') + '/' + os.getenv('DATABASE_NAME'), encoding="utf8", echo=False)
Session = sessionmaker(bind=db_engine)
db_session = Session()
