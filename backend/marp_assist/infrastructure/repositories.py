# backend/marp_assist/infrastructure/repositories.py (修正版)
# データベースのテーブル定義とドメインモデルに完全に一致するように修正します。

from .database import db_session
from ..domain.models import Template
from typing import List, Optional

class TemplateRepository:
    def get_all(self) -> List[Template]:
        """DBから全てのテンプレートを取得する"""
        templates = []
        with db_session() as conn:
            with conn.cursor() as cur:
                # データベースのスキーマに合わせた正しいSQLクエリ
                cur.execute("""
                    SELECT template_id, template_name, persona, tone_and_manner, 
                           target_audience, keywords, banned_words 
                    FROM templates 
                    ORDER BY created_at DESC
                """)
                rows = cur.fetchall()
                for row in rows:
                    # domain/models.pyのTemplateクラスに合わせてインスタンス化
                    templates.append(Template(
                        template_id=row[0],
                        template_name=row[1],
                        persona=row[2],
                        tone_and_manner=row[3],
                        target_audience=row[4],
                        keywords=row[5],
                        banned_words=row[6]
                    ))
        return templates

    def find_by_name(self, name: str) -> Optional[Template]:
        """指定された名前のテンプレートを1件取得する (生成時に使用)"""
        with db_session() as conn:
            with conn.cursor() as cur:
                # こちらもデータベースのスキーマに合わせた正しいSQLクエリ
                cur.execute("""
                    SELECT template_id, template_name, persona, tone_and_manner, 
                           target_audience, keywords, banned_words 
                    FROM templates 
                    WHERE template_name = %s
                """, (name,))
                row = cur.fetchone()
                if row:
                    # domain/models.pyのTemplateクラスに合わせてインスタンス化
                    return Template(
                        template_id=row[0],
                        template_name=row[1],
                        persona=row[2],
                        tone_and_manner=row[3],
                        target_audience=row[4],
                        keywords=row[5],
                        banned_words=row[6]
                    )
        return None

