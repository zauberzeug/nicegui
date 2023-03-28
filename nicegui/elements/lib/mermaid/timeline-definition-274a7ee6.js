import { p as bt } from "./utils-aa888deb.js";
import { c as kt, f as vt } from "./commonDb-4dc3d465.js";
import { f as Z, g as wt, l as T, K as St, L as Et } from "./config-e567ef17.js";
import { d as it } from "./arc-1bd4335b.js";
import { s as Tt } from "./setupGraphViewbox-a4603a92.js";
import { i as It } from "./is_dark-151801f4.js";
import "./constant-2fe7eae5.js";
var Y = function() {
  var n = function(k, r, a, h) {
    for (a = a || {}, h = k.length; h--; a[k[h]] = r)
      ;
    return a;
  }, t = [1, 2], e = [1, 5], s = [6, 9, 11, 17, 18, 20, 22, 23, 26, 27, 28], i = [1, 15], l = [1, 16], o = [1, 17], y = [1, 18], g = [1, 19], d = [1, 23], m = [1, 24], S = [1, 27], _ = [4, 6, 9, 11, 17, 18, 20, 22, 23, 26, 27, 28], b = {
    trace: function() {
    },
    yy: {},
    symbols_: { error: 2, start: 3, timeline: 4, document: 5, EOF: 6, directive: 7, line: 8, SPACE: 9, statement: 10, NEWLINE: 11, openDirective: 12, typeDirective: 13, closeDirective: 14, ":": 15, argDirective: 16, title: 17, acc_title: 18, acc_title_value: 19, acc_descr: 20, acc_descr_value: 21, acc_descr_multiline_value: 22, section: 23, period_statement: 24, event_statement: 25, period: 26, event: 27, open_directive: 28, type_directive: 29, arg_directive: 30, close_directive: 31, $accept: 0, $end: 1 },
    terminals_: { 2: "error", 4: "timeline", 6: "EOF", 9: "SPACE", 11: "NEWLINE", 15: ":", 17: "title", 18: "acc_title", 19: "acc_title_value", 20: "acc_descr", 21: "acc_descr_value", 22: "acc_descr_multiline_value", 23: "section", 26: "period", 27: "event", 28: "open_directive", 29: "type_directive", 30: "arg_directive", 31: "close_directive" },
    productions_: [0, [3, 3], [3, 2], [5, 0], [5, 2], [8, 2], [8, 1], [8, 1], [8, 1], [7, 4], [7, 6], [10, 1], [10, 2], [10, 2], [10, 1], [10, 1], [10, 1], [10, 1], [10, 1], [24, 1], [25, 1], [12, 1], [13, 1], [16, 1], [14, 1]],
    performAction: function(r, a, h, u, f, c, L) {
      var x = c.length - 1;
      switch (f) {
        case 1:
          return c[x - 1];
        case 3:
          this.$ = [];
          break;
        case 4:
          c[x - 1].push(c[x]), this.$ = c[x - 1];
          break;
        case 5:
        case 6:
          this.$ = c[x];
          break;
        case 7:
        case 8:
          this.$ = [];
          break;
        case 11:
          u.getCommonDb().setDiagramTitle(c[x].substr(6)), this.$ = c[x].substr(6);
          break;
        case 12:
          this.$ = c[x].trim(), u.getCommonDb().setAccTitle(this.$);
          break;
        case 13:
        case 14:
          this.$ = c[x].trim(), u.getCommonDb().setAccDescription(this.$);
          break;
        case 15:
          u.addSection(c[x].substr(8)), this.$ = c[x].substr(8);
          break;
        case 19:
          u.addTask(c[x], 0, ""), this.$ = c[x];
          break;
        case 20:
          u.addEvent(c[x].substr(2)), this.$ = c[x];
          break;
        case 21:
          u.parseDirective("%%{", "open_directive");
          break;
        case 22:
          u.parseDirective(c[x], "type_directive");
          break;
        case 23:
          c[x] = c[x].trim().replace(/'/g, '"'), u.parseDirective(c[x], "arg_directive");
          break;
        case 24:
          u.parseDirective("}%%", "close_directive", "timeline");
          break;
      }
    },
    table: [{ 3: 1, 4: t, 7: 3, 12: 4, 28: e }, { 1: [3] }, n(s, [2, 3], { 5: 6 }), { 3: 7, 4: t, 7: 3, 12: 4, 28: e }, { 13: 8, 29: [1, 9] }, { 29: [2, 21] }, { 6: [1, 10], 7: 22, 8: 11, 9: [1, 12], 10: 13, 11: [1, 14], 12: 4, 17: i, 18: l, 20: o, 22: y, 23: g, 24: 20, 25: 21, 26: d, 27: m, 28: e }, { 1: [2, 2] }, { 14: 25, 15: [1, 26], 31: S }, n([15, 31], [2, 22]), n(s, [2, 8], { 1: [2, 1] }), n(s, [2, 4]), { 7: 22, 10: 28, 12: 4, 17: i, 18: l, 20: o, 22: y, 23: g, 24: 20, 25: 21, 26: d, 27: m, 28: e }, n(s, [2, 6]), n(s, [2, 7]), n(s, [2, 11]), { 19: [1, 29] }, { 21: [1, 30] }, n(s, [2, 14]), n(s, [2, 15]), n(s, [2, 16]), n(s, [2, 17]), n(s, [2, 18]), n(s, [2, 19]), n(s, [2, 20]), { 11: [1, 31] }, { 16: 32, 30: [1, 33] }, { 11: [2, 24] }, n(s, [2, 5]), n(s, [2, 12]), n(s, [2, 13]), n(_, [2, 9]), { 14: 34, 31: S }, { 31: [2, 23] }, { 11: [1, 35] }, n(_, [2, 10])],
    defaultActions: { 5: [2, 21], 7: [2, 2], 27: [2, 24], 33: [2, 23] },
    parseError: function(r, a) {
      if (a.recoverable)
        this.trace(r);
      else {
        var h = new Error(r);
        throw h.hash = a, h;
      }
    },
    parse: function(r) {
      var a = this, h = [0], u = [], f = [null], c = [], L = this.table, x = "", C = 0, O = 0, G = 2, j = 1, P = c.slice.call(arguments, 1), p = Object.create(this.lexer), E = { yy: {} };
      for (var M in this.yy)
        Object.prototype.hasOwnProperty.call(this.yy, M) && (E.yy[M] = this.yy[M]);
      p.setInput(r, E.yy), E.yy.lexer = p, E.yy.parser = this, typeof p.yylloc > "u" && (p.yylloc = {});
      var H = p.yylloc;
      c.push(H);
      var V = p.options && p.options.ranges;
      typeof E.yy.parseError == "function" ? this.parseError = E.yy.parseError : this.parseError = Object.getPrototypeOf(this).parseError;
      function et() {
        var A;
        return A = u.pop() || p.lex() || j, typeof A != "number" && (A instanceof Array && (u = A, A = u.pop()), A = a.symbols_[A] || A), A;
      }
      for (var w, z, N, Q, F = {}, q, $, nt, U; ; ) {
        if (z = h[h.length - 1], this.defaultActions[z] ? N = this.defaultActions[z] : ((w === null || typeof w > "u") && (w = et()), N = L[z] && L[z][w]), typeof N > "u" || !N.length || !N[0]) {
          var X = "";
          U = [];
          for (q in L[z])
            this.terminals_[q] && q > G && U.push("'" + this.terminals_[q] + "'");
          p.showPosition ? X = "Parse error on line " + (C + 1) + `:
` + p.showPosition() + `
Expecting ` + U.join(", ") + ", got '" + (this.terminals_[w] || w) + "'" : X = "Parse error on line " + (C + 1) + ": Unexpected " + (w == j ? "end of input" : "'" + (this.terminals_[w] || w) + "'"), this.parseError(X, {
            text: p.match,
            token: this.terminals_[w] || w,
            line: p.yylineno,
            loc: H,
            expected: U
          });
        }
        if (N[0] instanceof Array && N.length > 1)
          throw new Error("Parse Error: multiple actions possible at state: " + z + ", token: " + w);
        switch (N[0]) {
          case 1:
            h.push(w), f.push(p.yytext), c.push(p.yylloc), h.push(N[1]), w = null, O = p.yyleng, x = p.yytext, C = p.yylineno, H = p.yylloc;
            break;
          case 2:
            if ($ = this.productions_[N[1]][1], F.$ = f[f.length - $], F._$ = {
              first_line: c[c.length - ($ || 1)].first_line,
              last_line: c[c.length - 1].last_line,
              first_column: c[c.length - ($ || 1)].first_column,
              last_column: c[c.length - 1].last_column
            }, V && (F._$.range = [
              c[c.length - ($ || 1)].range[0],
              c[c.length - 1].range[1]
            ]), Q = this.performAction.apply(F, [
              x,
              O,
              C,
              E.yy,
              N[1],
              f,
              c
            ].concat(P)), typeof Q < "u")
              return Q;
            $ && (h = h.slice(0, -1 * $ * 2), f = f.slice(0, -1 * $), c = c.slice(0, -1 * $)), h.push(this.productions_[N[1]][0]), f.push(F.$), c.push(F._$), nt = L[h[h.length - 2]][h[h.length - 1]], h.push(nt);
            break;
          case 3:
            return !0;
        }
      }
      return !0;
    }
  }, v = function() {
    var k = {
      EOF: 1,
      parseError: function(a, h) {
        if (this.yy.parser)
          this.yy.parser.parseError(a, h);
        else
          throw new Error(a);
      },
      // resets the lexer, sets new input
      setInput: function(r, a) {
        return this.yy = a || this.yy || {}, this._input = r, this._more = this._backtrack = this.done = !1, this.yylineno = this.yyleng = 0, this.yytext = this.matched = this.match = "", this.conditionStack = ["INITIAL"], this.yylloc = {
          first_line: 1,
          first_column: 0,
          last_line: 1,
          last_column: 0
        }, this.options.ranges && (this.yylloc.range = [0, 0]), this.offset = 0, this;
      },
      // consumes and returns one char from the input
      input: function() {
        var r = this._input[0];
        this.yytext += r, this.yyleng++, this.offset++, this.match += r, this.matched += r;
        var a = r.match(/(?:\r\n?|\n).*/g);
        return a ? (this.yylineno++, this.yylloc.last_line++) : this.yylloc.last_column++, this.options.ranges && this.yylloc.range[1]++, this._input = this._input.slice(1), r;
      },
      // unshifts one char (or a string) into the input
      unput: function(r) {
        var a = r.length, h = r.split(/(?:\r\n?|\n)/g);
        this._input = r + this._input, this.yytext = this.yytext.substr(0, this.yytext.length - a), this.offset -= a;
        var u = this.match.split(/(?:\r\n?|\n)/g);
        this.match = this.match.substr(0, this.match.length - 1), this.matched = this.matched.substr(0, this.matched.length - 1), h.length - 1 && (this.yylineno -= h.length - 1);
        var f = this.yylloc.range;
        return this.yylloc = {
          first_line: this.yylloc.first_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.first_column,
          last_column: h ? (h.length === u.length ? this.yylloc.first_column : 0) + u[u.length - h.length].length - h[0].length : this.yylloc.first_column - a
        }, this.options.ranges && (this.yylloc.range = [f[0], f[0] + this.yyleng - a]), this.yyleng = this.yytext.length, this;
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
      less: function(r) {
        this.unput(this.match.slice(r));
      },
      // displays already matched input, i.e. for error messages
      pastInput: function() {
        var r = this.matched.substr(0, this.matched.length - this.match.length);
        return (r.length > 20 ? "..." : "") + r.substr(-20).replace(/\n/g, "");
      },
      // displays upcoming input, i.e. for error messages
      upcomingInput: function() {
        var r = this.match;
        return r.length < 20 && (r += this._input.substr(0, 20 - r.length)), (r.substr(0, 20) + (r.length > 20 ? "..." : "")).replace(/\n/g, "");
      },
      // displays the character position where the lexing error occurred, i.e. for error messages
      showPosition: function() {
        var r = this.pastInput(), a = new Array(r.length + 1).join("-");
        return r + this.upcomingInput() + `
` + a + "^";
      },
      // test the lexed token: return FALSE when not a match, otherwise return token
      test_match: function(r, a) {
        var h, u, f;
        if (this.options.backtrack_lexer && (f = {
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
        }, this.options.ranges && (f.yylloc.range = this.yylloc.range.slice(0))), u = r[0].match(/(?:\r\n?|\n).*/g), u && (this.yylineno += u.length), this.yylloc = {
          first_line: this.yylloc.last_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.last_column,
          last_column: u ? u[u.length - 1].length - u[u.length - 1].match(/\r?\n?/)[0].length : this.yylloc.last_column + r[0].length
        }, this.yytext += r[0], this.match += r[0], this.matches = r, this.yyleng = this.yytext.length, this.options.ranges && (this.yylloc.range = [this.offset, this.offset += this.yyleng]), this._more = !1, this._backtrack = !1, this._input = this._input.slice(r[0].length), this.matched += r[0], h = this.performAction.call(this, this.yy, this, a, this.conditionStack[this.conditionStack.length - 1]), this.done && this._input && (this.done = !1), h)
          return h;
        if (this._backtrack) {
          for (var c in f)
            this[c] = f[c];
          return !1;
        }
        return !1;
      },
      // return next match in input
      next: function() {
        if (this.done)
          return this.EOF;
        this._input || (this.done = !0);
        var r, a, h, u;
        this._more || (this.yytext = "", this.match = "");
        for (var f = this._currentRules(), c = 0; c < f.length; c++)
          if (h = this._input.match(this.rules[f[c]]), h && (!a || h[0].length > a[0].length)) {
            if (a = h, u = c, this.options.backtrack_lexer) {
              if (r = this.test_match(h, f[c]), r !== !1)
                return r;
              if (this._backtrack) {
                a = !1;
                continue;
              } else
                return !1;
            } else if (!this.options.flex)
              break;
          }
        return a ? (r = this.test_match(a, f[u]), r !== !1 ? r : !1) : this._input === "" ? this.EOF : this.parseError("Lexical error on line " + (this.yylineno + 1) + `. Unrecognized text.
` + this.showPosition(), {
          text: "",
          token: null,
          line: this.yylineno
        });
      },
      // return next match that has a token
      lex: function() {
        var a = this.next();
        return a || this.lex();
      },
      // activates a new lexer condition state (pushes the new lexer condition state onto the condition stack)
      begin: function(a) {
        this.conditionStack.push(a);
      },
      // pop the previously active lexer condition state off the condition stack
      popState: function() {
        var a = this.conditionStack.length - 1;
        return a > 0 ? this.conditionStack.pop() : this.conditionStack[0];
      },
      // produce the lexer rule set which is active for the currently active lexer condition state
      _currentRules: function() {
        return this.conditionStack.length && this.conditionStack[this.conditionStack.length - 1] ? this.conditions[this.conditionStack[this.conditionStack.length - 1]].rules : this.conditions.INITIAL.rules;
      },
      // return the currently active lexer condition state; when an index argument is provided it produces the N-th previous condition state, if available
      topState: function(a) {
        return a = this.conditionStack.length - 1 - Math.abs(a || 0), a >= 0 ? this.conditionStack[a] : "INITIAL";
      },
      // alias for begin(condition)
      pushState: function(a) {
        this.begin(a);
      },
      // return the number of states currently on the stack
      stateStackSize: function() {
        return this.conditionStack.length;
      },
      options: { "case-insensitive": !0 },
      performAction: function(a, h, u, f) {
        switch (u) {
          case 0:
            return this.begin("open_directive"), 28;
          case 1:
            return this.begin("type_directive"), 29;
          case 2:
            return this.popState(), this.begin("arg_directive"), 15;
          case 3:
            return this.popState(), this.popState(), 31;
          case 4:
            return 30;
          case 5:
            break;
          case 6:
            break;
          case 7:
            return 11;
          case 8:
            break;
          case 9:
            break;
          case 10:
            return 4;
          case 11:
            return 17;
          case 12:
            return this.begin("acc_title"), 18;
          case 13:
            return this.popState(), "acc_title_value";
          case 14:
            return this.begin("acc_descr"), 20;
          case 15:
            return this.popState(), "acc_descr_value";
          case 16:
            this.begin("acc_descr_multiline");
            break;
          case 17:
            this.popState();
            break;
          case 18:
            return "acc_descr_multiline_value";
          case 19:
            return 23;
          case 20:
            return 27;
          case 21:
            return 26;
          case 22:
            return 6;
          case 23:
            return "INVALID";
        }
      },
      rules: [/^(?:%%\{)/i, /^(?:((?:(?!\}%%)[^:.])*))/i, /^(?::)/i, /^(?:\}%%)/i, /^(?:((?:(?!\}%%).|\n)*))/i, /^(?:%(?!\{)[^\n]*)/i, /^(?:[^\}]%%[^\n]*)/i, /^(?:[\n]+)/i, /^(?:\s+)/i, /^(?:#[^\n]*)/i, /^(?:timeline\b)/i, /^(?:title\s[^#\n;]+)/i, /^(?:accTitle\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*\{\s*)/i, /^(?:[\}])/i, /^(?:[^\}]*)/i, /^(?:section\s[^#:\n;]+)/i, /^(?::\s[^#:\n;]+)/i, /^(?:[^#:\n;]+)/i, /^(?:$)/i, /^(?:.)/i],
      conditions: { open_directive: { rules: [1], inclusive: !1 }, type_directive: { rules: [2, 3], inclusive: !1 }, arg_directive: { rules: [3, 4], inclusive: !1 }, acc_descr_multiline: { rules: [17, 18], inclusive: !1 }, acc_descr: { rules: [15], inclusive: !1 }, acc_title: { rules: [13], inclusive: !1 }, INITIAL: { rules: [0, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 19, 20, 21, 22, 23], inclusive: !0 } }
    };
    return k;
  }();
  b.lexer = v;
  function I() {
    this.yy = {};
  }
  return I.prototype = b, b.Parser = I, new I();
}();
Y.parser = Y;
const Nt = Y;
let W = "", ct = 0;
const D = [], K = [], B = [], ot = () => kt, lt = (n, t, e) => {
  bt(globalThis, n, t, e);
}, ht = function() {
  D.length = 0, K.length = 0, W = "", B.length = 0, vt();
}, dt = function(n) {
  W = n, D.push(n);
}, ut = function() {
  return D;
}, pt = function() {
  let n = st();
  const t = 100;
  let e = 0;
  for (; !n && e < t; )
    n = st(), e++;
  return K.push(...B), K;
}, yt = function(n, t, e) {
  const s = {
    id: ct++,
    section: W,
    type: W,
    task: n,
    score: t || 0,
    //if event is defined, then add it the events array
    events: e ? [e] : []
  };
  B.push(s);
}, ft = function(n) {
  B.find((e) => e.id === ct - 1).events.push(n);
}, gt = function(n) {
  const t = {
    section: W,
    type: W,
    description: n,
    task: n,
    classes: []
  };
  K.push(t);
}, st = function() {
  const n = function(e) {
    return B[e].processed;
  };
  let t = !0;
  for (const [e, s] of B.entries())
    n(e), t = t && s.processed;
  return t;
}, Lt = {
  clear: ht,
  getCommonDb: ot,
  addSection: dt,
  getSections: ut,
  getTasks: pt,
  addTask: yt,
  addTaskOrg: gt,
  addEvent: ft,
  parseDirective: lt
}, Mt = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  addEvent: ft,
  addSection: dt,
  addTask: yt,
  addTaskOrg: gt,
  clear: ht,
  default: Lt,
  getCommonDb: ot,
  getSections: ut,
  getTasks: pt,
  parseDirective: lt
}, Symbol.toStringTag, { value: "Module" })), $t = 12, J = function(n, t) {
  const e = n.append("rect");
  return e.attr("x", t.x), e.attr("y", t.y), e.attr("fill", t.fill), e.attr("stroke", t.stroke), e.attr("width", t.width), e.attr("height", t.height), e.attr("rx", t.rx), e.attr("ry", t.ry), t.class !== void 0 && e.attr("class", t.class), e;
}, At = function(n, t) {
  const s = n.append("circle").attr("cx", t.cx).attr("cy", t.cy).attr("class", "face").attr("r", 15).attr("stroke-width", 2).attr("overflow", "visible"), i = n.append("g");
  i.append("circle").attr("cx", t.cx - 15 / 3).attr("cy", t.cy - 15 / 3).attr("r", 1.5).attr("stroke-width", 2).attr("fill", "#666").attr("stroke", "#666"), i.append("circle").attr("cx", t.cx + 15 / 3).attr("cy", t.cy - 15 / 3).attr("r", 1.5).attr("stroke-width", 2).attr("fill", "#666").attr("stroke", "#666");
  function l(g) {
    const d = it().startAngle(Math.PI / 2).endAngle(3 * (Math.PI / 2)).innerRadius(7.5).outerRadius(6.8181818181818175);
    g.append("path").attr("class", "mouth").attr("d", d).attr("transform", "translate(" + t.cx + "," + (t.cy + 2) + ")");
  }
  function o(g) {
    const d = it().startAngle(3 * Math.PI / 2).endAngle(5 * (Math.PI / 2)).innerRadius(7.5).outerRadius(6.8181818181818175);
    g.append("path").attr("class", "mouth").attr("d", d).attr("transform", "translate(" + t.cx + "," + (t.cy + 7) + ")");
  }
  function y(g) {
    g.append("line").attr("class", "mouth").attr("stroke", 2).attr("x1", t.cx - 5).attr("y1", t.cy + 7).attr("x2", t.cx + 5).attr("y2", t.cy + 7).attr("class", "mouth").attr("stroke-width", "1px").attr("stroke", "#666");
  }
  return t.score > 3 ? l(i) : t.score < 3 ? o(i) : y(i), s;
}, Pt = function(n, t) {
  const e = n.append("circle");
  return e.attr("cx", t.cx), e.attr("cy", t.cy), e.attr("class", "actor-" + t.pos), e.attr("fill", t.fill), e.attr("stroke", t.stroke), e.attr("r", t.r), e.class !== void 0 && e.attr("class", e.class), t.title !== void 0 && e.append("title").text(t.title), e;
}, mt = function(n, t) {
  const e = t.text.replace(/<br\s*\/?>/gi, " "), s = n.append("text");
  s.attr("x", t.x), s.attr("y", t.y), s.attr("class", "legend"), s.style("text-anchor", t.anchor), t.class !== void 0 && s.attr("class", t.class);
  const i = s.append("tspan");
  return i.attr("x", t.x + t.textMargin * 2), i.text(e), s;
}, Ht = function(n, t) {
  function e(i, l, o, y, g) {
    return i + "," + l + " " + (i + o) + "," + l + " " + (i + o) + "," + (l + y - g) + " " + (i + o - g * 1.2) + "," + (l + y) + " " + i + "," + (l + y);
  }
  const s = n.append("polygon");
  s.attr("points", e(t.x, t.y, 50, 20, 7)), s.attr("class", "labelBox"), t.y = t.y + t.labelMargin, t.x = t.x + 0.5 * t.labelMargin, mt(n, t);
}, Ct = function(n, t, e) {
  const s = n.append("g"), i = tt();
  i.x = t.x, i.y = t.y, i.fill = t.fill, i.width = e.width, i.height = e.height, i.class = "journey-section section-type-" + t.num, i.rx = 3, i.ry = 3, J(s, i), xt(e)(
    t.text,
    s,
    i.x,
    i.y,
    i.width,
    i.height,
    { class: "journey-section section-type-" + t.num },
    e,
    t.colour
  );
};
let rt = -1;
const Vt = function(n, t, e) {
  const s = t.x + e.width / 2, i = n.append("g");
  rt++;
  const l = 300 + 5 * 30;
  i.append("line").attr("id", "task" + rt).attr("x1", s).attr("y1", t.y).attr("x2", s).attr("y2", l).attr("class", "task-line").attr("stroke-width", "1px").attr("stroke-dasharray", "4 2").attr("stroke", "#666"), At(i, {
    cx: s,
    cy: 300 + (5 - t.score) * 30,
    score: t.score
  });
  const o = tt();
  o.x = t.x, o.y = t.y, o.fill = t.fill, o.width = e.width, o.height = e.height, o.class = "task task-type-" + t.num, o.rx = 3, o.ry = 3, J(i, o), t.x + 14, xt(e)(
    t.task,
    i,
    o.x,
    o.y,
    o.width,
    o.height,
    { class: "task" },
    e,
    t.colour
  );
}, zt = function(n, t) {
  J(n, {
    x: t.startx,
    y: t.starty,
    width: t.stopx - t.startx,
    height: t.stopy - t.starty,
    fill: t.fill,
    class: "rect"
  }).lower();
}, Rt = function() {
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
}, tt = function() {
  return {
    x: 0,
    y: 0,
    width: 100,
    anchor: "start",
    height: 100,
    rx: 0,
    ry: 0
  };
}, xt = function() {
  function n(i, l, o, y, g, d, m, S) {
    const _ = l.append("text").attr("x", o + g / 2).attr("y", y + d / 2 + 5).style("font-color", S).style("text-anchor", "middle").text(i);
    s(_, m);
  }
  function t(i, l, o, y, g, d, m, S, _) {
    const { taskFontSize: b, taskFontFamily: v } = S, I = i.split(/<br\s*\/?>/gi);
    for (let k = 0; k < I.length; k++) {
      const r = k * b - b * (I.length - 1) / 2, a = l.append("text").attr("x", o + g / 2).attr("y", y).attr("fill", _).style("text-anchor", "middle").style("font-size", b).style("font-family", v);
      a.append("tspan").attr("x", o + g / 2).attr("dy", r).text(I[k]), a.attr("y", y + d / 2).attr("dominant-baseline", "central").attr("alignment-baseline", "central"), s(a, m);
    }
  }
  function e(i, l, o, y, g, d, m, S) {
    const _ = l.append("switch"), v = _.append("foreignObject").attr("x", o).attr("y", y).attr("width", g).attr("height", d).attr("position", "fixed").append("xhtml:div").style("display", "table").style("height", "100%").style("width", "100%");
    v.append("div").attr("class", "label").style("display", "table-cell").style("text-align", "center").style("vertical-align", "middle").text(i), t(i, _, o, y, g, d, m, S), s(v, m);
  }
  function s(i, l) {
    for (const o in l)
      o in l && i.attr(o, l[o]);
  }
  return function(i) {
    return i.textPlacement === "fo" ? e : i.textPlacement === "old" ? n : t;
  };
}(), Ft = function(n) {
  n.append("defs").append("marker").attr("id", "arrowhead").attr("refX", 5).attr("refY", 2).attr("markerWidth", 6).attr("markerHeight", 4).attr("orient", "auto").append("path").attr("d", "M 0,0 V 4 L6,2 Z");
};
function _t(n, t) {
  n.each(function() {
    var e = Z(this), s = e.text().split(/(\s+|<br>)/).reverse(), i, l = [], o = 1.1, y = e.attr("y"), g = parseFloat(e.attr("dy")), d = e.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", g + "em");
    for (let m = 0; m < s.length; m++)
      i = s[s.length - 1 - m], l.push(i), d.text(l.join(" ").trim()), (d.node().getComputedTextLength() > t || i === "<br>") && (l.pop(), d.text(l.join(" ").trim()), i === "<br>" ? l = [""] : l = [i], d = e.append("tspan").attr("x", 0).attr("y", y).attr("dy", o + "em").text(i));
  });
}
const Wt = function(n, t, e, s) {
  const i = e % $t - 1, l = n.append("g");
  t.section = i, l.attr(
    "class",
    (t.class ? t.class + " " : "") + "timeline-node " + ("section-" + i)
  );
  const o = l.append("g"), y = l.append("g"), d = y.append("text").text(t.descr).attr("dy", "1em").attr("alignment-baseline", "middle").attr("dominant-baseline", "middle").attr("text-anchor", "middle").call(_t, t.width).node().getBBox(), m = s.fontSize && s.fontSize.replace ? s.fontSize.replace("px", "") : s.fontSize;
  return t.height = d.height + m * 1.1 * 0.5 + t.padding, t.height = Math.max(t.height, t.maxHeight), t.width = t.width + 2 * t.padding, y.attr("transform", "translate(" + t.width / 2 + ", " + t.padding / 2 + ")"), Ot(o, t, i), t;
}, Bt = function(n, t, e) {
  const s = n.append("g"), l = s.append("text").text(t.descr).attr("dy", "1em").attr("alignment-baseline", "middle").attr("dominant-baseline", "middle").attr("text-anchor", "middle").call(_t, t.width).node().getBBox(), o = e.fontSize && e.fontSize.replace ? e.fontSize.replace("px", "") : e.fontSize;
  return s.remove(), l.height + o * 1.1 * 0.5 + t.padding;
}, Ot = function(n, t, e) {
  n.append("path").attr("id", "node-" + t.id).attr("class", "node-bkg node-" + t.type).attr(
    "d",
    `M0 ${t.height - 5} v${-t.height + 2 * 5} q0,-5 5,-5 h${t.width - 2 * 5} q5,0 5,5 v${t.height - 5} H0 Z`
  ), n.append("line").attr("class", "node-line-" + e).attr("x1", 0).attr("y1", t.height).attr("x2", t.width).attr("y2", t.height);
}, R = {
  drawRect: J,
  drawCircle: Pt,
  drawSection: Ct,
  drawText: mt,
  drawLabel: Ht,
  drawTask: Vt,
  drawBackgroundRect: zt,
  getTextObj: Rt,
  getNoteRect: tt,
  initGraphics: Ft,
  drawNode: Wt,
  getVirtualNodeHeight: Bt
}, jt = function(n, t, e, s) {
  var C, O, G, j;
  const i = wt(), l = i.leftMargin ?? 50;
  (O = (C = s.db).clear) == null || O.call(C), s.parser.parse(n + `
`), T.debug("timeline", s.db);
  const o = i.securityLevel;
  let y;
  o === "sandbox" && (y = Z("#i" + t));
  const d = (o === "sandbox" ? (
    // @ts-ignore d3 types are wrong
    Z(y.nodes()[0].contentDocument.body)
  ) : Z("body")).select("#" + t);
  d.append("g");
  const m = s.db.getTasks(), S = s.db.getCommonDb().getDiagramTitle();
  T.debug("task", m), R.initGraphics(d);
  const _ = s.db.getSections();
  T.debug("sections", _);
  let b = 0, v = 0, I = 0, k = 0, r = 50 + l, a = 50;
  k = 50;
  let h = 0, u = !0;
  _.forEach(function(P) {
    const p = {
      number: h,
      descr: P,
      section: h,
      width: 150,
      padding: 20,
      maxHeight: b
    }, E = R.getVirtualNodeHeight(d, p, i);
    T.debug("sectionHeight before draw", E), b = Math.max(b, E + 20);
  });
  let f = 0, c = 0;
  T.debug("tasks.length", m.length);
  for (const [P, p] of m.entries()) {
    const E = {
      number: P,
      descr: p,
      section: p.section,
      width: 150,
      padding: 20,
      maxHeight: v
    }, M = R.getVirtualNodeHeight(d, E, i);
    T.debug("taskHeight before draw", M), v = Math.max(v, M + 20), f = Math.max(f, p.events.length);
    let H = 0;
    for (let V = 0; V < p.events.length; V++) {
      const w = {
        descr: p.events[V],
        section: p.section,
        number: p.section,
        width: 150,
        padding: 20,
        maxHeight: 50
      };
      H += R.getVirtualNodeHeight(d, w, i);
    }
    c = Math.max(c, H);
  }
  T.debug("maxSectionHeight before draw", b), T.debug("maxTaskHeight before draw", v), _ && _.length > 0 ? _.forEach((P) => {
    const p = m.filter((V) => V.section === P), E = {
      number: h,
      descr: P,
      section: h,
      width: 200 * Math.max(p.length, 1) - 50,
      padding: 20,
      maxHeight: b
    };
    T.debug("sectionNode", E);
    const M = d.append("g"), H = R.drawNode(M, E, h, i);
    T.debug("sectionNode output", H), M.attr("transform", `translate(${r}, ${k})`), a += b + 50, p.length > 0 && at(
      d,
      p,
      h,
      r,
      a,
      v,
      i,
      f,
      c,
      b,
      !1
    ), r += 200 * Math.max(p.length, 1), a = k, h++;
  }) : (u = !1, at(
    d,
    m,
    h,
    r,
    a,
    v,
    i,
    f,
    c,
    b,
    !0
  ));
  const L = d.node().getBBox();
  T.debug("bounds", L), S && d.append("text").text(S).attr("x", L.width / 2 - l).attr("font-size", "4ex").attr("font-weight", "bold").attr("y", 20), I = u ? b + v + 150 : v + 100, d.append("g").attr("class", "lineWrapper").append("line").attr("x1", l).attr("y1", I).attr("x2", L.width + 3 * l).attr("y2", I).attr("stroke-width", 4).attr("stroke", "black").attr("marker-end", "url(#arrowhead)"), Tt(
    void 0,
    d,
    ((G = i.timeline) == null ? void 0 : G.padding) ?? 50,
    ((j = i.timeline) == null ? void 0 : j.useMaxWidth) ?? !1
  );
}, at = function(n, t, e, s, i, l, o, y, g, d, m) {
  var S;
  for (const _ of t) {
    const b = {
      descr: _.task,
      section: e,
      number: e,
      width: 150,
      padding: 20,
      maxHeight: l
    };
    T.debug("taskNode", b);
    const v = n.append("g").attr("class", "taskWrapper"), k = R.drawNode(v, b, e, o).height;
    if (T.debug("taskHeight after draw", k), v.attr("transform", `translate(${s}, ${i})`), l = Math.max(l, k), _.events) {
      const r = n.append("g").attr("class", "lineWrapper");
      let a = l;
      i += 100, a = a + Gt(n, _.events, e, s, i, o), i -= 100, r.append("line").attr("x1", s + 190 / 2).attr("y1", i + l).attr("x2", s + 190 / 2).attr(
        "y2",
        i + l + (m ? l : d) + g + 120
      ).attr("stroke-width", 2).attr("stroke", "black").attr("marker-end", "url(#arrowhead)").attr("stroke-dasharray", "5,5");
    }
    s = s + 200, m && !((S = o.timeline) != null && S.disableMulticolor) && e++;
  }
  i = i - 10;
}, Gt = function(n, t, e, s, i, l) {
  let o = 0;
  const y = i;
  i = i + 100;
  for (const g of t) {
    const d = {
      descr: g,
      section: e,
      number: e,
      width: 150,
      padding: 20,
      maxHeight: 50
    };
    T.debug("eventNode", d);
    const m = n.append("g").attr("class", "eventWrapper"), _ = R.drawNode(m, d, e, l).height;
    o = o + _, m.attr("transform", `translate(${s}, ${i})`), i = i + 10 + _;
  }
  return i = y, o;
}, qt = {
  setConf: () => {
  },
  draw: jt
}, Ut = (n) => {
  let t = "";
  for (let e = 0; e < n.THEME_COLOR_LIMIT; e++)
    n["lineColor" + e] = n["lineColor" + e] || n["cScaleInv" + e], It(n["lineColor" + e]) ? n["lineColor" + e] = St(n["lineColor" + e], 20) : n["lineColor" + e] = Et(n["lineColor" + e], 20);
  for (let e = 0; e < n.THEME_COLOR_LIMIT; e++) {
    const s = "" + (17 - 3 * e);
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
      stroke-width: ${s};
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
}, Zt = (n) => `
  .edge {
    stroke-width: 3;
  }
  ${Ut(n)}
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
`, Kt = Zt, ne = {
  db: Mt,
  renderer: qt,
  parser: Nt,
  styles: Kt
};
export {
  ne as diagram
};
//# sourceMappingURL=timeline-definition-274a7ee6.js.map
