# -*- coding: utf-8 -*-
import os
from sqlmodel import SQLModel, create_engine, Session

# Single place to build/hold the engine
_engine = None

def get_engine():
    """Lazily build the engine. Uses POCKET_DB_PATH if set (tests),
    otherwise defaults to data/pocket.db."""
    global _engine
    if _engine is None:
        db_path = os.getenv("POCKET_DB_PATH", "data/pocket.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        _engine = create_engine(f"sqlite:///{db_path}", echo=False)
    return _engine

def set_engine_for_tests(engine):
    """Allow tests to inject their own engine."""
    global _engine
    _engine = engine

def init_db():
    SQLModel.metadata.create_all(get_engine())

def get_session() -> Session:
    return Session(get_engine())
