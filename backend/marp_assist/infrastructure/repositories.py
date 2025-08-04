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
            output_type=row[2],
            persona=row[3],
            tone_and_manner=row[4],
            target_audience=row[5],
            keywords=row[6],
            banned_words=row[7]
        )

    def get_all(self) -> List[Template]:
        """DBから全てのテンプレートを取得する"""
        templates = []
        with db_session() as conn:
            with conn.cursor() as cur:
                # output_type をSELECT文に追加
                cur.execute("""
                    SELECT template_id, template_name, output_type, persona,
                           tone_and_manner, target_audience, keywords, banned_words
                    FROM templates 
                    ORDER BY created_at DESC
                """)
                rows = cur.fetchall()
                for row in rows:
                    # ヘルパー関数を使ってマッピング
                    templates.append(self._map_row_to_template(row))
        return templates

    def find_by_name(self, name: str) -> Optional[Template]:
        """指定された名前のテンプレートを1件取得する (生成時に使用)"""
        with db_session() as conn:
            with conn.cursor() as cur:
                # output_type をSELECT文に追加
                cur.execute("""
                    SELECT template_id, template_name, output_type, persona,
                           tone_and_manner, target_audience, keywords, banned_words
                    FROM templates 
                    WHERE template_name = %s
                """, (name,))
                row = cur.fetchone()
                if row:
                    # ヘルパー関数を使ってマッピング
                    return self._map_row_to_template(row)
        return None

