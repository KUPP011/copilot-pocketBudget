# -*- coding: utf-8 -*-
import streamlit as st
from db import init_db, get_session
from sqlmodel import select
from models import Transaction

st.set_page_config(page_title="Pocket Budget", page_icon="Budget")
st.title("Pocket Budget")

# Initialize the database
init_db()

# Calculate totals
with get_session() as db:
    income = db.exec(select(Transaction).where(Transaction.kind == "income")).all()
    expense = db.exec(select(Transaction).where(Transaction.kind == "expense")).all()
    total_income = sum(t.amount for t in income)
    total_expense = sum(t.amount for t in expense)
    balance = total_income - total_expense

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"{total_income:,.2f}")
col2.metric("Total Expense", f"{total_expense:,.2f}")
col3.metric("Balance", f"{balance:,.2f}")

st.info("Use the sidebar to add transactions (next step).")

st.caption("Quick links:  ➜  Transactions (add data) · Dashboard (charts & CSV)")
