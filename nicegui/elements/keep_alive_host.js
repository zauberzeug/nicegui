const CACHE_ID = "nicegui-keep-alive-cache";

export default {
  template: `
    <Teleport :to="target">
      <slot></slot>
    </Teleport>
  `,
  props: {
    anchorSelector: String,
  },
  data() {
    return { target: `#${CACHE_ID}` };
  },
  beforeMount() {
    if (!document.getElementById(CACHE_ID)) {
      const cache = document.createElement("div");
      cache.id = CACHE_ID;
      cache.style.display = "none";
      cache.setAttribute("aria-hidden", "true");
      document.body.appendChild(cache);
    }
  },
  methods: {
    setAnchorReady(ready) {
      this.target = ready ? this.anchorSelector : `#${CACHE_ID}`;
    },
  },
};
