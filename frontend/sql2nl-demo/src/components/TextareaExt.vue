<script>
export default {
    props: { 'placeholder': String, 'value': String, 'readonly': Boolean },
    emits: ['update:value'],
}

</script>

<template>
    <div>
        <textarea :readonly="readonly" type="text" class="common-input" :placeholder="placeholder" :value="value"
            @input="$emit('update:value', $event.target.value)"></textarea>

    </div>
</template>

<style>
.common-input {
    padding: 10px;
    width: 756px;
    height: 96px;
    border-width: 1px;
    /* border-radius: 25px;
    border-top-right-radius: 0px;
    border-bottom-right-radius: 0px; */
}
</style>