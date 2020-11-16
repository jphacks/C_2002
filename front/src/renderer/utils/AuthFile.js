// モジュールの取得
import OS from '../utils/OS'
const fs = require('fs')

// OS依存の文字列
const delimiter = OS.delimiterChar()
const JSONpath = OS.homeDirectory() + delimiter + 'frankfrut' + delimiter + 'data' + delimiter + 'address.json'

// ユーザ認証情報用JSONの確認（存在/値）
function checkAuthJSON () {
  // ファイルの存在チェック
  if (!fs.existsSync(JSONpath)) {
    return false
  }

  // JSONの取得
  getAuth().then((object) => {
    // オブジェクトの値の存在チェック
    if ('type' in object) {
      return false
    } else if ('smtp' in object) {
      return false
    } else if ('port' in object) {
      return false
    } else if ('imap' in object) {
      return false
    } else if ('pop' in object) {
      return false
    } else if ('user' in object) {
      return false
    } else if ('auth' in object) {
      return false
    }

    // 結果返却
    return true
  })
}

// 連絡先一覧の取得
async function getAuth () {
  return new Promise(resolve => {
    fs.readFile(JSONpath, 'utf8', function (err, addressJSON) {
      // エラー処理
      if (err) {
        console.log(err)
      }
      // JSONが空の場合
      if (addressJSON === '') {
        return resolve({})
      }

      // JSONからオブジェクトへの変換
      const addressObj = JSON.parse(addressJSON)
      console.log(addressObj)

      return resolve(addressObj)
    })
  })
}

export default { checkAuthJSON, getAuth }
