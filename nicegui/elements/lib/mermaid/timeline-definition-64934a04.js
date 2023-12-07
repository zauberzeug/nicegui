import { aS as ft, E as gt, j, c as mt, l as T, r as xt, aT as bt, aU as kt, aV as _t } from "./mermaid-5f2d2ec5.js";
import { d as D } from "./arc-907dcd53.js";
import "./constant-2fe7eae5.js";
var K = function() {
  var n = function(f, i, r, h) {
    for (r = r || {}, h = f.length; h--; r[f[h]] = i)
      ;
    return r;
  }, t = [6, 8, 10, 11, 12, 14, 16, 17, 20, 21], e = [1, 9], a = [1, 10], s = [1, 11], c = [1, 12], o = [1, 13], y = [1, 16], g = [1, 17], u = {
    trace: function() {
    },
    yy: {},
    symbols_: { error: 2, start: 3, timeline: 4, document: 5, EOF: 6, line: 7, SPACE: 8, statement: 9, NEWLINE: 10, title: 11, acc_title: 12, acc_title_value: 13, acc_descr: 14, acc_descr_value: 15, acc_descr_multiline_value: 16, section: 17, period_statement: 18, event_statement: 19, period: 20, event: 21, $accept: 0, $end: 1 },
    terminals_: { 2: "error", 4: "timeline", 6: "EOF", 8: "SPACE", 10: "NEWLINE", 11: "title", 12: "acc_title", 13: "acc_title_value", 14: "acc_descr", 15: "acc_descr_value", 16: "acc_descr_multiline_value", 17: "section", 20: "period", 21: "event" },
    productions_: [0, [3, 3], [5, 0], [5, 2], [7, 2], [7, 1], [7, 1], [7, 1], [9, 1], [9, 2], [9, 2], [9, 1], [9, 1], [9, 1], [9, 1], [18, 1], [19, 1]],
    performAction: function(i, r, h, d, p, l, w) {
      var x = l.length - 1;
      switch (p) {
        case 1:
          return l[x - 1];
        case 2:
          this.$ = [];
          break;
        case 3:
          l[x - 1].push(l[x]), this.$ = l[x - 1];
          break;
        case 4:
        case 5:
          this.$ = l[x];
          break;
        case 6:
        case 7:
          this.$ = [];
          break;
        case 8:
          d.getCommonDb().setDiagramTitle(l[x].substr(6)), this.$ = l[x].substr(6);
          break;
        case 9:
          this.$ = l[x].trim(), d.getCommonDb().setAccTitle(this.$);
          break;
        case 10:
        case 11:
          this.$ = l[x].trim(), d.getCommonDb().setAccDescription(this.$);
          break;
        case 12:
          d.addSection(l[x].substr(8)), this.$ = l[x].substr(8);
          break;
        case 15:
          d.addTask(l[x], 0, ""), this.$ = l[x];
          break;
        case 16:
          d.addEvent(l[x].substr(2)), this.$ = l[x];
          break;
      }
    },
    table: [{ 3: 1, 4: [1, 2] }, { 1: [3] }, n(t, [2, 2], { 5: 3 }), { 6: [1, 4], 7: 5, 8: [1, 6], 9: 7, 10: [1, 8], 11: e, 12: a, 14: s, 16: c, 17: o, 18: 14, 19: 15, 20: y, 21: g }, n(t, [2, 7], { 1: [2, 1] }), n(t, [2, 3]), { 9: 18, 11: e, 12: a, 14: s, 16: c, 17: o, 18: 14, 19: 15, 20: y, 21: g }, n(t, [2, 5]), n(t, [2, 6]), n(t, [2, 8]), { 13: [1, 19] }, { 15: [1, 20] }, n(t, [2, 11]), n(t, [2, 12]), n(t, [2, 13]), n(t, [2, 14]), n(t, [2, 15]), n(t, [2, 16]), n(t, [2, 4]), n(t, [2, 9]), n(t, [2, 10])],
    defaultActions: {},
    parseError: function(i, r) {
      if (r.recoverable)
        this.trace(i);
      else {
        var h = new Error(i);
        throw h.hash = r, h;
      }
    },
    parse: function(i) {
      var r = this, h = [0], d = [], p = [null], l = [], w = this.table, x = "", N = 0, A = 0, F = 2, q = 1, W = l.slice.call(arguments, 1), b = Object.create(this.lexer), S = { yy: {} };
      for (var _ in this.yy)
        Object.prototype.hasOwnProperty.call(this.yy, _) && (S.yy[_] = this.yy[_]);
      b.setInput(i, S.yy), S.yy.lexer = b, S.yy.parser = this, typeof b.yylloc > "u" && (b.yylloc = {});
      var I = b.yylloc;
      l.push(I);
      var P = b.options && b.options.ranges;
      typeof S.yy.parseError == "function" ? this.parseError = S.yy.parseError : this.parseError = Object.getPrototypeOf(this).parseError;
      function C() {
        var M;
        return M = d.pop() || b.lex() || q, typeof M != "number" && (M instanceof Array && (d = M, M = d.pop()), M = r.symbols_[M] || M), M;
      }
      for (var k, L, E, Z, z = {}, B, $, Y, O; ; ) {
        if (L = h[h.length - 1], this.defaultActions[L] ? E = this.defaultActions[L] : ((k === null || typeof k > "u") && (k = C()), E = w[L] && w[L][k]), typeof E > "u" || !E.length || !E[0]) {
          var J = "";
          O = [];
          for (B in w[L])
            this.terminals_[B] && B > F && O.push("'" + this.terminals_[B] + "'");
          b.showPosition ? J = "Parse error on line " + (N + 1) + `:
` + b.showPosition() + `
Expecting ` + O.join(", ") + ", got '" + (this.terminals_[k] || k) + "'" : J = "Parse error on line " + (N + 1) + ": Unexpected " + (k == q ? "end of input" : "'" + (this.terminals_[k] || k) + "'"), this.parseError(J, {
            text: b.match,
            token: this.terminals_[k] || k,
            line: b.yylineno,
            loc: I,
            expected: O
          });
        }
        if (E[0] instanceof Array && E.length > 1)
          throw new Error("Parse Error: multiple actions possible at state: " + L + ", token: " + k);
        switch (E[0]) {
          case 1:
            h.push(k), p.push(b.yytext), l.push(b.yylloc), h.push(E[1]), k = null, A = b.yyleng, x = b.yytext, N = b.yylineno, I = b.yylloc;
            break;
          case 2:
            if ($ = this.productions_[E[1]][1], z.$ = p[p.length - $], z._$ = {
              first_line: l[l.length - ($ || 1)].first_line,
              last_line: l[l.length - 1].last_line,
              first_column: l[l.length - ($ || 1)].first_column,
              last_column: l[l.length - 1].last_column
            }, P && (z._$.range = [
              l[l.length - ($ || 1)].range[0],
              l[l.length - 1].range[1]
            ]), Z = this.performAction.apply(z, [
              x,
              A,
              N,
              S.yy,
              E[1],
              p,
              l
            ].concat(W)), typeof Z < "u")
              return Z;
            $ && (h = h.slice(0, -1 * $ * 2), p = p.slice(0, -1 * $), l = l.slice(0, -1 * $)), h.push(this.productions_[E[1]][0]), p.push(z.$), l.push(z._$), Y = w[h[h.length - 2]][h[h.length - 1]], h.push(Y);
            break;
          case 3:
            return !0;
        }
      }
      return !0;
    }
  }, m = function() {
    var f = {
      EOF: 1,
      parseError: function(r, h) {
        if (this.yy.parser)
          this.yy.parser.parseError(r, h);
        else
          throw new Error(r);
      },
      // resets the lexer, sets new input
      setInput: function(i, r) {
        return this.yy = r || this.yy || {}, this._input = i, this._more = this._backtrack = this.done = !1, this.yylineno = this.yyleng = 0, this.yytext = this.matched = this.match = "", this.conditionStack = ["INITIAL"], this.yylloc = {
          first_line: 1,
          first_column: 0,
          last_line: 1,
          last_column: 0
        }, this.options.ranges && (this.yylloc.range = [0, 0]), this.offset = 0, this;
      },
      // consumes and returns one char from the input
      input: function() {
        var i = this._input[0];
        this.yytext += i, this.yyleng++, this.offset++, this.match += i, this.matched += i;
        var r = i.match(/(?:\r\n?|\n).*/g);
        return r ? (this.yylineno++, this.yylloc.last_line++) : this.yylloc.last_column++, this.options.ranges && this.yylloc.range[1]++, this._input = this._input.slice(1), i;
      },
      // unshifts one char (or a string) into the input
      unput: function(i) {
        var r = i.length, h = i.split(/(?:\r\n?|\n)/g);
        this._input = i + this._input, this.yytext = this.yytext.substr(0, this.yytext.length - r), this.offset -= r;
        var d = this.match.split(/(?:\r\n?|\n)/g);
        this.match = this.match.substr(0, this.match.length - 1), this.matched = this.matched.substr(0, this.matched.length - 1), h.length - 1 && (this.yylineno -= h.length - 1);
        var p = this.yylloc.range;
        return this.yylloc = {
          first_line: this.yylloc.first_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.first_column,
          last_column: h ? (h.length === d.length ? this.yylloc.first_column : 0) + d[d.length - h.length].length - h[0].length : this.yylloc.first_column - r
        }, this.options.ranges && (this.yylloc.range = [p[0], p[0] + this.yyleng - r]), this.yyleng = this.yytext.length, this;
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
      less: function(i) {
        this.unput(this.match.slice(i));
      },
      // displays already matched input, i.e. for error messages
      pastInput: function() {
        var i = this.matched.substr(0, this.matched.length - this.match.length);
        return (i.length > 20 ? "..." : "") + i.substr(-20).replace(/\n/g, "");
      },
      // displays upcoming input, i.e. for error messages
      upcomingInput: function() {
        var i = this.match;
        return i.length < 20 && (i += this._input.substr(0, 20 - i.length)), (i.substr(0, 20) + (i.length > 20 ? "..." : "")).replace(/\n/g, "");
      },
      // displays the character position where the lexing error occurred, i.e. for error messages
      showPosition: function() {
        var i = this.pastInput(), r = new Array(i.length + 1).join("-");
        return i + this.upcomingInput() + `
` + r + "^";
      },
      // test the lexed token: return FALSE when not a match, otherwise return token
      test_match: function(i, r) {
        var h, d, p;
        if (this.options.backtrack_lexer && (p = {
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
        }, this.options.ranges && (p.yylloc.range = this.yylloc.range.slice(0))), d = i[0].match(/(?:\r\n?|\n).*/g), d && (this.yylineno += d.length), this.yylloc = {
          first_line: this.yylloc.last_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.last_column,
          last_column: d ? d[d.length - 1].length - d[d.length - 1].match(/\r?\n?/)[0].length : this.yylloc.last_column + i[0].length
        }, this.yytext += i[0], this.match += i[0], this.matches = i, this.yyleng = this.yytext.length, this.options.ranges && (this.yylloc.range = [this.offset, this.offset += this.yyleng]), this._more = !1, this._backtrack = !1, this._input = this._input.slice(i[0].length), this.matched += i[0], h = this.performAction.call(this, this.yy, this, r, this.conditionStack[this.conditionStack.length - 1]), this.done && this._input && (this.done = !1), h)
          return h;
        if (this._backtrack) {
          for (var l in p)
            this[l] = p[l];
          return !1;
        }
        return !1;
      },
      // return next match in input
      next: function() {
        if (this.done)
          return this.EOF;
        this._input || (this.done = !0);
        var i, r, h, d;
        this._more || (this.yytext = "", this.match = "");
        for (var p = this._currentRules(), l = 0; l < p.length; l++)
          if (h = this._input.match(this.rules[p[l]]), h && (!r || h[0].length > r[0].length)) {
            if (r = h, d = l, this.options.backtrack_lexer) {
              if (i = this.test_match(h, p[l]), i !== !1)
                return i;
              if (this._backtrack) {
                r = !1;
                continue;
              } else
                return !1;
            } else if (!this.options.flex)
              break;
          }
        return r ? (i = this.test_match(r, p[d]), i !== !1 ? i : !1) : this._input === "" ? this.EOF : this.parseError("Lexical error on line " + (this.yylineno + 1) + `. Unrecognized text.
` + this.showPosition(), {
          text: "",
          token: null,
          line: this.yylineno
        });
      },
      // return next match that has a token
      lex: function() {
        var r = this.next();
        return r || this.lex();
      },
      // activates a new lexer condition state (pushes the new lexer condition state onto the condition stack)
      begin: function(r) {
        this.conditionStack.push(r);
      },
      // pop the previously active lexer condition state off the condition stack
      popState: function() {
        var r = this.conditionStack.length - 1;
        return r > 0 ? this.conditionStack.pop() : this.conditionStack[0];
      },
      // produce the lexer rule set which is active for the currently active lexer condition state
      _currentRules: function() {
        return this.conditionStack.length && this.conditionStack[this.conditionStack.length - 1] ? this.conditions[this.conditionStack[this.conditionStack.length - 1]].rules : this.conditions.INITIAL.rules;
      },
      // return the currently active lexer condition state; when an index argument is provided it produces the N-th previous condition state, if available
      topState: function(r) {
        return r = this.conditionStack.length - 1 - Math.abs(r || 0), r >= 0 ? this.conditionStack[r] : "INITIAL";
      },
      // alias for begin(condition)
      pushState: function(r) {
        this.begin(r);
      },
      // return the number of states currently on the stack
      stateStackSize: function() {
        return this.conditionStack.length;
      },
      options: { "case-insensitive": !0 },
      performAction: function(r, h, d, p) {
        switch (d) {
          case 0:
            break;
          case 1:
            break;
          case 2:
            return 10;
          case 3:
            break;
          case 4:
            break;
          case 5:
            return 4;
          case 6:
            return 11;
          case 7:
            return this.begin("acc_title"), 12;
          case 8:
            return this.popState(), "acc_title_value";
          case 9:
            return this.begin("acc_descr"), 14;
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
            return 17;
          case 15:
            return 21;
          case 16:
            return 20;
          case 17:
            return 6;
          case 18:
            return "INVALID";
        }
      },
      rules: [/^(?:%(?!\{)[^\n]*)/i, /^(?:[^\}]%%[^\n]*)/i, /^(?:[\n]+)/i, /^(?:\s+)/i, /^(?:#[^\n]*)/i, /^(?:timeline\b)/i, /^(?:title\s[^#\n;]+)/i, /^(?:accTitle\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*\{\s*)/i, /^(?:[\}])/i, /^(?:[^\}]*)/i, /^(?:section\s[^#:\n;]+)/i, /^(?::\s[^#:\n;]+)/i, /^(?:[^#:\n;]+)/i, /^(?:$)/i, /^(?:.)/i],
      conditions: { acc_descr_multiline: { rules: [12, 13], inclusive: !1 }, acc_descr: { rules: [10], inclusive: !1 }, acc_title: { rules: [8], inclusive: !1 }, INITIAL: { rules: [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 14, 15, 16, 17, 18], inclusive: !0 } }
    };
    return f;
  }();
  u.lexer = m;
  function v() {
    this.yy = {};
  }
  return v.prototype = u, u.Parser = v, new v();
}();
K.parser = K;
const vt = K;
let R = "", st = 0;
const Q = [], G = [], V = [], it = () => ft, rt = function() {
  Q.length = 0, G.length = 0, R = "", V.length = 0, gt();
}, at = function(n) {
  R = n, Q.push(n);
}, lt = function() {
  return Q;
}, ot = function() {
  let n = tt();
  const t = 100;
  let e = 0;
  for (; !n && e < t; )
    n = tt(), e++;
  return G.push(...V), G;
}, ct = function(n, t, e) {
  const a = {
    id: st++,
    section: R,
    type: R,
    task: n,
    score: t || 0,
    //if event is defined, then add it the events array
    events: e ? [e] : []
  };
  V.push(a);
}, ht = function(n) {
  V.find((e) => e.id === st - 1).events.push(n);
}, dt = function(n) {
  const t = {
    section: R,
    type: R,
    description: n,
    task: n,
    classes: []
  };
  G.push(t);
}, tt = function() {
  const n = function(e) {
    return V[e].processed;
  };
  let t = !0;
  for (const [e, a] of V.entries())
    n(e), t = t && a.processed;
  return t;
}, wt = {
  clear: rt,
  getCommonDb: it,
  addSection: at,
  getSections: lt,
  getTasks: ot,
  addTask: ct,
  addTaskOrg: dt,
  addEvent: ht
}, St = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  addEvent: ht,
  addSection: at,
  addTask: ct,
  addTaskOrg: dt,
  clear: rt,
  default: wt,
  getCommonDb: it,
  getSections: lt,
  getTasks: ot
}, Symbol.toStringTag, { value: "Module" })), Et = 12, U = function(n, t) {
  const e = n.append("rect");
  return e.attr("x", t.x), e.attr("y", t.y), e.attr("fill", t.fill), e.attr("stroke", t.stroke), e.attr("width", t.width), e.attr("height", t.height), e.attr("rx", t.rx), e.attr("ry", t.ry), t.class !== void 0 && e.attr("class", t.class), e;
}, Tt = function(n, t) {
  const a = n.append("circle").attr("cx", t.cx).attr("cy", t.cy).attr("class", "face").attr("r", 15).attr("stroke-width", 2).attr("overflow", "visible"), s = n.append("g");
  s.append("circle").attr("cx", t.cx - 15 / 3).attr("cy", t.cy - 15 / 3).attr("r", 1.5).attr("stroke-width", 2).attr("fill", "#666").attr("stroke", "#666"), s.append("circle").attr("cx", t.cx + 15 / 3).attr("cy", t.cy - 15 / 3).attr("r", 1.5).attr("stroke-width", 2).attr("fill", "#666").attr("stroke", "#666");
  function c(g) {
    const u = D().startAngle(Math.PI / 2).endAngle(3 * (Math.PI / 2)).innerRadius(7.5).outerRadius(6.8181818181818175);
    g.append("path").attr("class", "mouth").attr("d", u).attr("transform", "translate(" + t.cx + "," + (t.cy + 2) + ")");
  }
  function o(g) {
    const u = D().startAngle(3 * Math.PI / 2).endAngle(5 * (Math.PI / 2)).innerRadius(7.5).outerRadius(6.8181818181818175);
    g.append("path").attr("class", "mouth").attr("d", u).attr("transform", "translate(" + t.cx + "," + (t.cy + 7) + ")");
  }
  function y(g) {
    g.append("line").attr("class", "mouth").attr("stroke", 2).attr("x1", t.cx - 5).attr("y1", t.cy + 7).attr("x2", t.cx + 5).attr("y2", t.cy + 7).attr("class", "mouth").attr("stroke-width", "1px").attr("stroke", "#666");
  }
  return t.score > 3 ? c(s) : t.score < 3 ? o(s) : y(s), a;
}, It = function(n, t) {
  const e = n.append("circle");
  return e.attr("cx", t.cx), e.attr("cy", t.cy), e.attr("class", "actor-" + t.pos), e.attr("fill", t.fill), e.attr("stroke", t.stroke), e.attr("r", t.r), e.class !== void 0 && e.attr("class", e.class), t.title !== void 0 && e.append("title").text(t.title), e;
}, ut = function(n, t) {
  const e = t.text.replace(/<br\s*\/?>/gi, " "), a = n.append("text");
  a.attr("x", t.x), a.attr("y", t.y), a.attr("class", "legend"), a.style("text-anchor", t.anchor), t.class !== void 0 && a.attr("class", t.class);
  const s = a.append("tspan");
  return s.attr("x", t.x + t.textMargin * 2), s.text(e), a;
}, Nt = function(n, t) {
  function e(s, c, o, y, g) {
    return s + "," + c + " " + (s + o) + "," + c + " " + (s + o) + "," + (c + y - g) + " " + (s + o - g * 1.2) + "," + (c + y) + " " + s + "," + (c + y);
  }
  const a = n.append("polygon");
  a.attr("points", e(t.x, t.y, 50, 20, 7)), a.attr("class", "labelBox"), t.y = t.y + t.labelMargin, t.x = t.x + 0.5 * t.labelMargin, ut(n, t);
}, $t = function(n, t, e) {
  const a = n.append("g"), s = X();
  s.x = t.x, s.y = t.y, s.fill = t.fill, s.width = e.width, s.height = e.height, s.class = "journey-section section-type-" + t.num, s.rx = 3, s.ry = 3, U(a, s), pt(e)(
    t.text,
    a,
    s.x,
    s.y,
    s.width,
    s.height,
    { class: "journey-section section-type-" + t.num },
    e,
    t.colour
  );
};
let et = -1;
const Mt = function(n, t, e) {
  const a = t.x + e.width / 2, s = n.append("g");
  et++;
  const c = 300 + 5 * 30;
  s.append("line").attr("id", "task" + et).attr("x1", a).attr("y1", t.y).attr("x2", a).attr("y2", c).attr("class", "task-line").attr("stroke-width", "1px").attr("stroke-dasharray", "4 2").attr("stroke", "#666"), Tt(s, {
    cx: a,
    cy: 300 + (5 - t.score) * 30,
    score: t.score
  });
  const o = X();
  o.x = t.x, o.y = t.y, o.fill = t.fill, o.width = e.width, o.height = e.height, o.class = "task task-type-" + t.num, o.rx = 3, o.ry = 3, U(s, o), t.x + 14, pt(e)(
    t.task,
    s,
    o.x,
    o.y,
    o.width,
    o.height,
    { class: "task" },
    e,
    t.colour
  );
}, Lt = function(n, t) {
  U(n, {
    x: t.startx,
    y: t.starty,
    width: t.stopx - t.startx,
    height: t.stopy - t.starty,
    fill: t.fill,
    class: "rect"
  }).lower();
}, At = function() {
  return {
    x: 0,
    y: 0,
    fill: void 0,
    "text-anchor": "start",
    width: 100,
    height: 100,
    textMargin: 0,
    rx: 0,
    ry: 0
  };
}, X = function() {
  return {
    x: 0,
    y: 0,
    width: 100,
    anchor: "start",
    height: 100,
    rx: 0,
    ry: 0
  };
}, pt = function() {
  function n(s, c, o, y, g, u, m, v) {
    const f = c.append("text").attr("x", o + g / 2).attr("y", y + u / 2 + 5).style("font-color", v).style("text-anchor", "middle").text(s);
    a(f, m);
  }
  function t(s, c, o, y, g, u, m, v, f) {
    const { taskFontSize: i, taskFontFamily: r } = v, h = s.split(/<br\s*\/?>/gi);
    for (let d = 0; d < h.length; d++) {
      const p = d * i - i * (h.length - 1) / 2, l = c.append("text").attr("x", o + g / 2).attr("y", y).attr("fill", f).style("text-anchor", "middle").style("font-size", i).style("font-family", r);
      l.append("tspan").attr("x", o + g / 2).attr("dy", p).text(h[d]), l.attr("y", y + u / 2).attr("dominant-baseline", "central").attr("alignment-baseline", "central"), a(l, m);
    }
  }
  function e(s, c, o, y, g, u, m, v) {
    const f = c.append("switch"), r = f.append("foreignObject").attr("x", o).attr("y", y).attr("width", g).attr("height", u).attr("position", "fixed").append("xhtml:div").style("display", "table").style("height", "100%").style("width", "100%");
    r.append("div").attr("class", "label").style("display", "table-cell").style("text-align", "center").style("vertical-align", "middle").text(s), t(s, f, o, y, g, u, m, v), a(r, m);
  }
  function a(s, c) {
    for (const o in c)
      o in c && s.attr(o, c[o]);
  }
  return function(s) {
    return s.textPlacement === "fo" ? e : s.textPlacement === "old" ? n : t;
  };
}(), Pt = function(n) {
  n.append("defs").append("marker").attr("id", "arrowhead").attr("refX", 5).attr("refY", 2).attr("markerWidth", 6).attr("markerHeight", 4).attr("orient", "auto").append("path").attr("d", "M 0,0 V 4 L6,2 Z");
};
function yt(n, t) {
  n.each(function() {
    var e = j(this), a = e.text().split(/(\s+|<br>)/).reverse(), s, c = [], o = 1.1, y = e.attr("y"), g = parseFloat(e.attr("dy")), u = e.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", g + "em");
    for (let m = 0; m < a.length; m++)
      s = a[a.length - 1 - m], c.push(s), u.text(c.join(" ").trim()), (u.node().getComputedTextLength() > t || s === "<br>") && (c.pop(), u.text(c.join(" ").trim()), s === "<br>" ? c = [""] : c = [s], u = e.append("tspan").attr("x", 0).attr("y", y).attr("dy", o + "em").text(s));
  });
}
const Ht = function(n, t, e, a) {
  const s = e % Et - 1, c = n.append("g");
  t.section = s, c.attr(
    "class",
    (t.class ? t.class + " " : "") + "timeline-node " + ("section-" + s)
  );
  const o = c.append("g"), y = c.append("g"), u = y.append("text").text(t.descr).attr("dy", "1em").attr("alignment-baseline", "middle").attr("dominant-baseline", "middle").attr("text-anchor", "middle").call(yt, t.width).node().getBBox(), m = a.fontSize && a.fontSize.replace ? a.fontSize.replace("px", "") : a.fontSize;
  return t.height = u.height + m * 1.1 * 0.5 + t.padding, t.height = Math.max(t.height, t.maxHeight), t.width = t.width + 2 * t.padding, y.attr("transform", "translate(" + t.width / 2 + ", " + t.padding / 2 + ")"), zt(o, t, s), t;
}, Ct = function(n, t, e) {
  const a = n.append("g"), c = a.append("text").text(t.descr).attr("dy", "1em").attr("alignment-baseline", "middle").attr("dominant-baseline", "middle").attr("text-anchor", "middle").call(yt, t.width).node().getBBox(), o = e.fontSize && e.fontSize.replace ? e.fontSize.replace("px", "") : e.fontSize;
  return a.remove(), c.height + o * 1.1 * 0.5 + t.padding;
}, zt = function(n, t, e) {
  n.append("path").attr("id", "node-" + t.id).attr("class", "node-bkg node-" + t.type).attr(
    "d",
    `M0 ${t.height - 5} v${-t.height + 2 * 5} q0,-5 5,-5 h${t.width - 2 * 5} q5,0 5,5 v${t.height - 5} H0 Z`
  ), n.append("line").attr("class", "node-line-" + e).attr("x1", 0).attr("y1", t.height).attr("x2", t.width).attr("y2", t.height);
}, H = {
  drawRect: U,
  drawCircle: It,
  drawSection: $t,
  drawText: ut,
  drawLabel: Nt,
  drawTask: Mt,
  drawBackgroundRect: Lt,
  getTextObj: At,
  getNoteRect: X,
  initGraphics: Pt,
  drawNode: Ht,
  getVirtualNodeHeight: Ct
}, Rt = function(n, t, e, a) {
  var W, b;
  const s = mt(), c = s.leftMargin ?? 50;
  T.debug("timeline", a.db);
  const o = s.securityLevel;
  let y;
  o === "sandbox" && (y = j("#i" + t));
  const u = (o === "sandbox" ? j(y.nodes()[0].contentDocument.body) : j("body")).select("#" + t);
  u.append("g");
  const m = a.db.getTasks(), v = a.db.getCommonDb().getDiagramTitle();
  T.debug("task", m), H.initGraphics(u);
  const f = a.db.getSections();
  T.debug("sections", f);
  let i = 0, r = 0, h = 0, d = 0, p = 50 + c, l = 50;
  d = 50;
  let w = 0, x = !0;
  f.forEach(function(S) {
    const _ = {
      number: w,
      descr: S,
      section: w,
      width: 150,
      padding: 20,
      maxHeight: i
    }, I = H.getVirtualNodeHeight(u, _, s);
    T.debug("sectionHeight before draw", I), i = Math.max(i, I + 20);
  });
  let N = 0, A = 0;
  T.debug("tasks.length", m.length);
  for (const [S, _] of m.entries()) {
    const I = {
      number: S,
      descr: _,
      section: _.section,
      width: 150,
      padding: 20,
      maxHeight: r
    }, P = H.getVirtualNodeHeight(u, I, s);
    T.debug("taskHeight before draw", P), r = Math.max(r, P + 20), N = Math.max(N, _.events.length);
    let C = 0;
    for (let k = 0; k < _.events.length; k++) {
      const E = {
        descr: _.events[k],
        section: _.section,
        number: _.section,
        width: 150,
        padding: 20,
        maxHeight: 50
      };
      C += H.getVirtualNodeHeight(u, E, s);
    }
    A = Math.max(A, C);
  }
  T.debug("maxSectionHeight before draw", i), T.debug("maxTaskHeight before draw", r), f && f.length > 0 ? f.forEach((S) => {
    const _ = m.filter((k) => k.section === S), I = {
      number: w,
      descr: S,
      section: w,
      width: 200 * Math.max(_.length, 1) - 50,
      padding: 20,
      maxHeight: i
    };
    T.debug("sectionNode", I);
    const P = u.append("g"), C = H.drawNode(P, I, w, s);
    T.debug("sectionNode output", C), P.attr("transform", `translate(${p}, ${d})`), l += i + 50, _.length > 0 && nt(
      u,
      _,
      w,
      p,
      l,
      r,
      s,
      N,
      A,
      i,
      !1
    ), p += 200 * Math.max(_.length, 1), l = d, w++;
  }) : (x = !1, nt(
    u,
    m,
    w,
    p,
    l,
    r,
    s,
    N,
    A,
    i,
    !0
  ));
  const F = u.node().getBBox();
  T.debug("bounds", F), v && u.append("text").text(v).attr("x", F.width / 2 - c).attr("font-size", "4ex").attr("font-weight", "bold").attr("y", 20), h = x ? i + r + 150 : r + 100, u.append("g").attr("class", "lineWrapper").append("line").attr("x1", c).attr("y1", h).attr("x2", F.width + 3 * c).attr("y2", h).attr("stroke-width", 4).attr("stroke", "black").attr("marker-end", "url(#arrowhead)"), xt(
    void 0,
    u,
    ((W = s.timeline) == null ? void 0 : W.padding) ?? 50,
    ((b = s.timeline) == null ? void 0 : b.useMaxWidth) ?? !1
  );
}, nt = function(n, t, e, a, s, c, o, y, g, u, m) {
  var v;
  for (const f of t) {
    const i = {
      descr: f.task,
      section: e,
      number: e,
      width: 150,
      padding: 20,
      maxHeight: c
    };
    T.debug("taskNode", i);
    const r = n.append("g").attr("class", "taskWrapper"), d = H.drawNode(r, i, e, o).height;
    if (T.debug("taskHeight after draw", d), r.attr("transform", `translate(${a}, ${s})`), c = Math.max(c, d), f.events) {
      const p = n.append("g").attr("class", "lineWrapper");
      let l = c;
      s += 100, l = l + Vt(n, f.events, e, a, s, o), s -= 100, p.append("line").attr("x1", a + 190 / 2).attr("y1", s + c).attr("x2", a + 190 / 2).attr(
        "y2",
        s + c + (m ? c : u) + g + 120
      ).attr("stroke-width", 2).attr("stroke", "black").attr("marker-end", "url(#arrowhead)").attr("stroke-dasharray", "5,5");
    }
    a = a + 200, m && !((v = o.timeline) != null && v.disableMulticolor) && e++;
  }
  s = s - 10;
}, Vt = function(n, t, e, a, s, c) {
  let o = 0;
  const y = s;
  s = s + 100;
  for (const g of t) {
    const u = {
      descr: g,
      section: e,
      number: e,
      width: 150,
      padding: 20,
      maxHeight: 50
    };
    T.debug("eventNode", u);
    const m = n.append("g").attr("class", "eventWrapper"), f = H.drawNode(m, u, e, c).height;
    o = o + f, m.attr("transform", `translate(${a}, ${s})`), s = s + 10 + f;
  }
  return s = y, o;
}, Ft = {
  setConf: () => {
  },
  draw: Rt
}, Wt = (n) => {
  let t = "";
  for (let e = 0; e < n.THEME_COLOR_LIMIT; e++)
    n["lineColor" + e] = n["lineColor" + e] || n["cScaleInv" + e], bt(n["lineColor" + e]) ? n["lineColor" + e] = kt(n["lineColor" + e], 20) : n["lineColor" + e] = _t(n["lineColor" + e], 20);
  for (let e = 0; e < n.THEME_COLOR_LIMIT; e++) {
    const a = "" + (17 - 3 * e);
    t += `
    .section-${e - 1} rect, .section-${e - 1} path, .section-${e - 1} circle, .section-${e - 1} path  {
      fill: ${n["cScale" + e]};
    }
    .section-${e - 1} text {
     fill: ${n["cScaleLabel" + e]};
    }
    .node-icon-${e - 1} {
      font-size: 40px;
      color: ${n["cScaleLabel" + e]};
    }
    .section-edge-${e - 1}{
      stroke: ${n["cScale" + e]};
    }
    .edge-depth-${e - 1}{
      stroke-width: ${a};
    }
    .section-${e - 1} line {
      stroke: ${n["cScaleInv" + e]} ;
      stroke-width: 3;
    }

    .lineWrapper line{
      stroke: ${n["cScaleLabel" + e]} ;
    }

    .disabled, .disabled circle, .disabled text {
      fill: lightgray;
    }
    .disabled text {
      fill: #efefef;
    }
    `;
  }
  return t;
}, Bt = (n) => `
  .edge {
    stroke-width: 3;
  }
  ${Wt(n)}
  .section-root rect, .section-root path, .section-root circle  {
    fill: ${n.git0};
  }
  .section-root text {
    fill: ${n.gitBranchLabel0};
  }
  .icon-container {
    height:100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .edge {
    fill: none;
  }
  .eventWrapper  {
   filter: brightness(120%);
  }
`, Ot = Bt, qt = {
  db: St,
  renderer: Ft,
  parser: vt,
  styles: Ot
};
export {
  qt as diagram
};
