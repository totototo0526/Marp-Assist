# Marp Assist

**Subtitle: VectorPost**

AIを活用して、SNS投稿用のMarp形式の下書きを生成するアプリケーション。
詳細は `/docs/01_README.md` を参照してください。

## 起動方法

### バックエンド
1. `cd backend`
2. `pip install -r requirements.txt`
3. `python run.py`

### フロントエンド
1. `frontend/index.html` をブラウザで開く

---

## テンプレートの追加方法

新しいコンテンツ生成テンプレートを追加するには、`templates`テーブルにレコードを直接追加します。
`backend/database_setup.py` 内の `insert_...` 関数を参考に、新しい挿入ロジックを追加するのが推奨です。

### `templates`テーブルのカラム定義

| カラム名 | 型 | 説明 |
|:---|:---|:---|
| `template_id` | `VARCHAR(36)` | テンプレートのユニークID (UUID) |
| `template_name` | `VARCHAR(255)` | テンプレートの内部的な名前。APIで利用する。 |
| `label` | `VARCHAR(255)` | フロントエンドのドロップダウンに表示される、人間可読な名前。 |
| `persona` | `TEXT` | AIに与える役割（ペルソナ）を定義する文章。 |
| `output_type` | `VARCHAR(50)` | 出力形式を区別するタイプ名 (`tweet` または `marp`)。 |
| `tone_and_manner` | `TEXT` | 生成される文章のトーン＆マナーを指定する。 |
| `target_audience` | `TEXT` | 想定する読者層を指定する。 |
| `keywords` | `TEXT[]` | 生成される文章に含めるべきキーワードの配列。 |
| `banned_words` | `TEXT[]` | 生成される文章に含めてはいけないキーワードの配列。 |
| `created_at` | `TIMESTAMP` | 作成日時 |
| `updated_at` | `TIMESTAMP` | 更新日時 |

### INSERT文のサンプル

#### `tweet` タイプのサンプル
```sql
INSERT INTO templates (template_id, template_name, label, persona, output_type, tone_and_manner, target_audience, keywords, banned_words)
VALUES
('your-uuid-here', 'friendly_tweet', '親しみやすいツイート', 'あなたは、最新の技術トレンドに詳しい、フレンドリーなテック系インフルエンサーです。', 'tweet', '明るく、親しみやすいトーンで', '技術に興味がある若者', ARRAY['AI', 'Python'], ARRAY['難しい専門用語']);
```

#### `marp` タイプのサンプル
```sql
INSERT INTO templates (template_id, template_name, label, persona, output_type, tone_and_manner, target_audience, keywords, banned_words)
VALUES
('your-uuid-here-2', 'tech_presentation', '技術解説スライド', 'あなたは、複雑な技術を初心者にも分かりやすく解説する経験豊富なソフトウェアエンジニアです。', 'marp', NULL, NULL, ARRAY['DDD', 'クリーンアーキテクチャ'], NULL);
```
