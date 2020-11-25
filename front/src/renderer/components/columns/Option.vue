<template>
  <div
    id="option"
    v-on:mouseover="optionMouseOver"
    v-on:mouseleave="optionMouseLeave"
    :style="'width: ' + optionColumn.width + 'px'">

    <div class="number_sign" style="color: #ff3c41">
      <h2>{{ people.length }}</h2>
      people
    </div>
    <div
      class="name_list"
      v-if="optionColumn.mode === 'wide'">
      <ul>
        <li
          v-for="person in people"
          @click="replaceSet(person)"
          :key="person">
          {{ person }}
        </li>
      </ul>
    </div>

    <div class="number_sign" style="color: #0080ff">
      <h2>{{ companies.length }}</h2>
      companies
    </div>
    <div
      class="name_list"
      v-if="optionColumn.mode === 'wide'">
      <ul>
        <li
          v-for="company in companies"
          @click="replaceSet(company)"
          :key="company">
          {{ company }}
        </li>
      </ul>
    </div>

    <div class="number_sign" style="color: #ff7100">
      <h2>{{ Object.keys(files).length }}</h2>
      files
    </div>
    <div
      class="name_list"
      v-if="optionColumn.mode === 'wide'">
      <ul>
        <li
          v-for="(file, index) in files"
          :key="index"
          title="ファイルを開く"
          @click="openFile(file['path'])">
          {{ file['name'] }}
          <span
            class="remove_file"
            title="ファイルを削除"
            @click.stop="removeFile(index)">
          </span>
        </li>
      </ul>
    </div>

    <div
      id="replace_area"
      v-if="optionColumn.mode === 'wide'">
      <input type="text" v-model="replace.target" placeholder="">
      <input type="text" v-model="replace.update" placeholder="">
      <button @click="replaceExe">置換</button>
    </div>
  </div>
</template>

<script>
  import OS from '../../utils/OS'
  const childProcess = require('child_process')

  export default {
    name: 'Option',
    props: {
      people: [],
      companies: [],
      files: {}
    },
    data () {
      return {
        optionColumn: {
          width: 60,
          mode: 'narrow'
        },
        replace: {
          target: '',
          update: ''
        }
      }
    },
    methods: {
      optionMouseOver () {
        this.optionColumn.width = 200
        this.optionColumn.mode = 'wide'
      },
      optionMouseLeave () {
        this.optionColumn.width = 60
        this.optionColumn.mode = 'narrow'
      },
      replaceSet (targetText) {
        this.replace.target = targetText
      },
      replaceExe () {
        // 置換
        this.$emit('replaceText', {
          target: this.replace.target,
          update: this.replace.update,
          timestamp: new Date()
        })
      },
      openFile (path) {
        // OS毎に処理を変更
        if (OS.isWindows()) {
          this.exe('start ' + path, OS.homeDirectory())
        } else {
          this.exe('open ' + path, OS.homeDirectory())
        }
      },
      removeFile (fileKey) {
        // 添付ファイルの削除
        delete this.files[fileKey]
        console.log(this.files)
      },
      exe (command, pwd = OS.homeDirectory()) { // コマンド実行関数
        console.log('実行コマンド：' + command)
        console.log('実行ディレクトリ：' + pwd)

        // 実行部分 https://nodejs.org/api/childProcess.html
        const child = childProcess.exec(command, {
          cwd: pwd, // 子プロセスの現在の作業ディレクトリ（デフォルト：null）
          shell: true // コマンドを実行するシェル（デフォルト： [Unix]/bin/sh [Windows]process.env.ComSpec）
        })

        return child
      }
    }
  }
</script>

<style lang="scss">
  #option{
    display: inline-block;
    width: 60px;
    height: 100vh;
    vertical-align: top;
    background: #222222;
    color: #ffffff;
    -webkit-transition: all 0.2s ease;
    -moz-transition: all 0.2s ease;
    -o-transition: all 0.2s ease;
    transition: all  0.2s ease;
  }

  // 各種パラメータの数値表現の際のスタイル
  .number_sign{
    margin-top: 15px;
    font-size: 15px;
    font-weight: bold;
    color: #5645ff;
    text-align: center;

    h2{
      font-size: 25px;
    }
  }

  // 名称一覧
  .name_list{
    li{
      margin-top: 10px;
      display: inline-block;
      max-width: 80%;
      margin-left: 5%;
      padding: 5px 5%;
      word-break: break-all;
      background: #777777;
      border-radius: 10px;
      font-size: 15px;
      cursor: pointer;

      -webkit-transition: all 0.3s ease;
      -moz-transition: all 0.3s ease;
      -o-transition: all 0.3s ease;
      transition: all  0.3s ease;

      &:hover{
        opacity: .7;
      }
    }
  }

  // 添付ファイル削除ボタン
  .remove_file{
    display: inline-block;
    width: 15px;
    height: 15px;
    vertical-align: middle;
    background-image:  url('../../assets/img/removeFile.png');
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;

    -webkit-transition: all 0.3s ease;
    -moz-transition: all 0.3s ease;
    -o-transition: all 0.3s ease;
    transition: all  0.3s ease;

    &:hover{
      background-image:  url('../../assets/img/removeFileActive.png');
    }
  }

  // 置換部分
  #replace_area{
    position: absolute;
    width: 100%;
    right: 0;
    bottom: 0;

    input[type="text"]{
      display: block;
      width: 86%;
      height: 30px;
      margin: 4px 5%;
      padding: 0 2%;
      background: #444444;
      outline: none;
      border: solid 1px #aaaaaa;
      border-radius: 3px;
      color: #ffffff;
      font-size: 15px;
    }

    button{
      display: block;
      width: 80px;
      height: 28px;
      margin: 4px calc((200px - 80px) / 2) 10px;
      background: #ff4441;
      border-radius: 30px;
      color: #ffffff;
      font-size: 15px;
      font-weight: bold;
      text-align: center;

      -webkit-transition: all 0.3s ease;
      -moz-transition: all 0.3s ease;
      -o-transition: all 0.3s ease;
      transition: all  0.3s ease;

      &:hover{
        opacity: .7;
      }
    }
  }
</style>