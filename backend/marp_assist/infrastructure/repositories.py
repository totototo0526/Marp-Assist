# backend/marp_assist/infrastructure/repositories.py (修正版)
# データベースのテーブル定義とドメインモデルに完全に一致するように修正します。

from .database import db_session
from ..domain.models import Template
from typing import List, Optional

class TemplateRepository:
    def _map_row_to_template(self, row) -> Template:
        """DBの行データ（辞書）をTemplateオブジェクトにマッピングするヘルパー関数"""
        # DictCursorから受け取ったrowは辞書ライクなオブジェクト
        return Template(
            template_id=row['template_id'],
            template_name=row['template_name'],
            label=row['label'],
            output_type=row['output_type'],
            persona=row['persona'],
            tone_and_manner=row['tone_and_manner'],
            target_audience=row['target_audience'],
            keywords=row['keywords'],
            banned_words=row['banned_words']
        )

    def get_all(self) -> List[Template]:
        """DBから全てのテンプレートを取得する"""
        templates = []
        with db_session() as conn:
            # DictCursorを使うように修正
            with conn.cursor() as cur:
                # SELECT * を使い、モデルで必要な全てのカラムを取得する
                # ORDER BY句で使うcreated_atもこれで取得できる
                cur.execute("SELECT * FROM templates ORDER BY created_at DESC")
                rows = cur.fetchall()
                for row in rows:
                    templates.append(self._map_row_to_template(row))
        return templates

    def find_by_name(self, name: str) -> Optional[Template]:
        """指定された名前のテンプレートを1件取得する (生成時に使用)"""
        with db_session() as conn:
            # DictCursorを使うように修正
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM templates WHERE template_name = %s", (name,))
                row = cur.fetchone()
                if row:
                    return self._map_row_to_template(row)
        return None
