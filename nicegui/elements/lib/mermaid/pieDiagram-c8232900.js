import { S as it, c as U, s as gt, g as dt, z as mt, A as _t, a as vt, b as kt, m as bt, f as xt, l as Y, B as St, j as nt, k as wt, T as At } from "./mermaid-be6aa4a6.js";
import { i as Et } from "./init-f9637058.js";
import { a as Dt } from "./array-2ff2c7a6.js";
import { c as z } from "./constant-2fe7eae5.js";
import { d as lt } from "./arc-3976c622.js";
class ct extends Map {
  constructor(s, c = It) {
    if (super(), Object.defineProperties(this, { _intern: { value: /* @__PURE__ */ new Map() }, _key: { value: c } }), s != null)
      for (const [o, y] of s)
        this.set(o, y);
  }
  get(s) {
    return super.get(ot(this, s));
  }
  has(s) {
    return super.has(ot(this, s));
  }
  set(s, c) {
    return super.set(Tt(this, s), c);
  }
  delete(s) {
    return super.delete($t(this, s));
  }
}
function ot({ _intern: t, _key: s }, c) {
  const o = s(c);
  return t.has(o) ? t.get(o) : c;
}
function Tt({ _intern: t, _key: s }, c) {
  const o = s(c);
  return t.has(o) ? t.get(o) : (t.set(o, c), c);
}
function $t({ _intern: t, _key: s }, c) {
  const o = s(c);
  return t.has(o) && (c = t.get(o), t.delete(o)), c;
}
function It(t) {
  return t !== null && typeof t == "object" ? t.valueOf() : t;
}
const ht = Symbol("implicit");
function ut() {
  var t = new ct(), s = [], c = [], o = ht;
  function y(u) {
    let h = t.get(u);
    if (h === void 0) {
      if (o !== ht)
        return o;
      t.set(u, h = s.push(u) - 1);
    }
    return c[h % c.length];
  }
  return y.domain = function(u) {
    if (!arguments.length)
      return s.slice();
    s = [], t = new ct();
    for (const h of u)
      t.has(h) || t.set(h, s.push(h) - 1);
    return y;
  }, y.range = function(u) {
    return arguments.length ? (c = Array.from(u), y) : c.slice();
  }, y.unknown = function(u) {
    return arguments.length ? (o = u, y) : o;
  }, y.copy = function() {
    return ut(s, c).unknown(o);
  }, Et.apply(y, arguments), y;
}
function Vt(t, s) {
  return s < t ? -1 : s > t ? 1 : s >= t ? 0 : NaN;
}
function Pt(t) {
  return t;
}
function Ot() {
  var t = Pt, s = Vt, c = null, o = z(0), y = z(it), u = z(0);
  function h(l) {
    var g, m = (l = Dt(l)).length, D, C, x = 0, $ = new Array(m), w = new Array(m), A = +o.apply(this, arguments), N = Math.min(it, Math.max(-it, y.apply(this, arguments) - A)), W, I = Math.min(Math.abs(N) / m, u.apply(this, arguments)), V = I * (N < 0 ? -1 : 1), v;
    for (g = 0; g < m; ++g)
      (v = w[$[g] = g] = +t(l[g], g, l)) > 0 && (x += v);
    for (s != null ? $.sort(function(E, k) {
      return s(w[E], w[k]);
    }) : c != null && $.sort(function(E, k) {
      return c(l[E], l[k]);
    }), g = 0, C = x ? (N - m * V) / x : 0; g < m; ++g, A = W)
      D = $[g], v = w[D], W = A + (v > 0 ? v * C : 0) + V, w[D] = {
        data: l[D],
        index: g,
        value: v,
        startAngle: A,
        endAngle: W,
        padAngle: I
      };
    return w;
  }
  return h.value = function(l) {
    return arguments.length ? (t = typeof l == "function" ? l : z(+l), h) : t;
  }, h.sortValues = function(l) {
    return arguments.length ? (s = l, c = null, h) : s;
  }, h.sort = function(l) {
    return arguments.length ? (c = l, s = null, h) : c;
  }, h.startAngle = function(l) {
    return arguments.length ? (o = typeof l == "function" ? l : z(+l), h) : o;
  }, h.endAngle = function(l) {
    return arguments.length ? (y = typeof l == "function" ? l : z(+l), h) : y;
  }, h.padAngle = function(l) {
    return arguments.length ? (u = typeof l == "function" ? l : z(+l), h) : u;
  }, h;
}
var rt = function() {
  var t = function(k, e, i, a) {
    for (i = i || {}, a = k.length; a--; i[k[a]] = e)
      ;
    return i;
  }, s = [1, 4], c = [1, 5], o = [1, 6], y = [1, 7], u = [1, 9], h = [1, 11, 13, 15, 17, 19, 20, 26, 27, 28, 29], l = [2, 5], g = [1, 6, 11, 13, 15, 17, 19, 20, 26, 27, 28, 29], m = [26, 27, 28], D = [2, 8], C = [1, 18], x = [1, 19], $ = [1, 20], w = [1, 21], A = [1, 22], N = [1, 23], W = [1, 28], I = [6, 26, 27, 28, 29], V = {
    trace: function() {
    },
    yy: {},
    symbols_: { error: 2, start: 3, eol: 4, directive: 5, PIE: 6, document: 7, showData: 8, line: 9, statement: 10, txt: 11, value: 12, title: 13, title_value: 14, acc_title: 15, acc_title_value: 16, acc_descr: 17, acc_descr_value: 18, acc_descr_multiline_value: 19, section: 20, openDirective: 21, typeDirective: 22, closeDirective: 23, ":": 24, argDirective: 25, NEWLINE: 26, ";": 27, EOF: 28, open_directive: 29, type_directive: 30, arg_directive: 31, close_directive: 32, $accept: 0, $end: 1 },
    terminals_: { 2: "error", 6: "PIE", 8: "showData", 11: "txt", 12: "value", 13: "title", 14: "title_value", 15: "acc_title", 16: "acc_title_value", 17: "acc_descr", 18: "acc_descr_value", 19: "acc_descr_multiline_value", 20: "section", 24: ":", 26: "NEWLINE", 27: ";", 28: "EOF", 29: "open_directive", 30: "type_directive", 31: "arg_directive", 32: "close_directive" },
    productions_: [0, [3, 2], [3, 2], [3, 2], [3, 3], [7, 0], [7, 2], [9, 2], [10, 0], [10, 2], [10, 2], [10, 2], [10, 2], [10, 1], [10, 1], [10, 1], [5, 3], [5, 5], [4, 1], [4, 1], [4, 1], [21, 1], [22, 1], [25, 1], [23, 1]],
    performAction: function(e, i, a, n, f, r, p) {
      var d = r.length - 1;
      switch (f) {
        case 4:
          n.setShowData(!0);
          break;
        case 7:
          this.$ = r[d - 1];
          break;
        case 9:
          n.addSection(r[d - 1], n.cleanupValue(r[d]));
          break;
        case 10:
          this.$ = r[d].trim(), n.setDiagramTitle(this.$);
          break;
        case 11:
          this.$ = r[d].trim(), n.setAccTitle(this.$);
          break;
        case 12:
        case 13:
          this.$ = r[d].trim(), n.setAccDescription(this.$);
          break;
        case 14:
          n.addSection(r[d].substr(8)), this.$ = r[d].substr(8);
          break;
        case 21:
          n.parseDirective("%%{", "open_directive");
          break;
        case 22:
          n.parseDirective(r[d], "type_directive");
          break;
        case 23:
          r[d] = r[d].trim().replace(/'/g, '"'), n.parseDirective(r[d], "arg_directive");
          break;
        case 24:
          n.parseDirective("}%%", "close_directive", "pie");
          break;
      }
    },
    table: [{ 3: 1, 4: 2, 5: 3, 6: s, 21: 8, 26: c, 27: o, 28: y, 29: u }, { 1: [3] }, { 3: 10, 4: 2, 5: 3, 6: s, 21: 8, 26: c, 27: o, 28: y, 29: u }, { 3: 11, 4: 2, 5: 3, 6: s, 21: 8, 26: c, 27: o, 28: y, 29: u }, t(h, l, { 7: 12, 8: [1, 13] }), t(g, [2, 18]), t(g, [2, 19]), t(g, [2, 20]), { 22: 14, 30: [1, 15] }, { 30: [2, 21] }, { 1: [2, 1] }, { 1: [2, 2] }, t(m, D, { 21: 8, 9: 16, 10: 17, 5: 24, 1: [2, 3], 11: C, 13: x, 15: $, 17: w, 19: A, 20: N, 29: u }), t(h, l, { 7: 25 }), { 23: 26, 24: [1, 27], 32: W }, t([24, 32], [2, 22]), t(h, [2, 6]), { 4: 29, 26: c, 27: o, 28: y }, { 12: [1, 30] }, { 14: [1, 31] }, { 16: [1, 32] }, { 18: [1, 33] }, t(m, [2, 13]), t(m, [2, 14]), t(m, [2, 15]), t(m, D, { 21: 8, 9: 16, 10: 17, 5: 24, 1: [2, 4], 11: C, 13: x, 15: $, 17: w, 19: A, 20: N, 29: u }), t(I, [2, 16]), { 25: 34, 31: [1, 35] }, t(I, [2, 24]), t(h, [2, 7]), t(m, [2, 9]), t(m, [2, 10]), t(m, [2, 11]), t(m, [2, 12]), { 23: 36, 32: W }, { 32: [2, 23] }, t(I, [2, 17])],
    defaultActions: { 9: [2, 21], 10: [2, 1], 11: [2, 2], 35: [2, 23] },
    parseError: function(e, i) {
      if (i.recoverable)
        this.trace(e);
      else {
        var a = new Error(e);
        throw a.hash = i, a;
      }
    },
    parse: function(e) {
      var i = this, a = [0], n = [], f = [null], r = [], p = this.table, d = "", F = 0, q = 0, Q = 2, G = 1, ft = r.slice.call(arguments, 1), _ = Object.create(this.lexer), M = { yy: {} };
      for (var X in this.yy)
        Object.prototype.hasOwnProperty.call(this.yy, X) && (M.yy[X] = this.yy[X]);
      _.setInput(e, M.yy), M.yy.lexer = _, M.yy.parser = this, typeof _.yylloc > "u" && (_.yylloc = {});
      var Z = _.yylloc;
      r.push(Z);
      var pt = _.options && _.options.ranges;
      typeof M.yy.parseError == "function" ? this.parseError = M.yy.parseError : this.parseError = Object.getPrototypeOf(this).parseError;
      function yt() {
        var O;
        return O = n.pop() || _.lex() || G, typeof O != "number" && (O instanceof Array && (n = O, O = n.pop()), O = i.symbols_[O] || O), O;
      }
      for (var b, j, S, tt, R = {}, H, P, at, J; ; ) {
        if (j = a[a.length - 1], this.defaultActions[j] ? S = this.defaultActions[j] : ((b === null || typeof b > "u") && (b = yt()), S = p[j] && p[j][b]), typeof S > "u" || !S.length || !S[0]) {
          var et = "";
          J = [];
          for (H in p[j])
            this.terminals_[H] && H > Q && J.push("'" + this.terminals_[H] + "'");
          _.showPosition ? et = "Parse error on line " + (F + 1) + `:
` + _.showPosition() + `
Expecting ` + J.join(", ") + ", got '" + (this.terminals_[b] || b) + "'" : et = "Parse error on line " + (F + 1) + ": Unexpected " + (b == G ? "end of input" : "'" + (this.terminals_[b] || b) + "'"), this.parseError(et, {
            text: _.match,
            token: this.terminals_[b] || b,
            line: _.yylineno,
            loc: Z,
            expected: J
          });
        }
        if (S[0] instanceof Array && S.length > 1)
          throw new Error("Parse Error: multiple actions possible at state: " + j + ", token: " + b);
        switch (S[0]) {
          case 1:
            a.push(b), f.push(_.yytext), r.push(_.yylloc), a.push(S[1]), b = null, q = _.yyleng, d = _.yytext, F = _.yylineno, Z = _.yylloc;
            break;
          case 2:
            if (P = this.productions_[S[1]][1], R.$ = f[f.length - P], R._$ = {
              first_line: r[r.length - (P || 1)].first_line,
              last_line: r[r.length - 1].last_line,
              first_column: r[r.length - (P || 1)].first_column,
              last_column: r[r.length - 1].last_column
            }, pt && (R._$.range = [
              r[r.length - (P || 1)].range[0],
              r[r.length - 1].range[1]
            ]), tt = this.performAction.apply(R, [
              d,
              q,
              F,
              M.yy,
              S[1],
              f,
              r
            ].concat(ft)), typeof tt < "u")
              return tt;
            P && (a = a.slice(0, -1 * P * 2), f = f.slice(0, -1 * P), r = r.slice(0, -1 * P)), a.push(this.productions_[S[1]][0]), f.push(R.$), r.push(R._$), at = p[a[a.length - 2]][a[a.length - 1]], a.push(at);
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
      parseError: function(i, a) {
        if (this.yy.parser)
          this.yy.parser.parseError(i, a);
        else
          throw new Error(i);
      },
      // resets the lexer, sets new input
      setInput: function(e, i) {
        return this.yy = i || this.yy || {}, this._input = e, this._more = this._backtrack = this.done = !1, this.yylineno = this.yyleng = 0, this.yytext = this.matched = this.match = "", this.conditionStack = ["INITIAL"], this.yylloc = {
          first_line: 1,
          first_column: 0,
          last_line: 1,
          last_column: 0
        }, this.options.ranges && (this.yylloc.range = [0, 0]), this.offset = 0, this;
      },
      // consumes and returns one char from the input
      input: function() {
        var e = this._input[0];
        this.yytext += e, this.yyleng++, this.offset++, this.match += e, this.matched += e;
        var i = e.match(/(?:\r\n?|\n).*/g);
        return i ? (this.yylineno++, this.yylloc.last_line++) : this.yylloc.last_column++, this.options.ranges && this.yylloc.range[1]++, this._input = this._input.slice(1), e;
      },
      // unshifts one char (or a string) into the input
      unput: function(e) {
        var i = e.length, a = e.split(/(?:\r\n?|\n)/g);
        this._input = e + this._input, this.yytext = this.yytext.substr(0, this.yytext.length - i), this.offset -= i;
        var n = this.match.split(/(?:\r\n?|\n)/g);
        this.match = this.match.substr(0, this.match.length - 1), this.matched = this.matched.substr(0, this.matched.length - 1), a.length - 1 && (this.yylineno -= a.length - 1);
        var f = this.yylloc.range;
        return this.yylloc = {
          first_line: this.yylloc.first_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.first_column,
          last_column: a ? (a.length === n.length ? this.yylloc.first_column : 0) + n[n.length - a.length].length - a[0].length : this.yylloc.first_column - i
        }, this.options.ranges && (this.yylloc.range = [f[0], f[0] + this.yyleng - i]), this.yyleng = this.yytext.length, this;
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
      less: function(e) {
        this.unput(this.match.slice(e));
      },
      // displays already matched input, i.e. for error messages
      pastInput: function() {
        var e = this.matched.substr(0, this.matched.length - this.match.length);
        return (e.length > 20 ? "..." : "") + e.substr(-20).replace(/\n/g, "");
      },
      // displays upcoming input, i.e. for error messages
      upcomingInput: function() {
        var e = this.match;
        return e.length < 20 && (e += this._input.substr(0, 20 - e.length)), (e.substr(0, 20) + (e.length > 20 ? "..." : "")).replace(/\n/g, "");
      },
      // displays the character position where the lexing error occurred, i.e. for error messages
      showPosition: function() {
        var e = this.pastInput(), i = new Array(e.length + 1).join("-");
        return e + this.upcomingInput() + `
` + i + "^";
      },
      // test the lexed token: return FALSE when not a match, otherwise return token
      test_match: function(e, i) {
        var a, n, f;
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
        }, this.options.ranges && (f.yylloc.range = this.yylloc.range.slice(0))), n = e[0].match(/(?:\r\n?|\n).*/g), n && (this.yylineno += n.length), this.yylloc = {
          first_line: this.yylloc.last_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.last_column,
          last_column: n ? n[n.length - 1].length - n[n.length - 1].match(/\r?\n?/)[0].length : this.yylloc.last_column + e[0].length
        }, this.yytext += e[0], this.match += e[0], this.matches = e, this.yyleng = this.yytext.length, this.options.ranges && (this.yylloc.range = [this.offset, this.offset += this.yyleng]), this._more = !1, this._backtrack = !1, this._input = this._input.slice(e[0].length), this.matched += e[0], a = this.performAction.call(this, this.yy, this, i, this.conditionStack[this.conditionStack.length - 1]), this.done && this._input && (this.done = !1), a)
          return a;
        if (this._backtrack) {
          for (var r in f)
            this[r] = f[r];
          return !1;
        }
        return !1;
      },
      // return next match in input
      next: function() {
        if (this.done)
          return this.EOF;
        this._input || (this.done = !0);
        var e, i, a, n;
        this._more || (this.yytext = "", this.match = "");
        for (var f = this._currentRules(), r = 0; r < f.length; r++)
          if (a = this._input.match(this.rules[f[r]]), a && (!i || a[0].length > i[0].length)) {
            if (i = a, n = r, this.options.backtrack_lexer) {
              if (e = this.test_match(a, f[r]), e !== !1)
                return e;
              if (this._backtrack) {
                i = !1;
                continue;
              } else
                return !1;
            } else if (!this.options.flex)
              break;
          }
        return i ? (e = this.test_match(i, f[n]), e !== !1 ? e : !1) : this._input === "" ? this.EOF : this.parseError("Lexical error on line " + (this.yylineno + 1) + `. Unrecognized text.
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
      performAction: function(i, a, n, f) {
        switch (n) {
          case 0:
            return this.begin("open_directive"), 29;
          case 1:
            return this.begin("type_directive"), 30;
          case 2:
            return this.popState(), this.begin("arg_directive"), 24;
          case 3:
            return this.popState(), this.popState(), 32;
          case 4:
            return 31;
          case 5:
            break;
          case 6:
            break;
          case 7:
            return 26;
          case 8:
            break;
          case 9:
            break;
          case 10:
            return this.begin("title"), 13;
          case 11:
            return this.popState(), "title_value";
          case 12:
            return this.begin("acc_title"), 15;
          case 13:
            return this.popState(), "acc_title_value";
          case 14:
            return this.begin("acc_descr"), 17;
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
            this.begin("string");
            break;
          case 20:
            this.popState();
            break;
          case 21:
            return "txt";
          case 22:
            return 6;
          case 23:
            return 8;
          case 24:
            return "value";
          case 25:
            return 28;
        }
      },
      rules: [/^(?:%%\{)/i, /^(?:((?:(?!\}%%)[^:.])*))/i, /^(?::)/i, /^(?:\}%%)/i, /^(?:((?:(?!\}%%).|\n)*))/i, /^(?:%%(?!\{)[^\n]*)/i, /^(?:[^\}]%%[^\n]*)/i, /^(?:[\n\r]+)/i, /^(?:%%[^\n]*)/i, /^(?:[\s]+)/i, /^(?:title\b)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accTitle\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*\{\s*)/i, /^(?:[\}])/i, /^(?:[^\}]*)/i, /^(?:["])/i, /^(?:["])/i, /^(?:[^"]*)/i, /^(?:pie\b)/i, /^(?:showData\b)/i, /^(?::[\s]*[\d]+(?:\.[\d]+)?)/i, /^(?:$)/i],
      conditions: { acc_descr_multiline: { rules: [17, 18], inclusive: !1 }, acc_descr: { rules: [15], inclusive: !1 }, acc_title: { rules: [13], inclusive: !1 }, close_directive: { rules: [], inclusive: !1 }, arg_directive: { rules: [3, 4], inclusive: !1 }, type_directive: { rules: [2, 3], inclusive: !1 }, open_directive: { rules: [1], inclusive: !1 }, title: { rules: [11], inclusive: !1 }, string: { rules: [20, 21], inclusive: !1 }, INITIAL: { rules: [0, 5, 6, 7, 8, 9, 10, 12, 14, 16, 19, 22, 23, 24, 25], inclusive: !0 } }
    };
    return k;
  }();
  V.lexer = v;
  function E() {
    this.yy = {};
  }
  return E.prototype = V, V.Parser = E, new E();
}();
rt.parser = rt;
const Lt = rt;
let K = {}, st = !1;
const Nt = function(t, s, c) {
  bt.parseDirective(this, t, s, c);
}, Wt = function(t, s) {
  t = xt.sanitizeText(t, U()), K[t] === void 0 && (K[t] = s, Y.debug("Added new section :", t));
}, Ct = () => K, Ft = function(t) {
  st = t;
}, Mt = function() {
  return st;
}, jt = function(t) {
  return t.substring(0, 1) === ":" && (t = t.substring(1).trim()), Number(t.trim());
}, zt = function() {
  K = {}, st = !1, St();
}, Rt = {
  parseDirective: Nt,
  getConfig: () => U().pie,
  addSection: Wt,
  getSections: Ct,
  cleanupValue: jt,
  clear: zt,
  setAccTitle: gt,
  getAccTitle: dt,
  setDiagramTitle: mt,
  getDiagramTitle: _t,
  setShowData: Ft,
  getShowData: Mt,
  getAccDescription: vt,
  setAccDescription: kt
}, Bt = (t) => `
  .pieCircle{
    stroke: ${t.pieStrokeColor};
    stroke-width : ${t.pieStrokeWidth};
    opacity : ${t.pieOpacity};
  }
  .pieOuterCircle{
    stroke: ${t.pieOuterStrokeColor};
    stroke-width: ${t.pieOuterStrokeWidth};
    fill: none;
  }
  .pieTitleText {
    text-anchor: middle;
    font-size: ${t.pieTitleTextSize};
    fill: ${t.pieTitleTextColor};
    font-family: ${t.fontFamily};
  }
  .slice {
    font-family: ${t.fontFamily};
    fill: ${t.pieSectionTextColor};
    font-size:${t.pieSectionTextSize};
    // fill: white;
  }
  .legend text {
    fill: ${t.pieLegendTextColor};
    font-family: ${t.fontFamily};
    font-size: ${t.pieLegendTextSize};
  }
`, Yt = Bt;
let T = U(), L;
const B = 450, Ut = (t, s, c, o) => {
  var V;
  try {
    T = U(), Y.debug(`Rendering info diagram
` + t);
    const v = U().securityLevel;
    let E;
    v === "sandbox" && (E = nt("#i" + s));
    const k = v === "sandbox" ? nt(E.nodes()[0].contentDocument.body) : nt("body"), e = v === "sandbox" ? E.nodes()[0].contentDocument : document;
    o.db.clear(), o.parser.parse(t), Y.debug("Parsed info diagram");
    const i = e.getElementById(s);
    L = i.parentElement.offsetWidth, L === void 0 && (L = 1200), T.useWidth !== void 0 && (L = T.useWidth), T.pie.useWidth !== void 0 && (L = T.pie.useWidth);
    const a = k.select("#" + s);
    wt(a, B, L, T.pie.useMaxWidth), i.setAttribute("viewBox", "0 0 " + L + " " + B);
    var y = 40, u = 18, h = 4, l = Math.min(L, B) / 2 - y, g = a.append("g").attr("transform", "translate(" + L / 2 + "," + B / 2 + ")"), m = o.db.getSections(), D = 0;
    Object.keys(m).forEach(function(p) {
      D += m[p];
    });
    const n = T.themeVariables;
    var C = [
      n.pie1,
      n.pie2,
      n.pie3,
      n.pie4,
      n.pie5,
      n.pie6,
      n.pie7,
      n.pie8,
      n.pie9,
      n.pie10,
      n.pie11,
      n.pie12
    ];
    const f = ((V = T.pie) == null ? void 0 : V.textPosition) ?? 0.75;
    let [r] = At(n.pieOuterStrokeWidth);
    r ?? (r = 2);
    var x = ut().range(C), $ = Object.entries(m).map(function(p, d) {
      return {
        order: d,
        name: p[0],
        value: p[1]
      };
    }), w = Ot().value(function(p) {
      return p.value;
    }).sort(function(p, d) {
      return p.order - d.order;
    }), A = w($), N = lt().innerRadius(0).outerRadius(l), W = lt().innerRadius(l * f).outerRadius(l * f);
    g.append("circle").attr("cx", 0).attr("cy", 0).attr("r", l + r / 2).attr("class", "pieOuterCircle"), g.selectAll("mySlices").data(A).enter().append("path").attr("d", N).attr("fill", function(p) {
      return x(p.data.name);
    }).attr("class", "pieCircle"), g.selectAll("mySlices").data(A).enter().append("text").text(function(p) {
      return (p.data.value / D * 100).toFixed(0) + "%";
    }).attr("transform", function(p) {
      return "translate(" + W.centroid(p) + ")";
    }).style("text-anchor", "middle").attr("class", "slice"), g.append("text").text(o.db.getDiagramTitle()).attr("x", 0).attr("y", -(B - 50) / 2).attr("class", "pieTitleText");
    var I = g.selectAll(".legend").data(x.domain()).enter().append("g").attr("class", "legend").attr("transform", function(p, d) {
      const F = u + h, q = F * x.domain().length / 2, Q = 12 * u, G = d * F - q;
      return "translate(" + Q + "," + G + ")";
    });
    I.append("rect").attr("width", u).attr("height", u).style("fill", x).style("stroke", x), I.data(A).append("text").attr("x", u + h).attr("y", u - h).text(function(p) {
      return o.db.getShowData() || T.showData || T.pie.showData ? p.data.name + " [" + p.data.value + "]" : p.data.name;
    });
  } catch (v) {
    Y.error("Error while rendering info diagram"), Y.error(v);
  }
}, qt = {
  draw: Ut
}, Xt = {
  parser: Lt,
  db: Rt,
  renderer: qt,
  styles: Yt
};
export {
  Xt as diagram
};
