<template>
  <div id="setting_frame">
    <div id="select_service" class="mail_cliant_frame" v-if="!fileCheck">

      <h2>メールサービスを選択してください</h2>

      <div class="mail_cliant" @click="dispInfoBox('gmail')">
        Gmail
      </div>
      <div class="mail_cliant" @click="dispInfoBox('yahoo')">
        Yahoo!
      </div>
      <div class="mail_cliant" @click="dispInfoBox('outlook')">
        Outlook.com
      </div>
      <div class="mail_cliant" @click="dispInfoBox('icloud')">
        iCloud
      </div>
      <div class="mail_cliant" @click="dispInfoBox('other')">
        その他
      </div>
    </div>
    <div class="mail_cliant_frame" v-else-if="userObj['type'] === 'other'">
      <div class="input_frame">
        <h3 class="client_title" style="margin-bottom: 10px">SMTP</h3>
        <div>
          <h3>HOST</h3>
          <input type="text" v-model="jsonData.smtp.host">
          <h3>PORT</h3>
          <input type="number" v-model="jsonData.smtp.port">
        </div>
      </div>
      <div class="input_frame" v-if="flag.isIMAP">
        <h3 class="client_title_imap" style="margin-bottom: 10px">IMAP</h3>
        <div>
          <h3>HOST</h3>
          <input type="text" v-model="jsonData.imap.host">
          <h3>PORT</h3>
          <input type="number" v-model="jsonData.imap.port">
        </div>
      </div>
      <div class="input_frame" v-else>
        <h3 class="client_title_pop" style="margin-bottom: 10px">POP</h3>
        <div>
          <h3>HOST</h3>
          <input type="text" v-model="jsonData.pop.host">
          <h3>PORT</h3>
          <input type="number" v-model="jsonData.pop.port">
        </div>
      </div>
      <div class="switch_frame">
        <div class="btn" v-if="flag.isIMAP" @click="switchImapFlag">
          <h3 class="client_title_pop">POP</h3>
        </div>
        <div class="btn" v-else @click="switchImapFlag">
          <h3 class="client_title_imap">IMAP</h3>
        </div>
        <div class="btn" @click="updateUser">
          登録
        </div>
      </div>
    </div>
    <div class="mail_cliant_frame" v-else>
      <h2>認証情報</h2>
      <h3>メールアドレス</h3>
      <input type="email" v-model="userObj['auth'].user">
      <h3>パスワード</h3>
      <input type="password" v-model="userObj['auth'].pass">

      <h2>連絡先情報</h2>
      <h3>氏 名</h3>
      <input type="text" v-model="userObj['user'].name">
      <h3>所属（学校 / 会社）</h3>
      <input type="text" v-model="userObj['user'].affiliation">
      <div class="btn" @click="updateUser">
        登録
      </div>
    </div>
  </div>
</template>

<script>
  import FileAction from '../utils/FileAction'
  import MailAuth from '../assets/json/MailAuth.json'
  import OS from '../utils/OS'
  const fs = require('fs')

  export default {
    name: 'Setting',
    data () {
      return {
        fileCheck: true,
        userObj: {},
        mailAuth: MailAuth,
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
      async UpdateJSON () {
        return new Promise(resolve => {
          // ファイルのパスを取得
          const delimiter = OS.delimiterChar()
          const filePath = OS.homeDirectory() + delimiter + 'frankfrut' + delimiter + 'data' + delimiter + 'userInformation.json'

          // オブジェクトをJSONへ変換
          const userJSON = JSON.stringify(this.userObj)

          // ファイルへの書き込み
          const optionJson = { flag: 'w' }
          fs.writeFile(filePath, userJSON, optionJson, function (err) {
            if (err) {
              console.log(err)
            }
            return resolve(0)
          })
        })
      },
      updateUser () {
        const self = this
        // JSONをアップデート
        this.UpdateJSON().then(() => {
          // 完了後ホームへ戻る
          self.$router.push('/')
        })
      },
      switchImapFlag () {
        this.flag.isIMAP = !this.flag.isIMAP
      },
      dispInfoBox (client) {
        // メールサービスの確定
        this.userObj['type'] = client
        if (!(client === 'other')) {
          console.log('start')
          this.userObj['smtp'].host = this.mailAuth[client]['smtp'].host
          this.userObj['smtp'].port = this.mailAuth[client]['smtp'].port
          this.userObj['imap'].host = this.mailAuth[client]['imap'].host
          this.userObj['imap'].port = this.mailAuth[client]['imap'].port
          this.userObj['pop'].host = this.mailAuth[client]['pop'].host
          this.userObj['pop'].port = this.mailAuth[client]['pop'].port
          console.log('fin')
        }
        // JSONのアップデート
        this.UpdateJSON()
        this.fileCheck = true
      }
    },
    mounted () {
      // ファイルのパスを取得
      const delimiter = OS.delimiterChar()
      const filePath = OS.homeDirectory() + delimiter + 'frankfrut' + delimiter + 'data' + delimiter + 'userInformation.json'
      const self = this

      if (!fs.existsSync(filePath)) {
        this.fileCheck = false

        // ディレクトリの作成
        FileAction.mkdir(OS.homeDirectory() + delimiter + 'frankfrut' + delimiter + 'data').then(() => {
          // ファイルの作成
          fs.writeFile(filePath, '', '', function (err) {
            if (err) {
              console.log(err)
            }
            self.userObj = {
              type: '',
              smtp: {
                host: '',
                port: '',
                secure: true
              },
              imap: {
                host: '',
                port: ''
              },
              pop: {
                host: '',
                port: ''
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
          })
        })
      } else {
        this.fileCheck = true

        // ファイルの読み込み
        fs.readFile(filePath, 'utf8', function (err, addressJSON) {
          // エラー処理
          if (err) {
            console.log(err)
          }

          // JSONからオブジェクトへの変換
          self.userObj = JSON.parse(addressJSON)
        })
      }
    }
  }
</script>

<style scoped lang="scss">
  .mail_cliant_frame{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100vh;
    overflow-y: scroll;

    h2{
      text-align: center;
      color: #ffffff;
      font-size: 25px;
      margin-bottom: 30px;
    }

    // ラベルスタイル
    h3{
      display: block;
      text-align: center;
      margin: 20px 0 10px;
      color: #ffffff;
    }
    
    // ボタンスタイル
    .btn{
      display: flex;
      align-items: center;
      justify-content: center;
      width: 85px;
      margin: 15px 0 0;
      padding: 10px;
      color: #ffffff;
      background: #222222;
      cursor: pointer;

      -webkit-transition: all 0.3s ease;
      -moz-transition: all 0.3s ease;
      -o-transition: all 0.3s ease;
      transition: all  0.3s ease;

      &:hover{
        background: #5645ff;
      }
    }

    // 入力フォームスタイル
    input[type="text"], input[type="email"], input[type="password"]{
      // リセット
      background: none;
      outline: none;

      border: solid 1px #ffffff;
      border-radius: 7px;
      margin: 0 5px 0 5px;
      width: 350px;
      height: 40px;
      line-height: 40px;
      font-size: 20px;
      text-align: center;
      color: #ffffff;
    }
  }

  #setting_frame{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100vh;
    background-color: #333333;
  }

  // メールサービス選択のUI
  #select_service{
    .mail_cliant{
      margin: 15px 0 15px 0;
      width: 300px;
      height: 50px;
      line-height: 50px;
      text-align: center;
      border-radius: 10px;
      color: #ffffff;
      background-color: #222222;
      font-size: 20px;
      cursor: pointer;
      -webkit-transition: all 0.3s ease;
      -moz-transition: all 0.3s ease;
      -o-transition: all 0.3s ease;
      transition: all  0.3s ease;

      &:hover{
        background: #5645ff;
      }
    }
  }
</style>