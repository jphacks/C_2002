// 読み込み
const childProcess = require('child_process')

// デフォルトの実行ディレクトリの確認
const HOMEDIR =
  process.env[process.platform === 'win32' ? 'USERPROFILE' : 'HOME']

function exe (command, pwd = HOMEDIR) { // コマンド実行関数
  console.log('実行コマンド：' + command)
  console.log('実行ディレクトリ：' + pwd)

  // 実行部分 https://nodejs.org/api/childProcess.html
  const child = childProcess.exec(command, {
    cwd: pwd, // 子プロセスの現在の作業ディレクトリ（デフォルト：null）
    shell: true // コマンドを実行するシェル（デフォルト： [Unix]/bin/sh [Windows]process.env.ComSpec）
  })

  return child
}

// git init
function gitInit (pwd) {
  return new Promise(resolve => {
    const child = exe('git init', pwd)

    // 標準出力受け取り
    child.stdout.on('close', data => {
      console.log(data)
      return resolve(0)
    })

    // 標準エラー受け取り
    child.stderr.on('close', data => {
      console.log(data)
      return resolve(data)
    })
  })
}

// git add
function gitAdd (file = '.', pwd = HOMEDIR) {
  return new Promise(resolve => {
    // コマンド実行
    const child = exe('git add ' + file, pwd)

    // 標準出力受け取り
    child.stdout.on('close', data => {
      console.log(data)
      return resolve(0)
    })

    // 標準エラー受け取り
    child.stderr.on('close', data => {
      console.log(data)
      return resolve(data)
    })
  })
}

// git commit
function gitCommit (message, pwd = HOMEDIR) {
  return new Promise(resolve => {
    // コマンド実行
    const child = exe('git commit -m"' + message + '"', pwd)

    // 標準出力受け取り
    child.stderr.on('close', data => {
      console.log(data)
      return resolve(data)
    })

    // 標準エラー受け取り
    child.stderr.on('close', data => {
      console.log(data)
      return resolve(data)
    })
  })
}

// git rev-parse --short HEAD
function getCommitID (pwd) {
  return new Promise(resolve => {
    // 短縮CommitID取得
    const childGetID = exe('git rev-parse --short HEAD', pwd)

    // 標準出力受け取り
    childGetID.stdout.on('data', data => {
      console.log(data)
      return resolve(data)
    })

    // 標準エラー受け取り
    childGetID.stderr.on('data', data => {
      console.log(data)
      return resolve(data)
    })
  })
}

// git diff
function gitDiff (prevID, pwd) {
  return new Promise(resolve => {
    let command
    if (prevID) {
      command = 'git diff ' + prevID
    } else {
      command = 'git diff --unified=0'
    }
    const child = exe(command, pwd)

    // 標準出力受け取り
    child.stdout.on('data', data => {
      // 差分を抜き出す
      return resolve(data)
    })

    // 標準エラー受け取り
    child.stderr.on('data', data => {
      console.log(data)
      return resolve(data)
    })
  })
}

export default {gitInit, gitAdd, gitCommit, gitDiff, getCommitID}
