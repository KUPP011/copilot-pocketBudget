# -*- coding: utf-8 -*-
from datetime import date
from repository import add_transaction, totals
from models import TxKind

def test_income_increases_balance(session):
    add_transaction(session, date=date.today(), description="Salary", amount=1000, kind=TxKind.income, category_name=None)
    inc, exp, bal = totals(session)
    assert inc == 1000
    assert exp == 0
    assert bal == 1000

def test_expense_reduces_balance(session):
    add_transaction(session, date=date.today(), description="Groceries", amount=200, kind=TxKind.expense, category_name="Food")
    inc, exp, bal = totals(session)
    assert inc == 0
    assert exp == 200
    assert bal == -200
