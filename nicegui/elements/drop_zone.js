export default {
  template: `
  <div>
      <div :class="hover_style"></div>
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
      this.$emit("__file-dropped", e);
    };

    // Handle dropped files
    el.addEventListener("drop", handleDrop, false);
  },
  props: {
    hover_style: String,
  },
  methods: {
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
