import { leaflet as L, loadLeafletDraw } from "nicegui-leaflet";
import { loadResource } from "../../static/utils/resources.js";
import { cleanObject } from "../../static/utils/json.js";

export default {
  template: "<div></div>",
  props: {
    center: Array,
    zoom: Number,
    options: Object,
    drawControl: Object,
    resourcePath: String,
    hideDrawnItems: Boolean,
    additionalResources: Array,
  },
  async mounted() {
    await this.$nextTick(); // NOTE: wait for window.path_prefix to be set
    await loadResource(window.path_prefix + `${this.resourcePath}/leaflet/leaflet.css`);
    window.L = L;
    await Promise.all(this.additionalResources.map((resource) => loadResource(resource)));
    if (this.drawControl) {
      await Promise.all([
        loadResource(window.path_prefix + `${this.resourcePath}/leaflet-draw/leaflet.draw.css`),
        loadLeafletDraw(),
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
    if (this.drawControl) {
      for (const key in L.Draw.Event) {
        const type = L.Draw.Event[key];
        this.map.on(type, async (e) => {
          await this.$nextTick(); // NOTE: allow drawn layers to be added
          const cleanedObject = cleanObject(e, [
            "_map",
            "_events",
            "_eventParents",
            "_handlers",
            "_mapToAdd",
            "_initHooksCalled",
          ]);
          this.$emit(type, {
            ...cleanedObject,
            target: undefined,
            sourceTarget: undefined,
          });
        });
      }

      // HACK: set window.type to avoid a bug in leaflet-draw (https://github.com/Leaflet/Leaflet.draw/issues/1026)
      const originalType = window.type;
      window.type = "Feature";
      const drawnItems = new L.FeatureGroup();
      window.type = originalType;
      this.map.addLayer(drawnItems);

      // Normalize drawControl options: allow boolean True -> {}
      const dc = this.drawControl && typeof this.drawControl === "object" ? this.drawControl : {};
      const drawOptions = dc.draw === true || dc.draw === undefined ? {} : dc.draw || {};
      let editOptions = dc.edit === true || dc.edit === undefined ? {} : dc.edit || {};
      if (typeof editOptions === "object" && "edit" in editOptions) {
        const { edit: _ignoredEditFlag, ...rest } = editOptions;
        editOptions = rest;
      }

      const drawControl = new L.Control.Draw({
        draw: drawOptions,
        edit: {
          ...editOptions,
          featureGroup: drawnItems,
        },
      });
      this.map.addControl(drawControl);
      if (!this.hideDrawnItems) {
        this.map.on("draw:created", (e) => drawnItems.addLayer(e.layer));
      }
    }
    const connectInterval = setInterval(async () => {
      if (window.socket.id === undefined) return;
      this.$emit("init");
      clearInterval(connectInterval);
    }, 100);
    this.observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) this.run_map_method("invalidateSize");
    });
    this.observer.observe(this.$el);
  },
  unmounted() {
    this.observer?.disconnect();
  },
  methods: {
    add_layer(layer, id) {
      let obj = L;
      for (const part of layer.type.split(".")) {
        obj = obj[part];
      }
      const l = obj(...layer.args);
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
