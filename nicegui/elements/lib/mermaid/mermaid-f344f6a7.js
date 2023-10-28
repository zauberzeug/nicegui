function dedent(templ) {
  var values = [];
  for (var _i = 1; _i < arguments.length; _i++) {
    values[_i - 1] = arguments[_i];
  }
  var strings = Array.from(typeof templ === "string" ? [templ] : templ);
  strings[strings.length - 1] = strings[strings.length - 1].replace(/\r?\n([\t ]*)$/, "");
  var indentLengths = strings.reduce(function(arr, str2) {
    var matches = str2.match(/\n([\t ]+|(?!\s).)/g);
    if (matches) {
      return arr.concat(matches.map(function(match) {
        var _a, _b;
        return (_b = (_a = match.match(/[\t ]/g)) === null || _a === void 0 ? void 0 : _a.length) !== null && _b !== void 0 ? _b : 0;
      }));
    }
    return arr;
  }, []);
  if (indentLengths.length) {
    var pattern_1 = new RegExp("\n[	 ]{" + Math.min.apply(Math, indentLengths) + "}", "g");
    strings = strings.map(function(str2) {
      return str2.replace(pattern_1, "\n");
    });
  }
  strings[0] = strings[0].replace(/^\r?\n/, "");
  var string = strings[0];
  values.forEach(function(value, i) {
    var endentations = string.match(/(?:^|\n)( *)$/);
    var endentation = endentations ? endentations[1] : "";
    var indentedValue = value;
    if (typeof value === "string" && value.includes("\n")) {
      indentedValue = String(value).split("\n").map(function(str2, i2) {
        return i2 === 0 ? str2 : "" + endentation + str2;
      }).join("\n");
    }
    string += indentedValue + strings[i + 1];
  });
  return string;
}
var commonjsGlobal = typeof globalThis !== "undefined" ? globalThis : typeof window !== "undefined" ? window : typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : {};
function getDefaultExportFromCjs(x) {
  return x && x.__esModule && Object.prototype.hasOwnProperty.call(x, "default") ? x["default"] : x;
}
var dayjs_min = { exports: {} };
(function(module2, exports2) {
  !function(t, e) {
    module2.exports = e();
  }(commonjsGlobal, function() {
    var t = 1e3, e = 6e4, n = 36e5, r = "millisecond", i = "second", s = "minute", u = "hour", a = "day", o = "week", f = "month", h = "quarter", c = "year", d = "date", l = "Invalid Date", $ = /^(\d{4})[-/]?(\d{1,2})?[-/]?(\d{0,2})[Tt\s]*(\d{1,2})?:?(\d{1,2})?:?(\d{1,2})?[.:]?(\d+)?$/, y = /\[([^\]]+)]|Y{1,4}|M{1,4}|D{1,2}|d{1,4}|H{1,2}|h{1,2}|a|A|m{1,2}|s{1,2}|Z{1,2}|SSS/g, M = { name: "en", weekdays: "Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday".split("_"), months: "January_February_March_April_May_June_July_August_September_October_November_December".split("_"), ordinal: function(t2) {
      var e2 = ["th", "st", "nd", "rd"], n2 = t2 % 100;
      return "[" + t2 + (e2[(n2 - 20) % 10] || e2[n2] || e2[0]) + "]";
    } }, m = function(t2, e2, n2) {
      var r2 = String(t2);
      return !r2 || r2.length >= e2 ? t2 : "" + Array(e2 + 1 - r2.length).join(n2) + t2;
    }, v = { s: m, z: function(t2) {
      var e2 = -t2.utcOffset(), n2 = Math.abs(e2), r2 = Math.floor(n2 / 60), i2 = n2 % 60;
      return (e2 <= 0 ? "+" : "-") + m(r2, 2, "0") + ":" + m(i2, 2, "0");
    }, m: function t2(e2, n2) {
      if (e2.date() < n2.date())
        return -t2(n2, e2);
      var r2 = 12 * (n2.year() - e2.year()) + (n2.month() - e2.month()), i2 = e2.clone().add(r2, f), s2 = n2 - i2 < 0, u2 = e2.clone().add(r2 + (s2 ? -1 : 1), f);
      return +(-(r2 + (n2 - i2) / (s2 ? i2 - u2 : u2 - i2)) || 0);
    }, a: function(t2) {
      return t2 < 0 ? Math.ceil(t2) || 0 : Math.floor(t2);
    }, p: function(t2) {
      return { M: f, y: c, w: o, d: a, D: d, h: u, m: s, s: i, ms: r, Q: h }[t2] || String(t2 || "").toLowerCase().replace(/s$/, "");
    }, u: function(t2) {
      return void 0 === t2;
    } }, g = "en", D = {};
    D[g] = M;
    var p = function(t2) {
      return t2 instanceof _2;
    }, S = function t2(e2, n2, r2) {
      var i2;
      if (!e2)
        return g;
      if ("string" == typeof e2) {
        var s2 = e2.toLowerCase();
        D[s2] && (i2 = s2), n2 && (D[s2] = n2, i2 = s2);
        var u2 = e2.split("-");
        if (!i2 && u2.length > 1)
          return t2(u2[0]);
      } else {
        var a2 = e2.name;
        D[a2] = e2, i2 = a2;
      }
      return !r2 && i2 && (g = i2), i2 || !r2 && g;
    }, w = function(t2, e2) {
      if (p(t2))
        return t2.clone();
      var n2 = "object" == typeof e2 ? e2 : {};
      return n2.date = t2, n2.args = arguments, new _2(n2);
    }, O = v;
    O.l = S, O.i = p, O.w = function(t2, e2) {
      return w(t2, { locale: e2.$L, utc: e2.$u, x: e2.$x, $offset: e2.$offset });
    };
    var _2 = function() {
      function M2(t2) {
        this.$L = S(t2.locale, null, true), this.parse(t2);
      }
      var m2 = M2.prototype;
      return m2.parse = function(t2) {
        this.$d = function(t3) {
          var e2 = t3.date, n2 = t3.utc;
          if (null === e2)
            return /* @__PURE__ */ new Date(NaN);
          if (O.u(e2))
            return /* @__PURE__ */ new Date();
          if (e2 instanceof Date)
            return new Date(e2);
          if ("string" == typeof e2 && !/Z$/i.test(e2)) {
            var r2 = e2.match($);
            if (r2) {
              var i2 = r2[2] - 1 || 0, s2 = (r2[7] || "0").substring(0, 3);
              return n2 ? new Date(Date.UTC(r2[1], i2, r2[3] || 1, r2[4] || 0, r2[5] || 0, r2[6] || 0, s2)) : new Date(r2[1], i2, r2[3] || 1, r2[4] || 0, r2[5] || 0, r2[6] || 0, s2);
            }
          }
          return new Date(e2);
        }(t2), this.$x = t2.x || {}, this.init();
      }, m2.init = function() {
        var t2 = this.$d;
        this.$y = t2.getFullYear(), this.$M = t2.getMonth(), this.$D = t2.getDate(), this.$W = t2.getDay(), this.$H = t2.getHours(), this.$m = t2.getMinutes(), this.$s = t2.getSeconds(), this.$ms = t2.getMilliseconds();
      }, m2.$utils = function() {
        return O;
      }, m2.isValid = function() {
        return !(this.$d.toString() === l);
      }, m2.isSame = function(t2, e2) {
        var n2 = w(t2);
        return this.startOf(e2) <= n2 && n2 <= this.endOf(e2);
      }, m2.isAfter = function(t2, e2) {
        return w(t2) < this.startOf(e2);
      }, m2.isBefore = function(t2, e2) {
        return this.endOf(e2) < w(t2);
      }, m2.$g = function(t2, e2, n2) {
        return O.u(t2) ? this[e2] : this.set(n2, t2);
      }, m2.unix = function() {
        return Math.floor(this.valueOf() / 1e3);
      }, m2.valueOf = function() {
        return this.$d.getTime();
      }, m2.startOf = function(t2, e2) {
        var n2 = this, r2 = !!O.u(e2) || e2, h2 = O.p(t2), l2 = function(t3, e3) {
          var i2 = O.w(n2.$u ? Date.UTC(n2.$y, e3, t3) : new Date(n2.$y, e3, t3), n2);
          return r2 ? i2 : i2.endOf(a);
        }, $2 = function(t3, e3) {
          return O.w(n2.toDate()[t3].apply(n2.toDate("s"), (r2 ? [0, 0, 0, 0] : [23, 59, 59, 999]).slice(e3)), n2);
        }, y2 = this.$W, M3 = this.$M, m3 = this.$D, v2 = "set" + (this.$u ? "UTC" : "");
        switch (h2) {
          case c:
            return r2 ? l2(1, 0) : l2(31, 11);
          case f:
            return r2 ? l2(1, M3) : l2(0, M3 + 1);
          case o:
            var g2 = this.$locale().weekStart || 0, D2 = (y2 < g2 ? y2 + 7 : y2) - g2;
            return l2(r2 ? m3 - D2 : m3 + (6 - D2), M3);
          case a:
          case d:
            return $2(v2 + "Hours", 0);
          case u:
            return $2(v2 + "Minutes", 1);
          case s:
            return $2(v2 + "Seconds", 2);
          case i:
            return $2(v2 + "Milliseconds", 3);
          default:
            return this.clone();
        }
      }, m2.endOf = function(t2) {
        return this.startOf(t2, false);
      }, m2.$set = function(t2, e2) {
        var n2, o2 = O.p(t2), h2 = "set" + (this.$u ? "UTC" : ""), l2 = (n2 = {}, n2[a] = h2 + "Date", n2[d] = h2 + "Date", n2[f] = h2 + "Month", n2[c] = h2 + "FullYear", n2[u] = h2 + "Hours", n2[s] = h2 + "Minutes", n2[i] = h2 + "Seconds", n2[r] = h2 + "Milliseconds", n2)[o2], $2 = o2 === a ? this.$D + (e2 - this.$W) : e2;
        if (o2 === f || o2 === c) {
          var y2 = this.clone().set(d, 1);
          y2.$d[l2]($2), y2.init(), this.$d = y2.set(d, Math.min(this.$D, y2.daysInMonth())).$d;
        } else
          l2 && this.$d[l2]($2);
        return this.init(), this;
      }, m2.set = function(t2, e2) {
        return this.clone().$set(t2, e2);
      }, m2.get = function(t2) {
        return this[O.p(t2)]();
      }, m2.add = function(r2, h2) {
        var d2, l2 = this;
        r2 = Number(r2);
        var $2 = O.p(h2), y2 = function(t2) {
          var e2 = w(l2);
          return O.w(e2.date(e2.date() + Math.round(t2 * r2)), l2);
        };
        if ($2 === f)
          return this.set(f, this.$M + r2);
        if ($2 === c)
          return this.set(c, this.$y + r2);
        if ($2 === a)
          return y2(1);
        if ($2 === o)
          return y2(7);
        var M3 = (d2 = {}, d2[s] = e, d2[u] = n, d2[i] = t, d2)[$2] || 1, m3 = this.$d.getTime() + r2 * M3;
        return O.w(m3, this);
      }, m2.subtract = function(t2, e2) {
        return this.add(-1 * t2, e2);
      }, m2.format = function(t2) {
        var e2 = this, n2 = this.$locale();
        if (!this.isValid())
          return n2.invalidDate || l;
        var r2 = t2 || "YYYY-MM-DDTHH:mm:ssZ", i2 = O.z(this), s2 = this.$H, u2 = this.$m, a2 = this.$M, o2 = n2.weekdays, f2 = n2.months, h2 = function(t3, n3, i3, s3) {
          return t3 && (t3[n3] || t3(e2, r2)) || i3[n3].slice(0, s3);
        }, c2 = function(t3) {
          return O.s(s2 % 12 || 12, t3, "0");
        }, d2 = n2.meridiem || function(t3, e3, n3) {
          var r3 = t3 < 12 ? "AM" : "PM";
          return n3 ? r3.toLowerCase() : r3;
        }, $2 = { YY: String(this.$y).slice(-2), YYYY: this.$y, M: a2 + 1, MM: O.s(a2 + 1, 2, "0"), MMM: h2(n2.monthsShort, a2, f2, 3), MMMM: h2(f2, a2), D: this.$D, DD: O.s(this.$D, 2, "0"), d: String(this.$W), dd: h2(n2.weekdaysMin, this.$W, o2, 2), ddd: h2(n2.weekdaysShort, this.$W, o2, 3), dddd: o2[this.$W], H: String(s2), HH: O.s(s2, 2, "0"), h: c2(1), hh: c2(2), a: d2(s2, u2, true), A: d2(s2, u2, false), m: String(u2), mm: O.s(u2, 2, "0"), s: String(this.$s), ss: O.s(this.$s, 2, "0"), SSS: O.s(this.$ms, 3, "0"), Z: i2 };
        return r2.replace(y, function(t3, e3) {
          return e3 || $2[t3] || i2.replace(":", "");
        });
      }, m2.utcOffset = function() {
        return 15 * -Math.round(this.$d.getTimezoneOffset() / 15);
      }, m2.diff = function(r2, d2, l2) {
        var $2, y2 = O.p(d2), M3 = w(r2), m3 = (M3.utcOffset() - this.utcOffset()) * e, v2 = this - M3, g2 = O.m(this, M3);
        return g2 = ($2 = {}, $2[c] = g2 / 12, $2[f] = g2, $2[h] = g2 / 3, $2[o] = (v2 - m3) / 6048e5, $2[a] = (v2 - m3) / 864e5, $2[u] = v2 / n, $2[s] = v2 / e, $2[i] = v2 / t, $2)[y2] || v2, l2 ? g2 : O.a(g2);
      }, m2.daysInMonth = function() {
        return this.endOf(f).$D;
      }, m2.$locale = function() {
        return D[this.$L];
      }, m2.locale = function(t2, e2) {
        if (!t2)
          return this.$L;
        var n2 = this.clone(), r2 = S(t2, e2, true);
        return r2 && (n2.$L = r2), n2;
      }, m2.clone = function() {
        return O.w(this.$d, this);
      }, m2.toDate = function() {
        return new Date(this.valueOf());
      }, m2.toJSON = function() {
        return this.isValid() ? this.toISOString() : null;
      }, m2.toISOString = function() {
        return this.$d.toISOString();
      }, m2.toString = function() {
        return this.$d.toUTCString();
      }, M2;
    }(), T = _2.prototype;
    return w.prototype = T, [["$ms", r], ["$s", i], ["$m", s], ["$H", u], ["$W", a], ["$M", f], ["$y", c], ["$D", d]].forEach(function(t2) {
      T[t2[1]] = function(e2) {
        return this.$g(e2, t2[0], t2[1]);
      };
    }), w.extend = function(t2, e2) {
      return t2.$i || (t2(e2, _2, w), t2.$i = true), w;
    }, w.locale = S, w.isDayjs = p, w.unix = function(t2) {
      return w(1e3 * t2);
    }, w.en = D[g], w.Ls = D, w.p = {}, w;
  });
})(dayjs_min);
var dayjs_minExports = dayjs_min.exports;
const dayjs = /* @__PURE__ */ getDefaultExportFromCjs(dayjs_minExports);
const LEVELS = {
  trace: 0,
  debug: 1,
  info: 2,
  warn: 3,
  error: 4,
  fatal: 5
};
const log$1 = {
  trace: (..._args) => {
  },
  debug: (..._args) => {
  },
  info: (..._args) => {
  },
  warn: (..._args) => {
  },
  error: (..._args) => {
  },
  fatal: (..._args) => {
  }
};
const setLogLevel$1 = function(level = "fatal") {
  let numericLevel = LEVELS.fatal;
  if (typeof level === "string") {
    level = level.toLowerCase();
    if (level in LEVELS) {
      numericLevel = LEVELS[level];
    }
  } else if (typeof level === "number") {
    numericLevel = level;
  }
  log$1.trace = () => {
  };
  log$1.debug = () => {
  };
  log$1.info = () => {
  };
  log$1.warn = () => {
  };
  log$1.error = () => {
  };
  log$1.fatal = () => {
  };
  if (numericLevel <= LEVELS.fatal) {
    log$1.fatal = console.error ? console.error.bind(console, format("FATAL"), "color: orange") : console.log.bind(console, "\x1B[35m", format("FATAL"));
  }
  if (numericLevel <= LEVELS.error) {
    log$1.error = console.error ? console.error.bind(console, format("ERROR"), "color: orange") : console.log.bind(console, "\x1B[31m", format("ERROR"));
  }
  if (numericLevel <= LEVELS.warn) {
    log$1.warn = console.warn ? console.warn.bind(console, format("WARN"), "color: orange") : console.log.bind(console, `\x1B[33m`, format("WARN"));
  }
  if (numericLevel <= LEVELS.info) {
    log$1.info = console.info ? console.info.bind(console, format("INFO"), "color: lightblue") : console.log.bind(console, "\x1B[34m", format("INFO"));
  }
  if (numericLevel <= LEVELS.debug) {
    log$1.debug = console.debug ? console.debug.bind(console, format("DEBUG"), "color: lightgreen") : console.log.bind(console, "\x1B[32m", format("DEBUG"));
  }
  if (numericLevel <= LEVELS.trace) {
    log$1.trace = console.debug ? console.debug.bind(console, format("TRACE"), "color: lightgreen") : console.log.bind(console, "\x1B[32m", format("TRACE"));
  }
};
const format = (level) => {
  const time = dayjs().format("ss.SSS");
  return `%c${time} : ${level} : `;
};
var dist = {};
Object.defineProperty(dist, "__esModule", { value: true });
var sanitizeUrl_1 = dist.sanitizeUrl = void 0;
var invalidProtocolRegex = /^([^\w]*)(javascript|data|vbscript)/im;
var htmlEntitiesRegex = /&#(\w+)(^\w|;)?/g;
var htmlCtrlEntityRegex = /&(newline|tab);/gi;
var ctrlCharactersRegex = /[\u0000-\u001F\u007F-\u009F\u2000-\u200D\uFEFF]/gim;
var urlSchemeRegex = /^.+(:|&colon;)/gim;
var relativeFirstCharacters = [".", "/"];
function isRelativeUrlWithoutProtocol(url) {
  return relativeFirstCharacters.indexOf(url[0]) > -1;
}
function decodeHtmlCharacters(str2) {
  return str2.replace(htmlEntitiesRegex, function(match, dec) {
    return String.fromCharCode(dec);
  });
}
function sanitizeUrl(url) {
  var sanitizedUrl = decodeHtmlCharacters(url || "").replace(htmlCtrlEntityRegex, "").replace(ctrlCharactersRegex, "").trim();
  if (!sanitizedUrl) {
    return "about:blank";
  }
  if (isRelativeUrlWithoutProtocol(sanitizedUrl)) {
    return sanitizedUrl;
  }
  var urlSchemeParseResults = sanitizedUrl.match(urlSchemeRegex);
  if (!urlSchemeParseResults) {
    return sanitizedUrl;
  }
  var urlScheme = urlSchemeParseResults[0];
  if (invalidProtocolRegex.test(urlScheme)) {
    return "about:blank";
  }
  return sanitizedUrl;
}
sanitizeUrl_1 = dist.sanitizeUrl = sanitizeUrl;
var noop$1 = { value: () => {
} };
function dispatch() {
  for (var i = 0, n = arguments.length, _2 = {}, t; i < n; ++i) {
    if (!(t = arguments[i] + "") || t in _2 || /[\s.]/.test(t))
      throw new Error("illegal type: " + t);
    _2[t] = [];
  }
  return new Dispatch(_2);
}
function Dispatch(_2) {
  this._ = _2;
}
function parseTypenames$1(typenames, types) {
  return typenames.trim().split(/^|\s+/).map(function(t) {
    var name = "", i = t.indexOf(".");
    if (i >= 0)
      name = t.slice(i + 1), t = t.slice(0, i);
    if (t && !types.hasOwnProperty(t))
      throw new Error("unknown type: " + t);
    return { type: t, name };
  });
}
Dispatch.prototype = dispatch.prototype = {
  constructor: Dispatch,
  on: function(typename, callback) {
    var _2 = this._, T = parseTypenames$1(typename + "", _2), t, i = -1, n = T.length;
    if (arguments.length < 2) {
      while (++i < n)
        if ((t = (typename = T[i]).type) && (t = get$1(_2[t], typename.name)))
          return t;
      return;
    }
    if (callback != null && typeof callback !== "function")
      throw new Error("invalid callback: " + callback);
    while (++i < n) {
      if (t = (typename = T[i]).type)
        _2[t] = set$2(_2[t], typename.name, callback);
      else if (callback == null)
        for (t in _2)
          _2[t] = set$2(_2[t], typename.name, null);
    }
    return this;
  },
  copy: function() {
    var copy = {}, _2 = this._;
    for (var t in _2)
      copy[t] = _2[t].slice();
    return new Dispatch(copy);
  },
  call: function(type2, that) {
    if ((n = arguments.length - 2) > 0)
      for (var args = new Array(n), i = 0, n, t; i < n; ++i)
        args[i] = arguments[i + 2];
    if (!this._.hasOwnProperty(type2))
      throw new Error("unknown type: " + type2);
    for (t = this._[type2], i = 0, n = t.length; i < n; ++i)
      t[i].value.apply(that, args);
  },
  apply: function(type2, that, args) {
    if (!this._.hasOwnProperty(type2))
      throw new Error("unknown type: " + type2);
    for (var t = this._[type2], i = 0, n = t.length; i < n; ++i)
      t[i].value.apply(that, args);
  }
};
function get$1(type2, name) {
  for (var i = 0, n = type2.length, c; i < n; ++i) {
    if ((c = type2[i]).name === name) {
      return c.value;
    }
  }
}
function set$2(type2, name, callback) {
  for (var i = 0, n = type2.length; i < n; ++i) {
    if (type2[i].name === name) {
      type2[i] = noop$1, type2 = type2.slice(0, i).concat(type2.slice(i + 1));
      break;
    }
  }
  if (callback != null)
    type2.push({ name, value: callback });
  return type2;
}
var xhtml = "http://www.w3.org/1999/xhtml";
const namespaces = {
  svg: "http://www.w3.org/2000/svg",
  xhtml,
  xlink: "http://www.w3.org/1999/xlink",
  xml: "http://www.w3.org/XML/1998/namespace",
  xmlns: "http://www.w3.org/2000/xmlns/"
};
function namespace(name) {
  var prefix = name += "", i = prefix.indexOf(":");
  if (i >= 0 && (prefix = name.slice(0, i)) !== "xmlns")
    name = name.slice(i + 1);
  return namespaces.hasOwnProperty(prefix) ? { space: namespaces[prefix], local: name } : name;
}
function creatorInherit(name) {
  return function() {
    var document2 = this.ownerDocument, uri = this.namespaceURI;
    return uri === xhtml && document2.documentElement.namespaceURI === xhtml ? document2.createElement(name) : document2.createElementNS(uri, name);
  };
}
function creatorFixed(fullname) {
  return function() {
    return this.ownerDocument.createElementNS(fullname.space, fullname.local);
  };
}
function creator(name) {
  var fullname = namespace(name);
  return (fullname.local ? creatorFixed : creatorInherit)(fullname);
}
function none() {
}
function selector(selector2) {
  return selector2 == null ? none : function() {
    return this.querySelector(selector2);
  };
}
function selection_select(select) {
  if (typeof select !== "function")
    select = selector(select);
  for (var groups = this._groups, m = groups.length, subgroups = new Array(m), j = 0; j < m; ++j) {
    for (var group = groups[j], n = group.length, subgroup = subgroups[j] = new Array(n), node2, subnode, i = 0; i < n; ++i) {
      if ((node2 = group[i]) && (subnode = select.call(node2, node2.__data__, i, group))) {
        if ("__data__" in node2)
          subnode.__data__ = node2.__data__;
        subgroup[i] = subnode;
      }
    }
  }
  return new Selection$1(subgroups, this._parents);
}
function array(x) {
  return x == null ? [] : Array.isArray(x) ? x : Array.from(x);
}
function empty() {
  return [];
}
function selectorAll(selector2) {
  return selector2 == null ? empty : function() {
    return this.querySelectorAll(selector2);
  };
}
function arrayAll(select) {
  return function() {
    return array(select.apply(this, arguments));
  };
}
function selection_selectAll(select) {
  if (typeof select === "function")
    select = arrayAll(select);
  else
    select = selectorAll(select);
  for (var groups = this._groups, m = groups.length, subgroups = [], parents = [], j = 0; j < m; ++j) {
    for (var group = groups[j], n = group.length, node2, i = 0; i < n; ++i) {
      if (node2 = group[i]) {
        subgroups.push(select.call(node2, node2.__data__, i, group));
        parents.push(node2);
      }
    }
  }
  return new Selection$1(subgroups, parents);
}
function matcher(selector2) {
  return function() {
    return this.matches(selector2);
  };
}
function childMatcher(selector2) {
  return function(node2) {
    return node2.matches(selector2);
  };
}
var find = Array.prototype.find;
function childFind(match) {
  return function() {
    return find.call(this.children, match);
  };
}
function childFirst() {
  return this.firstElementChild;
}
function selection_selectChild(match) {
  return this.select(match == null ? childFirst : childFind(typeof match === "function" ? match : childMatcher(match)));
}
var filter = Array.prototype.filter;
function children() {
  return Array.from(this.children);
}
function childrenFilter(match) {
  return function() {
    return filter.call(this.children, match);
  };
}
function selection_selectChildren(match) {
  return this.selectAll(match == null ? children : childrenFilter(typeof match === "function" ? match : childMatcher(match)));
}
function selection_filter(match) {
  if (typeof match !== "function")
    match = matcher(match);
  for (var groups = this._groups, m = groups.length, subgroups = new Array(m), j = 0; j < m; ++j) {
    for (var group = groups[j], n = group.length, subgroup = subgroups[j] = [], node2, i = 0; i < n; ++i) {
      if ((node2 = group[i]) && match.call(node2, node2.__data__, i, group)) {
        subgroup.push(node2);
      }
    }
  }
  return new Selection$1(subgroups, this._parents);
}
function sparse(update) {
  return new Array(update.length);
}
function selection_enter() {
  return new Selection$1(this._enter || this._groups.map(sparse), this._parents);
}
function EnterNode(parent, datum2) {
  this.ownerDocument = parent.ownerDocument;
  this.namespaceURI = parent.namespaceURI;
  this._next = null;
  this._parent = parent;
  this.__data__ = datum2;
}
EnterNode.prototype = {
  constructor: EnterNode,
  appendChild: function(child) {
    return this._parent.insertBefore(child, this._next);
  },
  insertBefore: function(child, next2) {
    return this._parent.insertBefore(child, next2);
  },
  querySelector: function(selector2) {
    return this._parent.querySelector(selector2);
  },
  querySelectorAll: function(selector2) {
    return this._parent.querySelectorAll(selector2);
  }
};
function constant$2(x) {
  return function() {
    return x;
  };
}
function bindIndex(parent, group, enter, update, exit, data) {
  var i = 0, node2, groupLength = group.length, dataLength = data.length;
  for (; i < dataLength; ++i) {
    if (node2 = group[i]) {
      node2.__data__ = data[i];
      update[i] = node2;
    } else {
      enter[i] = new EnterNode(parent, data[i]);
    }
  }
  for (; i < groupLength; ++i) {
    if (node2 = group[i]) {
      exit[i] = node2;
    }
  }
}
function bindKey(parent, group, enter, update, exit, data, key) {
  var i, node2, nodeByKeyValue = /* @__PURE__ */ new Map(), groupLength = group.length, dataLength = data.length, keyValues = new Array(groupLength), keyValue;
  for (i = 0; i < groupLength; ++i) {
    if (node2 = group[i]) {
      keyValues[i] = keyValue = key.call(node2, node2.__data__, i, group) + "";
      if (nodeByKeyValue.has(keyValue)) {
        exit[i] = node2;
      } else {
        nodeByKeyValue.set(keyValue, node2);
      }
    }
  }
  for (i = 0; i < dataLength; ++i) {
    keyValue = key.call(parent, data[i], i, data) + "";
    if (node2 = nodeByKeyValue.get(keyValue)) {
      update[i] = node2;
      node2.__data__ = data[i];
      nodeByKeyValue.delete(keyValue);
    } else {
      enter[i] = new EnterNode(parent, data[i]);
    }
  }
  for (i = 0; i < groupLength; ++i) {
    if ((node2 = group[i]) && nodeByKeyValue.get(keyValues[i]) === node2) {
      exit[i] = node2;
    }
  }
}
function datum(node2) {
  return node2.__data__;
}
function selection_data(value, key) {
  if (!arguments.length)
    return Array.from(this, datum);
  var bind = key ? bindKey : bindIndex, parents = this._parents, groups = this._groups;
  if (typeof value !== "function")
    value = constant$2(value);
  for (var m = groups.length, update = new Array(m), enter = new Array(m), exit = new Array(m), j = 0; j < m; ++j) {
    var parent = parents[j], group = groups[j], groupLength = group.length, data = arraylike(value.call(parent, parent && parent.__data__, j, parents)), dataLength = data.length, enterGroup = enter[j] = new Array(dataLength), updateGroup = update[j] = new Array(dataLength), exitGroup = exit[j] = new Array(groupLength);
    bind(parent, group, enterGroup, updateGroup, exitGroup, data, key);
    for (var i0 = 0, i1 = 0, previous, next2; i0 < dataLength; ++i0) {
      if (previous = enterGroup[i0]) {
        if (i0 >= i1)
          i1 = i0 + 1;
        while (!(next2 = updateGroup[i1]) && ++i1 < dataLength)
          ;
        previous._next = next2 || null;
      }
    }
  }
  update = new Selection$1(update, parents);
  update._enter = enter;
  update._exit = exit;
  return update;
}
function arraylike(data) {
  return typeof data === "object" && "length" in data ? data : Array.from(data);
}
function selection_exit() {
  return new Selection$1(this._exit || this._groups.map(sparse), this._parents);
}
function selection_join(onenter, onupdate, onexit) {
  var enter = this.enter(), update = this, exit = this.exit();
  if (typeof onenter === "function") {
    enter = onenter(enter);
    if (enter)
      enter = enter.selection();
  } else {
    enter = enter.append(onenter + "");
  }
  if (onupdate != null) {
    update = onupdate(update);
    if (update)
      update = update.selection();
  }
  if (onexit == null)
    exit.remove();
  else
    onexit(exit);
  return enter && update ? enter.merge(update).order() : update;
}
function selection_merge(context) {
  var selection2 = context.selection ? context.selection() : context;
  for (var groups0 = this._groups, groups1 = selection2._groups, m0 = groups0.length, m1 = groups1.length, m = Math.min(m0, m1), merges = new Array(m0), j = 0; j < m; ++j) {
    for (var group0 = groups0[j], group1 = groups1[j], n = group0.length, merge2 = merges[j] = new Array(n), node2, i = 0; i < n; ++i) {
      if (node2 = group0[i] || group1[i]) {
        merge2[i] = node2;
      }
    }
  }
  for (; j < m0; ++j) {
    merges[j] = groups0[j];
  }
  return new Selection$1(merges, this._parents);
}
function selection_order() {
  for (var groups = this._groups, j = -1, m = groups.length; ++j < m; ) {
    for (var group = groups[j], i = group.length - 1, next2 = group[i], node2; --i >= 0; ) {
      if (node2 = group[i]) {
        if (next2 && node2.compareDocumentPosition(next2) ^ 4)
          next2.parentNode.insertBefore(node2, next2);
        next2 = node2;
      }
    }
  }
  return this;
}
function selection_sort(compare) {
  if (!compare)
    compare = ascending;
  function compareNode(a, b) {
    return a && b ? compare(a.__data__, b.__data__) : !a - !b;
  }
  for (var groups = this._groups, m = groups.length, sortgroups = new Array(m), j = 0; j < m; ++j) {
    for (var group = groups[j], n = group.length, sortgroup = sortgroups[j] = new Array(n), node2, i = 0; i < n; ++i) {
      if (node2 = group[i]) {
        sortgroup[i] = node2;
      }
    }
    sortgroup.sort(compareNode);
  }
  return new Selection$1(sortgroups, this._parents).order();
}
function ascending(a, b) {
  return a < b ? -1 : a > b ? 1 : a >= b ? 0 : NaN;
}
function selection_call() {
  var callback = arguments[0];
  arguments[0] = this;
  callback.apply(null, arguments);
  return this;
}
function selection_nodes() {
  return Array.from(this);
}
function selection_node() {
  for (var groups = this._groups, j = 0, m = groups.length; j < m; ++j) {
    for (var group = groups[j], i = 0, n = group.length; i < n; ++i) {
      var node2 = group[i];
      if (node2)
        return node2;
    }
  }
  return null;
}
function selection_size() {
  let size = 0;
  for (const node2 of this)
    ++size;
  return size;
}
function selection_empty() {
  return !this.node();
}
function selection_each(callback) {
  for (var groups = this._groups, j = 0, m = groups.length; j < m; ++j) {
    for (var group = groups[j], i = 0, n = group.length, node2; i < n; ++i) {
      if (node2 = group[i])
        callback.call(node2, node2.__data__, i, group);
    }
  }
  return this;
}
function attrRemove$1(name) {
  return function() {
    this.removeAttribute(name);
  };
}
function attrRemoveNS$1(fullname) {
  return function() {
    this.removeAttributeNS(fullname.space, fullname.local);
  };
}
function attrConstant$1(name, value) {
  return function() {
    this.setAttribute(name, value);
  };
}
function attrConstantNS$1(fullname, value) {
  return function() {
    this.setAttributeNS(fullname.space, fullname.local, value);
  };
}
function attrFunction$1(name, value) {
  return function() {
    var v = value.apply(this, arguments);
    if (v == null)
      this.removeAttribute(name);
    else
      this.setAttribute(name, v);
  };
}
function attrFunctionNS$1(fullname, value) {
  return function() {
    var v = value.apply(this, arguments);
    if (v == null)
      this.removeAttributeNS(fullname.space, fullname.local);
    else
      this.setAttributeNS(fullname.space, fullname.local, v);
  };
}
function selection_attr(name, value) {
  var fullname = namespace(name);
  if (arguments.length < 2) {
    var node2 = this.node();
    return fullname.local ? node2.getAttributeNS(fullname.space, fullname.local) : node2.getAttribute(fullname);
  }
  return this.each((value == null ? fullname.local ? attrRemoveNS$1 : attrRemove$1 : typeof value === "function" ? fullname.local ? attrFunctionNS$1 : attrFunction$1 : fullname.local ? attrConstantNS$1 : attrConstant$1)(fullname, value));
}
function defaultView(node2) {
  return node2.ownerDocument && node2.ownerDocument.defaultView || node2.document && node2 || node2.defaultView;
}
function styleRemove$1(name) {
  return function() {
    this.style.removeProperty(name);
  };
}
function styleConstant$1(name, value, priority) {
  return function() {
    this.style.setProperty(name, value, priority);
  };
}
function styleFunction$1(name, value, priority) {
  return function() {
    var v = value.apply(this, arguments);
    if (v == null)
      this.style.removeProperty(name);
    else
      this.style.setProperty(name, v, priority);
  };
}
function selection_style(name, value, priority) {
  return arguments.length > 1 ? this.each((value == null ? styleRemove$1 : typeof value === "function" ? styleFunction$1 : styleConstant$1)(name, value, priority == null ? "" : priority)) : styleValue(this.node(), name);
}
function styleValue(node2, name) {
  return node2.style.getPropertyValue(name) || defaultView(node2).getComputedStyle(node2, null).getPropertyValue(name);
}
function propertyRemove(name) {
  return function() {
    delete this[name];
  };
}
function propertyConstant(name, value) {
  return function() {
    this[name] = value;
  };
}
function propertyFunction(name, value) {
  return function() {
    var v = value.apply(this, arguments);
    if (v == null)
      delete this[name];
    else
      this[name] = v;
  };
}
function selection_property(name, value) {
  return arguments.length > 1 ? this.each((value == null ? propertyRemove : typeof value === "function" ? propertyFunction : propertyConstant)(name, value)) : this.node()[name];
}
function classArray(string) {
  return string.trim().split(/^|\s+/);
}
function classList(node2) {
  return node2.classList || new ClassList(node2);
}
function ClassList(node2) {
  this._node = node2;
  this._names = classArray(node2.getAttribute("class") || "");
}
ClassList.prototype = {
  add: function(name) {
    var i = this._names.indexOf(name);
    if (i < 0) {
      this._names.push(name);
      this._node.setAttribute("class", this._names.join(" "));
    }
  },
  remove: function(name) {
    var i = this._names.indexOf(name);
    if (i >= 0) {
      this._names.splice(i, 1);
      this._node.setAttribute("class", this._names.join(" "));
    }
  },
  contains: function(name) {
    return this._names.indexOf(name) >= 0;
  }
};
function classedAdd(node2, names) {
  var list = classList(node2), i = -1, n = names.length;
  while (++i < n)
    list.add(names[i]);
}
function classedRemove(node2, names) {
  var list = classList(node2), i = -1, n = names.length;
  while (++i < n)
    list.remove(names[i]);
}
function classedTrue(names) {
  return function() {
    classedAdd(this, names);
  };
}
function classedFalse(names) {
  return function() {
    classedRemove(this, names);
  };
}
function classedFunction(names, value) {
  return function() {
    (value.apply(this, arguments) ? classedAdd : classedRemove)(this, names);
  };
}
function selection_classed(name, value) {
  var names = classArray(name + "");
  if (arguments.length < 2) {
    var list = classList(this.node()), i = -1, n = names.length;
    while (++i < n)
      if (!list.contains(names[i]))
        return false;
    return true;
  }
  return this.each((typeof value === "function" ? classedFunction : value ? classedTrue : classedFalse)(names, value));
}
function textRemove() {
  this.textContent = "";
}
function textConstant$1(value) {
  return function() {
    this.textContent = value;
  };
}
function textFunction$1(value) {
  return function() {
    var v = value.apply(this, arguments);
    this.textContent = v == null ? "" : v;
  };
}
function selection_text(value) {
  return arguments.length ? this.each(value == null ? textRemove : (typeof value === "function" ? textFunction$1 : textConstant$1)(value)) : this.node().textContent;
}
function htmlRemove() {
  this.innerHTML = "";
}
function htmlConstant(value) {
  return function() {
    this.innerHTML = value;
  };
}
function htmlFunction(value) {
  return function() {
    var v = value.apply(this, arguments);
    this.innerHTML = v == null ? "" : v;
  };
}
function selection_html(value) {
  return arguments.length ? this.each(value == null ? htmlRemove : (typeof value === "function" ? htmlFunction : htmlConstant)(value)) : this.node().innerHTML;
}
function raise() {
  if (this.nextSibling)
    this.parentNode.appendChild(this);
}
function selection_raise() {
  return this.each(raise);
}
function lower() {
  if (this.previousSibling)
    this.parentNode.insertBefore(this, this.parentNode.firstChild);
}
function selection_lower() {
  return this.each(lower);
}
function selection_append(name) {
  var create2 = typeof name === "function" ? name : creator(name);
  return this.select(function() {
    return this.appendChild(create2.apply(this, arguments));
  });
}
function constantNull() {
  return null;
}
function selection_insert(name, before) {
  var create2 = typeof name === "function" ? name : creator(name), select = before == null ? constantNull : typeof before === "function" ? before : selector(before);
  return this.select(function() {
    return this.insertBefore(create2.apply(this, arguments), select.apply(this, arguments) || null);
  });
}
function remove() {
  var parent = this.parentNode;
  if (parent)
    parent.removeChild(this);
}
function selection_remove() {
  return this.each(remove);
}
function selection_cloneShallow() {
  var clone2 = this.cloneNode(false), parent = this.parentNode;
  return parent ? parent.insertBefore(clone2, this.nextSibling) : clone2;
}
function selection_cloneDeep() {
  var clone2 = this.cloneNode(true), parent = this.parentNode;
  return parent ? parent.insertBefore(clone2, this.nextSibling) : clone2;
}
function selection_clone(deep) {
  return this.select(deep ? selection_cloneDeep : selection_cloneShallow);
}
function selection_datum(value) {
  return arguments.length ? this.property("__data__", value) : this.node().__data__;
}
function contextListener(listener) {
  return function(event) {
    listener.call(this, event, this.__data__);
  };
}
function parseTypenames(typenames) {
  return typenames.trim().split(/^|\s+/).map(function(t) {
    var name = "", i = t.indexOf(".");
    if (i >= 0)
      name = t.slice(i + 1), t = t.slice(0, i);
    return { type: t, name };
  });
}
function onRemove(typename) {
  return function() {
    var on = this.__on;
    if (!on)
      return;
    for (var j = 0, i = -1, m = on.length, o; j < m; ++j) {
      if (o = on[j], (!typename.type || o.type === typename.type) && o.name === typename.name) {
        this.removeEventListener(o.type, o.listener, o.options);
      } else {
        on[++i] = o;
      }
    }
    if (++i)
      on.length = i;
    else
      delete this.__on;
  };
}
function onAdd(typename, value, options) {
  return function() {
    var on = this.__on, o, listener = contextListener(value);
    if (on)
      for (var j = 0, m = on.length; j < m; ++j) {
        if ((o = on[j]).type === typename.type && o.name === typename.name) {
          this.removeEventListener(o.type, o.listener, o.options);
          this.addEventListener(o.type, o.listener = listener, o.options = options);
          o.value = value;
          return;
        }
      }
    this.addEventListener(typename.type, listener, options);
    o = { type: typename.type, name: typename.name, value, listener, options };
    if (!on)
      this.__on = [o];
    else
      on.push(o);
  };
}
function selection_on(typename, value, options) {
  var typenames = parseTypenames(typename + ""), i, n = typenames.length, t;
  if (arguments.length < 2) {
    var on = this.node().__on;
    if (on)
      for (var j = 0, m = on.length, o; j < m; ++j) {
        for (i = 0, o = on[j]; i < n; ++i) {
          if ((t = typenames[i]).type === o.type && t.name === o.name) {
            return o.value;
          }
        }
      }
    return;
  }
  on = value ? onAdd : onRemove;
  for (i = 0; i < n; ++i)
    this.each(on(typenames[i], value, options));
  return this;
}
function dispatchEvent(node2, type2, params) {
  var window2 = defaultView(node2), event = window2.CustomEvent;
  if (typeof event === "function") {
    event = new event(type2, params);
  } else {
    event = window2.document.createEvent("Event");
    if (params)
      event.initEvent(type2, params.bubbles, params.cancelable), event.detail = params.detail;
    else
      event.initEvent(type2, false, false);
  }
  node2.dispatchEvent(event);
}
function dispatchConstant(type2, params) {
  return function() {
    return dispatchEvent(this, type2, params);
  };
}
function dispatchFunction(type2, params) {
  return function() {
    return dispatchEvent(this, type2, params.apply(this, arguments));
  };
}
function selection_dispatch(type2, params) {
  return this.each((typeof params === "function" ? dispatchFunction : dispatchConstant)(type2, params));
}
function* selection_iterator() {
  for (var groups = this._groups, j = 0, m = groups.length; j < m; ++j) {
    for (var group = groups[j], i = 0, n = group.length, node2; i < n; ++i) {
      if (node2 = group[i])
        yield node2;
    }
  }
}
var root$2 = [null];
function Selection$1(groups, parents) {
  this._groups = groups;
  this._parents = parents;
}
function selection() {
  return new Selection$1([[document.documentElement]], root$2);
}
function selection_selection() {
  return this;
}
Selection$1.prototype = selection.prototype = {
  constructor: Selection$1,
  select: selection_select,
  selectAll: selection_selectAll,
  selectChild: selection_selectChild,
  selectChildren: selection_selectChildren,
  filter: selection_filter,
  data: selection_data,
  enter: selection_enter,
  exit: selection_exit,
  join: selection_join,
  merge: selection_merge,
  selection: selection_selection,
  order: selection_order,
  sort: selection_sort,
  call: selection_call,
  nodes: selection_nodes,
  node: selection_node,
  size: selection_size,
  empty: selection_empty,
  each: selection_each,
  attr: selection_attr,
  style: selection_style,
  property: selection_property,
  classed: selection_classed,
  text: selection_text,
  html: selection_html,
  raise: selection_raise,
  lower: selection_lower,
  append: selection_append,
  insert: selection_insert,
  remove: selection_remove,
  clone: selection_clone,
  datum: selection_datum,
  on: selection_on,
  dispatch: selection_dispatch,
  [Symbol.iterator]: selection_iterator
};
function d3select(selector2) {
  return typeof selector2 === "string" ? new Selection$1([[document.querySelector(selector2)]], [document.documentElement]) : new Selection$1([[selector2]], root$2);
}
function define(constructor, factory, prototype) {
  constructor.prototype = factory.prototype = prototype;
  prototype.constructor = constructor;
}
function extend$1(parent, definition) {
  var prototype = Object.create(parent.prototype);
  for (var key in definition)
    prototype[key] = definition[key];
  return prototype;
}
function Color$2() {
}
var darker = 0.7;
var brighter = 1 / darker;
var reI = "\\s*([+-]?\\d+)\\s*", reN = "\\s*([+-]?(?:\\d*\\.)?\\d+(?:[eE][+-]?\\d+)?)\\s*", reP = "\\s*([+-]?(?:\\d*\\.)?\\d+(?:[eE][+-]?\\d+)?)%\\s*", reHex = /^#([0-9a-f]{3,8})$/, reRgbInteger = new RegExp(`^rgb\\(${reI},${reI},${reI}\\)$`), reRgbPercent = new RegExp(`^rgb\\(${reP},${reP},${reP}\\)$`), reRgbaInteger = new RegExp(`^rgba\\(${reI},${reI},${reI},${reN}\\)$`), reRgbaPercent = new RegExp(`^rgba\\(${reP},${reP},${reP},${reN}\\)$`), reHslPercent = new RegExp(`^hsl\\(${reN},${reP},${reP}\\)$`), reHslaPercent = new RegExp(`^hsla\\(${reN},${reP},${reP},${reN}\\)$`);
var named = {
  aliceblue: 15792383,
  antiquewhite: 16444375,
  aqua: 65535,
  aquamarine: 8388564,
  azure: 15794175,
  beige: 16119260,
  bisque: 16770244,
  black: 0,
  blanchedalmond: 16772045,
  blue: 255,
  blueviolet: 9055202,
  brown: 10824234,
  burlywood: 14596231,
  cadetblue: 6266528,
  chartreuse: 8388352,
  chocolate: 13789470,
  coral: 16744272,
  cornflowerblue: 6591981,
  cornsilk: 16775388,
  crimson: 14423100,
  cyan: 65535,
  darkblue: 139,
  darkcyan: 35723,
  darkgoldenrod: 12092939,
  darkgray: 11119017,
  darkgreen: 25600,
  darkgrey: 11119017,
  darkkhaki: 12433259,
  darkmagenta: 9109643,
  darkolivegreen: 5597999,
  darkorange: 16747520,
  darkorchid: 10040012,
  darkred: 9109504,
  darksalmon: 15308410,
  darkseagreen: 9419919,
  darkslateblue: 4734347,
  darkslategray: 3100495,
  darkslategrey: 3100495,
  darkturquoise: 52945,
  darkviolet: 9699539,
  deeppink: 16716947,
  deepskyblue: 49151,
  dimgray: 6908265,
  dimgrey: 6908265,
  dodgerblue: 2003199,
  firebrick: 11674146,
  floralwhite: 16775920,
  forestgreen: 2263842,
  fuchsia: 16711935,
  gainsboro: 14474460,
  ghostwhite: 16316671,
  gold: 16766720,
  goldenrod: 14329120,
  gray: 8421504,
  green: 32768,
  greenyellow: 11403055,
  grey: 8421504,
  honeydew: 15794160,
  hotpink: 16738740,
  indianred: 13458524,
  indigo: 4915330,
  ivory: 16777200,
  khaki: 15787660,
  lavender: 15132410,
  lavenderblush: 16773365,
  lawngreen: 8190976,
  lemonchiffon: 16775885,
  lightblue: 11393254,
  lightcoral: 15761536,
  lightcyan: 14745599,
  lightgoldenrodyellow: 16448210,
  lightgray: 13882323,
  lightgreen: 9498256,
  lightgrey: 13882323,
  lightpink: 16758465,
  lightsalmon: 16752762,
  lightseagreen: 2142890,
  lightskyblue: 8900346,
  lightslategray: 7833753,
  lightslategrey: 7833753,
  lightsteelblue: 11584734,
  lightyellow: 16777184,
  lime: 65280,
  limegreen: 3329330,
  linen: 16445670,
  magenta: 16711935,
  maroon: 8388608,
  mediumaquamarine: 6737322,
  mediumblue: 205,
  mediumorchid: 12211667,
  mediumpurple: 9662683,
  mediumseagreen: 3978097,
  mediumslateblue: 8087790,
  mediumspringgreen: 64154,
  mediumturquoise: 4772300,
  mediumvioletred: 13047173,
  midnightblue: 1644912,
  mintcream: 16121850,
  mistyrose: 16770273,
  moccasin: 16770229,
  navajowhite: 16768685,
  navy: 128,
  oldlace: 16643558,
  olive: 8421376,
  olivedrab: 7048739,
  orange: 16753920,
  orangered: 16729344,
  orchid: 14315734,
  palegoldenrod: 15657130,
  palegreen: 10025880,
  paleturquoise: 11529966,
  palevioletred: 14381203,
  papayawhip: 16773077,
  peachpuff: 16767673,
  peru: 13468991,
  pink: 16761035,
  plum: 14524637,
  powderblue: 11591910,
  purple: 8388736,
  rebeccapurple: 6697881,
  red: 16711680,
  rosybrown: 12357519,
  royalblue: 4286945,
  saddlebrown: 9127187,
  salmon: 16416882,
  sandybrown: 16032864,
  seagreen: 3050327,
  seashell: 16774638,
  sienna: 10506797,
  silver: 12632256,
  skyblue: 8900331,
  slateblue: 6970061,
  slategray: 7372944,
  slategrey: 7372944,
  snow: 16775930,
  springgreen: 65407,
  steelblue: 4620980,
  tan: 13808780,
  teal: 32896,
  thistle: 14204888,
  tomato: 16737095,
  turquoise: 4251856,
  violet: 15631086,
  wheat: 16113331,
  white: 16777215,
  whitesmoke: 16119285,
  yellow: 16776960,
  yellowgreen: 10145074
};
define(Color$2, color, {
  copy(channels2) {
    return Object.assign(new this.constructor(), this, channels2);
  },
  displayable() {
    return this.rgb().displayable();
  },
  hex: color_formatHex,
  // Deprecated! Use color.formatHex.
  formatHex: color_formatHex,
  formatHex8: color_formatHex8,
  formatHsl: color_formatHsl,
  formatRgb: color_formatRgb,
  toString: color_formatRgb
});
function color_formatHex() {
  return this.rgb().formatHex();
}
function color_formatHex8() {
  return this.rgb().formatHex8();
}
function color_formatHsl() {
  return hslConvert(this).formatHsl();
}
function color_formatRgb() {
  return this.rgb().formatRgb();
}
function color(format2) {
  var m, l;
  format2 = (format2 + "").trim().toLowerCase();
  return (m = reHex.exec(format2)) ? (l = m[1].length, m = parseInt(m[1], 16), l === 6 ? rgbn(m) : l === 3 ? new Rgb(m >> 8 & 15 | m >> 4 & 240, m >> 4 & 15 | m & 240, (m & 15) << 4 | m & 15, 1) : l === 8 ? rgba$2(m >> 24 & 255, m >> 16 & 255, m >> 8 & 255, (m & 255) / 255) : l === 4 ? rgba$2(m >> 12 & 15 | m >> 8 & 240, m >> 8 & 15 | m >> 4 & 240, m >> 4 & 15 | m & 240, ((m & 15) << 4 | m & 15) / 255) : null) : (m = reRgbInteger.exec(format2)) ? new Rgb(m[1], m[2], m[3], 1) : (m = reRgbPercent.exec(format2)) ? new Rgb(m[1] * 255 / 100, m[2] * 255 / 100, m[3] * 255 / 100, 1) : (m = reRgbaInteger.exec(format2)) ? rgba$2(m[1], m[2], m[3], m[4]) : (m = reRgbaPercent.exec(format2)) ? rgba$2(m[1] * 255 / 100, m[2] * 255 / 100, m[3] * 255 / 100, m[4]) : (m = reHslPercent.exec(format2)) ? hsla(m[1], m[2] / 100, m[3] / 100, 1) : (m = reHslaPercent.exec(format2)) ? hsla(m[1], m[2] / 100, m[3] / 100, m[4]) : named.hasOwnProperty(format2) ? rgbn(named[format2]) : format2 === "transparent" ? new Rgb(NaN, NaN, NaN, 0) : null;
}
function rgbn(n) {
  return new Rgb(n >> 16 & 255, n >> 8 & 255, n & 255, 1);
}
function rgba$2(r, g, b, a) {
  if (a <= 0)
    r = g = b = NaN;
  return new Rgb(r, g, b, a);
}
function rgbConvert(o) {
  if (!(o instanceof Color$2))
    o = color(o);
  if (!o)
    return new Rgb();
  o = o.rgb();
  return new Rgb(o.r, o.g, o.b, o.opacity);
}
function rgb(r, g, b, opacity) {
  return arguments.length === 1 ? rgbConvert(r) : new Rgb(r, g, b, opacity == null ? 1 : opacity);
}
function Rgb(r, g, b, opacity) {
  this.r = +r;
  this.g = +g;
  this.b = +b;
  this.opacity = +opacity;
}
define(Rgb, rgb, extend$1(Color$2, {
  brighter(k) {
    k = k == null ? brighter : Math.pow(brighter, k);
    return new Rgb(this.r * k, this.g * k, this.b * k, this.opacity);
  },
  darker(k) {
    k = k == null ? darker : Math.pow(darker, k);
    return new Rgb(this.r * k, this.g * k, this.b * k, this.opacity);
  },
  rgb() {
    return this;
  },
  clamp() {
    return new Rgb(clampi(this.r), clampi(this.g), clampi(this.b), clampa(this.opacity));
  },
  displayable() {
    return -0.5 <= this.r && this.r < 255.5 && (-0.5 <= this.g && this.g < 255.5) && (-0.5 <= this.b && this.b < 255.5) && (0 <= this.opacity && this.opacity <= 1);
  },
  hex: rgb_formatHex,
  // Deprecated! Use color.formatHex.
  formatHex: rgb_formatHex,
  formatHex8: rgb_formatHex8,
  formatRgb: rgb_formatRgb,
  toString: rgb_formatRgb
}));
function rgb_formatHex() {
  return `#${hex(this.r)}${hex(this.g)}${hex(this.b)}`;
}
function rgb_formatHex8() {
  return `#${hex(this.r)}${hex(this.g)}${hex(this.b)}${hex((isNaN(this.opacity) ? 1 : this.opacity) * 255)}`;
}
function rgb_formatRgb() {
  const a = clampa(this.opacity);
  return `${a === 1 ? "rgb(" : "rgba("}${clampi(this.r)}, ${clampi(this.g)}, ${clampi(this.b)}${a === 1 ? ")" : `, ${a})`}`;
}
function clampa(opacity) {
  return isNaN(opacity) ? 1 : Math.max(0, Math.min(1, opacity));
}
function clampi(value) {
  return Math.max(0, Math.min(255, Math.round(value) || 0));
}
function hex(value) {
  value = clampi(value);
  return (value < 16 ? "0" : "") + value.toString(16);
}
function hsla(h, s, l, a) {
  if (a <= 0)
    h = s = l = NaN;
  else if (l <= 0 || l >= 1)
    h = s = NaN;
  else if (s <= 0)
    h = NaN;
  return new Hsl(h, s, l, a);
}
function hslConvert(o) {
  if (o instanceof Hsl)
    return new Hsl(o.h, o.s, o.l, o.opacity);
  if (!(o instanceof Color$2))
    o = color(o);
  if (!o)
    return new Hsl();
  if (o instanceof Hsl)
    return o;
  o = o.rgb();
  var r = o.r / 255, g = o.g / 255, b = o.b / 255, min2 = Math.min(r, g, b), max2 = Math.max(r, g, b), h = NaN, s = max2 - min2, l = (max2 + min2) / 2;
  if (s) {
    if (r === max2)
      h = (g - b) / s + (g < b) * 6;
    else if (g === max2)
      h = (b - r) / s + 2;
    else
      h = (r - g) / s + 4;
    s /= l < 0.5 ? max2 + min2 : 2 - max2 - min2;
    h *= 60;
  } else {
    s = l > 0 && l < 1 ? 0 : h;
  }
  return new Hsl(h, s, l, o.opacity);
}
function hsl(h, s, l, opacity) {
  return arguments.length === 1 ? hslConvert(h) : new Hsl(h, s, l, opacity == null ? 1 : opacity);
}
function Hsl(h, s, l, opacity) {
  this.h = +h;
  this.s = +s;
  this.l = +l;
  this.opacity = +opacity;
}
define(Hsl, hsl, extend$1(Color$2, {
  brighter(k) {
    k = k == null ? brighter : Math.pow(brighter, k);
    return new Hsl(this.h, this.s, this.l * k, this.opacity);
  },
  darker(k) {
    k = k == null ? darker : Math.pow(darker, k);
    return new Hsl(this.h, this.s, this.l * k, this.opacity);
  },
  rgb() {
    var h = this.h % 360 + (this.h < 0) * 360, s = isNaN(h) || isNaN(this.s) ? 0 : this.s, l = this.l, m2 = l + (l < 0.5 ? l : 1 - l) * s, m1 = 2 * l - m2;
    return new Rgb(
      hsl2rgb(h >= 240 ? h - 240 : h + 120, m1, m2),
      hsl2rgb(h, m1, m2),
      hsl2rgb(h < 120 ? h + 240 : h - 120, m1, m2),
      this.opacity
    );
  },
  clamp() {
    return new Hsl(clamph(this.h), clampt(this.s), clampt(this.l), clampa(this.opacity));
  },
  displayable() {
    return (0 <= this.s && this.s <= 1 || isNaN(this.s)) && (0 <= this.l && this.l <= 1) && (0 <= this.opacity && this.opacity <= 1);
  },
  formatHsl() {
    const a = clampa(this.opacity);
    return `${a === 1 ? "hsl(" : "hsla("}${clamph(this.h)}, ${clampt(this.s) * 100}%, ${clampt(this.l) * 100}%${a === 1 ? ")" : `, ${a})`}`;
  }
}));
function clamph(value) {
  value = (value || 0) % 360;
  return value < 0 ? value + 360 : value;
}
function clampt(value) {
  return Math.max(0, Math.min(1, value || 0));
}
function hsl2rgb(h, m1, m2) {
  return (h < 60 ? m1 + (m2 - m1) * h / 60 : h < 180 ? m2 : h < 240 ? m1 + (m2 - m1) * (240 - h) / 60 : m1) * 255;
}
const constant$1 = (x) => () => x;
function linear(a, d) {
  return function(t) {
    return a + t * d;
  };
}
function exponential(a, b, y) {
  return a = Math.pow(a, y), b = Math.pow(b, y) - a, y = 1 / y, function(t) {
    return Math.pow(a + t * b, y);
  };
}
function hue(a, b) {
  var d = b - a;
  return d ? linear(a, d > 180 || d < -180 ? d - 360 * Math.round(d / 360) : d) : constant$1(isNaN(a) ? b : a);
}
function gamma(y) {
  return (y = +y) === 1 ? nogamma : function(a, b) {
    return b - a ? exponential(a, b, y) : constant$1(isNaN(a) ? b : a);
  };
}
function nogamma(a, b) {
  var d = b - a;
  return d ? linear(a, d) : constant$1(isNaN(a) ? b : a);
}
const interpolateRgb = function rgbGamma(y) {
  var color2 = gamma(y);
  function rgb$1(start2, end) {
    var r = color2((start2 = rgb(start2)).r, (end = rgb(end)).r), g = color2(start2.g, end.g), b = color2(start2.b, end.b), opacity = nogamma(start2.opacity, end.opacity);
    return function(t) {
      start2.r = r(t);
      start2.g = g(t);
      start2.b = b(t);
      start2.opacity = opacity(t);
      return start2 + "";
    };
  }
  rgb$1.gamma = rgbGamma;
  return rgb$1;
}(1);
function interpolateNumber(a, b) {
  return a = +a, b = +b, function(t) {
    return a * (1 - t) + b * t;
  };
}
var reA = /[-+]?(?:\d+\.?\d*|\.?\d+)(?:[eE][-+]?\d+)?/g, reB = new RegExp(reA.source, "g");
function zero(b) {
  return function() {
    return b;
  };
}
function one(b) {
  return function(t) {
    return b(t) + "";
  };
}
function interpolateString(a, b) {
  var bi = reA.lastIndex = reB.lastIndex = 0, am, bm, bs, i = -1, s = [], q = [];
  a = a + "", b = b + "";
  while ((am = reA.exec(a)) && (bm = reB.exec(b))) {
    if ((bs = bm.index) > bi) {
      bs = b.slice(bi, bs);
      if (s[i])
        s[i] += bs;
      else
        s[++i] = bs;
    }
    if ((am = am[0]) === (bm = bm[0])) {
      if (s[i])
        s[i] += bm;
      else
        s[++i] = bm;
    } else {
      s[++i] = null;
      q.push({ i, x: interpolateNumber(am, bm) });
    }
    bi = reB.lastIndex;
  }
  if (bi < b.length) {
    bs = b.slice(bi);
    if (s[i])
      s[i] += bs;
    else
      s[++i] = bs;
  }
  return s.length < 2 ? q[0] ? one(q[0].x) : zero(b) : (b = q.length, function(t) {
    for (var i2 = 0, o; i2 < b; ++i2)
      s[(o = q[i2]).i] = o.x(t);
    return s.join("");
  });
}
var degrees = 180 / Math.PI;
var identity$1 = {
  translateX: 0,
  translateY: 0,
  rotate: 0,
  skewX: 0,
  scaleX: 1,
  scaleY: 1
};
function decompose(a, b, c, d, e, f) {
  var scaleX, scaleY, skewX;
  if (scaleX = Math.sqrt(a * a + b * b))
    a /= scaleX, b /= scaleX;
  if (skewX = a * c + b * d)
    c -= a * skewX, d -= b * skewX;
  if (scaleY = Math.sqrt(c * c + d * d))
    c /= scaleY, d /= scaleY, skewX /= scaleY;
  if (a * d < b * c)
    a = -a, b = -b, skewX = -skewX, scaleX = -scaleX;
  return {
    translateX: e,
    translateY: f,
    rotate: Math.atan2(b, a) * degrees,
    skewX: Math.atan(skewX) * degrees,
    scaleX,
    scaleY
  };
}
var svgNode;
function parseCss(value) {
  const m = new (typeof DOMMatrix === "function" ? DOMMatrix : WebKitCSSMatrix)(value + "");
  return m.isIdentity ? identity$1 : decompose(m.a, m.b, m.c, m.d, m.e, m.f);
}
function parseSvg(value) {
  if (value == null)
    return identity$1;
  if (!svgNode)
    svgNode = document.createElementNS("http://www.w3.org/2000/svg", "g");
  svgNode.setAttribute("transform", value);
  if (!(value = svgNode.transform.baseVal.consolidate()))
    return identity$1;
  value = value.matrix;
  return decompose(value.a, value.b, value.c, value.d, value.e, value.f);
}
function interpolateTransform(parse2, pxComma, pxParen, degParen) {
  function pop(s) {
    return s.length ? s.pop() + " " : "";
  }
  function translate(xa, ya, xb, yb, s, q) {
    if (xa !== xb || ya !== yb) {
      var i = s.push("translate(", null, pxComma, null, pxParen);
      q.push({ i: i - 4, x: interpolateNumber(xa, xb) }, { i: i - 2, x: interpolateNumber(ya, yb) });
    } else if (xb || yb) {
      s.push("translate(" + xb + pxComma + yb + pxParen);
    }
  }
  function rotate(a, b, s, q) {
    if (a !== b) {
      if (a - b > 180)
        b += 360;
      else if (b - a > 180)
        a += 360;
      q.push({ i: s.push(pop(s) + "rotate(", null, degParen) - 2, x: interpolateNumber(a, b) });
    } else if (b) {
      s.push(pop(s) + "rotate(" + b + degParen);
    }
  }
  function skewX(a, b, s, q) {
    if (a !== b) {
      q.push({ i: s.push(pop(s) + "skewX(", null, degParen) - 2, x: interpolateNumber(a, b) });
    } else if (b) {
      s.push(pop(s) + "skewX(" + b + degParen);
    }
  }
  function scale(xa, ya, xb, yb, s, q) {
    if (xa !== xb || ya !== yb) {
      var i = s.push(pop(s) + "scale(", null, ",", null, ")");
      q.push({ i: i - 4, x: interpolateNumber(xa, xb) }, { i: i - 2, x: interpolateNumber(ya, yb) });
    } else if (xb !== 1 || yb !== 1) {
      s.push(pop(s) + "scale(" + xb + "," + yb + ")");
    }
  }
  return function(a, b) {
    var s = [], q = [];
    a = parse2(a), b = parse2(b);
    translate(a.translateX, a.translateY, b.translateX, b.translateY, s, q);
    rotate(a.rotate, b.rotate, s, q);
    skewX(a.skewX, b.skewX, s, q);
    scale(a.scaleX, a.scaleY, b.scaleX, b.scaleY, s, q);
    a = b = null;
    return function(t) {
      var i = -1, n = q.length, o;
      while (++i < n)
        s[(o = q[i]).i] = o.x(t);
      return s.join("");
    };
  };
}
var interpolateTransformCss = interpolateTransform(parseCss, "px, ", "px)", "deg)");
var interpolateTransformSvg = interpolateTransform(parseSvg, ", ", ")", ")");
var frame = 0, timeout$1 = 0, interval = 0, pokeDelay = 1e3, taskHead, taskTail, clockLast = 0, clockNow = 0, clockSkew = 0, clock = typeof performance === "object" && performance.now ? performance : Date, setFrame = typeof window === "object" && window.requestAnimationFrame ? window.requestAnimationFrame.bind(window) : function(f) {
  setTimeout(f, 17);
};
function now() {
  return clockNow || (setFrame(clearNow), clockNow = clock.now() + clockSkew);
}
function clearNow() {
  clockNow = 0;
}
function Timer() {
  this._call = this._time = this._next = null;
}
Timer.prototype = timer.prototype = {
  constructor: Timer,
  restart: function(callback, delay, time) {
    if (typeof callback !== "function")
      throw new TypeError("callback is not a function");
    time = (time == null ? now() : +time) + (delay == null ? 0 : +delay);
    if (!this._next && taskTail !== this) {
      if (taskTail)
        taskTail._next = this;
      else
        taskHead = this;
      taskTail = this;
    }
    this._call = callback;
    this._time = time;
    sleep();
  },
  stop: function() {
    if (this._call) {
      this._call = null;
      this._time = Infinity;
      sleep();
    }
  }
};
function timer(callback, delay, time) {
  var t = new Timer();
  t.restart(callback, delay, time);
  return t;
}
function timerFlush() {
  now();
  ++frame;
  var t = taskHead, e;
  while (t) {
    if ((e = clockNow - t._time) >= 0)
      t._call.call(void 0, e);
    t = t._next;
  }
  --frame;
}
function wake() {
  clockNow = (clockLast = clock.now()) + clockSkew;
  frame = timeout$1 = 0;
  try {
    timerFlush();
  } finally {
    frame = 0;
    nap();
    clockNow = 0;
  }
}
function poke() {
  var now2 = clock.now(), delay = now2 - clockLast;
  if (delay > pokeDelay)
    clockSkew -= delay, clockLast = now2;
}
function nap() {
  var t0, t1 = taskHead, t2, time = Infinity;
  while (t1) {
    if (t1._call) {
      if (time > t1._time)
        time = t1._time;
      t0 = t1, t1 = t1._next;
    } else {
      t2 = t1._next, t1._next = null;
      t1 = t0 ? t0._next = t2 : taskHead = t2;
    }
  }
  taskTail = t0;
  sleep(time);
}
function sleep(time) {
  if (frame)
    return;
  if (timeout$1)
    timeout$1 = clearTimeout(timeout$1);
  var delay = time - clockNow;
  if (delay > 24) {
    if (time < Infinity)
      timeout$1 = setTimeout(wake, time - clock.now() - clockSkew);
    if (interval)
      interval = clearInterval(interval);
  } else {
    if (!interval)
      clockLast = clock.now(), interval = setInterval(poke, pokeDelay);
    frame = 1, setFrame(wake);
  }
}
function timeout(callback, delay, time) {
  var t = new Timer();
  delay = delay == null ? 0 : +delay;
  t.restart((elapsed) => {
    t.stop();
    callback(elapsed + delay);
  }, delay, time);
  return t;
}
var emptyOn = dispatch("start", "end", "cancel", "interrupt");
var emptyTween = [];
var CREATED = 0;
var SCHEDULED = 1;
var STARTING = 2;
var STARTED = 3;
var RUNNING = 4;
var ENDING = 5;
var ENDED = 6;
function schedule(node2, name, id2, index, group, timing) {
  var schedules = node2.__transition;
  if (!schedules)
    node2.__transition = {};
  else if (id2 in schedules)
    return;
  create$1(node2, id2, {
    name,
    index,
    // For context during callback.
    group,
    // For context during callback.
    on: emptyOn,
    tween: emptyTween,
    time: timing.time,
    delay: timing.delay,
    duration: timing.duration,
    ease: timing.ease,
    timer: null,
    state: CREATED
  });
}
function init$1(node2, id2) {
  var schedule2 = get(node2, id2);
  if (schedule2.state > CREATED)
    throw new Error("too late; already scheduled");
  return schedule2;
}
function set$1(node2, id2) {
  var schedule2 = get(node2, id2);
  if (schedule2.state > STARTED)
    throw new Error("too late; already running");
  return schedule2;
}
function get(node2, id2) {
  var schedule2 = node2.__transition;
  if (!schedule2 || !(schedule2 = schedule2[id2]))
    throw new Error("transition not found");
  return schedule2;
}
function create$1(node2, id2, self2) {
  var schedules = node2.__transition, tween;
  schedules[id2] = self2;
  self2.timer = timer(schedule2, 0, self2.time);
  function schedule2(elapsed) {
    self2.state = SCHEDULED;
    self2.timer.restart(start2, self2.delay, self2.time);
    if (self2.delay <= elapsed)
      start2(elapsed - self2.delay);
  }
  function start2(elapsed) {
    var i, j, n, o;
    if (self2.state !== SCHEDULED)
      return stop();
    for (i in schedules) {
      o = schedules[i];
      if (o.name !== self2.name)
        continue;
      if (o.state === STARTED)
        return timeout(start2);
      if (o.state === RUNNING) {
        o.state = ENDED;
        o.timer.stop();
        o.on.call("interrupt", node2, node2.__data__, o.index, o.group);
        delete schedules[i];
      } else if (+i < id2) {
        o.state = ENDED;
        o.timer.stop();
        o.on.call("cancel", node2, node2.__data__, o.index, o.group);
        delete schedules[i];
      }
    }
    timeout(function() {
      if (self2.state === STARTED) {
        self2.state = RUNNING;
        self2.timer.restart(tick, self2.delay, self2.time);
        tick(elapsed);
      }
    });
    self2.state = STARTING;
    self2.on.call("start", node2, node2.__data__, self2.index, self2.group);
    if (self2.state !== STARTING)
      return;
    self2.state = STARTED;
    tween = new Array(n = self2.tween.length);
    for (i = 0, j = -1; i < n; ++i) {
      if (o = self2.tween[i].value.call(node2, node2.__data__, self2.index, self2.group)) {
        tween[++j] = o;
      }
    }
    tween.length = j + 1;
  }
  function tick(elapsed) {
    var t = elapsed < self2.duration ? self2.ease.call(null, elapsed / self2.duration) : (self2.timer.restart(stop), self2.state = ENDING, 1), i = -1, n = tween.length;
    while (++i < n) {
      tween[i].call(node2, t);
    }
    if (self2.state === ENDING) {
      self2.on.call("end", node2, node2.__data__, self2.index, self2.group);
      stop();
    }
  }
  function stop() {
    self2.state = ENDED;
    self2.timer.stop();
    delete schedules[id2];
    for (var i in schedules)
      return;
    delete node2.__transition;
  }
}
function interrupt(node2, name) {
  var schedules = node2.__transition, schedule2, active, empty2 = true, i;
  if (!schedules)
    return;
  name = name == null ? null : name + "";
  for (i in schedules) {
    if ((schedule2 = schedules[i]).name !== name) {
      empty2 = false;
      continue;
    }
    active = schedule2.state > STARTING && schedule2.state < ENDING;
    schedule2.state = ENDED;
    schedule2.timer.stop();
    schedule2.on.call(active ? "interrupt" : "cancel", node2, node2.__data__, schedule2.index, schedule2.group);
    delete schedules[i];
  }
  if (empty2)
    delete node2.__transition;
}
function selection_interrupt(name) {
  return this.each(function() {
    interrupt(this, name);
  });
}
function tweenRemove(id2, name) {
  var tween0, tween1;
  return function() {
    var schedule2 = set$1(this, id2), tween = schedule2.tween;
    if (tween !== tween0) {
      tween1 = tween0 = tween;
      for (var i = 0, n = tween1.length; i < n; ++i) {
        if (tween1[i].name === name) {
          tween1 = tween1.slice();
          tween1.splice(i, 1);
          break;
        }
      }
    }
    schedule2.tween = tween1;
  };
}
function tweenFunction(id2, name, value) {
  var tween0, tween1;
  if (typeof value !== "function")
    throw new Error();
  return function() {
    var schedule2 = set$1(this, id2), tween = schedule2.tween;
    if (tween !== tween0) {
      tween1 = (tween0 = tween).slice();
      for (var t = { name, value }, i = 0, n = tween1.length; i < n; ++i) {
        if (tween1[i].name === name) {
          tween1[i] = t;
          break;
        }
      }
      if (i === n)
        tween1.push(t);
    }
    schedule2.tween = tween1;
  };
}
function transition_tween(name, value) {
  var id2 = this._id;
  name += "";
  if (arguments.length < 2) {
    var tween = get(this.node(), id2).tween;
    for (var i = 0, n = tween.length, t; i < n; ++i) {
      if ((t = tween[i]).name === name) {
        return t.value;
      }
    }
    return null;
  }
  return this.each((value == null ? tweenRemove : tweenFunction)(id2, name, value));
}
function tweenValue(transition, name, value) {
  var id2 = transition._id;
  transition.each(function() {
    var schedule2 = set$1(this, id2);
    (schedule2.value || (schedule2.value = {}))[name] = value.apply(this, arguments);
  });
  return function(node2) {
    return get(node2, id2).value[name];
  };
}
function interpolate(a, b) {
  var c;
  return (typeof b === "number" ? interpolateNumber : b instanceof color ? interpolateRgb : (c = color(b)) ? (b = c, interpolateRgb) : interpolateString)(a, b);
}
function attrRemove(name) {
  return function() {
    this.removeAttribute(name);
  };
}
function attrRemoveNS(fullname) {
  return function() {
    this.removeAttributeNS(fullname.space, fullname.local);
  };
}
function attrConstant(name, interpolate2, value1) {
  var string00, string1 = value1 + "", interpolate0;
  return function() {
    var string0 = this.getAttribute(name);
    return string0 === string1 ? null : string0 === string00 ? interpolate0 : interpolate0 = interpolate2(string00 = string0, value1);
  };
}
function attrConstantNS(fullname, interpolate2, value1) {
  var string00, string1 = value1 + "", interpolate0;
  return function() {
    var string0 = this.getAttributeNS(fullname.space, fullname.local);
    return string0 === string1 ? null : string0 === string00 ? interpolate0 : interpolate0 = interpolate2(string00 = string0, value1);
  };
}
function attrFunction(name, interpolate2, value) {
  var string00, string10, interpolate0;
  return function() {
    var string0, value1 = value(this), string1;
    if (value1 == null)
      return void this.removeAttribute(name);
    string0 = this.getAttribute(name);
    string1 = value1 + "";
    return string0 === string1 ? null : string0 === string00 && string1 === string10 ? interpolate0 : (string10 = string1, interpolate0 = interpolate2(string00 = string0, value1));
  };
}
function attrFunctionNS(fullname, interpolate2, value) {
  var string00, string10, interpolate0;
  return function() {
    var string0, value1 = value(this), string1;
    if (value1 == null)
      return void this.removeAttributeNS(fullname.space, fullname.local);
    string0 = this.getAttributeNS(fullname.space, fullname.local);
    string1 = value1 + "";
    return string0 === string1 ? null : string0 === string00 && string1 === string10 ? interpolate0 : (string10 = string1, interpolate0 = interpolate2(string00 = string0, value1));
  };
}
function transition_attr(name, value) {
  var fullname = namespace(name), i = fullname === "transform" ? interpolateTransformSvg : interpolate;
  return this.attrTween(name, typeof value === "function" ? (fullname.local ? attrFunctionNS : attrFunction)(fullname, i, tweenValue(this, "attr." + name, value)) : value == null ? (fullname.local ? attrRemoveNS : attrRemove)(fullname) : (fullname.local ? attrConstantNS : attrConstant)(fullname, i, value));
}
function attrInterpolate(name, i) {
  return function(t) {
    this.setAttribute(name, i.call(this, t));
  };
}
function attrInterpolateNS(fullname, i) {
  return function(t) {
    this.setAttributeNS(fullname.space, fullname.local, i.call(this, t));
  };
}
function attrTweenNS(fullname, value) {
  var t0, i0;
  function tween() {
    var i = value.apply(this, arguments);
    if (i !== i0)
      t0 = (i0 = i) && attrInterpolateNS(fullname, i);
    return t0;
  }
  tween._value = value;
  return tween;
}
function attrTween(name, value) {
  var t0, i0;
  function tween() {
    var i = value.apply(this, arguments);
    if (i !== i0)
      t0 = (i0 = i) && attrInterpolate(name, i);
    return t0;
  }
  tween._value = value;
  return tween;
}
function transition_attrTween(name, value) {
  var key = "attr." + name;
  if (arguments.length < 2)
    return (key = this.tween(key)) && key._value;
  if (value == null)
    return this.tween(key, null);
  if (typeof value !== "function")
    throw new Error();
  var fullname = namespace(name);
  return this.tween(key, (fullname.local ? attrTweenNS : attrTween)(fullname, value));
}
function delayFunction(id2, value) {
  return function() {
    init$1(this, id2).delay = +value.apply(this, arguments);
  };
}
function delayConstant(id2, value) {
  return value = +value, function() {
    init$1(this, id2).delay = value;
  };
}
function transition_delay(value) {
  var id2 = this._id;
  return arguments.length ? this.each((typeof value === "function" ? delayFunction : delayConstant)(id2, value)) : get(this.node(), id2).delay;
}
function durationFunction(id2, value) {
  return function() {
    set$1(this, id2).duration = +value.apply(this, arguments);
  };
}
function durationConstant(id2, value) {
  return value = +value, function() {
    set$1(this, id2).duration = value;
  };
}
function transition_duration(value) {
  var id2 = this._id;
  return arguments.length ? this.each((typeof value === "function" ? durationFunction : durationConstant)(id2, value)) : get(this.node(), id2).duration;
}
function easeConstant(id2, value) {
  if (typeof value !== "function")
    throw new Error();
  return function() {
    set$1(this, id2).ease = value;
  };
}
function transition_ease(value) {
  var id2 = this._id;
  return arguments.length ? this.each(easeConstant(id2, value)) : get(this.node(), id2).ease;
}
function easeVarying(id2, value) {
  return function() {
    var v = value.apply(this, arguments);
    if (typeof v !== "function")
      throw new Error();
    set$1(this, id2).ease = v;
  };
}
function transition_easeVarying(value) {
  if (typeof value !== "function")
    throw new Error();
  return this.each(easeVarying(this._id, value));
}
function transition_filter(match) {
  if (typeof match !== "function")
    match = matcher(match);
  for (var groups = this._groups, m = groups.length, subgroups = new Array(m), j = 0; j < m; ++j) {
    for (var group = groups[j], n = group.length, subgroup = subgroups[j] = [], node2, i = 0; i < n; ++i) {
      if ((node2 = group[i]) && match.call(node2, node2.__data__, i, group)) {
        subgroup.push(node2);
      }
    }
  }
  return new Transition(subgroups, this._parents, this._name, this._id);
}
function transition_merge(transition) {
  if (transition._id !== this._id)
    throw new Error();
  for (var groups0 = this._groups, groups1 = transition._groups, m0 = groups0.length, m1 = groups1.length, m = Math.min(m0, m1), merges = new Array(m0), j = 0; j < m; ++j) {
    for (var group0 = groups0[j], group1 = groups1[j], n = group0.length, merge2 = merges[j] = new Array(n), node2, i = 0; i < n; ++i) {
      if (node2 = group0[i] || group1[i]) {
        merge2[i] = node2;
      }
    }
  }
  for (; j < m0; ++j) {
    merges[j] = groups0[j];
  }
  return new Transition(merges, this._parents, this._name, this._id);
}
function start(name) {
  return (name + "").trim().split(/^|\s+/).every(function(t) {
    var i = t.indexOf(".");
    if (i >= 0)
      t = t.slice(0, i);
    return !t || t === "start";
  });
}
function onFunction(id2, name, listener) {
  var on0, on1, sit = start(name) ? init$1 : set$1;
  return function() {
    var schedule2 = sit(this, id2), on = schedule2.on;
    if (on !== on0)
      (on1 = (on0 = on).copy()).on(name, listener);
    schedule2.on = on1;
  };
}
function transition_on(name, listener) {
  var id2 = this._id;
  return arguments.length < 2 ? get(this.node(), id2).on.on(name) : this.each(onFunction(id2, name, listener));
}
function removeFunction(id2) {
  return function() {
    var parent = this.parentNode;
    for (var i in this.__transition)
      if (+i !== id2)
        return;
    if (parent)
      parent.removeChild(this);
  };
}
function transition_remove() {
  return this.on("end.remove", removeFunction(this._id));
}
function transition_select(select) {
  var name = this._name, id2 = this._id;
  if (typeof select !== "function")
    select = selector(select);
  for (var groups = this._groups, m = groups.length, subgroups = new Array(m), j = 0; j < m; ++j) {
    for (var group = groups[j], n = group.length, subgroup = subgroups[j] = new Array(n), node2, subnode, i = 0; i < n; ++i) {
      if ((node2 = group[i]) && (subnode = select.call(node2, node2.__data__, i, group))) {
        if ("__data__" in node2)
          subnode.__data__ = node2.__data__;
        subgroup[i] = subnode;
        schedule(subgroup[i], name, id2, i, subgroup, get(node2, id2));
      }
    }
  }
  return new Transition(subgroups, this._parents, name, id2);
}
function transition_selectAll(select) {
  var name = this._name, id2 = this._id;
  if (typeof select !== "function")
    select = selectorAll(select);
  for (var groups = this._groups, m = groups.length, subgroups = [], parents = [], j = 0; j < m; ++j) {
    for (var group = groups[j], n = group.length, node2, i = 0; i < n; ++i) {
      if (node2 = group[i]) {
        for (var children2 = select.call(node2, node2.__data__, i, group), child, inherit2 = get(node2, id2), k = 0, l = children2.length; k < l; ++k) {
          if (child = children2[k]) {
            schedule(child, name, id2, k, children2, inherit2);
          }
        }
        subgroups.push(children2);
        parents.push(node2);
      }
    }
  }
  return new Transition(subgroups, parents, name, id2);
}
var Selection = selection.prototype.constructor;
function transition_selection() {
  return new Selection(this._groups, this._parents);
}
function styleNull(name, interpolate2) {
  var string00, string10, interpolate0;
  return function() {
    var string0 = styleValue(this, name), string1 = (this.style.removeProperty(name), styleValue(this, name));
    return string0 === string1 ? null : string0 === string00 && string1 === string10 ? interpolate0 : interpolate0 = interpolate2(string00 = string0, string10 = string1);
  };
}
function styleRemove(name) {
  return function() {
    this.style.removeProperty(name);
  };
}
function styleConstant(name, interpolate2, value1) {
  var string00, string1 = value1 + "", interpolate0;
  return function() {
    var string0 = styleValue(this, name);
    return string0 === string1 ? null : string0 === string00 ? interpolate0 : interpolate0 = interpolate2(string00 = string0, value1);
  };
}
function styleFunction(name, interpolate2, value) {
  var string00, string10, interpolate0;
  return function() {
    var string0 = styleValue(this, name), value1 = value(this), string1 = value1 + "";
    if (value1 == null)
      string1 = value1 = (this.style.removeProperty(name), styleValue(this, name));
    return string0 === string1 ? null : string0 === string00 && string1 === string10 ? interpolate0 : (string10 = string1, interpolate0 = interpolate2(string00 = string0, value1));
  };
}
function styleMaybeRemove(id2, name) {
  var on0, on1, listener0, key = "style." + name, event = "end." + key, remove2;
  return function() {
    var schedule2 = set$1(this, id2), on = schedule2.on, listener = schedule2.value[key] == null ? remove2 || (remove2 = styleRemove(name)) : void 0;
    if (on !== on0 || listener0 !== listener)
      (on1 = (on0 = on).copy()).on(event, listener0 = listener);
    schedule2.on = on1;
  };
}
function transition_style(name, value, priority) {
  var i = (name += "") === "transform" ? interpolateTransformCss : interpolate;
  return value == null ? this.styleTween(name, styleNull(name, i)).on("end.style." + name, styleRemove(name)) : typeof value === "function" ? this.styleTween(name, styleFunction(name, i, tweenValue(this, "style." + name, value))).each(styleMaybeRemove(this._id, name)) : this.styleTween(name, styleConstant(name, i, value), priority).on("end.style." + name, null);
}
function styleInterpolate(name, i, priority) {
  return function(t) {
    this.style.setProperty(name, i.call(this, t), priority);
  };
}
function styleTween(name, value, priority) {
  var t, i0;
  function tween() {
    var i = value.apply(this, arguments);
    if (i !== i0)
      t = (i0 = i) && styleInterpolate(name, i, priority);
    return t;
  }
  tween._value = value;
  return tween;
}
function transition_styleTween(name, value, priority) {
  var key = "style." + (name += "");
  if (arguments.length < 2)
    return (key = this.tween(key)) && key._value;
  if (value == null)
    return this.tween(key, null);
  if (typeof value !== "function")
    throw new Error();
  return this.tween(key, styleTween(name, value, priority == null ? "" : priority));
}
function textConstant(value) {
  return function() {
    this.textContent = value;
  };
}
function textFunction(value) {
  return function() {
    var value1 = value(this);
    this.textContent = value1 == null ? "" : value1;
  };
}
function transition_text(value) {
  return this.tween("text", typeof value === "function" ? textFunction(tweenValue(this, "text", value)) : textConstant(value == null ? "" : value + ""));
}
function textInterpolate(i) {
  return function(t) {
    this.textContent = i.call(this, t);
  };
}
function textTween(value) {
  var t0, i0;
  function tween() {
    var i = value.apply(this, arguments);
    if (i !== i0)
      t0 = (i0 = i) && textInterpolate(i);
    return t0;
  }
  tween._value = value;
  return tween;
}
function transition_textTween(value) {
  var key = "text";
  if (arguments.length < 1)
    return (key = this.tween(key)) && key._value;
  if (value == null)
    return this.tween(key, null);
  if (typeof value !== "function")
    throw new Error();
  return this.tween(key, textTween(value));
}
function transition_transition() {
  var name = this._name, id0 = this._id, id1 = newId();
  for (var groups = this._groups, m = groups.length, j = 0; j < m; ++j) {
    for (var group = groups[j], n = group.length, node2, i = 0; i < n; ++i) {
      if (node2 = group[i]) {
        var inherit2 = get(node2, id0);
        schedule(node2, name, id1, i, group, {
          time: inherit2.time + inherit2.delay + inherit2.duration,
          delay: 0,
          duration: inherit2.duration,
          ease: inherit2.ease
        });
      }
    }
  }
  return new Transition(groups, this._parents, name, id1);
}
function transition_end() {
  var on0, on1, that = this, id2 = that._id, size = that.size();
  return new Promise(function(resolve, reject) {
    var cancel = { value: reject }, end = { value: function() {
      if (--size === 0)
        resolve();
    } };
    that.each(function() {
      var schedule2 = set$1(this, id2), on = schedule2.on;
      if (on !== on0) {
        on1 = (on0 = on).copy();
        on1._.cancel.push(cancel);
        on1._.interrupt.push(cancel);
        on1._.end.push(end);
      }
      schedule2.on = on1;
    });
    if (size === 0)
      resolve();
  });
}
var id$k = 0;
function Transition(groups, parents, name, id2) {
  this._groups = groups;
  this._parents = parents;
  this._name = name;
  this._id = id2;
}
function newId() {
  return ++id$k;
}
var selection_prototype = selection.prototype;
Transition.prototype = {
  constructor: Transition,
  select: transition_select,
  selectAll: transition_selectAll,
  selectChild: selection_prototype.selectChild,
  selectChildren: selection_prototype.selectChildren,
  filter: transition_filter,
  merge: transition_merge,
  selection: transition_selection,
  transition: transition_transition,
  call: selection_prototype.call,
  nodes: selection_prototype.nodes,
  node: selection_prototype.node,
  size: selection_prototype.size,
  empty: selection_prototype.empty,
  each: selection_prototype.each,
  on: transition_on,
  attr: transition_attr,
  attrTween: transition_attrTween,
  style: transition_style,
  styleTween: transition_styleTween,
  text: transition_text,
  textTween: transition_textTween,
  remove: transition_remove,
  tween: transition_tween,
  delay: transition_delay,
  duration: transition_duration,
  ease: transition_ease,
  easeVarying: transition_easeVarying,
  end: transition_end,
  [Symbol.iterator]: selection_prototype[Symbol.iterator]
};
function cubicInOut(t) {
  return ((t *= 2) <= 1 ? t * t * t : (t -= 2) * t * t + 2) / 2;
}
var defaultTiming = {
  time: null,
  // Set on use.
  delay: 0,
  duration: 250,
  ease: cubicInOut
};
function inherit(node2, id2) {
  var timing;
  while (!(timing = node2.__transition) || !(timing = timing[id2])) {
    if (!(node2 = node2.parentNode)) {
      throw new Error(`transition ${id2} not found`);
    }
  }
  return timing;
}
function selection_transition(name) {
  var id2, timing;
  if (name instanceof Transition) {
    id2 = name._id, name = name._name;
  } else {
    id2 = newId(), (timing = defaultTiming).time = now(), name = name == null ? null : name + "";
  }
  for (var groups = this._groups, m = groups.length, j = 0; j < m; ++j) {
    for (var group = groups[j], n = group.length, node2, i = 0; i < n; ++i) {
      if (node2 = group[i]) {
        schedule(node2, name, id2, i, group, timing || inherit(node2, id2));
      }
    }
  }
  return new Transition(groups, this._parents, name, id2);
}
selection.prototype.interrupt = selection_interrupt;
selection.prototype.transition = selection_transition;
const abs$1 = Math.abs;
const atan2 = Math.atan2;
const cos = Math.cos;
const max = Math.max;
const min = Math.min;
const sin = Math.sin;
const sqrt = Math.sqrt;
const epsilon = 1e-12;
const pi = Math.PI;
const halfPi = pi / 2;
const tau = 2 * pi;
function acos(x) {
  return x > 1 ? 0 : x < -1 ? pi : Math.acos(x);
}
function asin(x) {
  return x >= 1 ? halfPi : x <= -1 ? -halfPi : Math.asin(x);
}
function Linear(context) {
  this._context = context;
}
Linear.prototype = {
  areaStart: function() {
    this._line = 0;
  },
  areaEnd: function() {
    this._line = NaN;
  },
  lineStart: function() {
    this._point = 0;
  },
  lineEnd: function() {
    if (this._line || this._line !== 0 && this._point === 1)
      this._context.closePath();
    this._line = 1 - this._line;
  },
  point: function(x, y) {
    x = +x, y = +y;
    switch (this._point) {
      case 0:
        this._point = 1;
        this._line ? this._context.lineTo(x, y) : this._context.moveTo(x, y);
        break;
      case 1:
        this._point = 2;
      default:
        this._context.lineTo(x, y);
        break;
    }
  }
};
function curveLinear(context) {
  return new Linear(context);
}
class Bump {
  constructor(context, x) {
    this._context = context;
    this._x = x;
  }
  areaStart() {
    this._line = 0;
  }
  areaEnd() {
    this._line = NaN;
  }
  lineStart() {
    this._point = 0;
  }
  lineEnd() {
    if (this._line || this._line !== 0 && this._point === 1)
      this._context.closePath();
    this._line = 1 - this._line;
  }
  point(x, y) {
    x = +x, y = +y;
    switch (this._point) {
      case 0: {
        this._point = 1;
        if (this._line)
          this._context.lineTo(x, y);
        else
          this._context.moveTo(x, y);
        break;
      }
      case 1:
        this._point = 2;
      default: {
        if (this._x)
          this._context.bezierCurveTo(this._x0 = (this._x0 + x) / 2, this._y0, this._x0, y, x, y);
        else
          this._context.bezierCurveTo(this._x0, this._y0 = (this._y0 + y) / 2, x, this._y0, x, y);
        break;
      }
    }
    this._x0 = x, this._y0 = y;
  }
}
function bumpX(context) {
  return new Bump(context, true);
}
function bumpY(context) {
  return new Bump(context, false);
}
function noop() {
}
function point$3(that, x, y) {
  that._context.bezierCurveTo(
    (2 * that._x0 + that._x1) / 3,
    (2 * that._y0 + that._y1) / 3,
    (that._x0 + 2 * that._x1) / 3,
    (that._y0 + 2 * that._y1) / 3,
    (that._x0 + 4 * that._x1 + x) / 6,
    (that._y0 + 4 * that._y1 + y) / 6
  );
}
function Basis(context) {
  this._context = context;
}
Basis.prototype = {
  areaStart: function() {
    this._line = 0;
  },
  areaEnd: function() {
    this._line = NaN;
  },
  lineStart: function() {
    this._x0 = this._x1 = this._y0 = this._y1 = NaN;
    this._point = 0;
  },
  lineEnd: function() {
    switch (this._point) {
      case 3:
        point$3(this, this._x1, this._y1);
      case 2:
        this._context.lineTo(this._x1, this._y1);
        break;
    }
    if (this._line || this._line !== 0 && this._point === 1)
      this._context.closePath();
    this._line = 1 - this._line;
  },
  point: function(x, y) {
    x = +x, y = +y;
    switch (this._point) {
      case 0:
        this._point = 1;
        this._line ? this._context.lineTo(x, y) : this._context.moveTo(x, y);
        break;
      case 1:
        this._point = 2;
        break;
      case 2:
        this._point = 3;
        this._context.lineTo((5 * this._x0 + this._x1) / 6, (5 * this._y0 + this._y1) / 6);
      default:
        point$3(this, x, y);
        break;
    }
    this._x0 = this._x1, this._x1 = x;
    this._y0 = this._y1, this._y1 = y;
  }
};
function curveBasis(context) {
  return new Basis(context);
}
function BasisClosed(context) {
  this._context = context;
}
BasisClosed.prototype = {
  areaStart: noop,
  areaEnd: noop,
  lineStart: function() {
    this._x0 = this._x1 = this._x2 = this._x3 = this._x4 = this._y0 = this._y1 = this._y2 = this._y3 = this._y4 = NaN;
    this._point = 0;
  },
  lineEnd: function() {
    switch (this._point) {
      case 1: {
        this._context.moveTo(this._x2, this._y2);
        this._context.closePath();
        break;
      }
      case 2: {
        this._context.moveTo((this._x2 + 2 * this._x3) / 3, (this._y2 + 2 * this._y3) / 3);
        this._context.lineTo((this._x3 + 2 * this._x2) / 3, (this._y3 + 2 * this._y2) / 3);
        this._context.closePath();
        break;
      }
      case 3: {
        this.point(this._x2, this._y2);
        this.point(this._x3, this._y3);
        this.point(this._x4, this._y4);
        break;
      }
    }
  },
  point: function(x, y) {
    x = +x, y = +y;
    switch (this._point) {
      case 0:
        this._point = 1;
        this._x2 = x, this._y2 = y;
        break;
      case 1:
        this._point = 2;
        this._x3 = x, this._y3 = y;
        break;
      case 2:
        this._point = 3;
        this._x4 = x, this._y4 = y;
        this._context.moveTo((this._x0 + 4 * this._x1 + x) / 6, (this._y0 + 4 * this._y1 + y) / 6);
        break;
      default:
        point$3(this, x, y);
        break;
    }
    this._x0 = this._x1, this._x1 = x;
    this._y0 = this._y1, this._y1 = y;
  }
};
function curveBasisClosed(context) {
  return new BasisClosed(context);
}
function BasisOpen(context) {
  this._context = context;
}
BasisOpen.prototype = {
  areaStart: function() {
    this._line = 0;
  },
  areaEnd: function() {
    this._line = NaN;
  },
  lineStart: function() {
    this._x0 = this._x1 = this._y0 = this._y1 = NaN;
    this._point = 0;
  },
  lineEnd: function() {
    if (this._line || this._line !== 0 && this._point === 3)
      this._context.closePath();
    this._line = 1 - this._line;
  },
  point: function(x, y) {
    x = +x, y = +y;
    switch (this._point) {
      case 0:
        this._point = 1;
        break;
      case 1:
        this._point = 2;
        break;
      case 2:
        this._point = 3;
        var x0 = (this._x0 + 4 * this._x1 + x) / 6, y0 = (this._y0 + 4 * this._y1 + y) / 6;
        this._line ? this._context.lineTo(x0, y0) : this._context.moveTo(x0, y0);
        break;
      case 3:
        this._point = 4;
      default:
        point$3(this, x, y);
        break;
    }
    this._x0 = this._x1, this._x1 = x;
    this._y0 = this._y1, this._y1 = y;
  }
};
function curveBasisOpen(context) {
  return new BasisOpen(context);
}
function Bundle(context, beta) {
  this._basis = new Basis(context);
  this._beta = beta;
}
Bundle.prototype = {
  lineStart: function() {
    this._x = [];
    this._y = [];
    this._basis.lineStart();
  },
  lineEnd: function() {
    var x = this._x, y = this._y, j = x.length - 1;
    if (j > 0) {
      var x0 = x[0], y0 = y[0], dx = x[j] - x0, dy = y[j] - y0, i = -1, t;
      while (++i <= j) {
        t = i / j;
        this._basis.point(
          this._beta * x[i] + (1 - this._beta) * (x0 + t * dx),
          this._beta * y[i] + (1 - this._beta) * (y0 + t * dy)
        );
      }
    }
    this._x = this._y = null;
    this._basis.lineEnd();
  },
  point: function(x, y) {
    this._x.push(+x);
    this._y.push(+y);
  }
};
const curveBundle = function custom(beta) {
  function bundle(context) {
    return beta === 1 ? new Basis(context) : new Bundle(context, beta);
  }
  bundle.beta = function(beta2) {
    return custom(+beta2);
  };
  return bundle;
}(0.85);
function point$2(that, x, y) {
  that._context.bezierCurveTo(
    that._x1 + that._k * (that._x2 - that._x0),
    that._y1 + that._k * (that._y2 - that._y0),
    that._x2 + that._k * (that._x1 - x),
    that._y2 + that._k * (that._y1 - y),
    that._x2,
    that._y2
  );
}
function Cardinal(context, tension) {
  this._context = context;
  this._k = (1 - tension) / 6;
}
Cardinal.prototype = {
  areaStart: function() {
    this._line = 0;
  },
  areaEnd: function() {
    this._line = NaN;
  },
  lineStart: function() {
    this._x0 = this._x1 = this._x2 = this._y0 = this._y1 = this._y2 = NaN;
    this._point = 0;
  },
  lineEnd: function() {
    switch (this._point) {
      case 2:
        this._context.lineTo(this._x2, this._y2);
        break;
      case 3:
        point$2(this, this._x1, this._y1);
        break;
    }
    if (this._line || this._line !== 0 && this._point === 1)
      this._context.closePath();
    this._line = 1 - this._line;
  },
  point: function(x, y) {
    x = +x, y = +y;
    switch (this._point) {
      case 0:
        this._point = 1;
        this._line ? this._context.lineTo(x, y) : this._context.moveTo(x, y);
        break;
      case 1:
        this._point = 2;
        this._x1 = x, this._y1 = y;
        break;
      case 2:
        this._point = 3;
      default:
        point$2(this, x, y);
        break;
    }
    this._x0 = this._x1, this._x1 = this._x2, this._x2 = x;
    this._y0 = this._y1, this._y1 = this._y2, this._y2 = y;
  }
};
const curveCardinal = function custom2(tension) {
  function cardinal(context) {
    return new Cardinal(context, tension);
  }
  cardinal.tension = function(tension2) {
    return custom2(+tension2);
  };
  return cardinal;
}(0);
function CardinalClosed(context, tension) {
  this._context = context;
  this._k = (1 - tension) / 6;
}
CardinalClosed.prototype = {
  areaStart: noop,
  areaEnd: noop,
  lineStart: function() {
    this._x0 = this._x1 = this._x2 = this._x3 = this._x4 = this._x5 = this._y0 = this._y1 = this._y2 = this._y3 = this._y4 = this._y5 = NaN;
    this._point = 0;
  },
  lineEnd: function() {
    switch (this._point) {
      case 1: {
        this._context.moveTo(this._x3, this._y3);
        this._context.closePath();
        break;
      }
      case 2: {
        this._context.lineTo(this._x3, this._y3);
        this._context.closePath();
        break;
      }
      case 3: {
        this.point(this._x3, this._y3);
        this.point(this._x4, this._y4);
        this.point(this._x5, this._y5);
        break;
      }
    }
  },
  point: function(x, y) {
    x = +x, y = +y;
    switch (this._point) {
      case 0:
        this._point = 1;
        this._x3 = x, this._y3 = y;
        break;
      case 1:
        this._point = 2;
        this._context.moveTo(this._x4 = x, this._y4 = y);
        break;
      case 2:
        this._point = 3;
        this._x5 = x, this._y5 = y;
        break;
      default:
        point$2(this, x, y);
        break;
    }
    this._x0 = this._x1, this._x1 = this._x2, this._x2 = x;
    this._y0 = this._y1, this._y1 = this._y2, this._y2 = y;
  }
};
const curveCardinalClosed = function custom3(tension) {
  function cardinal(context) {
    return new CardinalClosed(context, tension);
  }
  cardinal.tension = function(tension2) {
    return custom3(+tension2);
  };
  return cardinal;
}(0);
function CardinalOpen(context, tension) {
  this._context = context;
  this._k = (1 - tension) / 6;
}
CardinalOpen.prototype = {
  areaStart: function() {
    this._line = 0;
  },
  areaEnd: function() {
    this._line = NaN;
  },
  lineStart: function() {
    this._x0 = this._x1 = this._x2 = this._y0 = this._y1 = this._y2 = NaN;
    this._point = 0;
  },
  lineEnd: function() {
    if (this._line || this._line !== 0 && this._point === 3)
      this._context.closePath();
    this._line = 1 - this._line;
  },
  point: function(x, y) {
    x = +x, y = +y;
    switch (this._point) {
      case 0:
        this._point = 1;
        break;
      case 1:
        this._point = 2;
        break;
      case 2:
        this._point = 3;
        this._line ? this._context.lineTo(this._x2, this._y2) : this._context.moveTo(this._x2, this._y2);
        break;
      case 3:
        this._point = 4;
      default:
        point$2(this, x, y);
        break;
    }
    this._x0 = this._x1, this._x1 = this._x2, this._x2 = x;
    this._y0 = this._y1, this._y1 = this._y2, this._y2 = y;
  }
};
const curveCardinalOpen = function custom4(tension) {
  function cardinal(context) {
    return new CardinalOpen(context, tension);
  }
  cardinal.tension = function(tension2) {
    return custom4(+tension2);
  };
  return cardinal;
}(0);
function point$1(that, x, y) {
  var x1 = that._x1, y1 = that._y1, x2 = that._x2, y2 = that._y2;
  if (that._l01_a > epsilon) {
    var a = 2 * that._l01_2a + 3 * that._l01_a * that._l12_a + that._l12_2a, n = 3 * that._l01_a * (that._l01_a + that._l12_a);
    x1 = (x1 * a - that._x0 * that._l12_2a + that._x2 * that._l01_2a) / n;
    y1 = (y1 * a - that._y0 * that._l12_2a + that._y2 * that._l01_2a) / n;
  }
  if (that._l23_a > epsilon) {
    var b = 2 * that._l23_2a + 3 * that._l23_a * that._l12_a + that._l12_2a, m = 3 * that._l23_a * (that._l23_a + that._l12_a);
    x2 = (x2 * b + that._x1 * that._l23_2a - x * that._l12_2a) / m;
    y2 = (y2 * b + that._y1 * that._l23_2a - y * that._l12_2a) / m;
  }
  that._context.bezierCurveTo(x1, y1, x2, y2, that._x2, that._y2);
}
function CatmullRom(context, alpha) {
  this._context = context;
  this._alpha = alpha;
}
CatmullRom.prototype = {
  areaStart: function() {
    this._line = 0;
  },
  areaEnd: function() {
    this._line = NaN;
  },
  lineStart: function() {
    this._x0 = this._x1 = this._x2 = this._y0 = this._y1 = this._y2 = NaN;
    this._l01_a = this._l12_a = this._l23_a = this._l01_2a = this._l12_2a = this._l23_2a = this._point = 0;
  },
  lineEnd: function() {
    switch (this._point) {
      case 2:
        this._context.lineTo(this._x2, this._y2);
        break;
      case 3:
        this.point(this._x2, this._y2);
        break;
    }
    if (this._line || this._line !== 0 && this._point === 1)
      this._context.closePath();
    this._line = 1 - this._line;
  },
  point: function(x, y) {
    x = +x, y = +y;
    if (this._point) {
      var x23 = this._x2 - x, y23 = this._y2 - y;
      this._l23_a = Math.sqrt(this._l23_2a = Math.pow(x23 * x23 + y23 * y23, this._alpha));
    }
    switch (this._point) {
      case 0:
        this._point = 1;
        this._line ? this._context.lineTo(x, y) : this._context.moveTo(x, y);
        break;
      case 1:
        this._point = 2;
        break;
      case 2:
        this._point = 3;
      default:
        point$1(this, x, y);
        break;
    }
    this._l01_a = this._l12_a, this._l12_a = this._l23_a;
    this._l01_2a = this._l12_2a, this._l12_2a = this._l23_2a;
    this._x0 = this._x1, this._x1 = this._x2, this._x2 = x;
    this._y0 = this._y1, this._y1 = this._y2, this._y2 = y;
  }
};
const curveCatmullRom = function custom5(alpha) {
  function catmullRom(context) {
    return alpha ? new CatmullRom(context, alpha) : new Cardinal(context, 0);
  }
  catmullRom.alpha = function(alpha2) {
    return custom5(+alpha2);
  };
  return catmullRom;
}(0.5);
function CatmullRomClosed(context, alpha) {
  this._context = context;
  this._alpha = alpha;
}
CatmullRomClosed.prototype = {
  areaStart: noop,
  areaEnd: noop,
  lineStart: function() {
    this._x0 = this._x1 = this._x2 = this._x3 = this._x4 = this._x5 = this._y0 = this._y1 = this._y2 = this._y3 = this._y4 = this._y5 = NaN;
    this._l01_a = this._l12_a = this._l23_a = this._l01_2a = this._l12_2a = this._l23_2a = this._point = 0;
  },
  lineEnd: function() {
    switch (this._point) {
      case 1: {
        this._context.moveTo(this._x3, this._y3);
        this._context.closePath();
        break;
      }
      case 2: {
        this._context.lineTo(this._x3, this._y3);
        this._context.closePath();
        break;
      }
      case 3: {
        this.point(this._x3, this._y3);
        this.point(this._x4, this._y4);
        this.point(this._x5, this._y5);
        break;
      }
    }
  },
  point: function(x, y) {
    x = +x, y = +y;
    if (this._point) {
      var x23 = this._x2 - x, y23 = this._y2 - y;
      this._l23_a = Math.sqrt(this._l23_2a = Math.pow(x23 * x23 + y23 * y23, this._alpha));
    }
    switch (this._point) {
      case 0:
        this._point = 1;
        this._x3 = x, this._y3 = y;
        break;
      case 1:
        this._point = 2;
        this._context.moveTo(this._x4 = x, this._y4 = y);
        break;
      case 2:
        this._point = 3;
        this._x5 = x, this._y5 = y;
        break;
      default:
        point$1(this, x, y);
        break;
    }
    this._l01_a = this._l12_a, this._l12_a = this._l23_a;
    this._l01_2a = this._l12_2a, this._l12_2a = this._l23_2a;
    this._x0 = this._x1, this._x1 = this._x2, this._x2 = x;
    this._y0 = this._y1, this._y1 = this._y2, this._y2 = y;
  }
};
const curveCatmullRomClosed = function custom6(alpha) {
  function catmullRom(context) {
    return alpha ? new CatmullRomClosed(context, alpha) : new CardinalClosed(context, 0);
  }
  catmullRom.alpha = function(alpha2) {
    return custom6(+alpha2);
  };
  return catmullRom;
}(0.5);
function CatmullRomOpen(context, alpha) {
  this._context = context;
  this._alpha = alpha;
}
CatmullRomOpen.prototype = {
  areaStart: function() {
    this._line = 0;
  },
  areaEnd: function() {
    this._line = NaN;
  },
  lineStart: function() {
    this._x0 = this._x1 = this._x2 = this._y0 = this._y1 = this._y2 = NaN;
    this._l01_a = this._l12_a = this._l23_a = this._l01_2a = this._l12_2a = this._l23_2a = this._point = 0;
  },
  lineEnd: function() {
    if (this._line || this._line !== 0 && this._point === 3)
      this._context.closePath();
    this._line = 1 - this._line;
  },
  point: function(x, y) {
    x = +x, y = +y;
    if (this._point) {
      var x23 = this._x2 - x, y23 = this._y2 - y;
      this._l23_a = Math.sqrt(this._l23_2a = Math.pow(x23 * x23 + y23 * y23, this._alpha));
    }
    switch (this._point) {
      case 0:
        this._point = 1;
        break;
      case 1:
        this._point = 2;
        break;
      case 2:
        this._point = 3;
        this._line ? this._context.lineTo(this._x2, this._y2) : this._context.moveTo(this._x2, this._y2);
        break;
      case 3:
        this._point = 4;
      default:
        point$1(this, x, y);
        break;
    }
    this._l01_a = this._l12_a, this._l12_a = this._l23_a;
    this._l01_2a = this._l12_2a, this._l12_2a = this._l23_2a;
    this._x0 = this._x1, this._x1 = this._x2, this._x2 = x;
    this._y0 = this._y1, this._y1 = this._y2, this._y2 = y;
  }
};
const curveCatmullRomOpen = function custom7(alpha) {
  function catmullRom(context) {
    return alpha ? new CatmullRomOpen(context, alpha) : new CardinalOpen(context, 0);
  }
  catmullRom.alpha = function(alpha2) {
    return custom7(+alpha2);
  };
  return catmullRom;
}(0.5);
function LinearClosed(context) {
  this._context = context;
}
LinearClosed.prototype = {
  areaStart: noop,
  areaEnd: noop,
  lineStart: function() {
    this._point = 0;
  },
  lineEnd: function() {
    if (this._point)
      this._context.closePath();
  },
  point: function(x, y) {
    x = +x, y = +y;
    if (this._point)
      this._context.lineTo(x, y);
    else
      this._point = 1, this._context.moveTo(x, y);
  }
};
function curveLinearClosed(context) {
  return new LinearClosed(context);
}
function sign(x) {
  return x < 0 ? -1 : 1;
}
function slope3(that, x2, y2) {
  var h0 = that._x1 - that._x0, h1 = x2 - that._x1, s0 = (that._y1 - that._y0) / (h0 || h1 < 0 && -0), s1 = (y2 - that._y1) / (h1 || h0 < 0 && -0), p = (s0 * h1 + s1 * h0) / (h0 + h1);
  return (sign(s0) + sign(s1)) * Math.min(Math.abs(s0), Math.abs(s1), 0.5 * Math.abs(p)) || 0;
}
function slope2(that, t) {
  var h = that._x1 - that._x0;
  return h ? (3 * (that._y1 - that._y0) / h - t) / 2 : t;
}
function point(that, t0, t1) {
  var x0 = that._x0, y0 = that._y0, x1 = that._x1, y1 = that._y1, dx = (x1 - x0) / 3;
  that._context.bezierCurveTo(x0 + dx, y0 + dx * t0, x1 - dx, y1 - dx * t1, x1, y1);
}
function MonotoneX(context) {
  this._context = context;
}
MonotoneX.prototype = {
  areaStart: function() {
    this._line = 0;
  },
  areaEnd: function() {
    this._line = NaN;
  },
  lineStart: function() {
    this._x0 = this._x1 = this._y0 = this._y1 = this._t0 = NaN;
    this._point = 0;
  },
  lineEnd: function() {
    switch (this._point) {
      case 2:
        this._context.lineTo(this._x1, this._y1);
        break;
      case 3:
        point(this, this._t0, slope2(this, this._t0));
        break;
    }
    if (this._line || this._line !== 0 && this._point === 1)
      this._context.closePath();
    this._line = 1 - this._line;
  },
  point: function(x, y) {
    var t1 = NaN;
    x = +x, y = +y;
    if (x === this._x1 && y === this._y1)
      return;
    switch (this._point) {
      case 0:
        this._point = 1;
        this._line ? this._context.lineTo(x, y) : this._context.moveTo(x, y);
        break;
      case 1:
        this._point = 2;
        break;
      case 2:
        this._point = 3;
        point(this, slope2(this, t1 = slope3(this, x, y)), t1);
        break;
      default:
        point(this, this._t0, t1 = slope3(this, x, y));
        break;
    }
    this._x0 = this._x1, this._x1 = x;
    this._y0 = this._y1, this._y1 = y;
    this._t0 = t1;
  }
};
function MonotoneY(context) {
  this._context = new ReflectContext(context);
}
(MonotoneY.prototype = Object.create(MonotoneX.prototype)).point = function(x, y) {
  MonotoneX.prototype.point.call(this, y, x);
};
function ReflectContext(context) {
  this._context = context;
}
ReflectContext.prototype = {
  moveTo: function(x, y) {
    this._context.moveTo(y, x);
  },
  closePath: function() {
    this._context.closePath();
  },
  lineTo: function(x, y) {
    this._context.lineTo(y, x);
  },
  bezierCurveTo: function(x1, y1, x2, y2, x, y) {
    this._context.bezierCurveTo(y1, x1, y2, x2, y, x);
  }
};
function monotoneX(context) {
  return new MonotoneX(context);
}
function monotoneY(context) {
  return new MonotoneY(context);
}
function Natural(context) {
  this._context = context;
}
Natural.prototype = {
  areaStart: function() {
    this._line = 0;
  },
  areaEnd: function() {
    this._line = NaN;
  },
  lineStart: function() {
    this._x = [];
    this._y = [];
  },
  lineEnd: function() {
    var x = this._x, y = this._y, n = x.length;
    if (n) {
      this._line ? this._context.lineTo(x[0], y[0]) : this._context.moveTo(x[0], y[0]);
      if (n === 2) {
        this._context.lineTo(x[1], y[1]);
      } else {
        var px = controlPoints(x), py = controlPoints(y);
        for (var i0 = 0, i1 = 1; i1 < n; ++i0, ++i1) {
          this._context.bezierCurveTo(px[0][i0], py[0][i0], px[1][i0], py[1][i0], x[i1], y[i1]);
        }
      }
    }
    if (this._line || this._line !== 0 && n === 1)
      this._context.closePath();
    this._line = 1 - this._line;
    this._x = this._y = null;
  },
  point: function(x, y) {
    this._x.push(+x);
    this._y.push(+y);
  }
};
function controlPoints(x) {
  var i, n = x.length - 1, m, a = new Array(n), b = new Array(n), r = new Array(n);
  a[0] = 0, b[0] = 2, r[0] = x[0] + 2 * x[1];
  for (i = 1; i < n - 1; ++i)
    a[i] = 1, b[i] = 4, r[i] = 4 * x[i] + 2 * x[i + 1];
  a[n - 1] = 2, b[n - 1] = 7, r[n - 1] = 8 * x[n - 1] + x[n];
  for (i = 1; i < n; ++i)
    m = a[i] / b[i - 1], b[i] -= m, r[i] -= m * r[i - 1];
  a[n - 1] = r[n - 1] / b[n - 1];
  for (i = n - 2; i >= 0; --i)
    a[i] = (r[i] - a[i + 1]) / b[i];
  b[n - 1] = (x[n] + a[n - 1]) / 2;
  for (i = 0; i < n - 1; ++i)
    b[i] = 2 * x[i + 1] - a[i + 1];
  return [a, b];
}
function curveNatural(context) {
  return new Natural(context);
}
function Step(context, t) {
  this._context = context;
  this._t = t;
}
Step.prototype = {
  areaStart: function() {
    this._line = 0;
  },
  areaEnd: function() {
    this._line = NaN;
  },
  lineStart: function() {
    this._x = this._y = NaN;
    this._point = 0;
  },
  lineEnd: function() {
    if (0 < this._t && this._t < 1 && this._point === 2)
      this._context.lineTo(this._x, this._y);
    if (this._line || this._line !== 0 && this._point === 1)
      this._context.closePath();
    if (this._line >= 0)
      this._t = 1 - this._t, this._line = 1 - this._line;
  },
  point: function(x, y) {
    x = +x, y = +y;
    switch (this._point) {
      case 0:
        this._point = 1;
        this._line ? this._context.lineTo(x, y) : this._context.moveTo(x, y);
        break;
      case 1:
        this._point = 2;
      default: {
        if (this._t <= 0) {
          this._context.lineTo(this._x, y);
          this._context.lineTo(x, y);
        } else {
          var x1 = this._x * (1 - this._t) + x * this._t;
          this._context.lineTo(x1, this._y);
          this._context.lineTo(x1, y);
        }
        break;
      }
    }
    this._x = x, this._y = y;
  }
};
function curveStep(context) {
  return new Step(context, 0.5);
}
function stepBefore(context) {
  return new Step(context, 0);
}
function stepAfter(context) {
  return new Step(context, 1);
}
function Transform(k, x, y) {
  this.k = k;
  this.x = x;
  this.y = y;
}
Transform.prototype = {
  constructor: Transform,
  scale: function(k) {
    return k === 1 ? this : new Transform(this.k * k, this.x, this.y);
  },
  translate: function(x, y) {
    return x === 0 & y === 0 ? this : new Transform(this.k, this.x + this.k * x, this.y + this.k * y);
  },
  apply: function(point2) {
    return [point2[0] * this.k + this.x, point2[1] * this.k + this.y];
  },
  applyX: function(x) {
    return x * this.k + this.x;
  },
  applyY: function(y) {
    return y * this.k + this.y;
  },
  invert: function(location) {
    return [(location[0] - this.x) / this.k, (location[1] - this.y) / this.k];
  },
  invertX: function(x) {
    return (x - this.x) / this.k;
  },
  invertY: function(y) {
    return (y - this.y) / this.k;
  },
  rescaleX: function(x) {
    return x.copy().domain(x.range().map(this.invertX, this).map(x.invert, x));
  },
  rescaleY: function(y) {
    return y.copy().domain(y.range().map(this.invertY, this).map(y.invert, y));
  },
  toString: function() {
    return "translate(" + this.x + "," + this.y + ") scale(" + this.k + ")";
  }
};
Transform.prototype;
/*! @license DOMPurify 3.0.5 | (c) Cure53 and other contributors | Released under the Apache license 2.0 and Mozilla Public License 2.0 | github.com/cure53/DOMPurify/blob/3.0.5/LICENSE */
const {
  entries,
  setPrototypeOf,
  isFrozen,
  getPrototypeOf,
  getOwnPropertyDescriptor
} = Object;
let {
  freeze,
  seal,
  create
} = Object;
let {
  apply: apply$1,
  construct
} = typeof Reflect !== "undefined" && Reflect;
if (!apply$1) {
  apply$1 = function apply2(fun, thisValue, args) {
    return fun.apply(thisValue, args);
  };
}
if (!freeze) {
  freeze = function freeze2(x) {
    return x;
  };
}
if (!seal) {
  seal = function seal2(x) {
    return x;
  };
}
if (!construct) {
  construct = function construct2(Func, args) {
    return new Func(...args);
  };
}
const arrayForEach = unapply(Array.prototype.forEach);
const arrayPop = unapply(Array.prototype.pop);
const arrayPush = unapply(Array.prototype.push);
const stringToLowerCase = unapply(String.prototype.toLowerCase);
const stringToString = unapply(String.prototype.toString);
const stringMatch = unapply(String.prototype.match);
const stringReplace = unapply(String.prototype.replace);
const stringIndexOf = unapply(String.prototype.indexOf);
const stringTrim = unapply(String.prototype.trim);
const regExpTest = unapply(RegExp.prototype.test);
const typeErrorCreate = unconstruct(TypeError);
function unapply(func) {
  return function(thisArg) {
    for (var _len = arguments.length, args = new Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
      args[_key - 1] = arguments[_key];
    }
    return apply$1(func, thisArg, args);
  };
}
function unconstruct(func) {
  return function() {
    for (var _len2 = arguments.length, args = new Array(_len2), _key2 = 0; _key2 < _len2; _key2++) {
      args[_key2] = arguments[_key2];
    }
    return construct(func, args);
  };
}
function addToSet(set2, array2, transformCaseFunc) {
  var _transformCaseFunc;
  transformCaseFunc = (_transformCaseFunc = transformCaseFunc) !== null && _transformCaseFunc !== void 0 ? _transformCaseFunc : stringToLowerCase;
  if (setPrototypeOf) {
    setPrototypeOf(set2, null);
  }
  let l = array2.length;
  while (l--) {
    let element = array2[l];
    if (typeof element === "string") {
      const lcElement = transformCaseFunc(element);
      if (lcElement !== element) {
        if (!isFrozen(array2)) {
          array2[l] = lcElement;
        }
        element = lcElement;
      }
    }
    set2[element] = true;
  }
  return set2;
}
function clone(object) {
  const newObject = create(null);
  for (const [property, value] of entries(object)) {
    newObject[property] = value;
  }
  return newObject;
}
function lookupGetter(object, prop) {
  while (object !== null) {
    const desc = getOwnPropertyDescriptor(object, prop);
    if (desc) {
      if (desc.get) {
        return unapply(desc.get);
      }
      if (typeof desc.value === "function") {
        return unapply(desc.value);
      }
    }
    object = getPrototypeOf(object);
  }
  function fallbackValue(element) {
    console.warn("fallback value for", element);
    return null;
  }
  return fallbackValue;
}
const html$1 = freeze(["a", "abbr", "acronym", "address", "area", "article", "aside", "audio", "b", "bdi", "bdo", "big", "blink", "blockquote", "body", "br", "button", "canvas", "caption", "center", "cite", "code", "col", "colgroup", "content", "data", "datalist", "dd", "decorator", "del", "details", "dfn", "dialog", "dir", "div", "dl", "dt", "element", "em", "fieldset", "figcaption", "figure", "font", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "img", "input", "ins", "kbd", "label", "legend", "li", "main", "map", "mark", "marquee", "menu", "menuitem", "meter", "nav", "nobr", "ol", "optgroup", "option", "output", "p", "picture", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "section", "select", "shadow", "small", "source", "spacer", "span", "strike", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "tr", "track", "tt", "u", "ul", "var", "video", "wbr"]);
const svg$1 = freeze(["svg", "a", "altglyph", "altglyphdef", "altglyphitem", "animatecolor", "animatemotion", "animatetransform", "circle", "clippath", "defs", "desc", "ellipse", "filter", "font", "g", "glyph", "glyphref", "hkern", "image", "line", "lineargradient", "marker", "mask", "metadata", "mpath", "path", "pattern", "polygon", "polyline", "radialgradient", "rect", "stop", "style", "switch", "symbol", "text", "textpath", "title", "tref", "tspan", "view", "vkern"]);
const svgFilters = freeze(["feBlend", "feColorMatrix", "feComponentTransfer", "feComposite", "feConvolveMatrix", "feDiffuseLighting", "feDisplacementMap", "feDistantLight", "feDropShadow", "feFlood", "feFuncA", "feFuncB", "feFuncG", "feFuncR", "feGaussianBlur", "feImage", "feMerge", "feMergeNode", "feMorphology", "feOffset", "fePointLight", "feSpecularLighting", "feSpotLight", "feTile", "feTurbulence"]);
const svgDisallowed = freeze(["animate", "color-profile", "cursor", "discard", "font-face", "font-face-format", "font-face-name", "font-face-src", "font-face-uri", "foreignobject", "hatch", "hatchpath", "mesh", "meshgradient", "meshpatch", "meshrow", "missing-glyph", "script", "set", "solidcolor", "unknown", "use"]);
const mathMl$1 = freeze(["math", "menclose", "merror", "mfenced", "mfrac", "mglyph", "mi", "mlabeledtr", "mmultiscripts", "mn", "mo", "mover", "mpadded", "mphantom", "mroot", "mrow", "ms", "mspace", "msqrt", "mstyle", "msub", "msup", "msubsup", "mtable", "mtd", "mtext", "mtr", "munder", "munderover", "mprescripts"]);
const mathMlDisallowed = freeze(["maction", "maligngroup", "malignmark", "mlongdiv", "mscarries", "mscarry", "msgroup", "mstack", "msline", "msrow", "semantics", "annotation", "annotation-xml", "mprescripts", "none"]);
const text = freeze(["#text"]);
const html = freeze(["accept", "action", "align", "alt", "autocapitalize", "autocomplete", "autopictureinpicture", "autoplay", "background", "bgcolor", "border", "capture", "cellpadding", "cellspacing", "checked", "cite", "class", "clear", "color", "cols", "colspan", "controls", "controlslist", "coords", "crossorigin", "datetime", "decoding", "default", "dir", "disabled", "disablepictureinpicture", "disableremoteplayback", "download", "draggable", "enctype", "enterkeyhint", "face", "for", "headers", "height", "hidden", "high", "href", "hreflang", "id", "inputmode", "integrity", "ismap", "kind", "label", "lang", "list", "loading", "loop", "low", "max", "maxlength", "media", "method", "min", "minlength", "multiple", "muted", "name", "nonce", "noshade", "novalidate", "nowrap", "open", "optimum", "pattern", "placeholder", "playsinline", "poster", "preload", "pubdate", "radiogroup", "readonly", "rel", "required", "rev", "reversed", "role", "rows", "rowspan", "spellcheck", "scope", "selected", "shape", "size", "sizes", "span", "srclang", "start", "src", "srcset", "step", "style", "summary", "tabindex", "title", "translate", "type", "usemap", "valign", "value", "width", "xmlns", "slot"]);
const svg = freeze(["accent-height", "accumulate", "additive", "alignment-baseline", "ascent", "attributename", "attributetype", "azimuth", "basefrequency", "baseline-shift", "begin", "bias", "by", "class", "clip", "clippathunits", "clip-path", "clip-rule", "color", "color-interpolation", "color-interpolation-filters", "color-profile", "color-rendering", "cx", "cy", "d", "dx", "dy", "diffuseconstant", "direction", "display", "divisor", "dur", "edgemode", "elevation", "end", "fill", "fill-opacity", "fill-rule", "filter", "filterunits", "flood-color", "flood-opacity", "font-family", "font-size", "font-size-adjust", "font-stretch", "font-style", "font-variant", "font-weight", "fx", "fy", "g1", "g2", "glyph-name", "glyphref", "gradientunits", "gradienttransform", "height", "href", "id", "image-rendering", "in", "in2", "k", "k1", "k2", "k3", "k4", "kerning", "keypoints", "keysplines", "keytimes", "lang", "lengthadjust", "letter-spacing", "kernelmatrix", "kernelunitlength", "lighting-color", "local", "marker-end", "marker-mid", "marker-start", "markerheight", "markerunits", "markerwidth", "maskcontentunits", "maskunits", "max", "mask", "media", "method", "mode", "min", "name", "numoctaves", "offset", "operator", "opacity", "order", "orient", "orientation", "origin", "overflow", "paint-order", "path", "pathlength", "patterncontentunits", "patterntransform", "patternunits", "points", "preservealpha", "preserveaspectratio", "primitiveunits", "r", "rx", "ry", "radius", "refx", "refy", "repeatcount", "repeatdur", "restart", "result", "rotate", "scale", "seed", "shape-rendering", "specularconstant", "specularexponent", "spreadmethod", "startoffset", "stddeviation", "stitchtiles", "stop-color", "stop-opacity", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke", "stroke-width", "style", "surfacescale", "systemlanguage", "tabindex", "targetx", "targety", "transform", "transform-origin", "text-anchor", "text-decoration", "text-rendering", "textlength", "type", "u1", "u2", "unicode", "values", "viewbox", "visibility", "version", "vert-adv-y", "vert-origin-x", "vert-origin-y", "width", "word-spacing", "wrap", "writing-mode", "xchannelselector", "ychannelselector", "x", "x1", "x2", "xmlns", "y", "y1", "y2", "z", "zoomandpan"]);
const mathMl = freeze(["accent", "accentunder", "align", "bevelled", "close", "columnsalign", "columnlines", "columnspan", "denomalign", "depth", "dir", "display", "displaystyle", "encoding", "fence", "frame", "height", "href", "id", "largeop", "length", "linethickness", "lspace", "lquote", "mathbackground", "mathcolor", "mathsize", "mathvariant", "maxsize", "minsize", "movablelimits", "notation", "numalign", "open", "rowalign", "rowlines", "rowspacing", "rowspan", "rspace", "rquote", "scriptlevel", "scriptminsize", "scriptsizemultiplier", "selection", "separator", "separators", "stretchy", "subscriptshift", "supscriptshift", "symmetric", "voffset", "width", "xmlns"]);
const xml = freeze(["xlink:href", "xml:id", "xlink:title", "xml:space", "xmlns:xlink"]);
const MUSTACHE_EXPR = seal(/\{\{[\w\W]*|[\w\W]*\}\}/gm);
const ERB_EXPR = seal(/<%[\w\W]*|[\w\W]*%>/gm);
const TMPLIT_EXPR = seal(/\${[\w\W]*}/gm);
const DATA_ATTR = seal(/^data-[\-\w.\u00B7-\uFFFF]/);
const ARIA_ATTR = seal(/^aria-[\-\w]+$/);
const IS_ALLOWED_URI = seal(
  /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i
  // eslint-disable-line no-useless-escape
);
const IS_SCRIPT_OR_DATA = seal(/^(?:\w+script|data):/i);
const ATTR_WHITESPACE = seal(
  /[\u0000-\u0020\u00A0\u1680\u180E\u2000-\u2029\u205F\u3000]/g
  // eslint-disable-line no-control-regex
);
const DOCTYPE_NAME = seal(/^html$/i);
var EXPRESSIONS = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  MUSTACHE_EXPR,
  ERB_EXPR,
  TMPLIT_EXPR,
  DATA_ATTR,
  ARIA_ATTR,
  IS_ALLOWED_URI,
  IS_SCRIPT_OR_DATA,
  ATTR_WHITESPACE,
  DOCTYPE_NAME
});
const getGlobal = () => typeof window === "undefined" ? null : window;
const _createTrustedTypesPolicy = function _createTrustedTypesPolicy2(trustedTypes, purifyHostElement) {
  if (typeof trustedTypes !== "object" || typeof trustedTypes.createPolicy !== "function") {
    return null;
  }
  let suffix = null;
  const ATTR_NAME = "data-tt-policy-suffix";
  if (purifyHostElement && purifyHostElement.hasAttribute(ATTR_NAME)) {
    suffix = purifyHostElement.getAttribute(ATTR_NAME);
  }
  const policyName = "dompurify" + (suffix ? "#" + suffix : "");
  try {
    return trustedTypes.createPolicy(policyName, {
      createHTML(html2) {
        return html2;
      },
      createScriptURL(scriptUrl) {
        return scriptUrl;
      }
    });
  } catch (_2) {
    console.warn("TrustedTypes policy " + policyName + " could not be created.");
    return null;
  }
};
function createDOMPurify() {
  let window2 = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : getGlobal();
  const DOMPurify = (root2) => createDOMPurify(root2);
  DOMPurify.version = "3.0.5";
  DOMPurify.removed = [];
  if (!window2 || !window2.document || window2.document.nodeType !== 9) {
    DOMPurify.isSupported = false;
    return DOMPurify;
  }
  const originalDocument = window2.document;
  const currentScript = originalDocument.currentScript;
  let {
    document: document2
  } = window2;
  const {
    DocumentFragment,
    HTMLTemplateElement,
    Node,
    Element,
    NodeFilter,
    NamedNodeMap = window2.NamedNodeMap || window2.MozNamedAttrMap,
    HTMLFormElement,
    DOMParser,
    trustedTypes
  } = window2;
  const ElementPrototype = Element.prototype;
  const cloneNode = lookupGetter(ElementPrototype, "cloneNode");
  const getNextSibling = lookupGetter(ElementPrototype, "nextSibling");
  const getChildNodes = lookupGetter(ElementPrototype, "childNodes");
  const getParentNode = lookupGetter(ElementPrototype, "parentNode");
  if (typeof HTMLTemplateElement === "function") {
    const template = document2.createElement("template");
    if (template.content && template.content.ownerDocument) {
      document2 = template.content.ownerDocument;
    }
  }
  let trustedTypesPolicy;
  let emptyHTML = "";
  const {
    implementation,
    createNodeIterator,
    createDocumentFragment,
    getElementsByTagName
  } = document2;
  const {
    importNode
  } = originalDocument;
  let hooks = {};
  DOMPurify.isSupported = typeof entries === "function" && typeof getParentNode === "function" && implementation && implementation.createHTMLDocument !== void 0;
  const {
    MUSTACHE_EXPR: MUSTACHE_EXPR2,
    ERB_EXPR: ERB_EXPR2,
    TMPLIT_EXPR: TMPLIT_EXPR2,
    DATA_ATTR: DATA_ATTR2,
    ARIA_ATTR: ARIA_ATTR2,
    IS_SCRIPT_OR_DATA: IS_SCRIPT_OR_DATA2,
    ATTR_WHITESPACE: ATTR_WHITESPACE2
  } = EXPRESSIONS;
  let {
    IS_ALLOWED_URI: IS_ALLOWED_URI$1
  } = EXPRESSIONS;
  let ALLOWED_TAGS = null;
  const DEFAULT_ALLOWED_TAGS = addToSet({}, [...html$1, ...svg$1, ...svgFilters, ...mathMl$1, ...text]);
  let ALLOWED_ATTR = null;
  const DEFAULT_ALLOWED_ATTR = addToSet({}, [...html, ...svg, ...mathMl, ...xml]);
  let CUSTOM_ELEMENT_HANDLING = Object.seal(Object.create(null, {
    tagNameCheck: {
      writable: true,
      configurable: false,
      enumerable: true,
      value: null
    },
    attributeNameCheck: {
      writable: true,
      configurable: false,
      enumerable: true,
      value: null
    },
    allowCustomizedBuiltInElements: {
      writable: true,
      configurable: false,
      enumerable: true,
      value: false
    }
  }));
  let FORBID_TAGS = null;
  let FORBID_ATTR = null;
  let ALLOW_ARIA_ATTR = true;
  let ALLOW_DATA_ATTR = true;
  let ALLOW_UNKNOWN_PROTOCOLS = false;
  let ALLOW_SELF_CLOSE_IN_ATTR = true;
  let SAFE_FOR_TEMPLATES = false;
  let WHOLE_DOCUMENT = false;
  let SET_CONFIG = false;
  let FORCE_BODY = false;
  let RETURN_DOM = false;
  let RETURN_DOM_FRAGMENT = false;
  let RETURN_TRUSTED_TYPE = false;
  let SANITIZE_DOM = true;
  let SANITIZE_NAMED_PROPS = false;
  const SANITIZE_NAMED_PROPS_PREFIX = "user-content-";
  let KEEP_CONTENT = true;
  let IN_PLACE = false;
  let USE_PROFILES = {};
  let FORBID_CONTENTS = null;
  const DEFAULT_FORBID_CONTENTS = addToSet({}, ["annotation-xml", "audio", "colgroup", "desc", "foreignobject", "head", "iframe", "math", "mi", "mn", "mo", "ms", "mtext", "noembed", "noframes", "noscript", "plaintext", "script", "style", "svg", "template", "thead", "title", "video", "xmp"]);
  let DATA_URI_TAGS = null;
  const DEFAULT_DATA_URI_TAGS = addToSet({}, ["audio", "video", "img", "source", "image", "track"]);
  let URI_SAFE_ATTRIBUTES = null;
  const DEFAULT_URI_SAFE_ATTRIBUTES = addToSet({}, ["alt", "class", "for", "id", "label", "name", "pattern", "placeholder", "role", "summary", "title", "value", "style", "xmlns"]);
  const MATHML_NAMESPACE = "http://www.w3.org/1998/Math/MathML";
  const SVG_NAMESPACE = "http://www.w3.org/2000/svg";
  const HTML_NAMESPACE = "http://www.w3.org/1999/xhtml";
  let NAMESPACE = HTML_NAMESPACE;
  let IS_EMPTY_INPUT = false;
  let ALLOWED_NAMESPACES = null;
  const DEFAULT_ALLOWED_NAMESPACES = addToSet({}, [MATHML_NAMESPACE, SVG_NAMESPACE, HTML_NAMESPACE], stringToString);
  let PARSER_MEDIA_TYPE;
  const SUPPORTED_PARSER_MEDIA_TYPES = ["application/xhtml+xml", "text/html"];
  const DEFAULT_PARSER_MEDIA_TYPE = "text/html";
  let transformCaseFunc;
  let CONFIG = null;
  const formElement = document2.createElement("form");
  const isRegexOrFunction = function isRegexOrFunction2(testValue) {
    return testValue instanceof RegExp || testValue instanceof Function;
  };
  const _parseConfig = function _parseConfig2(cfg) {
    if (CONFIG && CONFIG === cfg) {
      return;
    }
    if (!cfg || typeof cfg !== "object") {
      cfg = {};
    }
    cfg = clone(cfg);
    PARSER_MEDIA_TYPE = // eslint-disable-next-line unicorn/prefer-includes
    SUPPORTED_PARSER_MEDIA_TYPES.indexOf(cfg.PARSER_MEDIA_TYPE) === -1 ? PARSER_MEDIA_TYPE = DEFAULT_PARSER_MEDIA_TYPE : PARSER_MEDIA_TYPE = cfg.PARSER_MEDIA_TYPE;
    transformCaseFunc = PARSER_MEDIA_TYPE === "application/xhtml+xml" ? stringToString : stringToLowerCase;
    ALLOWED_TAGS = "ALLOWED_TAGS" in cfg ? addToSet({}, cfg.ALLOWED_TAGS, transformCaseFunc) : DEFAULT_ALLOWED_TAGS;
    ALLOWED_ATTR = "ALLOWED_ATTR" in cfg ? addToSet({}, cfg.ALLOWED_ATTR, transformCaseFunc) : DEFAULT_ALLOWED_ATTR;
    ALLOWED_NAMESPACES = "ALLOWED_NAMESPACES" in cfg ? addToSet({}, cfg.ALLOWED_NAMESPACES, stringToString) : DEFAULT_ALLOWED_NAMESPACES;
    URI_SAFE_ATTRIBUTES = "ADD_URI_SAFE_ATTR" in cfg ? addToSet(
      clone(DEFAULT_URI_SAFE_ATTRIBUTES),
      // eslint-disable-line indent
      cfg.ADD_URI_SAFE_ATTR,
      // eslint-disable-line indent
      transformCaseFunc
      // eslint-disable-line indent
    ) : DEFAULT_URI_SAFE_ATTRIBUTES;
    DATA_URI_TAGS = "ADD_DATA_URI_TAGS" in cfg ? addToSet(
      clone(DEFAULT_DATA_URI_TAGS),
      // eslint-disable-line indent
      cfg.ADD_DATA_URI_TAGS,
      // eslint-disable-line indent
      transformCaseFunc
      // eslint-disable-line indent
    ) : DEFAULT_DATA_URI_TAGS;
    FORBID_CONTENTS = "FORBID_CONTENTS" in cfg ? addToSet({}, cfg.FORBID_CONTENTS, transformCaseFunc) : DEFAULT_FORBID_CONTENTS;
    FORBID_TAGS = "FORBID_TAGS" in cfg ? addToSet({}, cfg.FORBID_TAGS, transformCaseFunc) : {};
    FORBID_ATTR = "FORBID_ATTR" in cfg ? addToSet({}, cfg.FORBID_ATTR, transformCaseFunc) : {};
    USE_PROFILES = "USE_PROFILES" in cfg ? cfg.USE_PROFILES : false;
    ALLOW_ARIA_ATTR = cfg.ALLOW_ARIA_ATTR !== false;
    ALLOW_DATA_ATTR = cfg.ALLOW_DATA_ATTR !== false;
    ALLOW_UNKNOWN_PROTOCOLS = cfg.ALLOW_UNKNOWN_PROTOCOLS || false;
    ALLOW_SELF_CLOSE_IN_ATTR = cfg.ALLOW_SELF_CLOSE_IN_ATTR !== false;
    SAFE_FOR_TEMPLATES = cfg.SAFE_FOR_TEMPLATES || false;
    WHOLE_DOCUMENT = cfg.WHOLE_DOCUMENT || false;
    RETURN_DOM = cfg.RETURN_DOM || false;
    RETURN_DOM_FRAGMENT = cfg.RETURN_DOM_FRAGMENT || false;
    RETURN_TRUSTED_TYPE = cfg.RETURN_TRUSTED_TYPE || false;
    FORCE_BODY = cfg.FORCE_BODY || false;
    SANITIZE_DOM = cfg.SANITIZE_DOM !== false;
    SANITIZE_NAMED_PROPS = cfg.SANITIZE_NAMED_PROPS || false;
    KEEP_CONTENT = cfg.KEEP_CONTENT !== false;
    IN_PLACE = cfg.IN_PLACE || false;
    IS_ALLOWED_URI$1 = cfg.ALLOWED_URI_REGEXP || IS_ALLOWED_URI;
    NAMESPACE = cfg.NAMESPACE || HTML_NAMESPACE;
    CUSTOM_ELEMENT_HANDLING = cfg.CUSTOM_ELEMENT_HANDLING || {};
    if (cfg.CUSTOM_ELEMENT_HANDLING && isRegexOrFunction(cfg.CUSTOM_ELEMENT_HANDLING.tagNameCheck)) {
      CUSTOM_ELEMENT_HANDLING.tagNameCheck = cfg.CUSTOM_ELEMENT_HANDLING.tagNameCheck;
    }
    if (cfg.CUSTOM_ELEMENT_HANDLING && isRegexOrFunction(cfg.CUSTOM_ELEMENT_HANDLING.attributeNameCheck)) {
      CUSTOM_ELEMENT_HANDLING.attributeNameCheck = cfg.CUSTOM_ELEMENT_HANDLING.attributeNameCheck;
    }
    if (cfg.CUSTOM_ELEMENT_HANDLING && typeof cfg.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements === "boolean") {
      CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements = cfg.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements;
    }
    if (SAFE_FOR_TEMPLATES) {
      ALLOW_DATA_ATTR = false;
    }
    if (RETURN_DOM_FRAGMENT) {
      RETURN_DOM = true;
    }
    if (USE_PROFILES) {
      ALLOWED_TAGS = addToSet({}, [...text]);
      ALLOWED_ATTR = [];
      if (USE_PROFILES.html === true) {
        addToSet(ALLOWED_TAGS, html$1);
        addToSet(ALLOWED_ATTR, html);
      }
      if (USE_PROFILES.svg === true) {
        addToSet(ALLOWED_TAGS, svg$1);
        addToSet(ALLOWED_ATTR, svg);
        addToSet(ALLOWED_ATTR, xml);
      }
      if (USE_PROFILES.svgFilters === true) {
        addToSet(ALLOWED_TAGS, svgFilters);
        addToSet(ALLOWED_ATTR, svg);
        addToSet(ALLOWED_ATTR, xml);
      }
      if (USE_PROFILES.mathMl === true) {
        addToSet(ALLOWED_TAGS, mathMl$1);
        addToSet(ALLOWED_ATTR, mathMl);
        addToSet(ALLOWED_ATTR, xml);
      }
    }
    if (cfg.ADD_TAGS) {
      if (ALLOWED_TAGS === DEFAULT_ALLOWED_TAGS) {
        ALLOWED_TAGS = clone(ALLOWED_TAGS);
      }
      addToSet(ALLOWED_TAGS, cfg.ADD_TAGS, transformCaseFunc);
    }
    if (cfg.ADD_ATTR) {
      if (ALLOWED_ATTR === DEFAULT_ALLOWED_ATTR) {
        ALLOWED_ATTR = clone(ALLOWED_ATTR);
      }
      addToSet(ALLOWED_ATTR, cfg.ADD_ATTR, transformCaseFunc);
    }
    if (cfg.ADD_URI_SAFE_ATTR) {
      addToSet(URI_SAFE_ATTRIBUTES, cfg.ADD_URI_SAFE_ATTR, transformCaseFunc);
    }
    if (cfg.FORBID_CONTENTS) {
      if (FORBID_CONTENTS === DEFAULT_FORBID_CONTENTS) {
        FORBID_CONTENTS = clone(FORBID_CONTENTS);
      }
      addToSet(FORBID_CONTENTS, cfg.FORBID_CONTENTS, transformCaseFunc);
    }
    if (KEEP_CONTENT) {
      ALLOWED_TAGS["#text"] = true;
    }
    if (WHOLE_DOCUMENT) {
      addToSet(ALLOWED_TAGS, ["html", "head", "body"]);
    }
    if (ALLOWED_TAGS.table) {
      addToSet(ALLOWED_TAGS, ["tbody"]);
      delete FORBID_TAGS.tbody;
    }
    if (cfg.TRUSTED_TYPES_POLICY) {
      if (typeof cfg.TRUSTED_TYPES_POLICY.createHTML !== "function") {
        throw typeErrorCreate('TRUSTED_TYPES_POLICY configuration option must provide a "createHTML" hook.');
      }
      if (typeof cfg.TRUSTED_TYPES_POLICY.createScriptURL !== "function") {
        throw typeErrorCreate('TRUSTED_TYPES_POLICY configuration option must provide a "createScriptURL" hook.');
      }
      trustedTypesPolicy = cfg.TRUSTED_TYPES_POLICY;
      emptyHTML = trustedTypesPolicy.createHTML("");
    } else {
      if (trustedTypesPolicy === void 0) {
        trustedTypesPolicy = _createTrustedTypesPolicy(trustedTypes, currentScript);
      }
      if (trustedTypesPolicy !== null && typeof emptyHTML === "string") {
        emptyHTML = trustedTypesPolicy.createHTML("");
      }
    }
    if (freeze) {
      freeze(cfg);
    }
    CONFIG = cfg;
  };
  const MATHML_TEXT_INTEGRATION_POINTS = addToSet({}, ["mi", "mo", "mn", "ms", "mtext"]);
  const HTML_INTEGRATION_POINTS = addToSet({}, ["foreignobject", "desc", "title", "annotation-xml"]);
  const COMMON_SVG_AND_HTML_ELEMENTS = addToSet({}, ["title", "style", "font", "a", "script"]);
  const ALL_SVG_TAGS = addToSet({}, svg$1);
  addToSet(ALL_SVG_TAGS, svgFilters);
  addToSet(ALL_SVG_TAGS, svgDisallowed);
  const ALL_MATHML_TAGS = addToSet({}, mathMl$1);
  addToSet(ALL_MATHML_TAGS, mathMlDisallowed);
  const _checkValidNamespace = function _checkValidNamespace2(element) {
    let parent = getParentNode(element);
    if (!parent || !parent.tagName) {
      parent = {
        namespaceURI: NAMESPACE,
        tagName: "template"
      };
    }
    const tagName = stringToLowerCase(element.tagName);
    const parentTagName = stringToLowerCase(parent.tagName);
    if (!ALLOWED_NAMESPACES[element.namespaceURI]) {
      return false;
    }
    if (element.namespaceURI === SVG_NAMESPACE) {
      if (parent.namespaceURI === HTML_NAMESPACE) {
        return tagName === "svg";
      }
      if (parent.namespaceURI === MATHML_NAMESPACE) {
        return tagName === "svg" && (parentTagName === "annotation-xml" || MATHML_TEXT_INTEGRATION_POINTS[parentTagName]);
      }
      return Boolean(ALL_SVG_TAGS[tagName]);
    }
    if (element.namespaceURI === MATHML_NAMESPACE) {
      if (parent.namespaceURI === HTML_NAMESPACE) {
        return tagName === "math";
      }
      if (parent.namespaceURI === SVG_NAMESPACE) {
        return tagName === "math" && HTML_INTEGRATION_POINTS[parentTagName];
      }
      return Boolean(ALL_MATHML_TAGS[tagName]);
    }
    if (element.namespaceURI === HTML_NAMESPACE) {
      if (parent.namespaceURI === SVG_NAMESPACE && !HTML_INTEGRATION_POINTS[parentTagName]) {
        return false;
      }
      if (parent.namespaceURI === MATHML_NAMESPACE && !MATHML_TEXT_INTEGRATION_POINTS[parentTagName]) {
        return false;
      }
      return !ALL_MATHML_TAGS[tagName] && (COMMON_SVG_AND_HTML_ELEMENTS[tagName] || !ALL_SVG_TAGS[tagName]);
    }
    if (PARSER_MEDIA_TYPE === "application/xhtml+xml" && ALLOWED_NAMESPACES[element.namespaceURI]) {
      return true;
    }
    return false;
  };
  const _forceRemove = function _forceRemove2(node2) {
    arrayPush(DOMPurify.removed, {
      element: node2
    });
    try {
      node2.parentNode.removeChild(node2);
    } catch (_2) {
      node2.remove();
    }
  };
  const _removeAttribute = function _removeAttribute2(name, node2) {
    try {
      arrayPush(DOMPurify.removed, {
        attribute: node2.getAttributeNode(name),
        from: node2
      });
    } catch (_2) {
      arrayPush(DOMPurify.removed, {
        attribute: null,
        from: node2
      });
    }
    node2.removeAttribute(name);
    if (name === "is" && !ALLOWED_ATTR[name]) {
      if (RETURN_DOM || RETURN_DOM_FRAGMENT) {
        try {
          _forceRemove(node2);
        } catch (_2) {
        }
      } else {
        try {
          node2.setAttribute(name, "");
        } catch (_2) {
        }
      }
    }
  };
  const _initDocument = function _initDocument2(dirty) {
    let doc;
    let leadingWhitespace;
    if (FORCE_BODY) {
      dirty = "<remove></remove>" + dirty;
    } else {
      const matches = stringMatch(dirty, /^[\r\n\t ]+/);
      leadingWhitespace = matches && matches[0];
    }
    if (PARSER_MEDIA_TYPE === "application/xhtml+xml" && NAMESPACE === HTML_NAMESPACE) {
      dirty = '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>' + dirty + "</body></html>";
    }
    const dirtyPayload = trustedTypesPolicy ? trustedTypesPolicy.createHTML(dirty) : dirty;
    if (NAMESPACE === HTML_NAMESPACE) {
      try {
        doc = new DOMParser().parseFromString(dirtyPayload, PARSER_MEDIA_TYPE);
      } catch (_2) {
      }
    }
    if (!doc || !doc.documentElement) {
      doc = implementation.createDocument(NAMESPACE, "template", null);
      try {
        doc.documentElement.innerHTML = IS_EMPTY_INPUT ? emptyHTML : dirtyPayload;
      } catch (_2) {
      }
    }
    const body = doc.body || doc.documentElement;
    if (dirty && leadingWhitespace) {
      body.insertBefore(document2.createTextNode(leadingWhitespace), body.childNodes[0] || null);
    }
    if (NAMESPACE === HTML_NAMESPACE) {
      return getElementsByTagName.call(doc, WHOLE_DOCUMENT ? "html" : "body")[0];
    }
    return WHOLE_DOCUMENT ? doc.documentElement : body;
  };
  const _createIterator = function _createIterator2(root2) {
    return createNodeIterator.call(
      root2.ownerDocument || root2,
      root2,
      // eslint-disable-next-line no-bitwise
      NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_COMMENT | NodeFilter.SHOW_TEXT,
      null,
      false
    );
  };
  const _isClobbered = function _isClobbered2(elm) {
    return elm instanceof HTMLFormElement && (typeof elm.nodeName !== "string" || typeof elm.textContent !== "string" || typeof elm.removeChild !== "function" || !(elm.attributes instanceof NamedNodeMap) || typeof elm.removeAttribute !== "function" || typeof elm.setAttribute !== "function" || typeof elm.namespaceURI !== "string" || typeof elm.insertBefore !== "function" || typeof elm.hasChildNodes !== "function");
  };
  const _isNode = function _isNode2(object) {
    return typeof Node === "object" ? object instanceof Node : object && typeof object === "object" && typeof object.nodeType === "number" && typeof object.nodeName === "string";
  };
  const _executeHook = function _executeHook2(entryPoint, currentNode, data) {
    if (!hooks[entryPoint]) {
      return;
    }
    arrayForEach(hooks[entryPoint], (hook) => {
      hook.call(DOMPurify, currentNode, data, CONFIG);
    });
  };
  const _sanitizeElements = function _sanitizeElements2(currentNode) {
    let content;
    _executeHook("beforeSanitizeElements", currentNode, null);
    if (_isClobbered(currentNode)) {
      _forceRemove(currentNode);
      return true;
    }
    const tagName = transformCaseFunc(currentNode.nodeName);
    _executeHook("uponSanitizeElement", currentNode, {
      tagName,
      allowedTags: ALLOWED_TAGS
    });
    if (currentNode.hasChildNodes() && !_isNode(currentNode.firstElementChild) && (!_isNode(currentNode.content) || !_isNode(currentNode.content.firstElementChild)) && regExpTest(/<[/\w]/g, currentNode.innerHTML) && regExpTest(/<[/\w]/g, currentNode.textContent)) {
      _forceRemove(currentNode);
      return true;
    }
    if (!ALLOWED_TAGS[tagName] || FORBID_TAGS[tagName]) {
      if (!FORBID_TAGS[tagName] && _basicCustomElementTest(tagName)) {
        if (CUSTOM_ELEMENT_HANDLING.tagNameCheck instanceof RegExp && regExpTest(CUSTOM_ELEMENT_HANDLING.tagNameCheck, tagName))
          return false;
        if (CUSTOM_ELEMENT_HANDLING.tagNameCheck instanceof Function && CUSTOM_ELEMENT_HANDLING.tagNameCheck(tagName))
          return false;
      }
      if (KEEP_CONTENT && !FORBID_CONTENTS[tagName]) {
        const parentNode = getParentNode(currentNode) || currentNode.parentNode;
        const childNodes = getChildNodes(currentNode) || currentNode.childNodes;
        if (childNodes && parentNode) {
          const childCount = childNodes.length;
          for (let i = childCount - 1; i >= 0; --i) {
            parentNode.insertBefore(cloneNode(childNodes[i], true), getNextSibling(currentNode));
          }
        }
      }
      _forceRemove(currentNode);
      return true;
    }
    if (currentNode instanceof Element && !_checkValidNamespace(currentNode)) {
      _forceRemove(currentNode);
      return true;
    }
    if ((tagName === "noscript" || tagName === "noembed" || tagName === "noframes") && regExpTest(/<\/no(script|embed|frames)/i, currentNode.innerHTML)) {
      _forceRemove(currentNode);
      return true;
    }
    if (SAFE_FOR_TEMPLATES && currentNode.nodeType === 3) {
      content = currentNode.textContent;
      content = stringReplace(content, MUSTACHE_EXPR2, " ");
      content = stringReplace(content, ERB_EXPR2, " ");
      content = stringReplace(content, TMPLIT_EXPR2, " ");
      if (currentNode.textContent !== content) {
        arrayPush(DOMPurify.removed, {
          element: currentNode.cloneNode()
        });
        currentNode.textContent = content;
      }
    }
    _executeHook("afterSanitizeElements", currentNode, null);
    return false;
  };
  const _isValidAttribute = function _isValidAttribute2(lcTag, lcName, value) {
    if (SANITIZE_DOM && (lcName === "id" || lcName === "name") && (value in document2 || value in formElement)) {
      return false;
    }
    if (ALLOW_DATA_ATTR && !FORBID_ATTR[lcName] && regExpTest(DATA_ATTR2, lcName))
      ;
    else if (ALLOW_ARIA_ATTR && regExpTest(ARIA_ATTR2, lcName))
      ;
    else if (!ALLOWED_ATTR[lcName] || FORBID_ATTR[lcName]) {
      if (
        // First condition does a very basic check if a) it's basically a valid custom element tagname AND
        // b) if the tagName passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
        // and c) if the attribute name passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.attributeNameCheck
        _basicCustomElementTest(lcTag) && (CUSTOM_ELEMENT_HANDLING.tagNameCheck instanceof RegExp && regExpTest(CUSTOM_ELEMENT_HANDLING.tagNameCheck, lcTag) || CUSTOM_ELEMENT_HANDLING.tagNameCheck instanceof Function && CUSTOM_ELEMENT_HANDLING.tagNameCheck(lcTag)) && (CUSTOM_ELEMENT_HANDLING.attributeNameCheck instanceof RegExp && regExpTest(CUSTOM_ELEMENT_HANDLING.attributeNameCheck, lcName) || CUSTOM_ELEMENT_HANDLING.attributeNameCheck instanceof Function && CUSTOM_ELEMENT_HANDLING.attributeNameCheck(lcName)) || // Alternative, second condition checks if it's an `is`-attribute, AND
        // the value passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
        lcName === "is" && CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements && (CUSTOM_ELEMENT_HANDLING.tagNameCheck instanceof RegExp && regExpTest(CUSTOM_ELEMENT_HANDLING.tagNameCheck, value) || CUSTOM_ELEMENT_HANDLING.tagNameCheck instanceof Function && CUSTOM_ELEMENT_HANDLING.tagNameCheck(value))
      )
        ;
      else {
        return false;
      }
    } else if (URI_SAFE_ATTRIBUTES[lcName])
      ;
    else if (regExpTest(IS_ALLOWED_URI$1, stringReplace(value, ATTR_WHITESPACE2, "")))
      ;
    else if ((lcName === "src" || lcName === "xlink:href" || lcName === "href") && lcTag !== "script" && stringIndexOf(value, "data:") === 0 && DATA_URI_TAGS[lcTag])
      ;
    else if (ALLOW_UNKNOWN_PROTOCOLS && !regExpTest(IS_SCRIPT_OR_DATA2, stringReplace(value, ATTR_WHITESPACE2, "")))
      ;
    else if (value) {
      return false;
    } else
      ;
    return true;
  };
  const _basicCustomElementTest = function _basicCustomElementTest2(tagName) {
    return tagName.indexOf("-") > 0;
  };
  const _sanitizeAttributes = function _sanitizeAttributes2(currentNode) {
    let attr;
    let value;
    let lcName;
    let l;
    _executeHook("beforeSanitizeAttributes", currentNode, null);
    const {
      attributes
    } = currentNode;
    if (!attributes) {
      return;
    }
    const hookEvent = {
      attrName: "",
      attrValue: "",
      keepAttr: true,
      allowedAttributes: ALLOWED_ATTR
    };
    l = attributes.length;
    while (l--) {
      attr = attributes[l];
      const {
        name,
        namespaceURI
      } = attr;
      value = name === "value" ? attr.value : stringTrim(attr.value);
      lcName = transformCaseFunc(name);
      hookEvent.attrName = lcName;
      hookEvent.attrValue = value;
      hookEvent.keepAttr = true;
      hookEvent.forceKeepAttr = void 0;
      _executeHook("uponSanitizeAttribute", currentNode, hookEvent);
      value = hookEvent.attrValue;
      if (hookEvent.forceKeepAttr) {
        continue;
      }
      _removeAttribute(name, currentNode);
      if (!hookEvent.keepAttr) {
        continue;
      }
      if (!ALLOW_SELF_CLOSE_IN_ATTR && regExpTest(/\/>/i, value)) {
        _removeAttribute(name, currentNode);
        continue;
      }
      if (SAFE_FOR_TEMPLATES) {
        value = stringReplace(value, MUSTACHE_EXPR2, " ");
        value = stringReplace(value, ERB_EXPR2, " ");
        value = stringReplace(value, TMPLIT_EXPR2, " ");
      }
      const lcTag = transformCaseFunc(currentNode.nodeName);
      if (!_isValidAttribute(lcTag, lcName, value)) {
        continue;
      }
      if (SANITIZE_NAMED_PROPS && (lcName === "id" || lcName === "name")) {
        _removeAttribute(name, currentNode);
        value = SANITIZE_NAMED_PROPS_PREFIX + value;
      }
      if (trustedTypesPolicy && typeof trustedTypes === "object" && typeof trustedTypes.getAttributeType === "function") {
        if (namespaceURI)
          ;
        else {
          switch (trustedTypes.getAttributeType(lcTag, lcName)) {
            case "TrustedHTML": {
              value = trustedTypesPolicy.createHTML(value);
              break;
            }
            case "TrustedScriptURL": {
              value = trustedTypesPolicy.createScriptURL(value);
              break;
            }
          }
        }
      }
      try {
        if (namespaceURI) {
          currentNode.setAttributeNS(namespaceURI, name, value);
        } else {
          currentNode.setAttribute(name, value);
        }
        arrayPop(DOMPurify.removed);
      } catch (_2) {
      }
    }
    _executeHook("afterSanitizeAttributes", currentNode, null);
  };
  const _sanitizeShadowDOM = function _sanitizeShadowDOM2(fragment) {
    let shadowNode;
    const shadowIterator = _createIterator(fragment);
    _executeHook("beforeSanitizeShadowDOM", fragment, null);
    while (shadowNode = shadowIterator.nextNode()) {
      _executeHook("uponSanitizeShadowNode", shadowNode, null);
      if (_sanitizeElements(shadowNode)) {
        continue;
      }
      if (shadowNode.content instanceof DocumentFragment) {
        _sanitizeShadowDOM2(shadowNode.content);
      }
      _sanitizeAttributes(shadowNode);
    }
    _executeHook("afterSanitizeShadowDOM", fragment, null);
  };
  DOMPurify.sanitize = function(dirty) {
    let cfg = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {};
    let body;
    let importedNode;
    let currentNode;
    let returnNode;
    IS_EMPTY_INPUT = !dirty;
    if (IS_EMPTY_INPUT) {
      dirty = "<!-->";
    }
    if (typeof dirty !== "string" && !_isNode(dirty)) {
      if (typeof dirty.toString === "function") {
        dirty = dirty.toString();
        if (typeof dirty !== "string") {
          throw typeErrorCreate("dirty is not a string, aborting");
        }
      } else {
        throw typeErrorCreate("toString is not a function");
      }
    }
    if (!DOMPurify.isSupported) {
      return dirty;
    }
    if (!SET_CONFIG) {
      _parseConfig(cfg);
    }
    DOMPurify.removed = [];
    if (typeof dirty === "string") {
      IN_PLACE = false;
    }
    if (IN_PLACE) {
      if (dirty.nodeName) {
        const tagName = transformCaseFunc(dirty.nodeName);
        if (!ALLOWED_TAGS[tagName] || FORBID_TAGS[tagName]) {
          throw typeErrorCreate("root node is forbidden and cannot be sanitized in-place");
        }
      }
    } else if (dirty instanceof Node) {
      body = _initDocument("<!---->");
      importedNode = body.ownerDocument.importNode(dirty, true);
      if (importedNode.nodeType === 1 && importedNode.nodeName === "BODY") {
        body = importedNode;
      } else if (importedNode.nodeName === "HTML") {
        body = importedNode;
      } else {
        body.appendChild(importedNode);
      }
    } else {
      if (!RETURN_DOM && !SAFE_FOR_TEMPLATES && !WHOLE_DOCUMENT && // eslint-disable-next-line unicorn/prefer-includes
      dirty.indexOf("<") === -1) {
        return trustedTypesPolicy && RETURN_TRUSTED_TYPE ? trustedTypesPolicy.createHTML(dirty) : dirty;
      }
      body = _initDocument(dirty);
      if (!body) {
        return RETURN_DOM ? null : RETURN_TRUSTED_TYPE ? emptyHTML : "";
      }
    }
    if (body && FORCE_BODY) {
      _forceRemove(body.firstChild);
    }
    const nodeIterator = _createIterator(IN_PLACE ? dirty : body);
    while (currentNode = nodeIterator.nextNode()) {
      if (_sanitizeElements(currentNode)) {
        continue;
      }
      if (currentNode.content instanceof DocumentFragment) {
        _sanitizeShadowDOM(currentNode.content);
      }
      _sanitizeAttributes(currentNode);
    }
    if (IN_PLACE) {
      return dirty;
    }
    if (RETURN_DOM) {
      if (RETURN_DOM_FRAGMENT) {
        returnNode = createDocumentFragment.call(body.ownerDocument);
        while (body.firstChild) {
          returnNode.appendChild(body.firstChild);
        }
      } else {
        returnNode = body;
      }
      if (ALLOWED_ATTR.shadowroot || ALLOWED_ATTR.shadowrootmode) {
        returnNode = importNode.call(originalDocument, returnNode, true);
      }
      return returnNode;
    }
    let serializedHTML = WHOLE_DOCUMENT ? body.outerHTML : body.innerHTML;
    if (WHOLE_DOCUMENT && ALLOWED_TAGS["!doctype"] && body.ownerDocument && body.ownerDocument.doctype && body.ownerDocument.doctype.name && regExpTest(DOCTYPE_NAME, body.ownerDocument.doctype.name)) {
      serializedHTML = "<!DOCTYPE " + body.ownerDocument.doctype.name + ">\n" + serializedHTML;
    }
    if (SAFE_FOR_TEMPLATES) {
      serializedHTML = stringReplace(serializedHTML, MUSTACHE_EXPR2, " ");
      serializedHTML = stringReplace(serializedHTML, ERB_EXPR2, " ");
      serializedHTML = stringReplace(serializedHTML, TMPLIT_EXPR2, " ");
    }
    return trustedTypesPolicy && RETURN_TRUSTED_TYPE ? trustedTypesPolicy.createHTML(serializedHTML) : serializedHTML;
  };
  DOMPurify.setConfig = function(cfg) {
    _parseConfig(cfg);
    SET_CONFIG = true;
  };
  DOMPurify.clearConfig = function() {
    CONFIG = null;
    SET_CONFIG = false;
  };
  DOMPurify.isValidAttribute = function(tag, attr, value) {
    if (!CONFIG) {
      _parseConfig({});
    }
    const lcTag = transformCaseFunc(tag);
    const lcName = transformCaseFunc(attr);
    return _isValidAttribute(lcTag, lcName, value);
  };
  DOMPurify.addHook = function(entryPoint, hookFunction) {
    if (typeof hookFunction !== "function") {
      return;
    }
    hooks[entryPoint] = hooks[entryPoint] || [];
    arrayPush(hooks[entryPoint], hookFunction);
  };
  DOMPurify.removeHook = function(entryPoint) {
    if (hooks[entryPoint]) {
      return arrayPop(hooks[entryPoint]);
    }
  };
  DOMPurify.removeHooks = function(entryPoint) {
    if (hooks[entryPoint]) {
      hooks[entryPoint] = [];
    }
  };
  DOMPurify.removeAllHooks = function() {
    hooks = {};
  };
  return DOMPurify;
}
var purify = createDOMPurify();
const lineBreakRegex = /<br\s*\/?>/gi;
const getRows = (s) => {
  if (!s) {
    return [""];
  }
  const str2 = breakToPlaceholder(s).replace(/\\n/g, "#br#");
  return str2.split("#br#");
};
const removeScript = (txt) => {
  return purify.sanitize(txt);
};
const sanitizeMore = (text2, config2) => {
  var _a;
  if (((_a = config2.flowchart) == null ? void 0 : _a.htmlLabels) !== false) {
    const level = config2.securityLevel;
    if (level === "antiscript" || level === "strict") {
      text2 = removeScript(text2);
    } else if (level !== "loose") {
      text2 = breakToPlaceholder(text2);
      text2 = text2.replace(/</g, "&lt;").replace(/>/g, "&gt;");
      text2 = text2.replace(/=/g, "&equals;");
      text2 = placeholderToBreak(text2);
    }
  }
  return text2;
};
const sanitizeText$2 = (text2, config2) => {
  if (!text2) {
    return text2;
  }
  if (config2.dompurifyConfig) {
    text2 = purify.sanitize(sanitizeMore(text2, config2), config2.dompurifyConfig).toString();
  } else {
    text2 = purify.sanitize(sanitizeMore(text2, config2), {
      FORBID_TAGS: ["style"]
    }).toString();
  }
  return text2;
};
const sanitizeTextOrArray = (a, config2) => {
  if (typeof a === "string") {
    return sanitizeText$2(a, config2);
  }
  return a.flat().map((x) => sanitizeText$2(x, config2));
};
const hasBreaks = (text2) => {
  return lineBreakRegex.test(text2);
};
const splitBreaks = (text2) => {
  return text2.split(lineBreakRegex);
};
const placeholderToBreak = (s) => {
  return s.replace(/#br#/g, "<br/>");
};
const breakToPlaceholder = (s) => {
  return s.replace(lineBreakRegex, "#br#");
};
const getUrl = (useAbsolute) => {
  let url = "";
  if (useAbsolute) {
    url = window.location.protocol + "//" + window.location.host + window.location.pathname + window.location.search;
    url = url.replaceAll(/\(/g, "\\(");
    url = url.replaceAll(/\)/g, "\\)");
  }
  return url;
};
const evaluate = (val) => val === false || ["false", "null", "0"].includes(String(val).trim().toLowerCase()) ? false : true;
const getMax = function(...values) {
  const newValues = values.filter((value) => {
    return !isNaN(value);
  });
  return Math.max(...newValues);
};
const getMin = function(...values) {
  const newValues = values.filter((value) => {
    return !isNaN(value);
  });
  return Math.min(...newValues);
};
const parseGenericTypes = function(input) {
  const inputSets = input.split(/(,)/);
  const output = [];
  for (let i = 0; i < inputSets.length; i++) {
    let thisSet = inputSets[i];
    if (thisSet === "," && i > 0 && i + 1 < inputSets.length) {
      const previousSet = inputSets[i - 1];
      const nextSet = inputSets[i + 1];
      if (shouldCombineSets(previousSet, nextSet)) {
        thisSet = previousSet + "," + nextSet;
        i++;
        output.pop();
      }
    }
    output.push(processSet(thisSet));
  }
  return output.join("");
};
const countOccurrence = (string, substring) => {
  return Math.max(0, string.split(substring).length - 1);
};
const shouldCombineSets = (previousSet, nextSet) => {
  const prevCount = countOccurrence(previousSet, "~");
  const nextCount = countOccurrence(nextSet, "~");
  return prevCount === 1 && nextCount === 1;
};
const processSet = (input) => {
  const tildeCount = countOccurrence(input, "~");
  let hasStartingTilde = false;
  if (tildeCount <= 1) {
    return input;
  }
  if (tildeCount % 2 !== 0 && input.startsWith("~")) {
    input = input.substring(1);
    hasStartingTilde = true;
  }
  const chars = [...input];
  let first = chars.indexOf("~");
  let last = chars.lastIndexOf("~");
  while (first !== -1 && last !== -1 && first !== last) {
    chars[first] = "<";
    chars[last] = ">";
    first = chars.indexOf("~");
    last = chars.lastIndexOf("~");
  }
  if (hasStartingTilde) {
    chars.unshift("~");
  }
  return chars.join("");
};
const common$1 = {
  getRows,
  sanitizeText: sanitizeText$2,
  sanitizeTextOrArray,
  hasBreaks,
  splitBreaks,
  lineBreakRegex,
  removeScript,
  getUrl,
  evaluate,
  getMax,
  getMin
};
const Channel = {
  /* CLAMP */
  min: {
    r: 0,
    g: 0,
    b: 0,
    s: 0,
    l: 0,
    a: 0
  },
  max: {
    r: 255,
    g: 255,
    b: 255,
    h: 360,
    s: 100,
    l: 100,
    a: 1
  },
  clamp: {
    r: (r) => r >= 255 ? 255 : r < 0 ? 0 : r,
    g: (g) => g >= 255 ? 255 : g < 0 ? 0 : g,
    b: (b) => b >= 255 ? 255 : b < 0 ? 0 : b,
    h: (h) => h % 360,
    s: (s) => s >= 100 ? 100 : s < 0 ? 0 : s,
    l: (l) => l >= 100 ? 100 : l < 0 ? 0 : l,
    a: (a) => a >= 1 ? 1 : a < 0 ? 0 : a
  },
  /* CONVERSION */
  //SOURCE: https://planetcalc.com/7779
  toLinear: (c) => {
    const n = c / 255;
    return c > 0.03928 ? Math.pow((n + 0.055) / 1.055, 2.4) : n / 12.92;
  },
  //SOURCE: https://gist.github.com/mjackson/5311256
  hue2rgb: (p, q, t) => {
    if (t < 0)
      t += 1;
    if (t > 1)
      t -= 1;
    if (t < 1 / 6)
      return p + (q - p) * 6 * t;
    if (t < 1 / 2)
      return q;
    if (t < 2 / 3)
      return p + (q - p) * (2 / 3 - t) * 6;
    return p;
  },
  hsl2rgb: ({ h, s, l }, channel2) => {
    if (!s)
      return l * 2.55;
    h /= 360;
    s /= 100;
    l /= 100;
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    switch (channel2) {
      case "r":
        return Channel.hue2rgb(p, q, h + 1 / 3) * 255;
      case "g":
        return Channel.hue2rgb(p, q, h) * 255;
      case "b":
        return Channel.hue2rgb(p, q, h - 1 / 3) * 255;
    }
  },
  rgb2hsl: ({ r, g, b }, channel2) => {
    r /= 255;
    g /= 255;
    b /= 255;
    const max2 = Math.max(r, g, b);
    const min2 = Math.min(r, g, b);
    const l = (max2 + min2) / 2;
    if (channel2 === "l")
      return l * 100;
    if (max2 === min2)
      return 0;
    const d = max2 - min2;
    const s = l > 0.5 ? d / (2 - max2 - min2) : d / (max2 + min2);
    if (channel2 === "s")
      return s * 100;
    switch (max2) {
      case r:
        return ((g - b) / d + (g < b ? 6 : 0)) * 60;
      case g:
        return ((b - r) / d + 2) * 60;
      case b:
        return ((r - g) / d + 4) * 60;
      default:
        return -1;
    }
  }
};
const channel = Channel;
const Lang = {
  /* API */
  clamp: (number, lower2, upper) => {
    if (lower2 > upper)
      return Math.min(lower2, Math.max(upper, number));
    return Math.min(upper, Math.max(lower2, number));
  },
  round: (number) => {
    return Math.round(number * 1e10) / 1e10;
  }
};
const lang = Lang;
const Unit = {
  /* API */
  dec2hex: (dec) => {
    const hex2 = Math.round(dec).toString(16);
    return hex2.length > 1 ? hex2 : `0${hex2}`;
  }
};
const unit = Unit;
const Utils = {
  channel,
  lang,
  unit
};
const _ = Utils;
const DEC2HEX = {};
for (let i = 0; i <= 255; i++)
  DEC2HEX[i] = _.unit.dec2hex(i);
const TYPE = {
  ALL: 0,
  RGB: 1,
  HSL: 2
};
class Type {
  constructor() {
    this.type = TYPE.ALL;
  }
  /* API */
  get() {
    return this.type;
  }
  set(type2) {
    if (this.type && this.type !== type2)
      throw new Error("Cannot change both RGB and HSL channels at the same time");
    this.type = type2;
  }
  reset() {
    this.type = TYPE.ALL;
  }
  is(type2) {
    return this.type === type2;
  }
}
const Type$2 = Type;
class Channels {
  /* CONSTRUCTOR */
  constructor(data, color2) {
    this.color = color2;
    this.changed = false;
    this.data = data;
    this.type = new Type$2();
  }
  /* API */
  set(data, color2) {
    this.color = color2;
    this.changed = false;
    this.data = data;
    this.type.type = TYPE.ALL;
    return this;
  }
  /* HELPERS */
  _ensureHSL() {
    const data = this.data;
    const { h, s, l } = data;
    if (h === void 0)
      data.h = _.channel.rgb2hsl(data, "h");
    if (s === void 0)
      data.s = _.channel.rgb2hsl(data, "s");
    if (l === void 0)
      data.l = _.channel.rgb2hsl(data, "l");
  }
  _ensureRGB() {
    const data = this.data;
    const { r, g, b } = data;
    if (r === void 0)
      data.r = _.channel.hsl2rgb(data, "r");
    if (g === void 0)
      data.g = _.channel.hsl2rgb(data, "g");
    if (b === void 0)
      data.b = _.channel.hsl2rgb(data, "b");
  }
  /* GETTERS */
  get r() {
    const data = this.data;
    const r = data.r;
    if (!this.type.is(TYPE.HSL) && r !== void 0)
      return r;
    this._ensureHSL();
    return _.channel.hsl2rgb(data, "r");
  }
  get g() {
    const data = this.data;
    const g = data.g;
    if (!this.type.is(TYPE.HSL) && g !== void 0)
      return g;
    this._ensureHSL();
    return _.channel.hsl2rgb(data, "g");
  }
  get b() {
    const data = this.data;
    const b = data.b;
    if (!this.type.is(TYPE.HSL) && b !== void 0)
      return b;
    this._ensureHSL();
    return _.channel.hsl2rgb(data, "b");
  }
  get h() {
    const data = this.data;
    const h = data.h;
    if (!this.type.is(TYPE.RGB) && h !== void 0)
      return h;
    this._ensureRGB();
    return _.channel.rgb2hsl(data, "h");
  }
  get s() {
    const data = this.data;
    const s = data.s;
    if (!this.type.is(TYPE.RGB) && s !== void 0)
      return s;
    this._ensureRGB();
    return _.channel.rgb2hsl(data, "s");
  }
  get l() {
    const data = this.data;
    const l = data.l;
    if (!this.type.is(TYPE.RGB) && l !== void 0)
      return l;
    this._ensureRGB();
    return _.channel.rgb2hsl(data, "l");
  }
  get a() {
    return this.data.a;
  }
  /* SETTERS */
  set r(r) {
    this.type.set(TYPE.RGB);
    this.changed = true;
    this.data.r = r;
  }
  set g(g) {
    this.type.set(TYPE.RGB);
    this.changed = true;
    this.data.g = g;
  }
  set b(b) {
    this.type.set(TYPE.RGB);
    this.changed = true;
    this.data.b = b;
  }
  set h(h) {
    this.type.set(TYPE.HSL);
    this.changed = true;
    this.data.h = h;
  }
  set s(s) {
    this.type.set(TYPE.HSL);
    this.changed = true;
    this.data.s = s;
  }
  set l(l) {
    this.type.set(TYPE.HSL);
    this.changed = true;
    this.data.l = l;
  }
  set a(a) {
    this.changed = true;
    this.data.a = a;
  }
}
const Channels$1 = Channels;
const channels = new Channels$1({ r: 0, g: 0, b: 0, a: 0 }, "transparent");
const ChannelsReusable = channels;
const Hex = {
  /* VARIABLES */
  re: /^#((?:[a-f0-9]{2}){2,4}|[a-f0-9]{3})$/i,
  /* API */
  parse: (color2) => {
    if (color2.charCodeAt(0) !== 35)
      return;
    const match = color2.match(Hex.re);
    if (!match)
      return;
    const hex2 = match[1];
    const dec = parseInt(hex2, 16);
    const length2 = hex2.length;
    const hasAlpha = length2 % 4 === 0;
    const isFullLength = length2 > 4;
    const multiplier = isFullLength ? 1 : 17;
    const bits = isFullLength ? 8 : 4;
    const bitsOffset = hasAlpha ? 0 : -1;
    const mask = isFullLength ? 255 : 15;
    return ChannelsReusable.set({
      r: (dec >> bits * (bitsOffset + 3) & mask) * multiplier,
      g: (dec >> bits * (bitsOffset + 2) & mask) * multiplier,
      b: (dec >> bits * (bitsOffset + 1) & mask) * multiplier,
      a: hasAlpha ? (dec & mask) * multiplier / 255 : 1
    }, color2);
  },
  stringify: (channels2) => {
    const { r, g, b, a } = channels2;
    if (a < 1) {
      return `#${DEC2HEX[Math.round(r)]}${DEC2HEX[Math.round(g)]}${DEC2HEX[Math.round(b)]}${DEC2HEX[Math.round(a * 255)]}`;
    } else {
      return `#${DEC2HEX[Math.round(r)]}${DEC2HEX[Math.round(g)]}${DEC2HEX[Math.round(b)]}`;
    }
  }
};
const Hex$1 = Hex;
const HSL = {
  /* VARIABLES */
  re: /^hsla?\(\s*?(-?(?:\d+(?:\.\d+)?|(?:\.\d+))(?:e-?\d+)?(?:deg|grad|rad|turn)?)\s*?(?:,|\s)\s*?(-?(?:\d+(?:\.\d+)?|(?:\.\d+))(?:e-?\d+)?%)\s*?(?:,|\s)\s*?(-?(?:\d+(?:\.\d+)?|(?:\.\d+))(?:e-?\d+)?%)(?:\s*?(?:,|\/)\s*?\+?(-?(?:\d+(?:\.\d+)?|(?:\.\d+))(?:e-?\d+)?(%)?))?\s*?\)$/i,
  hueRe: /^(.+?)(deg|grad|rad|turn)$/i,
  /* HELPERS */
  _hue2deg: (hue2) => {
    const match = hue2.match(HSL.hueRe);
    if (match) {
      const [, number, unit2] = match;
      switch (unit2) {
        case "grad":
          return _.channel.clamp.h(parseFloat(number) * 0.9);
        case "rad":
          return _.channel.clamp.h(parseFloat(number) * 180 / Math.PI);
        case "turn":
          return _.channel.clamp.h(parseFloat(number) * 360);
      }
    }
    return _.channel.clamp.h(parseFloat(hue2));
  },
  /* API */
  parse: (color2) => {
    const charCode = color2.charCodeAt(0);
    if (charCode !== 104 && charCode !== 72)
      return;
    const match = color2.match(HSL.re);
    if (!match)
      return;
    const [, h, s, l, a, isAlphaPercentage] = match;
    return ChannelsReusable.set({
      h: HSL._hue2deg(h),
      s: _.channel.clamp.s(parseFloat(s)),
      l: _.channel.clamp.l(parseFloat(l)),
      a: a ? _.channel.clamp.a(isAlphaPercentage ? parseFloat(a) / 100 : parseFloat(a)) : 1
    }, color2);
  },
  stringify: (channels2) => {
    const { h, s, l, a } = channels2;
    if (a < 1) {
      return `hsla(${_.lang.round(h)}, ${_.lang.round(s)}%, ${_.lang.round(l)}%, ${a})`;
    } else {
      return `hsl(${_.lang.round(h)}, ${_.lang.round(s)}%, ${_.lang.round(l)}%)`;
    }
  }
};
const HSL$1 = HSL;
const Keyword = {
  /* VARIABLES */
  colors: {
    aliceblue: "#f0f8ff",
    antiquewhite: "#faebd7",
    aqua: "#00ffff",
    aquamarine: "#7fffd4",
    azure: "#f0ffff",
    beige: "#f5f5dc",
    bisque: "#ffe4c4",
    black: "#000000",
    blanchedalmond: "#ffebcd",
    blue: "#0000ff",
    blueviolet: "#8a2be2",
    brown: "#a52a2a",
    burlywood: "#deb887",
    cadetblue: "#5f9ea0",
    chartreuse: "#7fff00",
    chocolate: "#d2691e",
    coral: "#ff7f50",
    cornflowerblue: "#6495ed",
    cornsilk: "#fff8dc",
    crimson: "#dc143c",
    cyanaqua: "#00ffff",
    darkblue: "#00008b",
    darkcyan: "#008b8b",
    darkgoldenrod: "#b8860b",
    darkgray: "#a9a9a9",
    darkgreen: "#006400",
    darkgrey: "#a9a9a9",
    darkkhaki: "#bdb76b",
    darkmagenta: "#8b008b",
    darkolivegreen: "#556b2f",
    darkorange: "#ff8c00",
    darkorchid: "#9932cc",
    darkred: "#8b0000",
    darksalmon: "#e9967a",
    darkseagreen: "#8fbc8f",
    darkslateblue: "#483d8b",
    darkslategray: "#2f4f4f",
    darkslategrey: "#2f4f4f",
    darkturquoise: "#00ced1",
    darkviolet: "#9400d3",
    deeppink: "#ff1493",
    deepskyblue: "#00bfff",
    dimgray: "#696969",
    dimgrey: "#696969",
    dodgerblue: "#1e90ff",
    firebrick: "#b22222",
    floralwhite: "#fffaf0",
    forestgreen: "#228b22",
    fuchsia: "#ff00ff",
    gainsboro: "#dcdcdc",
    ghostwhite: "#f8f8ff",
    gold: "#ffd700",
    goldenrod: "#daa520",
    gray: "#808080",
    green: "#008000",
    greenyellow: "#adff2f",
    grey: "#808080",
    honeydew: "#f0fff0",
    hotpink: "#ff69b4",
    indianred: "#cd5c5c",
    indigo: "#4b0082",
    ivory: "#fffff0",
    khaki: "#f0e68c",
    lavender: "#e6e6fa",
    lavenderblush: "#fff0f5",
    lawngreen: "#7cfc00",
    lemonchiffon: "#fffacd",
    lightblue: "#add8e6",
    lightcoral: "#f08080",
    lightcyan: "#e0ffff",
    lightgoldenrodyellow: "#fafad2",
    lightgray: "#d3d3d3",
    lightgreen: "#90ee90",
    lightgrey: "#d3d3d3",
    lightpink: "#ffb6c1",
    lightsalmon: "#ffa07a",
    lightseagreen: "#20b2aa",
    lightskyblue: "#87cefa",
    lightslategray: "#778899",
    lightslategrey: "#778899",
    lightsteelblue: "#b0c4de",
    lightyellow: "#ffffe0",
    lime: "#00ff00",
    limegreen: "#32cd32",
    linen: "#faf0e6",
    magenta: "#ff00ff",
    maroon: "#800000",
    mediumaquamarine: "#66cdaa",
    mediumblue: "#0000cd",
    mediumorchid: "#ba55d3",
    mediumpurple: "#9370db",
    mediumseagreen: "#3cb371",
    mediumslateblue: "#7b68ee",
    mediumspringgreen: "#00fa9a",
    mediumturquoise: "#48d1cc",
    mediumvioletred: "#c71585",
    midnightblue: "#191970",
    mintcream: "#f5fffa",
    mistyrose: "#ffe4e1",
    moccasin: "#ffe4b5",
    navajowhite: "#ffdead",
    navy: "#000080",
    oldlace: "#fdf5e6",
    olive: "#808000",
    olivedrab: "#6b8e23",
    orange: "#ffa500",
    orangered: "#ff4500",
    orchid: "#da70d6",
    palegoldenrod: "#eee8aa",
    palegreen: "#98fb98",
    paleturquoise: "#afeeee",
    palevioletred: "#db7093",
    papayawhip: "#ffefd5",
    peachpuff: "#ffdab9",
    peru: "#cd853f",
    pink: "#ffc0cb",
    plum: "#dda0dd",
    powderblue: "#b0e0e6",
    purple: "#800080",
    rebeccapurple: "#663399",
    red: "#ff0000",
    rosybrown: "#bc8f8f",
    royalblue: "#4169e1",
    saddlebrown: "#8b4513",
    salmon: "#fa8072",
    sandybrown: "#f4a460",
    seagreen: "#2e8b57",
    seashell: "#fff5ee",
    sienna: "#a0522d",
    silver: "#c0c0c0",
    skyblue: "#87ceeb",
    slateblue: "#6a5acd",
    slategray: "#708090",
    slategrey: "#708090",
    snow: "#fffafa",
    springgreen: "#00ff7f",
    tan: "#d2b48c",
    teal: "#008080",
    thistle: "#d8bfd8",
    transparent: "#00000000",
    turquoise: "#40e0d0",
    violet: "#ee82ee",
    wheat: "#f5deb3",
    white: "#ffffff",
    whitesmoke: "#f5f5f5",
    yellow: "#ffff00",
    yellowgreen: "#9acd32"
  },
  /* API */
  parse: (color2) => {
    color2 = color2.toLowerCase();
    const hex2 = Keyword.colors[color2];
    if (!hex2)
      return;
    return Hex$1.parse(hex2);
  },
  stringify: (channels2) => {
    const hex2 = Hex$1.stringify(channels2);
    for (const name in Keyword.colors) {
      if (Keyword.colors[name] === hex2)
        return name;
    }
    return;
  }
};
const Keyword$1 = Keyword;
const RGB = {
  /* VARIABLES */
  re: /^rgba?\(\s*?(-?(?:\d+(?:\.\d+)?|(?:\.\d+))(?:e\d+)?(%?))\s*?(?:,|\s)\s*?(-?(?:\d+(?:\.\d+)?|(?:\.\d+))(?:e\d+)?(%?))\s*?(?:,|\s)\s*?(-?(?:\d+(?:\.\d+)?|(?:\.\d+))(?:e\d+)?(%?))(?:\s*?(?:,|\/)\s*?\+?(-?(?:\d+(?:\.\d+)?|(?:\.\d+))(?:e\d+)?(%?)))?\s*?\)$/i,
  /* API */
  parse: (color2) => {
    const charCode = color2.charCodeAt(0);
    if (charCode !== 114 && charCode !== 82)
      return;
    const match = color2.match(RGB.re);
    if (!match)
      return;
    const [, r, isRedPercentage, g, isGreenPercentage, b, isBluePercentage, a, isAlphaPercentage] = match;
    return ChannelsReusable.set({
      r: _.channel.clamp.r(isRedPercentage ? parseFloat(r) * 2.55 : parseFloat(r)),
      g: _.channel.clamp.g(isGreenPercentage ? parseFloat(g) * 2.55 : parseFloat(g)),
      b: _.channel.clamp.b(isBluePercentage ? parseFloat(b) * 2.55 : parseFloat(b)),
      a: a ? _.channel.clamp.a(isAlphaPercentage ? parseFloat(a) / 100 : parseFloat(a)) : 1
    }, color2);
  },
  stringify: (channels2) => {
    const { r, g, b, a } = channels2;
    if (a < 1) {
      return `rgba(${_.lang.round(r)}, ${_.lang.round(g)}, ${_.lang.round(b)}, ${_.lang.round(a)})`;
    } else {
      return `rgb(${_.lang.round(r)}, ${_.lang.round(g)}, ${_.lang.round(b)})`;
    }
  }
};
const RGB$1 = RGB;
const Color = {
  /* VARIABLES */
  format: {
    keyword: Keyword$1,
    hex: Hex$1,
    rgb: RGB$1,
    rgba: RGB$1,
    hsl: HSL$1,
    hsla: HSL$1
  },
  /* API */
  parse: (color2) => {
    if (typeof color2 !== "string")
      return color2;
    const channels2 = Hex$1.parse(color2) || RGB$1.parse(color2) || HSL$1.parse(color2) || Keyword$1.parse(color2);
    if (channels2)
      return channels2;
    throw new Error(`Unsupported color format: "${color2}"`);
  },
  stringify: (channels2) => {
    if (!channels2.changed && channels2.color)
      return channels2.color;
    if (channels2.type.is(TYPE.HSL) || channels2.data.r === void 0) {
      return HSL$1.stringify(channels2);
    } else if (channels2.a < 1 || !Number.isInteger(channels2.r) || !Number.isInteger(channels2.g) || !Number.isInteger(channels2.b)) {
      return RGB$1.stringify(channels2);
    } else {
      return Hex$1.stringify(channels2);
    }
  }
};
const Color$1 = Color;
const change = (color2, channels2) => {
  const ch = Color$1.parse(color2);
  for (const c in channels2) {
    ch[c] = _.channel.clamp[c](channels2[c]);
  }
  return Color$1.stringify(ch);
};
const change$1 = change;
const rgba = (r, g, b = 0, a = 1) => {
  if (typeof r !== "number")
    return change$1(r, { a: g });
  const channels2 = ChannelsReusable.set({
    r: _.channel.clamp.r(r),
    g: _.channel.clamp.g(g),
    b: _.channel.clamp.b(b),
    a: _.channel.clamp.a(a)
  });
  return Color$1.stringify(channels2);
};
const rgba$1 = rgba;
const luminance = (color2) => {
  const { r, g, b } = Color$1.parse(color2);
  const luminance2 = 0.2126 * _.channel.toLinear(r) + 0.7152 * _.channel.toLinear(g) + 0.0722 * _.channel.toLinear(b);
  return _.lang.round(luminance2);
};
const luminance$1 = luminance;
const isLight = (color2) => {
  return luminance$1(color2) >= 0.5;
};
const isLight$1 = isLight;
const isDark = (color2) => {
  return !isLight$1(color2);
};
const isDark$1 = isDark;
const adjustChannel = (color2, channel2, amount) => {
  const channels2 = Color$1.parse(color2);
  const amountCurrent = channels2[channel2];
  const amountNext = _.channel.clamp[channel2](amountCurrent + amount);
  if (amountCurrent !== amountNext)
    channels2[channel2] = amountNext;
  return Color$1.stringify(channels2);
};
const adjustChannel$1 = adjustChannel;
const lighten = (color2, amount) => {
  return adjustChannel$1(color2, "l", amount);
};
const lighten$1 = lighten;
const darken = (color2, amount) => {
  return adjustChannel$1(color2, "l", -amount);
};
const darken$1 = darken;
const adjust = (color2, channels2) => {
  const ch = Color$1.parse(color2);
  const changes = {};
  for (const c in channels2) {
    if (!channels2[c])
      continue;
    changes[c] = ch[c] + channels2[c];
  }
  return change$1(color2, changes);
};
const adjust$1 = adjust;
const mix = (color1, color2, weight = 50) => {
  const { r: r1, g: g1, b: b1, a: a1 } = Color$1.parse(color1);
  const { r: r2, g: g2, b: b2, a: a2 } = Color$1.parse(color2);
  const weightScale = weight / 100;
  const weightNormalized = weightScale * 2 - 1;
  const alphaDelta = a1 - a2;
  const weight1combined = weightNormalized * alphaDelta === -1 ? weightNormalized : (weightNormalized + alphaDelta) / (1 + weightNormalized * alphaDelta);
  const weight1 = (weight1combined + 1) / 2;
  const weight2 = 1 - weight1;
  const r = r1 * weight1 + r2 * weight2;
  const g = g1 * weight1 + g2 * weight2;
  const b = b1 * weight1 + b2 * weight2;
  const a = a1 * weightScale + a2 * (1 - weightScale);
  return rgba$1(r, g, b, a);
};
const mix$1 = mix;
const invert = (color2, weight = 100) => {
  const inverse = Color$1.parse(color2);
  inverse.r = 255 - inverse.r;
  inverse.g = 255 - inverse.g;
  inverse.b = 255 - inverse.b;
  return mix$1(inverse, color2, weight);
};
const invert$1 = invert;
const mkBorder = (col, darkMode) => darkMode ? adjust$1(col, { s: -40, l: 10 }) : adjust$1(col, { s: -40, l: -10 });
const oldAttributeBackgroundColorOdd = "#ffffff";
const oldAttributeBackgroundColorEven = "#f2f2f2";
let Theme$4 = class Theme {
  constructor() {
    this.background = "#f4f4f4";
    this.primaryColor = "#fff4dd";
    this.noteBkgColor = "#fff5ad";
    this.noteTextColor = "#333";
    this.THEME_COLOR_LIMIT = 12;
    this.fontFamily = '"trebuchet ms", verdana, arial, sans-serif';
    this.fontSize = "16px";
  }
  updateColors() {
    this.primaryTextColor = this.primaryTextColor || (this.darkMode ? "#eee" : "#333");
    this.secondaryColor = this.secondaryColor || adjust$1(this.primaryColor, { h: -120 });
    this.tertiaryColor = this.tertiaryColor || adjust$1(this.primaryColor, { h: 180, l: 5 });
    this.primaryBorderColor = this.primaryBorderColor || mkBorder(this.primaryColor, this.darkMode);
    this.secondaryBorderColor = this.secondaryBorderColor || mkBorder(this.secondaryColor, this.darkMode);
    this.tertiaryBorderColor = this.tertiaryBorderColor || mkBorder(this.tertiaryColor, this.darkMode);
    this.noteBorderColor = this.noteBorderColor || mkBorder(this.noteBkgColor, this.darkMode);
    this.noteBkgColor = this.noteBkgColor || "#fff5ad";
    this.noteTextColor = this.noteTextColor || "#333";
    this.secondaryTextColor = this.secondaryTextColor || invert$1(this.secondaryColor);
    this.tertiaryTextColor = this.tertiaryTextColor || invert$1(this.tertiaryColor);
    this.lineColor = this.lineColor || invert$1(this.background);
    this.arrowheadColor = this.arrowheadColor || invert$1(this.background);
    this.textColor = this.textColor || this.primaryTextColor;
    this.border2 = this.border2 || this.tertiaryBorderColor;
    this.nodeBkg = this.nodeBkg || this.primaryColor;
    this.mainBkg = this.mainBkg || this.primaryColor;
    this.nodeBorder = this.nodeBorder || this.primaryBorderColor;
    this.clusterBkg = this.clusterBkg || this.tertiaryColor;
    this.clusterBorder = this.clusterBorder || this.tertiaryBorderColor;
    this.defaultLinkColor = this.defaultLinkColor || this.lineColor;
    this.titleColor = this.titleColor || this.tertiaryTextColor;
    this.edgeLabelBackground = this.edgeLabelBackground || (this.darkMode ? darken$1(this.secondaryColor, 30) : this.secondaryColor);
    this.nodeTextColor = this.nodeTextColor || this.primaryTextColor;
    this.actorBorder = this.actorBorder || this.primaryBorderColor;
    this.actorBkg = this.actorBkg || this.mainBkg;
    this.actorTextColor = this.actorTextColor || this.primaryTextColor;
    this.actorLineColor = this.actorLineColor || "grey";
    this.labelBoxBkgColor = this.labelBoxBkgColor || this.actorBkg;
    this.signalColor = this.signalColor || this.textColor;
    this.signalTextColor = this.signalTextColor || this.textColor;
    this.labelBoxBorderColor = this.labelBoxBorderColor || this.actorBorder;
    this.labelTextColor = this.labelTextColor || this.actorTextColor;
    this.loopTextColor = this.loopTextColor || this.actorTextColor;
    this.activationBorderColor = this.activationBorderColor || darken$1(this.secondaryColor, 10);
    this.activationBkgColor = this.activationBkgColor || this.secondaryColor;
    this.sequenceNumberColor = this.sequenceNumberColor || invert$1(this.lineColor);
    this.sectionBkgColor = this.sectionBkgColor || this.tertiaryColor;
    this.altSectionBkgColor = this.altSectionBkgColor || "white";
    this.sectionBkgColor = this.sectionBkgColor || this.secondaryColor;
    this.sectionBkgColor2 = this.sectionBkgColor2 || this.primaryColor;
    this.excludeBkgColor = this.excludeBkgColor || "#eeeeee";
    this.taskBorderColor = this.taskBorderColor || this.primaryBorderColor;
    this.taskBkgColor = this.taskBkgColor || this.primaryColor;
    this.activeTaskBorderColor = this.activeTaskBorderColor || this.primaryColor;
    this.activeTaskBkgColor = this.activeTaskBkgColor || lighten$1(this.primaryColor, 23);
    this.gridColor = this.gridColor || "lightgrey";
    this.doneTaskBkgColor = this.doneTaskBkgColor || "lightgrey";
    this.doneTaskBorderColor = this.doneTaskBorderColor || "grey";
    this.critBorderColor = this.critBorderColor || "#ff8888";
    this.critBkgColor = this.critBkgColor || "red";
    this.todayLineColor = this.todayLineColor || "red";
    this.taskTextColor = this.taskTextColor || this.textColor;
    this.taskTextOutsideColor = this.taskTextOutsideColor || this.textColor;
    this.taskTextLightColor = this.taskTextLightColor || this.textColor;
    this.taskTextColor = this.taskTextColor || this.primaryTextColor;
    this.taskTextDarkColor = this.taskTextDarkColor || this.textColor;
    this.taskTextClickableColor = this.taskTextClickableColor || "#003163";
    this.personBorder = this.personBorder || this.primaryBorderColor;
    this.personBkg = this.personBkg || this.mainBkg;
    this.transitionColor = this.transitionColor || this.lineColor;
    this.transitionLabelColor = this.transitionLabelColor || this.textColor;
    this.stateLabelColor = this.stateLabelColor || this.stateBkg || this.primaryTextColor;
    this.stateBkg = this.stateBkg || this.mainBkg;
    this.labelBackgroundColor = this.labelBackgroundColor || this.stateBkg;
    this.compositeBackground = this.compositeBackground || this.background || this.tertiaryColor;
    this.altBackground = this.altBackground || this.tertiaryColor;
    this.compositeTitleBackground = this.compositeTitleBackground || this.mainBkg;
    this.compositeBorder = this.compositeBorder || this.nodeBorder;
    this.innerEndBackground = this.nodeBorder;
    this.errorBkgColor = this.errorBkgColor || this.tertiaryColor;
    this.errorTextColor = this.errorTextColor || this.tertiaryTextColor;
    this.transitionColor = this.transitionColor || this.lineColor;
    this.specialStateColor = this.lineColor;
    this.cScale0 = this.cScale0 || this.primaryColor;
    this.cScale1 = this.cScale1 || this.secondaryColor;
    this.cScale2 = this.cScale2 || this.tertiaryColor;
    this.cScale3 = this.cScale3 || adjust$1(this.primaryColor, { h: 30 });
    this.cScale4 = this.cScale4 || adjust$1(this.primaryColor, { h: 60 });
    this.cScale5 = this.cScale5 || adjust$1(this.primaryColor, { h: 90 });
    this.cScale6 = this.cScale6 || adjust$1(this.primaryColor, { h: 120 });
    this.cScale7 = this.cScale7 || adjust$1(this.primaryColor, { h: 150 });
    this.cScale8 = this.cScale8 || adjust$1(this.primaryColor, { h: 210, l: 150 });
    this.cScale9 = this.cScale9 || adjust$1(this.primaryColor, { h: 270 });
    this.cScale10 = this.cScale10 || adjust$1(this.primaryColor, { h: 300 });
    this.cScale11 = this.cScale11 || adjust$1(this.primaryColor, { h: 330 });
    if (this.darkMode) {
      for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
        this["cScale" + i] = darken$1(this["cScale" + i], 75);
      }
    } else {
      for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
        this["cScale" + i] = darken$1(this["cScale" + i], 25);
      }
    }
    for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
      this["cScaleInv" + i] = this["cScaleInv" + i] || invert$1(this["cScale" + i]);
    }
    for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
      if (this.darkMode) {
        this["cScalePeer" + i] = this["cScalePeer" + i] || lighten$1(this["cScale" + i], 10);
      } else {
        this["cScalePeer" + i] = this["cScalePeer" + i] || darken$1(this["cScale" + i], 10);
      }
    }
    this.scaleLabelColor = this.scaleLabelColor || this.labelTextColor;
    for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
      this["cScaleLabel" + i] = this["cScaleLabel" + i] || this.scaleLabelColor;
    }
    const multiplier = this.darkMode ? -4 : -1;
    for (let i = 0; i < 5; i++) {
      this["surface" + i] = this["surface" + i] || adjust$1(this.mainBkg, { h: 180, s: -15, l: multiplier * (5 + i * 3) });
      this["surfacePeer" + i] = this["surfacePeer" + i] || adjust$1(this.mainBkg, { h: 180, s: -15, l: multiplier * (8 + i * 3) });
    }
    this.classText = this.classText || this.textColor;
    this.fillType0 = this.fillType0 || this.primaryColor;
    this.fillType1 = this.fillType1 || this.secondaryColor;
    this.fillType2 = this.fillType2 || adjust$1(this.primaryColor, { h: 64 });
    this.fillType3 = this.fillType3 || adjust$1(this.secondaryColor, { h: 64 });
    this.fillType4 = this.fillType4 || adjust$1(this.primaryColor, { h: -64 });
    this.fillType5 = this.fillType5 || adjust$1(this.secondaryColor, { h: -64 });
    this.fillType6 = this.fillType6 || adjust$1(this.primaryColor, { h: 128 });
    this.fillType7 = this.fillType7 || adjust$1(this.secondaryColor, { h: 128 });
    this.pie1 = this.pie1 || this.primaryColor;
    this.pie2 = this.pie2 || this.secondaryColor;
    this.pie3 = this.pie3 || this.tertiaryColor;
    this.pie4 = this.pie4 || adjust$1(this.primaryColor, { l: -10 });
    this.pie5 = this.pie5 || adjust$1(this.secondaryColor, { l: -10 });
    this.pie6 = this.pie6 || adjust$1(this.tertiaryColor, { l: -10 });
    this.pie7 = this.pie7 || adjust$1(this.primaryColor, { h: 60, l: -10 });
    this.pie8 = this.pie8 || adjust$1(this.primaryColor, { h: -60, l: -10 });
    this.pie9 = this.pie9 || adjust$1(this.primaryColor, { h: 120, l: 0 });
    this.pie10 = this.pie10 || adjust$1(this.primaryColor, { h: 60, l: -20 });
    this.pie11 = this.pie11 || adjust$1(this.primaryColor, { h: -60, l: -20 });
    this.pie12 = this.pie12 || adjust$1(this.primaryColor, { h: 120, l: -10 });
    this.pieTitleTextSize = this.pieTitleTextSize || "25px";
    this.pieTitleTextColor = this.pieTitleTextColor || this.taskTextDarkColor;
    this.pieSectionTextSize = this.pieSectionTextSize || "17px";
    this.pieSectionTextColor = this.pieSectionTextColor || this.textColor;
    this.pieLegendTextSize = this.pieLegendTextSize || "17px";
    this.pieLegendTextColor = this.pieLegendTextColor || this.taskTextDarkColor;
    this.pieStrokeColor = this.pieStrokeColor || "black";
    this.pieStrokeWidth = this.pieStrokeWidth || "2px";
    this.pieOuterStrokeWidth = this.pieOuterStrokeWidth || "2px";
    this.pieOuterStrokeColor = this.pieOuterStrokeColor || "black";
    this.pieOpacity = this.pieOpacity || "0.7";
    this.quadrant1Fill = this.quadrant1Fill || this.primaryColor;
    this.quadrant2Fill = this.quadrant2Fill || adjust$1(this.primaryColor, { r: 5, g: 5, b: 5 });
    this.quadrant3Fill = this.quadrant3Fill || adjust$1(this.primaryColor, { r: 10, g: 10, b: 10 });
    this.quadrant4Fill = this.quadrant4Fill || adjust$1(this.primaryColor, { r: 15, g: 15, b: 15 });
    this.quadrant1TextFill = this.quadrant1TextFill || this.primaryTextColor;
    this.quadrant2TextFill = this.quadrant2TextFill || adjust$1(this.primaryTextColor, { r: -5, g: -5, b: -5 });
    this.quadrant3TextFill = this.quadrant3TextFill || adjust$1(this.primaryTextColor, { r: -10, g: -10, b: -10 });
    this.quadrant4TextFill = this.quadrant4TextFill || adjust$1(this.primaryTextColor, { r: -15, g: -15, b: -15 });
    this.quadrantPointFill = this.quadrantPointFill || isDark$1(this.quadrant1Fill) ? lighten$1(this.quadrant1Fill) : darken$1(this.quadrant1Fill);
    this.quadrantPointTextFill = this.quadrantPointTextFill || this.primaryTextColor;
    this.quadrantXAxisTextFill = this.quadrantXAxisTextFill || this.primaryTextColor;
    this.quadrantYAxisTextFill = this.quadrantYAxisTextFill || this.primaryTextColor;
    this.quadrantInternalBorderStrokeFill = this.quadrantInternalBorderStrokeFill || this.primaryBorderColor;
    this.quadrantExternalBorderStrokeFill = this.quadrantExternalBorderStrokeFill || this.primaryBorderColor;
    this.quadrantTitleFill = this.quadrantTitleFill || this.primaryTextColor;
    this.requirementBackground = this.requirementBackground || this.primaryColor;
    this.requirementBorderColor = this.requirementBorderColor || this.primaryBorderColor;
    this.requirementBorderSize = this.requirementBorderSize || "1";
    this.requirementTextColor = this.requirementTextColor || this.primaryTextColor;
    this.relationColor = this.relationColor || this.lineColor;
    this.relationLabelBackground = this.relationLabelBackground || (this.darkMode ? darken$1(this.secondaryColor, 30) : this.secondaryColor);
    this.relationLabelColor = this.relationLabelColor || this.actorTextColor;
    this.git0 = this.git0 || this.primaryColor;
    this.git1 = this.git1 || this.secondaryColor;
    this.git2 = this.git2 || this.tertiaryColor;
    this.git3 = this.git3 || adjust$1(this.primaryColor, { h: -30 });
    this.git4 = this.git4 || adjust$1(this.primaryColor, { h: -60 });
    this.git5 = this.git5 || adjust$1(this.primaryColor, { h: -90 });
    this.git6 = this.git6 || adjust$1(this.primaryColor, { h: 60 });
    this.git7 = this.git7 || adjust$1(this.primaryColor, { h: 120 });
    if (this.darkMode) {
      this.git0 = lighten$1(this.git0, 25);
      this.git1 = lighten$1(this.git1, 25);
      this.git2 = lighten$1(this.git2, 25);
      this.git3 = lighten$1(this.git3, 25);
      this.git4 = lighten$1(this.git4, 25);
      this.git5 = lighten$1(this.git5, 25);
      this.git6 = lighten$1(this.git6, 25);
      this.git7 = lighten$1(this.git7, 25);
    } else {
      this.git0 = darken$1(this.git0, 25);
      this.git1 = darken$1(this.git1, 25);
      this.git2 = darken$1(this.git2, 25);
      this.git3 = darken$1(this.git3, 25);
      this.git4 = darken$1(this.git4, 25);
      this.git5 = darken$1(this.git5, 25);
      this.git6 = darken$1(this.git6, 25);
      this.git7 = darken$1(this.git7, 25);
    }
    this.gitInv0 = this.gitInv0 || invert$1(this.git0);
    this.gitInv1 = this.gitInv1 || invert$1(this.git1);
    this.gitInv2 = this.gitInv2 || invert$1(this.git2);
    this.gitInv3 = this.gitInv3 || invert$1(this.git3);
    this.gitInv4 = this.gitInv4 || invert$1(this.git4);
    this.gitInv5 = this.gitInv5 || invert$1(this.git5);
    this.gitInv6 = this.gitInv6 || invert$1(this.git6);
    this.gitInv7 = this.gitInv7 || invert$1(this.git7);
    this.branchLabelColor = this.branchLabelColor || (this.darkMode ? "black" : this.labelTextColor);
    this.gitBranchLabel0 = this.gitBranchLabel0 || this.branchLabelColor;
    this.gitBranchLabel1 = this.gitBranchLabel1 || this.branchLabelColor;
    this.gitBranchLabel2 = this.gitBranchLabel2 || this.branchLabelColor;
    this.gitBranchLabel3 = this.gitBranchLabel3 || this.branchLabelColor;
    this.gitBranchLabel4 = this.gitBranchLabel4 || this.branchLabelColor;
    this.gitBranchLabel5 = this.gitBranchLabel5 || this.branchLabelColor;
    this.gitBranchLabel6 = this.gitBranchLabel6 || this.branchLabelColor;
    this.gitBranchLabel7 = this.gitBranchLabel7 || this.branchLabelColor;
    this.tagLabelColor = this.tagLabelColor || this.primaryTextColor;
    this.tagLabelBackground = this.tagLabelBackground || this.primaryColor;
    this.tagLabelBorder = this.tagBorder || this.primaryBorderColor;
    this.tagLabelFontSize = this.tagLabelFontSize || "10px";
    this.commitLabelColor = this.commitLabelColor || this.secondaryTextColor;
    this.commitLabelBackground = this.commitLabelBackground || this.secondaryColor;
    this.commitLabelFontSize = this.commitLabelFontSize || "10px";
    this.attributeBackgroundColorOdd = this.attributeBackgroundColorOdd || oldAttributeBackgroundColorOdd;
    this.attributeBackgroundColorEven = this.attributeBackgroundColorEven || oldAttributeBackgroundColorEven;
  }
  calculate(overrides) {
    if (typeof overrides !== "object") {
      this.updateColors();
      return;
    }
    const keys = Object.keys(overrides);
    keys.forEach((k) => {
      this[k] = overrides[k];
    });
    this.updateColors();
    keys.forEach((k) => {
      this[k] = overrides[k];
    });
  }
};
const getThemeVariables$4 = (userOverrides) => {
  const theme2 = new Theme$4();
  theme2.calculate(userOverrides);
  return theme2;
};
let Theme$3 = class Theme2 {
  constructor() {
    this.background = "#333";
    this.primaryColor = "#1f2020";
    this.secondaryColor = lighten$1(this.primaryColor, 16);
    this.tertiaryColor = adjust$1(this.primaryColor, { h: -160 });
    this.primaryBorderColor = invert$1(this.background);
    this.secondaryBorderColor = mkBorder(this.secondaryColor, this.darkMode);
    this.tertiaryBorderColor = mkBorder(this.tertiaryColor, this.darkMode);
    this.primaryTextColor = invert$1(this.primaryColor);
    this.secondaryTextColor = invert$1(this.secondaryColor);
    this.tertiaryTextColor = invert$1(this.tertiaryColor);
    this.lineColor = invert$1(this.background);
    this.textColor = invert$1(this.background);
    this.mainBkg = "#1f2020";
    this.secondBkg = "calculated";
    this.mainContrastColor = "lightgrey";
    this.darkTextColor = lighten$1(invert$1("#323D47"), 10);
    this.lineColor = "calculated";
    this.border1 = "#81B1DB";
    this.border2 = rgba$1(255, 255, 255, 0.25);
    this.arrowheadColor = "calculated";
    this.fontFamily = '"trebuchet ms", verdana, arial, sans-serif';
    this.fontSize = "16px";
    this.labelBackground = "#181818";
    this.textColor = "#ccc";
    this.THEME_COLOR_LIMIT = 12;
    this.nodeBkg = "calculated";
    this.nodeBorder = "calculated";
    this.clusterBkg = "calculated";
    this.clusterBorder = "calculated";
    this.defaultLinkColor = "calculated";
    this.titleColor = "#F9FFFE";
    this.edgeLabelBackground = "calculated";
    this.actorBorder = "calculated";
    this.actorBkg = "calculated";
    this.actorTextColor = "calculated";
    this.actorLineColor = "calculated";
    this.signalColor = "calculated";
    this.signalTextColor = "calculated";
    this.labelBoxBkgColor = "calculated";
    this.labelBoxBorderColor = "calculated";
    this.labelTextColor = "calculated";
    this.loopTextColor = "calculated";
    this.noteBorderColor = "calculated";
    this.noteBkgColor = "#fff5ad";
    this.noteTextColor = "calculated";
    this.activationBorderColor = "calculated";
    this.activationBkgColor = "calculated";
    this.sequenceNumberColor = "black";
    this.sectionBkgColor = darken$1("#EAE8D9", 30);
    this.altSectionBkgColor = "calculated";
    this.sectionBkgColor2 = "#EAE8D9";
    this.excludeBkgColor = darken$1(this.sectionBkgColor, 10);
    this.taskBorderColor = rgba$1(255, 255, 255, 70);
    this.taskBkgColor = "calculated";
    this.taskTextColor = "calculated";
    this.taskTextLightColor = "calculated";
    this.taskTextOutsideColor = "calculated";
    this.taskTextClickableColor = "#003163";
    this.activeTaskBorderColor = rgba$1(255, 255, 255, 50);
    this.activeTaskBkgColor = "#81B1DB";
    this.gridColor = "calculated";
    this.doneTaskBkgColor = "calculated";
    this.doneTaskBorderColor = "grey";
    this.critBorderColor = "#E83737";
    this.critBkgColor = "#E83737";
    this.taskTextDarkColor = "calculated";
    this.todayLineColor = "#DB5757";
    this.personBorder = this.primaryBorderColor;
    this.personBkg = this.mainBkg;
    this.labelColor = "calculated";
    this.errorBkgColor = "#a44141";
    this.errorTextColor = "#ddd";
  }
  updateColors() {
    this.secondBkg = lighten$1(this.mainBkg, 16);
    this.lineColor = this.mainContrastColor;
    this.arrowheadColor = this.mainContrastColor;
    this.nodeBkg = this.mainBkg;
    this.nodeBorder = this.border1;
    this.clusterBkg = this.secondBkg;
    this.clusterBorder = this.border2;
    this.defaultLinkColor = this.lineColor;
    this.edgeLabelBackground = lighten$1(this.labelBackground, 25);
    this.actorBorder = this.border1;
    this.actorBkg = this.mainBkg;
    this.actorTextColor = this.mainContrastColor;
    this.actorLineColor = this.mainContrastColor;
    this.signalColor = this.mainContrastColor;
    this.signalTextColor = this.mainContrastColor;
    this.labelBoxBkgColor = this.actorBkg;
    this.labelBoxBorderColor = this.actorBorder;
    this.labelTextColor = this.mainContrastColor;
    this.loopTextColor = this.mainContrastColor;
    this.noteBorderColor = this.secondaryBorderColor;
    this.noteBkgColor = this.secondBkg;
    this.noteTextColor = this.secondaryTextColor;
    this.activationBorderColor = this.border1;
    this.activationBkgColor = this.secondBkg;
    this.altSectionBkgColor = this.background;
    this.taskBkgColor = lighten$1(this.mainBkg, 23);
    this.taskTextColor = this.darkTextColor;
    this.taskTextLightColor = this.mainContrastColor;
    this.taskTextOutsideColor = this.taskTextLightColor;
    this.gridColor = this.mainContrastColor;
    this.doneTaskBkgColor = this.mainContrastColor;
    this.taskTextDarkColor = this.darkTextColor;
    this.transitionColor = this.transitionColor || this.lineColor;
    this.transitionLabelColor = this.transitionLabelColor || this.textColor;
    this.stateLabelColor = this.stateLabelColor || this.stateBkg || this.primaryTextColor;
    this.stateBkg = this.stateBkg || this.mainBkg;
    this.labelBackgroundColor = this.labelBackgroundColor || this.stateBkg;
    this.compositeBackground = this.compositeBackground || this.background || this.tertiaryColor;
    this.altBackground = this.altBackground || "#555";
    this.compositeTitleBackground = this.compositeTitleBackground || this.mainBkg;
    this.compositeBorder = this.compositeBorder || this.nodeBorder;
    this.innerEndBackground = this.primaryBorderColor;
    this.specialStateColor = "#f4f4f4";
    this.errorBkgColor = this.errorBkgColor || this.tertiaryColor;
    this.errorTextColor = this.errorTextColor || this.tertiaryTextColor;
    this.fillType0 = this.primaryColor;
    this.fillType1 = this.secondaryColor;
    this.fillType2 = adjust$1(this.primaryColor, { h: 64 });
    this.fillType3 = adjust$1(this.secondaryColor, { h: 64 });
    this.fillType4 = adjust$1(this.primaryColor, { h: -64 });
    this.fillType5 = adjust$1(this.secondaryColor, { h: -64 });
    this.fillType6 = adjust$1(this.primaryColor, { h: 128 });
    this.fillType7 = adjust$1(this.secondaryColor, { h: 128 });
    this.cScale1 = this.cScale1 || "#0b0000";
    this.cScale2 = this.cScale2 || "#4d1037";
    this.cScale3 = this.cScale3 || "#3f5258";
    this.cScale4 = this.cScale4 || "#4f2f1b";
    this.cScale5 = this.cScale5 || "#6e0a0a";
    this.cScale6 = this.cScale6 || "#3b0048";
    this.cScale7 = this.cScale7 || "#995a01";
    this.cScale8 = this.cScale8 || "#154706";
    this.cScale9 = this.cScale9 || "#161722";
    this.cScale10 = this.cScale10 || "#00296f";
    this.cScale11 = this.cScale11 || "#01629c";
    this.cScale12 = this.cScale12 || "#010029";
    this.cScale0 = this.cScale0 || this.primaryColor;
    this.cScale1 = this.cScale1 || this.secondaryColor;
    this.cScale2 = this.cScale2 || this.tertiaryColor;
    this.cScale3 = this.cScale3 || adjust$1(this.primaryColor, { h: 30 });
    this.cScale4 = this.cScale4 || adjust$1(this.primaryColor, { h: 60 });
    this.cScale5 = this.cScale5 || adjust$1(this.primaryColor, { h: 90 });
    this.cScale6 = this.cScale6 || adjust$1(this.primaryColor, { h: 120 });
    this.cScale7 = this.cScale7 || adjust$1(this.primaryColor, { h: 150 });
    this.cScale8 = this.cScale8 || adjust$1(this.primaryColor, { h: 210 });
    this.cScale9 = this.cScale9 || adjust$1(this.primaryColor, { h: 270 });
    this.cScale10 = this.cScale10 || adjust$1(this.primaryColor, { h: 300 });
    this.cScale11 = this.cScale11 || adjust$1(this.primaryColor, { h: 330 });
    for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
      this["cScaleInv" + i] = this["cScaleInv" + i] || invert$1(this["cScale" + i]);
    }
    for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
      this["cScalePeer" + i] = this["cScalePeer" + i] || lighten$1(this["cScale" + i], 10);
    }
    for (let i = 0; i < 5; i++) {
      this["surface" + i] = this["surface" + i] || adjust$1(this.mainBkg, { h: 30, s: -30, l: -(-10 + i * 4) });
      this["surfacePeer" + i] = this["surfacePeer" + i] || adjust$1(this.mainBkg, { h: 30, s: -30, l: -(-7 + i * 4) });
    }
    this.scaleLabelColor = this.scaleLabelColor || (this.darkMode ? "black" : this.labelTextColor);
    for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
      this["cScaleLabel" + i] = this["cScaleLabel" + i] || this.scaleLabelColor;
    }
    for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
      this["pie" + i] = this["cScale" + i];
    }
    this.pieTitleTextSize = this.pieTitleTextSize || "25px";
    this.pieTitleTextColor = this.pieTitleTextColor || this.taskTextDarkColor;
    this.pieSectionTextSize = this.pieSectionTextSize || "17px";
    this.pieSectionTextColor = this.pieSectionTextColor || this.textColor;
    this.pieLegendTextSize = this.pieLegendTextSize || "17px";
    this.pieLegendTextColor = this.pieLegendTextColor || this.taskTextDarkColor;
    this.pieStrokeColor = this.pieStrokeColor || "black";
    this.pieStrokeWidth = this.pieStrokeWidth || "2px";
    this.pieOuterStrokeWidth = this.pieOuterStrokeWidth || "2px";
    this.pieOuterStrokeColor = this.pieOuterStrokeColor || "black";
    this.pieOpacity = this.pieOpacity || "0.7";
    this.quadrant1Fill = this.quadrant1Fill || this.primaryColor;
    this.quadrant2Fill = this.quadrant2Fill || adjust$1(this.primaryColor, { r: 5, g: 5, b: 5 });
    this.quadrant3Fill = this.quadrant3Fill || adjust$1(this.primaryColor, { r: 10, g: 10, b: 10 });
    this.quadrant4Fill = this.quadrant4Fill || adjust$1(this.primaryColor, { r: 15, g: 15, b: 15 });
    this.quadrant1TextFill = this.quadrant1TextFill || this.primaryTextColor;
    this.quadrant2TextFill = this.quadrant2TextFill || adjust$1(this.primaryTextColor, { r: -5, g: -5, b: -5 });
    this.quadrant3TextFill = this.quadrant3TextFill || adjust$1(this.primaryTextColor, { r: -10, g: -10, b: -10 });
    this.quadrant4TextFill = this.quadrant4TextFill || adjust$1(this.primaryTextColor, { r: -15, g: -15, b: -15 });
    this.quadrantPointFill = this.quadrantPointFill || isDark$1(this.quadrant1Fill) ? lighten$1(this.quadrant1Fill) : darken$1(this.quadrant1Fill);
    this.quadrantPointTextFill = this.quadrantPointTextFill || this.primaryTextColor;
    this.quadrantXAxisTextFill = this.quadrantXAxisTextFill || this.primaryTextColor;
    this.quadrantYAxisTextFill = this.quadrantYAxisTextFill || this.primaryTextColor;
    this.quadrantInternalBorderStrokeFill = this.quadrantInternalBorderStrokeFill || this.primaryBorderColor;
    this.quadrantExternalBorderStrokeFill = this.quadrantExternalBorderStrokeFill || this.primaryBorderColor;
    this.quadrantTitleFill = this.quadrantTitleFill || this.primaryTextColor;
    this.classText = this.primaryTextColor;
    this.requirementBackground = this.requirementBackground || this.primaryColor;
    this.requirementBorderColor = this.requirementBorderColor || this.primaryBorderColor;
    this.requirementBorderSize = this.requirementBorderSize || "1";
    this.requirementTextColor = this.requirementTextColor || this.primaryTextColor;
    this.relationColor = this.relationColor || this.lineColor;
    this.relationLabelBackground = this.relationLabelBackground || (this.darkMode ? darken$1(this.secondaryColor, 30) : this.secondaryColor);
    this.relationLabelColor = this.relationLabelColor || this.actorTextColor;
    this.git0 = lighten$1(this.secondaryColor, 20);
    this.git1 = lighten$1(this.pie2 || this.secondaryColor, 20);
    this.git2 = lighten$1(this.pie3 || this.tertiaryColor, 20);
    this.git3 = lighten$1(this.pie4 || adjust$1(this.primaryColor, { h: -30 }), 20);
    this.git4 = lighten$1(this.pie5 || adjust$1(this.primaryColor, { h: -60 }), 20);
    this.git5 = lighten$1(this.pie6 || adjust$1(this.primaryColor, { h: -90 }), 10);
    this.git6 = lighten$1(this.pie7 || adjust$1(this.primaryColor, { h: 60 }), 10);
    this.git7 = lighten$1(this.pie8 || adjust$1(this.primaryColor, { h: 120 }), 20);
    this.gitInv0 = this.gitInv0 || invert$1(this.git0);
    this.gitInv1 = this.gitInv1 || invert$1(this.git1);
    this.gitInv2 = this.gitInv2 || invert$1(this.git2);
    this.gitInv3 = this.gitInv3 || invert$1(this.git3);
    this.gitInv4 = this.gitInv4 || invert$1(this.git4);
    this.gitInv5 = this.gitInv5 || invert$1(this.git5);
    this.gitInv6 = this.gitInv6 || invert$1(this.git6);
    this.gitInv7 = this.gitInv7 || invert$1(this.git7);
    this.gitBranchLabel0 = this.gitBranchLabel0 || invert$1(this.labelTextColor);
    this.gitBranchLabel1 = this.gitBranchLabel1 || this.labelTextColor;
    this.gitBranchLabel2 = this.gitBranchLabel2 || this.labelTextColor;
    this.gitBranchLabel3 = this.gitBranchLabel3 || invert$1(this.labelTextColor);
    this.gitBranchLabel4 = this.gitBranchLabel4 || this.labelTextColor;
    this.gitBranchLabel5 = this.gitBranchLabel5 || this.labelTextColor;
    this.gitBranchLabel6 = this.gitBranchLabel6 || this.labelTextColor;
    this.gitBranchLabel7 = this.gitBranchLabel7 || this.labelTextColor;
    this.tagLabelColor = this.tagLabelColor || this.primaryTextColor;
    this.tagLabelBackground = this.tagLabelBackground || this.primaryColor;
    this.tagLabelBorder = this.tagBorder || this.primaryBorderColor;
    this.tagLabelFontSize = this.tagLabelFontSize || "10px";
    this.commitLabelColor = this.commitLabelColor || this.secondaryTextColor;
    this.commitLabelBackground = this.commitLabelBackground || this.secondaryColor;
    this.commitLabelFontSize = this.commitLabelFontSize || "10px";
    this.attributeBackgroundColorOdd = this.attributeBackgroundColorOdd || lighten$1(this.background, 12);
    this.attributeBackgroundColorEven = this.attributeBackgroundColorEven || lighten$1(this.background, 2);
  }
  calculate(overrides) {
    if (typeof overrides !== "object") {
      this.updateColors();
      return;
    }
    const keys = Object.keys(overrides);
    keys.forEach((k) => {
      this[k] = overrides[k];
    });
    this.updateColors();
    keys.forEach((k) => {
      this[k] = overrides[k];
    });
  }
};
const getThemeVariables$3 = (userOverrides) => {
  const theme2 = new Theme$3();
  theme2.calculate(userOverrides);
  return theme2;
};
let Theme$2 = class Theme3 {
  constructor() {
    this.background = "#f4f4f4";
    this.primaryColor = "#ECECFF";
    this.secondaryColor = adjust$1(this.primaryColor, { h: 120 });
    this.secondaryColor = "#ffffde";
    this.tertiaryColor = adjust$1(this.primaryColor, { h: -160 });
    this.primaryBorderColor = mkBorder(this.primaryColor, this.darkMode);
    this.secondaryBorderColor = mkBorder(this.secondaryColor, this.darkMode);
    this.tertiaryBorderColor = mkBorder(this.tertiaryColor, this.darkMode);
    this.primaryTextColor = invert$1(this.primaryColor);
    this.secondaryTextColor = invert$1(this.secondaryColor);
    this.tertiaryTextColor = invert$1(this.tertiaryColor);
    this.lineColor = invert$1(this.background);
    this.textColor = invert$1(this.background);
    this.background = "white";
    this.mainBkg = "#ECECFF";
    this.secondBkg = "#ffffde";
    this.lineColor = "#333333";
    this.border1 = "#9370DB";
    this.border2 = "#aaaa33";
    this.arrowheadColor = "#333333";
    this.fontFamily = '"trebuchet ms", verdana, arial, sans-serif';
    this.fontSize = "16px";
    this.labelBackground = "#e8e8e8";
    this.textColor = "#333";
    this.THEME_COLOR_LIMIT = 12;
    this.nodeBkg = "calculated";
    this.nodeBorder = "calculated";
    this.clusterBkg = "calculated";
    this.clusterBorder = "calculated";
    this.defaultLinkColor = "calculated";
    this.titleColor = "calculated";
    this.edgeLabelBackground = "calculated";
    this.actorBorder = "calculated";
    this.actorBkg = "calculated";
    this.actorTextColor = "black";
    this.actorLineColor = "grey";
    this.signalColor = "calculated";
    this.signalTextColor = "calculated";
    this.labelBoxBkgColor = "calculated";
    this.labelBoxBorderColor = "calculated";
    this.labelTextColor = "calculated";
    this.loopTextColor = "calculated";
    this.noteBorderColor = "calculated";
    this.noteBkgColor = "#fff5ad";
    this.noteTextColor = "calculated";
    this.activationBorderColor = "#666";
    this.activationBkgColor = "#f4f4f4";
    this.sequenceNumberColor = "white";
    this.sectionBkgColor = "calculated";
    this.altSectionBkgColor = "calculated";
    this.sectionBkgColor2 = "calculated";
    this.excludeBkgColor = "#eeeeee";
    this.taskBorderColor = "calculated";
    this.taskBkgColor = "calculated";
    this.taskTextLightColor = "calculated";
    this.taskTextColor = this.taskTextLightColor;
    this.taskTextDarkColor = "calculated";
    this.taskTextOutsideColor = this.taskTextDarkColor;
    this.taskTextClickableColor = "calculated";
    this.activeTaskBorderColor = "calculated";
    this.activeTaskBkgColor = "calculated";
    this.gridColor = "calculated";
    this.doneTaskBkgColor = "calculated";
    this.doneTaskBorderColor = "calculated";
    this.critBorderColor = "calculated";
    this.critBkgColor = "calculated";
    this.todayLineColor = "calculated";
    this.sectionBkgColor = rgba$1(102, 102, 255, 0.49);
    this.altSectionBkgColor = "white";
    this.sectionBkgColor2 = "#fff400";
    this.taskBorderColor = "#534fbc";
    this.taskBkgColor = "#8a90dd";
    this.taskTextLightColor = "white";
    this.taskTextColor = "calculated";
    this.taskTextDarkColor = "black";
    this.taskTextOutsideColor = "calculated";
    this.taskTextClickableColor = "#003163";
    this.activeTaskBorderColor = "#534fbc";
    this.activeTaskBkgColor = "#bfc7ff";
    this.gridColor = "lightgrey";
    this.doneTaskBkgColor = "lightgrey";
    this.doneTaskBorderColor = "grey";
    this.critBorderColor = "#ff8888";
    this.critBkgColor = "red";
    this.todayLineColor = "red";
    this.personBorder = this.primaryBorderColor;
    this.personBkg = this.mainBkg;
    this.labelColor = "black";
    this.errorBkgColor = "#552222";
    this.errorTextColor = "#552222";
    this.updateColors();
  }
  updateColors() {
    this.cScale0 = this.cScale0 || this.primaryColor;
    this.cScale1 = this.cScale1 || this.secondaryColor;
    this.cScale2 = this.cScale2 || this.tertiaryColor;
    this.cScale3 = this.cScale3 || adjust$1(this.primaryColor, { h: 30 });
    this.cScale4 = this.cScale4 || adjust$1(this.primaryColor, { h: 60 });
    this.cScale5 = this.cScale5 || adjust$1(this.primaryColor, { h: 90 });
    this.cScale6 = this.cScale6 || adjust$1(this.primaryColor, { h: 120 });
    this.cScale7 = this.cScale7 || adjust$1(this.primaryColor, { h: 150 });
    this.cScale8 = this.cScale8 || adjust$1(this.primaryColor, { h: 210 });
    this.cScale9 = this.cScale9 || adjust$1(this.primaryColor, { h: 270 });
    this.cScale10 = this.cScale10 || adjust$1(this.primaryColor, { h: 300 });
    this.cScale11 = this.cScale11 || adjust$1(this.primaryColor, { h: 330 });
    this["cScalePeer1"] = this["cScalePeer1"] || darken$1(this.secondaryColor, 45);
    this["cScalePeer2"] = this["cScalePeer2"] || darken$1(this.tertiaryColor, 40);
    for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
      this["cScale" + i] = darken$1(this["cScale" + i], 10);
      this["cScalePeer" + i] = this["cScalePeer" + i] || darken$1(this["cScale" + i], 25);
    }
    for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
      this["cScaleInv" + i] = this["cScaleInv" + i] || adjust$1(this["cScale" + i], { h: 180 });
    }
    for (let i = 0; i < 5; i++) {
      this["surface" + i] = this["surface" + i] || adjust$1(this.mainBkg, { h: 30, l: -(5 + i * 5) });
      this["surfacePeer" + i] = this["surfacePeer" + i] || adjust$1(this.mainBkg, { h: 30, l: -(7 + i * 5) });
    }
    this.scaleLabelColor = this.scaleLabelColor !== "calculated" && this.scaleLabelColor ? this.scaleLabelColor : this.labelTextColor;
    if (this.labelTextColor !== "calculated") {
      this.cScaleLabel0 = this.cScaleLabel0 || invert$1(this.labelTextColor);
      this.cScaleLabel3 = this.cScaleLabel3 || invert$1(this.labelTextColor);
      for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
        this["cScaleLabel" + i] = this["cScaleLabel" + i] || this.labelTextColor;
      }
    }
    this.nodeBkg = this.mainBkg;
    this.nodeBorder = this.border1;
    this.clusterBkg = this.secondBkg;
    this.clusterBorder = this.border2;
    this.defaultLinkColor = this.lineColor;
    this.titleColor = this.textColor;
    this.edgeLabelBackground = this.labelBackground;
    this.actorBorder = lighten$1(this.border1, 23);
    this.actorBkg = this.mainBkg;
    this.labelBoxBkgColor = this.actorBkg;
    this.signalColor = this.textColor;
    this.signalTextColor = this.textColor;
    this.labelBoxBorderColor = this.actorBorder;
    this.labelTextColor = this.actorTextColor;
    this.loopTextColor = this.actorTextColor;
    this.noteBorderColor = this.border2;
    this.noteTextColor = this.actorTextColor;
    this.taskTextColor = this.taskTextLightColor;
    this.taskTextOutsideColor = this.taskTextDarkColor;
    this.transitionColor = this.transitionColor || this.lineColor;
    this.transitionLabelColor = this.transitionLabelColor || this.textColor;
    this.stateLabelColor = this.stateLabelColor || this.stateBkg || this.primaryTextColor;
    this.stateBkg = this.stateBkg || this.mainBkg;
    this.labelBackgroundColor = this.labelBackgroundColor || this.stateBkg;
    this.compositeBackground = this.compositeBackground || this.background || this.tertiaryColor;
    this.altBackground = this.altBackground || "#f0f0f0";
    this.compositeTitleBackground = this.compositeTitleBackground || this.mainBkg;
    this.compositeBorder = this.compositeBorder || this.nodeBorder;
    this.innerEndBackground = this.nodeBorder;
    this.specialStateColor = this.lineColor;
    this.errorBkgColor = this.errorBkgColor || this.tertiaryColor;
    this.errorTextColor = this.errorTextColor || this.tertiaryTextColor;
    this.transitionColor = this.transitionColor || this.lineColor;
    this.classText = this.primaryTextColor;
    this.fillType0 = this.primaryColor;
    this.fillType1 = this.secondaryColor;
    this.fillType2 = adjust$1(this.primaryColor, { h: 64 });
    this.fillType3 = adjust$1(this.secondaryColor, { h: 64 });
    this.fillType4 = adjust$1(this.primaryColor, { h: -64 });
    this.fillType5 = adjust$1(this.secondaryColor, { h: -64 });
    this.fillType6 = adjust$1(this.primaryColor, { h: 128 });
    this.fillType7 = adjust$1(this.secondaryColor, { h: 128 });
    this.pie1 = this.pie1 || this.primaryColor;
    this.pie2 = this.pie2 || this.secondaryColor;
    this.pie3 = this.pie3 || adjust$1(this.tertiaryColor, { l: -40 });
    this.pie4 = this.pie4 || adjust$1(this.primaryColor, { l: -10 });
    this.pie5 = this.pie5 || adjust$1(this.secondaryColor, { l: -30 });
    this.pie6 = this.pie6 || adjust$1(this.tertiaryColor, { l: -20 });
    this.pie7 = this.pie7 || adjust$1(this.primaryColor, { h: 60, l: -20 });
    this.pie8 = this.pie8 || adjust$1(this.primaryColor, { h: -60, l: -40 });
    this.pie9 = this.pie9 || adjust$1(this.primaryColor, { h: 120, l: -40 });
    this.pie10 = this.pie10 || adjust$1(this.primaryColor, { h: 60, l: -40 });
    this.pie11 = this.pie11 || adjust$1(this.primaryColor, { h: -90, l: -40 });
    this.pie12 = this.pie12 || adjust$1(this.primaryColor, { h: 120, l: -30 });
    this.pieTitleTextSize = this.pieTitleTextSize || "25px";
    this.pieTitleTextColor = this.pieTitleTextColor || this.taskTextDarkColor;
    this.pieSectionTextSize = this.pieSectionTextSize || "17px";
    this.pieSectionTextColor = this.pieSectionTextColor || this.textColor;
    this.pieLegendTextSize = this.pieLegendTextSize || "17px";
    this.pieLegendTextColor = this.pieLegendTextColor || this.taskTextDarkColor;
    this.pieStrokeColor = this.pieStrokeColor || "black";
    this.pieStrokeWidth = this.pieStrokeWidth || "2px";
    this.pieOuterStrokeWidth = this.pieOuterStrokeWidth || "2px";
    this.pieOuterStrokeColor = this.pieOuterStrokeColor || "black";
    this.pieOpacity = this.pieOpacity || "0.7";
    this.quadrant1Fill = this.quadrant1Fill || this.primaryColor;
    this.quadrant2Fill = this.quadrant2Fill || adjust$1(this.primaryColor, { r: 5, g: 5, b: 5 });
    this.quadrant3Fill = this.quadrant3Fill || adjust$1(this.primaryColor, { r: 10, g: 10, b: 10 });
    this.quadrant4Fill = this.quadrant4Fill || adjust$1(this.primaryColor, { r: 15, g: 15, b: 15 });
    this.quadrant1TextFill = this.quadrant1TextFill || this.primaryTextColor;
    this.quadrant2TextFill = this.quadrant2TextFill || adjust$1(this.primaryTextColor, { r: -5, g: -5, b: -5 });
    this.quadrant3TextFill = this.quadrant3TextFill || adjust$1(this.primaryTextColor, { r: -10, g: -10, b: -10 });
    this.quadrant4TextFill = this.quadrant4TextFill || adjust$1(this.primaryTextColor, { r: -15, g: -15, b: -15 });
    this.quadrantPointFill = this.quadrantPointFill || isDark$1(this.quadrant1Fill) ? lighten$1(this.quadrant1Fill) : darken$1(this.quadrant1Fill);
    this.quadrantPointTextFill = this.quadrantPointTextFill || this.primaryTextColor;
    this.quadrantXAxisTextFill = this.quadrantXAxisTextFill || this.primaryTextColor;
    this.quadrantYAxisTextFill = this.quadrantYAxisTextFill || this.primaryTextColor;
    this.quadrantInternalBorderStrokeFill = this.quadrantInternalBorderStrokeFill || this.primaryBorderColor;
    this.quadrantExternalBorderStrokeFill = this.quadrantExternalBorderStrokeFill || this.primaryBorderColor;
    this.quadrantTitleFill = this.quadrantTitleFill || this.primaryTextColor;
    this.requirementBackground = this.requirementBackground || this.primaryColor;
    this.requirementBorderColor = this.requirementBorderColor || this.primaryBorderColor;
    this.requirementBorderSize = this.requirementBorderSize || "1";
    this.requirementTextColor = this.requirementTextColor || this.primaryTextColor;
    this.relationColor = this.relationColor || this.lineColor;
    this.relationLabelBackground = this.relationLabelBackground || this.labelBackground;
    this.relationLabelColor = this.relationLabelColor || this.actorTextColor;
    this.git0 = this.git0 || this.primaryColor;
    this.git1 = this.git1 || this.secondaryColor;
    this.git2 = this.git2 || this.tertiaryColor;
    this.git3 = this.git3 || adjust$1(this.primaryColor, { h: -30 });
    this.git4 = this.git4 || adjust$1(this.primaryColor, { h: -60 });
    this.git5 = this.git5 || adjust$1(this.primaryColor, { h: -90 });
    this.git6 = this.git6 || adjust$1(this.primaryColor, { h: 60 });
    this.git7 = this.git7 || adjust$1(this.primaryColor, { h: 120 });
    if (this.darkMode) {
      this.git0 = lighten$1(this.git0, 25);
      this.git1 = lighten$1(this.git1, 25);
      this.git2 = lighten$1(this.git2, 25);
      this.git3 = lighten$1(this.git3, 25);
      this.git4 = lighten$1(this.git4, 25);
      this.git5 = lighten$1(this.git5, 25);
      this.git6 = lighten$1(this.git6, 25);
      this.git7 = lighten$1(this.git7, 25);
    } else {
      this.git0 = darken$1(this.git0, 25);
      this.git1 = darken$1(this.git1, 25);
      this.git2 = darken$1(this.git2, 25);
      this.git3 = darken$1(this.git3, 25);
      this.git4 = darken$1(this.git4, 25);
      this.git5 = darken$1(this.git5, 25);
      this.git6 = darken$1(this.git6, 25);
      this.git7 = darken$1(this.git7, 25);
    }
    this.gitInv0 = this.gitInv0 || darken$1(invert$1(this.git0), 25);
    this.gitInv1 = this.gitInv1 || invert$1(this.git1);
    this.gitInv2 = this.gitInv2 || invert$1(this.git2);
    this.gitInv3 = this.gitInv3 || invert$1(this.git3);
    this.gitInv4 = this.gitInv4 || invert$1(this.git4);
    this.gitInv5 = this.gitInv5 || invert$1(this.git5);
    this.gitInv6 = this.gitInv6 || invert$1(this.git6);
    this.gitInv7 = this.gitInv7 || invert$1(this.git7);
    this.gitBranchLabel0 = this.gitBranchLabel0 || invert$1(this.labelTextColor);
    this.gitBranchLabel1 = this.gitBranchLabel1 || this.labelTextColor;
    this.gitBranchLabel2 = this.gitBranchLabel2 || this.labelTextColor;
    this.gitBranchLabel3 = this.gitBranchLabel3 || invert$1(this.labelTextColor);
    this.gitBranchLabel4 = this.gitBranchLabel4 || this.labelTextColor;
    this.gitBranchLabel5 = this.gitBranchLabel5 || this.labelTextColor;
    this.gitBranchLabel6 = this.gitBranchLabel6 || this.labelTextColor;
    this.gitBranchLabel7 = this.gitBranchLabel7 || this.labelTextColor;
    this.tagLabelColor = this.tagLabelColor || this.primaryTextColor;
    this.tagLabelBackground = this.tagLabelBackground || this.primaryColor;
    this.tagLabelBorder = this.tagBorder || this.primaryBorderColor;
    this.tagLabelFontSize = this.tagLabelFontSize || "10px";
    this.commitLabelColor = this.commitLabelColor || this.secondaryTextColor;
    this.commitLabelBackground = this.commitLabelBackground || this.secondaryColor;
    this.commitLabelFontSize = this.commitLabelFontSize || "10px";
    this.attributeBackgroundColorOdd = this.attributeBackgroundColorOdd || oldAttributeBackgroundColorOdd;
    this.attributeBackgroundColorEven = this.attributeBackgroundColorEven || oldAttributeBackgroundColorEven;
  }
  calculate(overrides) {
    if (typeof overrides !== "object") {
      this.updateColors();
      return;
    }
    const keys = Object.keys(overrides);
    keys.forEach((k) => {
      this[k] = overrides[k];
    });
    this.updateColors();
    keys.forEach((k) => {
      this[k] = overrides[k];
    });
  }
};
const getThemeVariables$2 = (userOverrides) => {
  const theme2 = new Theme$2();
  theme2.calculate(userOverrides);
  return theme2;
};
let Theme$1 = class Theme4 {
  constructor() {
    this.background = "#f4f4f4";
    this.primaryColor = "#cde498";
    this.secondaryColor = "#cdffb2";
    this.background = "white";
    this.mainBkg = "#cde498";
    this.secondBkg = "#cdffb2";
    this.lineColor = "green";
    this.border1 = "#13540c";
    this.border2 = "#6eaa49";
    this.arrowheadColor = "green";
    this.fontFamily = '"trebuchet ms", verdana, arial, sans-serif';
    this.fontSize = "16px";
    this.tertiaryColor = lighten$1("#cde498", 10);
    this.primaryBorderColor = mkBorder(this.primaryColor, this.darkMode);
    this.secondaryBorderColor = mkBorder(this.secondaryColor, this.darkMode);
    this.tertiaryBorderColor = mkBorder(this.tertiaryColor, this.darkMode);
    this.primaryTextColor = invert$1(this.primaryColor);
    this.secondaryTextColor = invert$1(this.secondaryColor);
    this.tertiaryTextColor = invert$1(this.primaryColor);
    this.lineColor = invert$1(this.background);
    this.textColor = invert$1(this.background);
    this.THEME_COLOR_LIMIT = 12;
    this.nodeBkg = "calculated";
    this.nodeBorder = "calculated";
    this.clusterBkg = "calculated";
    this.clusterBorder = "calculated";
    this.defaultLinkColor = "calculated";
    this.titleColor = "#333";
    this.edgeLabelBackground = "#e8e8e8";
    this.actorBorder = "calculated";
    this.actorBkg = "calculated";
    this.actorTextColor = "black";
    this.actorLineColor = "grey";
    this.signalColor = "#333";
    this.signalTextColor = "#333";
    this.labelBoxBkgColor = "calculated";
    this.labelBoxBorderColor = "#326932";
    this.labelTextColor = "calculated";
    this.loopTextColor = "calculated";
    this.noteBorderColor = "calculated";
    this.noteBkgColor = "#fff5ad";
    this.noteTextColor = "calculated";
    this.activationBorderColor = "#666";
    this.activationBkgColor = "#f4f4f4";
    this.sequenceNumberColor = "white";
    this.sectionBkgColor = "#6eaa49";
    this.altSectionBkgColor = "white";
    this.sectionBkgColor2 = "#6eaa49";
    this.excludeBkgColor = "#eeeeee";
    this.taskBorderColor = "calculated";
    this.taskBkgColor = "#487e3a";
    this.taskTextLightColor = "white";
    this.taskTextColor = "calculated";
    this.taskTextDarkColor = "black";
    this.taskTextOutsideColor = "calculated";
    this.taskTextClickableColor = "#003163";
    this.activeTaskBorderColor = "calculated";
    this.activeTaskBkgColor = "calculated";
    this.gridColor = "lightgrey";
    this.doneTaskBkgColor = "lightgrey";
    this.doneTaskBorderColor = "grey";
    this.critBorderColor = "#ff8888";
    this.critBkgColor = "red";
    this.todayLineColor = "red";
    this.personBorder = this.primaryBorderColor;
    this.personBkg = this.mainBkg;
    this.labelColor = "black";
    this.errorBkgColor = "#552222";
    this.errorTextColor = "#552222";
  }
  updateColors() {
    this.actorBorder = darken$1(this.mainBkg, 20);
    this.actorBkg = this.mainBkg;
    this.labelBoxBkgColor = this.actorBkg;
    this.labelTextColor = this.actorTextColor;
    this.loopTextColor = this.actorTextColor;
    this.noteBorderColor = this.border2;
    this.noteTextColor = this.actorTextColor;
    this.cScale0 = this.cScale0 || this.primaryColor;
    this.cScale1 = this.cScale1 || this.secondaryColor;
    this.cScale2 = this.cScale2 || this.tertiaryColor;
    this.cScale3 = this.cScale3 || adjust$1(this.primaryColor, { h: 30 });
    this.cScale4 = this.cScale4 || adjust$1(this.primaryColor, { h: 60 });
    this.cScale5 = this.cScale5 || adjust$1(this.primaryColor, { h: 90 });
    this.cScale6 = this.cScale6 || adjust$1(this.primaryColor, { h: 120 });
    this.cScale7 = this.cScale7 || adjust$1(this.primaryColor, { h: 150 });
    this.cScale8 = this.cScale8 || adjust$1(this.primaryColor, { h: 210 });
    this.cScale9 = this.cScale9 || adjust$1(this.primaryColor, { h: 270 });
    this.cScale10 = this.cScale10 || adjust$1(this.primaryColor, { h: 300 });
    this.cScale11 = this.cScale11 || adjust$1(this.primaryColor, { h: 330 });
    this["cScalePeer1"] = this["cScalePeer1"] || darken$1(this.secondaryColor, 45);
    this["cScalePeer2"] = this["cScalePeer2"] || darken$1(this.tertiaryColor, 40);
    for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
      this["cScale" + i] = darken$1(this["cScale" + i], 10);
      this["cScalePeer" + i] = this["cScalePeer" + i] || darken$1(this["cScale" + i], 25);
    }
    for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
      this["cScaleInv" + i] = this["cScaleInv" + i] || adjust$1(this["cScale" + i], { h: 180 });
    }
    this.scaleLabelColor = this.scaleLabelColor !== "calculated" && this.scaleLabelColor ? this.scaleLabelColor : this.labelTextColor;
    for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
      this["cScaleLabel" + i] = this["cScaleLabel" + i] || this.scaleLabelColor;
    }
    for (let i = 0; i < 5; i++) {
      this["surface" + i] = this["surface" + i] || adjust$1(this.mainBkg, { h: 30, s: -30, l: -(5 + i * 5) });
      this["surfacePeer" + i] = this["surfacePeer" + i] || adjust$1(this.mainBkg, { h: 30, s: -30, l: -(8 + i * 5) });
    }
    this.nodeBkg = this.mainBkg;
    this.nodeBorder = this.border1;
    this.clusterBkg = this.secondBkg;
    this.clusterBorder = this.border2;
    this.defaultLinkColor = this.lineColor;
    this.taskBorderColor = this.border1;
    this.taskTextColor = this.taskTextLightColor;
    this.taskTextOutsideColor = this.taskTextDarkColor;
    this.activeTaskBorderColor = this.taskBorderColor;
    this.activeTaskBkgColor = this.mainBkg;
    this.transitionColor = this.transitionColor || this.lineColor;
    this.transitionLabelColor = this.transitionLabelColor || this.textColor;
    this.stateLabelColor = this.stateLabelColor || this.stateBkg || this.primaryTextColor;
    this.stateBkg = this.stateBkg || this.mainBkg;
    this.labelBackgroundColor = this.labelBackgroundColor || this.stateBkg;
    this.compositeBackground = this.compositeBackground || this.background || this.tertiaryColor;
    this.altBackground = this.altBackground || "#f0f0f0";
    this.compositeTitleBackground = this.compositeTitleBackground || this.mainBkg;
    this.compositeBorder = this.compositeBorder || this.nodeBorder;
    this.innerEndBackground = this.primaryBorderColor;
    this.specialStateColor = this.lineColor;
    this.errorBkgColor = this.errorBkgColor || this.tertiaryColor;
    this.errorTextColor = this.errorTextColor || this.tertiaryTextColor;
    this.transitionColor = this.transitionColor || this.lineColor;
    this.classText = this.primaryTextColor;
    this.fillType0 = this.primaryColor;
    this.fillType1 = this.secondaryColor;
    this.fillType2 = adjust$1(this.primaryColor, { h: 64 });
    this.fillType3 = adjust$1(this.secondaryColor, { h: 64 });
    this.fillType4 = adjust$1(this.primaryColor, { h: -64 });
    this.fillType5 = adjust$1(this.secondaryColor, { h: -64 });
    this.fillType6 = adjust$1(this.primaryColor, { h: 128 });
    this.fillType7 = adjust$1(this.secondaryColor, { h: 128 });
    this.pie1 = this.pie1 || this.primaryColor;
    this.pie2 = this.pie2 || this.secondaryColor;
    this.pie3 = this.pie3 || this.tertiaryColor;
    this.pie4 = this.pie4 || adjust$1(this.primaryColor, { l: -30 });
    this.pie5 = this.pie5 || adjust$1(this.secondaryColor, { l: -30 });
    this.pie6 = this.pie6 || adjust$1(this.tertiaryColor, { h: 40, l: -40 });
    this.pie7 = this.pie7 || adjust$1(this.primaryColor, { h: 60, l: -10 });
    this.pie8 = this.pie8 || adjust$1(this.primaryColor, { h: -60, l: -10 });
    this.pie9 = this.pie9 || adjust$1(this.primaryColor, { h: 120, l: 0 });
    this.pie10 = this.pie10 || adjust$1(this.primaryColor, { h: 60, l: -50 });
    this.pie11 = this.pie11 || adjust$1(this.primaryColor, { h: -60, l: -50 });
    this.pie12 = this.pie12 || adjust$1(this.primaryColor, { h: 120, l: -50 });
    this.pieTitleTextSize = this.pieTitleTextSize || "25px";
    this.pieTitleTextColor = this.pieTitleTextColor || this.taskTextDarkColor;
    this.pieSectionTextSize = this.pieSectionTextSize || "17px";
    this.pieSectionTextColor = this.pieSectionTextColor || this.textColor;
    this.pieLegendTextSize = this.pieLegendTextSize || "17px";
    this.pieLegendTextColor = this.pieLegendTextColor || this.taskTextDarkColor;
    this.pieStrokeColor = this.pieStrokeColor || "black";
    this.pieStrokeWidth = this.pieStrokeWidth || "2px";
    this.pieOuterStrokeWidth = this.pieOuterStrokeWidth || "2px";
    this.pieOuterStrokeColor = this.pieOuterStrokeColor || "black";
    this.pieOpacity = this.pieOpacity || "0.7";
    this.quadrant1Fill = this.quadrant1Fill || this.primaryColor;
    this.quadrant2Fill = this.quadrant2Fill || adjust$1(this.primaryColor, { r: 5, g: 5, b: 5 });
    this.quadrant3Fill = this.quadrant3Fill || adjust$1(this.primaryColor, { r: 10, g: 10, b: 10 });
    this.quadrant4Fill = this.quadrant4Fill || adjust$1(this.primaryColor, { r: 15, g: 15, b: 15 });
    this.quadrant1TextFill = this.quadrant1TextFill || this.primaryTextColor;
    this.quadrant2TextFill = this.quadrant2TextFill || adjust$1(this.primaryTextColor, { r: -5, g: -5, b: -5 });
    this.quadrant3TextFill = this.quadrant3TextFill || adjust$1(this.primaryTextColor, { r: -10, g: -10, b: -10 });
    this.quadrant4TextFill = this.quadrant4TextFill || adjust$1(this.primaryTextColor, { r: -15, g: -15, b: -15 });
    this.quadrantPointFill = this.quadrantPointFill || isDark$1(this.quadrant1Fill) ? lighten$1(this.quadrant1Fill) : darken$1(this.quadrant1Fill);
    this.quadrantPointTextFill = this.quadrantPointTextFill || this.primaryTextColor;
    this.quadrantXAxisTextFill = this.quadrantXAxisTextFill || this.primaryTextColor;
    this.quadrantYAxisTextFill = this.quadrantYAxisTextFill || this.primaryTextColor;
    this.quadrantInternalBorderStrokeFill = this.quadrantInternalBorderStrokeFill || this.primaryBorderColor;
    this.quadrantExternalBorderStrokeFill = this.quadrantExternalBorderStrokeFill || this.primaryBorderColor;
    this.quadrantTitleFill = this.quadrantTitleFill || this.primaryTextColor;
    this.requirementBackground = this.requirementBackground || this.primaryColor;
    this.requirementBorderColor = this.requirementBorderColor || this.primaryBorderColor;
    this.requirementBorderSize = this.requirementBorderSize || "1";
    this.requirementTextColor = this.requirementTextColor || this.primaryTextColor;
    this.relationColor = this.relationColor || this.lineColor;
    this.relationLabelBackground = this.relationLabelBackground || this.edgeLabelBackground;
    this.relationLabelColor = this.relationLabelColor || this.actorTextColor;
    this.git0 = this.git0 || this.primaryColor;
    this.git1 = this.git1 || this.secondaryColor;
    this.git2 = this.git2 || this.tertiaryColor;
    this.git3 = this.git3 || adjust$1(this.primaryColor, { h: -30 });
    this.git4 = this.git4 || adjust$1(this.primaryColor, { h: -60 });
    this.git5 = this.git5 || adjust$1(this.primaryColor, { h: -90 });
    this.git6 = this.git6 || adjust$1(this.primaryColor, { h: 60 });
    this.git7 = this.git7 || adjust$1(this.primaryColor, { h: 120 });
    if (this.darkMode) {
      this.git0 = lighten$1(this.git0, 25);
      this.git1 = lighten$1(this.git1, 25);
      this.git2 = lighten$1(this.git2, 25);
      this.git3 = lighten$1(this.git3, 25);
      this.git4 = lighten$1(this.git4, 25);
      this.git5 = lighten$1(this.git5, 25);
      this.git6 = lighten$1(this.git6, 25);
      this.git7 = lighten$1(this.git7, 25);
    } else {
      this.git0 = darken$1(this.git0, 25);
      this.git1 = darken$1(this.git1, 25);
      this.git2 = darken$1(this.git2, 25);
      this.git3 = darken$1(this.git3, 25);
      this.git4 = darken$1(this.git4, 25);
      this.git5 = darken$1(this.git5, 25);
      this.git6 = darken$1(this.git6, 25);
      this.git7 = darken$1(this.git7, 25);
    }
    this.gitInv0 = this.gitInv0 || invert$1(this.git0);
    this.gitInv1 = this.gitInv1 || invert$1(this.git1);
    this.gitInv2 = this.gitInv2 || invert$1(this.git2);
    this.gitInv3 = this.gitInv3 || invert$1(this.git3);
    this.gitInv4 = this.gitInv4 || invert$1(this.git4);
    this.gitInv5 = this.gitInv5 || invert$1(this.git5);
    this.gitInv6 = this.gitInv6 || invert$1(this.git6);
    this.gitInv7 = this.gitInv7 || invert$1(this.git7);
    this.gitBranchLabel0 = this.gitBranchLabel0 || invert$1(this.labelTextColor);
    this.gitBranchLabel1 = this.gitBranchLabel1 || this.labelTextColor;
    this.gitBranchLabel2 = this.gitBranchLabel2 || this.labelTextColor;
    this.gitBranchLabel3 = this.gitBranchLabel3 || invert$1(this.labelTextColor);
    this.gitBranchLabel4 = this.gitBranchLabel4 || this.labelTextColor;
    this.gitBranchLabel5 = this.gitBranchLabel5 || this.labelTextColor;
    this.gitBranchLabel6 = this.gitBranchLabel6 || this.labelTextColor;
    this.gitBranchLabel7 = this.gitBranchLabel7 || this.labelTextColor;
    this.tagLabelColor = this.tagLabelColor || this.primaryTextColor;
    this.tagLabelBackground = this.tagLabelBackground || this.primaryColor;
    this.tagLabelBorder = this.tagBorder || this.primaryBorderColor;
    this.tagLabelFontSize = this.tagLabelFontSize || "10px";
    this.commitLabelColor = this.commitLabelColor || this.secondaryTextColor;
    this.commitLabelBackground = this.commitLabelBackground || this.secondaryColor;
    this.commitLabelFontSize = this.commitLabelFontSize || "10px";
    this.attributeBackgroundColorOdd = this.attributeBackgroundColorOdd || oldAttributeBackgroundColorOdd;
    this.attributeBackgroundColorEven = this.attributeBackgroundColorEven || oldAttributeBackgroundColorEven;
  }
  calculate(overrides) {
    if (typeof overrides !== "object") {
      this.updateColors();
      return;
    }
    const keys = Object.keys(overrides);
    keys.forEach((k) => {
      this[k] = overrides[k];
    });
    this.updateColors();
    keys.forEach((k) => {
      this[k] = overrides[k];
    });
  }
};
const getThemeVariables$1 = (userOverrides) => {
  const theme2 = new Theme$1();
  theme2.calculate(userOverrides);
  return theme2;
};
class Theme5 {
  constructor() {
    this.primaryColor = "#eee";
    this.contrast = "#707070";
    this.secondaryColor = lighten$1(this.contrast, 55);
    this.background = "#ffffff";
    this.tertiaryColor = adjust$1(this.primaryColor, { h: -160 });
    this.primaryBorderColor = mkBorder(this.primaryColor, this.darkMode);
    this.secondaryBorderColor = mkBorder(this.secondaryColor, this.darkMode);
    this.tertiaryBorderColor = mkBorder(this.tertiaryColor, this.darkMode);
    this.primaryTextColor = invert$1(this.primaryColor);
    this.secondaryTextColor = invert$1(this.secondaryColor);
    this.tertiaryTextColor = invert$1(this.tertiaryColor);
    this.lineColor = invert$1(this.background);
    this.textColor = invert$1(this.background);
    this.mainBkg = "#eee";
    this.secondBkg = "calculated";
    this.lineColor = "#666";
    this.border1 = "#999";
    this.border2 = "calculated";
    this.note = "#ffa";
    this.text = "#333";
    this.critical = "#d42";
    this.done = "#bbb";
    this.arrowheadColor = "#333333";
    this.fontFamily = '"trebuchet ms", verdana, arial, sans-serif';
    this.fontSize = "16px";
    this.THEME_COLOR_LIMIT = 12;
    this.nodeBkg = "calculated";
    this.nodeBorder = "calculated";
    this.clusterBkg = "calculated";
    this.clusterBorder = "calculated";
    this.defaultLinkColor = "calculated";
    this.titleColor = "calculated";
    this.edgeLabelBackground = "white";
    this.actorBorder = "calculated";
    this.actorBkg = "calculated";
    this.actorTextColor = "calculated";
    this.actorLineColor = "calculated";
    this.signalColor = "calculated";
    this.signalTextColor = "calculated";
    this.labelBoxBkgColor = "calculated";
    this.labelBoxBorderColor = "calculated";
    this.labelTextColor = "calculated";
    this.loopTextColor = "calculated";
    this.noteBorderColor = "calculated";
    this.noteBkgColor = "calculated";
    this.noteTextColor = "calculated";
    this.activationBorderColor = "#666";
    this.activationBkgColor = "#f4f4f4";
    this.sequenceNumberColor = "white";
    this.sectionBkgColor = "calculated";
    this.altSectionBkgColor = "white";
    this.sectionBkgColor2 = "calculated";
    this.excludeBkgColor = "#eeeeee";
    this.taskBorderColor = "calculated";
    this.taskBkgColor = "calculated";
    this.taskTextLightColor = "white";
    this.taskTextColor = "calculated";
    this.taskTextDarkColor = "calculated";
    this.taskTextOutsideColor = "calculated";
    this.taskTextClickableColor = "#003163";
    this.activeTaskBorderColor = "calculated";
    this.activeTaskBkgColor = "calculated";
    this.gridColor = "calculated";
    this.doneTaskBkgColor = "calculated";
    this.doneTaskBorderColor = "calculated";
    this.critBkgColor = "calculated";
    this.critBorderColor = "calculated";
    this.todayLineColor = "calculated";
    this.personBorder = this.primaryBorderColor;
    this.personBkg = this.mainBkg;
    this.labelColor = "black";
    this.errorBkgColor = "#552222";
    this.errorTextColor = "#552222";
  }
  updateColors() {
    this.secondBkg = lighten$1(this.contrast, 55);
    this.border2 = this.contrast;
    this.actorBorder = lighten$1(this.border1, 23);
    this.actorBkg = this.mainBkg;
    this.actorTextColor = this.text;
    this.actorLineColor = this.lineColor;
    this.signalColor = this.text;
    this.signalTextColor = this.text;
    this.labelBoxBkgColor = this.actorBkg;
    this.labelBoxBorderColor = this.actorBorder;
    this.labelTextColor = this.text;
    this.loopTextColor = this.text;
    this.noteBorderColor = "#999";
    this.noteBkgColor = "#666";
    this.noteTextColor = "#fff";
    this.cScale0 = this.cScale0 || "#555";
    this.cScale1 = this.cScale1 || "#F4F4F4";
    this.cScale2 = this.cScale2 || "#555";
    this.cScale3 = this.cScale3 || "#BBB";
    this.cScale4 = this.cScale4 || "#777";
    this.cScale5 = this.cScale5 || "#999";
    this.cScale6 = this.cScale6 || "#DDD";
    this.cScale7 = this.cScale7 || "#FFF";
    this.cScale8 = this.cScale8 || "#DDD";
    this.cScale9 = this.cScale9 || "#BBB";
    this.cScale10 = this.cScale10 || "#999";
    this.cScale11 = this.cScale11 || "#777";
    for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
      this["cScaleInv" + i] = this["cScaleInv" + i] || invert$1(this["cScale" + i]);
    }
    for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
      if (this.darkMode) {
        this["cScalePeer" + i] = this["cScalePeer" + i] || lighten$1(this["cScale" + i], 10);
      } else {
        this["cScalePeer" + i] = this["cScalePeer" + i] || darken$1(this["cScale" + i], 10);
      }
    }
    this.scaleLabelColor = this.scaleLabelColor || (this.darkMode ? "black" : this.labelTextColor);
    this["cScaleLabel0"] = this["cScaleLabel0"] || this.cScale1;
    this["cScaleLabel2"] = this["cScaleLabel2"] || this.cScale1;
    for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
      this["cScaleLabel" + i] = this["cScaleLabel" + i] || this.scaleLabelColor;
    }
    for (let i = 0; i < 5; i++) {
      this["surface" + i] = this["surface" + i] || adjust$1(this.mainBkg, { l: -(5 + i * 5) });
      this["surfacePeer" + i] = this["surfacePeer" + i] || adjust$1(this.mainBkg, { l: -(8 + i * 5) });
    }
    this.nodeBkg = this.mainBkg;
    this.nodeBorder = this.border1;
    this.clusterBkg = this.secondBkg;
    this.clusterBorder = this.border2;
    this.defaultLinkColor = this.lineColor;
    this.titleColor = this.text;
    this.sectionBkgColor = lighten$1(this.contrast, 30);
    this.sectionBkgColor2 = lighten$1(this.contrast, 30);
    this.taskBorderColor = darken$1(this.contrast, 10);
    this.taskBkgColor = this.contrast;
    this.taskTextColor = this.taskTextLightColor;
    this.taskTextDarkColor = this.text;
    this.taskTextOutsideColor = this.taskTextDarkColor;
    this.activeTaskBorderColor = this.taskBorderColor;
    this.activeTaskBkgColor = this.mainBkg;
    this.gridColor = lighten$1(this.border1, 30);
    this.doneTaskBkgColor = this.done;
    this.doneTaskBorderColor = this.lineColor;
    this.critBkgColor = this.critical;
    this.critBorderColor = darken$1(this.critBkgColor, 10);
    this.todayLineColor = this.critBkgColor;
    this.transitionColor = this.transitionColor || "#000";
    this.transitionLabelColor = this.transitionLabelColor || this.textColor;
    this.stateLabelColor = this.stateLabelColor || this.stateBkg || this.primaryTextColor;
    this.stateBkg = this.stateBkg || this.mainBkg;
    this.labelBackgroundColor = this.labelBackgroundColor || this.stateBkg;
    this.compositeBackground = this.compositeBackground || this.background || this.tertiaryColor;
    this.altBackground = this.altBackground || "#f4f4f4";
    this.compositeTitleBackground = this.compositeTitleBackground || this.mainBkg;
    this.stateBorder = this.stateBorder || "#000";
    this.innerEndBackground = this.primaryBorderColor;
    this.specialStateColor = "#222";
    this.errorBkgColor = this.errorBkgColor || this.tertiaryColor;
    this.errorTextColor = this.errorTextColor || this.tertiaryTextColor;
    this.classText = this.primaryTextColor;
    this.fillType0 = this.primaryColor;
    this.fillType1 = this.secondaryColor;
    this.fillType2 = adjust$1(this.primaryColor, { h: 64 });
    this.fillType3 = adjust$1(this.secondaryColor, { h: 64 });
    this.fillType4 = adjust$1(this.primaryColor, { h: -64 });
    this.fillType5 = adjust$1(this.secondaryColor, { h: -64 });
    this.fillType6 = adjust$1(this.primaryColor, { h: 128 });
    this.fillType7 = adjust$1(this.secondaryColor, { h: 128 });
    for (let i = 0; i < this.THEME_COLOR_LIMIT; i++) {
      this["pie" + i] = this["cScale" + i];
    }
    this.pie12 = this.pie0;
    this.pieTitleTextSize = this.pieTitleTextSize || "25px";
    this.pieTitleTextColor = this.pieTitleTextColor || this.taskTextDarkColor;
    this.pieSectionTextSize = this.pieSectionTextSize || "17px";
    this.pieSectionTextColor = this.pieSectionTextColor || this.textColor;
    this.pieLegendTextSize = this.pieLegendTextSize || "17px";
    this.pieLegendTextColor = this.pieLegendTextColor || this.taskTextDarkColor;
    this.pieStrokeColor = this.pieStrokeColor || "black";
    this.pieStrokeWidth = this.pieStrokeWidth || "2px";
    this.pieOuterStrokeWidth = this.pieOuterStrokeWidth || "2px";
    this.pieOuterStrokeColor = this.pieOuterStrokeColor || "black";
    this.pieOpacity = this.pieOpacity || "0.7";
    this.quadrant1Fill = this.quadrant1Fill || this.primaryColor;
    this.quadrant2Fill = this.quadrant2Fill || adjust$1(this.primaryColor, { r: 5, g: 5, b: 5 });
    this.quadrant3Fill = this.quadrant3Fill || adjust$1(this.primaryColor, { r: 10, g: 10, b: 10 });
    this.quadrant4Fill = this.quadrant4Fill || adjust$1(this.primaryColor, { r: 15, g: 15, b: 15 });
    this.quadrant1TextFill = this.quadrant1TextFill || this.primaryTextColor;
    this.quadrant2TextFill = this.quadrant2TextFill || adjust$1(this.primaryTextColor, { r: -5, g: -5, b: -5 });
    this.quadrant3TextFill = this.quadrant3TextFill || adjust$1(this.primaryTextColor, { r: -10, g: -10, b: -10 });
    this.quadrant4TextFill = this.quadrant4TextFill || adjust$1(this.primaryTextColor, { r: -15, g: -15, b: -15 });
    this.quadrantPointFill = this.quadrantPointFill || isDark$1(this.quadrant1Fill) ? lighten$1(this.quadrant1Fill) : darken$1(this.quadrant1Fill);
    this.quadrantPointTextFill = this.quadrantPointTextFill || this.primaryTextColor;
    this.quadrantXAxisTextFill = this.quadrantXAxisTextFill || this.primaryTextColor;
    this.quadrantYAxisTextFill = this.quadrantYAxisTextFill || this.primaryTextColor;
    this.quadrantInternalBorderStrokeFill = this.quadrantInternalBorderStrokeFill || this.primaryBorderColor;
    this.quadrantExternalBorderStrokeFill = this.quadrantExternalBorderStrokeFill || this.primaryBorderColor;
    this.quadrantTitleFill = this.quadrantTitleFill || this.primaryTextColor;
    this.requirementBackground = this.requirementBackground || this.primaryColor;
    this.requirementBorderColor = this.requirementBorderColor || this.primaryBorderColor;
    this.requirementBorderSize = this.requirementBorderSize || "1";
    this.requirementTextColor = this.requirementTextColor || this.primaryTextColor;
    this.relationColor = this.relationColor || this.lineColor;
    this.relationLabelBackground = this.relationLabelBackground || this.edgeLabelBackground;
    this.relationLabelColor = this.relationLabelColor || this.actorTextColor;
    this.git0 = darken$1(this.pie1, 25) || this.primaryColor;
    this.git1 = this.pie2 || this.secondaryColor;
    this.git2 = this.pie3 || this.tertiaryColor;
    this.git3 = this.pie4 || adjust$1(this.primaryColor, { h: -30 });
    this.git4 = this.pie5 || adjust$1(this.primaryColor, { h: -60 });
    this.git5 = this.pie6 || adjust$1(this.primaryColor, { h: -90 });
    this.git6 = this.pie7 || adjust$1(this.primaryColor, { h: 60 });
    this.git7 = this.pie8 || adjust$1(this.primaryColor, { h: 120 });
    this.gitInv0 = this.gitInv0 || invert$1(this.git0);
    this.gitInv1 = this.gitInv1 || invert$1(this.git1);
    this.gitInv2 = this.gitInv2 || invert$1(this.git2);
    this.gitInv3 = this.gitInv3 || invert$1(this.git3);
    this.gitInv4 = this.gitInv4 || invert$1(this.git4);
    this.gitInv5 = this.gitInv5 || invert$1(this.git5);
    this.gitInv6 = this.gitInv6 || invert$1(this.git6);
    this.gitInv7 = this.gitInv7 || invert$1(this.git7);
    this.branchLabelColor = this.branchLabelColor || this.labelTextColor;
    this.gitBranchLabel0 = this.branchLabelColor;
    this.gitBranchLabel1 = "white";
    this.gitBranchLabel2 = this.branchLabelColor;
    this.gitBranchLabel3 = "white";
    this.gitBranchLabel4 = this.branchLabelColor;
    this.gitBranchLabel5 = this.branchLabelColor;
    this.gitBranchLabel6 = this.branchLabelColor;
    this.gitBranchLabel7 = this.branchLabelColor;
    this.tagLabelColor = this.tagLabelColor || this.primaryTextColor;
    this.tagLabelBackground = this.tagLabelBackground || this.primaryColor;
    this.tagLabelBorder = this.tagBorder || this.primaryBorderColor;
    this.tagLabelFontSize = this.tagLabelFontSize || "10px";
    this.commitLabelColor = this.commitLabelColor || this.secondaryTextColor;
    this.commitLabelBackground = this.commitLabelBackground || this.secondaryColor;
    this.commitLabelFontSize = this.commitLabelFontSize || "10px";
    this.attributeBackgroundColorOdd = this.attributeBackgroundColorOdd || oldAttributeBackgroundColorOdd;
    this.attributeBackgroundColorEven = this.attributeBackgroundColorEven || oldAttributeBackgroundColorEven;
  }
  calculate(overrides) {
    if (typeof overrides !== "object") {
      this.updateColors();
      return;
    }
    const keys = Object.keys(overrides);
    keys.forEach((k) => {
      this[k] = overrides[k];
    });
    this.updateColors();
    keys.forEach((k) => {
      this[k] = overrides[k];
    });
  }
}
const getThemeVariables = (userOverrides) => {
  const theme2 = new Theme5();
  theme2.calculate(userOverrides);
  return theme2;
};
const theme = {
  base: {
    getThemeVariables: getThemeVariables$4
  },
  dark: {
    getThemeVariables: getThemeVariables$3
  },
  default: {
    getThemeVariables: getThemeVariables$2
  },
  forest: {
    getThemeVariables: getThemeVariables$1
  },
  neutral: {
    getThemeVariables
  }
};
const defaultConfigJson = {
  "flowchart": {
    "useMaxWidth": true,
    "titleTopMargin": 25,
    "diagramPadding": 8,
    "htmlLabels": true,
    "nodeSpacing": 50,
    "rankSpacing": 50,
    "curve": "basis",
    "padding": 15,
    "defaultRenderer": "dagre-wrapper",
    "wrappingWidth": 200
  },
  "sequence": {
    "useMaxWidth": true,
    "hideUnusedParticipants": false,
    "activationWidth": 10,
    "diagramMarginX": 50,
    "diagramMarginY": 10,
    "actorMargin": 50,
    "width": 150,
    "height": 65,
    "boxMargin": 10,
    "boxTextMargin": 5,
    "noteMargin": 10,
    "messageMargin": 35,
    "messageAlign": "center",
    "mirrorActors": true,
    "forceMenus": false,
    "bottomMarginAdj": 1,
    "rightAngles": false,
    "showSequenceNumbers": false,
    "actorFontSize": 14,
    "actorFontFamily": '"Open Sans", sans-serif',
    "actorFontWeight": 400,
    "noteFontSize": 14,
    "noteFontFamily": '"trebuchet ms", verdana, arial, sans-serif',
    "noteFontWeight": 400,
    "noteAlign": "center",
    "messageFontSize": 16,
    "messageFontFamily": '"trebuchet ms", verdana, arial, sans-serif',
    "messageFontWeight": 400,
    "wrap": false,
    "wrapPadding": 10,
    "labelBoxWidth": 50,
    "labelBoxHeight": 20
  },
  "gantt": {
    "useMaxWidth": true,
    "titleTopMargin": 25,
    "barHeight": 20,
    "barGap": 4,
    "topPadding": 50,
    "rightPadding": 75,
    "leftPadding": 75,
    "gridLineStartPadding": 35,
    "fontSize": 11,
    "sectionFontSize": 11,
    "numberSectionStyles": 4,
    "axisFormat": "%Y-%m-%d",
    "topAxis": false,
    "displayMode": "",
    "weekday": "sunday"
  },
  "journey": {
    "useMaxWidth": true,
    "diagramMarginX": 50,
    "diagramMarginY": 10,
    "leftMargin": 150,
    "width": 150,
    "height": 50,
    "boxMargin": 10,
    "boxTextMargin": 5,
    "noteMargin": 10,
    "messageMargin": 35,
    "messageAlign": "center",
    "bottomMarginAdj": 1,
    "rightAngles": false,
    "taskFontSize": 14,
    "taskFontFamily": '"Open Sans", sans-serif',
    "taskMargin": 50,
    "activationWidth": 10,
    "textPlacement": "fo",
    "actorColours": [
      "#8FBC8F",
      "#7CFC00",
      "#00FFFF",
      "#20B2AA",
      "#B0E0E6",
      "#FFFFE0"
    ],
    "sectionFills": [
      "#191970",
      "#8B008B",
      "#4B0082",
      "#2F4F4F",
      "#800000",
      "#8B4513",
      "#00008B"
    ],
    "sectionColours": [
      "#fff"
    ]
  },
  "class": {
    "useMaxWidth": true,
    "titleTopMargin": 25,
    "arrowMarkerAbsolute": false,
    "dividerMargin": 10,
    "padding": 5,
    "textHeight": 10,
    "defaultRenderer": "dagre-wrapper",
    "htmlLabels": false
  },
  "state": {
    "useMaxWidth": true,
    "titleTopMargin": 25,
    "dividerMargin": 10,
    "sizeUnit": 5,
    "padding": 8,
    "textHeight": 10,
    "titleShift": -15,
    "noteMargin": 10,
    "forkWidth": 70,
    "forkHeight": 7,
    "miniPadding": 2,
    "fontSizeFactor": 5.02,
    "fontSize": 24,
    "labelHeight": 16,
    "edgeLengthFactor": "20",
    "compositTitleSize": 35,
    "radius": 5,
    "defaultRenderer": "dagre-wrapper"
  },
  "er": {
    "useMaxWidth": true,
    "titleTopMargin": 25,
    "diagramPadding": 20,
    "layoutDirection": "TB",
    "minEntityWidth": 100,
    "minEntityHeight": 75,
    "entityPadding": 15,
    "stroke": "gray",
    "fill": "honeydew",
    "fontSize": 12
  },
  "pie": {
    "useMaxWidth": true,
    "textPosition": 0.75
  },
  "quadrantChart": {
    "useMaxWidth": true,
    "chartWidth": 500,
    "chartHeight": 500,
    "titleFontSize": 20,
    "titlePadding": 10,
    "quadrantPadding": 5,
    "xAxisLabelPadding": 5,
    "yAxisLabelPadding": 5,
    "xAxisLabelFontSize": 16,
    "yAxisLabelFontSize": 16,
    "quadrantLabelFontSize": 16,
    "quadrantTextTopPadding": 5,
    "pointTextPadding": 5,
    "pointLabelFontSize": 12,
    "pointRadius": 5,
    "xAxisPosition": "top",
    "yAxisPosition": "left",
    "quadrantInternalBorderStrokeWidth": 1,
    "quadrantExternalBorderStrokeWidth": 2
  },
  "requirement": {
    "useMaxWidth": true,
    "rect_fill": "#f9f9f9",
    "text_color": "#333",
    "rect_border_size": "0.5px",
    "rect_border_color": "#bbb",
    "rect_min_width": 200,
    "rect_min_height": 200,
    "fontSize": 14,
    "rect_padding": 10,
    "line_height": 20
  },
  "mindmap": {
    "useMaxWidth": true,
    "padding": 10,
    "maxNodeWidth": 200
  },
  "timeline": {
    "useMaxWidth": true,
    "diagramMarginX": 50,
    "diagramMarginY": 10,
    "leftMargin": 150,
    "width": 150,
    "height": 50,
    "boxMargin": 10,
    "boxTextMargin": 5,
    "noteMargin": 10,
    "messageMargin": 35,
    "messageAlign": "center",
    "bottomMarginAdj": 1,
    "rightAngles": false,
    "taskFontSize": 14,
    "taskFontFamily": '"Open Sans", sans-serif',
    "taskMargin": 50,
    "activationWidth": 10,
    "textPlacement": "fo",
    "actorColours": [
      "#8FBC8F",
      "#7CFC00",
      "#00FFFF",
      "#20B2AA",
      "#B0E0E6",
      "#FFFFE0"
    ],
    "sectionFills": [
      "#191970",
      "#8B008B",
      "#4B0082",
      "#2F4F4F",
      "#800000",
      "#8B4513",
      "#00008B"
    ],
    "sectionColours": [
      "#fff"
    ],
    "disableMulticolor": false
  },
  "gitGraph": {
    "useMaxWidth": true,
    "titleTopMargin": 25,
    "diagramPadding": 8,
    "nodeLabel": {
      "width": 75,
      "height": 100,
      "x": -25,
      "y": 0
    },
    "mainBranchName": "main",
    "mainBranchOrder": 0,
    "showCommitLabel": true,
    "showBranches": true,
    "rotateCommitLabel": true,
    "arrowMarkerAbsolute": false
  },
  "c4": {
    "useMaxWidth": true,
    "diagramMarginX": 50,
    "diagramMarginY": 10,
    "c4ShapeMargin": 50,
    "c4ShapePadding": 20,
    "width": 216,
    "height": 60,
    "boxMargin": 10,
    "c4ShapeInRow": 4,
    "nextLinePaddingX": 0,
    "c4BoundaryInRow": 2,
    "personFontSize": 14,
    "personFontFamily": '"Open Sans", sans-serif',
    "personFontWeight": "normal",
    "external_personFontSize": 14,
    "external_personFontFamily": '"Open Sans", sans-serif',
    "external_personFontWeight": "normal",
    "systemFontSize": 14,
    "systemFontFamily": '"Open Sans", sans-serif',
    "systemFontWeight": "normal",
    "external_systemFontSize": 14,
    "external_systemFontFamily": '"Open Sans", sans-serif',
    "external_systemFontWeight": "normal",
    "system_dbFontSize": 14,
    "system_dbFontFamily": '"Open Sans", sans-serif',
    "system_dbFontWeight": "normal",
    "external_system_dbFontSize": 14,
    "external_system_dbFontFamily": '"Open Sans", sans-serif',
    "external_system_dbFontWeight": "normal",
    "system_queueFontSize": 14,
    "system_queueFontFamily": '"Open Sans", sans-serif',
    "system_queueFontWeight": "normal",
    "external_system_queueFontSize": 14,
    "external_system_queueFontFamily": '"Open Sans", sans-serif',
    "external_system_queueFontWeight": "normal",
    "boundaryFontSize": 14,
    "boundaryFontFamily": '"Open Sans", sans-serif',
    "boundaryFontWeight": "normal",
    "messageFontSize": 12,
    "messageFontFamily": '"Open Sans", sans-serif',
    "messageFontWeight": "normal",
    "containerFontSize": 14,
    "containerFontFamily": '"Open Sans", sans-serif',
    "containerFontWeight": "normal",
    "external_containerFontSize": 14,
    "external_containerFontFamily": '"Open Sans", sans-serif',
    "external_containerFontWeight": "normal",
    "container_dbFontSize": 14,
    "container_dbFontFamily": '"Open Sans", sans-serif',
    "container_dbFontWeight": "normal",
    "external_container_dbFontSize": 14,
    "external_container_dbFontFamily": '"Open Sans", sans-serif',
    "external_container_dbFontWeight": "normal",
    "container_queueFontSize": 14,
    "container_queueFontFamily": '"Open Sans", sans-serif',
    "container_queueFontWeight": "normal",
    "external_container_queueFontSize": 14,
    "external_container_queueFontFamily": '"Open Sans", sans-serif',
    "external_container_queueFontWeight": "normal",
    "componentFontSize": 14,
    "componentFontFamily": '"Open Sans", sans-serif',
    "componentFontWeight": "normal",
    "external_componentFontSize": 14,
    "external_componentFontFamily": '"Open Sans", sans-serif',
    "external_componentFontWeight": "normal",
    "component_dbFontSize": 14,
    "component_dbFontFamily": '"Open Sans", sans-serif',
    "component_dbFontWeight": "normal",
    "external_component_dbFontSize": 14,
    "external_component_dbFontFamily": '"Open Sans", sans-serif',
    "external_component_dbFontWeight": "normal",
    "component_queueFontSize": 14,
    "component_queueFontFamily": '"Open Sans", sans-serif',
    "component_queueFontWeight": "normal",
    "external_component_queueFontSize": 14,
    "external_component_queueFontFamily": '"Open Sans", sans-serif',
    "external_component_queueFontWeight": "normal",
    "wrap": true,
    "wrapPadding": 10,
    "person_bg_color": "#08427B",
    "person_border_color": "#073B6F",
    "external_person_bg_color": "#686868",
    "external_person_border_color": "#8A8A8A",
    "system_bg_color": "#1168BD",
    "system_border_color": "#3C7FC0",
    "system_db_bg_color": "#1168BD",
    "system_db_border_color": "#3C7FC0",
    "system_queue_bg_color": "#1168BD",
    "system_queue_border_color": "#3C7FC0",
    "external_system_bg_color": "#999999",
    "external_system_border_color": "#8A8A8A",
    "external_system_db_bg_color": "#999999",
    "external_system_db_border_color": "#8A8A8A",
    "external_system_queue_bg_color": "#999999",
    "external_system_queue_border_color": "#8A8A8A",
    "container_bg_color": "#438DD5",
    "container_border_color": "#3C7FC0",
    "container_db_bg_color": "#438DD5",
    "container_db_border_color": "#3C7FC0",
    "container_queue_bg_color": "#438DD5",
    "container_queue_border_color": "#3C7FC0",
    "external_container_bg_color": "#B3B3B3",
    "external_container_border_color": "#A6A6A6",
    "external_container_db_bg_color": "#B3B3B3",
    "external_container_db_border_color": "#A6A6A6",
    "external_container_queue_bg_color": "#B3B3B3",
    "external_container_queue_border_color": "#A6A6A6",
    "component_bg_color": "#85BBF0",
    "component_border_color": "#78A8D8",
    "component_db_bg_color": "#85BBF0",
    "component_db_border_color": "#78A8D8",
    "component_queue_bg_color": "#85BBF0",
    "component_queue_border_color": "#78A8D8",
    "external_component_bg_color": "#CCCCCC",
    "external_component_border_color": "#BFBFBF",
    "external_component_db_bg_color": "#CCCCCC",
    "external_component_db_border_color": "#BFBFBF",
    "external_component_queue_bg_color": "#CCCCCC",
    "external_component_queue_border_color": "#BFBFBF"
  },
  "sankey": {
    "useMaxWidth": true,
    "width": 600,
    "height": 400,
    "linkColor": "gradient",
    "nodeAlignment": "justify",
    "showValues": true,
    "prefix": "",
    "suffix": ""
  },
  "theme": "default",
  "maxTextSize": 5e4,
  "darkMode": false,
  "fontFamily": '"trebuchet ms", verdana, arial, sans-serif;',
  "logLevel": 5,
  "securityLevel": "strict",
  "startOnLoad": true,
  "arrowMarkerAbsolute": false,
  "secure": [
    "secure",
    "securityLevel",
    "startOnLoad",
    "maxTextSize"
  ],
  "deterministicIds": false,
  "fontSize": 16
};
const config = {
  ...defaultConfigJson,
  // Set, even though they're `undefined` so that `configKeys` finds these keys
  // TODO: Should we replace these with `null` so that they can go in the JSON Schema?
  deterministicIDSeed: void 0,
  themeCSS: void 0,
  // add non-JSON default config values
  themeVariables: theme["default"].getThemeVariables(),
  sequence: {
    ...defaultConfigJson.sequence,
    messageFont: function() {
      return {
        fontFamily: this.messageFontFamily,
        fontSize: this.messageFontSize,
        fontWeight: this.messageFontWeight
      };
    },
    noteFont: function() {
      return {
        fontFamily: this.noteFontFamily,
        fontSize: this.noteFontSize,
        fontWeight: this.noteFontWeight
      };
    },
    actorFont: function() {
      return {
        fontFamily: this.actorFontFamily,
        fontSize: this.actorFontSize,
        fontWeight: this.actorFontWeight
      };
    }
  },
  gantt: {
    ...defaultConfigJson.gantt,
    tickInterval: void 0,
    useWidth: void 0
    // can probably be removed since `configKeys` already includes this
  },
  c4: {
    ...defaultConfigJson.c4,
    useWidth: void 0,
    personFont: function() {
      return {
        fontFamily: this.personFontFamily,
        fontSize: this.personFontSize,
        fontWeight: this.personFontWeight
      };
    },
    external_personFont: function() {
      return {
        fontFamily: this.external_personFontFamily,
        fontSize: this.external_personFontSize,
        fontWeight: this.external_personFontWeight
      };
    },
    systemFont: function() {
      return {
        fontFamily: this.systemFontFamily,
        fontSize: this.systemFontSize,
        fontWeight: this.systemFontWeight
      };
    },
    external_systemFont: function() {
      return {
        fontFamily: this.external_systemFontFamily,
        fontSize: this.external_systemFontSize,
        fontWeight: this.external_systemFontWeight
      };
    },
    system_dbFont: function() {
      return {
        fontFamily: this.system_dbFontFamily,
        fontSize: this.system_dbFontSize,
        fontWeight: this.system_dbFontWeight
      };
    },
    external_system_dbFont: function() {
      return {
        fontFamily: this.external_system_dbFontFamily,
        fontSize: this.external_system_dbFontSize,
        fontWeight: this.external_system_dbFontWeight
      };
    },
    system_queueFont: function() {
      return {
        fontFamily: this.system_queueFontFamily,
        fontSize: this.system_queueFontSize,
        fontWeight: this.system_queueFontWeight
      };
    },
    external_system_queueFont: function() {
      return {
        fontFamily: this.external_system_queueFontFamily,
        fontSize: this.external_system_queueFontSize,
        fontWeight: this.external_system_queueFontWeight
      };
    },
    containerFont: function() {
      return {
        fontFamily: this.containerFontFamily,
        fontSize: this.containerFontSize,
        fontWeight: this.containerFontWeight
      };
    },
    external_containerFont: function() {
      return {
        fontFamily: this.external_containerFontFamily,
        fontSize: this.external_containerFontSize,
        fontWeight: this.external_containerFontWeight
      };
    },
    container_dbFont: function() {
      return {
        fontFamily: this.container_dbFontFamily,
        fontSize: this.container_dbFontSize,
        fontWeight: this.container_dbFontWeight
      };
    },
    external_container_dbFont: function() {
      return {
        fontFamily: this.external_container_dbFontFamily,
        fontSize: this.external_container_dbFontSize,
        fontWeight: this.external_container_dbFontWeight
      };
    },
    container_queueFont: function() {
      return {
        fontFamily: this.container_queueFontFamily,
        fontSize: this.container_queueFontSize,
        fontWeight: this.container_queueFontWeight
      };
    },
    external_container_queueFont: function() {
      return {
        fontFamily: this.external_container_queueFontFamily,
        fontSize: this.external_container_queueFontSize,
        fontWeight: this.external_container_queueFontWeight
      };
    },
    componentFont: function() {
      return {
        fontFamily: this.componentFontFamily,
        fontSize: this.componentFontSize,
        fontWeight: this.componentFontWeight
      };
    },
    external_componentFont: function() {
      return {
        fontFamily: this.external_componentFontFamily,
        fontSize: this.external_componentFontSize,
        fontWeight: this.external_componentFontWeight
      };
    },
    component_dbFont: function() {
      return {
        fontFamily: this.component_dbFontFamily,
        fontSize: this.component_dbFontSize,
        fontWeight: this.component_dbFontWeight
      };
    },
    external_component_dbFont: function() {
      return {
        fontFamily: this.external_component_dbFontFamily,
        fontSize: this.external_component_dbFontSize,
        fontWeight: this.external_component_dbFontWeight
      };
    },
    component_queueFont: function() {
      return {
        fontFamily: this.component_queueFontFamily,
        fontSize: this.component_queueFontSize,
        fontWeight: this.component_queueFontWeight
      };
    },
    external_component_queueFont: function() {
      return {
        fontFamily: this.external_component_queueFontFamily,
        fontSize: this.external_component_queueFontSize,
        fontWeight: this.external_component_queueFontWeight
      };
    },
    boundaryFont: function() {
      return {
        fontFamily: this.boundaryFontFamily,
        fontSize: this.boundaryFontSize,
        fontWeight: this.boundaryFontWeight
      };
    },
    messageFont: function() {
      return {
        fontFamily: this.messageFontFamily,
        fontSize: this.messageFontSize,
        fontWeight: this.messageFontWeight
      };
    }
  },
  pie: {
    ...defaultConfigJson.pie,
    useWidth: 984
  },
  requirement: {
    ...defaultConfigJson.requirement,
    useWidth: void 0
  },
  gitGraph: {
    ...defaultConfigJson.gitGraph,
    // TODO: This is a temporary override for `gitGraph`, since every other
    //       diagram does have `useMaxWidth`, but instead sets it to `true`.
    //       Should we set this to `true` instead?
    useMaxWidth: false
  },
  sankey: {
    ...defaultConfigJson.sankey,
    // this is false, unlike every other diagram (other than gitGraph)
    // TODO: can we make this default to `true` instead?
    useMaxWidth: false
  }
};
const keyify = (obj, prefix = "") => Object.keys(obj).reduce((res, el) => {
  if (Array.isArray(obj[el])) {
    return res;
  } else if (typeof obj[el] === "object" && obj[el] !== null) {
    return [...res, prefix + el, ...keyify(obj[el], "")];
  }
  return [...res, prefix + el];
}, []);
const configKeys = new Set(keyify(config, ""));
const defaultConfig$1 = config;
const sanitizeDirective = (args) => {
  log$1.debug("sanitizeDirective called with", args);
  if (typeof args !== "object" || args == null) {
    return;
  }
  if (Array.isArray(args)) {
    args.forEach((arg) => sanitizeDirective(arg));
    return;
  }
  for (const key of Object.keys(args)) {
    log$1.debug("Checking key", key);
    if (key.startsWith("__") || key.includes("proto") || key.includes("constr") || !configKeys.has(key) || args[key] == null) {
      log$1.debug("sanitize deleting key: ", key);
      delete args[key];
      continue;
    }
    if (typeof args[key] === "object") {
      log$1.debug("sanitizing object", key);
      sanitizeDirective(args[key]);
      continue;
    }
    const cssMatchers = ["themeCSS", "fontFamily", "altFontFamily"];
    for (const cssKey of cssMatchers) {
      if (key.includes(cssKey)) {
        log$1.debug("sanitizing css option", key);
        args[key] = sanitizeCss(args[key]);
      }
    }
  }
  if (args.themeVariables) {
    for (const k of Object.keys(args.themeVariables)) {
      const val = args.themeVariables[k];
      if ((val == null ? void 0 : val.match) && !val.match(/^[\d "#%(),.;A-Za-z]+$/)) {
        args.themeVariables[k] = "";
      }
    }
  }
  log$1.debug("After sanitization", args);
};
const sanitizeCss = (str2) => {
  let startCnt = 0;
  let endCnt = 0;
  for (const element of str2) {
    if (startCnt < endCnt) {
      return "{ /* ERROR: Unbalanced CSS */ }";
    }
    if (element === "{") {
      startCnt++;
    } else if (element === "}") {
      endCnt++;
    }
  }
  if (startCnt !== endCnt) {
    return "{ /* ERROR: Unbalanced CSS */ }";
  }
  return str2;
};
const frontMatterRegex = /^-{3}\s*[\n\r](.*?)[\n\r]-{3}\s*[\n\r]+/s;
const directiveRegex = /%{2}{\s*(?:(\w+)\s*:|(\w+))\s*(?:(\w+)|((?:(?!}%{2}).|\r?\n)*))?\s*(?:}%{2})?/gi;
const anyCommentRegex = /\s*%%.*\n/gm;
class UnknownDiagramError extends Error {
  constructor(message) {
    super(message);
    this.name = "UnknownDiagramError";
  }
}
const detectors = {};
const detectType = function(text2, config2) {
  text2 = text2.replace(frontMatterRegex, "").replace(directiveRegex, "").replace(anyCommentRegex, "\n");
  for (const [key, { detector: detector2 }] of Object.entries(detectors)) {
    const diagram2 = detector2(text2, config2);
    if (diagram2) {
      return key;
    }
  }
  throw new UnknownDiagramError(
    `No diagram type detected matching given configuration for text: ${text2}`
  );
};
const registerLazyLoadedDiagrams = (...diagrams2) => {
  for (const { id: id2, detector: detector2, loader: loader2 } of diagrams2) {
    addDetector(id2, detector2, loader2);
  }
};
const addDetector = (key, detector2, loader2) => {
  if (detectors[key]) {
    log$1.error(`Detector with key ${key} already exists`);
  } else {
    detectors[key] = { detector: detector2, loader: loader2 };
  }
  log$1.debug(`Detector with key ${key} added${loader2 ? " with loader" : ""}`);
};
const getDiagramLoader = (key) => {
  return detectors[key].loader;
};
const assignWithDepth = (dst, src, { depth = 2, clobber = false } = {}) => {
  const config2 = { depth, clobber };
  if (Array.isArray(src) && !Array.isArray(dst)) {
    src.forEach((s) => assignWithDepth(dst, s, config2));
    return dst;
  } else if (Array.isArray(src) && Array.isArray(dst)) {
    src.forEach((s) => {
      if (!dst.includes(s)) {
        dst.push(s);
      }
    });
    return dst;
  }
  if (dst === void 0 || depth <= 0) {
    if (dst !== void 0 && dst !== null && typeof dst === "object" && typeof src === "object") {
      return Object.assign(dst, src);
    } else {
      return src;
    }
  }
  if (src !== void 0 && typeof dst === "object" && typeof src === "object") {
    Object.keys(src).forEach((key) => {
      if (typeof src[key] === "object" && (dst[key] === void 0 || typeof dst[key] === "object")) {
        if (dst[key] === void 0) {
          dst[key] = Array.isArray(src[key]) ? [] : {};
        }
        dst[key] = assignWithDepth(dst[key], src[key], { depth: depth - 1, clobber });
      } else if (clobber || typeof dst[key] !== "object" && typeof src[key] !== "object") {
        dst[key] = src[key];
      }
    });
  }
  return dst;
};
const assignWithDepth$1 = assignWithDepth;
var freeGlobal = typeof global == "object" && global && global.Object === Object && global;
const freeGlobal$1 = freeGlobal;
var freeSelf = typeof self == "object" && self && self.Object === Object && self;
var root = freeGlobal$1 || freeSelf || Function("return this")();
const root$1 = root;
var Symbol$1 = root$1.Symbol;
const Symbol$2 = Symbol$1;
var objectProto$c = Object.prototype;
var hasOwnProperty$a = objectProto$c.hasOwnProperty;
var nativeObjectToString$1 = objectProto$c.toString;
var symToStringTag$1 = Symbol$2 ? Symbol$2.toStringTag : void 0;
function getRawTag(value) {
  var isOwn = hasOwnProperty$a.call(value, symToStringTag$1), tag = value[symToStringTag$1];
  try {
    value[symToStringTag$1] = void 0;
    var unmasked = true;
  } catch (e) {
  }
  var result = nativeObjectToString$1.call(value);
  if (unmasked) {
    if (isOwn) {
      value[symToStringTag$1] = tag;
    } else {
      delete value[symToStringTag$1];
    }
  }
  return result;
}
var objectProto$b = Object.prototype;
var nativeObjectToString = objectProto$b.toString;
function objectToString(value) {
  return nativeObjectToString.call(value);
}
var nullTag = "[object Null]", undefinedTag = "[object Undefined]";
var symToStringTag = Symbol$2 ? Symbol$2.toStringTag : void 0;
function baseGetTag(value) {
  if (value == null) {
    return value === void 0 ? undefinedTag : nullTag;
  }
  return symToStringTag && symToStringTag in Object(value) ? getRawTag(value) : objectToString(value);
}
function isObject$1(value) {
  var type2 = typeof value;
  return value != null && (type2 == "object" || type2 == "function");
}
var asyncTag = "[object AsyncFunction]", funcTag$1 = "[object Function]", genTag = "[object GeneratorFunction]", proxyTag = "[object Proxy]";
function isFunction(value) {
  if (!isObject$1(value)) {
    return false;
  }
  var tag = baseGetTag(value);
  return tag == funcTag$1 || tag == genTag || tag == asyncTag || tag == proxyTag;
}
var coreJsData = root$1["__core-js_shared__"];
const coreJsData$1 = coreJsData;
var maskSrcKey = function() {
  var uid = /[^.]+$/.exec(coreJsData$1 && coreJsData$1.keys && coreJsData$1.keys.IE_PROTO || "");
  return uid ? "Symbol(src)_1." + uid : "";
}();
function isMasked(func) {
  return !!maskSrcKey && maskSrcKey in func;
}
var funcProto$2 = Function.prototype;
var funcToString$2 = funcProto$2.toString;
function toSource(func) {
  if (func != null) {
    try {
      return funcToString$2.call(func);
    } catch (e) {
    }
    try {
      return func + "";
    } catch (e) {
    }
  }
  return "";
}
var reRegExpChar = /[\\^$.*+?()[\]{}|]/g;
var reIsHostCtor = /^\[object .+?Constructor\]$/;
var funcProto$1 = Function.prototype, objectProto$a = Object.prototype;
var funcToString$1 = funcProto$1.toString;
var hasOwnProperty$9 = objectProto$a.hasOwnProperty;
var reIsNative = RegExp(
  "^" + funcToString$1.call(hasOwnProperty$9).replace(reRegExpChar, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$"
);
function baseIsNative(value) {
  if (!isObject$1(value) || isMasked(value)) {
    return false;
  }
  var pattern = isFunction(value) ? reIsNative : reIsHostCtor;
  return pattern.test(toSource(value));
}
function getValue(object, key) {
  return object == null ? void 0 : object[key];
}
function getNative(object, key) {
  var value = getValue(object, key);
  return baseIsNative(value) ? value : void 0;
}
var nativeCreate = getNative(Object, "create");
const nativeCreate$1 = nativeCreate;
function hashClear() {
  this.__data__ = nativeCreate$1 ? nativeCreate$1(null) : {};
  this.size = 0;
}
function hashDelete(key) {
  var result = this.has(key) && delete this.__data__[key];
  this.size -= result ? 1 : 0;
  return result;
}
var HASH_UNDEFINED$1 = "__lodash_hash_undefined__";
var objectProto$9 = Object.prototype;
var hasOwnProperty$8 = objectProto$9.hasOwnProperty;
function hashGet(key) {
  var data = this.__data__;
  if (nativeCreate$1) {
    var result = data[key];
    return result === HASH_UNDEFINED$1 ? void 0 : result;
  }
  return hasOwnProperty$8.call(data, key) ? data[key] : void 0;
}
var objectProto$8 = Object.prototype;
var hasOwnProperty$7 = objectProto$8.hasOwnProperty;
function hashHas(key) {
  var data = this.__data__;
  return nativeCreate$1 ? data[key] !== void 0 : hasOwnProperty$7.call(data, key);
}
var HASH_UNDEFINED = "__lodash_hash_undefined__";
function hashSet(key, value) {
  var data = this.__data__;
  this.size += this.has(key) ? 0 : 1;
  data[key] = nativeCreate$1 && value === void 0 ? HASH_UNDEFINED : value;
  return this;
}
function Hash(entries2) {
  var index = -1, length2 = entries2 == null ? 0 : entries2.length;
  this.clear();
  while (++index < length2) {
    var entry = entries2[index];
    this.set(entry[0], entry[1]);
  }
}
Hash.prototype.clear = hashClear;
Hash.prototype["delete"] = hashDelete;
Hash.prototype.get = hashGet;
Hash.prototype.has = hashHas;
Hash.prototype.set = hashSet;
function listCacheClear() {
  this.__data__ = [];
  this.size = 0;
}
function eq(value, other) {
  return value === other || value !== value && other !== other;
}
function assocIndexOf(array2, key) {
  var length2 = array2.length;
  while (length2--) {
    if (eq(array2[length2][0], key)) {
      return length2;
    }
  }
  return -1;
}
var arrayProto = Array.prototype;
var splice = arrayProto.splice;
function listCacheDelete(key) {
  var data = this.__data__, index = assocIndexOf(data, key);
  if (index < 0) {
    return false;
  }
  var lastIndex = data.length - 1;
  if (index == lastIndex) {
    data.pop();
  } else {
    splice.call(data, index, 1);
  }
  --this.size;
  return true;
}
function listCacheGet(key) {
  var data = this.__data__, index = assocIndexOf(data, key);
  return index < 0 ? void 0 : data[index][1];
}
function listCacheHas(key) {
  return assocIndexOf(this.__data__, key) > -1;
}
function listCacheSet(key, value) {
  var data = this.__data__, index = assocIndexOf(data, key);
  if (index < 0) {
    ++this.size;
    data.push([key, value]);
  } else {
    data[index][1] = value;
  }
  return this;
}
function ListCache(entries2) {
  var index = -1, length2 = entries2 == null ? 0 : entries2.length;
  this.clear();
  while (++index < length2) {
    var entry = entries2[index];
    this.set(entry[0], entry[1]);
  }
}
ListCache.prototype.clear = listCacheClear;
ListCache.prototype["delete"] = listCacheDelete;
ListCache.prototype.get = listCacheGet;
ListCache.prototype.has = listCacheHas;
ListCache.prototype.set = listCacheSet;
var Map$1 = getNative(root$1, "Map");
const Map$2 = Map$1;
function mapCacheClear() {
  this.size = 0;
  this.__data__ = {
    "hash": new Hash(),
    "map": new (Map$2 || ListCache)(),
    "string": new Hash()
  };
}
function isKeyable(value) {
  var type2 = typeof value;
  return type2 == "string" || type2 == "number" || type2 == "symbol" || type2 == "boolean" ? value !== "__proto__" : value === null;
}
function getMapData(map2, key) {
  var data = map2.__data__;
  return isKeyable(key) ? data[typeof key == "string" ? "string" : "hash"] : data.map;
}
function mapCacheDelete(key) {
  var result = getMapData(this, key)["delete"](key);
  this.size -= result ? 1 : 0;
  return result;
}
function mapCacheGet(key) {
  return getMapData(this, key).get(key);
}
function mapCacheHas(key) {
  return getMapData(this, key).has(key);
}
function mapCacheSet(key, value) {
  var data = getMapData(this, key), size = data.size;
  data.set(key, value);
  this.size += data.size == size ? 0 : 1;
  return this;
}
function MapCache(entries2) {
  var index = -1, length2 = entries2 == null ? 0 : entries2.length;
  this.clear();
  while (++index < length2) {
    var entry = entries2[index];
    this.set(entry[0], entry[1]);
  }
}
MapCache.prototype.clear = mapCacheClear;
MapCache.prototype["delete"] = mapCacheDelete;
MapCache.prototype.get = mapCacheGet;
MapCache.prototype.has = mapCacheHas;
MapCache.prototype.set = mapCacheSet;
var FUNC_ERROR_TEXT = "Expected a function";
function memoize(func, resolver) {
  if (typeof func != "function" || resolver != null && typeof resolver != "function") {
    throw new TypeError(FUNC_ERROR_TEXT);
  }
  var memoized = function() {
    var args = arguments, key = resolver ? resolver.apply(this, args) : args[0], cache = memoized.cache;
    if (cache.has(key)) {
      return cache.get(key);
    }
    var result = func.apply(this, args);
    memoized.cache = cache.set(key, result) || cache;
    return result;
  };
  memoized.cache = new (memoize.Cache || MapCache)();
  return memoized;
}
memoize.Cache = MapCache;
function stackClear() {
  this.__data__ = new ListCache();
  this.size = 0;
}
function stackDelete(key) {
  var data = this.__data__, result = data["delete"](key);
  this.size = data.size;
  return result;
}
function stackGet(key) {
  return this.__data__.get(key);
}
function stackHas(key) {
  return this.__data__.has(key);
}
var LARGE_ARRAY_SIZE = 200;
function stackSet(key, value) {
  var data = this.__data__;
  if (data instanceof ListCache) {
    var pairs2 = data.__data__;
    if (!Map$2 || pairs2.length < LARGE_ARRAY_SIZE - 1) {
      pairs2.push([key, value]);
      this.size = ++data.size;
      return this;
    }
    data = this.__data__ = new MapCache(pairs2);
  }
  data.set(key, value);
  this.size = data.size;
  return this;
}
function Stack(entries2) {
  var data = this.__data__ = new ListCache(entries2);
  this.size = data.size;
}
Stack.prototype.clear = stackClear;
Stack.prototype["delete"] = stackDelete;
Stack.prototype.get = stackGet;
Stack.prototype.has = stackHas;
Stack.prototype.set = stackSet;
var defineProperty = function() {
  try {
    var func = getNative(Object, "defineProperty");
    func({}, "", {});
    return func;
  } catch (e) {
  }
}();
const defineProperty$1 = defineProperty;
function baseAssignValue(object, key, value) {
  if (key == "__proto__" && defineProperty$1) {
    defineProperty$1(object, key, {
      "configurable": true,
      "enumerable": true,
      "value": value,
      "writable": true
    });
  } else {
    object[key] = value;
  }
}
function assignMergeValue(object, key, value) {
  if (value !== void 0 && !eq(object[key], value) || value === void 0 && !(key in object)) {
    baseAssignValue(object, key, value);
  }
}
function createBaseFor(fromRight) {
  return function(object, iteratee, keysFunc) {
    var index = -1, iterable = Object(object), props = keysFunc(object), length2 = props.length;
    while (length2--) {
      var key = props[fromRight ? length2 : ++index];
      if (iteratee(iterable[key], key, iterable) === false) {
        break;
      }
    }
    return object;
  };
}
var baseFor = createBaseFor();
const baseFor$1 = baseFor;
var freeExports$2 = typeof exports == "object" && exports && !exports.nodeType && exports;
var freeModule$2 = freeExports$2 && typeof module == "object" && module && !module.nodeType && module;
var moduleExports$2 = freeModule$2 && freeModule$2.exports === freeExports$2;
var Buffer$1 = moduleExports$2 ? root$1.Buffer : void 0, allocUnsafe = Buffer$1 ? Buffer$1.allocUnsafe : void 0;
function cloneBuffer(buffer, isDeep) {
  if (isDeep) {
    return buffer.slice();
  }
  var length2 = buffer.length, result = allocUnsafe ? allocUnsafe(length2) : new buffer.constructor(length2);
  buffer.copy(result);
  return result;
}
var Uint8Array$1 = root$1.Uint8Array;
const Uint8Array$2 = Uint8Array$1;
function cloneArrayBuffer(arrayBuffer) {
  var result = new arrayBuffer.constructor(arrayBuffer.byteLength);
  new Uint8Array$2(result).set(new Uint8Array$2(arrayBuffer));
  return result;
}
function cloneTypedArray(typedArray, isDeep) {
  var buffer = isDeep ? cloneArrayBuffer(typedArray.buffer) : typedArray.buffer;
  return new typedArray.constructor(buffer, typedArray.byteOffset, typedArray.length);
}
function copyArray(source, array2) {
  var index = -1, length2 = source.length;
  array2 || (array2 = Array(length2));
  while (++index < length2) {
    array2[index] = source[index];
  }
  return array2;
}
var objectCreate = Object.create;
var baseCreate = function() {
  function object() {
  }
  return function(proto) {
    if (!isObject$1(proto)) {
      return {};
    }
    if (objectCreate) {
      return objectCreate(proto);
    }
    object.prototype = proto;
    var result = new object();
    object.prototype = void 0;
    return result;
  };
}();
const baseCreate$1 = baseCreate;
function overArg(func, transform) {
  return function(arg) {
    return func(transform(arg));
  };
}
var getPrototype = overArg(Object.getPrototypeOf, Object);
const getPrototype$1 = getPrototype;
var objectProto$7 = Object.prototype;
function isPrototype(value) {
  var Ctor = value && value.constructor, proto = typeof Ctor == "function" && Ctor.prototype || objectProto$7;
  return value === proto;
}
function initCloneObject(object) {
  return typeof object.constructor == "function" && !isPrototype(object) ? baseCreate$1(getPrototype$1(object)) : {};
}
function isObjectLike(value) {
  return value != null && typeof value == "object";
}
var argsTag$1 = "[object Arguments]";
function baseIsArguments(value) {
  return isObjectLike(value) && baseGetTag(value) == argsTag$1;
}
var objectProto$6 = Object.prototype;
var hasOwnProperty$6 = objectProto$6.hasOwnProperty;
var propertyIsEnumerable = objectProto$6.propertyIsEnumerable;
var isArguments = baseIsArguments(function() {
  return arguments;
}()) ? baseIsArguments : function(value) {
  return isObjectLike(value) && hasOwnProperty$6.call(value, "callee") && !propertyIsEnumerable.call(value, "callee");
};
const isArguments$1 = isArguments;
var isArray = Array.isArray;
const isArray$1 = isArray;
var MAX_SAFE_INTEGER$1 = 9007199254740991;
function isLength(value) {
  return typeof value == "number" && value > -1 && value % 1 == 0 && value <= MAX_SAFE_INTEGER$1;
}
function isArrayLike(value) {
  return value != null && isLength(value.length) && !isFunction(value);
}
function isArrayLikeObject(value) {
  return isObjectLike(value) && isArrayLike(value);
}
function stubFalse() {
  return false;
}
var freeExports$1 = typeof exports == "object" && exports && !exports.nodeType && exports;
var freeModule$1 = freeExports$1 && typeof module == "object" && module && !module.nodeType && module;
var moduleExports$1 = freeModule$1 && freeModule$1.exports === freeExports$1;
var Buffer = moduleExports$1 ? root$1.Buffer : void 0;
var nativeIsBuffer = Buffer ? Buffer.isBuffer : void 0;
var isBuffer = nativeIsBuffer || stubFalse;
const isBuffer$1 = isBuffer;
var objectTag$2 = "[object Object]";
var funcProto = Function.prototype, objectProto$5 = Object.prototype;
var funcToString = funcProto.toString;
var hasOwnProperty$5 = objectProto$5.hasOwnProperty;
var objectCtorString = funcToString.call(Object);
function isPlainObject(value) {
  if (!isObjectLike(value) || baseGetTag(value) != objectTag$2) {
    return false;
  }
  var proto = getPrototype$1(value);
  if (proto === null) {
    return true;
  }
  var Ctor = hasOwnProperty$5.call(proto, "constructor") && proto.constructor;
  return typeof Ctor == "function" && Ctor instanceof Ctor && funcToString.call(Ctor) == objectCtorString;
}
var argsTag = "[object Arguments]", arrayTag = "[object Array]", boolTag = "[object Boolean]", dateTag = "[object Date]", errorTag = "[object Error]", funcTag = "[object Function]", mapTag$2 = "[object Map]", numberTag = "[object Number]", objectTag$1 = "[object Object]", regexpTag = "[object RegExp]", setTag$2 = "[object Set]", stringTag = "[object String]", weakMapTag$1 = "[object WeakMap]";
var arrayBufferTag = "[object ArrayBuffer]", dataViewTag$1 = "[object DataView]", float32Tag = "[object Float32Array]", float64Tag = "[object Float64Array]", int8Tag = "[object Int8Array]", int16Tag = "[object Int16Array]", int32Tag = "[object Int32Array]", uint8Tag = "[object Uint8Array]", uint8ClampedTag = "[object Uint8ClampedArray]", uint16Tag = "[object Uint16Array]", uint32Tag = "[object Uint32Array]";
var typedArrayTags = {};
typedArrayTags[float32Tag] = typedArrayTags[float64Tag] = typedArrayTags[int8Tag] = typedArrayTags[int16Tag] = typedArrayTags[int32Tag] = typedArrayTags[uint8Tag] = typedArrayTags[uint8ClampedTag] = typedArrayTags[uint16Tag] = typedArrayTags[uint32Tag] = true;
typedArrayTags[argsTag] = typedArrayTags[arrayTag] = typedArrayTags[arrayBufferTag] = typedArrayTags[boolTag] = typedArrayTags[dataViewTag$1] = typedArrayTags[dateTag] = typedArrayTags[errorTag] = typedArrayTags[funcTag] = typedArrayTags[mapTag$2] = typedArrayTags[numberTag] = typedArrayTags[objectTag$1] = typedArrayTags[regexpTag] = typedArrayTags[setTag$2] = typedArrayTags[stringTag] = typedArrayTags[weakMapTag$1] = false;
function baseIsTypedArray(value) {
  return isObjectLike(value) && isLength(value.length) && !!typedArrayTags[baseGetTag(value)];
}
function baseUnary(func) {
  return function(value) {
    return func(value);
  };
}
var freeExports = typeof exports == "object" && exports && !exports.nodeType && exports;
var freeModule = freeExports && typeof module == "object" && module && !module.nodeType && module;
var moduleExports = freeModule && freeModule.exports === freeExports;
var freeProcess = moduleExports && freeGlobal$1.process;
var nodeUtil = function() {
  try {
    var types = freeModule && freeModule.require && freeModule.require("util").types;
    if (types) {
      return types;
    }
    return freeProcess && freeProcess.binding && freeProcess.binding("util");
  } catch (e) {
  }
}();
const nodeUtil$1 = nodeUtil;
var nodeIsTypedArray = nodeUtil$1 && nodeUtil$1.isTypedArray;
var isTypedArray = nodeIsTypedArray ? baseUnary(nodeIsTypedArray) : baseIsTypedArray;
const isTypedArray$1 = isTypedArray;
function safeGet(object, key) {
  if (key === "constructor" && typeof object[key] === "function") {
    return;
  }
  if (key == "__proto__") {
    return;
  }
  return object[key];
}
var objectProto$4 = Object.prototype;
var hasOwnProperty$4 = objectProto$4.hasOwnProperty;
function assignValue(object, key, value) {
  var objValue = object[key];
  if (!(hasOwnProperty$4.call(object, key) && eq(objValue, value)) || value === void 0 && !(key in object)) {
    baseAssignValue(object, key, value);
  }
}
function copyObject(source, props, object, customizer) {
  var isNew = !object;
  object || (object = {});
  var index = -1, length2 = props.length;
  while (++index < length2) {
    var key = props[index];
    var newValue = customizer ? customizer(object[key], source[key], key, object, source) : void 0;
    if (newValue === void 0) {
      newValue = source[key];
    }
    if (isNew) {
      baseAssignValue(object, key, newValue);
    } else {
      assignValue(object, key, newValue);
    }
  }
  return object;
}
function baseTimes(n, iteratee) {
  var index = -1, result = Array(n);
  while (++index < n) {
    result[index] = iteratee(index);
  }
  return result;
}
var MAX_SAFE_INTEGER = 9007199254740991;
var reIsUint = /^(?:0|[1-9]\d*)$/;
function isIndex(value, length2) {
  var type2 = typeof value;
  length2 = length2 == null ? MAX_SAFE_INTEGER : length2;
  return !!length2 && (type2 == "number" || type2 != "symbol" && reIsUint.test(value)) && (value > -1 && value % 1 == 0 && value < length2);
}
var objectProto$3 = Object.prototype;
var hasOwnProperty$3 = objectProto$3.hasOwnProperty;
function arrayLikeKeys(value, inherited) {
  var isArr = isArray$1(value), isArg = !isArr && isArguments$1(value), isBuff = !isArr && !isArg && isBuffer$1(value), isType = !isArr && !isArg && !isBuff && isTypedArray$1(value), skipIndexes = isArr || isArg || isBuff || isType, result = skipIndexes ? baseTimes(value.length, String) : [], length2 = result.length;
  for (var key in value) {
    if ((inherited || hasOwnProperty$3.call(value, key)) && !(skipIndexes && // Safari 9 has enumerable `arguments.length` in strict mode.
    (key == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
    isBuff && (key == "offset" || key == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
    isType && (key == "buffer" || key == "byteLength" || key == "byteOffset") || // Skip index properties.
    isIndex(key, length2)))) {
      result.push(key);
    }
  }
  return result;
}
function nativeKeysIn(object) {
  var result = [];
  if (object != null) {
    for (var key in Object(object)) {
      result.push(key);
    }
  }
  return result;
}
var objectProto$2 = Object.prototype;
var hasOwnProperty$2 = objectProto$2.hasOwnProperty;
function baseKeysIn(object) {
  if (!isObject$1(object)) {
    return nativeKeysIn(object);
  }
  var isProto = isPrototype(object), result = [];
  for (var key in object) {
    if (!(key == "constructor" && (isProto || !hasOwnProperty$2.call(object, key)))) {
      result.push(key);
    }
  }
  return result;
}
function keysIn(object) {
  return isArrayLike(object) ? arrayLikeKeys(object, true) : baseKeysIn(object);
}
function toPlainObject(value) {
  return copyObject(value, keysIn(value));
}
function baseMergeDeep(object, source, key, srcIndex, mergeFunc, customizer, stack) {
  var objValue = safeGet(object, key), srcValue = safeGet(source, key), stacked = stack.get(srcValue);
  if (stacked) {
    assignMergeValue(object, key, stacked);
    return;
  }
  var newValue = customizer ? customizer(objValue, srcValue, key + "", object, source, stack) : void 0;
  var isCommon = newValue === void 0;
  if (isCommon) {
    var isArr = isArray$1(srcValue), isBuff = !isArr && isBuffer$1(srcValue), isTyped = !isArr && !isBuff && isTypedArray$1(srcValue);
    newValue = srcValue;
    if (isArr || isBuff || isTyped) {
      if (isArray$1(objValue)) {
        newValue = objValue;
      } else if (isArrayLikeObject(objValue)) {
        newValue = copyArray(objValue);
      } else if (isBuff) {
        isCommon = false;
        newValue = cloneBuffer(srcValue, true);
      } else if (isTyped) {
        isCommon = false;
        newValue = cloneTypedArray(srcValue, true);
      } else {
        newValue = [];
      }
    } else if (isPlainObject(srcValue) || isArguments$1(srcValue)) {
      newValue = objValue;
      if (isArguments$1(objValue)) {
        newValue = toPlainObject(objValue);
      } else if (!isObject$1(objValue) || isFunction(objValue)) {
        newValue = initCloneObject(srcValue);
      }
    } else {
      isCommon = false;
    }
  }
  if (isCommon) {
    stack.set(srcValue, newValue);
    mergeFunc(newValue, srcValue, srcIndex, customizer, stack);
    stack["delete"](srcValue);
  }
  assignMergeValue(object, key, newValue);
}
function baseMerge(object, source, srcIndex, customizer, stack) {
  if (object === source) {
    return;
  }
  baseFor$1(source, function(srcValue, key) {
    stack || (stack = new Stack());
    if (isObject$1(srcValue)) {
      baseMergeDeep(object, source, key, srcIndex, baseMerge, customizer, stack);
    } else {
      var newValue = customizer ? customizer(safeGet(object, key), srcValue, key + "", object, source, stack) : void 0;
      if (newValue === void 0) {
        newValue = srcValue;
      }
      assignMergeValue(object, key, newValue);
    }
  }, keysIn);
}
function identity(value) {
  return value;
}
function apply(func, thisArg, args) {
  switch (args.length) {
    case 0:
      return func.call(thisArg);
    case 1:
      return func.call(thisArg, args[0]);
    case 2:
      return func.call(thisArg, args[0], args[1]);
    case 3:
      return func.call(thisArg, args[0], args[1], args[2]);
  }
  return func.apply(thisArg, args);
}
var nativeMax = Math.max;
function overRest(func, start2, transform) {
  start2 = nativeMax(start2 === void 0 ? func.length - 1 : start2, 0);
  return function() {
    var args = arguments, index = -1, length2 = nativeMax(args.length - start2, 0), array2 = Array(length2);
    while (++index < length2) {
      array2[index] = args[start2 + index];
    }
    index = -1;
    var otherArgs = Array(start2 + 1);
    while (++index < start2) {
      otherArgs[index] = args[index];
    }
    otherArgs[start2] = transform(array2);
    return apply(func, this, otherArgs);
  };
}
function constant(value) {
  return function() {
    return value;
  };
}
var baseSetToString = !defineProperty$1 ? identity : function(func, string) {
  return defineProperty$1(func, "toString", {
    "configurable": true,
    "enumerable": false,
    "value": constant(string),
    "writable": true
  });
};
const baseSetToString$1 = baseSetToString;
var HOT_COUNT = 800, HOT_SPAN = 16;
var nativeNow = Date.now;
function shortOut(func) {
  var count = 0, lastCalled = 0;
  return function() {
    var stamp = nativeNow(), remaining = HOT_SPAN - (stamp - lastCalled);
    lastCalled = stamp;
    if (remaining > 0) {
      if (++count >= HOT_COUNT) {
        return arguments[0];
      }
    } else {
      count = 0;
    }
    return func.apply(void 0, arguments);
  };
}
var setToString = shortOut(baseSetToString$1);
const setToString$1 = setToString;
function baseRest(func, start2) {
  return setToString$1(overRest(func, start2, identity), func + "");
}
function isIterateeCall(value, index, object) {
  if (!isObject$1(object)) {
    return false;
  }
  var type2 = typeof index;
  if (type2 == "number" ? isArrayLike(object) && isIndex(index, object.length) : type2 == "string" && index in object) {
    return eq(object[index], value);
  }
  return false;
}
function createAssigner(assigner) {
  return baseRest(function(object, sources) {
    var index = -1, length2 = sources.length, customizer = length2 > 1 ? sources[length2 - 1] : void 0, guard = length2 > 2 ? sources[2] : void 0;
    customizer = assigner.length > 3 && typeof customizer == "function" ? (length2--, customizer) : void 0;
    if (guard && isIterateeCall(sources[0], sources[1], guard)) {
      customizer = length2 < 3 ? void 0 : customizer;
      length2 = 1;
    }
    object = Object(object);
    while (++index < length2) {
      var source = sources[index];
      if (source) {
        assigner(object, source, index, customizer);
      }
    }
    return object;
  });
}
var merge$1 = createAssigner(function(object, source, srcIndex) {
  baseMerge(object, source, srcIndex);
});
const merge$2 = merge$1;
const ZERO_WIDTH_SPACE = "​";
const d3CurveTypes = {
  curveBasis,
  curveBasisClosed,
  curveBasisOpen,
  curveBumpX: bumpX,
  curveBumpY: bumpY,
  curveBundle,
  curveCardinalClosed,
  curveCardinalOpen,
  curveCardinal,
  curveCatmullRomClosed,
  curveCatmullRomOpen,
  curveCatmullRom,
  curveLinear,
  curveLinearClosed,
  curveMonotoneX: monotoneX,
  curveMonotoneY: monotoneY,
  curveNatural,
  curveStep,
  curveStepAfter: stepAfter,
  curveStepBefore: stepBefore
};
const directiveWithoutOpen = /\s*(?:(\w+)(?=:):|(\w+))\s*(?:(\w+)|((?:(?!}%{2}).|\r?\n)*))?\s*(?:}%{2})?/gi;
const detectInit = function(text2, config2) {
  const inits = detectDirective(text2, /(?:init\b)|(?:initialize\b)/);
  let results = {};
  if (Array.isArray(inits)) {
    const args = inits.map((init2) => init2.args);
    sanitizeDirective(args);
    results = assignWithDepth$1(results, [...args]);
  } else {
    results = inits.args;
  }
  if (!results) {
    return;
  }
  let type2 = detectType(text2, config2);
  const prop = "config";
  if (results[prop] !== void 0) {
    if (type2 === "flowchart-v2") {
      type2 = "flowchart";
    }
    results[type2] = results[prop];
    delete results[prop];
  }
  return results;
};
const detectDirective = function(text2, type2 = null) {
  try {
    const commentWithoutDirectives = new RegExp(
      `[%]{2}(?![{]${directiveWithoutOpen.source})(?=[}][%]{2}).*
`,
      "ig"
    );
    text2 = text2.trim().replace(commentWithoutDirectives, "").replace(/'/gm, '"');
    log$1.debug(
      `Detecting diagram directive${type2 !== null ? " type:" + type2 : ""} based on the text:${text2}`
    );
    let match;
    const result = [];
    while ((match = directiveRegex.exec(text2)) !== null) {
      if (match.index === directiveRegex.lastIndex) {
        directiveRegex.lastIndex++;
      }
      if (match && !type2 || type2 && match[1] && match[1].match(type2) || type2 && match[2] && match[2].match(type2)) {
        const type22 = match[1] ? match[1] : match[2];
        const args = match[3] ? match[3].trim() : match[4] ? JSON.parse(match[4].trim()) : null;
        result.push({ type: type22, args });
      }
    }
    if (result.length === 0) {
      return { type: text2, args: null };
    }
    return result.length === 1 ? result[0] : result;
  } catch (error) {
    log$1.error(
      `ERROR: ${error.message} - Unable to parse directive type: '${type2}' based on the text: '${text2}'`
    );
    return { type: void 0, args: null };
  }
};
const removeDirectives = function(text2) {
  return text2.replace(directiveRegex, "");
};
const isSubstringInArray = function(str2, arr) {
  for (const [i, element] of arr.entries()) {
    if (element.match(str2)) {
      return i;
    }
  }
  return -1;
};
function interpolateToCurve(interpolate2, defaultCurve) {
  if (!interpolate2) {
    return defaultCurve;
  }
  const curveName = `curve${interpolate2.charAt(0).toUpperCase() + interpolate2.slice(1)}`;
  return d3CurveTypes[curveName] ?? defaultCurve;
}
function formatUrl(linkStr, config2) {
  const url = linkStr.trim();
  if (!url) {
    return void 0;
  }
  if (config2.securityLevel !== "loose") {
    return sanitizeUrl_1(url);
  }
  return url;
}
const runFunc = (functionName, ...params) => {
  const arrPaths = functionName.split(".");
  const len = arrPaths.length - 1;
  const fnName = arrPaths[len];
  let obj = window;
  for (let i = 0; i < len; i++) {
    obj = obj[arrPaths[i]];
    if (!obj) {
      log$1.error(`Function name: ${functionName} not found in window`);
      return;
    }
  }
  obj[fnName](...params);
};
function distance(p1, p2) {
  if (!p1 || !p2) {
    return 0;
  }
  return Math.sqrt(Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2));
}
function traverseEdge(points) {
  let prevPoint;
  let totalDistance = 0;
  points.forEach((point2) => {
    totalDistance += distance(point2, prevPoint);
    prevPoint = point2;
  });
  const remainingDistance = totalDistance / 2;
  return calculatePoint(points, remainingDistance);
}
function calcLabelPosition(points) {
  if (points.length === 1) {
    return points[0];
  }
  return traverseEdge(points);
}
const roundNumber = (num, precision = 2) => {
  const factor = Math.pow(10, precision);
  return Math.round(num * factor) / factor;
};
const calculatePoint = (points, distanceToTraverse) => {
  let prevPoint = void 0;
  let remainingDistance = distanceToTraverse;
  for (const point2 of points) {
    if (prevPoint) {
      const vectorDistance = distance(point2, prevPoint);
      if (vectorDistance < remainingDistance) {
        remainingDistance -= vectorDistance;
      } else {
        const distanceRatio = remainingDistance / vectorDistance;
        if (distanceRatio <= 0) {
          return prevPoint;
        }
        if (distanceRatio >= 1) {
          return { x: point2.x, y: point2.y };
        }
        if (distanceRatio > 0 && distanceRatio < 1) {
          return {
            x: roundNumber((1 - distanceRatio) * prevPoint.x + distanceRatio * point2.x, 5),
            y: roundNumber((1 - distanceRatio) * prevPoint.y + distanceRatio * point2.y, 5)
          };
        }
      }
    }
    prevPoint = point2;
  }
  throw new Error("Could not find a suitable point for the given distance");
};
const calcCardinalityPosition = (isRelationTypePresent, points, initialPosition) => {
  log$1.info(`our points ${JSON.stringify(points)}`);
  if (points[0] !== initialPosition) {
    points = points.reverse();
  }
  const distanceToCardinalityPoint = 25;
  const center = calculatePoint(points, distanceToCardinalityPoint);
  const d = isRelationTypePresent ? 10 : 5;
  const angle = Math.atan2(points[0].y - center.y, points[0].x - center.x);
  const cardinalityPosition = { x: 0, y: 0 };
  cardinalityPosition.x = Math.sin(angle) * d + (points[0].x + center.x) / 2;
  cardinalityPosition.y = -Math.cos(angle) * d + (points[0].y + center.y) / 2;
  return cardinalityPosition;
};
function calcTerminalLabelPosition(terminalMarkerSize, position2, _points) {
  const points = structuredClone(_points);
  log$1.info("our points", points);
  if (position2 !== "start_left" && position2 !== "start_right") {
    points.reverse();
  }
  const distanceToCardinalityPoint = 25 + terminalMarkerSize;
  const center = calculatePoint(points, distanceToCardinalityPoint);
  const d = 10 + terminalMarkerSize * 0.5;
  const angle = Math.atan2(points[0].y - center.y, points[0].x - center.x);
  const cardinalityPosition = { x: 0, y: 0 };
  if (position2 === "start_left") {
    cardinalityPosition.x = Math.sin(angle + Math.PI) * d + (points[0].x + center.x) / 2;
    cardinalityPosition.y = -Math.cos(angle + Math.PI) * d + (points[0].y + center.y) / 2;
  } else if (position2 === "end_right") {
    cardinalityPosition.x = Math.sin(angle - Math.PI) * d + (points[0].x + center.x) / 2 - 5;
    cardinalityPosition.y = -Math.cos(angle - Math.PI) * d + (points[0].y + center.y) / 2 - 5;
  } else if (position2 === "end_left") {
    cardinalityPosition.x = Math.sin(angle) * d + (points[0].x + center.x) / 2 - 5;
    cardinalityPosition.y = -Math.cos(angle) * d + (points[0].y + center.y) / 2 - 5;
  } else {
    cardinalityPosition.x = Math.sin(angle) * d + (points[0].x + center.x) / 2;
    cardinalityPosition.y = -Math.cos(angle) * d + (points[0].y + center.y) / 2;
  }
  return cardinalityPosition;
}
function getStylesFromArray(arr) {
  let style = "";
  let labelStyle = "";
  for (const element of arr) {
    if (element !== void 0) {
      if (element.startsWith("color:") || element.startsWith("text-align:")) {
        labelStyle = labelStyle + element + ";";
      } else {
        style = style + element + ";";
      }
    }
  }
  return { style, labelStyle };
}
let cnt = 0;
const generateId = () => {
  cnt++;
  return "id-" + Math.random().toString(36).substr(2, 12) + "-" + cnt;
};
function makeRandomHex(length2) {
  let result = "";
  const characters2 = "0123456789abcdef";
  const charactersLength = characters2.length;
  for (let i = 0; i < length2; i++) {
    result += characters2.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}
const random = (options) => {
  return makeRandomHex(options.length);
};
const getTextObj = function() {
  return {
    x: 0,
    y: 0,
    fill: void 0,
    anchor: "start",
    style: "#666",
    width: 100,
    height: 100,
    textMargin: 0,
    rx: 0,
    ry: 0,
    valign: void 0,
    text: ""
  };
};
const drawSimpleText = function(elem, textData) {
  const nText = textData.text.replace(common$1.lineBreakRegex, " ");
  const [, _fontSizePx] = parseFontSize(textData.fontSize);
  const textElem = elem.append("text");
  textElem.attr("x", textData.x);
  textElem.attr("y", textData.y);
  textElem.style("text-anchor", textData.anchor);
  textElem.style("font-family", textData.fontFamily);
  textElem.style("font-size", _fontSizePx);
  textElem.style("font-weight", textData.fontWeight);
  textElem.attr("fill", textData.fill);
  if (textData.class !== void 0) {
    textElem.attr("class", textData.class);
  }
  const span = textElem.append("tspan");
  span.attr("x", textData.x + textData.textMargin * 2);
  span.attr("fill", textData.fill);
  span.text(nText);
  return textElem;
};
const wrapLabel = memoize(
  (label, maxWidth, config2) => {
    if (!label) {
      return label;
    }
    config2 = Object.assign(
      { fontSize: 12, fontWeight: 400, fontFamily: "Arial", joinWith: "<br/>" },
      config2
    );
    if (common$1.lineBreakRegex.test(label)) {
      return label;
    }
    const words = label.split(" ");
    const completedLines = [];
    let nextLine = "";
    words.forEach((word, index) => {
      const wordLength = calculateTextWidth(`${word} `, config2);
      const nextLineLength = calculateTextWidth(nextLine, config2);
      if (wordLength > maxWidth) {
        const { hyphenatedStrings, remainingWord } = breakString(word, maxWidth, "-", config2);
        completedLines.push(nextLine, ...hyphenatedStrings);
        nextLine = remainingWord;
      } else if (nextLineLength + wordLength >= maxWidth) {
        completedLines.push(nextLine);
        nextLine = word;
      } else {
        nextLine = [nextLine, word].filter(Boolean).join(" ");
      }
      const currentWord = index + 1;
      const isLastWord = currentWord === words.length;
      if (isLastWord) {
        completedLines.push(nextLine);
      }
    });
    return completedLines.filter((line2) => line2 !== "").join(config2.joinWith);
  },
  (label, maxWidth, config2) => `${label}${maxWidth}${config2.fontSize}${config2.fontWeight}${config2.fontFamily}${config2.joinWith}`
);
const breakString = memoize(
  (word, maxWidth, hyphenCharacter = "-", config2) => {
    config2 = Object.assign(
      { fontSize: 12, fontWeight: 400, fontFamily: "Arial", margin: 0 },
      config2
    );
    const characters2 = [...word];
    const lines = [];
    let currentLine = "";
    characters2.forEach((character2, index) => {
      const nextLine = `${currentLine}${character2}`;
      const lineWidth = calculateTextWidth(nextLine, config2);
      if (lineWidth >= maxWidth) {
        const currentCharacter = index + 1;
        const isLastLine = characters2.length === currentCharacter;
        const hyphenatedNextLine = `${nextLine}${hyphenCharacter}`;
        lines.push(isLastLine ? nextLine : hyphenatedNextLine);
        currentLine = "";
      } else {
        currentLine = nextLine;
      }
    });
    return { hyphenatedStrings: lines, remainingWord: currentLine };
  },
  (word, maxWidth, hyphenCharacter = "-", config2) => `${word}${maxWidth}${hyphenCharacter}${config2.fontSize}${config2.fontWeight}${config2.fontFamily}`
);
function calculateTextHeight(text2, config2) {
  return calculateTextDimensions(text2, config2).height;
}
function calculateTextWidth(text2, config2) {
  return calculateTextDimensions(text2, config2).width;
}
const calculateTextDimensions = memoize(
  (text2, config2) => {
    const { fontSize = 12, fontFamily = "Arial", fontWeight = 400 } = config2;
    if (!text2) {
      return { width: 0, height: 0 };
    }
    const [, _fontSizePx] = parseFontSize(fontSize);
    const fontFamilies = ["sans-serif", fontFamily];
    const lines = text2.split(common$1.lineBreakRegex);
    const dims = [];
    const body = d3select("body");
    if (!body.remove) {
      return { width: 0, height: 0, lineHeight: 0 };
    }
    const g = body.append("svg");
    for (const fontFamily2 of fontFamilies) {
      let cHeight = 0;
      const dim = { width: 0, height: 0, lineHeight: 0 };
      for (const line2 of lines) {
        const textObj = getTextObj();
        textObj.text = line2 || ZERO_WIDTH_SPACE;
        const textElem = drawSimpleText(g, textObj).style("font-size", _fontSizePx).style("font-weight", fontWeight).style("font-family", fontFamily2);
        const bBox = (textElem._groups || textElem)[0][0].getBBox();
        if (bBox.width === 0 && bBox.height === 0) {
          throw new Error("svg element not in render tree");
        }
        dim.width = Math.round(Math.max(dim.width, bBox.width));
        cHeight = Math.round(bBox.height);
        dim.height += cHeight;
        dim.lineHeight = Math.round(Math.max(dim.lineHeight, cHeight));
      }
      dims.push(dim);
    }
    g.remove();
    const index = isNaN(dims[1].height) || isNaN(dims[1].width) || isNaN(dims[1].lineHeight) || dims[0].height > dims[1].height && dims[0].width > dims[1].width && dims[0].lineHeight > dims[1].lineHeight ? 0 : 1;
    return dims[index];
  },
  (text2, config2) => `${text2}${config2.fontSize}${config2.fontWeight}${config2.fontFamily}`
);
class InitIDGenerator {
  constructor(deterministic = false, seed) {
    this.count = 0;
    this.count = seed ? seed.length : 0;
    this.next = deterministic ? () => this.count++ : () => Date.now();
  }
}
let decoder;
const entityDecode = function(html2) {
  decoder = decoder || document.createElement("div");
  html2 = escape(html2).replace(/%26/g, "&").replace(/%23/g, "#").replace(/%3B/g, ";");
  decoder.innerHTML = html2;
  return unescape(decoder.textContent);
};
function isDetailedError(error) {
  return "str" in error;
}
const insertTitle = (parent, cssClass, titleTopMargin, title) => {
  var _a;
  if (!title) {
    return;
  }
  const bounds = (_a = parent.node()) == null ? void 0 : _a.getBBox();
  if (!bounds) {
    return;
  }
  parent.append("text").text(title).attr("x", bounds.x + bounds.width / 2).attr("y", -titleTopMargin).attr("class", cssClass);
};
const parseFontSize = (fontSize) => {
  if (typeof fontSize === "number") {
    return [fontSize, fontSize + "px"];
  }
  const fontSizeNumber = parseInt(fontSize ?? "", 10);
  if (Number.isNaN(fontSizeNumber)) {
    return [void 0, void 0];
  } else if (fontSize === String(fontSizeNumber)) {
    return [fontSizeNumber, fontSize + "px"];
  } else {
    return [fontSizeNumber, fontSize];
  }
};
function cleanAndMerge(defaultData, data) {
  return merge$2({}, defaultData, data);
}
const utils = {
  assignWithDepth: assignWithDepth$1,
  wrapLabel,
  calculateTextHeight,
  calculateTextWidth,
  calculateTextDimensions,
  cleanAndMerge,
  detectInit,
  detectDirective,
  isSubstringInArray,
  interpolateToCurve,
  calcLabelPosition,
  calcCardinalityPosition,
  calcTerminalLabelPosition,
  formatUrl,
  getStylesFromArray,
  generateId,
  random,
  runFunc,
  entityDecode,
  insertTitle,
  parseFontSize,
  InitIDGenerator
};
var COMMENT = "comm";
var RULESET = "rule";
var DECLARATION = "decl";
var IMPORT = "@import";
var KEYFRAMES = "@keyframes";
var abs = Math.abs;
var from = String.fromCharCode;
function trim(value) {
  return value.trim();
}
function replace(value, pattern, replacement) {
  return value.replace(pattern, replacement);
}
function indexof(value, search) {
  return value.indexOf(search);
}
function charat(value, index) {
  return value.charCodeAt(index) | 0;
}
function substr(value, begin, end) {
  return value.slice(begin, end);
}
function strlen(value) {
  return value.length;
}
function sizeof(value) {
  return value.length;
}
function append(value, array2) {
  return array2.push(value), value;
}
var line = 1;
var column = 1;
var length = 0;
var position = 0;
var character = 0;
var characters = "";
function node(value, root2, parent, type2, props, children2, length2) {
  return { value, root: root2, parent, type: type2, props, children: children2, line, column, length: length2, return: "" };
}
function char() {
  return character;
}
function prev() {
  character = position > 0 ? charat(characters, --position) : 0;
  if (column--, character === 10)
    column = 1, line--;
  return character;
}
function next() {
  character = position < length ? charat(characters, position++) : 0;
  if (column++, character === 10)
    column = 1, line++;
  return character;
}
function peek() {
  return charat(characters, position);
}
function caret() {
  return position;
}
function slice(begin, end) {
  return substr(characters, begin, end);
}
function token(type2) {
  switch (type2) {
    case 0:
    case 9:
    case 10:
    case 13:
    case 32:
      return 5;
    case 33:
    case 43:
    case 44:
    case 47:
    case 62:
    case 64:
    case 126:
    case 59:
    case 123:
    case 125:
      return 4;
    case 58:
      return 3;
    case 34:
    case 39:
    case 40:
    case 91:
      return 2;
    case 41:
    case 93:
      return 1;
  }
  return 0;
}
function alloc(value) {
  return line = column = 1, length = strlen(characters = value), position = 0, [];
}
function dealloc(value) {
  return characters = "", value;
}
function delimit(type2) {
  return trim(slice(position - 1, delimiter(type2 === 91 ? type2 + 2 : type2 === 40 ? type2 + 1 : type2)));
}
function whitespace(type2) {
  while (character = peek())
    if (character < 33)
      next();
    else
      break;
  return token(type2) > 2 || token(character) > 3 ? "" : " ";
}
function escaping(index, count) {
  while (--count && next())
    if (character < 48 || character > 102 || character > 57 && character < 65 || character > 70 && character < 97)
      break;
  return slice(index, caret() + (count < 6 && peek() == 32 && next() == 32));
}
function delimiter(type2) {
  while (next())
    switch (character) {
      case type2:
        return position;
      case 34:
      case 39:
        if (type2 !== 34 && type2 !== 39)
          delimiter(character);
        break;
      case 40:
        if (type2 === 41)
          delimiter(type2);
        break;
      case 92:
        next();
        break;
    }
  return position;
}
function commenter(type2, index) {
  while (next())
    if (type2 + character === 47 + 10)
      break;
    else if (type2 + character === 42 + 42 && peek() === 47)
      break;
  return "/*" + slice(index, position - 1) + "*" + from(type2 === 47 ? type2 : next());
}
function identifier(index) {
  while (!token(peek()))
    next();
  return slice(index, position);
}
function compile(value) {
  return dealloc(parse$2("", null, null, null, [""], value = alloc(value), 0, [0], value));
}
function parse$2(value, root2, parent, rule, rules, rulesets, pseudo, points, declarations) {
  var index = 0;
  var offset = 0;
  var length2 = pseudo;
  var atrule = 0;
  var property = 0;
  var previous = 0;
  var variable = 1;
  var scanning = 1;
  var ampersand = 1;
  var character2 = 0;
  var type2 = "";
  var props = rules;
  var children2 = rulesets;
  var reference = rule;
  var characters2 = type2;
  while (scanning)
    switch (previous = character2, character2 = next()) {
      case 40:
        if (previous != 108 && charat(characters2, length2 - 1) == 58) {
          if (indexof(characters2 += replace(delimit(character2), "&", "&\f"), "&\f") != -1)
            ampersand = -1;
          break;
        }
      case 34:
      case 39:
      case 91:
        characters2 += delimit(character2);
        break;
      case 9:
      case 10:
      case 13:
      case 32:
        characters2 += whitespace(previous);
        break;
      case 92:
        characters2 += escaping(caret() - 1, 7);
        continue;
      case 47:
        switch (peek()) {
          case 42:
          case 47:
            append(comment(commenter(next(), caret()), root2, parent), declarations);
            break;
          default:
            characters2 += "/";
        }
        break;
      case 123 * variable:
        points[index++] = strlen(characters2) * ampersand;
      case 125 * variable:
      case 59:
      case 0:
        switch (character2) {
          case 0:
          case 125:
            scanning = 0;
          case 59 + offset:
            if (property > 0 && strlen(characters2) - length2)
              append(property > 32 ? declaration(characters2 + ";", rule, parent, length2 - 1) : declaration(replace(characters2, " ", "") + ";", rule, parent, length2 - 2), declarations);
            break;
          case 59:
            characters2 += ";";
          default:
            append(reference = ruleset(characters2, root2, parent, index, offset, rules, points, type2, props = [], children2 = [], length2), rulesets);
            if (character2 === 123)
              if (offset === 0)
                parse$2(characters2, root2, reference, reference, props, rulesets, length2, points, children2);
              else
                switch (atrule === 99 && charat(characters2, 3) === 110 ? 100 : atrule) {
                  case 100:
                  case 109:
                  case 115:
                    parse$2(value, reference, reference, rule && append(ruleset(value, reference, reference, 0, 0, rules, points, type2, rules, props = [], length2), children2), rules, children2, length2, points, rule ? props : children2);
                    break;
                  default:
                    parse$2(characters2, reference, reference, reference, [""], children2, 0, points, children2);
                }
        }
        index = offset = property = 0, variable = ampersand = 1, type2 = characters2 = "", length2 = pseudo;
        break;
      case 58:
        length2 = 1 + strlen(characters2), property = previous;
      default:
        if (variable < 1) {
          if (character2 == 123)
            --variable;
          else if (character2 == 125 && variable++ == 0 && prev() == 125)
            continue;
        }
        switch (characters2 += from(character2), character2 * variable) {
          case 38:
            ampersand = offset > 0 ? 1 : (characters2 += "\f", -1);
            break;
          case 44:
            points[index++] = (strlen(characters2) - 1) * ampersand, ampersand = 1;
            break;
          case 64:
            if (peek() === 45)
              characters2 += delimit(next());
            atrule = peek(), offset = length2 = strlen(type2 = characters2 += identifier(caret())), character2++;
            break;
          case 45:
            if (previous === 45 && strlen(characters2) == 2)
              variable = 0;
        }
    }
  return rulesets;
}
function ruleset(value, root2, parent, index, offset, rules, points, type2, props, children2, length2) {
  var post = offset - 1;
  var rule = offset === 0 ? rules : [""];
  var size = sizeof(rule);
  for (var i = 0, j = 0, k = 0; i < index; ++i)
    for (var x = 0, y = substr(value, post + 1, post = abs(j = points[i])), z = value; x < size; ++x)
      if (z = trim(j > 0 ? rule[x] + " " + y : replace(y, /&\f/g, rule[x])))
        props[k++] = z;
  return node(value, root2, parent, offset === 0 ? RULESET : type2, props, children2, length2);
}
function comment(value, root2, parent) {
  return node(value, root2, parent, COMMENT, from(char()), substr(value, 2, -2), 0);
}
function declaration(value, root2, parent, length2) {
  return node(value, root2, parent, DECLARATION, substr(value, 0, length2), substr(value, length2 + 1, -1), length2);
}
function serialize(children2, callback) {
  var output = "";
  var length2 = sizeof(children2);
  for (var i = 0; i < length2; i++)
    output += callback(children2[i], i, children2, callback) || "";
  return output;
}
function stringify(element, index, children2, callback) {
  switch (element.type) {
    case IMPORT:
    case DECLARATION:
      return element.return = element.return || element.value;
    case COMMENT:
      return "";
    case KEYFRAMES:
      return element.return = element.value + "{" + serialize(element.children, callback) + "}";
    case RULESET:
      element.value = element.props.join(",");
  }
  return strlen(children2 = serialize(element.children, callback)) ? element.return = element.value + "{" + children2 + "}" : "";
}
const version = "10.5.1";
const defaultConfig = Object.freeze(defaultConfig$1);
let siteConfig = assignWithDepth$1({}, defaultConfig);
let configFromInitialize;
let directives = [];
let currentConfig = assignWithDepth$1({}, defaultConfig);
const updateCurrentConfig = (siteCfg, _directives) => {
  let cfg = assignWithDepth$1({}, siteCfg);
  let sumOfDirectives = {};
  for (const d of _directives) {
    sanitize(d);
    sumOfDirectives = assignWithDepth$1(sumOfDirectives, d);
  }
  cfg = assignWithDepth$1(cfg, sumOfDirectives);
  if (sumOfDirectives.theme && sumOfDirectives.theme in theme) {
    const tmpConfigFromInitialize = assignWithDepth$1({}, configFromInitialize);
    const themeVariables = assignWithDepth$1(
      tmpConfigFromInitialize.themeVariables || {},
      sumOfDirectives.themeVariables
    );
    if (cfg.theme && cfg.theme in theme) {
      cfg.themeVariables = theme[cfg.theme].getThemeVariables(themeVariables);
    }
  }
  currentConfig = cfg;
  checkConfig(currentConfig);
  return currentConfig;
};
const setSiteConfig = (conf) => {
  siteConfig = assignWithDepth$1({}, defaultConfig);
  siteConfig = assignWithDepth$1(siteConfig, conf);
  if (conf.theme && theme[conf.theme]) {
    siteConfig.themeVariables = theme[conf.theme].getThemeVariables(conf.themeVariables);
  }
  updateCurrentConfig(siteConfig, directives);
  return siteConfig;
};
const saveConfigFromInitialize = (conf) => {
  configFromInitialize = assignWithDepth$1({}, conf);
};
const updateSiteConfig = (conf) => {
  siteConfig = assignWithDepth$1(siteConfig, conf);
  updateCurrentConfig(siteConfig, directives);
  return siteConfig;
};
const getSiteConfig = () => {
  return assignWithDepth$1({}, siteConfig);
};
const setConfig = (conf) => {
  checkConfig(conf);
  assignWithDepth$1(currentConfig, conf);
  return getConfig$1();
};
const getConfig$1 = () => {
  return assignWithDepth$1({}, currentConfig);
};
const sanitize = (options) => {
  if (!options) {
    return;
  }
  ["secure", ...siteConfig.secure ?? []].forEach((key) => {
    if (Object.hasOwn(options, key)) {
      log$1.debug(`Denied attempt to modify a secure key ${key}`, options[key]);
      delete options[key];
    }
  });
  Object.keys(options).forEach((key) => {
    if (key.startsWith("__")) {
      delete options[key];
    }
  });
  Object.keys(options).forEach((key) => {
    if (typeof options[key] === "string" && (options[key].includes("<") || options[key].includes(">") || options[key].includes("url(data:"))) {
      delete options[key];
    }
    if (typeof options[key] === "object") {
      sanitize(options[key]);
    }
  });
};
const addDirective = (directive) => {
  sanitizeDirective(directive);
  if (directive.fontFamily && (!directive.themeVariables || !directive.themeVariables.fontFamily)) {
    directive.themeVariables = { fontFamily: directive.fontFamily };
  }
  directives.push(directive);
  updateCurrentConfig(siteConfig, directives);
};
const reset = (config2 = siteConfig) => {
  directives = [];
  updateCurrentConfig(config2, directives);
};
const ConfigWarning = {
  LAZY_LOAD_DEPRECATED: "The configuration options lazyLoadedDiagrams and loadExternalDiagramsAtStartup are deprecated. Please use registerExternalDiagrams instead."
};
const issuedWarnings = {};
const issueWarning = (warning) => {
  if (issuedWarnings[warning]) {
    return;
  }
  log$1.warn(ConfigWarning[warning]);
  issuedWarnings[warning] = true;
};
const checkConfig = (config2) => {
  if (!config2) {
    return;
  }
  if (config2.lazyLoadedDiagrams || config2.loadExternalDiagramsAtStartup) {
    issueWarning("LAZY_LOAD_DEPRECATED");
  }
};
const id$j = "c4";
const detector$j = (txt) => {
  return /^\s*C4Context|C4Container|C4Component|C4Dynamic|C4Deployment/.test(txt);
};
const loader$k = async () => {
  const { diagram: diagram2 } = await import("./c4Diagram-4bfe15a7.js");
  return { id: id$j, diagram: diagram2 };
};
const plugin$h = {
  id: id$j,
  detector: detector$j,
  loader: loader$k
};
const c4 = plugin$h;
const id$i = "flowchart";
const detector$i = (txt, config2) => {
  var _a, _b;
  if (((_a = config2 == null ? void 0 : config2.flowchart) == null ? void 0 : _a.defaultRenderer) === "dagre-wrapper" || ((_b = config2 == null ? void 0 : config2.flowchart) == null ? void 0 : _b.defaultRenderer) === "elk") {
    return false;
  }
  return /^\s*graph/.test(txt);
};
const loader$j = async () => {
  const { diagram: diagram2 } = await import("./flowDiagram-fc477a2f.js");
  return { id: id$i, diagram: diagram2 };
};
const plugin$g = {
  id: id$i,
  detector: detector$i,
  loader: loader$j
};
const flowchart = plugin$g;
const id$h = "flowchart-v2";
const detector$h = (txt, config2) => {
  var _a, _b, _c;
  if (((_a = config2 == null ? void 0 : config2.flowchart) == null ? void 0 : _a.defaultRenderer) === "dagre-d3" || ((_b = config2 == null ? void 0 : config2.flowchart) == null ? void 0 : _b.defaultRenderer) === "elk") {
    return false;
  }
  if (/^\s*graph/.test(txt) && ((_c = config2 == null ? void 0 : config2.flowchart) == null ? void 0 : _c.defaultRenderer) === "dagre-wrapper") {
    return true;
  }
  return /^\s*flowchart/.test(txt);
};
const loader$i = async () => {
  const { diagram: diagram2 } = await import("./flowDiagram-v2-54a189bd.js");
  return { id: id$h, diagram: diagram2 };
};
const plugin$f = {
  id: id$h,
  detector: detector$h,
  loader: loader$i
};
const flowchartV2 = plugin$f;
const id$g = "er";
const detector$g = (txt) => {
  return /^\s*erDiagram/.test(txt);
};
const loader$h = async () => {
  const { diagram: diagram2 } = await import("./erDiagram-5d923d74.js");
  return { id: id$g, diagram: diagram2 };
};
const plugin$e = {
  id: id$g,
  detector: detector$g,
  loader: loader$h
};
const er = plugin$e;
const id$f = "gitGraph";
const detector$f = (txt) => {
  return /^\s*gitGraph/.test(txt);
};
const loader$g = async () => {
  const { diagram: diagram2 } = await import("./gitGraphDiagram-94f74fa6.js");
  return { id: id$f, diagram: diagram2 };
};
const plugin$d = {
  id: id$f,
  detector: detector$f,
  loader: loader$g
};
const git = plugin$d;
const id$e = "gantt";
const detector$e = (txt) => {
  return /^\s*gantt/.test(txt);
};
const loader$f = async () => {
  const { diagram: diagram2 } = await import("./ganttDiagram-67dd342e.js");
  return { id: id$e, diagram: diagram2 };
};
const plugin$c = {
  id: id$e,
  detector: detector$e,
  loader: loader$f
};
const gantt = plugin$c;
const id$d = "info";
const detector$d = (txt) => {
  return /^\s*info/.test(txt);
};
const loader$e = async () => {
  const { diagram: diagram2 } = await import("./infoDiagram-6a975df6.js");
  return { id: id$d, diagram: diagram2 };
};
const info = {
  id: id$d,
  detector: detector$d,
  loader: loader$e
};
const id$c = "pie";
const detector$c = (txt) => {
  return /^\s*pie/.test(txt);
};
const loader$d = async () => {
  const { diagram: diagram2 } = await import("./pieDiagram-cdffdf74.js");
  return { id: id$c, diagram: diagram2 };
};
const pie = {
  id: id$c,
  detector: detector$c,
  loader: loader$d
};
const id$b = "quadrantChart";
const detector$b = (txt) => {
  return /^\s*quadrantChart/.test(txt);
};
const loader$c = async () => {
  const { diagram: diagram2 } = await import("./quadrantDiagram-f86baae9.js");
  return { id: id$b, diagram: diagram2 };
};
const plugin$b = {
  id: id$b,
  detector: detector$b,
  loader: loader$c
};
const quadrantChart = plugin$b;
const id$a = "requirement";
const detector$a = (txt) => {
  return /^\s*requirement(Diagram)?/.test(txt);
};
const loader$b = async () => {
  const { diagram: diagram2 } = await import("./requirementDiagram-d7b522a1.js");
  return { id: id$a, diagram: diagram2 };
};
const plugin$a = {
  id: id$a,
  detector: detector$a,
  loader: loader$b
};
const requirement = plugin$a;
const id$9 = "sequence";
const detector$9 = (txt) => {
  return /^\s*sequenceDiagram/.test(txt);
};
const loader$a = async () => {
  const { diagram: diagram2 } = await import("./sequenceDiagram-e03e412c.js");
  return { id: id$9, diagram: diagram2 };
};
const plugin$9 = {
  id: id$9,
  detector: detector$9,
  loader: loader$a
};
const sequence = plugin$9;
const id$8 = "class";
const detector$8 = (txt, config2) => {
  var _a;
  if (((_a = config2 == null ? void 0 : config2.class) == null ? void 0 : _a.defaultRenderer) === "dagre-wrapper") {
    return false;
  }
  return /^\s*classDiagram/.test(txt);
};
const loader$9 = async () => {
  const { diagram: diagram2 } = await import("./classDiagram-8fd6d062.js");
  return { id: id$8, diagram: diagram2 };
};
const plugin$8 = {
  id: id$8,
  detector: detector$8,
  loader: loader$9
};
const classDiagram = plugin$8;
const id$7 = "classDiagram";
const detector$7 = (txt, config2) => {
  var _a;
  if (/^\s*classDiagram/.test(txt) && ((_a = config2 == null ? void 0 : config2.class) == null ? void 0 : _a.defaultRenderer) === "dagre-wrapper") {
    return true;
  }
  return /^\s*classDiagram-v2/.test(txt);
};
const loader$8 = async () => {
  const { diagram: diagram2 } = await import("./classDiagram-v2-e3ddc2d7.js");
  return { id: id$7, diagram: diagram2 };
};
const plugin$7 = {
  id: id$7,
  detector: detector$7,
  loader: loader$8
};
const classDiagramV2 = plugin$7;
const id$6 = "state";
const detector$6 = (txt, config2) => {
  var _a;
  if (((_a = config2 == null ? void 0 : config2.state) == null ? void 0 : _a.defaultRenderer) === "dagre-wrapper") {
    return false;
  }
  return /^\s*stateDiagram/.test(txt);
};
const loader$7 = async () => {
  const { diagram: diagram2 } = await import("./stateDiagram-096e8085.js");
  return { id: id$6, diagram: diagram2 };
};
const plugin$6 = {
  id: id$6,
  detector: detector$6,
  loader: loader$7
};
const state = plugin$6;
const id$5 = "stateDiagram";
const detector$5 = (txt, config2) => {
  var _a;
  if (/^\s*stateDiagram-v2/.test(txt)) {
    return true;
  }
  if (/^\s*stateDiagram/.test(txt) && ((_a = config2 == null ? void 0 : config2.state) == null ? void 0 : _a.defaultRenderer) === "dagre-wrapper") {
    return true;
  }
  return false;
};
const loader$6 = async () => {
  const { diagram: diagram2 } = await import("./stateDiagram-v2-9dc5bbab.js");
  return { id: id$5, diagram: diagram2 };
};
const plugin$5 = {
  id: id$5,
  detector: detector$5,
  loader: loader$6
};
const stateV2 = plugin$5;
const id$4 = "journey";
const detector$4 = (txt) => {
  return /^\s*journey/.test(txt);
};
const loader$5 = async () => {
  const { diagram: diagram2 } = await import("./journeyDiagram-67cc1186.js");
  return { id: id$4, diagram: diagram2 };
};
const plugin$4 = {
  id: id$4,
  detector: detector$4,
  loader: loader$5
};
const journey = plugin$4;
const selectSvgElement = (id2) => {
  var _a;
  const { securityLevel } = getConfig$1();
  let root2 = d3select("body");
  if (securityLevel === "sandbox") {
    const sandboxElement = d3select(`#i${id2}`);
    const doc = ((_a = sandboxElement.node()) == null ? void 0 : _a.contentDocument) ?? document;
    root2 = d3select(doc.body);
  }
  const svg2 = root2.select(`#${id2}`);
  return svg2;
};
const d3Attrs = function(d3Elem, attrs) {
  for (let attr of attrs) {
    d3Elem.attr(attr[0], attr[1]);
  }
};
const calculateSvgSizeAttrs = function(height, width, useMaxWidth) {
  let attrs = /* @__PURE__ */ new Map();
  if (useMaxWidth) {
    attrs.set("width", "100%");
    attrs.set("style", `max-width: ${width}px;`);
  } else {
    attrs.set("height", height);
    attrs.set("width", width);
  }
  return attrs;
};
const configureSvgSize = function(svgElem, height, width, useMaxWidth) {
  const attrs = calculateSvgSizeAttrs(height, width, useMaxWidth);
  d3Attrs(svgElem, attrs);
};
const setupGraphViewbox$1 = function(graph, svgElem, padding, useMaxWidth) {
  const svgBounds = svgElem.node().getBBox();
  const sWidth = svgBounds.width;
  const sHeight = svgBounds.height;
  log$1.info(`SVG bounds: ${sWidth}x${sHeight}`, svgBounds);
  let width = 0;
  let height = 0;
  log$1.info(`Graph bounds: ${width}x${height}`, graph);
  width = sWidth + padding * 2;
  height = sHeight + padding * 2;
  log$1.info(`Calculated bounds: ${width}x${height}`);
  configureSvgSize(svgElem, height, width, useMaxWidth);
  const vBox = `${svgBounds.x - padding} ${svgBounds.y - padding} ${svgBounds.width + 2 * padding} ${svgBounds.height + 2 * padding}`;
  svgElem.attr("viewBox", vBox);
};
const draw = (_text, id2, version2) => {
  log$1.debug("renering svg for syntax error\n");
  const svg2 = selectSvgElement(id2);
  svg2.attr("viewBox", "0 0 2412 512");
  configureSvgSize(svg2, 100, 512, true);
  const g = svg2.append("g");
  g.append("path").attr("class", "error-icon").attr(
    "d",
    "m411.313,123.313c6.25-6.25 6.25-16.375 0-22.625s-16.375-6.25-22.625,0l-32,32-9.375,9.375-20.688-20.688c-12.484-12.5-32.766-12.5-45.25,0l-16,16c-1.261,1.261-2.304,2.648-3.31,4.051-21.739-8.561-45.324-13.426-70.065-13.426-105.867,0-192,86.133-192,192s86.133,192 192,192 192-86.133 192-192c0-24.741-4.864-48.327-13.426-70.065 1.402-1.007 2.79-2.049 4.051-3.31l16-16c12.5-12.492 12.5-32.758 0-45.25l-20.688-20.688 9.375-9.375 32.001-31.999zm-219.313,100.687c-52.938,0-96,43.063-96,96 0,8.836-7.164,16-16,16s-16-7.164-16-16c0-70.578 57.422-128 128-128 8.836,0 16,7.164 16,16s-7.164,16-16,16z"
  );
  g.append("path").attr("class", "error-icon").attr(
    "d",
    "m459.02,148.98c-6.25-6.25-16.375-6.25-22.625,0s-6.25,16.375 0,22.625l16,16c3.125,3.125 7.219,4.688 11.313,4.688 4.094,0 8.188-1.563 11.313-4.688 6.25-6.25 6.25-16.375 0-22.625l-16.001-16z"
  );
  g.append("path").attr("class", "error-icon").attr(
    "d",
    "m340.395,75.605c3.125,3.125 7.219,4.688 11.313,4.688 4.094,0 8.188-1.563 11.313-4.688 6.25-6.25 6.25-16.375 0-22.625l-16-16c-6.25-6.25-16.375-6.25-22.625,0s-6.25,16.375 0,22.625l15.999,16z"
  );
  g.append("path").attr("class", "error-icon").attr(
    "d",
    "m400,64c8.844,0 16-7.164 16-16v-32c0-8.836-7.156-16-16-16-8.844,0-16,7.164-16,16v32c0,8.836 7.156,16 16,16z"
  );
  g.append("path").attr("class", "error-icon").attr(
    "d",
    "m496,96.586h-32c-8.844,0-16,7.164-16,16 0,8.836 7.156,16 16,16h32c8.844,0 16-7.164 16-16 0-8.836-7.156-16-16-16z"
  );
  g.append("path").attr("class", "error-icon").attr(
    "d",
    "m436.98,75.605c3.125,3.125 7.219,4.688 11.313,4.688 4.094,0 8.188-1.563 11.313-4.688l32-32c6.25-6.25 6.25-16.375 0-22.625s-16.375-6.25-22.625,0l-32,32c-6.251,6.25-6.251,16.375-0.001,22.625z"
  );
  g.append("text").attr("class", "error-text").attr("x", 1440).attr("y", 250).attr("font-size", "150px").style("text-anchor", "middle").text("Syntax error in text");
  g.append("text").attr("class", "error-text").attr("x", 1250).attr("y", 400).attr("font-size", "100px").style("text-anchor", "middle").text(`mermaid version ${version2}`);
};
const renderer = { draw };
const errorRenderer = renderer;
const diagram = {
  db: {},
  renderer,
  parser: {
    parser: { yy: {} },
    parse: () => {
      return;
    }
  }
};
const errorDiagram = diagram;
const id$3 = "flowchart-elk";
const detector$3 = (txt, config2) => {
  var _a;
  if (
    // If diagram explicitly states flowchart-elk
    /^\s*flowchart-elk/.test(txt) || // If a flowchart/graph diagram has their default renderer set to elk
    /^\s*flowchart|graph/.test(txt) && ((_a = config2 == null ? void 0 : config2.flowchart) == null ? void 0 : _a.defaultRenderer) === "elk"
  ) {
    return true;
  }
  return false;
};
const loader$4 = async () => {
  const { diagram: diagram2 } = await import("./flowchart-elk-definition-387761c1.js");
  return { id: id$3, diagram: diagram2 };
};
const plugin$3 = {
  id: id$3,
  detector: detector$3,
  loader: loader$4
};
const flowchartElk = plugin$3;
const id$2 = "timeline";
const detector$2 = (txt) => {
  return /^\s*timeline/.test(txt);
};
const loader$3 = async () => {
  const { diagram: diagram2 } = await import("./timeline-definition-fd64d3c8.js");
  return { id: id$2, diagram: diagram2 };
};
const plugin$2 = {
  id: id$2,
  detector: detector$2,
  loader: loader$3
};
const timeline = plugin$2;
const id$1 = "mindmap";
const detector$1 = (txt) => {
  return /^\s*mindmap/.test(txt);
};
const loader$2 = async () => {
  const { diagram: diagram2 } = await import("./mindmap-definition-e624fba5.js");
  return { id: id$1, diagram: diagram2 };
};
const plugin$1 = {
  id: id$1,
  detector: detector$1,
  loader: loader$2
};
const mindmap = plugin$1;
const id = "sankey";
const detector = (txt) => {
  return /^\s*sankey-beta/.test(txt);
};
const loader$1 = async () => {
  const { diagram: diagram2 } = await import("./sankeyDiagram-3886b48b.js");
  return { id, diagram: diagram2 };
};
const plugin = {
  id,
  detector,
  loader: loader$1
};
const sankey = plugin;
const themes = {};
const getStyles = (type2, userStyles, options) => {
  let diagramStyles = "";
  if (type2 in themes && themes[type2]) {
    diagramStyles = themes[type2](options);
  } else {
    log$1.warn(`No theme found for ${type2}`);
  }
  return ` & {
    font-family: ${options.fontFamily};
    font-size: ${options.fontSize};
    fill: ${options.textColor}
  }

  /* Classes common for multiple diagrams */

  & .error-icon {
    fill: ${options.errorBkgColor};
  }
  & .error-text {
    fill: ${options.errorTextColor};
    stroke: ${options.errorTextColor};
  }

  & .edge-thickness-normal {
    stroke-width: 2px;
  }
  & .edge-thickness-thick {
    stroke-width: 3.5px
  }
  & .edge-pattern-solid {
    stroke-dasharray: 0;
  }

  & .edge-pattern-dashed{
    stroke-dasharray: 3;
  }
  .edge-pattern-dotted {
    stroke-dasharray: 2;
  }

  & .marker {
    fill: ${options.lineColor};
    stroke: ${options.lineColor};
  }
  & .marker.cross {
    stroke: ${options.lineColor};
  }

  & svg {
    font-family: ${options.fontFamily};
    font-size: ${options.fontSize};
  }

  ${diagramStyles}

  ${userStyles}
`;
};
const addStylesForDiagram = (type2, diagramTheme) => {
  if (diagramTheme !== void 0) {
    themes[type2] = diagramTheme;
  }
};
const getStyles$1 = getStyles;
let accTitle = "";
let diagramTitle = "";
let accDescription = "";
const sanitizeText$1 = (txt) => sanitizeText$2(txt, getConfig$1());
const clear = () => {
  accTitle = "";
  accDescription = "";
  diagramTitle = "";
};
const setAccTitle = (txt) => {
  accTitle = sanitizeText$1(txt).replace(/^\s+/g, "");
};
const getAccTitle = () => accTitle;
const setAccDescription = (txt) => {
  accDescription = sanitizeText$1(txt).replace(/\n\s+/g, "\n");
};
const getAccDescription = () => accDescription;
const setDiagramTitle = (txt) => {
  diagramTitle = sanitizeText$1(txt);
};
const getDiagramTitle = () => diagramTitle;
const commonDb = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  clear,
  getAccDescription,
  getAccTitle,
  getDiagramTitle,
  setAccDescription,
  setAccTitle,
  setDiagramTitle
}, Symbol.toStringTag, { value: "Module" }));
const log = log$1;
const setLogLevel = setLogLevel$1;
const getConfig = getConfig$1;
const sanitizeText = (text2) => sanitizeText$2(text2, getConfig());
const setupGraphViewbox = setupGraphViewbox$1;
const getCommonDb = () => {
  return commonDb;
};
const diagrams = {};
const registerDiagram = (id2, diagram2, detector2) => {
  var _a;
  if (diagrams[id2]) {
    throw new Error(`Diagram ${id2} already registered.`);
  }
  diagrams[id2] = diagram2;
  if (detector2) {
    addDetector(id2, detector2);
  }
  addStylesForDiagram(id2, diagram2.styles);
  (_a = diagram2.injectUtils) == null ? void 0 : _a.call(
    diagram2,
    log,
    setLogLevel,
    getConfig,
    sanitizeText,
    setupGraphViewbox,
    getCommonDb(),
    () => {
    }
  );
};
const getDiagram = (name) => {
  if (name in diagrams) {
    return diagrams[name];
  }
  throw new DiagramNotFoundError(name);
};
class DiagramNotFoundError extends Error {
  constructor(name) {
    super(`Diagram ${name} not found.`);
  }
}
let hasLoadedDiagrams = false;
const addDiagrams = () => {
  if (hasLoadedDiagrams) {
    return;
  }
  hasLoadedDiagrams = true;
  registerDiagram("error", errorDiagram, (text2) => {
    return text2.toLowerCase().trim() === "error";
  });
  registerDiagram(
    "---",
    // --- diagram type may appear if YAML front-matter is not parsed correctly
    {
      db: {
        clear: () => {
        }
      },
      styles: {},
      // should never be used
      renderer: {
        draw: () => {
        }
      },
      parser: {
        parser: { yy: {} },
        parse: () => {
          throw new Error(
            "Diagrams beginning with --- are not valid. If you were trying to use a YAML front-matter, please ensure that you've correctly opened and closed the YAML front-matter with un-indented `---` blocks"
          );
        }
      },
      init: () => null
      // no op
    },
    (text2) => {
      return text2.toLowerCase().trimStart().startsWith("---");
    }
  );
  registerLazyLoadedDiagrams(
    c4,
    classDiagramV2,
    classDiagram,
    er,
    gantt,
    info,
    pie,
    requirement,
    sequence,
    flowchartElk,
    flowchartV2,
    flowchart,
    mindmap,
    timeline,
    git,
    stateV2,
    state,
    journey,
    quadrantChart,
    sankey
  );
};
class Diagram {
  constructor(text2, metadata = {}) {
    this.text = text2;
    this.metadata = metadata;
    this.type = "graph";
    this.text += "\n";
    const cnf = getConfig$1();
    try {
      this.type = detectType(text2, cnf);
    } catch (e) {
      this.type = "error";
      this.detectError = e;
    }
    const diagram2 = getDiagram(this.type);
    log$1.debug("Type " + this.type);
    this.db = diagram2.db;
    this.renderer = diagram2.renderer;
    this.parser = diagram2.parser;
    this.parser.parser.yy = this.db;
    this.init = diagram2.init;
    this.parse();
  }
  parse() {
    var _a, _b, _c, _d, _e;
    if (this.detectError) {
      throw this.detectError;
    }
    (_b = (_a = this.db).clear) == null ? void 0 : _b.call(_a);
    const config2 = getConfig$1();
    (_c = this.init) == null ? void 0 : _c.call(this, config2);
    if (this.metadata.title) {
      (_e = (_d = this.db).setDiagramTitle) == null ? void 0 : _e.call(_d, this.metadata.title);
    }
    this.parser.parse(this.text);
  }
  async render(id2, version2) {
    await this.renderer.draw(this.text, id2, version2, this);
  }
  getParser() {
    return this.parser;
  }
  getType() {
    return this.type;
  }
}
const getDiagramFromText = async (text2, metadata = {}) => {
  const type2 = detectType(text2, getConfig$1());
  try {
    getDiagram(type2);
  } catch (error) {
    const loader2 = getDiagramLoader(type2);
    if (!loader2) {
      throw new UnknownDiagramError(`Diagram ${type2} not found.`);
    }
    const { id: id2, diagram: diagram2 } = await loader2();
    registerDiagram(id2, diagram2);
  }
  return new Diagram(text2, metadata);
};
let interactionFunctions = [];
const addFunction = (func) => {
  interactionFunctions.push(func);
};
const attachFunctions = () => {
  interactionFunctions.forEach((f) => {
    f();
  });
  interactionFunctions = [];
};
var nativeKeys = overArg(Object.keys, Object);
const nativeKeys$1 = nativeKeys;
var objectProto$1 = Object.prototype;
var hasOwnProperty$1 = objectProto$1.hasOwnProperty;
function baseKeys(object) {
  if (!isPrototype(object)) {
    return nativeKeys$1(object);
  }
  var result = [];
  for (var key in Object(object)) {
    if (hasOwnProperty$1.call(object, key) && key != "constructor") {
      result.push(key);
    }
  }
  return result;
}
var DataView = getNative(root$1, "DataView");
const DataView$1 = DataView;
var Promise$1 = getNative(root$1, "Promise");
const Promise$2 = Promise$1;
var Set$1 = getNative(root$1, "Set");
const Set$2 = Set$1;
var WeakMap = getNative(root$1, "WeakMap");
const WeakMap$1 = WeakMap;
var mapTag$1 = "[object Map]", objectTag = "[object Object]", promiseTag = "[object Promise]", setTag$1 = "[object Set]", weakMapTag = "[object WeakMap]";
var dataViewTag = "[object DataView]";
var dataViewCtorString = toSource(DataView$1), mapCtorString = toSource(Map$2), promiseCtorString = toSource(Promise$2), setCtorString = toSource(Set$2), weakMapCtorString = toSource(WeakMap$1);
var getTag = baseGetTag;
if (DataView$1 && getTag(new DataView$1(new ArrayBuffer(1))) != dataViewTag || Map$2 && getTag(new Map$2()) != mapTag$1 || Promise$2 && getTag(Promise$2.resolve()) != promiseTag || Set$2 && getTag(new Set$2()) != setTag$1 || WeakMap$1 && getTag(new WeakMap$1()) != weakMapTag) {
  getTag = function(value) {
    var result = baseGetTag(value), Ctor = result == objectTag ? value.constructor : void 0, ctorString = Ctor ? toSource(Ctor) : "";
    if (ctorString) {
      switch (ctorString) {
        case dataViewCtorString:
          return dataViewTag;
        case mapCtorString:
          return mapTag$1;
        case promiseCtorString:
          return promiseTag;
        case setCtorString:
          return setTag$1;
        case weakMapCtorString:
          return weakMapTag;
      }
    }
    return result;
  };
}
const getTag$1 = getTag;
var mapTag = "[object Map]", setTag = "[object Set]";
var objectProto = Object.prototype;
var hasOwnProperty = objectProto.hasOwnProperty;
function isEmpty(value) {
  if (value == null) {
    return true;
  }
  if (isArrayLike(value) && (isArray$1(value) || typeof value == "string" || typeof value.splice == "function" || isBuffer$1(value) || isTypedArray$1(value) || isArguments$1(value))) {
    return !value.length;
  }
  var tag = getTag$1(value);
  if (tag == mapTag || tag == setTag) {
    return !value.size;
  }
  if (isPrototype(value)) {
    return !baseKeys(value).length;
  }
  for (var key in value) {
    if (hasOwnProperty.call(value, key)) {
      return false;
    }
  }
  return true;
}
const SVG_ROLE = "graphics-document document";
function setA11yDiagramInfo(svg2, diagramType) {
  svg2.attr("role", SVG_ROLE);
  if (diagramType !== "") {
    svg2.attr("aria-roledescription", diagramType);
  }
}
function addSVGa11yTitleDescription(svg2, a11yTitle, a11yDesc, baseId) {
  if (svg2.insert === void 0) {
    return;
  }
  if (a11yDesc) {
    const descId = `chart-desc-${baseId}`;
    svg2.attr("aria-describedby", descId);
    svg2.insert("desc", ":first-child").attr("id", descId).text(a11yDesc);
  }
  if (a11yTitle) {
    const titleId = `chart-title-${baseId}`;
    svg2.attr("aria-labelledby", titleId);
    svg2.insert("title", ":first-child").attr("id", titleId).text(a11yTitle);
  }
}
const cleanupComments = (text2) => {
  return text2.replace(/^\s*%%(?!{)[^\n]+\n?/gm, "").trimStart();
};
/*! js-yaml 4.1.0 https://github.com/nodeca/js-yaml @license MIT */
function isNothing(subject) {
  return typeof subject === "undefined" || subject === null;
}
function isObject(subject) {
  return typeof subject === "object" && subject !== null;
}
function toArray(sequence2) {
  if (Array.isArray(sequence2))
    return sequence2;
  else if (isNothing(sequence2))
    return [];
  return [sequence2];
}
function extend(target, source) {
  var index, length2, key, sourceKeys;
  if (source) {
    sourceKeys = Object.keys(source);
    for (index = 0, length2 = sourceKeys.length; index < length2; index += 1) {
      key = sourceKeys[index];
      target[key] = source[key];
    }
  }
  return target;
}
function repeat(string, count) {
  var result = "", cycle;
  for (cycle = 0; cycle < count; cycle += 1) {
    result += string;
  }
  return result;
}
function isNegativeZero(number) {
  return number === 0 && Number.NEGATIVE_INFINITY === 1 / number;
}
var isNothing_1 = isNothing;
var isObject_1 = isObject;
var toArray_1 = toArray;
var repeat_1 = repeat;
var isNegativeZero_1 = isNegativeZero;
var extend_1 = extend;
var common = {
  isNothing: isNothing_1,
  isObject: isObject_1,
  toArray: toArray_1,
  repeat: repeat_1,
  isNegativeZero: isNegativeZero_1,
  extend: extend_1
};
function formatError(exception2, compact) {
  var where = "", message = exception2.reason || "(unknown reason)";
  if (!exception2.mark)
    return message;
  if (exception2.mark.name) {
    where += 'in "' + exception2.mark.name + '" ';
  }
  where += "(" + (exception2.mark.line + 1) + ":" + (exception2.mark.column + 1) + ")";
  if (!compact && exception2.mark.snippet) {
    where += "\n\n" + exception2.mark.snippet;
  }
  return message + " " + where;
}
function YAMLException$1(reason, mark) {
  Error.call(this);
  this.name = "YAMLException";
  this.reason = reason;
  this.mark = mark;
  this.message = formatError(this, false);
  if (Error.captureStackTrace) {
    Error.captureStackTrace(this, this.constructor);
  } else {
    this.stack = new Error().stack || "";
  }
}
YAMLException$1.prototype = Object.create(Error.prototype);
YAMLException$1.prototype.constructor = YAMLException$1;
YAMLException$1.prototype.toString = function toString(compact) {
  return this.name + ": " + formatError(this, compact);
};
var exception = YAMLException$1;
function getLine(buffer, lineStart, lineEnd, position2, maxLineLength) {
  var head = "";
  var tail = "";
  var maxHalfLength = Math.floor(maxLineLength / 2) - 1;
  if (position2 - lineStart > maxHalfLength) {
    head = " ... ";
    lineStart = position2 - maxHalfLength + head.length;
  }
  if (lineEnd - position2 > maxHalfLength) {
    tail = " ...";
    lineEnd = position2 + maxHalfLength - tail.length;
  }
  return {
    str: head + buffer.slice(lineStart, lineEnd).replace(/\t/g, "→") + tail,
    pos: position2 - lineStart + head.length
    // relative position
  };
}
function padStart(string, max2) {
  return common.repeat(" ", max2 - string.length) + string;
}
function makeSnippet(mark, options) {
  options = Object.create(options || null);
  if (!mark.buffer)
    return null;
  if (!options.maxLength)
    options.maxLength = 79;
  if (typeof options.indent !== "number")
    options.indent = 1;
  if (typeof options.linesBefore !== "number")
    options.linesBefore = 3;
  if (typeof options.linesAfter !== "number")
    options.linesAfter = 2;
  var re = /\r?\n|\r|\0/g;
  var lineStarts = [0];
  var lineEnds = [];
  var match;
  var foundLineNo = -1;
  while (match = re.exec(mark.buffer)) {
    lineEnds.push(match.index);
    lineStarts.push(match.index + match[0].length);
    if (mark.position <= match.index && foundLineNo < 0) {
      foundLineNo = lineStarts.length - 2;
    }
  }
  if (foundLineNo < 0)
    foundLineNo = lineStarts.length - 1;
  var result = "", i, line2;
  var lineNoLength = Math.min(mark.line + options.linesAfter, lineEnds.length).toString().length;
  var maxLineLength = options.maxLength - (options.indent + lineNoLength + 3);
  for (i = 1; i <= options.linesBefore; i++) {
    if (foundLineNo - i < 0)
      break;
    line2 = getLine(
      mark.buffer,
      lineStarts[foundLineNo - i],
      lineEnds[foundLineNo - i],
      mark.position - (lineStarts[foundLineNo] - lineStarts[foundLineNo - i]),
      maxLineLength
    );
    result = common.repeat(" ", options.indent) + padStart((mark.line - i + 1).toString(), lineNoLength) + " | " + line2.str + "\n" + result;
  }
  line2 = getLine(mark.buffer, lineStarts[foundLineNo], lineEnds[foundLineNo], mark.position, maxLineLength);
  result += common.repeat(" ", options.indent) + padStart((mark.line + 1).toString(), lineNoLength) + " | " + line2.str + "\n";
  result += common.repeat("-", options.indent + lineNoLength + 3 + line2.pos) + "^\n";
  for (i = 1; i <= options.linesAfter; i++) {
    if (foundLineNo + i >= lineEnds.length)
      break;
    line2 = getLine(
      mark.buffer,
      lineStarts[foundLineNo + i],
      lineEnds[foundLineNo + i],
      mark.position - (lineStarts[foundLineNo] - lineStarts[foundLineNo + i]),
      maxLineLength
    );
    result += common.repeat(" ", options.indent) + padStart((mark.line + i + 1).toString(), lineNoLength) + " | " + line2.str + "\n";
  }
  return result.replace(/\n$/, "");
}
var snippet = makeSnippet;
var TYPE_CONSTRUCTOR_OPTIONS = [
  "kind",
  "multi",
  "resolve",
  "construct",
  "instanceOf",
  "predicate",
  "represent",
  "representName",
  "defaultStyle",
  "styleAliases"
];
var YAML_NODE_KINDS = [
  "scalar",
  "sequence",
  "mapping"
];
function compileStyleAliases(map2) {
  var result = {};
  if (map2 !== null) {
    Object.keys(map2).forEach(function(style) {
      map2[style].forEach(function(alias) {
        result[String(alias)] = style;
      });
    });
  }
  return result;
}
function Type$1(tag, options) {
  options = options || {};
  Object.keys(options).forEach(function(name) {
    if (TYPE_CONSTRUCTOR_OPTIONS.indexOf(name) === -1) {
      throw new exception('Unknown option "' + name + '" is met in definition of "' + tag + '" YAML type.');
    }
  });
  this.options = options;
  this.tag = tag;
  this.kind = options["kind"] || null;
  this.resolve = options["resolve"] || function() {
    return true;
  };
  this.construct = options["construct"] || function(data) {
    return data;
  };
  this.instanceOf = options["instanceOf"] || null;
  this.predicate = options["predicate"] || null;
  this.represent = options["represent"] || null;
  this.representName = options["representName"] || null;
  this.defaultStyle = options["defaultStyle"] || null;
  this.multi = options["multi"] || false;
  this.styleAliases = compileStyleAliases(options["styleAliases"] || null);
  if (YAML_NODE_KINDS.indexOf(this.kind) === -1) {
    throw new exception('Unknown kind "' + this.kind + '" is specified for "' + tag + '" YAML type.');
  }
}
var type = Type$1;
function compileList(schema2, name) {
  var result = [];
  schema2[name].forEach(function(currentType) {
    var newIndex = result.length;
    result.forEach(function(previousType, previousIndex) {
      if (previousType.tag === currentType.tag && previousType.kind === currentType.kind && previousType.multi === currentType.multi) {
        newIndex = previousIndex;
      }
    });
    result[newIndex] = currentType;
  });
  return result;
}
function compileMap() {
  var result = {
    scalar: {},
    sequence: {},
    mapping: {},
    fallback: {},
    multi: {
      scalar: [],
      sequence: [],
      mapping: [],
      fallback: []
    }
  }, index, length2;
  function collectType(type2) {
    if (type2.multi) {
      result.multi[type2.kind].push(type2);
      result.multi["fallback"].push(type2);
    } else {
      result[type2.kind][type2.tag] = result["fallback"][type2.tag] = type2;
    }
  }
  for (index = 0, length2 = arguments.length; index < length2; index += 1) {
    arguments[index].forEach(collectType);
  }
  return result;
}
function Schema$1(definition) {
  return this.extend(definition);
}
Schema$1.prototype.extend = function extend2(definition) {
  var implicit = [];
  var explicit = [];
  if (definition instanceof type) {
    explicit.push(definition);
  } else if (Array.isArray(definition)) {
    explicit = explicit.concat(definition);
  } else if (definition && (Array.isArray(definition.implicit) || Array.isArray(definition.explicit))) {
    if (definition.implicit)
      implicit = implicit.concat(definition.implicit);
    if (definition.explicit)
      explicit = explicit.concat(definition.explicit);
  } else {
    throw new exception("Schema.extend argument should be a Type, [ Type ], or a schema definition ({ implicit: [...], explicit: [...] })");
  }
  implicit.forEach(function(type$1) {
    if (!(type$1 instanceof type)) {
      throw new exception("Specified list of YAML types (or a single Type object) contains a non-Type object.");
    }
    if (type$1.loadKind && type$1.loadKind !== "scalar") {
      throw new exception("There is a non-scalar type in the implicit list of a schema. Implicit resolving of such types is not supported.");
    }
    if (type$1.multi) {
      throw new exception("There is a multi type in the implicit list of a schema. Multi tags can only be listed as explicit.");
    }
  });
  explicit.forEach(function(type$1) {
    if (!(type$1 instanceof type)) {
      throw new exception("Specified list of YAML types (or a single Type object) contains a non-Type object.");
    }
  });
  var result = Object.create(Schema$1.prototype);
  result.implicit = (this.implicit || []).concat(implicit);
  result.explicit = (this.explicit || []).concat(explicit);
  result.compiledImplicit = compileList(result, "implicit");
  result.compiledExplicit = compileList(result, "explicit");
  result.compiledTypeMap = compileMap(result.compiledImplicit, result.compiledExplicit);
  return result;
};
var schema = Schema$1;
var str = new type("tag:yaml.org,2002:str", {
  kind: "scalar",
  construct: function(data) {
    return data !== null ? data : "";
  }
});
var seq = new type("tag:yaml.org,2002:seq", {
  kind: "sequence",
  construct: function(data) {
    return data !== null ? data : [];
  }
});
var map = new type("tag:yaml.org,2002:map", {
  kind: "mapping",
  construct: function(data) {
    return data !== null ? data : {};
  }
});
var failsafe = new schema({
  explicit: [
    str,
    seq,
    map
  ]
});
function resolveYamlNull(data) {
  if (data === null)
    return true;
  var max2 = data.length;
  return max2 === 1 && data === "~" || max2 === 4 && (data === "null" || data === "Null" || data === "NULL");
}
function constructYamlNull() {
  return null;
}
function isNull(object) {
  return object === null;
}
var _null = new type("tag:yaml.org,2002:null", {
  kind: "scalar",
  resolve: resolveYamlNull,
  construct: constructYamlNull,
  predicate: isNull,
  represent: {
    canonical: function() {
      return "~";
    },
    lowercase: function() {
      return "null";
    },
    uppercase: function() {
      return "NULL";
    },
    camelcase: function() {
      return "Null";
    },
    empty: function() {
      return "";
    }
  },
  defaultStyle: "lowercase"
});
function resolveYamlBoolean(data) {
  if (data === null)
    return false;
  var max2 = data.length;
  return max2 === 4 && (data === "true" || data === "True" || data === "TRUE") || max2 === 5 && (data === "false" || data === "False" || data === "FALSE");
}
function constructYamlBoolean(data) {
  return data === "true" || data === "True" || data === "TRUE";
}
function isBoolean(object) {
  return Object.prototype.toString.call(object) === "[object Boolean]";
}
var bool = new type("tag:yaml.org,2002:bool", {
  kind: "scalar",
  resolve: resolveYamlBoolean,
  construct: constructYamlBoolean,
  predicate: isBoolean,
  represent: {
    lowercase: function(object) {
      return object ? "true" : "false";
    },
    uppercase: function(object) {
      return object ? "TRUE" : "FALSE";
    },
    camelcase: function(object) {
      return object ? "True" : "False";
    }
  },
  defaultStyle: "lowercase"
});
function isHexCode(c) {
  return 48 <= c && c <= 57 || 65 <= c && c <= 70 || 97 <= c && c <= 102;
}
function isOctCode(c) {
  return 48 <= c && c <= 55;
}
function isDecCode(c) {
  return 48 <= c && c <= 57;
}
function resolveYamlInteger(data) {
  if (data === null)
    return false;
  var max2 = data.length, index = 0, hasDigits = false, ch;
  if (!max2)
    return false;
  ch = data[index];
  if (ch === "-" || ch === "+") {
    ch = data[++index];
  }
  if (ch === "0") {
    if (index + 1 === max2)
      return true;
    ch = data[++index];
    if (ch === "b") {
      index++;
      for (; index < max2; index++) {
        ch = data[index];
        if (ch === "_")
          continue;
        if (ch !== "0" && ch !== "1")
          return false;
        hasDigits = true;
      }
      return hasDigits && ch !== "_";
    }
    if (ch === "x") {
      index++;
      for (; index < max2; index++) {
        ch = data[index];
        if (ch === "_")
          continue;
        if (!isHexCode(data.charCodeAt(index)))
          return false;
        hasDigits = true;
      }
      return hasDigits && ch !== "_";
    }
    if (ch === "o") {
      index++;
      for (; index < max2; index++) {
        ch = data[index];
        if (ch === "_")
          continue;
        if (!isOctCode(data.charCodeAt(index)))
          return false;
        hasDigits = true;
      }
      return hasDigits && ch !== "_";
    }
  }
  if (ch === "_")
    return false;
  for (; index < max2; index++) {
    ch = data[index];
    if (ch === "_")
      continue;
    if (!isDecCode(data.charCodeAt(index))) {
      return false;
    }
    hasDigits = true;
  }
  if (!hasDigits || ch === "_")
    return false;
  return true;
}
function constructYamlInteger(data) {
  var value = data, sign2 = 1, ch;
  if (value.indexOf("_") !== -1) {
    value = value.replace(/_/g, "");
  }
  ch = value[0];
  if (ch === "-" || ch === "+") {
    if (ch === "-")
      sign2 = -1;
    value = value.slice(1);
    ch = value[0];
  }
  if (value === "0")
    return 0;
  if (ch === "0") {
    if (value[1] === "b")
      return sign2 * parseInt(value.slice(2), 2);
    if (value[1] === "x")
      return sign2 * parseInt(value.slice(2), 16);
    if (value[1] === "o")
      return sign2 * parseInt(value.slice(2), 8);
  }
  return sign2 * parseInt(value, 10);
}
function isInteger(object) {
  return Object.prototype.toString.call(object) === "[object Number]" && (object % 1 === 0 && !common.isNegativeZero(object));
}
var int = new type("tag:yaml.org,2002:int", {
  kind: "scalar",
  resolve: resolveYamlInteger,
  construct: constructYamlInteger,
  predicate: isInteger,
  represent: {
    binary: function(obj) {
      return obj >= 0 ? "0b" + obj.toString(2) : "-0b" + obj.toString(2).slice(1);
    },
    octal: function(obj) {
      return obj >= 0 ? "0o" + obj.toString(8) : "-0o" + obj.toString(8).slice(1);
    },
    decimal: function(obj) {
      return obj.toString(10);
    },
    /* eslint-disable max-len */
    hexadecimal: function(obj) {
      return obj >= 0 ? "0x" + obj.toString(16).toUpperCase() : "-0x" + obj.toString(16).toUpperCase().slice(1);
    }
  },
  defaultStyle: "decimal",
  styleAliases: {
    binary: [2, "bin"],
    octal: [8, "oct"],
    decimal: [10, "dec"],
    hexadecimal: [16, "hex"]
  }
});
var YAML_FLOAT_PATTERN = new RegExp(
  // 2.5e4, 2.5 and integers
  "^(?:[-+]?(?:[0-9][0-9_]*)(?:\\.[0-9_]*)?(?:[eE][-+]?[0-9]+)?|\\.[0-9_]+(?:[eE][-+]?[0-9]+)?|[-+]?\\.(?:inf|Inf|INF)|\\.(?:nan|NaN|NAN))$"
);
function resolveYamlFloat(data) {
  if (data === null)
    return false;
  if (!YAML_FLOAT_PATTERN.test(data) || // Quick hack to not allow integers end with `_`
  // Probably should update regexp & check speed
  data[data.length - 1] === "_") {
    return false;
  }
  return true;
}
function constructYamlFloat(data) {
  var value, sign2;
  value = data.replace(/_/g, "").toLowerCase();
  sign2 = value[0] === "-" ? -1 : 1;
  if ("+-".indexOf(value[0]) >= 0) {
    value = value.slice(1);
  }
  if (value === ".inf") {
    return sign2 === 1 ? Number.POSITIVE_INFINITY : Number.NEGATIVE_INFINITY;
  } else if (value === ".nan") {
    return NaN;
  }
  return sign2 * parseFloat(value, 10);
}
var SCIENTIFIC_WITHOUT_DOT = /^[-+]?[0-9]+e/;
function representYamlFloat(object, style) {
  var res;
  if (isNaN(object)) {
    switch (style) {
      case "lowercase":
        return ".nan";
      case "uppercase":
        return ".NAN";
      case "camelcase":
        return ".NaN";
    }
  } else if (Number.POSITIVE_INFINITY === object) {
    switch (style) {
      case "lowercase":
        return ".inf";
      case "uppercase":
        return ".INF";
      case "camelcase":
        return ".Inf";
    }
  } else if (Number.NEGATIVE_INFINITY === object) {
    switch (style) {
      case "lowercase":
        return "-.inf";
      case "uppercase":
        return "-.INF";
      case "camelcase":
        return "-.Inf";
    }
  } else if (common.isNegativeZero(object)) {
    return "-0.0";
  }
  res = object.toString(10);
  return SCIENTIFIC_WITHOUT_DOT.test(res) ? res.replace("e", ".e") : res;
}
function isFloat(object) {
  return Object.prototype.toString.call(object) === "[object Number]" && (object % 1 !== 0 || common.isNegativeZero(object));
}
var float = new type("tag:yaml.org,2002:float", {
  kind: "scalar",
  resolve: resolveYamlFloat,
  construct: constructYamlFloat,
  predicate: isFloat,
  represent: representYamlFloat,
  defaultStyle: "lowercase"
});
var json = failsafe.extend({
  implicit: [
    _null,
    bool,
    int,
    float
  ]
});
var core = json;
var YAML_DATE_REGEXP = new RegExp(
  "^([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9])$"
);
var YAML_TIMESTAMP_REGEXP = new RegExp(
  "^([0-9][0-9][0-9][0-9])-([0-9][0-9]?)-([0-9][0-9]?)(?:[Tt]|[ \\t]+)([0-9][0-9]?):([0-9][0-9]):([0-9][0-9])(?:\\.([0-9]*))?(?:[ \\t]*(Z|([-+])([0-9][0-9]?)(?::([0-9][0-9]))?))?$"
);
function resolveYamlTimestamp(data) {
  if (data === null)
    return false;
  if (YAML_DATE_REGEXP.exec(data) !== null)
    return true;
  if (YAML_TIMESTAMP_REGEXP.exec(data) !== null)
    return true;
  return false;
}
function constructYamlTimestamp(data) {
  var match, year, month, day, hour, minute, second, fraction = 0, delta = null, tz_hour, tz_minute, date;
  match = YAML_DATE_REGEXP.exec(data);
  if (match === null)
    match = YAML_TIMESTAMP_REGEXP.exec(data);
  if (match === null)
    throw new Error("Date resolve error");
  year = +match[1];
  month = +match[2] - 1;
  day = +match[3];
  if (!match[4]) {
    return new Date(Date.UTC(year, month, day));
  }
  hour = +match[4];
  minute = +match[5];
  second = +match[6];
  if (match[7]) {
    fraction = match[7].slice(0, 3);
    while (fraction.length < 3) {
      fraction += "0";
    }
    fraction = +fraction;
  }
  if (match[9]) {
    tz_hour = +match[10];
    tz_minute = +(match[11] || 0);
    delta = (tz_hour * 60 + tz_minute) * 6e4;
    if (match[9] === "-")
      delta = -delta;
  }
  date = new Date(Date.UTC(year, month, day, hour, minute, second, fraction));
  if (delta)
    date.setTime(date.getTime() - delta);
  return date;
}
function representYamlTimestamp(object) {
  return object.toISOString();
}
var timestamp = new type("tag:yaml.org,2002:timestamp", {
  kind: "scalar",
  resolve: resolveYamlTimestamp,
  construct: constructYamlTimestamp,
  instanceOf: Date,
  represent: representYamlTimestamp
});
function resolveYamlMerge(data) {
  return data === "<<" || data === null;
}
var merge = new type("tag:yaml.org,2002:merge", {
  kind: "scalar",
  resolve: resolveYamlMerge
});
var BASE64_MAP = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\n\r";
function resolveYamlBinary(data) {
  if (data === null)
    return false;
  var code, idx, bitlen = 0, max2 = data.length, map2 = BASE64_MAP;
  for (idx = 0; idx < max2; idx++) {
    code = map2.indexOf(data.charAt(idx));
    if (code > 64)
      continue;
    if (code < 0)
      return false;
    bitlen += 6;
  }
  return bitlen % 8 === 0;
}
function constructYamlBinary(data) {
  var idx, tailbits, input = data.replace(/[\r\n=]/g, ""), max2 = input.length, map2 = BASE64_MAP, bits = 0, result = [];
  for (idx = 0; idx < max2; idx++) {
    if (idx % 4 === 0 && idx) {
      result.push(bits >> 16 & 255);
      result.push(bits >> 8 & 255);
      result.push(bits & 255);
    }
    bits = bits << 6 | map2.indexOf(input.charAt(idx));
  }
  tailbits = max2 % 4 * 6;
  if (tailbits === 0) {
    result.push(bits >> 16 & 255);
    result.push(bits >> 8 & 255);
    result.push(bits & 255);
  } else if (tailbits === 18) {
    result.push(bits >> 10 & 255);
    result.push(bits >> 2 & 255);
  } else if (tailbits === 12) {
    result.push(bits >> 4 & 255);
  }
  return new Uint8Array(result);
}
function representYamlBinary(object) {
  var result = "", bits = 0, idx, tail, max2 = object.length, map2 = BASE64_MAP;
  for (idx = 0; idx < max2; idx++) {
    if (idx % 3 === 0 && idx) {
      result += map2[bits >> 18 & 63];
      result += map2[bits >> 12 & 63];
      result += map2[bits >> 6 & 63];
      result += map2[bits & 63];
    }
    bits = (bits << 8) + object[idx];
  }
  tail = max2 % 3;
  if (tail === 0) {
    result += map2[bits >> 18 & 63];
    result += map2[bits >> 12 & 63];
    result += map2[bits >> 6 & 63];
    result += map2[bits & 63];
  } else if (tail === 2) {
    result += map2[bits >> 10 & 63];
    result += map2[bits >> 4 & 63];
    result += map2[bits << 2 & 63];
    result += map2[64];
  } else if (tail === 1) {
    result += map2[bits >> 2 & 63];
    result += map2[bits << 4 & 63];
    result += map2[64];
    result += map2[64];
  }
  return result;
}
function isBinary(obj) {
  return Object.prototype.toString.call(obj) === "[object Uint8Array]";
}
var binary = new type("tag:yaml.org,2002:binary", {
  kind: "scalar",
  resolve: resolveYamlBinary,
  construct: constructYamlBinary,
  predicate: isBinary,
  represent: representYamlBinary
});
var _hasOwnProperty$3 = Object.prototype.hasOwnProperty;
var _toString$2 = Object.prototype.toString;
function resolveYamlOmap(data) {
  if (data === null)
    return true;
  var objectKeys = [], index, length2, pair, pairKey, pairHasKey, object = data;
  for (index = 0, length2 = object.length; index < length2; index += 1) {
    pair = object[index];
    pairHasKey = false;
    if (_toString$2.call(pair) !== "[object Object]")
      return false;
    for (pairKey in pair) {
      if (_hasOwnProperty$3.call(pair, pairKey)) {
        if (!pairHasKey)
          pairHasKey = true;
        else
          return false;
      }
    }
    if (!pairHasKey)
      return false;
    if (objectKeys.indexOf(pairKey) === -1)
      objectKeys.push(pairKey);
    else
      return false;
  }
  return true;
}
function constructYamlOmap(data) {
  return data !== null ? data : [];
}
var omap = new type("tag:yaml.org,2002:omap", {
  kind: "sequence",
  resolve: resolveYamlOmap,
  construct: constructYamlOmap
});
var _toString$1 = Object.prototype.toString;
function resolveYamlPairs(data) {
  if (data === null)
    return true;
  var index, length2, pair, keys, result, object = data;
  result = new Array(object.length);
  for (index = 0, length2 = object.length; index < length2; index += 1) {
    pair = object[index];
    if (_toString$1.call(pair) !== "[object Object]")
      return false;
    keys = Object.keys(pair);
    if (keys.length !== 1)
      return false;
    result[index] = [keys[0], pair[keys[0]]];
  }
  return true;
}
function constructYamlPairs(data) {
  if (data === null)
    return [];
  var index, length2, pair, keys, result, object = data;
  result = new Array(object.length);
  for (index = 0, length2 = object.length; index < length2; index += 1) {
    pair = object[index];
    keys = Object.keys(pair);
    result[index] = [keys[0], pair[keys[0]]];
  }
  return result;
}
var pairs = new type("tag:yaml.org,2002:pairs", {
  kind: "sequence",
  resolve: resolveYamlPairs,
  construct: constructYamlPairs
});
var _hasOwnProperty$2 = Object.prototype.hasOwnProperty;
function resolveYamlSet(data) {
  if (data === null)
    return true;
  var key, object = data;
  for (key in object) {
    if (_hasOwnProperty$2.call(object, key)) {
      if (object[key] !== null)
        return false;
    }
  }
  return true;
}
function constructYamlSet(data) {
  return data !== null ? data : {};
}
var set = new type("tag:yaml.org,2002:set", {
  kind: "mapping",
  resolve: resolveYamlSet,
  construct: constructYamlSet
});
var _default = core.extend({
  implicit: [
    timestamp,
    merge
  ],
  explicit: [
    binary,
    omap,
    pairs,
    set
  ]
});
var _hasOwnProperty$1 = Object.prototype.hasOwnProperty;
var CONTEXT_FLOW_IN = 1;
var CONTEXT_FLOW_OUT = 2;
var CONTEXT_BLOCK_IN = 3;
var CONTEXT_BLOCK_OUT = 4;
var CHOMPING_CLIP = 1;
var CHOMPING_STRIP = 2;
var CHOMPING_KEEP = 3;
var PATTERN_NON_PRINTABLE = /[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x84\x86-\x9F\uFFFE\uFFFF]|[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?:[^\uD800-\uDBFF]|^)[\uDC00-\uDFFF]/;
var PATTERN_NON_ASCII_LINE_BREAKS = /[\x85\u2028\u2029]/;
var PATTERN_FLOW_INDICATORS = /[,\[\]\{\}]/;
var PATTERN_TAG_HANDLE = /^(?:!|!!|![a-z\-]+!)$/i;
var PATTERN_TAG_URI = /^(?:!|[^,\[\]\{\}])(?:%[0-9a-f]{2}|[0-9a-z\-#;\/\?:@&=\+\$,_\.!~\*'\(\)\[\]])*$/i;
function _class(obj) {
  return Object.prototype.toString.call(obj);
}
function is_EOL(c) {
  return c === 10 || c === 13;
}
function is_WHITE_SPACE(c) {
  return c === 9 || c === 32;
}
function is_WS_OR_EOL(c) {
  return c === 9 || c === 32 || c === 10 || c === 13;
}
function is_FLOW_INDICATOR(c) {
  return c === 44 || c === 91 || c === 93 || c === 123 || c === 125;
}
function fromHexCode(c) {
  var lc;
  if (48 <= c && c <= 57) {
    return c - 48;
  }
  lc = c | 32;
  if (97 <= lc && lc <= 102) {
    return lc - 97 + 10;
  }
  return -1;
}
function escapedHexLen(c) {
  if (c === 120) {
    return 2;
  }
  if (c === 117) {
    return 4;
  }
  if (c === 85) {
    return 8;
  }
  return 0;
}
function fromDecimalCode(c) {
  if (48 <= c && c <= 57) {
    return c - 48;
  }
  return -1;
}
function simpleEscapeSequence(c) {
  return c === 48 ? "\0" : c === 97 ? "\x07" : c === 98 ? "\b" : c === 116 ? "	" : c === 9 ? "	" : c === 110 ? "\n" : c === 118 ? "\v" : c === 102 ? "\f" : c === 114 ? "\r" : c === 101 ? "\x1B" : c === 32 ? " " : c === 34 ? '"' : c === 47 ? "/" : c === 92 ? "\\" : c === 78 ? "" : c === 95 ? " " : c === 76 ? "\u2028" : c === 80 ? "\u2029" : "";
}
function charFromCodepoint(c) {
  if (c <= 65535) {
    return String.fromCharCode(c);
  }
  return String.fromCharCode(
    (c - 65536 >> 10) + 55296,
    (c - 65536 & 1023) + 56320
  );
}
var simpleEscapeCheck = new Array(256);
var simpleEscapeMap = new Array(256);
for (var i = 0; i < 256; i++) {
  simpleEscapeCheck[i] = simpleEscapeSequence(i) ? 1 : 0;
  simpleEscapeMap[i] = simpleEscapeSequence(i);
}
function State$1(input, options) {
  this.input = input;
  this.filename = options["filename"] || null;
  this.schema = options["schema"] || _default;
  this.onWarning = options["onWarning"] || null;
  this.legacy = options["legacy"] || false;
  this.json = options["json"] || false;
  this.listener = options["listener"] || null;
  this.implicitTypes = this.schema.compiledImplicit;
  this.typeMap = this.schema.compiledTypeMap;
  this.length = input.length;
  this.position = 0;
  this.line = 0;
  this.lineStart = 0;
  this.lineIndent = 0;
  this.firstTabInLine = -1;
  this.documents = [];
}
function generateError(state2, message) {
  var mark = {
    name: state2.filename,
    buffer: state2.input.slice(0, -1),
    // omit trailing \0
    position: state2.position,
    line: state2.line,
    column: state2.position - state2.lineStart
  };
  mark.snippet = snippet(mark);
  return new exception(message, mark);
}
function throwError(state2, message) {
  throw generateError(state2, message);
}
function throwWarning(state2, message) {
  if (state2.onWarning) {
    state2.onWarning.call(null, generateError(state2, message));
  }
}
var directiveHandlers = {
  YAML: function handleYamlDirective(state2, name, args) {
    var match, major, minor;
    if (state2.version !== null) {
      throwError(state2, "duplication of %YAML directive");
    }
    if (args.length !== 1) {
      throwError(state2, "YAML directive accepts exactly one argument");
    }
    match = /^([0-9]+)\.([0-9]+)$/.exec(args[0]);
    if (match === null) {
      throwError(state2, "ill-formed argument of the YAML directive");
    }
    major = parseInt(match[1], 10);
    minor = parseInt(match[2], 10);
    if (major !== 1) {
      throwError(state2, "unacceptable YAML version of the document");
    }
    state2.version = args[0];
    state2.checkLineBreaks = minor < 2;
    if (minor !== 1 && minor !== 2) {
      throwWarning(state2, "unsupported YAML version of the document");
    }
  },
  TAG: function handleTagDirective(state2, name, args) {
    var handle, prefix;
    if (args.length !== 2) {
      throwError(state2, "TAG directive accepts exactly two arguments");
    }
    handle = args[0];
    prefix = args[1];
    if (!PATTERN_TAG_HANDLE.test(handle)) {
      throwError(state2, "ill-formed tag handle (first argument) of the TAG directive");
    }
    if (_hasOwnProperty$1.call(state2.tagMap, handle)) {
      throwError(state2, 'there is a previously declared suffix for "' + handle + '" tag handle');
    }
    if (!PATTERN_TAG_URI.test(prefix)) {
      throwError(state2, "ill-formed tag prefix (second argument) of the TAG directive");
    }
    try {
      prefix = decodeURIComponent(prefix);
    } catch (err) {
      throwError(state2, "tag prefix is malformed: " + prefix);
    }
    state2.tagMap[handle] = prefix;
  }
};
function captureSegment(state2, start2, end, checkJson) {
  var _position, _length, _character, _result;
  if (start2 < end) {
    _result = state2.input.slice(start2, end);
    if (checkJson) {
      for (_position = 0, _length = _result.length; _position < _length; _position += 1) {
        _character = _result.charCodeAt(_position);
        if (!(_character === 9 || 32 <= _character && _character <= 1114111)) {
          throwError(state2, "expected valid JSON character");
        }
      }
    } else if (PATTERN_NON_PRINTABLE.test(_result)) {
      throwError(state2, "the stream contains non-printable characters");
    }
    state2.result += _result;
  }
}
function mergeMappings(state2, destination, source, overridableKeys) {
  var sourceKeys, key, index, quantity;
  if (!common.isObject(source)) {
    throwError(state2, "cannot merge mappings; the provided source object is unacceptable");
  }
  sourceKeys = Object.keys(source);
  for (index = 0, quantity = sourceKeys.length; index < quantity; index += 1) {
    key = sourceKeys[index];
    if (!_hasOwnProperty$1.call(destination, key)) {
      destination[key] = source[key];
      overridableKeys[key] = true;
    }
  }
}
function storeMappingPair(state2, _result, overridableKeys, keyTag, keyNode, valueNode, startLine, startLineStart, startPos) {
  var index, quantity;
  if (Array.isArray(keyNode)) {
    keyNode = Array.prototype.slice.call(keyNode);
    for (index = 0, quantity = keyNode.length; index < quantity; index += 1) {
      if (Array.isArray(keyNode[index])) {
        throwError(state2, "nested arrays are not supported inside keys");
      }
      if (typeof keyNode === "object" && _class(keyNode[index]) === "[object Object]") {
        keyNode[index] = "[object Object]";
      }
    }
  }
  if (typeof keyNode === "object" && _class(keyNode) === "[object Object]") {
    keyNode = "[object Object]";
  }
  keyNode = String(keyNode);
  if (_result === null) {
    _result = {};
  }
  if (keyTag === "tag:yaml.org,2002:merge") {
    if (Array.isArray(valueNode)) {
      for (index = 0, quantity = valueNode.length; index < quantity; index += 1) {
        mergeMappings(state2, _result, valueNode[index], overridableKeys);
      }
    } else {
      mergeMappings(state2, _result, valueNode, overridableKeys);
    }
  } else {
    if (!state2.json && !_hasOwnProperty$1.call(overridableKeys, keyNode) && _hasOwnProperty$1.call(_result, keyNode)) {
      state2.line = startLine || state2.line;
      state2.lineStart = startLineStart || state2.lineStart;
      state2.position = startPos || state2.position;
      throwError(state2, "duplicated mapping key");
    }
    if (keyNode === "__proto__") {
      Object.defineProperty(_result, keyNode, {
        configurable: true,
        enumerable: true,
        writable: true,
        value: valueNode
      });
    } else {
      _result[keyNode] = valueNode;
    }
    delete overridableKeys[keyNode];
  }
  return _result;
}
function readLineBreak(state2) {
  var ch;
  ch = state2.input.charCodeAt(state2.position);
  if (ch === 10) {
    state2.position++;
  } else if (ch === 13) {
    state2.position++;
    if (state2.input.charCodeAt(state2.position) === 10) {
      state2.position++;
    }
  } else {
    throwError(state2, "a line break is expected");
  }
  state2.line += 1;
  state2.lineStart = state2.position;
  state2.firstTabInLine = -1;
}
function skipSeparationSpace(state2, allowComments, checkIndent) {
  var lineBreaks = 0, ch = state2.input.charCodeAt(state2.position);
  while (ch !== 0) {
    while (is_WHITE_SPACE(ch)) {
      if (ch === 9 && state2.firstTabInLine === -1) {
        state2.firstTabInLine = state2.position;
      }
      ch = state2.input.charCodeAt(++state2.position);
    }
    if (allowComments && ch === 35) {
      do {
        ch = state2.input.charCodeAt(++state2.position);
      } while (ch !== 10 && ch !== 13 && ch !== 0);
    }
    if (is_EOL(ch)) {
      readLineBreak(state2);
      ch = state2.input.charCodeAt(state2.position);
      lineBreaks++;
      state2.lineIndent = 0;
      while (ch === 32) {
        state2.lineIndent++;
        ch = state2.input.charCodeAt(++state2.position);
      }
    } else {
      break;
    }
  }
  if (checkIndent !== -1 && lineBreaks !== 0 && state2.lineIndent < checkIndent) {
    throwWarning(state2, "deficient indentation");
  }
  return lineBreaks;
}
function testDocumentSeparator(state2) {
  var _position = state2.position, ch;
  ch = state2.input.charCodeAt(_position);
  if ((ch === 45 || ch === 46) && ch === state2.input.charCodeAt(_position + 1) && ch === state2.input.charCodeAt(_position + 2)) {
    _position += 3;
    ch = state2.input.charCodeAt(_position);
    if (ch === 0 || is_WS_OR_EOL(ch)) {
      return true;
    }
  }
  return false;
}
function writeFoldedLines(state2, count) {
  if (count === 1) {
    state2.result += " ";
  } else if (count > 1) {
    state2.result += common.repeat("\n", count - 1);
  }
}
function readPlainScalar(state2, nodeIndent, withinFlowCollection) {
  var preceding, following, captureStart, captureEnd, hasPendingContent, _line, _lineStart, _lineIndent, _kind = state2.kind, _result = state2.result, ch;
  ch = state2.input.charCodeAt(state2.position);
  if (is_WS_OR_EOL(ch) || is_FLOW_INDICATOR(ch) || ch === 35 || ch === 38 || ch === 42 || ch === 33 || ch === 124 || ch === 62 || ch === 39 || ch === 34 || ch === 37 || ch === 64 || ch === 96) {
    return false;
  }
  if (ch === 63 || ch === 45) {
    following = state2.input.charCodeAt(state2.position + 1);
    if (is_WS_OR_EOL(following) || withinFlowCollection && is_FLOW_INDICATOR(following)) {
      return false;
    }
  }
  state2.kind = "scalar";
  state2.result = "";
  captureStart = captureEnd = state2.position;
  hasPendingContent = false;
  while (ch !== 0) {
    if (ch === 58) {
      following = state2.input.charCodeAt(state2.position + 1);
      if (is_WS_OR_EOL(following) || withinFlowCollection && is_FLOW_INDICATOR(following)) {
        break;
      }
    } else if (ch === 35) {
      preceding = state2.input.charCodeAt(state2.position - 1);
      if (is_WS_OR_EOL(preceding)) {
        break;
      }
    } else if (state2.position === state2.lineStart && testDocumentSeparator(state2) || withinFlowCollection && is_FLOW_INDICATOR(ch)) {
      break;
    } else if (is_EOL(ch)) {
      _line = state2.line;
      _lineStart = state2.lineStart;
      _lineIndent = state2.lineIndent;
      skipSeparationSpace(state2, false, -1);
      if (state2.lineIndent >= nodeIndent) {
        hasPendingContent = true;
        ch = state2.input.charCodeAt(state2.position);
        continue;
      } else {
        state2.position = captureEnd;
        state2.line = _line;
        state2.lineStart = _lineStart;
        state2.lineIndent = _lineIndent;
        break;
      }
    }
    if (hasPendingContent) {
      captureSegment(state2, captureStart, captureEnd, false);
      writeFoldedLines(state2, state2.line - _line);
      captureStart = captureEnd = state2.position;
      hasPendingContent = false;
    }
    if (!is_WHITE_SPACE(ch)) {
      captureEnd = state2.position + 1;
    }
    ch = state2.input.charCodeAt(++state2.position);
  }
  captureSegment(state2, captureStart, captureEnd, false);
  if (state2.result) {
    return true;
  }
  state2.kind = _kind;
  state2.result = _result;
  return false;
}
function readSingleQuotedScalar(state2, nodeIndent) {
  var ch, captureStart, captureEnd;
  ch = state2.input.charCodeAt(state2.position);
  if (ch !== 39) {
    return false;
  }
  state2.kind = "scalar";
  state2.result = "";
  state2.position++;
  captureStart = captureEnd = state2.position;
  while ((ch = state2.input.charCodeAt(state2.position)) !== 0) {
    if (ch === 39) {
      captureSegment(state2, captureStart, state2.position, true);
      ch = state2.input.charCodeAt(++state2.position);
      if (ch === 39) {
        captureStart = state2.position;
        state2.position++;
        captureEnd = state2.position;
      } else {
        return true;
      }
    } else if (is_EOL(ch)) {
      captureSegment(state2, captureStart, captureEnd, true);
      writeFoldedLines(state2, skipSeparationSpace(state2, false, nodeIndent));
      captureStart = captureEnd = state2.position;
    } else if (state2.position === state2.lineStart && testDocumentSeparator(state2)) {
      throwError(state2, "unexpected end of the document within a single quoted scalar");
    } else {
      state2.position++;
      captureEnd = state2.position;
    }
  }
  throwError(state2, "unexpected end of the stream within a single quoted scalar");
}
function readDoubleQuotedScalar(state2, nodeIndent) {
  var captureStart, captureEnd, hexLength, hexResult, tmp, ch;
  ch = state2.input.charCodeAt(state2.position);
  if (ch !== 34) {
    return false;
  }
  state2.kind = "scalar";
  state2.result = "";
  state2.position++;
  captureStart = captureEnd = state2.position;
  while ((ch = state2.input.charCodeAt(state2.position)) !== 0) {
    if (ch === 34) {
      captureSegment(state2, captureStart, state2.position, true);
      state2.position++;
      return true;
    } else if (ch === 92) {
      captureSegment(state2, captureStart, state2.position, true);
      ch = state2.input.charCodeAt(++state2.position);
      if (is_EOL(ch)) {
        skipSeparationSpace(state2, false, nodeIndent);
      } else if (ch < 256 && simpleEscapeCheck[ch]) {
        state2.result += simpleEscapeMap[ch];
        state2.position++;
      } else if ((tmp = escapedHexLen(ch)) > 0) {
        hexLength = tmp;
        hexResult = 0;
        for (; hexLength > 0; hexLength--) {
          ch = state2.input.charCodeAt(++state2.position);
          if ((tmp = fromHexCode(ch)) >= 0) {
            hexResult = (hexResult << 4) + tmp;
          } else {
            throwError(state2, "expected hexadecimal character");
          }
        }
        state2.result += charFromCodepoint(hexResult);
        state2.position++;
      } else {
        throwError(state2, "unknown escape sequence");
      }
      captureStart = captureEnd = state2.position;
    } else if (is_EOL(ch)) {
      captureSegment(state2, captureStart, captureEnd, true);
      writeFoldedLines(state2, skipSeparationSpace(state2, false, nodeIndent));
      captureStart = captureEnd = state2.position;
    } else if (state2.position === state2.lineStart && testDocumentSeparator(state2)) {
      throwError(state2, "unexpected end of the document within a double quoted scalar");
    } else {
      state2.position++;
      captureEnd = state2.position;
    }
  }
  throwError(state2, "unexpected end of the stream within a double quoted scalar");
}
function readFlowCollection(state2, nodeIndent) {
  var readNext = true, _line, _lineStart, _pos, _tag = state2.tag, _result, _anchor = state2.anchor, following, terminator, isPair, isExplicitPair, isMapping, overridableKeys = /* @__PURE__ */ Object.create(null), keyNode, keyTag, valueNode, ch;
  ch = state2.input.charCodeAt(state2.position);
  if (ch === 91) {
    terminator = 93;
    isMapping = false;
    _result = [];
  } else if (ch === 123) {
    terminator = 125;
    isMapping = true;
    _result = {};
  } else {
    return false;
  }
  if (state2.anchor !== null) {
    state2.anchorMap[state2.anchor] = _result;
  }
  ch = state2.input.charCodeAt(++state2.position);
  while (ch !== 0) {
    skipSeparationSpace(state2, true, nodeIndent);
    ch = state2.input.charCodeAt(state2.position);
    if (ch === terminator) {
      state2.position++;
      state2.tag = _tag;
      state2.anchor = _anchor;
      state2.kind = isMapping ? "mapping" : "sequence";
      state2.result = _result;
      return true;
    } else if (!readNext) {
      throwError(state2, "missed comma between flow collection entries");
    } else if (ch === 44) {
      throwError(state2, "expected the node content, but found ','");
    }
    keyTag = keyNode = valueNode = null;
    isPair = isExplicitPair = false;
    if (ch === 63) {
      following = state2.input.charCodeAt(state2.position + 1);
      if (is_WS_OR_EOL(following)) {
        isPair = isExplicitPair = true;
        state2.position++;
        skipSeparationSpace(state2, true, nodeIndent);
      }
    }
    _line = state2.line;
    _lineStart = state2.lineStart;
    _pos = state2.position;
    composeNode(state2, nodeIndent, CONTEXT_FLOW_IN, false, true);
    keyTag = state2.tag;
    keyNode = state2.result;
    skipSeparationSpace(state2, true, nodeIndent);
    ch = state2.input.charCodeAt(state2.position);
    if ((isExplicitPair || state2.line === _line) && ch === 58) {
      isPair = true;
      ch = state2.input.charCodeAt(++state2.position);
      skipSeparationSpace(state2, true, nodeIndent);
      composeNode(state2, nodeIndent, CONTEXT_FLOW_IN, false, true);
      valueNode = state2.result;
    }
    if (isMapping) {
      storeMappingPair(state2, _result, overridableKeys, keyTag, keyNode, valueNode, _line, _lineStart, _pos);
    } else if (isPair) {
      _result.push(storeMappingPair(state2, null, overridableKeys, keyTag, keyNode, valueNode, _line, _lineStart, _pos));
    } else {
      _result.push(keyNode);
    }
    skipSeparationSpace(state2, true, nodeIndent);
    ch = state2.input.charCodeAt(state2.position);
    if (ch === 44) {
      readNext = true;
      ch = state2.input.charCodeAt(++state2.position);
    } else {
      readNext = false;
    }
  }
  throwError(state2, "unexpected end of the stream within a flow collection");
}
function readBlockScalar(state2, nodeIndent) {
  var captureStart, folding, chomping = CHOMPING_CLIP, didReadContent = false, detectedIndent = false, textIndent = nodeIndent, emptyLines = 0, atMoreIndented = false, tmp, ch;
  ch = state2.input.charCodeAt(state2.position);
  if (ch === 124) {
    folding = false;
  } else if (ch === 62) {
    folding = true;
  } else {
    return false;
  }
  state2.kind = "scalar";
  state2.result = "";
  while (ch !== 0) {
    ch = state2.input.charCodeAt(++state2.position);
    if (ch === 43 || ch === 45) {
      if (CHOMPING_CLIP === chomping) {
        chomping = ch === 43 ? CHOMPING_KEEP : CHOMPING_STRIP;
      } else {
        throwError(state2, "repeat of a chomping mode identifier");
      }
    } else if ((tmp = fromDecimalCode(ch)) >= 0) {
      if (tmp === 0) {
        throwError(state2, "bad explicit indentation width of a block scalar; it cannot be less than one");
      } else if (!detectedIndent) {
        textIndent = nodeIndent + tmp - 1;
        detectedIndent = true;
      } else {
        throwError(state2, "repeat of an indentation width identifier");
      }
    } else {
      break;
    }
  }
  if (is_WHITE_SPACE(ch)) {
    do {
      ch = state2.input.charCodeAt(++state2.position);
    } while (is_WHITE_SPACE(ch));
    if (ch === 35) {
      do {
        ch = state2.input.charCodeAt(++state2.position);
      } while (!is_EOL(ch) && ch !== 0);
    }
  }
  while (ch !== 0) {
    readLineBreak(state2);
    state2.lineIndent = 0;
    ch = state2.input.charCodeAt(state2.position);
    while ((!detectedIndent || state2.lineIndent < textIndent) && ch === 32) {
      state2.lineIndent++;
      ch = state2.input.charCodeAt(++state2.position);
    }
    if (!detectedIndent && state2.lineIndent > textIndent) {
      textIndent = state2.lineIndent;
    }
    if (is_EOL(ch)) {
      emptyLines++;
      continue;
    }
    if (state2.lineIndent < textIndent) {
      if (chomping === CHOMPING_KEEP) {
        state2.result += common.repeat("\n", didReadContent ? 1 + emptyLines : emptyLines);
      } else if (chomping === CHOMPING_CLIP) {
        if (didReadContent) {
          state2.result += "\n";
        }
      }
      break;
    }
    if (folding) {
      if (is_WHITE_SPACE(ch)) {
        atMoreIndented = true;
        state2.result += common.repeat("\n", didReadContent ? 1 + emptyLines : emptyLines);
      } else if (atMoreIndented) {
        atMoreIndented = false;
        state2.result += common.repeat("\n", emptyLines + 1);
      } else if (emptyLines === 0) {
        if (didReadContent) {
          state2.result += " ";
        }
      } else {
        state2.result += common.repeat("\n", emptyLines);
      }
    } else {
      state2.result += common.repeat("\n", didReadContent ? 1 + emptyLines : emptyLines);
    }
    didReadContent = true;
    detectedIndent = true;
    emptyLines = 0;
    captureStart = state2.position;
    while (!is_EOL(ch) && ch !== 0) {
      ch = state2.input.charCodeAt(++state2.position);
    }
    captureSegment(state2, captureStart, state2.position, false);
  }
  return true;
}
function readBlockSequence(state2, nodeIndent) {
  var _line, _tag = state2.tag, _anchor = state2.anchor, _result = [], following, detected = false, ch;
  if (state2.firstTabInLine !== -1)
    return false;
  if (state2.anchor !== null) {
    state2.anchorMap[state2.anchor] = _result;
  }
  ch = state2.input.charCodeAt(state2.position);
  while (ch !== 0) {
    if (state2.firstTabInLine !== -1) {
      state2.position = state2.firstTabInLine;
      throwError(state2, "tab characters must not be used in indentation");
    }
    if (ch !== 45) {
      break;
    }
    following = state2.input.charCodeAt(state2.position + 1);
    if (!is_WS_OR_EOL(following)) {
      break;
    }
    detected = true;
    state2.position++;
    if (skipSeparationSpace(state2, true, -1)) {
      if (state2.lineIndent <= nodeIndent) {
        _result.push(null);
        ch = state2.input.charCodeAt(state2.position);
        continue;
      }
    }
    _line = state2.line;
    composeNode(state2, nodeIndent, CONTEXT_BLOCK_IN, false, true);
    _result.push(state2.result);
    skipSeparationSpace(state2, true, -1);
    ch = state2.input.charCodeAt(state2.position);
    if ((state2.line === _line || state2.lineIndent > nodeIndent) && ch !== 0) {
      throwError(state2, "bad indentation of a sequence entry");
    } else if (state2.lineIndent < nodeIndent) {
      break;
    }
  }
  if (detected) {
    state2.tag = _tag;
    state2.anchor = _anchor;
    state2.kind = "sequence";
    state2.result = _result;
    return true;
  }
  return false;
}
function readBlockMapping(state2, nodeIndent, flowIndent) {
  var following, allowCompact, _line, _keyLine, _keyLineStart, _keyPos, _tag = state2.tag, _anchor = state2.anchor, _result = {}, overridableKeys = /* @__PURE__ */ Object.create(null), keyTag = null, keyNode = null, valueNode = null, atExplicitKey = false, detected = false, ch;
  if (state2.firstTabInLine !== -1)
    return false;
  if (state2.anchor !== null) {
    state2.anchorMap[state2.anchor] = _result;
  }
  ch = state2.input.charCodeAt(state2.position);
  while (ch !== 0) {
    if (!atExplicitKey && state2.firstTabInLine !== -1) {
      state2.position = state2.firstTabInLine;
      throwError(state2, "tab characters must not be used in indentation");
    }
    following = state2.input.charCodeAt(state2.position + 1);
    _line = state2.line;
    if ((ch === 63 || ch === 58) && is_WS_OR_EOL(following)) {
      if (ch === 63) {
        if (atExplicitKey) {
          storeMappingPair(state2, _result, overridableKeys, keyTag, keyNode, null, _keyLine, _keyLineStart, _keyPos);
          keyTag = keyNode = valueNode = null;
        }
        detected = true;
        atExplicitKey = true;
        allowCompact = true;
      } else if (atExplicitKey) {
        atExplicitKey = false;
        allowCompact = true;
      } else {
        throwError(state2, "incomplete explicit mapping pair; a key node is missed; or followed by a non-tabulated empty line");
      }
      state2.position += 1;
      ch = following;
    } else {
      _keyLine = state2.line;
      _keyLineStart = state2.lineStart;
      _keyPos = state2.position;
      if (!composeNode(state2, flowIndent, CONTEXT_FLOW_OUT, false, true)) {
        break;
      }
      if (state2.line === _line) {
        ch = state2.input.charCodeAt(state2.position);
        while (is_WHITE_SPACE(ch)) {
          ch = state2.input.charCodeAt(++state2.position);
        }
        if (ch === 58) {
          ch = state2.input.charCodeAt(++state2.position);
          if (!is_WS_OR_EOL(ch)) {
            throwError(state2, "a whitespace character is expected after the key-value separator within a block mapping");
          }
          if (atExplicitKey) {
            storeMappingPair(state2, _result, overridableKeys, keyTag, keyNode, null, _keyLine, _keyLineStart, _keyPos);
            keyTag = keyNode = valueNode = null;
          }
          detected = true;
          atExplicitKey = false;
          allowCompact = false;
          keyTag = state2.tag;
          keyNode = state2.result;
        } else if (detected) {
          throwError(state2, "can not read an implicit mapping pair; a colon is missed");
        } else {
          state2.tag = _tag;
          state2.anchor = _anchor;
          return true;
        }
      } else if (detected) {
        throwError(state2, "can not read a block mapping entry; a multiline key may not be an implicit key");
      } else {
        state2.tag = _tag;
        state2.anchor = _anchor;
        return true;
      }
    }
    if (state2.line === _line || state2.lineIndent > nodeIndent) {
      if (atExplicitKey) {
        _keyLine = state2.line;
        _keyLineStart = state2.lineStart;
        _keyPos = state2.position;
      }
      if (composeNode(state2, nodeIndent, CONTEXT_BLOCK_OUT, true, allowCompact)) {
        if (atExplicitKey) {
          keyNode = state2.result;
        } else {
          valueNode = state2.result;
        }
      }
      if (!atExplicitKey) {
        storeMappingPair(state2, _result, overridableKeys, keyTag, keyNode, valueNode, _keyLine, _keyLineStart, _keyPos);
        keyTag = keyNode = valueNode = null;
      }
      skipSeparationSpace(state2, true, -1);
      ch = state2.input.charCodeAt(state2.position);
    }
    if ((state2.line === _line || state2.lineIndent > nodeIndent) && ch !== 0) {
      throwError(state2, "bad indentation of a mapping entry");
    } else if (state2.lineIndent < nodeIndent) {
      break;
    }
  }
  if (atExplicitKey) {
    storeMappingPair(state2, _result, overridableKeys, keyTag, keyNode, null, _keyLine, _keyLineStart, _keyPos);
  }
  if (detected) {
    state2.tag = _tag;
    state2.anchor = _anchor;
    state2.kind = "mapping";
    state2.result = _result;
  }
  return detected;
}
function readTagProperty(state2) {
  var _position, isVerbatim = false, isNamed = false, tagHandle, tagName, ch;
  ch = state2.input.charCodeAt(state2.position);
  if (ch !== 33)
    return false;
  if (state2.tag !== null) {
    throwError(state2, "duplication of a tag property");
  }
  ch = state2.input.charCodeAt(++state2.position);
  if (ch === 60) {
    isVerbatim = true;
    ch = state2.input.charCodeAt(++state2.position);
  } else if (ch === 33) {
    isNamed = true;
    tagHandle = "!!";
    ch = state2.input.charCodeAt(++state2.position);
  } else {
    tagHandle = "!";
  }
  _position = state2.position;
  if (isVerbatim) {
    do {
      ch = state2.input.charCodeAt(++state2.position);
    } while (ch !== 0 && ch !== 62);
    if (state2.position < state2.length) {
      tagName = state2.input.slice(_position, state2.position);
      ch = state2.input.charCodeAt(++state2.position);
    } else {
      throwError(state2, "unexpected end of the stream within a verbatim tag");
    }
  } else {
    while (ch !== 0 && !is_WS_OR_EOL(ch)) {
      if (ch === 33) {
        if (!isNamed) {
          tagHandle = state2.input.slice(_position - 1, state2.position + 1);
          if (!PATTERN_TAG_HANDLE.test(tagHandle)) {
            throwError(state2, "named tag handle cannot contain such characters");
          }
          isNamed = true;
          _position = state2.position + 1;
        } else {
          throwError(state2, "tag suffix cannot contain exclamation marks");
        }
      }
      ch = state2.input.charCodeAt(++state2.position);
    }
    tagName = state2.input.slice(_position, state2.position);
    if (PATTERN_FLOW_INDICATORS.test(tagName)) {
      throwError(state2, "tag suffix cannot contain flow indicator characters");
    }
  }
  if (tagName && !PATTERN_TAG_URI.test(tagName)) {
    throwError(state2, "tag name cannot contain such characters: " + tagName);
  }
  try {
    tagName = decodeURIComponent(tagName);
  } catch (err) {
    throwError(state2, "tag name is malformed: " + tagName);
  }
  if (isVerbatim) {
    state2.tag = tagName;
  } else if (_hasOwnProperty$1.call(state2.tagMap, tagHandle)) {
    state2.tag = state2.tagMap[tagHandle] + tagName;
  } else if (tagHandle === "!") {
    state2.tag = "!" + tagName;
  } else if (tagHandle === "!!") {
    state2.tag = "tag:yaml.org,2002:" + tagName;
  } else {
    throwError(state2, 'undeclared tag handle "' + tagHandle + '"');
  }
  return true;
}
function readAnchorProperty(state2) {
  var _position, ch;
  ch = state2.input.charCodeAt(state2.position);
  if (ch !== 38)
    return false;
  if (state2.anchor !== null) {
    throwError(state2, "duplication of an anchor property");
  }
  ch = state2.input.charCodeAt(++state2.position);
  _position = state2.position;
  while (ch !== 0 && !is_WS_OR_EOL(ch) && !is_FLOW_INDICATOR(ch)) {
    ch = state2.input.charCodeAt(++state2.position);
  }
  if (state2.position === _position) {
    throwError(state2, "name of an anchor node must contain at least one character");
  }
  state2.anchor = state2.input.slice(_position, state2.position);
  return true;
}
function readAlias(state2) {
  var _position, alias, ch;
  ch = state2.input.charCodeAt(state2.position);
  if (ch !== 42)
    return false;
  ch = state2.input.charCodeAt(++state2.position);
  _position = state2.position;
  while (ch !== 0 && !is_WS_OR_EOL(ch) && !is_FLOW_INDICATOR(ch)) {
    ch = state2.input.charCodeAt(++state2.position);
  }
  if (state2.position === _position) {
    throwError(state2, "name of an alias node must contain at least one character");
  }
  alias = state2.input.slice(_position, state2.position);
  if (!_hasOwnProperty$1.call(state2.anchorMap, alias)) {
    throwError(state2, 'unidentified alias "' + alias + '"');
  }
  state2.result = state2.anchorMap[alias];
  skipSeparationSpace(state2, true, -1);
  return true;
}
function composeNode(state2, parentIndent, nodeContext, allowToSeek, allowCompact) {
  var allowBlockStyles, allowBlockScalars, allowBlockCollections, indentStatus = 1, atNewLine = false, hasContent = false, typeIndex, typeQuantity, typeList, type2, flowIndent, blockIndent;
  if (state2.listener !== null) {
    state2.listener("open", state2);
  }
  state2.tag = null;
  state2.anchor = null;
  state2.kind = null;
  state2.result = null;
  allowBlockStyles = allowBlockScalars = allowBlockCollections = CONTEXT_BLOCK_OUT === nodeContext || CONTEXT_BLOCK_IN === nodeContext;
  if (allowToSeek) {
    if (skipSeparationSpace(state2, true, -1)) {
      atNewLine = true;
      if (state2.lineIndent > parentIndent) {
        indentStatus = 1;
      } else if (state2.lineIndent === parentIndent) {
        indentStatus = 0;
      } else if (state2.lineIndent < parentIndent) {
        indentStatus = -1;
      }
    }
  }
  if (indentStatus === 1) {
    while (readTagProperty(state2) || readAnchorProperty(state2)) {
      if (skipSeparationSpace(state2, true, -1)) {
        atNewLine = true;
        allowBlockCollections = allowBlockStyles;
        if (state2.lineIndent > parentIndent) {
          indentStatus = 1;
        } else if (state2.lineIndent === parentIndent) {
          indentStatus = 0;
        } else if (state2.lineIndent < parentIndent) {
          indentStatus = -1;
        }
      } else {
        allowBlockCollections = false;
      }
    }
  }
  if (allowBlockCollections) {
    allowBlockCollections = atNewLine || allowCompact;
  }
  if (indentStatus === 1 || CONTEXT_BLOCK_OUT === nodeContext) {
    if (CONTEXT_FLOW_IN === nodeContext || CONTEXT_FLOW_OUT === nodeContext) {
      flowIndent = parentIndent;
    } else {
      flowIndent = parentIndent + 1;
    }
    blockIndent = state2.position - state2.lineStart;
    if (indentStatus === 1) {
      if (allowBlockCollections && (readBlockSequence(state2, blockIndent) || readBlockMapping(state2, blockIndent, flowIndent)) || readFlowCollection(state2, flowIndent)) {
        hasContent = true;
      } else {
        if (allowBlockScalars && readBlockScalar(state2, flowIndent) || readSingleQuotedScalar(state2, flowIndent) || readDoubleQuotedScalar(state2, flowIndent)) {
          hasContent = true;
        } else if (readAlias(state2)) {
          hasContent = true;
          if (state2.tag !== null || state2.anchor !== null) {
            throwError(state2, "alias node should not have any properties");
          }
        } else if (readPlainScalar(state2, flowIndent, CONTEXT_FLOW_IN === nodeContext)) {
          hasContent = true;
          if (state2.tag === null) {
            state2.tag = "?";
          }
        }
        if (state2.anchor !== null) {
          state2.anchorMap[state2.anchor] = state2.result;
        }
      }
    } else if (indentStatus === 0) {
      hasContent = allowBlockCollections && readBlockSequence(state2, blockIndent);
    }
  }
  if (state2.tag === null) {
    if (state2.anchor !== null) {
      state2.anchorMap[state2.anchor] = state2.result;
    }
  } else if (state2.tag === "?") {
    if (state2.result !== null && state2.kind !== "scalar") {
      throwError(state2, 'unacceptable node kind for !<?> tag; it should be "scalar", not "' + state2.kind + '"');
    }
    for (typeIndex = 0, typeQuantity = state2.implicitTypes.length; typeIndex < typeQuantity; typeIndex += 1) {
      type2 = state2.implicitTypes[typeIndex];
      if (type2.resolve(state2.result)) {
        state2.result = type2.construct(state2.result);
        state2.tag = type2.tag;
        if (state2.anchor !== null) {
          state2.anchorMap[state2.anchor] = state2.result;
        }
        break;
      }
    }
  } else if (state2.tag !== "!") {
    if (_hasOwnProperty$1.call(state2.typeMap[state2.kind || "fallback"], state2.tag)) {
      type2 = state2.typeMap[state2.kind || "fallback"][state2.tag];
    } else {
      type2 = null;
      typeList = state2.typeMap.multi[state2.kind || "fallback"];
      for (typeIndex = 0, typeQuantity = typeList.length; typeIndex < typeQuantity; typeIndex += 1) {
        if (state2.tag.slice(0, typeList[typeIndex].tag.length) === typeList[typeIndex].tag) {
          type2 = typeList[typeIndex];
          break;
        }
      }
    }
    if (!type2) {
      throwError(state2, "unknown tag !<" + state2.tag + ">");
    }
    if (state2.result !== null && type2.kind !== state2.kind) {
      throwError(state2, "unacceptable node kind for !<" + state2.tag + '> tag; it should be "' + type2.kind + '", not "' + state2.kind + '"');
    }
    if (!type2.resolve(state2.result, state2.tag)) {
      throwError(state2, "cannot resolve a node with !<" + state2.tag + "> explicit tag");
    } else {
      state2.result = type2.construct(state2.result, state2.tag);
      if (state2.anchor !== null) {
        state2.anchorMap[state2.anchor] = state2.result;
      }
    }
  }
  if (state2.listener !== null) {
    state2.listener("close", state2);
  }
  return state2.tag !== null || state2.anchor !== null || hasContent;
}
function readDocument(state2) {
  var documentStart = state2.position, _position, directiveName, directiveArgs, hasDirectives = false, ch;
  state2.version = null;
  state2.checkLineBreaks = state2.legacy;
  state2.tagMap = /* @__PURE__ */ Object.create(null);
  state2.anchorMap = /* @__PURE__ */ Object.create(null);
  while ((ch = state2.input.charCodeAt(state2.position)) !== 0) {
    skipSeparationSpace(state2, true, -1);
    ch = state2.input.charCodeAt(state2.position);
    if (state2.lineIndent > 0 || ch !== 37) {
      break;
    }
    hasDirectives = true;
    ch = state2.input.charCodeAt(++state2.position);
    _position = state2.position;
    while (ch !== 0 && !is_WS_OR_EOL(ch)) {
      ch = state2.input.charCodeAt(++state2.position);
    }
    directiveName = state2.input.slice(_position, state2.position);
    directiveArgs = [];
    if (directiveName.length < 1) {
      throwError(state2, "directive name must not be less than one character in length");
    }
    while (ch !== 0) {
      while (is_WHITE_SPACE(ch)) {
        ch = state2.input.charCodeAt(++state2.position);
      }
      if (ch === 35) {
        do {
          ch = state2.input.charCodeAt(++state2.position);
        } while (ch !== 0 && !is_EOL(ch));
        break;
      }
      if (is_EOL(ch))
        break;
      _position = state2.position;
      while (ch !== 0 && !is_WS_OR_EOL(ch)) {
        ch = state2.input.charCodeAt(++state2.position);
      }
      directiveArgs.push(state2.input.slice(_position, state2.position));
    }
    if (ch !== 0)
      readLineBreak(state2);
    if (_hasOwnProperty$1.call(directiveHandlers, directiveName)) {
      directiveHandlers[directiveName](state2, directiveName, directiveArgs);
    } else {
      throwWarning(state2, 'unknown document directive "' + directiveName + '"');
    }
  }
  skipSeparationSpace(state2, true, -1);
  if (state2.lineIndent === 0 && state2.input.charCodeAt(state2.position) === 45 && state2.input.charCodeAt(state2.position + 1) === 45 && state2.input.charCodeAt(state2.position + 2) === 45) {
    state2.position += 3;
    skipSeparationSpace(state2, true, -1);
  } else if (hasDirectives) {
    throwError(state2, "directives end mark is expected");
  }
  composeNode(state2, state2.lineIndent - 1, CONTEXT_BLOCK_OUT, false, true);
  skipSeparationSpace(state2, true, -1);
  if (state2.checkLineBreaks && PATTERN_NON_ASCII_LINE_BREAKS.test(state2.input.slice(documentStart, state2.position))) {
    throwWarning(state2, "non-ASCII line breaks are interpreted as content");
  }
  state2.documents.push(state2.result);
  if (state2.position === state2.lineStart && testDocumentSeparator(state2)) {
    if (state2.input.charCodeAt(state2.position) === 46) {
      state2.position += 3;
      skipSeparationSpace(state2, true, -1);
    }
    return;
  }
  if (state2.position < state2.length - 1) {
    throwError(state2, "end of the stream or a document separator is expected");
  } else {
    return;
  }
}
function loadDocuments(input, options) {
  input = String(input);
  options = options || {};
  if (input.length !== 0) {
    if (input.charCodeAt(input.length - 1) !== 10 && input.charCodeAt(input.length - 1) !== 13) {
      input += "\n";
    }
    if (input.charCodeAt(0) === 65279) {
      input = input.slice(1);
    }
  }
  var state2 = new State$1(input, options);
  var nullpos = input.indexOf("\0");
  if (nullpos !== -1) {
    state2.position = nullpos;
    throwError(state2, "null byte is not allowed in input");
  }
  state2.input += "\0";
  while (state2.input.charCodeAt(state2.position) === 32) {
    state2.lineIndent += 1;
    state2.position += 1;
  }
  while (state2.position < state2.length - 1) {
    readDocument(state2);
  }
  return state2.documents;
}
function loadAll$1(input, iterator, options) {
  if (iterator !== null && typeof iterator === "object" && typeof options === "undefined") {
    options = iterator;
    iterator = null;
  }
  var documents = loadDocuments(input, options);
  if (typeof iterator !== "function") {
    return documents;
  }
  for (var index = 0, length2 = documents.length; index < length2; index += 1) {
    iterator(documents[index]);
  }
}
function load$1(input, options) {
  var documents = loadDocuments(input, options);
  if (documents.length === 0) {
    return void 0;
  } else if (documents.length === 1) {
    return documents[0];
  }
  throw new exception("expected a single document in the stream, but found more");
}
var loadAll_1 = loadAll$1;
var load_1 = load$1;
var loader = {
  loadAll: loadAll_1,
  load: load_1
};
var JSON_SCHEMA = json;
var load = loader.load;
function extractFrontMatter(text2) {
  const matches = text2.match(frontMatterRegex);
  if (!matches) {
    return {
      text: text2,
      metadata: {}
    };
  }
  let parsed = load(matches[1], {
    // To support config, we need JSON schema.
    // https://www.yaml.org/spec/1.2/spec.html#id2803231
    schema: JSON_SCHEMA
  }) ?? {};
  parsed = typeof parsed === "object" && !Array.isArray(parsed) ? parsed : {};
  const metadata = {};
  if (parsed.displayMode) {
    metadata.displayMode = parsed.displayMode.toString();
  }
  if (parsed.title) {
    metadata.title = parsed.title.toString();
  }
  if (parsed.config) {
    metadata.config = parsed.config;
  }
  return {
    text: text2.slice(matches[0].length),
    metadata
  };
}
const cleanupText = (code) => {
  return code.replace(/\r\n?/g, "\n").replace(
    /<(\w+)([^>]*)>/g,
    (match, tag, attributes) => "<" + tag + attributes.replace(/="([^"]*)"/g, "='$1'") + ">"
  );
};
const processFrontmatter = (code) => {
  const { text: text2, metadata } = extractFrontMatter(code);
  const { displayMode, title, config: config2 = {} } = metadata;
  if (displayMode) {
    if (!config2.gantt) {
      config2.gantt = {};
    }
    config2.gantt.displayMode = displayMode;
  }
  return { title, config: config2, text: text2 };
};
const processDirectives = (code) => {
  const initDirective = utils.detectInit(code) ?? {};
  const wrapDirectives = utils.detectDirective(code, "wrap");
  if (Array.isArray(wrapDirectives)) {
    initDirective.wrap = wrapDirectives.some(({ type: type2 }) => {
    });
  } else if ((wrapDirectives == null ? void 0 : wrapDirectives.type) === "wrap") {
    initDirective.wrap = true;
  }
  return {
    text: removeDirectives(code),
    directive: initDirective
  };
};
function preprocessDiagram(code) {
  const cleanedCode = cleanupText(code);
  const frontMatterResult = processFrontmatter(cleanedCode);
  const directiveResult = processDirectives(frontMatterResult.text);
  const config2 = cleanAndMerge(frontMatterResult.config, directiveResult.directive);
  code = cleanupComments(directiveResult.text);
  return {
    code,
    title: frontMatterResult.title,
    config: config2
  };
}
const MAX_TEXTLENGTH = 5e4;
const MAX_TEXTLENGTH_EXCEEDED_MSG = "graph TB;a[Maximum text size in diagram exceeded];style a fill:#faa";
const SECURITY_LVL_SANDBOX = "sandbox";
const SECURITY_LVL_LOOSE = "loose";
const XMLNS_SVG_STD = "http://www.w3.org/2000/svg";
const XMLNS_XLINK_STD = "http://www.w3.org/1999/xlink";
const XMLNS_XHTML_STD = "http://www.w3.org/1999/xhtml";
const IFRAME_WIDTH = "100%";
const IFRAME_HEIGHT = "100%";
const IFRAME_STYLES = "border:0;margin:0;";
const IFRAME_BODY_STYLE = "margin:0";
const IFRAME_SANDBOX_OPTS = "allow-top-navigation-by-user-activation allow-popups";
const IFRAME_NOT_SUPPORTED_MSG = 'The "iframe" tag is not supported by your browser.';
const DOMPURIFY_TAGS = ["foreignobject"];
const DOMPURIFY_ATTR = ["dominant-baseline"];
function processAndSetConfigs(text2) {
  const processed = preprocessDiagram(text2);
  reset();
  addDirective(processed.config ?? {});
  return processed;
}
async function parse$1(text2, parseOptions) {
  addDiagrams();
  text2 = processAndSetConfigs(text2).code;
  try {
    await getDiagramFromText(text2);
  } catch (error) {
    if (parseOptions == null ? void 0 : parseOptions.suppressErrors) {
      return false;
    }
    throw error;
  }
  return true;
}
const encodeEntities = function(text2) {
  let txt = text2;
  txt = txt.replace(/style.*:\S*#.*;/g, function(s) {
    return s.substring(0, s.length - 1);
  });
  txt = txt.replace(/classDef.*:\S*#.*;/g, function(s) {
    return s.substring(0, s.length - 1);
  });
  txt = txt.replace(/#\w+;/g, function(s) {
    const innerTxt = s.substring(1, s.length - 1);
    const isInt = /^\+?\d+$/.test(innerTxt);
    if (isInt) {
      return "ﬂ°°" + innerTxt + "¶ß";
    } else {
      return "ﬂ°" + innerTxt + "¶ß";
    }
  });
  return txt;
};
const decodeEntities = function(text2) {
  return text2.replace(/ﬂ°°/g, "&#").replace(/ﬂ°/g, "&").replace(/¶ß/g, ";");
};
const cssImportantStyles = (cssClass, element, cssClasses = []) => {
  return `
.${cssClass} ${element} { ${cssClasses.join(" !important; ")} !important; }`;
};
const createCssStyles = (config2, classDefs = {}) => {
  var _a;
  let cssStyles = "";
  if (config2.themeCSS !== void 0) {
    cssStyles += `
${config2.themeCSS}`;
  }
  if (config2.fontFamily !== void 0) {
    cssStyles += `
:root { --mermaid-font-family: ${config2.fontFamily}}`;
  }
  if (config2.altFontFamily !== void 0) {
    cssStyles += `
:root { --mermaid-alt-font-family: ${config2.altFontFamily}}`;
  }
  if (!isEmpty(classDefs)) {
    const htmlLabels = config2.htmlLabels || ((_a = config2.flowchart) == null ? void 0 : _a.htmlLabels);
    const cssHtmlElements = ["> *", "span"];
    const cssShapeElements = ["rect", "polygon", "ellipse", "circle", "path"];
    const cssElements = htmlLabels ? cssHtmlElements : cssShapeElements;
    for (const classId in classDefs) {
      const styleClassDef = classDefs[classId];
      if (!isEmpty(styleClassDef.styles)) {
        cssElements.forEach((cssElement) => {
          cssStyles += cssImportantStyles(styleClassDef.id, cssElement, styleClassDef.styles);
        });
      }
      if (!isEmpty(styleClassDef.textStyles)) {
        cssStyles += cssImportantStyles(styleClassDef.id, "tspan", styleClassDef.textStyles);
      }
    }
  }
  return cssStyles;
};
const createUserStyles = (config2, graphType, classDefs, svgId) => {
  const userCSSstyles = createCssStyles(config2, classDefs);
  const allStyles = getStyles$1(graphType, userCSSstyles, config2.themeVariables);
  return serialize(compile(`${svgId}{${allStyles}}`), stringify);
};
const cleanUpSvgCode = (svgCode = "", inSandboxMode, useArrowMarkerUrls) => {
  let cleanedUpSvg = svgCode;
  if (!useArrowMarkerUrls && !inSandboxMode) {
    cleanedUpSvg = cleanedUpSvg.replace(
      /marker-end="url\([\d+./:=?A-Za-z-]*?#/g,
      'marker-end="url(#'
    );
  }
  cleanedUpSvg = decodeEntities(cleanedUpSvg);
  cleanedUpSvg = cleanedUpSvg.replace(/<br>/g, "<br/>");
  return cleanedUpSvg;
};
const putIntoIFrame = (svgCode = "", svgElement) => {
  var _a, _b;
  const height = ((_b = (_a = svgElement == null ? void 0 : svgElement.viewBox) == null ? void 0 : _a.baseVal) == null ? void 0 : _b.height) ? svgElement.viewBox.baseVal.height + "px" : IFRAME_HEIGHT;
  const base64encodedSrc = btoa('<body style="' + IFRAME_BODY_STYLE + '">' + svgCode + "</body>");
  return `<iframe style="width:${IFRAME_WIDTH};height:${height};${IFRAME_STYLES}" src="data:text/html;base64,${base64encodedSrc}" sandbox="${IFRAME_SANDBOX_OPTS}">
  ${IFRAME_NOT_SUPPORTED_MSG}
</iframe>`;
};
const appendDivSvgG = (parentRoot, id2, enclosingDivId, divStyle, svgXlink) => {
  const enclosingDiv = parentRoot.append("div");
  enclosingDiv.attr("id", enclosingDivId);
  if (divStyle) {
    enclosingDiv.attr("style", divStyle);
  }
  const svgNode2 = enclosingDiv.append("svg").attr("id", id2).attr("width", "100%").attr("xmlns", XMLNS_SVG_STD);
  if (svgXlink) {
    svgNode2.attr("xmlns:xlink", svgXlink);
  }
  svgNode2.append("g");
  return parentRoot;
};
function sandboxedIframe(parentNode, iFrameId) {
  return parentNode.append("iframe").attr("id", iFrameId).attr("style", "width: 100%; height: 100%;").attr("sandbox", "");
}
const removeExistingElements = (doc, id2, divId, iFrameId) => {
  var _a, _b, _c;
  (_a = doc.getElementById(id2)) == null ? void 0 : _a.remove();
  (_b = doc.getElementById(divId)) == null ? void 0 : _b.remove();
  (_c = doc.getElementById(iFrameId)) == null ? void 0 : _c.remove();
};
const render$1 = async function(id2, text2, svgContainingElement) {
  var _a, _b, _c, _d, _e, _f;
  addDiagrams();
  const processed = processAndSetConfigs(text2);
  text2 = processed.code;
  const config2 = getConfig$1();
  log$1.debug(config2);
  if (text2.length > ((config2 == null ? void 0 : config2.maxTextSize) ?? MAX_TEXTLENGTH)) {
    text2 = MAX_TEXTLENGTH_EXCEEDED_MSG;
  }
  const idSelector = "#" + id2;
  const iFrameID = "i" + id2;
  const iFrameID_selector = "#" + iFrameID;
  const enclosingDivID = "d" + id2;
  const enclosingDivID_selector = "#" + enclosingDivID;
  let root2 = d3select("body");
  const isSandboxed = config2.securityLevel === SECURITY_LVL_SANDBOX;
  const isLooseSecurityLevel = config2.securityLevel === SECURITY_LVL_LOOSE;
  const fontFamily = config2.fontFamily;
  if (svgContainingElement !== void 0) {
    if (svgContainingElement) {
      svgContainingElement.innerHTML = "";
    }
    if (isSandboxed) {
      const iframe = sandboxedIframe(d3select(svgContainingElement), iFrameID);
      root2 = d3select(iframe.nodes()[0].contentDocument.body);
      root2.node().style.margin = 0;
    } else {
      root2 = d3select(svgContainingElement);
    }
    appendDivSvgG(root2, id2, enclosingDivID, `font-family: ${fontFamily}`, XMLNS_XLINK_STD);
  } else {
    removeExistingElements(document, id2, enclosingDivID, iFrameID);
    if (isSandboxed) {
      const iframe = sandboxedIframe(d3select("body"), iFrameID);
      root2 = d3select(iframe.nodes()[0].contentDocument.body);
      root2.node().style.margin = 0;
    } else {
      root2 = d3select("body");
    }
    appendDivSvgG(root2, id2, enclosingDivID);
  }
  text2 = encodeEntities(text2);
  let diag;
  let parseEncounteredException;
  try {
    diag = await getDiagramFromText(text2, { title: processed.title });
  } catch (error) {
    diag = new Diagram("error");
    parseEncounteredException = error;
  }
  const element = root2.select(enclosingDivID_selector).node();
  const diagramType = diag.type;
  const svg2 = element.firstChild;
  const firstChild = svg2.firstChild;
  const diagramClassDefs = (_b = (_a = diag.renderer).getClasses) == null ? void 0 : _b.call(_a, text2, diag);
  const rules = createUserStyles(config2, diagramType, diagramClassDefs, idSelector);
  const style1 = document.createElement("style");
  style1.innerHTML = rules;
  svg2.insertBefore(style1, firstChild);
  try {
    await diag.renderer.draw(text2, id2, version, diag);
  } catch (e) {
    errorRenderer.draw(text2, id2, version);
    throw e;
  }
  const svgNode2 = root2.select(`${enclosingDivID_selector} svg`);
  const a11yTitle = (_d = (_c = diag.db).getAccTitle) == null ? void 0 : _d.call(_c);
  const a11yDescr = (_f = (_e = diag.db).getAccDescription) == null ? void 0 : _f.call(_e);
  addA11yInfo(diagramType, svgNode2, a11yTitle, a11yDescr);
  root2.select(`[id="${id2}"]`).selectAll("foreignobject > *").attr("xmlns", XMLNS_XHTML_STD);
  let svgCode = root2.select(enclosingDivID_selector).node().innerHTML;
  log$1.debug("config.arrowMarkerAbsolute", config2.arrowMarkerAbsolute);
  svgCode = cleanUpSvgCode(svgCode, isSandboxed, evaluate(config2.arrowMarkerAbsolute));
  if (isSandboxed) {
    const svgEl = root2.select(enclosingDivID_selector + " svg").node();
    svgCode = putIntoIFrame(svgCode, svgEl);
  } else if (!isLooseSecurityLevel) {
    svgCode = purify.sanitize(svgCode, {
      ADD_TAGS: DOMPURIFY_TAGS,
      ADD_ATTR: DOMPURIFY_ATTR
    });
  }
  attachFunctions();
  if (parseEncounteredException) {
    throw parseEncounteredException;
  }
  const tmpElementSelector = isSandboxed ? iFrameID_selector : enclosingDivID_selector;
  const node2 = d3select(tmpElementSelector).node();
  if (node2 && "remove" in node2) {
    node2.remove();
  }
  return {
    svg: svgCode,
    bindFunctions: diag.db.bindFunctions
  };
};
function initialize$1(options = {}) {
  var _a;
  if ((options == null ? void 0 : options.fontFamily) && !((_a = options.themeVariables) == null ? void 0 : _a.fontFamily)) {
    if (!options.themeVariables) {
      options.themeVariables = {};
    }
    options.themeVariables.fontFamily = options.fontFamily;
  }
  saveConfigFromInitialize(options);
  if ((options == null ? void 0 : options.theme) && options.theme in theme) {
    options.themeVariables = theme[options.theme].getThemeVariables(
      options.themeVariables
    );
  } else if (options) {
    options.themeVariables = theme.default.getThemeVariables(options.themeVariables);
  }
  const config2 = typeof options === "object" ? setSiteConfig(options) : getSiteConfig();
  setLogLevel$1(config2.logLevel);
  addDiagrams();
}
function addA11yInfo(diagramType, svgNode2, a11yTitle, a11yDescr) {
  setA11yDiagramInfo(svgNode2, diagramType);
  addSVGa11yTitleDescription(svgNode2, a11yTitle, a11yDescr, svgNode2.attr("id"));
}
const mermaidAPI = Object.freeze({
  render: render$1,
  parse: parse$1,
  getDiagramFromText,
  initialize: initialize$1,
  getConfig: getConfig$1,
  setConfig,
  getSiteConfig,
  updateSiteConfig,
  reset: () => {
    reset();
  },
  globalReset: () => {
    reset(defaultConfig);
  },
  defaultConfig
});
setLogLevel$1(getConfig$1().logLevel);
reset(getConfig$1());
const loadRegisteredDiagrams = async () => {
  log$1.debug(`Loading registered diagrams`);
  const results = await Promise.allSettled(
    Object.entries(detectors).map(async ([key, { detector: detector2, loader: loader2 }]) => {
      if (loader2) {
        try {
          getDiagram(key);
        } catch (error) {
          try {
            const { diagram: diagram2, id: id2 } = await loader2();
            registerDiagram(id2, diagram2, detector2);
          } catch (err) {
            log$1.error(`Failed to load external diagram with key ${key}. Removing from detectors.`);
            delete detectors[key];
            throw err;
          }
        }
      }
    })
  );
  const failed = results.filter((result) => result.status === "rejected");
  if (failed.length > 0) {
    log$1.error(`Failed to load ${failed.length} external diagrams`);
    for (const res of failed) {
      log$1.error(res);
    }
    throw new Error(`Failed to load ${failed.length} external diagrams`);
  }
};
const handleError = (error, errors, parseError) => {
  log$1.warn(error);
  if (isDetailedError(error)) {
    if (parseError) {
      parseError(error.str, error.hash);
    }
    errors.push({ ...error, message: error.str, error });
  } else {
    if (parseError) {
      parseError(error);
    }
    if (error instanceof Error) {
      errors.push({
        str: error.message,
        message: error.message,
        hash: error.name,
        error
      });
    }
  }
};
const run = async function(options = {
  querySelector: ".mermaid"
}) {
  try {
    await runThrowsErrors(options);
  } catch (e) {
    if (isDetailedError(e)) {
      log$1.error(e.str);
    }
    if (mermaid.parseError) {
      mermaid.parseError(e);
    }
    if (!options.suppressErrors) {
      log$1.error("Use the suppressErrors option to suppress these errors");
      throw e;
    }
  }
};
const runThrowsErrors = async function({ postRenderCallback, querySelector, nodes } = {
  querySelector: ".mermaid"
}) {
  const conf = mermaidAPI.getConfig();
  log$1.debug(`${!postRenderCallback ? "No " : ""}Callback function found`);
  let nodesToProcess;
  if (nodes) {
    nodesToProcess = nodes;
  } else if (querySelector) {
    nodesToProcess = document.querySelectorAll(querySelector);
  } else {
    throw new Error("Nodes and querySelector are both undefined");
  }
  log$1.debug(`Found ${nodesToProcess.length} diagrams`);
  if ((conf == null ? void 0 : conf.startOnLoad) !== void 0) {
    log$1.debug("Start On Load: " + (conf == null ? void 0 : conf.startOnLoad));
    mermaidAPI.updateSiteConfig({ startOnLoad: conf == null ? void 0 : conf.startOnLoad });
  }
  const idGenerator = new utils.InitIDGenerator(conf.deterministicIds, conf.deterministicIDSeed);
  let txt;
  const errors = [];
  for (const element of Array.from(nodesToProcess)) {
    log$1.info("Rendering diagram: " + element.id);
    /*! Check if previously processed */
    if (element.getAttribute("data-processed")) {
      continue;
    }
    element.setAttribute("data-processed", "true");
    const id2 = `mermaid-${idGenerator.next()}`;
    txt = element.innerHTML;
    txt = dedent(utils.entityDecode(txt)).trim().replace(/<br\s*\/?>/gi, "<br/>");
    const init2 = utils.detectInit(txt);
    if (init2) {
      log$1.debug("Detected early reinit: ", init2);
    }
    try {
      const { svg: svg2, bindFunctions } = await render(id2, txt, element);
      element.innerHTML = svg2;
      if (postRenderCallback) {
        await postRenderCallback(id2);
      }
      if (bindFunctions) {
        bindFunctions(element);
      }
    } catch (error) {
      handleError(error, errors, mermaid.parseError);
    }
  }
  if (errors.length > 0) {
    throw errors[0];
  }
};
const initialize = function(config2) {
  mermaidAPI.initialize(config2);
};
const init = async function(config2, nodes, callback) {
  log$1.warn("mermaid.init is deprecated. Please use run instead.");
  if (config2) {
    initialize(config2);
  }
  const runOptions = { postRenderCallback: callback, querySelector: ".mermaid" };
  if (typeof nodes === "string") {
    runOptions.querySelector = nodes;
  } else if (nodes) {
    if (nodes instanceof HTMLElement) {
      runOptions.nodes = [nodes];
    } else {
      runOptions.nodes = nodes;
    }
  }
  await run(runOptions);
};
const registerExternalDiagrams = async (diagrams2, {
  lazyLoad = true
} = {}) => {
  registerLazyLoadedDiagrams(...diagrams2);
  if (lazyLoad === false) {
    await loadRegisteredDiagrams();
  }
};
const contentLoaded = function() {
  if (mermaid.startOnLoad) {
    const { startOnLoad } = mermaidAPI.getConfig();
    if (startOnLoad) {
      mermaid.run().catch((err) => log$1.error("Mermaid failed to initialize", err));
    }
  }
};
if (typeof document !== "undefined") {
  /*!
   * Wait for document loaded before starting the execution
   */
  window.addEventListener("load", contentLoaded, false);
}
const setParseErrorHandler = function(parseErrorHandler) {
  mermaid.parseError = parseErrorHandler;
};
const executionQueue = [];
let executionQueueRunning = false;
const executeQueue = async () => {
  if (executionQueueRunning) {
    return;
  }
  executionQueueRunning = true;
  while (executionQueue.length > 0) {
    const f = executionQueue.shift();
    if (f) {
      try {
        await f();
      } catch (e) {
        log$1.error("Error executing queue", e);
      }
    }
  }
  executionQueueRunning = false;
};
const parse = async (text2, parseOptions) => {
  return new Promise((resolve, reject) => {
    const performCall = () => new Promise((res, rej) => {
      mermaidAPI.parse(text2, parseOptions).then(
        (r) => {
          res(r);
          resolve(r);
        },
        (e) => {
          var _a;
          log$1.error("Error parsing", e);
          (_a = mermaid.parseError) == null ? void 0 : _a.call(mermaid, e);
          rej(e);
          reject(e);
        }
      );
    });
    executionQueue.push(performCall);
    executeQueue().catch(reject);
  });
};
const render = (id2, text2, container) => {
  return new Promise((resolve, reject) => {
    const performCall = () => new Promise((res, rej) => {
      mermaidAPI.render(id2, text2, container).then(
        (r) => {
          res(r);
          resolve(r);
        },
        (e) => {
          var _a;
          log$1.error("Error parsing", e);
          (_a = mermaid.parseError) == null ? void 0 : _a.call(mermaid, e);
          rej(e);
          reject(e);
        }
      );
    });
    executionQueue.push(performCall);
    executeQueue().catch(reject);
  });
};
const mermaid = {
  startOnLoad: true,
  mermaidAPI,
  parse,
  render,
  init,
  run,
  registerExternalDiagrams,
  initialize,
  parseError: void 0,
  contentLoaded,
  setParseErrorHandler,
  detectType
};
export {
  getThemeVariables$2 as $,
  rgba$1 as A,
  setDiagramTitle as B,
  Color$1 as C,
  getDiagramTitle as D,
  clear as E,
  curveBasis as F,
  parseGenericTypes as G,
  random as H,
  getConfig as I,
  setupGraphViewbox as J,
  define as K,
  extend$1 as L,
  Color$2 as M,
  rgbConvert as N,
  nogamma as O,
  hue as P,
  commonjsGlobal as Q,
  Rgb as R,
  Selection$1 as S,
  getDefaultExportFromCjs as T,
  dayjs as U,
  selectSvgElement as V,
  tau as W,
  defaultConfig$1 as X,
  cleanAndMerge as Y,
  parseFontSize as Z,
  _,
  getAccDescription as a,
  sqrt as a$,
  constant$1 as a0,
  interpolateNumber as a1,
  color as a2,
  interpolateRgb as a3,
  interpolateString as a4,
  addFunction as a5,
  ZERO_WIDTH_SPACE as a6,
  generateId as a7,
  isObjectLike as a8,
  baseGetTag as a9,
  Uint8Array$2 as aA,
  isTypedArray$1 as aB,
  isLength as aC,
  isIndex as aD,
  identity as aE,
  baseFor$1 as aF,
  root$1 as aG,
  baseRest as aH,
  isIterateeCall as aI,
  baseAssignValue as aJ,
  Set$2 as aK,
  isArrayLikeObject as aL,
  constant as aM,
  isEmpty as aN,
  merge$2 as aO,
  lineBreakRegex as aP,
  defaultConfig as aQ,
  decodeEntities as aR,
  commonDb as aS,
  isDark$1 as aT,
  lighten$1 as aU,
  darken$1 as aV,
  pi as aW,
  cos as aX,
  sin as aY,
  halfPi as aZ,
  epsilon as a_,
  Symbol$2 as aa,
  isArray$1 as ab,
  isObject$1 as ac,
  isArrayLike as ad,
  arrayLikeKeys as ae,
  baseKeys as af,
  memoize as ag,
  isArguments$1 as ah,
  setToString$1 as ai,
  overRest as aj,
  copyObject as ak,
  keysIn as al,
  getPrototype$1 as am,
  cloneArrayBuffer as an,
  cloneTypedArray as ao,
  getTag$1 as ap,
  nodeUtil$1 as aq,
  baseUnary as ar,
  copyArray as as,
  isBuffer$1 as at,
  cloneBuffer as au,
  initCloneObject as av,
  Stack as aw,
  assignValue as ax,
  MapCache as ay,
  eq as az,
  setAccDescription as b,
  min as b0,
  abs$1 as b1,
  atan2 as b2,
  asin as b3,
  acos as b4,
  max as b5,
  dedent as b6,
  mermaid as b7,
  getConfig$1 as c,
  sanitizeText$2 as d,
  sanitizeUrl_1 as e,
  common$1 as f,
  getAccTitle as g,
  assignWithDepth$1 as h,
  calculateTextWidth as i,
  d3select as j,
  configureSvgSize as k,
  log$1 as l,
  calculateTextHeight as m,
  curveLinear as n,
  getStylesFromArray as o,
  evaluate as p,
  interpolateToCurve as q,
  setupGraphViewbox$1 as r,
  setAccTitle as s,
  setConfig as t,
  root$2 as u,
  array as v,
  wrapLabel as w,
  isPlainObject as x,
  isFunction as y,
  utils as z
};
