# Flaskアプリケーションのインスタンスを作成する「Application Factory」と呼ばれる部分です。

from flask import Flask
from flask_cors import CORS

def create_app():
    """Flaskアプリケーションのインスタンスを作成するファクトリ関数"""
    app = Flask(__name__)
    CORS(app)

    with app.app_context():
        # --- この部分を追記 ---
        from .presentation.routes import bp as presentation_bp
        app.register_blueprint(presentation_bp)
        
        print("✅ Presentation Blueprint has been registered.")

    return app
