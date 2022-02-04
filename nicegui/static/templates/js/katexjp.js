// {* raw *}


Vue.component('katexjp', {
    template:
        `<div  v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style"  ></div>`,
    data: function () {
        return {
            equation: ''
        }
    },
    methods: {
        equation_create() {
            this.equation = this.$props.jp_props.equation;
            katex.render(this.$props.jp_props.equation, document.getElementById(this.$props.jp_props.id.toString()), this.$props.jp_props.options);
        }
    },
    mounted() {
        this.equation_create();
    },
    updated() {
        if (this.equation != this.$props.jp_props.equation) {
            this.equation_create();
        }
    },
    props: {
        jp_props: Object
    }
});

// {* endraw *}