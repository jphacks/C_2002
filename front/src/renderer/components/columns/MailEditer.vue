<template>
  <div id="MailEditor">
    <input
      class="editor__input"
      type="text"
      v-model="mailData.destination"
      placeholder="宛先"
      autocomplete="on"
      list="addressList">
    <datalist id="addressList">
      <option
        v-for="address in addressList"
        :key="address.name">{{address.mail}}</option>
    </datalist>

    <input
      class="editor__input"
      type="text"
      maxlength="50"
      v-model="mailData.subject"
      placeholder="件名">

    <div id="editor__body">
      <VueComplete
        v-if="mailBodyInitFlg"
        :mailBody="mailBodyInit"
        @bodyEnterAction="bodyEnterAction"
        @bodyDeleteAction="bodyDeleteAction"
        @sendMail="sendMail"
        @value="mailData.body = $event">
      </VueComplete>
    </div>

    <div id="editor__contents">
      <button @click="sendMail">送信</button>
      <label
        class="attach_file"
        title="添付ファイルを追加">
        <input
          type="file"
          @change="addFile">
      </label>
      <div class="switch_span">
        <p>校正モード</p>
        <div class="toggle-switch">
          <input
            id="toggle"
            class="toggle-input"
            type="checkbox"
            v-model="proofread"
            checked/>
          <label for="toggle" class="toggle-label"/>
          <span></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  // for Vue
  import GitCommand from '../../utils/NodeGit'
  import FileAction from '../../utils/FileAction'
  import axios from 'axios'
  import DiffParser from '../../utils/DiffParser'
  import OS from '../../utils/OS'
  import VueComplete from '../module/TextArea'
  import ContactsList from '../../utils/ContactsList'

  const fs = require('fs')

  const isWindows = process.platform === 'win32'

  // デフォルトの実行ディレクトリの確認
  const HOMEDIR =
    process.env[isWindows ? 'USERPROFILE' : 'HOME']

  // Vue.js
  export default {
    name: 'MailEditer',
    components: {
      VueComplete
    },
    props: {
      draftID: '',
      replace: {
        target: '',
        update: '',
        timestamp: 0
      },
      attachFileUpdate: {}
    },
    data () {
      return {
        proofread: true,
        draft: {
          directory: '/frankfrut/draft/',
          fileName: '/draft.txt',
          resultName: 'result.txt',
          delimiter: '/'
        },
        commitID: '',
        mailData: {
          subject: '',
          destination: '',
          body: '',
          bodyLINE: 0,
          bodyLength: 0,
          resultBody: '',
          resultSubject: ''
        },
        breakChar: '\n',
        addressList: {},
        attachmentFile: {
          data: {},
          count: 0
        },
        userCtrCheck: {
          ID: '',
          time: 4000
        },
        nounList: {
          people: [],
          companies: []
        },
        mailBodyInit: '',
        mailBodyInitFlg: false
      }
    },
    methods: {
      async saveDraft () { // 下書きの上書き
        const draftDirectory = HOMEDIR + this.draft.directory + this.draftID

        // ファイルへの書き込み
        const optionJson = { flag: 'w' }
        await fs.writeFile(draftDirectory + this.draft.delimiter + this.draft.fileName, this.mailData.body, optionJson, function (err) {
          if (err) { throw err }
        })

        // 差分の取得
        const diffStd = await GitCommand.gitDiff('', draftDirectory)
        const diffObj = DiffParser.diffParse(diffStd)

        // git add
        await GitCommand.gitAdd('.', draftDirectory)

        // git commit
        const commitMessage = Date.now() + ' draft commit'
        await GitCommand.gitCommit(commitMessage, draftDirectory)

        // commit ID の取得
        diffObj['commit_id'] = await GitCommand.getCommitID(HOMEDIR + this.draft.directory + this.draftID)

        return diffObj
      },
      async convertHonorific (commitID, sentence, key) { // 校正処理
        const API = 'http://54.64.167.36:5000/postchange'
        // 送信用のJSONの作成
        const sendJSON = {'commit_id': commitID, 'sentence': sentence}
        const self = this
        // APIへPOST
        await axios.post(API, sendJSON, {
          headers: {
            'Content-Type': 'application/json'
          }
        })
          .then((res) => {
            // レスポンスが200の時の処理
            console.log(res)
            // 新企業を追加
            FileAction.addLINE(
              HOMEDIR + self.draft.directory + self.draftID + self.draft.delimiter + self.draft.resultName,
              Number(key),
              res.data['change_sentence']
            ).then(self.updatePreview)
          })
          .catch(err => {
            console.log(err)
            if (err.response) {
              // レスポンスが200以外の時の処理
            }
          })
      },
      async autoUpdate () {
        const regexp = new RegExp(this.breakChar + '(.*?)', 'g')
        const breakPoints = (this.mailData.body.match(regexp) || []).length

        // 行数に変化があった場合
        this.mailData.bodyLINE = breakPoints
        const self = this

        // 差分オブジェクトを取得
        const diffObj = await this.saveDraft()

        // 削除行を取得
        let keysArr = []
        Object.keys(diffObj.remove).forEach(function (key) {
          keysArr.push(key)
        })
        const keyLength = keysArr.length
        // 後ろの行から取り出し
        for (let i = keyLength - 1; i >= 0; i--) {
          console.log(keysArr[i] + ' remove : ' + diffObj.remove[keysArr[i]])
          await FileAction.deleteLINE(HOMEDIR + self.draft.directory + self.draftID + self.draft.delimiter + self.draft.resultName, Number(keysArr[i]))
        }

        // 追加部分の追加
        Object.keys(diffObj.add).forEach(function (key) {
          console.log(key + ' add : ' + diffObj.add[key])
          if (diffObj.add[key] !== '') {
            self.convertHonorific(diffObj['commit_id'], diffObj.add[key], key)
          }
        })

        // プレビューの更新
        this.updatePreview()
      },
      async bodyEnterAction () { // Enterキーが押されたときの処理
        const regexp = new RegExp(this.breakChar + '(.*?)', 'g')
        if (this.mailData.bodyLength + 1 < this.mailData.body.length) {
          if (this.mailData.bodyLINE !== (this.mailData.body.match(regexp) || []).length) {
            // タイムアウトの停止
            clearTimeout(this.userCtrCheck.ID)

            this.mailData.bodyLINE = (this.mailData.body.match(regexp) || []).length
            const self = this

            // 差分オブジェクトを取得
            const diffObj = await this.saveDraft()

            // 抜き出し
            Object.keys(diffObj.add).forEach(function (key) {
              console.log(key + '/' + diffObj.add[key])
              if (diffObj.add[key] !== '') {
                self.convertHonorific(diffObj['commit_id'], diffObj.add[key], key)
              }
            })
          }
        } else {
          // 作業ディレクトリの定義
          const draftDirectory = HOMEDIR + this.draft.directory + this.draftID

          // ファイルへの書き込み
          const optionJson = { flag: 'w' }
          await fs.writeFile(draftDirectory + this.draft.delimiter + this.draft.fileName, this.mailData.body, optionJson, function (err) {
            if (err) { throw err }
          })

          // git add
          await GitCommand.gitAdd('.', draftDirectory)

          // git commit
          const commitMessage = Date.now() + ' draft commit'
          await GitCommand.gitCommit(commitMessage, draftDirectory)
        }
        this.mailData.bodyLength = this.mailData.body.length

        // プレビューの更新
        this.updatePreview()
      },
      async bodyDeleteAction () { // デリートキーが押されたときの処理
        const regexp = new RegExp(this.breakChar + '(.*?)', 'g')
        const breakPoints = (this.mailData.body.match(regexp) || []).length

        // 行数に変化があった場合
        if (this.mailData.bodyLINE !== breakPoints) {
          // タイムアウトの停止
          clearTimeout(this.userCtrCheck.ID)

          this.mailData.bodyLINE = breakPoints
          const self = this

          // 差分オブジェクトを取得
          const diffObj = await this.saveDraft()

          // 削除行を取得
          let keysArr = []
          Object.keys(diffObj.remove).forEach(function (key) {
            keysArr.push(key)
          })
          const keyLength = keysArr.length
          // 後ろの行から取り出し
          for (let i = keyLength - 1; i >= 0; i--) {
            console.log(keysArr[i] + ' remove : ' + diffObj.remove[keysArr[i]])
            await FileAction.deleteLINE(HOMEDIR + self.draft.directory + self.draftID + self.draft.delimiter + self.draft.resultName, Number(keysArr[i]))
          }

          // 追加部分の追加
          Object.keys(diffObj.add).forEach(function (key) {
            console.log(key + ' add : ' + diffObj.add[key])
            if (diffObj.add[key] !== '') {
              self.convertHonorific(diffObj['commit_id'], diffObj.add[key], key)
            }
          })
        }

        // プレビューの更新
        this.updatePreview()
      },
      updatePreview () {
        const self = this

        // 校正結果の取得と反映
        fs.readFile(HOMEDIR + this.draft.directory + this.draftID + this.draft.delimiter + this.draft.resultName, 'utf8', function (err, data) {
          // エラー処理
          if (err) {
            throw err
          }
          console.log('updated : ' + data)
          // 変更結果を代入
          self.mailData.resultBody = data

          // 親コンポーネントへ渡す
          self.$emit('updateBody', self.mailData.resultBody)
        })

        // 人物一覧の取得
        console.log('1')
        this.updateNumbers(this.mailData.body)
      },
      updateNumbers (mailBody) { // 数値データのアップデート
        const API = 'http://54.64.167.36:5000/postnames'
        // 送信用のJSONの作成
        const sendJSON = {'sentence': mailBody}
        const self = this
        // APIへPOST
        axios.post(API, sendJSON, {
          headers: {
            'Content-Type': 'application/json'
          }
        })
          .then((res) => {
            // レスポンスが200の時の処理
            console.log(res)
            // 人物が返ってきた場合
            if (res.data['people_name_list'].length) {
              self.nounList.people = res.data['people_name_list']
            }

            // 会社・団体名が返ってきた場合
            if (res.data['companies_name_list'].length) {
              self.nounList.companies = res.data['companies_name_list']
            }
          })
          .catch(err => {
            console.log(err)
            if (err.response) {
              // レスポンスが200以外の時の処理
            }
          })
      },
      sendMail () { // メール送信処理
        const self = this

        // SMTP情報を取得
        fs.readFile(HOMEDIR + this.draft.delimiter + 'frankfrut' + this.draft.delimiter + 'data' + this.draft.delimiter + 'userInformation.json', 'utf8', function (err, data) {
          // エラー処理
          if (err) {
            throw err
          }
          const userData = JSON.parse(data)

          // 校正を渡すか分岐
          let sendText = ''
          let sendSubject = ''
          if (self.proofread) {
            sendText = self.mailData.resultBody
            sendSubject = self.mailData.resultSubject
          } else {
            sendText = self.mailData.body
            sendSubject = self.mailData.subject
          }

          // 送信内容オブジェクトの作成
          let mailData = {
            from: '"' + userData['user'].affiliation + ' ' + userData['user'].name + '" <' + userData['auth'].user + '>',
            to: self.mailData.destination,
            bcc: userData['auth'].user,
            subject: sendSubject,
            text: sendText
          }

          // 添付ファイルの追加処理
          if (self.attachmentFile.count > 0) {
            for (let i = 0; i < self.attachmentFile.count; i++) {
              mailData['attachments'] = {
                filename: self.attachmentFile.data[i].name,
                path: self.attachmentFile.data[i].path
              }
            }
          }

          // 認証情報オブジェクトの作成
          const authData = {
            'smtp': {
              'host': userData['smtp'].host,
              'port': userData['smtp'].port,
              'secure': userData['smtp'].secure,
              'auth': {
                'user': userData['auth'].user,
                'pass': userData['auth'].pass
              }
            }
          }

          // メールデータを渡す
          self.$router.push({
            name: 'tray',
            query: {
              userData: self.addressList[self.mailData.destination],
              mailData: mailData,
              authData: authData['smtp'],
              timestamp: new Date(),
              draftID: self.draftID
            }})
        })
      },
      addFile (event) {
        console.log('File Event')
        console.log(event)
        // 添付ファイル追加処理
        const files = event.target.files || event.dataTransfer.files

        console.log(files)
        console.log('this.attachmentFile')
        console.log(this.attachmentFile)
        // ファイル情報を格納
        this.attachmentFile.data[this.attachmentFile.count] = {
          name: files[0].name,
          path: files[0].path,
          size: files[0].size,
          type: files[0].type
        }

        // ファイル数をカウント
        this.attachmentFile.count++
        console.log(this.attachmentFile)

        // デバッグ用出力
        console.log(files)
      },
      getDraft () {
        // 下書きのディレクトリを定義
        const draftDirectory = HOMEDIR + this.draft.directory + this.draftID
        const self = this

        // 下書きファイルの取得
        fs.readFile(draftDirectory + OS.delimiterChar() + 'draft.txt', 'utf8', function (err, draftText) {
          if (err) {
            console.log(err)
            setTimeout(
              self.getDraft,
              200
            )
          }
          // 代入
          console.log('draftText')
          console.log(draftText)
          self.mailBodyInit = draftText
          self.mailData.body = draftText
          self.mailBodyInitFlg = true
        })

        // 下書きヘッダファイルの取得
        fs.readFile(draftDirectory + OS.delimiterChar() + 'header.txt', 'utf8', function (err, headerJSON) {
          if (err) {
            console.log(err)
            setTimeout(
              self.getDraft,
              200
            )
          }

          // JSONからオブジェクトへ変換
          const headerObj = JSON.parse(headerJSON)

          // 値を設定
          self.mailData.subject = headerObj.subject.original
          self.mailData.resultSubject = headerObj.subject.result
          self.attachmentFile = headerObj.attachmentFile
          self.mailData.destination = headerObj.destination
          self.$emit('updateSubject', self.mailData.resultSubject)
        })
      },
      updateHeader () {
        // 下書きのディレクトリを定義
        const draftDirectory = HOMEDIR + this.draft.directory + this.draftID

        // オブジェクトに格納
        const headerObj = {
          subject: {
            original: this.mailData.subject,
            result: this.mailData.resultSubject
          },
          attachmentFile: this.attachmentFile,
          destination: this.mailData.destination
        }

        // オブジェクトからJSONへ変更
        const headerJSON = JSON.stringify(headerObj)

        // ファイルの上書
        const optionJson = { flag: 'w' }
        fs.writeFile(draftDirectory + OS.delimiterChar() + 'header.txt', headerJSON, optionJson, function (err) {
          if (err) {
            console.log(err)
          }
        })
      }
    },
    watch: {
      'mailData.subject': function (newval, oldval) {
        // 初期パラメータが存在する場合タイトルの校正はしない
        console.log('this.mailData.subject.indexOf(\'Re: \') : ' + this.mailData.subject.indexOf('Re: '))
        if (this.mailData.subject.indexOf('Re: ') === 0) {
          this.mailData.resultSubject = this.mailData.subject
          this.$emit('updateSubject', this.mailData.subject)
          this.updateHeader()
          return
        }

        // APIのURL
        const API = 'http://54.64.167.36:5000/postchange'
        const self = this

        // 件名が短いときはAPIを通さない
        if (this.mailData.subject.length < 4) {
          this.$emit('updateSubject', this.mailData.subject)
        } else {
          // 送信用のJSONの作成
          const sendJSON = {'commit_id': 'subject', 'sentence': this.mailData.subject}
          // APIへPOST
          return axios.post(API, sendJSON, {
            headers: {
              'Content-Type': 'application/json'
            }
          })
            .then((res) => {
              console.log(res)
              self.mailData.resultSubject = res.data['change_sentence']
              self.$emit('updateSubject', res.data['change_sentence'])
              self.updateHeader()
            })
            .catch(err => {
              console.log(err)
              if (err.response) {
                // レスポンスが200以外の時の処理
              }
            })
        }
      },
      'mailData.destination': function (newval, oldval) {
        this.updateHeader()
      },
      'mailData.body': function (newval, oldval) {
        // タイムアウトの停止
        clearTimeout(this.userCtrCheck.ID)

        // タイムアウトの設定
        const self = this
        this.userCtrCheck.ID = setTimeout(
          function () {
            self.autoUpdate()
          },
          this.userCtrCheck.time
        )
      },
      'attachmentFile.count': function (newval, oldval) {
        console.log(this.attachmentFile)
        this.$emit('attachFile', this.attachmentFile)
        this.updateHeader()
      },
      'replace.timestamp': function (newval, oldval) {
        while (this.mailData.body.indexOf(this.replace.target) !== -1) {
          this.mailBodyInit = this.mailData.body.replace(this.replace.target, this.replace.update)
        }
      },
      'attachFileUpdate.count': function (newval, oldval) {
        this.attachmentFile = this.attachFileUpdate
        this.updateHeader()
      },
      proofread: function (newval, oldval) {
        this.$emit('proofread', newval)
      },
      'nounList.people': function (newval, oldval) {
        this.$emit('updateNounList', this.nounList)
      },
      'nounList.companies': function (newval, oldval) {
        this.$emit('updateNounList', this.nounList)
      }
    },
    mounted () {
      // 改行コードの設定
      this.breakChar = OS.breakChar()

      // 下書きの取得
      this.getDraft()

      // 連絡先の取得
      const self = this
      ContactsList.getAddress().then(addressObj => {
        console.log('addressobj : ')
        console.log(addressObj)
        self.addressList = addressObj
      })
    }
  }
</script>

<style lang="scss">
  // 全体スタイル
  #MailEditor{
    width: 600px;
    color: #ffffff;
  }

  // テキスト入力部分のスタイル
  .editor__input{
    // スタイルのリセット
    outline: none;
    border: none;
    // スタイル
    width: 94%;
    padding: 0 3%;
    font-size: 17px;
    line-height: 40px;
    border-bottom: 1px solid #888888;
    background: none;
    color: #ffffff;
  }
  #addressList{
    color: #ffffff;
    background: #222222;
  }

  // 本文編集部分
  #editor__body{
    outline: none;
    border: none;
    resize: none;
    width: 94%;
    height: calc(100vh - 10px - 140px);
    margin: 5px 0 0 3%;
    /*
    font-size: 17px;
    line-height: 26px;
    overflow-y: scroll;
    background: none;
    color: #ffffff;
     */
    &:focus{
      outline: none;
    }
  }

  // 下部メニューバー
  $ui-size: 35px;
  #editor__contents{
    width: 100%;
    height: $ui-size + 10;
    border-top: solid 2px #888888;

    button{
      display: inline-block;
      width: 70px;
      height: $ui-size;
      margin: 7px 0 0 7px;
      vertical-align: top;
      border-radius: 5px;
      background: #5645ff;
      text-align: center;
      color: #ffffff;
      font-weight: bold;
      -webkit-transition: all 0.3s ease;
      -moz-transition: all 0.3s ease;
      -o-transition: all 0.3s ease;
      transition: all  0.3s ease;

      &:hover{
        opacity: .7;
      }
    }

    // ファイル添付ボタン
    .attach_file{
      display: inline-block;
      width: $ui-size;
      height: $ui-size;
      margin: 7px 0 0 7px;
      vertical-align: top;
      overflow: hidden;
      background-image:  url('../../assets/img/clip_icon.png');
      background-repeat: no-repeat;
      background-size: $ui-size;
      cursor: pointer;
      -webkit-transition: all 0.3s ease;
      -moz-transition: all 0.3s ease;
      -o-transition: all 0.3s ease;
      transition: all  0.3s ease;

      &:hover{
        opacity: .7;
      }

      input[type="file"]{
        opacity: 0;
        display: none;
      }
    }

    // メニュー内のラベル
    .label{
      display: inline-block;
      width: auto;
      height: $ui-size + 10px;
      line-height: $ui-size + 10px;
      margin: 0 0 0 10px;
      font-weight: bold;
      color: #ffffff;
      vertical-align: top;
    }
  }

  .switch_span{
    display: inline-block;
    width: auto;
    margin: 7px 0 0 10px;
    vertical-align: top;

    p{
      width: 100%;
      text-align: center;
      font-size: 10px;
    }
  }

  // トグルスイッチ
  .toggle-switch {
    display: inline-block;
    position: relative;
    width: 50px;
    height: $ui-size - 15px;
    margin: 4px 0 0 0;
    vertical-align: top;

    input[type="checkbox"] {
      position: absolute;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      z-index: 5;
      opacity: 0;
      cursor: pointer;
    }

    label {
      width: 50px;
      height: $ui-size - 15px;
      background: #ccc;
      position: relative;
      display: inline-block;
      border-radius: $ui-size - 15px;
      transition: 0.4s;
      box-sizing: border-box;
      &:after {
        content: '';
        position: absolute;
        width: $ui-size - 15px;
        height: $ui-size - 15px;
        border-radius: 100%;
        left: 0;
        top: 0;
        z-index: 2;
        background: #fff;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
        transition: 0.4s;
      }
    }

    input:checked {
      +label{
        background-color: #ff3c41;
        &:after{
          left: 65 - $ui-size;
        }
      }
    }
  }
</style>