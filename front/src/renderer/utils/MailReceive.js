// モジュールのインポート
const inbox = require('inbox')
const iconv = require('iconv')
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
          return resolve(messages)
        })
      })
    })
    client.connect()
  })
}

// 特定ユーザのメール受信
async function mailReceiveUser (authData, targetAddress, getMailCount = 20) {
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
          return resolve(numbers)
        })
      })
    })
    client.connect()
  })
}

// メール内容の取得
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
    client.on('connect', function () {
      client.openMailbox('INBOX', function (error, info) {
        if (error) console.log(error)
        console.log('Successfully connected to server')
        client.createMessageStream(messageUID).on('data', function (data) {
          // BASE64をデコード
          const body = conv.convert(data).toString()
          console.log(body)
          const resultText = mailDataParser(body)

          console.log('resultText : ')
          console.log(resultText)

          if (resultText !== '') {
            return resolve(resultText)
          }
        })
      })
    })
    client.connect()
  })
}

// Base64の本文をパースしてデコード
function mailDataParser (targetSource) {
  const delimiterPrevText = 'Content-Type: multipart/alternative; boundary="'
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

  // Base64にエンコードされた本文を取得
  const base64Text = targetSource.substr(base64HeadPosition, base64TailPosition)

  // Base64からのデコード
  const plainText = decodeURIComponent(escape(atob(base64Text)))

  console.log('plaintext : ' + plainText)

  return plainText
}

export default {mailReceive, mailReceiveUser, getMailText}
