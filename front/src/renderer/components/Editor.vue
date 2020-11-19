<template>
  <div id="editor">
    <!-- 左側 -->
    <div id="editor_frame__left">
      <MailEditer
        v-if="draftID"
        :draftID="draftID"
        @updateBody="mailData.body = $event"
        @updateSubject="mailData.subject = $event"
        @proofread="proofreadMode = $event"
        @joinPeople="people = $event"
        @attachFile="attachmentFile = $event"/>
    </div>
    <!-- リサイズバー -->
    <div id="resize_bar"></div>
    <!-- 右側 -->
    <div id="editor_frame__right">
      <Preview
        v-if="proofreadMode && draftID"
        :draftID="draftID"
        :mailBody="mailData.body"
        :subject="mailData.subject"
        :sendUser="false"/>
      <Start
        v-else/>
    </div>
    <div id="editor_option_bar">
      <Option
        :people="people"
        :files="attachmentFile"
      ></Option>
    </div>
  </div>
</template>

<script>
  import MailEditer from './columns/MailEditer'
  import Preview from './columns/Preview'
  import Start from './Start'
  import FileAction from '../utils/FileAction'
  import GitCommand from '../utils/NodeGit'
  import OS from '../utils/OS'
  import Option from './columns/Option'
  import AuthFile from '../utils/AuthFile'
  const fs = require('fs')

  export default {
    name: 'Editor',
    components: {
      Option,
      MailEditer,
      Preview,
      Start
    },
    data () {
      return {
        draftID: null,
        proofreadMode: true,
        mailData: {
          body: '',
          subject: ''
        },
        people: [],
        attachmentFile: {}
      }
    },
    methods: {
      async draftInit () {
        // OS依存文字列を取得
        const delimiter = OS.delimiterChar()
        const draftDirectory = OS.homeDirectory() + delimiter + 'frankfrut' + delimiter + 'draft' + delimiter

        // 各ファイルの命名
        const draftFile = 'draft.txt'
        const resultFile = 'result.txt'
        console.log('draftID' + this.draftID)

        // 下書きごとのIDはUNIX時間を指定
        this.draftID = Date.now()
        console.log('draftID' + this.draftID)
        const targetDirectory = draftDirectory + this.draftID + delimiter

        // 作業ディレクトリの作成
        await FileAction.mkdir(targetDirectory)

        // git init
        await GitCommand.gitInit(targetDirectory)

        const initText = '\n\n\n' + await this.createSign()

        // ファイルの作成
        fs.writeFile(targetDirectory + draftFile, initText, function (err) { // 下書き管理ファイル
          if (err) { throw err }
        })
        fs.writeFile(targetDirectory + '.gitignore', resultFile, function (err) { // gitignore
          if (err) { throw err }
        })
        fs.writeFile(targetDirectory + resultFile, '', function (err) { // 結果保存ファイル
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
      async createSign () {
        // 認証情報を取得
        const userInfo = await AuthFile.getAuth()

        console.log('Auth')
        console.log(userInfo)

        const sign =
          '-----------------------------------------' + '\n' +
          userInfo['user']['affiliation'] + '\n' +
          userInfo['user']['name'] + '\n' +
          'Mail：' + userInfo['auth']['user'] + '\n' +
          '-----------------------------------------' + '\n'

        return sign
      }
    },
    mounted () {
      // 新規下書きの作成
      this.draftInit()
    }
  }
</script>

<style lang="scss">
  #editor{
    height: 100vh;
    width: 100%;
    display: flex;
    flex-direction: row;
    background: #333333;
  }
  #resize_bar{
    height: 100%;
    width: 4px;
    background-color: gray;
    cursor: col-resize;
    transition-delay: 0.2s;
    transition: 0.5s ;
    &:hover{
      background-color: mediumturquoise;
    }
  }
  #editor_frame__left{
    padding-left: 60px;
    height: 100%;
  }
  #editor_frame__right{
    height: 100%;
    width: 60%;
    padding-right: 60px;
  }
  #editor_option_bar{
    position: fixed;
    z-index: 200;
    top: 0;
    right: 0;
    display: inline-block;
    width: auto;
    height: 100vh;
    -webkit-transition: all 0.2s ease;
    -moz-transition: all 0.2s ease;
    -o-transition: all 0.2s ease;
    transition: all  0.2s ease;
  }
</style>