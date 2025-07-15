import "xterm";
import "addon-fit";
import "addon-web-links";
import { loadResource } from "../../static/utils/resources.js";

export default {
  template: "<div></div>",
  async mounted() {
    await this.$nextTick(); // NOTE: wait for window.path_prefix to be set
    await loadResource(window.path_prefix + `${this.resource_path}/xterm/css/xterm.css`);

    // Create terminal with addons
    this.terminal = new Terminal(this.options);
    this.fit_addon = new FitAddon.FitAddon();
    this.terminal.loadAddon(this.fit_addon);
    this.terminal.loadAddon(new WebLinksAddon.WebLinksAddon());
    this.terminal.open(this.$el);

    // Register events that are re-emitted by the vue component
    for (const event of [
      "Bell",
      "Binary",
      "CursorMove",
      "Data",
      "Key",
      "LineFeed",
      "Render",
      "WriteParsed",
      "Resize",
      "Scroll",
      "SelectionChange",
      "TitleChange",
    ]) {
      this.terminal[`on${event}`]((e) => this.$emit(event.toLowerCase(), e));
    }
  },
  methods: {
    getRows() {
      return this.terminal.rows;
    },
    getColumns() {
      return this.terminal.cols;
    },
    fit() {
      this.fit_addon.fit();
    },
    input(data, wasUserInput = true) {
      return this.terminal.input(data, wasUserInput);
    },
    write(data) {
      return this.terminal.write(data);
    },
    writeln(data) {
      return this.terminal.writeln(data);
    },
    run_terminal_method(name, ...args) {
      if (name.startsWith(":")) {
        name = name.slice(1);
        args = args.map((arg) => new Function(`return (${arg});`).call(this.terminal));
      }
      return runMethod(this.terminal, name, args);
    },
  },
  props: {
    options: Object,
    resource_path: String,
  },
};
