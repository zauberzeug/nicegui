<template>
    <div>
      <table cellspacing=1 cellpadding=0>
          <tr v-for="(val,key) in dict">
              <td>
                {{key}}
              </td>
              <td>
                <input v-model="dict[key]"/>
              </td>
              <td>
                <a href="#" @click="sup(key)">&#10006;</a>
              </td>
          </tr>
          <tr>
              <td>
                <input v-model="newKey" placeholder="new key"/>
              </td>
              <td>
                <input v-model="newVal" placeholder="new value"/>
              </td>
              <td>
                <a href="#" @click="add()">&#10010;</a>
              </td>
          </tr>
      </table>
      </div>
</template>
<script>
{
  props: ["dict"],
  data:function() {
    return {
        newKey:"",
        newVal:"",
    }
  },
  methods: {
    add() {
        var k=this.newKey.trim()
        var v=this.newVal.trim()
        if(k && v) {
            Vue.set(this.dict,k,v);
            this.newKey=""
            this.newVal=""
        }
    },
    sup(key) {
        Vue.delete(this.dict, key);
    }    
  }
}
</script>
<style scoped>
</style>
