# ビジネスロジック（ユースケース）を担当します。
# リポジトリからデータを取得し、プロンプトを組み立て、AIを呼び出します。

import requests
from typing import Optional
from ..infrastructure.repositories import TemplateRepository, ThemeRepository
from config import config

class PromptService:
    def __init__(self):
        self.template_repo = TemplateRepository()
        self.theme_repo = ThemeRepository()

    def get_all_templates(self):
        """全てのテンプレートの基本情報（名前、ラベル、出力タイプ）を取得する"""
        templates = self.template_repo.get_all()
        # フロントエンドが必要な情報だけを辞書のリストに変換
        return [{"name": t.template_name, "label": t.label, "output_type": t.output_type} for t in templates]

    def get_all_themes(self):
        """全てのテーマの基本情報（IDと名前）を取得する"""
        themes = self.theme_repo.get_all()
        # フロントエンドが必要な情報だけを辞書のリストに変換
        return [{"id": t.theme_id, "name": t.theme_name} for t in themes]

    def generate_content(self, topic: str, template_name: str, theme_id: Optional[int] = None, slide_count: Optional[int] = None, include_hashtags: Optional[bool] = None) -> str:
        """
        指定された情報でコンテンツを生成する。
        プロンプトの組み立てロジックもこのメソッド内で担当する。
        """
        target_template = self.template_repo.find_by_name(template_name)

        if not target_template:
            raise ValueError(f"テンプレート '{template_name}' が見つかりません。")

        # --- プロンプト条件の組み立て ---
        conditions_parts = []
        if target_template.output_type == 'tweet':
            conditions_parts.append("# 投稿文の生成条件")
            if target_template.tone_and_manner:
                conditions_parts.append(f"- 文章のトーン＆マナー: {target_template.tone_and_manner}")
            if target_template.target_audience:
                conditions_parts.append(f"- ターゲット読者: {target_template.target_audience}")
            if target_template.keywords:
                keyword_str = ", ".join(target_template.keywords)
                conditions_parts.append(f"- 含めるべきキーワード: {keyword_str}")
            if target_template.banned_words:
                banned_word_str = ", ".join(target_template.banned_words)
                conditions_parts.append(f"- 含めてはいけないキーワード: {banned_word_str}")
            conditions_parts.append("- 必ず140文字以内で、提案を3案作成してください。")

        elif target_template.output_type == 'marp':
            conditions_parts.append("# Marpスライド原稿の生成条件")

            # スライド枚数を指定（リクエストの値 > DBのデフォルト値）
            final_slide_count = slide_count if slide_count is not None else target_template.slide_count
            conditions_parts.append(f"- スライドを{final_slide_count}枚構成で作成してください。")

            conditions_parts.append("- 1枚目がタイトル、最後の1枚がまとめのスライドになるようにしてください。")
            conditions_parts.append("- 各スライドは`---`で区切ってください。")
            conditions_parts.append("- スライドのタイトルは`#`、箇条書きは`-`や`*`を使ってMarkdown形式で記述してください。")
            conditions_parts.append("- コードを記述する場合は、適切な言語名を指定したコードブロックを使用してください。例: ```python ... ```")
            if target_template.keywords:
                keyword_str = ", ".join(target_template.keywords)
                conditions_parts.append(f"- 含めるべきキーワード: {keyword_str}")

            # ハッシュタグの有無を制御（リクエストの値 > DBのデフォルト値）
            final_include_hashtags = include_hashtags if include_hashtags is not None else target_template.include_hashtags
            if not final_include_hashtags:
                conditions_parts.append("- ハッシュタグは絶対に含めないでください。")

        conditions = "\n".join(conditions_parts)
        # --- プロンプト条件の組み立て完了 ---

        prompt = f"""
{target_template.persona}

# トピック
{topic}

# 条件
{conditions}

以上の情報に基づき、コンテンツを生成してください。
"""

        # Axon AI Gatewayにリクエストを送信
        try:
            payload = {
                "prompt": prompt,
                "model": config.MODEL_NAME
            }
            response = requests.post(config.AXON_GATEWAY_URL, json=payload, timeout=60)
            response.raise_for_status()

            response_data = response.json()
            generated_text = response_data.get("response")

            if not generated_text:
                raise Exception("AIからのレスポンスに 'response' キーが含まれていません。")

        except requests.exceptions.RequestException as e:
            print(f"Axon Gatewayとの通信に失敗しました: {e}")
            raise Exception("AIゲートウェイとの通信に失敗しました。")
        except Exception as e:
            print(f"コンテンツ生成中に予期せぬエラーが発生しました: {e}")
            raise

        # output_typeに応じて後処理を分岐
        if target_template.output_type == 'marp':
            marp_config = ""
            if theme_id:
                theme = self.theme_repo.find_by_id(theme_id)
                if theme:
                    marp_config = theme.marp_config + "\n\n---\n\n"
                else:
                    print(f"警告: 指定されたtheme_id {theme_id} が見つかりませんでした。")
            return marp_config + generated_text
        else:
            return generated_text
