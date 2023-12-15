import { loadResource } from "../../static/utils/resources.js";

export default {
  template: "<div></div>",
  props: {
    map_options: Object,
    resource_path: String,
  },
  async mounted() {
    await this.$nextTick(); // NOTE: wait for window.path_prefix to be set
    await Promise.all([
      loadResource(window.path_prefix + `${this.resource_path}/leaflet/leaflet.css`),
      loadResource(window.path_prefix + `${this.resource_path}/leaflet/leaflet.js`),
    ]);
    if (this.map_options.drawControl) {
      await Promise.all([
        loadResource(window.path_prefix + `${this.resource_path}/leaflet-draw/leaflet.draw.css`),
        loadResource(window.path_prefix + `${this.resource_path}/leaflet-draw/leaflet.draw.js`),
      ]);
    }
    this.map = L.map(this.$el, this.map_options);
    for (const type of [
      "baselayerchange",
      "overlayadd",
      "overlayremove",
      "layeradd",
      "layerremove",
      "zoomlevelschange",
      "resize",
      "unload",
      "viewreset",
      "load",
      "zoomstart",
      "movestart",
      "zoom",
      "move",
      "zoomend",
      "moveend",
      "popupopen",
      "popupclose",
      "autopanstart",
      "tooltipopen",
      "tooltipclose",
      "locationerror",
      "locationfound",
      "click",
      "dblclick",
      "mousedown",
      "mouseup",
      "mouseover",
      "mouseout",
      "mousemove",
      "contextmenu",
      "keypress",
      "keydown",
      "keyup",
      "preclick",
      "zoomanim",
    ]) {
      this.map.on(type, (e) => {
        this.$emit(`map-${type}`, {
          ...e,
          originalEvent: undefined,
          target: undefined,
          sourceTarget: undefined,
          location: [e.target.getCenter().lat, e.target.getCenter().lng],
          zoom: e.target.getZoom(),
        });
      });
    }
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
    add_layer(layer) {
      L[layer.type](...layer.args).addTo(this.map);
    },
  },
};
