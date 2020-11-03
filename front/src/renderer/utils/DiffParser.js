// diff内容のパース
function diffParse (diff) {
  let addObj = {}
  let rmObj = {}

  for (let dataPosition = diff.indexOf('\n@@ '); dataPosition > -1;) {
    const positionDataStart = dataPosition + 4
    const positionDataSeparate = diff.substr(positionDataStart).indexOf(' ')
    const positionDataEnd = diff.substr(positionDataStart + positionDataSeparate + 1).indexOf(' ')

    // 追加/削除行数情報の取得
    const addLINEstr = diff.substr(positionDataStart + positionDataSeparate + 2, positionDataEnd)
    const removeLINEstr = diff.substr(positionDataStart + 1, positionDataSeparate)

    // 連続行数情報（カンマ区切り）の有無を確認
    const addDelimiter = addLINEstr.indexOf(',')
    const removeDelimiter = removeLINEstr.indexOf(',')

    let addLINE
    let removeLINE

    if (addDelimiter > -1) { // 連続行数情報が与えられている場合
      addLINE = Number(addLINEstr.substr(0, addDelimiter))
    } else {
      addLINE = Number(addLINEstr)
    }

    if (removeDelimiter > -1) { // 連続行数情報が与えられている場合
      removeLINE = Number(removeLINEstr.substr(0, removeDelimiter))
    } else {
      removeLINE = Number(removeLINEstr)
    }

    // 探索関数の引数整形
    const positionDataFull = positionDataStart + positionDataSeparate + positionDataEnd
    const positionDataNext = diff.substr(positionDataFull).indexOf('\n@@') // 行情報の行開始位置

    // 探索関数実行
    if (positionDataNext === -1) {
      addObj = Object.assign(addObj, searchAddLINE(diff.substr(positionDataFull), addLINE))
      rmObj = Object.assign(rmObj, searchRemoveLINE(diff.substr(positionDataFull), removeLINE))
    } else {
      addObj = Object.assign(addObj, searchAddLINE(diff.substr(positionDataFull, positionDataNext), addLINE))
      rmObj = Object.assign(rmObj, searchRemoveLINE(diff.substr(positionDataFull, positionDataNext), removeLINE))
    }

    if (positionDataNext === -1) {
      break
    } else {
      dataPosition = positionDataFull + positionDataNext
    }
  }
  // オブジェクトを返す
  let diffObj = {
    add: addObj,
    remove: rmObj
  }
  return diffObj
}

function searchAddLINE (targetText, addLINE) {
  let addObj = {}

  // 追加内容探索
  for (let prevPosition = 0; targetText.substr(prevPosition).indexOf('\n+') > -1;) {
    // +開始部分取得
    const startPosition = targetText.substr(prevPosition).indexOf('\n+')
    const endPosition = targetText.substr(prevPosition + startPosition + 1).indexOf('\n')

    // パース
    if (endPosition === -1) {
      addObj[addLINE] = targetText.substr(prevPosition).substr(startPosition + 2)
    } else {
      addObj[addLINE] = targetText.substr(prevPosition).substr(startPosition + 2, endPosition)
    }

    if (endPosition === -1) { // 最終行の場合
      break
    } else { // 現在の位置を次回の位置へ
      prevPosition += (startPosition + endPosition)
      addLINE++
    }
  }
  // オブジェクトを返す
  return addObj
}

function searchRemoveLINE (targetText, rmLINE) {
  let rmObj = {}

  // 削除内容探索
  for (let prevPosition = 0; targetText.substr(prevPosition).indexOf('\n-') > -1;) {
    // +開始部分取得
    const startPosition = targetText.substr(prevPosition).indexOf('\n-')
    const endPosition = targetText.substr(prevPosition + startPosition + 1).indexOf('\n')
    if (endPosition === -1) {
      rmObj[rmLINE] = targetText.substr(prevPosition).substr(startPosition + 2)
    } else {
      rmObj[rmLINE] = targetText.substr(prevPosition).substr(startPosition + 2, endPosition)
    }

    if (endPosition === -1) { // 最終行の場合
      break
    } else { // 現在の位置を次回の位置へ
      prevPosition += (startPosition + endPosition)
      rmLINE++
    }
  }
  return rmObj
}

export default { diffParse }
