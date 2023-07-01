import { M as Color, _ } from "./config-b4fa35bb.js";
const luminance = (color) => {
  const { r, g, b } = Color.parse(color);
  const luminance2 = 0.2126 * _.channel.toLinear(r) + 0.7152 * _.channel.toLinear(g) + 0.0722 * _.channel.toLinear(b);
  return _.lang.round(luminance2);
};
const luminance$1 = luminance;
const isLight = (color) => {
  return luminance$1(color) >= 0.5;
};
const isLight$1 = isLight;
const isDark = (color) => {
  return !isLight$1(color);
};
const isDark$1 = isDark;
export {
  isDark$1 as i
};
//# sourceMappingURL=is_dark-c10d892f.js.map
