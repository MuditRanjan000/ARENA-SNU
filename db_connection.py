import mysql.connector
from mysql.connector import Error, pooling
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "ARENA_SNU")
}

# Cache the connection pool resource globally, not the data
@st.cache_resource
def get_connection_pool():
    return pooling.MySQLConnectionPool(
        pool_name="arena_pool",
        pool_size=10,
        pool_reset_session=True,
        **DB_CONFIG
    )

def get_connection():
    try:
        pool = get_connection_pool()
        return pool.get_connection()
    except Error as e:
        st.error(f"❌ Database connection failed: {e}")
        return None

def run_query(query: str, params: tuple = (), fetch: bool = True):
    conn = get_connection()
    if not conn:
        return [] if fetch else 0

    cursor = None
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
        # Closing cursor prevents "Unread result found" MySQL errors
        if cursor:
            cursor.close()
        # Closing the connection returns it to the pool
        if conn:
            conn.close()

def call_procedure(proc_name: str, args: tuple = ()):
    conn = get_connection()
    if not conn:
        return None, "Connection failed"

    cursor = None
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
        if cursor:
            cursor.close()
        if conn:
            conn.close()