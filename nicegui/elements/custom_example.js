Vue.component("custom_example", {
  template: `
  <button v-bind:id="jp_props.id">
    <strong>Custom example component</strong><br/>
    Value = {{jp_props.options.value}}<br/>
    Click to add 1!
    </button>`,
  mounted() {
    document.getElementById(this.$props.jp_props.id).onclick = () => {
      const event = {
        event_type: "onAdd",
        vue_type: this.$props.jp_props.vue_type,
        id: this.$props.jp_props.id,
        page_id: page_id,
        websocket_id: websocket_id,
        number: 1,
      };
      send_to_server(event, "event");
    };
  },
  props: {
    jp_props: Object,
  },
});
