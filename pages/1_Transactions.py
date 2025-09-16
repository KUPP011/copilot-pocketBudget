# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import date, timedelta
from db import get_session, init_db
from repository import add_transaction, list_categories, fetch_transactions, delete_transaction
from models import TxKind

st.set_page_config(page_title="Transactions | Pocket Budget", page_icon="📒")
st.title("Transactions")

# Ensure tables exist
init_db()

with get_session() as db:
    st.subheader("Add Transaction")

    with st.form("tx_form", clear_on_submit=True):
        tx_date = st.date_input("Date", value=date.today())
        description = st.text_input("Description", placeholder="e.g., Groceries at Tesco")

        col1, col2 = st.columns(2)
        kind_str = col1.radio("Type", options=["expense", "income"], horizontal=True)
        amount = col2.number_input("Amount", min_value=0.0, step=1.0, format="%.2f")

        # categories
        current_cats = [c.name for c in list_categories(db)]
        existing_choice = st.selectbox("Category (existing)", ["— None —"] + current_cats, index=0)
        new_cat = st.text_input("Or create a new category", placeholder="e.g., Food")

        submitted = st.form_submit_button("Add")
        if submitted:
            category_name = None
            if new_cat.strip():
                category_name = new_cat.strip()
            elif existing_choice != "— None —":
                category_name = existing_choice

            add_transaction(
                db,
                date=tx_date,
                description=(description or "").strip() or "(no description)",
                amount=amount,
                kind=TxKind(kind_str),
                category_name=category_name,
            )
            st.success("Transaction added.")
            st.rerun()

    st.subheader("All Transactions")

    st.subheader("Filters")
    with st.container():
        colf1, colf2, colf3, colf4 = st.columns([1,1,1,1])

        # sensible defaults: this month
        today = date.today()
        first_of_month = today.replace(day=1)

        with colf1:
            f_from = st.date_input("From", value=first_of_month, key="from_date")
        with colf2:
            f_to = st.date_input("To", value=today, key="to_date")
        with colf3:
            kinds = ["All", "expense", "income"]
            f_kind = st.selectbox("Type", kinds, index=0)
        with colf4:
            cats = ["All"] + [c.name for c in list_categories(db)]
            f_cat = st.selectbox("Category", options=cats, index=0)

        # normalize filter values
        kind_val = None if f_kind == "All" else TxKind(f_kind)
        cat_val = None if f_cat == "All" else f_cat


    rows = fetch_transactions(
    db,
    date_from=f_from,
    date_to=f_to,
    category_name=cat_val,
    kind=kind_val,
    )
    if rows:
        df = pd.DataFrame(
            rows,
            columns=["id", "date", "description", "type", "amount", "category", "created_at"],
        ).sort_values(by=["date", "id"], ascending=[False, False], ignore_index=True)

        # Display with delete buttons
        st.write("")

        # Show a compact table with delete buttons to the right
        for i, r in df.iterrows():
            c1, c2, c3, c4, c5, c6 = st.columns([1.1, 2.3, 2.6, 1.2, 2.0, 1.1])
            c1.write(r["date"])
            c2.write(r["description"])
            c3.write(r["category"] if pd.notna(r["category"]) else "—")
            c4.write(r["type"])
            c5.write(f"{r['amount']:,.2f}")

            # Delete with confirm
            with c6:
                if st.button("Delete", key=f"del_{int(r['id'])}"):
                    with st.popup(f"Delete Transaction #{int(r['id'])}?"):
                        st.write(f"**{r['date']} • {r['description']} • {r['amount']:,.2f}**")
                        col_ok, col_cancel = st.columns(2)
                        if col_ok.button("Yes, delete", key=f"ok_{int(r['id'])}"):
                            ok = delete_transaction(db, int(r["id"]))
                            if ok:
                                st.success("Deleted.")
                            else:
                                st.error("Could not delete (already removed?).")
                            st.rerun()
                        if col_cancel.button("Cancel", key=f"cancel_{int(r['id'])}"):
                            st.rerun()

        # Optional: also show the DataFrame for bulk view
        with st.expander("Show as table"):
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No transactions found for the selected filters.")
