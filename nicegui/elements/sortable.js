import { default as Sortable } from 'sortable';

// Add CancelClonePlugin
function CancelClonePlugin() {
  function CancelClone() {
    this.defaults = {
      cancelClone: false  // Disabled by default
    };
  }

  CancelClone.prototype = {
    drop({ rootEl, parentEl, dispatchSortableEvent, dragEl, cloneEl, newIndex, oldIndex }) {
      // Only act if cancelClone is enabled
      if (!this.options.cancelClone) return;

      try {
        // Only call revertOnSpill if an actual drag operation occurred
        if (this.sortable.revertOnSpill && this.sortable.revertOnSpill.onSpill && rootEl != parentEl) {
          // Store original index before reverting
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
                // Otherwise append to the end
                rootEl.appendChild(dragEl);
              }
            }
          }
        } else {
          return;
        }

        // Clean up the drag element
        if (dragEl) {
          dragEl.classList.remove(this.options.ghostClass || '');
          dragEl.classList.remove(this.options.chosenClass || '');
          dragEl.removeAttribute('draggable');
        }

        // Remove any clone created by SortableJS
        if (cloneEl) {
          cloneEl.remove();
        }

        // Emit a special event for true cloning with all necessary data
        if (this.options.onCancelClone && dragEl) {
          this.options.onCancelClone({
            sourceItem: dragEl ? (dragEl.id || dragEl.dataset.id || null) : null,
            newIndex: newIndex !== undefined ? newIndex : -1,
            sourceList: rootEl ? (rootEl.id || rootEl.dataset.id || null) : null,
            targetList: parentEl ? (parentEl.id || parentEl.dataset.id || null) : null,
          });
        }

        // Dispatch 'end' event
        dispatchSortableEvent('end');
      } catch (error) {
        console.error("Error in CancelClone plugin:", error);
      }

      return false; // Cancel the default drop
    }
  };

  return Object.assign(CancelClone, {
    pluginName: 'cancelClone'
  });
}

// Mount the CancelClonePlugin
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
    try {
      const el = this.$el;
      const options = {
        ...this.options,
        // Add plugin defaults if not explicitly overridden
        cancelClone: this.options.cancelClone !== undefined ? this.options.cancelClone : false,
      };

      this.sortableInstance = Sortable.create(el, {
        ...options,
        dataIdAttr: 'id', // Explicitly tell SortableJS to use the HTML id attribute
        onChoose: (evt) => {
          this.$emit('sort_choose', {
            item: evt.item.id || evt.item.dataset.id || null,
            oldIndex: evt.oldIndex
          });
        },
        onUnchoose: (evt) => {
          this.$emit('sort_unchoose', {
            item: evt.item.id || evt.item.dataset.id || null,
            oldIndex: evt.oldIndex
          });
        },
        onStart: (evt) => {
          this.$emit('sort_start', {
            item: evt.item.id || evt.item.dataset.id || null,
            oldIndex: evt.oldIndex
          });
        },
        onEnd: (evt) => {
          // Get the complete current order of all elements to synchronize with Python
          const currentOrder = this.sortableInstance.toArray();
          const childElements = Array.from(this.sortableInstance.el.children);
          const childrenData = childElements.map(el => ({
            id: el.id || el.dataset.id || null,
            index: currentOrder.indexOf(el.id || el.dataset.id || "")
          }));

          this.$emit('sort_end', {
            item: evt.item.id || evt.item.dataset.id || null,
            to: evt.to ? (evt.to.id || null) : null,
            from: evt.from ? (evt.from.id || null) : null,
            oldIndex: evt.oldIndex,
            newIndex: evt.newIndex,
            oldDraggableIndex: evt.oldDraggableIndex,
            newDraggableIndex: evt.newDraggableIndex,
            clone: evt.clone,
            pullMode: evt.pullMode,
            childrenData: childrenData
          });
        },
        onAdd: (evt) => {
          this.$emit('sort_add', {
            item: evt.item.id || evt.item.dataset.id || null,
            newIndex: evt.newIndex,
            from: evt.from ? (evt.from.id || null) : null,
            to: evt.to ? (evt.to.id || null) : null,
          });
        },
        onUpdate: (evt) => {
          this.$emit('sort_update', {
            item: evt.item.id || evt.item.dataset.id || null,
            newIndex: evt.newIndex,
            oldIndex: evt.oldIndex
          });
        },
        onSort: (evt) => {
          // Get the complete current order of all elements to synchronize with Python
          const currentOrder = this.sortableInstance.toArray();
          const childElements = Array.from(this.sortableInstance.el.children);
          const childrenData = childElements.map(el => ({
            id: el.id || el.dataset.id || null,
            index: currentOrder.indexOf(el.id || el.dataset.id || "")
          }));

          this.$emit('sort_sort', {
            item: evt.item.id || evt.item.dataset.id || null,
            to: evt.to ? (evt.to.id || null) : null,
            from: evt.from ? (evt.from.id || null) : null,
            oldIndex: evt.oldIndex,
            newIndex: evt.newIndex,
            oldDraggableIndex: evt.oldDraggableIndex,
            newDraggableIndex: evt.newDraggableIndex,
            clone: evt.clone,
            pullMode: evt.pullMode,
            childrenData: childrenData
          });
        },
        onRemove: (evt) => {
          this.$emit('sort_remove', {
            item: evt.item.id || evt.item.dataset.id || null,
            oldIndex: evt.oldIndex,
            from: evt.from ? (evt.from.id || null) : null,
            to: evt.to ? (evt.to.id || null) : null
          });
        },
        onFilter: (evt) => {
          this.$emit('sort_filter', {
            item: evt.item.id || evt.item.dataset.id || null
          });
        },
        onMove: (evt, originalEvent) => {
          const result = this.$emit('sort_move', {
            dragged: evt.dragged.id || evt.dragged.dataset.id || null,
            draggedRect: evt.draggedRect,
            related: evt.related.id || evt.related.dataset.id || null,
            relatedRect: evt.relatedRect,
            willInsertAfter: evt.willInsertAfter,

          });
          return result !== false;
        },
        onClone: (evt) => {
          // Assign a new unique id to the clone in the source list
          if (evt.clone && !evt.clone.id) {
            evt.clone.id = evt.item.id;
          }
          this.$emit('sort_clone', {
            item: evt.item.id || evt.item.dataset.id || null,
            origEl: evt.item ? (evt.item.id || evt.item.dataset.id || null) : null,
            clone: evt.clone ? (evt.clone.id || evt.clone.dataset.id || null) : null,
          });
        },
        onCancelClone: (evt) => {
          this.$emit('sort_cancel_clone', {
            sourceItem: evt.sourceItem || null,
            newIndex: evt.newIndex,
            sourceList: evt.sourceList || null,
            targetList: evt.targetList || null
          });
        },
        onChange: (evt) => {
          this.$emit('sort_change', {
            item: evt.item.id || evt.item.dataset.id || null,
            newIndex: evt.newIndex,
            oldIndex: evt.oldIndex
          });
        },
        // Plugin event handlers
        onSpill: (evt) => {
          this.$emit('sort_spill', {
            item: evt.item.id || evt.item.dataset.id || null,
            clone: evt.clone ? (evt.clone.id || evt.clone.dataset.id || null) : null
          });
        },
        onSelect: (evt) => {
          this.$emit('sort_select', {
            item: evt.item.id || evt.item.dataset.id || null
          });
        },
        onDeselect: (evt) => {
          this.$emit('sort_deselect', {
            item: evt.item.id || evt.item.dataset.id || null
          });
        }
      });
    } catch (error) {
      console.error("Error initializing Sortable:", error);
    }
  },
  methods: {
    sort(order, useAnimation) {
      if (this.sortableInstance) {
        this.sortableInstance.sort(order, useAnimation);
      }
    },

    enable() {
      if (this.sortableInstance) {
        this.sortableInstance.option('disabled', false);
      }
    },
    disable() {
      if (this.sortableInstance) {
        this.sortableInstance.option('disabled', true);
      }
    },
    // Add a method to get a specific option value
    getOption(optionName) {
      if (this.sortableInstance) {
        return this.sortableInstance.option(optionName);
      }
      return null;
    },
    // Add a method to set a specific option
    setOption(optionName, value) {
      if (this.sortableInstance) {
        // Directly set the option on the SortableJS instance
        this.sortableInstance.option(optionName, value);
        // Also update our local options object to keep it in sync
        this.options[optionName] = value;
        console.debug(`Set ${optionName} to:`, value);
        return true;
      }
      return false;
    },
    // MultiDrag plugin methods
    select(elementId) {
      try {
        const element = document.getElementById(elementId);
        if (element) {
          Sortable.utils.select(element);
        }
      } catch (error) {
        console.error("Error in select method:", error);
      }
    },
    deselect(elementId) {
      try {
        const element = document.getElementById(elementId);
        if (element) {
          Sortable.utils.deselect(element);
        }
      } catch (error) {
        console.error("Error in deselect method:", error);
      }
    },
    remove(elementId) {
      const element = this.sortableInstance.el.querySelector(`#${elementId}`);
      if (element) {
        if (element.parentNode === this.sortableInstance.el) {
          element.parentNode.removeChild(element);
          return true;
        }
      }
      return false;
    },
    getChildrenOrder() {
      if (this.sortableInstance) {
        // Get all children DOM elements
        const childElements = Array.from(this.sortableInstance.el.children);

        // Return array of element IDs in their current DOM order
        return childElements.map(el => el.id || el.dataset.id || null)
          .filter(id => id !== null); // Filter out any null IDs
      }
      return [];
    }
  },
  beforeDestroy() {
    if (this.sortableInstance) {
      this.sortableInstance.destroy();
    }
  }
}
