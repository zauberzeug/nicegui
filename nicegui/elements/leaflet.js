export default {
  template: "<div></div>",
  props: {
    map_options: Object,
  },
  async mounted() {
    await this.load_resource("https://unpkg.com/leaflet@1.6.0/dist/leaflet.css");
    await this.load_resource("https://unpkg.com/leaflet@1.6.0/dist/leaflet.js");
    if (this.map_options.drawControl) {
      await this.load_resource("https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.css");
      await this.load_resource("https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.js");
    }
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
    load_resource(url) {
      return new Promise((resolve, reject) => {
        const dataAttribute = `data-${url.split("/").pop().replace(/\./g, "-")}`;
        if (document.querySelector(`[${dataAttribute}]`)) {
          resolve();
          return;
        }
        let element;
        if (url.endsWith(".css")) {
          element = document.createElement("link");
          element.setAttribute("rel", "stylesheet");
          element.setAttribute("href", url);
        } else if (url.endsWith(".js")) {
          element = document.createElement("script");
          element.setAttribute("src", url);
        }
        element.setAttribute(dataAttribute, "");
        document.head.appendChild(element);
        element.onload = resolve;
        element.onerror = reject;
      });
    },
    add_layer(layer) {
      L[layer.type](...layer.args).addTo(this.map);
    },
  },
};
