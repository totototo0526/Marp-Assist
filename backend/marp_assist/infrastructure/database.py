# データベースへの接続と切断を管理する、基本的な仕組みをここに実装します。

import psycopg2
from psycopg2.extras import DictCursor # DictCursorをインポート
from contextlib import contextmanager
from config import config

def get_db_connection():
    """データベースへの接続を取得する"""
    # cursor_factory を指定して、カーソルが辞書を返すように設定
    conn = psycopg2.connect(config.DATABASE_URL, cursor_factory=DictCursor)
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

print("✅ データベース接続モジュールが準備されました。(DictCursor有効)")
