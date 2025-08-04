# backend/marp_assist/domain/models.py

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Template:
    """AIへの指示テンプレートを表すドメインモデル"""
    id: int
    name: str
    label: str
    persona: str
    conditions: str
    # 将来の拡張用 (現在は使用しない)
    tone_and_manner: Optional[str] = None
    target_audience: Optional[str] = None
    keywords: Optional[List[str]] = None
    banned_words: Optional[List[str]] = None
