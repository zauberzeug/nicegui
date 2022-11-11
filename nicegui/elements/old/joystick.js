Vue.component("joystick", {
  template: `
  <div data-nicegui='joystick' v-bind:id="jp_props.id" :class="jp_props.classes" style="background-color:AliceBlue;position:relative;width:10em;height:10em" :style="jp_props.style"></div>
    `,
  mounted() {
    const joystick = nipplejs.create({
      zone: document.getElementById(this.$props.jp_props.id),
      dynamicPage: true,
      ...this.$props.jp_props.options,
    });
    joystick.on("start", () => {
      const event = {
        event_type: "onStart",
        vue_type: this.$props.jp_props.vue_type,
        id: this.$props.jp_props.id,
        page_id: page_id,
        websocket_id: websocket_id,
      };
      send_to_server(event, "event");
    });
    joystick.on("move", (_, data) => {
      delete data.instance;
      const event = {
        event_type: "onMove",
        vue_type: this.$props.jp_props.vue_type,
        id: this.$props.jp_props.id,
        page_id: page_id,
        websocket_id: websocket_id,
        data: data,
      };
      send_to_server(event, "event");
    });
    joystick.on("end", () => {
      const event = {
        event_type: "onEnd",
        vue_type: this.$props.jp_props.vue_type,
        id: this.$props.jp_props.id,
        page_id: page_id,
        websocket_id: websocket_id,
      };
      send_to_server(event, "event");
    });
  },
  props: {
    jp_props: Object,
  },
});
