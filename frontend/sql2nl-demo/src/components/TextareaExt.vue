<script>
export default {
    props: { 'placeholder': String, 'value': String, 'readonly': Boolean, 'showSubmitButton': Boolean },
    emits: ['update:value', 'submit'],
}

</script>

<template>
    <div class="textarea-container">
        <textarea :readonly="readonly" type="text" class="common-input" :placeholder="placeholder" :value="value"
            @input="$emit('update:value', $event.target.value)"></textarea>
        <div v-if="showSubmitButton" class="common-input-button-container">
            <button type="submit" class="common-input-button" @click="$emit('submit')">
                <i class="fa-regular fa-circle-up fa-xl"> 确认 </i>
            </button>
        </div>
    </div>
</template>

<style>
.textarea-container{
    display: block;
    min-width:256px;
    width:750px;
}

.common-input {
    padding: 10px;
    width: 100%;
    height: 96px;
    border-width: 1px;
}

.common-input-button-container {
    display: flex;
    flex-direction: row-reverse;
}

.common-input-button {
    padding: 10px;
}

</style>