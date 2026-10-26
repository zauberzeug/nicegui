function deepCompare(a, b) {
  if (a === b) return true;
  if (typeof a !== typeof b) return false;
  if (!a || !b || typeof a !== "object") return false;
  if (Array.isArray(a)) {
    if (!Array.isArray(b) || a.length !== b.length) return false;
    for (let i = 0; i < a.length; i++) {
      if (!deepCompare(a[i], b[i])) return false;
    }
    return true;
  }
  // plain object
  const aKeys = Object.keys(a);
  const bKeys = Object.keys(b);
  if (aKeys.length !== bKeys.length) return false;
  for (let i = 0; i < aKeys.length; i++) {
    const k = aKeys[i];
    if (!b.hasOwnProperty(k) || !deepCompare(a[k], b[k])) return false;
  }
  return true;
}

// width and height are ignored because the chart is sized by its host element (see uplot.js)
export function optionsChanged(lhs, rhs) {
  const { width: _lhsWidth, height: _lhsHeight, ...lhsRest } = lhs;
  const { width: _rhsWidth, height: _rhsHeight, ...rhsRest } = rhs;
  return !deepCompare(lhsRest, rhsRest);
}

export function dataMatch(lhs, rhs) {
  if (lhs.length !== rhs.length) {
    return false;
  }
  return lhs.every(function (lhsOneSeries, seriesIdx) {
    const rhsOneSeries = rhs[seriesIdx];
    if (lhsOneSeries.length !== rhsOneSeries.length) {
      return false;
    }
    return lhsOneSeries.every(function (value, valueIdx) {
      return value === rhsOneSeries[valueIdx];
    });
  });
}
