import { load_widget, load_css } from "widget";
import { cleanObject } from "../../static/utils/json.js";

export default {
  template: "<div></div>",
  async mounted() {
    const emit_to_py = this.$emit;

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
        else this.callbacks[event]?.delete(callback);
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
    // TODO: cleanup_widget and cleanup_view should be called when the widget is destroyed
    this.cleanup_widget = await mod.initialize?.({ model: this.model });
    this.cleanup_view = await mod.render?.({ model: this.model, el: this.$el });

    load_css(this.css_content, this.traits._anywidget_id);
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
