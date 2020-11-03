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
      v-model="mailData.body">
    </textarea>
  </div>
</template>

<script>
  import GitCommand from '../utils/NodeGit'
  import FileAction from '../utils/FileAction'
  // import DiffParser from '../utils/DiffParser'
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
          directory: '/aaplication-name/draft/',
          fileName: '/draft.txt'
        },
        commitID: '',
        mailData: {
          subject: '',
          destination: '',
          body: '',
          draftID: ''
        }
      }
    },
    methods: {
      draftInit () {
        // Windows用のパス形式で指定
        if (isWindows) {
          this.draft.directory = '\\aaplication-name\\draft\\'
          this.draft.fileName = '\\draft.txt'
        }

        // 下書きごとのIDはUNIX時間を指定
        this.draftID = Date.now()
        const targetDirectory = HOMEDIR + this.draft.directory + this.draftID

        // 作業ディレクトリの作成
        FileAction.mkdir(targetDirectory)

        // git init
        GitCommand.gitInit(targetDirectory)

        // ファイルの作成
        fs.writeFile(targetDirectory + this.draft.fileName, '', function (err) {
          if (err) { throw err }
        })
      },
      async saveDraft () {
        // 作業ディレクトリの定義
        const draftDirectory = HOMEDIR + this.draft.directory + this.draftID

        // ファイルへの書き込み
        fs.appendFile(draftDirectory + this.draft.fileName, this.mailData.body, function (err) {
          if (err) { throw err }
        })

        // git add
        await GitCommand.gitAdd('.', draftDirectory).then(function (result) {
          console.log(result)
        })

        // git commit
        const commitMessage = Date.now() + ' draft commit'
        await GitCommand.gitCommit(commitMessage, draftDirectory).then(function (result) {
          console.log(result)
        })

        // commit ID の取得
        await GitCommand.getCommitID(draftDirectory).then(function (result) {
          console.log(result)
        })
      },
      convertHonorific () {
        console.log(HOMEDIR)
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
    width: 94%;
    height: calc(100vh - 10px - 140px);
    margin: 5px 0 0 3%;
    overflow-y: scroll;
    outline: none;

    &:focus{
      outline: none;
    }
  }
</style>