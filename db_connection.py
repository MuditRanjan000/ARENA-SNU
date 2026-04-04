# db_connection.py — ARENA SNU Shared Database Connection
# Uses .env for secure password handling

import mysql.connector
from mysql.connector import Error
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("DB_PASSWORD"),  # pulled from .env
    "database": "ARENA_SNU"
}

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"❌ Database connection failed: {e}")
        return None


def run_query(query: str, params: tuple = (), fetch: bool = True):
    """
    fetch=True  → SELECT → returns list of dicts
    fetch=False → INSERT/UPDATE/DELETE → commits immediately
    """
    conn = get_connection()
    if not conn:
        return [] if fetch else 0

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)

        if fetch:
            return cursor.fetchall()
        else:
            conn.commit()
            return cursor.rowcount

    except Error as e:
        st.error(f"❌ Query error: {e}")
        return [] if fetch else 0

    finally:
        conn.close()


def call_procedure(proc_name: str, args: tuple = ()):
    """Call stored procedure"""
    conn = get_connection()
    if not conn:
        return None, "Connection failed"

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.callproc(proc_name, args)
        conn.commit()

        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())

        return results, None

    except Error as e:
        return None, str(e)

    finally:
        conn.close()