import * as Lns from "leaflet/dist/leaflet-src.esm.js";

// Make a mutable Leaflet namespace object for plugins to augment
const L = { ...Lns };

export { L as leaflet };
