import {
  __name
} from "./chunk-DLQEHMXD.mjs";

// src/utils/subGraphTitleMargins.ts
var getSubGraphTitleMargins = /* @__PURE__ */ __name(({
  flowchart
}) => {
  const subGraphTitleTopMargin = flowchart?.subGraphTitleMargin?.top ?? 0;
  const subGraphTitleBottomMargin = flowchart?.subGraphTitleMargin?.bottom ?? 0;
  const subGraphTitleTotalMargin = subGraphTitleTopMargin + subGraphTitleBottomMargin;
  return {
    subGraphTitleTopMargin,
    subGraphTitleBottomMargin,
    subGraphTitleTotalMargin
  };
}, "getSubGraphTitleMargins");

// src/utils/lineWithOffset.ts
var markerOffsets = {
  aggregation: 18,
  extension: 18,
  composition: 18,
  dependency: 6,
  lollipop: 13.5,
  arrow_point: 4
};
function calculateDeltaAndAngle(point1, point2) {
  if (point1 === void 0 || point2 === void 0) {
    return { angle: 0, deltaX: 0, deltaY: 0 };
  }
  point1 = pointTransformer(point1);
  point2 = pointTransformer(point2);
  const [x1, y1] = [point1.x, point1.y];
  const [x2, y2] = [point2.x, point2.y];
  const deltaX = x2 - x1;
  const deltaY = y2 - y1;
  return { angle: Math.atan(deltaY / deltaX), deltaX, deltaY };
}
__name(calculateDeltaAndAngle, "calculateDeltaAndAngle");
var pointTransformer = /* @__PURE__ */ __name((data) => {
  if (Array.isArray(data)) {
    return { x: data[0], y: data[1] };
  }
  return data;
}, "pointTransformer");
var getLineFunctionsWithOffset = /* @__PURE__ */ __name((edge) => {
  return {
    x: /* @__PURE__ */ __name(function(d, i, data) {
      let offset = 0;
      if (i === 0 && Object.hasOwn(markerOffsets, edge.arrowTypeStart)) {
        const { angle, deltaX } = calculateDeltaAndAngle(data[0], data[1]);
        offset = markerOffsets[edge.arrowTypeStart] * Math.cos(angle) * (deltaX >= 0 ? 1 : -1);
      } else if (i === data.length - 1 && Object.hasOwn(markerOffsets, edge.arrowTypeEnd)) {
        const { angle, deltaX } = calculateDeltaAndAngle(
          data[data.length - 1],
          data[data.length - 2]
        );
        offset = markerOffsets[edge.arrowTypeEnd] * Math.cos(angle) * (deltaX >= 0 ? 1 : -1);
      }
      return pointTransformer(d).x + offset;
    }, "x"),
    y: /* @__PURE__ */ __name(function(d, i, data) {
      let offset = 0;
      if (i === 0 && Object.hasOwn(markerOffsets, edge.arrowTypeStart)) {
        const { angle, deltaY } = calculateDeltaAndAngle(data[0], data[1]);
        offset = markerOffsets[edge.arrowTypeStart] * Math.abs(Math.sin(angle)) * (deltaY >= 0 ? 1 : -1);
      } else if (i === data.length - 1 && Object.hasOwn(markerOffsets, edge.arrowTypeEnd)) {
        const { angle, deltaY } = calculateDeltaAndAngle(
          data[data.length - 1],
          data[data.length - 2]
        );
        offset = markerOffsets[edge.arrowTypeEnd] * Math.abs(Math.sin(angle)) * (deltaY >= 0 ? 1 : -1);
      }
      return pointTransformer(d).y + offset;
    }, "y")
  };
}, "getLineFunctionsWithOffset");
if (void 0) {
  const { it, expect, describe } = void 0;
  describe("calculateDeltaAndAngle", () => {
    it("should calculate the angle and deltas between two points", () => {
      expect(calculateDeltaAndAngle([0, 0], [0, 1])).toStrictEqual({
        angle: 1.5707963267948966,
        deltaX: 0,
        deltaY: 1
      });
      expect(calculateDeltaAndAngle([1, 0], [0, -1])).toStrictEqual({
        angle: 0.7853981633974483,
        deltaX: -1,
        deltaY: -1
      });
      expect(calculateDeltaAndAngle({ x: 1, y: 0 }, [0, -1])).toStrictEqual({
        angle: 0.7853981633974483,
        deltaX: -1,
        deltaY: -1
      });
      expect(calculateDeltaAndAngle({ x: 1, y: 0 }, { x: 1, y: 0 })).toStrictEqual({
        angle: NaN,
        deltaX: 0,
        deltaY: 0
      });
    });
    it("should calculate the angle and deltas if one point in undefined", () => {
      expect(calculateDeltaAndAngle(void 0, [0, 1])).toStrictEqual({
        angle: 0,
        deltaX: 0,
        deltaY: 0
      });
      expect(calculateDeltaAndAngle([0, 1], void 0)).toStrictEqual({
        angle: 0,
        deltaX: 0,
        deltaY: 0
      });
    });
  });
}

export {
  getSubGraphTitleMargins,
  getLineFunctionsWithOffset
};
