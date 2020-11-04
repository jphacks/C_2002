const inbox = require('inbox')

// メール受信関数
async function mailReceive (userData, getMailCount = 10) {
  return new Promise(resolve => {
    const client = inbox.createConnection(false, 'imap.gmail.com', {
      secureConnection: true,
      auth: {
        user: userData['user'],
        pass: userData['pass']
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
          messages.forEach(function (message) {
            console.log(message)
          })
          return resolve(messages)
        })
      })
    })
    client.connect()
  })
}

export default {mailReceive}

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
