const express = require('express');
const { exec } = require('child_process');
const app = express();
const port = 3000;

app.use(express.json());

app.post('/convert', (req, res) => {
    const markdown = req.body.markdown;
    if (!markdown) {
        return res.status(400).send('Markdown content is required.');
    }

    // Marp CLIに渡すための一時ファイルを作成
    const tempMarkdownPath = '/tmp/temp.md';
    require('fs').writeFileSync(tempMarkdownPath, markdown);

    // Marp CLIを実行してHTMLに変換
    exec(`marp ${tempMarkdownPath} --html`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).send('Failed to convert markdown.');
        }

        // Marpは標準出力に変換後のHTMLを出力します
        res.status(200).send(stdout);
    });
});

app.listen(port, () => {
    console.log(`Marp API server listening at http://localhost:${port}`);
});
