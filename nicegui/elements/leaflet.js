export default {
  template: "<div></div>",
  props: {
    map_options: Object,
    layers: Array,
  },
  async mounted() {
    await this.load_dependencies();
    this.map = L.map(this.$el, this.map_options);
    this.map.on("moveend", (e) => this.$emit("moveend", e.target.getCenter()));
    this.map.on("zoomend", (e) => this.$emit("zoomend", e.target.getZoom()));
    this.layers.forEach((layer) => L.tileLayer(layer.url_template, layer.options).addTo(this.map));
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
  },
};
