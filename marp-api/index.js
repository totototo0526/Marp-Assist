const express = require('express');
const { Marp } = require('@marp-team/marp-core');
const puppeteer = require('puppeteer');

const app = express();
const port = 3000;
const host = '0.0.0.0';

app.use(express.json({ limit: '10mb' }));

app.post('/convert', async (req, res) => {
    console.log('Received request for /convert');
    const { markdown } = req.body;
    if (!markdown) {
        return res.status(400).send('Markdown content is required.');
    }

    let browser;
    try {
        console.log('Initializing Marp Core...');
        const marp = new Marp({
            html: true, // Enable HTML for security-related features
        });

        console.log('Rendering Markdown...');
        const { html, css } = marp.render(markdown);
        console.log('Markdown rendered to HTML.');

        console.log('Launching Puppeteer...');
        browser = await puppeteer.launch({
            executablePath: '/usr/bin/google-chrome',
            headless: 'new',
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--no-zygote', // Often helps in restricted environments
                '--single-process' // Another flag that can help
            ]
        });

        const page = await browser.newPage();
        console.log('Setting page content...');
        // Set content and wait for it to be fully loaded
        await page.setContent(html, { waitUntil: 'networkidle0' });
        await page.addStyleTag({ content: css });

        console.log('Generating PDF...');
        const pdfBuffer = await page.pdf({
            printBackground: true,
            format: 'A4',
            margin: { top: '1cm', right: '1cm', bottom: '1cm', left: '1cm' }
        });
        console.log('PDF generated successfully.');

        res.setHeader('Content-Type', 'application/pdf');
        res.setHeader('Content-Disposition', 'attachment; filename=presentation.pdf');
        res.send(pdfBuffer);
        console.log('PDF sent successfully.');

    } catch (e) {
        console.error('Error during programmatic PDF conversion:', e);
        if (!res.headersSent) {
            res.status(500).send(`An error occurred: ${e.message}`);
        }
    } finally {
        if (browser) {
            console.log('Closing Puppeteer browser...');
            await browser.close();
            console.log('Puppeteer browser closed.');
        }
    }
});

app.listen(port, host, () => {
    console.log(`Server is running on http://${host}:${port}`);
});
