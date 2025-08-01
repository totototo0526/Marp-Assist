# --- アプリケーションの基本設定 ---
MODEL_NAME = 'gemini-2.5-pro'

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
---"""


# --- AIへの基本プロンプト（再設計） ---

# 1. AIへの役割設定（ペルソナ）
PERSONA_PROMPT = "あなたはSNSマーケティングの専門家です。"

# 2. 投稿の目的と前提（固定部分）
CONTEXT_PROMPT = """
私はX（旧Twitter）で、スライド画像4枚を添付する投稿をします。
目的は、投稿文を読んで興味を持ち、スライドを見てもらうことです。
添付するスライドのテーマは以下の通りです。

【スライドテーマ】
{topic}
"""

# 3. 投稿文の生成条件（調整可能な部分）
CONDITIONS_PROMPT = """
# 投稿文の生成条件
- 読者に危機感を刺激して、スライドを見たくなるような内容にしてください。
- CTA（フォローやいいねの誘導）は文章に含めないでください。
- ハッシュタグは不要です。
- 明るくなりすぎないように、しかし絵文字は適度に使用してください。
- 必ず140文字以内で、提案を3案作成してください。
"""

# 4. 最終的な指示
FINAL_INSTRUCTION = "以上の全ての前提と条件に基づき、スライドのテーマに沿ったツイート文を3案、作成してください。"
