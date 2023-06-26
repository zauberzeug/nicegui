const p = Math.PI, v = 2 * p, c = 1e-6, q = v - c;
function y() {
  this._x0 = this._y0 = // start of current subpath
  this._x1 = this._y1 = null, this._ = "";
}
function C() {
  return new y();
}
y.prototype = C.prototype = {
  constructor: y,
  moveTo: function(i, s) {
    this._ += "M" + (this._x0 = this._x1 = +i) + "," + (this._y0 = this._y1 = +s);
  },
  closePath: function() {
    this._x1 !== null && (this._x1 = this._x0, this._y1 = this._y0, this._ += "Z");
  },
  lineTo: function(i, s) {
    this._ += "L" + (this._x1 = +i) + "," + (this._y1 = +s);
  },
  quadraticCurveTo: function(i, s, t, h) {
    this._ += "Q" + +i + "," + +s + "," + (this._x1 = +t) + "," + (this._y1 = +h);
  },
  bezierCurveTo: function(i, s, t, h, _, e) {
    this._ += "C" + +i + "," + +s + "," + +t + "," + +h + "," + (this._x1 = +_) + "," + (this._y1 = +e);
  },
  arcTo: function(i, s, t, h, _) {
    i = +i, s = +s, t = +t, h = +h, _ = +_;
    var e = this._x1, r = this._y1, f = t - i, a = h - s, n = e - i, u = r - s, o = n * n + u * u;
    if (_ < 0)
      throw new Error("negative radius: " + _);
    if (this._x1 === null)
      this._ += "M" + (this._x1 = i) + "," + (this._y1 = s);
    else if (o > c)
      if (!(Math.abs(u * f - a * n) > c) || !_)
        this._ += "L" + (this._x1 = i) + "," + (this._y1 = s);
      else {
        var M = t - e, l = h - r, d = f * f + a * a, g = M * M + l * l, b = Math.sqrt(d), T = Math.sqrt(o), A = _ * Math.tan((p - Math.acos((d + o - g) / (2 * b * T))) / 2), x = A / T, L = A / b;
        Math.abs(x - 1) > c && (this._ += "L" + (i + x * n) + "," + (s + x * u)), this._ += "A" + _ + "," + _ + ",0,0," + +(u * M > n * l) + "," + (this._x1 = i + L * f) + "," + (this._y1 = s + L * a);
      }
  },
  arc: function(i, s, t, h, _, e) {
    i = +i, s = +s, t = +t, e = !!e;
    var r = t * Math.cos(h), f = t * Math.sin(h), a = i + r, n = s + f, u = 1 ^ e, o = e ? h - _ : _ - h;
    if (t < 0)
      throw new Error("negative radius: " + t);
    this._x1 === null ? this._ += "M" + a + "," + n : (Math.abs(this._x1 - a) > c || Math.abs(this._y1 - n) > c) && (this._ += "L" + a + "," + n), t && (o < 0 && (o = o % v + v), o > q ? this._ += "A" + t + "," + t + ",0,1," + u + "," + (i - r) + "," + (s - f) + "A" + t + "," + t + ",0,1," + u + "," + (this._x1 = a) + "," + (this._y1 = n) : o > c && (this._ += "A" + t + "," + t + ",0," + +(o >= p) + "," + u + "," + (this._x1 = i + t * Math.cos(_)) + "," + (this._y1 = s + t * Math.sin(_))));
  },
  rect: function(i, s, t, h) {
    this._ += "M" + (this._x0 = this._x1 = +i) + "," + (this._y0 = this._y1 = +s) + "h" + +t + "v" + +h + "h" + -t + "Z";
  },
  toString: function() {
    return this._;
  }
};
function E(i) {
  return function() {
    return i;
  };
}
export {
  E as c,
  C as p
};
//# sourceMappingURL=constant-2fe7eae5.js.map
