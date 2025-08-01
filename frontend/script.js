document.addEventListener('DOMContentLoaded', () => {
    const topicInput = document.getElementById('topic-input');
    const generateButton = document.getElementById('generate-button');
    const resultDiv = document.getElementById('result');

    // バックエンドAPIのURL（ローカル開発環境）
    const API_URL = 'http://127.0.0.1:5000/api/generate';

    generateButton.addEventListener('click', async () => {
        const topic = topicInput.value;
        if (!topic) {
            alert('お題を入力してください。');
            return;
        }

        // ボタンを無効化し、ローディング表示
        generateButton.disabled = true;
        resultDiv.textContent = 'AIが生成中です...';
        resultDiv.classList.add('loading');

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
            resultDiv.textContent = data.marp_content;

        } catch (error) {
            // エラーが発生した場合
            console.error('Error:', error);
            resultDiv.textContent = `エラーが発生しました：${error.message}`;
            alert(`エラーが発生しました：${error.message}`);
        } finally {
            // ボタンを再度有効化し、ローディング表示を解除
            generateButton.disabled = false;
            resultDiv.classList.remove('loading');
        }
    });
});
