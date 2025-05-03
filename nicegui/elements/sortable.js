export default {
    template: `
    <div>
        <slot></slot>
    </div>`,
    props: {
        options: Object,
        resource_path: String
    },
    data() {
        return {
            sortableInstance: null,
            Sortable: null
        };
    },
    async mounted() {
        await this.$nextTick(); // Wait for window.path_prefix to be set

        // Dynamically import Sortable
        try {
            // Import the module
            const SortableModule = await import(window.path_prefix + `${this.resource_path}/sortable.complete.esm.js`);

            // Get the Sortable constructor (could be exported in different ways)
            this.Sortable = SortableModule.default || SortableModule.Sortable || window.Sortable;

            if (!this.Sortable) {
                console.error("Failed to load Sortable library. Not found in module exports or global scope.");
                return;
            }

            const el = this.$el;
            const options = { ...this.options };

            this.sortableInstance = this.Sortable.create(el, {
                ...options,
                onClone: (evt) => {
                    // Assign a new unique id to the clone in the source list
                    if (this.options["removeOnAdd"] == true) {
                        if (evt.clone && !evt.clone.id) {
                            evt.clone.id = evt.item.id;
                        }
                    }
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
                        oldIndex: evt.oldIndex,
                        newIndex: evt.newIndex,
                        item: evt.item.id || evt.item.dataset.id || null,
                        childrenData: childrenData
                    });

                    // Emit a separate event for synchronizing order
                    this.$emit('order_updated', {
                        childrenData: childrenData
                    });
                },
                onAdd: (evt) => {
                    this.$emit('sort_add', {
                        item: evt.item.id || evt.item.dataset.id || null,
                        newIndex: evt.newIndex
                    });
                },
                onSort: (evt) => {
                    this.$emit('sort_change', {
                        item: evt.item.id || evt.item.dataset.id || null
                    });
                },
                onMove: (evt, originalEvent) => {
                    const result = this.$emit('sort_move', {
                        related: evt.related.id || evt.related.dataset.id || null,
                        dragged: evt.dragged.id || evt.dragged.dataset.id || null
                    });
                    return result !== false;
                },
                onFilter: (evt) => {
                    this.$emit('sort_filter', {
                        item: evt.item.id || evt.item.dataset.id || null
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
        getSelected() {
            if (this.sortableInstance) {
                // Try to get selected items from the MultiDrag plugin
                const sortable = this.sortableInstance;
                if (sortable.multiDrag && sortable.multiDrag.selectedItems) {
                    return sortable.multiDrag.selectedItems.map(item =>
                        item.id || item.dataset.id || null
                    );
                }
            }
            return [];
        },
        select(elementId) {
            try {
                const element = document.getElementById(elementId);
                if (element && this.sortableInstance) {
                    const parent = element.parentNode;
                    if (parent && parent[this.Sortable.expando]) {
                        // Get the Sortable instance that manages this element
                        const sortableInstance = parent[this.Sortable.expando];

                        // Use the MultiDrag plugin's select utility if available
                        if (this.Sortable.utils && this.Sortable.utils.select) {
                            this.Sortable.utils.select(element);
                        } else if (sortableInstance.multiDrag) {
                            // Attempt to access the select method via plugin
                            this.Sortable.plugins.find(p => p.pluginName === 'multiDrag')?.utils?.select(element);
                        }
                    }
                }
            } catch (error) {
                console.error("Error in select method:", error);
            }
        },
        deselect(elementId) {
            try {
                const element = document.getElementById(elementId);
                if (element && this.sortableInstance) {
                    const parent = element.parentNode;
                    if (parent && parent[this.Sortable.expando]) {
                        // Get the Sortable instance that manages this element
                        const sortableInstance = parent[this.Sortable.expando];

                        // Use the MultiDrag plugin's deselect utility if available
                        if (this.Sortable.utils && this.Sortable.utils.deselect) {
                            this.Sortable.utils.deselect(element);
                        } else if (sortableInstance.multiDrag) {
                            // Attempt to access the deselect method via plugin
                            this.Sortable.plugins.find(p => p.pluginName === 'multiDrag')?.utils?.deselect(element);
                        }
                    }
                }
            } catch (error) {
                console.error("Error in deselect method:", error);
            }
        },
        removeItemById(elementId) {
            try {
                const el = document.getElementById(elementId);
                if (el && el.parentNode) {
                    el.parentNode.removeChild(el);
                    return true;
                }
                return false;
            } catch (error) {
                console.error("Error removing element:", elementId, error);
                return false;
            }
        }
    },
    beforeDestroy() {
        if (this.sortableInstance) {
            this.sortableInstance.destroy();
        }
    }
}