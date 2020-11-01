// POST送信テスト
const request = require('request');

var options = {
    uri: "http://localhost:5000/test",
    headers: {
        "Content-type": "application/json",
    },
    json: {
        'people_name': 'test',
        'companies_name': 'test'
    }
};
request.post(options, function(error, response, body){});