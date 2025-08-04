# Webリクエストの受付（APIエンドポイント）を担当します。
# Serviceを呼び出し、結果をJSONとして返します。

from flask import Blueprint, request, jsonify
from ..application.services import PromptService

# Blueprintを作成
bp = Blueprint('presentation', __name__, url_prefix='/api')

prompt_service = PromptService()

@bp.route('/templates', methods=['GET'])
def get_templates():
    """利用可能なテンプレートの一覧を返すAPI"""
    try:
        templates = prompt_service.get_all_templates()
        return jsonify(templates)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/generate', methods=['POST'])
def generate():
    """コンテンツを生成するAPI"""
    data = request.get_json()
    if not data or 'topic' not in data or 'template_name' not in data:
        return jsonify({"error": "topicとtemplate_nameは必須です"}), 400

    try:
        content = prompt_service.generate_content(data['topic'], data['template_name'])
        return jsonify({"content": content})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
