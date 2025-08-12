const express = require('express');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const app = express();
const port = 3000;
const host = '0.0.0.0';

app.use(express.json({ limit: '10mb' }));

app.post('/convert', (req, res) => {
    console.log('Received request for /convert');
    const markdown = req.body.markdown;
    if (!markdown) {
        return res.status(400).send('Markdown content is required.');
    }

    const tempMarkdownPath = path.join(os.tmpdir(), `temp-marp-${Date.now()}.md`);
    console.log(`Creating temporary file at: ${tempMarkdownPath}`);

    fs.writeFile(tempMarkdownPath, markdown, (writeErr) => {
        if (writeErr) {
            console.error(`File write error: ${writeErr}`);
            return res.status(500).send('Failed to create temporary markdown file.');
        }
        console.log('Temporary file created successfully.');

        const marpCliScriptPath = path.join(__dirname, 'node_modules', '@marp-team', 'marp-cli', 'marp-cli.js');

        const program = 'node';
        const args = [
            marpCliScriptPath,
            tempMarkdownPath,
            '--pdf',
            '--allow-local-files',
            '--engine-options', '{"executablePath": "/usr/bin/google-chrome", "headless": "new", "args": ["--no-sandbox", "--disable-setuid-sandbox", "--user-data-dir=/tmp/marp-chrome-profile", "--disable-dev-shm-usage", "--disable-gpu"]}',
            '-o',
            '-'
        ];

        console.log(`Executing command: ${program} ${args.join(' ')}`);

        const marpProcess = spawn(program, args);

        // --- ここからが修正部分：より堅牢なストリーム処理 ---
        res.setHeader('Content-Type', 'application/pdf');
        res.setHeader('Content-Disposition', 'attachment; filename=presentation.pdf');

        // marp-cliの標準出力を、直接レスポンスのストリームに流し込む
        marpProcess.stdout.pipe(res);

        let errorOutput = '';
        marpProcess.stderr.on('data', (data) => {
            const stderrStr = data.toString();
            console.error(`Marp CLI stderr: ${stderrStr}`);
            errorOutput += stderrStr;
        });

        marpProcess.on('close', (code) => {
            console.log(`Marp CLI process exited with code ${code}`);
            fs.unlink(tempMarkdownPath, () => {}); // 一時ファイルを削除

            if (code !== 0) {
                console.error('Marp CLI process failed.');
                // ストリームはすでに閉じられているので、ここではログに残すだけ
            }
        });

        marpProcess.on('error', (err) => {
            console.error('Failed to start Marp CLI process.', err);
            if (!res.headersSent) {
                res.status(500).send('Failed to start PDF generation process.');
            }
        });
        // --- ここまでが修正部分 ---
    });
});

app.listen(port, host, () => {
    console.log(`Server is running on http://${host}:${port}`);
});
