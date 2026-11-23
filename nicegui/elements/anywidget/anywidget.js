import { load_widget, load_css } from "widget";
import { cleanObject } from "../../static/utils/json.js";

// AFM: a lifecycle hook may return a cleanup function, which has to run when its signal aborts
async function run_hook(hook, props) {
  const cleanup = await hook?.(props);
  if (typeof cleanup !== "function") return; // initialize may also return an object of exports
  if (props.signal.aborted) cleanup(); // the element was deleted while the hook was running
  else props.signal.addEventListener("abort", () => cleanup());
}

export default {
  template: "<div></div>",
  async mounted() {
    const emit_to_py = this.$emit;
    this.controller = new AbortController();
    const { signal } = this.controller;

    // Implement AFM: https://anywidget.dev/en/afm/
    // References:
    // * Marimo AFM impl:
    // https://github.com/marimo-team/marimo/blob/7f3023ff0caef22b2bf4c1b5a18ad1899bd40fa3/frontend/src/plugins/impl/anywidget/AnyWidgetPlugin.tsx#L161-L267
    this.model = {
      attributes: { ...this.traits },
      callbacks: {},
      get: function (key) {
        return cleanObject(this.attributes[key]);
      },
      set: function (key, value) {
        this.attributes[key] = value;
        this.emit("change:" + key, value);
      },
      save_changes: function () {
        if (this.callbacks.change && Array.isArray(this.callbacks.change)) {
          this.callbacks.change.forEach((cb) => cb());
        }
        emit_to_py("update:traits", { ...this.attributes });
      },
      on: function (event, callback) {
        if (!this.callbacks[event]) this.callbacks[event] = [];
        this.callbacks[event].push(callback);
      },
      off: function (event, callback) {
        if (!event) this.callbacks = {};
        else if (!callback) this.callbacks[event] = [];
        else if (this.callbacks[event]) this.callbacks[event] = this.callbacks[event].filter((cb) => cb !== callback);
      },
      emit: function (event, value) {
        this.callbacks[event]?.forEach((cb) => cb(value));
      },
      send: function (content, callbacks, buffers) {
        console.warn("anywidget.send() is not yet implemented in NiceGUI", content);
      },
    };

    // Dynamically load esm_content as an ECMAScript module
    const mod = await load_widget(this.esm_content, this.traits._anywidget_id);
    if (signal.aborted) return; // the element was deleted while the module was loading
    try {
      await run_hook(mod.initialize, { model: this.model, signal });
      if (signal.aborted) return; // the element was deleted while initialize was running
      await run_hook(mod.render, { model: this.model, el: this.$el, signal });
      if (signal.aborted) return; // the element was deleted while render was running
    } catch (error) {
      if (signal.aborted) return; // the element was deleted while the hook was awaiting the signal, e.g. in a fetch
      this.controller.abort(); // AFM: a failing hook aborts its signal, which runs the cleanups wired to it
      throw error;
    }

    load_css(this.css_content, this.traits._anywidget_id);
  },
  unmounted() {
    this.controller.abort(); // runs the cleanups of the widget and the view
  },
  methods: {
    update_trait(trait, value) {
      this.model.set(trait, value);
    },
  },
  props: {
    traits: Object,
    esm_content: String,
    css_content: String,
  },
};
