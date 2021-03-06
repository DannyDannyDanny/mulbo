const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();
const port = 8081;

app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(express.static(`${__dirname}/front-end/`));

app.get('/', (req, res) => {
    res.sendFile('index.html');
});

app.post('/api/demo/', (req, res) => {
    if (!req.body || !req.body.string) {
        return res.status(400).send('Bad request: request data should be an object with key "string".');
    }
    fs.appendFileSync(`${__dirname}/requests/strings.txt`, `{\n    "string": "${req.body.string.replaceAll('\n', '\\n')}"\n}, `);
    res.status(204).end();
});

app.listen(port, () => {
    console.log(`Listening at http://localhost:${port}`);
});