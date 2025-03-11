export default {
  template: `
  <div>
    <div :class="hover_overlay_style"></div>
    <slot></slot>
  </div>
  `,
  data() {
    return {
      dragCounter: 0,
    };
  },
  mounted() {
    this.$el.addEventListener("dragenter", (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.dragCounter++;
      if (this.dragCounter === 1) {
        this.$emit("drag_over");
      }
    });

    this.$el.addEventListener("dragover", (e) => {
      e.preventDefault();
      e.stopPropagation();
    });

    this.$el.addEventListener("dragleave", (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.dragCounter--;
      if (this.dragCounter === 0) {
        this.$emit("drag_leave");
      }
    });

    this.$el.addEventListener("drop", (e) => {
      e.preventDefault();
      this.dragCounter = 0;
      this.$emit("file_drop", e);
    });
  },
  props: {
    hover_overlay_style: String,
  },
};
