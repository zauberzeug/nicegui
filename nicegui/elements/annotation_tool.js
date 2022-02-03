Vue.component("annotation_tool", {
  template: `<img v-bind:id="jp_props.id" :src="jp_props.options.source"></div>`,
  mounted() {
    console.log(this.$props.jp_props);
    const image = document.getElementById(this.$props.jp_props.id);
    image.addEventListener("click", (e) => {
      const event = {
        event_type: "onClick",
        vue_type: this.$props.jp_props.vue_type,
        id: this.$props.jp_props.id,
        page_id: page_id,
        websocket_id: websocket_id,
        image_x: (e.offsetX * e.target.naturalWidth) / e.target.clientWidth,
        image_y: (e.offsetY * e.target.naturalHeight) / e.target.clientHeight,
      };
      send_to_server(event, "event");
    });
  },
  props: {
    jp_props: Object,
  },
});
