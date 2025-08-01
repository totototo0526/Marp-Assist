// DOMが完全に読み込まれたら処理を開始
document.addEventListener('DOMContentLoaded', () => {
    // 操作対象のHTML要素を取得
    const topicInput = document.getElementById('topic-input');
    const generateButton = document.getElementById('generate-button');
    const resultDiv = document.getElementById('result');

    // バックエンドAPIのURLを定義
    const API_URL = 'http://127.0.0.1:5000/api/generate';

    // 「生成する」ボタンがクリックされた時の処理を定義
    generateButton.addEventListener('click', async () => {
        const topic = topicInput.value;
        // テキストエリアが空の場合はアラートを表示して処理を中断
        if (!topic) {
            alert('お題を入力してください。');
            return;
        }

        // --- APIリクエスト開始 ---

        // ボタンを無効化し、ローディングメッセージを表示
        generateButton.disabled = true;
        resultDiv.textContent = 'AIが生成中です...';
        resultDiv.classList.add('loading');

        try {
            // fetch APIを使用してバックエンドにPOSTリクエストを送信
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    // 送信するデータがJSON形式であることをサーバーに伝える
                    'Content-Type': 'application/json',
                },
                // JavaScriptのオブジェクトをJSON文字列に変換してbodyに設定
                body: JSON.stringify({ topic: topic }),
            });

            // レスポンスが成功でない場合 (ステータスコードが200番台でない場合)
            if (!response.ok) {
                const errorData = await response.json();
                // サーバーから返されたエラーメッセージを使って、Errorオブジェクトを生成
                throw new Error(errorData.error || 'サーバーでエラーが発生しました。');
            }

            // レスポンスボディをJSONとしてパース
            const data = await response.json();
            // 結果表示エリアに、AIが生成したMarpコンテンツを表示
            resultDiv.textContent = data.marp_content;

        } catch (error) {
            // tryブロック内で発生したエラーをキャッチ
            console.error('Error:', error);
            // ユーザーにアラートでエラーを通知
            resultDiv.textContent = `エラーが発生しました：${error.message}`;
            alert(`エラーが発生しました：${error.message}`);
        } finally {
            // --- 処理完了 ---
            // 成功・失敗にかかわらず、ボタンを再度有効化し、ローディング表示を解除
            generateButton.disabled = false;
            resultDiv.classList.remove('loading');
        }
    });
});
