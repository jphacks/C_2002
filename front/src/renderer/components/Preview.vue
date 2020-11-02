<template>
  <div id="preview">
    <div id="content">
      <div id="subject">
        件名
      </div>
      <div id="main_message">
        メッセージ本文
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Tray'
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
      height: 50%;
      width: 50%;
      margin: 10px;
      #subject{
        height: 10%;
        width: 100%;
        background-color: khaki;
      }
      #main_message{
        height: 90%;
        width: 100%;
        background-color: lavenderblush;
      }
    }
  }
</style>