<template>
  <div id="app">
    <div v-if="displayFlag.settingModal" id="setting_modal">
      <div class="form_frame">
        <span>メールアドレス</span>
        <input type="email" placeholder="example@example.com" v-model="userInformation.email">
        <span>パスワード</span>
        <input type="password" v-model="userInformation.password">
        <button v-if="userInformation.email.match(/[\w\-._]+@[\w\-._]+\.[A-Za-z]+/)  && userInformation.password" v-on:click="settingModalDispOff" style="background: #f1a90c; cursor: pointer;">登録</button>
        <button v-else style="background: #919191; cursor: not-allowed;">登録</button>
      </div>
    </div>
    <div id="column__user"
         v-on:mouseover="userMouseOver"
         v-on:mouseleave="userMouseLeave"
         :style="'width: ' + userColumn.width + 'px'">
      <div class="user_content" v-for="user in users">
        <span class="user_icon">
          {{ user.name.charAt(0) }}
        </span>
        <div v-if="userColumn.openFlg" class="user_info">
          <h3>{{ user.name }}</h3>
          <p>{{ user.mail }}</p>
        </div>
      </div>
      <div id="setting_icon" v-on:click="settingModalDispOn">
        <setting-icon></setting-icon>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
  // アイコンインポート
  import SettingIcon from './components/icons/setting.vue'
  // fsモジュールをインポート
  const fs = require('fs')
  // ディレクトリを生成
  const homedir = require('os').homedir() // ホームディレクトリ
  const targetdir = require('path').join(homedir, 'goateat') // ホーム/アプリディレクトリ
  const generateFiledir = require('path').join(targetdir, 'userInformation.json') // userInfomation.jsonパス
  export default {
    name: 'c2002',
    components: {
      // 設定アイコンのコンポーネント
      SettingIcon
    },
    data () {
      return {
        displayFlag: {
          settingModal: false
        },
        userInformation: {
          email: '',
          password: ''
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
            name: 'Test1',
            mail: 'test@example.com'
          },
          '3': {
            name: 'Test1',
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
        console.log('leave')
        this.userColumn.width = 60
        this.userColumn.openFlg = false
      },
      settingModalDispOn () {
        console.log('modal ON')
        if (fs.existsSync(generateFiledir)) {
          console.log(generateFiledir + 'は存在します。')
          let jsonObject = JSON.parse(fs.readFileSync(generateFiledir, 'utf8'))
          this.userInformation.email = jsonObject['email']
          this.userInformation.password = jsonObject['password']
        } else {
          console.log(generateFiledir + 'は存在しません。')
        }
        this.displayFlag.settingModal = true
      },
      settingModalDispOff () {
        console.log('modal OFF')
        // json生成
        const jsonData = {
          email: this.userInformation.email,
          password: this.userInformation.password
        }
        if (fs.existsSync(targetdir)) {
          console.log(targetdir + 'は存在します。')
        } else {
          console.log(targetdir + 'は存在しません。')
          fs.mkdir(targetdir)
        }
        fs.writeFile(generateFiledir, JSON.stringify(jsonData, null, '    '), (err) => {
          // 書き出しに失敗した場合
          if (err) {
            console.log('json書き出しにエラーが発生しました' + err)
            throw err
          }
          // 書き出しに成功した場合
          if (err) {
            console.log('json書き出しに成功しました')
          }
        })
        this.displayFlag.settingModal = false
      }
    }
  }
</script>

<style lang="scss">
  // ユーザ一覧カラム
  $icon-size: 40px;
  $usercolumn__size: 60px;
  #setting_modal{
    z-index:200;
    position:fixed;
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
        border: solid 3px;
        border-color: #aaaaaa;
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
        border: solid 2px;
        border-color: #aaaaaa;
      }
    }
  }
  #column__user{
    width: $usercolumn__size;
    height: 100vh;
    background: #cccccc;
    -webkit-transition: all 0.2s ease;
    -moz-transition: all 0.2s ease;
    -o-transition: all 0.2s ease;
    transition: all  0.2s ease;
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
  #setting_icon{
    z-index:200;
    position: absolute;       // 絶対位置指定することを定義
    bottom: 0px;              // 絶対位置指定(左0px,下0px)
    margin: 8px 8px 8px 8px;
    width: $icon-size;
    height: $icon-size;
    border-radius: $icon-size;
    border: solid 2px;
    border-color: #aaaaaa;
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
