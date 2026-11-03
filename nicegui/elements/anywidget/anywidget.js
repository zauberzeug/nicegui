import { load_widget, load_css } from "widget";
import { cleanObject } from "../../static/utils/json.js";

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
    // AFM: initialize and render may return a cleanup function, which has to run when the element goes away
    const cleanup_widget = await mod.initialize?.({ model: this.model, signal });
    this.cleanup_widget = typeof cleanup_widget === 'function' ? cleanup_widget : null;
    if (signal.aborted) return this._run_cleanups();  // the element was deleted while initialize was running
    const cleanup_view = await mod.render?.({ model: this.model, el: this.$el, signal });
    this.cleanup_view = typeof cleanup_view === 'function' ? cleanup_view : null;
    if (signal.aborted) return this._run_cleanups();  // the element was deleted while render was running

    load_css(this.css_content, this.traits._anywidget_id);
  },
  unmounted() {
    this.controller.abort();
    this._run_cleanups();
  },
  methods: {
    update_trait(trait, value) {
      this.model.set(trait, value);
    },
    _run_cleanups() {
      // the view's cleanup runs before the widget's, the reverse of the order in which they were created
      this.cleanup_view?.();
      this.cleanup_widget?.();
      this.cleanup_view = this.cleanup_widget = null;
    },
  },
  props: {
    traits: Object,
    esm_content: String,
    css_content: String,
  },
};
