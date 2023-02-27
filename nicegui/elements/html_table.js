export default {
    template: '<table v-html="this.table_config"></table>',
    props: {
        table_config: String,
    },
};
