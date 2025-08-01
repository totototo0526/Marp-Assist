# --- アプリケーションの基本設定 ---
MODEL_NAME = 'gemini-1.5-pro-latest'

# --- Marpスライドのデフォルト設定 ---
MARP_CONFIG = """
---
marp: true
theme: default
class: lead
paginate: true
backgroundColor: #e6f0f9
style: |
  section {
    font-family: 'Noto Sans JP', 'Meiryo', sans-serif;
    padding: 2em;
  }
  h1 {
    font-size: 1.8em;
    color: #0a3558;
  }
  p {
    font-size: 1.1em;
    line-height: 1.8;
    color: #1a1a1a;
  }
  ul {
    font-size: 1.1em;
    line-height: 2;
    color: #1a1a1a;
  }
---
"""

# --- AIへの基本プロンプト ---
BASE_PROMPT = """
以下のトピックに関する、X(旧Twitter)投稿用のMarp形式のプレゼンテーションスライドを3枚構成で作成してください。

# トピック
{topic}

# 条件
- 1枚目は、ユーザーの興味を引くキャッチーな見出しと短い導入文にしてください。
- 2枚目は、具体的な内容を箇条書きで分かりやすく説明してください。
- 3枚目は、簡単なまとめと、関連するハッシュタグを3つ付けてください。
- 各スライドは `---` で区切ってください。
- Marpのヘッダー設定（---で囲まれた部分）は出力に含めないでください。
"""
