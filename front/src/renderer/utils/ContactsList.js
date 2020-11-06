// モジュールの取得
import FileAction from './FileAction'
import OS from '../utils/OS'
const fs = require('fs')

// OS毎の文字列
const delimiter = OS.delimiterChar()
const JSONpath = OS.homeDirectory() + delimiter + 'frankfrut' + delimiter + 'data' + delimiter + 'address.json'

// 連絡先一覧管理JSONの作成
async function contactInit () {
  if (!fs.existsSync(JSONpath)) {
    // ディレクトリの作成
    await FileAction.mkdir(OS.homeDirectory() + delimiter + 'frankfrut' + delimiter + 'data' + delimiter)

    // ファイルへの書き込み
    return new Promise(resolve => {
      fs.writeFile(JSONpath, '', '', function (err) {
        if (err) {
          console.log(err)
        }
        return resolve(0)
      })
    })
  }
}

// 連絡先一覧の取得
async function getAddress () {
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

// 連絡先一覧の上書
function updateAddress (addressObj) {
  // オブジェクトをJSONに変換
  const addressJSON = JSON.stringify(addressObj)

  console.log('address : ' + addressObj)

  // ファイルへの書き込み
  const optionJson = { flag: 'w' }
  return new Promise(resolve => {
    fs.writeFile(JSONpath, addressJSON, optionJson, function (err) {
      if (err) {
        console.log(err)
      }
      return resolve(0)
    })
  })
}

// エクスポート
export default { contactInit, getAddress, updateAddress }
