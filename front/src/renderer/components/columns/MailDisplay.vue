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

    <div
      id="reply_button"
      @click="sendReply"
      title="返信">
    </div>
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
      sendReply () {
        console.log('sendUser')
        console.log(this.sendUser)

        let replySubject = this.subject

        console.log('replySubject.indexOf(\'Re:\')')
        console.log(replySubject.indexOf('Re:'))
        if (replySubject.indexOf('Re:') !== 0) {
          replySubject = 'Re:' + replySubject
        }

        this.$router.push({
          name: 'editor',
          query: {
            subject: replySubject,
            address: this.sendUser.mail
          }
        })
      }
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

  // 返信ボタン
  #reply_button{
    position: absolute;
    z-index: 100;
    bottom: 30px;
    right: 30px;
    display: inline-block;
    width: 60px;
    height: 60px;
    border-radius: 60px;
    cursor: pointer;
    // 背景
    background-color: #ff3c41;
    background-image:  url('../../assets/img/reply.png');
    background-position: center;
    background-repeat: no-repeat;
    background-size: 30px;
    // アニメーション
    -webkit-transition: all 0.3s ease;
    -moz-transition: all 0.3s ease;
    -o-transition: all 0.3s ease;
    transition: all  0.3s ease;
    &:hover{
      opacity: .7;
    }
  }
</style>