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

export default { mkdir }
