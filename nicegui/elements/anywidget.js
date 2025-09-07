import { load_widget, load_css } from "widget";  // lib/anywidget/widget.js
import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";

export default {
  template: "<div></div>",
  mounted() {
    this.init_widget();
  },
  methods: {
    init_widget() {
      (async () => {
        const this_ = this;

        // Implement AFM: https://anywidget.dev/en/afm/
        // References:
        // * Marimo AFM impl:
        // https://github.com/marimo-team/marimo/blob/7f3023ff0caef22b2bf4c1b5a18ad1899bd40fa3/frontend/src/plugins/impl/anywidget/AnyWidgetPlugin.tsx#L161-L267
        const model = {
          attributes: { ...this.traits },
          callbacks: {},
          get: function (key) {
            console.log('Getting value for', key, ':', this.attributes[key]);
            const value = this.attributes[key];
            try {
              // TODO: this should not be necessary but was running into some
              // JavaScript issues that haven't tried to figure out
              return JSON.parse(JSON.stringify(value));
            } catch (e) {
              // If value is not serializable, return null or a fallback
              console.warn('Value for key', key, 'is not JSON-serializable:', value);
              return null;
            }
          },
          set: function (key, value) {
            console.log('Setting value for', key, ':', value);
            this.attributes[key] = value;
            this.emit('change:' + key, value);
          },
          save_changes: function () {
            console.log('Saving changes:', this.attributes);

            // Trigger any change callbacks
            if (this.callbacks['change'] && Array.isArray(this.callbacks['change'])) {
              this.callbacks['change'].forEach((cb) => cb());
            }

            // Propagate the change back to python backend
            this_.$emit('update:traits', { ...this.attributes });
          },
          on: function (event, callback) {
            console.log('Registering callback for event:', event);
            if (!this.callbacks[event]) {
              this.callbacks[event] = [];
            }
            this.callbacks[event].push(callback);

            // For property-specific change events
            if (event.startsWith('change:') && callback) {
              const propName = event.split(':')[1];
              console.log('Registered property change callback for', propName);
            }
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
              this.callbacks[event].forEach(cb => cb(value));
            }
          },
          send: function (content, callbacks, buffers) {
            if (buffers) {
              console.warn('anywidget.send() buffers are not supported in NiceGUI currently');
            }
            console.warn('anywidget.send() is not yet implemented in NiceGUI;', content);
            // this_.$emit('custom', content);
          }
        };

        // Dynamically load esm_content as an ECMAScript module
        const mod = await load_widget(this.esm_content, this.traits["_anywidget_id"]);
        // TODO: cleanup_widget and cleanup_view should be called when the widget is destroyed
        this.cleanup_widget = await mod.initialize?.({ model: model });
        this.cleanup_view = await mod.render?.({ model: model, el: this.$el });
        this.model = model;

        // // Create a Blob from the ESM content
        // const blob = new Blob([this.esm_content], { type: 'text/javascript' });
        // const url = URL.createObjectURL(blob);
        // // TODO: initialize()
        // try {
        //   // Dynamically import the module
        //   const mod = await import(/* @vite-ignore */ url);
        //   if (mod && typeof mod.render === 'function') {
        //     // Call the render function with the model and element
        //     mod.render({ model: model, el: this.$el });
        //   } else if (mod && mod.default && typeof mod.default.render === 'function') {
        //     mod.default.render({ model: model, el: this.$el });
        //   }
        //   this.model = model;
        // } finally {
        //   // Clean up the object URL
        //   URL.revokeObjectURL(url);
        // }
      })();

      load_css(this.css_content, this.traits["_anywidget_id"]);
      // // Optionally inject CSS if provided
      // if (this.css_content) {
      //   const style = document.createElement('style');
      //   style.textContent = this.css_content;
      //   document.head.appendChild(style);
      // }

      // If you have an API to add listeners, do so here (placeholder)
      // this.api.addGlobalListener(this.handle_event);
    },
    update_trait(change) {
      // Callback from Python traitlet backend change event
      // change is a dictionary with 'trait', 'new', and 'old' keys
      convertDynamicProperties(change, true);
      console.log('Updating trait:', change);
      if (change) {
        this.model.attributes[change['trait']] = change['new'];
        this.model.emit("change:" + change['trait'], change['new']);
      }
    },
    update_traits() {
      // Currently no-op
      console.log('Updating traits:', this.traits, this.model.attributes);
    },
    handle_event(type, args) {
      console.log('handle_event', type, args);
    },
  },
  props: {
    traits: Object,
    esm_content: String,
    css_content: String,
  },
};
