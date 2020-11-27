<template>
  <div id="autocomplete">
    <p
      v-if="searchMatch.length > 0"
      @click="selectItem(selectWord)"
      :style="'top: ' + caretPosition.y + 'px; left: ' + caretPosition.x + 'px;'"
      id="autocomplete-word">
      {{ searchMatch[selectWord] }}
      <span
        v-if="searchMatch.length > 1"
        @click="nextWord">{{ selectWord + 1 }}/{{ searchMatch.length }}</span>
    </p>
    <textarea
      id="autocomplete-input"
      @focusout="focusout"
      @focus="focus"
      @keyup="update"
      @keydown.enter.exact.prevent
      @keydown.enter="chooseItem"
      @keydown.tab="chooseItem"
      @keydown.right="nextWord"
      @keydown.8.exact.prevent
      @keydown.8="completeCancel"
      @click="selectItem(selectWord)"
      @compositionend="update"
      @keyup.enter.exact="$emit('bodyEnterAction')"
      @keyup.delete.exact="$emit('bodyDeleteAction')"
      @keydown.ctrl.enter="$emit('sendMail')"
      ref="input"
      v-model="inputValue"></textarea>
    <div
      id="autocomplete-back">
    </div>
  </div>
</template>

<script>
  import TinySegmenter from '../../utils/TinySegmenter'
  import YomikataDict from '../../utils/YomikataDict'
  const yomikataDict = YomikataDict.YomikataDict()

  export default {
    name: 'Test',
    props: {
      inputValue: ''
    },
    data () {
      return {
        searchMatch: [],
        selectedIndex: 0,
        clickedChooseItem: false,
        wordIndex: 0,
        font: {
          size: 17,
          lineheight: 26
        },
        caretPosition: {
          x: 0,
          y: 0
        },
        selectWord: 0
      }
    },
    mounted () {
    },
    computed: {
      listToSearch () {
        if (typeof this.items !== 'undefined' && this.items.length > 0) {
          // いつここを通ってる？
          return this.items
        } else {
          return Object.keys(yomikataDict)
        }
      },
      currentWord () {
        let segmenter = new TinySegmenter.TinySegmenter()
        // this.inputValue:textareaに入ってる文字全て（全角英字も）
        let morphList = segmenter.segment(this.inputValue.substr(0, this.$refs.input.selectionStart).replace(/[Ａ-ｚ]/gm, '').split(/[。]/gm)[this.wordIndex])
        // wordIndex:句読点で区切った中で、一番後ろの要素
        let wordBeforeConversion = morphList.slice(-1)[0]
        // wordBeforeConversion:"おせ"
        return wordBeforeConversion
      },
      inputSplitted () {
        return this.inputValue.split(/[。]/gm)
      }
    },
    watch: {
      'inputValue': function () { // 入力内容が変化した場合
        // 親コンポーネントに内容を渡す
        this.$emit('value', this.inputValue)
        this.focus()
        // 現在のキャレットの位置を更新
        this.getCaret()
      }
    },
    methods: {
      nextWord () {
        if (this.searchMatch.length > 0) {
          let caretPosition = this.$refs.input.selectionStart
          this.$refs.input.setSelectionRange(caretPosition - 1, caretPosition - 1)
          if (this.searchMatch.length === this.selectWord + 1) {
            this.selectWord = 0
          } else {
            this.selectWord++
          }
        }
      },
      completeCancel () {
        // 選択をキャンセルする
        if (this.searchMatch.length > 0) {
          // 候補を初期化
          this.searchMatch = []
        } else {
          // 1文字削除処理
          let caretPosition = this.$refs.input.selectionStart

          // 最初の位置であれば何もしない
          if (caretPosition === 0) {
            return
          }

          // 1文字削除
          this.inputValue = this.inputValue.substr(0, caretPosition - 1) + this.inputValue.substr(caretPosition)

          // キャレットを削除後の位置へ移動
          const self = this
          setTimeout(
            function () {
              self.$refs.input.setSelectionRange(caretPosition - 1, caretPosition - 1)
            },
            1
          )
        }
      },
      update (e) {
        this.inputValue = e.target.value
        // e.target:autocompleteのhtmlタグ
        // e.target.value:textareaの中身全部
        this.selectedIndex = 0
        this.wordIndex = this.inputSplitted.length - 1
        // wordIndex:句読点で区切った中で、一番後ろの要素←keyを押すたびに更新している。
      },
      highlightWord (word) {
        // 構造上ひらがなしか認識してくれないからhighlightしてない
        // return word.replace("(" + this.currentWord + ")/g", '<mark>$1</mark>')
        return word
      },
      setWord (word) {
        let currentWords = this.inputValue.split(/[。]/)
        // サジェストを選択したときに、サジェスト前のtextarea内の全てを句読点で区切ったリスト
        if (typeof word === 'undefined') {
          // this.currentWordがundefinedに変更されるのを防ぐ
          word = ''
        }
        currentWords[this.wordIndex] = currentWords[this.wordIndex].replace(/[Ａ-ｚ]/gm, '').replace(this.currentWord, word)
        // wordIndex（句読点で区切った中で、一番後ろの要素）をサジェストで選択したワードに変換
        this.wordIndex += 1
        this.inputValue = currentWords.join('。')
        document.getElementById('autocomplete-input').focus()
        // 選択した番号をリセット
        this.selectWord = 0
      },
      selectItem (index) {
        // 上と同様
        this.selectedIndex = index
        this.chooseItem()
      },
      chooseItem (e) {
        let caretPosition = this.$refs.input.selectionStart
        const prevInputValue = this.inputValue.length
        this.clickedChooseItem = true

        // 選択肢が存在する場合
        if (this.selectedIndex !== -1 && this.searchMatch.length > 0) {
          // 選択された候補を反映
          this.setWord(this.searchMatch[this.selectWord])
          this.selectedIndex = -1

          // キャレットの位置を増えた文字数分移動
          caretPosition += (this.inputValue.length - prevInputValue - 1)
        } else if (e.key === 'Enter') {
          // エンターキーが押されたものの選択肢が存在しない
          this.inputValue = this.inputValue.substr(0, caretPosition) + '\n' + this.inputValue.substr(caretPosition)
        }

        // キャレットを改行後の位置へ移動
        const self = this
        setTimeout(
          function () {
            self.$refs.input.setSelectionRange(caretPosition + 1, caretPosition + 1)
          },
          1
        )
      },
      focusout (e) {
        setTimeout(() => {
          if (!this.clickedChooseItem) {
            this.searchMatch = []
            this.selectedIndex = -1
          }
          this.clickedChooseItem = false
        }, 100)
      },
      focus () {
        this.searchMatch = []
        if (this.currentWord.length > 1) {
          // this.currentWord:変換前の文字
          let regexp = new RegExp('^' + this.currentWord + '.*$')
          // this.listToSearch:よみがな全リスト
          this.searchMatchHiragana = this.listToSearch.filter(hiragana => hiragana.match(regexp))
          // this.searchMatch:よみがなを漢字入りに戻す
          this.searchMatch = this.searchMatchHiragana.map(hiragana => yomikataDict[hiragana])
        }
        if (this.searchMatch.length === 1 && this.currentWord === this.searchMatch[0]) {
          this.searchMatch = []
        }
        console.log(this.searchMatch)
      },
      getCaret () { // キャレットの位置を取得
        const input = this.$refs.input
        const inputValueSlice = this.inputValue.slice(0, input.selectionStart)

        // 2行以上の場合
        if (inputValueSlice.indexOf('\n') > -1) {
          let prevPosition = 0
          let cnt
          // 改行数を求める
          for (cnt = 0; ; cnt++) {
            const position = inputValueSlice.indexOf('\n', prevPosition + 1)
            if (position + prevPosition >= input.selectionStart || position === -1) { // キャレットの行に到着したときの処理 || 改行文字がもう存在しないとき（末尾行）
              console.log('input.selectionStart : ' + input.selectionStart)
              console.log('prevPosition : ' + prevPosition)
              console.log('this.font.size : ' + this.font.size)
              this.caretPosition.x = (input.selectionStart - prevPosition - 1) * this.font.size + this.font.size
              this.caretPosition.y = cnt * this.font.lineheight
              break
            }
            // 基準となる位置を変更
            prevPosition += position
          }
        } else {
          // 改行されていない場合
          this.caretPosition.x = input.selectionStart * this.font.size + this.font.size
          this.caretPosition.y = 0
        }
        console.log('this.caretPosition : ')
        console.log(this.caretPosition)
      }
    }
  }
</script>

<style lang="scss">
  // 全体の親要素のスタイル
  #autocomplete{
    position: relative;
    display: block;
    width: 100%;
    height: 100%;
  }

  // 入力エリア共通スタイル
  #autocomplete-input, #autocomplete-back{
    position: absolute;
    display: block;
    padding: 5px 10px;
    width: calc(100% - 20px);
    height: calc(100% - 10px);
    outline: none;
    overflow-y: scroll;
    background: none;
    font-size: 17px;
    line-height: 26px;
    font-family: 'JapaneseFont';
    color: #ffffff;
    border: none;
    outline: none;
    resize: none;
  }

  // ユーザ入力用テキストエリア
  #autocomplete-input{
    z-index: 1;

    &:focus{
      border: none;
      outline: none;
    }
  }
  // 背景側UI
  #autocomplete-back{
    z-index: 0;
  }

  // 変換候補のスタイル
  $word-height: 24px;
  #autocomplete-word{
    position: absolute;
    top: 0;
    left: 60px;
    z-index: 100;
    display: block;
    width: auto;
    height: $word-height;
    line-height: $word-height;
    padding: 0 0 0 6px;
    background: #444444;
    color: #ffffff;
    border-radius: 3px;
    overflow: hidden;

    // 変換候補切り替えボタン
    span{
      display: inline-block;
      height: $word-height;
      line-height: $word-height;
      font-size: 0.8em;
      margin: 0 0 0 3px;
      padding: 0 6px;
      background: #ff4441;
      color: #ffffff;
      cursor: pointer;
      -webkit-transition: all 0.3s ease;
      -moz-transition: all 0.3s ease;
      -o-transition: all 0.3s ease;
      transition: all  0.3s ease;
      vertical-align: top;

      &:hover{
        opacity: .7;
      }
    }
  }

</style>