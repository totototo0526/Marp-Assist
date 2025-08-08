document.addEventListener('DOMContentLoaded', () => {
    // DOM要素の取得
    const topicInput = document.getElementById('topic-input');
    const generateButton = document.getElementById('generate-button');
    const copyButton = document.getElementById('copy-button');
    const resultArea = document.getElementById('result');
    const templateSelect = document.getElementById('template-select'); // ドロップダウンを追加

    // バックエンドAPIのURL (相対パスに変更)
    const API_BASE_URL = '/api';
    const GENERATE_API_URL = `${API_BASE_URL}/generate`;
    const TEMPLATES_API_URL = `${API_BASE_URL}/templates`;

    // コピーボタンの初期のテキスト
    const originalCopyButtonText = copyButton.textContent;

    // テンプレートをバックエンドから取得してドロップダウンを生成する関数
    async function populateTemplates() {
        try {
            const response = await fetch(TEMPLATES_API_URL);
            if (!response.ok) {
                throw new Error('テンプレートの読み込みに失敗しました。');
            }
            const templates = await response.json();

            // 取得したテンプレートでドロップダウンの選択肢を作成
            templates.forEach(template => {
                const option = document.createElement('option');
                option.value = template.name;
                option.textContent = template.label;
                templateSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching templates:', error);
            alert(error.message);
        }
    }

    // ページ読み込み時にテンプレートを取得
    populateTemplates();

    // 生成ボタンのクリックイベント
    generateButton.addEventListener('click', async () => {
        const topic = topicInput.value;
        const templateName = templateSelect.value; // 選択されたテンプレート名を取得

        if (!topic.trim()) {
            alert('お題を入力してください。');
            return;
        }
        if (!templateName) {
            alert('テンプレートを選択してください。');
            return;
        }

        // ボタンを無効化し、ローディング表示
        generateButton.disabled = true;
        resultArea.textContent = 'AIが生成中です...';
        resultArea.classList.add('loading');

        try {
            // バックエンドAPIにリクエストを送信
            const response = await fetch(GENERATE_API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                // topic と template_name の両方を送信
                body: JSON.stringify({ topic: topic, template_name: templateName }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'サーバーでエラーが発生しました。');
            }

            const data = await response.json();
            // 結果を表示 (バックエンドからのキーを`content`に合わせる)
            resultArea.textContent = data.content;

        } catch (error) {
            console.error('Error:', error);
            resultArea.textContent = `エラーが発生しました：${error.message}`;
            alert(`エラーが発生しました：${error.message}`);
        } finally {
            generateButton.disabled = false;
            resultArea.classList.remove('loading');
        }
    });

    // コピーボタンのクリックイベント
    copyButton.addEventListener('click', () => {
        const textToCopy = resultArea.textContent;
        if (textToCopy && !resultArea.classList.contains('loading') && !textToCopy.startsWith('ここに結果が') && !textToCopy.startsWith('エラーが発生')) {
            navigator.clipboard.writeText(textToCopy).then(() => {
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
