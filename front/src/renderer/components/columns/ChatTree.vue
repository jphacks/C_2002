<template>
  <div
    id="chat_tree">
    <div id="tree__title">
      <input
        type="text"
        v-model="targetUser.name"
        :readonly="nameEdit.flg">
      <span
        class="edit_button"
        @click="editName"
        v-if="nameEdit.flg">編集</span>
      <span
        class="edit_button"
        @click="saveName"
        v-else>保存</span>
      <p>{{ targetUser.mail }}</p>
    </div>
    <div
      id="tree_frame"
      ref="tree_frame">
      <div
        class="chat"
        v-for="(message, index) in messages"
        v-if="
          (message.from.address === targetUser.mail) ||
          ((message.from.address === authData['auth'].user) && (message.to[0].address === targetUser.mail))"
        :key="index">
        <div
          @click="openMailData(message)"
          :class="[authData['auth'].user === message.from.address ? 'chat__send_me' : '', 'chat__frame receive']">
          <p class="chat__title">{{ message.title }}</p>
        </div>
        <span class="chat__time">{{ dateFormat(new Date(message.date)) }}</span><!-- 時間に関してはメールサーバからの情報によって変更 -->
      </div>
    </div>
  </div>
</template>

<script>
  import MailReciver from '../../utils/MailReceive'
  import OS from '../../utils/OS'
  import ContactsList from '../../utils/ContactsList'
  // モジュールをインポート
  const fs = require('fs')
  const isWindows = process.platform === 'win32'
  // デフォルトの実行ディレクトリの確認
  const HOMEDIR =
    process.env[isWindows ? 'USERPROFILE' : 'HOME']

  export default {
    name: 'Chattree',
    props: {
      targetUser: {}
    },
    data () {
      return {
        messages: {},
        userData: {
          mail: '',
          name: ''
        },
        authData: {},
        nameEdit: {
          flg: true,
          prev: ''
        }
      }
    },
    methods: {
      async searchMail (authData, targetAddress) {
        console.log(targetAddress)
        const myNumbers = await MailReciver.mailReceiveUser(authData, authData['auth'].user)
        const targetNumbers = await MailReciver.mailReceiveUser(authData, targetAddress)
        const numbers = myNumbers.concat(targetNumbers)
        console.log(numbers)

        // メールを取得
        this.messages = await MailReciver.mailReceive(authData, numbers[numbers.length - 10])
      },
      dateFormat (date, format = 'YYYY-MM-DD hh:mm:ss') {
        // パース
        format = format.replace(/YYYY/g, date.getFullYear())
        format = format.replace(/MM/g, ('0' + (date.getMonth() + 1)).slice(-2))
        format = format.replace(/DD/g, ('0' + date.getDate()).slice(-2))
        format = format.replace(/hh/g, ('0' + date.getHours()).slice(-2))
        format = format.replace(/mm/g, ('0' + date.getMinutes()).slice(-2))
        format = format.replace(/ss/g, ('0' + date.getSeconds()).slice(-2))

        if (format.match(/S/g)) {
          let milliSeconds = ('00' + date.getMilliseconds()).slice(-3)
          let length = format.match(/S/g).length
          for (let i = 0; i < length; i++) format = format.replace(/S/, milliSeconds.substring(i, i + 1))
        }

        // 文字列を返す
        return format
      },
      openMailData (mailData) {
        console.log(mailData)
        this.$emit('getMailData', mailData)
      },
      editName () {
        this.nameEdit.prev = this.targetUser.name
        this.nameEdit.flg = false
      },
      saveName () {
        const self = this
        this.nameEdit.flg = true
        if (this.nameEdit.prev !== this.targetUser.name) {
          ContactsList.getAddress().then((userObj) => {
            // 名前を上書
            userObj[self.targetUser.mail].name = self.targetUser.name

            // 変更を保存
            ContactsList.updateAddress(userObj)
          })
        }
      }
    },
    watch: {
    },
    mounted () {
      const delimiter = OS.delimiterChar()
      const self = this
      // メール一覧の取得
      fs.readFile(HOMEDIR + delimiter + 'frankfrut' + delimiter + 'data' + delimiter + 'userInformation.json', 'utf8', function (err, data) {
        // エラー処理
        if (err) {
          throw err
        }
        // ユーザ情報のJSONをオブジェクトへ変換
        const userData = JSON.parse(data)

        // メール受信用の認証情報をオブジェクトに格納
        self.authData = {
          auth: {
            user: userData['auth'].user,
            pass: userData['auth'].pass
          },
          imap: {
            host: userData['imap'].host,
            port: userData['imap'].port
          }
        }

        // メールを受信
        self.searchMail(self.authData, self.targetUser.mail).then(function () {
          const chatLog = self.$refs.tree_frame
          if (!chatLog) return
          chatLog.scrollTop = chatLog.scrollHeight
        })
      })
    }
  }
</script>

<style scoped lang="scss">
  #chat_tree {
    display: flex;
    flex-direction: column;
    background-color: #333333;
    width: 450px;
    height: 100vh;
  }
  #tree_frame {
    width: 95%;
    height: 100vh;
    margin-left: 5%;
    overflow-y: scroll;
    padding-bottom: 20px;
  }
  #tree__title{
    width: 96%;
    height: 80px;
    padding-left: 4%;
    background: #222222;
    color: #ffffff;
    font-weight: bold;
    input[type="text"]{
      outline: none;
      border: none;
      background: none;

      color: #ffffff;
      margin-top: 12px;
      font-size: 20px;
      line-height: 20px;
      padding: 0;

      &:focus{
        outline: none;
        border: none;
      }
    }
    p{
      margin-top: 8px;
      font-size: 13px;
      line-height: 13px;
      color: #aaaaaa;
    }
    .edit_button{
      display: inline-block;
      text-decoration: underline;
      color: #aaaaaa;
      cursor: pointer;
    }
  }

  $chat__time-fontsize: 10px;

  // チャット風UI
  .chat{
    // 送受信時間表記
    .chat__time{
      display: inline-block;
      width: 60px;
      color: #aaaaaa;
      height: $chat__time-fontsize;
      line-height: $chat__time-fontsize;
      font-size: $chat__time-fontsize;
      vertical-align: middle;
      word-wrap:break-word;
    }
    // 吹き出し風ボックス
    .chat__frame {
      display: inline-block;
      margin: 1px 1px 0 10px;
      padding: 6px 20px;
      width: 250px;
      height: auto;
      background-color: #444444;
      color: #ffffff;
      border-radius: 10px 10px 10px 0;
      cursor: pointer;
      vertical-align: middle;
      -webkit-transition: all 0.3s ease;
      -moz-transition: all 0.3s ease;
      -o-transition: all 0.3s ease;
      transition: all  0.3s ease;

      // 自身の送信したメールスタイル
      &.chat__send_me{
        background-color: #5645ff;
        color: #ffffff;
        border-radius: 10px 10px 0 10px;
      }

      // 通常メールスタイル
      &.receive{
        margin: 20px 40px 0 0;
      }

      // 返信メール（スレッド）スタイル
      &.thread{
        margin: 0 10px 0 30px;
      }

      // ホバー
      &:hover{
        opacity: .7;
      }
    }
  }

</style>