const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();
const port = 8081;

app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.get('/api/demo/', (req, res) => {
    res.send("hello");
});

app.post('/api/demo/', (req, res) => {
    if (!req.body || !req.body.string) {
        return res.status(400).send('Bad request: request data should be an object with key "string".');
    }
    fs.appendFileSync('nodeJS/requests/strings.txt', `{\n    "string": "${req.body.string.replaceAll('\n', '\\n')}"\n}, `);
});

app.listen(port, () => {
    console.log(`Listening at http://localhost:${port}`);
});