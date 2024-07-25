export default {
    template: "<div><slot></slot></div>",
    mounted() {
        const el = this.$el;

        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave'].forEach(eventName => {
            el.addEventListener(eventName, preventDefaults);
            document.body.addEventListener(eventName, preventDefaults);
        });

        // Highlight drop area when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            el.addEventListener(eventName, () => el.classList.add('dragover'));
        });

        ['dragleave', 'drop'].forEach(eventName => {
            el.addEventListener(eventName, () => el.classList.remove('dragover'));
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        const handleDrop = (e) => {
            this.$emit('__file-dropped', '__file-dropped');
        };

        // Handle dropped files
        el.addEventListener('drop', handleDrop, false);
    },
    methods: {
        async drop_emitter(data) {
            this.$emit('drop_zone', data);
        },
    }
}
