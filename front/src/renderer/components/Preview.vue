<template>
  <div id="preview">

    <div class="upbar_list">
      UPDATED {{ updated }}
    </div>

    <div class="upbar_list">
      件名：{{ subject }}
    </div>

    <textarea
      id="main_message"
      v-model="mailBody">
    </textarea>
  </div>
</template>

<script>
  export default {
    name: 'Preview',
    props: {
      subject: '',
      mailBody: ''
    },
    data () {
      return {
        updated: ''
      }
    },
    methods: {
      dateFormat (date, format = 'YYYY-MM-DD hh:mm:ss') {
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
      }
    },
    watch: {
      'mailBody': function () {
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
  }

  // 上部のスタイル
  .upbar_list{
    width: 94%;
    padding: 0 3%;
    font-size: 17px;
    line-height: 40px;
    height: 40px;
    border-bottom: 1px solid #262626;
  }

  // 本文
  #main_message{
    outline: none;
    border: none;
    resize: none;
    width: 94%;
    margin: 5px 0 0 3%;
    height: calc(100vh - 10px - 90px);
    overflow: scroll;
    font-size: 17px;
    line-height: 26px;
    &:focus{
      outline: none;
    }
  }
</style>