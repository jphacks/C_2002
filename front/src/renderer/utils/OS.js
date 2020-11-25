// Windowsか確認
const isWindowsOS = process.platform === 'win32'

// 改行文字関数
function breakChar () {
  let delimiter
  if (isWindowsOS) {
    delimiter = '\n'
  } else {
    delimiter = '\n'
  }
  return delimiter
}

// 区切り文字
function delimiterChar () {
  let delimiter
  if (isWindowsOS) {
    delimiter = '\\'
  } else {
    delimiter = '/'
  }
  return delimiter
}

// ホームディレクトリの取得
function homeDirectory () {
  // デフォルトの実行ディレクトリの確認
  return process.env[isWindowsOS ? 'USERPROFILE' : 'HOME']
}

function isWindows () {
  return isWindows
}

// エクスポート
export default { breakChar, delimiterChar, homeDirectory, isWindows }
