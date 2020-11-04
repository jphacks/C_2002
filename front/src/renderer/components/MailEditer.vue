<template>
  <div id="MailEditor">
    <div id="editor__menu">
      <button v-on:click="saveDraft">save</button>
      <button v-on:click="convertHonorific">convert</button>
    </div>
    <input
      class="editor__input"
      type="text"
      v-model="mailData.subject"
      placeholder="件名">
    <input
      class="editor__input"
      type="text"
      v-model="mailData.destination"
      placeholder="宛先">

    <textarea
      id="editor__body"
      v-model="mailData.body"
      v-on:keyup.enter.exact="bodyEnterAction"
      v-on:keyup.delete.exact="bodyDeleteAction">
    </textarea>
  </div>
</template>

<script>
  import GitCommand from '../utils/NodeGit'
  import FileAction from '../utils/FileAction'
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
          bodyLength: 0
        }
      }
    },
    methods: {
      async draftInit () {
        // Windows用のパス形式で指定
        if (isWindows) {
          this.draft.directory = '\\aaplication-name\\draft\\'
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
        fs.writeFile(targetDirectory + this.draft.delimiter + this.draft.fileName, '', function (err) {
          if (err) { throw err }
        })
        fs.writeFile(targetDirectory + this.draft.delimiter + '.gitignore', this.draft.resultName, function (err) {
          if (err) { throw err }
        })
        fs.writeFile(targetDirectory + this.draft.delimiter + this.draft.resultName, '', function (err) {
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

        const sendJSON = {'commit_id': commitID, 'sentence': sentence}
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
            )
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

          // 抜き出し
          Object.keys(diffObj.remove).forEach(function (key) {
            FileAction.deleteLINE(HOMEDIR + self.draft.directory + self.draftID + self.draft.delimiter + self.draft.resultName, key)
            console.log(key)
          })
        }
      }
    },
    watch: {
      mailData: function () {
      }
    },
    mounted () {
      this.draftInit()
    }
  }
</script>

<style lang="scss">
  #editor__MailEditor{
    width: 600px;
  }

  // 上部メニューバー
  #editor__menu{
    width: 100%;
    height: 60px;
    background: #4B4B4B;
  }

  // テキスト入力部分のスタイル
  .editor__input{
    // スタイルのリセット
    outline: none;
    border: none;
    // スタイル
    width: 94%;
    padding: 0 3%;
    font-size: 1em;
    line-height: 40px;
    border-bottom: 1px solid #262626;
  }

  // 本文編集部分
  #editor__body{
    outline: none;
    border: none;
    width: 94%;
    height: calc(100vh - 10px - 140px);
    margin: 5px 0 0 3%;
    overflow-y: scroll;
    &:focus{
      outline: none;
    }
  }
</style>