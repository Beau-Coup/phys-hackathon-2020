const express = require('express')
const app = express()
const port = 3000

app.get('/snowflake', (req, res) => {
    var spawn = require("child_process").spawn;

    var process = spawn('python',["./test.py",
        "asdasd",
        "asdasfafd"] );
    process.stdout.on('data', function(data) {
        res.send(data.toString());
    } )
});

app.use('/', express.static('../dist'))
app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
});
