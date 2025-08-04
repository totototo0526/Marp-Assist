# backend/config.py

import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

class Config:
    """アプリケーションの設定を管理するクラス"""
    
    # --- データベース設定 ---
    # .envファイルからデータベース接続URLを取得
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@host:port/dbname")
    
    # --- AIモデル設定 ---
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = 'gemini-2.5-pro'

# 設定クラスのインスタンスを作成
config = Config()
