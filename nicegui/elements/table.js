export default {
  template: "<div></div>",
  mounted() {
    this.gridOptions = {
      ...this.options,
      onGridReady: (params) => params.api.sizeColumnsToFit(),
    };
    this.grid = new agGrid.Grid(this.$el, this.gridOptions);
    this.gridOptions.api.addGlobalListener(this.handle_event);
  },
  methods: {
    update_grid() {
      replaceObject(this.options, this.gridOptions);
      this.gridOptions.api.refreshCells();
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
  },
};

function replaceArray(source, target) {
  for (let i = 0; i < source.length; i++) {
    if (typeof source[i] === "object") {
      replaceObject(source[i], target[i]);
    } else if (typeof source[i] === "array") {
      replaceArray(source[i], target[i]);
    } else {
      target[i] = source[i];
    }
  }
}

function replaceObject(source, target) {
  for (let key in source) {
    if (typeof source[key] === "object") {
      replaceObject(source[key], target[key]);
    } else if (typeof source[key] === "array") {
      replaceArray(source[key], target[key]);
    } else {
      target[key] = source[key];
    }
  }
}
