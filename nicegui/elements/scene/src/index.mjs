import * as THREE from "three";
import { CSS2DRenderer, CSS2DObject } from "three/addons/renderers/CSS2DRenderer.js";
import { CSS3DRenderer, CSS3DObject } from "three/addons/renderers/CSS3DRenderer.js";
import { DragControls } from "three/addons/controls/DragControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { MapControls } from "three/addons/controls/MapControls.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { TrackballControls } from "three/addons/controls/TrackballControls.js";
import { STLLoader } from "three/addons/loaders/STLLoader.js";
import { TransformControls } from "three/addons/controls/TransformControls.js";
import * as TWEEN from "@tweenjs/tween.js";
import Stats from "three/examples/jsm/libs/stats.module.js";

function find_object_with_id(object) {
  // Custom components can create children without an "object_id";
  // hits on them are reported under their closest ancestor with an identity.
  // Untagged objects like the grid have no such ancestor, so their hits are dropped.
  let current_object = object;
  while (current_object) {
    if (current_object.object_id) return current_object;
    current_object = current_object.parent;
  }
}

function apply_material(material, { color, opacity, side }) {
  const vertexColors = color === null;
  (Array.isArray(material) ? material : [material]).forEach((m) => {
    m.color.set(vertexColors ? "#ffffff" : color);
    m.needsUpdate = m.vertexColors != vertexColors;
    m.vertexColors = vertexColors;
    m.opacity = opacity;
    if (side == "front") m.side = THREE.FrontSide;
    else if (side == "back") m.side = THREE.BackSide;
    else m.side = THREE.DoubleSide;
  });
}

export {
  apply_material,
  CSS2DObject,
  CSS2DRenderer,
  CSS3DObject,
  CSS3DRenderer,
  DragControls,
  find_object_with_id,
  GLTFLoader,
  MapControls,
  OrbitControls,
  TrackballControls,
  STLLoader,
  TransformControls,
  THREE,
  TWEEN,
  Stats,
};
