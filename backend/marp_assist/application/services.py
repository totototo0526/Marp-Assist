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
        """全てのテンプレートの基本情報（名前とラベル）を取得する"""
        templates = self.template_repo.get_all()
        # フロントエンドが必要な情報だけを辞書のリストに変換
        return [{"name": t.template_name, "label": t.label} for t in templates]

    def get_all_themes(self):
        """全てのテーマの基本情報（IDと名前）を取得する"""
        themes = self.theme_repo.get_all()
        # フロントエンドが必要な情報だけを辞書のリストに変換
        return [{"id": t.theme_id, "name": t.theme_name} for t in themes]

    def generate_content(self, topic: str, template_name: str, theme_id: Optional[int] = None) -> str:
        """指定された情報でコンテンツを生成する"""
        target_template = self.template_repo.find_by_name(template_name)

        if not target_template:
            raise ValueError(f"テンプレート '{template_name}' が見つかりません。")

        # プロンプトを組み立てる
        prompt = f"""
{target_template.persona}

# トピック
{topic}

# 条件
{target_template.conditions}

以上の情報に基づき、コンテンツを生成してください。
"""

        # Axon AI Gatewayにリクエストを送信
        try:
            payload = {
                "prompt": prompt,
                "model": config.MODEL_NAME
            }
            response = requests.post(config.AXON_GATEWAY_URL, json=payload, timeout=60)
            response.raise_for_status()  # HTTPエラーがあれば例外を発生させる

            response_data = response.json()
            generated_text = response_data.get("response")

            if not generated_text:
                raise Exception("AIからのレスポンスに 'response' キーが含まれていません。")

        except requests.exceptions.RequestException as e:
            # ネットワークエラーやタイムアウトなど
            print(f"Axon Gatewayとの通信に失敗しました: {e}")
            raise Exception("AIゲートウェイとの通信に失敗しました。")
        except Exception as e:
            # JSONデコードエラーやその他の予期せぬエラー
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
                    # 指定されたtheme_idが見つからない場合、警告を出すかデフォルトに倒す
                    print(f"警告: 指定されたtheme_id {theme_id} が見つかりませんでした。")

            # Marpの場合は、設定情報を先頭に結合する
            return marp_config + generated_text
        else:
            # それ以外の場合は、生成されたテキストをそのまま返す
            return generated_text
