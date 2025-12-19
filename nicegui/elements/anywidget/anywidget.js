import { load_widget, load_css } from "widget"; // lib/anywidget/widget.js

export default {
  template: "<div></div>",
  mounted() {
    this.init_widget();
  },
  methods: {
    _log(...args) {
      if (this._debug) {
        console.log("NiceGUI-Anywidget", ...args);
      }
    },
    init_widget() {
      (async () => {
        const emit_to_py = this.$emit;
        const log = this._log;

        // Implement AFM: https://anywidget.dev/en/afm/
        // References:
        // * Marimo AFM impl:
        // https://github.com/marimo-team/marimo/blob/7f3023ff0caef22b2bf4c1b5a18ad1899bd40fa3/frontend/src/plugins/impl/anywidget/AnyWidgetPlugin.tsx#L161-L267
        const model = {
          attributes: { ...this.traits },
          callbacks: {},
          get: function (key) {
            log("Getting value for", key, ":", this.attributes[key]);
            const value = this.attributes[key];
            try {
              // TODO: this should not be necessary but was running into some
              // JavaScript issues that haven't tried to figure out
              return JSON.parse(JSON.stringify(value));
            } catch (e) {
              // If value is not serializable, return null or a fallback
              console.warn("NiceGUI-Anywidget: Value for key", key, "is not JSON-serializable:", value);
              return null;
            }
          },
          set: function (key, value) {
            log("Setting value for", key, ":", value);
            this.attributes[key] = value;
            this.emit("change:" + key, value);
          },
          save_changes: function () {
            log("Saving changes:", this.attributes);

            // Trigger any change callbacks
            if (this.callbacks["change"] && Array.isArray(this.callbacks["change"])) {
              this.callbacks["change"].forEach((cb) => cb());
            }

            // Propagate the change back to python backend;
            // currently serializing all traits instead of just the changed ones
            // (ideally would do this to reduce communication overhead)
            emit_to_py("update:traits", { ...this.attributes });
          },
          on: function (event, callback) {
            log("Registering callback for event:", event);
            if (!this.callbacks[event]) {
              this.callbacks[event] = [];
            }
            this.callbacks[event].push(callback);
          },
          off: function (event, callback) {
            if (!event) {
              this.callbacks = {};
              return;
            }
            if (!callback) {
              this.callbacks[event] = [];
              return;
            }
            this.callbacks[event]?.delete(callback);
          },
          emit: function (event, value) {
            if (this.callbacks[event]) {
              this.callbacks[event].forEach((cb) => cb(value));
            }
          },
          send: function (content, callbacks, buffers) {
            if (buffers) {
              console.warn("anywidget.send() buffers are not supported in NiceGUI currently");
            } else {
              console.warn("anywidget.send() is not yet implemented in NiceGUI;", content);
            }
            // emit_to_py('custom', content);
          },
        };

        // Dynamically load esm_content as an ECMAScript module
        const mod = await load_widget(this.esm_content, this.traits["_anywidget_id"]);
        // TODO: cleanup_widget and cleanup_view should be called when the widget is destroyed
        this.cleanup_widget = await mod.initialize?.({ model: model });
        this.cleanup_view = await mod.render?.({ model: model, el: this.$el });
        this.model = model;
      })();

      load_css(this.css_content, this.traits["_anywidget_id"]);

      // If you have an API to add listeners, do so here (placeholder)
      // this.api.addGlobalListener(this.handle_event);
    },
    update_trait(trait, value) {
      this._log("Updating trait:", trait, value);
      this.model.attributes[trait] = value;
      this.model.emit("change:" + trait, value);
    },
    update_traits() {
      // Currently no-op
      this._log("Updating traits:", this.traits, this.model.attributes);
    },
    handle_event(type, args) {
      // Currently unused
      this._log("handle_event", type, args);
    },
  },
  props: {
    traits: Object,
    esm_content: String,
    css_content: String,
    _debug: Boolean,
  },
};
