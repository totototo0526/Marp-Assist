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
        """
        conditions_parts = ["# 投稿文の生成条件"]
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

        self.conditions = "\n".join(conditions_parts)

