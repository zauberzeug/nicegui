export default {
  template: `
    <div style="position:relative">
      <img style="width:100%; height:100%" />
      <svg style="position:absolute;top:0;left:0;pointer-events:none">
        <g style="display:none">
          <line x1="100" y1="0" x2="100" y2="100%" stroke="black" />
          <line x1="0" y1="100" x2="100%" y2="100" stroke="black" />
        </g>
        <g v-html="content"></g>
      </svg>
    </div>
  `,
  data() {
    return {
      content: "",
    };
  },
  mounted() {
    this.image = this.$el.firstChild;
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
    this.svg = this.$el.lastChild;
    const cross = this.svg.firstChild;
    this.image.ondragstart = () => false;
    if (this.cross) {
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
      this.svg.setAttribute("viewBox", viewBox);
    };
    this.image.src = this.src;
    for (const type of this.events) {
      this.image.addEventListener(type, (e) => {
        this.$emit("mouse", {
          mouse_event_type: type,
          image_x: (e.offsetX * e.target.naturalWidth) / e.target.clientWidth,
          image_y: (e.offsetY * e.target.naturalHeight) / e.target.clientHeight,
        });
      });
    }

    this.is_initialized = false;
    const sendConnectEvent = () => {
      if (!this.is_initialized) this.$emit("connect");
      else clearInterval(connectInterval);
    };
    const connectInterval = setInterval(sendConnectEvent, 100);
  },
  methods: {
    set_source(source) {
      this.is_initialized = true;
      if (this.loading) {
        this.waiting_source = source;
        return;
      }
      this.loading = true;
      this.image.src = source;
    },
    set_content(content) {
      this.content = content;
    },
  },
  props: {
    src: String,
    events: Array,
    cross: Boolean,
  },
};
