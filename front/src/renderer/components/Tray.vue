<template>
  <div>
    <!-- 左側 -->
    <div id="tree_frame__left">
      <ChatTree
        v-if="$route.query['userData']"
        :targetUser="$route.query['userData']"
      />
      <div v-else>

      </div>
    </div>
      <!-- リサイズバー -->
      <div id="resize_bar"></div>
      <!-- 右側 -->
      <div id="tree_frame__right">
        <Preview
          :mailBody="$route.query['userData'].title"
          :subject="$route.query['userData'].title"/>
      </div>
  </div>
</template>

<script>
  import ChatTree from './columns/ChatTree'
  import Preview from './columns/Preview'

  export default {
    name: 'Tray',
    components: {
      ChatTree,
      Preview
    },
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
    },
    mounted () {
      console.log('$route : ')
      console.log(this.$route.query['userData'])
    }
  }
</script>

<style lang="scss">
  #chat_tree{
    height: 100vh;
    width: 100%;
    display: flex;
    flex-direction: row;
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
  #tree_frame__left{
    padding-left: 60px;
    height: 100%;
  }
  #tree_frame__right{
    height: 100%;
    width: 60%;
  }
</style>