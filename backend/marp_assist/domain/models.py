# backend/marp_assist/domain/models.py (修正版)
# データベースのテーブル定義と完全に一致するように、データモデルを修正します。
# __post_init__を追加し、DBの各カラムからconditions属性を自動生成します。

from dataclasses import dataclass, field
from typing import List, Optional
import uuid

@dataclass
class Template:
    """AIへの指示テンプレートを表すドメインモデル"""
    template_id: uuid.UUID
    template_name: str
    output_type: str
    persona: Optional[str]
    tone_and_manner: Optional[str]
    target_audience: Optional[str]
    keywords: Optional[List[str]]
    banned_words: Optional[List[str]]
    conditions: str = field(init=False)

    def __post_init__(self):
        """
        オブジェクト初期化後に、DBの各カラムから
        AIへの指示となるconditions文字列を自動的に組み立てる。
        output_typeに応じて、組み立てる内容を切り替える。
        """
        conditions_parts = []
        if self.output_type == 'tweet':
            conditions_parts.append("# 投稿文の生成条件")
            if self.tone_and_manner:
                conditions_parts.append(f"- 文章のトーン＆マナー: {self.tone_and_manner}")
            if self.target_audience:
                conditions_parts.append(f"- ターゲット読者: {self.target_audience}")
            if self.keywords:
                keyword_str = ", ".join(self.keywords)
                conditions_parts.append(f"- 含めるべきキーワード: {keyword_str}")
            if self.banned_words:
                banned_word_str = ", ".join(self.banned_words)
                conditions_parts.append(f"- 含めてはいけないキーワード: {banned_word_str}")

            # デフォルトの指示を追加
            conditions_parts.append("- 必ず140文字以内で、提案を3案作成してください。")

        elif self.output_type == 'marp':
            conditions_parts.append("# Marpスライド原稿の生成条件")
            conditions_parts.append("- 全体は5〜7枚程度のスライドで構成してください。")
            conditions_parts.append("- 1枚目がタイトル、最後の1枚がまとめのスライドになるようにしてください。")
            conditions_parts.append("- 各スライドは`---`で区切ってください。")
            conditions_parts.append("- スライドのタイトルは`#`、箇条書きは`-`や`*`を使ってMarkdown形式で記述してください。")
            conditions_parts.append("- コードを記述する場合は、適切な言語名を指定したコードブロックを使用してください。例: ```python ... ```")
            if self.keywords:
                keyword_str = ", ".join(self.keywords)
                conditions_parts.append(f"- 含めるべきキーワード: {keyword_str}")

        self.conditions = "\n".join(conditions_parts)

