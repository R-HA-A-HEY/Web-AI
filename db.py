from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(DIR, ".db")

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR, exist_ok = True)

DB_FILE = os.path.join(DB_DIR, "history.db").replace("\\", "/")
URL =  f"sqlite:///{DB_FILE}"

engine = create_engine(URL, connect_args = {"check_same_thread": False})
session = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()

class History(Base):
    __tablename__ = "History"
    id = Column(Integer, primary_key = True, index = True)
    prompt = Column(Text, nullable = False)
    reply = Column(Text, nullable = False)
    time = Column(DateTime, default = datetime.datetime.utcnow)

Base.metadata.create_all(bind = engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()