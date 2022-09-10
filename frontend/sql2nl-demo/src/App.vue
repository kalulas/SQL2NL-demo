<script setup>
import Greetings from './components/Greetings.vue'
import ToggleButton from './components/ToggleButton.vue'
import TextareaExt from './components/TextareaExt.vue'
import CascadingDropdown from './components/CascadingDropdown.vue'
import axios from 'axios'
</script>

<script>
export default {
  data() {
    return {
      titleMessage: "SQL2NL模型的组合泛化能力评估系统",
      inputPlaceholder: "在此处输入需要处理的sql语句...",
      goldInputPlaceholder: "在此处输入参考答案...（可选，填写后输出评分）",
      outputPlaceholder: "输出结果会显示在这里...",
      inputValue: "",
      outputValue: "",
      goldInputValue: "",
      selectedDatabase: "",
      targetModels: [ // TODO get all models from server
        { id: 1, name: "Transformer", selected: false }, 
        { id: 2, name: "Relative-Transformer", selected: false }, 
        { id: 3, name: "BiLSTM", selected: false }, 
        { id: 4, name: "TreeLSTM", selected: false }, 
      ],
      db_ids: [ // TODO get all db_ids from server
        "db_id:0",
        "db_id:1",
        "db_id:2",
        "db_id:3",
      ],
      selectedModels: [],
    }
  },
  components: {
    Greetings,
    ToggleButton,
    TextareaExt,
    CascadingDropdown,
  },
  computed: {
  },
  methods: {
    updateSelected(selectedArray){
      this.selectedModels = selectedArray
      // console.log("selectedModels is current: " + this.selectedModels)
    },
    updateInputValue(inputValue){
      this.inputValue = inputValue
      // console.log("inputValue is now: " + this.inputValue)
    },
    updateGoldInputValue(inputValue){
      this.goldInputValue = inputValue
      // console.log("goldInputValue is now: " + this.goldInputValue)
    },
    onDatabaseSelected(database){
      this.selectedDatabase = database
      console.log("current selected database: " + this.selectedDatabase)
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
      this.outputValue = ""
      axios.post('/predict', {
        sql: this.inputValue,
        gold_nl: this.goldInputValue,
        db_id: this.selectedDatabase,
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
  <header class="title">
    <!-- <img alt="under construction" class="logo" src="./assets/drill.gif" width="200" height="150" /> -->
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
    <label class="content-item-title">db_id</label>
    <CascadingDropdown :dropdownItems="db_ids" @dropdownItemSelected="onDatabaseSelected"/>
  </div>
  <div class="content-item">
    <label class="content-item-title">SQL</label>
    <TextareaExt :placeholder="inputPlaceholder" :readonly="false" :showSubmitButton="false" :value="inputValue" :overrideHeight=60 @update:value="updateInputValue"/>
  </div>
  <div class="content-item">
    <label class="content-item-title">GOLD-NL</label>
    <TextareaExt :placeholder="goldInputPlaceholder" :readonly="false" :showSubmitButton="true" :value="goldInputValue" :overrideHeight=60 @update:value="updateGoldInputValue" @submit="onSubmitBtnClick"/>
  </div>
  <div class="content-item">
    <label class="content-item-title">NL</label>
    <TextareaExt :placeholder="outputPlaceholder" :readonly="true" :showSubmitButton="false" :overrideHeight=320 v-model:value="outputValue"/>
  </div>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.title{
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
  margin-top: 60px;
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
  margin-right: 20px;
}

.common-input-button {
    padding: 10px;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    /* padding-right: calc(var(--section-gap) / 2); */
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
