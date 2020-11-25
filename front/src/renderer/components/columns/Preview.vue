<template>
  <div id="preview">

    <div class="upbar_list">
      UPDATED {{ updated }}
    </div>

    <div class="upbar_list">
      件　名：{{ subject }}
    </div>

    <textarea
      id="main_message"
      v-model="mailBody">
    </textarea>
  </div>
</template>

<script>
  import OS from '../../utils/OS'
  const fs = require('fs')

  export default {
    name: 'Preview',
    props: {
      subject: '',
      mailBody: '',
      draftID: '',
      sendUser: ''
    },
    data () {
      return {
        updated: ''
      }
    },
    methods: {
      dateFormat (date, format = 'YYYY-MM-DD hh:mm:ss') { // 日付フォーマット
        // パース
        format = format.replace(/YYYY/g, date.getFullYear())
        format = format.replace(/MM/g, ('0' + (date.getMonth() + 1)).slice(-2))
        format = format.replace(/DD/g, ('0' + date.getDate()).slice(-2))
        format = format.replace(/hh/g, ('0' + date.getHours()).slice(-2))
        format = format.replace(/mm/g, ('0' + date.getMinutes()).slice(-2))
        format = format.replace(/ss/g, ('0' + date.getSeconds()).slice(-2))

        if (format.match(/S/g)) {
          let milliSeconds = ('00' + date.getMilliseconds()).slice(-3)
          let length = format.match(/S/g).length
          for (let i = 0; i < length; i++) format = format.replace(/S/, milliSeconds.substring(i, i + 1))
        }

        // 文字列を返す
        return format
      },
      saveResult () { // 変更結果の上書き
        const delimiter = OS.delimiterChar()
        const fullPath = OS.homeDirectory() + delimiter + 'frankfrut' + delimiter + 'data' + delimiter + 'userInformation.json'
        const optionJson = {flag: 'w'}
        fs.writeFile(fullPath, this.mailBody, optionJson, function (err) {
          if (err) {
            console.log(err)
          }
        })
      }
    },
    watch: {
      'mailBody': function () { // メール本文が変更された場合
        console.log(this.mailBody)
        console.log(this.subject)
        this.updated = this.dateFormat(new Date())
      }
    },
    mounted () {
      this.updated = this.dateFormat(new Date())
    }
  }
</script>

<style scoped lang="scss">
  #preview{
    height: 100%;
    width: 100%;
    color: #ffffff;
    background: #333333;
  }

  // 上部のスタイル
  .upbar_list{
    width: 94%;
    padding: 0 3%;
    font-size: 17px;
    line-height: 40px;
    height: 40px;
    border-bottom: 1px solid #888888;
    color: #ffffff;
  }

  // 本文
  #main_message{
    outline: none;
    border: none;
    background: none;
    resize: none;

    width: 94%;
    margin: 5px 0 0 3%;
    height: calc(100vh - 10px - 90px);
    overflow-y: scroll;
    font-size: 17px;
    line-height: 26px;
    color: #ffffff;
    &:focus{
      outline: none;
    }
  }
</style>