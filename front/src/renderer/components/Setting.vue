<template>
  <div id="setting_frame">
    <div id="mail_cliant_frame" v-if="!flag.isOther && !flag.isEnroll">
      <div class="mail_cliant" @click="dispInfoBox('gmail')">
        <span>Google</span>
      </div>
      <div class="mail_cliant" @click="dispInfoBox('yahoo')">
        <span>Yahoo!</span>
      </div>
      <div class="mail_cliant" @click="dispInfoBox('outlook')">
        <span>Outlook</span>
      </div>
      <div class="mail_cliant" @click="dispInfoBox('icloud')">
        <span>iCloud</span>
      </div>
      <div class="mail_cliant" @click="dispInfoBox('other')">
        <span>その他</span>
      </div>
    </div>
    <div id="mail_cliant_frame" v-else-if="flag.isOther && !flag.isEnroll">
      <div class="input_frame">
        <span class="client_title" style="margin-bottom: 10px">SMTP</span>
        <div>
          <span>HOST</span>
          <input type="text" v-model="jsonData.smtp.host">
          <span>PORT</span>
          <input type="number" v-model="jsonData.smtp.port">
        </div>
      </div>
      <div class="input_frame" v-if="flag.isIMAP">
        <span class="client_title_imap" style="margin-bottom: 10px">IMAP</span>
        <div>
          <span>HOST</span>
          <input type="text" v-model="jsonData.imap.host">
          <span>PORT</span>
          <input type="number" v-model="jsonData.imap.port">
        </div>
      </div>
      <div class="input_frame" v-else>
        <span class="client_title_pop" style="margin-bottom: 10px">POP</span>
        <div>
          <span>HOST</span>
          <input type="text" v-model="jsonData.pop.host">
          <span>PORT</span>
          <input type="number" v-model="jsonData.pop.port">
        </div>
      </div>
      <div class="switch_frame">
        <div class="btn" v-if="flag.isIMAP" @click="switchImapFlag">
          <span class="client_title_pop">POP</span>
        </div>
        <div class="btn" v-else @click="switchImapFlag">
          <span class="client_title_imap">IMAP</span>
        </div>
        <div class="btn" @click="moveOn">
          <span>登録</span>
        </div>
      </div>
    </div>
    <div id="mail_cliant_frame" v-else-if="flag.isEnroll">
      <div class="user_content">
        <span>ユーザー名</span>
        <input type="text" v-model="jsonData.user.name">
      </div>
      <div class="user_content">
        <span>所属</span>
        <input type="text" v-model="jsonData.user.affiliation">
      </div>
      <div class="user_content">
        <span>メールアドレス</span>
        <input type="email" v-model="jsonData.auth.user">
      </div>
      <div class="user_content">
        <span>パスワード</span>
        <input type="password" v-model="jsonData.auth.pass">
      </div>
      <div class="submit_btn" @click="CreateJSON">
          <span>登録</span>
      </div>
    </div>
  </div>
</template>

<script>
  import FileAction from '../utils/FileAction'
  import MailAuth from '../assets/json/MailAuth.json'
  const fs = require('fs')
  
  const isWindows = process.platform === 'win32'
  // デフォルトの実行ディレクトリの確認
  const HOMEDIR =
    process.env[isWindows ? 'USERPROFILE' : 'HOME']

  export default {
    name: 'Setting',
    data () {
      return {
        infomation: {
          directory: '/frankfrut/data/',
          fileName: '/userInformation.json',
          delimiter: '/'
        },
        flag: {
          isIMAP: false,
          isOther: false,
          isEnroll: false
        },
        jsonData: {
          smtp: {
            host: '',
            port: 0,
            secure: true
          },
          imap: {
            host: '',
            port: 0
          },
          pop: {
            host: '',
            port: 0
          },
          user: {
            name: '',
            affiliation: ''
          },
          auth: {
            user: '',
            pass: ''
          }
        }
      }
    },
    methods: {
      async CreateJSON () {
        // Windows用のパス形式で指定
        if (isWindows) {
          this.infomation.directory = '\\frankfrut\\data\\'
          this.infomation.delimiter = '\\'
        }
        // Win/Mac両対応のディレクトリを生成
        const targetDirectory = HOMEDIR + this.infomation.directory

        // 作業ディレクトリの作成
        await FileAction.mkdir(targetDirectory)
        fs.writeFileSync(targetDirectory + this.infomation.delimiter + this.infomation.fileName, JSON.stringify(this.jsonData, null, '    ', function (err) { // jsonファイル
          if (err) { throw err }
        }))

        this.$router.push('/')
      },
      moveOn () {
        this.flag.isEnroll = true
      },
      switchImapFlag () {
        this.flag.isIMAP = !this.flag.isIMAP
      },
      async dispInfoBox (client) {
        console.log(client)
        if (client === 'other') {
          this.flag.isOther = true
        } else {
          this.flag.isEnroll = true
          this.jsonData.smtp.host = MailAuth[client]['smtp']['host']
          this.jsonData.smtp.port = MailAuth[client]['smtp']['port']
          this.jsonData.imap.host = MailAuth[client]['imap']['host']
          this.jsonData.imap.port = MailAuth[client]['imap']['port']
          this.jsonData.pop.host = MailAuth[client]['pop']['host']
          this.jsonData.pop.port = MailAuth[client]['pop']['port']
        }
      }
    }
  }
</script>

<style scoped lang="scss">
  #setting_frame{
    display: flex;
    align-items: center;
    justify-content: center; 
    width: 100%;
    height: 100vh;
    background-color: #333333;
    #mail_cliant_frame{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      width: 90%;
      height: 90vh;
      margin-left: 60px;
      border-radius: 5px;
      background-color: #444444;
      overflow-y: scroll;
      color: #cccccc;
      font-size: 2rem;
      .input_frame{
        width: auto;
        height: auto;
        padding: 15px;
        border-radius: 5px;
        background-color: #222222;
        margin: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        input{
          margin: 0 5px 0 5px;
          font-size: 1.5rem;
          width: 30%;
          border-radius: 7px;
        }
      }
      .switch_frame{
        width: auto;
        height: auto;
        margin: 10px;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-around;
        .btn{
          display: flex;
          align-items: center;
          justify-content: center;
          width: 85px;
          margin: 15px;
          padding: 10px;
          border-radius: 7px;
          border: solid 5px #222222;
          background-color: #222222;
          &:hover{
            transition: 0.15s ;
            border: solid 5px #80ffff;
          }
        }
      }
      .user_content{
        font-size: 1.2rem;
        min-width: 400px;
        max-width: 700px;
        width: auto;
        height: auto;
        padding: 15px;
        border-radius: 5px;
        background-color: #222222;
        margin: 5px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content:flex-start;
        input{
          margin-top:10px;
          font-size: 1.5rem;
          height: auto;
          width: 90%;
          border-radius: 7px;
        }
      }
      .submit_btn{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 85px;
        margin: 15px;
        padding: 10px;
        border-radius: 7px;
        border: solid 5px #222222;
        background-color: #222222;
        &:hover{
          transition: 0.15s ;
          border: solid 5px #80ffff;
        }
      }
    }
  }
  .client_title{
    color: #efefef;
    font-weight: 600;
  }
  .client_title_imap{
    color: #ffddcc;
    font-weight: 600;
  }
  .client_title_pop{
    color: #ccffee;
    font-weight: 600;
  }
  .mail_cliant{
    margin: 15px 0 15px 0; 
    display: flex;
    align-items: center;
    justify-content: center;
    max-width: 600px;
    min-width: 400px;
    width: 40%;
    height: 200px;
    border: solid 2px #777777;
    border-radius: 5px;
    background-color: #222222;
    cursor: pointer;
    span{
      color: #efefef;
      font-size: 2rem;
      font-weight: 500;
    }
    &:hover{
      transition: 0.15s ;
      border: solid 7px #80ffff;
    }
  }
</style>