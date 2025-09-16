# -*- coding: utf-8 -*-
import os
from sqlmodel import SQLModel, create_engine, Session

DB_PATH = "data/pocket.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)
