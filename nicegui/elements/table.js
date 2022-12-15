export default {
  template: "<div></div>",
  mounted() {
    this.gridOptions = {
      ...this.options,
      onGridReady: (params) => params.api.sizeColumnsToFit(),
    };
    this.grid = new agGrid.Grid(this.$el, this.gridOptions);
  },
  methods: {
    update_grid() {
      replaceObject(this.options, this.gridOptions);
      this.gridOptions.api.refreshCells();
    },
    call_api_method(name, ...args) {
      this.gridOptions.api[name](...args);
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
