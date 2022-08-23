<script setup>
import Greetings from './components/Greetings.vue'
import ToggleButton from './components/ToggleButton.vue'
</script>

<script>
export default {
  data() {
    return {
      titleMessage: "sql2nl-demo 站点施工中",
      targetModels: [{ id: 1, name: "model1" }, { id: 2, name: "model2" }, { id: 3, name: "model3" }, { id: 4, name: "model4" }, { id: 5, name: "model5" }]
    }
  },
  components: {
    Greetings,
    ToggleButton
  },
  methods: {
    onModelToggleValueChanged(modelID) {
      console.log(`toggle[${modelID}] value is changed`)
    }
  }
}

</script>

<template>
  <header>
    <img alt="under construction" class="logo" src="./assets/drill.gif" width="200" height="150" />
    <div class="wrapper">
      <Greetings :msg="titleMessage" />
    </div>
  </header>

  <!-- <div class="content-item">
    TODO: input
  </div> -->
  <div class="content-item">
    <ToggleButton v-for="model in targetModels" :title="model.name" :id="model.id" :key="model.id"
      @toggleValueChanged="onModelToggleValueChanged" />
  </div>
  <!-- <div class="content-item">
    TODO: submit btn
  </div>
  <div class="content-item">
    TODO: outcome
  </div> -->
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
  justify-content: center;
  margin-top: 1rem;
  margin-bottom: 1rem;
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
