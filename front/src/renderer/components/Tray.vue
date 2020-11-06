<template>
  <div id="chat_tree">
    <!-- 左側 -->
    <div id="tree_frame__left">
      <ChatTree
        v-if="$route.query['userData']"
        :targetUser="$route.query['userData']"
        @getMailData="mailData = $event"/>
    </div>
    <!-- リサイズバー -->
    <div id="resize_bar"></div>
    <!-- 右側 -->
    <div id="tree_frame__right">
      <Preview
        :subject="mailData.title"
        :mailBody="mailText"/>
    </div>
  </div>
</template>

<script>
  import MailReceive from '../utils/MailReceive'
  import ChatTree from './columns/ChatTree'
  import Preview from './columns/Preview'
  import OS from '../utils/OS'

  // モジュールをインポート
  const fs = require('fs')

  // デフォルトの実行ディレクトリの確認
  const isWindows = process.platform === 'win32'
  const HOMEDIR =
    process.env[isWindows ? 'USERPROFILE' : 'HOME']

  export default {
    name: 'Tray',
    components: {
      ChatTree,
      Preview
    },
    props: {
      users: {},
      targetUser: ''
    },
    data () {
      return {
        // チャットツリーに転送するためのオブジェクト
        transferData: {
          serchEmail: ''
        },
        mailData: {},
        mailText: ''
      }
    },
    methods: {
      async getText (authData, UID) {
        // テキストの初期化
        this.mailText = ''

        const self = this
        await MailReceive.getMailText(authData, UID).then(text => {
          console.log('this.mailText : ')
          console.log(self.mailText)
          self.mailText = text
        })
      }
    },
    mounted () {
    },
    watch: {
      mailData: async function (newData, oldData) {
        console.log('data : ')
        console.log(newData.title)
        const self = this
        const delimiter = OS.delimiterChar()
        // SMTP情報を取得
        await fs.readFile(HOMEDIR + delimiter + 'frankfrut' + delimiter + 'data' + delimiter + 'userInformation.json', 'utf8', function (err, data) {
          // エラー処理
          if (err) {
            throw err
          }
          const userData = JSON.parse(data)

          const authData = {
            auth: {
              user: userData['auth'].user,
              pass: userData['auth'].pass
            },
            imap: {
              host: userData['imap'].host,
              port: userData['imap'].port
            }
          }
          // 結果を取得
          self.getText(authData, newData.UID)
        })
      }
    }
  }
</script>

<style lang="scss">
  #chat_tree{
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
  #tree_frame__left{
    padding-left: 60px;
    height: 100%;
  }
  #tree_frame__right{
    height: 100%;
    width: 60%;
  }
</style>