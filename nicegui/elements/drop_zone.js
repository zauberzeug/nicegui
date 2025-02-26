export default {
  template: `
  <div>
    <div :class="hover_overlay_style"></div>
    <slot></slot>
  </div>
  `,
  data() {
    return {
      dragCounter: 0
    }
  },
  mounted() {
    const el = this.$el;

    el.addEventListener("dragenter", (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.dragCounter++;
      if (this.dragCounter === 1) {
        this.$emit("drag_over", "drag_over");
      }
    });

    el.addEventListener("dragover", (e) => {
      e.preventDefault();
      e.stopPropagation();
    });

    el.addEventListener("dragleave", (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.dragCounter--;
      if (this.dragCounter === 0) {
        this.$emit("drag_leave", "drag_leave");
      }
    });

    el.addEventListener("drop", (e) => {
      e.preventDefault();
      this.dragCounter = 0;
      this.$emit("drag_leave", "drag_leave");
      this.$emit("__file_dropped", e);
    });
  },
  props: {
    hover_overlay_style: String,
  },
}
