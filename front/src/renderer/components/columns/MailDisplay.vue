<template>
  <div id="mailDisplay">

    <div class="upbar_list">
      差出人：{{ sendUser.name }}
    </div>

    <div class="upbar_list">
      件　名：{{ subject }}
    </div>

    <textarea
      id="main_message"
      v-model="mailBody"
      readonly>
    </textarea>
  </div>
</template>

<script>
  export default {
    name: 'MailDisplay',
    props: {
      subject: '',
      mailBody: '',
      draftID: '',
      sendUser: ''
    },
    data () {
      return {
      }
    },
    methods: {
    },
    watch: {
    },
    mounted () {
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