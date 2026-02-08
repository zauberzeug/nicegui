import { Sortable } from "nicegui-sortable";

export default {
  template: `<div><slot></slot></div>`,
  props: {
    options: Object,
  },
  async mounted() {
    this.sortable = Sortable.create(this.$el, { ...this.options, onChange: () => this.$emit("sort_change") });
  },
  beforeUnmount() {
    this.sortable?.destroy();
  },
};
