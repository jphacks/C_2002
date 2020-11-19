<template>
  <div
    id="option"
    v-on:mouseover="optionMouseOver"
    v-on:mouseleave="optionMouseLeave"
    :style="'width: ' + optionColumn.width + 'px'">

    <div class="number_sign">
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
  </div>
</template>

<script>
  export default {
    name: 'Option',
    props: {
      people: []
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
    padding-left: 20px;
    li{
      margin-top: 10px;
    }
  }
</style>