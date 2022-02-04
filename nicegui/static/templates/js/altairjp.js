// {* raw *}

// Uses https://github.com/vega/vega-embed

Vue.component('altairjp', {
    template:
        `<div  v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style"  >
<div v-bind:id="'altair' + jp_props.id" :class="jp_props.classes"  :style="jp_props.style" ></div>
</div>`,
    data: function () {
        return {
            vega_source: {}
        }
    },
    methods: {
        chart_create() {
            this.vega_source = this.$props.jp_props.vega_source;
            el = document.getElementById('altair' + this.$props.jp_props.id.toString());
            vegaEmbed(el, JSON.parse(this.$props.jp_props.vega_source), this.$props.jp_props.options).then(function (result) {
            }).catch(console.error);
        }
    },
    mounted() {
        this.chart_create();
    },
    updated() {
        if (this.vega_source != this.$props.jp_props.vega_source) this.chart_create();
    },
    props: {
        jp_props: Object
    }
});

// {* endraw *}