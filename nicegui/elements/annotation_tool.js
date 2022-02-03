Vue.component("annotation_tool", {
  template: `<img v-bind:id="jp_props.id" :src="jp_props.options.source"></div>`,
  mounted() {
    const image = document.getElementById(this.$props.jp_props.id);
    for (const type of this.$props.jp_props.options.events) {
      image.addEventListener(type, (e) => {
        const event = {
          event_type: "onMouse",
          mouse_event_type: type,
          vue_type: this.$props.jp_props.vue_type,
          id: this.$props.jp_props.id,
          page_id: page_id,
          websocket_id: websocket_id,
          image_x: (e.offsetX * e.target.naturalWidth) / e.target.clientWidth,
          image_y: (e.offsetY * e.target.naturalHeight) / e.target.clientHeight,
        };
        send_to_server(event, "event");
      });
    }
  },
  props: {
    jp_props: Object,
  },
});
