<template>
  <div>
    <!-- 左側 -->
    <div id="frame_left">
      <ChatTree
        v-if="users[transferData.serchEmail]"
        v-bind:targetUser="users[transferData.serchEmail]"
        v-bind:reroadTrigger="transferData.reroadTrigger"
      />
      <div v-else>

      </div>
    </div>
      <!-- リサイズバー -->
      <div id="resize_bar"></div>
      <!-- 右側 -->
      <div id="frame_right">
        <Preview
          :mailBody="mailData.mailBody"
          :subject="mailData.subject"/>
      </div>
  </div>
</template>

<script>
  export default {
    name: 'Tray',
    props: {
      users: {},
      targetUser: ''
    },
    data () {
      return {
        // チャットツリーに転送するためのオブジェクト
        transferData: {
          serchEmail: '検索するメールアドレス',
          reroadTrigger: false
        }
      }
    }
  }
</script>

<style scoped>
</style>