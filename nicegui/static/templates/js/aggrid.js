// {* raw *}

var cached_grid_def = {};

Vue.component('grid', {
    template:
        `<div  v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style"  ></div>`,
    methods: {
        evaluate_formatters(def) {
            if (Array.isArray(def)) {
                for (const element of def) {
                    this.evaluate_formatters(element);
                }
            } else if (typeof def == "object" && def !== null) {
                for (const [key, value] of Object.entries(def)) {
                    if (key.toLowerCase().includes('formatter')) {
                        eval('def[key] = ' + def[key]);
                    }
                    this.evaluate_formatters(value);
                }
            }
        },
        grid_change() {
            var j = JSON.stringify(this.$props.jp_props.def);
            var grid_def = JSON.parse(j);  // Deep copy the grid definition
            for (let i = 0; i < this.$props.jp_props.html_columns.length; i++) {
                if (grid_def.columnDefs[this.$props.jp_props.html_columns[i]].cellRenderer === undefined)
                grid_def.columnDefs[this.$props.jp_props.html_columns[i]].cellRenderer = function (params) {
                    return params.value ? params.value : '';
                };
            }
            cached_grid_def[this.$props.jp_props.id] = j;
            grid_def.onGridReady = grid_ready;
            grid_def.popupParent = document.querySelector('body');
            this.evaluate_formatters(grid_def);
            for (const field of this.$props.jp_props.evaluate) {
                eval('grid_def[field] = ' + grid_def[field]);
            }
            // Code for CheckboxRenderer https://blog.ag-grid.com/binding-boolean-values-to-checkboxes-in-ag-grid/
            function CheckboxRenderer() {
            }

            CheckboxRenderer.prototype.init = function (params) {
                this.params = params;

                this.eGui = document.createElement('input');
                this.eGui.type = 'checkbox';
                this.eGui.checked = params.value;

                this.checkedHandler = this.checkedHandler.bind(this);
                this.eGui.addEventListener('click', this.checkedHandler);
            };

            CheckboxRenderer.prototype.checkedHandler = function (e) {
                let checked = e.target.checked;
                let colId = this.params.column.colId;
                this.params.node.setDataValue(colId, checked);
            };

            CheckboxRenderer.prototype.getGui = function (params) {
                return this.eGui;
            };

            CheckboxRenderer.prototype.destroy = function (params) {
                this.eGui.removeEventListener('click', this.checkedHandler);
            };

            grid_def.components = {
                checkboxRenderer: CheckboxRenderer
            };


            new agGrid.Grid(document.getElementById(this.$props.jp_props.id.toString()), grid_def);  // the api calls are added to grid_def
            cached_grid_def['g' + this.$props.jp_props.id] = grid_def;
            var auto_size = this.$props.jp_props.auto_size;


            function grid_ready(event) {
                if (auto_size) {
                    var allColumnIds = [];
                    grid_def.columnApi.getAllColumns().forEach(function (column) {
                        allColumnIds.push(column.colId);
                    });
                    grid_def.columnApi.autoSizeColumns(allColumnIds);
                }
            }

            grid_def.api.addGlobalListener(global_listener);
            var events = this.$props.jp_props.events;
            var props = this.$props;

            function global_listener(event_name, event_obj) {
                if (events.includes(event_name)) {
                    var event_fields = ['data', 'rowIndex', 'type', 'value']; // for cellClicked and rowClicked
                    var e = {
                        'event_type': event_name,
                        'grid': 'ag-grid',
                        'id': props.jp_props.id,
                        'class_name': props.jp_props.class_name,
                        'html_tag': props.jp_props.html_tag,
                        'vue_type': props.jp_props.vue_type,
                        'page_id': page_id,
                        'websocket_id': websocket_id
                    };
                    var more_properties = ['value', 'oldValue', 'newValue', 'context', 'rowIndex', 'data', 'toIndex',
                        'firstRow', 'lastRow', 'clientWidth', 'clientHeight', 'started', 'finished', 'direction', 'top',
                        'left', 'animate', 'keepRenderedRows', 'newData', 'newPage', 'source', 'visible', 'pinned',
                        'filterInstance', 'rowPinned', 'forceBrowserFocus'];
                    for (let i = 0; i < more_properties.length; i++) {
                        let property = more_properties[i];
                        if (!(typeof event_obj[property] === "undefined")) {
                            e[property] = event_obj[property];
                        }
                    }
                    if (!(typeof event_obj.column === "undefined")) {
                        e.colId = event_obj.column.colId;
                    }
                    if (!(typeof event_obj.node === "undefined")) {
                        let node_properties = ['selected', 'rowHeight'];
                        for (let i = 0; i < node_properties.length; i++) {
                            let property = node_properties[i];
                            if (!(typeof event_obj.node[property] === "undefined")) {
                                e[property] = event_obj.node[property];
                            }
                        }
                        e.selected = event_obj.node.selected;
                    }

                    if (['sortChanged', 'filterChanged', 'columnMoved', 'rowDragEnd'].includes(event_name)) {
                        e.data = grid_def.api.getDataAsCsv();
                    }
                    send_to_server(e, 'event');
                }
            }
        }
    },
    mounted() {
        this.grid_change();
    },
    updated() {
        if (JSON.stringify(this.$props.jp_props.def) != cached_grid_def[this.$props.jp_props.id]) {
            grid_to_destroy = cached_grid_def['g' + this.$props.jp_props.id];
            grid_to_destroy.api.destroy();
            this.grid_change(); // Explore option to check difference and update with api instead of destroying and creating new grid
        }
    },
    props: {
        jp_props: Object
    }
});

// {* endraw *}