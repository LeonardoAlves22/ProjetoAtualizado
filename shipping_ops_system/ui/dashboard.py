import streamlit as st
import pandas as pd
import sqlite3


def load_prospects():

    conn = sqlite3.connect("shipping_ops.db")

    df = pd.read_sql_query("""

    SELECT
        v.name,
        v.branch,

        COALESCE(p.prospect_morning,0) as prospect_morning,
        COALESCE(p.prospect_afternoon,0) as prospect_afternoon,

        p.eta,
        p.etb,
        p.etd

    FROM vessels v

    LEFT JOIN prospects p
        ON v.id = p.vessel_id
        AND p.date = DATE('now')

    ORDER BY v.branch, v.name

    """, conn)

    conn.close()

    return df


def load_alerts():

    conn = sqlite3.connect("shipping_ops.db")

    df = pd.read_sql_query("""
    SELECT
        vessels.name,
        alerts.branch,
        alerts.alert_type,
        alerts.created_at
    FROM alerts
    JOIN vessels
    ON alerts.vessel_id = vessels.id
    WHERE alerts.resolved = 0
    """, conn)

    conn.close()

    return df


def render_dashboard():

    st.title("Shipping Operations Monitoring")

    df = load_prospects()

    # Separar filiais
    df_slz = df[df["branch"] == "SLZ"]
    df_belem = df[df["branch"] == "BELEM"]

    # Converter status prospect para visual
    def status_icon(value):
        if value == 1:
            return "🟢 OK"
        else:
            return "🔴 NÃO"

    df_slz["Prospect AM"] = df_slz["prospect_morning"].apply(status_icon)
    df_slz["Prospect PM"] = df_slz["prospect_afternoon"].apply(status_icon)

    df_belem["Prospect AM"] = df_belem["prospect_morning"].apply(status_icon)
    df_belem["Prospect PM"] = df_belem["prospect_afternoon"].apply(status_icon)

    df_slz = df_slz[["name","Prospect AM","Prospect PM","eta","etb","etd"]]
    df_belem = df_belem[["name","Prospect AM","Prospect PM","eta","etb","etd"]]

    st.header("São Luís (SLZ)")

    st.dataframe(
        df_slz,
        use_container_width=True,
        height=500
    )

    st.header("Belém")

    st.dataframe(
        df_belem,
        use_container_width=True,
        height=500
    )