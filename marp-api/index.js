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

    // --- ここからがテスト用のコード ---
    const program = 'env';
    const args = [];

    console.log(`Executing test command: ${program}`);
    const testProcess = spawn(program, args);

    let output = '';
    testProcess.stdout.on('data', (data) => {
        output += data.toString();
    });

    testProcess.on('close', (code) => {
        if (code === 0) {
            res.status(200).send(`Test command successful. Output:\n${output}`);
        } else {
            res.status(500).send(`Test command failed with code ${code}.`);
        }
    });
    // --- ここまでがテスト用のコード ---
});

app.listen(port, host, () => {
    console.log(`Server is running on http://${host}:${port}`);
});
