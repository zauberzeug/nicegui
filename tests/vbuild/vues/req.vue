<template>
<div req>

    <template v-if="mode!='view'">
        <div class="min">
            <button class="right" @click="replay()">replay</button> 
            <button class="right" @click="mode='view'">close</button> 
            <select v-model="value.req.method">
              <option>GET</option>
              <option>PUT</option>
              <option>POST</option>
              <option>DELETE</option>
            </select>        
            {{value.req.protocol}}://{{value.req.host}}{{value.req.port ? ":"+value.req.port : ""}} <br/>
        </div>
        <input class="min" v-model="value.req.path" size="80" style="width:100%"/>
        <editDict :dict="value.req.headers"></editDict>
        <textarea class="min" v-model="body"    cols="80" rows="12" placeholder="no body"></textarea>
    </template>
        
    <template v-if="mode=='view'">
        <div class="min">
            <b @click="mode='edit'">Question</b>
        </div>

<pre class="win max">
<b>{{value.req.method}} {{value.req.url}}</b>
<template v-for="v,k in value.req.headers"><b>{{k}}:</b> {{v}}
</template>{{prettify(value.req.body)}}
</pre>

    </template>
    
    <template v-if="value.res != null">
        <div class="min">
        <span class="right">({{value.res.time}})</span>
        <b>Reponse --> {{value.res.info}}</b>
        </div>
    
<pre class="win max">
<template v-for="v,k in value.res.headers"><b>{{k}}:</b> {{v}}
</template>{{prettify(value.res.content)}}
</pre>
    
    </template>
    
    
    <div class="max" v-if="value.res == null">
        Impossible d'executer �a ;-)
    </div>
    
    <div v-if="value.result.length>0" class="win">
        <b>Tests</b>
      <ul>
        <li v-for="i in value.result" :class="{'ok': i.value, 'ko':!i.value}">
            {{i.name}}
        </li>
      </ul>
    </div>
    
  </div>
</template>
<script>
{
  props: ["value"],
  data() {
    return {
        mode:"view",
    }
  },
  computed: {
    body: {
        get() { return this.prettify(this.value.req.body);},
        set(v) {this.value.req.body=v;}
    },
  },
  methods: {
    prettify: function(o) {
        if(o) {
            try { return JSON.stringify( JSON.parse(o), null, 2); }
            catch(e) { return o; }
        }
        else
            return "";
    },
    replay: async function() {
        var req={
            method:  this.value.req.method,
            path:    this.value.req.path.trim().toLowerCase().startsWith("http")?this.value.req.path:this.value.req.protocol+"://"+this.value.req.host+(this.value.req.port ? ":"+this.value.req.port : "")+this.value.req.path,
            body:    this.value.req.body,
            headers: this.value.req.headers,
            params:  [],
            saves:   [],
            tests:   [],
        }
        var r=await this.$store.dispatch("testRequest",req)
        this.$store.commit("setEchange",r)
    },
  }
}
</script>
<style scoped>
    :scope {
        background:#EEE;
        display:flex;
        flex-flow:column nowrap;
    }
    .min {
        flex: 0 0 auto;
    }
    .max {
        flex: 1 1 50%;
    }
</style>

