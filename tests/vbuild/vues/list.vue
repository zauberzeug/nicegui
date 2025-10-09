<template>
        <div>
            <a href="#" @click="runAll()" title="Run all">&#9654;</a> All
            
            <div class="reqs" v-for="g in $store.state.groups" :key="g.name">
            <h4><a href="#" @click="makeTests(g.reqs)">&#9654;</a> {{g.name}}</h4>
            <div :class="[ 'groupsreq', {'ok': req.run && req.tests.length==req.run.oks,'ko': req.run && req.tests.length!=req.run.oks } ]" v-for="(req,index) in g.reqs" :key="index" @click="testAndEdit(req)">
              <div :class="['route',req.method, req.selected && 'selected']">{{index+1}}<span>{{req.method}}</span>{{req.path}}
                   <i class="right" v-if="req.run">{{req.run.oks}}/{{req.tests.length}}</i>
              </div>

            </div>
          </div>
        </div>
</template>
<script>
{
      methods: {
        testAndEdit: async function(req) {
            var r=await this.$store.dispatch("testRequest",req)
            this.$store.commit("setSelected",req)
            this.$store.commit("setEchange",r)
        },
        makeTests: async function(reqs) {
            for(var req of reqs)
                this.$store.dispatch("testRequest",req)
        },
        runAll: async function() {
            var ll=[];
            for(var g of this.$store.state.groups)
                for(var r of g.reqs )
                    ll.push(r)
            this.makeTests(ll)
        },
      },

}
</script>
<style scoped>
h4 {padding:0px; margin:2px; color:blue;font-size:0.8em;margin-top:14px}
.reqs{ white-space: nowrap;}
.groupsreq {background:white; cursor:pointer;padding:4px;font-size:0.8em}

.route > span {padding:2px;border-radius:8px;margin:2px;color:black;display:inline-block;width:60px;text-align:center}
.route.GET > span {background:#AAFFAA}
.route.POST > span {background:#FFFFAA}
.route.PUT > span {background:#FFCCAA}
.route.DELETE > span {background:#FFCCCC}
.route.selected {background:#EEE}
</style>

