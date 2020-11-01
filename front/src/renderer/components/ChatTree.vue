<template>
  <div id="chat_tree">
    <div id="tree_frame">
      <div id="content_frame" v-for="messages in contents">
        <div id="content" v-for="message in messages">
          <div v-if="message.type=='receive'" class="receive">
            <h5>名前</h5>
            <span>{{ message.name }}</span>
            <h5>件名</h5>
            <span>{{ message.subject }}</span>
          </div>
          <div v-else-if="message.type=='thread'" class="thread">
            <h5>名前</h5>
            <span>{{ message.name }}</span>
            <h5>件名</h5>
            <span>{{ message.subject }}</span>
          </div>
          <div v-else-if="message.type=='reply'" class="reply">
            <h5>名前</h5>
            <span>{{ message.name }}</span>
            <h5>件名</h5>
            <span>{{ message.subject }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Chattree',
    data () {
      return {
        contents: {
          '1': {
            '1': {
              subject: 'Testsubject1',
              name: 'testName1',
              type: 'receive'
            },
            '2': {
              subject: 'Testsubject2',
              name: 'testName2',
              type: 'thread'
            },
            '3': {
              subject: 'Testsubject3',
              name: 'testName3',
              type: 'reply'
            },
            '4': {
              subject: 'Testsubject4',
              name: 'testName4',
              type: 'thread'
            }
          },
          '2': {
            '1': {
              subject: 'Testsubject1',
              name: 'testName1',
              type: 'receive'
            },
            '2': {
              subject: 'Testsubject2',
              name: 'testName2',
              type: 'reply'
            },
            '3': {
              subject: 'Testsubject3',
              name: 'testName3',
              type: 'reply'
            },
            '4': {
              subject: 'Testsubject4',
              name: 'testName4',
              type: 'thread'
            }
          },
          '3': {
            '1': {
              subject: 'Testsubject1',
              name: 'testName1',
              type: 'receive'
            },
            '2': {
              subject: 'Testsubject2',
              name: 'testName2',
              type: 'reply'
            },
            '3': {
              subject: 'Testsubject3',
              name: 'testName3',
              type: 'reply'
            },
            '4': {
              subject: 'Testsubject4',
              name: 'testName4',
              type: 'thread'
            }
          },
          '4': {
            '1': {
              subject: 'Testsubject1',
              name: 'testName1',
              type: 'receive'
            },
            '2': {
              subject: 'Testsubject2',
              name: 'testName2',
              type: 'reply'
            },
            '3': {
              subject: 'Testsubject3',
              name: 'testName3',
              type: 'reply'
            },
            '4': {
              subject: 'Testsubject4',
              name: 'testName4',
              type: 'thread'
            }
          }
        }
      }
    }
  }
</script>

<style scoped lang="scss">
  #chat_tree{
    display: flex;
    flex-direction: column;
    background-color: #eeeeee;
    width: 100%;
    height: 100vh;
    overflow-y: scroll;
    #tree_frame{
      width: 100%;
      height: 100vh;
      #content_frame{
        margin-top: 20px;
        margin-bottom: 10px;
        width: 100%;
        height: auto;
        // background-color: rgb(205, 255, 205);
        #content{
          margin-left: calc(5%);
          width: calc(100% - 10%);
          height: auto;
          .receive{
            padding: 3px;
            width: 50%;
            height: auto;
            border-radius: 10px;
            background-color:#ffcccc;
            box-shadow: rgba(0, 0, 0, 0.19) 0px 10px 20px, rgba(0, 0, 0, 0.23) 0px 6px 6px;
            cursor: pointer;
            h4{
              padding: 3px
            }
            span{
              padding-left: 10px;
            }
          }
          .thread{
            padding: 3px;
            margin-left: calc(10%);
            width: 50%;
            height: auto;
            border-radius: 10px;
            background-color: #ccffcc;
            box-shadow: rgba(0, 0, 0, 0.19) 0px 10px 20px, rgba(0, 0, 0, 0.23) 0px 6px 6px;
            cursor: pointer;
            h4{
              padding: 3px
            }
            span{
              padding-left: 10px;
            }
          }
          .reply{
            padding: 3px;
            margin-left: calc(50%);
            width: 50%;
            height: auto;
            border-radius: 10px;
            background-color: #ccccff;
            box-shadow: rgba(0, 0, 0, 0.19) 0px 10px 20px, rgba(0, 0, 0, 0.23) 0px 6px 6px;
            cursor: pointer;
            h4{
              padding: 3px
            }
            span{
              padding-left: 10px;
            }
          }
        }
      }
    }
  }
</style>