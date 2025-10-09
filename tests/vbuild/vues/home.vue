<template>
  <div>
      <template v-if="$store.state.mode=='loaded'">
        <div id="top" v-if="$store.getters.switchs">
          <span :class="[ 'switch', {'sel': s==$store.state.swich} ]" v-for="s in $store.getters.switchs" @click="$store.dispatch('setSwitch',s)">{{s || "default"}}</span>
        </div>
        <div id="main">
            <list></list>
            <req :value="$store.state.echange" v-if="$store.state.echange!=null"></req>
            <env :value="$store.getters.scope" v-if="$store.state.echange==null"></env>
        </div>
      </template>
                    
      <template v-if="$store.state.mode=='start'">
            <loading></loading>
      </template>
      
      <template v-if="$store.state.mode=='new'">
            <tuto></tuto>
      </template>
      
   </div>
</template>
<script>
{
    mounted: function() {
        this.$store.dispatch("reqLoad")
    },
}
</script>
<style scoped>

:scope {
    width:100%;height:100%;    
}

#top {
    background:#EEE;
    position: fixed;
    top:0px;
    left:0px;
    right:0px;
    height:30px;
}

#main {
    position: fixed;
    top:30px;
    left:0px;
    right:0px;
    bottom:0px;

    display:flex;
    flex-flow:row nowrap;
}

#main > * {
    flex: 0 0 50%;
    width:50%;
    height:100%;
    overflow-y: auto;
}

.switch {padding:1px;background:#CCC;border:1px solid grey;cursor:pointer;display:inline-block}
.switch.sel {border:1px solid black;background:white}

</style>
