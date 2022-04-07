// {% raw %}

// https://github.com/sparksuite/simplemde-markdown-editor
// Component for markup editor
Vue.component('editorjp', {

    render: function (h) {
        var comps = [this.jp_props.text];

        var vnode = h(this.jp_props.html_tag,
            {
                class: this.jp_props.classes,  // class always shows up in rendering even when there is no class
                style: this.jp_props.style,
                attrs: this.jp_props.attrs,
                on: {
                    change: this.eventFunction,
                },
                directives: [],
                ref: 'r' + this.jp_props.id

            },
            comps);
        return vnode;
    },
    methods: {
        eventFunction: (function (event) {
            eventHandler(this.$props, event);
        })
    },
    mounted() {
        var simplemde = new SimpleMDE({element: (this.$refs['r' + this.$props.jp_props.id])});
        this.$props.simplemde = simplemde;
        this.$props.updated = false;
        var p = this.$props;
        p.updated = true;
        if (this.$props.jp_props.value) {
            simplemde.value(this.$props.jp_props.value);
        } else {
            simplemde.value(this.$props.jp_props.text);
        }
        p.cached_value = simplemde.value();
        p.change_timeout = '';

        // if (props.jp_props.debounce) {
        // clearTimeout(props.timeout);
        // props.timeout = setTimeout(function () {
        //         send_to_server(e, props.jp_props.debug);
        //     }
        //     , props.jp_props.debounce);
    // } else {
    //     send_to_server(e, props.jp_props.debug);
    // }

        simplemde.codemirror.on("change", function (event) {
            clearTimeout(p.change_timeout);
            p.change_timeout = setTimeout(function () {

                p.updated = !p.updated;
                if (p.updated) {
                    return;
                }
                event.type = 'change';
                event.target = {};
                event.target.id = p.jp_props.id;
                event.target.value = simplemde.value();
                event.currentTarget = {};
                event.currentTarget.id = p.jp_props.id;
                event.form_data = false;
                eventHandler(p, event, false, simplemde.codemirror.getCursor());
            }, 200);
        });


    },
    updated() {
        if (this.$props.jp_props.input_type) {
            if (this.$props.cached_value != this.$props.jp_props.value) {
                var cursor_position = this.$props.simplemde.codemirror.getCursor();
                this.$props.simplemde.value(this.$props.jp_props.value);
                this.$props.simplemde.codemirror.setCursor(cursor_position);
                this.$props.cached_value = this.$props.jp_props.value;
            }
        }
    },
    props: {
        jp_props: Object,
    }
});

// {% endraw %}