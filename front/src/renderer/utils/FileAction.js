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

// 指定行の削除関数
async function deleteLINE (fullPath, LINE) {
  let lineText
  let resultText = ''
  console.log('LINE : ' + LINE)
  // ファイルの読み込み
  await fs.readFile(fullPath, 'utf8', function (err, data) {
    // エラー処理
    if (err) {
      throw err
    }

    console.log('dataLINE : ' + (data.match(/\n/g) || []).length)
    if (LINE === (data.match(/\n/g) || []).length) {
      return
    }
    console.log(data)
    // 行ごとに分ける
    lineText = data.split('\n')
    console.log('lineText : ' + lineText)

    for (let i = 0; i < lineText.length; i++) {
      console.log(i + ' : ' + lineText[i])
      if (i !== LINE - 1) {
        console.log(i + ' : ' + lineText[i])
        resultText = resultText + lineText[i] + '\n'
      }
    }
  })

  // ファイルへの書き込み
  console.log('resultText : ' + resultText)
  const optionJson = { flag: 'w' }
  fs.writeFile(fullPath, resultText, optionJson, function (err) {
    if (err) {
      console.log(err)
    }
  })
}

// 行追加関数
async function addLINE (fullPath, LINE, text) {
  let lineText
  let resultText = ''
  // ファイルの読み込み
  await fs.readFile(fullPath, 'utf8', (err, data) => {
    if (err) {
      console.log(err)
    }
    // 文字列に入っている改行コードを削除
    if (text.indexOf('\n') > -1) {
      text = text.substring(0, text.indexOf('\n'))
    }
    // データの有無を確認
    if (data === '') {
      resultText = text + '\n'
    } else {
      lineText = data.split('\n')

      // 文字列をファイル格納用に結合
      for (let i = 0; i < lineText.length; i++) {
        if (i === LINE - 1) {
          resultText = resultText + '\n' + text
        } else if (i === 0) {
          resultText = resultText + lineText[i]
          continue
        }
        resultText = resultText + '\n' + lineText[i]
      }
    }

    // ファイルへの書き込み
    const optionJson = { flag: 'w' }
    fs.writeFile(fullPath, resultText, optionJson, function (err) {
      if (err) {
        console.log(err)
      }
    })
  })
}

export default { mkdir, deleteLINE, addLINE }
