Vue.component("counter", {
  template: `
  <button v-bind:id="jp_props.id" v-on:click="handle_click">
    <strong>{{jp_props.options.title}}: {{jp_props.options.value}}</strong>
  </button>`,
  methods: {
    handle_click() {
      this.$props.jp_props.options.value += 1;
      const event = {
        event_type: "onChange",
        vue_type: this.$props.jp_props.vue_type,
        id: this.$props.jp_props.id,
        page_id: page_id,
        websocket_id: websocket_id,
        value: this.$props.jp_props.options.value,
      };
      send_to_server(event, "event");
    },
  },
  props: {
    jp_props: Object,
  },
});
