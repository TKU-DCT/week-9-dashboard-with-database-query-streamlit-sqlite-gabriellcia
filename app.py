import streamlit as st
import sqlite3
import pandas as pd
import os

DB_NAME = "log.db"

st.set_page_config(page_title="Data Center Dashboard", layout="wide")
st.title("🏗️ Data Center Monitoring Dashboard")

# Cek apakah database ada
if not os.path.exists(DB_NAME):
    st.warning("Database not found. Please run your logger (Week 7) first.")
else:
    # ============================
    # 1. Connect to SQLite
    # ============================
    conn = sqlite3.connect(DB_NAME)

    # ============================
    # 2. Read data from system_log
    # ============================
    query = "SELECT * FROM system_log"
    df = pd.read_sql_query(query, conn)

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    # ============================
    # 3. Filter by Ping_Status
    # ============================
    st.subheader("Filter")

  
    status_list = ["All"]
    if "ping_status" in df.columns:
        status_list += sorted(df["ping_status"].dropna().unique().tolist())

    selected_status = st.selectbox("Filter by Ping Status", status_list)

    if selected_status != "All":
        df = df[df["ping_status"] == selected_status]

    st.write(f"Showing {len(df)} records")

    # ============================
    # 4. Show latest 5 entries
    # ============================
    st.subheader("📌 Latest 5 Log Entries")

    if "timestamp" in df.columns:
        latest_5 = df.sort_values("timestamp", ascending=False).head(5)
    else:
        latest_5 = df.tail(5)

    st.dataframe(latest_5, use_container_width=True)

    # ============================
    # 5. Charts for CPU, Memory, Disk
    #    (sesuaikan nama kolom jika beda)
    # ============================
    st.subheader("📈 System Usage Over Time")


    if "timestamp" in df.columns:
        df_chart = df.sort_values("timestamp").set_index("timestamp")
    else:
        df_chart = df

    # CPU chart
    if "cpu" in df_chart.columns:
        st.subheader("CPU Usage")
        st.line_chart(df_chart["cpu"])

    # Memory chart
    if "memory" in df_chart.columns:
        st.subheader("Memory Usage")
        st.line_chart(df_chart["memory"])

    # Disk chart
    if "disk" in df_chart.columns:
        st.subheader("Disk Usage")
        st.line_chart(df_chart["disk"])

    # ============================
    # 6. Close DB connection
    # ============================
    conn.close()
