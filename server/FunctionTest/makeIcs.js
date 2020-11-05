const fs = require("fs");
const ics = require("ics")

// icsファイルの作成
// @title: カレンダーのタイトル
// @description: メモに記載する文章
// @start: 開始時刻（[年, 月, 日, 時間, 分]の配列で）
// @duration: 何分間の予定か
function makeIcs(title_str, description_str, start_time_array, duration_int) {
    ics.createEvent({
        title: title_str,
        description: description_str,
        busyStatus: 'FREE',
        start: start_time_array,
        duration: { minutes: duration_int }
    }, (error, value) => {
        if (error) {
        console.log(error)
        }
        
        fs.writeFileSync(__dirname + '/' + title_str + '.ics', value)
    })
}

makeIcs('Dinner', 'Nightly thing I do', [2018, 1, 15, 6, 30], 50);