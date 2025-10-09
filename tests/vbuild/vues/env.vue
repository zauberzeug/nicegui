<!-- doc

-->
<template>
    <div env>
        <template v-if="mode=='view'">
            <button @click="edit()">Edit</button>
            <pre>{{value}}</pre>
        </template>
        <template v-if="mode=='edit'"> {{$store.state.swich}}
            <button @click="save()">Save</button>
            <hr/>
            root:<input v-model="$store.getters.env.root"/>
            <hr/>
            timeout:<input v-model="$store.getters.env.timeout"/>
            <hr/>
            Global Headers:<editDict :dict="$store.getters.env.headers"></editDict>
            <hr/>
        </template>
    </div>
</template>
<script>
{
  props: ["value"],
  data() {
    return {
        mode:"view"
    }
  },
  methods: {
    edit() {
        this.mode="edit"
    },
    save() {
        this.mode="view"
    },
  }
}
</script>
<style scoped>
:scope {background: #DDD;}
</style>
