# backend/marp_assist/infrastructure/repositories.py (修正版)
# データベースのテーブル定義とドメインモデルに完全に一致するように修正します。

from .database import db_session
from ..domain.models import Template
from typing import List, Optional

class TemplateRepository:
    def _map_row_to_template(self, row) -> Template:
        """DBの行データをTemplateオブジェクトにマッピングするヘルパー関数"""
        return Template(
            template_id=row[0],
            template_name=row[1],
            label=row[2],
            output_type=row[3],
            persona=row[4],
            tone_and_manner=row[5],
            target_audience=row[6],
            keywords=row[7],
            banned_words=row[8]
        )

    def get_all(self) -> List[Template]:
        """DBから全てのテンプレートを取得する"""
        templates = []
        # SELECTするカラムのリストを定義してDRYにする
        columns = "template_id, template_name, label, output_type, persona, tone_and_manner, target_audience, keywords, banned_words"
        with db_session() as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT {columns} FROM templates ORDER BY created_at DESC")
                rows = cur.fetchall()
                for row in rows:
                    templates.append(self._map_row_to_template(row))
        return templates

    def find_by_name(self, name: str) -> Optional[Template]:
        """指定された名前のテンプレートを1件取得する (生成時に使用)"""
        # SELECTするカラムのリストを定義してDRYにする
        columns = "template_id, template_name, label, output_type, persona, tone_and_manner, target_audience, keywords, banned_words"
        with db_session() as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT {columns} FROM templates WHERE template_name = %s", (name,))
                row = cur.fetchone()
                if row:
                    return self._map_row_to_template(row)
        return None

