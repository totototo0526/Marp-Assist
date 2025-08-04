# backend/database_setup.py

import uuid
import psycopg2
from psycopg2 import sql
from marp_assist.infrastructure.database import db_session

def add_output_type_column():
    """
    templatesテーブルにoutput_typeカラムがなければ追加する。
    """
    with db_session() as conn:
        with conn.cursor() as cur:
            # カラムの存在チェック
            cur.execute("""
                SELECT 1 FROM information_schema.columns
                WHERE table_name='templates' AND column_name='output_type';
            """)
            exists = cur.fetchone()
            if not exists:
                cur.execute("ALTER TABLE templates ADD COLUMN output_type VARCHAR(50);")
                conn.commit()
                print("✅ `output_type`カラムを`templates`テーブルに追加しました。")
            else:
                print("ℹ️ `output_type`カラムは既に存在します。")

def update_existing_templates():
    """
    既存のテンプレートのoutput_typeを'tweet'に設定する。
    """
    with db_session() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE templates SET output_type = 'tweet' WHERE output_type IS NULL;")
            conn.commit()
            print(f"✅ {cur.rowcount}件の既存テンプレートを'tweet'タイプに更新しました。")

def insert_marp_template():
    """
    Marpスライド生成用の新しいテンプレートを挿入する。
    """
    template = {
        "template_id": str(uuid.uuid4()),
        "template_name": "marp_slide_generation",
        "label": "Marpスライド原稿を生成する",
        "persona": "あなたは、熟練したソフトウェアエンジニアであり、複雑な技術的なトピックを、初心者にも理解できるように、明確かつ簡潔なスライドにまとめる専門家です。",
        "output_type": "marp",
        # marpテンプレートでは使わないフィールドはNULLのまま
        "tone_and_manner": None,
        "target_audience": None,
        "keywords": None,
        "banned_words": None,
    }

    with db_session() as conn:
        with conn.cursor() as cur:
            # 既に存在するかチェック
            cur.execute("SELECT 1 FROM templates WHERE template_name = %s;", (template["template_name"],))
            if cur.fetchone():
                print(f"ℹ️ テンプレート '{template['template_name']}' は既に存在します。")
                return

            # 挿入クエリ
            query = sql.SQL("""
                INSERT INTO templates (template_id, template_name, label, persona, output_type, tone_and_manner, target_audience, keywords, banned_words)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """)
            cur.execute(query, (
                template["template_id"],
                template["template_name"],
                template["label"],
                template["persona"],
                template["output_type"],
                template["tone_and_manner"],
                template["target_audience"],
                template["keywords"],
                template["banned_words"]
            ))
            conn.commit()
            print(f"✅ 新しいテンプレート '{template['template_name']}' を追加しました。")

def main():
    """データベースのセットアップ処理を実行する"""
    print("データベースのセットアップを開始します...")
    add_output_type_column()
    update_existing_templates()
    insert_marp_template()
    print("データベースのセットアップが完了しました。")

if __name__ == "__main__":
    # このスクリプトが直接実行された場合にmain()を呼び出す
    # 例: python -m backend.database_setup
    main()
