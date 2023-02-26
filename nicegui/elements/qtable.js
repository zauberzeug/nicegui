function eval_fields(cols) {
    // For each Field, Sort and Format field within the column definition,
    // look for '=>' and if so, try to eval to run the function.

    cols.forEach((col) => {
        if (!col.field || !col.field.includes("=>")) return;
        col.field = eval(col.field);

        if (!col.sort || !col.sort.includes("=>")) return;
        col.sort = eval(col.sort);

        if (!col.format || !col.format.includes("=>")) return;
        col.format = eval(col.format);
    });
}

export default {
    template: `
        <q-table
            :rows="rows"
            :columns="columns"

            :row-key="this.selection_key"
            :selection="this.selection_mode"

            v-model:selected="selected"
            @selection="onSelection"

            :filter="filter"
        >

        <template v-slot:top-right>
            <q-input v-model="filter" type="search" :label=filter_config.label :placeholder=filter_config.placeholder :counter=filter_config.counter :filled=filter_config.filled :outlined=filter_config.outlined :standout=filter_config.standout :borderless=filter_config.borderless :color=filter_config.color :dense=filter_config.dense >
                <template v-slot:append>
                    <q-icon :name=filter_config.icon />
                </template>
            </q-input>
        </template>

      </q-table>
    `,

    setup() {
        return {
            selected: Vue.ref([]),
            filter: Vue.ref(""),
        };
    },

    mounted() {
        eval_fields(this.$props.columns);
    },

    props: {
        columns: Array,
        rows: Array,

        selection_mode: String,
        selection_key: String,

        filter_config: Object,
    },

    methods: {
        onSelection() {
            setTimeout(() => {
                this.$emit("selected", this.selected);
            }, 0);
        },

        evalFunction() {
            eval_fields(this.$props.columns);
        },
    },
};
