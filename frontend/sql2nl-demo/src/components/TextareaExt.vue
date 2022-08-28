<script>
export default {
    props: { 'placeholder': String, 'value': String, 'readonly': Boolean },
    emits: ['update:value'],
}

</script>

<template>
    <div class="textarea-container">
        <textarea :readonly="readonly" type="text" class="common-input" :placeholder="placeholder" :value="value"
            @input="$emit('update:value', $event.target.value)"></textarea>
    </div>
</template>

<style>
.textarea-container{
    min-width:256px;
    width:750px;
}

.common-input {
    padding: 10px;
    width: 100%;
    height: 96px;
    border-width: 1px;
}
</style>