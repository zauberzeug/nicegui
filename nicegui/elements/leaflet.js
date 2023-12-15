import { loadResource } from "../../static/utils/resources.js";

export default {
  template: "<div></div>",
  props: {
    map_options: Object,
    draw_control: Object,
    resource_path: String,
  },
  async mounted() {
    await this.$nextTick(); // NOTE: wait for window.path_prefix to be set
    await Promise.all([
      loadResource(window.path_prefix + `${this.resource_path}/leaflet/leaflet.css`),
      loadResource(window.path_prefix + `${this.resource_path}/leaflet/leaflet.js`),
    ]);
    if (this.draw_control) {
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
          center: [e.target.getCenter().lat, e.target.getCenter().lng],
          zoom: e.target.getZoom(),
        });
      });
    }
    if (this.draw_control) {
      for (const key in L.Draw.Event) {
        const type = L.Draw.Event[key];
        this.map.on(type, (e) => {
          this.$emit(type, {
            ...e,
            layer: e.layer ? { ...e.layer, editing: undefined, _events: undefined } : undefined,
            target: undefined,
            sourceTarget: undefined,
          });
        });
      }
      const drawnItems = new L.FeatureGroup();
      this.map.addLayer(drawnItems);
      const drawControl = new L.Control.Draw({
        edit: { featureGroup: drawnItems },
        ...this.draw_control,
      });
      this.map.addControl(drawControl);
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
