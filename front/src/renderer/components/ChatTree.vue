<template>
  <div id="chat_tree">
    <div id="tree__title">
      <h2>{{ targetUser.name }}</h2>
      <p>{{ targetUser.mail }}</p>
    </div>
    <div id="tree_frame">
      <div
        class="chat"
        v-for="(message, index) in messages"
        v-if="message.from.address === targetUser.mail"
        :key="index">
        <div :class="[userData.mail === message.from.address ? 'chat__send_me' : '', 'chat__frame receive']">
          <!-- <h5 class="chat__name">{{ message.name }}</h5> -->
          <p class="chat__title">{{ message.title }}</p>
        </div>
        <span class="chat__time">{{ dateFormat(new Date(message.date)) }}</span><!-- 時間に関してはメールサーバからの情報によって変更 -->
      </div>
    </div>
  </div>
</template>

<script>
  import MailReciver from '../utils/MailReceive'
  // モジュールをインポート
  const fs = require('fs')
  const isWindows = process.platform === 'win32'
  // デフォルトの実行ディレクトリの確認
  const HOMEDIR =
    process.env[isWindows ? 'USERPROFILE' : 'HOME']

  export default {
    name: 'Chattree',
    props: {
      targetUser: {},
      reroadTrigger: ''
    },
    data () {
      return {
        infomation: {
          directory: '/frankfrut/data/',
          fileName: '/userInformation.json',
          delimiter: '/'
        },
        messages: {},
        userData: {
          mail: '',
          name: ''
        }
      }
    },
    methods: {
      // ユーザーデータ（名前とメールアドレス）を取得
      getUserData () {
        // Windows用のパス形式で指定
        if (isWindows) {
          this.infomation.directory = '\\frankfrut\\data\\'
          this.infomation.delimiter = '\\'
        }
        // Win/Mac両対応のディレクトリを生成
        const targetDirectory = HOMEDIR + this.infomation.directory

        if (fs.existsSync(targetDirectory)) {
          console.log(targetDirectory + 'は存在します。')
          // ユーザー情報ファイルからデータを取得する
          let jsonObject = JSON.parse(fs.readFileSync(targetDirectory + this.infomation.delimiter + this.infomation.fileName, 'utf8'))
          this.userData.name = jsonObject['user']['name']
          this.userData.mail = jsonObject['smtp']['auth']['user']
        } else {
          console.log(targetDirectory + 'は存在しません。')
        }
      },
      // メールサーバーからメール一覧を取得してくる
      getReceiveEmail (serchTarget) {
        // Windows用のパス形式で指定
        if (isWindows) {
          this.infomation.directory = '\\frankfrut\\data\\'
          this.infomation.delimiter = '\\'
        }
        // Win/Mac両対応のディレクトリを生成
        const targetDirectory = HOMEDIR + this.infomation.directory

        if (fs.existsSync(targetDirectory)) {
          console.log(targetDirectory + 'は存在します。')
          // ユーザー情報ファイルからデータを取得する
          let jsonObject = JSON.parse(fs.readFileSync(targetDirectory + this.infomation.delimiter + this.infomation.fileName, 'utf8'))
          let AuthData = jsonObject['smtp']['auth']

          MailReciver.mailReceive(AuthData)
        } else {
          console.log(targetDirectory + 'は存在しません。')
        }
      },
      async searchMail (authData, targetAddress) {
        console.log(targetAddress)
        const numbers = await MailReciver.mailReceiveUser(authData, targetAddress)
        this.messages = await MailReciver.mailReceive(authData, numbers[numbers.length - 10]).then()
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
      }
    },
    watch: {
      // ユーザーデータが入力されたらそれを取得する
      reroadTrigger: function (newStatus, oldStatus) {
        if (newStatus === false) {
          this.getUserData()
        }
      }
    },
    mounted () {
      const self = this
      // メール一覧の取得
      fs.readFile(HOMEDIR + this.infomation.delimiter + 'frankfrut' + this.infomation.delimiter + 'data' + this.infomation.delimiter + 'userInformation.json', 'utf8', function (err, data) {
        // エラー処理
        if (err) {
          throw err
        }
        const userData = JSON.parse(data)

        // メール受信用の認証情報をオブジェクトに格納
        const authData = {
          auth: {
            user: userData['smtp'].auth.user,
            pass: userData['smtp'].auth.pass
          },
          imap: {
            host: userData['imap'].host,
            port: userData['imap'].port
          }
        }

        // メールを受信
        self.searchMail(authData, self.targetUser.mail)
      })
    }
  }
</script>

<style scoped lang="scss">
  #chat_tree {
    display: flex;
    flex-direction: column;
    background-color: #eeeeee;
    width: 450px;
    height: 100vh;
  }
  #tree_frame {
    width: 90%;
    height: 100vh;
    margin-left: 5%;
    overflow-y: scroll;
  }
  #tree__title{
    width: 96%;
    height: 80px;
    padding-left: 4%;
    background: #262626;
    color: #ffffff;
    font-weight: bold;
    h2{
      margin-top: 15px;
      font-size: 20px;
      line-height: 20px;
    }
    p{
      margin-top: 5px;
      font-size: 13px;
      line-height: 13px;
    }
  }

  $chat__time-fontsize: 10px;

  // チャット風UI
  .chat{
    // 送受信時間表記
    .chat__time{
      display: inline-block;
      width: 60px;
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
      background-color: #ffffff;
      color: #333333;
      border-radius: 10px 10px 10px 0;
      cursor: pointer;
      vertical-align: middle;
      .chat__name{
        font-weight: bold;
      }
      // .chat__title{

      // }
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
    }
  }

</style>