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
        onGridReady: (params) => params.api.sizeColumnsToFit(),
      };
      for (const column of this.html_columns) {
        if (this.gridOptions.columnDefs[column].cellRenderer === undefined) {
          this.gridOptions.columnDefs[column].cellRenderer = (params) => (params.value ? params.value : "");
        }
      }
      this.grid = new agGrid.Grid(this.$el, this.gridOptions);
      this.gridOptions.api.addGlobalListener(this.handle_event);
    },
    call_api_method(name, ...args) {
      this.gridOptions.api[name](...args);
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
  },
};
