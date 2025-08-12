# backend/marp_assist/domain/models.py

from dataclasses import dataclass, field
from typing import List, Optional
import uuid

@dataclass
class Theme:
    """CSSテーマを表すドメインモデル"""
    theme_id: int
    theme_name: str
    marp_config: str

@dataclass
class Template:
    """AIへの指示テンプレートを表すドメインモデル"""
    template_id: uuid.UUID
    template_name: str
    label: Optional[str]
    output_type: str
    persona: Optional[str]
    tone_and_manner: Optional[str]
    target_audience: Optional[str]
    keywords: Optional[List[str]]
    banned_words: Optional[List[str]]
    theme_id: Optional[int]
    slide_count: int
    include_hashtags: bool

