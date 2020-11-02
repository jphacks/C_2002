<template>
  <div id="preview">
    <div id="content">
      <div id="subject_frame">
        <div id="subject">
          件名：{{ content.subject}}
        </div>
        <div id="name">
          名前：{{ content.name }}
        </div>
      </div>
      <div id="main_message_frame">
        <div id="main_message">
          {{ content.message }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Preview',
    data () {
      return {
        content: {
          subject: 'テスト件名',
          name: 'テスト送信者',
          message: 'これはメッセージ本文です．改行をどうにかしないといけないわ'
        }
      }
    }
  }
</script>

<style scoped lang="scss">
  #preview{
    background-color: #ffffff;
    height: 100%;
    width: 100%;
    #content{
      display: flex;
      flex-direction: column;
      height: 100%;
      width: 100%;
      #subject_frame{
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        height: 10%;
        width: 100%;
        background-color: khaki;
        #subject{
          height: auto;
          width: auto;
          padding: 5px;
          margin: 10px 10px 0px 10px;
          border-radius: 10px;
          border: solid 2px #aaaaaa;
        }
        #name{
          height: auto;
          width: auto;
          padding: 5px;
          margin: 0px 10px 10px 10px;
          border-radius: 10px;
          border: solid 2px #aaaaaa;
        }
      }
      #main_message_frame{
        display: flex;
        height: 90%;
        width: 100%;
        background-color: lavenderblush;
        #main_message{
          margin: 10px;
          width: 100%;
          height: auto;
          border: solid 1px #cccccc;
          overflow: scroll;
          #test{
            font-size: 4rem;
          }
        }
      }
    }
  }
</style>