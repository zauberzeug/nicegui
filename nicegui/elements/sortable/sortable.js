import { Sortable } from "nicegui-sortable";

function CancelClonePlugin() {
  function CancelClone() {
    this.defaults = { cancelClone: false };
  }

  CancelClone.prototype = {
    drop({ rootEl, parentEl, dispatchSortableEvent, dragEl, cloneEl, newIndex, oldIndex }) {
      if (!this.options.cancelClone) return;

      // Only call revertOnSpill if an actual drag operation occurred
      if (!this.sortable.revertOnSpill?.onSpill || rootEl == parentEl) return;

      const originalIndex = oldIndex;

      this.sortable.revertOnSpill.onSpill(...arguments);

      // After reverting, move the element back to its original position
      if (dragEl && rootEl && originalIndex !== undefined) {
        const children = Array.from(rootEl.children);
        const currentIndex = children.indexOf(dragEl);

        // If it's not already at the right place, move it
        if (currentIndex !== originalIndex && currentIndex !== -1) {
          // If there's an element at the original position, insert before it
          if (children[originalIndex]) {
            rootEl.insertBefore(dragEl, children[originalIndex]);
          } else {
            rootEl.appendChild(dragEl);
          }
        }
      }

      // Clean up the drag element
      if (dragEl) {
        dragEl.classList.remove(this.options.ghostClass || "");
        dragEl.classList.remove(this.options.chosenClass || "");
        dragEl.removeAttribute("draggable");
      }

      // Remove any clone created by SortableJS
      if (cloneEl) {
        cloneEl.remove();
      }

      // Emit a special event for true cloning with all necessary data
      if (this.options.onCancelClone && dragEl) {
        this.options.onCancelClone({
          sourceItem: dragEl ? dragEl.id || dragEl.dataset.id || null : null,
          newIndex: newIndex !== undefined ? newIndex : -1,
          sourceList: rootEl ? rootEl.id || rootEl.dataset.id || null : null,
          targetList: parentEl ? parentEl.id || parentEl.dataset.id || null : null,
        });
      }

      dispatchSortableEvent("end");

      return false; // Cancel the default drop
    },
  };

  return Object.assign(CancelClone, { pluginName: "cancelClone" });
}

Sortable.mount(CancelClonePlugin());

export default {
  template: `
    <div>
        <slot></slot>
    </div>`,
  props: {
    options: Object,
  },
  data() {
    return {
      sortableInstance: null,
    };
  },
  async mounted() {
    this.sortableInstance = Sortable.create(this.$el, {
      cancelClone: false,
      ...this.options,
      dataIdAttr: "id", // Explicitly tell SortableJS to use the HTML id attribute
      onChoose: (evt) => {
        this.$emit("sort_choose", {
          item: evt.item.id || evt.item.dataset.id || null,
          oldIndex: evt.oldIndex,
        });
      },
      onUnchoose: (evt) => {
        this.$emit("sort_unchoose", {
          item: evt.item.id || evt.item.dataset.id || null,
          oldIndex: evt.oldIndex,
        });
      },
      onStart: (evt) => {
        this.$emit("sort_start", {
          item: evt.item.id || evt.item.dataset.id || null,
          oldIndex: evt.oldIndex,
        });
      },
      onEnd: (evt) => {
        this.$emit("sort_end", {
          item: evt.item.id || evt.item.dataset.id || null,
          to: evt.to ? evt.to.id || null : null,
          from: evt.from ? evt.from.id || null : null,
          oldIndex: evt.oldIndex,
          newIndex: evt.newIndex,
          oldDraggableIndex: evt.oldDraggableIndex,
          newDraggableIndex: evt.newDraggableIndex,
          clone: evt.clone,
          pullMode: evt.pullMode,
          childrenData: [...this.sortableInstance.el.children].map((el, index) => ({
            id: el.id || el.dataset.id || null,
            index: index,
          })),
        });
      },
      onAdd: (evt) => {
        this.$emit("sort_add", {
          item: evt.item.id || evt.item.dataset.id || null,
          newIndex: evt.newIndex,
          from: evt.from ? evt.from.id || null : null,
          to: evt.to ? evt.to.id || null : null,
        });
      },
      onUpdate: (evt) => {
        this.$emit("sort_update", {
          item: evt.item.id || evt.item.dataset.id || null,
          newIndex: evt.newIndex,
          oldIndex: evt.oldIndex,
        });
      },
      onSort: (evt) => {
        this.$emit("sort_sort", {
          item: evt.item.id || evt.item.dataset.id || null,
          to: evt.to ? evt.to.id || null : null,
          from: evt.from ? evt.from.id || null : null,
          oldIndex: evt.oldIndex,
          newIndex: evt.newIndex,
          oldDraggableIndex: evt.oldDraggableIndex,
          newDraggableIndex: evt.newDraggableIndex,
          clone: evt.clone,
          pullMode: evt.pullMode,
          childrenData: [...this.sortableInstance.el.children].map((el, index) => ({
            id: el.id || el.dataset.id || null,
            index: index,
          })),
        });
      },
      onRemove: (evt) => {
        this.$emit("sort_remove", {
          item: evt.item.id || evt.item.dataset.id || null,
          oldIndex: evt.oldIndex,
          from: evt.from ? evt.from.id || null : null,
          to: evt.to ? evt.to.id || null : null,
        });
      },
      onFilter: (evt) => {
        this.$emit("sort_filter", {
          item: evt.item.id || evt.item.dataset.id || null,
        });
      },
      onMove: (evt, originalEvent) => {
        this.$emit("sort_move", {
          dragged: evt.dragged.id || evt.dragged.dataset.id || null,
          draggedRect: evt.draggedRect,
          related: evt.related.id || evt.related.dataset.id || null,
          relatedRect: evt.relatedRect,
          willInsertAfter: evt.willInsertAfter,
          clientY: originalEvent.clientY,
        });
      },
      onClone: (evt) => {
        if (evt.clone && !evt.clone.id) evt.clone.id = evt.item.id; // Assign new unique ID to the clone in source list
        this.$emit("sort_clone", {
          item: evt.item.id || evt.item.dataset.id || null,
          origEl: evt.item ? evt.item.id || evt.item.dataset.id || null : null,
          clone: evt.clone ? evt.clone.id || evt.clone.dataset.id || null : null,
        });
      },
      onCancelClone: (evt) => {
        this.$emit("sort_cancel_clone", {
          sourceItem: evt.sourceItem || null,
          newIndex: evt.newIndex,
          sourceList: evt.sourceList || null,
          targetList: evt.targetList || null,
        });
      },
      onChange: (evt) => {
        this.$emit("sort_change", {
          item: evt.item.id || evt.item.dataset.id || null,
          newIndex: evt.newIndex,
          oldIndex: evt.oldIndex,
        });
      },
      onSpill: (evt) => {
        this.$emit("sort_spill", {
          item: evt.item.id || evt.item.dataset.id || null,
          clone: evt.clone ? evt.clone.id || evt.clone.dataset.id || null : null,
        });
      },
      onSelect: (evt) => {
        this.$emit("sort_select", {
          item: evt.item.id || evt.item.dataset.id || null,
        });
      },
      onDeselect: (evt) => {
        this.$emit("sort_deselect", {
          item: evt.item.id || evt.item.dataset.id || null,
        });
      },
    });
  },
  methods: {
    sort(order, useAnimation) {
      this.sortableInstance?.sort(order, useAnimation);
    },
    enable() {
      this.sortableInstance?.option("disabled", false);
    },
    disable() {
      this.sortableInstance?.option("disabled", true);
    },
    getOption(optionName) {
      return this.sortableInstance?.option(optionName);
    },
    setOption(optionName, value) {
      if (!this.sortableInstance) return;
      this.sortableInstance.option(optionName, value); // Directly set the option on the SortableJS instance
      this.options[optionName] = value; // Also update our local options object to keep it in sync
      console.debug(`Set ${optionName} to:`, value);
    },
    remove(elementId) {
      this.sortableInstance.el.querySelector(`:scope > #${elementId}`)?.remove();
    },
    getChildrenOrder() {
      if (!this.sortableInstance) return [];
      const childElements = Array.from(this.sortableInstance.el.children);
      return childElements.map((el) => el.id || el.dataset.id || null).filter((id) => id !== null); // Filter out any null IDs
    },
  },
  beforeUnmount() {
    this.sortableInstance?.destroy();
  },
};
