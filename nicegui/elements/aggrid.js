function recursive_has_dynamic(obj) {
  if (typeof obj !== "object" || obj === null) return false;
  if (Array.isArray(obj)) {
    return obj.some((v) => recursive_has_dynamic(v));
  }
  for (const [key, value] of Object.entries(obj)) {
    if (key.startsWith(":")) return true;
    if (recursive_has_dynamic(value)) {
      return true;
    }
  }
  return false;
}

function recursive_convert_dynamic(obj) {
  if (!recursive_has_dynamic(obj)) return obj; // double-loop hierarchy is probably safer and uses less RAM if dynamic not used
  if (typeof obj !== "object" || obj === null) return obj;
  if (Array.isArray(obj)) {
    return obj.map((v) => recursive_convert_dynamic(v));
  }
  const targetObj = {};
  for (const [attr, value] of Object.entries(obj)) {
    if (attr.startsWith(":")) {
      try {
        targetObj[attr.slice(1)] = new Function("return " + value)();
      } catch (e) {
        console.error(`Error while converting ${attr} attribute to function:`, e);
      }
    } else {
      targetObj[attr] = recursive_convert_dynamic(value);
    }
  }
  return targetObj;
}

export default {
  template: "<div></div>",
  mounted() {
    this.update_grid();
  },
  methods: {
    update_grid() {
      this.$el.textContent = "";
      this.gridOptions = {
        ...this.options,
        onGridReady: this.auto_size_columns ? (params) => params.api.sizeColumnsToFit() : undefined,
      };
      for (const column of this.html_columns) {
        if (this.gridOptions.columnDefs[column].cellRenderer === undefined) {
          this.gridOptions.columnDefs[column].cellRenderer = (params) => (params.value ? params.value : "");
        }
      }
      this.gridOptions = recursive_convert_dynamic(this.gridOptions);

      // Code for CheckboxRenderer https://blog.ag-grid.com/binding-boolean-values-to-checkboxes-in-ag-grid/
      function CheckboxRenderer() {}
      CheckboxRenderer.prototype.init = function (params) {
        this.params = params;
        this.eGui = document.createElement("input");
        this.eGui.type = "checkbox";
        this.eGui.checked = params.value;
        this.checkedHandler = this.checkedHandler.bind(this);
        this.eGui.addEventListener("click", this.checkedHandler);
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
        this.eGui.removeEventListener("click", this.checkedHandler);
      };
      this.gridOptions.components = {
        checkboxRenderer: CheckboxRenderer,
      };

      this.grid = new agGrid.Grid(this.$el, this.gridOptions);
      this.gridOptions.api.addGlobalListener(this.handle_event);
    },
    call_api_method(name, ...args) {
      this.gridOptions.api[name](...args);
    },
    call_column_api_method(name, ...args) {
      this.gridOptions.columnApi[name](...args);
    },
    handle_event(type, args) {
      this.$emit(type, {
        value: args.value,
        oldValue: args.oldValue,
        newValue: args.newValue,
        context: args.context,
        rowIndex: args.rowIndex,
        data: args.data,
        toIndex: args.toIndex,
        firstRow: args.firstRow,
        lastRow: args.lastRow,
        clientWidth: args.clientWidth,
        clientHeight: args.clientHeight,
        started: args.started,
        finished: args.finished,
        direction: args.direction,
        top: args.top,
        left: args.left,
        animate: args.animate,
        keepRenderedRows: args.keepRenderedRows,
        newData: args.newData,
        newPage: args.newPage,
        source: args.source,
        visible: args.visible,
        pinned: args.pinned,
        filterInstance: args.filterInstance,
        rowPinned: args.rowPinned,
        forceBrowserFocus: args.forceBrowserFocus,
        colId: args.column?.colId,
        selected: args.node?.selected,
        rowHeight: args.node?.rowHeight,
        rowId: args.node?.id,
      });
    },
  },
  props: {
    options: Object,
    html_columns: Array,
    auto_size_columns: Boolean,
  },
};
