# -*- coding: utf-8 -*-
from typing import Optional
from datetime import date, datetime
from enum import Enum
from sqlmodel import SQLModel, Field


class TxKind(str, Enum):
    income = "income"
    expense = "expense"


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    description: str
    amount: float  # store as positive; type captured by 'kind'
    kind: TxKind = Field(default=TxKind.expense)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
