const inbox = require('inbox')

function mailReceive(userData, getMailCount=10){

    const client = inbox.createConnection(false, 'imap.gmail.com', {
        secureConnection: true,
        userData
    })

    client.on('connect', function() {
        client.openMailbox('INBOX', function(error, info) {
            if(error) throw error
            console.log('Successfully connected to server')
            client.listMessages(-getMailCount, function(err, messages){
                messages.forEach(function(message){
                    console.log()
                    console.log(message.UID)
                    console.log('日時:\t\t' + message.date)
                    console.log('送信者:\t\t' + message.from.name + '-' + message.from.address)
                    console.log('タイトル:\t' + message.title)
                })
                return messages
            })
        })
    })
    client.connect()
}
/*
client.on('new', function(messages) {
    client.listMessages(-1, function(err, messages){
        messages.forEach(function(message){
            console.log()
            console.log(message.UID)
            console.log('日時:\t\t' + message.date)
            console.log('送信者:\t\t' + message.from.name + '-' + message.from.address)
            console.log('タイトル:\t' + message.title)
        })
    })
})

client.connect()
*/