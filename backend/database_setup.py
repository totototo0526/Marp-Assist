# backend/database_setup.py

import sys
import os

# database_setup.py の親ディレクトリ (backendディレクトリ) のパスを取得
current_dir = os.path.dirname(os.path.abspath(__file__))
# backendディレクトリをPythonの検索パスに追加
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import uuid
import psycopg2
from psycopg2 import sql
from .marp_assist.infrastructure.database import db_session

def create_templates_table():
    """
    'templates'テーブルを定義し、存在しない場合に作成する。
    """
    with db_session() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS templates (
                    template_id VARCHAR(36) PRIMARY KEY,
                    template_name VARCHAR(255) UNIQUE NOT NULL,
                    label VARCHAR(255),
                    persona TEXT,
                    output_type VARCHAR(50),
                    tone_and_manner TEXT,
                    target_audience TEXT,
                    keywords TEXT[],
                    banned_words TEXT[],
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            print("✅ `templates`テーブルが正常に確認・作成されました。")

def create_themes_table():
    """
    'themes'テーブルを定義し、存在しない場合に作成する。
    """
    with db_session() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS themes (
                    theme_id SERIAL PRIMARY KEY,
                    theme_name VARCHAR(255) UNIQUE NOT NULL,
                    marp_config TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            print("✅ `themes`テーブルが正常に確認・作成されました。")

def add_theme_id_to_templates():
    """
    templatesテーブルにtheme_idカラムと外部キー制約を追加する。
    """
    with db_session() as conn:
        with conn.cursor() as cur:
            # カラムの存在チェック
            cur.execute("""
                SELECT 1 FROM information_schema.columns
                WHERE table_name='templates' AND column_name='theme_id';
            """)
            exists = cur.fetchone()
            if not exists:
                cur.execute("ALTER TABLE templates ADD COLUMN theme_id INTEGER;")
                cur.execute("""
                    ALTER TABLE templates
                    ADD CONSTRAINT fk_theme
                    FOREIGN KEY (theme_id)
                    REFERENCES themes(theme_id);
                """)
                conn.commit()
                print("✅ `theme_id`カラムを`templates`テーブルに追加し、外部キーを設定しました。")
            else:
                print("ℹ️ `theme_id`カラムは既に存在します。")

def insert_sample_themes():
    """
    Marpスライド生成用のサンプルテーマを挿入する。
    """
    themes = [
        {
            "theme_name": "standard_blue",
            "marp_config": '''/* @theme standard_blue */

@import 'default';

section {
  background: #f0f7ff;
  color: #003366;
  font-size: 30px;
  padding: 40px;
}

h1, h2 {
  color: #00509e;
  text-align: center;
}

h1 {
  font-size: 2.5em;
}

h2 {
  font-size: 1.8em;
}
'''
        },
        {
            "theme_name": "dark_mode",
            "marp_config": '''/* @theme dark_mode */

@import 'default';

section {
  background: #1a1a1a;
  color: #e0e0e0;
  font-size: 30px;
  padding: 40px;
}

h1, h2 {
  color: #4fc3f7;
  text-align: center;
  border-bottom: 2px solid #4fc3f7;
  padding-bottom: 10px;
}

h1 {
  font-size: 2.8em;
}

h2 {
  font-size: 2.0em;
}

code {
  background: #2c2c2c;
  color: #f0f0f0;
}
'''
        }
    ]

    with db_session() as conn:
        with conn.cursor() as cur:
            for theme in themes:
                # 既に存在するかチェック
                cur.execute("SELECT 1 FROM themes WHERE theme_name = %s;", (theme["theme_name"],))
                if cur.fetchone():
                    print(f"ℹ️ テーマ '{theme['theme_name']}' は既に存在します。")
                    continue

                # 挿入クエリ
                query = sql.SQL("INSERT INTO themes (theme_name, marp_config) VALUES (%s, %s)")
                cur.execute(query, (theme["theme_name"], theme["marp_config"]))
                print(f"✅ 新しいテーマ '{theme['theme_name']}' を追加しました。")
            conn.commit()


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
        "tone_and_manner": None,
        "target_audience": None,
        "keywords": None,
        "banned_words": None,
    }

    with db_session() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM templates WHERE template_name = %s;", (template["template_name"],))
            if cur.fetchone():
                print(f"ℹ️ テンプレート '{template['template_name']}' は既に存在します。")
                return
            query = sql.SQL("""
                INSERT INTO templates (template_id, template_name, label, persona, output_type, tone_and_manner, target_audience, keywords, banned_words)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """)
            cur.execute(query, (
                template["template_id"], template["template_name"], template["label"], template["persona"],
                template["output_type"], template["tone_and_manner"], template["target_audience"],
                template["keywords"], template["banned_words"]
            ))
            conn.commit()
            print(f"✅ 新しいテンプレート '{template['template_name']}' を追加しました。")

def insert_weekend_it_slides_template():
    """
    「週末天気とITあるある」スライド用の新しいテンプレートを挿入する。
    """
    template = {
        "template_id": str(uuid.uuid4()),
        "template_name": "weekend_it_slides",
        "label": "週末天気とITあるあるスライド",
        "persona": "あなたは、IT業界のトレンドや「あるある」ネタに詳しい、親しみやすいウェブライターです。週末の予定に役立つ情報を、面白おかしく伝えるのが得意です。",
        "output_type": "marp",
        "tone_and_manner": "親しみやすく、少しユーモアを交えて",
        "target_audience": "週末の予定を立てたいと考えているITエンジニア",
        "keywords": ["天気", "ITあるある", "週末", "プログラミング"],
        "banned_words": None,
    }
    with db_session() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM templates WHERE template_name = %s;", (template["template_name"],))
            if cur.fetchone():
                print(f"ℹ️ テンプレート '{template['template_name']}' は既に存在します。")
                return
            query = sql.SQL("""
                INSERT INTO templates (template_id, template_name, label, persona, output_type, tone_and_manner, target_audience, keywords, banned_words)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """)
            cur.execute(query, (
                template["template_id"], template["template_name"], template["label"], template["persona"],
                template["output_type"], template["tone_and_manner"], template["target_audience"],
                template["keywords"], template["banned_words"]
            ))
            conn.commit()
            print(f"✅ 新しいテンプレート '{template['template_name']}' を追加しました。")

def main():
    """データベースのセットアップ処理を正しい順序で実行する"""
    print("データベースのセットアップを開始します...")

    # 1. テーブル構造を定義・作成する
    create_templates_table()
    create_themes_table()

    # 2. テーブル構造を更新する
    add_theme_id_to_templates()

    # 3. 初期データを挿入する
    insert_sample_themes()
    insert_marp_template()
    insert_weekend_it_slides_template()

    # 4. 既存のデータを更新する
    update_existing_templates()

    print("✅ データベースのセットアップが正常に完了しました。")

if __name__ == "__main__":
    main()
