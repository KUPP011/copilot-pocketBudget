# -*- coding: utf-8 -*-
from typing import Optional, Iterable
from sqlmodel import select, Session
from models import Category, Transaction, TxKind
import pandas as pd
from datetime import date

def get_or_create_category(db: Session, name: str) -> Category:
    name = name.strip()
    if not name:
        raise ValueError("Empty category name")
    existing = db.exec(select(Category).where(Category.name == name)).first()
    if existing:
        return existing
    cat = Category(name=name)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

def list_categories(db: Session) -> list[Category]:
    return list(db.exec(select(Category).order_by(Category.name)).all())

def add_transaction(
    db: Session,
    *,
    date,
    description: str,
    amount: float,
    kind: TxKind,
    category_name: Optional[str],
) -> Transaction:
    category_id = None
    if category_name:
        category_id = get_or_create_category(db, category_name).id
    tx = Transaction(
        date=date,
        description=description,
        amount=float(amount),
        kind=kind,
        category_id=category_id,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

def fetch_transactions(
    db: Session,
    *,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    category_name: Optional[str] = None,
    kind: Optional[TxKind] = None,
):
    stmt = (
        select(
            Transaction.id,
            Transaction.date,
            Transaction.description,
            Transaction.kind,
            Transaction.amount,
            Category.name.label("category"),
            Transaction.created_at,
        ).join(Category, isouter=True)
    )

    if date_from:
        stmt = stmt.where(Transaction.date >= date_from)
    if date_to:
        stmt = stmt.where(Transaction.date <= date_to)
    if kind:
        stmt = stmt.where(Transaction.kind == kind)
    if category_name:
        # join already present; filter by category name (NULL-safe)
        stmt = stmt.where(Category.name == category_name)

    stmt = stmt.order_by(Transaction.date.desc(), Transaction.id.desc())
    return db.exec(stmt).all()

def df_transactions(db: Session) -> pd.DataFrame:
    """Return transactions as a Pandas DataFrame with category name."""
    rows = (
        db.exec(
            select(
                Transaction.id,
                Transaction.date,
                Transaction.description,
                Transaction.kind,
                Transaction.amount,
                Category.name.label("category"),
                Transaction.created_at,
            ).join(Category, isouter=True)
        )
        .all()
    )
    return pd.DataFrame(
        rows,
        columns=["id", "date", "description", "kind", "amount", "category", "created_at"],
    )

def category_totals(db: Session) -> pd.DataFrame:
    df = df_transactions(db)
    if df.empty:
        return df
    # Only expenses for category breakdown
    exp = df[df["kind"] == TxKind.expense]
    if exp.empty:
        return pd.DataFrame(columns=["category", "amount"])
    out = exp.groupby("category", dropna=False)["amount"].sum().reset_index().fillna("— None —")
    out = out.sort_values("amount", ascending=False, ignore_index=True)
    return out

def monthly_trend(db: Session) -> pd.DataFrame:
    df = df_transactions(db)
    if df.empty:
        return df
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    # income as +, expense as -
    df["signed"] = df.apply(lambda r: r["amount"] if r["kind"] == TxKind.income else -r["amount"], axis=1)
    trend = df.groupby("month")["signed"].sum().reset_index()
    return trend.sort_values("month")

def delete_transaction(db: Session, tx_id: int) -> bool:
    tx = db.get(Transaction, tx_id)
    if not tx:
        return False
    db.delete(tx)
    db.commit()
    return True

def totals(db: Session):
    inc = db.exec(select(Transaction).where(Transaction.kind == TxKind.income)).all()
    exp = db.exec(select(Transaction).where(Transaction.kind == TxKind.expense)).all()
    sum_inc = sum(t.amount for t in inc)
    sum_exp = sum(t.amount for t in exp)
    return sum_inc, sum_exp, sum_inc - sum_exp