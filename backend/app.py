import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# 新しく作成した設定ファイルをインポート
import config

# .envファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__)
CORS(app)

# Gemini APIキーを設定
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    print("Error: GEMINI_API_KEY not found. Please set it in the .env file.")
    exit()

# モデルをconfigから読み込むように修正
model = genai.GenerativeModel(config.MODEL_NAME)

@app.route('/api/generate', methods=['POST'])
def generate_marp_content():
    """フロントエンドからお題を受け取り、Marp原稿を生成して返すAPI"""
    
    data = request.get_json()
    if not data or 'topic' not in data:
        return jsonify({"error": "No topic provided"}), 400

    topic = data['topic']

    # ツイート文生成用に、4つのプロンプト変数を結合して使用
    prompt = (
        config.PERSONA_PROMPT +
        config.CONTEXT_PROMPT.format(topic=topic) +
        config.CONDITIONS_PROMPT +
        config.FINAL_INSTRUCTION
    )

    try:
        # Gemini APIを呼び出してコンテンツを生成
        response = model.generate_content(prompt)
        
        # AIが生成したツイート文をそのままフロントエンドに返す
        # 【重要】要件に従い、Marpヘッダーの結合処理を削除
        return jsonify({"marp_content": response.text})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to generate content from AI"}), 500

if __name__ == '__main__':
    app.run(debug=True)
