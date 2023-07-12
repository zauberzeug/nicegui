import { U as Dt, V as I, l as lt, s as zt, g as Et, z as It, A as kt, a as Bt, b as Vt, c as Tt, m as wt, B as Rt, d as Wt, j as yt, k as Nt } from "./mermaid-be6aa4a6.js";
import { l as St } from "./linear-d8b7ca63.js";
import "./init-f9637058.js";
var qt = function() {
  var e = function(K, n, r, d) {
    for (r = r || {}, d = K.length; d--; r[K[d]] = n)
      ;
    return r;
  }, a = [1, 3], h = [1, 5], f = [1, 6], g = [1, 7], u = [1, 8], c = [1, 10], p = [1, 5, 14, 16, 18, 20, 21, 26, 28, 29, 30, 31, 32, 38, 39, 40, 41, 47, 48, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60], s = [1, 5, 7, 14, 16, 18, 20, 21, 26, 28, 29, 30, 31, 32, 38, 39, 40, 41, 47, 48, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60], o = [38, 39, 40], m = [2, 8], B = [1, 19], V = [1, 23], _ = [1, 24], D = [1, 25], b = [1, 26], H = [1, 27], G = [1, 29], Z = [1, 30], at = [1, 31], nt = [1, 32], et = [1, 33], ct = [1, 34], N = [1, 37], U = [1, 38], q = [1, 39], T = [1, 40], t = [1, 41], A = [1, 42], S = [1, 43], k = [1, 44], F = [1, 45], v = [1, 46], P = [1, 47], L = [1, 48], C = [1, 49], mt = [1, 52], M = [1, 67], X = [1, 68], z = [5, 23, 27, 38, 39, 40, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61], ht = [5, 7, 38, 39, 40, 41], dt = {
    trace: function() {
    },
    yy: {},
    symbols_: { error: 2, start: 3, eol: 4, SPACE: 5, directive: 6, QUADRANT: 7, document: 8, line: 9, statement: 10, axisDetails: 11, quadrantDetails: 12, points: 13, title: 14, title_value: 15, acc_title: 16, acc_title_value: 17, acc_descr: 18, acc_descr_value: 19, acc_descr_multiline_value: 20, section: 21, text: 22, point_start: 23, point_x: 24, point_y: 25, "X-AXIS": 26, "AXIS-TEXT-DELIMITER": 27, "Y-AXIS": 28, QUADRANT_1: 29, QUADRANT_2: 30, QUADRANT_3: 31, QUADRANT_4: 32, openDirective: 33, typeDirective: 34, closeDirective: 35, ":": 36, argDirective: 37, NEWLINE: 38, SEMI: 39, EOF: 40, open_directive: 41, type_directive: 42, arg_directive: 43, close_directive: 44, alphaNumToken: 45, textNoTagsToken: 46, STR: 47, MD_STR: 48, alphaNum: 49, PUNCTUATION: 50, AMP: 51, NUM: 52, ALPHA: 53, COMMA: 54, PLUS: 55, EQUALS: 56, MULT: 57, DOT: 58, BRKT: 59, UNDERSCORE: 60, MINUS: 61, $accept: 0, $end: 1 },
    terminals_: { 2: "error", 5: "SPACE", 7: "QUADRANT", 14: "title", 15: "title_value", 16: "acc_title", 17: "acc_title_value", 18: "acc_descr", 19: "acc_descr_value", 20: "acc_descr_multiline_value", 21: "section", 23: "point_start", 24: "point_x", 25: "point_y", 26: "X-AXIS", 27: "AXIS-TEXT-DELIMITER", 28: "Y-AXIS", 29: "QUADRANT_1", 30: "QUADRANT_2", 31: "QUADRANT_3", 32: "QUADRANT_4", 36: ":", 38: "NEWLINE", 39: "SEMI", 40: "EOF", 41: "open_directive", 42: "type_directive", 43: "arg_directive", 44: "close_directive", 47: "STR", 48: "MD_STR", 50: "PUNCTUATION", 51: "AMP", 52: "NUM", 53: "ALPHA", 54: "COMMA", 55: "PLUS", 56: "EQUALS", 57: "MULT", 58: "DOT", 59: "BRKT", 60: "UNDERSCORE", 61: "MINUS" },
    productions_: [0, [3, 2], [3, 2], [3, 2], [3, 2], [8, 0], [8, 2], [9, 2], [10, 0], [10, 2], [10, 1], [10, 1], [10, 1], [10, 2], [10, 2], [10, 2], [10, 1], [10, 1], [10, 1], [13, 4], [11, 4], [11, 3], [11, 2], [11, 4], [11, 3], [11, 2], [12, 2], [12, 2], [12, 2], [12, 2], [6, 3], [6, 5], [4, 1], [4, 1], [4, 1], [33, 1], [34, 1], [37, 1], [35, 1], [22, 1], [22, 2], [22, 1], [22, 1], [49, 1], [49, 2], [45, 1], [45, 1], [45, 1], [45, 1], [45, 1], [45, 1], [45, 1], [45, 1], [45, 1], [45, 1], [45, 1], [46, 1], [46, 1], [46, 1]],
    performAction: function(n, r, d, l, y, i, it) {
      var x = i.length - 1;
      switch (y) {
        case 13:
          this.$ = i[x].trim(), l.setDiagramTitle(this.$);
          break;
        case 14:
          this.$ = i[x].trim(), l.setAccTitle(this.$);
          break;
        case 15:
        case 16:
          this.$ = i[x].trim(), l.setAccDescription(this.$);
          break;
        case 17:
          l.addSection(i[x].substr(8)), this.$ = i[x].substr(8);
          break;
        case 19:
          l.addPoint(i[x - 3], i[x - 1], i[x]);
          break;
        case 20:
          l.setXAxisLeftText(i[x - 2]), l.setXAxisRightText(i[x]);
          break;
        case 21:
          i[x - 1].text += " ⟶ ", l.setXAxisLeftText(i[x - 1]);
          break;
        case 22:
          l.setXAxisLeftText(i[x]);
          break;
        case 23:
          l.setYAxisBottomText(i[x - 2]), l.setYAxisTopText(i[x]);
          break;
        case 24:
          i[x - 1].text += " ⟶ ", l.setYAxisBottomText(i[x - 1]);
          break;
        case 25:
          l.setYAxisBottomText(i[x]);
          break;
        case 26:
          l.setQuadrant1Text(i[x]);
          break;
        case 27:
          l.setQuadrant2Text(i[x]);
          break;
        case 28:
          l.setQuadrant3Text(i[x]);
          break;
        case 29:
          l.setQuadrant4Text(i[x]);
          break;
        case 35:
          l.parseDirective("%%{", "open_directive");
          break;
        case 36:
          l.parseDirective(i[x], "type_directive");
          break;
        case 37:
          i[x] = i[x].trim().replace(/'/g, '"'), l.parseDirective(i[x], "arg_directive");
          break;
        case 38:
          l.parseDirective("}%%", "close_directive", "quadrantChart");
          break;
        case 39:
          this.$ = { text: i[x], type: "text" };
          break;
        case 40:
          this.$ = { text: i[x - 1].text + "" + i[x], type: i[x - 1].type };
          break;
        case 41:
          this.$ = { text: i[x], type: "text" };
          break;
        case 42:
          this.$ = { text: i[x], type: "markdown" };
          break;
        case 43:
          this.$ = i[x];
          break;
        case 44:
          this.$ = i[x - 1] + "" + i[x];
          break;
      }
    },
    table: [{ 3: 1, 4: 2, 5: a, 6: 4, 7: h, 33: 9, 38: f, 39: g, 40: u, 41: c }, { 1: [3] }, { 3: 11, 4: 2, 5: a, 6: 4, 7: h, 33: 9, 38: f, 39: g, 40: u, 41: c }, { 3: 12, 4: 2, 5: a, 6: 4, 7: h, 33: 9, 38: f, 39: g, 40: u, 41: c }, { 3: 13, 4: 2, 5: a, 6: 4, 7: h, 33: 9, 38: f, 39: g, 40: u, 41: c }, e(p, [2, 5], { 8: 14 }), e(s, [2, 32]), e(s, [2, 33]), e(s, [2, 34]), { 34: 15, 42: [1, 16] }, { 42: [2, 35] }, { 1: [2, 1] }, { 1: [2, 2] }, { 1: [2, 3] }, e(o, m, { 33: 9, 9: 17, 10: 18, 11: 20, 12: 21, 13: 22, 6: 28, 22: 35, 45: 36, 1: [2, 4], 5: B, 14: V, 16: _, 18: D, 20: b, 21: H, 26: G, 28: Z, 29: at, 30: nt, 31: et, 32: ct, 41: c, 47: N, 48: U, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C }), { 35: 50, 36: [1, 51], 44: mt }, e([36, 44], [2, 36]), e(p, [2, 6]), { 4: 53, 38: f, 39: g, 40: u }, e(o, m, { 33: 9, 11: 20, 12: 21, 13: 22, 6: 28, 22: 35, 45: 36, 10: 54, 5: B, 14: V, 16: _, 18: D, 20: b, 21: H, 26: G, 28: Z, 29: at, 30: nt, 31: et, 32: ct, 41: c, 47: N, 48: U, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C }), e(o, [2, 10]), e(o, [2, 11]), e(o, [2, 12]), { 15: [1, 55] }, { 17: [1, 56] }, { 19: [1, 57] }, e(o, [2, 16]), e(o, [2, 17]), e(o, [2, 18]), { 22: 58, 45: 36, 47: N, 48: U, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C }, { 22: 59, 45: 36, 47: N, 48: U, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C }, { 22: 60, 45: 36, 47: N, 48: U, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C }, { 22: 61, 45: 36, 47: N, 48: U, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C }, { 22: 62, 45: 36, 47: N, 48: U, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C }, { 22: 63, 45: 36, 47: N, 48: U, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C }, { 5: M, 23: [1, 64], 45: 66, 46: 65, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C, 61: X }, e(z, [2, 39]), e(z, [2, 41]), e(z, [2, 42]), e(z, [2, 45]), e(z, [2, 46]), e(z, [2, 47]), e(z, [2, 48]), e(z, [2, 49]), e(z, [2, 50]), e(z, [2, 51]), e(z, [2, 52]), e(z, [2, 53]), e(z, [2, 54]), e(z, [2, 55]), e(ht, [2, 30]), { 37: 69, 43: [1, 70] }, e(ht, [2, 38]), e(p, [2, 7]), e(o, [2, 9]), e(o, [2, 13]), e(o, [2, 14]), e(o, [2, 15]), e(o, [2, 22], { 46: 65, 45: 66, 5: M, 27: [1, 71], 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C, 61: X }), e(o, [2, 25], { 46: 65, 45: 66, 5: M, 27: [1, 72], 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C, 61: X }), e(o, [2, 26], { 46: 65, 45: 66, 5: M, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C, 61: X }), e(o, [2, 27], { 46: 65, 45: 66, 5: M, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C, 61: X }), e(o, [2, 28], { 46: 65, 45: 66, 5: M, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C, 61: X }), e(o, [2, 29], { 46: 65, 45: 66, 5: M, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C, 61: X }), { 24: [1, 73] }, e(z, [2, 40]), e(z, [2, 56]), e(z, [2, 57]), e(z, [2, 58]), { 35: 74, 44: mt }, { 44: [2, 37] }, e(o, [2, 21], { 45: 36, 22: 75, 47: N, 48: U, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C }), e(o, [2, 24], { 45: 36, 22: 76, 47: N, 48: U, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C }), { 25: [1, 77] }, e(ht, [2, 31]), e(o, [2, 20], { 46: 65, 45: 66, 5: M, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C, 61: X }), e(o, [2, 23], { 46: 65, 45: 66, 5: M, 50: q, 51: T, 52: t, 53: A, 54: S, 55: k, 56: F, 57: v, 58: P, 59: L, 60: C, 61: X }), e(o, [2, 19])],
    defaultActions: { 10: [2, 35], 11: [2, 1], 12: [2, 2], 13: [2, 3], 70: [2, 37] },
    parseError: function(n, r) {
      if (r.recoverable)
        this.trace(n);
      else {
        var d = new Error(n);
        throw d.hash = r, d;
      }
    },
    parse: function(n) {
      var r = this, d = [0], l = [], y = [null], i = [], it = this.table, x = "", rt = 0, _t = 0, vt = 2, bt = 1, Pt = i.slice.call(arguments, 1), E = Object.create(this.lexer), J = { yy: {} };
      for (var xt in this.yy)
        Object.prototype.hasOwnProperty.call(this.yy, xt) && (J.yy[xt] = this.yy[xt]);
      E.setInput(n, J.yy), J.yy.lexer = E, J.yy.parser = this, typeof E.yylloc > "u" && (E.yylloc = {});
      var ft = E.yylloc;
      i.push(ft);
      var Lt = E.options && E.options.ranges;
      typeof J.yy.parseError == "function" ? this.parseError = J.yy.parseError : this.parseError = Object.getPrototypeOf(this).parseError;
      function Ct() {
        var Y;
        return Y = l.pop() || E.lex() || bt, typeof Y != "number" && (Y instanceof Array && (l = Y, Y = l.pop()), Y = r.symbols_[Y] || Y), Y;
      }
      for (var W, $, Q, gt, tt = {}, st, O, At, ot; ; ) {
        if ($ = d[d.length - 1], this.defaultActions[$] ? Q = this.defaultActions[$] : ((W === null || typeof W > "u") && (W = Ct()), Q = it[$] && it[$][W]), typeof Q > "u" || !Q.length || !Q[0]) {
          var pt = "";
          ot = [];
          for (st in it[$])
            this.terminals_[st] && st > vt && ot.push("'" + this.terminals_[st] + "'");
          E.showPosition ? pt = "Parse error on line " + (rt + 1) + `:
` + E.showPosition() + `
Expecting ` + ot.join(", ") + ", got '" + (this.terminals_[W] || W) + "'" : pt = "Parse error on line " + (rt + 1) + ": Unexpected " + (W == bt ? "end of input" : "'" + (this.terminals_[W] || W) + "'"), this.parseError(pt, {
            text: E.match,
            token: this.terminals_[W] || W,
            line: E.yylineno,
            loc: ft,
            expected: ot
          });
        }
        if (Q[0] instanceof Array && Q.length > 1)
          throw new Error("Parse Error: multiple actions possible at state: " + $ + ", token: " + W);
        switch (Q[0]) {
          case 1:
            d.push(W), y.push(E.yytext), i.push(E.yylloc), d.push(Q[1]), W = null, _t = E.yyleng, x = E.yytext, rt = E.yylineno, ft = E.yylloc;
            break;
          case 2:
            if (O = this.productions_[Q[1]][1], tt.$ = y[y.length - O], tt._$ = {
              first_line: i[i.length - (O || 1)].first_line,
              last_line: i[i.length - 1].last_line,
              first_column: i[i.length - (O || 1)].first_column,
              last_column: i[i.length - 1].last_column
            }, Lt && (tt._$.range = [
              i[i.length - (O || 1)].range[0],
              i[i.length - 1].range[1]
            ]), gt = this.performAction.apply(tt, [
              x,
              _t,
              rt,
              J.yy,
              Q[1],
              y,
              i
            ].concat(Pt)), typeof gt < "u")
              return gt;
            O && (d = d.slice(0, -1 * O * 2), y = y.slice(0, -1 * O), i = i.slice(0, -1 * O)), d.push(this.productions_[Q[1]][0]), y.push(tt.$), i.push(tt._$), At = it[d[d.length - 2]][d[d.length - 1]], d.push(At);
            break;
          case 3:
            return !0;
        }
      }
      return !0;
    }
  }, Ft = function() {
    var K = {
      EOF: 1,
      parseError: function(r, d) {
        if (this.yy.parser)
          this.yy.parser.parseError(r, d);
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
        var r = n.length, d = n.split(/(?:\r\n?|\n)/g);
        this._input = n + this._input, this.yytext = this.yytext.substr(0, this.yytext.length - r), this.offset -= r;
        var l = this.match.split(/(?:\r\n?|\n)/g);
        this.match = this.match.substr(0, this.match.length - 1), this.matched = this.matched.substr(0, this.matched.length - 1), d.length - 1 && (this.yylineno -= d.length - 1);
        var y = this.yylloc.range;
        return this.yylloc = {
          first_line: this.yylloc.first_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.first_column,
          last_column: d ? (d.length === l.length ? this.yylloc.first_column : 0) + l[l.length - d.length].length - d[0].length : this.yylloc.first_column - r
        }, this.options.ranges && (this.yylloc.range = [y[0], y[0] + this.yyleng - r]), this.yyleng = this.yytext.length, this;
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
        var d, l, y;
        if (this.options.backtrack_lexer && (y = {
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
        }, this.options.ranges && (y.yylloc.range = this.yylloc.range.slice(0))), l = n[0].match(/(?:\r\n?|\n).*/g), l && (this.yylineno += l.length), this.yylloc = {
          first_line: this.yylloc.last_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.last_column,
          last_column: l ? l[l.length - 1].length - l[l.length - 1].match(/\r?\n?/)[0].length : this.yylloc.last_column + n[0].length
        }, this.yytext += n[0], this.match += n[0], this.matches = n, this.yyleng = this.yytext.length, this.options.ranges && (this.yylloc.range = [this.offset, this.offset += this.yyleng]), this._more = !1, this._backtrack = !1, this._input = this._input.slice(n[0].length), this.matched += n[0], d = this.performAction.call(this, this.yy, this, r, this.conditionStack[this.conditionStack.length - 1]), this.done && this._input && (this.done = !1), d)
          return d;
        if (this._backtrack) {
          for (var i in y)
            this[i] = y[i];
          return !1;
        }
        return !1;
      },
      // return next match in input
      next: function() {
        if (this.done)
          return this.EOF;
        this._input || (this.done = !0);
        var n, r, d, l;
        this._more || (this.yytext = "", this.match = "");
        for (var y = this._currentRules(), i = 0; i < y.length; i++)
          if (d = this._input.match(this.rules[y[i]]), d && (!r || d[0].length > r[0].length)) {
            if (r = d, l = i, this.options.backtrack_lexer) {
              if (n = this.test_match(d, y[i]), n !== !1)
                return n;
              if (this._backtrack) {
                r = !1;
                continue;
              } else
                return !1;
            } else if (!this.options.flex)
              break;
          }
        return r ? (n = this.test_match(r, y[l]), n !== !1 ? n : !1) : this._input === "" ? this.EOF : this.parseError("Lexical error on line " + (this.yylineno + 1) + `. Unrecognized text.
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
      performAction: function(r, d, l, y) {
        switch (l) {
          case 0:
            return this.begin("open_directive"), 41;
          case 1:
            return this.begin("type_directive"), 42;
          case 2:
            return this.popState(), this.begin("arg_directive"), 36;
          case 3:
            return this.popState(), this.popState(), 44;
          case 4:
            return 43;
          case 5:
            break;
          case 6:
            break;
          case 7:
            return 38;
          case 8:
            break;
          case 9:
            return this.begin("title"), 14;
          case 10:
            return this.popState(), "title_value";
          case 11:
            return this.begin("acc_title"), 16;
          case 12:
            return this.popState(), "acc_title_value";
          case 13:
            return this.begin("acc_descr"), 18;
          case 14:
            return this.popState(), "acc_descr_value";
          case 15:
            this.begin("acc_descr_multiline");
            break;
          case 16:
            this.popState();
            break;
          case 17:
            return "acc_descr_multiline_value";
          case 18:
            return 26;
          case 19:
            return 28;
          case 20:
            return 27;
          case 21:
            return 29;
          case 22:
            return 30;
          case 23:
            return 31;
          case 24:
            return 32;
          case 25:
            this.begin("md_string");
            break;
          case 26:
            return "MD_STR";
          case 27:
            this.popState();
            break;
          case 28:
            this.begin("string");
            break;
          case 29:
            this.popState();
            break;
          case 30:
            return "STR";
          case 31:
            return this.begin("point_start"), 23;
          case 32:
            return this.begin("point_x"), 24;
          case 33:
            this.popState();
            break;
          case 34:
            this.popState(), this.begin("point_y");
            break;
          case 35:
            return this.popState(), 25;
          case 36:
            return 7;
          case 37:
            return 53;
          case 38:
            return "COLON";
          case 39:
            return 55;
          case 40:
            return 54;
          case 41:
            return 56;
          case 42:
            return 56;
          case 43:
            return 57;
          case 44:
            return 59;
          case 45:
            return 60;
          case 46:
            return 58;
          case 47:
            return 51;
          case 48:
            return 61;
          case 49:
            return 52;
          case 50:
            return 5;
          case 51:
            return 39;
          case 52:
            return 50;
          case 53:
            return 40;
        }
      },
      rules: [/^(?:%%\{)/i, /^(?:((?:(?!\}%%)[^:.])*))/i, /^(?::)/i, /^(?:\}%%)/i, /^(?:((?:(?!\}%%).|\n)*))/i, /^(?:%%(?!\{)[^\n]*)/i, /^(?:[^\}]%%[^\n]*)/i, /^(?:[\n\r]+)/i, /^(?:%%[^\n]*)/i, /^(?:title\b)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accTitle\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*\{\s*)/i, /^(?:[\}])/i, /^(?:[^\}]*)/i, /^(?: *x-axis *)/i, /^(?: *y-axis *)/i, /^(?: *--+> *)/i, /^(?: *quadrant-1 *)/i, /^(?: *quadrant-2 *)/i, /^(?: *quadrant-3 *)/i, /^(?: *quadrant-4 *)/i, /^(?:["][`])/i, /^(?:[^`"]+)/i, /^(?:[`]["])/i, /^(?:["])/i, /^(?:["])/i, /^(?:[^"]*)/i, /^(?:\s*:\s*\[\s*)/i, /^(?:(1)|(0(.\d+)?))/i, /^(?:\s*\] *)/i, /^(?:\s*,\s*)/i, /^(?:(1)|(0(.\d+)?))/i, /^(?: *quadrantChart *)/i, /^(?:[A-Za-z]+)/i, /^(?::)/i, /^(?:\+)/i, /^(?:,)/i, /^(?:=)/i, /^(?:=)/i, /^(?:\*)/i, /^(?:#)/i, /^(?:[\_])/i, /^(?:\.)/i, /^(?:&)/i, /^(?:-)/i, /^(?:[0-9]+)/i, /^(?:\s)/i, /^(?:;)/i, /^(?:[!"#$%&'*+,-.`?\\_/])/i, /^(?:$)/i],
      conditions: { point_y: { rules: [35], inclusive: !1 }, point_x: { rules: [34], inclusive: !1 }, point_start: { rules: [32, 33], inclusive: !1 }, acc_descr_multiline: { rules: [16, 17], inclusive: !1 }, acc_descr: { rules: [14], inclusive: !1 }, acc_title: { rules: [12], inclusive: !1 }, close_directive: { rules: [], inclusive: !1 }, arg_directive: { rules: [3, 4], inclusive: !1 }, type_directive: { rules: [2, 3], inclusive: !1 }, open_directive: { rules: [1], inclusive: !1 }, title: { rules: [10], inclusive: !1 }, md_string: { rules: [26, 27], inclusive: !1 }, string: { rules: [29, 30], inclusive: !1 }, INITIAL: { rules: [0, 5, 6, 7, 8, 9, 11, 13, 15, 18, 19, 20, 21, 22, 23, 24, 25, 28, 31, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53], inclusive: !0 } }
    };
    return K;
  }();
  dt.lexer = Ft;
  function ut() {
    this.yy = {};
  }
  return ut.prototype = dt, dt.Parser = ut, new ut();
}();
qt.parser = qt;
const Ut = qt, R = Dt();
class Qt {
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
    var a, h, f, g, u, c, p, s, o, m, B, V, _, D, b, H, G, Z;
    return {
      showXAxis: !0,
      showYAxis: !0,
      showTitle: !0,
      chartHeight: ((a = I.quadrantChart) == null ? void 0 : a.chartWidth) || 500,
      chartWidth: ((h = I.quadrantChart) == null ? void 0 : h.chartHeight) || 500,
      titlePadding: ((f = I.quadrantChart) == null ? void 0 : f.titlePadding) || 10,
      titleFontSize: ((g = I.quadrantChart) == null ? void 0 : g.titleFontSize) || 20,
      quadrantPadding: ((u = I.quadrantChart) == null ? void 0 : u.quadrantPadding) || 5,
      xAxisLabelPadding: ((c = I.quadrantChart) == null ? void 0 : c.xAxisLabelPadding) || 5,
      yAxisLabelPadding: ((p = I.quadrantChart) == null ? void 0 : p.yAxisLabelPadding) || 5,
      xAxisLabelFontSize: ((s = I.quadrantChart) == null ? void 0 : s.xAxisLabelFontSize) || 16,
      yAxisLabelFontSize: ((o = I.quadrantChart) == null ? void 0 : o.yAxisLabelFontSize) || 16,
      quadrantLabelFontSize: ((m = I.quadrantChart) == null ? void 0 : m.quadrantLabelFontSize) || 16,
      quadrantTextTopPadding: ((B = I.quadrantChart) == null ? void 0 : B.quadrantTextTopPadding) || 5,
      pointTextPadding: ((V = I.quadrantChart) == null ? void 0 : V.pointTextPadding) || 5,
      pointLabelFontSize: ((_ = I.quadrantChart) == null ? void 0 : _.pointLabelFontSize) || 12,
      pointRadius: ((D = I.quadrantChart) == null ? void 0 : D.pointRadius) || 5,
      xAxisPosition: ((b = I.quadrantChart) == null ? void 0 : b.xAxisPosition) || "top",
      yAxisPosition: ((H = I.quadrantChart) == null ? void 0 : H.yAxisPosition) || "left",
      quadrantInternalBorderStrokeWidth: ((G = I.quadrantChart) == null ? void 0 : G.quadrantInternalBorderStrokeWidth) || 1,
      quadrantExternalBorderStrokeWidth: ((Z = I.quadrantChart) == null ? void 0 : Z.quadrantExternalBorderStrokeWidth) || 2
    };
  }
  getDefaultThemeConfig() {
    return {
      quadrant1Fill: R.quadrant1Fill,
      quadrant2Fill: R.quadrant2Fill,
      quadrant3Fill: R.quadrant3Fill,
      quadrant4Fill: R.quadrant4Fill,
      quadrant1TextFill: R.quadrant1TextFill,
      quadrant2TextFill: R.quadrant2TextFill,
      quadrant3TextFill: R.quadrant3TextFill,
      quadrant4TextFill: R.quadrant4TextFill,
      quadrantPointFill: R.quadrantPointFill,
      quadrantPointTextFill: R.quadrantPointTextFill,
      quadrantXAxisTextFill: R.quadrantXAxisTextFill,
      quadrantYAxisTextFill: R.quadrantYAxisTextFill,
      quadrantTitleFill: R.quadrantTitleFill,
      quadrantInternalBorderStrokeFill: R.quadrantInternalBorderStrokeFill,
      quadrantExternalBorderStrokeFill: R.quadrantExternalBorderStrokeFill
    };
  }
  clear() {
    this.config = this.getDefaultConfig(), this.themeConfig = this.getDefaultThemeConfig(), this.data = this.getDefaultData(), lt.info("clear called");
  }
  setData(a) {
    this.data = { ...this.data, ...a };
  }
  addPoints(a) {
    this.data.points = [...a, ...this.data.points];
  }
  setConfig(a) {
    lt.trace("setConfig called with: ", a), this.config = { ...this.config, ...a };
  }
  setThemeConfig(a) {
    lt.trace("setThemeConfig called with: ", a), this.themeConfig = { ...this.themeConfig, ...a };
  }
  calculateSpace(a, h, f, g) {
    const u = this.config.xAxisLabelPadding * 2 + this.config.xAxisLabelFontSize, c = {
      top: a === "top" && h ? u : 0,
      bottom: a === "bottom" && h ? u : 0
    }, p = this.config.yAxisLabelPadding * 2 + this.config.yAxisLabelFontSize, s = {
      left: this.config.yAxisPosition === "left" && f ? p : 0,
      right: this.config.yAxisPosition === "right" && f ? p : 0
    }, o = this.config.titleFontSize + this.config.titlePadding * 2, m = {
      top: g ? o : 0
    }, B = this.config.quadrantPadding + s.left, V = this.config.quadrantPadding + c.top + m.top, _ = this.config.chartWidth - this.config.quadrantPadding * 2 - s.left - s.right, D = this.config.chartHeight - this.config.quadrantPadding * 2 - c.top - c.bottom - m.top, b = _ / 2, H = D / 2;
    return {
      xAxisSpace: c,
      yAxisSpace: s,
      titleSpace: m,
      quadrantSpace: {
        quadrantLeft: B,
        quadrantTop: V,
        quadrantWidth: _,
        quadrantHalfWidth: b,
        quadrantHeight: D,
        quadrantHalfHeight: H
      }
    };
  }
  getAxisLabels(a, h, f, g) {
    const { quadrantSpace: u, titleSpace: c } = g, {
      quadrantHalfHeight: p,
      quadrantHeight: s,
      quadrantLeft: o,
      quadrantHalfWidth: m,
      quadrantTop: B,
      quadrantWidth: V
    } = u, _ = this.data.points.length === 0, D = [];
    return this.data.xAxisLeftText && h && D.push({
      text: this.data.xAxisLeftText,
      fill: this.themeConfig.quadrantXAxisTextFill,
      x: o + (_ ? m / 2 : 0),
      y: a === "top" ? this.config.xAxisLabelPadding + c.top : this.config.xAxisLabelPadding + B + s + this.config.quadrantPadding,
      fontSize: this.config.xAxisLabelFontSize,
      verticalPos: _ ? "center" : "left",
      horizontalPos: "top",
      rotation: 0
    }), this.data.xAxisRightText && h && D.push({
      text: this.data.xAxisRightText,
      fill: this.themeConfig.quadrantXAxisTextFill,
      x: o + m + (_ ? m / 2 : 0),
      y: a === "top" ? this.config.xAxisLabelPadding + c.top : this.config.xAxisLabelPadding + B + s + this.config.quadrantPadding,
      fontSize: this.config.xAxisLabelFontSize,
      verticalPos: _ ? "center" : "left",
      horizontalPos: "top",
      rotation: 0
    }), this.data.yAxisBottomText && f && D.push({
      text: this.data.yAxisBottomText,
      fill: this.themeConfig.quadrantYAxisTextFill,
      x: this.config.yAxisPosition === "left" ? this.config.yAxisLabelPadding : this.config.yAxisLabelPadding + o + V + this.config.quadrantPadding,
      y: B + s - (_ ? p / 2 : 0),
      fontSize: this.config.yAxisLabelFontSize,
      verticalPos: _ ? "center" : "left",
      horizontalPos: "top",
      rotation: -90
    }), this.data.yAxisTopText && f && D.push({
      text: this.data.yAxisTopText,
      fill: this.themeConfig.quadrantYAxisTextFill,
      x: this.config.yAxisPosition === "left" ? this.config.yAxisLabelPadding : this.config.yAxisLabelPadding + o + V + this.config.quadrantPadding,
      y: B + p - (_ ? p / 2 : 0),
      fontSize: this.config.yAxisLabelFontSize,
      verticalPos: _ ? "center" : "left",
      horizontalPos: "top",
      rotation: -90
    }), D;
  }
  getQuadrants(a) {
    const { quadrantSpace: h } = a, { quadrantHalfHeight: f, quadrantLeft: g, quadrantHalfWidth: u, quadrantTop: c } = h, p = [
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
        x: g + u,
        y: c,
        width: u,
        height: f,
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
        x: g,
        y: c,
        width: u,
        height: f,
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
        x: g,
        y: c + f,
        width: u,
        height: f,
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
        x: g + u,
        y: c + f,
        width: u,
        height: f,
        fill: this.themeConfig.quadrant4Fill
      }
    ];
    for (const s of p)
      s.text.x = s.x + s.width / 2, this.data.points.length === 0 ? (s.text.y = s.y + s.height / 2, s.text.horizontalPos = "middle") : (s.text.y = s.y + this.config.quadrantTextTopPadding, s.text.horizontalPos = "top");
    return p;
  }
  getQuadrantPoints(a) {
    const { quadrantSpace: h } = a, { quadrantHeight: f, quadrantLeft: g, quadrantTop: u, quadrantWidth: c } = h, p = St().domain([0, 1]).range([g, c + g]), s = St().domain([0, 1]).range([f + u, u]);
    return this.data.points.map((m) => ({
      x: p(m.x),
      y: s(m.y),
      fill: this.themeConfig.quadrantPointFill,
      radius: this.config.pointRadius,
      text: {
        text: m.text,
        fill: this.themeConfig.quadrantPointTextFill,
        x: p(m.x),
        y: s(m.y) + this.config.pointTextPadding,
        verticalPos: "center",
        horizontalPos: "top",
        fontSize: this.config.pointLabelFontSize,
        rotation: 0
      }
    }));
  }
  getBorders(a) {
    const h = this.config.quadrantExternalBorderStrokeWidth / 2, { quadrantSpace: f } = a, {
      quadrantHalfHeight: g,
      quadrantHeight: u,
      quadrantLeft: c,
      quadrantHalfWidth: p,
      quadrantTop: s,
      quadrantWidth: o
    } = f;
    return [
      // top border
      {
        strokeFill: this.themeConfig.quadrantExternalBorderStrokeFill,
        strokeWidth: this.config.quadrantExternalBorderStrokeWidth,
        x1: c - h,
        y1: s,
        x2: c + o + h,
        y2: s
      },
      // right border
      {
        strokeFill: this.themeConfig.quadrantExternalBorderStrokeFill,
        strokeWidth: this.config.quadrantExternalBorderStrokeWidth,
        x1: c + o,
        y1: s + h,
        x2: c + o,
        y2: s + u - h
      },
      // bottom border
      {
        strokeFill: this.themeConfig.quadrantExternalBorderStrokeFill,
        strokeWidth: this.config.quadrantExternalBorderStrokeWidth,
        x1: c - h,
        y1: s + u,
        x2: c + o + h,
        y2: s + u
      },
      // left border
      {
        strokeFill: this.themeConfig.quadrantExternalBorderStrokeFill,
        strokeWidth: this.config.quadrantExternalBorderStrokeWidth,
        x1: c,
        y1: s + h,
        x2: c,
        y2: s + u - h
      },
      // vertical inner border
      {
        strokeFill: this.themeConfig.quadrantInternalBorderStrokeFill,
        strokeWidth: this.config.quadrantInternalBorderStrokeWidth,
        x1: c + p,
        y1: s + h,
        x2: c + p,
        y2: s + u - h
      },
      // horizontal inner border
      {
        strokeFill: this.themeConfig.quadrantInternalBorderStrokeFill,
        strokeWidth: this.config.quadrantInternalBorderStrokeWidth,
        x1: c + h,
        y1: s + g,
        x2: c + o - h,
        y2: s + g
      }
    ];
  }
  getTitle(a) {
    if (a)
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
    const a = this.config.showXAxis && !!(this.data.xAxisLeftText || this.data.xAxisRightText), h = this.config.showYAxis && !!(this.data.yAxisTopText || this.data.yAxisBottomText), f = this.config.showTitle && !!this.data.titleText, g = this.data.points.length > 0 ? "bottom" : this.config.xAxisPosition, u = this.calculateSpace(g, a, h, f);
    return {
      points: this.getQuadrantPoints(u),
      quadrants: this.getQuadrants(u),
      axisLabels: this.getAxisLabels(g, a, h, u),
      borderLines: this.getBorders(u),
      title: this.getTitle(f)
    };
  }
}
const Ht = Tt();
function j(e) {
  return Wt(e.trim(), Ht);
}
const w = new Qt();
function Mt(e) {
  w.setData({ quadrant1Text: j(e.text) });
}
function Xt(e) {
  w.setData({ quadrant2Text: j(e.text) });
}
function Ot(e) {
  w.setData({ quadrant3Text: j(e.text) });
}
function Yt(e) {
  w.setData({ quadrant4Text: j(e.text) });
}
function jt(e) {
  w.setData({ xAxisLeftText: j(e.text) });
}
function Gt(e) {
  w.setData({ xAxisRightText: j(e.text) });
}
function Kt(e) {
  w.setData({ yAxisTopText: j(e.text) });
}
function Zt(e) {
  w.setData({ yAxisBottomText: j(e.text) });
}
function Jt(e, a, h) {
  w.addPoints([{ x: a, y: h, text: j(e.text) }]);
}
function $t(e) {
  w.setConfig({ chartWidth: e });
}
function te(e) {
  w.setConfig({ chartHeight: e });
}
function ee() {
  const e = Tt(), { themeVariables: a, quadrantChart: h } = e;
  return h && w.setConfig(h), w.setThemeConfig({
    quadrant1Fill: a.quadrant1Fill,
    quadrant2Fill: a.quadrant2Fill,
    quadrant3Fill: a.quadrant3Fill,
    quadrant4Fill: a.quadrant4Fill,
    quadrant1TextFill: a.quadrant1TextFill,
    quadrant2TextFill: a.quadrant2TextFill,
    quadrant3TextFill: a.quadrant3TextFill,
    quadrant4TextFill: a.quadrant4TextFill,
    quadrantPointFill: a.quadrantPointFill,
    quadrantPointTextFill: a.quadrantPointTextFill,
    quadrantXAxisTextFill: a.quadrantXAxisTextFill,
    quadrantYAxisTextFill: a.quadrantYAxisTextFill,
    quadrantExternalBorderStrokeFill: a.quadrantExternalBorderStrokeFill,
    quadrantInternalBorderStrokeFill: a.quadrantInternalBorderStrokeFill,
    quadrantTitleFill: a.quadrantTitleFill
  }), w.setData({ titleText: kt() }), w.build();
}
const ie = function(e, a, h) {
  wt.parseDirective(this, e, a, h);
}, ae = function() {
  w.clear(), Rt();
}, ne = {
  setWidth: $t,
  setHeight: te,
  setQuadrant1Text: Mt,
  setQuadrant2Text: Xt,
  setQuadrant3Text: Ot,
  setQuadrant4Text: Yt,
  setXAxisLeftText: jt,
  setXAxisRightText: Gt,
  setYAxisTopText: Kt,
  setYAxisBottomText: Zt,
  addPoint: Jt,
  getQuadrantData: ee,
  parseDirective: ie,
  clear: ae,
  setAccTitle: zt,
  getAccTitle: Et,
  setDiagramTitle: It,
  getDiagramTitle: kt,
  getAccDescription: Bt,
  setAccDescription: Vt
}, re = (e, a, h, f) => {
  var U, q, T;
  function g(t) {
    return t === "top" ? "hanging" : "middle";
  }
  function u(t) {
    return t === "left" ? "start" : "middle";
  }
  function c(t) {
    return `translate(${t.x}, ${t.y}) rotate(${t.rotation || 0})`;
  }
  const p = Tt();
  lt.debug(`Rendering quadrant chart
` + e);
  const s = p.securityLevel;
  let o;
  s === "sandbox" && (o = yt("#i" + a));
  const B = (s === "sandbox" ? yt(o.nodes()[0].contentDocument.body) : yt("body")).select(`[id="${a}"]`), V = B.append("g").attr("class", "main"), _ = ((U = p.quadrantChart) == null ? void 0 : U.chartWidth) || 500, D = ((q = p.quadrantChart) == null ? void 0 : q.chartHeight) || 500;
  Nt(B, D, _, ((T = p.quadrantChart) == null ? void 0 : T.useMaxWidth) || !0), B.attr("viewBox", "0 0 " + _ + " " + D), f.db.setHeight(D), f.db.setWidth(_);
  const b = f.db.getQuadrantData(), H = V.append("g").attr("class", "quadrants"), G = V.append("g").attr("class", "border"), Z = V.append("g").attr("class", "data-points"), at = V.append("g").attr("class", "labels"), nt = V.append("g").attr("class", "title");
  b.title && nt.append("text").attr("x", 0).attr("y", 0).attr("fill", b.title.fill).attr("font-size", b.title.fontSize).attr("dominant-baseline", g(b.title.horizontalPos)).attr("text-anchor", u(b.title.verticalPos)).attr("transform", c(b.title)).text(b.title.text), b.borderLines && G.selectAll("line").data(b.borderLines).enter().append("line").attr("x1", (t) => t.x1).attr("y1", (t) => t.y1).attr("x2", (t) => t.x2).attr("y2", (t) => t.y2).style("stroke", (t) => t.strokeFill).style("stroke-width", (t) => t.strokeWidth);
  const et = H.selectAll("g.quadrant").data(b.quadrants).enter().append("g").attr("class", "quadrant");
  et.append("rect").attr("x", (t) => t.x).attr("y", (t) => t.y).attr("width", (t) => t.width).attr("height", (t) => t.height).attr("fill", (t) => t.fill), et.append("text").attr("x", 0).attr("y", 0).attr("fill", (t) => t.text.fill).attr("font-size", (t) => t.text.fontSize).attr(
    "dominant-baseline",
    (t) => g(t.text.horizontalPos)
  ).attr("text-anchor", (t) => u(t.text.verticalPos)).attr("transform", (t) => c(t.text)).text((t) => t.text.text), at.selectAll("g.label").data(b.axisLabels).enter().append("g").attr("class", "label").append("text").attr("x", 0).attr("y", 0).text((t) => t.text).attr("fill", (t) => t.fill).attr("font-size", (t) => t.fontSize).attr("dominant-baseline", (t) => g(t.horizontalPos)).attr("text-anchor", (t) => u(t.verticalPos)).attr("transform", (t) => c(t));
  const N = Z.selectAll("g.data-point").data(b.points).enter().append("g").attr("class", "data-point");
  N.append("circle").attr("cx", (t) => t.x).attr("cy", (t) => t.y).attr("r", (t) => t.radius).attr("fill", (t) => t.fill), N.append("text").attr("x", 0).attr("y", 0).text((t) => t.text.text).attr("fill", (t) => t.text.fill).attr("font-size", (t) => t.text.fontSize).attr(
    "dominant-baseline",
    (t) => g(t.text.horizontalPos)
  ).attr("text-anchor", (t) => u(t.text.verticalPos)).attr("transform", (t) => c(t.text));
}, se = {
  draw: re
}, he = {
  parser: Ut,
  db: ne,
  renderer: se,
  styles: () => ""
};
export {
  he as diagram
};
