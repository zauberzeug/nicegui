export default {
    template: "<div><slot></slot></div>",

    data() {
        return {
            isDragging: false,
            isProcessing: false
        }
    },

    mounted() {
        console.log('DropZone component mounted');
        const el = this.$el;

        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave'].forEach(eventName => {
            el.addEventListener(eventName, this.preventDefaults);
            document.body.addEventListener(eventName, this.preventDefaults);
        });

        // Highlight drop area when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            el.addEventListener(eventName, this.handleDragOver);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            el.addEventListener(eventName, this.handleDragLeave);
        });

        // Handle dropped files
        el.addEventListener('drop', this.handleDrop, false);
    },

    beforeDestroy() {
        const el = this.$el;
        // Clean up all event listeners
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            el.removeEventListener(eventName, this.handleDrop);
            el.removeEventListener(eventName, this.handleDragOver);
            el.removeEventListener(eventName, this.handleDragLeave);
            document.body.removeEventListener(eventName, this.preventDefaults);
        });
    },

    methods: {
        preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        },

        handleDragOver() {
            console.log('Drag over event');
            this.isDragging = true;
            this.$el.classList.add('dragover');
        },

        handleDragLeave() {
            console.log('Drag leave event');
            this.isDragging = false;
            this.$el.classList.remove('dragover');
        },

        handleDrop(e) {
            console.log('Drop event triggered');
            this.preventDefaults(e);
            this.isDragging = false;
            this.$el.classList.remove('dragover');

            const files = e.dataTransfer.files;
            console.log('Dropped files:', files);
            console.log('Files data:', Array.from(files).map(f => ({
                name: f.name,
                type: f.type,
                size: f.size
            })));

            const validFiles = Array.from(files).filter(file => true);
            console.log('Valid files to emit:', validFiles);
            this.$emit('__file-dropped', validFiles);
        },

        async drop_emitter(data) {
            console.log('drop_emitter called with data:', data);
            try {
                this.isProcessing = true;
                await this.$emit('drop_zone', data);
                console.log('drop_zone event emitted successfully');
            } catch (error) {
                console.error('Drop zone error:', error);
                this.$emit('error', error);
            } finally {
                this.isProcessing = false;
            }
        }
    }
}