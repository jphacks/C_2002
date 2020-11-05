// POST送信テスト
const request = require('request');

// ユーザからのキーボード入力を取得する Promise を生成する
function readUserInput(question) {
  const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise((resolve, reject) => {
    readline.question(question, (answer) => {
      resolve(answer);
      readline.close();
    });
  });
}
  
// メイン処理
(async function main() {
    while(true) {
        const sentence = await readUserInput('Send Sentence: ');

        var commit_id = '1c40b98';
        // var message = 'お世話様です。';
        // const fs = require('fs');
        // var message = fs.readFileSync(__dirname + "/before.txt", 'utf-8');
        // var message = '株式会社●●●●\n●●●●様\n\nお世話様です。\n株式会社Pied Piperの岡崎竜也です。\n\n先日は打ち合わせの時間をくれまして、誠にありがとうございます。\nご依頼された商品Aの見積りが用意できました。\n打ち合わせで聞いた要望を反映し、特別割引を設けております。\n詳細について説明させてほしいのですが、1時間ほど時間をください。\n来週でしたら以下の日程で行くことが可能です。\n＜候補日時＞　\n・●月●日（火）10:00～11:30\n・●月●日（水）14:00～17:00\n・●月●日（木）15:30～17:30\n・●月●日（金）10:00～15:00\n\n●●様の都合を聞かせてください。\n\n忙しいところすいませんが、ご検討よろしくお願いいたします。'
        // var sentences = message.split('\n')

        var options = {
            // uri: "http://0.0.0.0:5000/postdata",
            uri: "http://54.64.167.36:5000/postdata",
            headers: {
                "Content-type": "application/json",
            },
            json: {
                'commit_id': commit_id,
                'sentence': sentence
            }
        };
        console.log('Send { \ncommit_id: ' + commit_id + '\nsentence: ' + sentence + '\n}')
        request.post(options, function(error, response, body){
            console.log(body)
        });
    }
})();