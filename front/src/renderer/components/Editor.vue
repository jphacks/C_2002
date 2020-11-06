<template>
  <div id="editor">
    <!-- 左側 -->
    <div id="editor_frame__left">
      <MailEditer
        @updateBody="mailData.body = $event"
        @updateSubject="mailData.subject = $event"/>
    </div>
    <!-- リサイズバー -->
    <div id="resize_bar"></div>
    <!-- 右側 -->
    <div id="editor_frame__right">
      <Preview
        :mailBody="mailData.body"
        :subject="mailData.subject"
        :sendUser="false"/>
    </div>
  </div>
</template>

<script>
  import MailEditer from './columns/MailEditer'
  import Preview from './columns/Preview'

  export default {
    name: 'Editor',
    components: {
      MailEditer,
      Preview
    },
    props: {
      draftID: ''
    },
    data () {
      return {
        mailData: {
          body: '',
          subject: ''
        }
      }
    }
  }
</script>

<style lang="scss">
  #editor{
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
  #editor_frame__left{
    padding-left: 60px;
    height: 100%;
  }
  #editor_frame__right{
    height: 100%;
    width: 60%;
  }
</style>