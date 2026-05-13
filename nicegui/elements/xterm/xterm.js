import { Terminal, FitAddon, WebLinksAddon } from "nicegui-xterm";
import { loadResource } from "../../static/utils/resources.js";

export default {
  template: "<div></div>",
  mounted() {
    // Create terminal with addons
    this.terminal = new Terminal(this.options);
    this.terminal.loadAddon((this.fit_addon = new FitAddon()));
    this.terminal.loadAddon(new WebLinksAddon());
    this.terminal.open(this.$el);

    // Register events that are re-emitted by the vue component
    Object.getOwnPropertyNames(Object.getPrototypeOf(this.terminal))
      .filter((key) => key.startsWith("on") && typeof this.terminal[key] === "function")
      .forEach((key) => {
        this.terminal[key]((e) => this.$emit(key.slice(2).toLowerCase(), e));
      });

    // NOTE: wait for window.path_prefix to be set
    this.$nextTick().then(() => loadResource(window.path_prefix + `${this.resourcePath}/xterm.css`));
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
    resourcePath: String,
  },
};
