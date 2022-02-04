// {* raw *}


Vue.component('plotlyjp', {
    template:
        `<div  v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style"  >
<div v-bind:id="'plt' + jp_props.id" class="plotly-graph-div js-plotly-plot" style="height:600px; width:500px;"></div>
</div>`,
    data: function () {
        return {
            chart: null
        }
    },
    methods: {
        chart_create() {
            // console.log(this.$props.jp_props);
            this.chart = this.$props.jp_props.chart;
            const chart_obj = JSON.parse(this.$props.jp_props.chart);
            // https://plotly.com/javascript/plotlyjs-function-reference/
            Plotly.react(document.getElementById('plt'+this.$props.jp_props.id.toString()),
                chart_obj['data'], chart_obj['layout'], this.$props.jp_props.config);

            // this.$nextTick(function () {
           // katex.render(this.$props.jp_props.chart, document.getElementById(this.$props.jp_props.id.toString()), {throwOnError: false});
            // });
        }
    },
    mounted() {
        this.chart_create();
    },
    updated() {
        this.chart_create();
//         this.$nextTick(function() {
// });


    },
    props: {
        jp_props: Object
    }
});

// {* endraw *}