<template>
  <div id="MailEditor">
    <input
      class="editor__input"
      type="text"
      v-model="mailData.destination"
      placeholder="宛先">

    <input
      class="editor__input"
      type="text"
      maxlength="50"
      v-model="mailData.subject"
      placeholder="件名">

    <textarea
      id="editor__body"
      v-model="mailData.body"
      placeholder="本文を入力"
      v-on:keyup.enter.exact="bodyEnterAction"
      v-on:keyup.delete.exact="bodyDeleteAction">
    </textarea>

    <div id="editor__contents">
      <button @click="sendMail">送信</button>
    </div>
  </div>
</template>

<script>
  import GitCommand from '../utils/NodeGit'
  import FileAction from '../utils/FileAction'
  import MailSend from '../utils/MailSend'
  import axios from 'axios'
  import DiffParser from '../utils/DiffParser'
  const fs = require('fs')

  const isWindows = process.platform === 'win32'

  // デフォルトの実行ディレクトリの確認
  const HOMEDIR =
    process.env[isWindows ? 'USERPROFILE' : 'HOME']

  export default {
    name: 'MailEditer',
    data () {
      return {
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
          draftID: '',
          bodyLINE: 0,
          bodyLength: 0,
          resultBody: ''
        }
      }
    },
    methods: {
      async draftInit () {
        // Windows用のパス形式で指定
        if (isWindows) {
          this.draft.directory = '\\frankfrut\\draft\\'
          this.draft.delimiter = '\\'
        }

        // 下書きごとのIDはUNIX時間を指定
        this.draftID = Date.now()
        const targetDirectory = HOMEDIR + this.draft.directory + this.draftID

        // 作業ディレクトリの作成
        await FileAction.mkdir(targetDirectory)

        // git init
        await GitCommand.gitInit(targetDirectory)

        // ファイルの作成
        fs.writeFile(targetDirectory + this.draft.delimiter + this.draft.fileName, '', function (err) { // 下書き管理ファイル
          if (err) { throw err }
        })
        fs.writeFile(targetDirectory + this.draft.delimiter + '.gitignore', this.draft.resultName, function (err) { // gitignore
          if (err) { throw err }
        })
        fs.writeFile(targetDirectory + this.draft.delimiter + this.draft.resultName, '', function (err) { // 結果保存ファイル
          if (err) { throw err }
        })

        // git add
        await GitCommand.gitAdd('.', targetDirectory).then(function (result) {
          console.log(result)
        })

        // git commit
        const commitMessage = Date.now() + ' draft commit'
        await GitCommand.gitCommit(commitMessage, targetDirectory).then(function (result) {
          console.log(result)
        })
      },
      async saveDraft () {
        // 作業ディレクトリの定義
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
      async convertHonorific (commitID, sentence, key) {
        // APIのURL
        const API = 'http://54.64.167.36:5000/postdata'
        // 送信用のJSONの作成
        const sendJSON = {'commit_id': commitID, 'sentence': sentence}
        const self = this
        // APIへPOST
        return axios.post(API, sendJSON, {
          headers: {
            'Content-Type': 'application/json'
          }
        })
          .then((res) => {
            // レスポンスが200の時の処理
            console.log(res)
            FileAction.addLINE(
              HOMEDIR + this.draft.directory + this.draftID + this.draft.delimiter + this.draft.resultName,
              key,
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
      async bodyEnterAction () {
        if (this.mailData.bodyLength + 1 < this.mailData.body.length) {
          if (this.mailData.bodyLINE !== (this.mailData.body.match(/\n/g) || []).length) {
            this.mailData.bodyLINE = (this.mailData.body.match(/\n/g) || []).length
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
      },
      async bodyDeleteAction () {
        const breakPoints = (this.mailData.body.match(/\n/g) || []).length
        if (this.mailData.bodyLINE !== breakPoints) {
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
            // await FileAction.deleteLINE(HOMEDIR + self.draft.directory + self.draftID + self.draft.delimiter + self.draft.resultName, keysArr[i])
            await FileAction.deleteLINE(HOMEDIR + self.draft.directory + self.draftID + self.draft.delimiter + self.draft.resultName, keysArr[i])
          }

          // 追加部分の追加
          await Object.keys(diffObj.add).forEach(function (key) {
            console.log(key + ':' + diffObj.add[key])
            if (diffObj.add[key] !== '') {
              self.convertHonorific(diffObj['commit_id'], diffObj.add[key], key)
            }
          })
        }
      },
      updatePreview () {
        const self = this
        fs.readFile(HOMEDIR + this.draft.directory + this.draftID + this.draft.delimiter + this.draft.resultName, 'utf8', function (err, data) {
          // エラー処理
          if (err) {
            throw err
          }
          console.log(data)
          // 変更結果を代入
          self.mailData.resultBody = data

          // 親コンポーネントへ渡す
          self.$emit('updateBody', self.mailData.resultBody)
        })
      },
      sendMail () {
        const self = this
        // SMTP情報を取得
        fs.readFile(HOMEDIR + this.draft.delimiter + 'frankfrut' + this.draft.delimiter + 'data' + this.draft.delimiter + 'userInformation.json', 'utf8', function (err, data) {
          // エラー処理
          if (err) {
            throw err
          }
          const smtpData = JSON.parse(data)

          console.log(smtpData)

          const mailData = {
            from: '"' + smtpData['user'].affiliation + ' ' + smtpData['user'].name + '" <' + smtpData['smtp'].auth.user + '>',
            to: self.mailData.destination,
            subject: self.mailData.subject,
            text: self.mailData.resultBody
          }

          MailSend.sendMail(smtpData['smtp'], mailData)
        })
      }
    },
    watch: {
      'mailData.subject': function (val, oldVal) {
        // APIのURL
        const API = 'http://54.64.167.36:5000/postdata'
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
              self.$emit('updateSubject', res.data['change_sentence'])
            })
            .catch(err => {
              console.log(err)
              if (err.response) {
                // レスポンスが200以外の時の処理
              }
            })
        }
      }
    },
    mounted () {
      this.draftInit()
    }
  }
</script>

<style lang="scss">
  // 全体スタイル
  #editor__MailEditor{
    width: 600px;
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
    border-bottom: 1px solid #262626;
  }

  // 本文編集部分
  #editor__body{
    outline: none;
    border: none;
    resize: none;
    width: 94%;
    height: calc(100vh - 10px - 130px);
    margin: 5px 0 0 3%;
    font-size: 17px;
    line-height: 26px;
    overflow-y: scroll;
    &:focus{
      outline: none;
    }
  }

  // 下部メニューバー
  #editor__contents{
    width: 100%;
    height: 40px;
    border-top: solid 2px #d7d7d7;

    button{
      display: inline-block;
      width: 70px;
      height: 30px;
      margin: 7px 0 0 7px;
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
        opacity: .9;
      }
    }
  }
</style>