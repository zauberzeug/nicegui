export default {
    template: `
        <q-file
            v-model="file"
            @update:modelValue="file_pick"

            use-chips

            :label="label"
            :multiple="multiple"
            :accept="accept"
        />
    `,

    props: {
        label: String,
        multiple: Boolean,
        accept: String,
    },

    setup() {
        return {
            file: Vue.ref(null),
        };
    },

    methods: {
        file_pick() {
            setTimeout(() => {
                const m_file = this._.subTree.props.modelValue;

                if (!m_file) return;
                if (this.file_url) URL.revokeObjectURL(this.file_url);

                this.file_url = URL.createObjectURL(m_file);

                const m_return = {
                    name: m_file.name,
                    size: m_file.size,
                    type: m_file.type,
                    url: this.file_url,
                    last_modified: m_file.lastModified,
                };

                this.$emit("file_pick", m_return);
            }, 0);
        },
    },
};
