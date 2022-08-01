Vue.component("interactive_image", {
  template: `
    <div :id="jp_props.id" style="position:relative" :style="jp_props.style" :class="jp_props.classes">
      <img style="width:100%; height:100%">
      <svg style="position:absolute;top:0;left:0;pointer-events:none">
        <g style="display:none">
          <line x1="100" y1="0" x2="100" y2="100%" stroke="black" />
          <line x1="0" y1="100" x2="100%" y2="100" stroke="black" />
        </g>
        <g v-html="jp_props.options.svg_content"></g>
      </svg>
    </div>
  `,
  mounted() {
    comp_dict[this.$props.jp_props.id] = this;
    this.image = document.getElementById(this.$props.jp_props.id).firstChild;
    const handle_completion = () => {
      if (this.waiting_source) {
        this.image.src = this.waiting_source;
        this.waiting_source = undefined;
      } else {
        this.loading = false;
      }
    };
    this.image.addEventListener("load", handle_completion);
    this.image.addEventListener("error", handle_completion);
    const svg = document.getElementById(this.$props.jp_props.id).lastChild;
    const cross = svg.firstChild;
    this.image.ondragstart = () => false;
    if (this.$props.jp_props.options.cross) {
      this.image.style.cursor = "none";
      this.image.addEventListener("mouseenter", (e) => {
        cross.style.display = "block";
      });
      this.image.addEventListener("mouseleave", (e) => {
        cross.style.display = "none";
      });
      this.image.addEventListener("mousemove", (e) => {
        const x = (e.offsetX * e.target.naturalWidth) / e.target.clientWidth;
        const y = (e.offsetY * e.target.naturalHeight) / e.target.clientHeight;
        cross.firstChild.setAttribute("x1", x);
        cross.firstChild.setAttribute("x2", x);
        cross.lastChild.setAttribute("y1", y);
        cross.lastChild.setAttribute("y2", y);
      });
    }
    this.image.onload = (e) => {
      const viewBox = `0 0 ${this.image.naturalWidth} ${this.image.naturalHeight}`;
      svg.setAttribute("viewBox", viewBox);
    };
    this.image.src = this.$props.jp_props.options.source;
    for (const type of this.$props.jp_props.options.events) {
      this.image.addEventListener(type, (e) => {
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

    const sendConnectEvent = () => {
      if (websocket_id === "") return;
      const event = {
        event_type: "onConnect",
        vue_type: this.$props.jp_props.vue_type,
        id: this.$props.jp_props.id,
        page_id: page_id,
        websocket_id: websocket_id,
      };
      send_to_server(event, "event");
      clearInterval(connectInterval);
    };
    const connectInterval = setInterval(sendConnectEvent, 100);
  },
  updated() {
    this.image.src = this.$props.jp_props.options.source;
  },
  methods: {
    set_source(source) {
      if (this.loading) {
        this.waiting_source = source;
        return;
      }
      this.loading = true;
      this.image.src = source;
    },
  },
  props: {
    jp_props: Object,
  },
});
