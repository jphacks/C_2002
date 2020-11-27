<template>
  <div id="app">
    <!-- ユーザ一覧 -->
    <div id="column__user"
         v-on:mouseover="userMouseOver"
         v-on:mouseleave="userMouseLeave"
         :style="'width: ' + userColumn.width + 'px'">
      <div class="scroll-frame">
        <router-link
          class="user_content"
          v-for="(user, index) in users"
          :to="{ name: 'tray', query: { userData: user }}"
          :key="index">
          <span class="user_icon" :style="'background: ' + user.color">
            {{ user.name.charAt(0) }}
          </span>
          <div v-if="userColumn.openFlg" class="user_info">
            <h3>{{ user.name }}</h3>
            <p>{{ user.mail }}</p>
          </div>
        </router-link>
      </div>
      <div id="icons">
        <div class="icons_content">
          <router-link
            title="新規メールを作成"
            :to="{ name: 'editor' }">
            <span id="plus_icon">
              <PlusIcon/>
            </span>
          </router-link>
        </div>
        <div class="icons_content">
          <router-link
            :to="{ name: 'setting' }"
            title="設定を開く">
            <span id="setting_icon">
              <SettingIcon/>
            </span>
          </router-link>
        </div>
      </div>
    </div>
    <router-view/>
    <Sending
      v-if="sending.flg"
      :sendParam="sending.param"
      @finishProgress="sending.flg = false"/>
  </div>
</template>

<script>
  // ライブラリのインポート
  import SettingIcon from './components/icons/Setting'
  import PlusIcon from './components/icons/Plus'
  import MailReciver from './utils/MailReceive'
  import ContactsList from './utils/ContactsList'
  import AuthFile from './utils/AuthFile'
  import Sending from './components/toast/Sending'

  export default {
    name: 'c_2002',
    components: {
      SettingIcon,
      PlusIcon,
      Sending
    },
    data () {
      return {
        // チャットツリーに転送するためのオブジェクト
        transferData: {
          serchEmail: ''
        },
        userInformation: {
          email: '',
          password: ''
        },
        userColumn: {
          openFlg: false,
          width: 60
        },
        users: {},
        mailCheck: {
          id: '',
          interval: 60000,
          newestMsg: ''
        },
        authData: {},
        sending: {
          flg: false,
          param: {},
          prevTimestamp: 0
        }
      }
    },
    methods: {
      userMouseOver () { // ユーザ一覧にカーソルが重なった時
        this.userColumn.openFlg = true
        this.userColumn.width = 300
      },
      userMouseLeave () { // ユーザ一覧からカーソルが離れた時
        this.userColumn.width = 60
        this.userColumn.openFlg = false
      },
      async getContactList (authData) { // メール相手一覧の取得
        // 最新20件のメールを取得
        const messages = await MailReciver.mailReceive(authData, 20)
        const self = this

        // 連絡先一覧を取得
        this.users = await ContactsList.getAddress()

        // 新規メールを先頭（古い順）に参照
        await messages.forEach(function (message) {
          // 新規ユーザであれば追加
          if (!(message['from'].address in self.users) && (message['from'].address !== authData['auth'].user)) {
            self.users[message['from'].address] = {
              name: message['from'].name,
              mail: message['from'].address,
              color: ContactsList.userColor(message['from'].address)
            }
          }
        })

        // 連絡先一覧を更新
        await ContactsList.updateAddress(this.users)
      },
      async getMail (authData) { // メールの取得
        const messages = await MailReciver.mailReceive(authData, 1)
        const self = this

        console.log('最新メッセージ : ')
        console.log(messages)

        // UIDを取得
        await messages.forEach(function (message) {
          // 最新メッセージに変更があったか確認
          if (self.mailCheck.newestMsg !== message.UID) {
            self.mailCheck.newestMsg = message.UID
            self.getContactList(authData)
          }
        })
      }
    },
    mounted () {
      const self = this

      const testArray = ['test1', 'test2']
      console.log('testArray')
      console.log(testArray)

      console.log('mounted')
      // ユーザ認証情報が存在しない場合は setting.vue へ遷移
      if (AuthFile.checkAuthJSON()) {
        // 完了後ホームへ戻る
        self.$router.push('setting')
      } else {
        // 連絡先一覧の作成（存在しない場合）
        ContactsList.contactInit().then(data => {
          // 連絡先一覧の取得
          ContactsList.getAddress().then(Obj => {
            console.log(Obj)
            self.users = Obj
          })
        })

        // メール一覧の取得
        AuthFile.getAuth().then((userData) => {
          // メール受信用の認証情報をオブジェクトに格納
          self.authData = {
            auth: {
              user: userData['auth'].user,
              pass: userData['auth'].pass
            },
            imap: {
              host: userData['imap'].host,
              port: userData['imap'].port
            }
          }

          // メールを受信
          self.getMail(self.authData)
        })

        // 新規メール受信処理
        this.mailCheck.id = setInterval(
          function () {
            self.getMail(self.authData)
          },
          this.mailCheck.interval
        )
      }
    },
    updated () {
      console.log('update!')
      console.log(this.$route.query)
      // 送信メールの有無を確認
      if ('mailData' in this.$route.query && this.sending.prevTimestamp !== this.$route.query['timestamp']) {
        // 送信用パラメータの設定
        this.sending.param = this.$route.query
        // 送信中の開始
        this.sending.flg = true
        // タイムスタンプの上書き
        this.sending.prevTimestamp = this.$route.query['timestamp']
      }
    },
    beforeDestroy () {
      // 定期チェックを終了
      clearInterval(this.mailCheck.id)

      // サーバとの接続を切断
      MailReciver.disconnectServer(this.authData)
    },
    watch: {
    }
  }
</script>

<style lang="scss">
  // フォントの読み込み
  @font-face {
    font-family: 'JapaneseFont';
    src: url('./assets/font/KosugiMaru-Regular.ttf') format('truetype');
  }

  // RESET
  body{overflow: hidden;}
  html, body, div, span, applet, object, iframe, h1, h2, h3, h4, h5, h6, p, blockquote, pre, a, abbr, acronym, address, big, cite, code, del, dfn, em, img, ins, kbd, q, s, samp, small, strike, strong, sub, sup, tt, var, b, u, i, center, dl, dt, dd, ol, ul, li, fieldset, form, label, legend, table, caption, tbody, tfoot, thead, tr, th, td, article, aside, canvas, details, embed, figure, figcaption, footer, header, hgroup, menu, nav, output, ruby, section, summary, time, mark, audio, video {
    margin: 0;
    padding: 0;
    border: 0;
    font: inherit;
    vertical-align: baseline; }

  /* HTML5 display-role reset for older browsers */

  article, aside, details, figcaption, figure, footer, header, hgroup, menu, nav, section {
    display: block; }

  body {
    line-height: 1; }

  ol, ul {
    list-style: none; }

  blockquote, q {
    quotes: none; }

  blockquote {
    &:before, &:after {
      content: none; } }

  q {
    &:before, &:after {
      content: none; } }

  table {
    border-collapse: collapse;
    border-spacing: 0; }

  input[type='submit'], button {
    background-color: transparent;
    border: none;
    cursor: pointer;
    outline: none;
    padding: 0;
    appearance: none; }

  #app {
    display: flex;
    flex-direction: row;
    font-family: 'JapaneseFont';

    // スクロールバーのスタイル
    ::-webkit-scrollbar {
      width: 6px;
    }
    ::-webkit-scrollbar-track {
      background: none;
      border-radius: 6px;
      box-shadow: none;
    }
    ::-webkit-scrollbar-thumb {
      background-color: #666666;
      border-radius: 6px;
    }
  }

  // ユーザ一覧カラム
  $icon-size: 40px;
  $usercolumn__size: 60px;
  #column__user{
    z-index: 900;
    position: absolute;
    flex-direction: column;
    width: $usercolumn__size;
    height: 100vh;
    background: #222222;
    -webkit-transition: all 0.2s ease;
    -moz-transition: all 0.2s ease;
    -o-transition: all 0.2s ease;
    transition: all  0.2s ease;
    overflow-x: hidden;
    overflow-y: hidden;
    &::-webkit-scrollbar {
      display: none;
    }
  }
  .user_content{
    display: inline-block;
    width: 300px;
    height: auto;
    cursor: pointer;
    padding: 10px 0;
    -webkit-transition: all 0.3s ease;
    -moz-transition: all 0.3s ease;
    -o-transition: all 0.3s ease;
    transition: all  0.3s ease;

    // アイコンのスタイル
    .user_icon{
      display: inline-block;
      vertical-align: middle;
      margin: 0 0 0 ($usercolumn__size - $icon-size) / 2;
      width: $icon-size;
      height: $icon-size;
      border-radius: $icon-size;
      font-size: 30px;
      text-align: center;
      line-height: $icon-size;
      background: #f1a90c;
      color: #ffffff;
    }

    // ユーザ情報のスタイル
    .user_info{
      display: inline-block;
      vertical-align: middle;
      margin-left: 5px;
      width: 200px;
      height: $icon-size;
      color: #ffffff;
      overflow: hidden;
      -webkit-transition: all 0.3s ease;
      -moz-transition: all 0.3s ease;
      -o-transition: all 0.3s ease;
      transition: all  0.3s ease;
      h3, p{
        line-height: $icon-size / 2;
        height: $icon-size / 2;
        word-break: break-all;
      }
    }

    // リンクとしてのスタイル
    &:link, &:visited{
      text-decoration: none;
    }

    // ホバーアニメーション
    &:hover{
      background-color: rgba(255, 255, 255, .1);
    }
  }

  // アイコンエリア
  #icons{
    z-index: 200;
    position: absolute; // 絶対位置指定することを定義
    left: 0;
    bottom: 0;
    height: auto;

    // 新規作成アイコン
    #plus_icon{
      display: inline-block;
      width: $icon-size + 10px;
      height: $icon-size + 10px;
      margin-left: -2px;
      // margin: 0 0 0 ($usercolumn__size - $icon-size - 10) / 2;
      fill: #ffffff;
      cursor: pointer;
      -webkit-transition: all 0.3s ease;
      -moz-transition: all 0.3s ease;
      -o-transition: all 0.3s ease;
      transition: all  0.3s ease;
      vertical-align: top;
      &:hover{
        opacity: .8;
      }
    }

    // 設定アイコン
    #setting_icon{
      display: inline-block;
      width: $icon-size;
      height: $icon-size;
      border-radius: $icon-size;
      border: solid 2px #ffffff;
      cursor: pointer;
      vertical-align: top;
      path{
        fill: #ffffff;
      }

      // 歯車アイコン回転アニメーション
      &:hover{
        animation: r1 1s cubic-bezier(0, 0, 1.0, 1.0) infinite;
        @keyframes r1 {
          0%   { transform: rotate(0deg); }
          100% { transform: rotate(135deg); }
        }
      }
    }

    .icons_content{
      display: block;
      height: $icon-size + 2px;
      width: 100%;
      padding: 8px;
    }

    p{
      display: inline-block;
      width: auto;
      height: $icon-size;
      vertical-align: middle;
    }
  }
</style>
