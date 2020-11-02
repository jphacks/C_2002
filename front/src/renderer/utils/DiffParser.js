// diff内容のパース
function diffParse (diff) {
  console.log('原文')
  console.log(diff)

  for (let dataPosition = diff.indexOf('\n@@ '); dataPosition > -1;) {
    const positionDataStart = dataPosition + 4
    const positionDataSeparate = diff.substr(positionDataStart).indexOf(' ')
    const positionDataEnd = diff.substr(positionDataStart + positionDataSeparate + 1).indexOf(' ')

    console.log(
      diff.substr(positionDataStart,
        positionDataSeparate)
    )
    console.log(
      diff.substr(positionDataStart + positionDataSeparate + 1,
        positionDataEnd)
    )

    const positionDataFull = positionDataStart + positionDataSeparate + positionDataEnd
    const positionDataNext = diff.substr(positionDataFull).indexOf('\n@@') // 行情報の行開始位置

    if (positionDataNext === -1) {
      searchAddLINE(diff.substr(positionDataFull))
      searchRemoveLINE(diff.substr(positionDataFull))
    } else {
      searchAddLINE(diff.substr(positionDataFull, positionDataNext))
      searchRemoveLINE(diff.substr(positionDataFull, positionDataNext))
    }

    if (positionDataNext === -1) {
      break
    } else {
      dataPosition = positionDataFull + positionDataNext
    }
  }
}

function searchAddLINE (targetText) {
  // 追加内容探索
  for (let prevPosition = 0; targetText.substr(prevPosition).indexOf('\n+') > -1;) {
    // +開始部分取得
    const startPosition = targetText.substr(prevPosition).indexOf('\n+')
    const endPosition = targetText.substr(prevPosition + startPosition + 2).indexOf('\n')
    if (endPosition === -1) {
      console.log('+部分：' + targetText.substr(prevPosition).substr(startPosition + 2))
    } else {
      console.log('+部分：' + targetText.substr(prevPosition).substr(startPosition + 2, endPosition))
    }

    if (endPosition === -1) { // 最終行の場合
      break
    } else { // 現在の位置を次回の位置へ
      prevPosition += (startPosition + endPosition)
    }
  }
}

function searchRemoveLINE (targetText) {
  // 削除内容探索
  for (let prevPosition = 0; targetText.substr(prevPosition).indexOf('\n-') > -1;) {
    // +開始部分取得
    const startPosition = targetText.substr(prevPosition).indexOf('\n-')
    const endPosition = targetText.substr(prevPosition + startPosition + 2).indexOf('\n')
    if (endPosition === -1) {
      console.log('-部分：' + targetText.substr(prevPosition).substr(startPosition + 2))
    } else {
      console.log('-部分：' + targetText.substr(prevPosition).substr(startPosition + 2, endPosition))
    }

    if (endPosition === -1) { // 最終行の場合
      break
    } else { // 現在の位置を次回の位置へ
      prevPosition += (startPosition + endPosition)
    }
  }
}

export default { diffParse }
