import { m as gt } from "./mermaidAPI-04b5c286.js";
import { g as V, f as Z } from "./config-e567ef17.js";
import { d as mt, e as xt, s as _t, g as kt, b as vt, a as bt, f as wt } from "./commonDb-4dc3d465.js";
import { d as st } from "./arc-1bd4335b.js";
import { c as Tt } from "./setupGraphViewbox-a4603a92.js";
import "./utils-aa888deb.js";
import "./errorRenderer-a3c4bedb.js";
import "./constant-2fe7eae5.js";
var K = function() {
  var e = function(_, n, a, h) {
    for (a = a || {}, h = _.length; h--; a[_[h]] = n)
      ;
    return a;
  }, t = [1, 2], i = [1, 5], r = [6, 9, 11, 17, 18, 20, 22, 23, 24, 26], s = [1, 15], o = [1, 16], l = [1, 17], y = [1, 18], u = [1, 19], x = [1, 20], g = [1, 24], f = [4, 6, 9, 11, 17, 18, 20, 22, 23, 24, 26], p = {
    trace: function() {
    },
    yy: {},
    symbols_: { error: 2, start: 3, journey: 4, document: 5, EOF: 6, directive: 7, line: 8, SPACE: 9, statement: 10, NEWLINE: 11, openDirective: 12, typeDirective: 13, closeDirective: 14, ":": 15, argDirective: 16, title: 17, acc_title: 18, acc_title_value: 19, acc_descr: 20, acc_descr_value: 21, acc_descr_multiline_value: 22, section: 23, taskName: 24, taskData: 25, open_directive: 26, type_directive: 27, arg_directive: 28, close_directive: 29, $accept: 0, $end: 1 },
    terminals_: { 2: "error", 4: "journey", 6: "EOF", 9: "SPACE", 11: "NEWLINE", 15: ":", 17: "title", 18: "acc_title", 19: "acc_title_value", 20: "acc_descr", 21: "acc_descr_value", 22: "acc_descr_multiline_value", 23: "section", 24: "taskName", 25: "taskData", 26: "open_directive", 27: "type_directive", 28: "arg_directive", 29: "close_directive" },
    productions_: [0, [3, 3], [3, 2], [5, 0], [5, 2], [8, 2], [8, 1], [8, 1], [8, 1], [7, 4], [7, 6], [10, 1], [10, 2], [10, 2], [10, 1], [10, 1], [10, 2], [10, 1], [12, 1], [13, 1], [16, 1], [14, 1]],
    performAction: function(n, a, h, d, m, c, R) {
      var k = c.length - 1;
      switch (m) {
        case 1:
          return c[k - 1];
        case 3:
          this.$ = [];
          break;
        case 4:
          c[k - 1].push(c[k]), this.$ = c[k - 1];
          break;
        case 5:
        case 6:
          this.$ = c[k];
          break;
        case 7:
        case 8:
          this.$ = [];
          break;
        case 11:
          d.setDiagramTitle(c[k].substr(6)), this.$ = c[k].substr(6);
          break;
        case 12:
          this.$ = c[k].trim(), d.setAccTitle(this.$);
          break;
        case 13:
        case 14:
          this.$ = c[k].trim(), d.setAccDescription(this.$);
          break;
        case 15:
          d.addSection(c[k].substr(8)), this.$ = c[k].substr(8);
          break;
        case 16:
          d.addTask(c[k - 1], c[k]), this.$ = "task";
          break;
        case 18:
          d.parseDirective("%%{", "open_directive");
          break;
        case 19:
          d.parseDirective(c[k], "type_directive");
          break;
        case 20:
          c[k] = c[k].trim().replace(/'/g, '"'), d.parseDirective(c[k], "arg_directive");
          break;
        case 21:
          d.parseDirective("}%%", "close_directive", "journey");
          break;
      }
    },
    table: [{ 3: 1, 4: t, 7: 3, 12: 4, 26: i }, { 1: [3] }, e(r, [2, 3], { 5: 6 }), { 3: 7, 4: t, 7: 3, 12: 4, 26: i }, { 13: 8, 27: [1, 9] }, { 27: [2, 18] }, { 6: [1, 10], 7: 21, 8: 11, 9: [1, 12], 10: 13, 11: [1, 14], 12: 4, 17: s, 18: o, 20: l, 22: y, 23: u, 24: x, 26: i }, { 1: [2, 2] }, { 14: 22, 15: [1, 23], 29: g }, e([15, 29], [2, 19]), e(r, [2, 8], { 1: [2, 1] }), e(r, [2, 4]), { 7: 21, 10: 25, 12: 4, 17: s, 18: o, 20: l, 22: y, 23: u, 24: x, 26: i }, e(r, [2, 6]), e(r, [2, 7]), e(r, [2, 11]), { 19: [1, 26] }, { 21: [1, 27] }, e(r, [2, 14]), e(r, [2, 15]), { 25: [1, 28] }, e(r, [2, 17]), { 11: [1, 29] }, { 16: 30, 28: [1, 31] }, { 11: [2, 21] }, e(r, [2, 5]), e(r, [2, 12]), e(r, [2, 13]), e(r, [2, 16]), e(f, [2, 9]), { 14: 32, 29: g }, { 29: [2, 20] }, { 11: [1, 33] }, e(f, [2, 10])],
    defaultActions: { 5: [2, 18], 7: [2, 2], 24: [2, 21], 31: [2, 20] },
    parseError: function(n, a) {
      if (a.recoverable)
        this.trace(n);
      else {
        var h = new Error(n);
        throw h.hash = a, h;
      }
    },
    parse: function(n) {
      var a = this, h = [0], d = [], m = [null], c = [], R = this.table, k = "", z = 0, tt = 0, yt = 2, et = 1, pt = c.slice.call(arguments, 1), b = Object.create(this.lexer), I = { yy: {} };
      for (var X in this.yy)
        Object.prototype.hasOwnProperty.call(this.yy, X) && (I.yy[X] = this.yy[X]);
      b.setInput(n, I.yy), I.yy.lexer = b, I.yy.parser = this, typeof b.yylloc > "u" && (b.yylloc = {});
      var G = b.yylloc;
      c.push(G);
      var dt = b.options && b.options.ranges;
      typeof I.yy.parseError == "function" ? this.parseError = I.yy.parseError : this.parseError = Object.getPrototypeOf(this).parseError;
      function ft() {
        var E;
        return E = d.pop() || b.lex() || et, typeof E != "number" && (E instanceof Array && (d = E, E = d.pop()), E = a.symbols_[E] || E), E;
      }
      for (var w, A, M, H, F = {}, Y, $, it, q; ; ) {
        if (A = h[h.length - 1], this.defaultActions[A] ? M = this.defaultActions[A] : ((w === null || typeof w > "u") && (w = ft()), M = R[A] && R[A][w]), typeof M > "u" || !M.length || !M[0]) {
          var U = "";
          q = [];
          for (Y in R[A])
            this.terminals_[Y] && Y > yt && q.push("'" + this.terminals_[Y] + "'");
          b.showPosition ? U = "Parse error on line " + (z + 1) + `:
` + b.showPosition() + `
Expecting ` + q.join(", ") + ", got '" + (this.terminals_[w] || w) + "'" : U = "Parse error on line " + (z + 1) + ": Unexpected " + (w == et ? "end of input" : "'" + (this.terminals_[w] || w) + "'"), this.parseError(U, {
            text: b.match,
            token: this.terminals_[w] || w,
            line: b.yylineno,
            loc: G,
            expected: q
          });
        }
        if (M[0] instanceof Array && M.length > 1)
          throw new Error("Parse Error: multiple actions possible at state: " + A + ", token: " + w);
        switch (M[0]) {
          case 1:
            h.push(w), m.push(b.yytext), c.push(b.yylloc), h.push(M[1]), w = null, tt = b.yyleng, k = b.yytext, z = b.yylineno, G = b.yylloc;
            break;
          case 2:
            if ($ = this.productions_[M[1]][1], F.$ = m[m.length - $], F._$ = {
              first_line: c[c.length - ($ || 1)].first_line,
              last_line: c[c.length - 1].last_line,
              first_column: c[c.length - ($ || 1)].first_column,
              last_column: c[c.length - 1].last_column
            }, dt && (F._$.range = [
              c[c.length - ($ || 1)].range[0],
              c[c.length - 1].range[1]
            ]), H = this.performAction.apply(F, [
              k,
              tt,
              z,
              I.yy,
              M[1],
              m,
              c
            ].concat(pt)), typeof H < "u")
              return H;
            $ && (h = h.slice(0, -1 * $ * 2), m = m.slice(0, -1 * $), c = c.slice(0, -1 * $)), h.push(this.productions_[M[1]][0]), m.push(F.$), c.push(F._$), it = R[h[h.length - 2]][h[h.length - 1]], h.push(it);
            break;
          case 3:
            return !0;
        }
      }
      return !0;
    }
  }, T = function() {
    var _ = {
      EOF: 1,
      parseError: function(a, h) {
        if (this.yy.parser)
          this.yy.parser.parseError(a, h);
        else
          throw new Error(a);
      },
      // resets the lexer, sets new input
      setInput: function(n, a) {
        return this.yy = a || this.yy || {}, this._input = n, this._more = this._backtrack = this.done = !1, this.yylineno = this.yyleng = 0, this.yytext = this.matched = this.match = "", this.conditionStack = ["INITIAL"], this.yylloc = {
          first_line: 1,
          first_column: 0,
          last_line: 1,
          last_column: 0
        }, this.options.ranges && (this.yylloc.range = [0, 0]), this.offset = 0, this;
      },
      // consumes and returns one char from the input
      input: function() {
        var n = this._input[0];
        this.yytext += n, this.yyleng++, this.offset++, this.match += n, this.matched += n;
        var a = n.match(/(?:\r\n?|\n).*/g);
        return a ? (this.yylineno++, this.yylloc.last_line++) : this.yylloc.last_column++, this.options.ranges && this.yylloc.range[1]++, this._input = this._input.slice(1), n;
      },
      // unshifts one char (or a string) into the input
      unput: function(n) {
        var a = n.length, h = n.split(/(?:\r\n?|\n)/g);
        this._input = n + this._input, this.yytext = this.yytext.substr(0, this.yytext.length - a), this.offset -= a;
        var d = this.match.split(/(?:\r\n?|\n)/g);
        this.match = this.match.substr(0, this.match.length - 1), this.matched = this.matched.substr(0, this.matched.length - 1), h.length - 1 && (this.yylineno -= h.length - 1);
        var m = this.yylloc.range;
        return this.yylloc = {
          first_line: this.yylloc.first_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.first_column,
          last_column: h ? (h.length === d.length ? this.yylloc.first_column : 0) + d[d.length - h.length].length - h[0].length : this.yylloc.first_column - a
        }, this.options.ranges && (this.yylloc.range = [m[0], m[0] + this.yyleng - a]), this.yyleng = this.yytext.length, this;
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
      less: function(n) {
        this.unput(this.match.slice(n));
      },
      // displays already matched input, i.e. for error messages
      pastInput: function() {
        var n = this.matched.substr(0, this.matched.length - this.match.length);
        return (n.length > 20 ? "..." : "") + n.substr(-20).replace(/\n/g, "");
      },
      // displays upcoming input, i.e. for error messages
      upcomingInput: function() {
        var n = this.match;
        return n.length < 20 && (n += this._input.substr(0, 20 - n.length)), (n.substr(0, 20) + (n.length > 20 ? "..." : "")).replace(/\n/g, "");
      },
      // displays the character position where the lexing error occurred, i.e. for error messages
      showPosition: function() {
        var n = this.pastInput(), a = new Array(n.length + 1).join("-");
        return n + this.upcomingInput() + `
` + a + "^";
      },
      // test the lexed token: return FALSE when not a match, otherwise return token
      test_match: function(n, a) {
        var h, d, m;
        if (this.options.backtrack_lexer && (m = {
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
        }, this.options.ranges && (m.yylloc.range = this.yylloc.range.slice(0))), d = n[0].match(/(?:\r\n?|\n).*/g), d && (this.yylineno += d.length), this.yylloc = {
          first_line: this.yylloc.last_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.last_column,
          last_column: d ? d[d.length - 1].length - d[d.length - 1].match(/\r?\n?/)[0].length : this.yylloc.last_column + n[0].length
        }, this.yytext += n[0], this.match += n[0], this.matches = n, this.yyleng = this.yytext.length, this.options.ranges && (this.yylloc.range = [this.offset, this.offset += this.yyleng]), this._more = !1, this._backtrack = !1, this._input = this._input.slice(n[0].length), this.matched += n[0], h = this.performAction.call(this, this.yy, this, a, this.conditionStack[this.conditionStack.length - 1]), this.done && this._input && (this.done = !1), h)
          return h;
        if (this._backtrack) {
          for (var c in m)
            this[c] = m[c];
          return !1;
        }
        return !1;
      },
      // return next match in input
      next: function() {
        if (this.done)
          return this.EOF;
        this._input || (this.done = !0);
        var n, a, h, d;
        this._more || (this.yytext = "", this.match = "");
        for (var m = this._currentRules(), c = 0; c < m.length; c++)
          if (h = this._input.match(this.rules[m[c]]), h && (!a || h[0].length > a[0].length)) {
            if (a = h, d = c, this.options.backtrack_lexer) {
              if (n = this.test_match(h, m[c]), n !== !1)
                return n;
              if (this._backtrack) {
                a = !1;
                continue;
              } else
                return !1;
            } else if (!this.options.flex)
              break;
          }
        return a ? (n = this.test_match(a, m[d]), n !== !1 ? n : !1) : this._input === "" ? this.EOF : this.parseError("Lexical error on line " + (this.yylineno + 1) + `. Unrecognized text.
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
      performAction: function(a, h, d, m) {
        switch (d) {
          case 0:
            return this.begin("open_directive"), 26;
          case 1:
            return this.begin("type_directive"), 27;
          case 2:
            return this.popState(), this.begin("arg_directive"), 15;
          case 3:
            return this.popState(), this.popState(), 29;
          case 4:
            return 28;
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
            return 24;
          case 21:
            return 25;
          case 22:
            return 15;
          case 23:
            return 6;
          case 24:
            return "INVALID";
        }
      },
      rules: [/^(?:%%\{)/i, /^(?:((?:(?!\}%%)[^:.])*))/i, /^(?::)/i, /^(?:\}%%)/i, /^(?:((?:(?!\}%%).|\n)*))/i, /^(?:%(?!\{)[^\n]*)/i, /^(?:[^\}]%%[^\n]*)/i, /^(?:[\n]+)/i, /^(?:\s+)/i, /^(?:#[^\n]*)/i, /^(?:journey\b)/i, /^(?:title\s[^#\n;]+)/i, /^(?:accTitle\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*\{\s*)/i, /^(?:[\}])/i, /^(?:[^\}]*)/i, /^(?:section\s[^#:\n;]+)/i, /^(?:[^#:\n;]+)/i, /^(?::[^#\n;]+)/i, /^(?::)/i, /^(?:$)/i, /^(?:.)/i],
      conditions: { open_directive: { rules: [1], inclusive: !1 }, type_directive: { rules: [2, 3], inclusive: !1 }, arg_directive: { rules: [3, 4], inclusive: !1 }, acc_descr_multiline: { rules: [17, 18], inclusive: !1 }, acc_descr: { rules: [15], inclusive: !1 }, acc_title: { rules: [13], inclusive: !1 }, INITIAL: { rules: [0, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 19, 20, 21, 22, 23, 24], inclusive: !0 } }
    };
    return _;
  }();
  p.lexer = T;
  function v() {
    this.yy = {};
  }
  return v.prototype = p, p.Parser = v, new v();
}();
K.parser = K;
const Mt = K;
let L = "";
const Q = [], N = [], B = [], St = function(e, t, i) {
  gt.parseDirective(this, e, t, i);
}, $t = function() {
  Q.length = 0, N.length = 0, L = "", B.length = 0, wt();
}, Et = function(e) {
  L = e, Q.push(e);
}, Pt = function() {
  return Q;
}, It = function() {
  let e = rt();
  const t = 100;
  let i = 0;
  for (; !e && i < t; )
    e = rt(), i++;
  return N.push(...B), N;
}, At = function() {
  const e = [];
  return N.forEach((i) => {
    i.people && e.push(...i.people);
  }), [...new Set(e)].sort();
}, Ct = function(e, t) {
  const i = t.substr(1).split(":");
  let r = 0, s = [];
  i.length === 1 ? (r = Number(i[0]), s = []) : (r = Number(i[0]), s = i[1].split(","));
  const o = s.map((y) => y.trim()), l = {
    section: L,
    type: L,
    people: o,
    task: e,
    score: r
  };
  B.push(l);
}, Vt = function(e) {
  const t = {
    section: L,
    type: L,
    description: e,
    task: e,
    classes: []
  };
  N.push(t);
}, rt = function() {
  const e = function(i) {
    return B[i].processed;
  };
  let t = !0;
  for (const [i, r] of B.entries())
    e(i), t = t && r.processed;
  return t;
}, Ft = function() {
  return At();
}, nt = {
  parseDirective: St,
  getConfig: () => V().journey,
  clear: $t,
  setDiagramTitle: mt,
  getDiagramTitle: xt,
  setAccTitle: _t,
  getAccTitle: kt,
  setAccDescription: vt,
  getAccDescription: bt,
  addSection: Et,
  getSections: Pt,
  getTasks: It,
  addTask: Ct,
  addTaskOrg: Vt,
  getActors: Ft
}, Lt = (e) => `.label {
    font-family: 'trebuchet ms', verdana, arial, sans-serif;
    font-family: var(--mermaid-font-family);
    color: ${e.textColor};
  }
  .mouth {
    stroke: #666;
  }

  line {
    stroke: ${e.textColor}
  }

  .legend {
    fill: ${e.textColor};
  }

  .label text {
    fill: #333;
  }
  .label {
    color: ${e.textColor}
  }

  .face {
    ${e.faceColor ? `fill: ${e.faceColor}` : "fill: #FFF8DC"};
    stroke: #999;
  }

  .node rect,
  .node circle,
  .node ellipse,
  .node polygon,
  .node path {
    fill: ${e.mainBkg};
    stroke: ${e.nodeBorder};
    stroke-width: 1px;
  }

  .node .label {
    text-align: center;
  }
  .node.clickable {
    cursor: pointer;
  }

  .arrowheadPath {
    fill: ${e.arrowheadColor};
  }

  .edgePath .path {
    stroke: ${e.lineColor};
    stroke-width: 1.5px;
  }

  .flowchart-link {
    stroke: ${e.lineColor};
    fill: none;
  }

  .edgeLabel {
    background-color: ${e.edgeLabelBackground};
    rect {
      opacity: 0.5;
    }
    text-align: center;
  }

  .cluster rect {
  }

  .cluster text {
    fill: ${e.titleColor};
  }

  div.mermaidTooltip {
    position: absolute;
    text-align: center;
    max-width: 200px;
    padding: 2px;
    font-family: 'trebuchet ms', verdana, arial, sans-serif;
    font-family: var(--mermaid-font-family);
    font-size: 12px;
    background: ${e.tertiaryColor};
    border: 1px solid ${e.border2};
    border-radius: 2px;
    pointer-events: none;
    z-index: 100;
  }

  .task-type-0, .section-type-0  {
    ${e.fillType0 ? `fill: ${e.fillType0}` : ""};
  }
  .task-type-1, .section-type-1  {
    ${e.fillType0 ? `fill: ${e.fillType1}` : ""};
  }
  .task-type-2, .section-type-2  {
    ${e.fillType0 ? `fill: ${e.fillType2}` : ""};
  }
  .task-type-3, .section-type-3  {
    ${e.fillType0 ? `fill: ${e.fillType3}` : ""};
  }
  .task-type-4, .section-type-4  {
    ${e.fillType0 ? `fill: ${e.fillType4}` : ""};
  }
  .task-type-5, .section-type-5  {
    ${e.fillType0 ? `fill: ${e.fillType5}` : ""};
  }
  .task-type-6, .section-type-6  {
    ${e.fillType0 ? `fill: ${e.fillType6}` : ""};
  }
  .task-type-7, .section-type-7  {
    ${e.fillType0 ? `fill: ${e.fillType7}` : ""};
  }

  .actor-0 {
    ${e.actor0 ? `fill: ${e.actor0}` : ""};
  }
  .actor-1 {
    ${e.actor1 ? `fill: ${e.actor1}` : ""};
  }
  .actor-2 {
    ${e.actor2 ? `fill: ${e.actor2}` : ""};
  }
  .actor-3 {
    ${e.actor3 ? `fill: ${e.actor3}` : ""};
  }
  .actor-4 {
    ${e.actor4 ? `fill: ${e.actor4}` : ""};
  }
  .actor-5 {
    ${e.actor5 ? `fill: ${e.actor5}` : ""};
  }
`, Rt = Lt, O = function(e, t) {
  const i = e.append("rect");
  return i.attr("x", t.x), i.attr("y", t.y), i.attr("fill", t.fill), i.attr("stroke", t.stroke), i.attr("width", t.width), i.attr("height", t.height), i.attr("rx", t.rx), i.attr("ry", t.ry), t.class !== void 0 && i.attr("class", t.class), i;
}, Nt = function(e, t) {
  const r = e.append("circle").attr("cx", t.cx).attr("cy", t.cy).attr("class", "face").attr("r", 15).attr("stroke-width", 2).attr("overflow", "visible"), s = e.append("g");
  s.append("circle").attr("cx", t.cx - 15 / 3).attr("cy", t.cy - 15 / 3).attr("r", 1.5).attr("stroke-width", 2).attr("fill", "#666").attr("stroke", "#666"), s.append("circle").attr("cx", t.cx + 15 / 3).attr("cy", t.cy - 15 / 3).attr("r", 1.5).attr("stroke-width", 2).attr("fill", "#666").attr("stroke", "#666");
  function o(u) {
    const x = st().startAngle(Math.PI / 2).endAngle(3 * (Math.PI / 2)).innerRadius(7.5).outerRadius(6.8181818181818175);
    u.append("path").attr("class", "mouth").attr("d", x).attr("transform", "translate(" + t.cx + "," + (t.cy + 2) + ")");
  }
  function l(u) {
    const x = st().startAngle(3 * Math.PI / 2).endAngle(5 * (Math.PI / 2)).innerRadius(7.5).outerRadius(6.8181818181818175);
    u.append("path").attr("class", "mouth").attr("d", x).attr("transform", "translate(" + t.cx + "," + (t.cy + 7) + ")");
  }
  function y(u) {
    u.append("line").attr("class", "mouth").attr("stroke", 2).attr("x1", t.cx - 5).attr("y1", t.cy + 7).attr("x2", t.cx + 5).attr("y2", t.cy + 7).attr("class", "mouth").attr("stroke-width", "1px").attr("stroke", "#666");
  }
  return t.score > 3 ? o(s) : t.score < 3 ? l(s) : y(s), r;
}, ot = function(e, t) {
  const i = e.append("circle");
  return i.attr("cx", t.cx), i.attr("cy", t.cy), i.attr("class", "actor-" + t.pos), i.attr("fill", t.fill), i.attr("stroke", t.stroke), i.attr("r", t.r), i.class !== void 0 && i.attr("class", i.class), t.title !== void 0 && i.append("title").text(t.title), i;
}, ht = function(e, t) {
  const i = t.text.replace(/<br\s*\/?>/gi, " "), r = e.append("text");
  r.attr("x", t.x), r.attr("y", t.y), r.attr("class", "legend"), r.style("text-anchor", t.anchor), t.class !== void 0 && r.attr("class", t.class);
  const s = r.append("tspan");
  return s.attr("x", t.x + t.textMargin * 2), s.text(i), r;
}, Bt = function(e, t) {
  function i(s, o, l, y, u) {
    return s + "," + o + " " + (s + l) + "," + o + " " + (s + l) + "," + (o + y - u) + " " + (s + l - u * 1.2) + "," + (o + y) + " " + s + "," + (o + y);
  }
  const r = e.append("polygon");
  r.attr("points", i(t.x, t.y, 50, 20, 7)), r.attr("class", "labelBox"), t.y = t.y + t.labelMargin, t.x = t.x + 0.5 * t.labelMargin, ht(e, t);
}, jt = function(e, t, i) {
  const r = e.append("g"), s = D();
  s.x = t.x, s.y = t.y, s.fill = t.fill, s.width = i.width * t.taskCount + // width of the tasks
  i.diagramMarginX * (t.taskCount - 1), s.height = i.height, s.class = "journey-section section-type-" + t.num, s.rx = 3, s.ry = 3, O(r, s), ut(i)(
    t.text,
    r,
    s.x,
    s.y,
    s.width,
    s.height,
    { class: "journey-section section-type-" + t.num },
    i,
    t.colour
  );
};
let at = -1;
const zt = function(e, t, i) {
  const r = t.x + i.width / 2, s = e.append("g");
  at++;
  const o = 300 + 5 * 30;
  s.append("line").attr("id", "task" + at).attr("x1", r).attr("y1", t.y).attr("x2", r).attr("y2", o).attr("class", "task-line").attr("stroke-width", "1px").attr("stroke-dasharray", "4 2").attr("stroke", "#666"), Nt(s, {
    cx: r,
    cy: 300 + (5 - t.score) * 30,
    score: t.score
  });
  const l = D();
  l.x = t.x, l.y = t.y, l.fill = t.fill, l.width = i.width, l.height = i.height, l.class = "task task-type-" + t.num, l.rx = 3, l.ry = 3, O(s, l);
  let y = t.x + 14;
  t.people.forEach((u) => {
    const x = t.actors[u].color, g = {
      cx: y,
      cy: t.y,
      r: 7,
      fill: x,
      stroke: "#000",
      title: u,
      pos: t.actors[u].position
    };
    ot(s, g), y += 10;
  }), ut(i)(
    t.task,
    s,
    l.x,
    l.y,
    l.width,
    l.height,
    { class: "task" },
    i,
    t.colour
  );
}, Yt = function(e, t) {
  O(e, {
    x: t.startx,
    y: t.starty,
    width: t.stopx - t.startx,
    height: t.stopy - t.starty,
    fill: t.fill,
    class: "rect"
  }).lower();
}, qt = function() {
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
}, D = function() {
  return {
    x: 0,
    y: 0,
    width: 100,
    anchor: "start",
    height: 100,
    rx: 0,
    ry: 0
  };
}, ut = function() {
  function e(s, o, l, y, u, x, g, f) {
    const p = o.append("text").attr("x", l + u / 2).attr("y", y + x / 2 + 5).style("font-color", f).style("text-anchor", "middle").text(s);
    r(p, g);
  }
  function t(s, o, l, y, u, x, g, f, p) {
    const { taskFontSize: T, taskFontFamily: v } = f, _ = s.split(/<br\s*\/?>/gi);
    for (let n = 0; n < _.length; n++) {
      const a = n * T - T * (_.length - 1) / 2, h = o.append("text").attr("x", l + u / 2).attr("y", y).attr("fill", p).style("text-anchor", "middle").style("font-size", T).style("font-family", v);
      h.append("tspan").attr("x", l + u / 2).attr("dy", a).text(_[n]), h.attr("y", y + x / 2).attr("dominant-baseline", "central").attr("alignment-baseline", "central"), r(h, g);
    }
  }
  function i(s, o, l, y, u, x, g, f) {
    const p = o.append("switch"), v = p.append("foreignObject").attr("x", l).attr("y", y).attr("width", u).attr("height", x).attr("position", "fixed").append("xhtml:div").style("display", "table").style("height", "100%").style("width", "100%");
    v.append("div").attr("class", "label").style("display", "table-cell").style("text-align", "center").style("vertical-align", "middle").text(s), t(s, p, l, y, u, x, g, f), r(v, g);
  }
  function r(s, o) {
    for (const l in o)
      l in o && s.attr(l, o[l]);
  }
  return function(s) {
    return s.textPlacement === "fo" ? i : s.textPlacement === "old" ? e : t;
  };
}(), Ot = function(e) {
  e.append("defs").append("marker").attr("id", "arrowhead").attr("refX", 5).attr("refY", 2).attr("markerWidth", 6).attr("markerHeight", 4).attr("orient", "auto").append("path").attr("d", "M 0,0 V 4 L6,2 Z");
}, j = {
  drawRect: O,
  drawCircle: ot,
  drawSection: jt,
  drawText: ht,
  drawLabel: Bt,
  drawTask: zt,
  drawBackgroundRect: Yt,
  getTextObj: qt,
  getNoteRect: D,
  initGraphics: Ot
}, Wt = function(e) {
  Object.keys(e).forEach(function(i) {
    W[i] = e[i];
  });
}, P = {};
function Xt(e) {
  const t = V().journey;
  let i = 60;
  Object.keys(P).forEach((r) => {
    const s = P[r].color, o = {
      cx: 20,
      cy: i,
      r: 7,
      fill: s,
      stroke: "#000",
      pos: P[r].position
    };
    j.drawCircle(e, o);
    const l = {
      x: 40,
      y: i + 7,
      fill: "#666",
      text: r,
      textMargin: t.boxTextMargin | 5
    };
    j.drawText(e, l), i += 20;
  });
}
const W = V().journey, C = W.leftMargin, Gt = function(e, t, i, r) {
  const s = V().journey;
  r.db.clear(), r.parser.parse(e + `
`);
  const o = V().securityLevel;
  let l;
  o === "sandbox" && (l = Z("#i" + t));
  const y = o === "sandbox" ? Z(l.nodes()[0].contentDocument.body) : Z("body");
  S.init();
  const u = y.select("#" + t);
  j.initGraphics(u);
  const x = r.db.getTasks(), g = r.db.getDiagramTitle(), f = r.db.getActors();
  for (const a in P)
    delete P[a];
  let p = 0;
  f.forEach((a) => {
    P[a] = {
      color: s.actorColours[p % s.actorColours.length],
      position: p
    }, p++;
  }), Xt(u), S.insert(0, 0, C, Object.keys(P).length * 50), Ht(u, x, 0);
  const T = S.getBounds();
  g && u.append("text").text(g).attr("x", C).attr("font-size", "4ex").attr("font-weight", "bold").attr("y", 25);
  const v = T.stopy - T.starty + 2 * s.diagramMarginY, _ = C + T.stopx + 2 * s.diagramMarginX;
  Tt(u, v, _, s.useMaxWidth), u.append("line").attr("x1", C).attr("y1", s.height * 4).attr("x2", _ - C - 4).attr("y2", s.height * 4).attr("stroke-width", 4).attr("stroke", "black").attr("marker-end", "url(#arrowhead)");
  const n = g ? 70 : 0;
  u.attr("viewBox", `${T.startx} -25 ${_} ${v + n}`), u.attr("preserveAspectRatio", "xMinYMin meet"), u.attr("height", v + n + 25);
}, S = {
  data: {
    startx: void 0,
    stopx: void 0,
    starty: void 0,
    stopy: void 0
  },
  verticalPos: 0,
  sequenceItems: [],
  init: function() {
    this.sequenceItems = [], this.data = {
      startx: void 0,
      stopx: void 0,
      starty: void 0,
      stopy: void 0
    }, this.verticalPos = 0;
  },
  updateVal: function(e, t, i, r) {
    e[t] === void 0 ? e[t] = i : e[t] = r(i, e[t]);
  },
  updateBounds: function(e, t, i, r) {
    const s = V().journey, o = this;
    let l = 0;
    function y(u) {
      return function(g) {
        l++;
        const f = o.sequenceItems.length - l + 1;
        o.updateVal(g, "starty", t - f * s.boxMargin, Math.min), o.updateVal(g, "stopy", r + f * s.boxMargin, Math.max), o.updateVal(S.data, "startx", e - f * s.boxMargin, Math.min), o.updateVal(S.data, "stopx", i + f * s.boxMargin, Math.max), u !== "activation" && (o.updateVal(g, "startx", e - f * s.boxMargin, Math.min), o.updateVal(g, "stopx", i + f * s.boxMargin, Math.max), o.updateVal(S.data, "starty", t - f * s.boxMargin, Math.min), o.updateVal(S.data, "stopy", r + f * s.boxMargin, Math.max));
      };
    }
    this.sequenceItems.forEach(y());
  },
  insert: function(e, t, i, r) {
    const s = Math.min(e, i), o = Math.max(e, i), l = Math.min(t, r), y = Math.max(t, r);
    this.updateVal(S.data, "startx", s, Math.min), this.updateVal(S.data, "starty", l, Math.min), this.updateVal(S.data, "stopx", o, Math.max), this.updateVal(S.data, "stopy", y, Math.max), this.updateBounds(s, l, o, y);
  },
  bumpVerticalPos: function(e) {
    this.verticalPos = this.verticalPos + e, this.data.stopy = this.verticalPos;
  },
  getVerticalPos: function() {
    return this.verticalPos;
  },
  getBounds: function() {
    return this.data;
  }
}, J = W.sectionFills, lt = W.sectionColours, Ht = function(e, t, i) {
  const r = V().journey;
  let s = "";
  const o = r.height * 2 + r.diagramMarginY, l = i + o;
  let y = 0, u = "#CCC", x = "black", g = 0;
  for (const [f, p] of t.entries()) {
    if (s !== p.section) {
      u = J[y % J.length], g = y % J.length, x = lt[y % lt.length];
      let v = 0;
      const _ = p.section;
      for (let a = f; a < t.length && t[a].section == _; a++)
        v = v + 1;
      const n = {
        x: f * r.taskMargin + f * r.width + C,
        y: 50,
        text: p.section,
        fill: u,
        num: g,
        colour: x,
        taskCount: v
      };
      j.drawSection(e, n, r), s = p.section, y++;
    }
    const T = p.people.reduce((v, _) => (P[_] && (v[_] = P[_]), v), {});
    p.x = f * r.taskMargin + f * r.width + C, p.y = l, p.width = r.diagramMarginX, p.height = r.diagramMarginY, p.colour = x, p.fill = u, p.num = g, p.actors = T, j.drawTask(e, p, r), S.insert(p.x, p.y, p.x + p.width + r.taskMargin, 300 + 5 * 30);
  }
}, ct = {
  setConf: Wt,
  draw: Gt
}, ie = {
  parser: Mt,
  db: nt,
  renderer: ct,
  styles: Rt,
  init: (e) => {
    ct.setConf(e.journey), nt.clear();
  }
};
export {
  ie as diagram
};
//# sourceMappingURL=journeyDiagram-48369403.js.map
