
import streamlit as st
import psycopg2


def get_connection():
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        port=st.secrets["postgres"]["port"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"]
    )


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) DEFAULT 'user',
            failed_attempts INTEGER DEFAULT 0,
            is_locked BOOLEAN DEFAULT FALSE
        )
    """)

    cur.execute("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS email VARCHAR(255) UNIQUE
    """)

    cur.execute("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS failed_attempts INTEGER DEFAULT 0
    """)

    cur.execute("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS is_locked BOOLEAN DEFAULT FALSE
    """)

    conn.commit()
    cur.close()
    conn.close()
