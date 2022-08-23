<script setup>
import HelloWorld from './components/HelloWorld.vue'
import ToggleButton from './components/ToggleButton.vue'
// import TheWelcome from './components/TheWelcome.vue'
</script>

<script>
export default {
  data() {
    return {
      titleMessage: "sql2nl-demo站点施工中",
      targetModels: [{ id: 1, name: "model1" }, { id: 2, name: "model2" }, { id: 3, name: "model3" }, { id: 4, name: "model4" }, { id: 5, name: "model5" }]
    }
  },
  components: {
    HelloWorld,
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
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld :msg="titleMessage" />
      <ol>
        <!-- TODO: margin to class? -->
        <li style="margin-bottom: 5px;" v-for="model in targetModels">
          <ToggleButton :title="model.name" :id="model.id" :key="model.id"
            @toggleValueChanged="onModelToggleValueChanged" />
        </li>
      </ol>
    </div>
  </header>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
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
