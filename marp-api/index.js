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
        
        const tempPdfPath = path.join(os.tmpdir(), `temp-marp-output-${Date.now()}.pdf`);

        const program = 'node';
        const args = [
            marpCliScriptPath,
            tempMarkdownPath,
            '--pdf',
            '--allow-local-files',
            '--engine-options', '{"executablePath": "/usr/bin/google-chrome", "headless": "new", "args": ["--no-sandbox", "--disable-setuid-sandbox"]}',
            '-o',
            tempPdfPath
        ];

        console.log(`Executing command: ${program} ${args.join(' ')}`);

        const marpProcess = spawn(program, args);

        let errorOutput = '';
        marpProcess.stderr.on('data', (data) => {
            const stderrStr = data.toString();
            console.error(`Marp CLI stderr: ${stderrStr}`);
            errorOutput += stderrStr;
        });

        marpProcess.on('error', (err) => {
            console.error('Failed to start Marp CLI process.', err);
            fs.unlink(tempMarkdownPath, () => {}); // Clean up markdown file
            if (!res.headersSent) {
                res.status(500).send('Failed to start PDF generation process.');
            }
        });

        marpProcess.on('close', (code) => {
            console.log(`Marp CLI process exited with code ${code}`);
            // Always clean up the temporary markdown file
            fs.unlink(tempMarkdownPath, (unlinkErr) => {
                if (unlinkErr) console.error(`Failed to delete temp markdown file: ${unlinkErr}`);
            });

            if (code !== 0) {
                console.error(`Marp CLI process failed with code ${code}. Stderr: ${errorOutput}`);
                if (!res.headersSent) {
                    res.status(500).send(`Failed to generate PDF. Marp CLI exited with code ${code}.`);
                }
                return;
            }

            // Read the generated PDF and send it back
            fs.readFile(tempPdfPath, (readErr, pdfData) => {
                // Clean up the temporary PDF file as soon as we've read it
                fs.unlink(tempPdfPath, (unlinkErr) => {
                    if (unlinkErr) console.error(`Failed to delete temp PDF file: ${unlinkErr}`);
                });

                if (readErr) {
                    console.error(`Error reading temporary PDF file: ${readErr}`);
                    if (!res.headersSent) {
                        res.status(500).send('Failed to read generated PDF file.');
                    }
                    return;
                }

                res.setHeader('Content-Type', 'application/pdf');
                res.setHeader('Content-Disposition', 'attachment; filename=presentation.pdf');
                res.send(pdfData);
            });
        });
    });
});

app.listen(port, host, () => {
    console.log(`Server is running on http://${host}:${port}`);
});
