# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px

from db import get_session, init_db
from repository import df_transactions, category_totals, monthly_trend

st.set_page_config(page_title="Dashboard | Pocket Budget", page_icon="📊")
st.title("Dashboard")

init_db()

with get_session() as db:
    # ===== CSV Export / Import =====
    st.subheader("Data I/O")
    df = df_transactions(db)

    colA, colB = st.columns(2)
    with colA:
        st.caption("Export your data as CSV")
        if df.empty:
            st.warning("No transactions yet to export.")
        else:
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", data=csv, file_name="pocket_budget.csv", mime="text/csv")

    with colB:
        st.caption("Import CSV (columns: date, description, kind, amount, category)")
        uploaded = st.file_uploader("Upload CSV", type=["csv"], accept_multiple_files=False, label_visibility="collapsed")
        if uploaded is not None:
            try:
                up = pd.read_csv(uploaded)
                required = {"date", "description", "kind", "amount"}
                if not required.issubset(set(up.columns)):
                    st.error(f"CSV missing required columns: {required}")
                else:
                    # normalize
                    up["date"] = pd.to_datetime(up["date"]).dt.date
                    up["description"] = up["description"].fillna("(no description)").astype(str)
                    up["kind"] = up["kind"].str.lower().str.strip()
                    up["amount"] = up["amount"].astype(float)
                    up["category"] = up.get("category", None)

                    # insert
                    from repository import add_transaction, get_or_create_category  # local import to avoid cycles
                    from models import TxKind
                    inserted = 0
                    for _, r in up.iterrows():
                        kind = TxKind(r["kind"])
                        catname = r["category"] if pd.notna(r.get("category")) else None
                        add_transaction(
                            db,
                            date=r["date"],
                            description=r["description"],
                            amount=float(r["amount"]),
                            kind=kind,
                            category_name=str(catname) if catname else None,
                        )
                        inserted += 1
                    st.success(f"Imported {inserted} transactions.")
                    st.rerun()
            except Exception as e:
                st.exception(e)

    st.divider()

    # ===== Charts =====
    st.subheader("Charts")

    trend = monthly_trend(db)
    cats = category_totals(db)

    if trend.empty and cats.empty:
        st.info("Add some transactions to see charts.")
    else:
        if not trend.empty:
            fig1 = px.line(trend, x="month", y="signed", markers=True, title="Monthly Net Flow (Income − Expense)")
            st.plotly_chart(fig1, use_container_width=True)
        if not cats.empty:
            fig2 = px.pie(cats, names="category", values="amount", title="Expense Breakdown by Category")
            st.plotly_chart(fig2, use_container_width=True)

    # ===== Raw table (optional quick view) =====
    with st.expander("See raw data"):
        st.dataframe(df if not df.empty else pd.DataFrame(), use_container_width=True, hide_index=True)
