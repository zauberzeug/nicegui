export default {
  async mounted() {
    const { Sortable } = await import("nicegui-sortable");
    const element = document.getElementById(this.elementId);
    this.sortable = Sortable.create(element, {
      ...this.options,
      onEnd: (evt) => {
        const fromId = parseInt(evt.from.id.substring(1));
        const toId = parseInt(evt.to.id.substring(1));
        const fromSlot = window.mounted_app?.elements?.[fromId]?.slots?.default;
        const toSlot = window.mounted_app?.elements?.[toId]?.slots?.default;
        if (fromSlot && fromSlot.ids) {
          const itemId = fromSlot.ids.splice(evt.oldIndex, 1)[0];
          if (fromId === toId) {
            fromSlot.ids.splice(evt.newIndex, 0, itemId);
          } else if (toSlot && toSlot.ids) {
            toSlot.ids.splice(evt.newIndex, 0, itemId);
          }
        }
        element.dispatchEvent(
          new CustomEvent("sortend", {
            detail: {
              item_id: parseInt(evt.item.id.substring(1)),
              from_id: fromId,
              to_id: toId,
              old_index: evt.oldIndex,
              new_index: evt.newIndex,
            },
            bubbles: false,
          }),
        );
      },
    });
  },
  unmounted() {
    this.sortable?.destroy();
  },
  watch: {
    options: {
      deep: true,
      handler(opts) {
        if (this.sortable) {
          Object.entries(opts).forEach(([k, v]) => this.sortable.option(k, v));
        }
      },
    },
  },
  props: {
    elementId: String,
    options: Object,
  },
};
