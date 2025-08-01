document.addEventListener('DOMContentLoaded', () => {
    const topicInput = document.getElementById('topic-input');
    const generateButton = document.getElementById('generate-button');
    const copyButton = document.getElementById('copy-button');
    const resultArea = document.getElementById('result');

    // バックエンドAPIのURL（ローカル開発環境）
    const API_URL = 'http://127.0.0.1:5000/api/generate';

    // コピーボタンの初期のテキスト
    const originalCopyButtonText = copyButton.textContent;

    generateButton.addEventListener('click', async () => {
        const topic = topicInput.value;
        if (!topic.trim()) {
            alert('お題を入力してください。');
            return;
        }

        // ボタンを無効化し、ローディング表示
        generateButton.disabled = true;
        resultArea.textContent = 'AIが生成中です...';
        resultArea.classList.add('loading');

        try {
            // バックエンドAPIにリクエストを送信
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ topic: topic }),
            });

            if (!response.ok) {
                // エラーレスポンスを受け取った場合
                const errorData = await response.json();
                throw new Error(errorData.error || 'サーバーでエラーが発生しました。');
            }

            const data = await response.json();
            // 結果を表示
            resultArea.textContent = data.marp_content;

        } catch (error) {
            // エラーが発生した場合
            console.error('Error:', error);
            resultArea.textContent = `エラーが発生しました：${error.message}`;
            alert(`エラーが発生しました：${error.message}`);
        } finally {
            // ボタンを再度有効化し、ローディング表示を解除
            generateButton.disabled = false;
            resultArea.classList.remove('loading');
        }
    });

    copyButton.addEventListener('click', () => {
        const textToCopy = resultArea.textContent;
        // 初期状態やエラーメッセージはコピーしない
        if (textToCopy && !resultArea.classList.contains('loading') && !textToCopy.startsWith('ここに結果が') && !textToCopy.startsWith('エラーが発生')) {
            navigator.clipboard.writeText(textToCopy).then(() => {
                // コピー成功時のフィードバック
                copyButton.textContent = 'コピーしました！';
                setTimeout(() => {
                    copyButton.textContent = originalCopyButtonText;
                }, 2000);
            }).catch(err => {
                console.error('コピーに失敗しました', err);
                alert('クリップボードへのコピーに失敗しました。');
            });
        }
    });
});
