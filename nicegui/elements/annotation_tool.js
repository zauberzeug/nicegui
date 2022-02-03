Vue.component("annotation_tool", {
  template: `
    <div :id="jp_props.id" style="position:relative;display:inline-block">
      <img style="max-width:100%">
      <svg style="position:absolute;top:0;left:0;pointer-events:none" v-html="jp_props.options.svg_content"></svg>
    </div>
  `,
  mounted() {
    const image = document.getElementById(this.$props.jp_props.id).firstChild;
    const svg = document.getElementById(this.$props.jp_props.id).lastChild;
    image.ondragstart = () => false;
    if (this.$props.jp_props.options.cross) {
      image.style.cursor = "none";
    }
    image.onload = (e) => {
      const viewBox = `0 0 ${image.naturalWidth} ${image.naturalHeight}`;
      svg.setAttribute("viewBox", viewBox);
    };
    image.src = this.$props.jp_props.options.source;
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
