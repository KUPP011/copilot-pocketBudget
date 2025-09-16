# -*- coding: utf-8 -*-
from datetime import date
from repository import add_transaction, list_categories
from models import TxKind

def test_category_auto_create(session):
    add_transaction(session, date=date.today(), description="Dinner", amount=50, kind=TxKind.expense, category_name="Food")
    cats = [c.name for c in list_categories(session)]
    assert "Food" in cats
