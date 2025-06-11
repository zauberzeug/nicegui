export default {
  template: `<div><slot></slot></div>`,
  props: {
    tableCellSlotId: String,
    dataProps: Object,
  },
  async mounted() {
    if (this.tableCellSlotId === null) {
      return;
    }
    await this.$nextTick()
    const target = getElement(this.tableCellSlotId);
    runMethod(target, 'collectProps', [this.dataProps])
  },
};