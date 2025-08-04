# データベースとの具体的なデータ操作（読み書き）を担当します。
# まずは、全てのテンプレートを取得する機能を実装します。

from .database import db_session
from ..domain.models import Template
from typing import List, Optional

class TemplateRepository:
    def get_all(self) -> List[Template]:
        """DBから全てのテンプレートを取得する"""
        templates = []
        with db_session() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, label, persona, conditions FROM templates ORDER BY id")
                rows = cur.fetchall()
                for row in rows:
                    templates.append(Template(
                        id=row[0],
                        name=row[1],
                        label=row[2],
                        persona=row[3],
                        conditions=row[4]
                    ))
        return templates

    def find_by_name(self, name: str) -> Optional[Template]:
        """指定されたnameに一致するテンプレートをDBから1件取得する"""
        with db_session() as conn:
            with conn.cursor() as cur:
                # SQLインジェクション対策としてプレースホルダを使用
                cur.execute("SELECT id, name, label, persona, conditions FROM templates WHERE name = %s", (name,))
                row = cur.fetchone()
                if row:
                    return Template(
                        id=row[0],
                        name=row[1],
                        label=row[2],
                        persona=row[3],
                        conditions=row[4]
                    )
        return None
