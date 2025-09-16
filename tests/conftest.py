# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import tempfile
import pathlib
import pytest
from sqlmodel import create_engine, SQLModel, Session

import db as dbmod  # your db.py
from db import set_engine_for_tests
from models import Category, Transaction  # ensures tables are registered


@pytest.fixture(scope="function")
def test_db(tmp_path):
    """Each test gets a fresh temporary SQLite DB."""
    tmp_file = tmp_path / "test.db"
    os.environ["POCKET_DB_PATH"] = str(tmp_file)
    engine = create_engine(f"sqlite:///{tmp_file}", echo=False)
    set_engine_for_tests(engine)
    SQLModel.metadata.create_all(engine)
    try:
        yield engine
    finally:
        # cleanup
        if "POCKET_DB_PATH" in os.environ:
            del os.environ["POCKET_DB_PATH"]
        set_engine_for_tests(None)  # reset so app uses default next run


@pytest.fixture()
def session(test_db):
    """Convenience session fixture."""
    with Session(test_db) as s:
        yield s
