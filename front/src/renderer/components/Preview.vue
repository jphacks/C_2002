<template>
  <div id="preview">

    <div class="upbar_list">
      UPDATED
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
        content: {
          subject: 'テスト件名'
        }
      }
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