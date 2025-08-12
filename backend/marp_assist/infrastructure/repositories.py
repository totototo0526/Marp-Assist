# backend/marp_assist/infrastructure/repositories.py

from .database import db_session
from ..domain.models import Template, Theme
from typing import List, Optional

class ThemeRepository:
    def _map_row_to_theme(self, row) -> Theme:
        """DBの行データをThemeオブジェクトにマッピングする"""
        return Theme(
            theme_id=row['theme_id'],
            theme_name=row['theme_name'],
            marp_config=row['marp_config']
        )

    def get_all(self) -> List[Theme]:
        """DBから全てのテーマを取得する"""
        themes = []
        with db_session() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT theme_id, theme_name, marp_config FROM themes")
                rows = cur.fetchall()
                for row in rows:
                    themes.append(self._map_row_to_theme(row))
        return themes

    def find_by_id(self, theme_id: int) -> Optional[Theme]:
        """指定されたIDのテーマを1件取得する"""
        with db_session() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT theme_id, theme_name, marp_config FROM themes WHERE theme_id = %s", (theme_id,))
                row = cur.fetchone()
                if row:
                    return self._map_row_to_theme(row)
        return None

class TemplateRepository:
    def _map_row_to_template(self, row) -> Template:
        """DBの行データ（辞書）をTemplateオブジェクトにマッピングするヘルパー関数"""
        return Template(
            template_id=row['template_id'],
            template_name=row['template_name'],
            label=row['label'],
            output_type=row['output_type'],
            persona=row['persona'],
            tone_and_manner=row['tone_and_manner'],
            target_audience=row['target_audience'],
            keywords=row['keywords'],
            banned_words=row['banned_words'],
            theme_id=row.get('theme_id'), # NULLの場合があるので .get() を使用
            slide_count=row['slide_count'],
            include_hashtags=row['include_hashtags']
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
