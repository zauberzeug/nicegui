import * as THREE from "three";
import { CSS2DRenderer, CSS2DObject } from "three/addons/renderers/CSS2DRenderer.js";
import { CSS3DRenderer, CSS3DObject } from "three/addons/renderers/CSS3DRenderer.js";
import { DragControls } from "three/addons/controls/DragControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { MapControls } from "three/addons/controls/MapControls.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { TrackballControls } from "three/addons/controls/TrackballControls.js";
import { STLLoader } from "three/addons/loaders/STLLoader.js";
import * as TWEEN from "@tweenjs/tween.js";
import Stats from "three/examples/jsm/libs/stats.module.js";

class SimpleMaterialLoader {
  apply(material, color, opacity, side) {
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
}

export default {
  SimpleMaterialLoader,
  CSS2DObject,
  CSS2DRenderer,
  CSS3DObject,
  CSS3DRenderer,
  DragControls,
  GLTFLoader,
  MapControls,
  OrbitControls,
  TrackballControls,
  STLLoader,
  THREE,
  TWEEN,
  Stats,
};
