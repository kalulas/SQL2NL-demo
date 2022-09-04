<script setup>
import Greetings from './components/Greetings.vue'
import ToggleButton from './components/ToggleButton.vue'
import TextareaExt from './components/TextareaExt.vue'
import axios from 'axios'
</script>

<script>
export default {
  data() {
    return {
      titleMessage: "sql2nl-demo 站点施工中",
      inputPlaceholder: "在此处输入需要处理的sql语句...",
      outputPlaceholder: "输出结果会显示在这里...",
      inputValue: "SELECT YEAR FROM concert GROUP BY YEAR ORDER BY count(*) DESC LIMIT 1",
      outputValue: "",
      targetModels: [
        { id: 1, name: "BiLSTM", selected: false }, 
        { id: 2, name: "Transformer", selected: false }, 
        { id: 3, name: "Relative-Transformer", selected: false }, 
        { id: 4, name: "TreeLSTM", selected: false }, 
        { id: 5, name: "Bart", selected: false }
      ],
      selectedModels: [],
    }
  },
  components: {
    Greetings,
    ToggleButton,
    TextareaExt,
  },
  computed: {
  },
  methods: {
    updateSelected(selectedArray){
      this.selectedModels = selectedArray
      console.log("selectedModels is current: " + this.selectedModels)
    },

    onSubmitResponse(response){
      console.log("response:")
      console.log(response)
      console.log(response.config.data)
      this.outputValue = response.data
    },
    onSubmitError(response){
      console.log("error response:")
      console.log(response)
      console.log(response.config.data)
    },
    onSubmitBtnClick() {
      axios.post('/predict', {
        sql: this.inputValue,
        selected: this.selectedModels,
      })
      .then(this.onSubmitResponse)
      .catch(this.onSubmitError)
    }
  },

  beforeCreate() {
    let script = document.createElement('script')
    script.src = 'https://kit.fontawesome.com/fcc237718a.js'
    script.crossOrigin = 'anonymous'
    document.getElementsByTagName('head')[0].appendChild(script)
  }
}
</script>

<!-- <script src="https://kit.fontawesome.com/fcc237718a.js" crossorigin="anonymous"></script> -->

<template>
  <header style="margin-bottom: 10px;">
    <img alt="under construction" class="logo" src="./assets/drill.gif" width="200" height="150" />
    <div class="wrapper">
      <Greetings :msg="titleMessage" />
    </div>
  </header>

  <div class="content-item">
    <label class="content-item-title">模型</label>
    <ToggleButton v-for="model in targetModels" 
    :title="model.name" :selected="model.selected" :id="model.id" :selectedModels="selectedModels" @update:selectedModels="updateSelected" :key="model.id"/>
  </div>
  <div class="content-item">
    <label class="content-item-title">SQL</label>
    <TextareaExt :placeholder="inputPlaceholder" :readonly="false" :showSubmitButton="true" v-model:value="inputValue" @submit="onSubmitBtnClick"/>
  </div>
  <div class="content-item">
    <label class="content-item-title">NL</label>
    <TextareaExt :placeholder="outputPlaceholder" :readonly="true" :showSubmitButton="false" v-model:value="outputValue"/>
  </div>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

.content-item {
  display: flex;
  flex-wrap: wrap;
  /* justify-content: center; */
  margin-top: 10px;
  margin-bottom: 10px;
}

.content-item-title{
  display: inline-block;
  width: 64px;
}

.common-input-button {
    padding: 10px;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
