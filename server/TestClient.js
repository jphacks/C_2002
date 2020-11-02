// POST送信テスト
const request = require('request');
var message = '株式会社名城へ\nJPHACKS優勝したい！スマホ欲しい。佐藤より'
var options = {
    uri: "http://0.0.0.0:5000/postdata",
    headers: {
        "Content-type": "application/json",
    },
    json: {
        'sentence': message
    }
};
console.log('Send { sentence: ' + message + ' }')
request.post(options, function(error, response, body){
    console.log(body)
    console.log(body.calibration[0].alerts)
});