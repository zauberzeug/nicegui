<template>
    <div tuto v-if="info!=null">
    Aucun tests pr�sents dans {{info.path}}. 
    <br/>
    <br/>
    Que voulez vous faire ?
    <center>
    <button @click="mkSimple()">Creer un test simple</button>
    <button @click="" v-for="i in info.recettes">Creer un test {{i}}</button>
    <button @click="window.close()">Quitter</button>
    </center>
    Reprendre un test precedent ?
    <center>
    <a style="display:block" href="#" @click="select(path,swich)" v-for="swich,path in info.previous">{{path}} [{{swich || "default"}}]</a>
    </center>
    </div>
</template>
<script>
{
    data:function() {
        return {
            info: null,
        }
    },
    mounted: function() {
        wuy.check().then( i=>{
            this.info=i;
            this.$forceUpdate()
        })
    },
    methods: {
        mkSimple() {
            var u=prompt("URL � tester ?")
            if(u && u.trim()) {
                wuy.createTestSimple(u);
            }
        },
        async select(path,swich) {
            await wuy.changePath(path)
            $store.commit("setSwitch",swich);
        },    
    },
}
</script>
<style scoped>
    :scope {
        width:100%;height:100%;
        background: #DDD;
        font-size:2em;
        text-align:center;
    }
    button {
        width:50%;
        display:block;
        font-size: 1em;
        margin:20px;
    }
</style>
