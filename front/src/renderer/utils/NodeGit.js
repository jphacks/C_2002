// 読み込み
const childProcess = require('child_process')
// デフォルトの実行ディレクトリの確認
const HOMEDIR =
  process.env[process.platform === 'win32' ? 'USERPROFILE' : 'HOME']

export default {
  data () {
    return {
      test: ''
    }
  },
  method: {
    exe (command, pwd = HOMEDIR) { // コマンド実行関数
      console.log('実行コマンド：' + command)
      console.log('実行ディレクトリ：' + pwd)

      // 実行部分 https://nodejs.org/api/childProcess.html
      const child = childProcess.exec(command, {
        cwd: pwd, // 子プロセスの現在の作業ディレクトリ（デフォルト：null）
        shell: true // コマンドを実行するシェル（デフォルト： [Unix]/bin/sh [Windows]process.env.ComSpec）
      })
      // てすとaiu
      return child
    },
    gitAdd (file = '.', pwd = HOMEDIR) {
      // コマンド実行
      const child = this.exe('git add ' + file, pwd)

      // 標準出力受け取り
      child.stdout.on('data', data => {
        return 0
      })

      // 標準エラー受け取り
      child.stderr.on('data', data => {
        return data
      })
    },
    gitCommit (message, pwd = HOMEDIR) {
      // コマンド実行
      const child = this.exe('git commit -m "' + message + '"', pwd)

      // 標準エラー受け取り
      child.stderr.on('data', data => {
        return data
      })

      // 短縮CommitID取得
      const childGetID = this.exe('git rev-parse --short HEAD', pwd)

      // 標準出力受け取り
      childGetID.stdout.on('data', data => {
        // CommitIDを返す
        return data
      })
      // 標準エラー受け取り
      childGetID.stderr.on('data', data => {
        return data
      })
    },
    gitDiff (prevID, pwd) {
      const child = this.exe('git diff ' + prevID, pwd)

      // 標準出力受け取り
      child.stdout.on('data', data => {
        // 差分を抜き出す
        return data
      })

      // 標準エラー受け取り
      child.stderr.on('data', data => {
        return data
      })
    }
  }
}
