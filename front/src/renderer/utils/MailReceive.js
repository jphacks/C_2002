// モジュールのインポート
const inbox = require('inbox')

// メール受信関数
async function mailReceive (authData, getMailCount) {
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
          console.log(data)
          return resolve(data)
        })
      })
    })
    client.connect()
  })
}

export default {mailReceive, mailReceiveUser, getMailText}

// client.on('new', function(messages) {
//   client.listMessages(-1, function(err, messages){
//     messages.forEach(function(message){
//       console.log()
//       console.log(message.UID)
//       console.log('日時:\t\t' + message.date)
//       console.log('送信者:\t\t' + message.from.name + '-' + message.from.address)
//       console.log('タイトル:\t' + message.title)
//     })
//   })
// })

// client.connect()
