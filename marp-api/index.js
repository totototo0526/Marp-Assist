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
    const markdown = req.body.markdown;
    if (!markdown) {
        return res.status(400).send('Markdown content is required.');
    }

    // Create a temporary file to store the markdown content
    const tempMarkdownPath = path.join(os.tmpdir(), `temp-marp-${Date.now()}.md`);

    fs.writeFile(tempMarkdownPath, markdown, (writeErr) => {
        if (writeErr) {
            console.error(`File write error: ${writeErr}`);
            return res.status(500).send('Failed to create temporary markdown file.');
        }

        // Execute marp-cli to convert markdown to PDF, outputting to stdout
        const command = `npx @marp-team/marp-cli@latest ${tempMarkdownPath} --pdf --allow-local-files -o -`;

        exec(command, { encoding: 'binary', maxBuffer: 10 * 1024 * 1024 }, (error, stdout, stderr) => {
            // Clean up the temporary file
            fs.unlink(tempMarkdownPath, (unlinkErr) => {
                if (unlinkErr) console.error(`Failed to delete temp file: ${unlinkErr}`);
            });

            if (error) {
                console.error(`Marp CLI exec error: ${error}`);
                console.error(`Marp CLI stderr: ${stderr}`);
                return res.status(500).send('Failed to convert markdown to PDF.');
            }

            // Send the generated PDF as a response
            res.setHeader('Content-Type', 'application/pdf');
            res.setHeader('Content-Disposition', 'attachment; filename=presentation.pdf');
            res.status(200).send(Buffer.from(stdout, 'binary'));
        });
    });
});

app.listen(port, () => {
    console.log(`Marp API server listening at http://localhost:${port}`);
});
