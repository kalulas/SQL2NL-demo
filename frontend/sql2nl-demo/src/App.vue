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
      proccessingRequestCount: 0,
      titleMessage: "SQL2NL模型的组合泛化能力评估系统",
      inputPlaceholder: "在此处输入需要处理的sql语句...",
      goldInputPlaceholder: "在此处输入参考答案...（可选，填写后输出评分）",
      outputPlaceholder: "输出结果会显示在这里...",
      inputValue: "",
      outputValue: "",
      goldInputValue: "",
      selectedDatabase: "",
      targetModels: [],
      db_ids: [],
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
    isRequestProcessing(){
      return this.proccessingRequestCount != 0
    }
  },
  methods: {
    getPredictionStrFromObject(resultObject){
      if (resultObject.success) {
        if (resultObject.hasScore) {
          return `[${resultObject.modelName}] ${resultObject.result}\n (BLEU:${resultObject.score})`
        }

        return `[${resultObject.modelName}] ${resultObject.result}`
      }

      return `[${resultObject.modelName}] 解析失败！\n (reason:${resultObject.failedReason})`
    },

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
      // console.log("current selected database: " + this.selectedDatabase)
    },

    onRequestPredictResponse(response){
      this.proccessingRequestCount -= 1
      console.log(response)
      var output = ""
      response.data.forEach(element => {
        output += this.getPredictionStrFromObject(element) + '\n\n'
      });

      this.outputValue = output
    },
    onRequestFailed(response){
      this.proccessingRequestCount -= 1
      console.log("error response:")
      console.log(response)
    },
    requestPredict() {
      this.outputValue = ""
      axios.post('/predict/', {
        sql: this.inputValue,
        gold_nl: this.goldInputValue,
        db_id: this.selectedDatabase,
        selected: this.selectedModels,
      })
      .then(this.onRequestPredictResponse)
      .catch(this.onRequestFailed)
      this.proccessingRequestCount += 1
    },

    onRequsetAvailableModelsResponse(response){
      this.proccessingRequestCount -= 1
      console.log(response)
      this.targetModels = new Array(response.data.length);
      for (let index = 0; index < response.data.length; index++) {
        const element = response.data[index];
        this.targetModels[index] = { "id": index + 1, "name": element, "selected": false }
      }

      console.log(this.targetModels.length + " models received")
    },
    requestAvailableModels(){
      axios.post('/predict/models/').then(this.onRequsetAvailableModelsResponse).catch(this.onRequestFailed)
      this.proccessingRequestCount += 1
    },

    onRequestAvailableDatabasesResponse(response){
      this.proccessingRequestCount -= 1
      console.log(response)
      this.db_ids = response.data
      this.db_ids.sort()
      console.log(this.db_ids.length + " databases received")
    },
    requestAvailableDatabases(){
      axios.post('/predict/databases/').then(this.onRequestAvailableDatabasesResponse).catch(this.onRequestFailed)
      this.proccessingRequestCount += 1
    },
  },

  mounted() {
    this.requestAvailableModels()
    this.requestAvailableDatabases()
  }
  // beforeCreate() {
  //   let script = document.createElement('script')
  //   script.src = 'https://kit.fontawesome.com/fcc237718a.js'
  //   script.crossOrigin = 'anonymous'
  //   document.getElementsByTagName('head')[0].appendChild(script)
  // }
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
    <TextareaExt :placeholder="goldInputPlaceholder" :readonly="false" :showSubmitButton="true" :disableSubmitButton="isRequestProcessing" :value="goldInputValue" :overrideHeight=60 @update:value="updateGoldInputValue" @submit="requestPredict"/>
  </div>
  <div v-show="isRequestProcessing" class="content-item" style="justify-content: center;">
    <img alt="now loading..." src="./assets/Pulse-1s-200px.gif"/>
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
