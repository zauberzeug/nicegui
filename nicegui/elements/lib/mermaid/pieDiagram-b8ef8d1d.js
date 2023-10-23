import { W as H, X as at, B as lt, D as ot, s as ct, g as ht, b as ut, a as yt, E as ft, d as pt, c as et, l as it, Y as gt, V as dt, k as mt, Z as _t } from "./mermaid-5f2d2ec5.js";
import { d as tt } from "./arc-907dcd53.js";
import { o as kt } from "./ordinal-5695958c.js";
import { a as xt } from "./array-2ff2c7a6.js";
import { c as F } from "./constant-2fe7eae5.js";
import "./init-f9637058.js";
function vt(e, h) {
  return h < e ? -1 : h > e ? 1 : h >= e ? 0 : NaN;
}
function bt(e) {
  return e;
}
function St() {
  var e = bt, h = vt, S = null, f = F(0), g = F(H), E = F(0);
  function u(r) {
    var l, k = (r = xt(r)).length, I, v, w = 0, d = new Array(k), c = new Array(k), A = +f.apply(this, arguments), $ = Math.min(H, Math.max(-H, g.apply(this, arguments) - A)), T, O = Math.min(Math.abs($) / k, E.apply(this, arguments)), x = O * ($ < 0 ? -1 : 1), t;
    for (l = 0; l < k; ++l)
      (t = c[d[l] = l] = +e(r[l], l, r)) > 0 && (w += t);
    for (h != null ? d.sort(function(i, n) {
      return h(c[i], c[n]);
    }) : S != null && d.sort(function(i, n) {
      return S(r[i], r[n]);
    }), l = 0, v = w ? ($ - k * x) / w : 0; l < k; ++l, A = T)
      I = d[l], t = c[I], T = A + (t > 0 ? t * v : 0) + x, c[I] = {
        data: r[I],
        index: l,
        value: t,
        startAngle: A,
        endAngle: T,
        padAngle: O
      };
    return c;
  }
  return u.value = function(r) {
    return arguments.length ? (e = typeof r == "function" ? r : F(+r), u) : e;
  }, u.sortValues = function(r) {
    return arguments.length ? (h = r, S = null, u) : h;
  }, u.sort = function(r) {
    return arguments.length ? (S = r, h = null, u) : S;
  }, u.startAngle = function(r) {
    return arguments.length ? (f = typeof r == "function" ? r : F(+r), u) : f;
  }, u.endAngle = function(r) {
    return arguments.length ? (g = typeof r == "function" ? r : F(+r), u) : g;
  }, u.padAngle = function(r) {
    return arguments.length ? (E = typeof r == "function" ? r : F(+r), u) : E;
  }, u;
}
var J = function() {
  var e = function(x, t, i, n) {
    for (i = i || {}, n = x.length; n--; i[x[n]] = t)
      ;
    return i;
  }, h = [1, 3], S = [1, 4], f = [1, 5], g = [1, 6], E = [1, 10, 12, 14, 16, 18, 19, 20, 21, 22], u = [2, 4], r = [1, 5, 10, 12, 14, 16, 18, 19, 20, 21, 22], l = [20, 21, 22], k = [2, 7], I = [1, 12], v = [1, 13], w = [1, 14], d = [1, 15], c = [1, 16], A = [1, 17], $ = {
    trace: function() {
    },
    yy: {},
    symbols_: { error: 2, start: 3, eol: 4, PIE: 5, document: 6, showData: 7, line: 8, statement: 9, txt: 10, value: 11, title: 12, title_value: 13, acc_title: 14, acc_title_value: 15, acc_descr: 16, acc_descr_value: 17, acc_descr_multiline_value: 18, section: 19, NEWLINE: 20, ";": 21, EOF: 22, $accept: 0, $end: 1 },
    terminals_: { 2: "error", 5: "PIE", 7: "showData", 10: "txt", 11: "value", 12: "title", 13: "title_value", 14: "acc_title", 15: "acc_title_value", 16: "acc_descr", 17: "acc_descr_value", 18: "acc_descr_multiline_value", 19: "section", 20: "NEWLINE", 21: ";", 22: "EOF" },
    productions_: [0, [3, 2], [3, 2], [3, 3], [6, 0], [6, 2], [8, 2], [9, 0], [9, 2], [9, 2], [9, 2], [9, 2], [9, 1], [9, 1], [4, 1], [4, 1], [4, 1]],
    performAction: function(t, i, n, a, o, s, V) {
      var m = s.length - 1;
      switch (o) {
        case 3:
          a.setShowData(!0);
          break;
        case 6:
          this.$ = s[m - 1];
          break;
        case 8:
          a.addSection(s[m - 1], a.cleanupValue(s[m]));
          break;
        case 9:
          this.$ = s[m].trim(), a.setDiagramTitle(this.$);
          break;
        case 10:
          this.$ = s[m].trim(), a.setAccTitle(this.$);
          break;
        case 11:
        case 12:
          this.$ = s[m].trim(), a.setAccDescription(this.$);
          break;
        case 13:
          a.addSection(s[m].substr(8)), this.$ = s[m].substr(8);
          break;
      }
    },
    table: [{ 3: 1, 4: 2, 5: h, 20: S, 21: f, 22: g }, { 1: [3] }, { 3: 7, 4: 2, 5: h, 20: S, 21: f, 22: g }, e(E, u, { 6: 8, 7: [1, 9] }), e(r, [2, 14]), e(r, [2, 15]), e(r, [2, 16]), { 1: [2, 1] }, e(l, k, { 8: 10, 9: 11, 1: [2, 2], 10: I, 12: v, 14: w, 16: d, 18: c, 19: A }), e(E, u, { 6: 18 }), e(E, [2, 5]), { 4: 19, 20: S, 21: f, 22: g }, { 11: [1, 20] }, { 13: [1, 21] }, { 15: [1, 22] }, { 17: [1, 23] }, e(l, [2, 12]), e(l, [2, 13]), e(l, k, { 8: 10, 9: 11, 1: [2, 3], 10: I, 12: v, 14: w, 16: d, 18: c, 19: A }), e(E, [2, 6]), e(l, [2, 8]), e(l, [2, 9]), e(l, [2, 10]), e(l, [2, 11])],
    defaultActions: { 7: [2, 1] },
    parseError: function(t, i) {
      if (i.recoverable)
        this.trace(t);
      else {
        var n = new Error(t);
        throw n.hash = i, n;
      }
    },
    parse: function(t) {
      var i = this, n = [0], a = [], o = [null], s = [], V = this.table, m = "", p = 0, P = 0, z = 2, j = 1, U = s.slice.call(arguments, 1), y = Object.create(this.lexer), N = { yy: {} };
      for (var Y in this.yy)
        Object.prototype.hasOwnProperty.call(this.yy, Y) && (N.yy[Y] = this.yy[Y]);
      y.setInput(t, N.yy), N.yy.lexer = y, N.yy.parser = this, typeof y.yylloc > "u" && (y.yylloc = {});
      var Z = y.yylloc;
      s.push(Z);
      var st = y.options && y.options.ranges;
      typeof N.yy.parseError == "function" ? this.parseError = N.yy.parseError : this.parseError = Object.getPrototypeOf(this).parseError;
      function rt() {
        var C;
        return C = a.pop() || y.lex() || j, typeof C != "number" && (C instanceof Array && (a = C, C = a.pop()), C = i.symbols_[C] || C), C;
      }
      for (var _, L, b, X, R = {}, M, D, Q, W; ; ) {
        if (L = n[n.length - 1], this.defaultActions[L] ? b = this.defaultActions[L] : ((_ === null || typeof _ > "u") && (_ = rt()), b = V[L] && V[L][_]), typeof b > "u" || !b.length || !b[0]) {
          var q = "";
          W = [];
          for (M in V[L])
            this.terminals_[M] && M > z && W.push("'" + this.terminals_[M] + "'");
          y.showPosition ? q = "Parse error on line " + (p + 1) + `:
` + y.showPosition() + `
Expecting ` + W.join(", ") + ", got '" + (this.terminals_[_] || _) + "'" : q = "Parse error on line " + (p + 1) + ": Unexpected " + (_ == j ? "end of input" : "'" + (this.terminals_[_] || _) + "'"), this.parseError(q, {
            text: y.match,
            token: this.terminals_[_] || _,
            line: y.yylineno,
            loc: Z,
            expected: W
          });
        }
        if (b[0] instanceof Array && b.length > 1)
          throw new Error("Parse Error: multiple actions possible at state: " + L + ", token: " + _);
        switch (b[0]) {
          case 1:
            n.push(_), o.push(y.yytext), s.push(y.yylloc), n.push(b[1]), _ = null, P = y.yyleng, m = y.yytext, p = y.yylineno, Z = y.yylloc;
            break;
          case 2:
            if (D = this.productions_[b[1]][1], R.$ = o[o.length - D], R._$ = {
              first_line: s[s.length - (D || 1)].first_line,
              last_line: s[s.length - 1].last_line,
              first_column: s[s.length - (D || 1)].first_column,
              last_column: s[s.length - 1].last_column
            }, st && (R._$.range = [
              s[s.length - (D || 1)].range[0],
              s[s.length - 1].range[1]
            ]), X = this.performAction.apply(R, [
              m,
              P,
              p,
              N.yy,
              b[1],
              o,
              s
            ].concat(U)), typeof X < "u")
              return X;
            D && (n = n.slice(0, -1 * D * 2), o = o.slice(0, -1 * D), s = s.slice(0, -1 * D)), n.push(this.productions_[b[1]][0]), o.push(R.$), s.push(R._$), Q = V[n[n.length - 2]][n[n.length - 1]], n.push(Q);
            break;
          case 3:
            return !0;
        }
      }
      return !0;
    }
  }, T = function() {
    var x = {
      EOF: 1,
      parseError: function(i, n) {
        if (this.yy.parser)
          this.yy.parser.parseError(i, n);
        else
          throw new Error(i);
      },
      // resets the lexer, sets new input
      setInput: function(t, i) {
        return this.yy = i || this.yy || {}, this._input = t, this._more = this._backtrack = this.done = !1, this.yylineno = this.yyleng = 0, this.yytext = this.matched = this.match = "", this.conditionStack = ["INITIAL"], this.yylloc = {
          first_line: 1,
          first_column: 0,
          last_line: 1,
          last_column: 0
        }, this.options.ranges && (this.yylloc.range = [0, 0]), this.offset = 0, this;
      },
      // consumes and returns one char from the input
      input: function() {
        var t = this._input[0];
        this.yytext += t, this.yyleng++, this.offset++, this.match += t, this.matched += t;
        var i = t.match(/(?:\r\n?|\n).*/g);
        return i ? (this.yylineno++, this.yylloc.last_line++) : this.yylloc.last_column++, this.options.ranges && this.yylloc.range[1]++, this._input = this._input.slice(1), t;
      },
      // unshifts one char (or a string) into the input
      unput: function(t) {
        var i = t.length, n = t.split(/(?:\r\n?|\n)/g);
        this._input = t + this._input, this.yytext = this.yytext.substr(0, this.yytext.length - i), this.offset -= i;
        var a = this.match.split(/(?:\r\n?|\n)/g);
        this.match = this.match.substr(0, this.match.length - 1), this.matched = this.matched.substr(0, this.matched.length - 1), n.length - 1 && (this.yylineno -= n.length - 1);
        var o = this.yylloc.range;
        return this.yylloc = {
          first_line: this.yylloc.first_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.first_column,
          last_column: n ? (n.length === a.length ? this.yylloc.first_column : 0) + a[a.length - n.length].length - n[0].length : this.yylloc.first_column - i
        }, this.options.ranges && (this.yylloc.range = [o[0], o[0] + this.yyleng - i]), this.yyleng = this.yytext.length, this;
      },
      // When called from action, caches matched text and appends it on next action
      more: function() {
        return this._more = !0, this;
      },
      // When called from action, signals the lexer that this rule fails to match the input, so the next matching rule (regex) should be tested instead.
      reject: function() {
        if (this.options.backtrack_lexer)
          this._backtrack = !0;
        else
          return this.parseError("Lexical error on line " + (this.yylineno + 1) + `. You can only invoke reject() in the lexer when the lexer is of the backtracking persuasion (options.backtrack_lexer = true).
` + this.showPosition(), {
            text: "",
            token: null,
            line: this.yylineno
          });
        return this;
      },
      // retain first n characters of the match
      less: function(t) {
        this.unput(this.match.slice(t));
      },
      // displays already matched input, i.e. for error messages
      pastInput: function() {
        var t = this.matched.substr(0, this.matched.length - this.match.length);
        return (t.length > 20 ? "..." : "") + t.substr(-20).replace(/\n/g, "");
      },
      // displays upcoming input, i.e. for error messages
      upcomingInput: function() {
        var t = this.match;
        return t.length < 20 && (t += this._input.substr(0, 20 - t.length)), (t.substr(0, 20) + (t.length > 20 ? "..." : "")).replace(/\n/g, "");
      },
      // displays the character position where the lexing error occurred, i.e. for error messages
      showPosition: function() {
        var t = this.pastInput(), i = new Array(t.length + 1).join("-");
        return t + this.upcomingInput() + `
` + i + "^";
      },
      // test the lexed token: return FALSE when not a match, otherwise return token
      test_match: function(t, i) {
        var n, a, o;
        if (this.options.backtrack_lexer && (o = {
          yylineno: this.yylineno,
          yylloc: {
            first_line: this.yylloc.first_line,
            last_line: this.last_line,
            first_column: this.yylloc.first_column,
            last_column: this.yylloc.last_column
          },
          yytext: this.yytext,
          match: this.match,
          matches: this.matches,
          matched: this.matched,
          yyleng: this.yyleng,
          offset: this.offset,
          _more: this._more,
          _input: this._input,
          yy: this.yy,
          conditionStack: this.conditionStack.slice(0),
          done: this.done
        }, this.options.ranges && (o.yylloc.range = this.yylloc.range.slice(0))), a = t[0].match(/(?:\r\n?|\n).*/g), a && (this.yylineno += a.length), this.yylloc = {
          first_line: this.yylloc.last_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.last_column,
          last_column: a ? a[a.length - 1].length - a[a.length - 1].match(/\r?\n?/)[0].length : this.yylloc.last_column + t[0].length
        }, this.yytext += t[0], this.match += t[0], this.matches = t, this.yyleng = this.yytext.length, this.options.ranges && (this.yylloc.range = [this.offset, this.offset += this.yyleng]), this._more = !1, this._backtrack = !1, this._input = this._input.slice(t[0].length), this.matched += t[0], n = this.performAction.call(this, this.yy, this, i, this.conditionStack[this.conditionStack.length - 1]), this.done && this._input && (this.done = !1), n)
          return n;
        if (this._backtrack) {
          for (var s in o)
            this[s] = o[s];
          return !1;
        }
        return !1;
      },
      // return next match in input
      next: function() {
        if (this.done)
          return this.EOF;
        this._input || (this.done = !0);
        var t, i, n, a;
        this._more || (this.yytext = "", this.match = "");
        for (var o = this._currentRules(), s = 0; s < o.length; s++)
          if (n = this._input.match(this.rules[o[s]]), n && (!i || n[0].length > i[0].length)) {
            if (i = n, a = s, this.options.backtrack_lexer) {
              if (t = this.test_match(n, o[s]), t !== !1)
                return t;
              if (this._backtrack) {
                i = !1;
                continue;
              } else
                return !1;
            } else if (!this.options.flex)
              break;
          }
        return i ? (t = this.test_match(i, o[a]), t !== !1 ? t : !1) : this._input === "" ? this.EOF : this.parseError("Lexical error on line " + (this.yylineno + 1) + `. Unrecognized text.
` + this.showPosition(), {
          text: "",
          token: null,
          line: this.yylineno
        });
      },
      // return next match that has a token
      lex: function() {
        var i = this.next();
        return i || this.lex();
      },
      // activates a new lexer condition state (pushes the new lexer condition state onto the condition stack)
      begin: function(i) {
        this.conditionStack.push(i);
      },
      // pop the previously active lexer condition state off the condition stack
      popState: function() {
        var i = this.conditionStack.length - 1;
        return i > 0 ? this.conditionStack.pop() : this.conditionStack[0];
      },
      // produce the lexer rule set which is active for the currently active lexer condition state
      _currentRules: function() {
        return this.conditionStack.length && this.conditionStack[this.conditionStack.length - 1] ? this.conditions[this.conditionStack[this.conditionStack.length - 1]].rules : this.conditions.INITIAL.rules;
      },
      // return the currently active lexer condition state; when an index argument is provided it produces the N-th previous condition state, if available
      topState: function(i) {
        return i = this.conditionStack.length - 1 - Math.abs(i || 0), i >= 0 ? this.conditionStack[i] : "INITIAL";
      },
      // alias for begin(condition)
      pushState: function(i) {
        this.begin(i);
      },
      // return the number of states currently on the stack
      stateStackSize: function() {
        return this.conditionStack.length;
      },
      options: { "case-insensitive": !0 },
      performAction: function(i, n, a, o) {
        switch (a) {
          case 0:
            break;
          case 1:
            break;
          case 2:
            return 20;
          case 3:
            break;
          case 4:
            break;
          case 5:
            return this.begin("title"), 12;
          case 6:
            return this.popState(), "title_value";
          case 7:
            return this.begin("acc_title"), 14;
          case 8:
            return this.popState(), "acc_title_value";
          case 9:
            return this.begin("acc_descr"), 16;
          case 10:
            return this.popState(), "acc_descr_value";
          case 11:
            this.begin("acc_descr_multiline");
            break;
          case 12:
            this.popState();
            break;
          case 13:
            return "acc_descr_multiline_value";
          case 14:
            this.begin("string");
            break;
          case 15:
            this.popState();
            break;
          case 16:
            return "txt";
          case 17:
            return 5;
          case 18:
            return 7;
          case 19:
            return "value";
          case 20:
            return 22;
        }
      },
      rules: [/^(?:%%(?!\{)[^\n]*)/i, /^(?:[^\}]%%[^\n]*)/i, /^(?:[\n\r]+)/i, /^(?:%%[^\n]*)/i, /^(?:[\s]+)/i, /^(?:title\b)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accTitle\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*\{\s*)/i, /^(?:[\}])/i, /^(?:[^\}]*)/i, /^(?:["])/i, /^(?:["])/i, /^(?:[^"]*)/i, /^(?:pie\b)/i, /^(?:showData\b)/i, /^(?::[\s]*[\d]+(?:\.[\d]+)?)/i, /^(?:$)/i],
      conditions: { acc_descr_multiline: { rules: [12, 13], inclusive: !1 }, acc_descr: { rules: [10], inclusive: !1 }, acc_title: { rules: [8], inclusive: !1 }, title: { rules: [6], inclusive: !1 }, string: { rules: [15, 16], inclusive: !1 }, INITIAL: { rules: [0, 1, 2, 3, 4, 5, 7, 9, 11, 14, 17, 18, 19, 20], inclusive: !0 } }
    };
    return x;
  }();
  $.lexer = T;
  function O() {
    this.yy = {};
  }
  return O.prototype = $, $.Parser = O, new O();
}();
J.parser = J;
const Et = J, nt = at.pie, G = {
  sections: {},
  showData: !1,
  config: nt
};
let B = G.sections, K = G.showData;
const wt = structuredClone(nt), At = () => structuredClone(wt), $t = () => {
  B = structuredClone(G.sections), K = G.showData, ft();
}, Tt = (e, h) => {
  e = pt(e, et()), B[e] === void 0 && (B[e] = h, it.debug(`added new section: ${e}, with value: ${h}`));
}, It = () => B, Dt = (e) => (e.substring(0, 1) === ":" && (e = e.substring(1).trim()), Number(e.trim())), Ct = (e) => {
  K = e;
}, Ot = () => K, Vt = {
  getConfig: At,
  clear: $t,
  setDiagramTitle: lt,
  getDiagramTitle: ot,
  setAccTitle: ct,
  getAccTitle: ht,
  setAccDescription: ut,
  getAccDescription: yt,
  addSection: Tt,
  getSections: It,
  cleanupValue: Dt,
  setShowData: Ct,
  getShowData: Ot
}, Pt = (e) => `
  .pieCircle{
    stroke: ${e.pieStrokeColor};
    stroke-width : ${e.pieStrokeWidth};
    opacity : ${e.pieOpacity};
  }
  .pieOuterCircle{
    stroke: ${e.pieOuterStrokeColor};
    stroke-width: ${e.pieOuterStrokeWidth};
    fill: none;
  }
  .pieTitleText {
    text-anchor: middle;
    font-size: ${e.pieTitleTextSize};
    fill: ${e.pieTitleTextColor};
    font-family: ${e.fontFamily};
  }
  .slice {
    font-family: ${e.fontFamily};
    fill: ${e.pieSectionTextColor};
    font-size:${e.pieSectionTextSize};
    // fill: white;
  }
  .legend text {
    fill: ${e.pieLegendTextColor};
    font-family: ${e.fontFamily};
    font-size: ${e.pieLegendTextSize};
  }
`, Nt = Pt, Lt = (e) => {
  const h = Object.entries(e).map((f) => ({
    label: f[0],
    value: f[1]
  })).sort((f, g) => g.value - f.value);
  return St().value(
    (f) => f.value
  )(h);
}, Ft = (e, h, S, f) => {
  var V, m;
  it.debug(`rendering pie chart
` + e);
  const g = f.db, E = et(), u = gt(g.getConfig(), E.pie), r = 450, l = ((m = (V = document.getElementById(h)) == null ? void 0 : V.parentElement) == null ? void 0 : m.offsetWidth) ?? u.useWidth, k = dt(h);
  k.attr("viewBox", `0 0 ${l} ${r}`), mt(k, r, l, u.useMaxWidth);
  const I = 40, v = 18, w = 4, d = k.append("g");
  d.attr("transform", "translate(" + l / 2 + "," + r / 2 + ")");
  const { themeVariables: c } = E;
  let [A] = _t(c.pieOuterStrokeWidth);
  A ?? (A = 2);
  const $ = u.textPosition, T = Math.min(l, r) / 2 - I, O = tt().innerRadius(0).outerRadius(T), x = tt().innerRadius(T * $).outerRadius(T * $);
  d.append("circle").attr("cx", 0).attr("cy", 0).attr("r", T + A / 2).attr("class", "pieOuterCircle");
  const t = g.getSections(), i = Lt(t), n = [
    c.pie1,
    c.pie2,
    c.pie3,
    c.pie4,
    c.pie5,
    c.pie6,
    c.pie7,
    c.pie8,
    c.pie9,
    c.pie10,
    c.pie11,
    c.pie12
  ], a = kt(n);
  d.selectAll("mySlices").data(i).enter().append("path").attr("d", O).attr("fill", (p) => a(p.data.label)).attr("class", "pieCircle");
  let o = 0;
  Object.keys(t).forEach((p) => {
    o += t[p];
  }), d.selectAll("mySlices").data(i).enter().append("text").text((p) => (p.data.value / o * 100).toFixed(0) + "%").attr("transform", (p) => "translate(" + x.centroid(p) + ")").style("text-anchor", "middle").attr("class", "slice"), d.append("text").text(g.getDiagramTitle()).attr("x", 0).attr("y", -(r - 50) / 2).attr("class", "pieTitleText");
  const s = d.selectAll(".legend").data(a.domain()).enter().append("g").attr("class", "legend").attr("transform", (p, P) => {
    const z = v + w, j = z * a.domain().length / 2, U = 12 * v, y = P * z - j;
    return "translate(" + U + "," + y + ")";
  });
  s.append("rect").attr("width", v).attr("height", v).style("fill", a).style("stroke", a), s.data(i).append("text").attr("x", v + w).attr("y", v - w).text((p) => {
    const { label: P, value: z } = p.data;
    return g.getShowData() ? `${P} [${z}]` : P;
  });
}, zt = { draw: Ft }, Ut = {
  parser: Et,
  db: Vt,
  renderer: zt,
  styles: Nt
};
export {
  Ut as diagram
};
