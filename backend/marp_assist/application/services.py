# ビジネスロジック（ユースケース）を担当します。
# リポジトリからデータを取得し、プロンプトを組み立て、AIを呼び出します。

import google.generativeai as genai
from ..infrastructure.repositories import TemplateRepository
from config import config

class PromptService:
    def __init__(self):
        self.template_repo = TemplateRepository()
        # AIモデルの初期化
        try:
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(config.MODEL_NAME)
        except Exception as e:
            print(f"AIモデルの初期化に失敗しました: {e}")
            self.model = None

    def get_all_templates(self):
        """全てのテンプレートの基本情報（名前とラベル）を取得する"""
        templates = self.template_repo.get_all()
        # フロントエンドが必要な情報だけを辞書のリストに変換
        return [{"name": t.name, "label": t.label} for t in templates]

    def generate_content(self, topic: str, template_name: str) -> str:
        """指定されたトピックとテンプレート名でコンテンツを生成する"""
        if not self.model:
            raise Exception("AIモデルが利用できません。")

        templates = self.template_repo.get_all()
        target_template = next((t for t in templates if t.name == template_name), None)

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
        response = self.model.generate_content(prompt)
        return response.text
