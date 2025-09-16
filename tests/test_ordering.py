# -*- coding: utf-8 -*-
from datetime import date
from repository import add_transaction, fetch_transactions
from models import TxKind

def test_transactions_newest_first(session):
    add_transaction(session, date=date(2023, 1, 1), description="A", amount=10, kind=TxKind.expense, category_name=None)
    add_transaction(session, date=date(2023, 1, 2), description="B", amount=20, kind=TxKind.expense, category_name=None)
    rows = fetch_transactions(session)
    # rows columns: id, date, description, kind, amount, category, created_at
    assert rows[0][2] == "B"  # description of first row
