// {* raw *}

// https://docs.bokeh.org/en/latest/docs/user_guide/embed.html

Vue.component('bokehjp', {
    template:
        `<div  v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style">
<div v-bind:id="'bokeh' + jp_props.id"></div>
</div>`,
    data: function () {
        return {
            chart: null
        }
    },
    methods: {
        chart_create() {
            this.chart = this.$props.jp_props.chart;
            const chart_obj = JSON.parse(this.$props.jp_props.chart);
            Bokeh.embed.embed_item(chart_obj, 'bokeh' + this.$props.jp_props.id.toString());
        }
    },
    mounted() {
        this.chart_create();
    },
    updated() {
        if (this.chart != this.$props.jp_props.chart) {
            document.getElementById('bokeh' + this.$props.jp_props.id.toString()).innerHTML = "";
            this.chart_create();
       }
    },
    props: {
        jp_props: Object
    }
});

// {* endraw *}