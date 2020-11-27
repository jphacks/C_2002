<template>
  <div id="autocomplete">
    <p
      v-if="searchMatch.length > 0"
      @click="selectItem(selectWord)"
      :style="'top: ' + caretPosition.y + 'px; left: ' + caretPosition.x + 'px;'"
      id="autocomplete-word">
      {{ searchMatch[selectWord] }} <span @click="nextWord">→</span>
    </p>
    <textarea
      id="autocomplete-input"
      @focusout="focusout"
      @focus="focus"
      @keyup="update"
      @keydown.13="chooseItem"
      @keydown.tab="chooseItem"
      @keydown.40="moveDown"
      @keydown.38="moveUp"
      @keydown.right="nextWord"
      @click="selectItem(index)"
      @compositionend="update"
      ref="input"
      v-model="inputValue"></textarea>
    <div
      id="autocomplete-back">
    </div>
  </div>
</template>

<script>
  import TinySegmenter from '../utils/TinySegmenter'
  const yomikataDict = {
    'ありがとうございました': '有難うございました',
    'おせわになっております': 'お世話になっております',
    'いつもおせわになっております': 'いつもお世話になっております',
    'おせわになります': 'お世話になります',
    'さっそくのおへんじありがとうございました': '早速のお返事ありがとうございました',
    'よろしくおねがいいたします': 'よろしくお願いいたします',
    'おへんじおまちしております': 'お返事お待ちしております',
    'おてすうをおかけしますが': 'お手数をおかけしますが',
    'ひきつづきよろしくおねがいいいたします': '引き続きよろしくお願いいたします',
    'ますますのごかつやくをおいのりもうしあげます': 'ますますのご活躍をお祈り申し上げます',
    'もうしわけございません': '申し訳ございません',
    'こんごともよろしくおねがいもうしあげます': '今後ともよろしくお願い申し上げます',
    'ごぶさたしております': 'ご無沙汰しております',
    'ひきつづき、どうぞよろしくおねがいいたします': '引き続き、どうぞよろしくお願いいたします'
  }

  export default {
    name: 'Test',
    data () {
      return {
        id: 'input-' + parseInt(Math.random() * 1000),
        // 現時点では使用していない👆
        inputValue: '',
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
        let morphList = segmenter.segment(this.inputValue.replace(/[Ａ-ｚ]/gm, '').split(/[。]/gm)[this.wordIndex])
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
      inputValue () {
        const input = this.$refs.input
        console.log('passed')
        console.log('selectionStart : ' + input.selectionStart)
        console.log('selectionEnd : ' + input.selectionEnd)
        this.focus()
        this.getCaret()
      }
    },
    methods: {
      nextWord () {
        console.log('right!')
        if (this.searchMatch.length > 0) {
          if (this.searchMatch.length === this.selectWord + 1) {
            this.selectWord = 0
          } else {
            this.selectWord++
          }
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
        // 文章リストを句読点で句切る
      },
      moveDown () {
        // IMEとかのもとからあるサジェストがカーソルキーで動くので、キー動作なしで選択する方がよさそう
        // if (this.selectedIndex < this.searchMatch.length - 1) {
        //   this.selectedIndex++
        // }
      },
      moveUp () {
        // 上と同様
        // if (this.selectedIndex !== -1) {
        //   this.selectedIndex--
        // }
      },
      selectItem (index) {
        // 上と同様
        this.selectedIndex = index
        this.chooseItem()
      },
      chooseItem () {
        this.clickedChooseItem = true
        if (this.selectedIndex !== -1 && this.searchMatch.length > 0) {
          this.setWord(this.searchMatch[this.selectedIndex])
          this.selectedIndex = -1
        }
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
          let regexp = new RegExp('^.*' + this.currentWord + '.*$')
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
      getCaret () {
        const input = this.$refs.input

        // 2行以上の場合
        if (this.inputValue.indexOf('\n') > -1) {
          let prevPosition = 0
          let cnt
          // 改行数を求める
          for (cnt = 0; ; cnt++) {
            const position = this.inputValue.indexOf('\n', prevPosition + 1)
            console.log('position :')
            console.log(position)
            if (position > input.selectionStart) {
              this.caretPosition.x = (input.selectionStart - prevPosition - 1) * this.font.size + 60
              this.caretPosition.y = cnt * this.font.lineheight
              break
            } else if (position === -1) {
              this.caretPosition.x = (input.selectionStart - prevPosition - 1) * this.font.size + 60
              this.caretPosition.y = cnt * this.font.lineheight
              break
            } else if (position === this.inputValue.length) {
              break
            }
            prevPosition += position
          }
        } else {
          // 改行されていない場合
          this.caretPosition.x = input.selectionStart * this.font.size + 60
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
    width: calc(100% - 60px);
    height: 100%;
    padding-left: 60px;
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

  // 入力エリア共通スタイル
  #autocomplete-input, #autocomplete-back{
    position: absolute;
    display: block;
    padding: 20px 10px;
    width: 100%;
    border: 1px solid #ddd;
    outline: none;
    background: none;
    height: 200px;
    font-size: 17px;
    line-height: 26px;
    font-family: 'JapaneseFont'
  }

  // ユーザ入力用テキストエリア
  #autocomplete-input{
    z-index: 1;

    &:focus{
      border-color: #b0c4de;
    }
  }
  // 背景側UI
  #autocomplete-back{
    z-index: 0;
    color: red;
  }
</style>