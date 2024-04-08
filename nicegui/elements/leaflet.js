import { loadResource } from "../../static/utils/resources.js";

export default {
  template: "<div></div>",
  props: {
    center: Array,
    zoom: Number,
    options: Object,
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
    this.map = L.map(this.$el, {
      ...this.options,
      center: this.center,
      zoom: this.zoom,
    });
    for (const type of [
      "baselayerchange",
      "overlayadd",
      "overlayremove",
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
    for (const type of ["layeradd", "layerremove"]) {
      this.map.on(type, (e) => {
        this.$emit(`map-${type}`, {
          id: e.layer.id,
          leaflet_id: e.layer._leaflet_id,
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
    this.map?.setView(this.center, this.zoom);
  },
  methods: {
    add_layer(layer, id) {
      const l = L[layer.type](...layer.args);
      l.id = id;
      l.addTo(this.map);
    },
    remove_layer(id) {
      this.map.eachLayer((layer) => layer.id === id && this.map.removeLayer(layer));
    },
    clear_layers() {
      this.map.eachLayer((layer) => this.map.removeLayer(layer));
    },
    run_map_method(name, ...args) {
      if (name.startsWith(":")) {
        name = name.slice(1);
        args = args.map((arg) => new Function(`return (${arg})`)());
      }
      return runMethod(this.map, name, args);
    },
    run_layer_method(id, name, ...args) {
      let result = null;
      this.map.eachLayer((layer) => {
        if (layer.id !== id) return;
        if (name.startsWith(":")) {
          name = name.slice(1);
          args = args.map((arg) => new Function(`return (${arg})`)());
        }
        result = runMethod(layer, name, args);
      });
      return result;
    },
  },
};
