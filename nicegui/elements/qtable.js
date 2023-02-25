export default {
    template: `
        <q-table

            :rows="rows"
            :columns="columns"

            :row-key="this.selection_key"
            :selection="this.selection_mode"

            v-model:selected="selected"
            @selection="onSelection"
        />
    `,

    setup() {
        return {
            selected: Vue.ref([]),
            filter: Vue.ref(""),
        };
    },

    mounted() {
        // For each Field, Sort and Format field within the column definition,
        // look for '=>' and if so, try to eval to run the function.

        console.info(this.$props.columns);

        this.$props.columns.forEach((col) => {
            if (!col.field || !col.field.includes("=>")) return;
            col.field = eval(col.field);

            if (!col.sort || !col.sort.includes("=>")) return;
            col.sort = eval(col.sort);

            if (!col.format || !col.format.includes("=>")) return;
            col.format = eval(col.format);
        });
    },

    props: {
        columns: Array,
        rows: Array,

        selection_mode: String,
        selection_key: String,
    },

    methods: {
        onSelection() {
            setTimeout(() => {
                this.$emit("selected", this.selected);
            }, 0);
        },

        evalFunction() {
            this.$props.columns.forEach((col) => {
                if (!col.field || !col.field.includes("=>")) return;
                col.field = eval(col.field);

                if (!col.sort || !col.sort.includes("=>")) return;
                col.sort = eval(col.sort);

                if (!col.format || !col.format.includes("=>")) return;
                col.format = eval(col.format);
            });
        },
    },
};
