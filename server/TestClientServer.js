const express = require('express')
const app = express()
const bodyParser = require('body-parser')
const port = 5000

// POST送信テスト
// var request = require('request');
// var options = {
//     uri: "http://localhost:5000/test",
//     headers: {
//         "Content-type": "application/json",
//     },
//     json: {
//         'people_name': 'test',
//         'companies_name': 'test'
//     }
// };
// request.post(options, function(error, response, body){});

// POST受信テスト
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());
app.post('/test', (req, res) => {
  console.log(req.body);
  res.send("Received POST Data!");
});
app.listen(port, () => console.log(`Example app listening on port ${port}!`))