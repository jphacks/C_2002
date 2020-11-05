<template>
  <div id="setting_frame">
    <div id="mail_cliant_frame">
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Setting'
  }
</script>

<style scoped lang="scss">
  #setting_frame{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    #mail_cliant_frame{
      display: flex;      
      width: 100px;
      height: 100px;
      background-color: aqua;
    }
  }
</style>