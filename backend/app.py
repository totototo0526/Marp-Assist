import os
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# 新しく作成した設定ファイルをインポート
import config

# .envファイルから環境変数を読み込む
load_dotenv()

# app.pyから見て、一つ上の階層にある'frontend'フォルダを指定します。
app = Flask(__name__, static_folder='../frontend', static_url_path='/')

# フロントエンドからのリクエストを許可するための設定

CORS(app)

# Gemini APIキーを設定
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    print("Error: GEMINI_API_KEY not found. Please set it in the .env file.")
    exit()

# モデルをconfigから読み込むように修正
model = genai.GenerativeModel(config.MODEL_NAME)

@app.route('/')
def serve_index():
    """フロントエンドのindex.htmlを配信する"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """frontendフォルダ内の他のファイル（script.jsなど）を配信する"""
    return send_from_directory(app.static_folder, path)

@app.route('/api/generate', methods=['POST'])
def generate_marp_content():
    """フロントエンドからお題を受け取り、Marp原稿を生成して返すAPI"""
    
    data = request.get_json()
    if not data or 'topic' not in data:
        return jsonify({"error": "No topic provided"}), 400

    topic = data['topic']

    # プロンプトをconfigから読み込み、topicを埋め込むように修正
    prompt = config.BASE_PROMPT.format(topic=topic)

    try:
        # Gemini APIを呼び出してコンテンツを生成
        response = model.generate_content(prompt)
        
        # Marpヘッダー設定とAIの生成結果を結合して完全な原稿を作成
        final_marp_content = config.MARP_CONFIG + response.text

        # 結果をJSON形式でフロントエンドに返す
        return jsonify({"marp_content": final_marp_content})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to generate content from AI"}), 500

if __name__ == '__main__':

    # Flaskサーバーをデバッグモードで起動
    # app.run(debug=True)
    # 外部からアクセスできるように host='0.0.0.0' を指定
    app.run(host='0.0.0.0', port=5000, debug=True)

