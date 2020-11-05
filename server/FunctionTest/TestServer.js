// POST受信テスト
const express = require('express')
const app = express()
const bodyParser = require('body-parser')
const port = 5000

app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());
app.post('/test', (req, res) => {
  console.log(req.body);
  res.send("Received POST Data!");
});
app.listen(port, () => console.log(`Example app listening on port ${port}!`))