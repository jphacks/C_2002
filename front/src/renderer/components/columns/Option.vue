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
          :key="person">
          {{ person }}
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
          v-for="file in files"
          :key="file['name']">
          {{ file['name'] }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Option',
    props: {
      people: [],
      files: {}
    },
    data () {
      return {
        optionColumn: {
          width: 60,
          mode: 'narrow'
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
    }
  }
</style>