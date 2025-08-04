# アプリケーション全体で使われる設定値を管理します。
# ~/Marp-Assist/backend/config.py
import os
from dotenv import load_dotenv

# FLASK_ENV 環境変数に基づいて適切な .env ファイルを読み込む
flask_env = os.getenv('FLASK_ENV', 'development') # デフォルトは development
dotenv_path = os.path.join(os.path.dirname(__file__), f'.env.{flask_env}')
load_dotenv(dotenv_path)

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", 'gemini-2.5-pro') # .env にMODEL_NAMEを追加しても良い

    DEBUG = os.getenv("DEBUG", "False").lower() == 'true'
    TESTING = os.getenv("TESTING", "False").lower() == 'true'

    # Gunicorn がバインドするアドレスとポートも設定として持っておくと便利
    GUNICORN_BIND_ADDRESS = os.getenv("GUNICORN_BIND_ADDRESS", "127.0.0.1:8000")

    MARP_CONFIG = """\
---
marp: true
theme: default
size: 16:9
---

"""

# 設定クラスのインスタンスを作成
config = Config()
