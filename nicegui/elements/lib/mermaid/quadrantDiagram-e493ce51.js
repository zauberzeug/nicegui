import { $ as vt, X as I, l as lt, s as Lt, g as Ct, B as zt, D as At, a as Et, b as Dt, c as yt, E as It, d as Bt, j as gt, k as wt } from "./mermaid-5f2d2ec5.js";
import { l as bt } from "./linear-c9300245.js";
import "./init-f9637058.js";
var pt = function() {
  var e = function(G, n, r, o) {
    for (r = r || {}, o = G.length; o--; r[G[o]] = n)
      ;
    return r;
  }, s = [1, 3], c = [1, 4], x = [1, 5], f = [1, 6], d = [1, 7], l = [1, 5, 13, 15, 17, 19, 20, 25, 27, 28, 29, 30, 31, 32, 33, 34, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], g = [1, 5, 6, 13, 15, 17, 19, 20, 25, 27, 28, 29, 30, 31, 32, 33, 34, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], i = [32, 33, 34], y = [2, 7], b = [1, 13], B = [1, 17], w = [1, 18], A = [1, 19], z = [1, 20], _ = [1, 21], H = [1, 22], $ = [1, 23], K = [1, 24], at = [1, 25], nt = [1, 26], et = [1, 27], Q = [1, 30], N = [1, 31], q = [1, 32], T = [1, 33], m = [1, 34], t = [1, 35], S = [1, 36], k = [1, 37], F = [1, 38], P = [1, 39], v = [1, 40], L = [1, 41], C = [1, 42], X = [1, 57], M = [1, 58], E = [5, 22, 26, 32, 33, 34, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51], ht = {
    trace: function() {
    },
    yy: {},
    symbols_: { error: 2, start: 3, eol: 4, SPACE: 5, QUADRANT: 6, document: 7, line: 8, statement: 9, axisDetails: 10, quadrantDetails: 11, points: 12, title: 13, title_value: 14, acc_title: 15, acc_title_value: 16, acc_descr: 17, acc_descr_value: 18, acc_descr_multiline_value: 19, section: 20, text: 21, point_start: 22, point_x: 23, point_y: 24, "X-AXIS": 25, "AXIS-TEXT-DELIMITER": 26, "Y-AXIS": 27, QUADRANT_1: 28, QUADRANT_2: 29, QUADRANT_3: 30, QUADRANT_4: 31, NEWLINE: 32, SEMI: 33, EOF: 34, alphaNumToken: 35, textNoTagsToken: 36, STR: 37, MD_STR: 38, alphaNum: 39, PUNCTUATION: 40, AMP: 41, NUM: 42, ALPHA: 43, COMMA: 44, PLUS: 45, EQUALS: 46, MULT: 47, DOT: 48, BRKT: 49, UNDERSCORE: 50, MINUS: 51, $accept: 0, $end: 1 },
    terminals_: { 2: "error", 5: "SPACE", 6: "QUADRANT", 13: "title", 14: "title_value", 15: "acc_title", 16: "acc_title_value", 17: "acc_descr", 18: "acc_descr_value", 19: "acc_descr_multiline_value", 20: "section", 22: "point_start", 23: "point_x", 24: "point_y", 25: "X-AXIS", 26: "AXIS-TEXT-DELIMITER", 27: "Y-AXIS", 28: "QUADRANT_1", 29: "QUADRANT_2", 30: "QUADRANT_3", 31: "QUADRANT_4", 32: "NEWLINE", 33: "SEMI", 34: "EOF", 37: "STR", 38: "MD_STR", 40: "PUNCTUATION", 41: "AMP", 42: "NUM", 43: "ALPHA", 44: "COMMA", 45: "PLUS", 46: "EQUALS", 47: "MULT", 48: "DOT", 49: "BRKT", 50: "UNDERSCORE", 51: "MINUS" },
    productions_: [0, [3, 2], [3, 2], [3, 2], [7, 0], [7, 2], [8, 2], [9, 0], [9, 2], [9, 1], [9, 1], [9, 1], [9, 2], [9, 2], [9, 2], [9, 1], [9, 1], [12, 4], [10, 4], [10, 3], [10, 2], [10, 4], [10, 3], [10, 2], [11, 2], [11, 2], [11, 2], [11, 2], [4, 1], [4, 1], [4, 1], [21, 1], [21, 2], [21, 1], [21, 1], [39, 1], [39, 2], [35, 1], [35, 1], [35, 1], [35, 1], [35, 1], [35, 1], [35, 1], [35, 1], [35, 1], [35, 1], [35, 1], [36, 1], [36, 1], [36, 1]],
    performAction: function(n, r, o, h, p, a, it) {
      var u = a.length - 1;
      switch (p) {
        case 12:
          this.$ = a[u].trim(), h.setDiagramTitle(this.$);
          break;
        case 13:
          this.$ = a[u].trim(), h.setAccTitle(this.$);
          break;
        case 14:
        case 15:
          this.$ = a[u].trim(), h.setAccDescription(this.$);
          break;
        case 16:
          h.addSection(a[u].substr(8)), this.$ = a[u].substr(8);
          break;
        case 17:
          h.addPoint(a[u - 3], a[u - 1], a[u]);
          break;
        case 18:
          h.setXAxisLeftText(a[u - 2]), h.setXAxisRightText(a[u]);
          break;
        case 19:
          a[u - 1].text += " ⟶ ", h.setXAxisLeftText(a[u - 1]);
          break;
        case 20:
          h.setXAxisLeftText(a[u]);
          break;
        case 21:
          h.setYAxisBottomText(a[u - 2]), h.setYAxisTopText(a[u]);
          break;
        case 22:
          a[u - 1].text += " ⟶ ", h.setYAxisBottomText(a[u - 1]);
          break;
        case 23:
          h.setYAxisBottomText(a[u]);
          break;
        case 24:
          h.setQuadrant1Text(a[u]);
          break;
        case 25:
          h.setQuadrant2Text(a[u]);
          break;
        case 26:
          h.setQuadrant3Text(a[u]);
          break;
        case 27:
          h.setQuadrant4Text(a[u]);
          break;
        case 31:
          this.$ = { text: a[u], type: "text" };
          break;
        case 32:
          this.$ = { text: a[u - 1].text + "" + a[u], type: a[u - 1].type };
          break;
        case 33:
          this.$ = { text: a[u], type: "text" };
          break;
        case 34:
          this.$ = { text: a[u], type: "markdown" };
          break;
        case 35:
          this.$ = a[u];
          break;
        case 36:
          this.$ = a[u - 1] + "" + a[u];
          break;
      }
    },
    table: [{ 3: 1, 4: 2, 5: s, 6: c, 32: x, 33: f, 34: d }, { 1: [3] }, { 3: 8, 4: 2, 5: s, 6: c, 32: x, 33: f, 34: d }, { 3: 9, 4: 2, 5: s, 6: c, 32: x, 33: f, 34: d }, e(l, [2, 4], { 7: 10 }), e(g, [2, 28]), e(g, [2, 29]), e(g, [2, 30]), { 1: [2, 1] }, { 1: [2, 2] }, e(i, y, { 8: 11, 9: 12, 10: 14, 11: 15, 12: 16, 21: 28, 35: 29, 1: [2, 3], 5: b, 13: B, 15: w, 17: A, 19: z, 20: _, 25: H, 27: $, 28: K, 29: at, 30: nt, 31: et, 37: Q, 38: N, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C }), e(l, [2, 5]), { 4: 43, 32: x, 33: f, 34: d }, e(i, y, { 10: 14, 11: 15, 12: 16, 21: 28, 35: 29, 9: 44, 5: b, 13: B, 15: w, 17: A, 19: z, 20: _, 25: H, 27: $, 28: K, 29: at, 30: nt, 31: et, 37: Q, 38: N, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C }), e(i, [2, 9]), e(i, [2, 10]), e(i, [2, 11]), { 14: [1, 45] }, { 16: [1, 46] }, { 18: [1, 47] }, e(i, [2, 15]), e(i, [2, 16]), { 21: 48, 35: 29, 37: Q, 38: N, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C }, { 21: 49, 35: 29, 37: Q, 38: N, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C }, { 21: 50, 35: 29, 37: Q, 38: N, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C }, { 21: 51, 35: 29, 37: Q, 38: N, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C }, { 21: 52, 35: 29, 37: Q, 38: N, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C }, { 21: 53, 35: 29, 37: Q, 38: N, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C }, { 5: X, 22: [1, 54], 35: 56, 36: 55, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C, 51: M }, e(E, [2, 31]), e(E, [2, 33]), e(E, [2, 34]), e(E, [2, 37]), e(E, [2, 38]), e(E, [2, 39]), e(E, [2, 40]), e(E, [2, 41]), e(E, [2, 42]), e(E, [2, 43]), e(E, [2, 44]), e(E, [2, 45]), e(E, [2, 46]), e(E, [2, 47]), e(l, [2, 6]), e(i, [2, 8]), e(i, [2, 12]), e(i, [2, 13]), e(i, [2, 14]), e(i, [2, 20], { 36: 55, 35: 56, 5: X, 26: [1, 59], 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C, 51: M }), e(i, [2, 23], { 36: 55, 35: 56, 5: X, 26: [1, 60], 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C, 51: M }), e(i, [2, 24], { 36: 55, 35: 56, 5: X, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C, 51: M }), e(i, [2, 25], { 36: 55, 35: 56, 5: X, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C, 51: M }), e(i, [2, 26], { 36: 55, 35: 56, 5: X, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C, 51: M }), e(i, [2, 27], { 36: 55, 35: 56, 5: X, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C, 51: M }), { 23: [1, 61] }, e(E, [2, 32]), e(E, [2, 48]), e(E, [2, 49]), e(E, [2, 50]), e(i, [2, 19], { 35: 29, 21: 62, 37: Q, 38: N, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C }), e(i, [2, 22], { 35: 29, 21: 63, 37: Q, 38: N, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C }), { 24: [1, 64] }, e(i, [2, 18], { 36: 55, 35: 56, 5: X, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C, 51: M }), e(i, [2, 21], { 36: 55, 35: 56, 5: X, 40: q, 41: T, 42: m, 43: t, 44: S, 45: k, 46: F, 47: P, 48: v, 49: L, 50: C, 51: M }), e(i, [2, 17])],
    defaultActions: { 8: [2, 1], 9: [2, 2] },
    parseError: function(n, r) {
      if (r.recoverable)
        this.trace(n);
      else {
        var o = new Error(n);
        throw o.hash = r, o;
      }
    },
    parse: function(n) {
      var r = this, o = [0], h = [], p = [null], a = [], it = this.table, u = "", st = 0, qt = 0, St = 2, Tt = 1, kt = a.slice.call(arguments, 1), D = Object.create(this.lexer), Z = { yy: {} };
      for (var dt in this.yy)
        Object.prototype.hasOwnProperty.call(this.yy, dt) && (Z.yy[dt] = this.yy[dt]);
      D.setInput(n, Z.yy), Z.yy.lexer = D, Z.yy.parser = this, typeof D.yylloc > "u" && (D.yylloc = {});
      var ut = D.yylloc;
      a.push(ut);
      var Ft = D.options && D.options.ranges;
      typeof Z.yy.parseError == "function" ? this.parseError = Z.yy.parseError : this.parseError = Object.getPrototypeOf(this).parseError;
      function Pt() {
        var Y;
        return Y = h.pop() || D.lex() || Tt, typeof Y != "number" && (Y instanceof Array && (h = Y, Y = h.pop()), Y = r.symbols_[Y] || Y), Y;
      }
      for (var W, J, U, xt, tt = {}, rt, O, mt, ot; ; ) {
        if (J = o[o.length - 1], this.defaultActions[J] ? U = this.defaultActions[J] : ((W === null || typeof W > "u") && (W = Pt()), U = it[J] && it[J][W]), typeof U > "u" || !U.length || !U[0]) {
          var ft = "";
          ot = [];
          for (rt in it[J])
            this.terminals_[rt] && rt > St && ot.push("'" + this.terminals_[rt] + "'");
          D.showPosition ? ft = "Parse error on line " + (st + 1) + `:
` + D.showPosition() + `
Expecting ` + ot.join(", ") + ", got '" + (this.terminals_[W] || W) + "'" : ft = "Parse error on line " + (st + 1) + ": Unexpected " + (W == Tt ? "end of input" : "'" + (this.terminals_[W] || W) + "'"), this.parseError(ft, {
            text: D.match,
            token: this.terminals_[W] || W,
            line: D.yylineno,
            loc: ut,
            expected: ot
          });
        }
        if (U[0] instanceof Array && U.length > 1)
          throw new Error("Parse Error: multiple actions possible at state: " + J + ", token: " + W);
        switch (U[0]) {
          case 1:
            o.push(W), p.push(D.yytext), a.push(D.yylloc), o.push(U[1]), W = null, qt = D.yyleng, u = D.yytext, st = D.yylineno, ut = D.yylloc;
            break;
          case 2:
            if (O = this.productions_[U[1]][1], tt.$ = p[p.length - O], tt._$ = {
              first_line: a[a.length - (O || 1)].first_line,
              last_line: a[a.length - 1].last_line,
              first_column: a[a.length - (O || 1)].first_column,
              last_column: a[a.length - 1].last_column
            }, Ft && (tt._$.range = [
              a[a.length - (O || 1)].range[0],
              a[a.length - 1].range[1]
            ]), xt = this.performAction.apply(tt, [
              u,
              qt,
              st,
              Z.yy,
              U[1],
              p,
              a
            ].concat(kt)), typeof xt < "u")
              return xt;
            O && (o = o.slice(0, -1 * O * 2), p = p.slice(0, -1 * O), a = a.slice(0, -1 * O)), o.push(this.productions_[U[1]][0]), p.push(tt.$), a.push(tt._$), mt = it[o[o.length - 2]][o[o.length - 1]], o.push(mt);
            break;
          case 3:
            return !0;
        }
      }
      return !0;
    }
  }, _t = function() {
    var G = {
      EOF: 1,
      parseError: function(r, o) {
        if (this.yy.parser)
          this.yy.parser.parseError(r, o);
        else
          throw new Error(r);
      },
      // resets the lexer, sets new input
      setInput: function(n, r) {
        return this.yy = r || this.yy || {}, this._input = n, this._more = this._backtrack = this.done = !1, this.yylineno = this.yyleng = 0, this.yytext = this.matched = this.match = "", this.conditionStack = ["INITIAL"], this.yylloc = {
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
        var r = n.match(/(?:\r\n?|\n).*/g);
        return r ? (this.yylineno++, this.yylloc.last_line++) : this.yylloc.last_column++, this.options.ranges && this.yylloc.range[1]++, this._input = this._input.slice(1), n;
      },
      // unshifts one char (or a string) into the input
      unput: function(n) {
        var r = n.length, o = n.split(/(?:\r\n?|\n)/g);
        this._input = n + this._input, this.yytext = this.yytext.substr(0, this.yytext.length - r), this.offset -= r;
        var h = this.match.split(/(?:\r\n?|\n)/g);
        this.match = this.match.substr(0, this.match.length - 1), this.matched = this.matched.substr(0, this.matched.length - 1), o.length - 1 && (this.yylineno -= o.length - 1);
        var p = this.yylloc.range;
        return this.yylloc = {
          first_line: this.yylloc.first_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.first_column,
          last_column: o ? (o.length === h.length ? this.yylloc.first_column : 0) + h[h.length - o.length].length - o[0].length : this.yylloc.first_column - r
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
        var n = this.pastInput(), r = new Array(n.length + 1).join("-");
        return n + this.upcomingInput() + `
` + r + "^";
      },
      // test the lexed token: return FALSE when not a match, otherwise return token
      test_match: function(n, r) {
        var o, h, p;
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
        }, this.options.ranges && (p.yylloc.range = this.yylloc.range.slice(0))), h = n[0].match(/(?:\r\n?|\n).*/g), h && (this.yylineno += h.length), this.yylloc = {
          first_line: this.yylloc.last_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.last_column,
          last_column: h ? h[h.length - 1].length - h[h.length - 1].match(/\r?\n?/)[0].length : this.yylloc.last_column + n[0].length
        }, this.yytext += n[0], this.match += n[0], this.matches = n, this.yyleng = this.yytext.length, this.options.ranges && (this.yylloc.range = [this.offset, this.offset += this.yyleng]), this._more = !1, this._backtrack = !1, this._input = this._input.slice(n[0].length), this.matched += n[0], o = this.performAction.call(this, this.yy, this, r, this.conditionStack[this.conditionStack.length - 1]), this.done && this._input && (this.done = !1), o)
          return o;
        if (this._backtrack) {
          for (var a in p)
            this[a] = p[a];
          return !1;
        }
        return !1;
      },
      // return next match in input
      next: function() {
        if (this.done)
          return this.EOF;
        this._input || (this.done = !0);
        var n, r, o, h;
        this._more || (this.yytext = "", this.match = "");
        for (var p = this._currentRules(), a = 0; a < p.length; a++)
          if (o = this._input.match(this.rules[p[a]]), o && (!r || o[0].length > r[0].length)) {
            if (r = o, h = a, this.options.backtrack_lexer) {
              if (n = this.test_match(o, p[a]), n !== !1)
                return n;
              if (this._backtrack) {
                r = !1;
                continue;
              } else
                return !1;
            } else if (!this.options.flex)
              break;
          }
        return r ? (n = this.test_match(r, p[h]), n !== !1 ? n : !1) : this._input === "" ? this.EOF : this.parseError("Lexical error on line " + (this.yylineno + 1) + `. Unrecognized text.
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
      performAction: function(r, o, h, p) {
        switch (h) {
          case 0:
            break;
          case 1:
            break;
          case 2:
            return 32;
          case 3:
            break;
          case 4:
            return this.begin("title"), 13;
          case 5:
            return this.popState(), "title_value";
          case 6:
            return this.begin("acc_title"), 15;
          case 7:
            return this.popState(), "acc_title_value";
          case 8:
            return this.begin("acc_descr"), 17;
          case 9:
            return this.popState(), "acc_descr_value";
          case 10:
            this.begin("acc_descr_multiline");
            break;
          case 11:
            this.popState();
            break;
          case 12:
            return "acc_descr_multiline_value";
          case 13:
            return 25;
          case 14:
            return 27;
          case 15:
            return 26;
          case 16:
            return 28;
          case 17:
            return 29;
          case 18:
            return 30;
          case 19:
            return 31;
          case 20:
            this.begin("md_string");
            break;
          case 21:
            return "MD_STR";
          case 22:
            this.popState();
            break;
          case 23:
            this.begin("string");
            break;
          case 24:
            this.popState();
            break;
          case 25:
            return "STR";
          case 26:
            return this.begin("point_start"), 22;
          case 27:
            return this.begin("point_x"), 23;
          case 28:
            this.popState();
            break;
          case 29:
            this.popState(), this.begin("point_y");
            break;
          case 30:
            return this.popState(), 24;
          case 31:
            return 6;
          case 32:
            return 43;
          case 33:
            return "COLON";
          case 34:
            return 45;
          case 35:
            return 44;
          case 36:
            return 46;
          case 37:
            return 46;
          case 38:
            return 47;
          case 39:
            return 49;
          case 40:
            return 50;
          case 41:
            return 48;
          case 42:
            return 41;
          case 43:
            return 51;
          case 44:
            return 42;
          case 45:
            return 5;
          case 46:
            return 33;
          case 47:
            return 40;
          case 48:
            return 34;
        }
      },
      rules: [/^(?:%%(?!\{)[^\n]*)/i, /^(?:[^\}]%%[^\n]*)/i, /^(?:[\n\r]+)/i, /^(?:%%[^\n]*)/i, /^(?:title\b)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accTitle\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*\{\s*)/i, /^(?:[\}])/i, /^(?:[^\}]*)/i, /^(?: *x-axis *)/i, /^(?: *y-axis *)/i, /^(?: *--+> *)/i, /^(?: *quadrant-1 *)/i, /^(?: *quadrant-2 *)/i, /^(?: *quadrant-3 *)/i, /^(?: *quadrant-4 *)/i, /^(?:["][`])/i, /^(?:[^`"]+)/i, /^(?:[`]["])/i, /^(?:["])/i, /^(?:["])/i, /^(?:[^"]*)/i, /^(?:\s*:\s*\[\s*)/i, /^(?:(1)|(0(.\d+)?))/i, /^(?:\s*\] *)/i, /^(?:\s*,\s*)/i, /^(?:(1)|(0(.\d+)?))/i, /^(?: *quadrantChart *)/i, /^(?:[A-Za-z]+)/i, /^(?::)/i, /^(?:\+)/i, /^(?:,)/i, /^(?:=)/i, /^(?:=)/i, /^(?:\*)/i, /^(?:#)/i, /^(?:[\_])/i, /^(?:\.)/i, /^(?:&)/i, /^(?:-)/i, /^(?:[0-9]+)/i, /^(?:\s)/i, /^(?:;)/i, /^(?:[!"#$%&'*+,-.`?\\_/])/i, /^(?:$)/i],
      conditions: { point_y: { rules: [30], inclusive: !1 }, point_x: { rules: [29], inclusive: !1 }, point_start: { rules: [27, 28], inclusive: !1 }, acc_descr_multiline: { rules: [11, 12], inclusive: !1 }, acc_descr: { rules: [9], inclusive: !1 }, acc_title: { rules: [7], inclusive: !1 }, title: { rules: [5], inclusive: !1 }, md_string: { rules: [21, 22], inclusive: !1 }, string: { rules: [24, 25], inclusive: !1 }, INITIAL: { rules: [0, 1, 2, 3, 4, 6, 8, 10, 13, 14, 15, 16, 17, 18, 19, 20, 23, 26, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48], inclusive: !0 } }
    };
    return G;
  }();
  ht.lexer = _t;
  function ct() {
    this.yy = {};
  }
  return ct.prototype = ht, ht.Parser = ct, new ct();
}();
pt.parser = pt;
const Rt = pt, V = vt();
class Vt {
  constructor() {
    this.config = this.getDefaultConfig(), this.themeConfig = this.getDefaultThemeConfig(), this.data = this.getDefaultData();
  }
  getDefaultData() {
    return {
      titleText: "",
      quadrant1Text: "",
      quadrant2Text: "",
      quadrant3Text: "",
      quadrant4Text: "",
      xAxisLeftText: "",
      xAxisRightText: "",
      yAxisBottomText: "",
      yAxisTopText: "",
      points: []
    };
  }
  getDefaultConfig() {
    var s, c, x, f, d, l, g, i, y, b, B, w, A, z, _, H, $, K;
    return {
      showXAxis: !0,
      showYAxis: !0,
      showTitle: !0,
      chartHeight: ((s = I.quadrantChart) == null ? void 0 : s.chartWidth) || 500,
      chartWidth: ((c = I.quadrantChart) == null ? void 0 : c.chartHeight) || 500,
      titlePadding: ((x = I.quadrantChart) == null ? void 0 : x.titlePadding) || 10,
      titleFontSize: ((f = I.quadrantChart) == null ? void 0 : f.titleFontSize) || 20,
      quadrantPadding: ((d = I.quadrantChart) == null ? void 0 : d.quadrantPadding) || 5,
      xAxisLabelPadding: ((l = I.quadrantChart) == null ? void 0 : l.xAxisLabelPadding) || 5,
      yAxisLabelPadding: ((g = I.quadrantChart) == null ? void 0 : g.yAxisLabelPadding) || 5,
      xAxisLabelFontSize: ((i = I.quadrantChart) == null ? void 0 : i.xAxisLabelFontSize) || 16,
      yAxisLabelFontSize: ((y = I.quadrantChart) == null ? void 0 : y.yAxisLabelFontSize) || 16,
      quadrantLabelFontSize: ((b = I.quadrantChart) == null ? void 0 : b.quadrantLabelFontSize) || 16,
      quadrantTextTopPadding: ((B = I.quadrantChart) == null ? void 0 : B.quadrantTextTopPadding) || 5,
      pointTextPadding: ((w = I.quadrantChart) == null ? void 0 : w.pointTextPadding) || 5,
      pointLabelFontSize: ((A = I.quadrantChart) == null ? void 0 : A.pointLabelFontSize) || 12,
      pointRadius: ((z = I.quadrantChart) == null ? void 0 : z.pointRadius) || 5,
      xAxisPosition: ((_ = I.quadrantChart) == null ? void 0 : _.xAxisPosition) || "top",
      yAxisPosition: ((H = I.quadrantChart) == null ? void 0 : H.yAxisPosition) || "left",
      quadrantInternalBorderStrokeWidth: (($ = I.quadrantChart) == null ? void 0 : $.quadrantInternalBorderStrokeWidth) || 1,
      quadrantExternalBorderStrokeWidth: ((K = I.quadrantChart) == null ? void 0 : K.quadrantExternalBorderStrokeWidth) || 2
    };
  }
  getDefaultThemeConfig() {
    return {
      quadrant1Fill: V.quadrant1Fill,
      quadrant2Fill: V.quadrant2Fill,
      quadrant3Fill: V.quadrant3Fill,
      quadrant4Fill: V.quadrant4Fill,
      quadrant1TextFill: V.quadrant1TextFill,
      quadrant2TextFill: V.quadrant2TextFill,
      quadrant3TextFill: V.quadrant3TextFill,
      quadrant4TextFill: V.quadrant4TextFill,
      quadrantPointFill: V.quadrantPointFill,
      quadrantPointTextFill: V.quadrantPointTextFill,
      quadrantXAxisTextFill: V.quadrantXAxisTextFill,
      quadrantYAxisTextFill: V.quadrantYAxisTextFill,
      quadrantTitleFill: V.quadrantTitleFill,
      quadrantInternalBorderStrokeFill: V.quadrantInternalBorderStrokeFill,
      quadrantExternalBorderStrokeFill: V.quadrantExternalBorderStrokeFill
    };
  }
  clear() {
    this.config = this.getDefaultConfig(), this.themeConfig = this.getDefaultThemeConfig(), this.data = this.getDefaultData(), lt.info("clear called");
  }
  setData(s) {
    this.data = { ...this.data, ...s };
  }
  addPoints(s) {
    this.data.points = [...s, ...this.data.points];
  }
  setConfig(s) {
    lt.trace("setConfig called with: ", s), this.config = { ...this.config, ...s };
  }
  setThemeConfig(s) {
    lt.trace("setThemeConfig called with: ", s), this.themeConfig = { ...this.themeConfig, ...s };
  }
  calculateSpace(s, c, x, f) {
    const d = this.config.xAxisLabelPadding * 2 + this.config.xAxisLabelFontSize, l = {
      top: s === "top" && c ? d : 0,
      bottom: s === "bottom" && c ? d : 0
    }, g = this.config.yAxisLabelPadding * 2 + this.config.yAxisLabelFontSize, i = {
      left: this.config.yAxisPosition === "left" && x ? g : 0,
      right: this.config.yAxisPosition === "right" && x ? g : 0
    }, y = this.config.titleFontSize + this.config.titlePadding * 2, b = {
      top: f ? y : 0
    }, B = this.config.quadrantPadding + i.left, w = this.config.quadrantPadding + l.top + b.top, A = this.config.chartWidth - this.config.quadrantPadding * 2 - i.left - i.right, z = this.config.chartHeight - this.config.quadrantPadding * 2 - l.top - l.bottom - b.top, _ = A / 2, H = z / 2;
    return {
      xAxisSpace: l,
      yAxisSpace: i,
      titleSpace: b,
      quadrantSpace: {
        quadrantLeft: B,
        quadrantTop: w,
        quadrantWidth: A,
        quadrantHalfWidth: _,
        quadrantHeight: z,
        quadrantHalfHeight: H
      }
    };
  }
  getAxisLabels(s, c, x, f) {
    const { quadrantSpace: d, titleSpace: l } = f, {
      quadrantHalfHeight: g,
      quadrantHeight: i,
      quadrantLeft: y,
      quadrantHalfWidth: b,
      quadrantTop: B,
      quadrantWidth: w
    } = d, A = this.data.points.length === 0, z = [];
    return this.data.xAxisLeftText && c && z.push({
      text: this.data.xAxisLeftText,
      fill: this.themeConfig.quadrantXAxisTextFill,
      x: y + (A ? b / 2 : 0),
      y: s === "top" ? this.config.xAxisLabelPadding + l.top : this.config.xAxisLabelPadding + B + i + this.config.quadrantPadding,
      fontSize: this.config.xAxisLabelFontSize,
      verticalPos: A ? "center" : "left",
      horizontalPos: "top",
      rotation: 0
    }), this.data.xAxisRightText && c && z.push({
      text: this.data.xAxisRightText,
      fill: this.themeConfig.quadrantXAxisTextFill,
      x: y + b + (A ? b / 2 : 0),
      y: s === "top" ? this.config.xAxisLabelPadding + l.top : this.config.xAxisLabelPadding + B + i + this.config.quadrantPadding,
      fontSize: this.config.xAxisLabelFontSize,
      verticalPos: A ? "center" : "left",
      horizontalPos: "top",
      rotation: 0
    }), this.data.yAxisBottomText && x && z.push({
      text: this.data.yAxisBottomText,
      fill: this.themeConfig.quadrantYAxisTextFill,
      x: this.config.yAxisPosition === "left" ? this.config.yAxisLabelPadding : this.config.yAxisLabelPadding + y + w + this.config.quadrantPadding,
      y: B + i - (A ? g / 2 : 0),
      fontSize: this.config.yAxisLabelFontSize,
      verticalPos: A ? "center" : "left",
      horizontalPos: "top",
      rotation: -90
    }), this.data.yAxisTopText && x && z.push({
      text: this.data.yAxisTopText,
      fill: this.themeConfig.quadrantYAxisTextFill,
      x: this.config.yAxisPosition === "left" ? this.config.yAxisLabelPadding : this.config.yAxisLabelPadding + y + w + this.config.quadrantPadding,
      y: B + g - (A ? g / 2 : 0),
      fontSize: this.config.yAxisLabelFontSize,
      verticalPos: A ? "center" : "left",
      horizontalPos: "top",
      rotation: -90
    }), z;
  }
  getQuadrants(s) {
    const { quadrantSpace: c } = s, { quadrantHalfHeight: x, quadrantLeft: f, quadrantHalfWidth: d, quadrantTop: l } = c, g = [
      {
        text: {
          text: this.data.quadrant1Text,
          fill: this.themeConfig.quadrant1TextFill,
          x: 0,
          y: 0,
          fontSize: this.config.quadrantLabelFontSize,
          verticalPos: "center",
          horizontalPos: "middle",
          rotation: 0
        },
        x: f + d,
        y: l,
        width: d,
        height: x,
        fill: this.themeConfig.quadrant1Fill
      },
      {
        text: {
          text: this.data.quadrant2Text,
          fill: this.themeConfig.quadrant2TextFill,
          x: 0,
          y: 0,
          fontSize: this.config.quadrantLabelFontSize,
          verticalPos: "center",
          horizontalPos: "middle",
          rotation: 0
        },
        x: f,
        y: l,
        width: d,
        height: x,
        fill: this.themeConfig.quadrant2Fill
      },
      {
        text: {
          text: this.data.quadrant3Text,
          fill: this.themeConfig.quadrant3TextFill,
          x: 0,
          y: 0,
          fontSize: this.config.quadrantLabelFontSize,
          verticalPos: "center",
          horizontalPos: "middle",
          rotation: 0
        },
        x: f,
        y: l + x,
        width: d,
        height: x,
        fill: this.themeConfig.quadrant3Fill
      },
      {
        text: {
          text: this.data.quadrant4Text,
          fill: this.themeConfig.quadrant4TextFill,
          x: 0,
          y: 0,
          fontSize: this.config.quadrantLabelFontSize,
          verticalPos: "center",
          horizontalPos: "middle",
          rotation: 0
        },
        x: f + d,
        y: l + x,
        width: d,
        height: x,
        fill: this.themeConfig.quadrant4Fill
      }
    ];
    for (const i of g)
      i.text.x = i.x + i.width / 2, this.data.points.length === 0 ? (i.text.y = i.y + i.height / 2, i.text.horizontalPos = "middle") : (i.text.y = i.y + this.config.quadrantTextTopPadding, i.text.horizontalPos = "top");
    return g;
  }
  getQuadrantPoints(s) {
    const { quadrantSpace: c } = s, { quadrantHeight: x, quadrantLeft: f, quadrantTop: d, quadrantWidth: l } = c, g = bt().domain([0, 1]).range([f, l + f]), i = bt().domain([0, 1]).range([x + d, d]);
    return this.data.points.map((b) => ({
      x: g(b.x),
      y: i(b.y),
      fill: this.themeConfig.quadrantPointFill,
      radius: this.config.pointRadius,
      text: {
        text: b.text,
        fill: this.themeConfig.quadrantPointTextFill,
        x: g(b.x),
        y: i(b.y) + this.config.pointTextPadding,
        verticalPos: "center",
        horizontalPos: "top",
        fontSize: this.config.pointLabelFontSize,
        rotation: 0
      }
    }));
  }
  getBorders(s) {
    const c = this.config.quadrantExternalBorderStrokeWidth / 2, { quadrantSpace: x } = s, {
      quadrantHalfHeight: f,
      quadrantHeight: d,
      quadrantLeft: l,
      quadrantHalfWidth: g,
      quadrantTop: i,
      quadrantWidth: y
    } = x;
    return [
      // top border
      {
        strokeFill: this.themeConfig.quadrantExternalBorderStrokeFill,
        strokeWidth: this.config.quadrantExternalBorderStrokeWidth,
        x1: l - c,
        y1: i,
        x2: l + y + c,
        y2: i
      },
      // right border
      {
        strokeFill: this.themeConfig.quadrantExternalBorderStrokeFill,
        strokeWidth: this.config.quadrantExternalBorderStrokeWidth,
        x1: l + y,
        y1: i + c,
        x2: l + y,
        y2: i + d - c
      },
      // bottom border
      {
        strokeFill: this.themeConfig.quadrantExternalBorderStrokeFill,
        strokeWidth: this.config.quadrantExternalBorderStrokeWidth,
        x1: l - c,
        y1: i + d,
        x2: l + y + c,
        y2: i + d
      },
      // left border
      {
        strokeFill: this.themeConfig.quadrantExternalBorderStrokeFill,
        strokeWidth: this.config.quadrantExternalBorderStrokeWidth,
        x1: l,
        y1: i + c,
        x2: l,
        y2: i + d - c
      },
      // vertical inner border
      {
        strokeFill: this.themeConfig.quadrantInternalBorderStrokeFill,
        strokeWidth: this.config.quadrantInternalBorderStrokeWidth,
        x1: l + g,
        y1: i + c,
        x2: l + g,
        y2: i + d - c
      },
      // horizontal inner border
      {
        strokeFill: this.themeConfig.quadrantInternalBorderStrokeFill,
        strokeWidth: this.config.quadrantInternalBorderStrokeWidth,
        x1: l + c,
        y1: i + f,
        x2: l + y - c,
        y2: i + f
      }
    ];
  }
  getTitle(s) {
    if (s)
      return {
        text: this.data.titleText,
        fill: this.themeConfig.quadrantTitleFill,
        fontSize: this.config.titleFontSize,
        horizontalPos: "top",
        verticalPos: "center",
        rotation: 0,
        y: this.config.titlePadding,
        x: this.config.chartWidth / 2
      };
  }
  build() {
    const s = this.config.showXAxis && !!(this.data.xAxisLeftText || this.data.xAxisRightText), c = this.config.showYAxis && !!(this.data.yAxisTopText || this.data.yAxisBottomText), x = this.config.showTitle && !!this.data.titleText, f = this.data.points.length > 0 ? "bottom" : this.config.xAxisPosition, d = this.calculateSpace(f, s, c, x);
    return {
      points: this.getQuadrantPoints(d),
      quadrants: this.getQuadrants(d),
      axisLabels: this.getAxisLabels(f, s, c, d),
      borderLines: this.getBorders(d),
      title: this.getTitle(x)
    };
  }
}
const Wt = yt();
function j(e) {
  return Bt(e.trim(), Wt);
}
const R = new Vt();
function Nt(e) {
  R.setData({ quadrant1Text: j(e.text) });
}
function Ut(e) {
  R.setData({ quadrant2Text: j(e.text) });
}
function Qt(e) {
  R.setData({ quadrant3Text: j(e.text) });
}
function Ht(e) {
  R.setData({ quadrant4Text: j(e.text) });
}
function Xt(e) {
  R.setData({ xAxisLeftText: j(e.text) });
}
function Mt(e) {
  R.setData({ xAxisRightText: j(e.text) });
}
function Ot(e) {
  R.setData({ yAxisTopText: j(e.text) });
}
function Yt(e) {
  R.setData({ yAxisBottomText: j(e.text) });
}
function jt(e, s, c) {
  R.addPoints([{ x: s, y: c, text: j(e.text) }]);
}
function $t(e) {
  R.setConfig({ chartWidth: e });
}
function Gt(e) {
  R.setConfig({ chartHeight: e });
}
function Kt() {
  const e = yt(), { themeVariables: s, quadrantChart: c } = e;
  return c && R.setConfig(c), R.setThemeConfig({
    quadrant1Fill: s.quadrant1Fill,
    quadrant2Fill: s.quadrant2Fill,
    quadrant3Fill: s.quadrant3Fill,
    quadrant4Fill: s.quadrant4Fill,
    quadrant1TextFill: s.quadrant1TextFill,
    quadrant2TextFill: s.quadrant2TextFill,
    quadrant3TextFill: s.quadrant3TextFill,
    quadrant4TextFill: s.quadrant4TextFill,
    quadrantPointFill: s.quadrantPointFill,
    quadrantPointTextFill: s.quadrantPointTextFill,
    quadrantXAxisTextFill: s.quadrantXAxisTextFill,
    quadrantYAxisTextFill: s.quadrantYAxisTextFill,
    quadrantExternalBorderStrokeFill: s.quadrantExternalBorderStrokeFill,
    quadrantInternalBorderStrokeFill: s.quadrantInternalBorderStrokeFill,
    quadrantTitleFill: s.quadrantTitleFill
  }), R.setData({ titleText: At() }), R.build();
}
const Zt = function() {
  R.clear(), It();
}, Jt = {
  setWidth: $t,
  setHeight: Gt,
  setQuadrant1Text: Nt,
  setQuadrant2Text: Ut,
  setQuadrant3Text: Qt,
  setQuadrant4Text: Ht,
  setXAxisLeftText: Xt,
  setXAxisRightText: Mt,
  setYAxisTopText: Ot,
  setYAxisBottomText: Yt,
  addPoint: jt,
  getQuadrantData: Kt,
  clear: Zt,
  setAccTitle: Lt,
  getAccTitle: Ct,
  setDiagramTitle: zt,
  getDiagramTitle: At,
  getAccDescription: Et,
  setAccDescription: Dt
}, te = (e, s, c, x) => {
  var q, T, m;
  function f(t) {
    return t === "top" ? "hanging" : "middle";
  }
  function d(t) {
    return t === "left" ? "start" : "middle";
  }
  function l(t) {
    return `translate(${t.x}, ${t.y}) rotate(${t.rotation || 0})`;
  }
  const g = yt();
  lt.debug(`Rendering quadrant chart
` + e);
  const i = g.securityLevel;
  let y;
  i === "sandbox" && (y = gt("#i" + s));
  const B = (i === "sandbox" ? gt(y.nodes()[0].contentDocument.body) : gt("body")).select(`[id="${s}"]`), w = B.append("g").attr("class", "main"), A = ((q = g.quadrantChart) == null ? void 0 : q.chartWidth) || 500, z = ((T = g.quadrantChart) == null ? void 0 : T.chartHeight) || 500;
  wt(B, z, A, ((m = g.quadrantChart) == null ? void 0 : m.useMaxWidth) || !0), B.attr("viewBox", "0 0 " + A + " " + z), x.db.setHeight(z), x.db.setWidth(A);
  const _ = x.db.getQuadrantData(), H = w.append("g").attr("class", "quadrants"), $ = w.append("g").attr("class", "border"), K = w.append("g").attr("class", "data-points"), at = w.append("g").attr("class", "labels"), nt = w.append("g").attr("class", "title");
  _.title && nt.append("text").attr("x", 0).attr("y", 0).attr("fill", _.title.fill).attr("font-size", _.title.fontSize).attr("dominant-baseline", f(_.title.horizontalPos)).attr("text-anchor", d(_.title.verticalPos)).attr("transform", l(_.title)).text(_.title.text), _.borderLines && $.selectAll("line").data(_.borderLines).enter().append("line").attr("x1", (t) => t.x1).attr("y1", (t) => t.y1).attr("x2", (t) => t.x2).attr("y2", (t) => t.y2).style("stroke", (t) => t.strokeFill).style("stroke-width", (t) => t.strokeWidth);
  const et = H.selectAll("g.quadrant").data(_.quadrants).enter().append("g").attr("class", "quadrant");
  et.append("rect").attr("x", (t) => t.x).attr("y", (t) => t.y).attr("width", (t) => t.width).attr("height", (t) => t.height).attr("fill", (t) => t.fill), et.append("text").attr("x", 0).attr("y", 0).attr("fill", (t) => t.text.fill).attr("font-size", (t) => t.text.fontSize).attr(
    "dominant-baseline",
    (t) => f(t.text.horizontalPos)
  ).attr("text-anchor", (t) => d(t.text.verticalPos)).attr("transform", (t) => l(t.text)).text((t) => t.text.text), at.selectAll("g.label").data(_.axisLabels).enter().append("g").attr("class", "label").append("text").attr("x", 0).attr("y", 0).text((t) => t.text).attr("fill", (t) => t.fill).attr("font-size", (t) => t.fontSize).attr("dominant-baseline", (t) => f(t.horizontalPos)).attr("text-anchor", (t) => d(t.verticalPos)).attr("transform", (t) => l(t));
  const N = K.selectAll("g.data-point").data(_.points).enter().append("g").attr("class", "data-point");
  N.append("circle").attr("cx", (t) => t.x).attr("cy", (t) => t.y).attr("r", (t) => t.radius).attr("fill", (t) => t.fill), N.append("text").attr("x", 0).attr("y", 0).text((t) => t.text.text).attr("fill", (t) => t.text.fill).attr("font-size", (t) => t.text.fontSize).attr(
    "dominant-baseline",
    (t) => f(t.text.horizontalPos)
  ).attr("text-anchor", (t) => d(t.text.verticalPos)).attr("transform", (t) => l(t.text));
}, ee = {
  draw: te
}, se = {
  parser: Rt,
  db: Jt,
  renderer: ee,
  styles: () => ""
};
export {
  se as diagram
};
