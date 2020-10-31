<template>
  <div id="app">
    <div v-if="displayFlag.settingModal" id="settign_modal">
      <div class="form_frame">
        <span>メールアドレス</span>
        <input type="email" v-model="userInformation.email">
        <span>パスワード</span>
        <input type="password" v-model="userInformation.password">
        <button @click="settingModalDispOff">決定</button>
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
      <div class="rounded-test-btn" @click="settingModalDispOn">set</div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    name: 'c2002',
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
        this.displayFlag.settingModal = true
      },
      settingModalDispOff () {
        console.log('modal OFF')
        console.log(this.userInformation.email)
        console.log(this.userInformation.password)
        // json生成コード
        const fs = require('fs')
        const jsonData = {
          email: this.userInformation.email,
          password: this.userInformation.password
        }
        // ホームディレクトリを生成
        const homedir = require('os').homedir()
        const targetdir = require('path').join(homedir, 'goateat')
        const generateFiledir = require('path').join(targetdir, 'userInfomation.json')
        console.log(require('path').join(homedir, 'goateat'))
        // `homedir()` returns absolute path so we use `join` here
        if (fs.existsSync(generateFiledir)) {
          console.log(generateFiledir + 'は存在します。')
        } else {
          console.log(generateFiledir + 'は存在しません。')
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
  #settign_modal{
    z-index:100;
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
      background-color:rgba(255,255,255,1);
      display: flex;
      align-items: center;
      justify-content: center;
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
  .rounded-test-btn{
    height: 50px;
    width: 50px;
    border-radius: 10px;
    border: solid 3px;
    background-color: #cccccc;
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
