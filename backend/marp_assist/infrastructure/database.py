# backend/marp_assist/infrastructure/database.py

import psycopg2
from contextlib import contextmanager
from config import config

def get_db_connection():
    """データベースへの接続を取得する"""
    conn = psycopg2.connect(config.DATABASE_URL)
    return conn

@contextmanager
def db_session():
    """
    データベースセッションを管理するコンテキストマネージャ。
    'with'構文で使うことで、自動的に接続を確立し、
    処理が終わったらクローズしてくれる。
    """
    conn = None
    try:
        conn = get_db_connection()
        yield conn
    finally:
        if conn is not None:
            conn.close()

print("✅ データベース接続モジュールが準備されました。")
