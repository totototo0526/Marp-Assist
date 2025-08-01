import os
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__)

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

# モデルを設定
# 今回は高度な生成タスクなので、高性能なProモデルを指定
model = genai.GenerativeModel('gemini-1.5-pro-latest') # または 'gemini-2.5-pro' など最新のモデルを指定

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
    
    # フロントエンドから送信されたJSONデータを取得
    data = request.get_json()
    if not data or 'topic' not in data:
        return jsonify({"error": "No topic provided"}), 400

    topic = data['topic']

    # AIに渡すプロンプト（指示文）を組み立てる
    # このプロンプトを改良することが、生成品質向上の鍵となる
    prompt = f"""
    以下のトピックに関する、X(旧Twitter)投稿用のMarp形式のプレゼンテーションスライドを3枚構成で作成してください。

    # トピック
    {topic}

    # 条件
    - 1枚目は、ユーザーの興味を引くキャッチーな見出しと短い導入文にしてください。
    - 2枚目は、具体的な内容を箇条書きで分かりやすく説明してください。
    - 3枚目は、簡単なまとめと、関連するハッシュタグを3つ付けてください。
    - 各スライドは `---` で区切ってください。
    - 全体はMarpのMarkdown形式で出力してください。
    """

    try:
        # Gemini APIを呼び出してコンテンツを生成
        response = model.generate_content(prompt)
        
        # 結果をJSON形式でフロントエンドに返す
        return jsonify({"marp_content": response.text})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to generate content from AI"}), 500

if __name__ == '__main__':
    # Flaskサーバーをデバッグモードで起動
    # app.run(debug=True)
    # 外部からアクセスできるように host='0.0.0.0' を指定
    app.run(host='0.0.0.0', port=5000, debug=True)
