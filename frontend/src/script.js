import Marpit from '@marp-team/marpit';

document.addEventListener('DOMContentLoaded', () => {
    // DOM要素の取得
    const topicInput = document.getElementById('topic-input');
    const generateButton = document.getElementById('generate-button');
    const copyButton = document.getElementById('copy-button');
    const downloadPdfButton = document.getElementById('download-pdf-button');
    const resultTextarea = document.getElementById('result-textarea');
    const templateSelect = document.getElementById('template-select');
    const themeSelect = document.getElementById('theme-select');
    const marpOptionsContainer = document.getElementById('marp-options-container');
    const slideCountInput = document.getElementById('slide-count-input');
    const includeHashtagsCheckbox = document.getElementById('include-hashtags-checkbox');
    const previewArea = document.getElementById('preview-area');

    // Marpitのインスタンスを初期化
    const marpit = new Marpit();

    // バックエンドAPIのURL
    // Viteのプロキシ設定により、開発サーバーではリクエストがバックエンドに転送される
    const API_BASE_URL = '/api';
    const GENERATE_API_URL = `${API_BASE_URL}/generate`;
    const DOWNLOAD_PDF_API_URL = `${API_BASE_URL}/download_pdf`;
    const TEMPLATES_API_URL = `${API_BASE_URL}/templates`;
    const THEMES_API_URL = `${API_BASE_URL}/themes`;

    // コピーボタンの初期のテキスト
    const originalCopyButtonText = copyButton.textContent;

    // テンプレート情報を保持する変数
    let allTemplates = [];

    // --- プレビュー更新処理 ---
    const updatePreview = () => {
        const markdown = resultTextarea.value;
        const { html, css } = marpit.render(markdown);
        // プレビューエリアにスタイルとHTMLを適用
        previewArea.innerHTML = `<style>${css}</style>${html}`;
    };

    // テンプレートをバックエンドから取得してドロップダウンを生成する関数
    async function populateTemplates() {
        try {
            const response = await fetch(TEMPLATES_API_URL);
            if (!response.ok) {
                throw new Error('テンプレートの読み込みに失敗しました。');
            }
            allTemplates = await response.json(); // テンプレート情報を保持
            templateSelect.innerHTML = ''; // 一旦クリア
            allTemplates.forEach(template => {
                const option = document.createElement('option');
                option.value = template.name;
                option.textContent = template.label;
                templateSelect.appendChild(option);
            });
            // 初期表示のためにchangeイベントを発火
            templateSelect.dispatchEvent(new Event('change'));
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
                option.value = theme.id;
                option.textContent = theme.name;
                themeSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching themes:', error);
            alert(error.message);
        }
    }

    // テンプレート選択の変更イベント
    templateSelect.addEventListener('change', () => {
        const selectedTemplateName = templateSelect.value;
        const selectedTemplate = allTemplates.find(t => t.name === selectedTemplateName);
        if (selectedTemplate && selectedTemplate.output_type === 'marp') {
            marpOptionsContainer.style.display = 'flex';
        } else {
            marpOptionsContainer.style.display = 'none';
        }
    });

    // 生成ボタンのクリックイベント
    generateButton.addEventListener('click', async () => {
        const topic = topicInput.value;
        const templateName = templateSelect.value;
        const themeId = themeSelect.value;

        if (!topic.trim()) {
            alert('お題を入力してください。');
            return;
        }
        if (!templateName) {
            alert('テンプレートを選択してください。');
            return;
        }

        generateButton.disabled = true;
        downloadPdfButton.disabled = true;
        resultTextarea.value = 'AIが生成中です...';
        resultTextarea.classList.add('loading');
        updatePreview(); // ローディングメッセージもプレビュー

        // リクエストボディを構築
        const requestBody = {
            topic: topic,
            template_name: templateName,
            theme_id: parseInt(themeId, 10)
        };

        // Marpオプションが表示されている場合、値を追加
        if (marpOptionsContainer.style.display !== 'none') {
            requestBody.slide_count = parseInt(slideCountInput.value, 10);
            requestBody.include_hashtags = includeHashtagsCheckbox.checked;
        }

        try {
            const response = await fetch(GENERATE_API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'サーバーでエラーが発生しました。');
            }

            const data = await response.json();
            resultTextarea.value = data.content;
            downloadPdfButton.disabled = false;
            updatePreview(); // AI生成後にプレビューを更新

        } catch (error) {
            console.error('Error:', error);
            resultTextarea.value = `エラーが発生しました：${error.message}`;
            updatePreview(); // エラーメッセージもプレビュー
            alert(`エラーが発生しました：${error.message}`);
        } finally {
            generateButton.disabled = false;
            resultTextarea.classList.remove('loading');
        }
    });

    // コピーボタンのクリックイベント
    copyButton.addEventListener('click', () => {
        const textToCopy = resultTextarea.value;
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
        const markdownContent = resultTextarea.value;
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

    // テキストエリアでの入力に反応してプレビューを更新
    resultTextarea.addEventListener('input', updatePreview);

    // --- 初期化処理 ---
    populateTemplates();
    populateThemes();
    updatePreview(); // 初期表示のためにプレビューを一度実行
});
