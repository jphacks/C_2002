/*

caretposition.js

Copyright (c) 2012- Hiroki Akiyama http://akiroom.com/
caretposition.js is free software distributed under the terms of the MIT license.
*/

function CaretPosition () {
  // 関数開始
  this.caretPos = function (textarea, mode) {
    // テキストエリアの取得
    let targetElement = textarea
    // HTML Sanitizer
    let escapeHTML = function (s) {
      let obj = document.createElement('pre')
      obj[typeof obj.textContent !== 'undefined' ? 'textContent' : 'innerText'] = s
      return obj.innerHTML
    }

    // Get element css style.
    let getStyle = function (element) {
      let style = element.currentStyle || document.defaultView.getComputedStyle(element, '')
      return style
    }

    // Get element absolute position
    let getElementPosition = function (element) {
      // Get scroll amount.
      let html = document.documentElement
      let body = document.body
      let scrollLeft = (body.scrollLeft || html.scrollLeft)
      let scrollTop = (body.scrollTop || html.scrollTop)

      // Adjust 'IE 2px bugfix' and scroll amount.
      let rect = element.getBoundingClientRect()
      let left = rect.left - html.clientLeft + scrollLeft
      let top = rect.top - html.clientTop + scrollTop
      let right = rect.right - html.clientLeft + scrollLeft
      let bottom = rect.bottom - html.clientTop + scrollTop

      return {
        left: parseInt(left),
        top: parseInt(top),
        right: parseInt(right),
        bottom: parseInt(bottom)
      }
    }

    // 処理部分
    let textAreaPosition = getElementPosition(targetElement)
    let dummyName = targetElement.id + '_dummy'
    let dummyTextArea = document.getElementById(dummyName)
    if (!dummyTextArea) {
      // Generate dummy textarea.
      dummyTextArea = document.createElement('div')
      dummyTextArea.id = dummyName
      let textAreaStyle = getStyle(targetElement)
      dummyTextArea.style.cssText = textAreaStyle.cssText

      // Fix for browser differece.
      // let isWordWrap = false
      if (targetElement.wrap === 'off') {
        // chrome, firefox wordwrap=off
        dummyTextArea.style.overflow = 'auto'
        dummyTextArea.style.whiteSpace = 'pre'
      } else if (!targetElement.wrap === undefined) {
        // firefox wordwrap=on
        dummyTextArea.style.overflowY = 'auto'
      }
      dummyTextArea.style.visibility = 'hidden'
      dummyTextArea.style.position = 'absolute'
      dummyTextArea.style.top = '0px'
      dummyTextArea.style.left = '0px'

      // Firefox Support
      dummyTextArea.style.width = textAreaStyle.width
      dummyTextArea.style.height = textAreaStyle.height
      dummyTextArea.style.fontSize = textAreaStyle.fontSize
      dummyTextArea.style.maxWidth = textAreaStyle.width
      dummyTextArea.style.backgroundColor = textAreaStyle.backgroundColor
      dummyTextArea.style.fontFamily = textAreaStyle.fontFamily

      targetElement.parentNode.appendChild(dummyTextArea)
    }

    // Set scroll amount to dummy textarea.
    dummyTextArea.scrollLeft = targetElement.scrollLeft
    dummyTextArea.scrollTop = targetElement.scrollTop

    // Set code strings.
    let codeStr = targetElement.value

    // キャレットの位置の取得
    let selPos = getCaretPosition(targetElement)
    let leftText = codeStr.slice(0, selPos.start)
    let selText = codeStr.slice(selPos.start, selPos.end)
    let rightText = codeStr.slice(selPos.end, codeStr.length)
    if (selText === '') selText = 'a'

    // Set keyed text.
    let processText = function (text) {
      // Get array of [Character reference] or [Character] or [NewLine].
      let m = escapeHTML(text).match(/((&amp;|&lt;|&gt;|&#34;|&#39;)|.|\n)/g)
      if (m) {
        return m.join('<wbr>').replace(/\n/g, '<br>')
      } else {
        return ''
      }
    }

    // Set calculation text for in dummy text area.
    dummyTextArea.innerHTML = (processText(leftText) +
      '<wbr><span id="' + dummyName + '_i">' + processText(selText) + '</span><wbr>' +
      processText(rightText))

    // Get caret absolutely pixel position.
    let dummyTextAreaPos = getElementPosition(dummyTextArea)
    let caretPos = getElementPosition(document.getElementById(dummyName + '_i'))
    switch (mode) {
      case 'self':
        // Return absolutely pixel position - (0,0) is most top-left of TEXTAREA.
        return {
          left: caretPos.left - dummyTextAreaPos.left,
          top: caretPos.top - dummyTextAreaPos.top
        }
      case 'body':
      case 'screen':
      case 'stage':
      case 'page':
      default:
        // Return absolutely pixel position - (0,0) is most top-left of PAGE.
        return {
          left: textAreaPosition.left + caretPos.left - dummyTextAreaPos.left,
          top: textAreaPosition.top + caretPos.top - dummyTextAreaPos.top
        }
    }
  }
}

// キャレット位置の取得
let getCaretPosition = function (element) {
  let startpos = -1
  let endpos = -1

  // 選択されている場合
  if (document.selection) {
    let docRange = document.selection.createRange()
    let textRange = document.body.createTextRange()
    textRange.moveToElementText(element)

    let range = textRange.duplicate()
    range.setEndPoint('EndToStart', docRange)
    startpos = range.text.length

    range = textRange.duplicate()
    range.setEndPoint('EndToEnd', docRange)
    endpos = range.text.length
  } else if (element.selectionStart || element.selectionStart === '0') {
    // Firefox support
    startpos = element.selectionStart
    endpos = element.selectionEnd
  }
  return {start: startpos, end: endpos}
}

export default CaretPosition
