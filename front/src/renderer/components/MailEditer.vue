<template>
  <div id="MailEditor">
    <div id="editor__menu">
      <button v-on:click="convertHonorific">save</button>
      <button v-on:click="draftInit">init</button>
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

    <div
      id="editor__body"
      contenteditable="true">
    </div>
  </div>
</template>

<script>
  // import GitCommand from '../utils/NodeGit'
  import FileAction from '../utils/FileAction'
  // import DiffParser from '../utils/DiffParser'

  // デフォルトの実行ディレクトリの確認
  const HOMEDIR =
    process.env[process.platform === 'win32' ? 'USERPROFILE' : 'HOME']

  export default {
    name: 'MailEditer',
    data () {
      return {
        draftDirectory: '\\aaplication-name\\draft\\',
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
        this.draftID = Date.now()
        FileAction.mkdir(HOMEDIR + this.draftDirectory + this.draftID)
        // GitCommand.gitInit(HOMEDIR + this.draftDirectory + this.draftID)
      },
      convertHonorific () {
        console.log(HOMEDIR)
      }
    },
    watch: {
      bodyEditor: function () {

      }
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

    &:focus{
      outline: none;
    }
  }
</style>