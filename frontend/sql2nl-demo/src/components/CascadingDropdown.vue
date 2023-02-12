
<script>
    export default {
        props: {'selected':Number, 'dropdownItems':Array},
        emits: ['dropdownItemSelected'],
        methods: {
            onDropdownSelect(event){
                // console.log(event.target.value)
                this.$emit('dropdownItemSelected', event.target.value)
            }
        }
    }
    
    </script>
    
    <template>
    <!-- <select name="subject" id="subject"> -->
    <select @change="onDropdownSelect" class="article-content-text">
        <option value="none" class="article-content-text">select db_id here</option>
        <option v-for="(item, index) in dropdownItems" :value="item" :selected="index == selected" class="article-content-text">{{ item }}</option>
    </select>
    </template>
    
    <style scoped>

    </style>