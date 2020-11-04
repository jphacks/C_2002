<template>
  <div id="app">
    <!-- 左側メニュー -->
    <div v-if="displayFlag.settingModal" id="setting_modal">
      <div class="form_frame">
        <span>メールアドレス</span>
        <input type="email" placeholder="example@example.com" v-model="userInformation.email">
        <span>パスワード</span>
        <input type="password" v-model="userInformation.password">
        <button v-if="userInformation.email.match(/[\w\-._]+@[\w\-._]+\.[A-Za-z]+/) && userInformation.password" v-on:click="settingModalDispOff" style="background: #f1a90c; cursor: pointer;">登録</button>
        <button v-else style="background: #919191; cursor: not-allowed;">登録</button>
      </div>
    </div>
    <div id="column__user"
         v-on:mouseover="userMouseOver"
         v-on:mouseleave="userMouseLeave"
         :style="'width: ' + userColumn.width + 'px'">
      <div class="scroll-frame">
        <div class="user_content" v-for="(user, index) in users" :key="index">
          <span class="user_icon">
            {{ user.name.charAt(0) }}
          </span>
          <div v-if="userColumn.openFlg" class="user_info">
            <h3>{{ user.name }}</h3>
            <p>{{ user.mail }}</p>
          </div>
        </div>
      </div>
      <div id="setting_icon" v-on:click="settingModalDispOn">
        <SettingIcon/>
      </div>
    </div>
    <!-- 右側メニュー -->
    <div id="tray_frame">
      <!-- 左側 -->
      <div id="main_left">
        <!-- <ChatTree/> -->
        <MailEditer/>
      </div>
      <!-- リサイズバー -->
      <div id="resize_bar"></div>
      <!-- 右側 -->
      <div id="main_right">
        <Preview/>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
  import FileAction from './utils/FileAction'
  import SettingIcon from './components/icons/setting.vue'
  import ChatTree from './components/ChatTree.vue'
  import Preview from './components/Preview.vue'
  import MailEditer from './components/MailEditer'

  // モジュールをインポート
  const fs = require('fs')

  const isWindows = process.platform === 'win32'
  // デフォルトの実行ディレクトリの確認
  const HOMEDIR =
    process.env[isWindows ? 'USERPROFILE' : 'HOME']

  export default {
    name: 'c_2002',
    components: {
      MailEditer,
      // 設定アイコンのコンポーネント
      SettingIcon,
      ChatTree,
      Preview
    },
    data () {
      return {
        infomation: {
          directory: '/frankfrut/data/',
          fileName: '/userInformation.json',
          delimiter: '/'
        },
        userInformation: {
          email: '',
          password: ''
        },
        displayFlag: {
          settingModal: false
        },
        userColumn: {
          openFlg: false,
          width: 60
        },
        users: {
          '1': {
            name: 'Test1',
            mail: 'test@example.com'
          },
          '2': {
            name: 'Test2',
            mail: 'test@example.com'
          },
          '3': {
            name: 'Test3',
            mail: 'test@example.com'
          }
        }
      }
    },
    methods: {
      userMouseOver () {
        this.userColumn.openFlg = true
        this.userColumn.width = 220
      },
      userMouseLeave () {
        this.userColumn.width = 60
        this.userColumn.openFlg = false
      },
      // モーダル項目
      settingModalDispOn () {
        console.log('modal ON')
        // Windows用のパス形式で指定
        if (isWindows) {
          this.infomation.directory = '\\frankfrut\\draft\\'
          this.infomation.delimiter = '\\'
        }
        // Win/Mac両対応のディレクトリを生成
        const targetDirectory = HOMEDIR + this.infomation.directory

        if (fs.existsSync(targetDirectory)) {
          console.log(targetDirectory + 'は存在します。')
          // ユーザー情報ファイルからデータを取得する
          let jsonObject = JSON.parse(fs.readFileSync(targetDirectory + this.infomation.delimiter + this.infomation.fileName, 'utf8'))
          this.userInformation.email = jsonObject['auth']['user']
          this.userInformation.password = jsonObject['auth']['pass']
        } else {
          console.log(targetDirectory + 'は存在しません。')
        }
        this.displayFlag.settingModal = true
      },
      async settingModalDispOff () {
        console.log('modal OFF')
        // Windows用のパス形式で指定
        if (isWindows) {
          this.infomation.directory = '\\frankfrut\\draft\\'
          this.infomation.delimiter = '\\'
        }
        // Win/Mac両対応のディレクトリを生成
        const targetDirectory = HOMEDIR + this.infomation.directory

        // 作業ディレクトリの作成
        await FileAction.mkdir(targetDirectory)

        // json生成
        const jsonData = {
          host: 'smtp.gmail.com',
          port: 465,
          secure: true,
          auth: {
            user: this.userInformation.email,
            pass: this.userInformation.password
          }
        }

        // 作業ディレクトリの作成
        await FileAction.mkdir(targetDirectory)
        fs.writeFileSync(targetDirectory + this.infomation.delimiter + this.infomation.fileName, JSON.stringify(jsonData, null, '    ', function (err) { // jsonファイル
          if (err) { throw err }
        }))
        // モーダルフラグOFF
        this.displayFlag.settingModal = false
      }
    }
  }
</script>

<style lang="scss">
  // フォントの読み込み
  @font-face {
    font-family: 'JapaneseFont';
    src: url('~@/assets/font/KosugiMaru-Regular.ttf') format('truetype');
  }
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
      background-color: #cbcbcb;
      border-radius: 6px;
    }
  }

  // 設定モーダル
  #setting_modal{
    z-index:1000;
    position: absolute;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background-color:rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    .form_frame{
      min-height: 200px;
      min-width: 400px;
      width:50%;
      height:50%;
      border-radius: 10px;
      background-color:rgba(255,255,255,1);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      span{
        margin: 5px 0px 5px 0px;
        font-size: 25px;
        font-weight: 700;
      }
      input{
        margin: 5px 0px 10px 0px;
        padding: 2.5px 12.5px 2.5px 12.5px;
        min-height: 25px;
        min-width: 200px;
        max-width: 400px;
        width:50%;
        font-size: 25px;
        border-radius: 20px;
        border: solid 3px #aaaaaa;
      }
      button{
        margin: 5px 0px 10px 0px;
        min-height: 40px;
        min-width: 70px;
        max-width: 100px;
        width:30%;
        font-size: 20px;
        font-weight: 500;
        border-radius: 10px;
        border: solid 2px #aaaaaa;
      }
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
    background: #cccccc;
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
    width: 200px;
    height: auto;
    cursor: pointer;
    .user_icon{
      display: inline-block;
      vertical-align: center;
      margin: 15px 0 0 ($usercolumn__size - $icon-size) / 2;
      width: $icon-size;
      height: $icon-size;
      border-radius: $icon-size;
      font-size: 30px;
      text-align: center;
      line-height: $icon-size;
      background: #f1a90c;
      color: #ffffff;
    }
    .user_info{
      display: inline-block;
      vertical-align: center;
      margin-left: 5px;
      color: #ffffff;
      -webkit-transition: all 0.3s ease;
      -moz-transition: all 0.3s ease;
      -o-transition: all 0.3s ease;
      transition: all  0.3s ease;
    }
  }
  // 設定アイコン
  #setting_icon{
    z-index: 900;
    position: absolute; // 絶対位置指定することを定義
    bottom: 0px; // 絶対位置指定(左0px,下0px)
    margin: 8px 8px 8px 8px;
    width: $icon-size;
    height: $icon-size;
    border-radius: $icon-size;
    border: solid 2px #aaaaaa;
    background-color: #ffffff;
    cursor: pointer;
    &:hover{ // 歯車アイコン回転アニメーション
      animation: r1 1s cubic-bezier(0, 0, 1.0, 1.0) infinite;
      @keyframes r1 {
        0%   { transform: rotate(0deg); }
        100% { transform: rotate(135deg); }
      }
    }
  }

  // 右側メニュー
  #tray_frame{
    height: 100vh;
    width: 100%;
    display: flex;
    flex-direction: row;
    #main_left{
      padding-left: 60px;
      height: 100%;
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
    #main_right{
      height: 100%;
      width: 60%;
    }
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
</style>
