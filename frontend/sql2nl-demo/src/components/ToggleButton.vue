
<script>
export default {
    props: {'id':Number, 'title':String, 'selected':Boolean, 'selectedModels':Array},
    emits: ['update:selectedModels'],
    methods: {
        onToggleValueChanged(event){
            // console.log(`${this.title} changed to ${event.target.checked}`)
            var current = this.title
            if (event.target.checked && !this.selectedModels.includes(current)) {
              this.selectedModels.push(current)
            }
            else if(!event.target.checked && this.selectedModels.includes(current)) {
              var idx = this.selectedModels.indexOf(current)
              this.selectedModels.splice(idx, 1)
            }

            this.$emit('update:selectedModels', this.selectedModels)
        }
    }
}

</script>

<template>
<!-- reference: https://www.w3schools.com/howto/howto_css_switch.asp-->
<div class="toggle-btn">
<label class="switch">
  <input type="checkbox" :checked="selected" :value="title" @change="onToggleValueChanged">
  <!-- <span class="slider round"></span> -->
</label>
<label class="article-content-text">{{ title }}</label>
</div>
</template>

<style scoped>
.toggle-btn {
  /* display: inline-flex; */
  display: flex;
  margin-right: 10px;
}

.switch {
  margin-left: 5px;
  margin-right: 5px;
}
/*
.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
  margin-left: 5px;
  margin-right: 5px;
}

.switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}*/

/* Rounded sliders */
/*
.slider.round {
  border-radius: 24px;
}

.slider.round:before {
  border-radius: 50%;
} */
</style>