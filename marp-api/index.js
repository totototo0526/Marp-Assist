const express = require('express');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const app = express();
const port = 3000;

// Increase payload size limit for incoming JSON
app.use(express.json({ limit: '10mb' }));

app.post('/convert', (req, res) => {
    console.log('Received request for /convert');
    const markdown = req.body.markdown;
    if (!markdown) {
        console.error('Request failed: Markdown content is required.');
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
        const command = `node ${marpCliScriptPath} ${tempMarkdownPath} --pdf --allow-local-files -o -`;
        console.log(`Executing command: ${command}`);

        // Set the CWD to the marp-cli package directory to ensure it can find its own modules.
        const marpCliDir = path.dirname(marpCliScriptPath);

        exec(command, {
            encoding: 'binary',
            maxBuffer: 10 * 1024 * 1024,
            cwd: marpCliDir
        }, (error, stdout, stderr) => {
            fs.unlink(tempMarkdownPath, (unlinkErr) => {
                if (unlinkErr) {
                    console.error(`Failed to delete temp file '${tempMarkdownPath}': ${unlinkErr}`);
                } else {
                    console.log(`Successfully deleted temp file: ${tempMarkdownPath}`);
                }
            });

            if (error) {
                console.error(`Marp CLI exec error: ${error}`);
                console.error(`Marp CLI stderr: ${stderr}`);
                return res.status(500).send(`Failed to convert markdown to PDF. Stderr: ${stderr}`);
            }

            console.log('Marp CLI execution successful. Sending PDF response.');
            res.setHeader('Content-Type', 'application/pdf');
            res.setHeader('Content-Disposition', 'attachment; filename=presentation.pdf');
            res.status(200).send(Buffer.from(stdout, 'binary'));
        });
    });
});

app.listen(port, () => {
    console.log(`Marp API server listening at http://localhost:${port}`);
});
