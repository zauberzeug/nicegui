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
    if (this.map_options.drawControl) {
      var drawnItems = new L.FeatureGroup();
      this.map.addLayer(drawnItems);
    }
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
    async load_dependencies() {
      if (!document.querySelector(`style[data-leaflet-css]`)) {
        const link = document.createElement("link");
        link.setAttribute("href", "https://unpkg.com/leaflet@1.6.0/dist/leaflet.css");
        link.setAttribute("rel", "stylesheet");
        link.setAttribute("data-leaflet-css", "");
        document.head.appendChild(link);
      }
      if (!document.querySelector(`style[data-leaflet-draw-css]`)) {
        const drawLink = document.createElement("link");
        drawLink.setAttribute("href", "https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.css");
        drawLink.setAttribute("rel", "stylesheet");
        drawLink.setAttribute("data-leaflet-draw-css", "");
        document.head.appendChild(drawLink);
      }
      if (!document.querySelector(`script[data-leaflet-js]`)) {
        const script = document.createElement("script");
        script.setAttribute("src", "https://unpkg.com/leaflet@1.6.0/dist/leaflet.js");
        script.setAttribute("data-leaflet-js", "");
        document.head.appendChild(script);
        await new Promise((resolve, reject) => {
          script.onload = resolve;
          script.onerror = reject;
        });
      }
      if (!document.querySelector(`script[data-leaflet-draw-js]`)) {
        const drawScript = document.createElement("script");
        drawScript.setAttribute("src", "https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.js");
        drawScript.setAttribute("data-leaflet-draw-js", "");
        document.head.appendChild(drawScript);
        await new Promise((resolve, reject) => {
          drawScript.onload = resolve;
          drawScript.onerror = reject;
        });
      }
    },
    add_layer(layer) {
      L[layer.type](...layer.args).addTo(this.map);
    },
  },
};
