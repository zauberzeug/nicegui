export default {
  template: `
  <div>
      <div :class="drop_style"></div>
      <slot></slot>
  </div>`,
  mounted() {
    const el = this.$el;

    // Prevent default drag behaviors
    ["dragenter", "dragover", "dragleave"].forEach(eventName => {
      el.addEventListener(eventName, preventDefaults);
      document.body.addEventListener(eventName, preventDefaults);
    });

    // Highlight drop area when item is dragged over it
    ["dragenter", "dragover"].forEach(eventName => {
      el.addEventListener(eventName, () => this.$emit("drag_over", "drag_over"));
    });

    ["dragleave", "drop"].forEach(eventName => {
      el.addEventListener(eventName, () => this.$emit("drag_leave", "drag_leave"));
    });

    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
    }

    const handleDrop = (e) => {
      this.$emit("__file-dropped", "__file-dropped");
    };

    // Handle dropped files
    el.addEventListener("drop", handleDrop, false);
  },
  props: {
    drop_style: String,
  },
  methods: {
    handleDragLeave() {
      this.isDragging = false;
      this.$el.classList.remove("dragover");
    },

    handleDrop(e) {
      this.preventDefaults(e);
      this.isDragging = false;
      this.$el.classList.remove("dragover");

      const files = e.dataTransfer.files;

      const validFiles = Array.from(files).filter(file => true);
      this.$emit("__file-dropped", validFiles);
    },

    async drop_emitter(data) {
      try {
        this.isProcessing = true;
        await this.$emit("drop_zone", data);
      } catch (error) {
        console.error("Drop zone error:", error);
        this.$emit("error", error);
      } finally {
        this.isProcessing = false;
      }
    }
  }
}
