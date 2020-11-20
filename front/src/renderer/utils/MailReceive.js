// モジュールのインポート
const inbox = require('inbox')
const iconv = require('iconv')
const utf8 = require('utf8')
const quotedPrintable = require('quoted-printable')
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
          client.close()
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

// Base64の本文をパースしてデコード
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
      const decodeTarget = targetSource.substr(targetSource.indexOf(mimeText) + mimeText.length)
      let decodedText = ''
      // Base64の場合
      if (encodeType === 'base64') {
        decodedText = decodeURIComponent(escape(atob(decodeTarget)))
      } else if (encodeType === 'quoted-printable') {
        decodedText = utf8.decode(quotedPrintable.decode(decodeTarget))
      }
      console.log('デコード結果：' + decodedText)
      return decodedText
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

  console.log('base64TailPosition : ' + base64TailPosition)

  // 終端部分が見つからない場合はエラーを返す
  if (base64TailPosition === -1) {
    return -1
  }

  // Base64にエンコードされた本文を取得
  const decodeTarget = targetSource.substr(base64HeadPosition, base64TailPosition)

  let decodedText = ''
  // Base64の場合
  if (encodeType === 'base64') {
    decodedText = decodeURIComponent(escape(atob(decodeTarget)))
  } else if (encodeType === 'quoted-printable') {
    decodedText = utf8.decode(quotedPrintable.decode(decodeTarget))
  }
  console.log('デコード結果：' + decodedText)
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

export default {mailReceive, mailReceiveUser, getMailText, disconnectServer}
