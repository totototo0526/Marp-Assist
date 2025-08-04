# backend/run.py

from marp_assist import create_app

# アプリケーションのインスタンスを作成
app = create_app()

if __name__ == '__main__':
    # Flask開発サーバーを起動
    # host='0.0.0.0' で外部からのアクセスを許可
    app.run(host='0.0.0.0', port=5000, debug=True)
