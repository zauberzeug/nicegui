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

export default {
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
