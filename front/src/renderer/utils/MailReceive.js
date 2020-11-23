// モジュールのインポート
import FileAction from './FileAction'
import OS from './OS'

const inbox = require('inbox')
const iconv = require('iconv')
const fs = require('fs')
const utf8 = require('utf8')
const quotedPrintable = require('quoted-printable')

// conv
const conv = new iconv.Iconv('ISO-2022-JP', 'UTF-8')

// メール受信関数
async function mailReceive (authData, getMailCount) {
  return new Promise(resolve => {
    // メールクライアントの定義
    const client = inbox.createConnection(authData['imap'].port, authData['imap'].host, {
      secureConnection: true,
      auth: {
        user: authData['auth'].user,
        pass: authData['auth'].pass
      }
    })
    client.on('connect', function () {
      client.openMailbox('INBOX', function (error, info) {
        if (error) throw error
        console.log('Successfully connected to server')
        client.listMessages(-getMailCount, function (err, messages) {
          if (err) {
            console.log(err)
          }
          client.close()
          return resolve(messages)
        })
      })
    })
    client.connect()
  })
}

// 特定ユーザのメール受信
async function mailReceiveUser (authData, targetAddress) {
  return new Promise(resolve => {
    const client = inbox.createConnection(authData['imap'].port, authData['imap'].host, {
      secureConnection: true,
      auth: {
        user: authData['auth'].user,
        pass: authData['auth'].pass
      }
    })
    client.on('connect', function () {
      client.openMailbox('INBOX', function (error, info) {
        if (error) throw error
        const query = {header: ['from', targetAddress]}
        client.search(query, function (err, numbers) {
          if (err) {
            console.log(err)
          }
          client.close()
          return resolve(numbers)
        })
      })
    })
    client.connect()
  })
}

// メールソースの取得
async function getMailText (authData, messageUID) {
  return new Promise(resolve => {
    const client = inbox.createConnection(authData['imap'].port, authData['imap'].host, {
      secureConnection: true,
      auth: {
        user: authData['auth'].user,
        pass: authData['auth'].pass
      }
    })

    console.log(messageUID)
    let mailData = ''
    client.on('connect', function () {
      client.openMailbox('INBOX', function (error, info) {
        // エラー時の処理
        if (error) {
          console.log(error)
        }

        console.log('Successfully connected to server')
        client.createMessageStream(messageUID).on('data', function (data) {
          // BASE64をデコード
          const body = conv.convert(data).toString()
          console.log(body)
          // テキストを結合
          mailData += body

          // パース
          const resultText = mailDataParser(mailData)

          if (resultText !== -1) {
            // client.close()
            console.log('resultTextSum: ---------')
            console.log(resultText)
            return resolve(resultText)
          }
        })
      })
    })
    client.connect()
  })
}

// メール本文をパース
function mailDataParser (targetSource) {
  // 区切り文字の取得
  let delimiterPrevText = 'Content-Type: multipart/alternative; boundary="'
  if (targetSource.indexOf(delimiterPrevText) === -1) {
    delimiterPrevText = 'Content-Type: multipart/mixed; boundary="'
  }

  // エンコード方式の取得
  const encodePrevText = '\r\nContent-Transfer-Encoding: '
  const encodePrevPosition = targetSource.indexOf(encodePrevText) + encodePrevText.length

  // エンコード方式が表示されていない場合
  if (encodePrevPosition === -1) {
    return -1
  }
  // エンコード方式の取得
  const encodeType = targetSource.substr(encodePrevPosition, targetSource.substr(encodePrevPosition).indexOf('\r\n'))

  console.log('ENCODE TYPE : |' + encodeType + '|')

  // 指定されていない場合
  if (targetSource.indexOf(delimiterPrevText) === -1) {
    const mimeText = '\r\nMIME-Version: 1.0\r\n\r\n'
    if (targetSource.indexOf(mimeText) === -1) {
      console.log('mimetext result : -1')
      return -1
    } else {
      // デコードする部分をパース
      const decodeTarget = targetSource.substr(targetSource.indexOf(mimeText) + mimeText.length)

      // デコードして返す
      return decodeBody(decodeTarget, encodeType)
    }
  }

  // 区切り文字の位置を特定
  const delimiterPrevTextPosition = targetSource.indexOf(delimiterPrevText) + delimiterPrevText.length
  const delimiterNextTextPosition = targetSource.substr(delimiterPrevTextPosition).indexOf('"')

  // 区切り文字列の取得
  const delimiterText = targetSource.substr(delimiterPrevTextPosition, delimiterNextTextPosition)

  // 区切り文字部分に移動
  const delimiterPosition = targetSource.substr(delimiterPrevTextPosition + delimiterNextTextPosition).indexOf(delimiterText) + delimiterPrevTextPosition + delimiterNextTextPosition + delimiterText.length

  // 1行空いている部分を探索
  const breakChar = '\r\n' // SMTPサーバがLinuxのため
  const base64HeadPosition = targetSource.substr(delimiterPosition).indexOf(breakChar + breakChar) + delimiterPosition + (breakChar.length * 2)
  const base64TailPosition = targetSource.substr(base64HeadPosition).indexOf(breakChar + '--' + delimiterText)

  // 終端部分が見つからない場合はエラーを返す
  if (base64TailPosition === -1) {
    return -1
  }

  // デコードする部分をパース
  const decodeTarget = targetSource.substr(base64HeadPosition, base64TailPosition)

  // デコードして返す
  return decodeBody(decodeTarget, encodeType)
}

// メール本文のデコード
function decodeBody (decodeTarget, encodeType) {
  let decodedText = ''

  if (encodeType === 'base64') {
    // Base64の場合
    decodedText = decodeURIComponent(escape(atob(decodeTarget)))
  } else if (encodeType === 'quoted-printable') {
    // Quoted-Printableの場合
    decodedText = utf8.decode(quotedPrintable.decode(decodeTarget))
  }

  // デコード結果を返す
  return decodedText
}

// サーバとの接続を切断
function disconnectServer (authData) {
  // メールクライアントの定義
  const client = inbox.createConnection(authData['imap'].port, authData['imap'].host, {
    secureConnection: true,
    auth: {
      user: authData['auth'].user,
      pass: authData['auth'].pass
    }
  })

  // サーバとの接続を切断
  client.close()
  client.on('close', function () {
    console.log('DISCONNECTED!')
  })
}

// メール内容をローカルに保存
async function saveLocalMail (roomID, newMails) {
  // メールの保存先ディレクトリ
  const mailDirectory = OS.homeDirectory() + OS.delimiterChar() + 'frankfrut' + OS.delimiterChar() + 'mailbox'
  const mailJSONfile = mailDirectory + OS.delimiterChar() + roomID + '.json'

  // 保存用ディレクトリの作成（存在しない場合のみ）
  await FileAction.mkdir(mailDirectory)

  // 保存用ファイルの作成（存在しない場合のみ）
  await FileAction.touch(mailJSONfile)

  // 保存先ディレクトリの内容を取得
  fs.readFile(mailJSONfile, 'utf8', function (err, mailJSON) {
    // エラー処理
    if (err) {
      console.log(err)
    }

    // メール保存用連想配列
    let mailObj = []

    // JSONを連想配列へ変換
    if (mailJSON !== '') {
      mailObj = JSON.parse(mailJSON)
    }

    // メールをJSONへ保存
    for (let mailUID in newMails) {
      // メールを1件取得
      const mail = newMails[mailUID]

      // オブジェクトが存在する場合は何もしない
      if (mail['UID'] in mailObj) {
        continue
      }

      // 新規メールの追加
      mailObj[mail['UID']] = {
        'UID': mail['UID'],
        'from': {
          'address': mail['from']['address']
        },
        'to': {
          '0': {
            'address': mail['to']['0']['address']
          }
        },
        'xGMThreadId': mail['xGMThreadId'],
        'date': mail['date'],
        'title': mail['title']
      }
    }

    console.log('mailObj :')
    console.log(mailObj)

    // 上書保存
    const optionJson = { flag: 'w' }
    const updateMailJSON = JSON.stringify(mailObj)
    fs.writeFile(mailJSONfile, updateMailJSON, optionJson, function (err) {
      if (err) {
        console.log(err)
      }
    })
  })
}

// ローカルに保存されたメールを取得
async function getLocalMail (roomID) {
  return new Promise(resolve => {
    // メールの保存先ディレクトリ
    const mailDirectory = OS.homeDirectory() + OS.delimiterChar() + 'frankfrut' + OS.delimiterChar() + 'mailbox'
    const mailJSONfile = mailDirectory + OS.delimiterChar() + roomID + '.json'

    // 保存先ディレクトリの内容を取得
    fs.readFile(mailJSONfile, 'utf8', function (err, mailJSON) {
      // エラー処理
      if (err) {
        console.log(err)
      }

      console.log('JSONのままのやつ')
      console.log(mailJSON)

      // メール保存用オブジェクト
      let mailObj = {}

      // JSONをオブジェクトへ変換
      if (mailJSON !== '') {
        mailObj = JSON.parse(mailJSON)
        console.log('パース')
        console.log(mailObj)
      }

      return resolve(mailObj)
    })
  })
}

// エクスポート
export default {mailReceive, mailReceiveUser, getMailText, disconnectServer, saveLocalMail, getLocalMail}
