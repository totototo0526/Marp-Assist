# Webリクエストの受付（APIエンドポイント）を担当します。
# Serviceを呼び出し、結果をJSONとして返します。
import requests
import io
from flask import Blueprint, request, jsonify, send_file
from ..application.services import PromptService
from config import config


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

@bp.route('/download_pdf', methods=['POST'])
def download_pdf():
    """MarkdownをPDFに変換してダウンロードさせるAPI"""
    data = request.get_json()
    if not data or 'markdown' not in data:
        return jsonify({"error": "markdown content is required"}), 400

    markdown_content = data['markdown']

    try:
        # marp-apiサービスにリクエストを送信
        response = requests.post(
            config.MARP_API_URL,
            json={'markdown': markdown_content},
            timeout=30 # タイムアウトを30秒に設定
        )

        # レスポンスステータスコードをチェック
        response.raise_for_status()

        # PDFデータをバイナリとしてクライアントに送信
        return send_file(
            io.BytesIO(response.content),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='presentation.pdf'
        )

    except requests.exceptions.RequestException as e:
        # marp-apiへの接続エラー
        return jsonify({"error": f"Failed to connect to marp-api: {e}"}), 503
    except Exception as e:
        # その他のエラー
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
