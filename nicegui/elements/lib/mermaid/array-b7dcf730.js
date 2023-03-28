function array(x) {
  return typeof x === "object" && "length" in x ? x : Array.from(x);
}
export {
  array as a
};
//# sourceMappingURL=array-b7dcf730.js.map
