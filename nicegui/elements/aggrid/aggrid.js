import * as AgGrid from "nicegui-aggrid";
import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";

export default {
  template: "<div></div>",
  mounted() {
    AgGrid.ModuleRegistry.registerModules(this.modules.map((moduleName) => AgGrid[moduleName]));
    this.update_grid();

    const updateTheme = () =>
      this.$el.setAttribute("data-ag-theme-mode", document.body.classList.contains("body--dark") ? "dark" : "light");
    this.themeObserver = new MutationObserver(updateTheme);
    this.themeObserver.observe(document.body, { attributes: true, attributeFilter: ["class"] });
    updateTheme();
  },
  unmounted() {
    this.api?.destroy();
    this.themeObserver.disconnect();
  },
  methods: {
    update_grid() {
      this.$el.textContent = "";
      this.gridOptions = {
        ...this.options,
        theme: {
          quartz: AgGrid.themeQuartz,
          balham: AgGrid.themeBalham,
          material: AgGrid.themeMaterial,
          alpine: AgGrid.themeAlpine,
        }[this.options.theme].withPart(AgGrid.colorSchemeVariable),
      };

      for (const column of this.htmlColumns) {
        if (this.gridOptions.columnDefs[column].cellRenderer === undefined) {
          this.gridOptions.columnDefs[column].cellRenderer = (params) => (params.value ? params.value : "");
        }
      }
      convertDynamicProperties(this.gridOptions, true);

      const originalOnGridReady = this.gridOptions.onGridReady;
      this.gridOptions.onGridReady = (params) => {
        try {
          originalOnGridReady?.(params);
        } finally {
          this.handle_event("gridReady", params);
        }
      };
      this.api?.destroy();
      this.api = AgGrid.createGrid(this.$el, this.gridOptions);
      this.api.addGlobalListener(this.handle_event);
    },
    run_grid_method(name, ...args) {
      convertDynamicProperties(args, true);
      return runMethod(this.api, name, args);
    },
    run_row_method(row_id, name, ...args) {
      convertDynamicProperties(args, true);
      return runMethod(this.api.getRowNode(row_id), name, args);
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
    htmlColumns: Array,
    modules: Array,
  },
};
