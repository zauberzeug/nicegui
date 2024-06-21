export default {
    template: `<slot></slot>`,
    data() {
        this.rowProps = [];
        this.loaded = false;
    },

    methods: {
        collectProps(props) {
            if (!this.loaded) {
                this.rowProps.push(props);
            } else {
                this.$emit("placeholder_updated", props);
            }
        },
        emitUpdated() {
            this.rowProps.forEach(props => {
                this.$emit("placeholder_updated", props);
            })
            this.rowProps.length = 0;
        },
        setLoaded() {
            this.loaded = true;
            this.emitUpdated();
        },
    }
};