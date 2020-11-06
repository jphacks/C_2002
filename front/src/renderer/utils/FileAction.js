import OS from './OS'
const fs = require('fs')

// ディレクトリ作成関数
async function mkdir (fullPath) {
  // 区切り文字の指定
  let delimiter = '/'
  if (fullPath.indexOf('\\') > -1) {
    delimiter = '\\'
  }
  console.log(fullPath)

  // 区切り文字
  const directories = fullPath.split(delimiter)
  let createPath = ''

  // ディレクトリの作成
  for (let i = 0; i < directories.length; i++) {
    createPath += directories[i] + delimiter
    console.log(createPath)
    if (!fs.existsSync(createPath)) {
      await fs.mkdir(createPath, (err) => {
        if (err) { throw err }
        console.log('testディレクトリが作成されました')
      })
    }
  }
}

// 行追加関数
async function addLINE (fullPath, LINE, text) {
  return new Promise(resolve => {
    let lineText
    let resultText = ''

    // 区切り文字をOSに合わせる
    const delimiter = OS.breakChar()

    // ファイルの読み込み
    fs.readFile(fullPath, 'utf8', (err, data) => {
      if (err) {
        console.log(err)
      }
      // 文字列に入っている改行コードを削除
      if (text.indexOf(delimiter) > -1) {
        text = text.substring(0, text.indexOf(delimiter))
      }
      // データの有無を確認
      if (data === '') {
        resultText = text + delimiter
      } else {
        lineText = data.split(delimiter)

        // 文字列をファイル格納用に結合
        for (let i = 0; i < lineText.length; i++) {
          if (i === LINE - 1) {
            if (i === 0) {
              resultText = text
            } else {
              resultText = resultText + delimiter + text
            }
          } else if (i === 0) {
            resultText = resultText + lineText[i]
            continue
          }
          resultText = resultText + delimiter + lineText[i]
        }
      }

      // ファイルへの書き込み
      const optionJson = {flag: 'w'}
      fs.writeFile(fullPath, resultText, optionJson, function (err) {
        if (err) {
          console.log(err)
        }
        return resolve(0)
      })
    })
  })
}

// 指定行の削除関数
async function deleteLINE (fullPath, LINE) {
  return new Promise(resolve => {
    let lineText
    let resultText = ''

    // 区切り文字をOSに合わせる
    const delimiter = OS.breakChar()

    // ファイルの読み込み
    fs.readFile(fullPath, 'utf8', function (err, data) {
      // エラー処理
      if (err) {
        throw err
      }

      // 行ごとに分ける
      lineText = data.split(delimiter)

      for (let i = 0; i < lineText.length; i++) {
        if (i !== LINE - 1) {
          if (!(i === lineText.length - 1 && lineText[i] === '')) {
            resultText = resultText + lineText[i] + delimiter
          }
        }
      }

      // ファイルへの書き込み
      const optionJson = { flag: 'w' }
      fs.writeFile(fullPath, resultText, optionJson, function (err) {
        if (err) {
          console.log(err)
        }
        return resolve(0)
      })
    })
  })
}

export default { mkdir, deleteLINE, addLINE }
