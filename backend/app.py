import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

import config

load_dotenv()

app = Flask(__name__)
CORS(app)

try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    print("Error: GEMINI_API_KEY not found. Please set it in the .env file.")
    exit()

model = genai.GenerativeModel(config.MODEL_NAME)

@app.route('/api/generate', methods=['POST'])
def generate_marp_content():
    """フロントエンドからお題を受け取り、ツイート文を生成して返すAPI"""
    
    data = request.get_json()
    if not data or 'topic' not in data:
        return jsonify({"error": "No topic provided"}), 400

    topic = data['topic']

    # 新しい設定変数を使ってプロンプトを組み立てる
    prompt_parts = [
        config.PERSONA_PROMPT,
        config.CONTEXT_PROMPT.format(topic=topic),
        config.CONDITIONS_PROMPT,
        config.FINAL_INSTRUCTION
    ]
    prompt = "\n\n".join(prompt_parts)

    try:
        response = model.generate_content(prompt)
        
        # AIが生成したテキストをそのまま返す（Marpヘッダーは結合しない）
        return jsonify({"marp_content": response.text})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to generate content from AI"}), 500

if __name__ == '__main__':
    app.run(debug=True)
