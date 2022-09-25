Vue.component("keyboard", {
  template: `<span data-nicegui='keyboard' v-bind:id="jp_props.id" :class="jp_props.classes" :style="jp_props.style"></span>`,
  mounted() {
    for (const event of this.$props.jp_props.options.active_js_events) {
      document.addEventListener(event, (evt) => {
        // https://stackoverflow.com/a/36469636/3419103
        const ignored = ["input", "select", "button", "textarea"];
        const focus = document.activeElement;
        if (focus && ignored.includes(focus.tagName.toLowerCase())) return;

        const e = {
          event_type: "keyboardEvent",
          id: this.$props.jp_props.id,
          page_id: page_id,
          websocket_id: websocket_id,
        };
        if (evt instanceof KeyboardEvent) {
          if (evt.repeat && !this.$props.jp_props.options.repeating) return;
          e["key_data"] = {
            action: event,
            altKey: evt.altKey,
            ctrlKey: evt.ctrlKey,
            shiftKey: evt.shiftKey,
            metaKey: evt.metaKey,
            code: evt.code,
            key: evt.key,
            location: evt.location,
            repeat: evt.repeat,
            locale: evt.locale,
          };
        }
        send_to_server(e, "event");
      });
    }
  },
  props: {
    jp_props: Object,
  },
});
