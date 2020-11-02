<template>
  <div>
    <div class="test">
      <button @click="add">Git Add</button>
      <button @click="commit">Git Commit</button>
      <button @click="getID">Get ID</button>
      <button @click="diff">Git Diff</button>
    </div>
  </div>
</template>

<script>
  import GitCommand from '../utils/NodeGit'
  import DiffParser from '../utils/DiffParser'

  // デフォルトの実行ディレクトリの確認
  const HOMEDIR =
    process.env[process.platform === 'win32' ? 'USERPROFILE' : 'HOME']

  export default {
    name: 'Test',
    data () {
      return {
        commitID: {
          prev: '',
          next: ''
        }
      }
    },
    methods: {
      async add () {
        const res = await GitCommand.gitAdd('.', HOMEDIR + '/workspace/git_test')
        console.log('testtest')
        console.log(res)
      },
      async commit () {
        const res = await GitCommand.gitCommit('てすと！', HOMEDIR + '/workspace/git_test')
        console.log(res)
      },
      async getID () {
        const res = await GitCommand.getCommitID(HOMEDIR + '/workspace/git_test')
        console.log(res)
      },
      async diff () {
        const res = await GitCommand.gitDiff('', HOMEDIR + '/workspace/git_test')
        console.log(res)
        const diffObj = DiffParser.diffParse(res)
        console.log(diffObj)
      }
    }
  }
</script>

<style lang="scss">
  .test{
    position: fixed;
    z-index: 100;
    top: 0;
    left: 0;
    display: inline-block;
    background: #f1a90c;
  }
</style>