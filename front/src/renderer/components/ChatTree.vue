<template>
  <div id="chat_tree">
    <div id="tree_frame">
      <div
        class="chat"
        v-for="(message, index) in messages"
        :key="index">
        <div :class="[userData.mail === message.mail ? 'chat__send_me' : '', 'chat__frame ' + message.type]">
          <!-- <h5 class="chat__name">{{ message.name }}</h5> -->
          <p class="chat__title">{{ message.subject }}</p>
        </div>
        <span class="chat__time">{{ message.time }}</span><!-- 時間に関してはメールサーバからの情報によって変更 -->
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
    props: ['serchEmail', 'reroadTrigger'],
    data () {
      return {
        infomation: {
          directory: '/frankfrut/data/',
          fileName: '/userInformation.json',
          delimiter: '/'
        },
        userData: {
          name: 'TestUser',
          mail: 'user@test.com'
        },
        messages: { // テスト用データ
          '1': {
            subject: 'Testsubject1',
            name: 'testName1',
            mail: 'test@test.com',
            type: 'receive',
            mailID: '0001',
            time: '2020/11/02\n12:00'
          },
          '2': {
            subject: 'Testsubject1',
            name: 'TestUser',
            mail: 'user@test.com',
            type: 'thread',
            mailID: '0002',
            time: '2020/11/02\n12:00'
          },
          '3': {
            subject: 'Testsubject1',
            name: 'testName1',
            mail: 'test@test.com',
            type: 'thread',
            mailID: '0001',
            time: '2020/11/02\n12:00'
          }
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
      }
    },
    watch: {
      // ユーザーデータが入力されたらそれを取得する
      reroadTrigger: function (newStatus, oldStatus) {
        if (newStatus === false) {
          this.getUserData()
        }
      },
      serchEmail: function (newEmail, oldEmail) {
        // ここで検索する関数を書く
        console.log(newEmail)
        this.getReceiveEmail(newEmail)
      }
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
    overflow-y: scroll;
  }
  #tree_frame {
    width: 90%;
    height: 100vh;
    margin-left: 5%;
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
      color: #262626;
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