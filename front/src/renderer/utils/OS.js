// Windowsか確認
const isWindows = process.platform === 'win32'

// 改行文字関数
function breakChar () {
  let delimiter
  if (isWindows) {
    delimiter = '\n'
  } else {
    delimiter = '\r'
  }
  return delimiter
}

// 区切り文字
function delimiterChar () {
  let delimiter
  if (isWindows) {
    delimiter = '\\'
  } else {
    delimiter = '/'
  }
  return delimiter
}

// ホームディレクトリの取得
function homeDirectory () {
  // デフォルトの実行ディレクトリの確認
  return process.env[isWindows ? 'USERPROFILE' : 'HOME']
}

// エクスポート
export default { breakChar, delimiterChar, homeDirectory }
