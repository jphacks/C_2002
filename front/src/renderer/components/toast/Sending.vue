<template>
  <div id="sending">
    <h2>メール送信中</h2>

    <button
      @click="displayMail"
      style="color: #cccccc">表示</button>

    <button
      @click="cancel"
      style="color: #ff3c41">キャンセル</button>

    <span
      class="progress"
      :style="'width:' + progress + '%'"></span>
  </div>
</template>

<script>
  import MailSend from '../../utils/MailSend'

  export default {
    name: 'Sending',
    props: {
      sendParam: {}
    },
    data () {
      return {
        sendingInterval: 5000, // 5秒
        intervalInstance: '',
        progress: 0,
        draftID: '1606412310220'
      }
    },
    methods: {
      displayMail () {
        console.log('draftID in Sending : ')
        console.log(this.draftID)
        // 下書きを表示
        this.$router.push({
          name: 'editor',
          query: {
            draftID: this.draftID
          }
        })
      },
      cancel () {
        this.finishProgress()
      },
      finishProgress () {
        // 500mSec毎の処理を終了
        clearInterval(this.intervalInstance)
        // toastを非表示に
        this.$emit('finishProgress')
      }
    },
    mounted () {
      const self = this
      // 500mSecごとの処理を追加
      this.intervalInstance = setInterval(
        function () {
          // 500mSec毎の進捗を追加
          self.progress += 100 * 500 / self.sendingInterval

          // 100%に達した場合
          if (self.progress >= 100) {
            // メールの送信
            MailSend.sendMail(self.sendParam.authData, self.sendParam.mailData)
            // 終了
            self.finishProgress()
          }
        },
        500
      )
    }
  }
</script>

<style lang="scss">
  $toast-height: 60px;

  #sending{
    position: fixed;
    right: 20px;
    bottom: 20px;
    display: inline-block;
    width: 300px;
    height: $toast-height;
    background: #444444;
    h2{
      display: inline-block;
      width: 100px;
      height: $toast-height;
      margin: 0  10px 0 25px;
      line-height: $toast-height;
      text-align: center;
      color: #ffffff;
    }
    button{
      display: inline-block;
      height: 30px;
      line-height: 30px;
      margin: ($toast-height - 30px) / 2 0;
      padding: 0 10px;
      color: #ff4441;
      border-radius: 3px;

      -webkit-transition: all 0.5s ease;
      -moz-transition: all 0.5s ease;
      -o-transition: all 0.5s ease;
      transition: all  0.5s ease;

      &:hover{
        background: #555555;
      }
    }
  }
  // プログレスバー
  .progress{
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background: #5645ff;

    -webkit-transition: all 0.5s ease;
    -moz-transition: all 0.5s ease;
    -o-transition: all 0.5s ease;
    transition: all  0.5s ease;
  }
</style>