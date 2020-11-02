<template>
  <div id="chat_tree">
    <div id="tree_frame">
      <div id="content_frame" v-for="messages in contents" :key="messages">
        <div id="content" v-for="message in messages" :key="message">
          <div v-if="message.type=='receive'" class="receive">
            <h5 class="name">{{ message.name }}</h5>
            <p class="title">{{ message.subject }}</p>
          </div>
          <div v-else-if="message.type=='thread'" class="thread">
            <h5 class="name">{{ message.name }}</h5>
            <p class="title">{{ message.subject }}</p>
          </div>
          <div v-else-if="message.type=='reply'" class="reply">
            <h5 class="name">{{ message.name }}</h5>
            <p class="title">{{ message.subject }}</p>
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
            margin-top: 1px;
            margin-bottom: 1px;
            padding: 3px;
            width: 50%;
            height: auto;
            border-radius: 10px;
            background-color:#ffcccc;
            cursor: pointer;
            h4{
              padding: 3px
            }
            span{
              padding-left: 10px;
            }
          }
          .thread{
            margin-top: 1px;
            margin-bottom: 1px;
            padding: 3px;
            margin-left: calc(10%);
            width: 50%;
            height: auto;
            border-radius: 10px;
            background-color: #ccffcc;
            cursor: pointer;
            h4{
              padding: 3px
            }
            span{
              padding-left: 10px;
            }
          }
          .reply{
            margin-top: 1px;
            margin-bottom: 1px;
            padding: 3px;
            margin-left: calc(50%);
            width: 50%;
            height: auto;
            border-radius: 10px;
            background-color: #ccccff;
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