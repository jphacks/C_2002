<template>
  <div id="app">
    <div id="column__user"
         v-on:mouseover="userMouseOver"
         v-on:mouseleave="userMouseLeave"
         :style="'width: ' + userColumn.width + 'px'">
      <div class="user_content"
           v-for="user in users">
        <span class="user_icon">
          {{ user.name.charAt(0) }}
        </span>
        <div v-if="userColumn.openFlg" class="user_info">
          <h3>{{ user.name }}</h3>
          <p>{{ user.mail }}</p>
        </div>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    name: 'c2002',
    data () {
      return {
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
        this.userColumn.width = 60
        this.userColumn.openFlg = false
      }
    }
  }
</script>

<style lang="scss">
  // フォントファイルの読み込み
  @font-face {
    font-family: 'JapaneseFont';
    src: url('~@/assets/font/KosugiMaru-Regular.ttf') format('truetype');
  }

  // ユーザ一覧カラム
  $icon-size: 40px;
  $usercolumn__size: 60px;
  #column__user{
    display: inline-block;
    font-family: 'JapaneseFont';
    width: $usercolumn__size;
    height: 100vh;
    background: #cccccc;
    -webkit-transition: all 0.2s ease;
    -moz-transition: all 0.2s ease;
    -o-transition: all 0.2s ease;
    transition: all  0.2s ease;
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
  }

  // RESET
  body{overflow: hidden;}
  html, body, div, span, applet, object, iframe, h1, h2, h3, h4, h5, h6, p, blockquote, pre, a, abbr, acronym, address, big, cite, code, del, dfn, em, img, ins, kbd, q, s, samp, small, strike, strong, sub, sup, tt, var, b, u, i, center, dl, dt, dd, ol, ul, li, fieldset, form, label, legend, table, caption, tbody, tfoot, thead, tr, th, td, article, aside, canvas, details, embed, figure, figcaption, footer, header, hgroup, menu, nav, output, ruby, section, summary, time, mark, audio, video {margin: 0;padding: 0;border: 0;font: inherit;vertical-align: baseline; }
  article, aside, details, figcaption, figure, footer, header, hgroup, menu, nav, section { display: block; }
  body { line-height: 1; }
  ol, ul { list-style: none; }
  blockquote, q { quotes: none; }
  blockquote { &:before, &:after { content: none; } }
  q { &:before, &:after { content: none; } }
  table { border-collapse: collapse;border-spacing: 0; }
  input[type='submit'], button {background-color: transparent;border: none;cursor: pointer;outline: none;padding: 0;appearance: none; }
</style>
