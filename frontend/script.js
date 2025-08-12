document.addEventListener('DOMContentLoaded', () => {
    // DOM要素の取得
    const topicInput = document.getElementById('topic-input');
    const generateButton = document.getElementById('generate-button');
    const copyButton = document.getElementById('copy-button');
    const downloadPdfButton = document.getElementById('download-pdf-button');
    const resultTextarea = document.getElementById('result-textarea'); // <pre>から<textarea>に変更
    const templateSelect = document.getElementById('template-select');
    const themeSelect = document.getElementById('theme-select'); // テーマ選択用に追加

    // バックエンドAPIのURL
    const API_BASE_URL = '/api';
    const GENERATE_API_URL = `${API_BASE_URL}/generate`;
    const DOWNLOAD_PDF_API_URL = `${API_BASE_URL}/download_pdf`;
    const TEMPLATES_API_URL = `${API_BASE_URL}/templates`;
    const THEMES_API_URL = `${API_BASE_URL}/themes`; // テーマAPI用に追加

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

    // テーマをバックエンドから取得してドロップダウンを生成する関数
    async function populateThemes() {
        try {
            const response = await fetch(THEMES_API_URL);
            if (!response.ok) {
                throw new Error('テーマの読み込みに失敗しました。');
            }
            const themes = await response.json();
            themes.forEach(theme => {
                const option = document.createElement('option');
                option.value = theme.id; // valueをidに
                option.textContent = theme.name; // textをnameに
                themeSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching themes:', error);
            alert(error.message);
        }
    }

    // ページ読み込み時にテンプレートとテーマを取得
    populateTemplates();
    populateThemes();

    // 生成ボタンのクリックイベント
    generateButton.addEventListener('click', async () => {
        const topic = topicInput.value;
        const templateName = templateSelect.value;
        const themeId = themeSelect.value; // 選択されたテーマIDを取得

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
        downloadPdfButton.disabled = true;
        resultTextarea.value = 'AIが生成中です...'; // .textContentから.valueへ変更
        resultTextarea.classList.add('loading');

        try {
            // バックエンドAPIにリクエストを送信
            const response = await fetch(GENERATE_API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                // topic, template_name, theme_idを送信
                body: JSON.stringify({
                    topic: topic,
                    template_name: templateName,
                    theme_id: parseInt(themeId, 10) // 数値として送信
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'サーバーでエラーが発生しました。');
            }

            const data = await response.json();
            resultTextarea.value = data.content; // .textContentから.valueへ変更
            downloadPdfButton.disabled = false;

        } catch (error) {
            console.error('Error:', error);
            resultTextarea.value = `エラーが発生しました：${error.message}`;
            alert(`エラーが発生しました：${error.message}`);
        } finally {
            generateButton.disabled = false;
            resultTextarea.classList.remove('loading');
        }
    });

    // コピーボタンのクリックイベント
    copyButton.addEventListener('click', () => {
        const textToCopy = resultTextarea.value; // .textContentから.valueへ変更
        const placeholderText = 'ここに結果が表示されます...';
        if (textToCopy && textToCopy !== placeholderText && !textToCopy.startsWith('AIが生成中') && !textToCopy.startsWith('エラーが発生')) {
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

    // PDFダウンロードボタンのクリックイベント
    downloadPdfButton.addEventListener('click', async () => {
        const markdownContent = resultTextarea.value; // .textContentから.valueへ変更
        const placeholderText = 'ここに結果が表示されます...';

        if (!markdownContent || markdownContent === placeholderText || markdownContent.startsWith('AIが生成中') || markdownContent.startsWith('エラーが発生')) {
            alert('PDF化できるコンテンツがありません。');
            return;
        }

        downloadPdfButton.disabled = true;
        const originalButtonText = downloadPdfButton.textContent;
        downloadPdfButton.textContent = 'PDF生成中...';

        try {
            const response = await fetch(DOWNLOAD_PDF_API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ markdown: markdownContent }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'PDFの生成に失敗しました。');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'presentation.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

        } catch (error) {
            console.error('PDF Download Error:', error);
            alert(`エラーが発生しました：${error.message}`);
        } finally {
            downloadPdfButton.disabled = false;
            downloadPdfButton.textContent = originalButtonText;
        }
    });
});
