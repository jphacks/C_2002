<template>
  <div id="chat_tree">
    <div id="tree_frame">
      <div
        class="chat"
        v-for="(message, index) in messages"
        :key="index">
        <div :class="[userData.mail === message.mail ? 'chat__send_me' : '', 'chat__frame ' + message.type]">
          <!-- <h5 class="chat__name">{{ message.name }}</h5> -->
          <h5 class="chat__name">{{ email }}</h5>
          <p class="chat__title">{{ message.subject }}</p>
        </div>
        <span class="chat__time">{{ message.time }}</span><!-- 時間に関してはメールサーバからの情報によって変更 -->
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Chattree',
    props: {
      email: {
        type: String,
        default: null
      }
    },
    data () {
      return {
        userData: {
          name: 'TestUser',
          mail: 'user@test.com'
        },
        messages: { // テスト用データ
          '1': {
            subject: 'Testsubject1',
            name: 'testName1',
            mail: 'test@test.com',
            type: 'receive',
            mailID: '0001',
            time: '2020/11/02\n12:00'
          },
          '2': {
            subject: 'Testsubject1',
            name: 'TestUser',
            mail: 'user@test.com',
            type: 'thread',
            mailID: '0002',
            time: '2020/11/02\n12:00'
          },
          '3': {
            subject: 'Testsubject1',
            name: 'testName1',
            mail: 'test@test.com',
            type: 'thread',
            mailID: '0001',
            time: '2020/11/02\n12:00'
          },
          '4': {
            subject: 'Testsubject1',
            name: 'TestUser',
            mail: 'user@test.com',
            type: 'thread',
            mailID: '0002',
            time: '2020/11/02\n12:00'
          },
          '5': {
            subject: 'Testsubject1',
            name: 'testName1',
            mail: 'test@test.com',
            type: 'thread',
            mailID: '0001',
            time: '2020/11/02\n12:00'
          },
          '6': {
            subject: 'Testsubject1',
            name: 'testName1',
            mail: 'test@test.com',
            type: 'receive',
            mailID: '0001',
            time: '2020/11/02\n12:00'
          },
          '7': {
            subject: 'Testsubject1',
            name: 'TestUser',
            mail: 'user@test.com',
            type: 'receive',
            mailID: '0002',
            time: '2020/11/02\n12:00'
          },
          '8': {
            subject: 'Testsubject1',
            name: 'testName1',
            mail: 'test@test.com',
            type: 'thread',
            mailID: '0001',
            time: '2020/11/02\n12:00'
          },
          '9': {
            subject: 'Testsubject1',
            name: 'TestUser',
            mail: 'user@test.com',
            type: 'thread',
            mailID: '0002',
            time: '2020/11/02\n12:00'
          }
        }
      }
    }
  }
</script>

<style scoped lang="scss">
  #chat_tree {
    display: flex;
    flex-direction: column;
    background-color: #eeeeee;
    width: 450px;
    height: 100vh;
    overflow-y: scroll;
  }
  #tree_frame {
    width: 90%;
    height: 100vh;
    margin-left: 5%;
  }

  $chat__time-fontsize: 10px;
  // チャット風UI
  .chat{
    // 送受信時間表記
    .chat__time{
      display: inline-block;
      width: 60px;
      height: $chat__time-fontsize;
      line-height: $chat__time-fontsize;
      font-size: $chat__time-fontsize;
      vertical-align: middle;
      word-wrap:break-word;
    }
    // 吹き出し風ボックス
    .chat__frame {
      display: inline-block;
      margin: 1px 1px 0 10px;
      padding: 6px 20px;
      width: 250px;
      height: auto;
      background-color: #ffffff;
      color: #262626;
      border-radius: 10px 10px 10px 0;
      cursor: pointer;
      vertical-align: middle;
      .chat__name{
        font-weight: bold;
      }
      .chat__title{

      }
      // 自身の送信したメールスタイル
      &.chat__send_me{
        background-color: #5645ff;
        color: #ffffff;
        border-radius: 10px 10px 0 10px;
      }
      // 通常メールスタイル
      &.receive{
        margin: 20px 40px 0 0;
      }
      // 返信メール（スレッド）スタイル
      &.thread{
        margin: 0 10px 0 30px;
      }
    }
  }

</style>