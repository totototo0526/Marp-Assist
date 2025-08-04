import os
from flask import Flask, send_from_directory
from flask_cors import CORS

def create_app():
    """Flaskアプリケーションのインスタンスを作成するファクトリ関数"""

    # frontendフォルダの絶対パスを計算し、静的フォルダとして指定します。
    # これにより、どこから実行しても正しくfrontendフォルダを見つけられます。
    static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend'))
    
    app = Flask(__name__, static_folder=static_folder_path)
    CORS(app)

    # APIのBlueprintをアプリケーションに登録します
    with app.app_context():
        from .presentation.routes import bp as presentation_bp
        app.register_blueprint(presentation_bp)
        print("✅ Presentation Blueprint has been registered.")

    # --- フロントエンド配信用のルート ---
    # APIとは別に、Webページ自体を表示するためのルールを定義します。
    
    @app.route('/')
    def serve_index():
        """ルートURL ('/') へのアクセスには、index.htmlを返します。"""
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_static_files(path):
        """
        その他のパス（例: /script.js）へのアクセスには、
        frontendフォルダから対応するファイルを返します。
        """
        if os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            # ファイルが見つからない場合は404エラーを返します。
            return "File not found", 404

    return app
