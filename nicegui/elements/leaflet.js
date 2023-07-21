export default {
  template: "<div></div>",
  props: {
    map_options: Object,
  },
  async mounted() {
    await this.load_dependencies();
    this.map = L.map(this.$el, this.map_options);
    this.map.on("moveend", (e) => this.$emit("moveend", e.target.getCenter()));
    this.map.on("zoomend", (e) => this.$emit("zoomend", e.target.getZoom()));
    const connectInterval = setInterval(async () => {
      if (window.socket.id === undefined) return;
      this.$emit("init", { socket_id: window.socket.id });
      clearInterval(connectInterval);
    }, 100);
  },
  updated() {
    this.map.setView(L.latLng(this.map_options.center.lat, this.map_options.center.lng), this.map_options.zoom);
  },
  methods: {
    load_dependencies() {
      if (!document.querySelector(`style[data-leaflet-css]`)) {
        const link = document.createElement("link");
        link.setAttribute("href", "https://unpkg.com/leaflet@1.6.0/dist/leaflet.css");
        link.setAttribute("rel", "stylesheet");
        link.setAttribute("data-leaflet-css", "");
        document.head.appendChild(link);
      }
      if (!document.querySelector(`script[data-leaflet-js]`)) {
        const script = document.createElement("script");
        script.setAttribute("src", "https://unpkg.com/leaflet@1.6.0/dist/leaflet.js");
        script.setAttribute("data-leaflet-js", "");
        document.head.appendChild(script);
        return new Promise((resolve, reject) => {
          script.onload = resolve;
          script.onerror = reject;
        });
      }
    },
    add_layer(layer) {
      L[layer.type](...layer.args).addTo(this.map);
    },
  },
};
