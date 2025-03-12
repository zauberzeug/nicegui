export default {
  template: `
    <div>
      <div :class="hover_overlay_style"></div>
      <slot></slot>
    </div>
  `,
  mounted() {
    this.$el.addEventListener("dragenter", (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.$emit("drag_enter");
    });
    this.$el.addEventListener("dragover", (e) => {
      e.preventDefault();
      e.stopPropagation();
    });
    this.$el.addEventListener("dragleave", (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.$emit("drag_leave");
    });
    this.$el.addEventListener("drop", (e) => {
      e.preventDefault();
      this.$emit("file_drop", e);
    });
  },
  props: {
    hover_overlay_style: String,
  },
};
