import streamlit as st
import psycopg2
import pandas as pd
from pathlib import Path
from os import environ
from dotenv import load_dotenv

load_dotenv()

QUERIES_DIR = Path(__file__).parent / "queries"


@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=environ["DB_HOST"],
        port=environ["DB_PORT"],
        dbname=environ["DB_NAME"],
        user=environ["DB_USER"],
        password=environ["DB_PASSWORD"],
    )


def run_query(sql_file: str, params: dict) -> pd.DataFrame:
    sql_path = QUERIES_DIR / sql_file
    sql = sql_path.read_text()
    conn = get_connection()
    try:
        return pd.read_sql_query(sql, conn, params=params)
    except Exception:
        conn.rollback()
        raise


def run_raw_query(sql: str, params: dict = None) -> pd.DataFrame:
    conn = get_connection()
    try:
        return pd.read_sql_query(sql, conn, params=params)
    except Exception:
        conn.rollback()
        raise
