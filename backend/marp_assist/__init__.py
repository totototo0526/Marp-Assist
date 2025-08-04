# Flaskアプリケーションのインスタンスを作成する「Application Factory」と呼ばれる部分です。

from flask import Flask
from flask_cors import CORS

def create_app():
    """Flaskアプリケーションのインスタンスを作成するファクトリ関数"""
    app = Flask(__name__)
    CORS(app) # CORSを有効化

    with app.app_context():
        # --- ここに、各機能（Blueprint）を登録していく ---
        # from .presentation.routes import bp as presentation_bp
        # app.register_blueprint(presentation_bp)
        
        print("Flask App is created.")

    return app
