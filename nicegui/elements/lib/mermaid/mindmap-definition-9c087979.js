import { b as yp, g as sn, l as qr, f as nn, H as Ca, J as mp, K as bp, L as Ep } from "./config-e567ef17.js";
import { s as wp } from "./setupGraphViewbox-a4603a92.js";
import { i as xp } from "./is_dark-151801f4.js";
var Ki = function() {
  var fe = function(ee, H, te, S) {
    for (te = te || {}, S = ee.length; S--; te[ee[S]] = H)
      ;
    return te;
  }, he = [1, 4], Q = [1, 13], ce = [1, 12], Y = [1, 15], A = [1, 16], T = [1, 20], w = [1, 19], L = [6, 7, 8], G = [1, 26], U = [1, 24], P = [1, 25], K = [6, 7, 11], D = [1, 6, 13, 15, 16, 19, 22], V = [1, 33], _ = [1, 34], J = [1, 6, 7, 11, 13, 15, 16, 19, 22], ne = {
    trace: function() {
    },
    yy: {},
    symbols_: { error: 2, start: 3, mindMap: 4, spaceLines: 5, SPACELINE: 6, NL: 7, MINDMAP: 8, document: 9, stop: 10, EOF: 11, statement: 12, SPACELIST: 13, node: 14, ICON: 15, CLASS: 16, nodeWithId: 17, nodeWithoutId: 18, NODE_DSTART: 19, NODE_DESCR: 20, NODE_DEND: 21, NODE_ID: 22, $accept: 0, $end: 1 },
    terminals_: { 2: "error", 6: "SPACELINE", 7: "NL", 8: "MINDMAP", 11: "EOF", 13: "SPACELIST", 15: "ICON", 16: "CLASS", 19: "NODE_DSTART", 20: "NODE_DESCR", 21: "NODE_DEND", 22: "NODE_ID" },
    productions_: [0, [3, 1], [3, 2], [5, 1], [5, 2], [5, 2], [4, 2], [4, 3], [10, 1], [10, 1], [10, 1], [10, 2], [10, 2], [9, 3], [9, 2], [12, 2], [12, 2], [12, 2], [12, 1], [12, 1], [12, 1], [12, 1], [12, 1], [14, 1], [14, 1], [18, 3], [17, 1], [17, 4]],
    performAction: function(H, te, S, $, k, q, ve) {
      var pe = q.length - 1;
      switch (k) {
        case 6:
        case 7:
          return $;
        case 8:
          $.getLogger().trace("Stop NL ");
          break;
        case 9:
          $.getLogger().trace("Stop EOF ");
          break;
        case 11:
          $.getLogger().trace("Stop NL2 ");
          break;
        case 12:
          $.getLogger().trace("Stop EOF2 ");
          break;
        case 15:
          $.getLogger().info("Node: ", q[pe].id), $.addNode(q[pe - 1].length, q[pe].id, q[pe].descr, q[pe].type);
          break;
        case 16:
          $.getLogger().trace("Icon: ", q[pe]), $.decorateNode({ icon: q[pe] });
          break;
        case 17:
        case 21:
          $.decorateNode({ class: q[pe] });
          break;
        case 18:
          $.getLogger().trace("SPACELIST");
          break;
        case 19:
          $.getLogger().trace("Node: ", q[pe].id), $.addNode(0, q[pe].id, q[pe].descr, q[pe].type);
          break;
        case 20:
          $.decorateNode({ icon: q[pe] });
          break;
        case 25:
          $.getLogger().trace("node found ..", q[pe - 2]), this.$ = { id: q[pe - 1], descr: q[pe - 1], type: $.getType(q[pe - 2], q[pe]) };
          break;
        case 26:
          this.$ = { id: q[pe], descr: q[pe], type: $.nodeType.DEFAULT };
          break;
        case 27:
          $.getLogger().trace("node found ..", q[pe - 3]), this.$ = { id: q[pe - 3], descr: q[pe - 1], type: $.getType(q[pe - 2], q[pe]) };
          break;
      }
    },
    table: [{ 3: 1, 4: 2, 5: 3, 6: [1, 5], 8: he }, { 1: [3] }, { 1: [2, 1] }, { 4: 6, 6: [1, 7], 7: [1, 8], 8: he }, { 6: Q, 7: [1, 10], 9: 9, 12: 11, 13: ce, 14: 14, 15: Y, 16: A, 17: 17, 18: 18, 19: T, 22: w }, fe(L, [2, 3]), { 1: [2, 2] }, fe(L, [2, 4]), fe(L, [2, 5]), { 1: [2, 6], 6: Q, 12: 21, 13: ce, 14: 14, 15: Y, 16: A, 17: 17, 18: 18, 19: T, 22: w }, { 6: Q, 9: 22, 12: 11, 13: ce, 14: 14, 15: Y, 16: A, 17: 17, 18: 18, 19: T, 22: w }, { 6: G, 7: U, 10: 23, 11: P }, fe(K, [2, 22], { 17: 17, 18: 18, 14: 27, 15: [1, 28], 16: [1, 29], 19: T, 22: w }), fe(K, [2, 18]), fe(K, [2, 19]), fe(K, [2, 20]), fe(K, [2, 21]), fe(K, [2, 23]), fe(K, [2, 24]), fe(K, [2, 26], { 19: [1, 30] }), { 20: [1, 31] }, { 6: G, 7: U, 10: 32, 11: P }, { 1: [2, 7], 6: Q, 12: 21, 13: ce, 14: 14, 15: Y, 16: A, 17: 17, 18: 18, 19: T, 22: w }, fe(D, [2, 14], { 7: V, 11: _ }), fe(J, [2, 8]), fe(J, [2, 9]), fe(J, [2, 10]), fe(K, [2, 15]), fe(K, [2, 16]), fe(K, [2, 17]), { 20: [1, 35] }, { 21: [1, 36] }, fe(D, [2, 13], { 7: V, 11: _ }), fe(J, [2, 11]), fe(J, [2, 12]), { 21: [1, 37] }, fe(K, [2, 25]), fe(K, [2, 27])],
    defaultActions: { 2: [2, 1], 6: [2, 2] },
    parseError: function(H, te) {
      if (te.recoverable)
        this.trace(H);
      else {
        var S = new Error(H);
        throw S.hash = te, S;
      }
    },
    parse: function(H) {
      var te = this, S = [0], $ = [], k = [null], q = [], ve = this.table, pe = "", Ae = 0, Ne = 0, _e = 2, tt = 1, ct = q.slice.call(arguments, 1), Pe = Object.create(this.lexer), $e = { yy: {} };
      for (var Xe in this.yy)
        Object.prototype.hasOwnProperty.call(this.yy, Xe) && ($e.yy[Xe] = this.yy[Xe]);
      Pe.setInput(H, $e.yy), $e.yy.lexer = Pe, $e.yy.parser = this, typeof Pe.yylloc > "u" && (Pe.yylloc = {});
      var rt = Pe.yylloc;
      q.push(rt);
      var lt = Pe.options && Pe.options.ranges;
      typeof $e.yy.parseError == "function" ? this.parseError = $e.yy.parseError : this.parseError = Object.getPrototypeOf(this).parseError;
      function nt() {
        var jt;
        return jt = $.pop() || Pe.lex() || tt, typeof jt != "number" && (jt instanceof Array && ($ = jt, jt = $.pop()), jt = te.symbols_[jt] || jt), jt;
      }
      for (var je, pt, Et, kt, vt = {}, vr, qt, un, Kr; ; ) {
        if (pt = S[S.length - 1], this.defaultActions[pt] ? Et = this.defaultActions[pt] : ((je === null || typeof je > "u") && (je = nt()), Et = ve[pt] && ve[pt][je]), typeof Et > "u" || !Et.length || !Et[0]) {
          var Da = "";
          Kr = [];
          for (vr in ve[pt])
            this.terminals_[vr] && vr > _e && Kr.push("'" + this.terminals_[vr] + "'");
          Pe.showPosition ? Da = "Parse error on line " + (Ae + 1) + `:
` + Pe.showPosition() + `
Expecting ` + Kr.join(", ") + ", got '" + (this.terminals_[je] || je) + "'" : Da = "Parse error on line " + (Ae + 1) + ": Unexpected " + (je == tt ? "end of input" : "'" + (this.terminals_[je] || je) + "'"), this.parseError(Da, {
            text: Pe.match,
            token: this.terminals_[je] || je,
            line: Pe.yylineno,
            loc: rt,
            expected: Kr
          });
        }
        if (Et[0] instanceof Array && Et.length > 1)
          throw new Error("Parse Error: multiple actions possible at state: " + pt + ", token: " + je);
        switch (Et[0]) {
          case 1:
            S.push(je), k.push(Pe.yytext), q.push(Pe.yylloc), S.push(Et[1]), je = null, Ne = Pe.yyleng, pe = Pe.yytext, Ae = Pe.yylineno, rt = Pe.yylloc;
            break;
          case 2:
            if (qt = this.productions_[Et[1]][1], vt.$ = k[k.length - qt], vt._$ = {
              first_line: q[q.length - (qt || 1)].first_line,
              last_line: q[q.length - 1].last_line,
              first_column: q[q.length - (qt || 1)].first_column,
              last_column: q[q.length - 1].last_column
            }, lt && (vt._$.range = [
              q[q.length - (qt || 1)].range[0],
              q[q.length - 1].range[1]
            ]), kt = this.performAction.apply(vt, [
              pe,
              Ne,
              Ae,
              $e.yy,
              Et[1],
              k,
              q
            ].concat(ct)), typeof kt < "u")
              return kt;
            qt && (S = S.slice(0, -1 * qt * 2), k = k.slice(0, -1 * qt), q = q.slice(0, -1 * qt)), S.push(this.productions_[Et[1]][0]), k.push(vt.$), q.push(vt._$), un = ve[S[S.length - 2]][S[S.length - 1]], S.push(un);
            break;
          case 3:
            return !0;
        }
      }
      return !0;
    }
  }, ue = function() {
    var ee = {
      EOF: 1,
      parseError: function(te, S) {
        if (this.yy.parser)
          this.yy.parser.parseError(te, S);
        else
          throw new Error(te);
      },
      // resets the lexer, sets new input
      setInput: function(H, te) {
        return this.yy = te || this.yy || {}, this._input = H, this._more = this._backtrack = this.done = !1, this.yylineno = this.yyleng = 0, this.yytext = this.matched = this.match = "", this.conditionStack = ["INITIAL"], this.yylloc = {
          first_line: 1,
          first_column: 0,
          last_line: 1,
          last_column: 0
        }, this.options.ranges && (this.yylloc.range = [0, 0]), this.offset = 0, this;
      },
      // consumes and returns one char from the input
      input: function() {
        var H = this._input[0];
        this.yytext += H, this.yyleng++, this.offset++, this.match += H, this.matched += H;
        var te = H.match(/(?:\r\n?|\n).*/g);
        return te ? (this.yylineno++, this.yylloc.last_line++) : this.yylloc.last_column++, this.options.ranges && this.yylloc.range[1]++, this._input = this._input.slice(1), H;
      },
      // unshifts one char (or a string) into the input
      unput: function(H) {
        var te = H.length, S = H.split(/(?:\r\n?|\n)/g);
        this._input = H + this._input, this.yytext = this.yytext.substr(0, this.yytext.length - te), this.offset -= te;
        var $ = this.match.split(/(?:\r\n?|\n)/g);
        this.match = this.match.substr(0, this.match.length - 1), this.matched = this.matched.substr(0, this.matched.length - 1), S.length - 1 && (this.yylineno -= S.length - 1);
        var k = this.yylloc.range;
        return this.yylloc = {
          first_line: this.yylloc.first_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.first_column,
          last_column: S ? (S.length === $.length ? this.yylloc.first_column : 0) + $[$.length - S.length].length - S[0].length : this.yylloc.first_column - te
        }, this.options.ranges && (this.yylloc.range = [k[0], k[0] + this.yyleng - te]), this.yyleng = this.yytext.length, this;
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
      less: function(H) {
        this.unput(this.match.slice(H));
      },
      // displays already matched input, i.e. for error messages
      pastInput: function() {
        var H = this.matched.substr(0, this.matched.length - this.match.length);
        return (H.length > 20 ? "..." : "") + H.substr(-20).replace(/\n/g, "");
      },
      // displays upcoming input, i.e. for error messages
      upcomingInput: function() {
        var H = this.match;
        return H.length < 20 && (H += this._input.substr(0, 20 - H.length)), (H.substr(0, 20) + (H.length > 20 ? "..." : "")).replace(/\n/g, "");
      },
      // displays the character position where the lexing error occurred, i.e. for error messages
      showPosition: function() {
        var H = this.pastInput(), te = new Array(H.length + 1).join("-");
        return H + this.upcomingInput() + `
` + te + "^";
      },
      // test the lexed token: return FALSE when not a match, otherwise return token
      test_match: function(H, te) {
        var S, $, k;
        if (this.options.backtrack_lexer && (k = {
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
        }, this.options.ranges && (k.yylloc.range = this.yylloc.range.slice(0))), $ = H[0].match(/(?:\r\n?|\n).*/g), $ && (this.yylineno += $.length), this.yylloc = {
          first_line: this.yylloc.last_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.last_column,
          last_column: $ ? $[$.length - 1].length - $[$.length - 1].match(/\r?\n?/)[0].length : this.yylloc.last_column + H[0].length
        }, this.yytext += H[0], this.match += H[0], this.matches = H, this.yyleng = this.yytext.length, this.options.ranges && (this.yylloc.range = [this.offset, this.offset += this.yyleng]), this._more = !1, this._backtrack = !1, this._input = this._input.slice(H[0].length), this.matched += H[0], S = this.performAction.call(this, this.yy, this, te, this.conditionStack[this.conditionStack.length - 1]), this.done && this._input && (this.done = !1), S)
          return S;
        if (this._backtrack) {
          for (var q in k)
            this[q] = k[q];
          return !1;
        }
        return !1;
      },
      // return next match in input
      next: function() {
        if (this.done)
          return this.EOF;
        this._input || (this.done = !0);
        var H, te, S, $;
        this._more || (this.yytext = "", this.match = "");
        for (var k = this._currentRules(), q = 0; q < k.length; q++)
          if (S = this._input.match(this.rules[k[q]]), S && (!te || S[0].length > te[0].length)) {
            if (te = S, $ = q, this.options.backtrack_lexer) {
              if (H = this.test_match(S, k[q]), H !== !1)
                return H;
              if (this._backtrack) {
                te = !1;
                continue;
              } else
                return !1;
            } else if (!this.options.flex)
              break;
          }
        return te ? (H = this.test_match(te, k[$]), H !== !1 ? H : !1) : this._input === "" ? this.EOF : this.parseError("Lexical error on line " + (this.yylineno + 1) + `. Unrecognized text.
` + this.showPosition(), {
          text: "",
          token: null,
          line: this.yylineno
        });
      },
      // return next match that has a token
      lex: function() {
        var te = this.next();
        return te || this.lex();
      },
      // activates a new lexer condition state (pushes the new lexer condition state onto the condition stack)
      begin: function(te) {
        this.conditionStack.push(te);
      },
      // pop the previously active lexer condition state off the condition stack
      popState: function() {
        var te = this.conditionStack.length - 1;
        return te > 0 ? this.conditionStack.pop() : this.conditionStack[0];
      },
      // produce the lexer rule set which is active for the currently active lexer condition state
      _currentRules: function() {
        return this.conditionStack.length && this.conditionStack[this.conditionStack.length - 1] ? this.conditions[this.conditionStack[this.conditionStack.length - 1]].rules : this.conditions.INITIAL.rules;
      },
      // return the currently active lexer condition state; when an index argument is provided it produces the N-th previous condition state, if available
      topState: function(te) {
        return te = this.conditionStack.length - 1 - Math.abs(te || 0), te >= 0 ? this.conditionStack[te] : "INITIAL";
      },
      // alias for begin(condition)
      pushState: function(te) {
        this.begin(te);
      },
      // return the number of states currently on the stack
      stateStackSize: function() {
        return this.conditionStack.length;
      },
      options: { "case-insensitive": !0 },
      performAction: function(te, S, $, k) {
        switch ($) {
          case 0:
            te.getLogger().trace("Found comment", S.yytext);
            break;
          case 1:
            return 8;
          case 2:
            this.begin("CLASS");
            break;
          case 3:
            return this.popState(), 16;
          case 4:
            this.popState();
            break;
          case 5:
            te.getLogger().trace("Begin icon"), this.begin("ICON");
            break;
          case 6:
            return te.getLogger().trace("SPACELINE"), 6;
          case 7:
            return 7;
          case 8:
            return 15;
          case 9:
            te.getLogger().trace("end icon"), this.popState();
            break;
          case 10:
            return te.getLogger().trace("Exploding node"), this.begin("NODE"), 19;
          case 11:
            return te.getLogger().trace("Cloud"), this.begin("NODE"), 19;
          case 12:
            return te.getLogger().trace("Explosion Bang"), this.begin("NODE"), 19;
          case 13:
            return te.getLogger().trace("Cloud Bang"), this.begin("NODE"), 19;
          case 14:
            return this.begin("NODE"), 19;
          case 15:
            return this.begin("NODE"), 19;
          case 16:
            return this.begin("NODE"), 19;
          case 17:
            return this.begin("NODE"), 19;
          case 18:
            return 13;
          case 19:
            return 22;
          case 20:
            return 11;
          case 21:
            te.getLogger().trace("Starting NSTR"), this.begin("NSTR");
            break;
          case 22:
            return te.getLogger().trace("description:", S.yytext), "NODE_DESCR";
          case 23:
            this.popState();
            break;
          case 24:
            return this.popState(), te.getLogger().trace("node end ))"), "NODE_DEND";
          case 25:
            return this.popState(), te.getLogger().trace("node end )"), "NODE_DEND";
          case 26:
            return this.popState(), te.getLogger().trace("node end ...", S.yytext), "NODE_DEND";
          case 27:
            return this.popState(), te.getLogger().trace("node end (("), "NODE_DEND";
          case 28:
            return this.popState(), te.getLogger().trace("node end (-"), "NODE_DEND";
          case 29:
            return this.popState(), te.getLogger().trace("node end (-"), "NODE_DEND";
          case 30:
            return this.popState(), te.getLogger().trace("node end (("), "NODE_DEND";
          case 31:
            return this.popState(), te.getLogger().trace("node end (("), "NODE_DEND";
          case 32:
            return te.getLogger().trace("Long description:", S.yytext), 20;
          case 33:
            return te.getLogger().trace("Long description:", S.yytext), 20;
        }
      },
      rules: [/^(?:\s*%%.*)/i, /^(?:mindmap\b)/i, /^(?::::)/i, /^(?:.+)/i, /^(?:\n)/i, /^(?:::icon\()/i, /^(?:[\s]+[\n])/i, /^(?:[\n]+)/i, /^(?:[^\)]+)/i, /^(?:\))/i, /^(?:-\))/i, /^(?:\(-)/i, /^(?:\)\))/i, /^(?:\))/i, /^(?:\(\()/i, /^(?:\{\{)/i, /^(?:\()/i, /^(?:\[)/i, /^(?:[\s]+)/i, /^(?:[^\(\[\n\-\)\{\}]+)/i, /^(?:$)/i, /^(?:["])/i, /^(?:[^"]+)/i, /^(?:["])/i, /^(?:[\)]\))/i, /^(?:[\)])/i, /^(?:[\]])/i, /^(?:\}\})/i, /^(?:\(-)/i, /^(?:-\))/i, /^(?:\(\()/i, /^(?:\()/i, /^(?:[^\)\]\(\}]+)/i, /^(?:.+(?!\(\())/i],
      conditions: { CLASS: { rules: [3, 4], inclusive: !1 }, ICON: { rules: [8, 9], inclusive: !1 }, NSTR: { rules: [22, 23], inclusive: !1 }, NODE: { rules: [21, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33], inclusive: !1 }, INITIAL: { rules: [0, 1, 2, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], inclusive: !0 } }
    };
    return ee;
  }();
  ne.lexer = ue;
  function j() {
    this.yy = {};
  }
  return j.prototype = ne, ne.Parser = j, new j();
}();
Ki.parser = Ki;
const Tp = Ki, on = (fe) => yp(fe, sn());
let Jt = [], Uu = 0, Ji = {};
const Cp = () => {
  Jt = [], Uu = 0, Ji = {};
}, Dp = function(fe) {
  for (let he = Jt.length - 1; he >= 0; he--)
    if (Jt[he].level < fe)
      return Jt[he];
  return null;
}, Sp = () => Jt.length > 0 ? Jt[0] : null, Lp = (fe, he, Q, ce) => {
  qr.info("addNode", fe, he, Q, ce);
  const Y = sn(), A = {
    id: Uu++,
    nodeId: on(he),
    level: fe,
    descr: on(Q),
    type: ce,
    children: [],
    width: sn().mindmap.maxNodeWidth
  };
  switch (A.type) {
    case yt.ROUNDED_RECT:
      A.padding = 2 * Y.mindmap.padding;
      break;
    case yt.RECT:
      A.padding = 2 * Y.mindmap.padding;
      break;
    case yt.HEXAGON:
      A.padding = 2 * Y.mindmap.padding;
      break;
    default:
      A.padding = Y.mindmap.padding;
  }
  const T = Dp(fe);
  if (T)
    T.children.push(A), Jt.push(A);
  else if (Jt.length === 0)
    Jt.push(A);
  else {
    let w = new Error(
      'There can be only one root. No parent could be found for ("' + A.descr + '")'
    );
    throw w.hash = {
      text: "branch " + name,
      token: "branch " + name,
      line: "1",
      loc: { first_line: 1, last_line: 1, first_column: 1, last_column: 1 },
      expected: ['"checkout ' + name + '"']
    }, w;
  }
}, yt = {
  DEFAULT: 0,
  NO_BORDER: 0,
  ROUNDED_RECT: 1,
  RECT: 2,
  CIRCLE: 3,
  CLOUD: 4,
  BANG: 5,
  HEXAGON: 6
}, Ap = (fe, he) => {
  switch (qr.debug("In get type", fe, he), fe) {
    case "[":
      return yt.RECT;
    case "(":
      return he === ")" ? yt.ROUNDED_RECT : yt.CLOUD;
    case "((":
      return yt.CIRCLE;
    case ")":
      return yt.CLOUD;
    case "))":
      return yt.BANG;
    case "{{":
      return yt.HEXAGON;
    default:
      return yt.DEFAULT;
  }
}, Yu = (fe, he) => {
  Ji[fe] = he;
}, Op = (fe) => {
  const he = Jt[Jt.length - 1];
  fe && fe.icon && (he.icon = on(fe.icon)), fe && fe.class && (he.class = on(fe.class));
}, Wr = (fe) => {
  switch (fe) {
    case yt.DEFAULT:
      return "no-border";
    case yt.RECT:
      return "rect";
    case yt.ROUNDED_RECT:
      return "rounded-rect";
    case yt.CIRCLE:
      return "circle";
    case yt.CLOUD:
      return "cloud";
    case yt.BANG:
      return "bang";
    case yt.HEXAGON:
      return "hexgon";
    default:
      return "no-border";
  }
};
let Hu;
const Np = (fe) => {
  Hu = fe;
}, Mp = () => qr, Ip = (fe) => Jt[fe], ji = (fe) => Ji[fe], Rp = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  addNode: Lp,
  clear: Cp,
  decorateNode: Op,
  getElementById: ji,
  getLogger: Mp,
  getMindmap: Sp,
  getNodeById: Ip,
  getType: Ap,
  nodeType: yt,
  get parseError() {
    return Hu;
  },
  sanitizeText: on,
  setElementForId: Yu,
  setErrorHandler: Np,
  type2Str: Wr
}, Symbol.toStringTag, { value: "Module" })), Xu = 12;
function kp(fe, he) {
  fe.each(function() {
    var Q = nn(this), ce = Q.text().split(/(\s+|<br>)/).reverse(), Y, A = [], T = 1.1, w = Q.attr("y"), L = parseFloat(Q.attr("dy")), G = Q.text(null).append("tspan").attr("x", 0).attr("y", w).attr("dy", L + "em");
    for (let U = 0; U < ce.length; U++)
      Y = ce[ce.length - 1 - U], A.push(Y), G.text(A.join(" ").trim()), (G.node().getComputedTextLength() > he || Y === "<br>") && (A.pop(), G.text(A.join(" ").trim()), Y === "<br>" ? A = [""] : A = [Y], G = Q.append("tspan").attr("x", 0).attr("y", w).attr("dy", T + "em").text(Y));
  });
}
const Pp = function(fe, he, Q) {
  fe.append("path").attr("id", "node-" + he.id).attr("class", "node-bkg node-" + Wr(he.type)).attr(
    "d",
    `M0 ${he.height - 5} v${-he.height + 2 * 5} q0,-5 5,-5 h${he.width - 2 * 5} q5,0 5,5 v${he.height - 5} H0 Z`
  ), fe.append("line").attr("class", "node-line-" + Q).attr("x1", 0).attr("y1", he.height).attr("x2", he.width).attr("y2", he.height);
}, Bp = function(fe, he) {
  fe.append("rect").attr("id", "node-" + he.id).attr("class", "node-bkg node-" + Wr(he.type)).attr("height", he.height).attr("width", he.width);
}, Fp = function(fe, he) {
  const Q = he.width, ce = he.height, Y = 0.15 * Q, A = 0.25 * Q, T = 0.35 * Q, w = 0.2 * Q;
  fe.append("path").attr("id", "node-" + he.id).attr("class", "node-bkg node-" + Wr(he.type)).attr(
    "d",
    `M0 0 a${Y},${Y} 0 0,1 ${Q * 0.25},${-1 * Q * 0.1}
      a${T},${T} 1 0,1 ${Q * 0.4},${-1 * Q * 0.1}
      a${A},${A} 1 0,1 ${Q * 0.35},${1 * Q * 0.2}

      a${Y},${Y} 1 0,1 ${Q * 0.15},${1 * ce * 0.35}
      a${w},${w} 1 0,1 ${-1 * Q * 0.15},${1 * ce * 0.65}

      a${A},${Y} 1 0,1 ${-1 * Q * 0.25},${Q * 0.15}
      a${T},${T} 1 0,1 ${-1 * Q * 0.5},${0}
      a${Y},${Y} 1 0,1 ${-1 * Q * 0.25},${-1 * Q * 0.15}

      a${Y},${Y} 1 0,1 ${-1 * Q * 0.1},${-1 * ce * 0.35}
      a${w},${w} 1 0,1 ${Q * 0.1},${-1 * ce * 0.65}

    H0 V0 Z`
  );
}, zp = function(fe, he) {
  const Q = he.width, ce = he.height, Y = 0.15 * Q;
  fe.append("path").attr("id", "node-" + he.id).attr("class", "node-bkg node-" + Wr(he.type)).attr(
    "d",
    `M0 0 a${Y},${Y} 1 0,0 ${Q * 0.25},${-1 * ce * 0.1}
      a${Y},${Y} 1 0,0 ${Q * 0.25},${0}
      a${Y},${Y} 1 0,0 ${Q * 0.25},${0}
      a${Y},${Y} 1 0,0 ${Q * 0.25},${1 * ce * 0.1}

      a${Y},${Y} 1 0,0 ${Q * 0.15},${1 * ce * 0.33}
      a${Y * 0.8},${Y * 0.8} 1 0,0 ${0},${1 * ce * 0.34}
      a${Y},${Y} 1 0,0 ${-1 * Q * 0.15},${1 * ce * 0.33}

      a${Y},${Y} 1 0,0 ${-1 * Q * 0.25},${ce * 0.15}
      a${Y},${Y} 1 0,0 ${-1 * Q * 0.25},${0}
      a${Y},${Y} 1 0,0 ${-1 * Q * 0.25},${0}
      a${Y},${Y} 1 0,0 ${-1 * Q * 0.25},${-1 * ce * 0.15}

      a${Y},${Y} 1 0,0 ${-1 * Q * 0.1},${-1 * ce * 0.33}
      a${Y * 0.8},${Y * 0.8} 1 0,0 ${0},${-1 * ce * 0.34}
      a${Y},${Y} 1 0,0 ${Q * 0.1},${-1 * ce * 0.33}

    H0 V0 Z`
  );
}, Gp = function(fe, he) {
  fe.append("circle").attr("id", "node-" + he.id).attr("class", "node-bkg node-" + Wr(he.type)).attr("r", he.width / 2);
};
function $p(fe, he, Q, ce, Y) {
  return fe.insert("polygon", ":first-child").attr(
    "points",
    ce.map(function(A) {
      return A.x + "," + A.y;
    }).join(" ")
  ).attr("transform", "translate(" + (Y.width - he) / 2 + ", " + Q + ")");
}
const Vp = function(fe, he) {
  const Q = he.height, Y = Q / 4, A = he.width - he.padding + 2 * Y, T = [
    { x: Y, y: 0 },
    { x: A - Y, y: 0 },
    { x: A, y: -Q / 2 },
    { x: A - Y, y: -Q },
    { x: Y, y: -Q },
    { x: 0, y: -Q / 2 }
  ];
  $p(fe, A, Q, T, he);
}, _p = function(fe, he) {
  fe.append("rect").attr("id", "node-" + he.id).attr("class", "node-bkg node-" + Wr(he.type)).attr("height", he.height).attr("rx", he.padding).attr("ry", he.padding).attr("width", he.width);
}, Up = function(fe, he, Q, ce) {
  const Y = Q % (Xu - 1), A = fe.append("g");
  he.section = Y;
  let T = "section-" + Y;
  Y < 0 && (T += " section-root"), A.attr("class", (he.class ? he.class + " " : "") + "mindmap-node " + T);
  const w = A.append("g"), L = A.append("g"), U = L.append("text").text(he.descr).attr("dy", "1em").attr("alignment-baseline", "middle").attr("dominant-baseline", "middle").attr("text-anchor", "middle").call(kp, he.width).node().getBBox(), P = ce.fontSize.replace ? ce.fontSize.replace("px", "") : ce.fontSize;
  if (he.height = U.height + P * 1.1 * 0.5 + he.padding, he.width = U.width + 2 * he.padding, he.icon)
    if (he.type === yt.CIRCLE)
      he.height += 50, he.width += 50, A.append("foreignObject").attr("height", "50px").attr("width", he.width).attr("style", "text-align: center;").append("div").attr("class", "icon-container").append("i").attr("class", "node-icon-" + Y + " " + he.icon), L.attr(
        "transform",
        "translate(" + he.width / 2 + ", " + (he.height / 2 - 1.5 * he.padding) + ")"
      );
    else {
      he.width += 50;
      const K = he.height;
      he.height = Math.max(K, 60);
      const D = Math.abs(he.height - K);
      A.append("foreignObject").attr("width", "60px").attr("height", he.height).attr("style", "text-align: center;margin-top:" + D / 2 + "px;").append("div").attr("class", "icon-container").append("i").attr("class", "node-icon-" + Y + " " + he.icon), L.attr(
        "transform",
        "translate(" + (25 + he.width / 2) + ", " + (D / 2 + he.padding / 2) + ")"
      );
    }
  else
    L.attr("transform", "translate(" + he.width / 2 + ", " + he.padding / 2 + ")");
  switch (he.type) {
    case yt.DEFAULT:
      Pp(w, he, Y);
      break;
    case yt.ROUNDED_RECT:
      _p(w, he);
      break;
    case yt.RECT:
      Bp(w, he);
      break;
    case yt.CIRCLE:
      w.attr("transform", "translate(" + he.width / 2 + ", " + +he.height / 2 + ")"), Gp(w, he);
      break;
    case yt.CLOUD:
      Fp(w, he);
      break;
    case yt.BANG:
      zp(w, he);
      break;
    case yt.HEXAGON:
      Vp(w, he);
      break;
  }
  return Yu(he.id, A), he.height;
}, Yp = function(he, Q, ce, Y, A) {
  const T = A % (Xu - 1), w = ce.x + ce.width / 2, L = ce.y + ce.height / 2, G = Q.x + Q.width / 2, U = Q.y + Q.height / 2, P = G > w ? w + Math.abs(w - G) / 2 : w - Math.abs(w - G) / 2, K = U > L ? L + Math.abs(L - U) / 2 : L - Math.abs(L - U) / 2, D = G > w ? Math.abs(w - P) / 2 + w : -Math.abs(w - P) / 2 + w, V = U > L ? Math.abs(L - K) / 2 + L : -Math.abs(L - K) / 2 + L;
  he.append("path").attr(
    "d",
    ce.direction === "TB" || ce.direction === "BT" ? `M${w},${L} Q${w},${V} ${P},${K} T${G},${U}` : `M${w},${L} Q${D},${L} ${P},${K} T${G},${U}`
  ).attr("class", "edge section-edge-" + T + " edge-depth-" + Y);
}, Hp = function(fe) {
  const he = ji(fe.id), Q = fe.x || 0, ce = fe.y || 0;
  he.attr("transform", "translate(" + Q + "," + ce + ")");
}, qu = { drawNode: Up, positionNode: Hp, drawEdge: Yp };
var Zi = {}, Xp = {
  get exports() {
    return Zi;
  },
  set exports(fe) {
    Zi = fe;
  }
};
(function(fe, he) {
  (function(Q, ce) {
    fe.exports = ce();
  })(Ca, function() {
    function Q(t) {
      return Q = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
        return typeof e;
      } : function(e) {
        return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
      }, Q(t);
    }
    function ce(t, e) {
      if (!(t instanceof e))
        throw new TypeError("Cannot call a class as a function");
    }
    function Y(t, e) {
      for (var r = 0; r < e.length; r++) {
        var a = e[r];
        a.enumerable = a.enumerable || !1, a.configurable = !0, "value" in a && (a.writable = !0), Object.defineProperty(t, a.key, a);
      }
    }
    function A(t, e, r) {
      return e && Y(t.prototype, e), r && Y(t, r), Object.defineProperty(t, "prototype", {
        writable: !1
      }), t;
    }
    function T(t, e, r) {
      return e in t ? Object.defineProperty(t, e, {
        value: r,
        enumerable: !0,
        configurable: !0,
        writable: !0
      }) : t[e] = r, t;
    }
    function w(t, e) {
      return L(t) || G(t, e) || U(t, e) || K();
    }
    function L(t) {
      if (Array.isArray(t))
        return t;
    }
    function G(t, e) {
      var r = t == null ? null : typeof Symbol < "u" && t[Symbol.iterator] || t["@@iterator"];
      if (r != null) {
        var a = [], n = !0, i = !1, s, o;
        try {
          for (r = r.call(t); !(n = (s = r.next()).done) && (a.push(s.value), !(e && a.length === e)); n = !0)
            ;
        } catch (l) {
          i = !0, o = l;
        } finally {
          try {
            !n && r.return != null && r.return();
          } finally {
            if (i)
              throw o;
          }
        }
        return a;
      }
    }
    function U(t, e) {
      if (t) {
        if (typeof t == "string")
          return P(t, e);
        var r = Object.prototype.toString.call(t).slice(8, -1);
        if (r === "Object" && t.constructor && (r = t.constructor.name), r === "Map" || r === "Set")
          return Array.from(t);
        if (r === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))
          return P(t, e);
      }
    }
    function P(t, e) {
      (e == null || e > t.length) && (e = t.length);
      for (var r = 0, a = new Array(e); r < e; r++)
        a[r] = t[r];
      return a;
    }
    function K() {
      throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
    }
    var D = typeof window > "u" ? null : window, V = D ? D.navigator : null;
    D && D.document;
    var _ = Q(""), J = Q({}), ne = Q(function() {
    }), ue = typeof HTMLElement > "u" ? "undefined" : Q(HTMLElement), j = function(e) {
      return e && e.instanceString && H(e.instanceString) ? e.instanceString() : null;
    }, ee = function(e) {
      return e != null && Q(e) == _;
    }, H = function(e) {
      return e != null && Q(e) === ne;
    }, te = function(e) {
      return !pe(e) && (Array.isArray ? Array.isArray(e) : e != null && e instanceof Array);
    }, S = function(e) {
      return e != null && Q(e) === J && !te(e) && e.constructor === Object;
    }, $ = function(e) {
      return e != null && Q(e) === J;
    }, k = function(e) {
      return e != null && Q(e) === Q(1) && !isNaN(e);
    }, q = function(e) {
      return k(e) && Math.floor(e) === e;
    }, ve = function(e) {
      if (ue !== "undefined")
        return e != null && e instanceof HTMLElement;
    }, pe = function(e) {
      return Ae(e) || Ne(e);
    }, Ae = function(e) {
      return j(e) === "collection" && e._private.single;
    }, Ne = function(e) {
      return j(e) === "collection" && !e._private.single;
    }, _e = function(e) {
      return j(e) === "core";
    }, tt = function(e) {
      return j(e) === "stylesheet";
    }, ct = function(e) {
      return j(e) === "event";
    }, Pe = function(e) {
      return e == null ? !0 : !!(e === "" || e.match(/^\s+$/));
    }, $e = function(e) {
      return typeof HTMLElement > "u" ? !1 : e instanceof HTMLElement;
    }, Xe = function(e) {
      return S(e) && k(e.x1) && k(e.x2) && k(e.y1) && k(e.y2);
    }, rt = function(e) {
      return $(e) && H(e.then);
    }, lt = function() {
      return V && V.userAgent.match(/msie|trident|edge/i);
    }, nt = function(e, r) {
      r || (r = function() {
        if (arguments.length === 1)
          return arguments[0];
        if (arguments.length === 0)
          return "undefined";
        for (var i = [], s = 0; s < arguments.length; s++)
          i.push(arguments[s]);
        return i.join("$");
      });
      var a = function n() {
        var i = this, s = arguments, o, l = r.apply(i, s), u = n.cache;
        return (o = u[l]) || (o = u[l] = e.apply(i, s)), o;
      };
      return a.cache = {}, a;
    }, je = nt(function(t) {
      return t.replace(/([A-Z])/g, function(e) {
        return "-" + e.toLowerCase();
      });
    }), pt = nt(function(t) {
      return t.replace(/(-\w)/g, function(e) {
        return e[1].toUpperCase();
      });
    }), Et = nt(function(t, e) {
      return t + e[0].toUpperCase() + e.substring(1);
    }, function(t, e) {
      return t + "$" + e;
    }), kt = function(e) {
      return Pe(e) ? e : e.charAt(0).toUpperCase() + e.substring(1);
    }, vt = "(?:[-+]?(?:(?:\\d+|\\d*\\.\\d+)(?:[Ee][+-]?\\d+)?))", vr = "rgb[a]?\\((" + vt + "[%]?)\\s*,\\s*(" + vt + "[%]?)\\s*,\\s*(" + vt + "[%]?)(?:\\s*,\\s*(" + vt + "))?\\)", qt = "rgb[a]?\\((?:" + vt + "[%]?)\\s*,\\s*(?:" + vt + "[%]?)\\s*,\\s*(?:" + vt + "[%]?)(?:\\s*,\\s*(?:" + vt + "))?\\)", un = "hsl[a]?\\((" + vt + ")\\s*,\\s*(" + vt + "[%])\\s*,\\s*(" + vt + "[%])(?:\\s*,\\s*(" + vt + "))?\\)", Kr = "hsl[a]?\\((?:" + vt + ")\\s*,\\s*(?:" + vt + "[%])\\s*,\\s*(?:" + vt + "[%])(?:\\s*,\\s*(?:" + vt + "))?\\)", Da = "\\#[0-9a-fA-F]{3}", jt = "\\#[0-9a-fA-F]{6}", es = function(e, r) {
      return e < r ? -1 : e > r ? 1 : 0;
    }, Qu = function(e, r) {
      return -1 * es(e, r);
    }, Ue = Object.assign != null ? Object.assign.bind(Object) : function(t) {
      for (var e = arguments, r = 1; r < e.length; r++) {
        var a = e[r];
        if (a != null)
          for (var n = Object.keys(a), i = 0; i < n.length; i++) {
            var s = n[i];
            t[s] = a[s];
          }
      }
      return t;
    }, Ju = function(e) {
      if (!(!(e.length === 4 || e.length === 7) || e[0] !== "#")) {
        var r = e.length === 4, a, n, i, s = 16;
        return r ? (a = parseInt(e[1] + e[1], s), n = parseInt(e[2] + e[2], s), i = parseInt(e[3] + e[3], s)) : (a = parseInt(e[1] + e[2], s), n = parseInt(e[3] + e[4], s), i = parseInt(e[5] + e[6], s)), [a, n, i];
      }
    }, ju = function(e) {
      var r, a, n, i, s, o, l, u;
      function f(d, g, y) {
        return y < 0 && (y += 1), y > 1 && (y -= 1), y < 1 / 6 ? d + (g - d) * 6 * y : y < 1 / 2 ? g : y < 2 / 3 ? d + (g - d) * (2 / 3 - y) * 6 : d;
      }
      var h = new RegExp("^" + un + "$").exec(e);
      if (h) {
        if (a = parseInt(h[1]), a < 0 ? a = (360 - -1 * a % 360) % 360 : a > 360 && (a = a % 360), a /= 360, n = parseFloat(h[2]), n < 0 || n > 100 || (n = n / 100, i = parseFloat(h[3]), i < 0 || i > 100) || (i = i / 100, s = h[4], s !== void 0 && (s = parseFloat(s), s < 0 || s > 1)))
          return;
        if (n === 0)
          o = l = u = Math.round(i * 255);
        else {
          var c = i < 0.5 ? i * (1 + n) : i + n - i * n, v = 2 * i - c;
          o = Math.round(255 * f(v, c, a + 1 / 3)), l = Math.round(255 * f(v, c, a)), u = Math.round(255 * f(v, c, a - 1 / 3));
        }
        r = [o, l, u, s];
      }
      return r;
    }, el = function(e) {
      var r, a = new RegExp("^" + vr + "$").exec(e);
      if (a) {
        r = [];
        for (var n = [], i = 1; i <= 3; i++) {
          var s = a[i];
          if (s[s.length - 1] === "%" && (n[i] = !0), s = parseFloat(s), n[i] && (s = s / 100 * 255), s < 0 || s > 255)
            return;
          r.push(Math.floor(s));
        }
        var o = n[1] || n[2] || n[3], l = n[1] && n[2] && n[3];
        if (o && !l)
          return;
        var u = a[4];
        if (u !== void 0) {
          if (u = parseFloat(u), u < 0 || u > 1)
            return;
          r.push(u);
        }
      }
      return r;
    }, tl = function(e) {
      return al[e.toLowerCase()];
    }, rl = function(e) {
      return (te(e) ? e : null) || tl(e) || Ju(e) || el(e) || ju(e);
    }, al = {
      // special colour names
      transparent: [0, 0, 0, 0],
      // NB alpha === 0
      // regular colours
      aliceblue: [240, 248, 255],
      antiquewhite: [250, 235, 215],
      aqua: [0, 255, 255],
      aquamarine: [127, 255, 212],
      azure: [240, 255, 255],
      beige: [245, 245, 220],
      bisque: [255, 228, 196],
      black: [0, 0, 0],
      blanchedalmond: [255, 235, 205],
      blue: [0, 0, 255],
      blueviolet: [138, 43, 226],
      brown: [165, 42, 42],
      burlywood: [222, 184, 135],
      cadetblue: [95, 158, 160],
      chartreuse: [127, 255, 0],
      chocolate: [210, 105, 30],
      coral: [255, 127, 80],
      cornflowerblue: [100, 149, 237],
      cornsilk: [255, 248, 220],
      crimson: [220, 20, 60],
      cyan: [0, 255, 255],
      darkblue: [0, 0, 139],
      darkcyan: [0, 139, 139],
      darkgoldenrod: [184, 134, 11],
      darkgray: [169, 169, 169],
      darkgreen: [0, 100, 0],
      darkgrey: [169, 169, 169],
      darkkhaki: [189, 183, 107],
      darkmagenta: [139, 0, 139],
      darkolivegreen: [85, 107, 47],
      darkorange: [255, 140, 0],
      darkorchid: [153, 50, 204],
      darkred: [139, 0, 0],
      darksalmon: [233, 150, 122],
      darkseagreen: [143, 188, 143],
      darkslateblue: [72, 61, 139],
      darkslategray: [47, 79, 79],
      darkslategrey: [47, 79, 79],
      darkturquoise: [0, 206, 209],
      darkviolet: [148, 0, 211],
      deeppink: [255, 20, 147],
      deepskyblue: [0, 191, 255],
      dimgray: [105, 105, 105],
      dimgrey: [105, 105, 105],
      dodgerblue: [30, 144, 255],
      firebrick: [178, 34, 34],
      floralwhite: [255, 250, 240],
      forestgreen: [34, 139, 34],
      fuchsia: [255, 0, 255],
      gainsboro: [220, 220, 220],
      ghostwhite: [248, 248, 255],
      gold: [255, 215, 0],
      goldenrod: [218, 165, 32],
      gray: [128, 128, 128],
      grey: [128, 128, 128],
      green: [0, 128, 0],
      greenyellow: [173, 255, 47],
      honeydew: [240, 255, 240],
      hotpink: [255, 105, 180],
      indianred: [205, 92, 92],
      indigo: [75, 0, 130],
      ivory: [255, 255, 240],
      khaki: [240, 230, 140],
      lavender: [230, 230, 250],
      lavenderblush: [255, 240, 245],
      lawngreen: [124, 252, 0],
      lemonchiffon: [255, 250, 205],
      lightblue: [173, 216, 230],
      lightcoral: [240, 128, 128],
      lightcyan: [224, 255, 255],
      lightgoldenrodyellow: [250, 250, 210],
      lightgray: [211, 211, 211],
      lightgreen: [144, 238, 144],
      lightgrey: [211, 211, 211],
      lightpink: [255, 182, 193],
      lightsalmon: [255, 160, 122],
      lightseagreen: [32, 178, 170],
      lightskyblue: [135, 206, 250],
      lightslategray: [119, 136, 153],
      lightslategrey: [119, 136, 153],
      lightsteelblue: [176, 196, 222],
      lightyellow: [255, 255, 224],
      lime: [0, 255, 0],
      limegreen: [50, 205, 50],
      linen: [250, 240, 230],
      magenta: [255, 0, 255],
      maroon: [128, 0, 0],
      mediumaquamarine: [102, 205, 170],
      mediumblue: [0, 0, 205],
      mediumorchid: [186, 85, 211],
      mediumpurple: [147, 112, 219],
      mediumseagreen: [60, 179, 113],
      mediumslateblue: [123, 104, 238],
      mediumspringgreen: [0, 250, 154],
      mediumturquoise: [72, 209, 204],
      mediumvioletred: [199, 21, 133],
      midnightblue: [25, 25, 112],
      mintcream: [245, 255, 250],
      mistyrose: [255, 228, 225],
      moccasin: [255, 228, 181],
      navajowhite: [255, 222, 173],
      navy: [0, 0, 128],
      oldlace: [253, 245, 230],
      olive: [128, 128, 0],
      olivedrab: [107, 142, 35],
      orange: [255, 165, 0],
      orangered: [255, 69, 0],
      orchid: [218, 112, 214],
      palegoldenrod: [238, 232, 170],
      palegreen: [152, 251, 152],
      paleturquoise: [175, 238, 238],
      palevioletred: [219, 112, 147],
      papayawhip: [255, 239, 213],
      peachpuff: [255, 218, 185],
      peru: [205, 133, 63],
      pink: [255, 192, 203],
      plum: [221, 160, 221],
      powderblue: [176, 224, 230],
      purple: [128, 0, 128],
      red: [255, 0, 0],
      rosybrown: [188, 143, 143],
      royalblue: [65, 105, 225],
      saddlebrown: [139, 69, 19],
      salmon: [250, 128, 114],
      sandybrown: [244, 164, 96],
      seagreen: [46, 139, 87],
      seashell: [255, 245, 238],
      sienna: [160, 82, 45],
      silver: [192, 192, 192],
      skyblue: [135, 206, 235],
      slateblue: [106, 90, 205],
      slategray: [112, 128, 144],
      slategrey: [112, 128, 144],
      snow: [255, 250, 250],
      springgreen: [0, 255, 127],
      steelblue: [70, 130, 180],
      tan: [210, 180, 140],
      teal: [0, 128, 128],
      thistle: [216, 191, 216],
      tomato: [255, 99, 71],
      turquoise: [64, 224, 208],
      violet: [238, 130, 238],
      wheat: [245, 222, 179],
      white: [255, 255, 255],
      whitesmoke: [245, 245, 245],
      yellow: [255, 255, 0],
      yellowgreen: [154, 205, 50]
    }, ts = function(e) {
      for (var r = e.map, a = e.keys, n = a.length, i = 0; i < n; i++) {
        var s = a[i];
        if (S(s))
          throw Error("Tried to set map with object key");
        i < a.length - 1 ? (r[s] == null && (r[s] = {}), r = r[s]) : r[s] = e.value;
      }
    }, rs = function(e) {
      for (var r = e.map, a = e.keys, n = a.length, i = 0; i < n; i++) {
        var s = a[i];
        if (S(s))
          throw Error("Tried to get map with object key");
        if (r = r[s], r == null)
          return r;
      }
      return r;
    };
    function nl(t) {
      var e = typeof t;
      return t != null && (e == "object" || e == "function");
    }
    var Rr = nl, Sa = typeof globalThis < "u" ? globalThis : typeof window < "u" ? window : typeof Ca < "u" ? Ca : typeof self < "u" ? self : {};
    function il(t, e) {
      return e = { exports: {} }, t(e, e.exports), e.exports;
    }
    var sl = typeof Sa == "object" && Sa && Sa.Object === Object && Sa, ol = sl, ul = typeof self == "object" && self && self.Object === Object && self, ll = ol || ul || Function("return this")(), ln = ll, fl = function() {
      return ln.Date.now();
    }, ai = fl, hl = /\s/;
    function cl(t) {
      for (var e = t.length; e-- && hl.test(t.charAt(e)); )
        ;
      return e;
    }
    var vl = cl, dl = /^\s+/;
    function gl(t) {
      return t && t.slice(0, vl(t) + 1).replace(dl, "");
    }
    var pl = gl, yl = ln.Symbol, Zr = yl, as = Object.prototype, ml = as.hasOwnProperty, bl = as.toString, La = Zr ? Zr.toStringTag : void 0;
    function El(t) {
      var e = ml.call(t, La), r = t[La];
      try {
        t[La] = void 0;
        var a = !0;
      } catch {
      }
      var n = bl.call(t);
      return a && (e ? t[La] = r : delete t[La]), n;
    }
    var wl = El, xl = Object.prototype, Tl = xl.toString;
    function Cl(t) {
      return Tl.call(t);
    }
    var Dl = Cl, Sl = "[object Null]", Ll = "[object Undefined]", ns = Zr ? Zr.toStringTag : void 0;
    function Al(t) {
      return t == null ? t === void 0 ? Ll : Sl : ns && ns in Object(t) ? wl(t) : Dl(t);
    }
    var is = Al;
    function Ol(t) {
      return t != null && typeof t == "object";
    }
    var Nl = Ol, Ml = "[object Symbol]";
    function Il(t) {
      return typeof t == "symbol" || Nl(t) && is(t) == Ml;
    }
    var Aa = Il, ss = 0 / 0, Rl = /^[-+]0x[0-9a-f]+$/i, kl = /^0b[01]+$/i, Pl = /^0o[0-7]+$/i, Bl = parseInt;
    function Fl(t) {
      if (typeof t == "number")
        return t;
      if (Aa(t))
        return ss;
      if (Rr(t)) {
        var e = typeof t.valueOf == "function" ? t.valueOf() : t;
        t = Rr(e) ? e + "" : e;
      }
      if (typeof t != "string")
        return t === 0 ? t : +t;
      t = pl(t);
      var r = kl.test(t);
      return r || Pl.test(t) ? Bl(t.slice(2), r ? 2 : 8) : Rl.test(t) ? ss : +t;
    }
    var os = Fl, zl = "Expected a function", Gl = Math.max, $l = Math.min;
    function Vl(t, e, r) {
      var a, n, i, s, o, l, u = 0, f = !1, h = !1, c = !0;
      if (typeof t != "function")
        throw new TypeError(zl);
      e = os(e) || 0, Rr(r) && (f = !!r.leading, h = "maxWait" in r, i = h ? Gl(os(r.maxWait) || 0, e) : i, c = "trailing" in r ? !!r.trailing : c);
      function v(O) {
        var x = a, I = n;
        return a = n = void 0, u = O, s = t.apply(I, x), s;
      }
      function d(O) {
        return u = O, o = setTimeout(p, e), f ? v(O) : s;
      }
      function g(O) {
        var x = O - l, I = O - u, C = e - x;
        return h ? $l(C, i - I) : C;
      }
      function y(O) {
        var x = O - l, I = O - u;
        return l === void 0 || x >= e || x < 0 || h && I >= i;
      }
      function p() {
        var O = ai();
        if (y(O))
          return m(O);
        o = setTimeout(p, g(O));
      }
      function m(O) {
        return o = void 0, c && a ? v(O) : (a = n = void 0, s);
      }
      function b() {
        o !== void 0 && clearTimeout(o), u = 0, a = l = n = o = void 0;
      }
      function E() {
        return o === void 0 ? s : m(ai());
      }
      function M() {
        var O = ai(), x = y(O);
        if (a = arguments, n = this, l = O, x) {
          if (o === void 0)
            return d(l);
          if (h)
            return clearTimeout(o), o = setTimeout(p, e), v(l);
        }
        return o === void 0 && (o = setTimeout(p, e)), s;
      }
      return M.cancel = b, M.flush = E, M;
    }
    var fn = Vl, ni = D ? D.performance : null, us = ni && ni.now ? function() {
      return ni.now();
    } : function() {
      return Date.now();
    }, _l = function() {
      if (D) {
        if (D.requestAnimationFrame)
          return function(t) {
            D.requestAnimationFrame(t);
          };
        if (D.mozRequestAnimationFrame)
          return function(t) {
            D.mozRequestAnimationFrame(t);
          };
        if (D.webkitRequestAnimationFrame)
          return function(t) {
            D.webkitRequestAnimationFrame(t);
          };
        if (D.msRequestAnimationFrame)
          return function(t) {
            D.msRequestAnimationFrame(t);
          };
      }
      return function(t) {
        t && setTimeout(function() {
          t(us());
        }, 1e3 / 60);
      };
    }(), hn = function(e) {
      return _l(e);
    }, dr = us, Qr = 9261, ls = 65599, Oa = 5381, fs = function(e) {
      for (var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : Qr, a = r, n; n = e.next(), !n.done; )
        a = a * ls + n.value | 0;
      return a;
    }, Na = function(e) {
      var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : Qr;
      return r * ls + e | 0;
    }, Ma = function(e) {
      var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : Oa;
      return (r << 5) + r + e | 0;
    }, Ul = function(e, r) {
      return e * 2097152 + r;
    }, Er = function(e) {
      return e[0] * 2097152 + e[1];
    }, cn = function(e, r) {
      return [Na(e[0], r[0]), Ma(e[1], r[1])];
    }, Yl = function(e, r) {
      var a = {
        value: 0,
        done: !1
      }, n = 0, i = e.length, s = {
        next: function() {
          return n < i ? a.value = e[n++] : a.done = !0, a;
        }
      };
      return fs(s, r);
    }, kr = function(e, r) {
      var a = {
        value: 0,
        done: !1
      }, n = 0, i = e.length, s = {
        next: function() {
          return n < i ? a.value = e.charCodeAt(n++) : a.done = !0, a;
        }
      };
      return fs(s, r);
    }, hs = function() {
      return Hl(arguments);
    }, Hl = function(e) {
      for (var r, a = 0; a < e.length; a++) {
        var n = e[a];
        a === 0 ? r = kr(n) : r = kr(n, r);
      }
      return r;
    }, cs = !0, Xl = console.warn != null, ql = console.trace != null, ii = Number.MAX_SAFE_INTEGER || 9007199254740991, vs = function() {
      return !0;
    }, vn = function() {
      return !1;
    }, ds = function() {
      return 0;
    }, si = function() {
    }, xt = function(e) {
      throw new Error(e);
    }, gs = function(e) {
      if (e !== void 0)
        cs = !!e;
      else
        return cs;
    }, ft = function(e) {
      gs() && (Xl ? console.warn(e) : (console.log(e), ql && console.trace()));
    }, Wl = function(e) {
      return Ue({}, e);
    }, or = function(e) {
      return e == null ? e : te(e) ? e.slice() : S(e) ? Wl(e) : e;
    }, Kl = function(e) {
      return e.slice();
    }, ps = function(e, r) {
      for (
        // loop :)
        r = e = "";
        // b - result , a - numeric letiable
        e++ < 36;
        //
        r += e * 51 & 52 ? (
          //  return a random number or 4
          (e ^ 15 ? (
            // generate a random number from 0 to 15
            8 ^ Math.random() * (e ^ 20 ? 16 : 4)
          ) : 4).toString(16)
        ) : "-"
      )
        ;
      return r;
    }, Zl = {}, ys = function() {
      return Zl;
    }, Lt = function(e) {
      var r = Object.keys(e);
      return function(a) {
        for (var n = {}, i = 0; i < r.length; i++) {
          var s = r[i], o = a == null ? void 0 : a[s];
          n[s] = o === void 0 ? e[s] : o;
        }
        return n;
      };
    }, wr = function(e, r, a) {
      for (var n = e.length - 1; n >= 0 && !(e[n] === r && (e.splice(n, 1), a)); n--)
        ;
    }, oi = function(e) {
      e.splice(0, e.length);
    }, Ql = function(e, r) {
      for (var a = 0; a < r.length; a++) {
        var n = r[a];
        e.push(n);
      }
    }, er = function(e, r, a) {
      return a && (r = Et(a, r)), e[r];
    }, xr = function(e, r, a, n) {
      a && (r = Et(a, r)), e[r] = n;
    }, Jl = /* @__PURE__ */ function() {
      function t() {
        ce(this, t), this._obj = {};
      }
      return A(t, [{
        key: "set",
        value: function(r, a) {
          return this._obj[r] = a, this;
        }
      }, {
        key: "delete",
        value: function(r) {
          return this._obj[r] = void 0, this;
        }
      }, {
        key: "clear",
        value: function() {
          this._obj = {};
        }
      }, {
        key: "has",
        value: function(r) {
          return this._obj[r] !== void 0;
        }
      }, {
        key: "get",
        value: function(r) {
          return this._obj[r];
        }
      }]), t;
    }(), ur = typeof Map < "u" ? Map : Jl, jl = "undefined", ef = /* @__PURE__ */ function() {
      function t(e) {
        if (ce(this, t), this._obj = /* @__PURE__ */ Object.create(null), this.size = 0, e != null) {
          var r;
          e.instanceString != null && e.instanceString() === this.instanceString() ? r = e.toArray() : r = e;
          for (var a = 0; a < r.length; a++)
            this.add(r[a]);
        }
      }
      return A(t, [{
        key: "instanceString",
        value: function() {
          return "set";
        }
      }, {
        key: "add",
        value: function(r) {
          var a = this._obj;
          a[r] !== 1 && (a[r] = 1, this.size++);
        }
      }, {
        key: "delete",
        value: function(r) {
          var a = this._obj;
          a[r] === 1 && (a[r] = 0, this.size--);
        }
      }, {
        key: "clear",
        value: function() {
          this._obj = /* @__PURE__ */ Object.create(null);
        }
      }, {
        key: "has",
        value: function(r) {
          return this._obj[r] === 1;
        }
      }, {
        key: "toArray",
        value: function() {
          var r = this;
          return Object.keys(this._obj).filter(function(a) {
            return r.has(a);
          });
        }
      }, {
        key: "forEach",
        value: function(r, a) {
          return this.toArray().forEach(r, a);
        }
      }]), t;
    }(), Jr = (typeof Set > "u" ? "undefined" : Q(Set)) !== jl ? Set : ef, dn = function(e, r) {
      var a = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : !0;
      if (e === void 0 || r === void 0 || !_e(e)) {
        xt("An element must have a core reference and parameters set");
        return;
      }
      var n = r.group;
      if (n == null && (r.data && r.data.source != null && r.data.target != null ? n = "edges" : n = "nodes"), n !== "nodes" && n !== "edges") {
        xt("An element must be of type `nodes` or `edges`; you specified `" + n + "`");
        return;
      }
      this.length = 1, this[0] = this;
      var i = this._private = {
        cy: e,
        single: !0,
        // indicates this is an element
        data: r.data || {},
        // data object
        position: r.position || {
          x: 0,
          y: 0
        },
        // (x, y) position pair
        autoWidth: void 0,
        // width and height of nodes calculated by the renderer when set to special 'auto' value
        autoHeight: void 0,
        autoPadding: void 0,
        compoundBoundsClean: !1,
        // whether the compound dimensions need to be recalculated the next time dimensions are read
        listeners: [],
        // array of bound listeners
        group: n,
        // string; 'nodes' or 'edges'
        style: {},
        // properties as set by the style
        rstyle: {},
        // properties for style sent from the renderer to the core
        styleCxts: [],
        // applied style contexts from the styler
        styleKeys: {},
        // per-group keys of style property values
        removed: !0,
        // whether it's inside the vis; true if removed (set true here since we call restore)
        selected: !!r.selected,
        // whether it's selected
        selectable: r.selectable === void 0 ? !0 : !!r.selectable,
        // whether it's selectable
        locked: !!r.locked,
        // whether the element is locked (cannot be moved)
        grabbed: !1,
        // whether the element is grabbed by the mouse; renderer sets this privately
        grabbable: r.grabbable === void 0 ? !0 : !!r.grabbable,
        // whether the element can be grabbed
        pannable: r.pannable === void 0 ? n === "edges" : !!r.pannable,
        // whether the element has passthrough panning enabled
        active: !1,
        // whether the element is active from user interaction
        classes: new Jr(),
        // map ( className => true )
        animation: {
          // object for currently-running animations
          current: [],
          queue: []
        },
        rscratch: {},
        // object in which the renderer can store information
        scratch: r.scratch || {},
        // scratch objects
        edges: [],
        // array of connected edges
        children: [],
        // array of children
        parent: r.parent && r.parent.isNode() ? r.parent : null,
        // parent ref
        traversalCache: {},
        // cache of output of traversal functions
        backgrounding: !1,
        // whether background images are loading
        bbCache: null,
        // cache of the current bounding box
        bbCacheShift: {
          x: 0,
          y: 0
        },
        // shift applied to cached bb to be applied on next get
        bodyBounds: null,
        // bounds cache of element body, w/o overlay
        overlayBounds: null,
        // bounds cache of element body, including overlay
        labelBounds: {
          // bounds cache of labels
          all: null,
          source: null,
          target: null,
          main: null
        },
        arrowBounds: {
          // bounds cache of edge arrows
          source: null,
          target: null,
          "mid-source": null,
          "mid-target": null
        }
      };
      if (i.position.x == null && (i.position.x = 0), i.position.y == null && (i.position.y = 0), r.renderedPosition) {
        var s = r.renderedPosition, o = e.pan(), l = e.zoom();
        i.position = {
          x: (s.x - o.x) / l,
          y: (s.y - o.y) / l
        };
      }
      var u = [];
      te(r.classes) ? u = r.classes : ee(r.classes) && (u = r.classes.split(/\s+/));
      for (var f = 0, h = u.length; f < h; f++) {
        var c = u[f];
        !c || c === "" || i.classes.add(c);
      }
      this.createEmitter();
      var v = r.style || r.css;
      v && (ft("Setting a `style` bypass at element creation should be done only when absolutely necessary.  Try to use the stylesheet instead."), this.style(v)), (a === void 0 || a) && this.restore();
    }, ms = function(e) {
      return e = {
        bfs: e.bfs || !e.dfs,
        dfs: e.dfs || !e.bfs
      }, function(a, n, i) {
        var s;
        S(a) && !pe(a) && (s = a, a = s.roots || s.root, n = s.visit, i = s.directed), i = arguments.length === 2 && !H(n) ? n : i, n = H(n) ? n : function() {
        };
        for (var o = this._private.cy, l = a = ee(a) ? this.filter(a) : a, u = [], f = [], h = {}, c = {}, v = {}, d = 0, g, y = this.byGroup(), p = y.nodes, m = y.edges, b = 0; b < l.length; b++) {
          var E = l[b], M = E.id();
          E.isNode() && (u.unshift(E), e.bfs && (v[M] = !0, f.push(E)), c[M] = 0);
        }
        for (var O = function() {
          var X = e.bfs ? u.shift() : u.pop(), z = X.id();
          if (e.dfs) {
            if (v[z])
              return "continue";
            v[z] = !0, f.push(X);
          }
          var re = c[z], W = h[z], Z = W != null ? W.source() : null, ie = W != null ? W.target() : null, oe = W == null ? void 0 : X.same(Z) ? ie[0] : Z[0], ge = void 0;
          if (ge = n(X, W, oe, d++, re), ge === !0)
            return g = X, "break";
          if (ge === !1)
            return "break";
          for (var se = X.connectedEdges().filter(function(ye) {
            return (!i || ye.source().same(X)) && m.has(ye);
          }), de = 0; de < se.length; de++) {
            var we = se[de], Te = we.connectedNodes().filter(function(ye) {
              return !ye.same(X) && p.has(ye);
            }), Ee = Te.id();
            Te.length !== 0 && !v[Ee] && (Te = Te[0], u.push(Te), e.bfs && (v[Ee] = !0, f.push(Te)), h[Ee] = we, c[Ee] = c[z] + 1);
          }
        }; u.length !== 0; ) {
          var x = O();
          if (x !== "continue" && x === "break")
            break;
        }
        for (var I = o.collection(), C = 0; C < f.length; C++) {
          var B = f[C], F = h[B.id()];
          F != null && I.push(F), I.push(B);
        }
        return {
          path: o.collection(I),
          found: o.collection(g)
        };
      };
    }, Ia = {
      breadthFirstSearch: ms({
        bfs: !0
      }),
      depthFirstSearch: ms({
        dfs: !0
      })
    };
    Ia.bfs = Ia.breadthFirstSearch, Ia.dfs = Ia.depthFirstSearch;
    var tf = il(function(t, e) {
      (function() {
        var r, a, n, i, s, o, l, u, f, h, c, v, d, g, y;
        n = Math.floor, h = Math.min, a = function(p, m) {
          return p < m ? -1 : p > m ? 1 : 0;
        }, f = function(p, m, b, E, M) {
          var O;
          if (b == null && (b = 0), M == null && (M = a), b < 0)
            throw new Error("lo must be non-negative");
          for (E == null && (E = p.length); b < E; )
            O = n((b + E) / 2), M(m, p[O]) < 0 ? E = O : b = O + 1;
          return [].splice.apply(p, [b, b - b].concat(m)), m;
        }, o = function(p, m, b) {
          return b == null && (b = a), p.push(m), g(p, 0, p.length - 1, b);
        }, s = function(p, m) {
          var b, E;
          return m == null && (m = a), b = p.pop(), p.length ? (E = p[0], p[0] = b, y(p, 0, m)) : E = b, E;
        }, u = function(p, m, b) {
          var E;
          return b == null && (b = a), E = p[0], p[0] = m, y(p, 0, b), E;
        }, l = function(p, m, b) {
          var E;
          return b == null && (b = a), p.length && b(p[0], m) < 0 && (E = [p[0], m], m = E[0], p[0] = E[1], y(p, 0, b)), m;
        }, i = function(p, m) {
          var b, E, M, O, x, I;
          for (m == null && (m = a), O = function() {
            I = [];
            for (var C = 0, B = n(p.length / 2); 0 <= B ? C < B : C > B; 0 <= B ? C++ : C--)
              I.push(C);
            return I;
          }.apply(this).reverse(), x = [], E = 0, M = O.length; E < M; E++)
            b = O[E], x.push(y(p, b, m));
          return x;
        }, d = function(p, m, b) {
          var E;
          if (b == null && (b = a), E = p.indexOf(m), E !== -1)
            return g(p, 0, E, b), y(p, E, b);
        }, c = function(p, m, b) {
          var E, M, O, x, I;
          if (b == null && (b = a), M = p.slice(0, m), !M.length)
            return M;
          for (i(M, b), I = p.slice(m), O = 0, x = I.length; O < x; O++)
            E = I[O], l(M, E, b);
          return M.sort(b).reverse();
        }, v = function(p, m, b) {
          var E, M, O, x, I, C, B, F, R;
          if (b == null && (b = a), m * 10 <= p.length) {
            if (O = p.slice(0, m).sort(b), !O.length)
              return O;
            for (M = O[O.length - 1], B = p.slice(m), x = 0, C = B.length; x < C; x++)
              E = B[x], b(E, M) < 0 && (f(O, E, 0, null, b), O.pop(), M = O[O.length - 1]);
            return O;
          }
          for (i(p, b), R = [], I = 0, F = h(m, p.length); 0 <= F ? I < F : I > F; 0 <= F ? ++I : --I)
            R.push(s(p, b));
          return R;
        }, g = function(p, m, b, E) {
          var M, O, x;
          for (E == null && (E = a), M = p[b]; b > m; ) {
            if (x = b - 1 >> 1, O = p[x], E(M, O) < 0) {
              p[b] = O, b = x;
              continue;
            }
            break;
          }
          return p[b] = M;
        }, y = function(p, m, b) {
          var E, M, O, x, I;
          for (b == null && (b = a), M = p.length, I = m, O = p[m], E = 2 * m + 1; E < M; )
            x = E + 1, x < M && !(b(p[E], p[x]) < 0) && (E = x), p[m] = p[E], m = E, E = 2 * m + 1;
          return p[m] = O, g(p, I, m, b);
        }, r = function() {
          p.push = o, p.pop = s, p.replace = u, p.pushpop = l, p.heapify = i, p.updateItem = d, p.nlargest = c, p.nsmallest = v;
          function p(m) {
            this.cmp = m ?? a, this.nodes = [];
          }
          return p.prototype.push = function(m) {
            return o(this.nodes, m, this.cmp);
          }, p.prototype.pop = function() {
            return s(this.nodes, this.cmp);
          }, p.prototype.peek = function() {
            return this.nodes[0];
          }, p.prototype.contains = function(m) {
            return this.nodes.indexOf(m) !== -1;
          }, p.prototype.replace = function(m) {
            return u(this.nodes, m, this.cmp);
          }, p.prototype.pushpop = function(m) {
            return l(this.nodes, m, this.cmp);
          }, p.prototype.heapify = function() {
            return i(this.nodes, this.cmp);
          }, p.prototype.updateItem = function(m) {
            return d(this.nodes, m, this.cmp);
          }, p.prototype.clear = function() {
            return this.nodes = [];
          }, p.prototype.empty = function() {
            return this.nodes.length === 0;
          }, p.prototype.size = function() {
            return this.nodes.length;
          }, p.prototype.clone = function() {
            var m;
            return m = new p(), m.nodes = this.nodes.slice(0), m;
          }, p.prototype.toArray = function() {
            return this.nodes.slice(0);
          }, p.prototype.insert = p.prototype.push, p.prototype.top = p.prototype.peek, p.prototype.front = p.prototype.peek, p.prototype.has = p.prototype.contains, p.prototype.copy = p.prototype.clone, p;
        }(), function(p, m) {
          return t.exports = m();
        }(this, function() {
          return r;
        });
      }).call(Sa);
    }), Ra = tf, rf = Lt({
      root: null,
      weight: function(e) {
        return 1;
      },
      directed: !1
    }), af = {
      dijkstra: function(e) {
        if (!S(e)) {
          var r = arguments;
          e = {
            root: r[0],
            weight: r[1],
            directed: r[2]
          };
        }
        var a = rf(e), n = a.root, i = a.weight, s = a.directed, o = this, l = i, u = ee(n) ? this.filter(n)[0] : n[0], f = {}, h = {}, c = {}, v = this.byGroup(), d = v.nodes, g = v.edges;
        g.unmergeBy(function(re) {
          return re.isLoop();
        });
        for (var y = function(W) {
          return f[W.id()];
        }, p = function(W, Z) {
          f[W.id()] = Z, m.updateItem(W);
        }, m = new Ra(function(re, W) {
          return y(re) - y(W);
        }), b = 0; b < d.length; b++) {
          var E = d[b];
          f[E.id()] = E.same(u) ? 0 : 1 / 0, m.push(E);
        }
        for (var M = function(W, Z) {
          for (var ie = (s ? W.edgesTo(Z) : W.edgesWith(Z)).intersect(g), oe = 1 / 0, ge, se = 0; se < ie.length; se++) {
            var de = ie[se], we = l(de);
            (we < oe || !ge) && (oe = we, ge = de);
          }
          return {
            edge: ge,
            dist: oe
          };
        }; m.size() > 0; ) {
          var O = m.pop(), x = y(O), I = O.id();
          if (c[I] = x, x !== 1 / 0)
            for (var C = O.neighborhood().intersect(d), B = 0; B < C.length; B++) {
              var F = C[B], R = F.id(), X = M(O, F), z = x + X.dist;
              z < y(F) && (p(F, z), h[R] = {
                node: O,
                edge: X.edge
              });
            }
        }
        return {
          distanceTo: function(W) {
            var Z = ee(W) ? d.filter(W)[0] : W[0];
            return c[Z.id()];
          },
          pathTo: function(W) {
            var Z = ee(W) ? d.filter(W)[0] : W[0], ie = [], oe = Z, ge = oe.id();
            if (Z.length > 0)
              for (ie.unshift(Z); h[ge]; ) {
                var se = h[ge];
                ie.unshift(se.edge), ie.unshift(se.node), oe = se.node, ge = oe.id();
              }
            return o.spawn(ie);
          }
        };
      }
    }, nf = {
      // kruskal's algorithm (finds min spanning tree, assuming undirected graph)
      // implemented from pseudocode from wikipedia
      kruskal: function(e) {
        e = e || function(b) {
          return 1;
        };
        for (var r = this.byGroup(), a = r.nodes, n = r.edges, i = a.length, s = new Array(i), o = a, l = function(E) {
          for (var M = 0; M < s.length; M++) {
            var O = s[M];
            if (O.has(E))
              return M;
          }
        }, u = 0; u < i; u++)
          s[u] = this.spawn(a[u]);
        for (var f = n.sort(function(b, E) {
          return e(b) - e(E);
        }), h = 0; h < f.length; h++) {
          var c = f[h], v = c.source()[0], d = c.target()[0], g = l(v), y = l(d), p = s[g], m = s[y];
          g !== y && (o.merge(c), p.merge(m), s.splice(y, 1));
        }
        return o;
      }
    }, sf = Lt({
      root: null,
      goal: null,
      weight: function(e) {
        return 1;
      },
      heuristic: function(e) {
        return 0;
      },
      directed: !1
    }), of = {
      // Implemented from pseudocode from wikipedia
      aStar: function(e) {
        var r = this.cy(), a = sf(e), n = a.root, i = a.goal, s = a.heuristic, o = a.directed, l = a.weight;
        n = r.collection(n)[0], i = r.collection(i)[0];
        var u = n.id(), f = i.id(), h = {}, c = {}, v = {}, d = new Ra(function(ge, se) {
          return c[ge.id()] - c[se.id()];
        }), g = new Jr(), y = {}, p = {}, m = function(se, de) {
          d.push(se), g.add(de);
        }, b, E, M = function() {
          b = d.pop(), E = b.id(), g.delete(E);
        }, O = function(se) {
          return g.has(se);
        };
        m(n, u), h[u] = 0, c[u] = s(n);
        for (var x = 0; d.size() > 0; ) {
          if (M(), x++, E === f) {
            for (var I = [], C = i, B = f, F = p[B]; I.unshift(C), F != null && I.unshift(F), C = y[B], C != null; )
              B = C.id(), F = p[B];
            return {
              found: !0,
              distance: h[E],
              path: this.spawn(I),
              steps: x
            };
          }
          v[E] = !0;
          for (var R = b._private.edges, X = 0; X < R.length; X++) {
            var z = R[X];
            if (this.hasElementWithId(z.id()) && !(o && z.data("source") !== E)) {
              var re = z.source(), W = z.target(), Z = re.id() !== E ? re : W, ie = Z.id();
              if (this.hasElementWithId(ie) && !v[ie]) {
                var oe = h[E] + l(z);
                if (!O(ie)) {
                  h[ie] = oe, c[ie] = oe + s(Z), m(Z, ie), y[ie] = b, p[ie] = z;
                  continue;
                }
                oe < h[ie] && (h[ie] = oe, c[ie] = oe + s(Z), y[ie] = b, p[ie] = z);
              }
            }
          }
        }
        return {
          found: !1,
          distance: void 0,
          path: void 0,
          steps: x
        };
      }
    }, uf = Lt({
      weight: function(e) {
        return 1;
      },
      directed: !1
    }), lf = {
      // Implemented from pseudocode from wikipedia
      floydWarshall: function(e) {
        for (var r = this.cy(), a = uf(e), n = a.weight, i = a.directed, s = n, o = this.byGroup(), l = o.nodes, u = o.edges, f = l.length, h = f * f, c = function(we) {
          return l.indexOf(we);
        }, v = function(we) {
          return l[we];
        }, d = new Array(h), g = 0; g < h; g++) {
          var y = g % f, p = (g - y) / f;
          p === y ? d[g] = 0 : d[g] = 1 / 0;
        }
        for (var m = new Array(h), b = new Array(h), E = 0; E < u.length; E++) {
          var M = u[E], O = M.source()[0], x = M.target()[0];
          if (O !== x) {
            var I = c(O), C = c(x), B = I * f + C, F = s(M);
            if (d[B] > F && (d[B] = F, m[B] = C, b[B] = M), !i) {
              var R = C * f + I;
              !i && d[R] > F && (d[R] = F, m[R] = I, b[R] = M);
            }
          }
        }
        for (var X = 0; X < f; X++)
          for (var z = 0; z < f; z++)
            for (var re = z * f + X, W = 0; W < f; W++) {
              var Z = z * f + W, ie = X * f + W;
              d[re] + d[ie] < d[Z] && (d[Z] = d[re] + d[ie], m[Z] = m[re]);
            }
        var oe = function(we) {
          return (ee(we) ? r.filter(we) : we)[0];
        }, ge = function(we) {
          return c(oe(we));
        }, se = {
          distance: function(we, Te) {
            var Ee = ge(we), ye = ge(Te);
            return d[Ee * f + ye];
          },
          path: function(we, Te) {
            var Ee = ge(we), ye = ge(Te), ae = v(Ee);
            if (Ee === ye)
              return ae.collection();
            if (m[Ee * f + ye] == null)
              return r.collection();
            var xe = r.collection(), Ce = Ee, Oe;
            for (xe.merge(ae); Ee !== ye; )
              Ce = Ee, Ee = m[Ee * f + ye], Oe = b[Ce * f + Ee], xe.merge(Oe), xe.merge(v(Ee));
            return xe;
          }
        };
        return se;
      }
      // floydWarshall
    }, ff = Lt({
      weight: function(e) {
        return 1;
      },
      directed: !1,
      root: null
    }), hf = {
      // Implemented from pseudocode from wikipedia
      bellmanFord: function(e) {
        var r = this, a = ff(e), n = a.weight, i = a.directed, s = a.root, o = n, l = this, u = this.cy(), f = this.byGroup(), h = f.edges, c = f.nodes, v = c.length, d = new ur(), g = !1, y = [];
        s = u.collection(s)[0], h.unmergeBy(function(Fe) {
          return Fe.isLoop();
        });
        for (var p = h.length, m = function(ke) {
          var Ge = d.get(ke.id());
          return Ge || (Ge = {}, d.set(ke.id(), Ge)), Ge;
        }, b = function(ke) {
          return (ee(ke) ? u.$(ke) : ke)[0];
        }, E = function(ke) {
          return m(b(ke)).dist;
        }, M = function(ke) {
          for (var Ge = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : s, et = b(ke), We = [], Ye = et; ; ) {
            if (Ye == null)
              return r.spawn();
            var Se = m(Ye), N = Se.edge, le = Se.pred;
            if (We.unshift(Ye[0]), Ye.same(Ge) && We.length > 0)
              break;
            N != null && We.unshift(N), Ye = le;
          }
          return l.spawn(We);
        }, O = 0; O < v; O++) {
          var x = c[O], I = m(x);
          x.same(s) ? I.dist = 0 : I.dist = 1 / 0, I.pred = null, I.edge = null;
        }
        for (var C = !1, B = function(ke, Ge, et, We, Ye, Se) {
          var N = We.dist + Se;
          N < Ye.dist && !et.same(We.edge) && (Ye.dist = N, Ye.pred = ke, Ye.edge = et, C = !0);
        }, F = 1; F < v; F++) {
          C = !1;
          for (var R = 0; R < p; R++) {
            var X = h[R], z = X.source(), re = X.target(), W = o(X), Z = m(z), ie = m(re);
            B(z, re, X, Z, ie, W), i || B(re, z, X, ie, Z, W);
          }
          if (!C)
            break;
        }
        if (C)
          for (var oe = [], ge = 0; ge < p; ge++) {
            var se = h[ge], de = se.source(), we = se.target(), Te = o(se), Ee = m(de).dist, ye = m(we).dist;
            if (Ee + Te < ye || !i && ye + Te < Ee)
              if (g || (ft("Graph contains a negative weight cycle for Bellman-Ford"), g = !0), e.findNegativeWeightCycles !== !1) {
                var ae = [];
                Ee + Te < ye && ae.push(de), !i && ye + Te < Ee && ae.push(we);
                for (var xe = ae.length, Ce = 0; Ce < xe; Ce++) {
                  var Oe = ae[Ce], Ie = [Oe];
                  Ie.push(m(Oe).edge);
                  for (var He = m(Oe).pred; Ie.indexOf(He) === -1; )
                    Ie.push(He), Ie.push(m(He).edge), He = m(He).pred;
                  Ie = Ie.slice(Ie.indexOf(He));
                  for (var qe = Ie[0].id(), Re = 0, Me = 2; Me < Ie.length; Me += 2)
                    Ie[Me].id() < qe && (qe = Ie[Me].id(), Re = Me);
                  Ie = Ie.slice(Re).concat(Ie.slice(0, Re)), Ie.push(Ie[0]);
                  var Ve = Ie.map(function(Fe) {
                    return Fe.id();
                  }).join(",");
                  oe.indexOf(Ve) === -1 && (y.push(l.spawn(Ie)), oe.push(Ve));
                }
              } else
                break;
          }
        return {
          distanceTo: E,
          pathTo: M,
          hasNegativeWeightCycle: g,
          negativeWeightCycles: y
        };
      }
      // bellmanFord
    }, cf = Math.sqrt(2), vf = function(e, r, a) {
      a.length === 0 && xt("Karger-Stein must be run on a connected (sub)graph");
      for (var n = a[e], i = n[1], s = n[2], o = r[i], l = r[s], u = a, f = u.length - 1; f >= 0; f--) {
        var h = u[f], c = h[1], v = h[2];
        (r[c] === o && r[v] === l || r[c] === l && r[v] === o) && u.splice(f, 1);
      }
      for (var d = 0; d < u.length; d++) {
        var g = u[d];
        g[1] === l ? (u[d] = g.slice(), u[d][1] = o) : g[2] === l && (u[d] = g.slice(), u[d][2] = o);
      }
      for (var y = 0; y < r.length; y++)
        r[y] === l && (r[y] = o);
      return u;
    }, ui = function(e, r, a, n) {
      for (; a > n; ) {
        var i = Math.floor(Math.random() * r.length);
        r = vf(i, e, r), a--;
      }
      return r;
    }, df = {
      // Computes the minimum cut of an undirected graph
      // Returns the correct answer with high probability
      kargerStein: function() {
        var e = this, r = this.byGroup(), a = r.nodes, n = r.edges;
        n.unmergeBy(function(ie) {
          return ie.isLoop();
        });
        var i = a.length, s = n.length, o = Math.ceil(Math.pow(Math.log(i) / Math.LN2, 2)), l = Math.floor(i / cf);
        if (i < 2) {
          xt("At least 2 nodes are required for Karger-Stein algorithm");
          return;
        }
        for (var u = [], f = 0; f < s; f++) {
          var h = n[f];
          u.push([f, a.indexOf(h.source()), a.indexOf(h.target())]);
        }
        for (var c = 1 / 0, v = [], d = new Array(i), g = new Array(i), y = new Array(i), p = function(oe, ge) {
          for (var se = 0; se < i; se++)
            ge[se] = oe[se];
        }, m = 0; m <= o; m++) {
          for (var b = 0; b < i; b++)
            g[b] = b;
          var E = ui(g, u.slice(), i, l), M = E.slice();
          p(g, y);
          var O = ui(g, E, l, 2), x = ui(y, M, l, 2);
          O.length <= x.length && O.length < c ? (c = O.length, v = O, p(g, d)) : x.length <= O.length && x.length < c && (c = x.length, v = x, p(y, d));
        }
        for (var I = this.spawn(v.map(function(ie) {
          return n[ie[0]];
        })), C = this.spawn(), B = this.spawn(), F = d[0], R = 0; R < d.length; R++) {
          var X = d[R], z = a[R];
          X === F ? C.merge(z) : B.merge(z);
        }
        var re = function(oe) {
          var ge = e.spawn();
          return oe.forEach(function(se) {
            ge.merge(se), se.connectedEdges().forEach(function(de) {
              e.contains(de) && !I.contains(de) && ge.merge(de);
            });
          }), ge;
        }, W = [re(C), re(B)], Z = {
          cut: I,
          components: W,
          // n.b. partitions are included to be compatible with the old api spec
          // (could be removed in a future major version)
          partition1: C,
          partition2: B
        };
        return Z;
      }
    }, gf = function(e) {
      return {
        x: e.x,
        y: e.y
      };
    }, gn = function(e, r, a) {
      return {
        x: e.x * r + a.x,
        y: e.y * r + a.y
      };
    }, bs = function(e, r, a) {
      return {
        x: (e.x - a.x) / r,
        y: (e.y - a.y) / r
      };
    }, jr = function(e) {
      return {
        x: e[0],
        y: e[1]
      };
    }, pf = function(e) {
      for (var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 0, a = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : e.length, n = 1 / 0, i = r; i < a; i++) {
        var s = e[i];
        isFinite(s) && (n = Math.min(s, n));
      }
      return n;
    }, yf = function(e) {
      for (var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 0, a = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : e.length, n = -1 / 0, i = r; i < a; i++) {
        var s = e[i];
        isFinite(s) && (n = Math.max(s, n));
      }
      return n;
    }, mf = function(e) {
      for (var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 0, a = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : e.length, n = 0, i = 0, s = r; s < a; s++) {
        var o = e[s];
        isFinite(o) && (n += o, i++);
      }
      return n / i;
    }, bf = function(e) {
      var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 0, a = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : e.length, n = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : !0, i = arguments.length > 4 && arguments[4] !== void 0 ? arguments[4] : !0, s = arguments.length > 5 && arguments[5] !== void 0 ? arguments[5] : !0;
      n ? e = e.slice(r, a) : (a < e.length && e.splice(a, e.length - a), r > 0 && e.splice(0, r));
      for (var o = 0, l = e.length - 1; l >= 0; l--) {
        var u = e[l];
        s ? isFinite(u) || (e[l] = -1 / 0, o++) : e.splice(l, 1);
      }
      i && e.sort(function(c, v) {
        return c - v;
      });
      var f = e.length, h = Math.floor(f / 2);
      return f % 2 !== 0 ? e[h + 1 + o] : (e[h - 1 + o] + e[h + o]) / 2;
    }, Ef = function(e) {
      return Math.PI * e / 180;
    }, pn = function(e, r) {
      return Math.atan2(r, e) - Math.PI / 2;
    }, li = Math.log2 || function(t) {
      return Math.log(t) / Math.log(2);
    }, Es = function(e) {
      return e > 0 ? 1 : e < 0 ? -1 : 0;
    }, Pr = function(e, r) {
      return Math.sqrt(Br(e, r));
    }, Br = function(e, r) {
      var a = r.x - e.x, n = r.y - e.y;
      return a * a + n * n;
    }, wf = function(e) {
      for (var r = e.length, a = 0, n = 0; n < r; n++)
        a += e[n];
      for (var i = 0; i < r; i++)
        e[i] = e[i] / a;
      return e;
    }, St = function(e, r, a, n) {
      return (1 - n) * (1 - n) * e + 2 * (1 - n) * n * r + n * n * a;
    }, ea = function(e, r, a, n) {
      return {
        x: St(e.x, r.x, a.x, n),
        y: St(e.y, r.y, a.y, n)
      };
    }, xf = function(e, r, a, n) {
      var i = {
        x: r.x - e.x,
        y: r.y - e.y
      }, s = Pr(e, r), o = {
        x: i.x / s,
        y: i.y / s
      };
      return a = a ?? 0, n = n ?? a * s, {
        x: e.x + o.x * n,
        y: e.y + o.y * n
      };
    }, ka = function(e, r, a) {
      return Math.max(e, Math.min(a, r));
    }, Ut = function(e) {
      if (e == null)
        return {
          x1: 1 / 0,
          y1: 1 / 0,
          x2: -1 / 0,
          y2: -1 / 0,
          w: 0,
          h: 0
        };
      if (e.x1 != null && e.y1 != null) {
        if (e.x2 != null && e.y2 != null && e.x2 >= e.x1 && e.y2 >= e.y1)
          return {
            x1: e.x1,
            y1: e.y1,
            x2: e.x2,
            y2: e.y2,
            w: e.x2 - e.x1,
            h: e.y2 - e.y1
          };
        if (e.w != null && e.h != null && e.w >= 0 && e.h >= 0)
          return {
            x1: e.x1,
            y1: e.y1,
            x2: e.x1 + e.w,
            y2: e.y1 + e.h,
            w: e.w,
            h: e.h
          };
      }
    }, Tf = function(e) {
      return {
        x1: e.x1,
        x2: e.x2,
        w: e.w,
        y1: e.y1,
        y2: e.y2,
        h: e.h
      };
    }, Cf = function(e) {
      e.x1 = 1 / 0, e.y1 = 1 / 0, e.x2 = -1 / 0, e.y2 = -1 / 0, e.w = 0, e.h = 0;
    }, Df = function(e, r) {
      e.x1 = Math.min(e.x1, r.x1), e.x2 = Math.max(e.x2, r.x2), e.w = e.x2 - e.x1, e.y1 = Math.min(e.y1, r.y1), e.y2 = Math.max(e.y2, r.y2), e.h = e.y2 - e.y1;
    }, Sf = function(e, r, a) {
      e.x1 = Math.min(e.x1, r), e.x2 = Math.max(e.x2, r), e.w = e.x2 - e.x1, e.y1 = Math.min(e.y1, a), e.y2 = Math.max(e.y2, a), e.h = e.y2 - e.y1;
    }, yn = function(e) {
      var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 0;
      return e.x1 -= r, e.x2 += r, e.y1 -= r, e.y2 += r, e.w = e.x2 - e.x1, e.h = e.y2 - e.y1, e;
    }, fi = function(e) {
      var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [0], a, n, i, s;
      if (r.length === 1)
        a = n = i = s = r[0];
      else if (r.length === 2)
        a = i = r[0], s = n = r[1];
      else if (r.length === 4) {
        var o = w(r, 4);
        a = o[0], n = o[1], i = o[2], s = o[3];
      }
      return e.x1 -= s, e.x2 += n, e.y1 -= a, e.y2 += i, e.w = e.x2 - e.x1, e.h = e.y2 - e.y1, e;
    }, ws = function(e, r) {
      e.x1 = r.x1, e.y1 = r.y1, e.x2 = r.x2, e.y2 = r.y2, e.w = e.x2 - e.x1, e.h = e.y2 - e.y1;
    }, hi = function(e, r) {
      return !(e.x1 > r.x2 || r.x1 > e.x2 || e.x2 < r.x1 || r.x2 < e.x1 || e.y2 < r.y1 || r.y2 < e.y1 || e.y1 > r.y2 || r.y1 > e.y2);
    }, ta = function(e, r, a) {
      return e.x1 <= r && r <= e.x2 && e.y1 <= a && a <= e.y2;
    }, Lf = function(e, r) {
      return ta(e, r.x, r.y);
    }, xs = function(e, r) {
      return ta(e, r.x1, r.y1) && ta(e, r.x2, r.y2);
    }, Ts = function(e, r, a, n, i, s, o) {
      var l = Fa(i, s), u = i / 2, f = s / 2, h;
      {
        var c = a - u + l - o, v = n - f - o, d = a + u - l + o, g = v;
        if (h = Tr(e, r, a, n, c, v, d, g, !1), h.length > 0)
          return h;
      }
      {
        var y = a + u + o, p = n - f + l - o, m = y, b = n + f - l + o;
        if (h = Tr(e, r, a, n, y, p, m, b, !1), h.length > 0)
          return h;
      }
      {
        var E = a - u + l - o, M = n + f + o, O = a + u - l + o, x = M;
        if (h = Tr(e, r, a, n, E, M, O, x, !1), h.length > 0)
          return h;
      }
      {
        var I = a - u - o, C = n - f + l - o, B = I, F = n + f - l + o;
        if (h = Tr(e, r, a, n, I, C, B, F, !1), h.length > 0)
          return h;
      }
      var R;
      {
        var X = a - u + l, z = n - f + l;
        if (R = Pa(e, r, a, n, X, z, l + o), R.length > 0 && R[0] <= X && R[1] <= z)
          return [R[0], R[1]];
      }
      {
        var re = a + u - l, W = n - f + l;
        if (R = Pa(e, r, a, n, re, W, l + o), R.length > 0 && R[0] >= re && R[1] <= W)
          return [R[0], R[1]];
      }
      {
        var Z = a + u - l, ie = n + f - l;
        if (R = Pa(e, r, a, n, Z, ie, l + o), R.length > 0 && R[0] >= Z && R[1] >= ie)
          return [R[0], R[1]];
      }
      {
        var oe = a - u + l, ge = n + f - l;
        if (R = Pa(e, r, a, n, oe, ge, l + o), R.length > 0 && R[0] <= oe && R[1] >= ge)
          return [R[0], R[1]];
      }
      return [];
    }, Af = function(e, r, a, n, i, s, o) {
      var l = o, u = Math.min(a, i), f = Math.max(a, i), h = Math.min(n, s), c = Math.max(n, s);
      return u - l <= e && e <= f + l && h - l <= r && r <= c + l;
    }, Of = function(e, r, a, n, i, s, o, l, u) {
      var f = {
        x1: Math.min(a, o, i) - u,
        x2: Math.max(a, o, i) + u,
        y1: Math.min(n, l, s) - u,
        y2: Math.max(n, l, s) + u
      };
      return !(e < f.x1 || e > f.x2 || r < f.y1 || r > f.y2);
    }, Nf = function(e, r, a, n) {
      a -= n;
      var i = r * r - 4 * e * a;
      if (i < 0)
        return [];
      var s = Math.sqrt(i), o = 2 * e, l = (-r + s) / o, u = (-r - s) / o;
      return [l, u];
    }, Mf = function(e, r, a, n, i) {
      var s = 1e-5;
      e === 0 && (e = s), r /= e, a /= e, n /= e;
      var o, l, u, f, h, c, v, d;
      if (l = (3 * a - r * r) / 9, u = -(27 * n) + r * (9 * a - 2 * (r * r)), u /= 54, o = l * l * l + u * u, i[1] = 0, v = r / 3, o > 0) {
        h = u + Math.sqrt(o), h = h < 0 ? -Math.pow(-h, 1 / 3) : Math.pow(h, 1 / 3), c = u - Math.sqrt(o), c = c < 0 ? -Math.pow(-c, 1 / 3) : Math.pow(c, 1 / 3), i[0] = -v + h + c, v += (h + c) / 2, i[4] = i[2] = -v, v = Math.sqrt(3) * (-c + h) / 2, i[3] = v, i[5] = -v;
        return;
      }
      if (i[5] = i[3] = 0, o === 0) {
        d = u < 0 ? -Math.pow(-u, 1 / 3) : Math.pow(u, 1 / 3), i[0] = -v + 2 * d, i[4] = i[2] = -(d + v);
        return;
      }
      l = -l, f = l * l * l, f = Math.acos(u / Math.sqrt(f)), d = 2 * Math.sqrt(l), i[0] = -v + d * Math.cos(f / 3), i[2] = -v + d * Math.cos((f + 2 * Math.PI) / 3), i[4] = -v + d * Math.cos((f + 4 * Math.PI) / 3);
    }, If = function(e, r, a, n, i, s, o, l) {
      var u = 1 * a * a - 4 * a * i + 2 * a * o + 4 * i * i - 4 * i * o + o * o + n * n - 4 * n * s + 2 * n * l + 4 * s * s - 4 * s * l + l * l, f = 1 * 9 * a * i - 3 * a * a - 3 * a * o - 6 * i * i + 3 * i * o + 9 * n * s - 3 * n * n - 3 * n * l - 6 * s * s + 3 * s * l, h = 1 * 3 * a * a - 6 * a * i + a * o - a * e + 2 * i * i + 2 * i * e - o * e + 3 * n * n - 6 * n * s + n * l - n * r + 2 * s * s + 2 * s * r - l * r, c = 1 * a * i - a * a + a * e - i * e + n * s - n * n + n * r - s * r, v = [];
      Mf(u, f, h, c, v);
      for (var d = 1e-7, g = [], y = 0; y < 6; y += 2)
        Math.abs(v[y + 1]) < d && v[y] >= 0 && v[y] <= 1 && g.push(v[y]);
      g.push(1), g.push(0);
      for (var p = -1, m, b, E, M = 0; M < g.length; M++)
        m = Math.pow(1 - g[M], 2) * a + 2 * (1 - g[M]) * g[M] * i + g[M] * g[M] * o, b = Math.pow(1 - g[M], 2) * n + 2 * (1 - g[M]) * g[M] * s + g[M] * g[M] * l, E = Math.pow(m - e, 2) + Math.pow(b - r, 2), p >= 0 ? E < p && (p = E) : p = E;
      return p;
    }, Rf = function(e, r, a, n, i, s) {
      var o = [e - a, r - n], l = [i - a, s - n], u = l[0] * l[0] + l[1] * l[1], f = o[0] * o[0] + o[1] * o[1], h = o[0] * l[0] + o[1] * l[1], c = h * h / u;
      return h < 0 ? f : c > u ? (e - i) * (e - i) + (r - s) * (r - s) : f - c;
    }, Yt = function(e, r, a) {
      for (var n, i, s, o, l, u = 0, f = 0; f < a.length / 2; f++)
        if (n = a[f * 2], i = a[f * 2 + 1], f + 1 < a.length / 2 ? (s = a[(f + 1) * 2], o = a[(f + 1) * 2 + 1]) : (s = a[(f + 1 - a.length / 2) * 2], o = a[(f + 1 - a.length / 2) * 2 + 1]), !(n == e && s == e))
          if (n >= e && e >= s || n <= e && e <= s)
            l = (e - n) / (s - n) * (o - i) + i, l > r && u++;
          else
            continue;
      return u % 2 !== 0;
    }, gr = function(e, r, a, n, i, s, o, l, u) {
      var f = new Array(a.length), h;
      l[0] != null ? (h = Math.atan(l[1] / l[0]), l[0] < 0 ? h = h + Math.PI / 2 : h = -h - Math.PI / 2) : h = l;
      for (var c = Math.cos(-h), v = Math.sin(-h), d = 0; d < f.length / 2; d++)
        f[d * 2] = s / 2 * (a[d * 2] * c - a[d * 2 + 1] * v), f[d * 2 + 1] = o / 2 * (a[d * 2 + 1] * c + a[d * 2] * v), f[d * 2] += n, f[d * 2 + 1] += i;
      var g;
      if (u > 0) {
        var y = Ds(f, -u);
        g = Cs(y);
      } else
        g = f;
      return Yt(e, r, g);
    }, kf = function(e, r, a, n, i, s, o) {
      for (var l = new Array(a.length), u = s / 2, f = o / 2, h = di(s, o), c = h * h, v = 0; v < a.length / 4; v++) {
        var d = void 0, g = void 0;
        v === 0 ? d = a.length - 2 : d = v * 4 - 2, g = v * 4 + 2;
        var y = n + u * a[v * 4], p = i + f * a[v * 4 + 1], m = -a[d] * a[g] - a[d + 1] * a[g + 1], b = h / Math.tan(Math.acos(m) / 2), E = y - b * a[d], M = p - b * a[d + 1], O = y + b * a[g], x = p + b * a[g + 1];
        l[v * 4] = E, l[v * 4 + 1] = M, l[v * 4 + 2] = O, l[v * 4 + 3] = x;
        var I = a[d + 1], C = -a[d], B = I * a[g] + C * a[g + 1];
        B < 0 && (I *= -1, C *= -1);
        var F = E + I * h, R = M + C * h, X = Math.pow(F - e, 2) + Math.pow(R - r, 2);
        if (X <= c)
          return !0;
      }
      return Yt(e, r, l);
    }, Cs = function(e) {
      for (var r = new Array(e.length / 2), a, n, i, s, o, l, u, f, h = 0; h < e.length / 4; h++) {
        a = e[h * 4], n = e[h * 4 + 1], i = e[h * 4 + 2], s = e[h * 4 + 3], h < e.length / 4 - 1 ? (o = e[(h + 1) * 4], l = e[(h + 1) * 4 + 1], u = e[(h + 1) * 4 + 2], f = e[(h + 1) * 4 + 3]) : (o = e[0], l = e[1], u = e[2], f = e[3]);
        var c = Tr(a, n, i, s, o, l, u, f, !0);
        r[h * 2] = c[0], r[h * 2 + 1] = c[1];
      }
      return r;
    }, Ds = function(e, r) {
      for (var a = new Array(e.length * 2), n, i, s, o, l = 0; l < e.length / 2; l++) {
        n = e[l * 2], i = e[l * 2 + 1], l < e.length / 2 - 1 ? (s = e[(l + 1) * 2], o = e[(l + 1) * 2 + 1]) : (s = e[0], o = e[1]);
        var u = o - i, f = -(s - n), h = Math.sqrt(u * u + f * f), c = u / h, v = f / h;
        a[l * 4] = n + c * r, a[l * 4 + 1] = i + v * r, a[l * 4 + 2] = s + c * r, a[l * 4 + 3] = o + v * r;
      }
      return a;
    }, Pf = function(e, r, a, n, i, s) {
      var o = a - e, l = n - r;
      o /= i, l /= s;
      var u = Math.sqrt(o * o + l * l), f = u - 1;
      if (f < 0)
        return [];
      var h = f / u;
      return [(a - e) * h + e, (n - r) * h + r];
    }, Fr = function(e, r, a, n, i, s, o) {
      return e -= i, r -= s, e /= a / 2 + o, r /= n / 2 + o, e * e + r * r <= 1;
    }, Pa = function(e, r, a, n, i, s, o) {
      var l = [a - e, n - r], u = [e - i, r - s], f = l[0] * l[0] + l[1] * l[1], h = 2 * (u[0] * l[0] + u[1] * l[1]), c = u[0] * u[0] + u[1] * u[1] - o * o, v = h * h - 4 * f * c;
      if (v < 0)
        return [];
      var d = (-h + Math.sqrt(v)) / (2 * f), g = (-h - Math.sqrt(v)) / (2 * f), y = Math.min(d, g), p = Math.max(d, g), m = [];
      if (y >= 0 && y <= 1 && m.push(y), p >= 0 && p <= 1 && m.push(p), m.length === 0)
        return [];
      var b = m[0] * l[0] + e, E = m[0] * l[1] + r;
      if (m.length > 1) {
        if (m[0] == m[1])
          return [b, E];
        var M = m[1] * l[0] + e, O = m[1] * l[1] + r;
        return [b, E, M, O];
      } else
        return [b, E];
    }, ci = function(e, r, a) {
      return r <= e && e <= a || a <= e && e <= r ? e : e <= r && r <= a || a <= r && r <= e ? r : a;
    }, Tr = function(e, r, a, n, i, s, o, l, u) {
      var f = e - i, h = a - e, c = o - i, v = r - s, d = n - r, g = l - s, y = c * v - g * f, p = h * v - d * f, m = g * h - c * d;
      if (m !== 0) {
        var b = y / m, E = p / m, M = 1e-3, O = 0 - M, x = 1 + M;
        return O <= b && b <= x && O <= E && E <= x ? [e + b * h, r + b * d] : u ? [e + b * h, r + b * d] : [];
      } else
        return y === 0 || p === 0 ? ci(e, a, o) === o ? [o, l] : ci(e, a, i) === i ? [i, s] : ci(i, o, a) === a ? [a, n] : [] : [];
    }, Ba = function(e, r, a, n, i, s, o, l) {
      var u = [], f, h = new Array(a.length), c = !0;
      s == null && (c = !1);
      var v;
      if (c) {
        for (var d = 0; d < h.length / 2; d++)
          h[d * 2] = a[d * 2] * s + n, h[d * 2 + 1] = a[d * 2 + 1] * o + i;
        if (l > 0) {
          var g = Ds(h, -l);
          v = Cs(g);
        } else
          v = h;
      } else
        v = a;
      for (var y, p, m, b, E = 0; E < v.length / 2; E++)
        y = v[E * 2], p = v[E * 2 + 1], E < v.length / 2 - 1 ? (m = v[(E + 1) * 2], b = v[(E + 1) * 2 + 1]) : (m = v[0], b = v[1]), f = Tr(e, r, n, i, y, p, m, b), f.length !== 0 && u.push(f[0], f[1]);
      return u;
    }, Bf = function(e, r, a, n, i, s, o, l) {
      for (var u = [], f, h = new Array(a.length), c = s / 2, v = o / 2, d = di(s, o), g = 0; g < a.length / 4; g++) {
        var y = void 0, p = void 0;
        g === 0 ? y = a.length - 2 : y = g * 4 - 2, p = g * 4 + 2;
        var m = n + c * a[g * 4], b = i + v * a[g * 4 + 1], E = -a[y] * a[p] - a[y + 1] * a[p + 1], M = d / Math.tan(Math.acos(E) / 2), O = m - M * a[y], x = b - M * a[y + 1], I = m + M * a[p], C = b + M * a[p + 1];
        g === 0 ? (h[a.length - 2] = O, h[a.length - 1] = x) : (h[g * 4 - 2] = O, h[g * 4 - 1] = x), h[g * 4] = I, h[g * 4 + 1] = C;
        var B = a[y + 1], F = -a[y], R = B * a[p] + F * a[p + 1];
        R < 0 && (B *= -1, F *= -1);
        var X = O + B * d, z = x + F * d;
        f = Pa(e, r, n, i, X, z, d), f.length !== 0 && u.push(f[0], f[1]);
      }
      for (var re = 0; re < h.length / 4; re++)
        f = Tr(e, r, n, i, h[re * 4], h[re * 4 + 1], h[re * 4 + 2], h[re * 4 + 3], !1), f.length !== 0 && u.push(f[0], f[1]);
      if (u.length > 2) {
        for (var W = [u[0], u[1]], Z = Math.pow(W[0] - e, 2) + Math.pow(W[1] - r, 2), ie = 1; ie < u.length / 2; ie++) {
          var oe = Math.pow(u[ie * 2] - e, 2) + Math.pow(u[ie * 2 + 1] - r, 2);
          oe <= Z && (W[0] = u[ie * 2], W[1] = u[ie * 2 + 1], Z = oe);
        }
        return W;
      }
      return u;
    }, mn = function(e, r, a) {
      var n = [e[0] - r[0], e[1] - r[1]], i = Math.sqrt(n[0] * n[0] + n[1] * n[1]), s = (i - a) / i;
      return s < 0 && (s = 1e-5), [r[0] + s * n[0], r[1] + s * n[1]];
    }, $t = function(e, r) {
      var a = vi(e, r);
      return a = Ss(a), a;
    }, Ss = function(e) {
      for (var r, a, n = e.length / 2, i = 1 / 0, s = 1 / 0, o = -1 / 0, l = -1 / 0, u = 0; u < n; u++)
        r = e[2 * u], a = e[2 * u + 1], i = Math.min(i, r), o = Math.max(o, r), s = Math.min(s, a), l = Math.max(l, a);
      for (var f = 2 / (o - i), h = 2 / (l - s), c = 0; c < n; c++)
        r = e[2 * c] = e[2 * c] * f, a = e[2 * c + 1] = e[2 * c + 1] * h, i = Math.min(i, r), o = Math.max(o, r), s = Math.min(s, a), l = Math.max(l, a);
      if (s < -1)
        for (var v = 0; v < n; v++)
          a = e[2 * v + 1] = e[2 * v + 1] + (-1 - s);
      return e;
    }, vi = function(e, r) {
      var a = 1 / e * 2 * Math.PI, n = e % 2 === 0 ? Math.PI / 2 + a / 2 : Math.PI / 2;
      n += r;
      for (var i = new Array(e * 2), s, o = 0; o < e; o++)
        s = o * a + n, i[2 * o] = Math.cos(s), i[2 * o + 1] = Math.sin(-s);
      return i;
    }, Fa = function(e, r) {
      return Math.min(e / 4, r / 4, 8);
    }, di = function(e, r) {
      return Math.min(e / 10, r / 10, 8);
    }, Ls = function() {
      return 8;
    }, Ff = function(e, r, a) {
      return [e - 2 * r + a, 2 * (r - e), e];
    }, gi = function(e, r) {
      return {
        heightOffset: Math.min(15, 0.05 * r),
        widthOffset: Math.min(100, 0.25 * e),
        ctrlPtOffsetPct: 0.05
      };
    }, zf = Lt({
      dampingFactor: 0.8,
      precision: 1e-6,
      iterations: 200,
      weight: function(e) {
        return 1;
      }
    }), Gf = {
      pageRank: function(e) {
        for (var r = zf(e), a = r.dampingFactor, n = r.precision, i = r.iterations, s = r.weight, o = this._private.cy, l = this.byGroup(), u = l.nodes, f = l.edges, h = u.length, c = h * h, v = f.length, d = new Array(c), g = new Array(h), y = (1 - a) / h, p = 0; p < h; p++) {
          for (var m = 0; m < h; m++) {
            var b = p * h + m;
            d[b] = 0;
          }
          g[p] = 0;
        }
        for (var E = 0; E < v; E++) {
          var M = f[E], O = M.data("source"), x = M.data("target");
          if (O !== x) {
            var I = u.indexOfId(O), C = u.indexOfId(x), B = s(M), F = C * h + I;
            d[F] += B, g[I] += B;
          }
        }
        for (var R = 1 / h + y, X = 0; X < h; X++)
          if (g[X] === 0)
            for (var z = 0; z < h; z++) {
              var re = z * h + X;
              d[re] = R;
            }
          else
            for (var W = 0; W < h; W++) {
              var Z = W * h + X;
              d[Z] = d[Z] / g[X] + y;
            }
        for (var ie = new Array(h), oe = new Array(h), ge, se = 0; se < h; se++)
          ie[se] = 1;
        for (var de = 0; de < i; de++) {
          for (var we = 0; we < h; we++)
            oe[we] = 0;
          for (var Te = 0; Te < h; Te++)
            for (var Ee = 0; Ee < h; Ee++) {
              var ye = Te * h + Ee;
              oe[Te] += d[ye] * ie[Ee];
            }
          wf(oe), ge = ie, ie = oe, oe = ge;
          for (var ae = 0, xe = 0; xe < h; xe++) {
            var Ce = ge[xe] - ie[xe];
            ae += Ce * Ce;
          }
          if (ae < n)
            break;
        }
        var Oe = {
          rank: function(He) {
            return He = o.collection(He)[0], ie[u.indexOf(He)];
          }
        };
        return Oe;
      }
      // pageRank
    }, As = Lt({
      root: null,
      weight: function(e) {
        return 1;
      },
      directed: !1,
      alpha: 0
    }), ra = {
      degreeCentralityNormalized: function(e) {
        e = As(e);
        var r = this.cy(), a = this.nodes(), n = a.length;
        if (e.directed) {
          for (var f = {}, h = {}, c = 0, v = 0, d = 0; d < n; d++) {
            var g = a[d], y = g.id();
            e.root = g;
            var p = this.degreeCentrality(e);
            c < p.indegree && (c = p.indegree), v < p.outdegree && (v = p.outdegree), f[y] = p.indegree, h[y] = p.outdegree;
          }
          return {
            indegree: function(b) {
              return c == 0 ? 0 : (ee(b) && (b = r.filter(b)), f[b.id()] / c);
            },
            outdegree: function(b) {
              return v === 0 ? 0 : (ee(b) && (b = r.filter(b)), h[b.id()] / v);
            }
          };
        } else {
          for (var i = {}, s = 0, o = 0; o < n; o++) {
            var l = a[o];
            e.root = l;
            var u = this.degreeCentrality(e);
            s < u.degree && (s = u.degree), i[l.id()] = u.degree;
          }
          return {
            degree: function(b) {
              return s === 0 ? 0 : (ee(b) && (b = r.filter(b)), i[b.id()] / s);
            }
          };
        }
      },
      // degreeCentralityNormalized
      // Implemented from the algorithm in Opsahl's paper
      // "Node centrality in weighted networks: Generalizing degree and shortest paths"
      // check the heading 2 "Degree"
      degreeCentrality: function(e) {
        e = As(e);
        var r = this.cy(), a = this, n = e, i = n.root, s = n.weight, o = n.directed, l = n.alpha;
        if (i = r.collection(i)[0], o) {
          for (var v = i.connectedEdges(), d = v.filter(function(O) {
            return O.target().same(i) && a.has(O);
          }), g = v.filter(function(O) {
            return O.source().same(i) && a.has(O);
          }), y = d.length, p = g.length, m = 0, b = 0, E = 0; E < d.length; E++)
            m += s(d[E]);
          for (var M = 0; M < g.length; M++)
            b += s(g[M]);
          return {
            indegree: Math.pow(y, 1 - l) * Math.pow(m, l),
            outdegree: Math.pow(p, 1 - l) * Math.pow(b, l)
          };
        } else {
          for (var u = i.connectedEdges().intersection(a), f = u.length, h = 0, c = 0; c < u.length; c++)
            h += s(u[c]);
          return {
            degree: Math.pow(f, 1 - l) * Math.pow(h, l)
          };
        }
      }
      // degreeCentrality
    };
    ra.dc = ra.degreeCentrality, ra.dcn = ra.degreeCentralityNormalised = ra.degreeCentralityNormalized;
    var Os = Lt({
      harmonic: !0,
      weight: function() {
        return 1;
      },
      directed: !1,
      root: null
    }), aa = {
      closenessCentralityNormalized: function(e) {
        for (var r = Os(e), a = r.harmonic, n = r.weight, i = r.directed, s = this.cy(), o = {}, l = 0, u = this.nodes(), f = this.floydWarshall({
          weight: n,
          directed: i
        }), h = 0; h < u.length; h++) {
          for (var c = 0, v = u[h], d = 0; d < u.length; d++)
            if (h !== d) {
              var g = f.distance(v, u[d]);
              a ? c += 1 / g : c += g;
            }
          a || (c = 1 / c), l < c && (l = c), o[v.id()] = c;
        }
        return {
          closeness: function(p) {
            return l == 0 ? 0 : (ee(p) ? p = s.filter(p)[0].id() : p = p.id(), o[p] / l);
          }
        };
      },
      // Implemented from pseudocode from wikipedia
      closenessCentrality: function(e) {
        var r = Os(e), a = r.root, n = r.weight, i = r.directed, s = r.harmonic;
        a = this.filter(a)[0];
        for (var o = this.dijkstra({
          root: a,
          weight: n,
          directed: i
        }), l = 0, u = this.nodes(), f = 0; f < u.length; f++) {
          var h = u[f];
          if (!h.same(a)) {
            var c = o.distanceTo(h);
            s ? l += 1 / c : l += c;
          }
        }
        return s ? l : 1 / l;
      }
      // closenessCentrality
    };
    aa.cc = aa.closenessCentrality, aa.ccn = aa.closenessCentralityNormalised = aa.closenessCentralityNormalized;
    var $f = Lt({
      weight: null,
      directed: !1
    }), pi = {
      // Implemented from the algorithm in the paper "On Variants of Shortest-Path Betweenness Centrality and their Generic Computation" by Ulrik Brandes
      betweennessCentrality: function(e) {
        for (var r = $f(e), a = r.directed, n = r.weight, i = n != null, s = this.cy(), o = this.nodes(), l = {}, u = {}, f = 0, h = {
          set: function(b, E) {
            u[b] = E, E > f && (f = E);
          },
          get: function(b) {
            return u[b];
          }
        }, c = 0; c < o.length; c++) {
          var v = o[c], d = v.id();
          a ? l[d] = v.outgoers().nodes() : l[d] = v.openNeighborhood().nodes(), h.set(d, 0);
        }
        for (var g = function(b) {
          for (var E = o[b].id(), M = [], O = {}, x = {}, I = {}, C = new Ra(function(Ee, ye) {
            return I[Ee] - I[ye];
          }), B = 0; B < o.length; B++) {
            var F = o[B].id();
            O[F] = [], x[F] = 0, I[F] = 1 / 0;
          }
          for (x[E] = 1, I[E] = 0, C.push(E); !C.empty(); ) {
            var R = C.pop();
            if (M.push(R), i)
              for (var X = 0; X < l[R].length; X++) {
                var z = l[R][X], re = s.getElementById(R), W = void 0;
                re.edgesTo(z).length > 0 ? W = re.edgesTo(z)[0] : W = z.edgesTo(re)[0];
                var Z = n(W);
                z = z.id(), I[z] > I[R] + Z && (I[z] = I[R] + Z, C.nodes.indexOf(z) < 0 ? C.push(z) : C.updateItem(z), x[z] = 0, O[z] = []), I[z] == I[R] + Z && (x[z] = x[z] + x[R], O[z].push(R));
              }
            else
              for (var ie = 0; ie < l[R].length; ie++) {
                var oe = l[R][ie].id();
                I[oe] == 1 / 0 && (C.push(oe), I[oe] = I[R] + 1), I[oe] == I[R] + 1 && (x[oe] = x[oe] + x[R], O[oe].push(R));
              }
          }
          for (var ge = {}, se = 0; se < o.length; se++)
            ge[o[se].id()] = 0;
          for (; M.length > 0; ) {
            for (var de = M.pop(), we = 0; we < O[de].length; we++) {
              var Te = O[de][we];
              ge[Te] = ge[Te] + x[Te] / x[de] * (1 + ge[de]);
            }
            de != o[b].id() && h.set(de, h.get(de) + ge[de]);
          }
        }, y = 0; y < o.length; y++)
          g(y);
        var p = {
          betweenness: function(b) {
            var E = s.collection(b).id();
            return h.get(E);
          },
          betweennessNormalized: function(b) {
            if (f == 0)
              return 0;
            var E = s.collection(b).id();
            return h.get(E) / f;
          }
        };
        return p.betweennessNormalised = p.betweennessNormalized, p;
      }
      // betweennessCentrality
    };
    pi.bc = pi.betweennessCentrality;
    var Vf = Lt({
      expandFactor: 2,
      // affects time of computation and cluster granularity to some extent: M * M
      inflateFactor: 2,
      // affects cluster granularity (the greater the value, the more clusters): M(i,j) / E(j)
      multFactor: 1,
      // optional self loops for each node. Use a neutral value to improve cluster computations.
      maxIterations: 20,
      // maximum number of iterations of the MCL algorithm in a single run
      attributes: [
        // attributes/features used to group nodes, ie. similarity values between nodes
        function(t) {
          return 1;
        }
      ]
    }), _f = function(e) {
      return Vf(e);
    }, Uf = function(e, r) {
      for (var a = 0, n = 0; n < r.length; n++)
        a += r[n](e);
      return a;
    }, Yf = function(e, r, a) {
      for (var n = 0; n < r; n++)
        e[n * r + n] = a;
    }, Ns = function(e, r) {
      for (var a, n = 0; n < r; n++) {
        a = 0;
        for (var i = 0; i < r; i++)
          a += e[i * r + n];
        for (var s = 0; s < r; s++)
          e[s * r + n] = e[s * r + n] / a;
      }
    }, Hf = function(e, r, a) {
      for (var n = new Array(a * a), i = 0; i < a; i++) {
        for (var s = 0; s < a; s++)
          n[i * a + s] = 0;
        for (var o = 0; o < a; o++)
          for (var l = 0; l < a; l++)
            n[i * a + l] += e[i * a + o] * r[o * a + l];
      }
      return n;
    }, Xf = function(e, r, a) {
      for (var n = e.slice(0), i = 1; i < a; i++)
        e = Hf(e, n, r);
      return e;
    }, qf = function(e, r, a) {
      for (var n = new Array(r * r), i = 0; i < r * r; i++)
        n[i] = Math.pow(e[i], a);
      return Ns(n, r), n;
    }, Wf = function(e, r, a, n) {
      for (var i = 0; i < a; i++) {
        var s = Math.round(e[i] * Math.pow(10, n)) / Math.pow(10, n), o = Math.round(r[i] * Math.pow(10, n)) / Math.pow(10, n);
        if (s !== o)
          return !1;
      }
      return !0;
    }, Kf = function(e, r, a, n) {
      for (var i = [], s = 0; s < r; s++) {
        for (var o = [], l = 0; l < r; l++)
          Math.round(e[s * r + l] * 1e3) / 1e3 > 0 && o.push(a[l]);
        o.length !== 0 && i.push(n.collection(o));
      }
      return i;
    }, Zf = function(e, r) {
      for (var a = 0; a < e.length; a++)
        if (!r[a] || e[a].id() !== r[a].id())
          return !1;
      return !0;
    }, Qf = function(e) {
      for (var r = 0; r < e.length; r++)
        for (var a = 0; a < e.length; a++)
          r != a && Zf(e[r], e[a]) && e.splice(a, 1);
      return e;
    }, Ms = function(e) {
      for (var r = this.nodes(), a = this.edges(), n = this.cy(), i = _f(e), s = {}, o = 0; o < r.length; o++)
        s[r[o].id()] = o;
      for (var l = r.length, u = l * l, f = new Array(u), h, c = 0; c < u; c++)
        f[c] = 0;
      for (var v = 0; v < a.length; v++) {
        var d = a[v], g = s[d.source().id()], y = s[d.target().id()], p = Uf(d, i.attributes);
        f[g * l + y] += p, f[y * l + g] += p;
      }
      Yf(f, l, i.multFactor), Ns(f, l);
      for (var m = !0, b = 0; m && b < i.maxIterations; )
        m = !1, h = Xf(f, l, i.expandFactor), f = qf(h, l, i.inflateFactor), Wf(f, h, u, 4) || (m = !0), b++;
      var E = Kf(f, l, r, n);
      return E = Qf(E), E;
    }, Jf = {
      markovClustering: Ms,
      mcl: Ms
    }, jf = function(e) {
      return e;
    }, Is = function(e, r) {
      return Math.abs(r - e);
    }, Rs = function(e, r, a) {
      return e + Is(r, a);
    }, ks = function(e, r, a) {
      return e + Math.pow(a - r, 2);
    }, eh = function(e) {
      return Math.sqrt(e);
    }, th = function(e, r, a) {
      return Math.max(e, Is(r, a));
    }, za = function(e, r, a, n, i) {
      for (var s = arguments.length > 5 && arguments[5] !== void 0 ? arguments[5] : jf, o = n, l, u, f = 0; f < e; f++)
        l = r(f), u = a(f), o = i(o, l, u);
      return s(o);
    }, na = {
      euclidean: function(e, r, a) {
        return e >= 2 ? za(e, r, a, 0, ks, eh) : za(e, r, a, 0, Rs);
      },
      squaredEuclidean: function(e, r, a) {
        return za(e, r, a, 0, ks);
      },
      manhattan: function(e, r, a) {
        return za(e, r, a, 0, Rs);
      },
      max: function(e, r, a) {
        return za(e, r, a, -1 / 0, th);
      }
    };
    na["squared-euclidean"] = na.squaredEuclidean, na.squaredeuclidean = na.squaredEuclidean;
    function bn(t, e, r, a, n, i) {
      var s;
      return H(t) ? s = t : s = na[t] || na.euclidean, e === 0 && H(t) ? s(n, i) : s(e, r, a, n, i);
    }
    var rh = Lt({
      k: 2,
      m: 2,
      sensitivityThreshold: 1e-4,
      distance: "euclidean",
      maxIterations: 10,
      attributes: [],
      testMode: !1,
      testCentroids: null
    }), yi = function(e) {
      return rh(e);
    }, En = function(e, r, a, n, i) {
      var s = i !== "kMedoids", o = s ? function(h) {
        return a[h];
      } : function(h) {
        return n[h](a);
      }, l = function(c) {
        return n[c](r);
      }, u = a, f = r;
      return bn(e, n.length, o, l, u, f);
    }, mi = function(e, r, a) {
      for (var n = a.length, i = new Array(n), s = new Array(n), o = new Array(r), l = null, u = 0; u < n; u++)
        i[u] = e.min(a[u]).value, s[u] = e.max(a[u]).value;
      for (var f = 0; f < r; f++) {
        l = [];
        for (var h = 0; h < n; h++)
          l[h] = Math.random() * (s[h] - i[h]) + i[h];
        o[f] = l;
      }
      return o;
    }, Ps = function(e, r, a, n, i) {
      for (var s = 1 / 0, o = 0, l = 0; l < r.length; l++) {
        var u = En(a, e, r[l], n, i);
        u < s && (s = u, o = l);
      }
      return o;
    }, Bs = function(e, r, a) {
      for (var n = [], i = null, s = 0; s < r.length; s++)
        i = r[s], a[i.id()] === e && n.push(i);
      return n;
    }, ah = function(e, r, a) {
      return Math.abs(r - e) <= a;
    }, nh = function(e, r, a) {
      for (var n = 0; n < e.length; n++)
        for (var i = 0; i < e[n].length; i++) {
          var s = Math.abs(e[n][i] - r[n][i]);
          if (s > a)
            return !1;
        }
      return !0;
    }, ih = function(e, r, a) {
      for (var n = 0; n < a; n++)
        if (e === r[n])
          return !0;
      return !1;
    }, Fs = function(e, r) {
      var a = new Array(r);
      if (e.length < 50)
        for (var n = 0; n < r; n++) {
          for (var i = e[Math.floor(Math.random() * e.length)]; ih(i, a, n); )
            i = e[Math.floor(Math.random() * e.length)];
          a[n] = i;
        }
      else
        for (var s = 0; s < r; s++)
          a[s] = e[Math.floor(Math.random() * e.length)];
      return a;
    }, zs = function(e, r, a) {
      for (var n = 0, i = 0; i < r.length; i++)
        n += En("manhattan", r[i], e, a, "kMedoids");
      return n;
    }, sh = function(e) {
      var r = this.cy(), a = this.nodes(), n = null, i = yi(e), s = new Array(i.k), o = {}, l;
      i.testMode ? typeof i.testCentroids == "number" ? (i.testCentroids, l = mi(a, i.k, i.attributes)) : Q(i.testCentroids) === "object" ? l = i.testCentroids : l = mi(a, i.k, i.attributes) : l = mi(a, i.k, i.attributes);
      for (var u = !0, f = 0; u && f < i.maxIterations; ) {
        for (var h = 0; h < a.length; h++)
          n = a[h], o[n.id()] = Ps(n, l, i.distance, i.attributes, "kMeans");
        u = !1;
        for (var c = 0; c < i.k; c++) {
          var v = Bs(c, a, o);
          if (v.length !== 0) {
            for (var d = i.attributes.length, g = l[c], y = new Array(d), p = new Array(d), m = 0; m < d; m++) {
              p[m] = 0;
              for (var b = 0; b < v.length; b++)
                n = v[b], p[m] += i.attributes[m](n);
              y[m] = p[m] / v.length, ah(y[m], g[m], i.sensitivityThreshold) || (u = !0);
            }
            l[c] = y, s[c] = r.collection(v);
          }
        }
        f++;
      }
      return s;
    }, oh = function(e) {
      var r = this.cy(), a = this.nodes(), n = null, i = yi(e), s = new Array(i.k), o, l = {}, u, f = new Array(i.k);
      i.testMode ? typeof i.testCentroids == "number" || (Q(i.testCentroids) === "object" ? o = i.testCentroids : o = Fs(a, i.k)) : o = Fs(a, i.k);
      for (var h = !0, c = 0; h && c < i.maxIterations; ) {
        for (var v = 0; v < a.length; v++)
          n = a[v], l[n.id()] = Ps(n, o, i.distance, i.attributes, "kMedoids");
        h = !1;
        for (var d = 0; d < o.length; d++) {
          var g = Bs(d, a, l);
          if (g.length !== 0) {
            f[d] = zs(o[d], g, i.attributes);
            for (var y = 0; y < g.length; y++)
              u = zs(g[y], g, i.attributes), u < f[d] && (f[d] = u, o[d] = g[y], h = !0);
            s[d] = r.collection(g);
          }
        }
        c++;
      }
      return s;
    }, uh = function(e, r, a, n, i) {
      for (var s, o, l = 0; l < r.length; l++)
        for (var u = 0; u < e.length; u++)
          n[l][u] = Math.pow(a[l][u], i.m);
      for (var f = 0; f < e.length; f++)
        for (var h = 0; h < i.attributes.length; h++) {
          s = 0, o = 0;
          for (var c = 0; c < r.length; c++)
            s += n[c][f] * i.attributes[h](r[c]), o += n[c][f];
          e[f][h] = s / o;
        }
    }, lh = function(e, r, a, n, i) {
      for (var s = 0; s < e.length; s++)
        r[s] = e[s].slice();
      for (var o, l, u, f = 2 / (i.m - 1), h = 0; h < a.length; h++)
        for (var c = 0; c < n.length; c++) {
          o = 0;
          for (var v = 0; v < a.length; v++)
            l = En(i.distance, n[c], a[h], i.attributes, "cmeans"), u = En(i.distance, n[c], a[v], i.attributes, "cmeans"), o += Math.pow(l / u, f);
          e[c][h] = 1 / o;
        }
    }, fh = function(e, r, a, n) {
      for (var i = new Array(a.k), s = 0; s < i.length; s++)
        i[s] = [];
      for (var o, l, u = 0; u < r.length; u++) {
        o = -1 / 0, l = -1;
        for (var f = 0; f < r[0].length; f++)
          r[u][f] > o && (o = r[u][f], l = f);
        i[l].push(e[u]);
      }
      for (var h = 0; h < i.length; h++)
        i[h] = n.collection(i[h]);
      return i;
    }, Gs = function(e) {
      var r = this.cy(), a = this.nodes(), n = yi(e), i, s, o, l, u;
      l = new Array(a.length);
      for (var f = 0; f < a.length; f++)
        l[f] = new Array(n.k);
      o = new Array(a.length);
      for (var h = 0; h < a.length; h++)
        o[h] = new Array(n.k);
      for (var c = 0; c < a.length; c++) {
        for (var v = 0, d = 0; d < n.k; d++)
          o[c][d] = Math.random(), v += o[c][d];
        for (var g = 0; g < n.k; g++)
          o[c][g] = o[c][g] / v;
      }
      s = new Array(n.k);
      for (var y = 0; y < n.k; y++)
        s[y] = new Array(n.attributes.length);
      u = new Array(a.length);
      for (var p = 0; p < a.length; p++)
        u[p] = new Array(n.k);
      for (var m = !0, b = 0; m && b < n.maxIterations; )
        m = !1, uh(s, a, o, u, n), lh(o, l, s, a, n), nh(o, l, n.sensitivityThreshold) || (m = !0), b++;
      return i = fh(a, o, n, r), {
        clusters: i,
        degreeOfMembership: o
      };
    }, hh = {
      kMeans: sh,
      kMedoids: oh,
      fuzzyCMeans: Gs,
      fcm: Gs
    }, ch = Lt({
      distance: "euclidean",
      // distance metric to compare nodes
      linkage: "min",
      // linkage criterion : how to determine the distance between clusters of nodes
      mode: "threshold",
      // mode:'threshold' => clusters must be threshold distance apart
      threshold: 1 / 0,
      // the distance threshold
      // mode:'dendrogram' => the nodes are organised as leaves in a tree (siblings are close), merging makes clusters
      addDendrogram: !1,
      // whether to add the dendrogram to the graph for viz
      dendrogramDepth: 0,
      // depth at which dendrogram branches are merged into the returned clusters
      attributes: []
      // array of attr functions
    }), vh = {
      single: "min",
      complete: "max"
    }, dh = function(e) {
      var r = ch(e), a = vh[r.linkage];
      return a != null && (r.linkage = a), r;
    }, $s = function(e, r, a, n, i) {
      for (var s = 0, o = 1 / 0, l, u = i.attributes, f = function(C, B) {
        return bn(i.distance, u.length, function(F) {
          return u[F](C);
        }, function(F) {
          return u[F](B);
        }, C, B);
      }, h = 0; h < e.length; h++) {
        var c = e[h].key, v = a[c][n[c]];
        v < o && (s = c, o = v);
      }
      if (i.mode === "threshold" && o >= i.threshold || i.mode === "dendrogram" && e.length === 1)
        return !1;
      var d = r[s], g = r[n[s]], y;
      i.mode === "dendrogram" ? y = {
        left: d,
        right: g,
        key: d.key
      } : y = {
        value: d.value.concat(g.value),
        key: d.key
      }, e[d.index] = y, e.splice(g.index, 1), r[d.key] = y;
      for (var p = 0; p < e.length; p++) {
        var m = e[p];
        d.key === m.key ? l = 1 / 0 : i.linkage === "min" ? (l = a[d.key][m.key], a[d.key][m.key] > a[g.key][m.key] && (l = a[g.key][m.key])) : i.linkage === "max" ? (l = a[d.key][m.key], a[d.key][m.key] < a[g.key][m.key] && (l = a[g.key][m.key])) : i.linkage === "mean" ? l = (a[d.key][m.key] * d.size + a[g.key][m.key] * g.size) / (d.size + g.size) : i.mode === "dendrogram" ? l = f(m.value, d.value) : l = f(m.value[0], d.value[0]), a[d.key][m.key] = a[m.key][d.key] = l;
      }
      for (var b = 0; b < e.length; b++) {
        var E = e[b].key;
        if (n[E] === d.key || n[E] === g.key) {
          for (var M = E, O = 0; O < e.length; O++) {
            var x = e[O].key;
            a[E][x] < a[E][M] && (M = x);
          }
          n[E] = M;
        }
        e[b].index = b;
      }
      return d.key = g.key = d.index = g.index = null, !0;
    }, wn = function t(e, r, a) {
      e && (e.value ? r.push(e.value) : (e.left && t(e.left, r), e.right && t(e.right, r)));
    }, gh = function t(e, r) {
      if (!e)
        return "";
      if (e.left && e.right) {
        var a = t(e.left, r), n = t(e.right, r), i = r.add({
          group: "nodes",
          data: {
            id: a + "," + n
          }
        });
        return r.add({
          group: "edges",
          data: {
            source: a,
            target: i.id()
          }
        }), r.add({
          group: "edges",
          data: {
            source: n,
            target: i.id()
          }
        }), i.id();
      } else if (e.value)
        return e.value.id();
    }, ph = function t(e, r, a) {
      if (!e)
        return [];
      var n = [], i = [], s = [];
      return r === 0 ? (e.left && wn(e.left, n), e.right && wn(e.right, i), s = n.concat(i), [a.collection(s)]) : r === 1 ? e.value ? [a.collection(e.value)] : (e.left && wn(e.left, n), e.right && wn(e.right, i), [a.collection(n), a.collection(i)]) : e.value ? [a.collection(e.value)] : (e.left && (n = t(e.left, r - 1, a)), e.right && (i = t(e.right, r - 1, a)), n.concat(i));
    }, Vs = function(e) {
      for (var r = this.cy(), a = this.nodes(), n = dh(e), i = n.attributes, s = function(b, E) {
        return bn(n.distance, i.length, function(M) {
          return i[M](b);
        }, function(M) {
          return i[M](E);
        }, b, E);
      }, o = [], l = [], u = [], f = [], h = 0; h < a.length; h++) {
        var c = {
          value: n.mode === "dendrogram" ? a[h] : [a[h]],
          key: h,
          index: h
        };
        o[h] = c, f[h] = c, l[h] = [], u[h] = 0;
      }
      for (var v = 0; v < o.length; v++)
        for (var d = 0; d <= v; d++) {
          var g = void 0;
          n.mode === "dendrogram" ? g = v === d ? 1 / 0 : s(o[v].value, o[d].value) : g = v === d ? 1 / 0 : s(o[v].value[0], o[d].value[0]), l[v][d] = g, l[d][v] = g, g < l[v][u[v]] && (u[v] = d);
        }
      for (var y = $s(o, f, l, u, n); y; )
        y = $s(o, f, l, u, n);
      var p;
      return n.mode === "dendrogram" ? (p = ph(o[0], n.dendrogramDepth, r), n.addDendrogram && gh(o[0], r)) : (p = new Array(o.length), o.forEach(function(m, b) {
        m.key = m.index = null, p[b] = r.collection(m.value);
      })), p;
    }, yh = {
      hierarchicalClustering: Vs,
      hca: Vs
    }, mh = Lt({
      distance: "euclidean",
      // distance metric to compare attributes between two nodes
      preference: "median",
      // suitability of a data point to serve as an exemplar
      damping: 0.8,
      // damping factor between [0.5, 1)
      maxIterations: 1e3,
      // max number of iterations to run
      minIterations: 100,
      // min number of iterations to run in order for clustering to stop
      attributes: [
        // functions to quantify the similarity between any two points
        // e.g. node => node.data('weight')
      ]
    }), bh = function(e) {
      var r = e.damping, a = e.preference;
      0.5 <= r && r < 1 || xt("Damping must range on [0.5, 1).  Got: ".concat(r));
      var n = ["median", "mean", "min", "max"];
      return n.some(function(i) {
        return i === a;
      }) || k(a) || xt("Preference must be one of [".concat(n.map(function(i) {
        return "'".concat(i, "'");
      }).join(", "), "] or a number.  Got: ").concat(a)), mh(e);
    }, Eh = function(e, r, a, n) {
      var i = function(o, l) {
        return n[l](o);
      };
      return -bn(e, n.length, function(s) {
        return i(r, s);
      }, function(s) {
        return i(a, s);
      }, r, a);
    }, wh = function(e, r) {
      var a = null;
      return r === "median" ? a = bf(e) : r === "mean" ? a = mf(e) : r === "min" ? a = pf(e) : r === "max" ? a = yf(e) : a = r, a;
    }, xh = function(e, r, a) {
      for (var n = [], i = 0; i < e; i++)
        r[i * e + i] + a[i * e + i] > 0 && n.push(i);
      return n;
    }, _s = function(e, r, a) {
      for (var n = [], i = 0; i < e; i++) {
        for (var s = -1, o = -1 / 0, l = 0; l < a.length; l++) {
          var u = a[l];
          r[i * e + u] > o && (s = u, o = r[i * e + u]);
        }
        s > 0 && n.push(s);
      }
      for (var f = 0; f < a.length; f++)
        n[a[f]] = a[f];
      return n;
    }, Th = function(e, r, a) {
      for (var n = _s(e, r, a), i = 0; i < a.length; i++) {
        for (var s = [], o = 0; o < n.length; o++)
          n[o] === a[i] && s.push(o);
        for (var l = -1, u = -1 / 0, f = 0; f < s.length; f++) {
          for (var h = 0, c = 0; c < s.length; c++)
            h += r[s[c] * e + s[f]];
          h > u && (l = f, u = h);
        }
        a[i] = s[l];
      }
      return n = _s(e, r, a), n;
    }, Us = function(e) {
      for (var r = this.cy(), a = this.nodes(), n = bh(e), i = {}, s = 0; s < a.length; s++)
        i[a[s].id()] = s;
      var o, l, u, f, h, c;
      o = a.length, l = o * o, u = new Array(l);
      for (var v = 0; v < l; v++)
        u[v] = -1 / 0;
      for (var d = 0; d < o; d++)
        for (var g = 0; g < o; g++)
          d !== g && (u[d * o + g] = Eh(n.distance, a[d], a[g], n.attributes));
      f = wh(u, n.preference);
      for (var y = 0; y < o; y++)
        u[y * o + y] = f;
      h = new Array(l);
      for (var p = 0; p < l; p++)
        h[p] = 0;
      c = new Array(l);
      for (var m = 0; m < l; m++)
        c[m] = 0;
      for (var b = new Array(o), E = new Array(o), M = new Array(o), O = 0; O < o; O++)
        b[O] = 0, E[O] = 0, M[O] = 0;
      for (var x = new Array(o * n.minIterations), I = 0; I < x.length; I++)
        x[I] = 0;
      var C;
      for (C = 0; C < n.maxIterations; C++) {
        for (var B = 0; B < o; B++) {
          for (var F = -1 / 0, R = -1 / 0, X = -1, z = 0, re = 0; re < o; re++)
            b[re] = h[B * o + re], z = c[B * o + re] + u[B * o + re], z >= F ? (R = F, F = z, X = re) : z > R && (R = z);
          for (var W = 0; W < o; W++)
            h[B * o + W] = (1 - n.damping) * (u[B * o + W] - F) + n.damping * b[W];
          h[B * o + X] = (1 - n.damping) * (u[B * o + X] - R) + n.damping * b[X];
        }
        for (var Z = 0; Z < o; Z++) {
          for (var ie = 0, oe = 0; oe < o; oe++)
            b[oe] = c[oe * o + Z], E[oe] = Math.max(0, h[oe * o + Z]), ie += E[oe];
          ie -= E[Z], E[Z] = h[Z * o + Z], ie += E[Z];
          for (var ge = 0; ge < o; ge++)
            c[ge * o + Z] = (1 - n.damping) * Math.min(0, ie - E[ge]) + n.damping * b[ge];
          c[Z * o + Z] = (1 - n.damping) * (ie - E[Z]) + n.damping * b[Z];
        }
        for (var se = 0, de = 0; de < o; de++) {
          var we = c[de * o + de] + h[de * o + de] > 0 ? 1 : 0;
          x[C % n.minIterations * o + de] = we, se += we;
        }
        if (se > 0 && (C >= n.minIterations - 1 || C == n.maxIterations - 1)) {
          for (var Te = 0, Ee = 0; Ee < o; Ee++) {
            M[Ee] = 0;
            for (var ye = 0; ye < n.minIterations; ye++)
              M[Ee] += x[ye * o + Ee];
            (M[Ee] === 0 || M[Ee] === n.minIterations) && Te++;
          }
          if (Te === o)
            break;
        }
      }
      for (var ae = xh(o, h, c), xe = Th(o, u, ae), Ce = {}, Oe = 0; Oe < ae.length; Oe++)
        Ce[ae[Oe]] = [];
      for (var Ie = 0; Ie < a.length; Ie++) {
        var He = i[a[Ie].id()], qe = xe[He];
        qe != null && Ce[qe].push(a[Ie]);
      }
      for (var Re = new Array(ae.length), Me = 0; Me < ae.length; Me++)
        Re[Me] = r.collection(Ce[ae[Me]]);
      return Re;
    }, Ch = {
      affinityPropagation: Us,
      ap: Us
    }, Dh = Lt({
      root: void 0,
      directed: !1
    }), Sh = {
      hierholzer: function(e) {
        if (!S(e)) {
          var r = arguments;
          e = {
            root: r[0],
            directed: r[1]
          };
        }
        var a = Dh(e), n = a.root, i = a.directed, s = this, o = !1, l, u, f;
        n && (f = ee(n) ? this.filter(n)[0].id() : n[0].id());
        var h = {}, c = {};
        i ? s.forEach(function(m) {
          var b = m.id();
          if (m.isNode()) {
            var E = m.indegree(!0), M = m.outdegree(!0), O = E - M, x = M - E;
            O == 1 ? l ? o = !0 : l = b : x == 1 ? u ? o = !0 : u = b : (x > 1 || O > 1) && (o = !0), h[b] = [], m.outgoers().forEach(function(I) {
              I.isEdge() && h[b].push(I.id());
            });
          } else
            c[b] = [void 0, m.target().id()];
        }) : s.forEach(function(m) {
          var b = m.id();
          if (m.isNode()) {
            var E = m.degree(!0);
            E % 2 && (l ? u ? o = !0 : u = b : l = b), h[b] = [], m.connectedEdges().forEach(function(M) {
              return h[b].push(M.id());
            });
          } else
            c[b] = [m.source().id(), m.target().id()];
        });
        var v = {
          found: !1,
          trail: void 0
        };
        if (o)
          return v;
        if (u && l)
          if (i) {
            if (f && u != f)
              return v;
            f = u;
          } else {
            if (f && u != f && l != f)
              return v;
            f || (f = u);
          }
        else
          f || (f = s[0].id());
        var d = function(b) {
          for (var E = b, M = [b], O, x, I; h[E].length; )
            O = h[E].shift(), x = c[O][0], I = c[O][1], E != I ? (h[I] = h[I].filter(function(C) {
              return C != O;
            }), E = I) : !i && E != x && (h[x] = h[x].filter(function(C) {
              return C != O;
            }), E = x), M.unshift(O), M.unshift(E);
          return M;
        }, g = [], y = [];
        for (y = d(f); y.length != 1; )
          h[y[0]].length == 0 ? (g.unshift(s.getElementById(y.shift())), g.unshift(s.getElementById(y.shift()))) : y = d(y.shift()).concat(y);
        g.unshift(s.getElementById(y.shift()));
        for (var p in h)
          if (h[p].length)
            return v;
        return v.found = !0, v.trail = this.spawn(g, !0), v;
      }
    }, xn = function() {
      var e = this, r = {}, a = 0, n = 0, i = [], s = [], o = {}, l = function(c, v) {
        for (var d = s.length - 1, g = [], y = e.spawn(); s[d].x != c || s[d].y != v; )
          g.push(s.pop().edge), d--;
        g.push(s.pop().edge), g.forEach(function(p) {
          var m = p.connectedNodes().intersection(e);
          y.merge(p), m.forEach(function(b) {
            var E = b.id(), M = b.connectedEdges().intersection(e);
            y.merge(b), r[E].cutVertex ? y.merge(M.filter(function(O) {
              return O.isLoop();
            })) : y.merge(M);
          });
        }), i.push(y);
      }, u = function h(c, v, d) {
        c === d && (n += 1), r[v] = {
          id: a,
          low: a++,
          cutVertex: !1
        };
        var g = e.getElementById(v).connectedEdges().intersection(e);
        if (g.size() === 0)
          i.push(e.spawn(e.getElementById(v)));
        else {
          var y, p, m, b;
          g.forEach(function(E) {
            y = E.source().id(), p = E.target().id(), m = y === v ? p : y, m !== d && (b = E.id(), o[b] || (o[b] = !0, s.push({
              x: v,
              y: m,
              edge: E
            })), m in r ? r[v].low = Math.min(r[v].low, r[m].id) : (h(c, m, v), r[v].low = Math.min(r[v].low, r[m].low), r[v].id <= r[m].low && (r[v].cutVertex = !0, l(v, m))));
          });
        }
      };
      e.forEach(function(h) {
        if (h.isNode()) {
          var c = h.id();
          c in r || (n = 0, u(c, c), r[c].cutVertex = n > 1);
        }
      });
      var f = Object.keys(r).filter(function(h) {
        return r[h].cutVertex;
      }).map(function(h) {
        return e.getElementById(h);
      });
      return {
        cut: e.spawn(f),
        components: i
      };
    }, Lh = {
      hopcroftTarjanBiconnected: xn,
      htbc: xn,
      htb: xn,
      hopcroftTarjanBiconnectedComponents: xn
    }, Tn = function() {
      var e = this, r = {}, a = 0, n = [], i = [], s = e.spawn(e), o = function l(u) {
        i.push(u), r[u] = {
          index: a,
          low: a++,
          explored: !1
        };
        var f = e.getElementById(u).connectedEdges().intersection(e);
        if (f.forEach(function(g) {
          var y = g.target().id();
          y !== u && (y in r || l(y), r[y].explored || (r[u].low = Math.min(r[u].low, r[y].low)));
        }), r[u].index === r[u].low) {
          for (var h = e.spawn(); ; ) {
            var c = i.pop();
            if (h.merge(e.getElementById(c)), r[c].low = r[u].index, r[c].explored = !0, c === u)
              break;
          }
          var v = h.edgesWith(h), d = h.merge(v);
          n.push(d), s = s.difference(d);
        }
      };
      return e.forEach(function(l) {
        if (l.isNode()) {
          var u = l.id();
          u in r || o(u);
        }
      }), {
        cut: s,
        components: n
      };
    }, Ah = {
      tarjanStronglyConnected: Tn,
      tsc: Tn,
      tscc: Tn,
      tarjanStronglyConnectedComponents: Tn
    }, Ys = {};
    [Ia, af, nf, of, lf, hf, df, Gf, ra, aa, pi, Jf, hh, yh, Ch, Sh, Lh, Ah].forEach(function(t) {
      Ue(Ys, t);
    });
    /*!
    Embeddable Minimum Strictly-Compliant Promises/A+ 1.1.1 Thenable
    Copyright (c) 2013-2014 Ralf S. Engelschall (http://engelschall.com)
    Licensed under The MIT License (http://opensource.org/licenses/MIT)
    */
    var Hs = 0, Xs = 1, qs = 2, pr = function t(e) {
      if (!(this instanceof t))
        return new t(e);
      this.id = "Thenable/1.0.7", this.state = Hs, this.fulfillValue = void 0, this.rejectReason = void 0, this.onFulfilled = [], this.onRejected = [], this.proxy = {
        then: this.then.bind(this)
      }, typeof e == "function" && e.call(this, this.fulfill.bind(this), this.reject.bind(this));
    };
    pr.prototype = {
      /*  promise resolving methods  */
      fulfill: function(e) {
        return Ws(this, Xs, "fulfillValue", e);
      },
      reject: function(e) {
        return Ws(this, qs, "rejectReason", e);
      },
      /*  "The then Method" [Promises/A+ 1.1, 1.2, 2.2]  */
      then: function(e, r) {
        var a = this, n = new pr();
        return a.onFulfilled.push(Qs(e, n, "fulfill")), a.onRejected.push(Qs(r, n, "reject")), Ks(a), n.proxy;
      }
    };
    var Ws = function(e, r, a, n) {
      return e.state === Hs && (e.state = r, e[a] = n, Ks(e)), e;
    }, Ks = function(e) {
      e.state === Xs ? Zs(e, "onFulfilled", e.fulfillValue) : e.state === qs && Zs(e, "onRejected", e.rejectReason);
    }, Zs = function(e, r, a) {
      if (e[r].length !== 0) {
        var n = e[r];
        e[r] = [];
        var i = function() {
          for (var o = 0; o < n.length; o++)
            n[o](a);
        };
        typeof setImmediate == "function" ? setImmediate(i) : setTimeout(i, 0);
      }
    }, Qs = function(e, r, a) {
      return function(n) {
        if (typeof e != "function")
          r[a].call(r, n);
        else {
          var i;
          try {
            i = e(n);
          } catch (s) {
            r.reject(s);
            return;
          }
          Oh(r, i);
        }
      };
    }, Oh = function t(e, r) {
      if (e === r || e.proxy === r) {
        e.reject(new TypeError("cannot resolve promise with itself"));
        return;
      }
      var a;
      if (Q(r) === "object" && r !== null || typeof r == "function")
        try {
          a = r.then;
        } catch (i) {
          e.reject(i);
          return;
        }
      if (typeof a == "function") {
        var n = !1;
        try {
          a.call(
            r,
            /*  resolvePromise  */
            /*  [Promises/A+ 2.3.3.3.1]  */
            function(i) {
              n || (n = !0, i === r ? e.reject(new TypeError("circular thenable chain")) : t(e, i));
            },
            /*  rejectPromise  */
            /*  [Promises/A+ 2.3.3.3.2]  */
            function(i) {
              n || (n = !0, e.reject(i));
            }
          );
        } catch (i) {
          n || e.reject(i);
        }
        return;
      }
      e.fulfill(r);
    };
    pr.all = function(t) {
      return new pr(function(e, r) {
        for (var a = new Array(t.length), n = 0, i = function(l, u) {
          a[l] = u, n++, n === t.length && e(a);
        }, s = 0; s < t.length; s++)
          (function(o) {
            var l = t[o], u = l != null && l.then != null;
            if (u)
              l.then(function(h) {
                i(o, h);
              }, function(h) {
                r(h);
              });
            else {
              var f = l;
              i(o, f);
            }
          })(s);
      });
    }, pr.resolve = function(t) {
      return new pr(function(e, r) {
        e(t);
      });
    }, pr.reject = function(t) {
      return new pr(function(e, r) {
        r(t);
      });
    };
    var ia = typeof Promise < "u" ? Promise : pr, bi = function(e, r, a) {
      var n = _e(e), i = !n, s = this._private = Ue({
        duration: 1e3
      }, r, a);
      if (s.target = e, s.style = s.style || s.css, s.started = !1, s.playing = !1, s.hooked = !1, s.applying = !1, s.progress = 0, s.completes = [], s.frames = [], s.complete && H(s.complete) && s.completes.push(s.complete), i) {
        var o = e.position();
        s.startPosition = s.startPosition || {
          x: o.x,
          y: o.y
        }, s.startStyle = s.startStyle || e.cy().style().getAnimationStartStyle(e, s.style);
      }
      if (n) {
        var l = e.pan();
        s.startPan = {
          x: l.x,
          y: l.y
        }, s.startZoom = e.zoom();
      }
      this.length = 1, this[0] = this;
    }, zr = bi.prototype;
    Ue(zr, {
      instanceString: function() {
        return "animation";
      },
      hook: function() {
        var e = this._private;
        if (!e.hooked) {
          var r, a = e.target._private.animation;
          e.queue ? r = a.queue : r = a.current, r.push(this), pe(e.target) && e.target.cy().addToAnimationPool(e.target), e.hooked = !0;
        }
        return this;
      },
      play: function() {
        var e = this._private;
        return e.progress === 1 && (e.progress = 0), e.playing = !0, e.started = !1, e.stopped = !1, this.hook(), this;
      },
      playing: function() {
        return this._private.playing;
      },
      apply: function() {
        var e = this._private;
        return e.applying = !0, e.started = !1, e.stopped = !1, this.hook(), this;
      },
      applying: function() {
        return this._private.applying;
      },
      pause: function() {
        var e = this._private;
        return e.playing = !1, e.started = !1, this;
      },
      stop: function() {
        var e = this._private;
        return e.playing = !1, e.started = !1, e.stopped = !0, this;
      },
      rewind: function() {
        return this.progress(0);
      },
      fastforward: function() {
        return this.progress(1);
      },
      time: function(e) {
        var r = this._private;
        return e === void 0 ? r.progress * r.duration : this.progress(e / r.duration);
      },
      progress: function(e) {
        var r = this._private, a = r.playing;
        return e === void 0 ? r.progress : (a && this.pause(), r.progress = e, r.started = !1, a && this.play(), this);
      },
      completed: function() {
        return this._private.progress === 1;
      },
      reverse: function() {
        var e = this._private, r = e.playing;
        r && this.pause(), e.progress = 1 - e.progress, e.started = !1;
        var a = function(u, f) {
          var h = e[u];
          h != null && (e[u] = e[f], e[f] = h);
        };
        if (a("zoom", "startZoom"), a("pan", "startPan"), a("position", "startPosition"), e.style)
          for (var n = 0; n < e.style.length; n++) {
            var i = e.style[n], s = i.name, o = e.startStyle[s];
            e.startStyle[s] = i, e.style[n] = o;
          }
        return r && this.play(), this;
      },
      promise: function(e) {
        var r = this._private, a;
        switch (e) {
          case "frame":
            a = r.frames;
            break;
          default:
          case "complete":
          case "completed":
            a = r.completes;
        }
        return new ia(function(n, i) {
          a.push(function() {
            n();
          });
        });
      }
    }), zr.complete = zr.completed, zr.run = zr.play, zr.running = zr.playing;
    var Nh = {
      animated: function() {
        return function() {
          var r = this, a = r.length !== void 0, n = a ? r : [r], i = this._private.cy || this;
          if (!i.styleEnabled())
            return !1;
          var s = n[0];
          if (s)
            return s._private.animation.current.length > 0;
        };
      },
      // animated
      clearQueue: function() {
        return function() {
          var r = this, a = r.length !== void 0, n = a ? r : [r], i = this._private.cy || this;
          if (!i.styleEnabled())
            return this;
          for (var s = 0; s < n.length; s++) {
            var o = n[s];
            o._private.animation.queue = [];
          }
          return this;
        };
      },
      // clearQueue
      delay: function() {
        return function(r, a) {
          var n = this._private.cy || this;
          return n.styleEnabled() ? this.animate({
            delay: r,
            duration: r,
            complete: a
          }) : this;
        };
      },
      // delay
      delayAnimation: function() {
        return function(r, a) {
          var n = this._private.cy || this;
          return n.styleEnabled() ? this.animation({
            delay: r,
            duration: r,
            complete: a
          }) : this;
        };
      },
      // delay
      animation: function() {
        return function(r, a) {
          var n = this, i = n.length !== void 0, s = i ? n : [n], o = this._private.cy || this, l = !i, u = !l;
          if (!o.styleEnabled())
            return this;
          var f = o.style();
          r = Ue({}, r, a);
          var h = Object.keys(r).length === 0;
          if (h)
            return new bi(s[0], r);
          switch (r.duration === void 0 && (r.duration = 400), r.duration) {
            case "slow":
              r.duration = 600;
              break;
            case "fast":
              r.duration = 200;
              break;
          }
          if (u && (r.style = f.getPropsList(r.style || r.css), r.css = void 0), u && r.renderedPosition != null) {
            var c = r.renderedPosition, v = o.pan(), d = o.zoom();
            r.position = bs(c, d, v);
          }
          if (l && r.panBy != null) {
            var g = r.panBy, y = o.pan();
            r.pan = {
              x: y.x + g.x,
              y: y.y + g.y
            };
          }
          var p = r.center || r.centre;
          if (l && p != null) {
            var m = o.getCenterPan(p.eles, r.zoom);
            m != null && (r.pan = m);
          }
          if (l && r.fit != null) {
            var b = r.fit, E = o.getFitViewport(b.eles || b.boundingBox, b.padding);
            E != null && (r.pan = E.pan, r.zoom = E.zoom);
          }
          if (l && S(r.zoom)) {
            var M = o.getZoomedViewport(r.zoom);
            M != null ? (M.zoomed && (r.zoom = M.zoom), M.panned && (r.pan = M.pan)) : r.zoom = null;
          }
          return new bi(s[0], r);
        };
      },
      // animate
      animate: function() {
        return function(r, a) {
          var n = this, i = n.length !== void 0, s = i ? n : [n], o = this._private.cy || this;
          if (!o.styleEnabled())
            return this;
          a && (r = Ue({}, r, a));
          for (var l = 0; l < s.length; l++) {
            var u = s[l], f = u.animated() && (r.queue === void 0 || r.queue), h = u.animation(r, f ? {
              queue: !0
            } : void 0);
            h.play();
          }
          return this;
        };
      },
      // animate
      stop: function() {
        return function(r, a) {
          var n = this, i = n.length !== void 0, s = i ? n : [n], o = this._private.cy || this;
          if (!o.styleEnabled())
            return this;
          for (var l = 0; l < s.length; l++) {
            for (var u = s[l], f = u._private, h = f.animation.current, c = 0; c < h.length; c++) {
              var v = h[c], d = v._private;
              a && (d.duration = 0);
            }
            r && (f.animation.queue = []), a || (f.animation.current = []);
          }
          return o.notify("draw"), this;
        };
      }
      // stop
    }, Mh = Array.isArray, Cn = Mh, Ih = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/, Rh = /^\w*$/;
    function kh(t, e) {
      if (Cn(t))
        return !1;
      var r = typeof t;
      return r == "number" || r == "symbol" || r == "boolean" || t == null || Aa(t) ? !0 : Rh.test(t) || !Ih.test(t) || e != null && t in Object(e);
    }
    var Ph = kh, Bh = "[object AsyncFunction]", Fh = "[object Function]", zh = "[object GeneratorFunction]", Gh = "[object Proxy]";
    function $h(t) {
      if (!Rr(t))
        return !1;
      var e = is(t);
      return e == Fh || e == zh || e == Bh || e == Gh;
    }
    var Vh = $h, _h = ln["__core-js_shared__"], Ei = _h, Js = function() {
      var t = /[^.]+$/.exec(Ei && Ei.keys && Ei.keys.IE_PROTO || "");
      return t ? "Symbol(src)_1." + t : "";
    }();
    function Uh(t) {
      return !!Js && Js in t;
    }
    var Yh = Uh, Hh = Function.prototype, Xh = Hh.toString;
    function qh(t) {
      if (t != null) {
        try {
          return Xh.call(t);
        } catch {
        }
        try {
          return t + "";
        } catch {
        }
      }
      return "";
    }
    var Wh = qh, Kh = /[\\^$.*+?()[\]{}|]/g, Zh = /^\[object .+?Constructor\]$/, Qh = Function.prototype, Jh = Object.prototype, jh = Qh.toString, ec = Jh.hasOwnProperty, tc = RegExp(
      "^" + jh.call(ec).replace(Kh, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$"
    );
    function rc(t) {
      if (!Rr(t) || Yh(t))
        return !1;
      var e = Vh(t) ? tc : Zh;
      return e.test(Wh(t));
    }
    var ac = rc;
    function nc(t, e) {
      return t == null ? void 0 : t[e];
    }
    var ic = nc;
    function sc(t, e) {
      var r = ic(t, e);
      return ac(r) ? r : void 0;
    }
    var wi = sc, oc = wi(Object, "create"), Ga = oc;
    function uc() {
      this.__data__ = Ga ? Ga(null) : {}, this.size = 0;
    }
    var lc = uc;
    function fc(t) {
      var e = this.has(t) && delete this.__data__[t];
      return this.size -= e ? 1 : 0, e;
    }
    var hc = fc, cc = "__lodash_hash_undefined__", vc = Object.prototype, dc = vc.hasOwnProperty;
    function gc(t) {
      var e = this.__data__;
      if (Ga) {
        var r = e[t];
        return r === cc ? void 0 : r;
      }
      return dc.call(e, t) ? e[t] : void 0;
    }
    var pc = gc, yc = Object.prototype, mc = yc.hasOwnProperty;
    function bc(t) {
      var e = this.__data__;
      return Ga ? e[t] !== void 0 : mc.call(e, t);
    }
    var Ec = bc, wc = "__lodash_hash_undefined__";
    function xc(t, e) {
      var r = this.__data__;
      return this.size += this.has(t) ? 0 : 1, r[t] = Ga && e === void 0 ? wc : e, this;
    }
    var Tc = xc;
    function sa(t) {
      var e = -1, r = t == null ? 0 : t.length;
      for (this.clear(); ++e < r; ) {
        var a = t[e];
        this.set(a[0], a[1]);
      }
    }
    sa.prototype.clear = lc, sa.prototype.delete = hc, sa.prototype.get = pc, sa.prototype.has = Ec, sa.prototype.set = Tc;
    var js = sa;
    function Cc() {
      this.__data__ = [], this.size = 0;
    }
    var Dc = Cc;
    function Sc(t, e) {
      return t === e || t !== t && e !== e;
    }
    var eo = Sc;
    function Lc(t, e) {
      for (var r = t.length; r--; )
        if (eo(t[r][0], e))
          return r;
      return -1;
    }
    var Dn = Lc, Ac = Array.prototype, Oc = Ac.splice;
    function Nc(t) {
      var e = this.__data__, r = Dn(e, t);
      if (r < 0)
        return !1;
      var a = e.length - 1;
      return r == a ? e.pop() : Oc.call(e, r, 1), --this.size, !0;
    }
    var Mc = Nc;
    function Ic(t) {
      var e = this.__data__, r = Dn(e, t);
      return r < 0 ? void 0 : e[r][1];
    }
    var Rc = Ic;
    function kc(t) {
      return Dn(this.__data__, t) > -1;
    }
    var Pc = kc;
    function Bc(t, e) {
      var r = this.__data__, a = Dn(r, t);
      return a < 0 ? (++this.size, r.push([t, e])) : r[a][1] = e, this;
    }
    var Fc = Bc;
    function oa(t) {
      var e = -1, r = t == null ? 0 : t.length;
      for (this.clear(); ++e < r; ) {
        var a = t[e];
        this.set(a[0], a[1]);
      }
    }
    oa.prototype.clear = Dc, oa.prototype.delete = Mc, oa.prototype.get = Rc, oa.prototype.has = Pc, oa.prototype.set = Fc;
    var zc = oa, Gc = wi(ln, "Map"), $c = Gc;
    function Vc() {
      this.size = 0, this.__data__ = {
        hash: new js(),
        map: new ($c || zc)(),
        string: new js()
      };
    }
    var _c = Vc;
    function Uc(t) {
      var e = typeof t;
      return e == "string" || e == "number" || e == "symbol" || e == "boolean" ? t !== "__proto__" : t === null;
    }
    var Yc = Uc;
    function Hc(t, e) {
      var r = t.__data__;
      return Yc(e) ? r[typeof e == "string" ? "string" : "hash"] : r.map;
    }
    var Sn = Hc;
    function Xc(t) {
      var e = Sn(this, t).delete(t);
      return this.size -= e ? 1 : 0, e;
    }
    var qc = Xc;
    function Wc(t) {
      return Sn(this, t).get(t);
    }
    var Kc = Wc;
    function Zc(t) {
      return Sn(this, t).has(t);
    }
    var Qc = Zc;
    function Jc(t, e) {
      var r = Sn(this, t), a = r.size;
      return r.set(t, e), this.size += r.size == a ? 0 : 1, this;
    }
    var jc = Jc;
    function ua(t) {
      var e = -1, r = t == null ? 0 : t.length;
      for (this.clear(); ++e < r; ) {
        var a = t[e];
        this.set(a[0], a[1]);
      }
    }
    ua.prototype.clear = _c, ua.prototype.delete = qc, ua.prototype.get = Kc, ua.prototype.has = Qc, ua.prototype.set = jc;
    var to = ua, ev = "Expected a function";
    function xi(t, e) {
      if (typeof t != "function" || e != null && typeof e != "function")
        throw new TypeError(ev);
      var r = function() {
        var a = arguments, n = e ? e.apply(this, a) : a[0], i = r.cache;
        if (i.has(n))
          return i.get(n);
        var s = t.apply(this, a);
        return r.cache = i.set(n, s) || i, s;
      };
      return r.cache = new (xi.Cache || to)(), r;
    }
    xi.Cache = to;
    var tv = xi, rv = 500;
    function av(t) {
      var e = tv(t, function(a) {
        return r.size === rv && r.clear(), a;
      }), r = e.cache;
      return e;
    }
    var nv = av, iv = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g, sv = /\\(\\)?/g, ov = nv(function(t) {
      var e = [];
      return t.charCodeAt(0) === 46 && e.push(""), t.replace(iv, function(r, a, n, i) {
        e.push(n ? i.replace(sv, "$1") : a || r);
      }), e;
    }), ro = ov;
    function uv(t, e) {
      for (var r = -1, a = t == null ? 0 : t.length, n = Array(a); ++r < a; )
        n[r] = e(t[r], r, t);
      return n;
    }
    var ao = uv, lv = 1 / 0, no = Zr ? Zr.prototype : void 0, io = no ? no.toString : void 0;
    function so(t) {
      if (typeof t == "string")
        return t;
      if (Cn(t))
        return ao(t, so) + "";
      if (Aa(t))
        return io ? io.call(t) : "";
      var e = t + "";
      return e == "0" && 1 / t == -lv ? "-0" : e;
    }
    var fv = so;
    function hv(t) {
      return t == null ? "" : fv(t);
    }
    var oo = hv;
    function cv(t, e) {
      return Cn(t) ? t : Ph(t, e) ? [t] : ro(oo(t));
    }
    var uo = cv, vv = 1 / 0;
    function dv(t) {
      if (typeof t == "string" || Aa(t))
        return t;
      var e = t + "";
      return e == "0" && 1 / t == -vv ? "-0" : e;
    }
    var Ti = dv;
    function gv(t, e) {
      e = uo(e, t);
      for (var r = 0, a = e.length; t != null && r < a; )
        t = t[Ti(e[r++])];
      return r && r == a ? t : void 0;
    }
    var pv = gv;
    function yv(t, e, r) {
      var a = t == null ? void 0 : pv(t, e);
      return a === void 0 ? r : a;
    }
    var mv = yv, bv = function() {
      try {
        var t = wi(Object, "defineProperty");
        return t({}, "", {}), t;
      } catch {
      }
    }(), lo = bv;
    function Ev(t, e, r) {
      e == "__proto__" && lo ? lo(t, e, {
        configurable: !0,
        enumerable: !0,
        value: r,
        writable: !0
      }) : t[e] = r;
    }
    var wv = Ev, xv = Object.prototype, Tv = xv.hasOwnProperty;
    function Cv(t, e, r) {
      var a = t[e];
      (!(Tv.call(t, e) && eo(a, r)) || r === void 0 && !(e in t)) && wv(t, e, r);
    }
    var Dv = Cv, Sv = 9007199254740991, Lv = /^(?:0|[1-9]\d*)$/;
    function Av(t, e) {
      var r = typeof t;
      return e = e ?? Sv, !!e && (r == "number" || r != "symbol" && Lv.test(t)) && t > -1 && t % 1 == 0 && t < e;
    }
    var Ov = Av;
    function Nv(t, e, r, a) {
      if (!Rr(t))
        return t;
      e = uo(e, t);
      for (var n = -1, i = e.length, s = i - 1, o = t; o != null && ++n < i; ) {
        var l = Ti(e[n]), u = r;
        if (l === "__proto__" || l === "constructor" || l === "prototype")
          return t;
        if (n != s) {
          var f = o[l];
          u = a ? a(f, l, o) : void 0, u === void 0 && (u = Rr(f) ? f : Ov(e[n + 1]) ? [] : {});
        }
        Dv(o, l, u), o = o[l];
      }
      return t;
    }
    var Mv = Nv;
    function Iv(t, e, r) {
      return t == null ? t : Mv(t, e, r);
    }
    var Rv = Iv;
    function kv(t, e) {
      var r = -1, a = t.length;
      for (e || (e = Array(a)); ++r < a; )
        e[r] = t[r];
      return e;
    }
    var Pv = kv;
    function Bv(t) {
      return Cn(t) ? ao(t, Ti) : Aa(t) ? [t] : Pv(ro(oo(t)));
    }
    var Fv = Bv, zv = {
      // access data field
      data: function(e) {
        var r = {
          field: "data",
          bindingEvent: "data",
          allowBinding: !1,
          allowSetting: !1,
          allowGetting: !1,
          settingEvent: "data",
          settingTriggersEvent: !1,
          triggerFnName: "trigger",
          immutableKeys: {},
          // key => true if immutable
          updateStyle: !1,
          beforeGet: function(n) {
          },
          beforeSet: function(n, i) {
          },
          onSet: function(n) {
          },
          canSet: function(n) {
            return !0;
          }
        };
        return e = Ue({}, r, e), function(n, i) {
          var s = e, o = this, l = o.length !== void 0, u = l ? o : [o], f = l ? o[0] : o;
          if (ee(n)) {
            var h = n.indexOf(".") !== -1, c = h && Fv(n);
            if (s.allowGetting && i === void 0) {
              var v;
              return f && (s.beforeGet(f), c && f._private[s.field][n] === void 0 ? v = mv(f._private[s.field], c) : v = f._private[s.field][n]), v;
            } else if (s.allowSetting && i !== void 0) {
              var d = !s.immutableKeys[n];
              if (d) {
                var g = T({}, n, i);
                s.beforeSet(o, g);
                for (var y = 0, p = u.length; y < p; y++) {
                  var m = u[y];
                  s.canSet(m) && (c && f._private[s.field][n] === void 0 ? Rv(m._private[s.field], c, i) : m._private[s.field][n] = i);
                }
                s.updateStyle && o.updateStyle(), s.onSet(o), s.settingTriggersEvent && o[s.triggerFnName](s.settingEvent);
              }
            }
          } else if (s.allowSetting && S(n)) {
            var b = n, E, M, O = Object.keys(b);
            s.beforeSet(o, b);
            for (var x = 0; x < O.length; x++) {
              E = O[x], M = b[E];
              var I = !s.immutableKeys[E];
              if (I)
                for (var C = 0; C < u.length; C++) {
                  var B = u[C];
                  s.canSet(B) && (B._private[s.field][E] = M);
                }
            }
            s.updateStyle && o.updateStyle(), s.onSet(o), s.settingTriggersEvent && o[s.triggerFnName](s.settingEvent);
          } else if (s.allowBinding && H(n)) {
            var F = n;
            o.on(s.bindingEvent, F);
          } else if (s.allowGetting && n === void 0) {
            var R;
            return f && (s.beforeGet(f), R = f._private[s.field]), R;
          }
          return o;
        };
      },
      // data
      // remove data field
      removeData: function(e) {
        var r = {
          field: "data",
          event: "data",
          triggerFnName: "trigger",
          triggerEvent: !1,
          immutableKeys: {}
          // key => true if immutable
        };
        return e = Ue({}, r, e), function(n) {
          var i = e, s = this, o = s.length !== void 0, l = o ? s : [s];
          if (ee(n)) {
            for (var u = n.split(/\s+/), f = u.length, h = 0; h < f; h++) {
              var c = u[h];
              if (!Pe(c)) {
                var v = !i.immutableKeys[c];
                if (v)
                  for (var d = 0, g = l.length; d < g; d++)
                    l[d]._private[i.field][c] = void 0;
              }
            }
            i.triggerEvent && s[i.triggerFnName](i.event);
          } else if (n === void 0) {
            for (var y = 0, p = l.length; y < p; y++)
              for (var m = l[y]._private[i.field], b = Object.keys(m), E = 0; E < b.length; E++) {
                var M = b[E], O = !i.immutableKeys[M];
                O && (m[M] = void 0);
              }
            i.triggerEvent && s[i.triggerFnName](i.event);
          }
          return s;
        };
      }
      // removeData
    }, Gv = {
      eventAliasesOn: function(e) {
        var r = e;
        r.addListener = r.listen = r.bind = r.on, r.unlisten = r.unbind = r.off = r.removeListener, r.trigger = r.emit, r.pon = r.promiseOn = function(a, n) {
          var i = this, s = Array.prototype.slice.call(arguments, 0);
          return new ia(function(o, l) {
            var u = function(v) {
              i.off.apply(i, h), o(v);
            }, f = s.concat([u]), h = f.concat([]);
            i.on.apply(i, f);
          });
        };
      }
    }, ht = {};
    [Nh, zv, Gv].forEach(function(t) {
      Ue(ht, t);
    });
    var $v = {
      animate: ht.animate(),
      animation: ht.animation(),
      animated: ht.animated(),
      clearQueue: ht.clearQueue(),
      delay: ht.delay(),
      delayAnimation: ht.delayAnimation(),
      stop: ht.stop()
    }, Ln = {
      classes: function(e) {
        var r = this;
        if (e === void 0) {
          var a = [];
          return r[0]._private.classes.forEach(function(d) {
            return a.push(d);
          }), a;
        } else
          te(e) || (e = (e || "").match(/\S+/g) || []);
        for (var n = [], i = new Jr(e), s = 0; s < r.length; s++) {
          for (var o = r[s], l = o._private, u = l.classes, f = !1, h = 0; h < e.length; h++) {
            var c = e[h], v = u.has(c);
            if (!v) {
              f = !0;
              break;
            }
          }
          f || (f = u.size !== e.length), f && (l.classes = i, n.push(o));
        }
        return n.length > 0 && this.spawn(n).updateStyle().emit("class"), r;
      },
      addClass: function(e) {
        return this.toggleClass(e, !0);
      },
      hasClass: function(e) {
        var r = this[0];
        return r != null && r._private.classes.has(e);
      },
      toggleClass: function(e, r) {
        te(e) || (e = e.match(/\S+/g) || []);
        for (var a = this, n = r === void 0, i = [], s = 0, o = a.length; s < o; s++)
          for (var l = a[s], u = l._private.classes, f = !1, h = 0; h < e.length; h++) {
            var c = e[h], v = u.has(c), d = !1;
            r || n && !v ? (u.add(c), d = !0) : (!r || n && v) && (u.delete(c), d = !0), !f && d && (i.push(l), f = !0);
          }
        return i.length > 0 && this.spawn(i).updateStyle().emit("class"), a;
      },
      removeClass: function(e) {
        return this.toggleClass(e, !1);
      },
      flashClass: function(e, r) {
        var a = this;
        if (r == null)
          r = 250;
        else if (r === 0)
          return a;
        return a.addClass(e), setTimeout(function() {
          a.removeClass(e);
        }, r), a;
      }
    };
    Ln.className = Ln.classNames = Ln.classes;
    var it = {
      metaChar: "[\\!\\\"\\#\\$\\%\\&\\'\\(\\)\\*\\+\\,\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\]\\^\\`\\{\\|\\}\\~]",
      // chars we need to escape in let names, etc
      comparatorOp: "=|\\!=|>|>=|<|<=|\\$=|\\^=|\\*=",
      // binary comparison op (used in data selectors)
      boolOp: "\\?|\\!|\\^",
      // boolean (unary) operators (used in data selectors)
      string: `"(?:\\\\"|[^"])*"|'(?:\\\\'|[^'])*'`,
      // string literals (used in data selectors) -- doublequotes | singlequotes
      number: vt,
      // number literal (used in data selectors) --- e.g. 0.1234, 1234, 12e123
      meta: "degree|indegree|outdegree",
      // allowed metadata fields (i.e. allowed functions to use from Collection)
      separator: "\\s*,\\s*",
      // queries are separated by commas, e.g. edge[foo = 'bar'], node.someClass
      descendant: "\\s+",
      child: "\\s+>\\s+",
      subject: "\\$",
      group: "node|edge|\\*",
      directedEdge: "\\s+->\\s+",
      undirectedEdge: "\\s+<->\\s+"
    };
    it.variable = "(?:[\\w-.]|(?:\\\\" + it.metaChar + "))+", it.className = "(?:[\\w-]|(?:\\\\" + it.metaChar + "))+", it.value = it.string + "|" + it.number, it.id = it.variable, function() {
      var t, e, r;
      for (t = it.comparatorOp.split("|"), r = 0; r < t.length; r++)
        e = t[r], it.comparatorOp += "|@" + e;
      for (t = it.comparatorOp.split("|"), r = 0; r < t.length; r++)
        e = t[r], !(e.indexOf("!") >= 0) && e !== "=" && (it.comparatorOp += "|\\!" + e);
    }();
    var gt = function() {
      return {
        checks: []
      };
    }, Be = {
      /** E.g. node */
      GROUP: 0,
      /** A collection of elements */
      COLLECTION: 1,
      /** A filter(ele) function */
      FILTER: 2,
      /** E.g. [foo > 1] */
      DATA_COMPARE: 3,
      /** E.g. [foo] */
      DATA_EXIST: 4,
      /** E.g. [?foo] */
      DATA_BOOL: 5,
      /** E.g. [[degree > 2]] */
      META_COMPARE: 6,
      /** E.g. :selected */
      STATE: 7,
      /** E.g. #foo */
      ID: 8,
      /** E.g. .foo */
      CLASS: 9,
      /** E.g. #foo <-> #bar */
      UNDIRECTED_EDGE: 10,
      /** E.g. #foo -> #bar */
      DIRECTED_EDGE: 11,
      /** E.g. $#foo -> #bar */
      NODE_SOURCE: 12,
      /** E.g. #foo -> $#bar */
      NODE_TARGET: 13,
      /** E.g. $#foo <-> #bar */
      NODE_NEIGHBOR: 14,
      /** E.g. #foo > #bar */
      CHILD: 15,
      /** E.g. #foo #bar */
      DESCENDANT: 16,
      /** E.g. $#foo > #bar */
      PARENT: 17,
      /** E.g. $#foo #bar */
      ANCESTOR: 18,
      /** E.g. #foo > $bar > #baz */
      COMPOUND_SPLIT: 19,
      /** Always matches, useful placeholder for subject in `COMPOUND_SPLIT` */
      TRUE: 20
    }, Ci = [{
      selector: ":selected",
      matches: function(e) {
        return e.selected();
      }
    }, {
      selector: ":unselected",
      matches: function(e) {
        return !e.selected();
      }
    }, {
      selector: ":selectable",
      matches: function(e) {
        return e.selectable();
      }
    }, {
      selector: ":unselectable",
      matches: function(e) {
        return !e.selectable();
      }
    }, {
      selector: ":locked",
      matches: function(e) {
        return e.locked();
      }
    }, {
      selector: ":unlocked",
      matches: function(e) {
        return !e.locked();
      }
    }, {
      selector: ":visible",
      matches: function(e) {
        return e.visible();
      }
    }, {
      selector: ":hidden",
      matches: function(e) {
        return !e.visible();
      }
    }, {
      selector: ":transparent",
      matches: function(e) {
        return e.transparent();
      }
    }, {
      selector: ":grabbed",
      matches: function(e) {
        return e.grabbed();
      }
    }, {
      selector: ":free",
      matches: function(e) {
        return !e.grabbed();
      }
    }, {
      selector: ":removed",
      matches: function(e) {
        return e.removed();
      }
    }, {
      selector: ":inside",
      matches: function(e) {
        return !e.removed();
      }
    }, {
      selector: ":grabbable",
      matches: function(e) {
        return e.grabbable();
      }
    }, {
      selector: ":ungrabbable",
      matches: function(e) {
        return !e.grabbable();
      }
    }, {
      selector: ":animated",
      matches: function(e) {
        return e.animated();
      }
    }, {
      selector: ":unanimated",
      matches: function(e) {
        return !e.animated();
      }
    }, {
      selector: ":parent",
      matches: function(e) {
        return e.isParent();
      }
    }, {
      selector: ":childless",
      matches: function(e) {
        return e.isChildless();
      }
    }, {
      selector: ":child",
      matches: function(e) {
        return e.isChild();
      }
    }, {
      selector: ":orphan",
      matches: function(e) {
        return e.isOrphan();
      }
    }, {
      selector: ":nonorphan",
      matches: function(e) {
        return e.isChild();
      }
    }, {
      selector: ":compound",
      matches: function(e) {
        return e.isNode() ? e.isParent() : e.source().isParent() || e.target().isParent();
      }
    }, {
      selector: ":loop",
      matches: function(e) {
        return e.isLoop();
      }
    }, {
      selector: ":simple",
      matches: function(e) {
        return e.isSimple();
      }
    }, {
      selector: ":active",
      matches: function(e) {
        return e.active();
      }
    }, {
      selector: ":inactive",
      matches: function(e) {
        return !e.active();
      }
    }, {
      selector: ":backgrounding",
      matches: function(e) {
        return e.backgrounding();
      }
    }, {
      selector: ":nonbackgrounding",
      matches: function(e) {
        return !e.backgrounding();
      }
    }].sort(function(t, e) {
      return Qu(t.selector, e.selector);
    }), Vv = function() {
      for (var t = {}, e, r = 0; r < Ci.length; r++)
        e = Ci[r], t[e.selector] = e.matches;
      return t;
    }(), _v = function(e, r) {
      return Vv[e](r);
    }, Uv = "(" + Ci.map(function(t) {
      return t.selector;
    }).join("|") + ")", la = function(e) {
      return e.replace(new RegExp("\\\\(" + it.metaChar + ")", "g"), function(r, a) {
        return a;
      });
    }, Cr = function(e, r, a) {
      e[e.length - 1] = a;
    }, Di = [{
      name: "group",
      // just used for identifying when debugging
      query: !0,
      regex: "(" + it.group + ")",
      populate: function(e, r, a) {
        var n = w(a, 1), i = n[0];
        r.checks.push({
          type: Be.GROUP,
          value: i === "*" ? i : i + "s"
        });
      }
    }, {
      name: "state",
      query: !0,
      regex: Uv,
      populate: function(e, r, a) {
        var n = w(a, 1), i = n[0];
        r.checks.push({
          type: Be.STATE,
          value: i
        });
      }
    }, {
      name: "id",
      query: !0,
      regex: "\\#(" + it.id + ")",
      populate: function(e, r, a) {
        var n = w(a, 1), i = n[0];
        r.checks.push({
          type: Be.ID,
          value: la(i)
        });
      }
    }, {
      name: "className",
      query: !0,
      regex: "\\.(" + it.className + ")",
      populate: function(e, r, a) {
        var n = w(a, 1), i = n[0];
        r.checks.push({
          type: Be.CLASS,
          value: la(i)
        });
      }
    }, {
      name: "dataExists",
      query: !0,
      regex: "\\[\\s*(" + it.variable + ")\\s*\\]",
      populate: function(e, r, a) {
        var n = w(a, 1), i = n[0];
        r.checks.push({
          type: Be.DATA_EXIST,
          field: la(i)
        });
      }
    }, {
      name: "dataCompare",
      query: !0,
      regex: "\\[\\s*(" + it.variable + ")\\s*(" + it.comparatorOp + ")\\s*(" + it.value + ")\\s*\\]",
      populate: function(e, r, a) {
        var n = w(a, 3), i = n[0], s = n[1], o = n[2], l = new RegExp("^" + it.string + "$").exec(o) != null;
        l ? o = o.substring(1, o.length - 1) : o = parseFloat(o), r.checks.push({
          type: Be.DATA_COMPARE,
          field: la(i),
          operator: s,
          value: o
        });
      }
    }, {
      name: "dataBool",
      query: !0,
      regex: "\\[\\s*(" + it.boolOp + ")\\s*(" + it.variable + ")\\s*\\]",
      populate: function(e, r, a) {
        var n = w(a, 2), i = n[0], s = n[1];
        r.checks.push({
          type: Be.DATA_BOOL,
          field: la(s),
          operator: i
        });
      }
    }, {
      name: "metaCompare",
      query: !0,
      regex: "\\[\\[\\s*(" + it.meta + ")\\s*(" + it.comparatorOp + ")\\s*(" + it.number + ")\\s*\\]\\]",
      populate: function(e, r, a) {
        var n = w(a, 3), i = n[0], s = n[1], o = n[2];
        r.checks.push({
          type: Be.META_COMPARE,
          field: la(i),
          operator: s,
          value: parseFloat(o)
        });
      }
    }, {
      name: "nextQuery",
      separator: !0,
      regex: it.separator,
      populate: function(e, r) {
        var a = e.currentSubject, n = e.edgeCount, i = e.compoundCount, s = e[e.length - 1];
        a != null && (s.subject = a, e.currentSubject = null), s.edgeCount = n, s.compoundCount = i, e.edgeCount = 0, e.compoundCount = 0;
        var o = e[e.length++] = gt();
        return o;
      }
    }, {
      name: "directedEdge",
      separator: !0,
      regex: it.directedEdge,
      populate: function(e, r) {
        if (e.currentSubject == null) {
          var a = gt(), n = r, i = gt();
          return a.checks.push({
            type: Be.DIRECTED_EDGE,
            source: n,
            target: i
          }), Cr(e, r, a), e.edgeCount++, i;
        } else {
          var s = gt(), o = r, l = gt();
          return s.checks.push({
            type: Be.NODE_SOURCE,
            source: o,
            target: l
          }), Cr(e, r, s), e.edgeCount++, l;
        }
      }
    }, {
      name: "undirectedEdge",
      separator: !0,
      regex: it.undirectedEdge,
      populate: function(e, r) {
        if (e.currentSubject == null) {
          var a = gt(), n = r, i = gt();
          return a.checks.push({
            type: Be.UNDIRECTED_EDGE,
            nodes: [n, i]
          }), Cr(e, r, a), e.edgeCount++, i;
        } else {
          var s = gt(), o = r, l = gt();
          return s.checks.push({
            type: Be.NODE_NEIGHBOR,
            node: o,
            neighbor: l
          }), Cr(e, r, s), l;
        }
      }
    }, {
      name: "child",
      separator: !0,
      regex: it.child,
      populate: function(e, r) {
        if (e.currentSubject == null) {
          var a = gt(), n = gt(), i = e[e.length - 1];
          return a.checks.push({
            type: Be.CHILD,
            parent: i,
            child: n
          }), Cr(e, r, a), e.compoundCount++, n;
        } else if (e.currentSubject === r) {
          var s = gt(), o = e[e.length - 1], l = gt(), u = gt(), f = gt(), h = gt();
          return s.checks.push({
            type: Be.COMPOUND_SPLIT,
            left: o,
            right: l,
            subject: u
          }), u.checks = r.checks, r.checks = [{
            type: Be.TRUE
          }], h.checks.push({
            type: Be.TRUE
          }), l.checks.push({
            type: Be.PARENT,
            // type is swapped on right side queries
            parent: h,
            child: f
            // empty for now
          }), Cr(e, o, s), e.currentSubject = u, e.compoundCount++, f;
        } else {
          var c = gt(), v = gt(), d = [{
            type: Be.PARENT,
            parent: c,
            child: v
          }];
          return c.checks = r.checks, r.checks = d, e.compoundCount++, v;
        }
      }
    }, {
      name: "descendant",
      separator: !0,
      regex: it.descendant,
      populate: function(e, r) {
        if (e.currentSubject == null) {
          var a = gt(), n = gt(), i = e[e.length - 1];
          return a.checks.push({
            type: Be.DESCENDANT,
            ancestor: i,
            descendant: n
          }), Cr(e, r, a), e.compoundCount++, n;
        } else if (e.currentSubject === r) {
          var s = gt(), o = e[e.length - 1], l = gt(), u = gt(), f = gt(), h = gt();
          return s.checks.push({
            type: Be.COMPOUND_SPLIT,
            left: o,
            right: l,
            subject: u
          }), u.checks = r.checks, r.checks = [{
            type: Be.TRUE
          }], h.checks.push({
            type: Be.TRUE
          }), l.checks.push({
            type: Be.ANCESTOR,
            // type is swapped on right side queries
            ancestor: h,
            descendant: f
            // empty for now
          }), Cr(e, o, s), e.currentSubject = u, e.compoundCount++, f;
        } else {
          var c = gt(), v = gt(), d = [{
            type: Be.ANCESTOR,
            ancestor: c,
            descendant: v
          }];
          return c.checks = r.checks, r.checks = d, e.compoundCount++, v;
        }
      }
    }, {
      name: "subject",
      modifier: !0,
      regex: it.subject,
      populate: function(e, r) {
        if (e.currentSubject != null && e.currentSubject !== r)
          return ft("Redefinition of subject in selector `" + e.toString() + "`"), !1;
        e.currentSubject = r;
        var a = e[e.length - 1], n = a.checks[0], i = n == null ? null : n.type;
        i === Be.DIRECTED_EDGE ? n.type = Be.NODE_TARGET : i === Be.UNDIRECTED_EDGE && (n.type = Be.NODE_NEIGHBOR, n.node = n.nodes[1], n.neighbor = n.nodes[0], n.nodes = null);
      }
    }];
    Di.forEach(function(t) {
      return t.regexObj = new RegExp("^" + t.regex);
    });
    var Yv = function(e) {
      for (var r, a, n, i = 0; i < Di.length; i++) {
        var s = Di[i], o = s.name, l = e.match(s.regexObj);
        if (l != null) {
          a = l, r = s, n = o;
          var u = l[0];
          e = e.substring(u.length);
          break;
        }
      }
      return {
        expr: r,
        match: a,
        name: n,
        remaining: e
      };
    }, Hv = function(e) {
      var r = e.match(/^\s+/);
      if (r) {
        var a = r[0];
        e = e.substring(a.length);
      }
      return e;
    }, Xv = function(e) {
      var r = this, a = r.inputText = e, n = r[0] = gt();
      for (r.length = 1, a = Hv(a); ; ) {
        var i = Yv(a);
        if (i.expr == null)
          return ft("The selector `" + e + "`is invalid"), !1;
        var s = i.match.slice(1), o = i.expr.populate(r, n, s);
        if (o === !1)
          return !1;
        if (o != null && (n = o), a = i.remaining, a.match(/^\s*$/))
          break;
      }
      var l = r[r.length - 1];
      r.currentSubject != null && (l.subject = r.currentSubject), l.edgeCount = r.edgeCount, l.compoundCount = r.compoundCount;
      for (var u = 0; u < r.length; u++) {
        var f = r[u];
        if (f.compoundCount > 0 && f.edgeCount > 0)
          return ft("The selector `" + e + "` is invalid because it uses both a compound selector and an edge selector"), !1;
        if (f.edgeCount > 1)
          return ft("The selector `" + e + "` is invalid because it uses multiple edge selectors"), !1;
        f.edgeCount === 1 && ft("The selector `" + e + "` is deprecated.  Edge selectors do not take effect on changes to source and target nodes after an edge is added, for performance reasons.  Use a class or data selector on edges instead, updating the class or data of an edge when your app detects a change in source or target nodes.");
      }
      return !0;
    }, qv = function() {
      if (this.toStringCache != null)
        return this.toStringCache;
      for (var e = function(f) {
        return f ?? "";
      }, r = function(f) {
        return ee(f) ? '"' + f + '"' : e(f);
      }, a = function(f) {
        return " " + f + " ";
      }, n = function(f, h) {
        var c = f.type, v = f.value;
        switch (c) {
          case Be.GROUP: {
            var d = e(v);
            return d.substring(0, d.length - 1);
          }
          case Be.DATA_COMPARE: {
            var g = f.field, y = f.operator;
            return "[" + g + a(e(y)) + r(v) + "]";
          }
          case Be.DATA_BOOL: {
            var p = f.operator, m = f.field;
            return "[" + e(p) + m + "]";
          }
          case Be.DATA_EXIST: {
            var b = f.field;
            return "[" + b + "]";
          }
          case Be.META_COMPARE: {
            var E = f.operator, M = f.field;
            return "[[" + M + a(e(E)) + r(v) + "]]";
          }
          case Be.STATE:
            return v;
          case Be.ID:
            return "#" + v;
          case Be.CLASS:
            return "." + v;
          case Be.PARENT:
          case Be.CHILD:
            return i(f.parent, h) + a(">") + i(f.child, h);
          case Be.ANCESTOR:
          case Be.DESCENDANT:
            return i(f.ancestor, h) + " " + i(f.descendant, h);
          case Be.COMPOUND_SPLIT: {
            var O = i(f.left, h), x = i(f.subject, h), I = i(f.right, h);
            return O + (O.length > 0 ? " " : "") + x + I;
          }
          case Be.TRUE:
            return "";
        }
      }, i = function(f, h) {
        return f.checks.reduce(function(c, v, d) {
          return c + (h === f && d === 0 ? "$" : "") + n(v, h);
        }, "");
      }, s = "", o = 0; o < this.length; o++) {
        var l = this[o];
        s += i(l, l.subject), this.length > 1 && o < this.length - 1 && (s += ", ");
      }
      return this.toStringCache = s, s;
    }, Wv = {
      parse: Xv,
      toString: qv
    }, fo = function(e, r, a) {
      var n, i = ee(e), s = k(e), o = ee(a), l, u, f = !1, h = !1, c = !1;
      switch (r.indexOf("!") >= 0 && (r = r.replace("!", ""), h = !0), r.indexOf("@") >= 0 && (r = r.replace("@", ""), f = !0), (i || o || f) && (l = !i && !s ? "" : "" + e, u = "" + a), f && (e = l = l.toLowerCase(), a = u = u.toLowerCase()), r) {
        case "*=":
          n = l.indexOf(u) >= 0;
          break;
        case "$=":
          n = l.indexOf(u, l.length - u.length) >= 0;
          break;
        case "^=":
          n = l.indexOf(u) === 0;
          break;
        case "=":
          n = e === a;
          break;
        case ">":
          c = !0, n = e > a;
          break;
        case ">=":
          c = !0, n = e >= a;
          break;
        case "<":
          c = !0, n = e < a;
          break;
        case "<=":
          c = !0, n = e <= a;
          break;
        default:
          n = !1;
          break;
      }
      return h && (e != null || !c) && (n = !n), n;
    }, Kv = function(e, r) {
      switch (r) {
        case "?":
          return !!e;
        case "!":
          return !e;
        case "^":
          return e === void 0;
      }
    }, Zv = function(e) {
      return e !== void 0;
    }, Si = function(e, r) {
      return e.data(r);
    }, Qv = function(e, r) {
      return e[r]();
    }, Tt = [], wt = function(e, r) {
      return e.checks.every(function(a) {
        return Tt[a.type](a, r);
      });
    };
    Tt[Be.GROUP] = function(t, e) {
      var r = t.value;
      return r === "*" || r === e.group();
    }, Tt[Be.STATE] = function(t, e) {
      var r = t.value;
      return _v(r, e);
    }, Tt[Be.ID] = function(t, e) {
      var r = t.value;
      return e.id() === r;
    }, Tt[Be.CLASS] = function(t, e) {
      var r = t.value;
      return e.hasClass(r);
    }, Tt[Be.META_COMPARE] = function(t, e) {
      var r = t.field, a = t.operator, n = t.value;
      return fo(Qv(e, r), a, n);
    }, Tt[Be.DATA_COMPARE] = function(t, e) {
      var r = t.field, a = t.operator, n = t.value;
      return fo(Si(e, r), a, n);
    }, Tt[Be.DATA_BOOL] = function(t, e) {
      var r = t.field, a = t.operator;
      return Kv(Si(e, r), a);
    }, Tt[Be.DATA_EXIST] = function(t, e) {
      var r = t.field;
      return t.operator, Zv(Si(e, r));
    }, Tt[Be.UNDIRECTED_EDGE] = function(t, e) {
      var r = t.nodes[0], a = t.nodes[1], n = e.source(), i = e.target();
      return wt(r, n) && wt(a, i) || wt(a, n) && wt(r, i);
    }, Tt[Be.NODE_NEIGHBOR] = function(t, e) {
      return wt(t.node, e) && e.neighborhood().some(function(r) {
        return r.isNode() && wt(t.neighbor, r);
      });
    }, Tt[Be.DIRECTED_EDGE] = function(t, e) {
      return wt(t.source, e.source()) && wt(t.target, e.target());
    }, Tt[Be.NODE_SOURCE] = function(t, e) {
      return wt(t.source, e) && e.outgoers().some(function(r) {
        return r.isNode() && wt(t.target, r);
      });
    }, Tt[Be.NODE_TARGET] = function(t, e) {
      return wt(t.target, e) && e.incomers().some(function(r) {
        return r.isNode() && wt(t.source, r);
      });
    }, Tt[Be.CHILD] = function(t, e) {
      return wt(t.child, e) && wt(t.parent, e.parent());
    }, Tt[Be.PARENT] = function(t, e) {
      return wt(t.parent, e) && e.children().some(function(r) {
        return wt(t.child, r);
      });
    }, Tt[Be.DESCENDANT] = function(t, e) {
      return wt(t.descendant, e) && e.ancestors().some(function(r) {
        return wt(t.ancestor, r);
      });
    }, Tt[Be.ANCESTOR] = function(t, e) {
      return wt(t.ancestor, e) && e.descendants().some(function(r) {
        return wt(t.descendant, r);
      });
    }, Tt[Be.COMPOUND_SPLIT] = function(t, e) {
      return wt(t.subject, e) && wt(t.left, e) && wt(t.right, e);
    }, Tt[Be.TRUE] = function() {
      return !0;
    }, Tt[Be.COLLECTION] = function(t, e) {
      var r = t.value;
      return r.has(e);
    }, Tt[Be.FILTER] = function(t, e) {
      var r = t.value;
      return r(e);
    };
    var Jv = function(e) {
      var r = this;
      if (r.length === 1 && r[0].checks.length === 1 && r[0].checks[0].type === Be.ID)
        return e.getElementById(r[0].checks[0].value).collection();
      var a = function(i) {
        for (var s = 0; s < r.length; s++) {
          var o = r[s];
          if (wt(o, i))
            return !0;
        }
        return !1;
      };
      return r.text() == null && (a = function() {
        return !0;
      }), e.filter(a);
    }, jv = function(e) {
      for (var r = this, a = 0; a < r.length; a++) {
        var n = r[a];
        if (wt(n, e))
          return !0;
      }
      return !1;
    }, ed = {
      matches: jv,
      filter: Jv
    }, Dr = function(e) {
      this.inputText = e, this.currentSubject = null, this.compoundCount = 0, this.edgeCount = 0, this.length = 0, e == null || ee(e) && e.match(/^\s*$/) || (pe(e) ? this.addQuery({
        checks: [{
          type: Be.COLLECTION,
          value: e.collection()
        }]
      }) : H(e) ? this.addQuery({
        checks: [{
          type: Be.FILTER,
          value: e
        }]
      }) : ee(e) ? this.parse(e) || (this.invalid = !0) : xt("A selector must be created from a string; found "));
    }, Sr = Dr.prototype;
    [Wv, ed].forEach(function(t) {
      return Ue(Sr, t);
    }), Sr.text = function() {
      return this.inputText;
    }, Sr.size = function() {
      return this.length;
    }, Sr.eq = function(t) {
      return this[t];
    }, Sr.sameText = function(t) {
      return !this.invalid && !t.invalid && this.text() === t.text();
    }, Sr.addQuery = function(t) {
      this[this.length++] = t;
    }, Sr.selector = Sr.toString;
    var Lr = {
      allAre: function(e) {
        var r = new Dr(e);
        return this.every(function(a) {
          return r.matches(a);
        });
      },
      is: function(e) {
        var r = new Dr(e);
        return this.some(function(a) {
          return r.matches(a);
        });
      },
      some: function(e, r) {
        for (var a = 0; a < this.length; a++) {
          var n = r ? e.apply(r, [this[a], a, this]) : e(this[a], a, this);
          if (n)
            return !0;
        }
        return !1;
      },
      every: function(e, r) {
        for (var a = 0; a < this.length; a++) {
          var n = r ? e.apply(r, [this[a], a, this]) : e(this[a], a, this);
          if (!n)
            return !1;
        }
        return !0;
      },
      same: function(e) {
        if (this === e)
          return !0;
        e = this.cy().collection(e);
        var r = this.length, a = e.length;
        return r !== a ? !1 : r === 1 ? this[0] === e[0] : this.every(function(n) {
          return e.hasElementWithId(n.id());
        });
      },
      anySame: function(e) {
        return e = this.cy().collection(e), this.some(function(r) {
          return e.hasElementWithId(r.id());
        });
      },
      allAreNeighbors: function(e) {
        e = this.cy().collection(e);
        var r = this.neighborhood();
        return e.every(function(a) {
          return r.hasElementWithId(a.id());
        });
      },
      contains: function(e) {
        e = this.cy().collection(e);
        var r = this;
        return e.every(function(a) {
          return r.hasElementWithId(a.id());
        });
      }
    };
    Lr.allAreNeighbours = Lr.allAreNeighbors, Lr.has = Lr.contains, Lr.equal = Lr.equals = Lr.same;
    var Kt = function(e, r) {
      return function(n, i, s, o) {
        var l = n, u = this, f;
        if (l == null ? f = "" : pe(l) && l.length === 1 && (f = l.id()), u.length === 1 && f) {
          var h = u[0]._private, c = h.traversalCache = h.traversalCache || {}, v = c[r] = c[r] || [], d = kr(f), g = v[d];
          return g || (v[d] = e.call(u, n, i, s, o));
        } else
          return e.call(u, n, i, s, o);
      };
    }, fa = {
      parent: function(e) {
        var r = [];
        if (this.length === 1) {
          var a = this[0]._private.parent;
          if (a)
            return a;
        }
        for (var n = 0; n < this.length; n++) {
          var i = this[n], s = i._private.parent;
          s && r.push(s);
        }
        return this.spawn(r, !0).filter(e);
      },
      parents: function(e) {
        for (var r = [], a = this.parent(); a.nonempty(); ) {
          for (var n = 0; n < a.length; n++) {
            var i = a[n];
            r.push(i);
          }
          a = a.parent();
        }
        return this.spawn(r, !0).filter(e);
      },
      commonAncestors: function(e) {
        for (var r, a = 0; a < this.length; a++) {
          var n = this[a], i = n.parents();
          r = r || i, r = r.intersect(i);
        }
        return r.filter(e);
      },
      orphans: function(e) {
        return this.stdFilter(function(r) {
          return r.isOrphan();
        }).filter(e);
      },
      nonorphans: function(e) {
        return this.stdFilter(function(r) {
          return r.isChild();
        }).filter(e);
      },
      children: Kt(function(t) {
        for (var e = [], r = 0; r < this.length; r++)
          for (var a = this[r], n = a._private.children, i = 0; i < n.length; i++)
            e.push(n[i]);
        return this.spawn(e, !0).filter(t);
      }, "children"),
      siblings: function(e) {
        return this.parent().children().not(this).filter(e);
      },
      isParent: function() {
        var e = this[0];
        if (e)
          return e.isNode() && e._private.children.length !== 0;
      },
      isChildless: function() {
        var e = this[0];
        if (e)
          return e.isNode() && e._private.children.length === 0;
      },
      isChild: function() {
        var e = this[0];
        if (e)
          return e.isNode() && e._private.parent != null;
      },
      isOrphan: function() {
        var e = this[0];
        if (e)
          return e.isNode() && e._private.parent == null;
      },
      descendants: function(e) {
        var r = [];
        function a(n) {
          for (var i = 0; i < n.length; i++) {
            var s = n[i];
            r.push(s), s.children().nonempty() && a(s.children());
          }
        }
        return a(this.children()), this.spawn(r, !0).filter(e);
      }
    };
    function Li(t, e, r, a) {
      for (var n = [], i = new Jr(), s = t.cy(), o = s.hasCompoundNodes(), l = 0; l < t.length; l++) {
        var u = t[l];
        r ? n.push(u) : o && a(n, i, u);
      }
      for (; n.length > 0; ) {
        var f = n.shift();
        e(f), i.add(f.id()), o && a(n, i, f);
      }
      return t;
    }
    function ho(t, e, r) {
      if (r.isParent())
        for (var a = r._private.children, n = 0; n < a.length; n++) {
          var i = a[n];
          e.has(i.id()) || t.push(i);
        }
    }
    fa.forEachDown = function(t) {
      var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !0;
      return Li(this, t, e, ho);
    };
    function co(t, e, r) {
      if (r.isChild()) {
        var a = r._private.parent;
        e.has(a.id()) || t.push(a);
      }
    }
    fa.forEachUp = function(t) {
      var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !0;
      return Li(this, t, e, co);
    };
    function td(t, e, r) {
      co(t, e, r), ho(t, e, r);
    }
    fa.forEachUpAndDown = function(t) {
      var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !0;
      return Li(this, t, e, td);
    }, fa.ancestors = fa.parents;
    var $a, vo;
    $a = vo = {
      data: ht.data({
        field: "data",
        bindingEvent: "data",
        allowBinding: !0,
        allowSetting: !0,
        settingEvent: "data",
        settingTriggersEvent: !0,
        triggerFnName: "trigger",
        allowGetting: !0,
        immutableKeys: {
          id: !0,
          source: !0,
          target: !0,
          parent: !0
        },
        updateStyle: !0
      }),
      removeData: ht.removeData({
        field: "data",
        event: "data",
        triggerFnName: "trigger",
        triggerEvent: !0,
        immutableKeys: {
          id: !0,
          source: !0,
          target: !0,
          parent: !0
        },
        updateStyle: !0
      }),
      scratch: ht.data({
        field: "scratch",
        bindingEvent: "scratch",
        allowBinding: !0,
        allowSetting: !0,
        settingEvent: "scratch",
        settingTriggersEvent: !0,
        triggerFnName: "trigger",
        allowGetting: !0,
        updateStyle: !0
      }),
      removeScratch: ht.removeData({
        field: "scratch",
        event: "scratch",
        triggerFnName: "trigger",
        triggerEvent: !0,
        updateStyle: !0
      }),
      rscratch: ht.data({
        field: "rscratch",
        allowBinding: !1,
        allowSetting: !0,
        settingTriggersEvent: !1,
        allowGetting: !0
      }),
      removeRscratch: ht.removeData({
        field: "rscratch",
        triggerEvent: !1
      }),
      id: function() {
        var e = this[0];
        if (e)
          return e._private.data.id;
      }
    }, $a.attr = $a.data, $a.removeAttr = $a.removeData;
    var rd = vo, An = {};
    function Ai(t) {
      return function(e) {
        var r = this;
        if (e === void 0 && (e = !0), r.length !== 0)
          if (r.isNode() && !r.removed()) {
            for (var a = 0, n = r[0], i = n._private.edges, s = 0; s < i.length; s++) {
              var o = i[s];
              !e && o.isLoop() || (a += t(n, o));
            }
            return a;
          } else
            return;
      };
    }
    Ue(An, {
      degree: Ai(function(t, e) {
        return e.source().same(e.target()) ? 2 : 1;
      }),
      indegree: Ai(function(t, e) {
        return e.target().same(t) ? 1 : 0;
      }),
      outdegree: Ai(function(t, e) {
        return e.source().same(t) ? 1 : 0;
      })
    });
    function ha(t, e) {
      return function(r) {
        for (var a, n = this.nodes(), i = 0; i < n.length; i++) {
          var s = n[i], o = s[t](r);
          o !== void 0 && (a === void 0 || e(o, a)) && (a = o);
        }
        return a;
      };
    }
    Ue(An, {
      minDegree: ha("degree", function(t, e) {
        return t < e;
      }),
      maxDegree: ha("degree", function(t, e) {
        return t > e;
      }),
      minIndegree: ha("indegree", function(t, e) {
        return t < e;
      }),
      maxIndegree: ha("indegree", function(t, e) {
        return t > e;
      }),
      minOutdegree: ha("outdegree", function(t, e) {
        return t < e;
      }),
      maxOutdegree: ha("outdegree", function(t, e) {
        return t > e;
      })
    }), Ue(An, {
      totalDegree: function(e) {
        for (var r = 0, a = this.nodes(), n = 0; n < a.length; n++)
          r += a[n].degree(e);
        return r;
      }
    });
    var tr, go, po = function(e, r, a) {
      for (var n = 0; n < e.length; n++) {
        var i = e[n];
        if (!i.locked()) {
          var s = i._private.position, o = {
            x: r.x != null ? r.x - s.x : 0,
            y: r.y != null ? r.y - s.y : 0
          };
          i.isParent() && !(o.x === 0 && o.y === 0) && i.children().shift(o, a), i.dirtyBoundingBoxCache();
        }
      }
    }, yo = {
      field: "position",
      bindingEvent: "position",
      allowBinding: !0,
      allowSetting: !0,
      settingEvent: "position",
      settingTriggersEvent: !0,
      triggerFnName: "emitAndNotify",
      allowGetting: !0,
      validKeys: ["x", "y"],
      beforeGet: function(e) {
        e.updateCompoundBounds();
      },
      beforeSet: function(e, r) {
        po(e, r, !1);
      },
      onSet: function(e) {
        e.dirtyCompoundBoundsCache();
      },
      canSet: function(e) {
        return !e.locked();
      }
    };
    tr = go = {
      position: ht.data(yo),
      // position but no notification to renderer
      silentPosition: ht.data(Ue({}, yo, {
        allowBinding: !1,
        allowSetting: !0,
        settingTriggersEvent: !1,
        allowGetting: !1,
        beforeSet: function(e, r) {
          po(e, r, !0);
        },
        onSet: function(e) {
          e.dirtyCompoundBoundsCache();
        }
      })),
      positions: function(e, r) {
        if (S(e))
          r ? this.silentPosition(e) : this.position(e);
        else if (H(e)) {
          var a = e, n = this.cy();
          n.startBatch();
          for (var i = 0; i < this.length; i++) {
            var s = this[i], o = void 0;
            (o = a(s, i)) && (r ? s.silentPosition(o) : s.position(o));
          }
          n.endBatch();
        }
        return this;
      },
      silentPositions: function(e) {
        return this.positions(e, !0);
      },
      shift: function(e, r, a) {
        var n;
        if (S(e) ? (n = {
          x: k(e.x) ? e.x : 0,
          y: k(e.y) ? e.y : 0
        }, a = r) : ee(e) && k(r) && (n = {
          x: 0,
          y: 0
        }, n[e] = r), n != null) {
          var i = this.cy();
          i.startBatch();
          for (var s = 0; s < this.length; s++) {
            var o = this[s];
            if (!(i.hasCompoundNodes() && o.isChild() && o.ancestors().anySame(this))) {
              var l = o.position(), u = {
                x: l.x + n.x,
                y: l.y + n.y
              };
              a ? o.silentPosition(u) : o.position(u);
            }
          }
          i.endBatch();
        }
        return this;
      },
      silentShift: function(e, r) {
        return S(e) ? this.shift(e, !0) : ee(e) && k(r) && this.shift(e, r, !0), this;
      },
      // get/set the rendered (i.e. on screen) positon of the element
      renderedPosition: function(e, r) {
        var a = this[0], n = this.cy(), i = n.zoom(), s = n.pan(), o = S(e) ? e : void 0, l = o !== void 0 || r !== void 0 && ee(e);
        if (a && a.isNode())
          if (l)
            for (var u = 0; u < this.length; u++) {
              var f = this[u];
              r !== void 0 ? f.position(e, (r - s[e]) / i) : o !== void 0 && f.position(bs(o, i, s));
            }
          else {
            var h = a.position();
            return o = gn(h, i, s), e === void 0 ? o : o[e];
          }
        else if (!l)
          return;
        return this;
      },
      // get/set the position relative to the parent
      relativePosition: function(e, r) {
        var a = this[0], n = this.cy(), i = S(e) ? e : void 0, s = i !== void 0 || r !== void 0 && ee(e), o = n.hasCompoundNodes();
        if (a && a.isNode())
          if (s)
            for (var l = 0; l < this.length; l++) {
              var u = this[l], f = o ? u.parent() : null, h = f && f.length > 0, c = h;
              h && (f = f[0]);
              var v = c ? f.position() : {
                x: 0,
                y: 0
              };
              r !== void 0 ? u.position(e, r + v[e]) : i !== void 0 && u.position({
                x: i.x + v.x,
                y: i.y + v.y
              });
            }
          else {
            var d = a.position(), g = o ? a.parent() : null, y = g && g.length > 0, p = y;
            y && (g = g[0]);
            var m = p ? g.position() : {
              x: 0,
              y: 0
            };
            return i = {
              x: d.x - m.x,
              y: d.y - m.y
            }, e === void 0 ? i : i[e];
          }
        else if (!s)
          return;
        return this;
      }
    }, tr.modelPosition = tr.point = tr.position, tr.modelPositions = tr.points = tr.positions, tr.renderedPoint = tr.renderedPosition, tr.relativePoint = tr.relativePosition;
    var ad = go, ca, Ar;
    ca = Ar = {}, Ar.renderedBoundingBox = function(t) {
      var e = this.boundingBox(t), r = this.cy(), a = r.zoom(), n = r.pan(), i = e.x1 * a + n.x, s = e.x2 * a + n.x, o = e.y1 * a + n.y, l = e.y2 * a + n.y;
      return {
        x1: i,
        x2: s,
        y1: o,
        y2: l,
        w: s - i,
        h: l - o
      };
    }, Ar.dirtyCompoundBoundsCache = function() {
      var t = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : !1, e = this.cy();
      return !e.styleEnabled() || !e.hasCompoundNodes() ? this : (this.forEachUp(function(r) {
        if (r.isParent()) {
          var a = r._private;
          a.compoundBoundsClean = !1, a.bbCache = null, t || r.emitAndNotify("bounds");
        }
      }), this);
    }, Ar.updateCompoundBounds = function() {
      var t = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : !1, e = this.cy();
      if (!e.styleEnabled() || !e.hasCompoundNodes())
        return this;
      if (!t && e.batching())
        return this;
      function r(s) {
        if (!s.isParent())
          return;
        var o = s._private, l = s.children(), u = s.pstyle("compound-sizing-wrt-labels").value === "include", f = {
          width: {
            val: s.pstyle("min-width").pfValue,
            left: s.pstyle("min-width-bias-left"),
            right: s.pstyle("min-width-bias-right")
          },
          height: {
            val: s.pstyle("min-height").pfValue,
            top: s.pstyle("min-height-bias-top"),
            bottom: s.pstyle("min-height-bias-bottom")
          }
        }, h = l.boundingBox({
          includeLabels: u,
          includeOverlays: !1,
          // updating the compound bounds happens outside of the regular
          // cache cycle (i.e. before fired events)
          useCache: !1
        }), c = o.position;
        (h.w === 0 || h.h === 0) && (h = {
          w: s.pstyle("width").pfValue,
          h: s.pstyle("height").pfValue
        }, h.x1 = c.x - h.w / 2, h.x2 = c.x + h.w / 2, h.y1 = c.y - h.h / 2, h.y2 = c.y + h.h / 2);
        function v(C, B, F) {
          var R = 0, X = 0, z = B + F;
          return C > 0 && z > 0 && (R = B / z * C, X = F / z * C), {
            biasDiff: R,
            biasComplementDiff: X
          };
        }
        function d(C, B, F, R) {
          if (F.units === "%")
            switch (R) {
              case "width":
                return C > 0 ? F.pfValue * C : 0;
              case "height":
                return B > 0 ? F.pfValue * B : 0;
              case "average":
                return C > 0 && B > 0 ? F.pfValue * (C + B) / 2 : 0;
              case "min":
                return C > 0 && B > 0 ? C > B ? F.pfValue * B : F.pfValue * C : 0;
              case "max":
                return C > 0 && B > 0 ? C > B ? F.pfValue * C : F.pfValue * B : 0;
              default:
                return 0;
            }
          else
            return F.units === "px" ? F.pfValue : 0;
        }
        var g = f.width.left.value;
        f.width.left.units === "px" && f.width.val > 0 && (g = g * 100 / f.width.val);
        var y = f.width.right.value;
        f.width.right.units === "px" && f.width.val > 0 && (y = y * 100 / f.width.val);
        var p = f.height.top.value;
        f.height.top.units === "px" && f.height.val > 0 && (p = p * 100 / f.height.val);
        var m = f.height.bottom.value;
        f.height.bottom.units === "px" && f.height.val > 0 && (m = m * 100 / f.height.val);
        var b = v(f.width.val - h.w, g, y), E = b.biasDiff, M = b.biasComplementDiff, O = v(f.height.val - h.h, p, m), x = O.biasDiff, I = O.biasComplementDiff;
        o.autoPadding = d(h.w, h.h, s.pstyle("padding"), s.pstyle("padding-relative-to").value), o.autoWidth = Math.max(h.w, f.width.val), c.x = (-E + h.x1 + h.x2 + M) / 2, o.autoHeight = Math.max(h.h, f.height.val), c.y = (-x + h.y1 + h.y2 + I) / 2;
      }
      for (var a = 0; a < this.length; a++) {
        var n = this[a], i = n._private;
        (!i.compoundBoundsClean || t) && (r(n), e.batching() || (i.compoundBoundsClean = !0));
      }
      return this;
    };
    var Zt = function(e) {
      return e === 1 / 0 || e === -1 / 0 ? 0 : e;
    }, rr = function(e, r, a, n, i) {
      n - r === 0 || i - a === 0 || r == null || a == null || n == null || i == null || (e.x1 = r < e.x1 ? r : e.x1, e.x2 = n > e.x2 ? n : e.x2, e.y1 = a < e.y1 ? a : e.y1, e.y2 = i > e.y2 ? i : e.y2, e.w = e.x2 - e.x1, e.h = e.y2 - e.y1);
    }, Gr = function(e, r) {
      return r == null ? e : rr(e, r.x1, r.y1, r.x2, r.y2);
    }, Va = function(e, r, a) {
      return er(e, r, a);
    }, On = function(e, r, a) {
      if (!r.cy().headless()) {
        var n = r._private, i = n.rstyle, s = i.arrowWidth / 2, o = r.pstyle(a + "-arrow-shape").value, l, u;
        if (o !== "none") {
          a === "source" ? (l = i.srcX, u = i.srcY) : a === "target" ? (l = i.tgtX, u = i.tgtY) : (l = i.midX, u = i.midY);
          var f = n.arrowBounds = n.arrowBounds || {}, h = f[a] = f[a] || {};
          h.x1 = l - s, h.y1 = u - s, h.x2 = l + s, h.y2 = u + s, h.w = h.x2 - h.x1, h.h = h.y2 - h.y1, yn(h, 1), rr(e, h.x1, h.y1, h.x2, h.y2);
        }
      }
    }, Oi = function(e, r, a) {
      if (!r.cy().headless()) {
        var n;
        a ? n = a + "-" : n = "";
        var i = r._private, s = i.rstyle, o = r.pstyle(n + "label").strValue;
        if (o) {
          var l = r.pstyle("text-halign"), u = r.pstyle("text-valign"), f = Va(s, "labelWidth", a), h = Va(s, "labelHeight", a), c = Va(s, "labelX", a), v = Va(s, "labelY", a), d = r.pstyle(n + "text-margin-x").pfValue, g = r.pstyle(n + "text-margin-y").pfValue, y = r.isEdge(), p = r.pstyle(n + "text-rotation"), m = r.pstyle("text-outline-width").pfValue, b = r.pstyle("text-border-width").pfValue, E = b / 2, M = r.pstyle("text-background-padding").pfValue, O = 2, x = h, I = f, C = I / 2, B = x / 2, F, R, X, z;
          if (y)
            F = c - C, R = c + C, X = v - B, z = v + B;
          else {
            switch (l.value) {
              case "left":
                F = c - I, R = c;
                break;
              case "center":
                F = c - C, R = c + C;
                break;
              case "right":
                F = c, R = c + I;
                break;
            }
            switch (u.value) {
              case "top":
                X = v - x, z = v;
                break;
              case "center":
                X = v - B, z = v + B;
                break;
              case "bottom":
                X = v, z = v + x;
                break;
            }
          }
          F += d - Math.max(m, E) - M - O, R += d + Math.max(m, E) + M + O, X += g - Math.max(m, E) - M - O, z += g + Math.max(m, E) + M + O;
          var re = a || "main", W = i.labelBounds, Z = W[re] = W[re] || {};
          Z.x1 = F, Z.y1 = X, Z.x2 = R, Z.y2 = z, Z.w = R - F, Z.h = z - X;
          var ie = y && p.strValue === "autorotate", oe = p.pfValue != null && p.pfValue !== 0;
          if (ie || oe) {
            var ge = ie ? Va(i.rstyle, "labelAngle", a) : p.pfValue, se = Math.cos(ge), de = Math.sin(ge), we = (F + R) / 2, Te = (X + z) / 2;
            if (!y) {
              switch (l.value) {
                case "left":
                  we = R;
                  break;
                case "right":
                  we = F;
                  break;
              }
              switch (u.value) {
                case "top":
                  Te = z;
                  break;
                case "bottom":
                  Te = X;
                  break;
              }
            }
            var Ee = function(qe, Re) {
              return qe = qe - we, Re = Re - Te, {
                x: qe * se - Re * de + we,
                y: qe * de + Re * se + Te
              };
            }, ye = Ee(F, X), ae = Ee(F, z), xe = Ee(R, X), Ce = Ee(R, z);
            F = Math.min(ye.x, ae.x, xe.x, Ce.x), R = Math.max(ye.x, ae.x, xe.x, Ce.x), X = Math.min(ye.y, ae.y, xe.y, Ce.y), z = Math.max(ye.y, ae.y, xe.y, Ce.y);
          }
          var Oe = re + "Rot", Ie = W[Oe] = W[Oe] || {};
          Ie.x1 = F, Ie.y1 = X, Ie.x2 = R, Ie.y2 = z, Ie.w = R - F, Ie.h = z - X, rr(e, F, X, R, z), rr(i.labelBounds.all, F, X, R, z);
        }
        return e;
      }
    }, nd = function(e, r) {
      var a = e._private.cy, n = a.styleEnabled(), i = a.headless(), s = Ut(), o = e._private, l = e.isNode(), u = e.isEdge(), f, h, c, v, d, g, y = o.rstyle, p = l && n ? e.pstyle("bounds-expansion").pfValue : [0], m = function(Ve) {
        return Ve.pstyle("display").value !== "none";
      }, b = !n || m(e) && (!u || m(e.source()) && m(e.target()));
      if (b) {
        var E = 0, M = 0;
        n && r.includeOverlays && (E = e.pstyle("overlay-opacity").value, E !== 0 && (M = e.pstyle("overlay-padding").value));
        var O = 0, x = 0;
        n && r.includeUnderlays && (O = e.pstyle("underlay-opacity").value, O !== 0 && (x = e.pstyle("underlay-padding").value));
        var I = Math.max(M, x), C = 0, B = 0;
        if (n && (C = e.pstyle("width").pfValue, B = C / 2), l && r.includeNodes) {
          var F = e.position();
          d = F.x, g = F.y;
          var R = e.outerWidth(), X = R / 2, z = e.outerHeight(), re = z / 2;
          f = d - X, h = d + X, c = g - re, v = g + re, rr(s, f, c, h, v);
        } else if (u && r.includeEdges)
          if (n && !i) {
            var W = e.pstyle("curve-style").strValue;
            if (f = Math.min(y.srcX, y.midX, y.tgtX), h = Math.max(y.srcX, y.midX, y.tgtX), c = Math.min(y.srcY, y.midY, y.tgtY), v = Math.max(y.srcY, y.midY, y.tgtY), f -= B, h += B, c -= B, v += B, rr(s, f, c, h, v), W === "haystack") {
              var Z = y.haystackPts;
              if (Z && Z.length === 2) {
                if (f = Z[0].x, c = Z[0].y, h = Z[1].x, v = Z[1].y, f > h) {
                  var ie = f;
                  f = h, h = ie;
                }
                if (c > v) {
                  var oe = c;
                  c = v, v = oe;
                }
                rr(s, f - B, c - B, h + B, v + B);
              }
            } else if (W === "bezier" || W === "unbundled-bezier" || W === "segments" || W === "taxi") {
              var ge;
              switch (W) {
                case "bezier":
                case "unbundled-bezier":
                  ge = y.bezierPts;
                  break;
                case "segments":
                case "taxi":
                  ge = y.linePts;
                  break;
              }
              if (ge != null)
                for (var se = 0; se < ge.length; se++) {
                  var de = ge[se];
                  f = de.x - B, h = de.x + B, c = de.y - B, v = de.y + B, rr(s, f, c, h, v);
                }
            }
          } else {
            var we = e.source(), Te = we.position(), Ee = e.target(), ye = Ee.position();
            if (f = Te.x, h = ye.x, c = Te.y, v = ye.y, f > h) {
              var ae = f;
              f = h, h = ae;
            }
            if (c > v) {
              var xe = c;
              c = v, v = xe;
            }
            f -= B, h += B, c -= B, v += B, rr(s, f, c, h, v);
          }
        if (n && r.includeEdges && u && (On(s, e, "mid-source"), On(s, e, "mid-target"), On(s, e, "source"), On(s, e, "target")), n) {
          var Ce = e.pstyle("ghost").value === "yes";
          if (Ce) {
            var Oe = e.pstyle("ghost-offset-x").pfValue, Ie = e.pstyle("ghost-offset-y").pfValue;
            rr(s, s.x1 + Oe, s.y1 + Ie, s.x2 + Oe, s.y2 + Ie);
          }
        }
        var He = o.bodyBounds = o.bodyBounds || {};
        ws(He, s), fi(He, p), yn(He, 1), n && (f = s.x1, h = s.x2, c = s.y1, v = s.y2, rr(s, f - I, c - I, h + I, v + I));
        var qe = o.overlayBounds = o.overlayBounds || {};
        ws(qe, s), fi(qe, p), yn(qe, 1);
        var Re = o.labelBounds = o.labelBounds || {};
        Re.all != null ? Cf(Re.all) : Re.all = Ut(), n && r.includeLabels && (r.includeMainLabels && Oi(s, e, null), u && (r.includeSourceLabels && Oi(s, e, "source"), r.includeTargetLabels && Oi(s, e, "target")));
      }
      return s.x1 = Zt(s.x1), s.y1 = Zt(s.y1), s.x2 = Zt(s.x2), s.y2 = Zt(s.y2), s.w = Zt(s.x2 - s.x1), s.h = Zt(s.y2 - s.y1), s.w > 0 && s.h > 0 && b && (fi(s, p), yn(s, 1)), s;
    }, mo = function(e) {
      var r = 0, a = function(s) {
        return (s ? 1 : 0) << r++;
      }, n = 0;
      return n += a(e.incudeNodes), n += a(e.includeEdges), n += a(e.includeLabels), n += a(e.includeMainLabels), n += a(e.includeSourceLabels), n += a(e.includeTargetLabels), n += a(e.includeOverlays), n;
    }, bo = function(e) {
      if (e.isEdge()) {
        var r = e.source().position(), a = e.target().position(), n = function(s) {
          return Math.round(s);
        };
        return Yl([n(r.x), n(r.y), n(a.x), n(a.y)]);
      } else
        return 0;
    }, Eo = function(e, r) {
      var a = e._private, n, i = e.isEdge(), s = r == null ? wo : mo(r), o = s === wo, l = bo(e), u = a.bbCachePosKey === l, f = r.useCache && u, h = function(g) {
        return g._private.bbCache == null || g._private.styleDirty;
      }, c = !f || h(e) || i && h(e.source()) || h(e.target());
      if (c ? (u || e.recalculateRenderedStyle(f), n = nd(e, _a), a.bbCache = n, a.bbCachePosKey = l) : n = a.bbCache, !o) {
        var v = e.isNode();
        n = Ut(), (r.includeNodes && v || r.includeEdges && !v) && (r.includeOverlays ? Gr(n, a.overlayBounds) : Gr(n, a.bodyBounds)), r.includeLabels && (r.includeMainLabels && (!i || r.includeSourceLabels && r.includeTargetLabels) ? Gr(n, a.labelBounds.all) : (r.includeMainLabels && Gr(n, a.labelBounds.mainRot), r.includeSourceLabels && Gr(n, a.labelBounds.sourceRot), r.includeTargetLabels && Gr(n, a.labelBounds.targetRot))), n.w = n.x2 - n.x1, n.h = n.y2 - n.y1;
      }
      return n;
    }, _a = {
      includeNodes: !0,
      includeEdges: !0,
      includeLabels: !0,
      includeMainLabels: !0,
      includeSourceLabels: !0,
      includeTargetLabels: !0,
      includeOverlays: !0,
      includeUnderlays: !0,
      useCache: !0
    }, wo = mo(_a), xo = Lt(_a);
    Ar.boundingBox = function(t) {
      var e;
      if (this.length === 1 && this[0]._private.bbCache != null && !this[0]._private.styleDirty && (t === void 0 || t.useCache === void 0 || t.useCache === !0))
        t === void 0 ? t = _a : t = xo(t), e = Eo(this[0], t);
      else {
        e = Ut(), t = t || _a;
        var r = xo(t), a = this, n = a.cy(), i = n.styleEnabled();
        if (i)
          for (var s = 0; s < a.length; s++) {
            var o = a[s], l = o._private, u = bo(o), f = l.bbCachePosKey === u, h = r.useCache && f && !l.styleDirty;
            o.recalculateRenderedStyle(h);
          }
        this.updateCompoundBounds(!t.useCache);
        for (var c = 0; c < a.length; c++) {
          var v = a[c];
          Gr(e, Eo(v, r));
        }
      }
      return e.x1 = Zt(e.x1), e.y1 = Zt(e.y1), e.x2 = Zt(e.x2), e.y2 = Zt(e.y2), e.w = Zt(e.x2 - e.x1), e.h = Zt(e.y2 - e.y1), e;
    }, Ar.dirtyBoundingBoxCache = function() {
      for (var t = 0; t < this.length; t++) {
        var e = this[t]._private;
        e.bbCache = null, e.bbCachePosKey = null, e.bodyBounds = null, e.overlayBounds = null, e.labelBounds.all = null, e.labelBounds.source = null, e.labelBounds.target = null, e.labelBounds.main = null, e.labelBounds.sourceRot = null, e.labelBounds.targetRot = null, e.labelBounds.mainRot = null, e.arrowBounds.source = null, e.arrowBounds.target = null, e.arrowBounds["mid-source"] = null, e.arrowBounds["mid-target"] = null;
      }
      return this.emitAndNotify("bounds"), this;
    }, Ar.boundingBoxAt = function(t) {
      var e = this.nodes(), r = this.cy(), a = r.hasCompoundNodes(), n = r.collection();
      if (a && (n = e.filter(function(u) {
        return u.isParent();
      }), e = e.not(n)), S(t)) {
        var i = t;
        t = function() {
          return i;
        };
      }
      var s = function(f, h) {
        return f._private.bbAtOldPos = t(f, h);
      }, o = function(f) {
        return f._private.bbAtOldPos;
      };
      r.startBatch(), e.forEach(s).silentPositions(t), a && (n.dirtyCompoundBoundsCache(), n.dirtyBoundingBoxCache(), n.updateCompoundBounds(!0));
      var l = Tf(this.boundingBox({
        useCache: !1
      }));
      return e.silentPositions(o), a && (n.dirtyCompoundBoundsCache(), n.dirtyBoundingBoxCache(), n.updateCompoundBounds(!0)), r.endBatch(), l;
    }, ca.boundingbox = ca.bb = ca.boundingBox, ca.renderedBoundingbox = ca.renderedBoundingBox;
    var id = Ar, Ua, Ya;
    Ua = Ya = {};
    var To = function(e) {
      e.uppercaseName = kt(e.name), e.autoName = "auto" + e.uppercaseName, e.labelName = "label" + e.uppercaseName, e.outerName = "outer" + e.uppercaseName, e.uppercaseOuterName = kt(e.outerName), Ua[e.name] = function() {
        var a = this[0], n = a._private, i = n.cy, s = i._private.styleEnabled;
        if (a)
          if (s) {
            if (a.isParent())
              return a.updateCompoundBounds(), n[e.autoName] || 0;
            var o = a.pstyle(e.name);
            switch (o.strValue) {
              case "label":
                return a.recalculateRenderedStyle(), n.rstyle[e.labelName] || 0;
              default:
                return o.pfValue;
            }
          } else
            return 1;
      }, Ua["outer" + e.uppercaseName] = function() {
        var a = this[0], n = a._private, i = n.cy, s = i._private.styleEnabled;
        if (a)
          if (s) {
            var o = a[e.name](), l = a.pstyle("border-width").pfValue, u = 2 * a.padding();
            return o + l + u;
          } else
            return 1;
      }, Ua["rendered" + e.uppercaseName] = function() {
        var a = this[0];
        if (a) {
          var n = a[e.name]();
          return n * this.cy().zoom();
        }
      }, Ua["rendered" + e.uppercaseOuterName] = function() {
        var a = this[0];
        if (a) {
          var n = a[e.outerName]();
          return n * this.cy().zoom();
        }
      };
    };
    To({
      name: "width"
    }), To({
      name: "height"
    }), Ya.padding = function() {
      var t = this[0], e = t._private;
      return t.isParent() ? (t.updateCompoundBounds(), e.autoPadding !== void 0 ? e.autoPadding : t.pstyle("padding").pfValue) : t.pstyle("padding").pfValue;
    }, Ya.paddedHeight = function() {
      var t = this[0];
      return t.height() + 2 * t.padding();
    }, Ya.paddedWidth = function() {
      var t = this[0];
      return t.width() + 2 * t.padding();
    };
    var sd = Ya, od = function(e, r) {
      if (e.isEdge())
        return r(e);
    }, ud = function(e, r) {
      if (e.isEdge()) {
        var a = e.cy();
        return gn(r(e), a.zoom(), a.pan());
      }
    }, ld = function(e, r) {
      if (e.isEdge()) {
        var a = e.cy(), n = a.pan(), i = a.zoom();
        return r(e).map(function(s) {
          return gn(s, i, n);
        });
      }
    }, fd = function(e) {
      return e.renderer().getControlPoints(e);
    }, hd = function(e) {
      return e.renderer().getSegmentPoints(e);
    }, cd = function(e) {
      return e.renderer().getSourceEndpoint(e);
    }, vd = function(e) {
      return e.renderer().getTargetEndpoint(e);
    }, dd = function(e) {
      return e.renderer().getEdgeMidpoint(e);
    }, Co = {
      controlPoints: {
        get: fd,
        mult: !0
      },
      segmentPoints: {
        get: hd,
        mult: !0
      },
      sourceEndpoint: {
        get: cd
      },
      targetEndpoint: {
        get: vd
      },
      midpoint: {
        get: dd
      }
    }, gd = function(e) {
      return "rendered" + e[0].toUpperCase() + e.substr(1);
    }, pd = Object.keys(Co).reduce(function(t, e) {
      var r = Co[e], a = gd(e);
      return t[e] = function() {
        return od(this, r.get);
      }, r.mult ? t[a] = function() {
        return ld(this, r.get);
      } : t[a] = function() {
        return ud(this, r.get);
      }, t;
    }, {}), yd = Ue({}, ad, id, sd, pd);
    /*!
    	  Event object based on jQuery events, MIT license
    
    	  https://jquery.org/license/
    	  https://tldrlegal.com/license/mit-license
    	  https://github.com/jquery/jquery/blob/master/src/event.js
    	  */
    var Do = function(e, r) {
      this.recycle(e, r);
    };
    function Ha() {
      return !1;
    }
    function Nn() {
      return !0;
    }
    Do.prototype = {
      instanceString: function() {
        return "event";
      },
      recycle: function(e, r) {
        if (this.isImmediatePropagationStopped = this.isPropagationStopped = this.isDefaultPrevented = Ha, e != null && e.preventDefault ? (this.type = e.type, this.isDefaultPrevented = e.defaultPrevented ? Nn : Ha) : e != null && e.type ? r = e : this.type = e, r != null && (this.originalEvent = r.originalEvent, this.type = r.type != null ? r.type : this.type, this.cy = r.cy, this.target = r.target, this.position = r.position, this.renderedPosition = r.renderedPosition, this.namespace = r.namespace, this.layout = r.layout), this.cy != null && this.position != null && this.renderedPosition == null) {
          var a = this.position, n = this.cy.zoom(), i = this.cy.pan();
          this.renderedPosition = {
            x: a.x * n + i.x,
            y: a.y * n + i.y
          };
        }
        this.timeStamp = e && e.timeStamp || Date.now();
      },
      preventDefault: function() {
        this.isDefaultPrevented = Nn;
        var e = this.originalEvent;
        e && e.preventDefault && e.preventDefault();
      },
      stopPropagation: function() {
        this.isPropagationStopped = Nn;
        var e = this.originalEvent;
        e && e.stopPropagation && e.stopPropagation();
      },
      stopImmediatePropagation: function() {
        this.isImmediatePropagationStopped = Nn, this.stopPropagation();
      },
      isDefaultPrevented: Ha,
      isPropagationStopped: Ha,
      isImmediatePropagationStopped: Ha
    };
    var So = /^([^.]+)(\.(?:[^.]+))?$/, md = ".*", Lo = {
      qualifierCompare: function(e, r) {
        return e === r;
      },
      eventMatches: function() {
        return !0;
      },
      addEventFields: function() {
      },
      callbackContext: function(e) {
        return e;
      },
      beforeEmit: function() {
      },
      afterEmit: function() {
      },
      bubble: function() {
        return !1;
      },
      parent: function() {
        return null;
      },
      context: null
    }, Ao = Object.keys(Lo), bd = {};
    function Mn() {
      for (var t = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : bd, e = arguments.length > 1 ? arguments[1] : void 0, r = 0; r < Ao.length; r++) {
        var a = Ao[r];
        this[a] = t[a] || Lo[a];
      }
      this.context = e || this.context, this.listeners = [], this.emitting = 0;
    }
    var Or = Mn.prototype, Oo = function(e, r, a, n, i, s, o) {
      H(n) && (i = n, n = null), o && (s == null ? s = o : s = Ue({}, s, o));
      for (var l = te(a) ? a : a.split(/\s+/), u = 0; u < l.length; u++) {
        var f = l[u];
        if (!Pe(f)) {
          var h = f.match(So);
          if (h) {
            var c = h[1], v = h[2] ? h[2] : null, d = r(e, f, c, v, n, i, s);
            if (d === !1)
              break;
          }
        }
      }
    }, No = function(e, r) {
      return e.addEventFields(e.context, r), new Do(r.type, r);
    }, Ed = function(e, r, a) {
      if (ct(a)) {
        r(e, a);
        return;
      } else if (S(a)) {
        r(e, No(e, a));
        return;
      }
      for (var n = te(a) ? a : a.split(/\s+/), i = 0; i < n.length; i++) {
        var s = n[i];
        if (!Pe(s)) {
          var o = s.match(So);
          if (o) {
            var l = o[1], u = o[2] ? o[2] : null, f = No(e, {
              type: l,
              namespace: u,
              target: e.context
            });
            r(e, f);
          }
        }
      }
    };
    Or.on = Or.addListener = function(t, e, r, a, n) {
      return Oo(this, function(i, s, o, l, u, f, h) {
        H(f) && i.listeners.push({
          event: s,
          // full event string
          callback: f,
          // callback to run
          type: o,
          // the event type (e.g. 'click')
          namespace: l,
          // the event namespace (e.g. ".foo")
          qualifier: u,
          // a restriction on whether to match this emitter
          conf: h
          // additional configuration
        });
      }, t, e, r, a, n), this;
    }, Or.one = function(t, e, r, a) {
      return this.on(t, e, r, a, {
        one: !0
      });
    }, Or.removeListener = Or.off = function(t, e, r, a) {
      var n = this;
      this.emitting !== 0 && (this.listeners = Kl(this.listeners));
      for (var i = this.listeners, s = function(u) {
        var f = i[u];
        Oo(n, function(h, c, v, d, g, y) {
          if ((f.type === v || t === "*") && (!d && f.namespace !== ".*" || f.namespace === d) && (!g || h.qualifierCompare(f.qualifier, g)) && (!y || f.callback === y))
            return i.splice(u, 1), !1;
        }, t, e, r, a);
      }, o = i.length - 1; o >= 0; o--)
        s(o);
      return this;
    }, Or.removeAllListeners = function() {
      return this.removeListener("*");
    }, Or.emit = Or.trigger = function(t, e, r) {
      var a = this.listeners, n = a.length;
      return this.emitting++, te(e) || (e = [e]), Ed(this, function(i, s) {
        r != null && (a = [{
          event: s.event,
          type: s.type,
          namespace: s.namespace,
          callback: r
        }], n = a.length);
        for (var o = function(f) {
          var h = a[f];
          if (h.type === s.type && (!h.namespace || h.namespace === s.namespace || h.namespace === md) && i.eventMatches(i.context, h, s)) {
            var c = [s];
            e != null && Ql(c, e), i.beforeEmit(i.context, h, s), h.conf && h.conf.one && (i.listeners = i.listeners.filter(function(g) {
              return g !== h;
            }));
            var v = i.callbackContext(i.context, h, s), d = h.callback.apply(v, c);
            i.afterEmit(i.context, h, s), d === !1 && (s.stopPropagation(), s.preventDefault());
          }
        }, l = 0; l < n; l++)
          o(l);
        i.bubble(i.context) && !s.isPropagationStopped() && i.parent(i.context).emit(s, e);
      }, t), this.emitting--, this;
    };
    var wd = {
      qualifierCompare: function(e, r) {
        return e == null || r == null ? e == null && r == null : e.sameText(r);
      },
      eventMatches: function(e, r, a) {
        var n = r.qualifier;
        return n != null ? e !== a.target && Ae(a.target) && n.matches(a.target) : !0;
      },
      addEventFields: function(e, r) {
        r.cy = e.cy(), r.target = e;
      },
      callbackContext: function(e, r, a) {
        return r.qualifier != null ? a.target : e;
      },
      beforeEmit: function(e, r) {
        r.conf && r.conf.once && r.conf.onceCollection.removeListener(r.event, r.qualifier, r.callback);
      },
      bubble: function() {
        return !0;
      },
      parent: function(e) {
        return e.isChild() ? e.parent() : e.cy();
      }
    }, In = function(e) {
      return ee(e) ? new Dr(e) : e;
    }, Mo = {
      createEmitter: function() {
        for (var e = 0; e < this.length; e++) {
          var r = this[e], a = r._private;
          a.emitter || (a.emitter = new Mn(wd, r));
        }
        return this;
      },
      emitter: function() {
        return this._private.emitter;
      },
      on: function(e, r, a) {
        for (var n = In(r), i = 0; i < this.length; i++) {
          var s = this[i];
          s.emitter().on(e, n, a);
        }
        return this;
      },
      removeListener: function(e, r, a) {
        for (var n = In(r), i = 0; i < this.length; i++) {
          var s = this[i];
          s.emitter().removeListener(e, n, a);
        }
        return this;
      },
      removeAllListeners: function() {
        for (var e = 0; e < this.length; e++) {
          var r = this[e];
          r.emitter().removeAllListeners();
        }
        return this;
      },
      one: function(e, r, a) {
        for (var n = In(r), i = 0; i < this.length; i++) {
          var s = this[i];
          s.emitter().one(e, n, a);
        }
        return this;
      },
      once: function(e, r, a) {
        for (var n = In(r), i = 0; i < this.length; i++) {
          var s = this[i];
          s.emitter().on(e, n, a, {
            once: !0,
            onceCollection: this
          });
        }
      },
      emit: function(e, r) {
        for (var a = 0; a < this.length; a++) {
          var n = this[a];
          n.emitter().emit(e, r);
        }
        return this;
      },
      emitAndNotify: function(e, r) {
        if (this.length !== 0)
          return this.cy().notify(e, this), this.emit(e, r), this;
      }
    };
    ht.eventAliasesOn(Mo);
    var Io = {
      nodes: function(e) {
        return this.filter(function(r) {
          return r.isNode();
        }).filter(e);
      },
      edges: function(e) {
        return this.filter(function(r) {
          return r.isEdge();
        }).filter(e);
      },
      // internal helper to get nodes and edges as separate collections with single iteration over elements
      byGroup: function() {
        for (var e = this.spawn(), r = this.spawn(), a = 0; a < this.length; a++) {
          var n = this[a];
          n.isNode() ? e.push(n) : r.push(n);
        }
        return {
          nodes: e,
          edges: r
        };
      },
      filter: function(e, r) {
        if (e === void 0)
          return this;
        if (ee(e) || pe(e))
          return new Dr(e).filter(this);
        if (H(e)) {
          for (var a = this.spawn(), n = this, i = 0; i < n.length; i++) {
            var s = n[i], o = r ? e.apply(r, [s, i, n]) : e(s, i, n);
            o && a.push(s);
          }
          return a;
        }
        return this.spawn();
      },
      not: function(e) {
        if (e) {
          ee(e) && (e = this.filter(e));
          for (var r = this.spawn(), a = 0; a < this.length; a++) {
            var n = this[a], i = e.has(n);
            i || r.push(n);
          }
          return r;
        } else
          return this;
      },
      absoluteComplement: function() {
        var e = this.cy();
        return e.mutableElements().not(this);
      },
      intersect: function(e) {
        if (ee(e)) {
          var r = e;
          return this.filter(r);
        }
        for (var a = this.spawn(), n = this, i = e, s = this.length < e.length, o = s ? n : i, l = s ? i : n, u = 0; u < o.length; u++) {
          var f = o[u];
          l.has(f) && a.push(f);
        }
        return a;
      },
      xor: function(e) {
        var r = this._private.cy;
        ee(e) && (e = r.$(e));
        var a = this.spawn(), n = this, i = e, s = function(l, u) {
          for (var f = 0; f < l.length; f++) {
            var h = l[f], c = h._private.data.id, v = u.hasElementWithId(c);
            v || a.push(h);
          }
        };
        return s(n, i), s(i, n), a;
      },
      diff: function(e) {
        var r = this._private.cy;
        ee(e) && (e = r.$(e));
        var a = this.spawn(), n = this.spawn(), i = this.spawn(), s = this, o = e, l = function(f, h, c) {
          for (var v = 0; v < f.length; v++) {
            var d = f[v], g = d._private.data.id, y = h.hasElementWithId(g);
            y ? i.merge(d) : c.push(d);
          }
        };
        return l(s, o, a), l(o, s, n), {
          left: a,
          right: n,
          both: i
        };
      },
      add: function(e) {
        var r = this._private.cy;
        if (!e)
          return this;
        if (ee(e)) {
          var a = e;
          e = r.mutableElements().filter(a);
        }
        for (var n = this.spawnSelf(), i = 0; i < e.length; i++) {
          var s = e[i], o = !this.has(s);
          o && n.push(s);
        }
        return n;
      },
      // in place merge on calling collection
      merge: function(e) {
        var r = this._private, a = r.cy;
        if (!e)
          return this;
        if (e && ee(e)) {
          var n = e;
          e = a.mutableElements().filter(n);
        }
        for (var i = r.map, s = 0; s < e.length; s++) {
          var o = e[s], l = o._private.data.id, u = !i.has(l);
          if (u) {
            var f = this.length++;
            this[f] = o, i.set(l, {
              ele: o,
              index: f
            });
          }
        }
        return this;
      },
      unmergeAt: function(e) {
        var r = this[e], a = r.id(), n = this._private, i = n.map;
        this[e] = void 0, i.delete(a);
        var s = e === this.length - 1;
        if (this.length > 1 && !s) {
          var o = this.length - 1, l = this[o], u = l._private.data.id;
          this[o] = void 0, this[e] = l, i.set(u, {
            ele: l,
            index: e
          });
        }
        return this.length--, this;
      },
      // remove single ele in place in calling collection
      unmergeOne: function(e) {
        e = e[0];
        var r = this._private, a = e._private.data.id, n = r.map, i = n.get(a);
        if (!i)
          return this;
        var s = i.index;
        return this.unmergeAt(s), this;
      },
      // remove eles in place on calling collection
      unmerge: function(e) {
        var r = this._private.cy;
        if (!e)
          return this;
        if (e && ee(e)) {
          var a = e;
          e = r.mutableElements().filter(a);
        }
        for (var n = 0; n < e.length; n++)
          this.unmergeOne(e[n]);
        return this;
      },
      unmergeBy: function(e) {
        for (var r = this.length - 1; r >= 0; r--) {
          var a = this[r];
          e(a) && this.unmergeAt(r);
        }
        return this;
      },
      map: function(e, r) {
        for (var a = [], n = this, i = 0; i < n.length; i++) {
          var s = n[i], o = r ? e.apply(r, [s, i, n]) : e(s, i, n);
          a.push(o);
        }
        return a;
      },
      reduce: function(e, r) {
        for (var a = r, n = this, i = 0; i < n.length; i++)
          a = e(a, n[i], i, n);
        return a;
      },
      max: function(e, r) {
        for (var a = -1 / 0, n, i = this, s = 0; s < i.length; s++) {
          var o = i[s], l = r ? e.apply(r, [o, s, i]) : e(o, s, i);
          l > a && (a = l, n = o);
        }
        return {
          value: a,
          ele: n
        };
      },
      min: function(e, r) {
        for (var a = 1 / 0, n, i = this, s = 0; s < i.length; s++) {
          var o = i[s], l = r ? e.apply(r, [o, s, i]) : e(o, s, i);
          l < a && (a = l, n = o);
        }
        return {
          value: a,
          ele: n
        };
      }
    }, st = Io;
    st.u = st["|"] = st["+"] = st.union = st.or = st.add, st["\\"] = st["!"] = st["-"] = st.difference = st.relativeComplement = st.subtract = st.not, st.n = st["&"] = st["."] = st.and = st.intersection = st.intersect, st["^"] = st["(+)"] = st["(-)"] = st.symmetricDifference = st.symdiff = st.xor, st.fnFilter = st.filterFn = st.stdFilter = st.filter, st.complement = st.abscomp = st.absoluteComplement;
    var xd = {
      isNode: function() {
        return this.group() === "nodes";
      },
      isEdge: function() {
        return this.group() === "edges";
      },
      isLoop: function() {
        return this.isEdge() && this.source()[0] === this.target()[0];
      },
      isSimple: function() {
        return this.isEdge() && this.source()[0] !== this.target()[0];
      },
      group: function() {
        var e = this[0];
        if (e)
          return e._private.group;
      }
    }, Ro = function(e, r) {
      var a = e.cy(), n = a.hasCompoundNodes();
      function i(f) {
        var h = f.pstyle("z-compound-depth");
        return h.value === "auto" ? n ? f.zDepth() : 0 : h.value === "bottom" ? -1 : h.value === "top" ? ii : 0;
      }
      var s = i(e) - i(r);
      if (s !== 0)
        return s;
      function o(f) {
        var h = f.pstyle("z-index-compare");
        return h.value === "auto" && f.isNode() ? 1 : 0;
      }
      var l = o(e) - o(r);
      if (l !== 0)
        return l;
      var u = e.pstyle("z-index").value - r.pstyle("z-index").value;
      return u !== 0 ? u : e.poolIndex() - r.poolIndex();
    }, Rn = {
      forEach: function(e, r) {
        if (H(e))
          for (var a = this.length, n = 0; n < a; n++) {
            var i = this[n], s = r ? e.apply(r, [i, n, this]) : e(i, n, this);
            if (s === !1)
              break;
          }
        return this;
      },
      toArray: function() {
        for (var e = [], r = 0; r < this.length; r++)
          e.push(this[r]);
        return e;
      },
      slice: function(e, r) {
        var a = [], n = this.length;
        r == null && (r = n), e == null && (e = 0), e < 0 && (e = n + e), r < 0 && (r = n + r);
        for (var i = e; i >= 0 && i < r && i < n; i++)
          a.push(this[i]);
        return this.spawn(a);
      },
      size: function() {
        return this.length;
      },
      eq: function(e) {
        return this[e] || this.spawn();
      },
      first: function() {
        return this[0] || this.spawn();
      },
      last: function() {
        return this[this.length - 1] || this.spawn();
      },
      empty: function() {
        return this.length === 0;
      },
      nonempty: function() {
        return !this.empty();
      },
      sort: function(e) {
        if (!H(e))
          return this;
        var r = this.toArray().sort(e);
        return this.spawn(r);
      },
      sortByZIndex: function() {
        return this.sort(Ro);
      },
      zDepth: function() {
        var e = this[0];
        if (e) {
          var r = e._private, a = r.group;
          if (a === "nodes") {
            var n = r.data.parent ? e.parents().size() : 0;
            return e.isParent() ? n : ii - 1;
          } else {
            var i = r.source, s = r.target, o = i.zDepth(), l = s.zDepth();
            return Math.max(o, l, 0);
          }
        }
      }
    };
    Rn.each = Rn.forEach;
    var Td = function() {
      var e = "undefined", r = (typeof Symbol > "u" ? "undefined" : Q(Symbol)) != e && Q(Symbol.iterator) != e;
      r && (Rn[Symbol.iterator] = function() {
        var a = this, n = {
          value: void 0,
          done: !1
        }, i = 0, s = this.length;
        return T({
          next: function() {
            return i < s ? n.value = a[i++] : (n.value = void 0, n.done = !0), n;
          }
        }, Symbol.iterator, function() {
          return this;
        });
      });
    };
    Td();
    var Cd = Lt({
      nodeDimensionsIncludeLabels: !1
    }), kn = {
      // Calculates and returns node dimensions { x, y } based on options given
      layoutDimensions: function(e) {
        e = Cd(e);
        var r;
        if (!this.takesUpSpace())
          r = {
            w: 0,
            h: 0
          };
        else if (e.nodeDimensionsIncludeLabels) {
          var a = this.boundingBox();
          r = {
            w: a.w,
            h: a.h
          };
        } else
          r = {
            w: this.outerWidth(),
            h: this.outerHeight()
          };
        return (r.w === 0 || r.h === 0) && (r.w = r.h = 1), r;
      },
      // using standard layout options, apply position function (w/ or w/o animation)
      layoutPositions: function(e, r, a) {
        var n = this.nodes().filter(function(M) {
          return !M.isParent();
        }), i = this.cy(), s = r.eles, o = function(O) {
          return O.id();
        }, l = nt(a, o);
        e.emit({
          type: "layoutstart",
          layout: e
        }), e.animations = [];
        var u = function(O, x, I) {
          var C = {
            x: x.x1 + x.w / 2,
            y: x.y1 + x.h / 2
          }, B = {
            // scale from center of bounding box (not necessarily 0,0)
            x: (I.x - C.x) * O,
            y: (I.y - C.y) * O
          };
          return {
            x: C.x + B.x,
            y: C.y + B.y
          };
        }, f = r.spacingFactor && r.spacingFactor !== 1, h = function() {
          if (!f)
            return null;
          for (var O = Ut(), x = 0; x < n.length; x++) {
            var I = n[x], C = l(I, x);
            Sf(O, C.x, C.y);
          }
          return O;
        }, c = h(), v = nt(function(M, O) {
          var x = l(M, O);
          if (f) {
            var I = Math.abs(r.spacingFactor);
            x = u(I, c, x);
          }
          return r.transform != null && (x = r.transform(M, x)), x;
        }, o);
        if (r.animate) {
          for (var d = 0; d < n.length; d++) {
            var g = n[d], y = v(g, d), p = r.animateFilter == null || r.animateFilter(g, d);
            if (p) {
              var m = g.animation({
                position: y,
                duration: r.animationDuration,
                easing: r.animationEasing
              });
              e.animations.push(m);
            } else
              g.position(y);
          }
          if (r.fit) {
            var b = i.animation({
              fit: {
                boundingBox: s.boundingBoxAt(v),
                padding: r.padding
              },
              duration: r.animationDuration,
              easing: r.animationEasing
            });
            e.animations.push(b);
          } else if (r.zoom !== void 0 && r.pan !== void 0) {
            var E = i.animation({
              zoom: r.zoom,
              pan: r.pan,
              duration: r.animationDuration,
              easing: r.animationEasing
            });
            e.animations.push(E);
          }
          e.animations.forEach(function(M) {
            return M.play();
          }), e.one("layoutready", r.ready), e.emit({
            type: "layoutready",
            layout: e
          }), ia.all(e.animations.map(function(M) {
            return M.promise();
          })).then(function() {
            e.one("layoutstop", r.stop), e.emit({
              type: "layoutstop",
              layout: e
            });
          });
        } else
          n.positions(v), r.fit && i.fit(r.eles, r.padding), r.zoom != null && i.zoom(r.zoom), r.pan && i.pan(r.pan), e.one("layoutready", r.ready), e.emit({
            type: "layoutready",
            layout: e
          }), e.one("layoutstop", r.stop), e.emit({
            type: "layoutstop",
            layout: e
          });
        return this;
      },
      layout: function(e) {
        var r = this.cy();
        return r.makeLayout(Ue({}, e, {
          eles: this
        }));
      }
    };
    kn.createLayout = kn.makeLayout = kn.layout;
    function ko(t, e, r) {
      var a = r._private, n = a.styleCache = a.styleCache || [], i;
      return (i = n[t]) != null || (i = n[t] = e(r)), i;
    }
    function Pn(t, e) {
      return t = kr(t), function(a) {
        return ko(t, e, a);
      };
    }
    function Bn(t, e) {
      t = kr(t);
      var r = function(n) {
        return e.call(n);
      };
      return function() {
        var n = this[0];
        if (n)
          return ko(t, r, n);
      };
    }
    var At = {
      recalculateRenderedStyle: function(e) {
        var r = this.cy(), a = r.renderer(), n = r.styleEnabled();
        return a && n && a.recalculateRenderedStyle(this, e), this;
      },
      dirtyStyleCache: function() {
        var e = this.cy(), r = function(i) {
          return i._private.styleCache = null;
        };
        if (e.hasCompoundNodes()) {
          var a;
          a = this.spawnSelf().merge(this.descendants()).merge(this.parents()), a.merge(a.connectedEdges()), a.forEach(r);
        } else
          this.forEach(function(n) {
            r(n), n.connectedEdges().forEach(r);
          });
        return this;
      },
      // fully updates (recalculates) the style for the elements
      updateStyle: function(e) {
        var r = this._private.cy;
        if (!r.styleEnabled())
          return this;
        if (r.batching()) {
          var a = r._private.batchStyleEles;
          return a.merge(this), this;
        }
        var n = r.hasCompoundNodes(), i = this;
        e = !!(e || e === void 0), n && (i = this.spawnSelf().merge(this.descendants()).merge(this.parents()));
        var s = i;
        return e ? s.emitAndNotify("style") : s.emit("style"), i.forEach(function(o) {
          return o._private.styleDirty = !0;
        }), this;
      },
      // private: clears dirty flag and recalculates style
      cleanStyle: function() {
        var e = this.cy();
        if (e.styleEnabled())
          for (var r = 0; r < this.length; r++) {
            var a = this[r];
            a._private.styleDirty && (a._private.styleDirty = !1, e.style().apply(a));
          }
      },
      // get the internal parsed style object for the specified property
      parsedStyle: function(e) {
        var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !0, a = this[0], n = a.cy();
        if (n.styleEnabled() && a) {
          this.cleanStyle();
          var i = a._private.style[e];
          return i ?? (r ? n.style().getDefaultProperty(e) : null);
        }
      },
      numericStyle: function(e) {
        var r = this[0];
        if (r.cy().styleEnabled() && r) {
          var a = r.pstyle(e);
          return a.pfValue !== void 0 ? a.pfValue : a.value;
        }
      },
      numericStyleUnits: function(e) {
        var r = this[0];
        if (r.cy().styleEnabled() && r)
          return r.pstyle(e).units;
      },
      // get the specified css property as a rendered value (i.e. on-screen value)
      // or get the whole rendered style if no property specified (NB doesn't allow setting)
      renderedStyle: function(e) {
        var r = this.cy();
        if (!r.styleEnabled())
          return this;
        var a = this[0];
        if (a)
          return r.style().getRenderedStyle(a, e);
      },
      // read the calculated css style of the element or override the style (via a bypass)
      style: function(e, r) {
        var a = this.cy();
        if (!a.styleEnabled())
          return this;
        var n = !1, i = a.style();
        if (S(e)) {
          var s = e;
          i.applyBypass(this, s, n), this.emitAndNotify("style");
        } else if (ee(e))
          if (r === void 0) {
            var o = this[0];
            return o ? i.getStylePropertyValue(o, e) : void 0;
          } else
            i.applyBypass(this, e, r, n), this.emitAndNotify("style");
        else if (e === void 0) {
          var l = this[0];
          return l ? i.getRawStyle(l) : void 0;
        }
        return this;
      },
      removeStyle: function(e) {
        var r = this.cy();
        if (!r.styleEnabled())
          return this;
        var a = !1, n = r.style(), i = this;
        if (e === void 0)
          for (var s = 0; s < i.length; s++) {
            var o = i[s];
            n.removeAllBypasses(o, a);
          }
        else {
          e = e.split(/\s+/);
          for (var l = 0; l < i.length; l++) {
            var u = i[l];
            n.removeBypasses(u, e, a);
          }
        }
        return this.emitAndNotify("style"), this;
      },
      show: function() {
        return this.css("display", "element"), this;
      },
      hide: function() {
        return this.css("display", "none"), this;
      },
      effectiveOpacity: function() {
        var e = this.cy();
        if (!e.styleEnabled())
          return 1;
        var r = e.hasCompoundNodes(), a = this[0];
        if (a) {
          var n = a._private, i = a.pstyle("opacity").value;
          if (!r)
            return i;
          var s = n.data.parent ? a.parents() : null;
          if (s)
            for (var o = 0; o < s.length; o++) {
              var l = s[o], u = l.pstyle("opacity").value;
              i = u * i;
            }
          return i;
        }
      },
      transparent: function() {
        var e = this.cy();
        if (!e.styleEnabled())
          return !1;
        var r = this[0], a = r.cy().hasCompoundNodes();
        if (r)
          return a ? r.effectiveOpacity() === 0 : r.pstyle("opacity").value === 0;
      },
      backgrounding: function() {
        var e = this.cy();
        if (!e.styleEnabled())
          return !1;
        var r = this[0];
        return !!r._private.backgrounding;
      }
    };
    function Ni(t, e) {
      var r = t._private, a = r.data.parent ? t.parents() : null;
      if (a)
        for (var n = 0; n < a.length; n++) {
          var i = a[n];
          if (!e(i))
            return !1;
        }
      return !0;
    }
    function Mi(t) {
      var e = t.ok, r = t.edgeOkViaNode || t.ok, a = t.parentOk || t.ok;
      return function() {
        var n = this.cy();
        if (!n.styleEnabled())
          return !0;
        var i = this[0], s = n.hasCompoundNodes();
        if (i) {
          var o = i._private;
          if (!e(i))
            return !1;
          if (i.isNode())
            return !s || Ni(i, a);
          var l = o.source, u = o.target;
          return r(l) && (!s || Ni(l, r)) && (l === u || r(u) && (!s || Ni(u, r)));
        }
      };
    }
    var va = Pn("eleTakesUpSpace", function(t) {
      return t.pstyle("display").value === "element" && t.width() !== 0 && (t.isNode() ? t.height() !== 0 : !0);
    });
    At.takesUpSpace = Bn("takesUpSpace", Mi({
      ok: va
    }));
    var Dd = Pn("eleInteractive", function(t) {
      return t.pstyle("events").value === "yes" && t.pstyle("visibility").value === "visible" && va(t);
    }), Sd = Pn("parentInteractive", function(t) {
      return t.pstyle("visibility").value === "visible" && va(t);
    });
    At.interactive = Bn("interactive", Mi({
      ok: Dd,
      parentOk: Sd,
      edgeOkViaNode: va
    })), At.noninteractive = function() {
      var t = this[0];
      if (t)
        return !t.interactive();
    };
    var Ld = Pn("eleVisible", function(t) {
      return t.pstyle("visibility").value === "visible" && t.pstyle("opacity").pfValue !== 0 && va(t);
    }), Ad = va;
    At.visible = Bn("visible", Mi({
      ok: Ld,
      edgeOkViaNode: Ad
    })), At.hidden = function() {
      var t = this[0];
      if (t)
        return !t.visible();
    }, At.isBundledBezier = Bn("isBundledBezier", function() {
      return this.cy().styleEnabled() ? !this.removed() && this.pstyle("curve-style").value === "bezier" && this.takesUpSpace() : !1;
    }), At.bypass = At.css = At.style, At.renderedCss = At.renderedStyle, At.removeBypass = At.removeCss = At.removeStyle, At.pstyle = At.parsedStyle;
    var Nr = {};
    function Po(t) {
      return function() {
        var e = arguments, r = [];
        if (e.length === 2) {
          var a = e[0], n = e[1];
          this.on(t.event, a, n);
        } else if (e.length === 1 && H(e[0])) {
          var i = e[0];
          this.on(t.event, i);
        } else if (e.length === 0 || e.length === 1 && te(e[0])) {
          for (var s = e.length === 1 ? e[0] : null, o = 0; o < this.length; o++) {
            var l = this[o], u = !t.ableField || l._private[t.ableField], f = l._private[t.field] != t.value;
            if (t.overrideAble) {
              var h = t.overrideAble(l);
              if (h !== void 0 && (u = h, !h))
                return this;
            }
            u && (l._private[t.field] = t.value, f && r.push(l));
          }
          var c = this.spawn(r);
          c.updateStyle(), c.emit(t.event), s && c.emit(s);
        }
        return this;
      };
    }
    function da(t) {
      Nr[t.field] = function() {
        var e = this[0];
        if (e) {
          if (t.overrideField) {
            var r = t.overrideField(e);
            if (r !== void 0)
              return r;
          }
          return e._private[t.field];
        }
      }, Nr[t.on] = Po({
        event: t.on,
        field: t.field,
        ableField: t.ableField,
        overrideAble: t.overrideAble,
        value: !0
      }), Nr[t.off] = Po({
        event: t.off,
        field: t.field,
        ableField: t.ableField,
        overrideAble: t.overrideAble,
        value: !1
      });
    }
    da({
      field: "locked",
      overrideField: function(e) {
        return e.cy().autolock() ? !0 : void 0;
      },
      on: "lock",
      off: "unlock"
    }), da({
      field: "grabbable",
      overrideField: function(e) {
        return e.cy().autoungrabify() || e.pannable() ? !1 : void 0;
      },
      on: "grabify",
      off: "ungrabify"
    }), da({
      field: "selected",
      ableField: "selectable",
      overrideAble: function(e) {
        return e.cy().autounselectify() ? !1 : void 0;
      },
      on: "select",
      off: "unselect"
    }), da({
      field: "selectable",
      overrideField: function(e) {
        return e.cy().autounselectify() ? !1 : void 0;
      },
      on: "selectify",
      off: "unselectify"
    }), Nr.deselect = Nr.unselect, Nr.grabbed = function() {
      var t = this[0];
      if (t)
        return t._private.grabbed;
    }, da({
      field: "active",
      on: "activate",
      off: "unactivate"
    }), da({
      field: "pannable",
      on: "panify",
      off: "unpanify"
    }), Nr.inactive = function() {
      var t = this[0];
      if (t)
        return !t._private.active;
    };
    var Pt = {}, Bo = function(e) {
      return function(a) {
        for (var n = this, i = [], s = 0; s < n.length; s++) {
          var o = n[s];
          if (o.isNode()) {
            for (var l = !1, u = o.connectedEdges(), f = 0; f < u.length; f++) {
              var h = u[f], c = h.source(), v = h.target();
              if (e.noIncomingEdges && v === o && c !== o || e.noOutgoingEdges && c === o && v !== o) {
                l = !0;
                break;
              }
            }
            l || i.push(o);
          }
        }
        return this.spawn(i, !0).filter(a);
      };
    }, Fo = function(e) {
      return function(r) {
        for (var a = this, n = [], i = 0; i < a.length; i++) {
          var s = a[i];
          if (s.isNode())
            for (var o = s.connectedEdges(), l = 0; l < o.length; l++) {
              var u = o[l], f = u.source(), h = u.target();
              e.outgoing && f === s ? (n.push(u), n.push(h)) : e.incoming && h === s && (n.push(u), n.push(f));
            }
        }
        return this.spawn(n, !0).filter(r);
      };
    }, zo = function(e) {
      return function(r) {
        for (var a = this, n = [], i = {}; ; ) {
          var s = e.outgoing ? a.outgoers() : a.incomers();
          if (s.length === 0)
            break;
          for (var o = !1, l = 0; l < s.length; l++) {
            var u = s[l], f = u.id();
            i[f] || (i[f] = !0, n.push(u), o = !0);
          }
          if (!o)
            break;
          a = s;
        }
        return this.spawn(n, !0).filter(r);
      };
    };
    Pt.clearTraversalCache = function() {
      for (var t = 0; t < this.length; t++)
        this[t]._private.traversalCache = null;
    }, Ue(Pt, {
      // get the root nodes in the DAG
      roots: Bo({
        noIncomingEdges: !0
      }),
      // get the leaf nodes in the DAG
      leaves: Bo({
        noOutgoingEdges: !0
      }),
      // normally called children in graph theory
      // these nodes =edges=> outgoing nodes
      outgoers: Kt(Fo({
        outgoing: !0
      }), "outgoers"),
      // aka DAG descendants
      successors: zo({
        outgoing: !0
      }),
      // normally called parents in graph theory
      // these nodes <=edges= incoming nodes
      incomers: Kt(Fo({
        incoming: !0
      }), "incomers"),
      // aka DAG ancestors
      predecessors: zo({
        incoming: !0
      })
    }), Ue(Pt, {
      neighborhood: Kt(function(t) {
        for (var e = [], r = this.nodes(), a = 0; a < r.length; a++)
          for (var n = r[a], i = n.connectedEdges(), s = 0; s < i.length; s++) {
            var o = i[s], l = o.source(), u = o.target(), f = n === l ? u : l;
            f.length > 0 && e.push(f[0]), e.push(o[0]);
          }
        return this.spawn(e, !0).filter(t);
      }, "neighborhood"),
      closedNeighborhood: function(e) {
        return this.neighborhood().add(this).filter(e);
      },
      openNeighborhood: function(e) {
        return this.neighborhood(e);
      }
    }), Pt.neighbourhood = Pt.neighborhood, Pt.closedNeighbourhood = Pt.closedNeighborhood, Pt.openNeighbourhood = Pt.openNeighborhood, Ue(Pt, {
      source: Kt(function(e) {
        var r = this[0], a;
        return r && (a = r._private.source || r.cy().collection()), a && e ? a.filter(e) : a;
      }, "source"),
      target: Kt(function(e) {
        var r = this[0], a;
        return r && (a = r._private.target || r.cy().collection()), a && e ? a.filter(e) : a;
      }, "target"),
      sources: Go({
        attr: "source"
      }),
      targets: Go({
        attr: "target"
      })
    });
    function Go(t) {
      return function(r) {
        for (var a = [], n = 0; n < this.length; n++) {
          var i = this[n], s = i._private[t.attr];
          s && a.push(s);
        }
        return this.spawn(a, !0).filter(r);
      };
    }
    Ue(Pt, {
      edgesWith: Kt($o(), "edgesWith"),
      edgesTo: Kt($o({
        thisIsSrc: !0
      }), "edgesTo")
    });
    function $o(t) {
      return function(r) {
        var a = [], n = this._private.cy, i = t || {};
        ee(r) && (r = n.$(r));
        for (var s = 0; s < r.length; s++)
          for (var o = r[s]._private.edges, l = 0; l < o.length; l++) {
            var u = o[l], f = u._private.data, h = this.hasElementWithId(f.source) && r.hasElementWithId(f.target), c = r.hasElementWithId(f.source) && this.hasElementWithId(f.target), v = h || c;
            v && ((i.thisIsSrc || i.thisIsTgt) && (i.thisIsSrc && !h || i.thisIsTgt && !c) || a.push(u));
          }
        return this.spawn(a, !0);
      };
    }
    Ue(Pt, {
      connectedEdges: Kt(function(t) {
        for (var e = [], r = this, a = 0; a < r.length; a++) {
          var n = r[a];
          if (n.isNode())
            for (var i = n._private.edges, s = 0; s < i.length; s++) {
              var o = i[s];
              e.push(o);
            }
        }
        return this.spawn(e, !0).filter(t);
      }, "connectedEdges"),
      connectedNodes: Kt(function(t) {
        for (var e = [], r = this, a = 0; a < r.length; a++) {
          var n = r[a];
          n.isEdge() && (e.push(n.source()[0]), e.push(n.target()[0]));
        }
        return this.spawn(e, !0).filter(t);
      }, "connectedNodes"),
      parallelEdges: Kt(Vo(), "parallelEdges"),
      codirectedEdges: Kt(Vo({
        codirected: !0
      }), "codirectedEdges")
    });
    function Vo(t) {
      var e = {
        codirected: !1
      };
      return t = Ue({}, e, t), function(a) {
        for (var n = [], i = this.edges(), s = t, o = 0; o < i.length; o++)
          for (var l = i[o], u = l._private, f = u.source, h = f._private.data.id, c = u.data.target, v = f._private.edges, d = 0; d < v.length; d++) {
            var g = v[d], y = g._private.data, p = y.target, m = y.source, b = p === c && m === h, E = h === p && c === m;
            (s.codirected && b || !s.codirected && (b || E)) && n.push(g);
          }
        return this.spawn(n, !0).filter(a);
      };
    }
    Ue(Pt, {
      components: function(e) {
        var r = this, a = r.cy(), n = a.collection(), i = e == null ? r.nodes() : e.nodes(), s = [];
        e != null && i.empty() && (i = e.sources());
        var o = function(f, h) {
          n.merge(f), i.unmerge(f), h.merge(f);
        };
        if (i.empty())
          return r.spawn();
        var l = function() {
          var f = a.collection();
          s.push(f);
          var h = i[0];
          o(h, f), r.bfs({
            directed: !1,
            roots: h,
            visit: function(v) {
              return o(v, f);
            }
          }), f.forEach(function(c) {
            c.connectedEdges().forEach(function(v) {
              r.has(v) && f.has(v.source()) && f.has(v.target()) && f.merge(v);
            });
          });
        };
        do
          l();
        while (i.length > 0);
        return s;
      },
      component: function() {
        var e = this[0];
        return e.cy().mutableElements().components(e)[0];
      }
    }), Pt.componentsOf = Pt.components;
    var Ot = function(e, r) {
      var a = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : !1, n = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : !1;
      if (e === void 0) {
        xt("A collection must have a reference to the core");
        return;
      }
      var i = new ur(), s = !1;
      if (!r)
        r = [];
      else if (r.length > 0 && S(r[0]) && !Ae(r[0])) {
        s = !0;
        for (var o = [], l = new Jr(), u = 0, f = r.length; u < f; u++) {
          var h = r[u];
          h.data == null && (h.data = {});
          var c = h.data;
          if (c.id == null)
            c.id = ps();
          else if (e.hasElementWithId(c.id) || l.has(c.id))
            continue;
          var v = new dn(e, h, !1);
          o.push(v), l.add(c.id);
        }
        r = o;
      }
      this.length = 0;
      for (var d = 0, g = r.length; d < g; d++) {
        var y = r[d][0];
        if (y != null) {
          var p = y._private.data.id;
          (!a || !i.has(p)) && (a && i.set(p, {
            index: this.length,
            ele: y
          }), this[this.length] = y, this.length++);
        }
      }
      this._private = {
        eles: this,
        cy: e,
        get map() {
          return this.lazyMap == null && this.rebuildMap(), this.lazyMap;
        },
        set map(m) {
          this.lazyMap = m;
        },
        rebuildMap: function() {
          for (var b = this.lazyMap = new ur(), E = this.eles, M = 0; M < E.length; M++) {
            var O = E[M];
            b.set(O.id(), {
              index: M,
              ele: O
            });
          }
        }
      }, a && (this._private.map = i), s && !n && this.restore();
    }, mt = dn.prototype = Ot.prototype = Object.create(Array.prototype);
    mt.instanceString = function() {
      return "collection";
    }, mt.spawn = function(t, e) {
      return new Ot(this.cy(), t, e);
    }, mt.spawnSelf = function() {
      return this.spawn(this);
    }, mt.cy = function() {
      return this._private.cy;
    }, mt.renderer = function() {
      return this._private.cy.renderer();
    }, mt.element = function() {
      return this[0];
    }, mt.collection = function() {
      return Ne(this) ? this : new Ot(this._private.cy, [this]);
    }, mt.unique = function() {
      return new Ot(this._private.cy, this, !0);
    }, mt.hasElementWithId = function(t) {
      return t = "" + t, this._private.map.has(t);
    }, mt.getElementById = function(t) {
      t = "" + t;
      var e = this._private.cy, r = this._private.map.get(t);
      return r ? r.ele : new Ot(e);
    }, mt.$id = mt.getElementById, mt.poolIndex = function() {
      var t = this._private.cy, e = t._private.elements, r = this[0]._private.data.id;
      return e._private.map.get(r).index;
    }, mt.indexOf = function(t) {
      var e = t[0]._private.data.id;
      return this._private.map.get(e).index;
    }, mt.indexOfId = function(t) {
      return t = "" + t, this._private.map.get(t).index;
    }, mt.json = function(t) {
      var e = this.element(), r = this.cy();
      if (e == null && t)
        return this;
      if (e != null) {
        var a = e._private;
        if (S(t)) {
          if (r.startBatch(), t.data) {
            e.data(t.data);
            var n = a.data;
            if (e.isEdge()) {
              var i = !1, s = {}, o = t.data.source, l = t.data.target;
              o != null && o != n.source && (s.source = "" + o, i = !0), l != null && l != n.target && (s.target = "" + l, i = !0), i && (e = e.move(s));
            } else {
              var u = "parent" in t.data, f = t.data.parent;
              u && (f != null || n.parent != null) && f != n.parent && (f === void 0 && (f = null), f != null && (f = "" + f), e = e.move({
                parent: f
              }));
            }
          }
          t.position && e.position(t.position);
          var h = function(g, y, p) {
            var m = t[g];
            m != null && m !== a[g] && (m ? e[y]() : e[p]());
          };
          return h("removed", "remove", "restore"), h("selected", "select", "unselect"), h("selectable", "selectify", "unselectify"), h("locked", "lock", "unlock"), h("grabbable", "grabify", "ungrabify"), h("pannable", "panify", "unpanify"), t.classes != null && e.classes(t.classes), r.endBatch(), this;
        } else if (t === void 0) {
          var c = {
            data: or(a.data),
            position: or(a.position),
            group: a.group,
            removed: a.removed,
            selected: a.selected,
            selectable: a.selectable,
            locked: a.locked,
            grabbable: a.grabbable,
            pannable: a.pannable,
            classes: null
          };
          c.classes = "";
          var v = 0;
          return a.classes.forEach(function(d) {
            return c.classes += v++ === 0 ? d : " " + d;
          }), c;
        }
      }
    }, mt.jsons = function() {
      for (var t = [], e = 0; e < this.length; e++) {
        var r = this[e], a = r.json();
        t.push(a);
      }
      return t;
    }, mt.clone = function() {
      for (var t = this.cy(), e = [], r = 0; r < this.length; r++) {
        var a = this[r], n = a.json(), i = new dn(t, n, !1);
        e.push(i);
      }
      return new Ot(t, e);
    }, mt.copy = mt.clone, mt.restore = function() {
      for (var t = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : !0, e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !0, r = this, a = r.cy(), n = a._private, i = [], s = [], o, l = 0, u = r.length; l < u; l++) {
        var f = r[l];
        e && !f.removed() || (f.isNode() ? i.push(f) : s.push(f));
      }
      o = i.concat(s);
      var h, c = function() {
        o.splice(h, 1), h--;
      };
      for (h = 0; h < o.length; h++) {
        var v = o[h], d = v._private, g = d.data;
        if (v.clearTraversalCache(), !(!e && !d.removed)) {
          if (g.id === void 0)
            g.id = ps();
          else if (k(g.id))
            g.id = "" + g.id;
          else if (Pe(g.id) || !ee(g.id)) {
            xt("Can not create element with invalid string ID `" + g.id + "`"), c();
            continue;
          } else if (a.hasElementWithId(g.id)) {
            xt("Can not create second element with ID `" + g.id + "`"), c();
            continue;
          }
        }
        var y = g.id;
        if (v.isNode()) {
          var p = d.position;
          p.x == null && (p.x = 0), p.y == null && (p.y = 0);
        }
        if (v.isEdge()) {
          for (var m = v, b = ["source", "target"], E = b.length, M = !1, O = 0; O < E; O++) {
            var x = b[O], I = g[x];
            k(I) && (I = g[x] = "" + g[x]), I == null || I === "" ? (xt("Can not create edge `" + y + "` with unspecified " + x), M = !0) : a.hasElementWithId(I) || (xt("Can not create edge `" + y + "` with nonexistant " + x + " `" + I + "`"), M = !0);
          }
          if (M) {
            c();
            continue;
          }
          var C = a.getElementById(g.source), B = a.getElementById(g.target);
          C.same(B) ? C._private.edges.push(m) : (C._private.edges.push(m), B._private.edges.push(m)), m._private.source = C, m._private.target = B;
        }
        d.map = new ur(), d.map.set(y, {
          ele: v,
          index: 0
        }), d.removed = !1, e && a.addToPool(v);
      }
      for (var F = 0; F < i.length; F++) {
        var R = i[F], X = R._private.data;
        k(X.parent) && (X.parent = "" + X.parent);
        var z = X.parent, re = z != null;
        if (re || R._private.parent) {
          var W = R._private.parent ? a.collection().merge(R._private.parent) : a.getElementById(z);
          if (W.empty())
            X.parent = void 0;
          else if (W[0].removed())
            ft("Node added with missing parent, reference to parent removed"), X.parent = void 0, R._private.parent = null;
          else {
            for (var Z = !1, ie = W; !ie.empty(); ) {
              if (R.same(ie)) {
                Z = !0, X.parent = void 0;
                break;
              }
              ie = ie.parent();
            }
            Z || (W[0]._private.children.push(R), R._private.parent = W[0], n.hasCompoundNodes = !0);
          }
        }
      }
      if (o.length > 0) {
        for (var oe = o.length === r.length ? r : new Ot(a, o), ge = 0; ge < oe.length; ge++) {
          var se = oe[ge];
          se.isNode() || (se.parallelEdges().clearTraversalCache(), se.source().clearTraversalCache(), se.target().clearTraversalCache());
        }
        var de;
        n.hasCompoundNodes ? de = a.collection().merge(oe).merge(oe.connectedNodes()).merge(oe.parent()) : de = oe, de.dirtyCompoundBoundsCache().dirtyBoundingBoxCache().updateStyle(t), t ? oe.emitAndNotify("add") : e && oe.emit("add");
      }
      return r;
    }, mt.removed = function() {
      var t = this[0];
      return t && t._private.removed;
    }, mt.inside = function() {
      var t = this[0];
      return t && !t._private.removed;
    }, mt.remove = function() {
      var t = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : !0, e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !0, r = this, a = [], n = {}, i = r._private.cy;
      function s(z) {
        for (var re = z._private.edges, W = 0; W < re.length; W++)
          l(re[W]);
      }
      function o(z) {
        for (var re = z._private.children, W = 0; W < re.length; W++)
          l(re[W]);
      }
      function l(z) {
        var re = n[z.id()];
        e && z.removed() || re || (n[z.id()] = !0, z.isNode() ? (a.push(z), s(z), o(z)) : a.unshift(z));
      }
      for (var u = 0, f = r.length; u < f; u++) {
        var h = r[u];
        l(h);
      }
      function c(z, re) {
        var W = z._private.edges;
        wr(W, re), z.clearTraversalCache();
      }
      function v(z) {
        z.clearTraversalCache();
      }
      var d = [];
      d.ids = {};
      function g(z, re) {
        re = re[0], z = z[0];
        var W = z._private.children, Z = z.id();
        wr(W, re), re._private.parent = null, d.ids[Z] || (d.ids[Z] = !0, d.push(z));
      }
      r.dirtyCompoundBoundsCache(), e && i.removeFromPool(a);
      for (var y = 0; y < a.length; y++) {
        var p = a[y];
        if (p.isEdge()) {
          var m = p.source()[0], b = p.target()[0];
          c(m, p), c(b, p);
          for (var E = p.parallelEdges(), M = 0; M < E.length; M++) {
            var O = E[M];
            v(O), O.isBundledBezier() && O.dirtyBoundingBoxCache();
          }
        } else {
          var x = p.parent();
          x.length !== 0 && g(x, p);
        }
        e && (p._private.removed = !0);
      }
      var I = i._private.elements;
      i._private.hasCompoundNodes = !1;
      for (var C = 0; C < I.length; C++) {
        var B = I[C];
        if (B.isParent()) {
          i._private.hasCompoundNodes = !0;
          break;
        }
      }
      var F = new Ot(this.cy(), a);
      F.size() > 0 && (t ? F.emitAndNotify("remove") : e && F.emit("remove"));
      for (var R = 0; R < d.length; R++) {
        var X = d[R];
        (!e || !X.removed()) && X.updateStyle();
      }
      return F;
    }, mt.move = function(t) {
      var e = this._private.cy, r = this, a = !1, n = !1, i = function(d) {
        return d == null ? d : "" + d;
      };
      if (t.source !== void 0 || t.target !== void 0) {
        var s = i(t.source), o = i(t.target), l = s != null && e.hasElementWithId(s), u = o != null && e.hasElementWithId(o);
        (l || u) && (e.batch(function() {
          r.remove(a, n), r.emitAndNotify("moveout");
          for (var v = 0; v < r.length; v++) {
            var d = r[v], g = d._private.data;
            d.isEdge() && (l && (g.source = s), u && (g.target = o));
          }
          r.restore(a, n);
        }), r.emitAndNotify("move"));
      } else if (t.parent !== void 0) {
        var f = i(t.parent), h = f === null || e.hasElementWithId(f);
        if (h) {
          var c = f === null ? void 0 : f;
          e.batch(function() {
            var v = r.remove(a, n);
            v.emitAndNotify("moveout");
            for (var d = 0; d < r.length; d++) {
              var g = r[d], y = g._private.data;
              g.isNode() && (y.parent = c);
            }
            v.restore(a, n);
          }), r.emitAndNotify("move");
        }
      }
      return this;
    }, [Ys, $v, Ln, Lr, fa, rd, An, yd, Mo, Io, xd, Rn, kn, At, Nr, Pt].forEach(function(t) {
      Ue(mt, t);
    });
    var Od = {
      add: function(e) {
        var r, a = this;
        if (pe(e)) {
          var n = e;
          if (n._private.cy === a)
            r = n.restore();
          else {
            for (var i = [], s = 0; s < n.length; s++) {
              var o = n[s];
              i.push(o.json());
            }
            r = new Ot(a, i);
          }
        } else if (te(e)) {
          var l = e;
          r = new Ot(a, l);
        } else if (S(e) && (te(e.nodes) || te(e.edges))) {
          for (var u = e, f = [], h = ["nodes", "edges"], c = 0, v = h.length; c < v; c++) {
            var d = h[c], g = u[d];
            if (te(g))
              for (var y = 0, p = g.length; y < p; y++) {
                var m = Ue({
                  group: d
                }, g[y]);
                f.push(m);
              }
          }
          r = new Ot(a, f);
        } else {
          var b = e;
          r = new dn(a, b).collection();
        }
        return r;
      },
      remove: function(e) {
        if (!pe(e)) {
          if (ee(e)) {
            var r = e;
            e = this.$(r);
          }
        }
        return e.remove();
      }
    };
    /*! Bezier curve function generator. Copyright Gaetan Renaudeau. MIT License: http://en.wikipedia.org/wiki/MIT_License */
    function Nd(t, e, r, a) {
      var n = 4, i = 1e-3, s = 1e-7, o = 10, l = 11, u = 1 / (l - 1), f = typeof Float32Array < "u";
      if (arguments.length !== 4)
        return !1;
      for (var h = 0; h < 4; ++h)
        if (typeof arguments[h] != "number" || isNaN(arguments[h]) || !isFinite(arguments[h]))
          return !1;
      t = Math.min(t, 1), r = Math.min(r, 1), t = Math.max(t, 0), r = Math.max(r, 0);
      var c = f ? new Float32Array(l) : new Array(l);
      function v(B, F) {
        return 1 - 3 * F + 3 * B;
      }
      function d(B, F) {
        return 3 * F - 6 * B;
      }
      function g(B) {
        return 3 * B;
      }
      function y(B, F, R) {
        return ((v(F, R) * B + d(F, R)) * B + g(F)) * B;
      }
      function p(B, F, R) {
        return 3 * v(F, R) * B * B + 2 * d(F, R) * B + g(F);
      }
      function m(B, F) {
        for (var R = 0; R < n; ++R) {
          var X = p(F, t, r);
          if (X === 0)
            return F;
          var z = y(F, t, r) - B;
          F -= z / X;
        }
        return F;
      }
      function b() {
        for (var B = 0; B < l; ++B)
          c[B] = y(B * u, t, r);
      }
      function E(B, F, R) {
        var X, z, re = 0;
        do
          z = F + (R - F) / 2, X = y(z, t, r) - B, X > 0 ? R = z : F = z;
        while (Math.abs(X) > s && ++re < o);
        return z;
      }
      function M(B) {
        for (var F = 0, R = 1, X = l - 1; R !== X && c[R] <= B; ++R)
          F += u;
        --R;
        var z = (B - c[R]) / (c[R + 1] - c[R]), re = F + z * u, W = p(re, t, r);
        return W >= i ? m(B, re) : W === 0 ? re : E(B, F, F + u);
      }
      var O = !1;
      function x() {
        O = !0, (t !== e || r !== a) && b();
      }
      var I = function(F) {
        return O || x(), t === e && r === a ? F : F === 0 ? 0 : F === 1 ? 1 : y(M(F), e, a);
      };
      I.getControlPoints = function() {
        return [{
          x: t,
          y: e
        }, {
          x: r,
          y: a
        }];
      };
      var C = "generateBezier(" + [t, e, r, a] + ")";
      return I.toString = function() {
        return C;
      }, I;
    }
    /*! Runge-Kutta spring physics function generator. Adapted from Framer.js, copyright Koen Bok. MIT License: http://en.wikipedia.org/wiki/MIT_License */
    var Md = function() {
      function t(a) {
        return -a.tension * a.x - a.friction * a.v;
      }
      function e(a, n, i) {
        var s = {
          x: a.x + i.dx * n,
          v: a.v + i.dv * n,
          tension: a.tension,
          friction: a.friction
        };
        return {
          dx: s.v,
          dv: t(s)
        };
      }
      function r(a, n) {
        var i = {
          dx: a.v,
          dv: t(a)
        }, s = e(a, n * 0.5, i), o = e(a, n * 0.5, s), l = e(a, n, o), u = 1 / 6 * (i.dx + 2 * (s.dx + o.dx) + l.dx), f = 1 / 6 * (i.dv + 2 * (s.dv + o.dv) + l.dv);
        return a.x = a.x + u * n, a.v = a.v + f * n, a;
      }
      return function a(n, i, s) {
        var o = {
          x: -1,
          v: 0,
          tension: null,
          friction: null
        }, l = [0], u = 0, f = 1 / 1e4, h = 16 / 1e3, c, v, d;
        for (n = parseFloat(n) || 500, i = parseFloat(i) || 20, s = s || null, o.tension = n, o.friction = i, c = s !== null, c ? (u = a(n, i), v = u / s * h) : v = h; d = r(d || o, v), l.push(1 + d.x), u += 16, Math.abs(d.x) > f && Math.abs(d.v) > f; )
          ;
        return c ? function(g) {
          return l[g * (l.length - 1) | 0];
        } : u;
      };
    }(), bt = function(e, r, a, n) {
      var i = Nd(e, r, a, n);
      return function(s, o, l) {
        return s + (o - s) * i(l);
      };
    }, Fn = {
      linear: function(e, r, a) {
        return e + (r - e) * a;
      },
      // default easings
      ease: bt(0.25, 0.1, 0.25, 1),
      "ease-in": bt(0.42, 0, 1, 1),
      "ease-out": bt(0, 0, 0.58, 1),
      "ease-in-out": bt(0.42, 0, 0.58, 1),
      // sine
      "ease-in-sine": bt(0.47, 0, 0.745, 0.715),
      "ease-out-sine": bt(0.39, 0.575, 0.565, 1),
      "ease-in-out-sine": bt(0.445, 0.05, 0.55, 0.95),
      // quad
      "ease-in-quad": bt(0.55, 0.085, 0.68, 0.53),
      "ease-out-quad": bt(0.25, 0.46, 0.45, 0.94),
      "ease-in-out-quad": bt(0.455, 0.03, 0.515, 0.955),
      // cubic
      "ease-in-cubic": bt(0.55, 0.055, 0.675, 0.19),
      "ease-out-cubic": bt(0.215, 0.61, 0.355, 1),
      "ease-in-out-cubic": bt(0.645, 0.045, 0.355, 1),
      // quart
      "ease-in-quart": bt(0.895, 0.03, 0.685, 0.22),
      "ease-out-quart": bt(0.165, 0.84, 0.44, 1),
      "ease-in-out-quart": bt(0.77, 0, 0.175, 1),
      // quint
      "ease-in-quint": bt(0.755, 0.05, 0.855, 0.06),
      "ease-out-quint": bt(0.23, 1, 0.32, 1),
      "ease-in-out-quint": bt(0.86, 0, 0.07, 1),
      // expo
      "ease-in-expo": bt(0.95, 0.05, 0.795, 0.035),
      "ease-out-expo": bt(0.19, 1, 0.22, 1),
      "ease-in-out-expo": bt(1, 0, 0, 1),
      // circ
      "ease-in-circ": bt(0.6, 0.04, 0.98, 0.335),
      "ease-out-circ": bt(0.075, 0.82, 0.165, 1),
      "ease-in-out-circ": bt(0.785, 0.135, 0.15, 0.86),
      // user param easings...
      spring: function(e, r, a) {
        if (a === 0)
          return Fn.linear;
        var n = Md(e, r, a);
        return function(i, s, o) {
          return i + (s - i) * n(o);
        };
      },
      "cubic-bezier": bt
    };
    function _o(t, e, r, a, n) {
      if (a === 1 || e === r)
        return r;
      var i = n(e, r, a);
      return t == null || ((t.roundValue || t.color) && (i = Math.round(i)), t.min !== void 0 && (i = Math.max(i, t.min)), t.max !== void 0 && (i = Math.min(i, t.max))), i;
    }
    function Uo(t, e) {
      return t.pfValue != null || t.value != null ? t.pfValue != null && (e == null || e.type.units !== "%") ? t.pfValue : t.value : t;
    }
    function ga(t, e, r, a, n) {
      var i = n != null ? n.type : null;
      r < 0 ? r = 0 : r > 1 && (r = 1);
      var s = Uo(t, n), o = Uo(e, n);
      if (k(s) && k(o))
        return _o(i, s, o, r, a);
      if (te(s) && te(o)) {
        for (var l = [], u = 0; u < o.length; u++) {
          var f = s[u], h = o[u];
          if (f != null && h != null) {
            var c = _o(i, f, h, r, a);
            l.push(c);
          } else
            l.push(h);
        }
        return l;
      }
    }
    function Id(t, e, r, a) {
      var n = !a, i = t._private, s = e._private, o = s.easing, l = s.startTime, u = a ? t : t.cy(), f = u.style();
      if (!s.easingImpl)
        if (o == null)
          s.easingImpl = Fn.linear;
        else {
          var h;
          if (ee(o)) {
            var c = f.parse("transition-timing-function", o);
            h = c.value;
          } else
            h = o;
          var v, d;
          ee(h) ? (v = h, d = []) : (v = h[1], d = h.slice(2).map(function(oe) {
            return +oe;
          })), d.length > 0 ? (v === "spring" && d.push(s.duration), s.easingImpl = Fn[v].apply(null, d)) : s.easingImpl = Fn[v];
        }
      var g = s.easingImpl, y;
      if (s.duration === 0 ? y = 1 : y = (r - l) / s.duration, s.applying && (y = s.progress), y < 0 ? y = 0 : y > 1 && (y = 1), s.delay == null) {
        var p = s.startPosition, m = s.position;
        if (m && n && !t.locked()) {
          var b = {};
          Xa(p.x, m.x) && (b.x = ga(p.x, m.x, y, g)), Xa(p.y, m.y) && (b.y = ga(p.y, m.y, y, g)), t.position(b);
        }
        var E = s.startPan, M = s.pan, O = i.pan, x = M != null && a;
        x && (Xa(E.x, M.x) && (O.x = ga(E.x, M.x, y, g)), Xa(E.y, M.y) && (O.y = ga(E.y, M.y, y, g)), t.emit("pan"));
        var I = s.startZoom, C = s.zoom, B = C != null && a;
        B && (Xa(I, C) && (i.zoom = ka(i.minZoom, ga(I, C, y, g), i.maxZoom)), t.emit("zoom")), (x || B) && t.emit("viewport");
        var F = s.style;
        if (F && F.length > 0 && n) {
          for (var R = 0; R < F.length; R++) {
            var X = F[R], z = X.name, re = X, W = s.startStyle[z], Z = f.properties[W.name], ie = ga(W, re, y, g, Z);
            f.overrideBypass(t, z, ie);
          }
          t.emit("style");
        }
      }
      return s.progress = y, y;
    }
    function Xa(t, e) {
      return t == null || e == null ? !1 : k(t) && k(e) ? !0 : !!(t && e);
    }
    function Rd(t, e, r, a) {
      var n = e._private;
      n.started = !0, n.startTime = r - n.progress * n.duration;
    }
    function Yo(t, e) {
      var r = e._private.aniEles, a = [];
      function n(f, h) {
        var c = f._private, v = c.animation.current, d = c.animation.queue, g = !1;
        if (v.length === 0) {
          var y = d.shift();
          y && v.push(y);
        }
        for (var p = function(O) {
          for (var x = O.length - 1; x >= 0; x--) {
            var I = O[x];
            I();
          }
          O.splice(0, O.length);
        }, m = v.length - 1; m >= 0; m--) {
          var b = v[m], E = b._private;
          if (E.stopped) {
            v.splice(m, 1), E.hooked = !1, E.playing = !1, E.started = !1, p(E.frames);
            continue;
          }
          !E.playing && !E.applying || (E.playing && E.applying && (E.applying = !1), E.started || Rd(f, b, t), Id(f, b, t, h), E.applying && (E.applying = !1), p(E.frames), E.step != null && E.step(t), b.completed() && (v.splice(m, 1), E.hooked = !1, E.playing = !1, E.started = !1, p(E.completes)), g = !0);
        }
        return !h && v.length === 0 && d.length === 0 && a.push(f), g;
      }
      for (var i = !1, s = 0; s < r.length; s++) {
        var o = r[s], l = n(o);
        i = i || l;
      }
      var u = n(e, !0);
      (i || u) && (r.length > 0 ? e.notify("draw", r) : e.notify("draw")), r.unmerge(a), e.emit("step");
    }
    var kd = {
      // pull in animation functions
      animate: ht.animate(),
      animation: ht.animation(),
      animated: ht.animated(),
      clearQueue: ht.clearQueue(),
      delay: ht.delay(),
      delayAnimation: ht.delayAnimation(),
      stop: ht.stop(),
      addToAnimationPool: function(e) {
        var r = this;
        r.styleEnabled() && r._private.aniEles.merge(e);
      },
      stopAnimationLoop: function() {
        this._private.animationsRunning = !1;
      },
      startAnimationLoop: function() {
        var e = this;
        if (e._private.animationsRunning = !0, !e.styleEnabled())
          return;
        function r() {
          e._private.animationsRunning && hn(function(i) {
            Yo(i, e), r();
          });
        }
        var a = e.renderer();
        a && a.beforeRender ? a.beforeRender(function(i, s) {
          Yo(s, e);
        }, a.beforeRenderPriorities.animations) : r();
      }
    }, Pd = {
      qualifierCompare: function(e, r) {
        return e == null || r == null ? e == null && r == null : e.sameText(r);
      },
      eventMatches: function(e, r, a) {
        var n = r.qualifier;
        return n != null ? e !== a.target && Ae(a.target) && n.matches(a.target) : !0;
      },
      addEventFields: function(e, r) {
        r.cy = e, r.target = e;
      },
      callbackContext: function(e, r, a) {
        return r.qualifier != null ? a.target : e;
      }
    }, zn = function(e) {
      return ee(e) ? new Dr(e) : e;
    }, Ho = {
      createEmitter: function() {
        var e = this._private;
        return e.emitter || (e.emitter = new Mn(Pd, this)), this;
      },
      emitter: function() {
        return this._private.emitter;
      },
      on: function(e, r, a) {
        return this.emitter().on(e, zn(r), a), this;
      },
      removeListener: function(e, r, a) {
        return this.emitter().removeListener(e, zn(r), a), this;
      },
      removeAllListeners: function() {
        return this.emitter().removeAllListeners(), this;
      },
      one: function(e, r, a) {
        return this.emitter().one(e, zn(r), a), this;
      },
      once: function(e, r, a) {
        return this.emitter().one(e, zn(r), a), this;
      },
      emit: function(e, r) {
        return this.emitter().emit(e, r), this;
      },
      emitAndNotify: function(e, r) {
        return this.emit(e), this.notify(e, r), this;
      }
    };
    ht.eventAliasesOn(Ho);
    var Ii = {
      png: function(e) {
        var r = this._private.renderer;
        return e = e || {}, r.png(e);
      },
      jpg: function(e) {
        var r = this._private.renderer;
        return e = e || {}, e.bg = e.bg || "#fff", r.jpg(e);
      }
    };
    Ii.jpeg = Ii.jpg;
    var Gn = {
      layout: function(e) {
        var r = this;
        if (e == null) {
          xt("Layout options must be specified to make a layout");
          return;
        }
        if (e.name == null) {
          xt("A `name` must be specified to make a layout");
          return;
        }
        var a = e.name, n = r.extension("layout", a);
        if (n == null) {
          xt("No such layout `" + a + "` found.  Did you forget to import it and `cytoscape.use()` it?");
          return;
        }
        var i;
        ee(e.eles) ? i = r.$(e.eles) : i = e.eles != null ? e.eles : r.$();
        var s = new n(Ue({}, e, {
          cy: r,
          eles: i
        }));
        return s;
      }
    };
    Gn.createLayout = Gn.makeLayout = Gn.layout;
    var Bd = {
      notify: function(e, r) {
        var a = this._private;
        if (this.batching()) {
          a.batchNotifications = a.batchNotifications || {};
          var n = a.batchNotifications[e] = a.batchNotifications[e] || this.collection();
          r != null && n.merge(r);
          return;
        }
        if (a.notificationsEnabled) {
          var i = this.renderer();
          this.destroyed() || !i || i.notify(e, r);
        }
      },
      notifications: function(e) {
        var r = this._private;
        return e === void 0 ? r.notificationsEnabled : (r.notificationsEnabled = !!e, this);
      },
      noNotifications: function(e) {
        this.notifications(!1), e(), this.notifications(!0);
      },
      batching: function() {
        return this._private.batchCount > 0;
      },
      startBatch: function() {
        var e = this._private;
        return e.batchCount == null && (e.batchCount = 0), e.batchCount === 0 && (e.batchStyleEles = this.collection(), e.batchNotifications = {}), e.batchCount++, this;
      },
      endBatch: function() {
        var e = this._private;
        if (e.batchCount === 0)
          return this;
        if (e.batchCount--, e.batchCount === 0) {
          e.batchStyleEles.updateStyle();
          var r = this.renderer();
          Object.keys(e.batchNotifications).forEach(function(a) {
            var n = e.batchNotifications[a];
            n.empty() ? r.notify(a) : r.notify(a, n);
          });
        }
        return this;
      },
      batch: function(e) {
        return this.startBatch(), e(), this.endBatch(), this;
      },
      // for backwards compatibility
      batchData: function(e) {
        var r = this;
        return this.batch(function() {
          for (var a = Object.keys(e), n = 0; n < a.length; n++) {
            var i = a[n], s = e[i], o = r.getElementById(i);
            o.data(s);
          }
        });
      }
    }, Fd = Lt({
      hideEdgesOnViewport: !1,
      textureOnViewport: !1,
      motionBlur: !1,
      motionBlurOpacity: 0.05,
      pixelRatio: void 0,
      desktopTapThreshold: 4,
      touchTapThreshold: 8,
      wheelSensitivity: 1,
      debug: !1,
      showFps: !1
    }), Ri = {
      renderTo: function(e, r, a, n) {
        var i = this._private.renderer;
        return i.renderTo(e, r, a, n), this;
      },
      renderer: function() {
        return this._private.renderer;
      },
      forceRender: function() {
        return this.notify("draw"), this;
      },
      resize: function() {
        return this.invalidateSize(), this.emitAndNotify("resize"), this;
      },
      initRenderer: function(e) {
        var r = this, a = r.extension("renderer", e.name);
        if (a == null) {
          xt("Can not initialise: No such renderer `".concat(e.name, "` found. Did you forget to import it and `cytoscape.use()` it?"));
          return;
        }
        e.wheelSensitivity !== void 0 && ft("You have set a custom wheel sensitivity.  This will make your app zoom unnaturally when using mainstream mice.  You should change this value from the default only if you can guarantee that all your users will use the same hardware and OS configuration as your current machine.");
        var n = Fd(e);
        n.cy = r, r._private.renderer = new a(n), this.notify("init");
      },
      destroyRenderer: function() {
        var e = this;
        e.notify("destroy");
        var r = e.container();
        if (r)
          for (r._cyreg = null; r.childNodes.length > 0; )
            r.removeChild(r.childNodes[0]);
        e._private.renderer = null, e.mutableElements().forEach(function(a) {
          var n = a._private;
          n.rscratch = {}, n.rstyle = {}, n.animation.current = [], n.animation.queue = [];
        });
      },
      onRender: function(e) {
        return this.on("render", e);
      },
      offRender: function(e) {
        return this.off("render", e);
      }
    };
    Ri.invalidateDimensions = Ri.resize;
    var $n = {
      // get a collection
      // - empty collection on no args
      // - collection of elements in the graph on selector arg
      // - guarantee a returned collection when elements or collection specified
      collection: function(e, r) {
        return ee(e) ? this.$(e) : pe(e) ? e.collection() : te(e) ? (r || (r = {}), new Ot(this, e, r.unique, r.removed)) : new Ot(this);
      },
      nodes: function(e) {
        var r = this.$(function(a) {
          return a.isNode();
        });
        return e ? r.filter(e) : r;
      },
      edges: function(e) {
        var r = this.$(function(a) {
          return a.isEdge();
        });
        return e ? r.filter(e) : r;
      },
      // search the graph like jQuery
      $: function(e) {
        var r = this._private.elements;
        return e ? r.filter(e) : r.spawnSelf();
      },
      mutableElements: function() {
        return this._private.elements;
      }
    };
    $n.elements = $n.filter = $n.$;
    var Bt = {}, qa = "t", zd = "f";
    Bt.apply = function(t) {
      for (var e = this, r = e._private, a = r.cy, n = a.collection(), i = 0; i < t.length; i++) {
        var s = t[i], o = e.getContextMeta(s);
        if (!o.empty) {
          var l = e.getContextStyle(o), u = e.applyContextStyle(o, l, s);
          s._private.appliedInitStyle ? e.updateTransitions(s, u.diffProps) : s._private.appliedInitStyle = !0;
          var f = e.updateStyleHints(s);
          f && n.push(s);
        }
      }
      return n;
    }, Bt.getPropertiesDiff = function(t, e) {
      var r = this, a = r._private.propDiffs = r._private.propDiffs || {}, n = t + "-" + e, i = a[n];
      if (i)
        return i;
      for (var s = [], o = {}, l = 0; l < r.length; l++) {
        var u = r[l], f = t[l] === qa, h = e[l] === qa, c = f !== h, v = u.mappedProperties.length > 0;
        if (c || h && v) {
          var d = void 0;
          c && v || c ? d = u.properties : v && (d = u.mappedProperties);
          for (var g = 0; g < d.length; g++) {
            for (var y = d[g], p = y.name, m = !1, b = l + 1; b < r.length; b++) {
              var E = r[b], M = e[b] === qa;
              if (M && (m = E.properties[y.name] != null, m))
                break;
            }
            !o[p] && !m && (o[p] = !0, s.push(p));
          }
        }
      }
      return a[n] = s, s;
    }, Bt.getContextMeta = function(t) {
      for (var e = this, r = "", a, n = t._private.styleCxtKey || "", i = 0; i < e.length; i++) {
        var s = e[i], o = s.selector && s.selector.matches(t);
        o ? r += qa : r += zd;
      }
      return a = e.getPropertiesDiff(n, r), t._private.styleCxtKey = r, {
        key: r,
        diffPropNames: a,
        empty: a.length === 0
      };
    }, Bt.getContextStyle = function(t) {
      var e = t.key, r = this, a = this._private.contextStyles = this._private.contextStyles || {};
      if (a[e])
        return a[e];
      for (var n = {
        _private: {
          key: e
        }
      }, i = 0; i < r.length; i++) {
        var s = r[i], o = e[i] === qa;
        if (o)
          for (var l = 0; l < s.properties.length; l++) {
            var u = s.properties[l];
            n[u.name] = u;
          }
      }
      return a[e] = n, n;
    }, Bt.applyContextStyle = function(t, e, r) {
      for (var a = this, n = t.diffPropNames, i = {}, s = a.types, o = 0; o < n.length; o++) {
        var l = n[o], u = e[l], f = r.pstyle(l);
        if (!u)
          if (f)
            f.bypass ? u = {
              name: l,
              deleteBypassed: !0
            } : u = {
              name: l,
              delete: !0
            };
          else
            continue;
        if (f !== u) {
          if (u.mapped === s.fn && f != null && f.mapping != null && f.mapping.value === u.value) {
            var h = f.mapping, c = h.fnValue = u.value(r);
            if (c === h.prevFnValue)
              continue;
          }
          var v = i[l] = {
            prev: f
          };
          a.applyParsedProperty(r, u), v.next = r.pstyle(l), v.next && v.next.bypass && (v.next = v.next.bypassed);
        }
      }
      return {
        diffProps: i
      };
    }, Bt.updateStyleHints = function(t) {
      var e = t._private, r = this, a = r.propertyGroupNames, n = r.propertyGroupKeys, i = function(Oe, Ie, He) {
        return r.getPropertiesHash(Oe, Ie, He);
      }, s = e.styleKey;
      if (t.removed())
        return !1;
      var o = e.group === "nodes", l = t._private.style;
      a = Object.keys(l);
      for (var u = 0; u < n.length; u++) {
        var f = n[u];
        e.styleKeys[f] = [Qr, Oa];
      }
      for (var h = function(Oe, Ie) {
        return e.styleKeys[Ie][0] = Na(Oe, e.styleKeys[Ie][0]);
      }, c = function(Oe, Ie) {
        return e.styleKeys[Ie][1] = Ma(Oe, e.styleKeys[Ie][1]);
      }, v = function(Oe, Ie) {
        h(Oe, Ie), c(Oe, Ie);
      }, d = function(Oe, Ie) {
        for (var He = 0; He < Oe.length; He++) {
          var qe = Oe.charCodeAt(He);
          h(qe, Ie), c(qe, Ie);
        }
      }, g = 2e9, y = function(Oe) {
        return -128 < Oe && Oe < 128 && Math.floor(Oe) !== Oe ? g - (Oe * 1024 | 0) : Oe;
      }, p = 0; p < a.length; p++) {
        var m = a[p], b = l[m];
        if (b != null) {
          var E = this.properties[m], M = E.type, O = E.groupKey, x = void 0;
          E.hashOverride != null ? x = E.hashOverride(t, b) : b.pfValue != null && (x = b.pfValue);
          var I = E.enums == null ? b.value : null, C = x != null, B = I != null, F = C || B, R = b.units;
          if (M.number && F && !M.multiple) {
            var X = C ? x : I;
            v(y(X), O), !C && R != null && d(R, O);
          } else
            d(b.strValue, O);
        }
      }
      for (var z = [Qr, Oa], re = 0; re < n.length; re++) {
        var W = n[re], Z = e.styleKeys[W];
        z[0] = Na(Z[0], z[0]), z[1] = Ma(Z[1], z[1]);
      }
      e.styleKey = Ul(z[0], z[1]);
      var ie = e.styleKeys;
      e.labelDimsKey = Er(ie.labelDimensions);
      var oe = i(t, ["label"], ie.labelDimensions);
      if (e.labelKey = Er(oe), e.labelStyleKey = Er(cn(ie.commonLabel, oe)), !o) {
        var ge = i(t, ["source-label"], ie.labelDimensions);
        e.sourceLabelKey = Er(ge), e.sourceLabelStyleKey = Er(cn(ie.commonLabel, ge));
        var se = i(t, ["target-label"], ie.labelDimensions);
        e.targetLabelKey = Er(se), e.targetLabelStyleKey = Er(cn(ie.commonLabel, se));
      }
      if (o) {
        var de = e.styleKeys, we = de.nodeBody, Te = de.nodeBorder, Ee = de.backgroundImage, ye = de.compound, ae = de.pie, xe = [we, Te, Ee, ye, ae].filter(function(Ce) {
          return Ce != null;
        }).reduce(cn, [Qr, Oa]);
        e.nodeKey = Er(xe), e.hasPie = ae != null && ae[0] !== Qr && ae[1] !== Oa;
      }
      return s !== e.styleKey;
    }, Bt.clearStyleHints = function(t) {
      var e = t._private;
      e.styleCxtKey = "", e.styleKeys = {}, e.styleKey = null, e.labelKey = null, e.labelStyleKey = null, e.sourceLabelKey = null, e.sourceLabelStyleKey = null, e.targetLabelKey = null, e.targetLabelStyleKey = null, e.nodeKey = null, e.hasPie = null;
    }, Bt.applyParsedProperty = function(t, e) {
      var r = this, a = e, n = t._private.style, i, s = r.types, o = r.properties[a.name].type, l = a.bypass, u = n[a.name], f = u && u.bypass, h = t._private, c = "mapping", v = function(we) {
        return we == null ? null : we.pfValue != null ? we.pfValue : we.value;
      }, d = function() {
        var we = v(u), Te = v(a);
        r.checkTriggers(t, a.name, we, Te);
      };
      if (a && a.name.substr(0, 3) === "pie" && ft("The pie style properties are deprecated.  Create charts using background images instead."), e.name === "curve-style" && t.isEdge() && // loops must be bundled beziers
      (e.value !== "bezier" && t.isLoop() || // edges connected to compound nodes can not be haystacks
      e.value === "haystack" && (t.source().isParent() || t.target().isParent())) && (a = e = this.parse(e.name, "bezier", l)), a.delete)
        return n[a.name] = void 0, d(), !0;
      if (a.deleteBypassed)
        return u ? u.bypass ? (u.bypassed = void 0, d(), !0) : !1 : (d(), !0);
      if (a.deleteBypass)
        return u ? u.bypass ? (n[a.name] = u.bypassed, d(), !0) : !1 : (d(), !0);
      var g = function() {
        ft("Do not assign mappings to elements without corresponding data (i.e. ele `" + t.id() + "` has no mapping for property `" + a.name + "` with data field `" + a.field + "`); try a `[" + a.field + "]` selector to limit scope to elements with `" + a.field + "` defined");
      };
      switch (a.mapped) {
        case s.mapData: {
          for (var y = a.field.split("."), p = h.data, m = 0; m < y.length && p; m++) {
            var b = y[m];
            p = p[b];
          }
          if (p == null)
            return g(), !1;
          var E;
          if (k(p)) {
            var M = a.fieldMax - a.fieldMin;
            M === 0 ? E = 0 : E = (p - a.fieldMin) / M;
          } else
            return ft("Do not use continuous mappers without specifying numeric data (i.e. `" + a.field + ": " + p + "` for `" + t.id() + "` is non-numeric)"), !1;
          if (E < 0 ? E = 0 : E > 1 && (E = 1), o.color) {
            var O = a.valueMin[0], x = a.valueMax[0], I = a.valueMin[1], C = a.valueMax[1], B = a.valueMin[2], F = a.valueMax[2], R = a.valueMin[3] == null ? 1 : a.valueMin[3], X = a.valueMax[3] == null ? 1 : a.valueMax[3], z = [Math.round(O + (x - O) * E), Math.round(I + (C - I) * E), Math.round(B + (F - B) * E), Math.round(R + (X - R) * E)];
            i = {
              // colours are simple, so just create the flat property instead of expensive string parsing
              bypass: a.bypass,
              // we're a bypass if the mapping property is a bypass
              name: a.name,
              value: z,
              strValue: "rgb(" + z[0] + ", " + z[1] + ", " + z[2] + ")"
            };
          } else if (o.number) {
            var re = a.valueMin + (a.valueMax - a.valueMin) * E;
            i = this.parse(a.name, re, a.bypass, c);
          } else
            return !1;
          if (!i)
            return g(), !1;
          i.mapping = a, a = i;
          break;
        }
        case s.data: {
          for (var W = a.field.split("."), Z = h.data, ie = 0; ie < W.length && Z; ie++) {
            var oe = W[ie];
            Z = Z[oe];
          }
          if (Z != null && (i = this.parse(a.name, Z, a.bypass, c)), !i)
            return g(), !1;
          i.mapping = a, a = i;
          break;
        }
        case s.fn: {
          var ge = a.value, se = a.fnValue != null ? a.fnValue : ge(t);
          if (a.prevFnValue = se, se == null)
            return ft("Custom function mappers may not return null (i.e. `" + a.name + "` for ele `" + t.id() + "` is null)"), !1;
          if (i = this.parse(a.name, se, a.bypass, c), !i)
            return ft("Custom function mappers may not return invalid values for the property type (i.e. `" + a.name + "` for ele `" + t.id() + "` is invalid)"), !1;
          i.mapping = or(a), a = i;
          break;
        }
        case void 0:
          break;
        default:
          return !1;
      }
      return l ? (f ? a.bypassed = u.bypassed : a.bypassed = u, n[a.name] = a) : f ? u.bypassed = a : n[a.name] = a, d(), !0;
    }, Bt.cleanElements = function(t, e) {
      for (var r = 0; r < t.length; r++) {
        var a = t[r];
        if (this.clearStyleHints(a), a.dirtyCompoundBoundsCache(), a.dirtyBoundingBoxCache(), !e)
          a._private.style = {};
        else
          for (var n = a._private.style, i = Object.keys(n), s = 0; s < i.length; s++) {
            var o = i[s], l = n[o];
            l != null && (l.bypass ? l.bypassed = null : n[o] = null);
          }
      }
    }, Bt.update = function() {
      var t = this._private.cy, e = t.mutableElements();
      e.updateStyle();
    }, Bt.updateTransitions = function(t, e) {
      var r = this, a = t._private, n = t.pstyle("transition-property").value, i = t.pstyle("transition-duration").pfValue, s = t.pstyle("transition-delay").pfValue;
      if (n.length > 0 && i > 0) {
        for (var o = {}, l = !1, u = 0; u < n.length; u++) {
          var f = n[u], h = t.pstyle(f), c = e[f];
          if (c) {
            var v = c.prev, d = v, g = c.next != null ? c.next : h, y = !1, p = void 0, m = 1e-6;
            d && (k(d.pfValue) && k(g.pfValue) ? (y = g.pfValue - d.pfValue, p = d.pfValue + m * y) : k(d.value) && k(g.value) ? (y = g.value - d.value, p = d.value + m * y) : te(d.value) && te(g.value) && (y = d.value[0] !== g.value[0] || d.value[1] !== g.value[1] || d.value[2] !== g.value[2], p = d.strValue), y && (o[f] = g.strValue, this.applyBypass(t, f, p), l = !0));
          }
        }
        if (!l)
          return;
        a.transitioning = !0, new ia(function(b) {
          s > 0 ? t.delayAnimation(s).play().promise().then(b) : b();
        }).then(function() {
          return t.animation({
            style: o,
            duration: i,
            easing: t.pstyle("transition-timing-function").value,
            queue: !1
          }).play().promise();
        }).then(function() {
          r.removeBypasses(t, n), t.emitAndNotify("style"), a.transitioning = !1;
        });
      } else
        a.transitioning && (this.removeBypasses(t, n), t.emitAndNotify("style"), a.transitioning = !1);
    }, Bt.checkTrigger = function(t, e, r, a, n, i) {
      var s = this.properties[e], o = n(s);
      o != null && o(r, a) && i(s);
    }, Bt.checkZOrderTrigger = function(t, e, r, a) {
      var n = this;
      this.checkTrigger(t, e, r, a, function(i) {
        return i.triggersZOrder;
      }, function() {
        n._private.cy.notify("zorder", t);
      });
    }, Bt.checkBoundsTrigger = function(t, e, r, a) {
      this.checkTrigger(t, e, r, a, function(n) {
        return n.triggersBounds;
      }, function(n) {
        t.dirtyCompoundBoundsCache(), t.dirtyBoundingBoxCache(), // only for beziers -- so performance of other edges isn't affected
        n.triggersBoundsOfParallelBeziers && (e === "curve-style" && (r === "bezier" || a === "bezier") || e === "display" && (r === "none" || a === "none")) && t.parallelEdges().forEach(function(i) {
          i.isBundledBezier() && i.dirtyBoundingBoxCache();
        });
      });
    }, Bt.checkTriggers = function(t, e, r, a) {
      t.dirtyStyleCache(), this.checkZOrderTrigger(t, e, r, a), this.checkBoundsTrigger(t, e, r, a);
    };
    var Wa = {};
    Wa.applyBypass = function(t, e, r, a) {
      var n = this, i = [], s = !0;
      if (e === "*" || e === "**") {
        if (r !== void 0)
          for (var o = 0; o < n.properties.length; o++) {
            var l = n.properties[o], u = l.name, f = this.parse(u, r, !0);
            f && i.push(f);
          }
      } else if (ee(e)) {
        var h = this.parse(e, r, !0);
        h && i.push(h);
      } else if (S(e)) {
        var c = e;
        a = r;
        for (var v = Object.keys(c), d = 0; d < v.length; d++) {
          var g = v[d], y = c[g];
          if (y === void 0 && (y = c[pt(g)]), y !== void 0) {
            var p = this.parse(g, y, !0);
            p && i.push(p);
          }
        }
      } else
        return !1;
      if (i.length === 0)
        return !1;
      for (var m = !1, b = 0; b < t.length; b++) {
        for (var E = t[b], M = {}, O = void 0, x = 0; x < i.length; x++) {
          var I = i[x];
          if (a) {
            var C = E.pstyle(I.name);
            O = M[I.name] = {
              prev: C
            };
          }
          m = this.applyParsedProperty(E, or(I)) || m, a && (O.next = E.pstyle(I.name));
        }
        m && this.updateStyleHints(E), a && this.updateTransitions(E, M, s);
      }
      return m;
    }, Wa.overrideBypass = function(t, e, r) {
      e = je(e);
      for (var a = 0; a < t.length; a++) {
        var n = t[a], i = n._private.style[e], s = this.properties[e].type, o = s.color, l = s.mutiple, u = i ? i.pfValue != null ? i.pfValue : i.value : null;
        !i || !i.bypass ? this.applyBypass(n, e, r) : (i.value = r, i.pfValue != null && (i.pfValue = r), o ? i.strValue = "rgb(" + r.join(",") + ")" : l ? i.strValue = r.join(" ") : i.strValue = "" + r, this.updateStyleHints(n)), this.checkTriggers(n, e, u, r);
      }
    }, Wa.removeAllBypasses = function(t, e) {
      return this.removeBypasses(t, this.propertyNames, e);
    }, Wa.removeBypasses = function(t, e, r) {
      for (var a = !0, n = 0; n < t.length; n++) {
        for (var i = t[n], s = {}, o = 0; o < e.length; o++) {
          var l = e[o], u = this.properties[l], f = i.pstyle(u.name);
          if (!(!f || !f.bypass)) {
            var h = "", c = this.parse(l, h, !0), v = s[u.name] = {
              prev: f
            };
            this.applyParsedProperty(i, c), v.next = i.pstyle(u.name);
          }
        }
        this.updateStyleHints(i), r && this.updateTransitions(i, s, a);
      }
    };
    var ki = {};
    ki.getEmSizeInPixels = function() {
      var t = this.containerCss("font-size");
      return t != null ? parseFloat(t) : 1;
    }, ki.containerCss = function(t) {
      var e = this._private.cy, r = e.container();
      if (D && r && D.getComputedStyle)
        return D.getComputedStyle(r).getPropertyValue(t);
    };
    var lr = {};
    lr.getRenderedStyle = function(t, e) {
      return e ? this.getStylePropertyValue(t, e, !0) : this.getRawStyle(t, !0);
    }, lr.getRawStyle = function(t, e) {
      var r = this;
      if (t = t[0], t) {
        for (var a = {}, n = 0; n < r.properties.length; n++) {
          var i = r.properties[n], s = r.getStylePropertyValue(t, i.name, e);
          s != null && (a[i.name] = s, a[pt(i.name)] = s);
        }
        return a;
      }
    }, lr.getIndexedStyle = function(t, e, r, a) {
      var n = t.pstyle(e)[r][a];
      return n ?? t.cy().style().getDefaultProperty(e)[r][0];
    }, lr.getStylePropertyValue = function(t, e, r) {
      var a = this;
      if (t = t[0], t) {
        var n = a.properties[e];
        n.alias && (n = n.pointsTo);
        var i = n.type, s = t.pstyle(n.name);
        if (s) {
          var o = s.value, l = s.units, u = s.strValue;
          if (r && i.number && o != null && k(o)) {
            var f = t.cy().zoom(), h = function(y) {
              return y * f;
            }, c = function(y, p) {
              return h(y) + p;
            }, v = te(o), d = v ? l.every(function(g) {
              return g != null;
            }) : l != null;
            return d ? v ? o.map(function(g, y) {
              return c(g, l[y]);
            }).join(" ") : c(o, l) : v ? o.map(function(g) {
              return ee(g) ? g : "" + h(g);
            }).join(" ") : "" + h(o);
          } else if (u != null)
            return u;
        }
        return null;
      }
    }, lr.getAnimationStartStyle = function(t, e) {
      for (var r = {}, a = 0; a < e.length; a++) {
        var n = e[a], i = n.name, s = t.pstyle(i);
        s !== void 0 && (S(s) ? s = this.parse(i, s.strValue) : s = this.parse(i, s)), s && (r[i] = s);
      }
      return r;
    }, lr.getPropsList = function(t) {
      var e = this, r = [], a = t, n = e.properties;
      if (a)
        for (var i = Object.keys(a), s = 0; s < i.length; s++) {
          var o = i[s], l = a[o], u = n[o] || n[je(o)], f = this.parse(u.name, l);
          f && r.push(f);
        }
      return r;
    }, lr.getNonDefaultPropertiesHash = function(t, e, r) {
      var a = r.slice(), n, i, s, o, l, u;
      for (l = 0; l < e.length; l++)
        if (n = e[l], i = t.pstyle(n, !1), i != null)
          if (i.pfValue != null)
            a[0] = Na(o, a[0]), a[1] = Ma(o, a[1]);
          else
            for (s = i.strValue, u = 0; u < s.length; u++)
              o = s.charCodeAt(u), a[0] = Na(o, a[0]), a[1] = Ma(o, a[1]);
      return a;
    }, lr.getPropertiesHash = lr.getNonDefaultPropertiesHash;
    var Vn = {};
    Vn.appendFromJson = function(t) {
      for (var e = this, r = 0; r < t.length; r++) {
        var a = t[r], n = a.selector, i = a.style || a.css, s = Object.keys(i);
        e.selector(n);
        for (var o = 0; o < s.length; o++) {
          var l = s[o], u = i[l];
          e.css(l, u);
        }
      }
      return e;
    }, Vn.fromJson = function(t) {
      var e = this;
      return e.resetToDefault(), e.appendFromJson(t), e;
    }, Vn.json = function() {
      for (var t = [], e = this.defaultLength; e < this.length; e++) {
        for (var r = this[e], a = r.selector, n = r.properties, i = {}, s = 0; s < n.length; s++) {
          var o = n[s];
          i[o.name] = o.strValue;
        }
        t.push({
          selector: a ? a.toString() : "core",
          style: i
        });
      }
      return t;
    };
    var Pi = {};
    Pi.appendFromString = function(t) {
      var e = this, r = this, a = "" + t, n, i, s;
      a = a.replace(/[/][*](\s|.)+?[*][/]/g, "");
      function o() {
        a.length > n.length ? a = a.substr(n.length) : a = "";
      }
      function l() {
        i.length > s.length ? i = i.substr(s.length) : i = "";
      }
      for (; ; ) {
        var u = a.match(/^\s*$/);
        if (u)
          break;
        var f = a.match(/^\s*((?:.|\s)+?)\s*\{((?:.|\s)+?)\}/);
        if (!f) {
          ft("Halting stylesheet parsing: String stylesheet contains more to parse but no selector and block found in: " + a);
          break;
        }
        n = f[0];
        var h = f[1];
        if (h !== "core") {
          var c = new Dr(h);
          if (c.invalid) {
            ft("Skipping parsing of block: Invalid selector found in string stylesheet: " + h), o();
            continue;
          }
        }
        var v = f[2], d = !1;
        i = v;
        for (var g = []; ; ) {
          var y = i.match(/^\s*$/);
          if (y)
            break;
          var p = i.match(/^\s*(.+?)\s*:\s*(.+?)(?:\s*;|\s*$)/);
          if (!p) {
            ft("Skipping parsing of block: Invalid formatting of style property and value definitions found in:" + v), d = !0;
            break;
          }
          s = p[0];
          var m = p[1], b = p[2], E = e.properties[m];
          if (!E) {
            ft("Skipping property: Invalid property name in: " + s), l();
            continue;
          }
          var M = r.parse(m, b);
          if (!M) {
            ft("Skipping property: Invalid property definition in: " + s), l();
            continue;
          }
          g.push({
            name: m,
            val: b
          }), l();
        }
        if (d) {
          o();
          break;
        }
        r.selector(h);
        for (var O = 0; O < g.length; O++) {
          var x = g[O];
          r.css(x.name, x.val);
        }
        o();
      }
      return r;
    }, Pi.fromString = function(t) {
      var e = this;
      return e.resetToDefault(), e.appendFromString(t), e;
    };
    var Nt = {};
    (function() {
      var t = vt, e = qt, r = Kr, a = Da, n = jt, i = function(xe) {
        return "^" + xe + "\\s*\\(\\s*([\\w\\.]+)\\s*\\)$";
      }, s = function(xe) {
        var Ce = t + "|\\w+|" + e + "|" + r + "|" + a + "|" + n;
        return "^" + xe + "\\s*\\(([\\w\\.]+)\\s*\\,\\s*(" + t + ")\\s*\\,\\s*(" + t + ")\\s*,\\s*(" + Ce + ")\\s*\\,\\s*(" + Ce + ")\\)$";
      }, o = [`^url\\s*\\(\\s*['"]?(.+?)['"]?\\s*\\)$`, "^(none)$", "^(.+)$"];
      Nt.types = {
        time: {
          number: !0,
          min: 0,
          units: "s|ms",
          implicitUnits: "ms"
        },
        percent: {
          number: !0,
          min: 0,
          max: 100,
          units: "%",
          implicitUnits: "%"
        },
        percentages: {
          number: !0,
          min: 0,
          max: 100,
          units: "%",
          implicitUnits: "%",
          multiple: !0
        },
        zeroOneNumber: {
          number: !0,
          min: 0,
          max: 1,
          unitless: !0
        },
        zeroOneNumbers: {
          number: !0,
          min: 0,
          max: 1,
          unitless: !0,
          multiple: !0
        },
        nOneOneNumber: {
          number: !0,
          min: -1,
          max: 1,
          unitless: !0
        },
        nonNegativeInt: {
          number: !0,
          min: 0,
          integer: !0,
          unitless: !0
        },
        position: {
          enums: ["parent", "origin"]
        },
        nodeSize: {
          number: !0,
          min: 0,
          enums: ["label"]
        },
        number: {
          number: !0,
          unitless: !0
        },
        numbers: {
          number: !0,
          unitless: !0,
          multiple: !0
        },
        positiveNumber: {
          number: !0,
          unitless: !0,
          min: 0,
          strictMin: !0
        },
        size: {
          number: !0,
          min: 0
        },
        bidirectionalSize: {
          number: !0
        },
        // allows negative
        bidirectionalSizeMaybePercent: {
          number: !0,
          allowPercent: !0
        },
        // allows negative
        bidirectionalSizes: {
          number: !0,
          multiple: !0
        },
        // allows negative
        sizeMaybePercent: {
          number: !0,
          min: 0,
          allowPercent: !0
        },
        axisDirection: {
          enums: ["horizontal", "leftward", "rightward", "vertical", "upward", "downward", "auto"]
        },
        paddingRelativeTo: {
          enums: ["width", "height", "average", "min", "max"]
        },
        bgWH: {
          number: !0,
          min: 0,
          allowPercent: !0,
          enums: ["auto"],
          multiple: !0
        },
        bgPos: {
          number: !0,
          allowPercent: !0,
          multiple: !0
        },
        bgRelativeTo: {
          enums: ["inner", "include-padding"],
          multiple: !0
        },
        bgRepeat: {
          enums: ["repeat", "repeat-x", "repeat-y", "no-repeat"],
          multiple: !0
        },
        bgFit: {
          enums: ["none", "contain", "cover"],
          multiple: !0
        },
        bgCrossOrigin: {
          enums: ["anonymous", "use-credentials"],
          multiple: !0
        },
        bgClip: {
          enums: ["none", "node"],
          multiple: !0
        },
        bgContainment: {
          enums: ["inside", "over"],
          multiple: !0
        },
        color: {
          color: !0
        },
        colors: {
          color: !0,
          multiple: !0
        },
        fill: {
          enums: ["solid", "linear-gradient", "radial-gradient"]
        },
        bool: {
          enums: ["yes", "no"]
        },
        bools: {
          enums: ["yes", "no"],
          multiple: !0
        },
        lineStyle: {
          enums: ["solid", "dotted", "dashed"]
        },
        lineCap: {
          enums: ["butt", "round", "square"]
        },
        borderStyle: {
          enums: ["solid", "dotted", "dashed", "double"]
        },
        curveStyle: {
          enums: ["bezier", "unbundled-bezier", "haystack", "segments", "straight", "straight-triangle", "taxi"]
        },
        fontFamily: {
          regex: '^([\\w- \\"]+(?:\\s*,\\s*[\\w- \\"]+)*)$'
        },
        fontStyle: {
          enums: ["italic", "normal", "oblique"]
        },
        fontWeight: {
          enums: ["normal", "bold", "bolder", "lighter", "100", "200", "300", "400", "500", "600", "800", "900", 100, 200, 300, 400, 500, 600, 700, 800, 900]
        },
        textDecoration: {
          enums: ["none", "underline", "overline", "line-through"]
        },
        textTransform: {
          enums: ["none", "uppercase", "lowercase"]
        },
        textWrap: {
          enums: ["none", "wrap", "ellipsis"]
        },
        textOverflowWrap: {
          enums: ["whitespace", "anywhere"]
        },
        textBackgroundShape: {
          enums: ["rectangle", "roundrectangle", "round-rectangle"]
        },
        nodeShape: {
          enums: ["rectangle", "roundrectangle", "round-rectangle", "cutrectangle", "cut-rectangle", "bottomroundrectangle", "bottom-round-rectangle", "barrel", "ellipse", "triangle", "round-triangle", "square", "pentagon", "round-pentagon", "hexagon", "round-hexagon", "concavehexagon", "concave-hexagon", "heptagon", "round-heptagon", "octagon", "round-octagon", "tag", "round-tag", "star", "diamond", "round-diamond", "vee", "rhomboid", "polygon"]
        },
        overlayShape: {
          enums: ["roundrectangle", "round-rectangle", "ellipse"]
        },
        compoundIncludeLabels: {
          enums: ["include", "exclude"]
        },
        arrowShape: {
          enums: ["tee", "triangle", "triangle-tee", "circle-triangle", "triangle-cross", "triangle-backcurve", "vee", "square", "circle", "diamond", "chevron", "none"]
        },
        arrowFill: {
          enums: ["filled", "hollow"]
        },
        display: {
          enums: ["element", "none"]
        },
        visibility: {
          enums: ["hidden", "visible"]
        },
        zCompoundDepth: {
          enums: ["bottom", "orphan", "auto", "top"]
        },
        zIndexCompare: {
          enums: ["auto", "manual"]
        },
        valign: {
          enums: ["top", "center", "bottom"]
        },
        halign: {
          enums: ["left", "center", "right"]
        },
        justification: {
          enums: ["left", "center", "right", "auto"]
        },
        text: {
          string: !0
        },
        data: {
          mapping: !0,
          regex: i("data")
        },
        layoutData: {
          mapping: !0,
          regex: i("layoutData")
        },
        scratch: {
          mapping: !0,
          regex: i("scratch")
        },
        mapData: {
          mapping: !0,
          regex: s("mapData")
        },
        mapLayoutData: {
          mapping: !0,
          regex: s("mapLayoutData")
        },
        mapScratch: {
          mapping: !0,
          regex: s("mapScratch")
        },
        fn: {
          mapping: !0,
          fn: !0
        },
        url: {
          regexes: o,
          singleRegexMatchValue: !0
        },
        urls: {
          regexes: o,
          singleRegexMatchValue: !0,
          multiple: !0
        },
        propList: {
          propList: !0
        },
        angle: {
          number: !0,
          units: "deg|rad",
          implicitUnits: "rad"
        },
        textRotation: {
          number: !0,
          units: "deg|rad",
          implicitUnits: "rad",
          enums: ["none", "autorotate"]
        },
        polygonPointList: {
          number: !0,
          multiple: !0,
          evenMultiple: !0,
          min: -1,
          max: 1,
          unitless: !0
        },
        edgeDistances: {
          enums: ["intersection", "node-position"]
        },
        edgeEndpoint: {
          number: !0,
          multiple: !0,
          units: "%|px|em|deg|rad",
          implicitUnits: "px",
          enums: ["inside-to-node", "outside-to-node", "outside-to-node-or-label", "outside-to-line", "outside-to-line-or-label"],
          singleEnum: !0,
          validate: function(xe, Ce) {
            switch (xe.length) {
              case 2:
                return Ce[0] !== "deg" && Ce[0] !== "rad" && Ce[1] !== "deg" && Ce[1] !== "rad";
              case 1:
                return ee(xe[0]) || Ce[0] === "deg" || Ce[0] === "rad";
              default:
                return !1;
            }
          }
        },
        easing: {
          regexes: ["^(spring)\\s*\\(\\s*(" + t + ")\\s*,\\s*(" + t + ")\\s*\\)$", "^(cubic-bezier)\\s*\\(\\s*(" + t + ")\\s*,\\s*(" + t + ")\\s*,\\s*(" + t + ")\\s*,\\s*(" + t + ")\\s*\\)$"],
          enums: ["linear", "ease", "ease-in", "ease-out", "ease-in-out", "ease-in-sine", "ease-out-sine", "ease-in-out-sine", "ease-in-quad", "ease-out-quad", "ease-in-out-quad", "ease-in-cubic", "ease-out-cubic", "ease-in-out-cubic", "ease-in-quart", "ease-out-quart", "ease-in-out-quart", "ease-in-quint", "ease-out-quint", "ease-in-out-quint", "ease-in-expo", "ease-out-expo", "ease-in-out-expo", "ease-in-circ", "ease-out-circ", "ease-in-out-circ"]
        },
        gradientDirection: {
          enums: [
            "to-bottom",
            "to-top",
            "to-left",
            "to-right",
            "to-bottom-right",
            "to-bottom-left",
            "to-top-right",
            "to-top-left",
            "to-right-bottom",
            "to-left-bottom",
            "to-right-top",
            "to-left-top"
            // different order
          ]
        },
        boundsExpansion: {
          number: !0,
          multiple: !0,
          min: 0,
          validate: function(xe) {
            var Ce = xe.length;
            return Ce === 1 || Ce === 2 || Ce === 4;
          }
        }
      };
      var l = {
        zeroNonZero: function(xe, Ce) {
          return (xe == null || Ce == null) && xe !== Ce || xe == 0 && Ce != 0 ? !0 : xe != 0 && Ce == 0;
        },
        any: function(xe, Ce) {
          return xe != Ce;
        },
        emptyNonEmpty: function(xe, Ce) {
          var Oe = Pe(xe), Ie = Pe(Ce);
          return Oe && !Ie || !Oe && Ie;
        }
      }, u = Nt.types, f = [{
        name: "label",
        type: u.text,
        triggersBounds: l.any,
        triggersZOrder: l.emptyNonEmpty
      }, {
        name: "text-rotation",
        type: u.textRotation,
        triggersBounds: l.any
      }, {
        name: "text-margin-x",
        type: u.bidirectionalSize,
        triggersBounds: l.any
      }, {
        name: "text-margin-y",
        type: u.bidirectionalSize,
        triggersBounds: l.any
      }], h = [{
        name: "source-label",
        type: u.text,
        triggersBounds: l.any
      }, {
        name: "source-text-rotation",
        type: u.textRotation,
        triggersBounds: l.any
      }, {
        name: "source-text-margin-x",
        type: u.bidirectionalSize,
        triggersBounds: l.any
      }, {
        name: "source-text-margin-y",
        type: u.bidirectionalSize,
        triggersBounds: l.any
      }, {
        name: "source-text-offset",
        type: u.size,
        triggersBounds: l.any
      }], c = [{
        name: "target-label",
        type: u.text,
        triggersBounds: l.any
      }, {
        name: "target-text-rotation",
        type: u.textRotation,
        triggersBounds: l.any
      }, {
        name: "target-text-margin-x",
        type: u.bidirectionalSize,
        triggersBounds: l.any
      }, {
        name: "target-text-margin-y",
        type: u.bidirectionalSize,
        triggersBounds: l.any
      }, {
        name: "target-text-offset",
        type: u.size,
        triggersBounds: l.any
      }], v = [{
        name: "font-family",
        type: u.fontFamily,
        triggersBounds: l.any
      }, {
        name: "font-style",
        type: u.fontStyle,
        triggersBounds: l.any
      }, {
        name: "font-weight",
        type: u.fontWeight,
        triggersBounds: l.any
      }, {
        name: "font-size",
        type: u.size,
        triggersBounds: l.any
      }, {
        name: "text-transform",
        type: u.textTransform,
        triggersBounds: l.any
      }, {
        name: "text-wrap",
        type: u.textWrap,
        triggersBounds: l.any
      }, {
        name: "text-overflow-wrap",
        type: u.textOverflowWrap,
        triggersBounds: l.any
      }, {
        name: "text-max-width",
        type: u.size,
        triggersBounds: l.any
      }, {
        name: "text-outline-width",
        type: u.size,
        triggersBounds: l.any
      }, {
        name: "line-height",
        type: u.positiveNumber,
        triggersBounds: l.any
      }], d = [{
        name: "text-valign",
        type: u.valign,
        triggersBounds: l.any
      }, {
        name: "text-halign",
        type: u.halign,
        triggersBounds: l.any
      }, {
        name: "color",
        type: u.color
      }, {
        name: "text-outline-color",
        type: u.color
      }, {
        name: "text-outline-opacity",
        type: u.zeroOneNumber
      }, {
        name: "text-background-color",
        type: u.color
      }, {
        name: "text-background-opacity",
        type: u.zeroOneNumber
      }, {
        name: "text-background-padding",
        type: u.size,
        triggersBounds: l.any
      }, {
        name: "text-border-opacity",
        type: u.zeroOneNumber
      }, {
        name: "text-border-color",
        type: u.color
      }, {
        name: "text-border-width",
        type: u.size,
        triggersBounds: l.any
      }, {
        name: "text-border-style",
        type: u.borderStyle,
        triggersBounds: l.any
      }, {
        name: "text-background-shape",
        type: u.textBackgroundShape,
        triggersBounds: l.any
      }, {
        name: "text-justification",
        type: u.justification
      }], g = [{
        name: "events",
        type: u.bool
      }, {
        name: "text-events",
        type: u.bool
      }], y = [{
        name: "display",
        type: u.display,
        triggersZOrder: l.any,
        triggersBounds: l.any,
        triggersBoundsOfParallelBeziers: !0
      }, {
        name: "visibility",
        type: u.visibility,
        triggersZOrder: l.any
      }, {
        name: "opacity",
        type: u.zeroOneNumber,
        triggersZOrder: l.zeroNonZero
      }, {
        name: "text-opacity",
        type: u.zeroOneNumber
      }, {
        name: "min-zoomed-font-size",
        type: u.size
      }, {
        name: "z-compound-depth",
        type: u.zCompoundDepth,
        triggersZOrder: l.any
      }, {
        name: "z-index-compare",
        type: u.zIndexCompare,
        triggersZOrder: l.any
      }, {
        name: "z-index",
        type: u.nonNegativeInt,
        triggersZOrder: l.any
      }], p = [{
        name: "overlay-padding",
        type: u.size,
        triggersBounds: l.any
      }, {
        name: "overlay-color",
        type: u.color
      }, {
        name: "overlay-opacity",
        type: u.zeroOneNumber,
        triggersBounds: l.zeroNonZero
      }, {
        name: "overlay-shape",
        type: u.overlayShape,
        triggersBounds: l.any
      }], m = [{
        name: "underlay-padding",
        type: u.size,
        triggersBounds: l.any
      }, {
        name: "underlay-color",
        type: u.color
      }, {
        name: "underlay-opacity",
        type: u.zeroOneNumber,
        triggersBounds: l.zeroNonZero
      }, {
        name: "underlay-shape",
        type: u.overlayShape,
        triggersBounds: l.any
      }], b = [{
        name: "transition-property",
        type: u.propList
      }, {
        name: "transition-duration",
        type: u.time
      }, {
        name: "transition-delay",
        type: u.time
      }, {
        name: "transition-timing-function",
        type: u.easing
      }], E = function(xe, Ce) {
        return Ce.value === "label" ? -xe.poolIndex() : Ce.pfValue;
      }, M = [{
        name: "height",
        type: u.nodeSize,
        triggersBounds: l.any,
        hashOverride: E
      }, {
        name: "width",
        type: u.nodeSize,
        triggersBounds: l.any,
        hashOverride: E
      }, {
        name: "shape",
        type: u.nodeShape,
        triggersBounds: l.any
      }, {
        name: "shape-polygon-points",
        type: u.polygonPointList,
        triggersBounds: l.any
      }, {
        name: "background-color",
        type: u.color
      }, {
        name: "background-fill",
        type: u.fill
      }, {
        name: "background-opacity",
        type: u.zeroOneNumber
      }, {
        name: "background-blacken",
        type: u.nOneOneNumber
      }, {
        name: "background-gradient-stop-colors",
        type: u.colors
      }, {
        name: "background-gradient-stop-positions",
        type: u.percentages
      }, {
        name: "background-gradient-direction",
        type: u.gradientDirection
      }, {
        name: "padding",
        type: u.sizeMaybePercent,
        triggersBounds: l.any
      }, {
        name: "padding-relative-to",
        type: u.paddingRelativeTo,
        triggersBounds: l.any
      }, {
        name: "bounds-expansion",
        type: u.boundsExpansion,
        triggersBounds: l.any
      }], O = [{
        name: "border-color",
        type: u.color
      }, {
        name: "border-opacity",
        type: u.zeroOneNumber
      }, {
        name: "border-width",
        type: u.size,
        triggersBounds: l.any
      }, {
        name: "border-style",
        type: u.borderStyle
      }], x = [{
        name: "background-image",
        type: u.urls
      }, {
        name: "background-image-crossorigin",
        type: u.bgCrossOrigin
      }, {
        name: "background-image-opacity",
        type: u.zeroOneNumbers
      }, {
        name: "background-image-containment",
        type: u.bgContainment
      }, {
        name: "background-image-smoothing",
        type: u.bools
      }, {
        name: "background-position-x",
        type: u.bgPos
      }, {
        name: "background-position-y",
        type: u.bgPos
      }, {
        name: "background-width-relative-to",
        type: u.bgRelativeTo
      }, {
        name: "background-height-relative-to",
        type: u.bgRelativeTo
      }, {
        name: "background-repeat",
        type: u.bgRepeat
      }, {
        name: "background-fit",
        type: u.bgFit
      }, {
        name: "background-clip",
        type: u.bgClip
      }, {
        name: "background-width",
        type: u.bgWH
      }, {
        name: "background-height",
        type: u.bgWH
      }, {
        name: "background-offset-x",
        type: u.bgPos
      }, {
        name: "background-offset-y",
        type: u.bgPos
      }], I = [{
        name: "position",
        type: u.position,
        triggersBounds: l.any
      }, {
        name: "compound-sizing-wrt-labels",
        type: u.compoundIncludeLabels,
        triggersBounds: l.any
      }, {
        name: "min-width",
        type: u.size,
        triggersBounds: l.any
      }, {
        name: "min-width-bias-left",
        type: u.sizeMaybePercent,
        triggersBounds: l.any
      }, {
        name: "min-width-bias-right",
        type: u.sizeMaybePercent,
        triggersBounds: l.any
      }, {
        name: "min-height",
        type: u.size,
        triggersBounds: l.any
      }, {
        name: "min-height-bias-top",
        type: u.sizeMaybePercent,
        triggersBounds: l.any
      }, {
        name: "min-height-bias-bottom",
        type: u.sizeMaybePercent,
        triggersBounds: l.any
      }], C = [{
        name: "line-style",
        type: u.lineStyle
      }, {
        name: "line-color",
        type: u.color
      }, {
        name: "line-fill",
        type: u.fill
      }, {
        name: "line-cap",
        type: u.lineCap
      }, {
        name: "line-opacity",
        type: u.zeroOneNumber
      }, {
        name: "line-dash-pattern",
        type: u.numbers
      }, {
        name: "line-dash-offset",
        type: u.number
      }, {
        name: "line-gradient-stop-colors",
        type: u.colors
      }, {
        name: "line-gradient-stop-positions",
        type: u.percentages
      }, {
        name: "curve-style",
        type: u.curveStyle,
        triggersBounds: l.any,
        triggersBoundsOfParallelBeziers: !0
      }, {
        name: "haystack-radius",
        type: u.zeroOneNumber,
        triggersBounds: l.any
      }, {
        name: "source-endpoint",
        type: u.edgeEndpoint,
        triggersBounds: l.any
      }, {
        name: "target-endpoint",
        type: u.edgeEndpoint,
        triggersBounds: l.any
      }, {
        name: "control-point-step-size",
        type: u.size,
        triggersBounds: l.any
      }, {
        name: "control-point-distances",
        type: u.bidirectionalSizes,
        triggersBounds: l.any
      }, {
        name: "control-point-weights",
        type: u.numbers,
        triggersBounds: l.any
      }, {
        name: "segment-distances",
        type: u.bidirectionalSizes,
        triggersBounds: l.any
      }, {
        name: "segment-weights",
        type: u.numbers,
        triggersBounds: l.any
      }, {
        name: "taxi-turn",
        type: u.bidirectionalSizeMaybePercent,
        triggersBounds: l.any
      }, {
        name: "taxi-turn-min-distance",
        type: u.size,
        triggersBounds: l.any
      }, {
        name: "taxi-direction",
        type: u.axisDirection,
        triggersBounds: l.any
      }, {
        name: "edge-distances",
        type: u.edgeDistances,
        triggersBounds: l.any
      }, {
        name: "arrow-scale",
        type: u.positiveNumber,
        triggersBounds: l.any
      }, {
        name: "loop-direction",
        type: u.angle,
        triggersBounds: l.any
      }, {
        name: "loop-sweep",
        type: u.angle,
        triggersBounds: l.any
      }, {
        name: "source-distance-from-node",
        type: u.size,
        triggersBounds: l.any
      }, {
        name: "target-distance-from-node",
        type: u.size,
        triggersBounds: l.any
      }], B = [{
        name: "ghost",
        type: u.bool,
        triggersBounds: l.any
      }, {
        name: "ghost-offset-x",
        type: u.bidirectionalSize,
        triggersBounds: l.any
      }, {
        name: "ghost-offset-y",
        type: u.bidirectionalSize,
        triggersBounds: l.any
      }, {
        name: "ghost-opacity",
        type: u.zeroOneNumber
      }], F = [{
        name: "selection-box-color",
        type: u.color
      }, {
        name: "selection-box-opacity",
        type: u.zeroOneNumber
      }, {
        name: "selection-box-border-color",
        type: u.color
      }, {
        name: "selection-box-border-width",
        type: u.size
      }, {
        name: "active-bg-color",
        type: u.color
      }, {
        name: "active-bg-opacity",
        type: u.zeroOneNumber
      }, {
        name: "active-bg-size",
        type: u.size
      }, {
        name: "outside-texture-bg-color",
        type: u.color
      }, {
        name: "outside-texture-bg-opacity",
        type: u.zeroOneNumber
      }], R = [];
      Nt.pieBackgroundN = 16, R.push({
        name: "pie-size",
        type: u.sizeMaybePercent
      });
      for (var X = 1; X <= Nt.pieBackgroundN; X++)
        R.push({
          name: "pie-" + X + "-background-color",
          type: u.color
        }), R.push({
          name: "pie-" + X + "-background-size",
          type: u.percent
        }), R.push({
          name: "pie-" + X + "-background-opacity",
          type: u.zeroOneNumber
        });
      var z = [], re = Nt.arrowPrefixes = ["source", "mid-source", "target", "mid-target"];
      [{
        name: "arrow-shape",
        type: u.arrowShape,
        triggersBounds: l.any
      }, {
        name: "arrow-color",
        type: u.color
      }, {
        name: "arrow-fill",
        type: u.arrowFill
      }].forEach(function(ae) {
        re.forEach(function(xe) {
          var Ce = xe + "-" + ae.name, Oe = ae.type, Ie = ae.triggersBounds;
          z.push({
            name: Ce,
            type: Oe,
            triggersBounds: Ie
          });
        });
      }, {});
      var W = Nt.properties = [].concat(g, b, y, p, m, B, d, v, f, h, c, M, O, x, R, I, C, z, F), Z = Nt.propertyGroups = {
        // common to all eles
        behavior: g,
        transition: b,
        visibility: y,
        overlay: p,
        underlay: m,
        ghost: B,
        // labels
        commonLabel: d,
        labelDimensions: v,
        mainLabel: f,
        sourceLabel: h,
        targetLabel: c,
        // node props
        nodeBody: M,
        nodeBorder: O,
        backgroundImage: x,
        pie: R,
        compound: I,
        // edge props
        edgeLine: C,
        edgeArrow: z,
        core: F
      }, ie = Nt.propertyGroupNames = {}, oe = Nt.propertyGroupKeys = Object.keys(Z);
      oe.forEach(function(ae) {
        ie[ae] = Z[ae].map(function(xe) {
          return xe.name;
        }), Z[ae].forEach(function(xe) {
          return xe.groupKey = ae;
        });
      });
      var ge = Nt.aliases = [{
        name: "content",
        pointsTo: "label"
      }, {
        name: "control-point-distance",
        pointsTo: "control-point-distances"
      }, {
        name: "control-point-weight",
        pointsTo: "control-point-weights"
      }, {
        name: "edge-text-rotation",
        pointsTo: "text-rotation"
      }, {
        name: "padding-left",
        pointsTo: "padding"
      }, {
        name: "padding-right",
        pointsTo: "padding"
      }, {
        name: "padding-top",
        pointsTo: "padding"
      }, {
        name: "padding-bottom",
        pointsTo: "padding"
      }];
      Nt.propertyNames = W.map(function(ae) {
        return ae.name;
      });
      for (var se = 0; se < W.length; se++) {
        var de = W[se];
        W[de.name] = de;
      }
      for (var we = 0; we < ge.length; we++) {
        var Te = ge[we], Ee = W[Te.pointsTo], ye = {
          name: Te.name,
          alias: !0,
          pointsTo: Ee
        };
        W.push(ye), W[Te.name] = ye;
      }
    })(), Nt.getDefaultProperty = function(t) {
      return this.getDefaultProperties()[t];
    }, Nt.getDefaultProperties = function() {
      var t = this._private;
      if (t.defaultProperties != null)
        return t.defaultProperties;
      for (var e = Ue({
        // core props
        "selection-box-color": "#ddd",
        "selection-box-opacity": 0.65,
        "selection-box-border-color": "#aaa",
        "selection-box-border-width": 1,
        "active-bg-color": "black",
        "active-bg-opacity": 0.15,
        "active-bg-size": 30,
        "outside-texture-bg-color": "#000",
        "outside-texture-bg-opacity": 0.125,
        // common node/edge props
        events: "yes",
        "text-events": "no",
        "text-valign": "top",
        "text-halign": "center",
        "text-justification": "auto",
        "line-height": 1,
        color: "#000",
        "text-outline-color": "#000",
        "text-outline-width": 0,
        "text-outline-opacity": 1,
        "text-opacity": 1,
        "text-decoration": "none",
        "text-transform": "none",
        "text-wrap": "none",
        "text-overflow-wrap": "whitespace",
        "text-max-width": 9999,
        "text-background-color": "#000",
        "text-background-opacity": 0,
        "text-background-shape": "rectangle",
        "text-background-padding": 0,
        "text-border-opacity": 0,
        "text-border-width": 0,
        "text-border-style": "solid",
        "text-border-color": "#000",
        "font-family": "Helvetica Neue, Helvetica, sans-serif",
        "font-style": "normal",
        "font-weight": "normal",
        "font-size": 16,
        "min-zoomed-font-size": 0,
        "text-rotation": "none",
        "source-text-rotation": "none",
        "target-text-rotation": "none",
        visibility: "visible",
        display: "element",
        opacity: 1,
        "z-compound-depth": "auto",
        "z-index-compare": "auto",
        "z-index": 0,
        label: "",
        "text-margin-x": 0,
        "text-margin-y": 0,
        "source-label": "",
        "source-text-offset": 0,
        "source-text-margin-x": 0,
        "source-text-margin-y": 0,
        "target-label": "",
        "target-text-offset": 0,
        "target-text-margin-x": 0,
        "target-text-margin-y": 0,
        "overlay-opacity": 0,
        "overlay-color": "#000",
        "overlay-padding": 10,
        "overlay-shape": "round-rectangle",
        "underlay-opacity": 0,
        "underlay-color": "#000",
        "underlay-padding": 10,
        "underlay-shape": "round-rectangle",
        "transition-property": "none",
        "transition-duration": 0,
        "transition-delay": 0,
        "transition-timing-function": "linear",
        // node props
        "background-blacken": 0,
        "background-color": "#999",
        "background-fill": "solid",
        "background-opacity": 1,
        "background-image": "none",
        "background-image-crossorigin": "anonymous",
        "background-image-opacity": 1,
        "background-image-containment": "inside",
        "background-image-smoothing": "yes",
        "background-position-x": "50%",
        "background-position-y": "50%",
        "background-offset-x": 0,
        "background-offset-y": 0,
        "background-width-relative-to": "include-padding",
        "background-height-relative-to": "include-padding",
        "background-repeat": "no-repeat",
        "background-fit": "none",
        "background-clip": "node",
        "background-width": "auto",
        "background-height": "auto",
        "border-color": "#000",
        "border-opacity": 1,
        "border-width": 0,
        "border-style": "solid",
        height: 30,
        width: 30,
        shape: "ellipse",
        "shape-polygon-points": "-1, -1,   1, -1,   1, 1,   -1, 1",
        "bounds-expansion": 0,
        // node gradient
        "background-gradient-direction": "to-bottom",
        "background-gradient-stop-colors": "#999",
        "background-gradient-stop-positions": "0%",
        // ghost props
        ghost: "no",
        "ghost-offset-y": 0,
        "ghost-offset-x": 0,
        "ghost-opacity": 0,
        // compound props
        padding: 0,
        "padding-relative-to": "width",
        position: "origin",
        "compound-sizing-wrt-labels": "include",
        "min-width": 0,
        "min-width-bias-left": 0,
        "min-width-bias-right": 0,
        "min-height": 0,
        "min-height-bias-top": 0,
        "min-height-bias-bottom": 0
      }, {
        // node pie bg
        "pie-size": "100%"
      }, [{
        name: "pie-{{i}}-background-color",
        value: "black"
      }, {
        name: "pie-{{i}}-background-size",
        value: "0%"
      }, {
        name: "pie-{{i}}-background-opacity",
        value: 1
      }].reduce(function(l, u) {
        for (var f = 1; f <= Nt.pieBackgroundN; f++) {
          var h = u.name.replace("{{i}}", f), c = u.value;
          l[h] = c;
        }
        return l;
      }, {}), {
        // edge props
        "line-style": "solid",
        "line-color": "#999",
        "line-fill": "solid",
        "line-cap": "butt",
        "line-opacity": 1,
        "line-gradient-stop-colors": "#999",
        "line-gradient-stop-positions": "0%",
        "control-point-step-size": 40,
        "control-point-weights": 0.5,
        "segment-weights": 0.5,
        "segment-distances": 20,
        "taxi-turn": "50%",
        "taxi-turn-min-distance": 10,
        "taxi-direction": "auto",
        "edge-distances": "intersection",
        "curve-style": "haystack",
        "haystack-radius": 0,
        "arrow-scale": 1,
        "loop-direction": "-45deg",
        "loop-sweep": "-90deg",
        "source-distance-from-node": 0,
        "target-distance-from-node": 0,
        "source-endpoint": "outside-to-node",
        "target-endpoint": "outside-to-node",
        "line-dash-pattern": [6, 3],
        "line-dash-offset": 0
      }, [{
        name: "arrow-shape",
        value: "none"
      }, {
        name: "arrow-color",
        value: "#999"
      }, {
        name: "arrow-fill",
        value: "filled"
      }].reduce(function(l, u) {
        return Nt.arrowPrefixes.forEach(function(f) {
          var h = f + "-" + u.name, c = u.value;
          l[h] = c;
        }), l;
      }, {})), r = {}, a = 0; a < this.properties.length; a++) {
        var n = this.properties[a];
        if (!n.pointsTo) {
          var i = n.name, s = e[i], o = this.parse(i, s);
          r[i] = o;
        }
      }
      return t.defaultProperties = r, t.defaultProperties;
    }, Nt.addDefaultStylesheet = function() {
      this.selector(":parent").css({
        shape: "rectangle",
        padding: 10,
        "background-color": "#eee",
        "border-color": "#ccc",
        "border-width": 1
      }).selector("edge").css({
        width: 3
      }).selector(":loop").css({
        "curve-style": "bezier"
      }).selector("edge:compound").css({
        "curve-style": "bezier",
        "source-endpoint": "outside-to-line",
        "target-endpoint": "outside-to-line"
      }).selector(":selected").css({
        "background-color": "#0169D9",
        "line-color": "#0169D9",
        "source-arrow-color": "#0169D9",
        "target-arrow-color": "#0169D9",
        "mid-source-arrow-color": "#0169D9",
        "mid-target-arrow-color": "#0169D9"
      }).selector(":parent:selected").css({
        "background-color": "#CCE1F9",
        "border-color": "#aec8e5"
      }).selector(":active").css({
        "overlay-color": "black",
        "overlay-padding": 10,
        "overlay-opacity": 0.25
      }), this.defaultLength = this.length;
    };
    var _n = {};
    _n.parse = function(t, e, r, a) {
      var n = this;
      if (H(e))
        return n.parseImplWarn(t, e, r, a);
      var i = a === "mapping" || a === !0 || a === !1 || a == null ? "dontcare" : a, s = r ? "t" : "f", o = "" + e, l = hs(t, o, s, i), u = n.propCache = n.propCache || [], f;
      return (f = u[l]) || (f = u[l] = n.parseImplWarn(t, e, r, a)), (r || a === "mapping") && (f = or(f), f && (f.value = or(f.value))), f;
    }, _n.parseImplWarn = function(t, e, r, a) {
      var n = this.parseImpl(t, e, r, a);
      return !n && e != null && ft("The style property `".concat(t, ": ").concat(e, "` is invalid")), n && (n.name === "width" || n.name === "height") && e === "label" && ft("The style value of `label` is deprecated for `" + n.name + "`"), n;
    }, _n.parseImpl = function(t, e, r, a) {
      var n = this;
      t = je(t);
      var i = n.properties[t], s = e, o = n.types;
      if (!i || e === void 0)
        return null;
      i.alias && (i = i.pointsTo, t = i.name);
      var l = ee(e);
      l && (e = e.trim());
      var u = i.type;
      if (!u)
        return null;
      if (r && (e === "" || e === null))
        return {
          name: t,
          value: e,
          bypass: !0,
          deleteBypass: !0
        };
      if (H(e))
        return {
          name: t,
          value: e,
          strValue: "fn",
          mapped: o.fn,
          bypass: r
        };
      var f, h;
      if (!(!l || a || e.length < 7 || e[1] !== "a")) {
        if (e.length >= 7 && e[0] === "d" && (f = new RegExp(o.data.regex).exec(e))) {
          if (r)
            return !1;
          var c = o.data;
          return {
            name: t,
            value: f,
            strValue: "" + e,
            mapped: c,
            field: f[1],
            bypass: r
          };
        } else if (e.length >= 10 && e[0] === "m" && (h = new RegExp(o.mapData.regex).exec(e))) {
          if (r || u.multiple)
            return !1;
          var v = o.mapData;
          if (!(u.color || u.number))
            return !1;
          var d = this.parse(t, h[4]);
          if (!d || d.mapped)
            return !1;
          var g = this.parse(t, h[5]);
          if (!g || g.mapped)
            return !1;
          if (d.pfValue === g.pfValue || d.strValue === g.strValue)
            return ft("`" + t + ": " + e + "` is not a valid mapper because the output range is zero; converting to `" + t + ": " + d.strValue + "`"), this.parse(t, d.strValue);
          if (u.color) {
            var y = d.value, p = g.value, m = y[0] === p[0] && y[1] === p[1] && y[2] === p[2] && // optional alpha
            (y[3] === p[3] || (y[3] == null || y[3] === 1) && (p[3] == null || p[3] === 1));
            if (m)
              return !1;
          }
          return {
            name: t,
            value: h,
            strValue: "" + e,
            mapped: v,
            field: h[1],
            fieldMin: parseFloat(h[2]),
            // min & max are numeric
            fieldMax: parseFloat(h[3]),
            valueMin: d.value,
            valueMax: g.value,
            bypass: r
          };
        }
      }
      if (u.multiple && a !== "multiple") {
        var b;
        if (l ? b = e.split(/\s+/) : te(e) ? b = e : b = [e], u.evenMultiple && b.length % 2 !== 0)
          return null;
        for (var E = [], M = [], O = [], x = "", I = !1, C = 0; C < b.length; C++) {
          var B = n.parse(t, b[C], r, "multiple");
          I = I || ee(B.value), E.push(B.value), O.push(B.pfValue != null ? B.pfValue : B.value), M.push(B.units), x += (C > 0 ? " " : "") + B.strValue;
        }
        return u.validate && !u.validate(E, M) ? null : u.singleEnum && I ? E.length === 1 && ee(E[0]) ? {
          name: t,
          value: E[0],
          strValue: E[0],
          bypass: r
        } : null : {
          name: t,
          value: E,
          pfValue: O,
          strValue: x,
          bypass: r,
          units: M
        };
      }
      var F = function() {
        for (var Ce = 0; Ce < u.enums.length; Ce++) {
          var Oe = u.enums[Ce];
          if (Oe === e)
            return {
              name: t,
              value: e,
              strValue: "" + e,
              bypass: r
            };
        }
        return null;
      };
      if (u.number) {
        var R, X = "px";
        if (u.units && (R = u.units), u.implicitUnits && (X = u.implicitUnits), !u.unitless)
          if (l) {
            var z = "px|em" + (u.allowPercent ? "|\\%" : "");
            R && (z = R);
            var re = e.match("^(" + vt + ")(" + z + ")?$");
            re && (e = re[1], R = re[2] || X);
          } else
            (!R || u.implicitUnits) && (R = X);
        if (e = parseFloat(e), isNaN(e) && u.enums === void 0)
          return null;
        if (isNaN(e) && u.enums !== void 0)
          return e = s, F();
        if (u.integer && !q(e) || u.min !== void 0 && (e < u.min || u.strictMin && e === u.min) || u.max !== void 0 && (e > u.max || u.strictMax && e === u.max))
          return null;
        var W = {
          name: t,
          value: e,
          strValue: "" + e + (R || ""),
          units: R,
          bypass: r
        };
        return u.unitless || R !== "px" && R !== "em" ? W.pfValue = e : W.pfValue = R === "px" || !R ? e : this.getEmSizeInPixels() * e, (R === "ms" || R === "s") && (W.pfValue = R === "ms" ? e : 1e3 * e), (R === "deg" || R === "rad") && (W.pfValue = R === "rad" ? e : Ef(e)), R === "%" && (W.pfValue = e / 100), W;
      } else if (u.propList) {
        var Z = [], ie = "" + e;
        if (ie !== "none") {
          for (var oe = ie.split(/\s*,\s*|\s+/), ge = 0; ge < oe.length; ge++) {
            var se = oe[ge].trim();
            n.properties[se] ? Z.push(se) : ft("`" + se + "` is not a valid property name");
          }
          if (Z.length === 0)
            return null;
        }
        return {
          name: t,
          value: Z,
          strValue: Z.length === 0 ? "none" : Z.join(" "),
          bypass: r
        };
      } else if (u.color) {
        var de = rl(e);
        return de ? {
          name: t,
          value: de,
          pfValue: de,
          strValue: "rgb(" + de[0] + "," + de[1] + "," + de[2] + ")",
          // n.b. no spaces b/c of multiple support
          bypass: r
        } : null;
      } else if (u.regex || u.regexes) {
        if (u.enums) {
          var we = F();
          if (we)
            return we;
        }
        for (var Te = u.regexes ? u.regexes : [u.regex], Ee = 0; Ee < Te.length; Ee++) {
          var ye = new RegExp(Te[Ee]), ae = ye.exec(e);
          if (ae)
            return {
              name: t,
              value: u.singleRegexMatchValue ? ae[1] : ae,
              strValue: "" + e,
              bypass: r
            };
        }
        return null;
      } else
        return u.string ? {
          name: t,
          value: "" + e,
          strValue: "" + e,
          bypass: r
        } : u.enums ? F() : null;
    };
    var Ft = function t(e) {
      if (!(this instanceof t))
        return new t(e);
      if (!_e(e)) {
        xt("A style must have a core reference");
        return;
      }
      this._private = {
        cy: e,
        coreStyle: {}
      }, this.length = 0, this.resetToDefault();
    }, zt = Ft.prototype;
    zt.instanceString = function() {
      return "style";
    }, zt.clear = function() {
      for (var t = this._private, e = t.cy, r = e.elements(), a = 0; a < this.length; a++)
        this[a] = void 0;
      return this.length = 0, t.contextStyles = {}, t.propDiffs = {}, this.cleanElements(r, !0), r.forEach(function(n) {
        var i = n[0]._private;
        i.styleDirty = !0, i.appliedInitStyle = !1;
      }), this;
    }, zt.resetToDefault = function() {
      return this.clear(), this.addDefaultStylesheet(), this;
    }, zt.core = function(t) {
      return this._private.coreStyle[t] || this.getDefaultProperty(t);
    }, zt.selector = function(t) {
      var e = t === "core" ? null : new Dr(t), r = this.length++;
      return this[r] = {
        selector: e,
        properties: [],
        mappedProperties: [],
        index: r
      }, this;
    }, zt.css = function() {
      var t = this, e = arguments;
      if (e.length === 1)
        for (var r = e[0], a = 0; a < t.properties.length; a++) {
          var n = t.properties[a], i = r[n.name];
          i === void 0 && (i = r[pt(n.name)]), i !== void 0 && this.cssRule(n.name, i);
        }
      else
        e.length === 2 && this.cssRule(e[0], e[1]);
      return this;
    }, zt.style = zt.css, zt.cssRule = function(t, e) {
      var r = this.parse(t, e);
      if (r) {
        var a = this.length - 1;
        this[a].properties.push(r), this[a].properties[r.name] = r, r.name.match(/pie-(\d+)-background-size/) && r.value && (this._private.hasPie = !0), r.mapped && this[a].mappedProperties.push(r);
        var n = !this[a].selector;
        n && (this._private.coreStyle[r.name] = r);
      }
      return this;
    }, zt.append = function(t) {
      return tt(t) ? t.appendToStyle(this) : te(t) ? this.appendFromJson(t) : ee(t) && this.appendFromString(t), this;
    }, Ft.fromJson = function(t, e) {
      var r = new Ft(t);
      return r.fromJson(e), r;
    }, Ft.fromString = function(t, e) {
      return new Ft(t).fromString(e);
    }, [Bt, Wa, ki, lr, Vn, Pi, Nt, _n].forEach(function(t) {
      Ue(zt, t);
    }), Ft.types = zt.types, Ft.properties = zt.properties, Ft.propertyGroups = zt.propertyGroups, Ft.propertyGroupNames = zt.propertyGroupNames, Ft.propertyGroupKeys = zt.propertyGroupKeys;
    var Gd = {
      style: function(e) {
        if (e) {
          var r = this.setStyle(e);
          r.update();
        }
        return this._private.style;
      },
      setStyle: function(e) {
        var r = this._private;
        return tt(e) ? r.style = e.generateStyle(this) : te(e) ? r.style = Ft.fromJson(this, e) : ee(e) ? r.style = Ft.fromString(this, e) : r.style = Ft(this), r.style;
      },
      // e.g. cy.data() changed => recalc ele mappers
      updateStyle: function() {
        this.mutableElements().updateStyle();
      }
    }, $d = "single", $r = {
      autolock: function(e) {
        if (e !== void 0)
          this._private.autolock = !!e;
        else
          return this._private.autolock;
        return this;
      },
      autoungrabify: function(e) {
        if (e !== void 0)
          this._private.autoungrabify = !!e;
        else
          return this._private.autoungrabify;
        return this;
      },
      autounselectify: function(e) {
        if (e !== void 0)
          this._private.autounselectify = !!e;
        else
          return this._private.autounselectify;
        return this;
      },
      selectionType: function(e) {
        var r = this._private;
        if (r.selectionType == null && (r.selectionType = $d), e !== void 0)
          (e === "additive" || e === "single") && (r.selectionType = e);
        else
          return r.selectionType;
        return this;
      },
      panningEnabled: function(e) {
        if (e !== void 0)
          this._private.panningEnabled = !!e;
        else
          return this._private.panningEnabled;
        return this;
      },
      userPanningEnabled: function(e) {
        if (e !== void 0)
          this._private.userPanningEnabled = !!e;
        else
          return this._private.userPanningEnabled;
        return this;
      },
      zoomingEnabled: function(e) {
        if (e !== void 0)
          this._private.zoomingEnabled = !!e;
        else
          return this._private.zoomingEnabled;
        return this;
      },
      userZoomingEnabled: function(e) {
        if (e !== void 0)
          this._private.userZoomingEnabled = !!e;
        else
          return this._private.userZoomingEnabled;
        return this;
      },
      boxSelectionEnabled: function(e) {
        if (e !== void 0)
          this._private.boxSelectionEnabled = !!e;
        else
          return this._private.boxSelectionEnabled;
        return this;
      },
      pan: function() {
        var e = arguments, r = this._private.pan, a, n, i, s, o;
        switch (e.length) {
          case 0:
            return r;
          case 1:
            if (ee(e[0]))
              return a = e[0], r[a];
            if (S(e[0])) {
              if (!this._private.panningEnabled)
                return this;
              i = e[0], s = i.x, o = i.y, k(s) && (r.x = s), k(o) && (r.y = o), this.emit("pan viewport");
            }
            break;
          case 2:
            if (!this._private.panningEnabled)
              return this;
            a = e[0], n = e[1], (a === "x" || a === "y") && k(n) && (r[a] = n), this.emit("pan viewport");
            break;
        }
        return this.notify("viewport"), this;
      },
      panBy: function(e, r) {
        var a = arguments, n = this._private.pan, i, s, o, l, u;
        if (!this._private.panningEnabled)
          return this;
        switch (a.length) {
          case 1:
            S(e) && (o = a[0], l = o.x, u = o.y, k(l) && (n.x += l), k(u) && (n.y += u), this.emit("pan viewport"));
            break;
          case 2:
            i = e, s = r, (i === "x" || i === "y") && k(s) && (n[i] += s), this.emit("pan viewport");
            break;
        }
        return this.notify("viewport"), this;
      },
      fit: function(e, r) {
        var a = this.getFitViewport(e, r);
        if (a) {
          var n = this._private;
          n.zoom = a.zoom, n.pan = a.pan, this.emit("pan zoom viewport"), this.notify("viewport");
        }
        return this;
      },
      getFitViewport: function(e, r) {
        if (k(e) && r === void 0 && (r = e, e = void 0), !(!this._private.panningEnabled || !this._private.zoomingEnabled)) {
          var a;
          if (ee(e)) {
            var n = e;
            e = this.$(n);
          } else if (Xe(e)) {
            var i = e;
            a = {
              x1: i.x1,
              y1: i.y1,
              x2: i.x2,
              y2: i.y2
            }, a.w = a.x2 - a.x1, a.h = a.y2 - a.y1;
          } else
            pe(e) || (e = this.mutableElements());
          if (!(pe(e) && e.empty())) {
            a = a || e.boundingBox();
            var s = this.width(), o = this.height(), l;
            if (r = k(r) ? r : 0, !isNaN(s) && !isNaN(o) && s > 0 && o > 0 && !isNaN(a.w) && !isNaN(a.h) && a.w > 0 && a.h > 0) {
              l = Math.min((s - 2 * r) / a.w, (o - 2 * r) / a.h), l = l > this._private.maxZoom ? this._private.maxZoom : l, l = l < this._private.minZoom ? this._private.minZoom : l;
              var u = {
                // now pan to middle
                x: (s - l * (a.x1 + a.x2)) / 2,
                y: (o - l * (a.y1 + a.y2)) / 2
              };
              return {
                zoom: l,
                pan: u
              };
            }
          }
        }
      },
      zoomRange: function(e, r) {
        var a = this._private;
        if (r == null) {
          var n = e;
          e = n.min, r = n.max;
        }
        return k(e) && k(r) && e <= r ? (a.minZoom = e, a.maxZoom = r) : k(e) && r === void 0 && e <= a.maxZoom ? a.minZoom = e : k(r) && e === void 0 && r >= a.minZoom && (a.maxZoom = r), this;
      },
      minZoom: function(e) {
        return e === void 0 ? this._private.minZoom : this.zoomRange({
          min: e
        });
      },
      maxZoom: function(e) {
        return e === void 0 ? this._private.maxZoom : this.zoomRange({
          max: e
        });
      },
      getZoomedViewport: function(e) {
        var r = this._private, a = r.pan, n = r.zoom, i, s, o = !1;
        if (r.zoomingEnabled || (o = !0), k(e) ? s = e : S(e) && (s = e.level, e.position != null ? i = gn(e.position, n, a) : e.renderedPosition != null && (i = e.renderedPosition), i != null && !r.panningEnabled && (o = !0)), s = s > r.maxZoom ? r.maxZoom : s, s = s < r.minZoom ? r.minZoom : s, o || !k(s) || s === n || i != null && (!k(i.x) || !k(i.y)))
          return null;
        if (i != null) {
          var l = a, u = n, f = s, h = {
            x: -f / u * (i.x - l.x) + i.x,
            y: -f / u * (i.y - l.y) + i.y
          };
          return {
            zoomed: !0,
            panned: !0,
            zoom: f,
            pan: h
          };
        } else
          return {
            zoomed: !0,
            panned: !1,
            zoom: s,
            pan: a
          };
      },
      zoom: function(e) {
        if (e === void 0)
          return this._private.zoom;
        var r = this.getZoomedViewport(e), a = this._private;
        return r == null || !r.zoomed ? this : (a.zoom = r.zoom, r.panned && (a.pan.x = r.pan.x, a.pan.y = r.pan.y), this.emit("zoom" + (r.panned ? " pan" : "") + " viewport"), this.notify("viewport"), this);
      },
      viewport: function(e) {
        var r = this._private, a = !0, n = !0, i = [], s = !1, o = !1;
        if (!e)
          return this;
        if (k(e.zoom) || (a = !1), S(e.pan) || (n = !1), !a && !n)
          return this;
        if (a) {
          var l = e.zoom;
          l < r.minZoom || l > r.maxZoom || !r.zoomingEnabled ? s = !0 : (r.zoom = l, i.push("zoom"));
        }
        if (n && (!s || !e.cancelOnFailedZoom) && r.panningEnabled) {
          var u = e.pan;
          k(u.x) && (r.pan.x = u.x, o = !1), k(u.y) && (r.pan.y = u.y, o = !1), o || i.push("pan");
        }
        return i.length > 0 && (i.push("viewport"), this.emit(i.join(" ")), this.notify("viewport")), this;
      },
      center: function(e) {
        var r = this.getCenterPan(e);
        return r && (this._private.pan = r, this.emit("pan viewport"), this.notify("viewport")), this;
      },
      getCenterPan: function(e, r) {
        if (this._private.panningEnabled) {
          if (ee(e)) {
            var a = e;
            e = this.mutableElements().filter(a);
          } else
            pe(e) || (e = this.mutableElements());
          if (e.length !== 0) {
            var n = e.boundingBox(), i = this.width(), s = this.height();
            r = r === void 0 ? this._private.zoom : r;
            var o = {
              // middle
              x: (i - r * (n.x1 + n.x2)) / 2,
              y: (s - r * (n.y1 + n.y2)) / 2
            };
            return o;
          }
        }
      },
      reset: function() {
        return !this._private.panningEnabled || !this._private.zoomingEnabled ? this : (this.viewport({
          pan: {
            x: 0,
            y: 0
          },
          zoom: 1
        }), this);
      },
      invalidateSize: function() {
        this._private.sizeCache = null;
      },
      size: function() {
        var e = this._private, r = e.container;
        return e.sizeCache = e.sizeCache || (r ? function() {
          var a = D.getComputedStyle(r), n = function(s) {
            return parseFloat(a.getPropertyValue(s));
          };
          return {
            width: r.clientWidth - n("padding-left") - n("padding-right"),
            height: r.clientHeight - n("padding-top") - n("padding-bottom")
          };
        }() : {
          // fallback if no container (not 0 b/c can be used for dividing etc)
          width: 1,
          height: 1
        });
      },
      width: function() {
        return this.size().width;
      },
      height: function() {
        return this.size().height;
      },
      extent: function() {
        var e = this._private.pan, r = this._private.zoom, a = this.renderedExtent(), n = {
          x1: (a.x1 - e.x) / r,
          x2: (a.x2 - e.x) / r,
          y1: (a.y1 - e.y) / r,
          y2: (a.y2 - e.y) / r
        };
        return n.w = n.x2 - n.x1, n.h = n.y2 - n.y1, n;
      },
      renderedExtent: function() {
        var e = this.width(), r = this.height();
        return {
          x1: 0,
          y1: 0,
          x2: e,
          y2: r,
          w: e,
          h: r
        };
      },
      multiClickDebounceTime: function(e) {
        if (e)
          this._private.multiClickDebounceTime = e;
        else
          return this._private.multiClickDebounceTime;
        return this;
      }
    };
    $r.centre = $r.center, $r.autolockNodes = $r.autolock, $r.autoungrabifyNodes = $r.autoungrabify;
    var Ka = {
      data: ht.data({
        field: "data",
        bindingEvent: "data",
        allowBinding: !0,
        allowSetting: !0,
        settingEvent: "data",
        settingTriggersEvent: !0,
        triggerFnName: "trigger",
        allowGetting: !0,
        updateStyle: !0
      }),
      removeData: ht.removeData({
        field: "data",
        event: "data",
        triggerFnName: "trigger",
        triggerEvent: !0,
        updateStyle: !0
      }),
      scratch: ht.data({
        field: "scratch",
        bindingEvent: "scratch",
        allowBinding: !0,
        allowSetting: !0,
        settingEvent: "scratch",
        settingTriggersEvent: !0,
        triggerFnName: "trigger",
        allowGetting: !0,
        updateStyle: !0
      }),
      removeScratch: ht.removeData({
        field: "scratch",
        event: "scratch",
        triggerFnName: "trigger",
        triggerEvent: !0,
        updateStyle: !0
      })
    };
    Ka.attr = Ka.data, Ka.removeAttr = Ka.removeData;
    var Za = function(e) {
      var r = this;
      e = Ue({}, e);
      var a = e.container;
      a && !ve(a) && ve(a[0]) && (a = a[0]);
      var n = a ? a._cyreg : null;
      n = n || {}, n && n.cy && (n.cy.destroy(), n = {});
      var i = n.readies = n.readies || [];
      a && (a._cyreg = n), n.cy = r;
      var s = D !== void 0 && a !== void 0 && !e.headless, o = e;
      o.layout = Ue({
        name: s ? "grid" : "null"
      }, o.layout), o.renderer = Ue({
        name: s ? "canvas" : "null"
      }, o.renderer);
      var l = function(d, g, y) {
        return g !== void 0 ? g : y !== void 0 ? y : d;
      }, u = this._private = {
        container: a,
        // html dom ele container
        ready: !1,
        // whether ready has been triggered
        options: o,
        // cached options
        elements: new Ot(this),
        // elements in the graph
        listeners: [],
        // list of listeners
        aniEles: new Ot(this),
        // elements being animated
        data: o.data || {},
        // data for the core
        scratch: {},
        // scratch object for core
        layout: null,
        renderer: null,
        destroyed: !1,
        // whether destroy was called
        notificationsEnabled: !0,
        // whether notifications are sent to the renderer
        minZoom: 1e-50,
        maxZoom: 1e50,
        zoomingEnabled: l(!0, o.zoomingEnabled),
        userZoomingEnabled: l(!0, o.userZoomingEnabled),
        panningEnabled: l(!0, o.panningEnabled),
        userPanningEnabled: l(!0, o.userPanningEnabled),
        boxSelectionEnabled: l(!0, o.boxSelectionEnabled),
        autolock: l(!1, o.autolock, o.autolockNodes),
        autoungrabify: l(!1, o.autoungrabify, o.autoungrabifyNodes),
        autounselectify: l(!1, o.autounselectify),
        styleEnabled: o.styleEnabled === void 0 ? s : o.styleEnabled,
        zoom: k(o.zoom) ? o.zoom : 1,
        pan: {
          x: S(o.pan) && k(o.pan.x) ? o.pan.x : 0,
          y: S(o.pan) && k(o.pan.y) ? o.pan.y : 0
        },
        animation: {
          // object for currently-running animations
          current: [],
          queue: []
        },
        hasCompoundNodes: !1,
        multiClickDebounceTime: l(250, o.multiClickDebounceTime)
      };
      this.createEmitter(), this.selectionType(o.selectionType), this.zoomRange({
        min: o.minZoom,
        max: o.maxZoom
      });
      var f = function(d, g) {
        var y = d.some(rt);
        if (y)
          return ia.all(d).then(g);
        g(d);
      };
      u.styleEnabled && r.setStyle([]);
      var h = Ue({}, o, o.renderer);
      r.initRenderer(h);
      var c = function(d, g, y) {
        r.notifications(!1);
        var p = r.mutableElements();
        p.length > 0 && p.remove(), d != null && (S(d) || te(d)) && r.add(d), r.one("layoutready", function(b) {
          r.notifications(!0), r.emit(b), r.one("load", g), r.emitAndNotify("load");
        }).one("layoutstop", function() {
          r.one("done", y), r.emit("done");
        });
        var m = Ue({}, r._private.options.layout);
        m.eles = r.elements(), r.layout(m).run();
      };
      f([o.style, o.elements], function(v) {
        var d = v[0], g = v[1];
        u.styleEnabled && r.style().append(d), c(g, function() {
          r.startAnimationLoop(), u.ready = !0, H(o.ready) && r.on("ready", o.ready);
          for (var y = 0; y < i.length; y++) {
            var p = i[y];
            r.on("ready", p);
          }
          n && (n.readies = []), r.emit("ready");
        }, o.done);
      });
    }, Un = Za.prototype;
    Ue(Un, {
      instanceString: function() {
        return "core";
      },
      isReady: function() {
        return this._private.ready;
      },
      destroyed: function() {
        return this._private.destroyed;
      },
      ready: function(e) {
        return this.isReady() ? this.emitter().emit("ready", [], e) : this.on("ready", e), this;
      },
      destroy: function() {
        var e = this;
        if (!e.destroyed())
          return e.stopAnimationLoop(), e.destroyRenderer(), this.emit("destroy"), e._private.destroyed = !0, e;
      },
      hasElementWithId: function(e) {
        return this._private.elements.hasElementWithId(e);
      },
      getElementById: function(e) {
        return this._private.elements.getElementById(e);
      },
      hasCompoundNodes: function() {
        return this._private.hasCompoundNodes;
      },
      headless: function() {
        return this._private.renderer.isHeadless();
      },
      styleEnabled: function() {
        return this._private.styleEnabled;
      },
      addToPool: function(e) {
        return this._private.elements.merge(e), this;
      },
      removeFromPool: function(e) {
        return this._private.elements.unmerge(e), this;
      },
      container: function() {
        return this._private.container || null;
      },
      mount: function(e) {
        if (e != null) {
          var r = this, a = r._private, n = a.options;
          return !ve(e) && ve(e[0]) && (e = e[0]), r.stopAnimationLoop(), r.destroyRenderer(), a.container = e, a.styleEnabled = !0, r.invalidateSize(), r.initRenderer(Ue({}, n, n.renderer, {
            // allow custom renderer name to be re-used, otherwise use canvas
            name: n.renderer.name === "null" ? "canvas" : n.renderer.name
          })), r.startAnimationLoop(), r.style(n.style), r.emit("mount"), r;
        }
      },
      unmount: function() {
        var e = this;
        return e.stopAnimationLoop(), e.destroyRenderer(), e.initRenderer({
          name: "null"
        }), e.emit("unmount"), e;
      },
      options: function() {
        return or(this._private.options);
      },
      json: function(e) {
        var r = this, a = r._private, n = r.mutableElements(), i = function(E) {
          return r.getElementById(E.id());
        };
        if (S(e)) {
          if (r.startBatch(), e.elements) {
            var s = {}, o = function(E, M) {
              for (var O = [], x = [], I = 0; I < E.length; I++) {
                var C = E[I];
                if (!C.data.id) {
                  ft("cy.json() cannot handle elements without an ID attribute");
                  continue;
                }
                var B = "" + C.data.id, F = r.getElementById(B);
                s[B] = !0, F.length !== 0 ? x.push({
                  ele: F,
                  json: C
                }) : (M && (C.group = M), O.push(C));
              }
              r.add(O);
              for (var R = 0; R < x.length; R++) {
                var X = x[R], z = X.ele, re = X.json;
                z.json(re);
              }
            };
            if (te(e.elements))
              o(e.elements);
            else
              for (var l = ["nodes", "edges"], u = 0; u < l.length; u++) {
                var f = l[u], h = e.elements[f];
                te(h) && o(h, f);
              }
            var c = r.collection();
            n.filter(function(b) {
              return !s[b.id()];
            }).forEach(function(b) {
              b.isParent() ? c.merge(b) : b.remove();
            }), c.forEach(function(b) {
              return b.children().move({
                parent: null
              });
            }), c.forEach(function(b) {
              return i(b).remove();
            });
          }
          e.style && r.style(e.style), e.zoom != null && e.zoom !== a.zoom && r.zoom(e.zoom), e.pan && (e.pan.x !== a.pan.x || e.pan.y !== a.pan.y) && r.pan(e.pan), e.data && r.data(e.data);
          for (var v = ["minZoom", "maxZoom", "zoomingEnabled", "userZoomingEnabled", "panningEnabled", "userPanningEnabled", "boxSelectionEnabled", "autolock", "autoungrabify", "autounselectify", "multiClickDebounceTime"], d = 0; d < v.length; d++) {
            var g = v[d];
            e[g] != null && r[g](e[g]);
          }
          return r.endBatch(), this;
        } else {
          var y = !!e, p = {};
          y ? p.elements = this.elements().map(function(b) {
            return b.json();
          }) : (p.elements = {}, n.forEach(function(b) {
            var E = b.group();
            p.elements[E] || (p.elements[E] = []), p.elements[E].push(b.json());
          })), this._private.styleEnabled && (p.style = r.style().json()), p.data = or(r.data());
          var m = a.options;
          return p.zoomingEnabled = a.zoomingEnabled, p.userZoomingEnabled = a.userZoomingEnabled, p.zoom = a.zoom, p.minZoom = a.minZoom, p.maxZoom = a.maxZoom, p.panningEnabled = a.panningEnabled, p.userPanningEnabled = a.userPanningEnabled, p.pan = or(a.pan), p.boxSelectionEnabled = a.boxSelectionEnabled, p.renderer = or(m.renderer), p.hideEdgesOnViewport = m.hideEdgesOnViewport, p.textureOnViewport = m.textureOnViewport, p.wheelSensitivity = m.wheelSensitivity, p.motionBlur = m.motionBlur, p.multiClickDebounceTime = m.multiClickDebounceTime, p;
        }
      }
    }), Un.$id = Un.getElementById, [Od, kd, Ho, Ii, Gn, Bd, Ri, $n, Gd, $r, Ka].forEach(function(t) {
      Ue(Un, t);
    });
    var Vd = {
      fit: !0,
      // whether to fit the viewport to the graph
      directed: !1,
      // whether the tree is directed downwards (or edges can point in any direction if false)
      padding: 30,
      // padding on fit
      circle: !1,
      // put depths in concentric circles if true, put depths top down if false
      grid: !1,
      // whether to create an even grid into which the DAG is placed (circle:false only)
      spacingFactor: 1.75,
      // positive spacing factor, larger => more space between nodes (N.B. n/a if causes overlap)
      boundingBox: void 0,
      // constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
      avoidOverlap: !0,
      // prevents node overlap, may overflow boundingBox if not enough space
      nodeDimensionsIncludeLabels: !1,
      // Excludes the label when calculating node bounding boxes for the layout algorithm
      roots: void 0,
      // the roots of the trees
      maximal: !1,
      // whether to shift nodes down their natural BFS depths in order to avoid upwards edges (DAGS only)
      depthSort: void 0,
      // a sorting function to order nodes at equal depth. e.g. function(a, b){ return a.data('weight') - b.data('weight') }
      animate: !1,
      // whether to transition the node positions
      animationDuration: 500,
      // duration of animation in ms if enabled
      animationEasing: void 0,
      // easing of animation if enabled,
      animateFilter: function(e, r) {
        return !0;
      },
      // a function that determines whether the node should be animated.  All nodes animated by default on animate enabled.  Non-animated nodes are positioned immediately when the layout starts
      ready: void 0,
      // callback on layoutready
      stop: void 0,
      // callback on layoutstop
      transform: function(e, r) {
        return r;
      }
      // transform a given node position. Useful for changing flow direction in discrete layouts
    }, pa = function(e) {
      return e.scratch("breadthfirst");
    }, Xo = function(e, r) {
      return e.scratch("breadthfirst", r);
    };
    function qo(t) {
      this.options = Ue({}, Vd, t);
    }
    qo.prototype.run = function() {
      var t = this.options, e = t, r = t.cy, a = e.eles, n = a.nodes().filter(function(Re) {
        return !Re.isParent();
      }), i = a, s = e.directed, o = e.maximal || e.maximalAdjustments > 0, l = Ut(e.boundingBox ? e.boundingBox : {
        x1: 0,
        y1: 0,
        w: r.width(),
        h: r.height()
      }), u;
      if (pe(e.roots))
        u = e.roots;
      else if (te(e.roots)) {
        for (var f = [], h = 0; h < e.roots.length; h++) {
          var c = e.roots[h], v = r.getElementById(c);
          f.push(v);
        }
        u = r.collection(f);
      } else if (ee(e.roots))
        u = r.$(e.roots);
      else if (s)
        u = n.roots();
      else {
        var d = a.components();
        u = r.collection();
        for (var g = function(Me) {
          var Ve = d[Me], Fe = Ve.maxDegree(!1), ke = Ve.filter(function(Ge) {
            return Ge.degree(!1) === Fe;
          });
          u = u.add(ke);
        }, y = 0; y < d.length; y++)
          g(y);
      }
      var p = [], m = {}, b = function(Me, Ve) {
        p[Ve] == null && (p[Ve] = []);
        var Fe = p[Ve].length;
        p[Ve].push(Me), Xo(Me, {
          index: Fe,
          depth: Ve
        });
      }, E = function(Me, Ve) {
        var Fe = pa(Me), ke = Fe.depth, Ge = Fe.index;
        p[ke][Ge] = null, b(Me, Ve);
      };
      i.bfs({
        roots: u,
        directed: e.directed,
        visit: function(Me, Ve, Fe, ke, Ge) {
          var et = Me[0], We = et.id();
          b(et, Ge), m[We] = !0;
        }
      });
      for (var M = [], O = 0; O < n.length; O++) {
        var x = n[O];
        m[x.id()] || M.push(x);
      }
      var I = function(Me) {
        for (var Ve = p[Me], Fe = 0; Fe < Ve.length; Fe++) {
          var ke = Ve[Fe];
          if (ke == null) {
            Ve.splice(Fe, 1), Fe--;
            continue;
          }
          Xo(ke, {
            depth: Me,
            index: Fe
          });
        }
      }, C = function() {
        for (var Me = 0; Me < p.length; Me++)
          I(Me);
      }, B = function(Me, Ve) {
        for (var Fe = pa(Me), ke = Me.incomers().filter(function(N) {
          return N.isNode() && a.has(N);
        }), Ge = -1, et = Me.id(), We = 0; We < ke.length; We++) {
          var Ye = ke[We], Se = pa(Ye);
          Ge = Math.max(Ge, Se.depth);
        }
        return Fe.depth <= Ge ? Ve[et] ? null : (E(Me, Ge + 1), Ve[et] = !0, !0) : !1;
      };
      if (s && o) {
        var F = [], R = {}, X = function(Me) {
          return F.push(Me);
        }, z = function() {
          return F.shift();
        };
        for (n.forEach(function(Re) {
          return F.push(Re);
        }); F.length > 0; ) {
          var re = z(), W = B(re, R);
          if (W)
            re.outgoers().filter(function(Re) {
              return Re.isNode() && a.has(Re);
            }).forEach(X);
          else if (W === null) {
            ft("Detected double maximal shift for node `" + re.id() + "`.  Bailing maximal adjustment due to cycle.  Use `options.maximal: true` only on DAGs.");
            break;
          }
        }
      }
      C();
      var Z = 0;
      if (e.avoidOverlap)
        for (var ie = 0; ie < n.length; ie++) {
          var oe = n[ie], ge = oe.layoutDimensions(e), se = ge.w, de = ge.h;
          Z = Math.max(Z, se, de);
        }
      var we = {}, Te = function(Me) {
        if (we[Me.id()])
          return we[Me.id()];
        for (var Ve = pa(Me).depth, Fe = Me.neighborhood(), ke = 0, Ge = 0, et = 0; et < Fe.length; et++) {
          var We = Fe[et];
          if (!(We.isEdge() || We.isParent() || !n.has(We))) {
            var Ye = pa(We);
            if (Ye != null) {
              var Se = Ye.index, N = Ye.depth;
              if (!(Se == null || N == null)) {
                var le = p[N].length;
                N < Ve && (ke += Se / le, Ge++);
              }
            }
          }
        }
        return Ge = Math.max(1, Ge), ke = ke / Ge, Ge === 0 && (ke = 0), we[Me.id()] = ke, ke;
      }, Ee = function(Me, Ve) {
        var Fe = Te(Me), ke = Te(Ve), Ge = Fe - ke;
        return Ge === 0 ? es(Me.id(), Ve.id()) : Ge;
      };
      e.depthSort !== void 0 && (Ee = e.depthSort);
      for (var ye = 0; ye < p.length; ye++)
        p[ye].sort(Ee), I(ye);
      for (var ae = [], xe = 0; xe < M.length; xe++)
        ae.push(M[xe]);
      p.unshift(ae), C();
      for (var Ce = 0, Oe = 0; Oe < p.length; Oe++)
        Ce = Math.max(p[Oe].length, Ce);
      var Ie = {
        x: l.x1 + l.w / 2,
        y: l.x1 + l.h / 2
      }, He = p.reduce(function(Re, Me) {
        return Math.max(Re, Me.length);
      }, 0), qe = function(Me) {
        var Ve = pa(Me), Fe = Ve.depth, ke = Ve.index, Ge = p[Fe].length, et = Math.max(l.w / ((e.grid ? He : Ge) + 1), Z), We = Math.max(l.h / (p.length + 1), Z), Ye = Math.min(l.w / 2 / p.length, l.h / 2 / p.length);
        if (Ye = Math.max(Ye, Z), e.circle) {
          var N = Ye * Fe + Ye - (p.length > 0 && p[0].length <= 3 ? Ye / 2 : 0), le = 2 * Math.PI / p[Fe].length * ke;
          return Fe === 0 && p[0].length === 1 && (N = 1), {
            x: Ie.x + N * Math.cos(le),
            y: Ie.y + N * Math.sin(le)
          };
        } else {
          var Se = {
            x: Ie.x + (ke + 1 - (Ge + 1) / 2) * et,
            y: (Fe + 1) * We
          };
          return Se;
        }
      };
      return a.nodes().layoutPositions(this, e, qe), this;
    };
    var _d = {
      fit: !0,
      // whether to fit the viewport to the graph
      padding: 30,
      // the padding on fit
      boundingBox: void 0,
      // constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
      avoidOverlap: !0,
      // prevents node overlap, may overflow boundingBox and radius if not enough space
      nodeDimensionsIncludeLabels: !1,
      // Excludes the label when calculating node bounding boxes for the layout algorithm
      spacingFactor: void 0,
      // Applies a multiplicative factor (>0) to expand or compress the overall area that the nodes take up
      radius: void 0,
      // the radius of the circle
      startAngle: 3 / 2 * Math.PI,
      // where nodes start in radians
      sweep: void 0,
      // how many radians should be between the first and last node (defaults to full circle)
      clockwise: !0,
      // whether the layout should go clockwise (true) or counterclockwise/anticlockwise (false)
      sort: void 0,
      // a sorting function to order the nodes; e.g. function(a, b){ return a.data('weight') - b.data('weight') }
      animate: !1,
      // whether to transition the node positions
      animationDuration: 500,
      // duration of animation in ms if enabled
      animationEasing: void 0,
      // easing of animation if enabled
      animateFilter: function(e, r) {
        return !0;
      },
      // a function that determines whether the node should be animated.  All nodes animated by default on animate enabled.  Non-animated nodes are positioned immediately when the layout starts
      ready: void 0,
      // callback on layoutready
      stop: void 0,
      // callback on layoutstop
      transform: function(e, r) {
        return r;
      }
      // transform a given node position. Useful for changing flow direction in discrete layouts 
    };
    function Wo(t) {
      this.options = Ue({}, _d, t);
    }
    Wo.prototype.run = function() {
      var t = this.options, e = t, r = t.cy, a = e.eles, n = e.counterclockwise !== void 0 ? !e.counterclockwise : e.clockwise, i = a.nodes().not(":parent");
      e.sort && (i = i.sort(e.sort));
      for (var s = Ut(e.boundingBox ? e.boundingBox : {
        x1: 0,
        y1: 0,
        w: r.width(),
        h: r.height()
      }), o = {
        x: s.x1 + s.w / 2,
        y: s.y1 + s.h / 2
      }, l = e.sweep === void 0 ? 2 * Math.PI - 2 * Math.PI / i.length : e.sweep, u = l / Math.max(1, i.length - 1), f, h = 0, c = 0; c < i.length; c++) {
        var v = i[c], d = v.layoutDimensions(e), g = d.w, y = d.h;
        h = Math.max(h, g, y);
      }
      if (k(e.radius) ? f = e.radius : i.length <= 1 ? f = 0 : f = Math.min(s.h, s.w) / 2 - h, i.length > 1 && e.avoidOverlap) {
        h *= 1.75;
        var p = Math.cos(u) - Math.cos(0), m = Math.sin(u) - Math.sin(0), b = Math.sqrt(h * h / (p * p + m * m));
        f = Math.max(b, f);
      }
      var E = function(O, x) {
        var I = e.startAngle + x * u * (n ? 1 : -1), C = f * Math.cos(I), B = f * Math.sin(I), F = {
          x: o.x + C,
          y: o.y + B
        };
        return F;
      };
      return a.nodes().layoutPositions(this, e, E), this;
    };
    var Ud = {
      fit: !0,
      // whether to fit the viewport to the graph
      padding: 30,
      // the padding on fit
      startAngle: 3 / 2 * Math.PI,
      // where nodes start in radians
      sweep: void 0,
      // how many radians should be between the first and last node (defaults to full circle)
      clockwise: !0,
      // whether the layout should go clockwise (true) or counterclockwise/anticlockwise (false)
      equidistant: !1,
      // whether levels have an equal radial distance betwen them, may cause bounding box overflow
      minNodeSpacing: 10,
      // min spacing between outside of nodes (used for radius adjustment)
      boundingBox: void 0,
      // constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
      avoidOverlap: !0,
      // prevents node overlap, may overflow boundingBox if not enough space
      nodeDimensionsIncludeLabels: !1,
      // Excludes the label when calculating node bounding boxes for the layout algorithm
      height: void 0,
      // height of layout area (overrides container height)
      width: void 0,
      // width of layout area (overrides container width)
      spacingFactor: void 0,
      // Applies a multiplicative factor (>0) to expand or compress the overall area that the nodes take up
      concentric: function(e) {
        return e.degree();
      },
      levelWidth: function(e) {
        return e.maxDegree() / 4;
      },
      animate: !1,
      // whether to transition the node positions
      animationDuration: 500,
      // duration of animation in ms if enabled
      animationEasing: void 0,
      // easing of animation if enabled
      animateFilter: function(e, r) {
        return !0;
      },
      // a function that determines whether the node should be animated.  All nodes animated by default on animate enabled.  Non-animated nodes are positioned immediately when the layout starts
      ready: void 0,
      // callback on layoutready
      stop: void 0,
      // callback on layoutstop
      transform: function(e, r) {
        return r;
      }
      // transform a given node position. Useful for changing flow direction in discrete layouts
    };
    function Ko(t) {
      this.options = Ue({}, Ud, t);
    }
    Ko.prototype.run = function() {
      for (var t = this.options, e = t, r = e.counterclockwise !== void 0 ? !e.counterclockwise : e.clockwise, a = t.cy, n = e.eles, i = n.nodes().not(":parent"), s = Ut(e.boundingBox ? e.boundingBox : {
        x1: 0,
        y1: 0,
        w: a.width(),
        h: a.height()
      }), o = {
        x: s.x1 + s.w / 2,
        y: s.y1 + s.h / 2
      }, l = [], u = 0, f = 0; f < i.length; f++) {
        var h = i[f], c = void 0;
        c = e.concentric(h), l.push({
          value: c,
          node: h
        }), h._private.scratch.concentric = c;
      }
      i.updateStyle();
      for (var v = 0; v < i.length; v++) {
        var d = i[v], g = d.layoutDimensions(e);
        u = Math.max(u, g.w, g.h);
      }
      l.sort(function(Re, Me) {
        return Me.value - Re.value;
      });
      for (var y = e.levelWidth(i), p = [[]], m = p[0], b = 0; b < l.length; b++) {
        var E = l[b];
        if (m.length > 0) {
          var M = Math.abs(m[0].value - E.value);
          M >= y && (m = [], p.push(m));
        }
        m.push(E);
      }
      var O = u + e.minNodeSpacing;
      if (!e.avoidOverlap) {
        var x = p.length > 0 && p[0].length > 1, I = Math.min(s.w, s.h) / 2 - O, C = I / (p.length + x ? 1 : 0);
        O = Math.min(O, C);
      }
      for (var B = 0, F = 0; F < p.length; F++) {
        var R = p[F], X = e.sweep === void 0 ? 2 * Math.PI - 2 * Math.PI / R.length : e.sweep, z = R.dTheta = X / Math.max(1, R.length - 1);
        if (R.length > 1 && e.avoidOverlap) {
          var re = Math.cos(z) - Math.cos(0), W = Math.sin(z) - Math.sin(0), Z = Math.sqrt(O * O / (re * re + W * W));
          B = Math.max(Z, B);
        }
        R.r = B, B += O;
      }
      if (e.equidistant) {
        for (var ie = 0, oe = 0, ge = 0; ge < p.length; ge++) {
          var se = p[ge], de = se.r - oe;
          ie = Math.max(ie, de);
        }
        oe = 0;
        for (var we = 0; we < p.length; we++) {
          var Te = p[we];
          we === 0 && (oe = Te.r), Te.r = oe, oe += ie;
        }
      }
      for (var Ee = {}, ye = 0; ye < p.length; ye++)
        for (var ae = p[ye], xe = ae.dTheta, Ce = ae.r, Oe = 0; Oe < ae.length; Oe++) {
          var Ie = ae[Oe], He = e.startAngle + (r ? 1 : -1) * xe * Oe, qe = {
            x: o.x + Ce * Math.cos(He),
            y: o.y + Ce * Math.sin(He)
          };
          Ee[Ie.node.id()] = qe;
        }
      return n.nodes().layoutPositions(this, e, function(Re) {
        var Me = Re.id();
        return Ee[Me];
      }), this;
    };
    var Bi, Yd = {
      // Called on `layoutready`
      ready: function() {
      },
      // Called on `layoutstop`
      stop: function() {
      },
      // Whether to animate while running the layout
      // true : Animate continuously as the layout is running
      // false : Just show the end result
      // 'end' : Animate with the end result, from the initial positions to the end positions
      animate: !0,
      // Easing of the animation for animate:'end'
      animationEasing: void 0,
      // The duration of the animation for animate:'end'
      animationDuration: void 0,
      // A function that determines whether the node should be animated
      // All nodes animated by default on animate enabled
      // Non-animated nodes are positioned immediately when the layout starts
      animateFilter: function(e, r) {
        return !0;
      },
      // The layout animates only after this many milliseconds for animate:true
      // (prevents flashing on fast runs)
      animationThreshold: 250,
      // Number of iterations between consecutive screen positions update
      refresh: 20,
      // Whether to fit the network view after when done
      fit: !0,
      // Padding on fit
      padding: 30,
      // Constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
      boundingBox: void 0,
      // Excludes the label when calculating node bounding boxes for the layout algorithm
      nodeDimensionsIncludeLabels: !1,
      // Randomize the initial positions of the nodes (true) or use existing positions (false)
      randomize: !1,
      // Extra spacing between components in non-compound graphs
      componentSpacing: 40,
      // Node repulsion (non overlapping) multiplier
      nodeRepulsion: function(e) {
        return 2048;
      },
      // Node repulsion (overlapping) multiplier
      nodeOverlap: 4,
      // Ideal edge (non nested) length
      idealEdgeLength: function(e) {
        return 32;
      },
      // Divisor to compute edge forces
      edgeElasticity: function(e) {
        return 32;
      },
      // Nesting factor (multiplier) to compute ideal edge length for nested edges
      nestingFactor: 1.2,
      // Gravity force (constant)
      gravity: 1,
      // Maximum number of iterations to perform
      numIter: 1e3,
      // Initial temperature (maximum node displacement)
      initialTemp: 1e3,
      // Cooling factor (how the temperature is reduced between consecutive iterations
      coolingFactor: 0.99,
      // Lower temperature threshold (below this point the layout will end)
      minTemp: 1
    };
    function Yn(t) {
      this.options = Ue({}, Yd, t), this.options.layout = this;
    }
    Yn.prototype.run = function() {
      var t = this.options, e = t.cy, r = this;
      r.stopped = !1, (t.animate === !0 || t.animate === !1) && r.emit({
        type: "layoutstart",
        layout: r
      }), t.debug === !0 ? Bi = !0 : Bi = !1;
      var a = Hd(e, r, t);
      Bi && Wd(a), t.randomize && Kd(a);
      var n = dr(), i = function() {
        Zd(a, e, t), t.fit === !0 && e.fit(t.padding);
      }, s = function(c) {
        return !(r.stopped || c >= t.numIter || (Qd(a, t), a.temperature = a.temperature * t.coolingFactor, a.temperature < t.minTemp));
      }, o = function() {
        if (t.animate === !0 || t.animate === !1)
          i(), r.one("layoutstop", t.stop), r.emit({
            type: "layoutstop",
            layout: r
          });
        else {
          var c = t.eles.nodes(), v = Zo(a, t, c);
          c.layoutPositions(r, t, v);
        }
      }, l = 0, u = !0;
      if (t.animate === !0) {
        var f = function h() {
          for (var c = 0; u && c < t.refresh; )
            u = s(l), l++, c++;
          if (!u)
            Jo(a, t), o();
          else {
            var v = dr();
            v - n >= t.animationThreshold && i(), hn(h);
          }
        };
        f();
      } else {
        for (; u; )
          u = s(l), l++;
        Jo(a, t), o();
      }
      return this;
    }, Yn.prototype.stop = function() {
      return this.stopped = !0, this.thread && this.thread.stop(), this.emit("layoutstop"), this;
    }, Yn.prototype.destroy = function() {
      return this.thread && this.thread.stop(), this;
    };
    var Hd = function(e, r, a) {
      for (var n = a.eles.edges(), i = a.eles.nodes(), s = {
        isCompound: e.hasCompoundNodes(),
        layoutNodes: [],
        idToIndex: {},
        nodeSize: i.size(),
        graphSet: [],
        indexToGraph: [],
        layoutEdges: [],
        edgeSize: n.size(),
        temperature: a.initialTemp,
        clientWidth: e.width(),
        clientHeight: e.width(),
        boundingBox: Ut(a.boundingBox ? a.boundingBox : {
          x1: 0,
          y1: 0,
          w: e.width(),
          h: e.height()
        })
      }, o = a.eles.components(), l = {}, u = 0; u < o.length; u++)
        for (var f = o[u], h = 0; h < f.length; h++) {
          var c = f[h];
          l[c.id()] = u;
        }
      for (var u = 0; u < s.nodeSize; u++) {
        var v = i[u], d = v.layoutDimensions(a), g = {};
        g.isLocked = v.locked(), g.id = v.data("id"), g.parentId = v.data("parent"), g.cmptId = l[v.id()], g.children = [], g.positionX = v.position("x"), g.positionY = v.position("y"), g.offsetX = 0, g.offsetY = 0, g.height = d.w, g.width = d.h, g.maxX = g.positionX + g.width / 2, g.minX = g.positionX - g.width / 2, g.maxY = g.positionY + g.height / 2, g.minY = g.positionY - g.height / 2, g.padLeft = parseFloat(v.style("padding")), g.padRight = parseFloat(v.style("padding")), g.padTop = parseFloat(v.style("padding")), g.padBottom = parseFloat(v.style("padding")), g.nodeRepulsion = H(a.nodeRepulsion) ? a.nodeRepulsion(v) : a.nodeRepulsion, s.layoutNodes.push(g), s.idToIndex[g.id] = u;
      }
      for (var y = [], p = 0, m = -1, b = [], u = 0; u < s.nodeSize; u++) {
        var v = s.layoutNodes[u], E = v.parentId;
        E != null ? s.layoutNodes[s.idToIndex[E]].children.push(v.id) : (y[++m] = v.id, b.push(v.id));
      }
      for (s.graphSet.push(b); p <= m; ) {
        var M = y[p++], O = s.idToIndex[M], c = s.layoutNodes[O], x = c.children;
        if (x.length > 0) {
          s.graphSet.push(x);
          for (var u = 0; u < x.length; u++)
            y[++m] = x[u];
        }
      }
      for (var u = 0; u < s.graphSet.length; u++)
        for (var I = s.graphSet[u], h = 0; h < I.length; h++) {
          var C = s.idToIndex[I[h]];
          s.indexToGraph[C] = u;
        }
      for (var u = 0; u < s.edgeSize; u++) {
        var B = n[u], F = {};
        F.id = B.data("id"), F.sourceId = B.data("source"), F.targetId = B.data("target");
        var R = H(a.idealEdgeLength) ? a.idealEdgeLength(B) : a.idealEdgeLength, X = H(a.edgeElasticity) ? a.edgeElasticity(B) : a.edgeElasticity, z = s.idToIndex[F.sourceId], re = s.idToIndex[F.targetId], W = s.indexToGraph[z], Z = s.indexToGraph[re];
        if (W != Z) {
          for (var ie = Xd(F.sourceId, F.targetId, s), oe = s.graphSet[ie], ge = 0, g = s.layoutNodes[z]; oe.indexOf(g.id) === -1; )
            g = s.layoutNodes[s.idToIndex[g.parentId]], ge++;
          for (g = s.layoutNodes[re]; oe.indexOf(g.id) === -1; )
            g = s.layoutNodes[s.idToIndex[g.parentId]], ge++;
          R *= ge * a.nestingFactor;
        }
        F.idealLength = R, F.elasticity = X, s.layoutEdges.push(F);
      }
      return s;
    }, Xd = function(e, r, a) {
      var n = qd(e, r, 0, a);
      return 2 > n.count ? 0 : n.graph;
    }, qd = function t(e, r, a, n) {
      var i = n.graphSet[a];
      if (-1 < i.indexOf(e) && -1 < i.indexOf(r))
        return {
          count: 2,
          graph: a
        };
      for (var s = 0, o = 0; o < i.length; o++) {
        var l = i[o], u = n.idToIndex[l], f = n.layoutNodes[u].children;
        if (f.length !== 0) {
          var h = n.indexToGraph[n.idToIndex[f[0]]], c = t(e, r, h, n);
          if (c.count !== 0)
            if (c.count === 1) {
              if (s++, s === 2)
                break;
            } else
              return c;
        }
      }
      return {
        count: s,
        graph: a
      };
    }, Wd, Kd = function(e, r) {
      for (var a = e.clientWidth, n = e.clientHeight, i = 0; i < e.nodeSize; i++) {
        var s = e.layoutNodes[i];
        s.children.length === 0 && !s.isLocked && (s.positionX = Math.random() * a, s.positionY = Math.random() * n);
      }
    }, Zo = function(e, r, a) {
      var n = e.boundingBox, i = {
        x1: 1 / 0,
        x2: -1 / 0,
        y1: 1 / 0,
        y2: -1 / 0
      };
      return r.boundingBox && (a.forEach(function(s) {
        var o = e.layoutNodes[e.idToIndex[s.data("id")]];
        i.x1 = Math.min(i.x1, o.positionX), i.x2 = Math.max(i.x2, o.positionX), i.y1 = Math.min(i.y1, o.positionY), i.y2 = Math.max(i.y2, o.positionY);
      }), i.w = i.x2 - i.x1, i.h = i.y2 - i.y1), function(s, o) {
        var l = e.layoutNodes[e.idToIndex[s.data("id")]];
        if (r.boundingBox) {
          var u = (l.positionX - i.x1) / i.w, f = (l.positionY - i.y1) / i.h;
          return {
            x: n.x1 + u * n.w,
            y: n.y1 + f * n.h
          };
        } else
          return {
            x: l.positionX,
            y: l.positionY
          };
      };
    }, Zd = function(e, r, a) {
      var n = a.layout, i = a.eles.nodes(), s = Zo(e, a, i);
      i.positions(s), e.ready !== !0 && (e.ready = !0, n.one("layoutready", a.ready), n.emit({
        type: "layoutready",
        layout: this
      }));
    }, Qd = function(e, r, a) {
      Jd(e, r), tg(e), rg(e, r), ag(e), ng(e);
    }, Jd = function(e, r) {
      for (var a = 0; a < e.graphSet.length; a++)
        for (var n = e.graphSet[a], i = n.length, s = 0; s < i; s++)
          for (var o = e.layoutNodes[e.idToIndex[n[s]]], l = s + 1; l < i; l++) {
            var u = e.layoutNodes[e.idToIndex[n[l]]];
            jd(o, u, e, r);
          }
    }, Qo = function(e) {
      return -e + 2 * e * Math.random();
    }, jd = function(e, r, a, n) {
      var i = e.cmptId, s = r.cmptId;
      if (!(i !== s && !a.isCompound)) {
        var o = r.positionX - e.positionX, l = r.positionY - e.positionY, u = 1;
        o === 0 && l === 0 && (o = Qo(u), l = Qo(u));
        var f = eg(e, r, o, l);
        if (f > 0)
          var h = n.nodeOverlap * f, c = Math.sqrt(o * o + l * l), v = h * o / c, d = h * l / c;
        else
          var g = Hn(e, o, l), y = Hn(r, -1 * o, -1 * l), p = y.x - g.x, m = y.y - g.y, b = p * p + m * m, c = Math.sqrt(b), h = (e.nodeRepulsion + r.nodeRepulsion) / b, v = h * p / c, d = h * m / c;
        e.isLocked || (e.offsetX -= v, e.offsetY -= d), r.isLocked || (r.offsetX += v, r.offsetY += d);
      }
    }, eg = function(e, r, a, n) {
      if (a > 0)
        var i = e.maxX - r.minX;
      else
        var i = r.maxX - e.minX;
      if (n > 0)
        var s = e.maxY - r.minY;
      else
        var s = r.maxY - e.minY;
      return i >= 0 && s >= 0 ? Math.sqrt(i * i + s * s) : 0;
    }, Hn = function(e, r, a) {
      var n = e.positionX, i = e.positionY, s = e.height || 1, o = e.width || 1, l = a / r, u = s / o, f = {};
      return r === 0 && 0 < a || r === 0 && 0 > a ? (f.x = n, f.y = i + s / 2, f) : 0 < r && -1 * u <= l && l <= u ? (f.x = n + o / 2, f.y = i + o * a / 2 / r, f) : 0 > r && -1 * u <= l && l <= u ? (f.x = n - o / 2, f.y = i - o * a / 2 / r, f) : 0 < a && (l <= -1 * u || l >= u) ? (f.x = n + s * r / 2 / a, f.y = i + s / 2, f) : (0 > a && (l <= -1 * u || l >= u) && (f.x = n - s * r / 2 / a, f.y = i - s / 2), f);
    }, tg = function(e, r) {
      for (var a = 0; a < e.edgeSize; a++) {
        var n = e.layoutEdges[a], i = e.idToIndex[n.sourceId], s = e.layoutNodes[i], o = e.idToIndex[n.targetId], l = e.layoutNodes[o], u = l.positionX - s.positionX, f = l.positionY - s.positionY;
        if (!(u === 0 && f === 0)) {
          var h = Hn(s, u, f), c = Hn(l, -1 * u, -1 * f), v = c.x - h.x, d = c.y - h.y, g = Math.sqrt(v * v + d * d), y = Math.pow(n.idealLength - g, 2) / n.elasticity;
          if (g !== 0)
            var p = y * v / g, m = y * d / g;
          else
            var p = 0, m = 0;
          s.isLocked || (s.offsetX += p, s.offsetY += m), l.isLocked || (l.offsetX -= p, l.offsetY -= m);
        }
      }
    }, rg = function(e, r) {
      if (r.gravity !== 0)
        for (var a = 1, n = 0; n < e.graphSet.length; n++) {
          var i = e.graphSet[n], s = i.length;
          if (n === 0)
            var o = e.clientHeight / 2, l = e.clientWidth / 2;
          else
            var u = e.layoutNodes[e.idToIndex[i[0]]], f = e.layoutNodes[e.idToIndex[u.parentId]], o = f.positionX, l = f.positionY;
          for (var h = 0; h < s; h++) {
            var c = e.layoutNodes[e.idToIndex[i[h]]];
            if (!c.isLocked) {
              var v = o - c.positionX, d = l - c.positionY, g = Math.sqrt(v * v + d * d);
              if (g > a) {
                var y = r.gravity * v / g, p = r.gravity * d / g;
                c.offsetX += y, c.offsetY += p;
              }
            }
          }
        }
    }, ag = function(e, r) {
      var a = [], n = 0, i = -1;
      for (a.push.apply(a, e.graphSet[0]), i += e.graphSet[0].length; n <= i; ) {
        var s = a[n++], o = e.idToIndex[s], l = e.layoutNodes[o], u = l.children;
        if (0 < u.length && !l.isLocked) {
          for (var f = l.offsetX, h = l.offsetY, c = 0; c < u.length; c++) {
            var v = e.layoutNodes[e.idToIndex[u[c]]];
            v.offsetX += f, v.offsetY += h, a[++i] = u[c];
          }
          l.offsetX = 0, l.offsetY = 0;
        }
      }
    }, ng = function(e, r) {
      for (var a = 0; a < e.nodeSize; a++) {
        var n = e.layoutNodes[a];
        0 < n.children.length && (n.maxX = void 0, n.minX = void 0, n.maxY = void 0, n.minY = void 0);
      }
      for (var a = 0; a < e.nodeSize; a++) {
        var n = e.layoutNodes[a];
        if (!(0 < n.children.length || n.isLocked)) {
          var i = ig(n.offsetX, n.offsetY, e.temperature);
          n.positionX += i.x, n.positionY += i.y, n.offsetX = 0, n.offsetY = 0, n.minX = n.positionX - n.width, n.maxX = n.positionX + n.width, n.minY = n.positionY - n.height, n.maxY = n.positionY + n.height, sg(n, e);
        }
      }
      for (var a = 0; a < e.nodeSize; a++) {
        var n = e.layoutNodes[a];
        0 < n.children.length && !n.isLocked && (n.positionX = (n.maxX + n.minX) / 2, n.positionY = (n.maxY + n.minY) / 2, n.width = n.maxX - n.minX, n.height = n.maxY - n.minY);
      }
    }, ig = function(e, r, a) {
      var n = Math.sqrt(e * e + r * r);
      if (n > a)
        var i = {
          x: a * e / n,
          y: a * r / n
        };
      else
        var i = {
          x: e,
          y: r
        };
      return i;
    }, sg = function t(e, r) {
      var a = e.parentId;
      if (a != null) {
        var n = r.layoutNodes[r.idToIndex[a]], i = !1;
        if ((n.maxX == null || e.maxX + n.padRight > n.maxX) && (n.maxX = e.maxX + n.padRight, i = !0), (n.minX == null || e.minX - n.padLeft < n.minX) && (n.minX = e.minX - n.padLeft, i = !0), (n.maxY == null || e.maxY + n.padBottom > n.maxY) && (n.maxY = e.maxY + n.padBottom, i = !0), (n.minY == null || e.minY - n.padTop < n.minY) && (n.minY = e.minY - n.padTop, i = !0), i)
          return t(n, r);
      }
    }, Jo = function(e, r) {
      for (var a = e.layoutNodes, n = [], i = 0; i < a.length; i++) {
        var s = a[i], o = s.cmptId, l = n[o] = n[o] || [];
        l.push(s);
      }
      for (var u = 0, i = 0; i < n.length; i++) {
        var f = n[i];
        if (f) {
          f.x1 = 1 / 0, f.x2 = -1 / 0, f.y1 = 1 / 0, f.y2 = -1 / 0;
          for (var h = 0; h < f.length; h++) {
            var c = f[h];
            f.x1 = Math.min(f.x1, c.positionX - c.width / 2), f.x2 = Math.max(f.x2, c.positionX + c.width / 2), f.y1 = Math.min(f.y1, c.positionY - c.height / 2), f.y2 = Math.max(f.y2, c.positionY + c.height / 2);
          }
          f.w = f.x2 - f.x1, f.h = f.y2 - f.y1, u += f.w * f.h;
        }
      }
      n.sort(function(m, b) {
        return b.w * b.h - m.w * m.h;
      });
      for (var v = 0, d = 0, g = 0, y = 0, p = Math.sqrt(u) * e.clientWidth / e.clientHeight, i = 0; i < n.length; i++) {
        var f = n[i];
        if (f) {
          for (var h = 0; h < f.length; h++) {
            var c = f[h];
            c.isLocked || (c.positionX += v - f.x1, c.positionY += d - f.y1);
          }
          v += f.w + r.componentSpacing, g += f.w + r.componentSpacing, y = Math.max(y, f.h), g > p && (d += y + r.componentSpacing, v = 0, g = 0, y = 0);
        }
      }
    }, og = {
      fit: !0,
      // whether to fit the viewport to the graph
      padding: 30,
      // padding used on fit
      boundingBox: void 0,
      // constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
      avoidOverlap: !0,
      // prevents node overlap, may overflow boundingBox if not enough space
      avoidOverlapPadding: 10,
      // extra spacing around nodes when avoidOverlap: true
      nodeDimensionsIncludeLabels: !1,
      // Excludes the label when calculating node bounding boxes for the layout algorithm
      spacingFactor: void 0,
      // Applies a multiplicative factor (>0) to expand or compress the overall area that the nodes take up
      condense: !1,
      // uses all available space on false, uses minimal space on true
      rows: void 0,
      // force num of rows in the grid
      cols: void 0,
      // force num of columns in the grid
      position: function(e) {
      },
      // returns { row, col } for element
      sort: void 0,
      // a sorting function to order the nodes; e.g. function(a, b){ return a.data('weight') - b.data('weight') }
      animate: !1,
      // whether to transition the node positions
      animationDuration: 500,
      // duration of animation in ms if enabled
      animationEasing: void 0,
      // easing of animation if enabled
      animateFilter: function(e, r) {
        return !0;
      },
      // a function that determines whether the node should be animated.  All nodes animated by default on animate enabled.  Non-animated nodes are positioned immediately when the layout starts
      ready: void 0,
      // callback on layoutready
      stop: void 0,
      // callback on layoutstop
      transform: function(e, r) {
        return r;
      }
      // transform a given node position. Useful for changing flow direction in discrete layouts 
    };
    function jo(t) {
      this.options = Ue({}, og, t);
    }
    jo.prototype.run = function() {
      var t = this.options, e = t, r = t.cy, a = e.eles, n = a.nodes().not(":parent");
      e.sort && (n = n.sort(e.sort));
      var i = Ut(e.boundingBox ? e.boundingBox : {
        x1: 0,
        y1: 0,
        w: r.width(),
        h: r.height()
      });
      if (i.h === 0 || i.w === 0)
        a.nodes().layoutPositions(this, e, function(we) {
          return {
            x: i.x1,
            y: i.y1
          };
        });
      else {
        var s = n.size(), o = Math.sqrt(s * i.h / i.w), l = Math.round(o), u = Math.round(i.w / i.h * o), f = function(Te) {
          if (Te == null)
            return Math.min(l, u);
          var Ee = Math.min(l, u);
          Ee == l ? l = Te : u = Te;
        }, h = function(Te) {
          if (Te == null)
            return Math.max(l, u);
          var Ee = Math.max(l, u);
          Ee == l ? l = Te : u = Te;
        }, c = e.rows, v = e.cols != null ? e.cols : e.columns;
        if (c != null && v != null)
          l = c, u = v;
        else if (c != null && v == null)
          l = c, u = Math.ceil(s / l);
        else if (c == null && v != null)
          u = v, l = Math.ceil(s / u);
        else if (u * l > s) {
          var d = f(), g = h();
          (d - 1) * g >= s ? f(d - 1) : (g - 1) * d >= s && h(g - 1);
        } else
          for (; u * l < s; ) {
            var y = f(), p = h();
            (p + 1) * y >= s ? h(p + 1) : f(y + 1);
          }
        var m = i.w / u, b = i.h / l;
        if (e.condense && (m = 0, b = 0), e.avoidOverlap)
          for (var E = 0; E < n.length; E++) {
            var M = n[E], O = M._private.position;
            (O.x == null || O.y == null) && (O.x = 0, O.y = 0);
            var x = M.layoutDimensions(e), I = e.avoidOverlapPadding, C = x.w + I, B = x.h + I;
            m = Math.max(m, C), b = Math.max(b, B);
          }
        for (var F = {}, R = function(Te, Ee) {
          return !!F["c-" + Te + "-" + Ee];
        }, X = function(Te, Ee) {
          F["c-" + Te + "-" + Ee] = !0;
        }, z = 0, re = 0, W = function() {
          re++, re >= u && (re = 0, z++);
        }, Z = {}, ie = 0; ie < n.length; ie++) {
          var oe = n[ie], ge = e.position(oe);
          if (ge && (ge.row !== void 0 || ge.col !== void 0)) {
            var se = {
              row: ge.row,
              col: ge.col
            };
            if (se.col === void 0)
              for (se.col = 0; R(se.row, se.col); )
                se.col++;
            else if (se.row === void 0)
              for (se.row = 0; R(se.row, se.col); )
                se.row++;
            Z[oe.id()] = se, X(se.row, se.col);
          }
        }
        var de = function(Te, Ee) {
          var ye, ae;
          if (Te.locked() || Te.isParent())
            return !1;
          var xe = Z[Te.id()];
          if (xe)
            ye = xe.col * m + m / 2 + i.x1, ae = xe.row * b + b / 2 + i.y1;
          else {
            for (; R(z, re); )
              W();
            ye = re * m + m / 2 + i.x1, ae = z * b + b / 2 + i.y1, X(z, re), W();
          }
          return {
            x: ye,
            y: ae
          };
        };
        n.layoutPositions(this, e, de);
      }
      return this;
    };
    var ug = {
      ready: function() {
      },
      // on layoutready
      stop: function() {
      }
      // on layoutstop
    };
    function Fi(t) {
      this.options = Ue({}, ug, t);
    }
    Fi.prototype.run = function() {
      var t = this.options, e = t.eles, r = this;
      return t.cy, r.emit("layoutstart"), e.nodes().positions(function() {
        return {
          x: 0,
          y: 0
        };
      }), r.one("layoutready", t.ready), r.emit("layoutready"), r.one("layoutstop", t.stop), r.emit("layoutstop"), this;
    }, Fi.prototype.stop = function() {
      return this;
    };
    var lg = {
      positions: void 0,
      // map of (node id) => (position obj); or function(node){ return somPos; }
      zoom: void 0,
      // the zoom level to set (prob want fit = false if set)
      pan: void 0,
      // the pan level to set (prob want fit = false if set)
      fit: !0,
      // whether to fit to viewport
      padding: 30,
      // padding on fit
      animate: !1,
      // whether to transition the node positions
      animationDuration: 500,
      // duration of animation in ms if enabled
      animationEasing: void 0,
      // easing of animation if enabled
      animateFilter: function(e, r) {
        return !0;
      },
      // a function that determines whether the node should be animated.  All nodes animated by default on animate enabled.  Non-animated nodes are positioned immediately when the layout starts
      ready: void 0,
      // callback on layoutready
      stop: void 0,
      // callback on layoutstop
      transform: function(e, r) {
        return r;
      }
      // transform a given node position. Useful for changing flow direction in discrete layouts
    };
    function eu(t) {
      this.options = Ue({}, lg, t);
    }
    eu.prototype.run = function() {
      var t = this.options, e = t.eles, r = e.nodes(), a = H(t.positions);
      function n(i) {
        if (t.positions == null)
          return gf(i.position());
        if (a)
          return t.positions(i);
        var s = t.positions[i._private.data.id];
        return s ?? null;
      }
      return r.layoutPositions(this, t, function(i, s) {
        var o = n(i);
        return i.locked() || o == null ? !1 : o;
      }), this;
    };
    var fg = {
      fit: !0,
      // whether to fit to viewport
      padding: 30,
      // fit padding
      boundingBox: void 0,
      // constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
      animate: !1,
      // whether to transition the node positions
      animationDuration: 500,
      // duration of animation in ms if enabled
      animationEasing: void 0,
      // easing of animation if enabled
      animateFilter: function(e, r) {
        return !0;
      },
      // a function that determines whether the node should be animated.  All nodes animated by default on animate enabled.  Non-animated nodes are positioned immediately when the layout starts
      ready: void 0,
      // callback on layoutready
      stop: void 0,
      // callback on layoutstop
      transform: function(e, r) {
        return r;
      }
      // transform a given node position. Useful for changing flow direction in discrete layouts 
    };
    function tu(t) {
      this.options = Ue({}, fg, t);
    }
    tu.prototype.run = function() {
      var t = this.options, e = t.cy, r = t.eles, a = Ut(t.boundingBox ? t.boundingBox : {
        x1: 0,
        y1: 0,
        w: e.width(),
        h: e.height()
      }), n = function(s, o) {
        return {
          x: a.x1 + Math.round(Math.random() * a.w),
          y: a.y1 + Math.round(Math.random() * a.h)
        };
      };
      return r.nodes().layoutPositions(this, t, n), this;
    };
    var hg = [{
      name: "breadthfirst",
      impl: qo
    }, {
      name: "circle",
      impl: Wo
    }, {
      name: "concentric",
      impl: Ko
    }, {
      name: "cose",
      impl: Yn
    }, {
      name: "grid",
      impl: jo
    }, {
      name: "null",
      impl: Fi
    }, {
      name: "preset",
      impl: eu
    }, {
      name: "random",
      impl: tu
    }];
    function ru(t) {
      this.options = t, this.notifications = 0;
    }
    var au = function() {
    }, nu = function() {
      throw new Error("A headless instance can not render images");
    };
    ru.prototype = {
      recalculateRenderedStyle: au,
      notify: function() {
        this.notifications++;
      },
      init: au,
      isHeadless: function() {
        return !0;
      },
      png: nu,
      jpg: nu
    };
    var zi = {};
    zi.arrowShapeWidth = 0.3, zi.registerArrowShapes = function() {
      var t = this.arrowShapes = {}, e = this, r = function(u, f, h, c, v, d, g) {
        var y = v.x - h / 2 - g, p = v.x + h / 2 + g, m = v.y - h / 2 - g, b = v.y + h / 2 + g, E = y <= u && u <= p && m <= f && f <= b;
        return E;
      }, a = function(u, f, h, c, v) {
        var d = u * Math.cos(c) - f * Math.sin(c), g = u * Math.sin(c) + f * Math.cos(c), y = d * h, p = g * h, m = y + v.x, b = p + v.y;
        return {
          x: m,
          y: b
        };
      }, n = function(u, f, h, c) {
        for (var v = [], d = 0; d < u.length; d += 2) {
          var g = u[d], y = u[d + 1];
          v.push(a(g, y, f, h, c));
        }
        return v;
      }, i = function(u) {
        for (var f = [], h = 0; h < u.length; h++) {
          var c = u[h];
          f.push(c.x, c.y);
        }
        return f;
      }, s = function(u) {
        return u.pstyle("width").pfValue * u.pstyle("arrow-scale").pfValue * 2;
      }, o = function(u, f) {
        ee(f) && (f = t[f]), t[u] = Ue({
          name: u,
          points: [-0.15, -0.3, 0.15, -0.3, 0.15, 0.3, -0.15, 0.3],
          collide: function(c, v, d, g, y, p) {
            var m = i(n(this.points, d + 2 * p, g, y)), b = Yt(c, v, m);
            return b;
          },
          roughCollide: r,
          draw: function(c, v, d, g) {
            var y = n(this.points, v, d, g);
            e.arrowShapeImpl("polygon")(c, y);
          },
          spacing: function(c) {
            return 0;
          },
          gap: s
        }, f);
      };
      o("none", {
        collide: vn,
        roughCollide: vn,
        draw: si,
        spacing: ds,
        gap: ds
      }), o("triangle", {
        points: [-0.15, -0.3, 0, 0, 0.15, -0.3]
      }), o("arrow", "triangle"), o("triangle-backcurve", {
        points: t.triangle.points,
        controlPoint: [0, -0.15],
        roughCollide: r,
        draw: function(u, f, h, c, v) {
          var d = n(this.points, f, h, c), g = this.controlPoint, y = a(g[0], g[1], f, h, c);
          e.arrowShapeImpl(this.name)(u, d, y);
        },
        gap: function(u) {
          return s(u) * 0.8;
        }
      }), o("triangle-tee", {
        points: [0, 0, 0.15, -0.3, -0.15, -0.3, 0, 0],
        pointsTee: [-0.15, -0.4, -0.15, -0.5, 0.15, -0.5, 0.15, -0.4],
        collide: function(u, f, h, c, v, d, g) {
          var y = i(n(this.points, h + 2 * g, c, v)), p = i(n(this.pointsTee, h + 2 * g, c, v)), m = Yt(u, f, y) || Yt(u, f, p);
          return m;
        },
        draw: function(u, f, h, c, v) {
          var d = n(this.points, f, h, c), g = n(this.pointsTee, f, h, c);
          e.arrowShapeImpl(this.name)(u, d, g);
        }
      }), o("circle-triangle", {
        radius: 0.15,
        pointsTr: [0, -0.15, 0.15, -0.45, -0.15, -0.45, 0, -0.15],
        collide: function(u, f, h, c, v, d, g) {
          var y = v, p = Math.pow(y.x - u, 2) + Math.pow(y.y - f, 2) <= Math.pow((h + 2 * g) * this.radius, 2), m = i(n(this.points, h + 2 * g, c, v));
          return Yt(u, f, m) || p;
        },
        draw: function(u, f, h, c, v) {
          var d = n(this.pointsTr, f, h, c);
          e.arrowShapeImpl(this.name)(u, d, c.x, c.y, this.radius * f);
        },
        spacing: function(u) {
          return e.getArrowWidth(u.pstyle("width").pfValue, u.pstyle("arrow-scale").value) * this.radius;
        }
      }), o("triangle-cross", {
        points: [0, 0, 0.15, -0.3, -0.15, -0.3, 0, 0],
        baseCrossLinePts: [
          -0.15,
          -0.4,
          // first half of the rectangle
          -0.15,
          -0.4,
          0.15,
          -0.4,
          // second half of the rectangle
          0.15,
          -0.4
        ],
        crossLinePts: function(u, f) {
          var h = this.baseCrossLinePts.slice(), c = f / u, v = 3, d = 5;
          return h[v] = h[v] - c, h[d] = h[d] - c, h;
        },
        collide: function(u, f, h, c, v, d, g) {
          var y = i(n(this.points, h + 2 * g, c, v)), p = i(n(this.crossLinePts(h, d), h + 2 * g, c, v)), m = Yt(u, f, y) || Yt(u, f, p);
          return m;
        },
        draw: function(u, f, h, c, v) {
          var d = n(this.points, f, h, c), g = n(this.crossLinePts(f, v), f, h, c);
          e.arrowShapeImpl(this.name)(u, d, g);
        }
      }), o("vee", {
        points: [-0.15, -0.3, 0, 0, 0.15, -0.3, 0, -0.15],
        gap: function(u) {
          return s(u) * 0.525;
        }
      }), o("circle", {
        radius: 0.15,
        collide: function(u, f, h, c, v, d, g) {
          var y = v, p = Math.pow(y.x - u, 2) + Math.pow(y.y - f, 2) <= Math.pow((h + 2 * g) * this.radius, 2);
          return p;
        },
        draw: function(u, f, h, c, v) {
          e.arrowShapeImpl(this.name)(u, c.x, c.y, this.radius * f);
        },
        spacing: function(u) {
          return e.getArrowWidth(u.pstyle("width").pfValue, u.pstyle("arrow-scale").value) * this.radius;
        }
      }), o("tee", {
        points: [-0.15, 0, -0.15, -0.1, 0.15, -0.1, 0.15, 0],
        spacing: function(u) {
          return 1;
        },
        gap: function(u) {
          return 1;
        }
      }), o("square", {
        points: [-0.15, 0, 0.15, 0, 0.15, -0.3, -0.15, -0.3]
      }), o("diamond", {
        points: [-0.15, -0.15, 0, -0.3, 0.15, -0.15, 0, 0],
        gap: function(u) {
          return u.pstyle("width").pfValue * u.pstyle("arrow-scale").value;
        }
      }), o("chevron", {
        points: [0, 0, -0.15, -0.15, -0.1, -0.2, 0, -0.1, 0.1, -0.2, 0.15, -0.15],
        gap: function(u) {
          return 0.95 * u.pstyle("width").pfValue * u.pstyle("arrow-scale").value;
        }
      });
    };
    var Vr = {};
    Vr.projectIntoViewport = function(t, e) {
      var r = this.cy, a = this.findContainerClientCoords(), n = a[0], i = a[1], s = a[4], o = r.pan(), l = r.zoom(), u = ((t - n) / s - o.x) / l, f = ((e - i) / s - o.y) / l;
      return [u, f];
    }, Vr.findContainerClientCoords = function() {
      if (this.containerBB)
        return this.containerBB;
      var t = this.container, e = t.getBoundingClientRect(), r = D.getComputedStyle(t), a = function(p) {
        return parseFloat(r.getPropertyValue(p));
      }, n = {
        left: a("padding-left"),
        right: a("padding-right"),
        top: a("padding-top"),
        bottom: a("padding-bottom")
      }, i = {
        left: a("border-left-width"),
        right: a("border-right-width"),
        top: a("border-top-width"),
        bottom: a("border-bottom-width")
      }, s = t.clientWidth, o = t.clientHeight, l = n.left + n.right, u = n.top + n.bottom, f = i.left + i.right, h = e.width / (s + f), c = s - l, v = o - u, d = e.left + n.left + i.left, g = e.top + n.top + i.top;
      return this.containerBB = [d, g, c, v, h];
    }, Vr.invalidateContainerClientCoordsCache = function() {
      this.containerBB = null;
    }, Vr.findNearestElement = function(t, e, r, a) {
      return this.findNearestElements(t, e, r, a)[0];
    }, Vr.findNearestElements = function(t, e, r, a) {
      var n = this, i = this, s = i.getCachedZSortedEles(), o = [], l = i.cy.zoom(), u = i.cy.hasCompoundNodes(), f = (a ? 24 : 8) / l, h = (a ? 8 : 2) / l, c = (a ? 8 : 2) / l, v = 1 / 0, d, g;
      r && (s = s.interactive);
      function y(x, I) {
        if (x.isNode()) {
          if (g)
            return;
          g = x, o.push(x);
        }
        if (x.isEdge() && (I == null || I < v))
          if (d) {
            if (d.pstyle("z-compound-depth").value === x.pstyle("z-compound-depth").value && d.pstyle("z-compound-depth").value === x.pstyle("z-compound-depth").value) {
              for (var C = 0; C < o.length; C++)
                if (o[C].isEdge()) {
                  o[C] = x, d = x, v = I ?? v;
                  break;
                }
            }
          } else
            o.push(x), d = x, v = I ?? v;
      }
      function p(x) {
        var I = x.outerWidth() + 2 * h, C = x.outerHeight() + 2 * h, B = I / 2, F = C / 2, R = x.position();
        if (R.x - B <= t && t <= R.x + B && R.y - F <= e && e <= R.y + F) {
          var X = i.nodeShapes[n.getNodeShape(x)];
          if (X.checkPoint(t, e, 0, I, C, R.x, R.y))
            return y(x, 0), !0;
        }
      }
      function m(x) {
        var I = x._private, C = I.rscratch, B = x.pstyle("width").pfValue, F = x.pstyle("arrow-scale").value, R = B / 2 + f, X = R * R, z = R * 2, ie = I.source, oe = I.target, re;
        if (C.edgeType === "segments" || C.edgeType === "straight" || C.edgeType === "haystack") {
          for (var W = C.allpts, Z = 0; Z + 3 < W.length; Z += 2)
            if (Af(t, e, W[Z], W[Z + 1], W[Z + 2], W[Z + 3], z) && X > (re = Rf(t, e, W[Z], W[Z + 1], W[Z + 2], W[Z + 3])))
              return y(x, re), !0;
        } else if (C.edgeType === "bezier" || C.edgeType === "multibezier" || C.edgeType === "self" || C.edgeType === "compound") {
          for (var W = C.allpts, Z = 0; Z + 5 < C.allpts.length; Z += 4)
            if (Of(t, e, W[Z], W[Z + 1], W[Z + 2], W[Z + 3], W[Z + 4], W[Z + 5], z) && X > (re = If(t, e, W[Z], W[Z + 1], W[Z + 2], W[Z + 3], W[Z + 4], W[Z + 5])))
              return y(x, re), !0;
        }
        for (var ie = ie || I.source, oe = oe || I.target, ge = n.getArrowWidth(B, F), se = [{
          name: "source",
          x: C.arrowStartX,
          y: C.arrowStartY,
          angle: C.srcArrowAngle
        }, {
          name: "target",
          x: C.arrowEndX,
          y: C.arrowEndY,
          angle: C.tgtArrowAngle
        }, {
          name: "mid-source",
          x: C.midX,
          y: C.midY,
          angle: C.midsrcArrowAngle
        }, {
          name: "mid-target",
          x: C.midX,
          y: C.midY,
          angle: C.midtgtArrowAngle
        }], Z = 0; Z < se.length; Z++) {
          var de = se[Z], we = i.arrowShapes[x.pstyle(de.name + "-arrow-shape").value], Te = x.pstyle("width").pfValue;
          if (we.roughCollide(t, e, ge, de.angle, {
            x: de.x,
            y: de.y
          }, Te, f) && we.collide(t, e, ge, de.angle, {
            x: de.x,
            y: de.y
          }, Te, f))
            return y(x), !0;
        }
        u && o.length > 0 && (p(ie), p(oe));
      }
      function b(x, I, C) {
        return er(x, I, C);
      }
      function E(x, I) {
        var C = x._private, B = c, F;
        I ? F = I + "-" : F = "", x.boundingBox();
        var R = C.labelBounds[I || "main"], X = x.pstyle(F + "label").value, z = x.pstyle("text-events").strValue === "yes";
        if (!(!z || !X)) {
          var re = b(C.rscratch, "labelX", I), W = b(C.rscratch, "labelY", I), Z = b(C.rscratch, "labelAngle", I), ie = x.pstyle(F + "text-margin-x").pfValue, oe = x.pstyle(F + "text-margin-y").pfValue, ge = R.x1 - B - ie, se = R.x2 + B - ie, de = R.y1 - B - oe, we = R.y2 + B - oe;
          if (Z) {
            var Te = Math.cos(Z), Ee = Math.sin(Z), ye = function(qe, Re) {
              return qe = qe - re, Re = Re - W, {
                x: qe * Te - Re * Ee + re,
                y: qe * Ee + Re * Te + W
              };
            }, ae = ye(ge, de), xe = ye(ge, we), Ce = ye(se, de), Oe = ye(se, we), Ie = [
              // with the margin added after the rotation is applied
              ae.x + ie,
              ae.y + oe,
              Ce.x + ie,
              Ce.y + oe,
              Oe.x + ie,
              Oe.y + oe,
              xe.x + ie,
              xe.y + oe
            ];
            if (Yt(t, e, Ie))
              return y(x), !0;
          } else if (ta(R, t, e))
            return y(x), !0;
        }
      }
      for (var M = s.length - 1; M >= 0; M--) {
        var O = s[M];
        O.isNode() ? p(O) || E(O) : m(O) || E(O) || E(O, "source") || E(O, "target");
      }
      return o;
    }, Vr.getAllInBox = function(t, e, r, a) {
      var n = this.getCachedZSortedEles().interactive, i = [], s = Math.min(t, r), o = Math.max(t, r), l = Math.min(e, a), u = Math.max(e, a);
      t = s, r = o, e = l, a = u;
      for (var f = Ut({
        x1: t,
        y1: e,
        x2: r,
        y2: a
      }), h = 0; h < n.length; h++) {
        var c = n[h];
        if (c.isNode()) {
          var v = c, d = v.boundingBox({
            includeNodes: !0,
            includeEdges: !1,
            includeLabels: !1
          });
          hi(f, d) && !xs(d, f) && i.push(v);
        } else {
          var g = c, y = g._private, p = y.rscratch;
          if (p.startX != null && p.startY != null && !ta(f, p.startX, p.startY) || p.endX != null && p.endY != null && !ta(f, p.endX, p.endY))
            continue;
          if (p.edgeType === "bezier" || p.edgeType === "multibezier" || p.edgeType === "self" || p.edgeType === "compound" || p.edgeType === "segments" || p.edgeType === "haystack") {
            for (var m = y.rstyle.bezierPts || y.rstyle.linePts || y.rstyle.haystackPts, b = !0, E = 0; E < m.length; E++)
              if (!Lf(f, m[E])) {
                b = !1;
                break;
              }
            b && i.push(g);
          } else
            (p.edgeType === "haystack" || p.edgeType === "straight") && i.push(g);
        }
      }
      return i;
    };
    var Xn = {};
    Xn.calculateArrowAngles = function(t) {
      var e = t._private.rscratch, r = e.edgeType === "haystack", a = e.edgeType === "bezier", n = e.edgeType === "multibezier", i = e.edgeType === "segments", s = e.edgeType === "compound", o = e.edgeType === "self", l, u, f, h, c, v, p, m;
      if (r ? (f = e.haystackPts[0], h = e.haystackPts[1], c = e.haystackPts[2], v = e.haystackPts[3]) : (f = e.arrowStartX, h = e.arrowStartY, c = e.arrowEndX, v = e.arrowEndY), p = e.midX, m = e.midY, i)
        l = f - e.segpts[0], u = h - e.segpts[1];
      else if (n || s || o || a) {
        var d = e.allpts, g = St(d[0], d[2], d[4], 0.1), y = St(d[1], d[3], d[5], 0.1);
        l = f - g, u = h - y;
      } else
        l = f - p, u = h - m;
      e.srcArrowAngle = pn(l, u);
      var p = e.midX, m = e.midY;
      if (r && (p = (f + c) / 2, m = (h + v) / 2), l = c - f, u = v - h, i) {
        var d = e.allpts;
        if (d.length / 2 % 2 === 0) {
          var b = d.length / 2, E = b - 2;
          l = d[b] - d[E], u = d[b + 1] - d[E + 1];
        } else {
          var b = d.length / 2 - 1, E = b - 2, M = b + 2;
          l = d[b] - d[E], u = d[b + 1] - d[E + 1];
        }
      } else if (n || s || o) {
        var d = e.allpts, O = e.ctrlpts, x, I, C, B;
        if (O.length / 2 % 2 === 0) {
          var F = d.length / 2 - 1, R = F + 2, X = R + 2;
          x = St(d[F], d[R], d[X], 0), I = St(d[F + 1], d[R + 1], d[X + 1], 0), C = St(d[F], d[R], d[X], 1e-4), B = St(d[F + 1], d[R + 1], d[X + 1], 1e-4);
        } else {
          var R = d.length / 2 - 1, F = R - 2, X = R + 2;
          x = St(d[F], d[R], d[X], 0.4999), I = St(d[F + 1], d[R + 1], d[X + 1], 0.4999), C = St(d[F], d[R], d[X], 0.5), B = St(d[F + 1], d[R + 1], d[X + 1], 0.5);
        }
        l = C - x, u = B - I;
      }
      if (e.midtgtArrowAngle = pn(l, u), e.midDispX = l, e.midDispY = u, l *= -1, u *= -1, i) {
        var d = e.allpts;
        if (d.length / 2 % 2 !== 0) {
          var b = d.length / 2 - 1, M = b + 2;
          l = -(d[M] - d[b]), u = -(d[M + 1] - d[b + 1]);
        }
      }
      if (e.midsrcArrowAngle = pn(l, u), i)
        l = c - e.segpts[e.segpts.length - 2], u = v - e.segpts[e.segpts.length - 1];
      else if (n || s || o || a) {
        var d = e.allpts, z = d.length, g = St(d[z - 6], d[z - 4], d[z - 2], 0.9), y = St(d[z - 5], d[z - 3], d[z - 1], 0.9);
        l = c - g, u = v - y;
      } else
        l = c - p, u = v - m;
      e.tgtArrowAngle = pn(l, u);
    }, Xn.getArrowWidth = Xn.getArrowHeight = function(t, e) {
      var r = this.arrowWidthCache = this.arrowWidthCache || {}, a = r[t + ", " + e];
      return a || (a = Math.max(Math.pow(t * 13.37, 0.9), 29) * e, r[t + ", " + e] = a, a);
    };
    var Vt = {};
    Vt.findHaystackPoints = function(t) {
      for (var e = 0; e < t.length; e++) {
        var r = t[e], a = r._private, n = a.rscratch;
        if (!n.haystack) {
          var i = Math.random() * 2 * Math.PI;
          n.source = {
            x: Math.cos(i),
            y: Math.sin(i)
          }, i = Math.random() * 2 * Math.PI, n.target = {
            x: Math.cos(i),
            y: Math.sin(i)
          };
        }
        var s = a.source, o = a.target, l = s.position(), u = o.position(), f = s.width(), h = o.width(), c = s.height(), v = o.height(), d = r.pstyle("haystack-radius").value, g = d / 2;
        n.haystackPts = n.allpts = [n.source.x * f * g + l.x, n.source.y * c * g + l.y, n.target.x * h * g + u.x, n.target.y * v * g + u.y], n.midX = (n.allpts[0] + n.allpts[2]) / 2, n.midY = (n.allpts[1] + n.allpts[3]) / 2, n.edgeType = "haystack", n.haystack = !0, this.storeEdgeProjections(r), this.calculateArrowAngles(r), this.recalculateEdgeLabelProjections(r), this.calculateLabelAngles(r);
      }
    }, Vt.findSegmentsPoints = function(t, e) {
      var r = t._private.rscratch, a = e.posPts, n = e.intersectionPts, i = e.vectorNormInverse, s = t.pstyle("edge-distances").value, o = t.pstyle("segment-weights"), l = t.pstyle("segment-distances"), u = Math.min(o.pfValue.length, l.pfValue.length);
      r.edgeType = "segments", r.segpts = [];
      for (var f = 0; f < u; f++) {
        var h = o.pfValue[f], c = l.pfValue[f], v = 1 - h, d = h, g = s === "node-position" ? a : n, y = {
          x: g.x1 * v + g.x2 * d,
          y: g.y1 * v + g.y2 * d
        };
        r.segpts.push(y.x + i.x * c, y.y + i.y * c);
      }
    }, Vt.findLoopPoints = function(t, e, r, a) {
      var n = t._private.rscratch, i = e.dirCounts, s = e.srcPos, o = t.pstyle("control-point-distances"), l = o ? o.pfValue[0] : void 0, u = t.pstyle("loop-direction").pfValue, f = t.pstyle("loop-sweep").pfValue, h = t.pstyle("control-point-step-size").pfValue;
      n.edgeType = "self";
      var c = r, v = h;
      a && (c = 0, v = l);
      var d = u - Math.PI / 2, g = d - f / 2, y = d + f / 2, p = String(u + "_" + f);
      c = i[p] === void 0 ? i[p] = 0 : ++i[p], n.ctrlpts = [s.x + Math.cos(g) * 1.4 * v * (c / 3 + 1), s.y + Math.sin(g) * 1.4 * v * (c / 3 + 1), s.x + Math.cos(y) * 1.4 * v * (c / 3 + 1), s.y + Math.sin(y) * 1.4 * v * (c / 3 + 1)];
    }, Vt.findCompoundLoopPoints = function(t, e, r, a) {
      var n = t._private.rscratch;
      n.edgeType = "compound";
      var i = e.srcPos, s = e.tgtPos, o = e.srcW, l = e.srcH, u = e.tgtW, f = e.tgtH, h = t.pstyle("control-point-step-size").pfValue, c = t.pstyle("control-point-distances"), v = c ? c.pfValue[0] : void 0, d = r, g = h;
      a && (d = 0, g = v);
      var y = 50, p = {
        x: i.x - o / 2,
        y: i.y - l / 2
      }, m = {
        x: s.x - u / 2,
        y: s.y - f / 2
      }, b = {
        x: Math.min(p.x, m.x),
        y: Math.min(p.y, m.y)
      }, E = 0.5, M = Math.max(E, Math.log(o * 0.01)), O = Math.max(E, Math.log(u * 0.01));
      n.ctrlpts = [b.x, b.y - (1 + Math.pow(y, 1.12) / 100) * g * (d / 3 + 1) * M, b.x - (1 + Math.pow(y, 1.12) / 100) * g * (d / 3 + 1) * O, b.y];
    }, Vt.findStraightEdgePoints = function(t) {
      t._private.rscratch.edgeType = "straight";
    }, Vt.findBezierPoints = function(t, e, r, a, n) {
      var i = t._private.rscratch, s = e.vectorNormInverse, o = e.posPts, l = e.intersectionPts, u = t.pstyle("edge-distances").value, f = t.pstyle("control-point-step-size").pfValue, h = t.pstyle("control-point-distances"), c = t.pstyle("control-point-weights"), v = h && c ? Math.min(h.value.length, c.value.length) : 1, d = h ? h.pfValue[0] : void 0, g = c.value[0], y = a;
      i.edgeType = y ? "multibezier" : "bezier", i.ctrlpts = [];
      for (var p = 0; p < v; p++) {
        var m = (0.5 - e.eles.length / 2 + r) * f * (n ? -1 : 1), b = void 0, E = Es(m);
        y && (d = h ? h.pfValue[p] : f, g = c.value[p]), a ? b = d : b = d !== void 0 ? E * d : void 0;
        var M = b !== void 0 ? b : m, O = 1 - g, x = g, I = u === "node-position" ? o : l, C = {
          x: I.x1 * O + I.x2 * x,
          y: I.y1 * O + I.y2 * x
        };
        i.ctrlpts.push(C.x + s.x * M, C.y + s.y * M);
      }
    }, Vt.findTaxiPoints = function(t, e) {
      var r = t._private.rscratch;
      r.edgeType = "segments";
      var a = "vertical", n = "horizontal", i = "leftward", s = "rightward", o = "downward", l = "upward", u = "auto", f = e.posPts, h = e.srcW, c = e.srcH, v = e.tgtW, d = e.tgtH, g = t.pstyle("edge-distances").value, y = g !== "node-position", p = t.pstyle("taxi-direction").value, m = p, b = t.pstyle("taxi-turn"), E = b.units === "%", M = b.pfValue, O = M < 0, x = t.pstyle("taxi-turn-min-distance").pfValue, I = y ? (h + v) / 2 : 0, C = y ? (c + d) / 2 : 0, B = f.x2 - f.x1, F = f.y2 - f.y1, R = function(ze, at) {
        return ze > 0 ? Math.max(ze - at, 0) : Math.min(ze + at, 0);
      }, X = R(B, I), z = R(F, C), re = !1;
      m === u ? p = Math.abs(X) > Math.abs(z) ? n : a : m === l || m === o ? (p = a, re = !0) : (m === i || m === s) && (p = n, re = !0);
      var W = p === a, Z = W ? z : X, ie = W ? F : B, oe = Es(ie), ge = !1;
      !(re && (E || O)) && (m === o && ie < 0 || m === l && ie > 0 || m === i && ie > 0 || m === s && ie < 0) && (oe *= -1, Z = oe * Math.abs(Z), ge = !0);
      var se;
      if (E) {
        var de = M < 0 ? 1 + M : M;
        se = de * Z;
      } else {
        var we = M < 0 ? Z : 0;
        se = we + M * oe;
      }
      var Te = function(ze) {
        return Math.abs(ze) < x || Math.abs(ze) >= Math.abs(Z);
      }, Ee = Te(se), ye = Te(Math.abs(Z) - Math.abs(se)), ae = Ee || ye;
      if (ae && !ge)
        if (W) {
          var xe = Math.abs(ie) <= c / 2, Ce = Math.abs(B) <= v / 2;
          if (xe) {
            var Oe = (f.x1 + f.x2) / 2, Ie = f.y1, He = f.y2;
            r.segpts = [Oe, Ie, Oe, He];
          } else if (Ce) {
            var qe = (f.y1 + f.y2) / 2, Re = f.x1, Me = f.x2;
            r.segpts = [Re, qe, Me, qe];
          } else
            r.segpts = [f.x1, f.y2];
        } else {
          var Ve = Math.abs(ie) <= h / 2, Fe = Math.abs(F) <= d / 2;
          if (Ve) {
            var ke = (f.y1 + f.y2) / 2, Ge = f.x1, et = f.x2;
            r.segpts = [Ge, ke, et, ke];
          } else if (Fe) {
            var We = (f.x1 + f.x2) / 2, Ye = f.y1, Se = f.y2;
            r.segpts = [We, Ye, We, Se];
          } else
            r.segpts = [f.x2, f.y1];
        }
      else if (W) {
        var N = f.y1 + se + (y ? c / 2 * oe : 0), le = f.x1, De = f.x2;
        r.segpts = [le, N, De, N];
      } else {
        var me = f.x1 + se + (y ? h / 2 * oe : 0), be = f.y1, Ke = f.y2;
        r.segpts = [me, be, me, Ke];
      }
    }, Vt.tryToCorrectInvalidPoints = function(t, e) {
      var r = t._private.rscratch;
      if (r.edgeType === "bezier") {
        var a = e.srcPos, n = e.tgtPos, i = e.srcW, s = e.srcH, o = e.tgtW, l = e.tgtH, u = e.srcShape, f = e.tgtShape, h = !k(r.startX) || !k(r.startY), c = !k(r.arrowStartX) || !k(r.arrowStartY), v = !k(r.endX) || !k(r.endY), d = !k(r.arrowEndX) || !k(r.arrowEndY), g = 3, y = this.getArrowWidth(t.pstyle("width").pfValue, t.pstyle("arrow-scale").value) * this.arrowShapeWidth, p = g * y, m = Pr({
          x: r.ctrlpts[0],
          y: r.ctrlpts[1]
        }, {
          x: r.startX,
          y: r.startY
        }), b = m < p, E = Pr({
          x: r.ctrlpts[0],
          y: r.ctrlpts[1]
        }, {
          x: r.endX,
          y: r.endY
        }), M = E < p, O = !1;
        if (h || c || b) {
          O = !0;
          var x = {
            // delta
            x: r.ctrlpts[0] - a.x,
            y: r.ctrlpts[1] - a.y
          }, I = Math.sqrt(x.x * x.x + x.y * x.y), C = {
            // normalised delta
            x: x.x / I,
            y: x.y / I
          }, B = Math.max(i, s), F = {
            // *2 radius guarantees outside shape
            x: r.ctrlpts[0] + C.x * 2 * B,
            y: r.ctrlpts[1] + C.y * 2 * B
          }, R = u.intersectLine(a.x, a.y, i, s, F.x, F.y, 0);
          b ? (r.ctrlpts[0] = r.ctrlpts[0] + C.x * (p - m), r.ctrlpts[1] = r.ctrlpts[1] + C.y * (p - m)) : (r.ctrlpts[0] = R[0] + C.x * p, r.ctrlpts[1] = R[1] + C.y * p);
        }
        if (v || d || M) {
          O = !0;
          var X = {
            // delta
            x: r.ctrlpts[0] - n.x,
            y: r.ctrlpts[1] - n.y
          }, z = Math.sqrt(X.x * X.x + X.y * X.y), re = {
            // normalised delta
            x: X.x / z,
            y: X.y / z
          }, W = Math.max(i, s), Z = {
            // *2 radius guarantees outside shape
            x: r.ctrlpts[0] + re.x * 2 * W,
            y: r.ctrlpts[1] + re.y * 2 * W
          }, ie = f.intersectLine(n.x, n.y, o, l, Z.x, Z.y, 0);
          M ? (r.ctrlpts[0] = r.ctrlpts[0] + re.x * (p - E), r.ctrlpts[1] = r.ctrlpts[1] + re.y * (p - E)) : (r.ctrlpts[0] = ie[0] + re.x * p, r.ctrlpts[1] = ie[1] + re.y * p);
        }
        O && this.findEndpoints(t);
      }
    }, Vt.storeAllpts = function(t) {
      var e = t._private.rscratch;
      if (e.edgeType === "multibezier" || e.edgeType === "bezier" || e.edgeType === "self" || e.edgeType === "compound") {
        e.allpts = [], e.allpts.push(e.startX, e.startY);
        for (var r = 0; r + 1 < e.ctrlpts.length; r += 2)
          e.allpts.push(e.ctrlpts[r], e.ctrlpts[r + 1]), r + 3 < e.ctrlpts.length && e.allpts.push((e.ctrlpts[r] + e.ctrlpts[r + 2]) / 2, (e.ctrlpts[r + 1] + e.ctrlpts[r + 3]) / 2);
        e.allpts.push(e.endX, e.endY);
        var a, n;
        e.ctrlpts.length / 2 % 2 === 0 ? (a = e.allpts.length / 2 - 1, e.midX = e.allpts[a], e.midY = e.allpts[a + 1]) : (a = e.allpts.length / 2 - 3, n = 0.5, e.midX = St(e.allpts[a], e.allpts[a + 2], e.allpts[a + 4], n), e.midY = St(e.allpts[a + 1], e.allpts[a + 3], e.allpts[a + 5], n));
      } else if (e.edgeType === "straight")
        e.allpts = [e.startX, e.startY, e.endX, e.endY], e.midX = (e.startX + e.endX + e.arrowStartX + e.arrowEndX) / 4, e.midY = (e.startY + e.endY + e.arrowStartY + e.arrowEndY) / 4;
      else if (e.edgeType === "segments")
        if (e.allpts = [], e.allpts.push(e.startX, e.startY), e.allpts.push.apply(e.allpts, e.segpts), e.allpts.push(e.endX, e.endY), e.segpts.length % 4 === 0) {
          var i = e.segpts.length / 2, s = i - 2;
          e.midX = (e.segpts[s] + e.segpts[i]) / 2, e.midY = (e.segpts[s + 1] + e.segpts[i + 1]) / 2;
        } else {
          var o = e.segpts.length / 2 - 1;
          e.midX = e.segpts[o], e.midY = e.segpts[o + 1];
        }
    }, Vt.checkForInvalidEdgeWarning = function(t) {
      var e = t[0]._private.rscratch;
      e.nodesOverlap || k(e.startX) && k(e.startY) && k(e.endX) && k(e.endY) ? e.loggedErr = !1 : e.loggedErr || (e.loggedErr = !0, ft("Edge `" + t.id() + "` has invalid endpoints and so it is impossible to draw.  Adjust your edge style (e.g. control points) accordingly or use an alternative edge type.  This is expected behaviour when the source node and the target node overlap."));
    }, Vt.findEdgeControlPoints = function(t) {
      var e = this;
      if (!(!t || t.length === 0)) {
        for (var r = this, a = r.cy, n = a.hasCompoundNodes(), i = {
          map: new ur(),
          get: function(x) {
            var I = this.map.get(x[0]);
            return I != null ? I.get(x[1]) : null;
          },
          set: function(x, I) {
            var C = this.map.get(x[0]);
            C == null && (C = new ur(), this.map.set(x[0], C)), C.set(x[1], I);
          }
        }, s = [], o = [], l = 0; l < t.length; l++) {
          var u = t[l], f = u._private, h = u.pstyle("curve-style").value;
          if (!(u.removed() || !u.takesUpSpace())) {
            if (h === "haystack") {
              o.push(u);
              continue;
            }
            var c = h === "unbundled-bezier" || h === "segments" || h === "straight" || h === "straight-triangle" || h === "taxi", v = h === "unbundled-bezier" || h === "bezier", d = f.source, g = f.target, y = d.poolIndex(), p = g.poolIndex(), m = [y, p].sort(), b = i.get(m);
            b == null && (b = {
              eles: []
            }, i.set(m, b), s.push(m)), b.eles.push(u), c && (b.hasUnbundled = !0), v && (b.hasBezier = !0);
          }
        }
        for (var E = function(x) {
          var I = s[x], C = i.get(I), B = void 0;
          if (!C.hasUnbundled) {
            var F = C.eles[0].parallelEdges().filter(function(Se) {
              return Se.isBundledBezier();
            });
            oi(C.eles), F.forEach(function(Se) {
              return C.eles.push(Se);
            }), C.eles.sort(function(Se, N) {
              return Se.poolIndex() - N.poolIndex();
            });
          }
          var R = C.eles[0], X = R.source(), z = R.target();
          if (X.poolIndex() > z.poolIndex()) {
            var re = X;
            X = z, z = re;
          }
          var W = C.srcPos = X.position(), Z = C.tgtPos = z.position(), ie = C.srcW = X.outerWidth(), oe = C.srcH = X.outerHeight(), ge = C.tgtW = z.outerWidth(), se = C.tgtH = z.outerHeight(), de = C.srcShape = r.nodeShapes[e.getNodeShape(X)], we = C.tgtShape = r.nodeShapes[e.getNodeShape(z)];
          C.dirCounts = {
            north: 0,
            west: 0,
            south: 0,
            east: 0,
            northwest: 0,
            southwest: 0,
            northeast: 0,
            southeast: 0
          };
          for (var Te = 0; Te < C.eles.length; Te++) {
            var Ee = C.eles[Te], ye = Ee[0]._private.rscratch, ae = Ee.pstyle("curve-style").value, xe = ae === "unbundled-bezier" || ae === "segments" || ae === "taxi", Ce = !X.same(Ee.source());
            if (!C.calculatedIntersection && X !== z && (C.hasBezier || C.hasUnbundled)) {
              C.calculatedIntersection = !0;
              var Oe = de.intersectLine(W.x, W.y, ie, oe, Z.x, Z.y, 0), Ie = C.srcIntn = Oe, He = we.intersectLine(Z.x, Z.y, ge, se, W.x, W.y, 0), qe = C.tgtIntn = He, Re = C.intersectionPts = {
                x1: Oe[0],
                x2: He[0],
                y1: Oe[1],
                y2: He[1]
              }, Me = C.posPts = {
                x1: W.x,
                x2: Z.x,
                y1: W.y,
                y2: Z.y
              }, Ve = He[1] - Oe[1], Fe = He[0] - Oe[0], ke = Math.sqrt(Fe * Fe + Ve * Ve), Ge = C.vector = {
                x: Fe,
                y: Ve
              }, et = C.vectorNorm = {
                x: Ge.x / ke,
                y: Ge.y / ke
              }, We = {
                x: -et.y,
                y: et.x
              };
              C.nodesOverlap = !k(ke) || we.checkPoint(Oe[0], Oe[1], 0, ge, se, Z.x, Z.y) || de.checkPoint(He[0], He[1], 0, ie, oe, W.x, W.y), C.vectorNormInverse = We, B = {
                nodesOverlap: C.nodesOverlap,
                dirCounts: C.dirCounts,
                calculatedIntersection: !0,
                hasBezier: C.hasBezier,
                hasUnbundled: C.hasUnbundled,
                eles: C.eles,
                srcPos: Z,
                tgtPos: W,
                srcW: ge,
                srcH: se,
                tgtW: ie,
                tgtH: oe,
                srcIntn: qe,
                tgtIntn: Ie,
                srcShape: we,
                tgtShape: de,
                posPts: {
                  x1: Me.x2,
                  y1: Me.y2,
                  x2: Me.x1,
                  y2: Me.y1
                },
                intersectionPts: {
                  x1: Re.x2,
                  y1: Re.y2,
                  x2: Re.x1,
                  y2: Re.y1
                },
                vector: {
                  x: -Ge.x,
                  y: -Ge.y
                },
                vectorNorm: {
                  x: -et.x,
                  y: -et.y
                },
                vectorNormInverse: {
                  x: -We.x,
                  y: -We.y
                }
              };
            }
            var Ye = Ce ? B : C;
            ye.nodesOverlap = Ye.nodesOverlap, ye.srcIntn = Ye.srcIntn, ye.tgtIntn = Ye.tgtIntn, n && (X.isParent() || X.isChild() || z.isParent() || z.isChild()) && (X.parents().anySame(z) || z.parents().anySame(X) || X.same(z) && X.isParent()) ? e.findCompoundLoopPoints(Ee, Ye, Te, xe) : X === z ? e.findLoopPoints(Ee, Ye, Te, xe) : ae === "segments" ? e.findSegmentsPoints(Ee, Ye) : ae === "taxi" ? e.findTaxiPoints(Ee, Ye) : ae === "straight" || !xe && C.eles.length % 2 === 1 && Te === Math.floor(C.eles.length / 2) ? e.findStraightEdgePoints(Ee) : e.findBezierPoints(Ee, Ye, Te, xe, Ce), e.findEndpoints(Ee), e.tryToCorrectInvalidPoints(Ee, Ye), e.checkForInvalidEdgeWarning(Ee), e.storeAllpts(Ee), e.storeEdgeProjections(Ee), e.calculateArrowAngles(Ee), e.recalculateEdgeLabelProjections(Ee), e.calculateLabelAngles(Ee);
          }
        }, M = 0; M < s.length; M++)
          E(M);
        this.findHaystackPoints(o);
      }
    };
    function iu(t) {
      var e = [];
      if (t != null) {
        for (var r = 0; r < t.length; r += 2) {
          var a = t[r], n = t[r + 1];
          e.push({
            x: a,
            y: n
          });
        }
        return e;
      }
    }
    Vt.getSegmentPoints = function(t) {
      var e = t[0]._private.rscratch, r = e.edgeType;
      if (r === "segments")
        return this.recalculateRenderedStyle(t), iu(e.segpts);
    }, Vt.getControlPoints = function(t) {
      var e = t[0]._private.rscratch, r = e.edgeType;
      if (r === "bezier" || r === "multibezier" || r === "self" || r === "compound")
        return this.recalculateRenderedStyle(t), iu(e.ctrlpts);
    }, Vt.getEdgeMidpoint = function(t) {
      var e = t[0]._private.rscratch;
      return this.recalculateRenderedStyle(t), {
        x: e.midX,
        y: e.midY
      };
    };
    var Qa = {};
    Qa.manualEndptToPx = function(t, e) {
      var r = this, a = t.position(), n = t.outerWidth(), i = t.outerHeight();
      if (e.value.length === 2) {
        var s = [e.pfValue[0], e.pfValue[1]];
        return e.units[0] === "%" && (s[0] = s[0] * n), e.units[1] === "%" && (s[1] = s[1] * i), s[0] += a.x, s[1] += a.y, s;
      } else {
        var o = e.pfValue[0];
        o = -Math.PI / 2 + o;
        var l = 2 * Math.max(n, i), u = [a.x + Math.cos(o) * l, a.y + Math.sin(o) * l];
        return r.nodeShapes[this.getNodeShape(t)].intersectLine(a.x, a.y, n, i, u[0], u[1], 0);
      }
    }, Qa.findEndpoints = function(t) {
      var e = this, r, a = t.source()[0], n = t.target()[0], i = a.position(), s = n.position(), o = t.pstyle("target-arrow-shape").value, l = t.pstyle("source-arrow-shape").value, u = t.pstyle("target-distance-from-node").pfValue, f = t.pstyle("source-distance-from-node").pfValue, h = t.pstyle("curve-style").value, c = t._private.rscratch, v = c.edgeType, d = h === "taxi", g = v === "self" || v === "compound", y = v === "bezier" || v === "multibezier" || g, p = v !== "bezier", m = v === "straight" || v === "segments", b = v === "segments", E = y || p || m, M = g || d, O = t.pstyle("source-endpoint"), x = M ? "outside-to-node" : O.value, I = t.pstyle("target-endpoint"), C = M ? "outside-to-node" : I.value;
      c.srcManEndpt = O, c.tgtManEndpt = I;
      var B, F, R, X;
      if (y) {
        var z = [c.ctrlpts[0], c.ctrlpts[1]], re = p ? [c.ctrlpts[c.ctrlpts.length - 2], c.ctrlpts[c.ctrlpts.length - 1]] : z;
        B = re, F = z;
      } else if (m) {
        var W = b ? c.segpts.slice(0, 2) : [s.x, s.y], Z = b ? c.segpts.slice(c.segpts.length - 2) : [i.x, i.y];
        B = Z, F = W;
      }
      if (C === "inside-to-node")
        r = [s.x, s.y];
      else if (I.units)
        r = this.manualEndptToPx(n, I);
      else if (C === "outside-to-line")
        r = c.tgtIntn;
      else if (C === "outside-to-node" || C === "outside-to-node-or-label" ? R = B : (C === "outside-to-line" || C === "outside-to-line-or-label") && (R = [i.x, i.y]), r = e.nodeShapes[this.getNodeShape(n)].intersectLine(s.x, s.y, n.outerWidth(), n.outerHeight(), R[0], R[1], 0), C === "outside-to-node-or-label" || C === "outside-to-line-or-label") {
        var ie = n._private.rscratch, oe = ie.labelWidth, ge = ie.labelHeight, se = ie.labelX, de = ie.labelY, we = oe / 2, Te = ge / 2, Ee = n.pstyle("text-valign").value;
        Ee === "top" ? de -= Te : Ee === "bottom" && (de += Te);
        var ye = n.pstyle("text-halign").value;
        ye === "left" ? se -= we : ye === "right" && (se += we);
        var ae = Ba(R[0], R[1], [se - we, de - Te, se + we, de - Te, se + we, de + Te, se - we, de + Te], s.x, s.y);
        if (ae.length > 0) {
          var xe = i, Ce = Br(xe, jr(r)), Oe = Br(xe, jr(ae)), Ie = Ce;
          if (Oe < Ce && (r = ae, Ie = Oe), ae.length > 2) {
            var He = Br(xe, {
              x: ae[2],
              y: ae[3]
            });
            He < Ie && (r = [ae[2], ae[3]]);
          }
        }
      }
      var qe = mn(r, B, e.arrowShapes[o].spacing(t) + u), Re = mn(r, B, e.arrowShapes[o].gap(t) + u);
      if (c.endX = Re[0], c.endY = Re[1], c.arrowEndX = qe[0], c.arrowEndY = qe[1], x === "inside-to-node")
        r = [i.x, i.y];
      else if (O.units)
        r = this.manualEndptToPx(a, O);
      else if (x === "outside-to-line")
        r = c.srcIntn;
      else if (x === "outside-to-node" || x === "outside-to-node-or-label" ? X = F : (x === "outside-to-line" || x === "outside-to-line-or-label") && (X = [s.x, s.y]), r = e.nodeShapes[this.getNodeShape(a)].intersectLine(i.x, i.y, a.outerWidth(), a.outerHeight(), X[0], X[1], 0), x === "outside-to-node-or-label" || x === "outside-to-line-or-label") {
        var Me = a._private.rscratch, Ve = Me.labelWidth, Fe = Me.labelHeight, ke = Me.labelX, Ge = Me.labelY, et = Ve / 2, We = Fe / 2, Ye = a.pstyle("text-valign").value;
        Ye === "top" ? Ge -= We : Ye === "bottom" && (Ge += We);
        var Se = a.pstyle("text-halign").value;
        Se === "left" ? ke -= et : Se === "right" && (ke += et);
        var N = Ba(X[0], X[1], [ke - et, Ge - We, ke + et, Ge - We, ke + et, Ge + We, ke - et, Ge + We], i.x, i.y);
        if (N.length > 0) {
          var le = s, De = Br(le, jr(r)), me = Br(le, jr(N)), be = De;
          if (me < De && (r = [N[0], N[1]], be = me), N.length > 2) {
            var Ke = Br(le, {
              x: N[2],
              y: N[3]
            });
            Ke < be && (r = [N[2], N[3]]);
          }
        }
      }
      var Le = mn(r, F, e.arrowShapes[l].spacing(t) + f), ze = mn(r, F, e.arrowShapes[l].gap(t) + f);
      c.startX = ze[0], c.startY = ze[1], c.arrowStartX = Le[0], c.arrowStartY = Le[1], E && (!k(c.startX) || !k(c.startY) || !k(c.endX) || !k(c.endY) ? c.badLine = !0 : c.badLine = !1);
    }, Qa.getSourceEndpoint = function(t) {
      var e = t[0]._private.rscratch;
      switch (this.recalculateRenderedStyle(t), e.edgeType) {
        case "haystack":
          return {
            x: e.haystackPts[0],
            y: e.haystackPts[1]
          };
        default:
          return {
            x: e.arrowStartX,
            y: e.arrowStartY
          };
      }
    }, Qa.getTargetEndpoint = function(t) {
      var e = t[0]._private.rscratch;
      switch (this.recalculateRenderedStyle(t), e.edgeType) {
        case "haystack":
          return {
            x: e.haystackPts[2],
            y: e.haystackPts[3]
          };
        default:
          return {
            x: e.arrowEndX,
            y: e.arrowEndY
          };
      }
    };
    var Gi = {};
    function cg(t, e, r) {
      for (var a = function(u, f, h, c) {
        return St(u, f, h, c);
      }, n = e._private, i = n.rstyle.bezierPts, s = 0; s < t.bezierProjPcts.length; s++) {
        var o = t.bezierProjPcts[s];
        i.push({
          x: a(r[0], r[2], r[4], o),
          y: a(r[1], r[3], r[5], o)
        });
      }
    }
    Gi.storeEdgeProjections = function(t) {
      var e = t._private, r = e.rscratch, a = r.edgeType;
      if (e.rstyle.bezierPts = null, e.rstyle.linePts = null, e.rstyle.haystackPts = null, a === "multibezier" || a === "bezier" || a === "self" || a === "compound") {
        e.rstyle.bezierPts = [];
        for (var n = 0; n + 5 < r.allpts.length; n += 4)
          cg(this, t, r.allpts.slice(n, n + 6));
      } else if (a === "segments")
        for (var i = e.rstyle.linePts = [], n = 0; n + 1 < r.allpts.length; n += 2)
          i.push({
            x: r.allpts[n],
            y: r.allpts[n + 1]
          });
      else if (a === "haystack") {
        var s = r.haystackPts;
        e.rstyle.haystackPts = [{
          x: s[0],
          y: s[1]
        }, {
          x: s[2],
          y: s[3]
        }];
      }
      e.rstyle.arrowWidth = this.getArrowWidth(t.pstyle("width").pfValue, t.pstyle("arrow-scale").value) * this.arrowShapeWidth;
    }, Gi.recalculateEdgeProjections = function(t) {
      this.findEdgeControlPoints(t);
    };
    var fr = {};
    fr.recalculateNodeLabelProjection = function(t) {
      var e = t.pstyle("label").strValue;
      if (!Pe(e)) {
        var r, a, n = t._private, i = t.width(), s = t.height(), o = t.padding(), l = t.position(), u = t.pstyle("text-halign").strValue, f = t.pstyle("text-valign").strValue, h = n.rscratch, c = n.rstyle;
        switch (u) {
          case "left":
            r = l.x - i / 2 - o;
            break;
          case "right":
            r = l.x + i / 2 + o;
            break;
          default:
            r = l.x;
        }
        switch (f) {
          case "top":
            a = l.y - s / 2 - o;
            break;
          case "bottom":
            a = l.y + s / 2 + o;
            break;
          default:
            a = l.y;
        }
        h.labelX = r, h.labelY = a, c.labelX = r, c.labelY = a, this.calculateLabelAngles(t), this.applyLabelDimensions(t);
      }
    };
    var su = function(e, r) {
      var a = Math.atan(r / e);
      return e === 0 && a < 0 && (a = a * -1), a;
    }, ou = function(e, r) {
      var a = r.x - e.x, n = r.y - e.y;
      return su(a, n);
    }, vg = function(e, r, a, n) {
      var i = ka(0, n - 1e-3, 1), s = ka(0, n + 1e-3, 1), o = ea(e, r, a, i), l = ea(e, r, a, s);
      return ou(o, l);
    };
    fr.recalculateEdgeLabelProjections = function(t) {
      var e, r = t._private, a = r.rscratch, n = this, i = {
        mid: t.pstyle("label").strValue,
        source: t.pstyle("source-label").strValue,
        target: t.pstyle("target-label").strValue
      };
      if (i.mid || i.source || i.target) {
        e = {
          x: a.midX,
          y: a.midY
        };
        var s = function(h, c, v) {
          xr(r.rscratch, h, c, v), xr(r.rstyle, h, c, v);
        };
        s("labelX", null, e.x), s("labelY", null, e.y);
        var o = su(a.midDispX, a.midDispY);
        s("labelAutoAngle", null, o);
        var l = function f() {
          if (f.cache)
            return f.cache;
          for (var h = [], c = 0; c + 5 < a.allpts.length; c += 4) {
            var v = {
              x: a.allpts[c],
              y: a.allpts[c + 1]
            }, d = {
              x: a.allpts[c + 2],
              y: a.allpts[c + 3]
            }, g = {
              x: a.allpts[c + 4],
              y: a.allpts[c + 5]
            };
            h.push({
              p0: v,
              p1: d,
              p2: g,
              startDist: 0,
              length: 0,
              segments: []
            });
          }
          var y = r.rstyle.bezierPts, p = n.bezierProjPcts.length;
          function m(x, I, C, B, F) {
            var R = Pr(I, C), X = x.segments[x.segments.length - 1], z = {
              p0: I,
              p1: C,
              t0: B,
              t1: F,
              startDist: X ? X.startDist + X.length : 0,
              length: R
            };
            x.segments.push(z), x.length += R;
          }
          for (var b = 0; b < h.length; b++) {
            var E = h[b], M = h[b - 1];
            M && (E.startDist = M.startDist + M.length), m(E, E.p0, y[b * p], 0, n.bezierProjPcts[0]);
            for (var O = 0; O < p - 1; O++)
              m(E, y[b * p + O], y[b * p + O + 1], n.bezierProjPcts[O], n.bezierProjPcts[O + 1]);
            m(E, y[b * p + p - 1], E.p2, n.bezierProjPcts[p - 1], 1);
          }
          return f.cache = h;
        }, u = function(h) {
          var c, v = h === "source";
          if (i[h]) {
            var d = t.pstyle(h + "-text-offset").pfValue;
            switch (a.edgeType) {
              case "self":
              case "compound":
              case "bezier":
              case "multibezier": {
                for (var g = l(), y, p = 0, m = 0, b = 0; b < g.length; b++) {
                  for (var E = g[v ? b : g.length - 1 - b], M = 0; M < E.segments.length; M++) {
                    var O = E.segments[v ? M : E.segments.length - 1 - M], x = b === g.length - 1 && M === E.segments.length - 1;
                    if (p = m, m += O.length, m >= d || x) {
                      y = {
                        cp: E,
                        segment: O
                      };
                      break;
                    }
                  }
                  if (y)
                    break;
                }
                var I = y.cp, C = y.segment, B = (d - p) / C.length, F = C.t1 - C.t0, R = v ? C.t0 + F * B : C.t1 - F * B;
                R = ka(0, R, 1), e = ea(I.p0, I.p1, I.p2, R), c = vg(I.p0, I.p1, I.p2, R);
                break;
              }
              case "straight":
              case "segments":
              case "haystack": {
                for (var X = 0, z, re, W, Z, ie = a.allpts.length, oe = 0; oe + 3 < ie && (v ? (W = {
                  x: a.allpts[oe],
                  y: a.allpts[oe + 1]
                }, Z = {
                  x: a.allpts[oe + 2],
                  y: a.allpts[oe + 3]
                }) : (W = {
                  x: a.allpts[ie - 2 - oe],
                  y: a.allpts[ie - 1 - oe]
                }, Z = {
                  x: a.allpts[ie - 4 - oe],
                  y: a.allpts[ie - 3 - oe]
                }), z = Pr(W, Z), re = X, X += z, !(X >= d)); oe += 2)
                  ;
                var ge = d - re, se = ge / z;
                se = ka(0, se, 1), e = xf(W, Z, se), c = ou(W, Z);
                break;
              }
            }
            s("labelX", h, e.x), s("labelY", h, e.y), s("labelAutoAngle", h, c);
          }
        };
        u("source"), u("target"), this.applyLabelDimensions(t);
      }
    }, fr.applyLabelDimensions = function(t) {
      this.applyPrefixedLabelDimensions(t), t.isEdge() && (this.applyPrefixedLabelDimensions(t, "source"), this.applyPrefixedLabelDimensions(t, "target"));
    }, fr.applyPrefixedLabelDimensions = function(t, e) {
      var r = t._private, a = this.getLabelText(t, e), n = this.calculateLabelDimensions(t, a), i = t.pstyle("line-height").pfValue, s = t.pstyle("text-wrap").strValue, o = er(r.rscratch, "labelWrapCachedLines", e) || [], l = s !== "wrap" ? 1 : Math.max(o.length, 1), u = n.height / l, f = u * i, h = n.width, c = n.height + (l - 1) * (i - 1) * u;
      xr(r.rstyle, "labelWidth", e, h), xr(r.rscratch, "labelWidth", e, h), xr(r.rstyle, "labelHeight", e, c), xr(r.rscratch, "labelHeight", e, c), xr(r.rscratch, "labelLineHeight", e, f);
    }, fr.getLabelText = function(t, e) {
      var r = t._private, a = e ? e + "-" : "", n = t.pstyle(a + "label").strValue, i = t.pstyle("text-transform").value, s = function(ge, se) {
        return se ? (xr(r.rscratch, ge, e, se), se) : er(r.rscratch, ge, e);
      };
      if (!n)
        return "";
      i == "none" || (i == "uppercase" ? n = n.toUpperCase() : i == "lowercase" && (n = n.toLowerCase()));
      var o = t.pstyle("text-wrap").value;
      if (o === "wrap") {
        var l = s("labelKey");
        if (l != null && s("labelWrapKey") === l)
          return s("labelWrapCachedText");
        for (var u = "​", f = n.split(`
`), h = t.pstyle("text-max-width").pfValue, c = t.pstyle("text-overflow-wrap").value, v = c === "anywhere", d = [], g = /[\s\u200b]+/, y = v ? "" : " ", p = 0; p < f.length; p++) {
          var m = f[p], b = this.calculateLabelDimensions(t, m), E = b.width;
          if (v) {
            var M = m.split("").join(u);
            m = M;
          }
          if (E > h) {
            for (var O = m.split(g), x = "", I = 0; I < O.length; I++) {
              var C = O[I], B = x.length === 0 ? C : x + y + C, F = this.calculateLabelDimensions(t, B), R = F.width;
              R <= h ? x += C + y : (x && d.push(x), x = C + y);
            }
            x.match(/^[\s\u200b]+$/) || d.push(x);
          } else
            d.push(m);
        }
        s("labelWrapCachedLines", d), n = s("labelWrapCachedText", d.join(`
`)), s("labelWrapKey", l);
      } else if (o === "ellipsis") {
        var X = t.pstyle("text-max-width").pfValue, z = "", re = "…", W = !1;
        if (this.calculateLabelDimensions(t, n).width < X)
          return n;
        for (var Z = 0; Z < n.length; Z++) {
          var ie = this.calculateLabelDimensions(t, z + n[Z] + re).width;
          if (ie > X)
            break;
          z += n[Z], Z === n.length - 1 && (W = !0);
        }
        return W || (z += re), z;
      }
      return n;
    }, fr.getLabelJustification = function(t) {
      var e = t.pstyle("text-justification").strValue, r = t.pstyle("text-halign").strValue;
      if (e === "auto")
        if (t.isNode())
          switch (r) {
            case "left":
              return "right";
            case "right":
              return "left";
            default:
              return "center";
          }
        else
          return "center";
      else
        return e;
    }, fr.calculateLabelDimensions = function(t, e) {
      var r = this, a = kr(e, t._private.labelDimsKey), n = r.labelDimCache || (r.labelDimCache = []), i = n[a];
      if (i != null)
        return i;
      var s = 0, o = t.pstyle("font-style").strValue, l = t.pstyle("font-size").pfValue, u = t.pstyle("font-family").strValue, f = t.pstyle("font-weight").strValue, h = this.labelCalcCanvas, c = this.labelCalcCanvasContext;
      if (!h) {
        h = this.labelCalcCanvas = document.createElement("canvas"), c = this.labelCalcCanvasContext = h.getContext("2d");
        var v = h.style;
        v.position = "absolute", v.left = "-9999px", v.top = "-9999px", v.zIndex = "-1", v.visibility = "hidden", v.pointerEvents = "none";
      }
      c.font = "".concat(o, " ").concat(f, " ").concat(l, "px ").concat(u);
      for (var d = 0, g = 0, y = e.split(`
`), p = 0; p < y.length; p++) {
        var m = y[p], b = c.measureText(m), E = Math.ceil(b.width), M = l;
        d = Math.max(E, d), g += M;
      }
      return d += s, g += s, n[a] = {
        width: d,
        height: g
      };
    }, fr.calculateLabelAngle = function(t, e) {
      var r = t._private, a = r.rscratch, n = t.isEdge(), i = e ? e + "-" : "", s = t.pstyle(i + "text-rotation"), o = s.strValue;
      return o === "none" ? 0 : n && o === "autorotate" ? a.labelAutoAngle : o === "autorotate" ? 0 : s.pfValue;
    }, fr.calculateLabelAngles = function(t) {
      var e = this, r = t.isEdge(), a = t._private, n = a.rscratch;
      n.labelAngle = e.calculateLabelAngle(t), r && (n.sourceLabelAngle = e.calculateLabelAngle(t, "source"), n.targetLabelAngle = e.calculateLabelAngle(t, "target"));
    };
    var uu = {}, lu = 28, fu = !1;
    uu.getNodeShape = function(t) {
      var e = this, r = t.pstyle("shape").value;
      if (r === "cutrectangle" && (t.width() < lu || t.height() < lu))
        return fu || (ft("The `cutrectangle` node shape can not be used at small sizes so `rectangle` is used instead"), fu = !0), "rectangle";
      if (t.isParent())
        return r === "rectangle" || r === "roundrectangle" || r === "round-rectangle" || r === "cutrectangle" || r === "cut-rectangle" || r === "barrel" ? r : "rectangle";
      if (r === "polygon") {
        var a = t.pstyle("shape-polygon-points").value;
        return e.nodeShapes.makePolygon(a).name;
      }
      return r;
    };
    var qn = {};
    qn.registerCalculationListeners = function() {
      var t = this.cy, e = t.collection(), r = this, a = function(s) {
        var o = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !0;
        if (e.merge(s), o)
          for (var l = 0; l < s.length; l++) {
            var u = s[l], f = u._private, h = f.rstyle;
            h.clean = !1, h.cleanConnected = !1;
          }
      };
      r.binder(t).on("bounds.* dirty.*", function(s) {
        var o = s.target;
        a(o);
      }).on("style.* background.*", function(s) {
        var o = s.target;
        a(o, !1);
      });
      var n = function(s) {
        if (s) {
          var o = r.onUpdateEleCalcsFns;
          e.cleanStyle();
          for (var l = 0; l < e.length; l++) {
            var u = e[l], f = u._private.rstyle;
            u.isNode() && !f.cleanConnected && (a(u.connectedEdges()), f.cleanConnected = !0);
          }
          if (o)
            for (var h = 0; h < o.length; h++) {
              var c = o[h];
              c(s, e);
            }
          r.recalculateRenderedStyle(e), e = t.collection();
        }
      };
      r.flushRenderedStyleQueue = function() {
        n(!0);
      }, r.beforeRender(n, r.beforeRenderPriorities.eleCalcs);
    }, qn.onUpdateEleCalcs = function(t) {
      var e = this.onUpdateEleCalcsFns = this.onUpdateEleCalcsFns || [];
      e.push(t);
    }, qn.recalculateRenderedStyle = function(t, e) {
      var r = function(E) {
        return E._private.rstyle.cleanConnected;
      }, a = [], n = [];
      if (!this.destroyed) {
        e === void 0 && (e = !0);
        for (var i = 0; i < t.length; i++) {
          var s = t[i], o = s._private, l = o.rstyle;
          s.isEdge() && (!r(s.source()) || !r(s.target())) && (l.clean = !1), !(e && l.clean || s.removed()) && s.pstyle("display").value !== "none" && (o.group === "nodes" ? n.push(s) : a.push(s), l.clean = !0);
        }
        for (var u = 0; u < n.length; u++) {
          var f = n[u], h = f._private, c = h.rstyle, v = f.position();
          this.recalculateNodeLabelProjection(f), c.nodeX = v.x, c.nodeY = v.y, c.nodeW = f.pstyle("width").pfValue, c.nodeH = f.pstyle("height").pfValue;
        }
        this.recalculateEdgeProjections(a);
        for (var d = 0; d < a.length; d++) {
          var g = a[d], y = g._private, p = y.rstyle, m = y.rscratch;
          p.srcX = m.arrowStartX, p.srcY = m.arrowStartY, p.tgtX = m.arrowEndX, p.tgtY = m.arrowEndY, p.midX = m.midX, p.midY = m.midY, p.labelAngle = m.labelAngle, p.sourceLabelAngle = m.sourceLabelAngle, p.targetLabelAngle = m.targetLabelAngle;
        }
      }
    };
    var Wn = {};
    Wn.updateCachedGrabbedEles = function() {
      var t = this.cachedZSortedEles;
      if (t) {
        t.drag = [], t.nondrag = [];
        for (var e = [], r = 0; r < t.length; r++) {
          var a = t[r], n = a._private.rscratch;
          a.grabbed() && !a.isParent() ? e.push(a) : n.inDragLayer ? t.drag.push(a) : t.nondrag.push(a);
        }
        for (var r = 0; r < e.length; r++) {
          var a = e[r];
          t.drag.push(a);
        }
      }
    }, Wn.invalidateCachedZSortedEles = function() {
      this.cachedZSortedEles = null;
    }, Wn.getCachedZSortedEles = function(t) {
      if (t || !this.cachedZSortedEles) {
        var e = this.cy.mutableElements().toArray();
        e.sort(Ro), e.interactive = e.filter(function(r) {
          return r.interactive();
        }), this.cachedZSortedEles = e, this.updateCachedGrabbedEles();
      } else
        e = this.cachedZSortedEles;
      return e;
    };
    var hu = {};
    [Vr, Xn, Vt, Qa, Gi, fr, uu, qn, Wn].forEach(function(t) {
      Ue(hu, t);
    });
    var cu = {};
    cu.getCachedImage = function(t, e, r) {
      var a = this, n = a.imageCache = a.imageCache || {}, i = n[t];
      if (i)
        return i.image.complete || i.image.addEventListener("load", r), i.image;
      i = n[t] = n[t] || {};
      var s = i.image = new Image();
      s.addEventListener("load", r), s.addEventListener("error", function() {
        s.error = !0;
      });
      var o = "data:", l = t.substring(0, o.length).toLowerCase() === o;
      return l || (s.crossOrigin = e), s.src = t, s;
    };
    var ya = {};
    ya.registerBinding = function(t, e, r, a) {
      var n = Array.prototype.slice.apply(arguments, [1]), i = this.binder(t);
      return i.on.apply(i, n);
    }, ya.binder = function(t) {
      var e = this, r = t === window || t === document || t === document.body || $e(t);
      if (e.supportsPassiveEvents == null) {
        var a = !1;
        try {
          var n = Object.defineProperty({}, "passive", {
            get: function() {
              return a = !0, !0;
            }
          });
          window.addEventListener("test", null, n);
        } catch {
        }
        e.supportsPassiveEvents = a;
      }
      var i = function(o, l, u) {
        var f = Array.prototype.slice.call(arguments);
        return r && e.supportsPassiveEvents && (f[2] = {
          capture: u ?? !1,
          passive: !1,
          once: !1
        }), e.bindings.push({
          target: t,
          args: f
        }), (t.addEventListener || t.on).apply(t, f), this;
      };
      return {
        on: i,
        addEventListener: i,
        addListener: i,
        bind: i
      };
    }, ya.nodeIsDraggable = function(t) {
      return t && t.isNode() && !t.locked() && t.grabbable();
    }, ya.nodeIsGrabbable = function(t) {
      return this.nodeIsDraggable(t) && t.interactive();
    }, ya.load = function() {
      var t = this, e = function(N) {
        return N.selected();
      }, r = function(N, le, De, me) {
        N == null && (N = t.cy);
        for (var be = 0; be < le.length; be++) {
          var Ke = le[be];
          N.emit({
            originalEvent: De,
            type: Ke,
            position: me
          });
        }
      }, a = function(N) {
        return N.shiftKey || N.metaKey || N.ctrlKey;
      }, n = function(N, le) {
        var De = !0;
        if (t.cy.hasCompoundNodes() && N && N.pannable())
          for (var me = 0; le && me < le.length; me++) {
            var N = le[me];
            if (N.isNode() && N.isParent() && !N.pannable()) {
              De = !1;
              break;
            }
          }
        else
          De = !0;
        return De;
      }, i = function(N) {
        N[0]._private.grabbed = !0;
      }, s = function(N) {
        N[0]._private.grabbed = !1;
      }, o = function(N) {
        N[0]._private.rscratch.inDragLayer = !0;
      }, l = function(N) {
        N[0]._private.rscratch.inDragLayer = !1;
      }, u = function(N) {
        N[0]._private.rscratch.isGrabTarget = !0;
      }, f = function(N) {
        N[0]._private.rscratch.isGrabTarget = !1;
      }, h = function(N, le) {
        var De = le.addToList, me = De.has(N);
        !me && N.grabbable() && !N.locked() && (De.merge(N), i(N));
      }, c = function(N, le) {
        if (N.cy().hasCompoundNodes() && !(le.inDragLayer == null && le.addToList == null)) {
          var De = N.descendants();
          le.inDragLayer && (De.forEach(o), De.connectedEdges().forEach(o)), le.addToList && h(De, le);
        }
      }, v = function(N, le) {
        le = le || {};
        var De = N.cy().hasCompoundNodes();
        le.inDragLayer && (N.forEach(o), N.neighborhood().stdFilter(function(me) {
          return !De || me.isEdge();
        }).forEach(o)), le.addToList && N.forEach(function(me) {
          h(me, le);
        }), c(N, le), y(N, {
          inDragLayer: le.inDragLayer
        }), t.updateCachedGrabbedEles();
      }, d = v, g = function(N) {
        N && (t.getCachedZSortedEles().forEach(function(le) {
          s(le), l(le), f(le);
        }), t.updateCachedGrabbedEles());
      }, y = function(N, le) {
        if (!(le.inDragLayer == null && le.addToList == null) && N.cy().hasCompoundNodes()) {
          var De = N.ancestors().orphans();
          if (!De.same(N)) {
            var me = De.descendants().spawnSelf().merge(De).unmerge(N).unmerge(N.descendants()), be = me.connectedEdges();
            le.inDragLayer && (be.forEach(o), me.forEach(o)), le.addToList && me.forEach(function(Ke) {
              h(Ke, le);
            });
          }
        }
      }, p = function() {
        document.activeElement != null && document.activeElement.blur != null && document.activeElement.blur();
      }, m = typeof MutationObserver < "u", b = typeof ResizeObserver < "u";
      m ? (t.removeObserver = new MutationObserver(function(Se) {
        for (var N = 0; N < Se.length; N++) {
          var le = Se[N], De = le.removedNodes;
          if (De)
            for (var me = 0; me < De.length; me++) {
              var be = De[me];
              if (be === t.container) {
                t.destroy();
                break;
              }
            }
        }
      }), t.container.parentNode && t.removeObserver.observe(t.container.parentNode, {
        childList: !0
      })) : t.registerBinding(t.container, "DOMNodeRemoved", function(Se) {
        t.destroy();
      });
      var E = fn(function() {
        t.cy.resize();
      }, 100);
      m && (t.styleObserver = new MutationObserver(E), t.styleObserver.observe(t.container, {
        attributes: !0
      })), t.registerBinding(window, "resize", E), b && (t.resizeObserver = new ResizeObserver(E), t.resizeObserver.observe(t.container));
      var M = function(N, le) {
        for (; N != null; )
          le(N), N = N.parentNode;
      }, O = function() {
        t.invalidateContainerClientCoordsCache();
      };
      M(t.container, function(Se) {
        t.registerBinding(Se, "transitionend", O), t.registerBinding(Se, "animationend", O), t.registerBinding(Se, "scroll", O);
      }), t.registerBinding(t.container, "contextmenu", function(Se) {
        Se.preventDefault();
      });
      var x = function() {
        return t.selection[4] !== 0;
      }, I = function(N) {
        for (var le = t.findContainerClientCoords(), De = le[0], me = le[1], be = le[2], Ke = le[3], Le = N.touches ? N.touches : [N], ze = !1, at = 0; at < Le.length; at++) {
          var dt = Le[at];
          if (De <= dt.clientX && dt.clientX <= De + be && me <= dt.clientY && dt.clientY <= me + Ke) {
            ze = !0;
            break;
          }
        }
        if (!ze)
          return !1;
        for (var Qe = t.container, ut = N.target, Ze = ut.parentNode, Je = !1; Ze; ) {
          if (Ze === Qe) {
            Je = !0;
            break;
          }
          Ze = Ze.parentNode;
        }
        return !!Je;
      };
      t.registerBinding(t.container, "mousedown", function(N) {
        if (I(N)) {
          N.preventDefault(), p(), t.hoverData.capture = !0, t.hoverData.which = N.which;
          var le = t.cy, De = [N.clientX, N.clientY], me = t.projectIntoViewport(De[0], De[1]), be = t.selection, Ke = t.findNearestElements(me[0], me[1], !0, !1), Le = Ke[0], ze = t.dragData.possibleDragElements;
          t.hoverData.mdownPos = me, t.hoverData.mdownGPos = De;
          var at = function() {
            t.hoverData.tapholdCancelled = !1, clearTimeout(t.hoverData.tapholdTimeout), t.hoverData.tapholdTimeout = setTimeout(function() {
              if (!t.hoverData.tapholdCancelled) {
                var Ct = t.hoverData.down;
                Ct ? Ct.emit({
                  originalEvent: N,
                  type: "taphold",
                  position: {
                    x: me[0],
                    y: me[1]
                  }
                }) : le.emit({
                  originalEvent: N,
                  type: "taphold",
                  position: {
                    x: me[0],
                    y: me[1]
                  }
                });
              }
            }, t.tapholdDuration);
          };
          if (N.which == 3) {
            t.hoverData.cxtStarted = !0;
            var dt = {
              originalEvent: N,
              type: "cxttapstart",
              position: {
                x: me[0],
                y: me[1]
              }
            };
            Le ? (Le.activate(), Le.emit(dt), t.hoverData.down = Le) : le.emit(dt), t.hoverData.downTime = new Date().getTime(), t.hoverData.cxtDragged = !1;
          } else if (N.which == 1) {
            Le && Le.activate();
            {
              if (Le != null && t.nodeIsGrabbable(Le)) {
                var Qe = function(Ct) {
                  return {
                    originalEvent: N,
                    type: Ct,
                    position: {
                      x: me[0],
                      y: me[1]
                    }
                  };
                }, ut = function(Ct) {
                  Ct.emit(Qe("grab"));
                };
                if (u(Le), !Le.selected())
                  ze = t.dragData.possibleDragElements = le.collection(), d(Le, {
                    addToList: ze
                  }), Le.emit(Qe("grabon")).emit(Qe("grab"));
                else {
                  ze = t.dragData.possibleDragElements = le.collection();
                  var Ze = le.$(function(Je) {
                    return Je.isNode() && Je.selected() && t.nodeIsGrabbable(Je);
                  });
                  v(Ze, {
                    addToList: ze
                  }), Le.emit(Qe("grabon")), Ze.forEach(ut);
                }
                t.redrawHint("eles", !0), t.redrawHint("drag", !0);
              }
              t.hoverData.down = Le, t.hoverData.downs = Ke, t.hoverData.downTime = new Date().getTime();
            }
            r(Le, ["mousedown", "tapstart", "vmousedown"], N, {
              x: me[0],
              y: me[1]
            }), Le == null ? (be[4] = 1, t.data.bgActivePosistion = {
              x: me[0],
              y: me[1]
            }, t.redrawHint("select", !0), t.redraw()) : Le.pannable() && (be[4] = 1), at();
          }
          be[0] = be[2] = me[0], be[1] = be[3] = me[1];
        }
      }, !1), t.registerBinding(window, "mousemove", function(N) {
        var le = t.hoverData.capture;
        if (!(!le && !I(N))) {
          var De = !1, me = t.cy, be = me.zoom(), Ke = [N.clientX, N.clientY], Le = t.projectIntoViewport(Ke[0], Ke[1]), ze = t.hoverData.mdownPos, at = t.hoverData.mdownGPos, dt = t.selection, Qe = null;
          !t.hoverData.draggingEles && !t.hoverData.dragging && !t.hoverData.selecting && (Qe = t.findNearestElement(Le[0], Le[1], !0, !1));
          var ut = t.hoverData.last, Ze = t.hoverData.down, Je = [Le[0] - dt[2], Le[1] - dt[3]], Ct = t.dragData.possibleDragElements, It;
          if (at) {
            var ar = Ke[0] - at[0], nr = ar * ar, Rt = Ke[1] - at[1], Qt = Rt * Rt, _t = nr + Qt;
            t.hoverData.isOverThresholdDrag = It = _t >= t.desktopTapThreshold2;
          }
          var br = a(N);
          It && (t.hoverData.tapholdCancelled = !0);
          var Ir = function() {
            var cr = t.hoverData.dragDelta = t.hoverData.dragDelta || [];
            cr.length === 0 ? (cr.push(Je[0]), cr.push(Je[1])) : (cr[0] += Je[0], cr[1] += Je[1]);
          };
          De = !0, r(Qe, ["mousemove", "vmousemove", "tapdrag"], N, {
            x: Le[0],
            y: Le[1]
          });
          var xa = function() {
            t.data.bgActivePosistion = void 0, t.hoverData.selecting || me.emit({
              originalEvent: N,
              type: "boxstart",
              position: {
                x: Le[0],
                y: Le[1]
              }
            }), dt[4] = 1, t.hoverData.selecting = !0, t.redrawHint("select", !0), t.redraw();
          };
          if (t.hoverData.which === 3) {
            if (It) {
              var Hr = {
                originalEvent: N,
                type: "cxtdrag",
                position: {
                  x: Le[0],
                  y: Le[1]
                }
              };
              Ze ? Ze.emit(Hr) : me.emit(Hr), t.hoverData.cxtDragged = !0, (!t.hoverData.cxtOver || Qe !== t.hoverData.cxtOver) && (t.hoverData.cxtOver && t.hoverData.cxtOver.emit({
                originalEvent: N,
                type: "cxtdragout",
                position: {
                  x: Le[0],
                  y: Le[1]
                }
              }), t.hoverData.cxtOver = Qe, Qe && Qe.emit({
                originalEvent: N,
                type: "cxtdragover",
                position: {
                  x: Le[0],
                  y: Le[1]
                }
              }));
            }
          } else if (t.hoverData.dragging) {
            if (De = !0, me.panningEnabled() && me.userPanningEnabled()) {
              var Ta;
              if (t.hoverData.justStartedPan) {
                var Jn = t.hoverData.mdownPos;
                Ta = {
                  x: (Le[0] - Jn[0]) * be,
                  y: (Le[1] - Jn[1]) * be
                }, t.hoverData.justStartedPan = !1;
              } else
                Ta = {
                  x: Je[0] * be,
                  y: Je[1] * be
                };
              me.panBy(Ta), me.emit("dragpan"), t.hoverData.dragged = !0;
            }
            Le = t.projectIntoViewport(N.clientX, N.clientY);
          } else if (dt[4] == 1 && (Ze == null || Ze.pannable())) {
            if (It) {
              if (!t.hoverData.dragging && me.boxSelectionEnabled() && (br || !me.panningEnabled() || !me.userPanningEnabled()))
                xa();
              else if (!t.hoverData.selecting && me.panningEnabled() && me.userPanningEnabled()) {
                var Xr = n(Ze, t.hoverData.downs);
                Xr && (t.hoverData.dragging = !0, t.hoverData.justStartedPan = !0, dt[4] = 0, t.data.bgActivePosistion = jr(ze), t.redrawHint("select", !0), t.redraw());
              }
              Ze && Ze.pannable() && Ze.active() && Ze.unactivate();
            }
          } else {
            if (Ze && Ze.pannable() && Ze.active() && Ze.unactivate(), (!Ze || !Ze.grabbed()) && Qe != ut && (ut && r(ut, ["mouseout", "tapdragout"], N, {
              x: Le[0],
              y: Le[1]
            }), Qe && r(Qe, ["mouseover", "tapdragover"], N, {
              x: Le[0],
              y: Le[1]
            }), t.hoverData.last = Qe), Ze)
              if (It) {
                if (me.boxSelectionEnabled() && br)
                  Ze && Ze.grabbed() && (g(Ct), Ze.emit("freeon"), Ct.emit("free"), t.dragData.didDrag && (Ze.emit("dragfreeon"), Ct.emit("dragfree"))), xa();
                else if (Ze && Ze.grabbed() && t.nodeIsDraggable(Ze)) {
                  var Ht = !t.dragData.didDrag;
                  Ht && t.redrawHint("eles", !0), t.dragData.didDrag = !0, t.hoverData.draggingEles || v(Ct, {
                    inDragLayer: !0
                  });
                  var Gt = {
                    x: 0,
                    y: 0
                  };
                  if (k(Je[0]) && k(Je[1]) && (Gt.x += Je[0], Gt.y += Je[1], Ht)) {
                    var Xt = t.hoverData.dragDelta;
                    Xt && k(Xt[0]) && k(Xt[1]) && (Gt.x += Xt[0], Gt.y += Xt[1]);
                  }
                  t.hoverData.draggingEles = !0, Ct.silentShift(Gt).emit("position drag"), t.redrawHint("drag", !0), t.redraw();
                }
              } else
                Ir();
            De = !0;
          }
          if (dt[2] = Le[0], dt[3] = Le[1], De)
            return N.stopPropagation && N.stopPropagation(), N.preventDefault && N.preventDefault(), !1;
        }
      }, !1);
      var C, B, F;
      t.registerBinding(window, "mouseup", function(N) {
        var le = t.hoverData.capture;
        if (le) {
          t.hoverData.capture = !1;
          var De = t.cy, me = t.projectIntoViewport(N.clientX, N.clientY), be = t.selection, Ke = t.findNearestElement(me[0], me[1], !0, !1), Le = t.dragData.possibleDragElements, ze = t.hoverData.down, at = a(N);
          if (t.data.bgActivePosistion && (t.redrawHint("select", !0), t.redraw()), t.hoverData.tapholdCancelled = !0, t.data.bgActivePosistion = void 0, ze && ze.unactivate(), t.hoverData.which === 3) {
            var dt = {
              originalEvent: N,
              type: "cxttapend",
              position: {
                x: me[0],
                y: me[1]
              }
            };
            if (ze ? ze.emit(dt) : De.emit(dt), !t.hoverData.cxtDragged) {
              var Qe = {
                originalEvent: N,
                type: "cxttap",
                position: {
                  x: me[0],
                  y: me[1]
                }
              };
              ze ? ze.emit(Qe) : De.emit(Qe);
            }
            t.hoverData.cxtDragged = !1, t.hoverData.which = null;
          } else if (t.hoverData.which === 1) {
            if (r(Ke, ["mouseup", "tapend", "vmouseup"], N, {
              x: me[0],
              y: me[1]
            }), !t.dragData.didDrag && // didn't move a node around
            !t.hoverData.dragged && // didn't pan
            !t.hoverData.selecting && // not box selection
            !t.hoverData.isOverThresholdDrag && (r(ze, ["click", "tap", "vclick"], N, {
              x: me[0],
              y: me[1]
            }), B = !1, N.timeStamp - F <= De.multiClickDebounceTime() ? (C && clearTimeout(C), B = !0, F = null, r(ze, ["dblclick", "dbltap", "vdblclick"], N, {
              x: me[0],
              y: me[1]
            })) : (C = setTimeout(function() {
              B || r(ze, ["oneclick", "onetap", "voneclick"], N, {
                x: me[0],
                y: me[1]
              });
            }, De.multiClickDebounceTime()), F = N.timeStamp)), ze == null && !t.dragData.didDrag && !t.hoverData.selecting && !t.hoverData.dragged && !a(N) && (De.$(e).unselect(["tapunselect"]), Le.length > 0 && t.redrawHint("eles", !0), t.dragData.possibleDragElements = Le = De.collection()), Ke == ze && !t.dragData.didDrag && !t.hoverData.selecting && Ke != null && Ke._private.selectable && (t.hoverData.dragging || (De.selectionType() === "additive" || at ? Ke.selected() ? Ke.unselect(["tapunselect"]) : Ke.select(["tapselect"]) : at || (De.$(e).unmerge(Ke).unselect(["tapunselect"]), Ke.select(["tapselect"]))), t.redrawHint("eles", !0)), t.hoverData.selecting) {
              var ut = De.collection(t.getAllInBox(be[0], be[1], be[2], be[3]));
              t.redrawHint("select", !0), ut.length > 0 && t.redrawHint("eles", !0), De.emit({
                type: "boxend",
                originalEvent: N,
                position: {
                  x: me[0],
                  y: me[1]
                }
              });
              var Ze = function(It) {
                return It.selectable() && !It.selected();
              };
              De.selectionType() === "additive" || at || De.$(e).unmerge(ut).unselect(), ut.emit("box").stdFilter(Ze).select().emit("boxselect"), t.redraw();
            }
            if (t.hoverData.dragging && (t.hoverData.dragging = !1, t.redrawHint("select", !0), t.redrawHint("eles", !0), t.redraw()), !be[4]) {
              t.redrawHint("drag", !0), t.redrawHint("eles", !0);
              var Je = ze && ze.grabbed();
              g(Le), Je && (ze.emit("freeon"), Le.emit("free"), t.dragData.didDrag && (ze.emit("dragfreeon"), Le.emit("dragfree")));
            }
          }
          be[4] = 0, t.hoverData.down = null, t.hoverData.cxtStarted = !1, t.hoverData.draggingEles = !1, t.hoverData.selecting = !1, t.hoverData.isOverThresholdDrag = !1, t.dragData.didDrag = !1, t.hoverData.dragged = !1, t.hoverData.dragDelta = [], t.hoverData.mdownPos = null, t.hoverData.mdownGPos = null;
        }
      }, !1);
      var R = function(N) {
        if (!t.scrollingPage) {
          var le = t.cy, De = le.zoom(), me = le.pan(), be = t.projectIntoViewport(N.clientX, N.clientY), Ke = [be[0] * De + me.x, be[1] * De + me.y];
          if (t.hoverData.draggingEles || t.hoverData.dragging || t.hoverData.cxtStarted || x()) {
            N.preventDefault();
            return;
          }
          if (le.panningEnabled() && le.userPanningEnabled() && le.zoomingEnabled() && le.userZoomingEnabled()) {
            N.preventDefault(), t.data.wheelZooming = !0, clearTimeout(t.data.wheelTimeout), t.data.wheelTimeout = setTimeout(function() {
              t.data.wheelZooming = !1, t.redrawHint("eles", !0), t.redraw();
            }, 150);
            var Le;
            N.deltaY != null ? Le = N.deltaY / -250 : N.wheelDeltaY != null ? Le = N.wheelDeltaY / 1e3 : Le = N.wheelDelta / 1e3, Le = Le * t.wheelSensitivity;
            var ze = N.deltaMode === 1;
            ze && (Le *= 33);
            var at = le.zoom() * Math.pow(10, Le);
            N.type === "gesturechange" && (at = t.gestureStartZoom * N.scale), le.zoom({
              level: at,
              renderedPosition: {
                x: Ke[0],
                y: Ke[1]
              }
            }), le.emit(N.type === "gesturechange" ? "pinchzoom" : "scrollzoom");
          }
        }
      };
      t.registerBinding(t.container, "wheel", R, !0), t.registerBinding(window, "scroll", function(N) {
        t.scrollingPage = !0, clearTimeout(t.scrollingPageTimeout), t.scrollingPageTimeout = setTimeout(function() {
          t.scrollingPage = !1;
        }, 250);
      }, !0), t.registerBinding(t.container, "gesturestart", function(N) {
        t.gestureStartZoom = t.cy.zoom(), t.hasTouchStarted || N.preventDefault();
      }, !0), t.registerBinding(t.container, "gesturechange", function(Se) {
        t.hasTouchStarted || R(Se);
      }, !0), t.registerBinding(t.container, "mouseout", function(N) {
        var le = t.projectIntoViewport(N.clientX, N.clientY);
        t.cy.emit({
          originalEvent: N,
          type: "mouseout",
          position: {
            x: le[0],
            y: le[1]
          }
        });
      }, !1), t.registerBinding(t.container, "mouseover", function(N) {
        var le = t.projectIntoViewport(N.clientX, N.clientY);
        t.cy.emit({
          originalEvent: N,
          type: "mouseover",
          position: {
            x: le[0],
            y: le[1]
          }
        });
      }, !1);
      var X, z, re, W, Z, ie, oe, ge, se, de, we, Te, Ee, ye = function(N, le, De, me) {
        return Math.sqrt((De - N) * (De - N) + (me - le) * (me - le));
      }, ae = function(N, le, De, me) {
        return (De - N) * (De - N) + (me - le) * (me - le);
      }, xe;
      t.registerBinding(t.container, "touchstart", xe = function(N) {
        if (t.hasTouchStarted = !0, !!I(N)) {
          p(), t.touchData.capture = !0, t.data.bgActivePosistion = void 0;
          var le = t.cy, De = t.touchData.now, me = t.touchData.earlier;
          if (N.touches[0]) {
            var be = t.projectIntoViewport(N.touches[0].clientX, N.touches[0].clientY);
            De[0] = be[0], De[1] = be[1];
          }
          if (N.touches[1]) {
            var be = t.projectIntoViewport(N.touches[1].clientX, N.touches[1].clientY);
            De[2] = be[0], De[3] = be[1];
          }
          if (N.touches[2]) {
            var be = t.projectIntoViewport(N.touches[2].clientX, N.touches[2].clientY);
            De[4] = be[0], De[5] = be[1];
          }
          if (N.touches[1]) {
            t.touchData.singleTouchMoved = !0, g(t.dragData.touchDragEles);
            var Ke = t.findContainerClientCoords();
            se = Ke[0], de = Ke[1], we = Ke[2], Te = Ke[3], X = N.touches[0].clientX - se, z = N.touches[0].clientY - de, re = N.touches[1].clientX - se, W = N.touches[1].clientY - de, Ee = 0 <= X && X <= we && 0 <= re && re <= we && 0 <= z && z <= Te && 0 <= W && W <= Te;
            var Le = le.pan(), ze = le.zoom();
            Z = ye(X, z, re, W), ie = ae(X, z, re, W), oe = [(X + re) / 2, (z + W) / 2], ge = [(oe[0] - Le.x) / ze, (oe[1] - Le.y) / ze];
            var at = 200, dt = at * at;
            if (ie < dt && !N.touches[2]) {
              var Qe = t.findNearestElement(De[0], De[1], !0, !0), ut = t.findNearestElement(De[2], De[3], !0, !0);
              Qe && Qe.isNode() ? (Qe.activate().emit({
                originalEvent: N,
                type: "cxttapstart",
                position: {
                  x: De[0],
                  y: De[1]
                }
              }), t.touchData.start = Qe) : ut && ut.isNode() ? (ut.activate().emit({
                originalEvent: N,
                type: "cxttapstart",
                position: {
                  x: De[0],
                  y: De[1]
                }
              }), t.touchData.start = ut) : le.emit({
                originalEvent: N,
                type: "cxttapstart",
                position: {
                  x: De[0],
                  y: De[1]
                }
              }), t.touchData.start && (t.touchData.start._private.grabbed = !1), t.touchData.cxt = !0, t.touchData.cxtDragged = !1, t.data.bgActivePosistion = void 0, t.redraw();
              return;
            }
          }
          if (N.touches[2])
            le.boxSelectionEnabled() && N.preventDefault();
          else if (!N.touches[1]) {
            if (N.touches[0]) {
              var Ze = t.findNearestElements(De[0], De[1], !0, !0), Je = Ze[0];
              if (Je != null && (Je.activate(), t.touchData.start = Je, t.touchData.starts = Ze, t.nodeIsGrabbable(Je))) {
                var Ct = t.dragData.touchDragEles = le.collection(), It = null;
                t.redrawHint("eles", !0), t.redrawHint("drag", !0), Je.selected() ? (It = le.$(function(_t) {
                  return _t.selected() && t.nodeIsGrabbable(_t);
                }), v(It, {
                  addToList: Ct
                })) : d(Je, {
                  addToList: Ct
                }), u(Je);
                var ar = function(br) {
                  return {
                    originalEvent: N,
                    type: br,
                    position: {
                      x: De[0],
                      y: De[1]
                    }
                  };
                };
                Je.emit(ar("grabon")), It ? It.forEach(function(_t) {
                  _t.emit(ar("grab"));
                }) : Je.emit(ar("grab"));
              }
              r(Je, ["touchstart", "tapstart", "vmousedown"], N, {
                x: De[0],
                y: De[1]
              }), Je == null && (t.data.bgActivePosistion = {
                x: be[0],
                y: be[1]
              }, t.redrawHint("select", !0), t.redraw()), t.touchData.singleTouchMoved = !1, t.touchData.singleTouchStartTime = +new Date(), clearTimeout(t.touchData.tapholdTimeout), t.touchData.tapholdTimeout = setTimeout(function() {
                t.touchData.singleTouchMoved === !1 && !t.pinching && !t.touchData.selecting && r(t.touchData.start, ["taphold"], N, {
                  x: De[0],
                  y: De[1]
                });
              }, t.tapholdDuration);
            }
          }
          if (N.touches.length >= 1) {
            for (var nr = t.touchData.startPosition = [], Rt = 0; Rt < De.length; Rt++)
              nr[Rt] = me[Rt] = De[Rt];
            var Qt = N.touches[0];
            t.touchData.startGPosition = [Qt.clientX, Qt.clientY];
          }
        }
      }, !1);
      var Ce;
      t.registerBinding(window, "touchmove", Ce = function(N) {
        var le = t.touchData.capture;
        if (!(!le && !I(N))) {
          var De = t.selection, me = t.cy, be = t.touchData.now, Ke = t.touchData.earlier, Le = me.zoom();
          if (N.touches[0]) {
            var ze = t.projectIntoViewport(N.touches[0].clientX, N.touches[0].clientY);
            be[0] = ze[0], be[1] = ze[1];
          }
          if (N.touches[1]) {
            var ze = t.projectIntoViewport(N.touches[1].clientX, N.touches[1].clientY);
            be[2] = ze[0], be[3] = ze[1];
          }
          if (N.touches[2]) {
            var ze = t.projectIntoViewport(N.touches[2].clientX, N.touches[2].clientY);
            be[4] = ze[0], be[5] = ze[1];
          }
          var at = t.touchData.startGPosition, dt;
          if (le && N.touches[0] && at) {
            for (var Qe = [], ut = 0; ut < be.length; ut++)
              Qe[ut] = be[ut] - Ke[ut];
            var Ze = N.touches[0].clientX - at[0], Je = Ze * Ze, Ct = N.touches[0].clientY - at[1], It = Ct * Ct, ar = Je + It;
            dt = ar >= t.touchTapThreshold2;
          }
          if (le && t.touchData.cxt) {
            N.preventDefault();
            var nr = N.touches[0].clientX - se, Rt = N.touches[0].clientY - de, Qt = N.touches[1].clientX - se, _t = N.touches[1].clientY - de, br = ae(nr, Rt, Qt, _t), Ir = br / ie, xa = 150, Hr = xa * xa, Ta = 1.5, Jn = Ta * Ta;
            if (Ir >= Jn || br >= Hr) {
              t.touchData.cxt = !1, t.data.bgActivePosistion = void 0, t.redrawHint("select", !0);
              var Xr = {
                originalEvent: N,
                type: "cxttapend",
                position: {
                  x: be[0],
                  y: be[1]
                }
              };
              t.touchData.start ? (t.touchData.start.unactivate().emit(Xr), t.touchData.start = null) : me.emit(Xr);
            }
          }
          if (le && t.touchData.cxt) {
            var Xr = {
              originalEvent: N,
              type: "cxtdrag",
              position: {
                x: be[0],
                y: be[1]
              }
            };
            t.data.bgActivePosistion = void 0, t.redrawHint("select", !0), t.touchData.start ? t.touchData.start.emit(Xr) : me.emit(Xr), t.touchData.start && (t.touchData.start._private.grabbed = !1), t.touchData.cxtDragged = !0;
            var Ht = t.findNearestElement(be[0], be[1], !0, !0);
            (!t.touchData.cxtOver || Ht !== t.touchData.cxtOver) && (t.touchData.cxtOver && t.touchData.cxtOver.emit({
              originalEvent: N,
              type: "cxtdragout",
              position: {
                x: be[0],
                y: be[1]
              }
            }), t.touchData.cxtOver = Ht, Ht && Ht.emit({
              originalEvent: N,
              type: "cxtdragover",
              position: {
                x: be[0],
                y: be[1]
              }
            }));
          } else if (le && N.touches[2] && me.boxSelectionEnabled())
            N.preventDefault(), t.data.bgActivePosistion = void 0, this.lastThreeTouch = +new Date(), t.touchData.selecting || me.emit({
              originalEvent: N,
              type: "boxstart",
              position: {
                x: be[0],
                y: be[1]
              }
            }), t.touchData.selecting = !0, t.touchData.didSelect = !0, De[4] = 1, !De || De.length === 0 || De[0] === void 0 ? (De[0] = (be[0] + be[2] + be[4]) / 3, De[1] = (be[1] + be[3] + be[5]) / 3, De[2] = (be[0] + be[2] + be[4]) / 3 + 1, De[3] = (be[1] + be[3] + be[5]) / 3 + 1) : (De[2] = (be[0] + be[2] + be[4]) / 3, De[3] = (be[1] + be[3] + be[5]) / 3), t.redrawHint("select", !0), t.redraw();
          else if (le && N.touches[1] && !t.touchData.didSelect && me.zoomingEnabled() && me.panningEnabled() && me.userZoomingEnabled() && me.userPanningEnabled()) {
            N.preventDefault(), t.data.bgActivePosistion = void 0, t.redrawHint("select", !0);
            var Gt = t.dragData.touchDragEles;
            if (Gt) {
              t.redrawHint("drag", !0);
              for (var Xt = 0; Xt < Gt.length; Xt++) {
                var jn = Gt[Xt]._private;
                jn.grabbed = !1, jn.rscratch.inDragLayer = !1;
              }
            }
            var cr = t.touchData.start, nr = N.touches[0].clientX - se, Rt = N.touches[0].clientY - de, Qt = N.touches[1].clientX - se, _t = N.touches[1].clientY - de, Fu = ye(nr, Rt, Qt, _t), up = Fu / Z;
            if (Ee) {
              var lp = nr - X, fp = Rt - z, hp = Qt - re, cp = _t - W, vp = (lp + hp) / 2, dp = (fp + cp) / 2, rn = me.zoom(), qi = rn * up, ei = me.pan(), zu = ge[0] * rn + ei.x, Gu = ge[1] * rn + ei.y, gp = {
                x: -qi / rn * (zu - ei.x - vp) + zu,
                y: -qi / rn * (Gu - ei.y - dp) + Gu
              };
              if (cr && cr.active()) {
                var Gt = t.dragData.touchDragEles;
                g(Gt), t.redrawHint("drag", !0), t.redrawHint("eles", !0), cr.unactivate().emit("freeon"), Gt.emit("free"), t.dragData.didDrag && (cr.emit("dragfreeon"), Gt.emit("dragfree"));
              }
              me.viewport({
                zoom: qi,
                pan: gp,
                cancelOnFailedZoom: !0
              }), me.emit("pinchzoom"), Z = Fu, X = nr, z = Rt, re = Qt, W = _t, t.pinching = !0;
            }
            if (N.touches[0]) {
              var ze = t.projectIntoViewport(N.touches[0].clientX, N.touches[0].clientY);
              be[0] = ze[0], be[1] = ze[1];
            }
            if (N.touches[1]) {
              var ze = t.projectIntoViewport(N.touches[1].clientX, N.touches[1].clientY);
              be[2] = ze[0], be[3] = ze[1];
            }
            if (N.touches[2]) {
              var ze = t.projectIntoViewport(N.touches[2].clientX, N.touches[2].clientY);
              be[4] = ze[0], be[5] = ze[1];
            }
          } else if (N.touches[0] && !t.touchData.didSelect) {
            var ir = t.touchData.start, Wi = t.touchData.last, Ht;
            if (!t.hoverData.draggingEles && !t.swipePanning && (Ht = t.findNearestElement(be[0], be[1], !0, !0)), le && ir != null && N.preventDefault(), le && ir != null && t.nodeIsDraggable(ir))
              if (dt) {
                var Gt = t.dragData.touchDragEles, $u = !t.dragData.didDrag;
                $u && v(Gt, {
                  inDragLayer: !0
                }), t.dragData.didDrag = !0;
                var an = {
                  x: 0,
                  y: 0
                };
                if (k(Qe[0]) && k(Qe[1]) && (an.x += Qe[0], an.y += Qe[1], $u)) {
                  t.redrawHint("eles", !0);
                  var sr = t.touchData.dragDelta;
                  sr && k(sr[0]) && k(sr[1]) && (an.x += sr[0], an.y += sr[1]);
                }
                t.hoverData.draggingEles = !0, Gt.silentShift(an).emit("position drag"), t.redrawHint("drag", !0), t.touchData.startPosition[0] == Ke[0] && t.touchData.startPosition[1] == Ke[1] && t.redrawHint("eles", !0), t.redraw();
              } else {
                var sr = t.touchData.dragDelta = t.touchData.dragDelta || [];
                sr.length === 0 ? (sr.push(Qe[0]), sr.push(Qe[1])) : (sr[0] += Qe[0], sr[1] += Qe[1]);
              }
            if (r(ir || Ht, ["touchmove", "tapdrag", "vmousemove"], N, {
              x: be[0],
              y: be[1]
            }), (!ir || !ir.grabbed()) && Ht != Wi && (Wi && Wi.emit({
              originalEvent: N,
              type: "tapdragout",
              position: {
                x: be[0],
                y: be[1]
              }
            }), Ht && Ht.emit({
              originalEvent: N,
              type: "tapdragover",
              position: {
                x: be[0],
                y: be[1]
              }
            })), t.touchData.last = Ht, le)
              for (var Xt = 0; Xt < be.length; Xt++)
                be[Xt] && t.touchData.startPosition[Xt] && dt && (t.touchData.singleTouchMoved = !0);
            if (le && (ir == null || ir.pannable()) && me.panningEnabled() && me.userPanningEnabled()) {
              var pp = n(ir, t.touchData.starts);
              pp && (N.preventDefault(), t.data.bgActivePosistion || (t.data.bgActivePosistion = jr(t.touchData.startPosition)), t.swipePanning ? (me.panBy({
                x: Qe[0] * Le,
                y: Qe[1] * Le
              }), me.emit("dragpan")) : dt && (t.swipePanning = !0, me.panBy({
                x: Ze * Le,
                y: Ct * Le
              }), me.emit("dragpan"), ir && (ir.unactivate(), t.redrawHint("select", !0), t.touchData.start = null)));
              var ze = t.projectIntoViewport(N.touches[0].clientX, N.touches[0].clientY);
              be[0] = ze[0], be[1] = ze[1];
            }
          }
          for (var ut = 0; ut < be.length; ut++)
            Ke[ut] = be[ut];
          le && N.touches.length > 0 && !t.hoverData.draggingEles && !t.swipePanning && t.data.bgActivePosistion != null && (t.data.bgActivePosistion = void 0, t.redrawHint("select", !0), t.redraw());
        }
      }, !1);
      var Oe;
      t.registerBinding(window, "touchcancel", Oe = function(N) {
        var le = t.touchData.start;
        t.touchData.capture = !1, le && le.unactivate();
      });
      var Ie, He, qe, Re;
      if (t.registerBinding(window, "touchend", Ie = function(N) {
        var le = t.touchData.start, De = t.touchData.capture;
        if (De)
          N.touches.length === 0 && (t.touchData.capture = !1), N.preventDefault();
        else
          return;
        var me = t.selection;
        t.swipePanning = !1, t.hoverData.draggingEles = !1;
        var be = t.cy, Ke = be.zoom(), Le = t.touchData.now, ze = t.touchData.earlier;
        if (N.touches[0]) {
          var at = t.projectIntoViewport(N.touches[0].clientX, N.touches[0].clientY);
          Le[0] = at[0], Le[1] = at[1];
        }
        if (N.touches[1]) {
          var at = t.projectIntoViewport(N.touches[1].clientX, N.touches[1].clientY);
          Le[2] = at[0], Le[3] = at[1];
        }
        if (N.touches[2]) {
          var at = t.projectIntoViewport(N.touches[2].clientX, N.touches[2].clientY);
          Le[4] = at[0], Le[5] = at[1];
        }
        le && le.unactivate();
        var dt;
        if (t.touchData.cxt) {
          if (dt = {
            originalEvent: N,
            type: "cxttapend",
            position: {
              x: Le[0],
              y: Le[1]
            }
          }, le ? le.emit(dt) : be.emit(dt), !t.touchData.cxtDragged) {
            var Qe = {
              originalEvent: N,
              type: "cxttap",
              position: {
                x: Le[0],
                y: Le[1]
              }
            };
            le ? le.emit(Qe) : be.emit(Qe);
          }
          t.touchData.start && (t.touchData.start._private.grabbed = !1), t.touchData.cxt = !1, t.touchData.start = null, t.redraw();
          return;
        }
        if (!N.touches[2] && be.boxSelectionEnabled() && t.touchData.selecting) {
          t.touchData.selecting = !1;
          var ut = be.collection(t.getAllInBox(me[0], me[1], me[2], me[3]));
          me[0] = void 0, me[1] = void 0, me[2] = void 0, me[3] = void 0, me[4] = 0, t.redrawHint("select", !0), be.emit({
            type: "boxend",
            originalEvent: N,
            position: {
              x: Le[0],
              y: Le[1]
            }
          });
          var Ze = function(Hr) {
            return Hr.selectable() && !Hr.selected();
          };
          ut.emit("box").stdFilter(Ze).select().emit("boxselect"), ut.nonempty() && t.redrawHint("eles", !0), t.redraw();
        }
        if (le != null && le.unactivate(), N.touches[2])
          t.data.bgActivePosistion = void 0, t.redrawHint("select", !0);
        else if (!N.touches[1]) {
          if (!N.touches[0]) {
            if (!N.touches[0]) {
              t.data.bgActivePosistion = void 0, t.redrawHint("select", !0);
              var Je = t.dragData.touchDragEles;
              if (le != null) {
                var Ct = le._private.grabbed;
                g(Je), t.redrawHint("drag", !0), t.redrawHint("eles", !0), Ct && (le.emit("freeon"), Je.emit("free"), t.dragData.didDrag && (le.emit("dragfreeon"), Je.emit("dragfree"))), r(le, ["touchend", "tapend", "vmouseup", "tapdragout"], N, {
                  x: Le[0],
                  y: Le[1]
                }), le.unactivate(), t.touchData.start = null;
              } else {
                var It = t.findNearestElement(Le[0], Le[1], !0, !0);
                r(It, ["touchend", "tapend", "vmouseup", "tapdragout"], N, {
                  x: Le[0],
                  y: Le[1]
                });
              }
              var ar = t.touchData.startPosition[0] - Le[0], nr = ar * ar, Rt = t.touchData.startPosition[1] - Le[1], Qt = Rt * Rt, _t = nr + Qt, br = _t * Ke * Ke;
              t.touchData.singleTouchMoved || (le || be.$(":selected").unselect(["tapunselect"]), r(le, ["tap", "vclick"], N, {
                x: Le[0],
                y: Le[1]
              }), He = !1, N.timeStamp - Re <= be.multiClickDebounceTime() ? (qe && clearTimeout(qe), He = !0, Re = null, r(le, ["dbltap", "vdblclick"], N, {
                x: Le[0],
                y: Le[1]
              })) : (qe = setTimeout(function() {
                He || r(le, ["onetap", "voneclick"], N, {
                  x: Le[0],
                  y: Le[1]
                });
              }, be.multiClickDebounceTime()), Re = N.timeStamp)), le != null && !t.dragData.didDrag && le._private.selectable && br < t.touchTapThreshold2 && !t.pinching && (be.selectionType() === "single" ? (be.$(e).unmerge(le).unselect(["tapunselect"]), le.select(["tapselect"])) : le.selected() ? le.unselect(["tapunselect"]) : le.select(["tapselect"]), t.redrawHint("eles", !0)), t.touchData.singleTouchMoved = !0;
            }
          }
        }
        for (var Ir = 0; Ir < Le.length; Ir++)
          ze[Ir] = Le[Ir];
        t.dragData.didDrag = !1, N.touches.length === 0 && (t.touchData.dragDelta = [], t.touchData.startPosition = null, t.touchData.startGPosition = null, t.touchData.didSelect = !1), N.touches.length < 2 && (N.touches.length === 1 && (t.touchData.startGPosition = [N.touches[0].clientX, N.touches[0].clientY]), t.pinching = !1, t.redrawHint("eles", !0), t.redraw());
      }, !1), typeof TouchEvent > "u") {
        var Me = [], Ve = function(N) {
          return {
            clientX: N.clientX,
            clientY: N.clientY,
            force: 1,
            identifier: N.pointerId,
            pageX: N.pageX,
            pageY: N.pageY,
            radiusX: N.width / 2,
            radiusY: N.height / 2,
            screenX: N.screenX,
            screenY: N.screenY,
            target: N.target
          };
        }, Fe = function(N) {
          return {
            event: N,
            touch: Ve(N)
          };
        }, ke = function(N) {
          Me.push(Fe(N));
        }, Ge = function(N) {
          for (var le = 0; le < Me.length; le++) {
            var De = Me[le];
            if (De.event.pointerId === N.pointerId) {
              Me.splice(le, 1);
              return;
            }
          }
        }, et = function(N) {
          var le = Me.filter(function(De) {
            return De.event.pointerId === N.pointerId;
          })[0];
          le.event = N, le.touch = Ve(N);
        }, We = function(N) {
          N.touches = Me.map(function(le) {
            return le.touch;
          });
        }, Ye = function(N) {
          return N.pointerType === "mouse" || N.pointerType === 4;
        };
        t.registerBinding(t.container, "pointerdown", function(Se) {
          Ye(Se) || (Se.preventDefault(), ke(Se), We(Se), xe(Se));
        }), t.registerBinding(t.container, "pointerup", function(Se) {
          Ye(Se) || (Ge(Se), We(Se), Ie(Se));
        }), t.registerBinding(t.container, "pointercancel", function(Se) {
          Ye(Se) || (Ge(Se), We(Se), Oe(Se));
        }), t.registerBinding(t.container, "pointermove", function(Se) {
          Ye(Se) || (Se.preventDefault(), et(Se), We(Se), Ce(Se));
        });
      }
    };
    var yr = {};
    yr.generatePolygon = function(t, e) {
      return this.nodeShapes[t] = {
        renderer: this,
        name: t,
        points: e,
        draw: function(a, n, i, s, o) {
          this.renderer.nodeShapeImpl("polygon", a, n, i, s, o, this.points);
        },
        intersectLine: function(a, n, i, s, o, l, u) {
          return Ba(o, l, this.points, a, n, i / 2, s / 2, u);
        },
        checkPoint: function(a, n, i, s, o, l, u) {
          return gr(a, n, this.points, l, u, s, o, [0, -1], i);
        }
      };
    }, yr.generateEllipse = function() {
      return this.nodeShapes.ellipse = {
        renderer: this,
        name: "ellipse",
        draw: function(e, r, a, n, i) {
          this.renderer.nodeShapeImpl(this.name, e, r, a, n, i);
        },
        intersectLine: function(e, r, a, n, i, s, o) {
          return Pf(i, s, e, r, a / 2 + o, n / 2 + o);
        },
        checkPoint: function(e, r, a, n, i, s, o) {
          return Fr(e, r, n, i, s, o, a);
        }
      };
    }, yr.generateRoundPolygon = function(t, e) {
      for (var r = new Array(e.length * 2), a = 0; a < e.length / 2; a++) {
        var n = a * 2, i = void 0;
        a < e.length / 2 - 1 ? i = (a + 1) * 2 : i = 0, r[a * 4] = e[n], r[a * 4 + 1] = e[n + 1];
        var s = e[i] - e[n], o = e[i + 1] - e[n + 1], l = Math.sqrt(s * s + o * o);
        r[a * 4 + 2] = s / l, r[a * 4 + 3] = o / l;
      }
      return this.nodeShapes[t] = {
        renderer: this,
        name: t,
        points: r,
        draw: function(f, h, c, v, d) {
          this.renderer.nodeShapeImpl("round-polygon", f, h, c, v, d, this.points);
        },
        intersectLine: function(f, h, c, v, d, g, y) {
          return Bf(d, g, this.points, f, h, c, v);
        },
        checkPoint: function(f, h, c, v, d, g, y) {
          return kf(f, h, this.points, g, y, v, d);
        }
      };
    }, yr.generateRoundRectangle = function() {
      return this.nodeShapes["round-rectangle"] = this.nodeShapes.roundrectangle = {
        renderer: this,
        name: "round-rectangle",
        points: $t(4, 0),
        draw: function(e, r, a, n, i) {
          this.renderer.nodeShapeImpl(this.name, e, r, a, n, i);
        },
        intersectLine: function(e, r, a, n, i, s, o) {
          return Ts(i, s, e, r, a, n, o);
        },
        checkPoint: function(e, r, a, n, i, s, o) {
          var l = Fa(n, i), u = l * 2;
          return !!(gr(e, r, this.points, s, o, n, i - u, [0, -1], a) || gr(e, r, this.points, s, o, n - u, i, [0, -1], a) || Fr(e, r, u, u, s - n / 2 + l, o - i / 2 + l, a) || Fr(e, r, u, u, s + n / 2 - l, o - i / 2 + l, a) || Fr(e, r, u, u, s + n / 2 - l, o + i / 2 - l, a) || Fr(e, r, u, u, s - n / 2 + l, o + i / 2 - l, a));
        }
      };
    }, yr.generateCutRectangle = function() {
      return this.nodeShapes["cut-rectangle"] = this.nodeShapes.cutrectangle = {
        renderer: this,
        name: "cut-rectangle",
        cornerLength: Ls(),
        points: $t(4, 0),
        draw: function(e, r, a, n, i) {
          this.renderer.nodeShapeImpl(this.name, e, r, a, n, i);
        },
        generateCutTrianglePts: function(e, r, a, n) {
          var i = this.cornerLength, s = r / 2, o = e / 2, l = a - o, u = a + o, f = n - s, h = n + s;
          return {
            topLeft: [l, f + i, l + i, f, l + i, f + i],
            topRight: [u - i, f, u, f + i, u - i, f + i],
            bottomRight: [u, h - i, u - i, h, u - i, h - i],
            bottomLeft: [l + i, h, l, h - i, l + i, h - i]
          };
        },
        intersectLine: function(e, r, a, n, i, s, o) {
          var l = this.generateCutTrianglePts(a + 2 * o, n + 2 * o, e, r), u = [].concat.apply([], [l.topLeft.splice(0, 4), l.topRight.splice(0, 4), l.bottomRight.splice(0, 4), l.bottomLeft.splice(0, 4)]);
          return Ba(i, s, u, e, r);
        },
        checkPoint: function(e, r, a, n, i, s, o) {
          if (gr(e, r, this.points, s, o, n, i - 2 * this.cornerLength, [0, -1], a) || gr(e, r, this.points, s, o, n - 2 * this.cornerLength, i, [0, -1], a))
            return !0;
          var l = this.generateCutTrianglePts(n, i, s, o);
          return Yt(e, r, l.topLeft) || Yt(e, r, l.topRight) || Yt(e, r, l.bottomRight) || Yt(e, r, l.bottomLeft);
        }
      };
    }, yr.generateBarrel = function() {
      return this.nodeShapes.barrel = {
        renderer: this,
        name: "barrel",
        points: $t(4, 0),
        draw: function(e, r, a, n, i) {
          this.renderer.nodeShapeImpl(this.name, e, r, a, n, i);
        },
        intersectLine: function(e, r, a, n, i, s, o) {
          var l = 0.15, u = 0.5, f = 0.85, h = this.generateBarrelBezierPts(a + 2 * o, n + 2 * o, e, r), c = function(g) {
            var y = ea({
              x: g[0],
              y: g[1]
            }, {
              x: g[2],
              y: g[3]
            }, {
              x: g[4],
              y: g[5]
            }, l), p = ea({
              x: g[0],
              y: g[1]
            }, {
              x: g[2],
              y: g[3]
            }, {
              x: g[4],
              y: g[5]
            }, u), m = ea({
              x: g[0],
              y: g[1]
            }, {
              x: g[2],
              y: g[3]
            }, {
              x: g[4],
              y: g[5]
            }, f);
            return [g[0], g[1], y.x, y.y, p.x, p.y, m.x, m.y, g[4], g[5]];
          }, v = [].concat(c(h.topLeft), c(h.topRight), c(h.bottomRight), c(h.bottomLeft));
          return Ba(i, s, v, e, r);
        },
        generateBarrelBezierPts: function(e, r, a, n) {
          var i = r / 2, s = e / 2, o = a - s, l = a + s, u = n - i, f = n + i, h = gi(e, r), c = h.heightOffset, v = h.widthOffset, d = h.ctrlPtOffsetPct * e, g = {
            topLeft: [o, u + c, o + d, u, o + v, u],
            topRight: [l - v, u, l - d, u, l, u + c],
            bottomRight: [l, f - c, l - d, f, l - v, f],
            bottomLeft: [o + v, f, o + d, f, o, f - c]
          };
          return g.topLeft.isTop = !0, g.topRight.isTop = !0, g.bottomLeft.isBottom = !0, g.bottomRight.isBottom = !0, g;
        },
        checkPoint: function(e, r, a, n, i, s, o) {
          var l = gi(n, i), u = l.heightOffset, f = l.widthOffset;
          if (gr(e, r, this.points, s, o, n, i - 2 * u, [0, -1], a) || gr(e, r, this.points, s, o, n - 2 * f, i, [0, -1], a))
            return !0;
          for (var h = this.generateBarrelBezierPts(n, i, s, o), c = function(x, I, C) {
            var B = C[4], F = C[2], R = C[0], X = C[5], z = C[1], re = Math.min(B, R), W = Math.max(B, R), Z = Math.min(X, z), ie = Math.max(X, z);
            if (re <= x && x <= W && Z <= I && I <= ie) {
              var oe = Ff(B, F, R), ge = Nf(oe[0], oe[1], oe[2], x), se = ge.filter(function(de) {
                return 0 <= de && de <= 1;
              });
              if (se.length > 0)
                return se[0];
            }
            return null;
          }, v = Object.keys(h), d = 0; d < v.length; d++) {
            var g = v[d], y = h[g], p = c(e, r, y);
            if (p != null) {
              var m = y[5], b = y[3], E = y[1], M = St(m, b, E, p);
              if (y.isTop && M <= r || y.isBottom && r <= M)
                return !0;
            }
          }
          return !1;
        }
      };
    }, yr.generateBottomRoundrectangle = function() {
      return this.nodeShapes["bottom-round-rectangle"] = this.nodeShapes.bottomroundrectangle = {
        renderer: this,
        name: "bottom-round-rectangle",
        points: $t(4, 0),
        draw: function(e, r, a, n, i) {
          this.renderer.nodeShapeImpl(this.name, e, r, a, n, i);
        },
        intersectLine: function(e, r, a, n, i, s, o) {
          var l = e - (a / 2 + o), u = r - (n / 2 + o), f = u, h = e + (a / 2 + o), c = Tr(i, s, e, r, l, u, h, f, !1);
          return c.length > 0 ? c : Ts(i, s, e, r, a, n, o);
        },
        checkPoint: function(e, r, a, n, i, s, o) {
          var l = Fa(n, i), u = 2 * l;
          if (gr(e, r, this.points, s, o, n, i - u, [0, -1], a) || gr(e, r, this.points, s, o, n - u, i, [0, -1], a))
            return !0;
          var f = n / 2 + 2 * a, h = i / 2 + 2 * a, c = [s - f, o - h, s - f, o, s + f, o, s + f, o - h];
          return !!(Yt(e, r, c) || Fr(e, r, u, u, s + n / 2 - l, o + i / 2 - l, a) || Fr(e, r, u, u, s - n / 2 + l, o + i / 2 - l, a));
        }
      };
    }, yr.registerNodeShapes = function() {
      var t = this.nodeShapes = {}, e = this;
      this.generateEllipse(), this.generatePolygon("triangle", $t(3, 0)), this.generateRoundPolygon("round-triangle", $t(3, 0)), this.generatePolygon("rectangle", $t(4, 0)), t.square = t.rectangle, this.generateRoundRectangle(), this.generateCutRectangle(), this.generateBarrel(), this.generateBottomRoundrectangle();
      {
        var r = [0, 1, 1, 0, 0, -1, -1, 0];
        this.generatePolygon("diamond", r), this.generateRoundPolygon("round-diamond", r);
      }
      this.generatePolygon("pentagon", $t(5, 0)), this.generateRoundPolygon("round-pentagon", $t(5, 0)), this.generatePolygon("hexagon", $t(6, 0)), this.generateRoundPolygon("round-hexagon", $t(6, 0)), this.generatePolygon("heptagon", $t(7, 0)), this.generateRoundPolygon("round-heptagon", $t(7, 0)), this.generatePolygon("octagon", $t(8, 0)), this.generateRoundPolygon("round-octagon", $t(8, 0));
      var a = new Array(20);
      {
        var n = vi(5, 0), i = vi(5, Math.PI / 5), s = 0.5 * (3 - Math.sqrt(5));
        s *= 1.57;
        for (var o = 0; o < i.length / 2; o++)
          i[o * 2] *= s, i[o * 2 + 1] *= s;
        for (var o = 0; o < 20 / 4; o++)
          a[o * 4] = n[o * 2], a[o * 4 + 1] = n[o * 2 + 1], a[o * 4 + 2] = i[o * 2], a[o * 4 + 3] = i[o * 2 + 1];
      }
      a = Ss(a), this.generatePolygon("star", a), this.generatePolygon("vee", [-1, -1, 0, -0.333, 1, -1, 0, 1]), this.generatePolygon("rhomboid", [-1, -1, 0.333, -1, 1, 1, -0.333, 1]), this.nodeShapes.concavehexagon = this.generatePolygon("concave-hexagon", [-1, -0.95, -0.75, 0, -1, 0.95, 1, 0.95, 0.75, 0, 1, -0.95]);
      {
        var l = [-1, -1, 0.25, -1, 1, 0, 0.25, 1, -1, 1];
        this.generatePolygon("tag", l), this.generateRoundPolygon("round-tag", l);
      }
      t.makePolygon = function(u) {
        var f = u.join("$"), h = "polygon-" + f, c;
        return (c = this[h]) ? c : e.generatePolygon(h, u);
      };
    };
    var Ja = {};
    Ja.timeToRender = function() {
      return this.redrawTotalTime / this.redrawCount;
    }, Ja.redraw = function(t) {
      t = t || ys();
      var e = this;
      e.averageRedrawTime === void 0 && (e.averageRedrawTime = 0), e.lastRedrawTime === void 0 && (e.lastRedrawTime = 0), e.lastDrawTime === void 0 && (e.lastDrawTime = 0), e.requestedFrame = !0, e.renderOptions = t;
    }, Ja.beforeRender = function(t, e) {
      if (!this.destroyed) {
        e == null && xt("Priority is not optional for beforeRender");
        var r = this.beforeRenderCallbacks;
        r.push({
          fn: t,
          priority: e
        }), r.sort(function(a, n) {
          return n.priority - a.priority;
        });
      }
    };
    var vu = function(e, r, a) {
      for (var n = e.beforeRenderCallbacks, i = 0; i < n.length; i++)
        n[i].fn(r, a);
    };
    Ja.startRenderLoop = function() {
      var t = this, e = t.cy;
      if (!t.renderLoopStarted) {
        t.renderLoopStarted = !0;
        var r = function a(n) {
          if (!t.destroyed) {
            if (!e.batching())
              if (t.requestedFrame && !t.skipFrame) {
                vu(t, !0, n);
                var i = dr();
                t.render(t.renderOptions);
                var s = t.lastDrawTime = dr();
                t.averageRedrawTime === void 0 && (t.averageRedrawTime = s - i), t.redrawCount === void 0 && (t.redrawCount = 0), t.redrawCount++, t.redrawTotalTime === void 0 && (t.redrawTotalTime = 0);
                var o = s - i;
                t.redrawTotalTime += o, t.lastRedrawTime = o, t.averageRedrawTime = t.averageRedrawTime / 2 + o / 2, t.requestedFrame = !1;
              } else
                vu(t, !1, n);
            t.skipFrame = !1, hn(a);
          }
        };
        hn(r);
      }
    };
    var dg = function(e) {
      this.init(e);
    }, du = dg, ma = du.prototype;
    ma.clientFunctions = ["redrawHint", "render", "renderTo", "matchCanvasSize", "nodeShapeImpl", "arrowShapeImpl"], ma.init = function(t) {
      var e = this;
      e.options = t, e.cy = t.cy;
      var r = e.container = t.cy.container();
      if (D) {
        var a = D.document, n = a.head, i = "__________cytoscape_stylesheet", s = "__________cytoscape_container", o = a.getElementById(i) != null;
        if (r.className.indexOf(s) < 0 && (r.className = (r.className || "") + " " + s), !o) {
          var l = a.createElement("style");
          l.id = i, l.innerHTML = "." + s + " { position: relative; }", n.insertBefore(l, n.children[0]);
        }
        var u = D.getComputedStyle(r), f = u.getPropertyValue("position");
        f === "static" && ft("A Cytoscape container has style position:static and so can not use UI extensions properly");
      }
      e.selection = [void 0, void 0, void 0, void 0, 0], e.bezierProjPcts = [0.05, 0.225, 0.4, 0.5, 0.6, 0.775, 0.95], e.hoverData = {
        down: null,
        last: null,
        downTime: null,
        triggerMode: null,
        dragging: !1,
        initialPan: [null, null],
        capture: !1
      }, e.dragData = {
        possibleDragElements: []
      }, e.touchData = {
        start: null,
        capture: !1,
        // These 3 fields related to tap, taphold events
        startPosition: [null, null, null, null, null, null],
        singleTouchStartTime: null,
        singleTouchMoved: !0,
        now: [null, null, null, null, null, null],
        earlier: [null, null, null, null, null, null]
      }, e.redraws = 0, e.showFps = t.showFps, e.debug = t.debug, e.hideEdgesOnViewport = t.hideEdgesOnViewport, e.textureOnViewport = t.textureOnViewport, e.wheelSensitivity = t.wheelSensitivity, e.motionBlurEnabled = t.motionBlur, e.forcedPixelRatio = k(t.pixelRatio) ? t.pixelRatio : null, e.motionBlur = t.motionBlur, e.motionBlurOpacity = t.motionBlurOpacity, e.motionBlurTransparency = 1 - e.motionBlurOpacity, e.motionBlurPxRatio = 1, e.mbPxRBlurry = 1, e.minMbLowQualFrames = 4, e.fullQualityMb = !1, e.clearedForMotionBlur = [], e.desktopTapThreshold = t.desktopTapThreshold, e.desktopTapThreshold2 = t.desktopTapThreshold * t.desktopTapThreshold, e.touchTapThreshold = t.touchTapThreshold, e.touchTapThreshold2 = t.touchTapThreshold * t.touchTapThreshold, e.tapholdDuration = 500, e.bindings = [], e.beforeRenderCallbacks = [], e.beforeRenderPriorities = {
        // higher priority execs before lower one
        animations: 400,
        eleCalcs: 300,
        eleTxrDeq: 200,
        lyrTxrDeq: 150,
        lyrTxrSkip: 100
      }, e.registerNodeShapes(), e.registerArrowShapes(), e.registerCalculationListeners();
    }, ma.notify = function(t, e) {
      var r = this, a = r.cy;
      if (!this.destroyed) {
        if (t === "init") {
          r.load();
          return;
        }
        if (t === "destroy") {
          r.destroy();
          return;
        }
        (t === "add" || t === "remove" || t === "move" && a.hasCompoundNodes() || t === "load" || t === "zorder" || t === "mount") && r.invalidateCachedZSortedEles(), t === "viewport" && r.redrawHint("select", !0), (t === "load" || t === "resize" || t === "mount") && (r.invalidateContainerClientCoordsCache(), r.matchCanvasSize(r.container)), r.redrawHint("eles", !0), r.redrawHint("drag", !0), this.startRenderLoop(), this.redraw();
      }
    }, ma.destroy = function() {
      var t = this;
      t.destroyed = !0, t.cy.stopAnimationLoop();
      for (var e = 0; e < t.bindings.length; e++) {
        var r = t.bindings[e], a = r, n = a.target;
        (n.off || n.removeEventListener).apply(n, a.args);
      }
      if (t.bindings = [], t.beforeRenderCallbacks = [], t.onUpdateEleCalcsFns = [], t.removeObserver && t.removeObserver.disconnect(), t.styleObserver && t.styleObserver.disconnect(), t.resizeObserver && t.resizeObserver.disconnect(), t.labelCalcDiv)
        try {
          document.body.removeChild(t.labelCalcDiv);
        } catch {
        }
    }, ma.isHeadless = function() {
      return !1;
    }, [zi, hu, cu, ya, yr, Ja].forEach(function(t) {
      Ue(ma, t);
    });
    var $i = 1e3 / 60, gu = {
      setupDequeueing: function(e) {
        return function() {
          var a = this, n = this.renderer;
          if (!a.dequeueingSetup) {
            a.dequeueingSetup = !0;
            var i = fn(function() {
              n.redrawHint("eles", !0), n.redrawHint("drag", !0), n.redraw();
            }, e.deqRedrawThreshold), s = function(u, f) {
              var h = dr(), c = n.averageRedrawTime, v = n.lastRedrawTime, d = [], g = n.cy.extent(), y = n.getPixelRatio();
              for (u || n.flushRenderedStyleQueue(); ; ) {
                var p = dr(), m = p - h, b = p - f;
                if (v < $i) {
                  var E = $i - (u ? c : 0);
                  if (b >= e.deqFastCost * E)
                    break;
                } else if (u) {
                  if (m >= e.deqCost * v || m >= e.deqAvgCost * c)
                    break;
                } else if (b >= e.deqNoDrawCost * $i)
                  break;
                var M = e.deq(a, y, g);
                if (M.length > 0)
                  for (var O = 0; O < M.length; O++)
                    d.push(M[O]);
                else
                  break;
              }
              d.length > 0 && (e.onDeqd(a, d), !u && e.shouldRedraw(a, d, y, g) && i());
            }, o = e.priority || si;
            n.beforeRender(s, o(a));
          }
        };
      }
    }, gg = /* @__PURE__ */ function() {
      function t(e) {
        var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : vn;
        ce(this, t), this.idsByKey = new ur(), this.keyForId = new ur(), this.cachesByLvl = new ur(), this.lvls = [], this.getKey = e, this.doesEleInvalidateKey = r;
      }
      return A(t, [{
        key: "getIdsFor",
        value: function(r) {
          r == null && xt("Can not get id list for null key");
          var a = this.idsByKey, n = this.idsByKey.get(r);
          return n || (n = new Jr(), a.set(r, n)), n;
        }
      }, {
        key: "addIdForKey",
        value: function(r, a) {
          r != null && this.getIdsFor(r).add(a);
        }
      }, {
        key: "deleteIdForKey",
        value: function(r, a) {
          r != null && this.getIdsFor(r).delete(a);
        }
      }, {
        key: "getNumberOfIdsForKey",
        value: function(r) {
          return r == null ? 0 : this.getIdsFor(r).size;
        }
      }, {
        key: "updateKeyMappingFor",
        value: function(r) {
          var a = r.id(), n = this.keyForId.get(a), i = this.getKey(r);
          this.deleteIdForKey(n, a), this.addIdForKey(i, a), this.keyForId.set(a, i);
        }
      }, {
        key: "deleteKeyMappingFor",
        value: function(r) {
          var a = r.id(), n = this.keyForId.get(a);
          this.deleteIdForKey(n, a), this.keyForId.delete(a);
        }
      }, {
        key: "keyHasChangedFor",
        value: function(r) {
          var a = r.id(), n = this.keyForId.get(a), i = this.getKey(r);
          return n !== i;
        }
      }, {
        key: "isInvalid",
        value: function(r) {
          return this.keyHasChangedFor(r) || this.doesEleInvalidateKey(r);
        }
      }, {
        key: "getCachesAt",
        value: function(r) {
          var a = this.cachesByLvl, n = this.lvls, i = a.get(r);
          return i || (i = new ur(), a.set(r, i), n.push(r)), i;
        }
      }, {
        key: "getCache",
        value: function(r, a) {
          return this.getCachesAt(a).get(r);
        }
      }, {
        key: "get",
        value: function(r, a) {
          var n = this.getKey(r), i = this.getCache(n, a);
          return i != null && this.updateKeyMappingFor(r), i;
        }
      }, {
        key: "getForCachedKey",
        value: function(r, a) {
          var n = this.keyForId.get(r.id()), i = this.getCache(n, a);
          return i;
        }
      }, {
        key: "hasCache",
        value: function(r, a) {
          return this.getCachesAt(a).has(r);
        }
      }, {
        key: "has",
        value: function(r, a) {
          var n = this.getKey(r);
          return this.hasCache(n, a);
        }
      }, {
        key: "setCache",
        value: function(r, a, n) {
          n.key = r, this.getCachesAt(a).set(r, n);
        }
      }, {
        key: "set",
        value: function(r, a, n) {
          var i = this.getKey(r);
          this.setCache(i, a, n), this.updateKeyMappingFor(r);
        }
      }, {
        key: "deleteCache",
        value: function(r, a) {
          this.getCachesAt(a).delete(r);
        }
      }, {
        key: "delete",
        value: function(r, a) {
          var n = this.getKey(r);
          this.deleteCache(n, a);
        }
      }, {
        key: "invalidateKey",
        value: function(r) {
          var a = this;
          this.lvls.forEach(function(n) {
            return a.deleteCache(r, n);
          });
        }
        // returns true if no other eles reference the invalidated cache (n.b. other eles may need the cache with the same key)
      }, {
        key: "invalidate",
        value: function(r) {
          var a = r.id(), n = this.keyForId.get(a);
          this.deleteKeyMappingFor(r);
          var i = this.doesEleInvalidateKey(r);
          return i && this.invalidateKey(n), i || this.getNumberOfIdsForKey(n) === 0;
        }
      }]), t;
    }(), pu = 25, Kn = 50, Zn = -4, Vi = 3, pg = 7.99, yg = 8, mg = 1024, bg = 1024, Eg = 1024, wg = 0.2, xg = 0.8, Tg = 10, Cg = 0.15, Dg = 0.1, Sg = 0.9, Lg = 0.9, Ag = 100, Og = 1, ba = {
      dequeue: "dequeue",
      downscale: "downscale",
      highQuality: "highQuality"
    }, Ng = Lt({
      getKey: null,
      doesEleInvalidateKey: vn,
      drawElement: null,
      getBoundingBox: null,
      getRotationPoint: null,
      getRotationOffset: null,
      isVisible: vs,
      allowEdgeTxrCaching: !0,
      allowParentTxrCaching: !0
    }), ja = function(e, r) {
      var a = this;
      a.renderer = e, a.onDequeues = [];
      var n = Ng(r);
      Ue(a, n), a.lookup = new gg(n.getKey, n.doesEleInvalidateKey), a.setupDequeueing();
    }, Dt = ja.prototype;
    Dt.reasons = ba, Dt.getTextureQueue = function(t) {
      var e = this;
      return e.eleImgCaches = e.eleImgCaches || {}, e.eleImgCaches[t] = e.eleImgCaches[t] || [];
    }, Dt.getRetiredTextureQueue = function(t) {
      var e = this, r = e.eleImgCaches.retired = e.eleImgCaches.retired || {}, a = r[t] = r[t] || [];
      return a;
    }, Dt.getElementQueue = function() {
      var t = this, e = t.eleCacheQueue = t.eleCacheQueue || new Ra(function(r, a) {
        return a.reqs - r.reqs;
      });
      return e;
    }, Dt.getElementKeyToQueue = function() {
      var t = this, e = t.eleKeyToCacheQueue = t.eleKeyToCacheQueue || {};
      return e;
    }, Dt.getElement = function(t, e, r, a, n) {
      var i = this, s = this.renderer, o = s.cy.zoom(), l = this.lookup;
      if (!e || e.w === 0 || e.h === 0 || isNaN(e.w) || isNaN(e.h) || !t.visible() || t.removed() || !i.allowEdgeTxrCaching && t.isEdge() || !i.allowParentTxrCaching && t.isParent())
        return null;
      if (a == null && (a = Math.ceil(li(o * r))), a < Zn)
        a = Zn;
      else if (o >= pg || a > Vi)
        return null;
      var u = Math.pow(2, a), f = e.h * u, h = e.w * u, c = s.eleTextBiggerThanMin(t, u);
      if (!this.isVisible(t, c))
        return null;
      var v = l.get(t, a);
      if (v && v.invalidated && (v.invalidated = !1, v.texture.invalidatedWidth -= v.width), v)
        return v;
      var d;
      if (f <= pu ? d = pu : f <= Kn ? d = Kn : d = Math.ceil(f / Kn) * Kn, f > Eg || h > bg)
        return null;
      var g = i.getTextureQueue(d), y = g[g.length - 2], p = function() {
        return i.recycleTexture(d, h) || i.addTexture(d, h);
      };
      y || (y = g[g.length - 1]), y || (y = p()), y.width - y.usedWidth < h && (y = p());
      for (var m = function(W) {
        return W && W.scaledLabelShown === c;
      }, b = n && n === ba.dequeue, E = n && n === ba.highQuality, M = n && n === ba.downscale, O, x = a + 1; x <= Vi; x++) {
        var I = l.get(t, x);
        if (I) {
          O = I;
          break;
        }
      }
      var C = O && O.level === a + 1 ? O : null, B = function() {
        y.context.drawImage(C.texture.canvas, C.x, 0, C.width, C.height, y.usedWidth, 0, h, f);
      };
      if (y.context.setTransform(1, 0, 0, 1, 0, 0), y.context.clearRect(y.usedWidth, 0, h, d), m(C))
        B();
      else if (m(O))
        if (E) {
          for (var F = O.level; F > a; F--)
            C = i.getElement(t, e, r, F, ba.downscale);
          B();
        } else
          return i.queueElement(t, O.level - 1), O;
      else {
        var R;
        if (!b && !E && !M)
          for (var X = a - 1; X >= Zn; X--) {
            var z = l.get(t, X);
            if (z) {
              R = z;
              break;
            }
          }
        if (m(R))
          return i.queueElement(t, a), R;
        y.context.translate(y.usedWidth, 0), y.context.scale(u, u), this.drawElement(y.context, t, e, c, !1), y.context.scale(1 / u, 1 / u), y.context.translate(-y.usedWidth, 0);
      }
      return v = {
        x: y.usedWidth,
        texture: y,
        level: a,
        scale: u,
        width: h,
        height: f,
        scaledLabelShown: c
      }, y.usedWidth += Math.ceil(h + yg), y.eleCaches.push(v), l.set(t, a, v), i.checkTextureFullness(y), v;
    }, Dt.invalidateElements = function(t) {
      for (var e = 0; e < t.length; e++)
        this.invalidateElement(t[e]);
    }, Dt.invalidateElement = function(t) {
      var e = this, r = e.lookup, a = [], n = r.isInvalid(t);
      if (n) {
        for (var i = Zn; i <= Vi; i++) {
          var s = r.getForCachedKey(t, i);
          s && a.push(s);
        }
        var o = r.invalidate(t);
        if (o)
          for (var l = 0; l < a.length; l++) {
            var u = a[l], f = u.texture;
            f.invalidatedWidth += u.width, u.invalidated = !0, e.checkTextureUtility(f);
          }
        e.removeFromQueue(t);
      }
    }, Dt.checkTextureUtility = function(t) {
      t.invalidatedWidth >= wg * t.width && this.retireTexture(t);
    }, Dt.checkTextureFullness = function(t) {
      var e = this, r = e.getTextureQueue(t.height);
      t.usedWidth / t.width > xg && t.fullnessChecks >= Tg ? wr(r, t) : t.fullnessChecks++;
    }, Dt.retireTexture = function(t) {
      var e = this, r = t.height, a = e.getTextureQueue(r), n = this.lookup;
      wr(a, t), t.retired = !0;
      for (var i = t.eleCaches, s = 0; s < i.length; s++) {
        var o = i[s];
        n.deleteCache(o.key, o.level);
      }
      oi(i);
      var l = e.getRetiredTextureQueue(r);
      l.push(t);
    }, Dt.addTexture = function(t, e) {
      var r = this, a = r.getTextureQueue(t), n = {};
      return a.push(n), n.eleCaches = [], n.height = t, n.width = Math.max(mg, e), n.usedWidth = 0, n.invalidatedWidth = 0, n.fullnessChecks = 0, n.canvas = r.renderer.makeOffscreenCanvas(n.width, n.height), n.context = n.canvas.getContext("2d"), n;
    }, Dt.recycleTexture = function(t, e) {
      for (var r = this, a = r.getTextureQueue(t), n = r.getRetiredTextureQueue(t), i = 0; i < n.length; i++) {
        var s = n[i];
        if (s.width >= e)
          return s.retired = !1, s.usedWidth = 0, s.invalidatedWidth = 0, s.fullnessChecks = 0, oi(s.eleCaches), s.context.setTransform(1, 0, 0, 1, 0, 0), s.context.clearRect(0, 0, s.width, s.height), wr(n, s), a.push(s), s;
      }
    }, Dt.queueElement = function(t, e) {
      var r = this, a = r.getElementQueue(), n = r.getElementKeyToQueue(), i = this.getKey(t), s = n[i];
      if (s)
        s.level = Math.max(s.level, e), s.eles.merge(t), s.reqs++, a.updateItem(s);
      else {
        var o = {
          eles: t.spawn().merge(t),
          level: e,
          reqs: 1,
          key: i
        };
        a.push(o), n[i] = o;
      }
    }, Dt.dequeue = function(t) {
      for (var e = this, r = e.getElementQueue(), a = e.getElementKeyToQueue(), n = [], i = e.lookup, s = 0; s < Og && r.size() > 0; s++) {
        var o = r.pop(), l = o.key, u = o.eles[0], f = i.hasCache(u, o.level);
        if (a[l] = null, f)
          continue;
        n.push(o);
        var h = e.getBoundingBox(u);
        e.getElement(u, h, t, o.level, ba.dequeue);
      }
      return n;
    }, Dt.removeFromQueue = function(t) {
      var e = this, r = e.getElementQueue(), a = e.getElementKeyToQueue(), n = this.getKey(t), i = a[n];
      i != null && (i.eles.length === 1 ? (i.reqs = ii, r.updateItem(i), r.pop(), a[n] = null) : i.eles.unmerge(t));
    }, Dt.onDequeue = function(t) {
      this.onDequeues.push(t);
    }, Dt.offDequeue = function(t) {
      wr(this.onDequeues, t);
    }, Dt.setupDequeueing = gu.setupDequeueing({
      deqRedrawThreshold: Ag,
      deqCost: Cg,
      deqAvgCost: Dg,
      deqNoDrawCost: Sg,
      deqFastCost: Lg,
      deq: function(e, r, a) {
        return e.dequeue(r, a);
      },
      onDeqd: function(e, r) {
        for (var a = 0; a < e.onDequeues.length; a++) {
          var n = e.onDequeues[a];
          n(r);
        }
      },
      shouldRedraw: function(e, r, a, n) {
        for (var i = 0; i < r.length; i++)
          for (var s = r[i].eles, o = 0; o < s.length; o++) {
            var l = s[o].boundingBox();
            if (hi(l, n))
              return !0;
          }
        return !1;
      },
      priority: function(e) {
        return e.renderer.beforeRenderPriorities.eleTxrDeq;
      }
    });
    var Mg = 1, en = -4, Qn = 2, Ig = 3.99, Rg = 50, kg = 50, Pg = 0.15, Bg = 0.1, Fg = 0.9, zg = 0.9, Gg = 1, yu = 250, $g = 4e3 * 4e3, Vg = !0, mu = function(e) {
      var r = this, a = r.renderer = e, n = a.cy;
      r.layersByLevel = {}, r.firstGet = !0, r.lastInvalidationTime = dr() - 2 * yu, r.skipping = !1, r.eleTxrDeqs = n.collection(), r.scheduleElementRefinement = fn(function() {
        r.refineElementTextures(r.eleTxrDeqs), r.eleTxrDeqs.unmerge(r.eleTxrDeqs);
      }, kg), a.beforeRender(function(s, o) {
        o - r.lastInvalidationTime <= yu ? r.skipping = !0 : r.skipping = !1;
      }, a.beforeRenderPriorities.lyrTxrSkip);
      var i = function(o, l) {
        return l.reqs - o.reqs;
      };
      r.layersQueue = new Ra(i), r.setupDequeueing();
    }, Mt = mu.prototype, bu = 0, _g = Math.pow(2, 53) - 1;
    Mt.makeLayer = function(t, e) {
      var r = Math.pow(2, e), a = Math.ceil(t.w * r), n = Math.ceil(t.h * r), i = this.renderer.makeOffscreenCanvas(a, n), s = {
        id: bu = ++bu % _g,
        bb: t,
        level: e,
        width: a,
        height: n,
        canvas: i,
        context: i.getContext("2d"),
        eles: [],
        elesQueue: [],
        reqs: 0
      }, o = s.context, l = -s.bb.x1, u = -s.bb.y1;
      return o.scale(r, r), o.translate(l, u), s;
    }, Mt.getLayers = function(t, e, r) {
      var a = this, n = a.renderer, i = n.cy, s = i.zoom(), o = a.firstGet;
      if (a.firstGet = !1, r == null) {
        if (r = Math.ceil(li(s * e)), r < en)
          r = en;
        else if (s >= Ig || r > Qn)
          return null;
      }
      a.validateLayersElesOrdering(r, t);
      var l = a.layersByLevel, u = Math.pow(2, r), f = l[r] = l[r] || [], h, c = a.levelIsComplete(r, t), v, d = function() {
        var B = function(re) {
          if (a.validateLayersElesOrdering(re, t), a.levelIsComplete(re, t))
            return v = l[re], !0;
        }, F = function(re) {
          if (!v)
            for (var W = r + re; en <= W && W <= Qn && !B(W); W += re)
              ;
        };
        F(1), F(-1);
        for (var R = f.length - 1; R >= 0; R--) {
          var X = f[R];
          X.invalid && wr(f, X);
        }
      };
      if (!c)
        d();
      else
        return f;
      var g = function() {
        if (!h) {
          h = Ut();
          for (var B = 0; B < t.length; B++)
            Df(h, t[B].boundingBox());
        }
        return h;
      }, y = function(B) {
        B = B || {};
        var F = B.after;
        g();
        var R = h.w * u * (h.h * u);
        if (R > $g)
          return null;
        var X = a.makeLayer(h, r);
        if (F != null) {
          var z = f.indexOf(F) + 1;
          f.splice(z, 0, X);
        } else
          (B.insert === void 0 || B.insert) && f.unshift(X);
        return X;
      };
      if (a.skipping && !o)
        return null;
      for (var p = null, m = t.length / Mg, b = !o, E = 0; E < t.length; E++) {
        var M = t[E], O = M._private.rscratch, x = O.imgLayerCaches = O.imgLayerCaches || {}, I = x[r];
        if (I) {
          p = I;
          continue;
        }
        if ((!p || p.eles.length >= m || !xs(p.bb, M.boundingBox())) && (p = y({
          insert: !0,
          after: p
        }), !p))
          return null;
        v || b ? a.queueLayer(p, M) : a.drawEleInLayer(p, M, r, e), p.eles.push(M), x[r] = p;
      }
      return v || (b ? null : f);
    }, Mt.getEleLevelForLayerLevel = function(t, e) {
      return t;
    }, Mt.drawEleInLayer = function(t, e, r, a) {
      var n = this, i = this.renderer, s = t.context, o = e.boundingBox();
      o.w === 0 || o.h === 0 || !e.visible() || (r = n.getEleLevelForLayerLevel(r, a), i.setImgSmoothing(s, !1), i.drawCachedElement(s, e, null, null, r, Vg), i.setImgSmoothing(s, !0));
    }, Mt.levelIsComplete = function(t, e) {
      var r = this, a = r.layersByLevel[t];
      if (!a || a.length === 0)
        return !1;
      for (var n = 0, i = 0; i < a.length; i++) {
        var s = a[i];
        if (s.reqs > 0 || s.invalid)
          return !1;
        n += s.eles.length;
      }
      return n === e.length;
    }, Mt.validateLayersElesOrdering = function(t, e) {
      var r = this.layersByLevel[t];
      if (r)
        for (var a = 0; a < r.length; a++) {
          for (var n = r[a], i = -1, s = 0; s < e.length; s++)
            if (n.eles[0] === e[s]) {
              i = s;
              break;
            }
          if (i < 0) {
            this.invalidateLayer(n);
            continue;
          }
          for (var o = i, s = 0; s < n.eles.length; s++)
            if (n.eles[s] !== e[o + s]) {
              this.invalidateLayer(n);
              break;
            }
        }
    }, Mt.updateElementsInLayers = function(t, e) {
      for (var r = this, a = Ae(t[0]), n = 0; n < t.length; n++)
        for (var i = a ? null : t[n], s = a ? t[n] : t[n].ele, o = s._private.rscratch, l = o.imgLayerCaches = o.imgLayerCaches || {}, u = en; u <= Qn; u++) {
          var f = l[u];
          f && (i && r.getEleLevelForLayerLevel(f.level) !== i.level || e(f, s, i));
        }
    }, Mt.haveLayers = function() {
      for (var t = this, e = !1, r = en; r <= Qn; r++) {
        var a = t.layersByLevel[r];
        if (a && a.length > 0) {
          e = !0;
          break;
        }
      }
      return e;
    }, Mt.invalidateElements = function(t) {
      var e = this;
      t.length !== 0 && (e.lastInvalidationTime = dr(), !(t.length === 0 || !e.haveLayers()) && e.updateElementsInLayers(t, function(a, n, i) {
        e.invalidateLayer(a);
      }));
    }, Mt.invalidateLayer = function(t) {
      if (this.lastInvalidationTime = dr(), !t.invalid) {
        var e = t.level, r = t.eles, a = this.layersByLevel[e];
        wr(a, t), t.elesQueue = [], t.invalid = !0, t.replacement && (t.replacement.invalid = !0);
        for (var n = 0; n < r.length; n++) {
          var i = r[n]._private.rscratch.imgLayerCaches;
          i && (i[e] = null);
        }
      }
    }, Mt.refineElementTextures = function(t) {
      var e = this;
      e.updateElementsInLayers(t, function(a, n, i) {
        var s = a.replacement;
        if (s || (s = a.replacement = e.makeLayer(a.bb, a.level), s.replaces = a, s.eles = a.eles), !s.reqs)
          for (var o = 0; o < s.eles.length; o++)
            e.queueLayer(s, s.eles[o]);
      });
    }, Mt.enqueueElementRefinement = function(t) {
      this.eleTxrDeqs.merge(t), this.scheduleElementRefinement();
    }, Mt.queueLayer = function(t, e) {
      var r = this, a = r.layersQueue, n = t.elesQueue, i = n.hasId = n.hasId || {};
      if (!t.replacement) {
        if (e) {
          if (i[e.id()])
            return;
          n.push(e), i[e.id()] = !0;
        }
        t.reqs ? (t.reqs++, a.updateItem(t)) : (t.reqs = 1, a.push(t));
      }
    }, Mt.dequeue = function(t) {
      for (var e = this, r = e.layersQueue, a = [], n = 0; n < Gg && r.size() !== 0; ) {
        var i = r.peek();
        if (i.replacement) {
          r.pop();
          continue;
        }
        if (i.replaces && i !== i.replaces.replacement) {
          r.pop();
          continue;
        }
        if (i.invalid) {
          r.pop();
          continue;
        }
        var s = i.elesQueue.shift();
        s && (e.drawEleInLayer(i, s, i.level, t), n++), a.length === 0 && a.push(!0), i.elesQueue.length === 0 && (r.pop(), i.reqs = 0, i.replaces && e.applyLayerReplacement(i), e.requestRedraw());
      }
      return a;
    }, Mt.applyLayerReplacement = function(t) {
      var e = this, r = e.layersByLevel[t.level], a = t.replaces, n = r.indexOf(a);
      if (!(n < 0 || a.invalid)) {
        r[n] = t;
        for (var i = 0; i < t.eles.length; i++) {
          var s = t.eles[i]._private, o = s.imgLayerCaches = s.imgLayerCaches || {};
          o && (o[t.level] = t);
        }
        e.requestRedraw();
      }
    }, Mt.requestRedraw = fn(function() {
      var t = this.renderer;
      t.redrawHint("eles", !0), t.redrawHint("drag", !0), t.redraw();
    }, 100), Mt.setupDequeueing = gu.setupDequeueing({
      deqRedrawThreshold: Rg,
      deqCost: Pg,
      deqAvgCost: Bg,
      deqNoDrawCost: Fg,
      deqFastCost: zg,
      deq: function(e, r) {
        return e.dequeue(r);
      },
      onDeqd: si,
      shouldRedraw: vs,
      priority: function(e) {
        return e.renderer.beforeRenderPriorities.lyrTxrDeq;
      }
    });
    var Eu = {}, wu;
    function Ug(t, e) {
      for (var r = 0; r < e.length; r++) {
        var a = e[r];
        t.lineTo(a.x, a.y);
      }
    }
    function Yg(t, e, r) {
      for (var a, n = 0; n < e.length; n++) {
        var i = e[n];
        n === 0 && (a = i), t.lineTo(i.x, i.y);
      }
      t.quadraticCurveTo(r.x, r.y, a.x, a.y);
    }
    function xu(t, e, r) {
      t.beginPath && t.beginPath();
      for (var a = e, n = 0; n < a.length; n++) {
        var i = a[n];
        t.lineTo(i.x, i.y);
      }
      var s = r, o = r[0];
      t.moveTo(o.x, o.y);
      for (var n = 1; n < s.length; n++) {
        var i = s[n];
        t.lineTo(i.x, i.y);
      }
      t.closePath && t.closePath();
    }
    function Hg(t, e, r, a, n) {
      t.beginPath && t.beginPath(), t.arc(r, a, n, 0, Math.PI * 2, !1);
      var i = e, s = i[0];
      t.moveTo(s.x, s.y);
      for (var o = 0; o < i.length; o++) {
        var l = i[o];
        t.lineTo(l.x, l.y);
      }
      t.closePath && t.closePath();
    }
    function Xg(t, e, r, a) {
      t.arc(e, r, a, 0, Math.PI * 2, !1);
    }
    Eu.arrowShapeImpl = function(t) {
      return (wu || (wu = {
        polygon: Ug,
        "triangle-backcurve": Yg,
        "triangle-tee": xu,
        "circle-triangle": Hg,
        "triangle-cross": xu,
        circle: Xg
      }))[t];
    };
    var hr = {};
    hr.drawElement = function(t, e, r, a, n, i) {
      var s = this;
      e.isNode() ? s.drawNode(t, e, r, a, n, i) : s.drawEdge(t, e, r, a, n, i);
    }, hr.drawElementOverlay = function(t, e) {
      var r = this;
      e.isNode() ? r.drawNodeOverlay(t, e) : r.drawEdgeOverlay(t, e);
    }, hr.drawElementUnderlay = function(t, e) {
      var r = this;
      e.isNode() ? r.drawNodeUnderlay(t, e) : r.drawEdgeUnderlay(t, e);
    }, hr.drawCachedElementPortion = function(t, e, r, a, n, i, s, o) {
      var l = this, u = r.getBoundingBox(e);
      if (!(u.w === 0 || u.h === 0)) {
        var f = r.getElement(e, u, a, n, i);
        if (f != null) {
          var h = o(l, e);
          if (h === 0)
            return;
          var c = s(l, e), v = u.x1, d = u.y1, g = u.w, y = u.h, p, m, b, E, M;
          if (c !== 0) {
            var O = r.getRotationPoint(e);
            b = O.x, E = O.y, t.translate(b, E), t.rotate(c), M = l.getImgSmoothing(t), M || l.setImgSmoothing(t, !0);
            var x = r.getRotationOffset(e);
            p = x.x, m = x.y;
          } else
            p = v, m = d;
          var I;
          h !== 1 && (I = t.globalAlpha, t.globalAlpha = I * h), t.drawImage(f.texture.canvas, f.x, 0, f.width, f.height, p, m, g, y), h !== 1 && (t.globalAlpha = I), c !== 0 && (t.rotate(-c), t.translate(-b, -E), M || l.setImgSmoothing(t, !1));
        } else
          r.drawElement(t, e);
      }
    };
    var qg = function() {
      return 0;
    }, Wg = function(e, r) {
      return e.getTextAngle(r, null);
    }, Kg = function(e, r) {
      return e.getTextAngle(r, "source");
    }, Zg = function(e, r) {
      return e.getTextAngle(r, "target");
    }, Qg = function(e, r) {
      return r.effectiveOpacity();
    }, _i = function(e, r) {
      return r.pstyle("text-opacity").pfValue * r.effectiveOpacity();
    };
    hr.drawCachedElement = function(t, e, r, a, n, i) {
      var s = this, o = s.data, l = o.eleTxrCache, u = o.lblTxrCache, f = o.slbTxrCache, h = o.tlbTxrCache, c = e.boundingBox(), v = i === !0 ? l.reasons.highQuality : null;
      if (!(c.w === 0 || c.h === 0 || !e.visible()) && (!a || hi(c, a))) {
        var d = e.isEdge(), g = e.element()._private.rscratch.badLine;
        s.drawElementUnderlay(t, e), s.drawCachedElementPortion(t, e, l, r, n, v, qg, Qg), (!d || !g) && s.drawCachedElementPortion(t, e, u, r, n, v, Wg, _i), d && !g && (s.drawCachedElementPortion(t, e, f, r, n, v, Kg, _i), s.drawCachedElementPortion(t, e, h, r, n, v, Zg, _i)), s.drawElementOverlay(t, e);
      }
    }, hr.drawElements = function(t, e) {
      for (var r = this, a = 0; a < e.length; a++) {
        var n = e[a];
        r.drawElement(t, n);
      }
    }, hr.drawCachedElements = function(t, e, r, a) {
      for (var n = this, i = 0; i < e.length; i++) {
        var s = e[i];
        n.drawCachedElement(t, s, r, a);
      }
    }, hr.drawCachedNodes = function(t, e, r, a) {
      for (var n = this, i = 0; i < e.length; i++) {
        var s = e[i];
        s.isNode() && n.drawCachedElement(t, s, r, a);
      }
    }, hr.drawLayeredElements = function(t, e, r, a) {
      var n = this, i = n.data.lyrTxrCache.getLayers(e, r);
      if (i)
        for (var s = 0; s < i.length; s++) {
          var o = i[s], l = o.bb;
          l.w === 0 || l.h === 0 || t.drawImage(o.canvas, l.x1, l.y1, l.w, l.h);
        }
      else
        n.drawCachedElements(t, e, r, a);
    };
    var mr = {};
    mr.drawEdge = function(t, e, r) {
      var a = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : !0, n = arguments.length > 4 && arguments[4] !== void 0 ? arguments[4] : !0, i = arguments.length > 5 && arguments[5] !== void 0 ? arguments[5] : !0, s = this, o = e._private.rscratch;
      if (!(i && !e.visible()) && !(o.badLine || o.allpts == null || isNaN(o.allpts[0]))) {
        var l;
        r && (l = r, t.translate(-l.x1, -l.y1));
        var u = i ? e.pstyle("opacity").value : 1, f = i ? e.pstyle("line-opacity").value : 1, h = e.pstyle("curve-style").value, c = e.pstyle("line-style").value, v = e.pstyle("width").pfValue, d = e.pstyle("line-cap").value, g = u * f, y = u * f, p = function() {
          var R = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : g;
          h === "straight-triangle" ? (s.eleStrokeStyle(t, e, R), s.drawEdgeTrianglePath(e, t, o.allpts)) : (t.lineWidth = v, t.lineCap = d, s.eleStrokeStyle(t, e, R), s.drawEdgePath(e, t, o.allpts, c), t.lineCap = "butt");
        }, m = function() {
          n && s.drawEdgeOverlay(t, e);
        }, b = function() {
          n && s.drawEdgeUnderlay(t, e);
        }, E = function() {
          var R = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : y;
          s.drawArrowheads(t, e, R);
        }, M = function() {
          s.drawElementText(t, e, null, a);
        };
        t.lineJoin = "round";
        var O = e.pstyle("ghost").value === "yes";
        if (O) {
          var x = e.pstyle("ghost-offset-x").pfValue, I = e.pstyle("ghost-offset-y").pfValue, C = e.pstyle("ghost-opacity").value, B = g * C;
          t.translate(x, I), p(B), E(B), t.translate(-x, -I);
        }
        b(), p(), E(), m(), M(), r && t.translate(l.x1, l.y1);
      }
    };
    var Tu = function(e) {
      if (!["overlay", "underlay"].includes(e))
        throw new Error("Invalid state");
      return function(r, a) {
        if (a.visible()) {
          var n = a.pstyle("".concat(e, "-opacity")).value;
          if (n !== 0) {
            var i = this, s = i.usePaths(), o = a._private.rscratch, l = a.pstyle("".concat(e, "-padding")).pfValue, u = 2 * l, f = a.pstyle("".concat(e, "-color")).value;
            r.lineWidth = u, o.edgeType === "self" && !s ? r.lineCap = "butt" : r.lineCap = "round", i.colorStrokeStyle(r, f[0], f[1], f[2], n), i.drawEdgePath(a, r, o.allpts, "solid");
          }
        }
      };
    };
    mr.drawEdgeOverlay = Tu("overlay"), mr.drawEdgeUnderlay = Tu("underlay"), mr.drawEdgePath = function(t, e, r, a) {
      var n = t._private.rscratch, i = e, s, o = !1, l = this.usePaths(), u = t.pstyle("line-dash-pattern").pfValue, f = t.pstyle("line-dash-offset").pfValue;
      if (l) {
        var h = r.join("$"), c = n.pathCacheKey && n.pathCacheKey === h;
        c ? (s = e = n.pathCache, o = !0) : (s = e = new Path2D(), n.pathCacheKey = h, n.pathCache = s);
      }
      if (i.setLineDash)
        switch (a) {
          case "dotted":
            i.setLineDash([1, 1]);
            break;
          case "dashed":
            i.setLineDash(u), i.lineDashOffset = f;
            break;
          case "solid":
            i.setLineDash([]);
            break;
        }
      if (!o && !n.badLine)
        switch (e.beginPath && e.beginPath(), e.moveTo(r[0], r[1]), n.edgeType) {
          case "bezier":
          case "self":
          case "compound":
          case "multibezier":
            for (var v = 2; v + 3 < r.length; v += 4)
              e.quadraticCurveTo(r[v], r[v + 1], r[v + 2], r[v + 3]);
            break;
          case "straight":
          case "segments":
          case "haystack":
            for (var d = 2; d + 1 < r.length; d += 2)
              e.lineTo(r[d], r[d + 1]);
            break;
        }
      e = i, l ? e.stroke(s) : e.stroke(), e.setLineDash && e.setLineDash([]);
    }, mr.drawEdgeTrianglePath = function(t, e, r) {
      e.fillStyle = e.strokeStyle;
      for (var a = t.pstyle("width").pfValue, n = 0; n + 1 < r.length; n += 2) {
        var i = [r[n + 2] - r[n], r[n + 3] - r[n + 1]], s = Math.sqrt(i[0] * i[0] + i[1] * i[1]), o = [i[1] / s, -i[0] / s], l = [o[0] * a / 2, o[1] * a / 2];
        e.beginPath(), e.moveTo(r[n] - l[0], r[n + 1] - l[1]), e.lineTo(r[n] + l[0], r[n + 1] + l[1]), e.lineTo(r[n + 2], r[n + 3]), e.closePath(), e.fill();
      }
    }, mr.drawArrowheads = function(t, e, r) {
      var a = e._private.rscratch, n = a.edgeType === "haystack";
      n || this.drawArrowhead(t, e, "source", a.arrowStartX, a.arrowStartY, a.srcArrowAngle, r), this.drawArrowhead(t, e, "mid-target", a.midX, a.midY, a.midtgtArrowAngle, r), this.drawArrowhead(t, e, "mid-source", a.midX, a.midY, a.midsrcArrowAngle, r), n || this.drawArrowhead(t, e, "target", a.arrowEndX, a.arrowEndY, a.tgtArrowAngle, r);
    }, mr.drawArrowhead = function(t, e, r, a, n, i, s) {
      if (!(isNaN(a) || a == null || isNaN(n) || n == null || isNaN(i) || i == null)) {
        var o = this, l = e.pstyle(r + "-arrow-shape").value;
        if (l !== "none") {
          var u = e.pstyle(r + "-arrow-fill").value === "hollow" ? "both" : "filled", f = e.pstyle(r + "-arrow-fill").value, h = e.pstyle("width").pfValue, c = e.pstyle("opacity").value;
          s === void 0 && (s = c);
          var v = t.globalCompositeOperation;
          (s !== 1 || f === "hollow") && (t.globalCompositeOperation = "destination-out", o.colorFillStyle(t, 255, 255, 255, 1), o.colorStrokeStyle(t, 255, 255, 255, 1), o.drawArrowShape(e, t, u, h, l, a, n, i), t.globalCompositeOperation = v);
          var d = e.pstyle(r + "-arrow-color").value;
          o.colorFillStyle(t, d[0], d[1], d[2], s), o.colorStrokeStyle(t, d[0], d[1], d[2], s), o.drawArrowShape(e, t, f, h, l, a, n, i);
        }
      }
    }, mr.drawArrowShape = function(t, e, r, a, n, i, s, o) {
      var l = this, u = this.usePaths() && n !== "triangle-cross", f = !1, h, c = e, v = {
        x: i,
        y: s
      }, d = t.pstyle("arrow-scale").value, g = this.getArrowWidth(a, d), y = l.arrowShapes[n];
      if (u) {
        var p = l.arrowPathCache = l.arrowPathCache || [], m = kr(n), b = p[m];
        b != null ? (h = e = b, f = !0) : (h = e = new Path2D(), p[m] = h);
      }
      f || (e.beginPath && e.beginPath(), u ? y.draw(e, 1, 0, {
        x: 0,
        y: 0
      }, 1) : y.draw(e, g, o, v, a), e.closePath && e.closePath()), e = c, u && (e.translate(i, s), e.rotate(o), e.scale(g, g)), (r === "filled" || r === "both") && (u ? e.fill(h) : e.fill()), (r === "hollow" || r === "both") && (e.lineWidth = (y.matchEdgeWidth ? a : 1) / (u ? g : 1), e.lineJoin = "miter", u ? e.stroke(h) : e.stroke()), u && (e.scale(1 / g, 1 / g), e.rotate(-o), e.translate(-i, -s));
    };
    var Ui = {};
    Ui.safeDrawImage = function(t, e, r, a, n, i, s, o, l, u) {
      if (!(n <= 0 || i <= 0 || l <= 0 || u <= 0))
        try {
          t.drawImage(e, r, a, n, i, s, o, l, u);
        } catch (f) {
          ft(f);
        }
    }, Ui.drawInscribedImage = function(t, e, r, a, n) {
      var i = this, s = r.position(), o = s.x, l = s.y, u = r.cy().style(), f = u.getIndexedStyle.bind(u), h = f(r, "background-fit", "value", a), c = f(r, "background-repeat", "value", a), v = r.width(), d = r.height(), g = r.padding() * 2, y = v + (f(r, "background-width-relative-to", "value", a) === "inner" ? 0 : g), p = d + (f(r, "background-height-relative-to", "value", a) === "inner" ? 0 : g), m = r._private.rscratch, b = f(r, "background-clip", "value", a), E = b === "node", M = f(r, "background-image-opacity", "value", a) * n, O = f(r, "background-image-smoothing", "value", a), x = e.width || e.cachedW, I = e.height || e.cachedH;
      (x == null || I == null) && (document.body.appendChild(e), x = e.cachedW = e.width || e.offsetWidth, I = e.cachedH = e.height || e.offsetHeight, document.body.removeChild(e));
      var C = x, B = I;
      if (f(r, "background-width", "value", a) !== "auto" && (f(r, "background-width", "units", a) === "%" ? C = f(r, "background-width", "pfValue", a) * y : C = f(r, "background-width", "pfValue", a)), f(r, "background-height", "value", a) !== "auto" && (f(r, "background-height", "units", a) === "%" ? B = f(r, "background-height", "pfValue", a) * p : B = f(r, "background-height", "pfValue", a)), !(C === 0 || B === 0)) {
        if (h === "contain") {
          var F = Math.min(y / C, p / B);
          C *= F, B *= F;
        } else if (h === "cover") {
          var F = Math.max(y / C, p / B);
          C *= F, B *= F;
        }
        var R = o - y / 2, X = f(r, "background-position-x", "units", a), z = f(r, "background-position-x", "pfValue", a);
        X === "%" ? R += (y - C) * z : R += z;
        var re = f(r, "background-offset-x", "units", a), W = f(r, "background-offset-x", "pfValue", a);
        re === "%" ? R += (y - C) * W : R += W;
        var Z = l - p / 2, ie = f(r, "background-position-y", "units", a), oe = f(r, "background-position-y", "pfValue", a);
        ie === "%" ? Z += (p - B) * oe : Z += oe;
        var ge = f(r, "background-offset-y", "units", a), se = f(r, "background-offset-y", "pfValue", a);
        ge === "%" ? Z += (p - B) * se : Z += se, m.pathCache && (R -= o, Z -= l, o = 0, l = 0);
        var de = t.globalAlpha;
        t.globalAlpha = M;
        var we = i.getImgSmoothing(t), Te = !1;
        if (O === "no" && we ? (i.setImgSmoothing(t, !1), Te = !0) : O === "yes" && !we && (i.setImgSmoothing(t, !0), Te = !0), c === "no-repeat")
          E && (t.save(), m.pathCache ? t.clip(m.pathCache) : (i.nodeShapes[i.getNodeShape(r)].draw(t, o, l, y, p), t.clip())), i.safeDrawImage(t, e, 0, 0, x, I, R, Z, C, B), E && t.restore();
        else {
          var Ee = t.createPattern(e, c);
          t.fillStyle = Ee, i.nodeShapes[i.getNodeShape(r)].draw(t, o, l, y, p), t.translate(R, Z), t.fill(), t.translate(-R, -Z);
        }
        t.globalAlpha = de, Te && i.setImgSmoothing(t, we);
      }
    };
    var _r = {};
    _r.eleTextBiggerThanMin = function(t, e) {
      if (!e) {
        var r = t.cy().zoom(), a = this.getPixelRatio(), n = Math.ceil(li(r * a));
        e = Math.pow(2, n);
      }
      var i = t.pstyle("font-size").pfValue * e, s = t.pstyle("min-zoomed-font-size").pfValue;
      return !(i < s);
    }, _r.drawElementText = function(t, e, r, a, n) {
      var i = arguments.length > 5 && arguments[5] !== void 0 ? arguments[5] : !0, s = this;
      if (a == null) {
        if (i && !s.eleTextBiggerThanMin(e))
          return;
      } else if (a === !1)
        return;
      if (e.isNode()) {
        var o = e.pstyle("label");
        if (!o || !o.value)
          return;
        var l = s.getLabelJustification(e);
        t.textAlign = l, t.textBaseline = "bottom";
      } else {
        var u = e.element()._private.rscratch.badLine, f = e.pstyle("label"), h = e.pstyle("source-label"), c = e.pstyle("target-label");
        if (u || (!f || !f.value) && (!h || !h.value) && (!c || !c.value))
          return;
        t.textAlign = "center", t.textBaseline = "bottom";
      }
      var v = !r, d;
      r && (d = r, t.translate(-d.x1, -d.y1)), n == null ? (s.drawText(t, e, null, v, i), e.isEdge() && (s.drawText(t, e, "source", v, i), s.drawText(t, e, "target", v, i))) : s.drawText(t, e, n, v, i), r && t.translate(d.x1, d.y1);
    }, _r.getFontCache = function(t) {
      var e;
      this.fontCaches = this.fontCaches || [];
      for (var r = 0; r < this.fontCaches.length; r++)
        if (e = this.fontCaches[r], e.context === t)
          return e;
      return e = {
        context: t
      }, this.fontCaches.push(e), e;
    }, _r.setupTextStyle = function(t, e) {
      var r = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : !0, a = e.pstyle("font-style").strValue, n = e.pstyle("font-size").pfValue + "px", i = e.pstyle("font-family").strValue, s = e.pstyle("font-weight").strValue, o = r ? e.effectiveOpacity() * e.pstyle("text-opacity").value : 1, l = e.pstyle("text-outline-opacity").value * o, u = e.pstyle("color").value, f = e.pstyle("text-outline-color").value;
      t.font = a + " " + s + " " + n + " " + i, t.lineJoin = "round", this.colorFillStyle(t, u[0], u[1], u[2], o), this.colorStrokeStyle(t, f[0], f[1], f[2], l);
    };
    function Jg(t, e, r, a, n) {
      var i = arguments.length > 5 && arguments[5] !== void 0 ? arguments[5] : 5;
      t.beginPath(), t.moveTo(e + i, r), t.lineTo(e + a - i, r), t.quadraticCurveTo(e + a, r, e + a, r + i), t.lineTo(e + a, r + n - i), t.quadraticCurveTo(e + a, r + n, e + a - i, r + n), t.lineTo(e + i, r + n), t.quadraticCurveTo(e, r + n, e, r + n - i), t.lineTo(e, r + i), t.quadraticCurveTo(e, r, e + i, r), t.closePath(), t.fill();
    }
    _r.getTextAngle = function(t, e) {
      var r, a = t._private, n = a.rscratch, i = e ? e + "-" : "", s = t.pstyle(i + "text-rotation"), o = er(n, "labelAngle", e);
      return s.strValue === "autorotate" ? r = t.isEdge() ? o : 0 : s.strValue === "none" ? r = 0 : r = s.pfValue, r;
    }, _r.drawText = function(t, e, r) {
      var a = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : !0, n = arguments.length > 4 && arguments[4] !== void 0 ? arguments[4] : !0, i = e._private, s = i.rscratch, o = n ? e.effectiveOpacity() : 1;
      if (!(n && (o === 0 || e.pstyle("text-opacity").value === 0))) {
        r === "main" && (r = null);
        var l = er(s, "labelX", r), u = er(s, "labelY", r), f, h, c = this.getLabelText(e, r);
        if (c != null && c !== "" && !isNaN(l) && !isNaN(u)) {
          this.setupTextStyle(t, e, n);
          var v = r ? r + "-" : "", d = er(s, "labelWidth", r), g = er(s, "labelHeight", r), y = e.pstyle(v + "text-margin-x").pfValue, p = e.pstyle(v + "text-margin-y").pfValue, m = e.isEdge(), b = e.pstyle("text-halign").value, E = e.pstyle("text-valign").value;
          m && (b = "center", E = "center"), l += y, u += p;
          var M;
          switch (a ? M = this.getTextAngle(e, r) : M = 0, M !== 0 && (f = l, h = u, t.translate(f, h), t.rotate(M), l = 0, u = 0), E) {
            case "top":
              break;
            case "center":
              u += g / 2;
              break;
            case "bottom":
              u += g;
              break;
          }
          var O = e.pstyle("text-background-opacity").value, x = e.pstyle("text-border-opacity").value, I = e.pstyle("text-border-width").pfValue, C = e.pstyle("text-background-padding").pfValue;
          if (O > 0 || I > 0 && x > 0) {
            var B = l - C;
            switch (b) {
              case "left":
                B -= d;
                break;
              case "center":
                B -= d / 2;
                break;
            }
            var F = u - g - C, R = d + 2 * C, X = g + 2 * C;
            if (O > 0) {
              var z = t.fillStyle, re = e.pstyle("text-background-color").value;
              t.fillStyle = "rgba(" + re[0] + "," + re[1] + "," + re[2] + "," + O * o + ")";
              var W = e.pstyle("text-background-shape").strValue;
              W.indexOf("round") === 0 ? Jg(t, B, F, R, X, 2) : t.fillRect(B, F, R, X), t.fillStyle = z;
            }
            if (I > 0 && x > 0) {
              var Z = t.strokeStyle, ie = t.lineWidth, oe = e.pstyle("text-border-color").value, ge = e.pstyle("text-border-style").value;
              if (t.strokeStyle = "rgba(" + oe[0] + "," + oe[1] + "," + oe[2] + "," + x * o + ")", t.lineWidth = I, t.setLineDash)
                switch (ge) {
                  case "dotted":
                    t.setLineDash([1, 1]);
                    break;
                  case "dashed":
                    t.setLineDash([4, 2]);
                    break;
                  case "double":
                    t.lineWidth = I / 4, t.setLineDash([]);
                    break;
                  case "solid":
                    t.setLineDash([]);
                    break;
                }
              if (t.strokeRect(B, F, R, X), ge === "double") {
                var se = I / 2;
                t.strokeRect(B + se, F + se, R - se * 2, X - se * 2);
              }
              t.setLineDash && t.setLineDash([]), t.lineWidth = ie, t.strokeStyle = Z;
            }
          }
          var de = 2 * e.pstyle("text-outline-width").pfValue;
          if (de > 0 && (t.lineWidth = de), e.pstyle("text-wrap").value === "wrap") {
            var we = er(s, "labelWrapCachedLines", r), Te = er(s, "labelLineHeight", r), Ee = d / 2, ye = this.getLabelJustification(e);
            switch (ye === "auto" || (b === "left" ? ye === "left" ? l += -d : ye === "center" && (l += -Ee) : b === "center" ? ye === "left" ? l += -Ee : ye === "right" && (l += Ee) : b === "right" && (ye === "center" ? l += Ee : ye === "right" && (l += d))), E) {
              case "top":
                u -= (we.length - 1) * Te;
                break;
              case "center":
              case "bottom":
                u -= (we.length - 1) * Te;
                break;
            }
            for (var ae = 0; ae < we.length; ae++)
              de > 0 && t.strokeText(we[ae], l, u), t.fillText(we[ae], l, u), u += Te;
          } else
            de > 0 && t.strokeText(c, l, u), t.fillText(c, l, u);
          M !== 0 && (t.rotate(-M), t.translate(-f, -h));
        }
      }
    };
    var Ea = {};
    Ea.drawNode = function(t, e, r) {
      var a = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : !0, n = arguments.length > 4 && arguments[4] !== void 0 ? arguments[4] : !0, i = arguments.length > 5 && arguments[5] !== void 0 ? arguments[5] : !0, s = this, o, l, u = e._private, f = u.rscratch, h = e.position();
      if (!(!k(h.x) || !k(h.y)) && !(i && !e.visible())) {
        var c = i ? e.effectiveOpacity() : 1, v = s.usePaths(), d, g = !1, y = e.padding();
        o = e.width() + 2 * y, l = e.height() + 2 * y;
        var p;
        r && (p = r, t.translate(-p.x1, -p.y1));
        for (var m = e.pstyle("background-image"), b = m.value, E = new Array(b.length), M = new Array(b.length), O = 0, x = 0; x < b.length; x++) {
          var I = b[x], C = E[x] = I != null && I !== "none";
          if (C) {
            var B = e.cy().style().getIndexedStyle(e, "background-image-crossorigin", "value", x);
            O++, M[x] = s.getCachedImage(I, B, function() {
              u.backgroundTimestamp = Date.now(), e.emitAndNotify("background");
            });
          }
        }
        var F = e.pstyle("background-blacken").value, R = e.pstyle("border-width").pfValue, X = e.pstyle("background-opacity").value * c, z = e.pstyle("border-color").value, re = e.pstyle("border-style").value, W = e.pstyle("border-opacity").value * c;
        t.lineJoin = "miter";
        var Z = function() {
          var ke = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : X;
          s.eleFillStyle(t, e, ke);
        }, ie = function() {
          var ke = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : W;
          s.colorStrokeStyle(t, z[0], z[1], z[2], ke);
        }, oe = e.pstyle("shape").strValue, ge = e.pstyle("shape-polygon-points").pfValue;
        if (v) {
          t.translate(h.x, h.y);
          var se = s.nodePathCache = s.nodePathCache || [], de = hs(oe === "polygon" ? oe + "," + ge.join(",") : oe, "" + l, "" + o), we = se[de];
          we != null ? (d = we, g = !0, f.pathCache = d) : (d = new Path2D(), se[de] = f.pathCache = d);
        }
        var Te = function() {
          if (!g) {
            var ke = h;
            v && (ke = {
              x: 0,
              y: 0
            }), s.nodeShapes[s.getNodeShape(e)].draw(d || t, ke.x, ke.y, o, l);
          }
          v ? t.fill(d) : t.fill();
        }, Ee = function() {
          for (var ke = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : c, Ge = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !0, et = u.backgrounding, We = 0, Ye = 0; Ye < M.length; Ye++) {
            var Se = e.cy().style().getIndexedStyle(e, "background-image-containment", "value", Ye);
            if (Ge && Se === "over" || !Ge && Se === "inside") {
              We++;
              continue;
            }
            E[Ye] && M[Ye].complete && !M[Ye].error && (We++, s.drawInscribedImage(t, M[Ye], e, Ye, ke));
          }
          u.backgrounding = We !== O, et !== u.backgrounding && e.updateStyle(!1);
        }, ye = function() {
          var ke = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : !1, Ge = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : c;
          s.hasPie(e) && (s.drawPie(t, e, Ge), ke && (v || s.nodeShapes[s.getNodeShape(e)].draw(t, h.x, h.y, o, l)));
        }, ae = function() {
          var ke = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : c, Ge = (F > 0 ? F : -F) * ke, et = F > 0 ? 0 : 255;
          F !== 0 && (s.colorFillStyle(t, et, et, et, Ge), v ? t.fill(d) : t.fill());
        }, xe = function() {
          if (R > 0) {
            if (t.lineWidth = R, t.lineCap = "butt", t.setLineDash)
              switch (re) {
                case "dotted":
                  t.setLineDash([1, 1]);
                  break;
                case "dashed":
                  t.setLineDash([4, 2]);
                  break;
                case "solid":
                case "double":
                  t.setLineDash([]);
                  break;
              }
            if (v ? t.stroke(d) : t.stroke(), re === "double") {
              t.lineWidth = R / 3;
              var ke = t.globalCompositeOperation;
              t.globalCompositeOperation = "destination-out", v ? t.stroke(d) : t.stroke(), t.globalCompositeOperation = ke;
            }
            t.setLineDash && t.setLineDash([]);
          }
        }, Ce = function() {
          n && s.drawNodeOverlay(t, e, h, o, l);
        }, Oe = function() {
          n && s.drawNodeUnderlay(t, e, h, o, l);
        }, Ie = function() {
          s.drawElementText(t, e, null, a);
        }, He = e.pstyle("ghost").value === "yes";
        if (He) {
          var qe = e.pstyle("ghost-offset-x").pfValue, Re = e.pstyle("ghost-offset-y").pfValue, Me = e.pstyle("ghost-opacity").value, Ve = Me * c;
          t.translate(qe, Re), Z(Me * X), Te(), Ee(Ve, !0), ie(Me * W), xe(), ye(F !== 0 || R !== 0), Ee(Ve, !1), ae(Ve), t.translate(-qe, -Re);
        }
        v && t.translate(-h.x, -h.y), Oe(), v && t.translate(h.x, h.y), Z(), Te(), Ee(c, !0), ie(), xe(), ye(F !== 0 || R !== 0), Ee(c, !1), ae(), v && t.translate(-h.x, -h.y), Ie(), Ce(), r && t.translate(p.x1, p.y1);
      }
    };
    var Cu = function(e) {
      if (!["overlay", "underlay"].includes(e))
        throw new Error("Invalid state");
      return function(r, a, n, i, s) {
        var o = this;
        if (a.visible()) {
          var l = a.pstyle("".concat(e, "-padding")).pfValue, u = a.pstyle("".concat(e, "-opacity")).value, f = a.pstyle("".concat(e, "-color")).value, h = a.pstyle("".concat(e, "-shape")).value;
          if (u > 0) {
            if (n = n || a.position(), i == null || s == null) {
              var c = a.padding();
              i = a.width() + 2 * c, s = a.height() + 2 * c;
            }
            o.colorFillStyle(r, f[0], f[1], f[2], u), o.nodeShapes[h].draw(r, n.x, n.y, i + l * 2, s + l * 2), r.fill();
          }
        }
      };
    };
    Ea.drawNodeOverlay = Cu("overlay"), Ea.drawNodeUnderlay = Cu("underlay"), Ea.hasPie = function(t) {
      return t = t[0], t._private.hasPie;
    }, Ea.drawPie = function(t, e, r, a) {
      e = e[0], a = a || e.position();
      var n = e.cy().style(), i = e.pstyle("pie-size"), s = a.x, o = a.y, l = e.width(), u = e.height(), f = Math.min(l, u) / 2, h = 0, c = this.usePaths();
      c && (s = 0, o = 0), i.units === "%" ? f = f * i.pfValue : i.pfValue !== void 0 && (f = i.pfValue / 2);
      for (var v = 1; v <= n.pieBackgroundN; v++) {
        var d = e.pstyle("pie-" + v + "-background-size").value, g = e.pstyle("pie-" + v + "-background-color").value, y = e.pstyle("pie-" + v + "-background-opacity").value * r, p = d / 100;
        p + h > 1 && (p = 1 - h);
        var m = 1.5 * Math.PI + 2 * Math.PI * h, b = 2 * Math.PI * p, E = m + b;
        d === 0 || h >= 1 || h + p > 1 || (t.beginPath(), t.moveTo(s, o), t.arc(s, o, f, m, E), t.closePath(), this.colorFillStyle(t, g[0], g[1], g[2], y), t.fill(), h += p);
      }
    };
    var Wt = {}, jg = 100;
    Wt.getPixelRatio = function() {
      var t = this.data.contexts[0];
      if (this.forcedPixelRatio != null)
        return this.forcedPixelRatio;
      var e = t.backingStorePixelRatio || t.webkitBackingStorePixelRatio || t.mozBackingStorePixelRatio || t.msBackingStorePixelRatio || t.oBackingStorePixelRatio || t.backingStorePixelRatio || 1;
      return (window.devicePixelRatio || 1) / e;
    }, Wt.paintCache = function(t) {
      for (var e = this.paintCaches = this.paintCaches || [], r = !0, a, n = 0; n < e.length; n++)
        if (a = e[n], a.context === t) {
          r = !1;
          break;
        }
      return r && (a = {
        context: t
      }, e.push(a)), a;
    }, Wt.createGradientStyleFor = function(t, e, r, a, n) {
      var i, s = this.usePaths(), o = r.pstyle(e + "-gradient-stop-colors").value, l = r.pstyle(e + "-gradient-stop-positions").pfValue;
      if (a === "radial-gradient")
        if (r.isEdge()) {
          var u = r.sourceEndpoint(), f = r.targetEndpoint(), h = r.midpoint(), c = Pr(u, h), v = Pr(f, h);
          i = t.createRadialGradient(h.x, h.y, 0, h.x, h.y, Math.max(c, v));
        } else {
          var d = s ? {
            x: 0,
            y: 0
          } : r.position(), g = r.paddedWidth(), y = r.paddedHeight();
          i = t.createRadialGradient(d.x, d.y, 0, d.x, d.y, Math.max(g, y));
        }
      else if (r.isEdge()) {
        var p = r.sourceEndpoint(), m = r.targetEndpoint();
        i = t.createLinearGradient(p.x, p.y, m.x, m.y);
      } else {
        var b = s ? {
          x: 0,
          y: 0
        } : r.position(), E = r.paddedWidth(), M = r.paddedHeight(), O = E / 2, x = M / 2, I = r.pstyle("background-gradient-direction").value;
        switch (I) {
          case "to-bottom":
            i = t.createLinearGradient(b.x, b.y - x, b.x, b.y + x);
            break;
          case "to-top":
            i = t.createLinearGradient(b.x, b.y + x, b.x, b.y - x);
            break;
          case "to-left":
            i = t.createLinearGradient(b.x + O, b.y, b.x - O, b.y);
            break;
          case "to-right":
            i = t.createLinearGradient(b.x - O, b.y, b.x + O, b.y);
            break;
          case "to-bottom-right":
          case "to-right-bottom":
            i = t.createLinearGradient(b.x - O, b.y - x, b.x + O, b.y + x);
            break;
          case "to-top-right":
          case "to-right-top":
            i = t.createLinearGradient(b.x - O, b.y + x, b.x + O, b.y - x);
            break;
          case "to-bottom-left":
          case "to-left-bottom":
            i = t.createLinearGradient(b.x + O, b.y - x, b.x - O, b.y + x);
            break;
          case "to-top-left":
          case "to-left-top":
            i = t.createLinearGradient(b.x + O, b.y + x, b.x - O, b.y - x);
            break;
        }
      }
      if (!i)
        return null;
      for (var C = l.length === o.length, B = o.length, F = 0; F < B; F++)
        i.addColorStop(C ? l[F] : F / (B - 1), "rgba(" + o[F][0] + "," + o[F][1] + "," + o[F][2] + "," + n + ")");
      return i;
    }, Wt.gradientFillStyle = function(t, e, r, a) {
      var n = this.createGradientStyleFor(t, "background", e, r, a);
      if (!n)
        return null;
      t.fillStyle = n;
    }, Wt.colorFillStyle = function(t, e, r, a, n) {
      t.fillStyle = "rgba(" + e + "," + r + "," + a + "," + n + ")";
    }, Wt.eleFillStyle = function(t, e, r) {
      var a = e.pstyle("background-fill").value;
      if (a === "linear-gradient" || a === "radial-gradient")
        this.gradientFillStyle(t, e, a, r);
      else {
        var n = e.pstyle("background-color").value;
        this.colorFillStyle(t, n[0], n[1], n[2], r);
      }
    }, Wt.gradientStrokeStyle = function(t, e, r, a) {
      var n = this.createGradientStyleFor(t, "line", e, r, a);
      if (!n)
        return null;
      t.strokeStyle = n;
    }, Wt.colorStrokeStyle = function(t, e, r, a, n) {
      t.strokeStyle = "rgba(" + e + "," + r + "," + a + "," + n + ")";
    }, Wt.eleStrokeStyle = function(t, e, r) {
      var a = e.pstyle("line-fill").value;
      if (a === "linear-gradient" || a === "radial-gradient")
        this.gradientStrokeStyle(t, e, a, r);
      else {
        var n = e.pstyle("line-color").value;
        this.colorStrokeStyle(t, n[0], n[1], n[2], r);
      }
    }, Wt.matchCanvasSize = function(t) {
      var e = this, r = e.data, a = e.findContainerClientCoords(), n = a[2], i = a[3], s = e.getPixelRatio(), o = e.motionBlurPxRatio;
      (t === e.data.bufferCanvases[e.MOTIONBLUR_BUFFER_NODE] || t === e.data.bufferCanvases[e.MOTIONBLUR_BUFFER_DRAG]) && (s = o);
      var l = n * s, u = i * s, f;
      if (!(l === e.canvasWidth && u === e.canvasHeight)) {
        e.fontCaches = null;
        var h = r.canvasContainer;
        h.style.width = n + "px", h.style.height = i + "px";
        for (var c = 0; c < e.CANVAS_LAYERS; c++)
          f = r.canvases[c], f.width = l, f.height = u, f.style.width = n + "px", f.style.height = i + "px";
        for (var c = 0; c < e.BUFFER_COUNT; c++)
          f = r.bufferCanvases[c], f.width = l, f.height = u, f.style.width = n + "px", f.style.height = i + "px";
        e.textureMult = 1, s <= 1 && (f = r.bufferCanvases[e.TEXTURE_BUFFER], e.textureMult = 2, f.width = l * e.textureMult, f.height = u * e.textureMult), e.canvasWidth = l, e.canvasHeight = u;
      }
    }, Wt.renderTo = function(t, e, r, a) {
      this.render({
        forcedContext: t,
        forcedZoom: e,
        forcedPan: r,
        drawAllLayers: !0,
        forcedPxRatio: a
      });
    }, Wt.render = function(t) {
      t = t || ys();
      var e = t.forcedContext, r = t.drawAllLayers, a = t.drawOnlyNodeLayer, n = t.forcedZoom, i = t.forcedPan, s = this, o = t.forcedPxRatio === void 0 ? this.getPixelRatio() : t.forcedPxRatio, l = s.cy, u = s.data, f = u.canvasNeedsRedraw, h = s.textureOnViewport && !e && (s.pinching || s.hoverData.dragging || s.swipePanning || s.data.wheelZooming), c = t.motionBlur !== void 0 ? t.motionBlur : s.motionBlur, v = s.motionBlurPxRatio, d = l.hasCompoundNodes(), g = s.hoverData.draggingEles, y = !!(s.hoverData.selecting || s.touchData.selecting);
      c = c && !e && s.motionBlurEnabled && !y;
      var p = c;
      e || (s.prevPxRatio !== o && (s.invalidateContainerClientCoordsCache(), s.matchCanvasSize(s.container), s.redrawHint("eles", !0), s.redrawHint("drag", !0)), s.prevPxRatio = o), !e && s.motionBlurTimeout && clearTimeout(s.motionBlurTimeout), c && (s.mbFrames == null && (s.mbFrames = 0), s.mbFrames++, s.mbFrames < 3 && (p = !1), s.mbFrames > s.minMbLowQualFrames && (s.motionBlurPxRatio = s.mbPxRBlurry)), s.clearingMotionBlur && (s.motionBlurPxRatio = 1), s.textureDrawLastFrame && !h && (f[s.NODE] = !0, f[s.SELECT_BOX] = !0);
      var m = l.style(), b = l.zoom(), E = n !== void 0 ? n : b, M = l.pan(), O = {
        x: M.x,
        y: M.y
      }, x = {
        zoom: b,
        pan: {
          x: M.x,
          y: M.y
        }
      }, I = s.prevViewport, C = I === void 0 || x.zoom !== I.zoom || x.pan.x !== I.pan.x || x.pan.y !== I.pan.y;
      !C && !(g && !d) && (s.motionBlurPxRatio = 1), i && (O = i), E *= o, O.x *= o, O.y *= o;
      var B = s.getCachedZSortedEles();
      function F(Re, Me, Ve, Fe, ke) {
        var Ge = Re.globalCompositeOperation;
        Re.globalCompositeOperation = "destination-out", s.colorFillStyle(Re, 255, 255, 255, s.motionBlurTransparency), Re.fillRect(Me, Ve, Fe, ke), Re.globalCompositeOperation = Ge;
      }
      function R(Re, Me) {
        var Ve, Fe, ke, Ge;
        !s.clearingMotionBlur && (Re === u.bufferContexts[s.MOTIONBLUR_BUFFER_NODE] || Re === u.bufferContexts[s.MOTIONBLUR_BUFFER_DRAG]) ? (Ve = {
          x: M.x * v,
          y: M.y * v
        }, Fe = b * v, ke = s.canvasWidth * v, Ge = s.canvasHeight * v) : (Ve = O, Fe = E, ke = s.canvasWidth, Ge = s.canvasHeight), Re.setTransform(1, 0, 0, 1, 0, 0), Me === "motionBlur" ? F(Re, 0, 0, ke, Ge) : !e && (Me === void 0 || Me) && Re.clearRect(0, 0, ke, Ge), r || (Re.translate(Ve.x, Ve.y), Re.scale(Fe, Fe)), i && Re.translate(i.x, i.y), n && Re.scale(n, n);
      }
      if (h || (s.textureDrawLastFrame = !1), h) {
        if (s.textureDrawLastFrame = !0, !s.textureCache) {
          s.textureCache = {}, s.textureCache.bb = l.mutableElements().boundingBox(), s.textureCache.texture = s.data.bufferCanvases[s.TEXTURE_BUFFER];
          var X = s.data.bufferContexts[s.TEXTURE_BUFFER];
          X.setTransform(1, 0, 0, 1, 0, 0), X.clearRect(0, 0, s.canvasWidth * s.textureMult, s.canvasHeight * s.textureMult), s.render({
            forcedContext: X,
            drawOnlyNodeLayer: !0,
            forcedPxRatio: o * s.textureMult
          });
          var x = s.textureCache.viewport = {
            zoom: l.zoom(),
            pan: l.pan(),
            width: s.canvasWidth,
            height: s.canvasHeight
          };
          x.mpan = {
            x: (0 - x.pan.x) / x.zoom,
            y: (0 - x.pan.y) / x.zoom
          };
        }
        f[s.DRAG] = !1, f[s.NODE] = !1;
        var z = u.contexts[s.NODE], re = s.textureCache.texture, x = s.textureCache.viewport;
        z.setTransform(1, 0, 0, 1, 0, 0), c ? F(z, 0, 0, x.width, x.height) : z.clearRect(0, 0, x.width, x.height);
        var W = m.core("outside-texture-bg-color").value, Z = m.core("outside-texture-bg-opacity").value;
        s.colorFillStyle(z, W[0], W[1], W[2], Z), z.fillRect(0, 0, x.width, x.height);
        var b = l.zoom();
        R(z, !1), z.clearRect(x.mpan.x, x.mpan.y, x.width / x.zoom / o, x.height / x.zoom / o), z.drawImage(re, x.mpan.x, x.mpan.y, x.width / x.zoom / o, x.height / x.zoom / o);
      } else
        s.textureOnViewport && !e && (s.textureCache = null);
      var ie = l.extent(), oe = s.pinching || s.hoverData.dragging || s.swipePanning || s.data.wheelZooming || s.hoverData.draggingEles || s.cy.animated(), ge = s.hideEdgesOnViewport && oe, se = [];
      if (se[s.NODE] = !f[s.NODE] && c && !s.clearedForMotionBlur[s.NODE] || s.clearingMotionBlur, se[s.NODE] && (s.clearedForMotionBlur[s.NODE] = !0), se[s.DRAG] = !f[s.DRAG] && c && !s.clearedForMotionBlur[s.DRAG] || s.clearingMotionBlur, se[s.DRAG] && (s.clearedForMotionBlur[s.DRAG] = !0), f[s.NODE] || r || a || se[s.NODE]) {
        var de = c && !se[s.NODE] && v !== 1, z = e || (de ? s.data.bufferContexts[s.MOTIONBLUR_BUFFER_NODE] : u.contexts[s.NODE]), we = c && !de ? "motionBlur" : void 0;
        R(z, we), ge ? s.drawCachedNodes(z, B.nondrag, o, ie) : s.drawLayeredElements(z, B.nondrag, o, ie), s.debug && s.drawDebugPoints(z, B.nondrag), !r && !c && (f[s.NODE] = !1);
      }
      if (!a && (f[s.DRAG] || r || se[s.DRAG])) {
        var de = c && !se[s.DRAG] && v !== 1, z = e || (de ? s.data.bufferContexts[s.MOTIONBLUR_BUFFER_DRAG] : u.contexts[s.DRAG]);
        R(z, c && !de ? "motionBlur" : void 0), ge ? s.drawCachedNodes(z, B.drag, o, ie) : s.drawCachedElements(z, B.drag, o, ie), s.debug && s.drawDebugPoints(z, B.drag), !r && !c && (f[s.DRAG] = !1);
      }
      if (s.showFps || !a && f[s.SELECT_BOX] && !r) {
        var z = e || u.contexts[s.SELECT_BOX];
        if (R(z), s.selection[4] == 1 && (s.hoverData.selecting || s.touchData.selecting)) {
          var b = s.cy.zoom(), Te = m.core("selection-box-border-width").value / b;
          z.lineWidth = Te, z.fillStyle = "rgba(" + m.core("selection-box-color").value[0] + "," + m.core("selection-box-color").value[1] + "," + m.core("selection-box-color").value[2] + "," + m.core("selection-box-opacity").value + ")", z.fillRect(s.selection[0], s.selection[1], s.selection[2] - s.selection[0], s.selection[3] - s.selection[1]), Te > 0 && (z.strokeStyle = "rgba(" + m.core("selection-box-border-color").value[0] + "," + m.core("selection-box-border-color").value[1] + "," + m.core("selection-box-border-color").value[2] + "," + m.core("selection-box-opacity").value + ")", z.strokeRect(s.selection[0], s.selection[1], s.selection[2] - s.selection[0], s.selection[3] - s.selection[1]));
        }
        if (u.bgActivePosistion && !s.hoverData.selecting) {
          var b = s.cy.zoom(), Ee = u.bgActivePosistion;
          z.fillStyle = "rgba(" + m.core("active-bg-color").value[0] + "," + m.core("active-bg-color").value[1] + "," + m.core("active-bg-color").value[2] + "," + m.core("active-bg-opacity").value + ")", z.beginPath(), z.arc(Ee.x, Ee.y, m.core("active-bg-size").pfValue / b, 0, 2 * Math.PI), z.fill();
        }
        var ye = s.lastRedrawTime;
        if (s.showFps && ye) {
          ye = Math.round(ye);
          var ae = Math.round(1e3 / ye);
          z.setTransform(1, 0, 0, 1, 0, 0), z.fillStyle = "rgba(255, 0, 0, 0.75)", z.strokeStyle = "rgba(255, 0, 0, 0.75)", z.lineWidth = 1, z.fillText("1 frame = " + ye + " ms = " + ae + " fps", 0, 20);
          var xe = 60;
          z.strokeRect(0, 30, 250, 20), z.fillRect(0, 30, 250 * Math.min(ae / xe, 1), 20);
        }
        r || (f[s.SELECT_BOX] = !1);
      }
      if (c && v !== 1) {
        var Ce = u.contexts[s.NODE], Oe = s.data.bufferCanvases[s.MOTIONBLUR_BUFFER_NODE], Ie = u.contexts[s.DRAG], He = s.data.bufferCanvases[s.MOTIONBLUR_BUFFER_DRAG], qe = function(Me, Ve, Fe) {
          Me.setTransform(1, 0, 0, 1, 0, 0), Fe || !p ? Me.clearRect(0, 0, s.canvasWidth, s.canvasHeight) : F(Me, 0, 0, s.canvasWidth, s.canvasHeight);
          var ke = v;
          Me.drawImage(
            Ve,
            // img
            0,
            0,
            // sx, sy
            s.canvasWidth * ke,
            s.canvasHeight * ke,
            // sw, sh
            0,
            0,
            // x, y
            s.canvasWidth,
            s.canvasHeight
            // w, h
          );
        };
        (f[s.NODE] || se[s.NODE]) && (qe(Ce, Oe, se[s.NODE]), f[s.NODE] = !1), (f[s.DRAG] || se[s.DRAG]) && (qe(Ie, He, se[s.DRAG]), f[s.DRAG] = !1);
      }
      s.prevViewport = x, s.clearingMotionBlur && (s.clearingMotionBlur = !1, s.motionBlurCleared = !0, s.motionBlur = !0), c && (s.motionBlurTimeout = setTimeout(function() {
        s.motionBlurTimeout = null, s.clearedForMotionBlur[s.NODE] = !1, s.clearedForMotionBlur[s.DRAG] = !1, s.motionBlur = !1, s.clearingMotionBlur = !h, s.mbFrames = 0, f[s.NODE] = !0, f[s.DRAG] = !0, s.redraw();
      }, jg)), e || l.emit("render");
    };
    var Mr = {};
    Mr.drawPolygonPath = function(t, e, r, a, n, i) {
      var s = a / 2, o = n / 2;
      t.beginPath && t.beginPath(), t.moveTo(e + s * i[0], r + o * i[1]);
      for (var l = 1; l < i.length / 2; l++)
        t.lineTo(e + s * i[l * 2], r + o * i[l * 2 + 1]);
      t.closePath();
    }, Mr.drawRoundPolygonPath = function(t, e, r, a, n, i) {
      var s = a / 2, o = n / 2, l = di(a, n);
      t.beginPath && t.beginPath();
      for (var u = 0; u < i.length / 4; u++) {
        var f = void 0, h = void 0;
        u === 0 ? f = i.length - 2 : f = u * 4 - 2, h = u * 4 + 2;
        var c = e + s * i[u * 4], v = r + o * i[u * 4 + 1], d = -i[f] * i[h] - i[f + 1] * i[h + 1], g = l / Math.tan(Math.acos(d) / 2), y = c - g * i[f], p = v - g * i[f + 1], m = c + g * i[h], b = v + g * i[h + 1];
        u === 0 ? t.moveTo(y, p) : t.lineTo(y, p), t.arcTo(c, v, m, b, l);
      }
      t.closePath();
    }, Mr.drawRoundRectanglePath = function(t, e, r, a, n) {
      var i = a / 2, s = n / 2, o = Fa(a, n);
      t.beginPath && t.beginPath(), t.moveTo(e, r - s), t.arcTo(e + i, r - s, e + i, r, o), t.arcTo(e + i, r + s, e, r + s, o), t.arcTo(e - i, r + s, e - i, r, o), t.arcTo(e - i, r - s, e, r - s, o), t.lineTo(e, r - s), t.closePath();
    }, Mr.drawBottomRoundRectanglePath = function(t, e, r, a, n) {
      var i = a / 2, s = n / 2, o = Fa(a, n);
      t.beginPath && t.beginPath(), t.moveTo(e, r - s), t.lineTo(e + i, r - s), t.lineTo(e + i, r), t.arcTo(e + i, r + s, e, r + s, o), t.arcTo(e - i, r + s, e - i, r, o), t.lineTo(e - i, r - s), t.lineTo(e, r - s), t.closePath();
    }, Mr.drawCutRectanglePath = function(t, e, r, a, n) {
      var i = a / 2, s = n / 2, o = Ls();
      t.beginPath && t.beginPath(), t.moveTo(e - i + o, r - s), t.lineTo(e + i - o, r - s), t.lineTo(e + i, r - s + o), t.lineTo(e + i, r + s - o), t.lineTo(e + i - o, r + s), t.lineTo(e - i + o, r + s), t.lineTo(e - i, r + s - o), t.lineTo(e - i, r - s + o), t.closePath();
    }, Mr.drawBarrelPath = function(t, e, r, a, n) {
      var i = a / 2, s = n / 2, o = e - i, l = e + i, u = r - s, f = r + s, h = gi(a, n), c = h.widthOffset, v = h.heightOffset, d = h.ctrlPtOffsetPct * c;
      t.beginPath && t.beginPath(), t.moveTo(o, u + v), t.lineTo(o, f - v), t.quadraticCurveTo(o + d, f, o + c, f), t.lineTo(l - c, f), t.quadraticCurveTo(l - d, f, l, f - v), t.lineTo(l, u + v), t.quadraticCurveTo(l - d, u, l - c, u), t.lineTo(o + c, u), t.quadraticCurveTo(o + d, u, o, u + v), t.closePath();
    };
    for (var Du = Math.sin(0), Su = Math.cos(0), Yi = {}, Hi = {}, Lu = Math.PI / 40, wa = 0 * Math.PI; wa < 2 * Math.PI; wa += Lu)
      Yi[wa] = Math.sin(wa), Hi[wa] = Math.cos(wa);
    Mr.drawEllipsePath = function(t, e, r, a, n) {
      if (t.beginPath && t.beginPath(), t.ellipse)
        t.ellipse(e, r, a / 2, n / 2, 0, 0, 2 * Math.PI);
      else
        for (var i, s, o = a / 2, l = n / 2, u = 0 * Math.PI; u < 2 * Math.PI; u += Lu)
          i = e - o * Yi[u] * Du + o * Hi[u] * Su, s = r + l * Hi[u] * Du + l * Yi[u] * Su, u === 0 ? t.moveTo(i, s) : t.lineTo(i, s);
      t.closePath();
    };
    var tn = {};
    tn.createBuffer = function(t, e) {
      var r = document.createElement("canvas");
      return r.width = t, r.height = e, [r, r.getContext("2d")];
    }, tn.bufferCanvasImage = function(t) {
      var e = this.cy, r = e.mutableElements(), a = r.boundingBox(), n = this.findContainerClientCoords(), i = t.full ? Math.ceil(a.w) : n[2], s = t.full ? Math.ceil(a.h) : n[3], o = k(t.maxWidth) || k(t.maxHeight), l = this.getPixelRatio(), u = 1;
      if (t.scale !== void 0)
        i *= t.scale, s *= t.scale, u = t.scale;
      else if (o) {
        var f = 1 / 0, h = 1 / 0;
        k(t.maxWidth) && (f = u * t.maxWidth / i), k(t.maxHeight) && (h = u * t.maxHeight / s), u = Math.min(f, h), i *= u, s *= u;
      }
      o || (i *= l, s *= l, u *= l);
      var c = document.createElement("canvas");
      c.width = i, c.height = s, c.style.width = i + "px", c.style.height = s + "px";
      var v = c.getContext("2d");
      if (i > 0 && s > 0) {
        v.clearRect(0, 0, i, s), v.globalCompositeOperation = "source-over";
        var d = this.getCachedZSortedEles();
        if (t.full)
          v.translate(-a.x1 * u, -a.y1 * u), v.scale(u, u), this.drawElements(v, d), v.scale(1 / u, 1 / u), v.translate(a.x1 * u, a.y1 * u);
        else {
          var g = e.pan(), y = {
            x: g.x * u,
            y: g.y * u
          };
          u *= e.zoom(), v.translate(y.x, y.y), v.scale(u, u), this.drawElements(v, d), v.scale(1 / u, 1 / u), v.translate(-y.x, -y.y);
        }
        t.bg && (v.globalCompositeOperation = "destination-over", v.fillStyle = t.bg, v.rect(0, 0, i, s), v.fill());
      }
      return c;
    };
    function ep(t, e) {
      for (var r = atob(t), a = new ArrayBuffer(r.length), n = new Uint8Array(a), i = 0; i < r.length; i++)
        n[i] = r.charCodeAt(i);
      return new Blob([a], {
        type: e
      });
    }
    function Au(t) {
      var e = t.indexOf(",");
      return t.substr(e + 1);
    }
    function Ou(t, e, r) {
      var a = function() {
        return e.toDataURL(r, t.quality);
      };
      switch (t.output) {
        case "blob-promise":
          return new ia(function(n, i) {
            try {
              e.toBlob(function(s) {
                s != null ? n(s) : i(new Error("`canvas.toBlob()` sent a null value in its callback"));
              }, r, t.quality);
            } catch (s) {
              i(s);
            }
          });
        case "blob":
          return ep(Au(a()), r);
        case "base64":
          return Au(a());
        case "base64uri":
        default:
          return a();
      }
    }
    tn.png = function(t) {
      return Ou(t, this.bufferCanvasImage(t), "image/png");
    }, tn.jpg = function(t) {
      return Ou(t, this.bufferCanvasImage(t), "image/jpeg");
    };
    var Nu = {};
    Nu.nodeShapeImpl = function(t, e, r, a, n, i, s) {
      switch (t) {
        case "ellipse":
          return this.drawEllipsePath(e, r, a, n, i);
        case "polygon":
          return this.drawPolygonPath(e, r, a, n, i, s);
        case "round-polygon":
          return this.drawRoundPolygonPath(e, r, a, n, i, s);
        case "roundrectangle":
        case "round-rectangle":
          return this.drawRoundRectanglePath(e, r, a, n, i);
        case "cutrectangle":
        case "cut-rectangle":
          return this.drawCutRectanglePath(e, r, a, n, i);
        case "bottomroundrectangle":
        case "bottom-round-rectangle":
          return this.drawBottomRoundRectanglePath(e, r, a, n, i);
        case "barrel":
          return this.drawBarrelPath(e, r, a, n, i);
      }
    };
    var tp = Mu, ot = Mu.prototype;
    ot.CANVAS_LAYERS = 3, ot.SELECT_BOX = 0, ot.DRAG = 1, ot.NODE = 2, ot.BUFFER_COUNT = 3, ot.TEXTURE_BUFFER = 0, ot.MOTIONBLUR_BUFFER_NODE = 1, ot.MOTIONBLUR_BUFFER_DRAG = 2;
    function Mu(t) {
      var e = this;
      e.data = {
        canvases: new Array(ot.CANVAS_LAYERS),
        contexts: new Array(ot.CANVAS_LAYERS),
        canvasNeedsRedraw: new Array(ot.CANVAS_LAYERS),
        bufferCanvases: new Array(ot.BUFFER_COUNT),
        bufferContexts: new Array(ot.CANVAS_LAYERS)
      };
      var r = "-webkit-tap-highlight-color", a = "rgba(0,0,0,0)";
      e.data.canvasContainer = document.createElement("div");
      var n = e.data.canvasContainer.style;
      e.data.canvasContainer.style[r] = a, n.position = "relative", n.zIndex = "0", n.overflow = "hidden";
      var i = t.cy.container();
      i.appendChild(e.data.canvasContainer), i.style[r] = a;
      var s = {
        "-webkit-user-select": "none",
        "-moz-user-select": "-moz-none",
        "user-select": "none",
        "-webkit-tap-highlight-color": "rgba(0,0,0,0)",
        "outline-style": "none"
      };
      lt() && (s["-ms-touch-action"] = "none", s["touch-action"] = "none");
      for (var o = 0; o < ot.CANVAS_LAYERS; o++) {
        var l = e.data.canvases[o] = document.createElement("canvas");
        e.data.contexts[o] = l.getContext("2d"), Object.keys(s).forEach(function(ye) {
          l.style[ye] = s[ye];
        }), l.style.position = "absolute", l.setAttribute("data-id", "layer" + o), l.style.zIndex = String(ot.CANVAS_LAYERS - o), e.data.canvasContainer.appendChild(l), e.data.canvasNeedsRedraw[o] = !1;
      }
      e.data.topCanvas = e.data.canvases[0], e.data.canvases[ot.NODE].setAttribute("data-id", "layer" + ot.NODE + "-node"), e.data.canvases[ot.SELECT_BOX].setAttribute("data-id", "layer" + ot.SELECT_BOX + "-selectbox"), e.data.canvases[ot.DRAG].setAttribute("data-id", "layer" + ot.DRAG + "-drag");
      for (var o = 0; o < ot.BUFFER_COUNT; o++)
        e.data.bufferCanvases[o] = document.createElement("canvas"), e.data.bufferContexts[o] = e.data.bufferCanvases[o].getContext("2d"), e.data.bufferCanvases[o].style.position = "absolute", e.data.bufferCanvases[o].setAttribute("data-id", "buffer" + o), e.data.bufferCanvases[o].style.zIndex = String(-o - 1), e.data.bufferCanvases[o].style.visibility = "hidden";
      e.pathsEnabled = !0;
      var u = Ut(), f = function(ae) {
        return {
          x: (ae.x1 + ae.x2) / 2,
          y: (ae.y1 + ae.y2) / 2
        };
      }, h = function(ae) {
        return {
          x: -ae.w / 2,
          y: -ae.h / 2
        };
      }, c = function(ae) {
        var xe = ae[0]._private, Ce = xe.oldBackgroundTimestamp === xe.backgroundTimestamp;
        return !Ce;
      }, v = function(ae) {
        return ae[0]._private.nodeKey;
      }, d = function(ae) {
        return ae[0]._private.labelStyleKey;
      }, g = function(ae) {
        return ae[0]._private.sourceLabelStyleKey;
      }, y = function(ae) {
        return ae[0]._private.targetLabelStyleKey;
      }, p = function(ae, xe, Ce, Oe, Ie) {
        return e.drawElement(ae, xe, Ce, !1, !1, Ie);
      }, m = function(ae, xe, Ce, Oe, Ie) {
        return e.drawElementText(ae, xe, Ce, Oe, "main", Ie);
      }, b = function(ae, xe, Ce, Oe, Ie) {
        return e.drawElementText(ae, xe, Ce, Oe, "source", Ie);
      }, E = function(ae, xe, Ce, Oe, Ie) {
        return e.drawElementText(ae, xe, Ce, Oe, "target", Ie);
      }, M = function(ae) {
        return ae.boundingBox(), ae[0]._private.bodyBounds;
      }, O = function(ae) {
        return ae.boundingBox(), ae[0]._private.labelBounds.main || u;
      }, x = function(ae) {
        return ae.boundingBox(), ae[0]._private.labelBounds.source || u;
      }, I = function(ae) {
        return ae.boundingBox(), ae[0]._private.labelBounds.target || u;
      }, C = function(ae, xe) {
        return xe;
      }, B = function(ae) {
        return f(M(ae));
      }, F = function(ae, xe, Ce) {
        var Oe = ae ? ae + "-" : "";
        return {
          x: xe.x + Ce.pstyle(Oe + "text-margin-x").pfValue,
          y: xe.y + Ce.pstyle(Oe + "text-margin-y").pfValue
        };
      }, R = function(ae, xe, Ce) {
        var Oe = ae[0]._private.rscratch;
        return {
          x: Oe[xe],
          y: Oe[Ce]
        };
      }, X = function(ae) {
        return F("", R(ae, "labelX", "labelY"), ae);
      }, z = function(ae) {
        return F("source", R(ae, "sourceLabelX", "sourceLabelY"), ae);
      }, re = function(ae) {
        return F("target", R(ae, "targetLabelX", "targetLabelY"), ae);
      }, W = function(ae) {
        return h(M(ae));
      }, Z = function(ae) {
        return h(x(ae));
      }, ie = function(ae) {
        return h(I(ae));
      }, oe = function(ae) {
        var xe = O(ae), Ce = h(O(ae));
        if (ae.isNode()) {
          switch (ae.pstyle("text-halign").value) {
            case "left":
              Ce.x = -xe.w;
              break;
            case "right":
              Ce.x = 0;
              break;
          }
          switch (ae.pstyle("text-valign").value) {
            case "top":
              Ce.y = -xe.h;
              break;
            case "bottom":
              Ce.y = 0;
              break;
          }
        }
        return Ce;
      }, ge = e.data.eleTxrCache = new ja(e, {
        getKey: v,
        doesEleInvalidateKey: c,
        drawElement: p,
        getBoundingBox: M,
        getRotationPoint: B,
        getRotationOffset: W,
        allowEdgeTxrCaching: !1,
        allowParentTxrCaching: !1
      }), se = e.data.lblTxrCache = new ja(e, {
        getKey: d,
        drawElement: m,
        getBoundingBox: O,
        getRotationPoint: X,
        getRotationOffset: oe,
        isVisible: C
      }), de = e.data.slbTxrCache = new ja(e, {
        getKey: g,
        drawElement: b,
        getBoundingBox: x,
        getRotationPoint: z,
        getRotationOffset: Z,
        isVisible: C
      }), we = e.data.tlbTxrCache = new ja(e, {
        getKey: y,
        drawElement: E,
        getBoundingBox: I,
        getRotationPoint: re,
        getRotationOffset: ie,
        isVisible: C
      }), Te = e.data.lyrTxrCache = new mu(e);
      e.onUpdateEleCalcs(function(ae, xe) {
        ge.invalidateElements(xe), se.invalidateElements(xe), de.invalidateElements(xe), we.invalidateElements(xe), Te.invalidateElements(xe);
        for (var Ce = 0; Ce < xe.length; Ce++) {
          var Oe = xe[Ce]._private;
          Oe.oldBackgroundTimestamp = Oe.backgroundTimestamp;
        }
      });
      var Ee = function(ae) {
        for (var xe = 0; xe < ae.length; xe++)
          Te.enqueueElementRefinement(ae[xe].ele);
      };
      ge.onDequeue(Ee), se.onDequeue(Ee), de.onDequeue(Ee), we.onDequeue(Ee);
    }
    ot.redrawHint = function(t, e) {
      var r = this;
      switch (t) {
        case "eles":
          r.data.canvasNeedsRedraw[ot.NODE] = e;
          break;
        case "drag":
          r.data.canvasNeedsRedraw[ot.DRAG] = e;
          break;
        case "select":
          r.data.canvasNeedsRedraw[ot.SELECT_BOX] = e;
          break;
      }
    };
    var rp = typeof Path2D < "u";
    ot.path2dEnabled = function(t) {
      if (t === void 0)
        return this.pathsEnabled;
      this.pathsEnabled = !!t;
    }, ot.usePaths = function() {
      return rp && this.pathsEnabled;
    }, ot.setImgSmoothing = function(t, e) {
      t.imageSmoothingEnabled != null ? t.imageSmoothingEnabled = e : (t.webkitImageSmoothingEnabled = e, t.mozImageSmoothingEnabled = e, t.msImageSmoothingEnabled = e);
    }, ot.getImgSmoothing = function(t) {
      return t.imageSmoothingEnabled != null ? t.imageSmoothingEnabled : t.webkitImageSmoothingEnabled || t.mozImageSmoothingEnabled || t.msImageSmoothingEnabled;
    }, ot.makeOffscreenCanvas = function(t, e) {
      var r;
      return (typeof OffscreenCanvas > "u" ? "undefined" : Q(OffscreenCanvas)) !== "undefined" ? r = new OffscreenCanvas(t, e) : (r = document.createElement("canvas"), r.width = t, r.height = e), r;
    }, [Eu, hr, mr, Ui, _r, Ea, Wt, Mr, tn, Nu].forEach(function(t) {
      Ue(ot, t);
    });
    var ap = [{
      name: "null",
      impl: ru
    }, {
      name: "base",
      impl: du
    }, {
      name: "canvas",
      impl: tp
    }], np = [{
      type: "layout",
      extensions: hg
    }, {
      type: "renderer",
      extensions: ap
    }], Iu = {}, Ru = {};
    function ku(t, e, r) {
      var a = r, n = function(I) {
        ft("Can not register `" + e + "` for `" + t + "` since `" + I + "` already exists in the prototype and can not be overridden");
      };
      if (t === "core") {
        if (Za.prototype[e])
          return n(e);
        Za.prototype[e] = r;
      } else if (t === "collection") {
        if (Ot.prototype[e])
          return n(e);
        Ot.prototype[e] = r;
      } else if (t === "layout") {
        for (var i = function(I) {
          this.options = I, r.call(this, I), S(this._private) || (this._private = {}), this._private.cy = I.cy, this._private.listeners = [], this.createEmitter();
        }, s = i.prototype = Object.create(r.prototype), o = [], l = 0; l < o.length; l++) {
          var u = o[l];
          s[u] = s[u] || function() {
            return this;
          };
        }
        s.start && !s.run ? s.run = function() {
          return this.start(), this;
        } : !s.start && s.run && (s.start = function() {
          return this.run(), this;
        });
        var f = r.prototype.stop;
        s.stop = function() {
          var x = this.options;
          if (x && x.animate) {
            var I = this.animations;
            if (I)
              for (var C = 0; C < I.length; C++)
                I[C].stop();
          }
          return f ? f.call(this) : this.emit("layoutstop"), this;
        }, s.destroy || (s.destroy = function() {
          return this;
        }), s.cy = function() {
          return this._private.cy;
        };
        var h = function(I) {
          return I._private.cy;
        }, c = {
          addEventFields: function(I, C) {
            C.layout = I, C.cy = h(I), C.target = I;
          },
          bubble: function() {
            return !0;
          },
          parent: function(I) {
            return h(I);
          }
        };
        Ue(s, {
          createEmitter: function() {
            return this._private.emitter = new Mn(c, this), this;
          },
          emitter: function() {
            return this._private.emitter;
          },
          on: function(I, C) {
            return this.emitter().on(I, C), this;
          },
          one: function(I, C) {
            return this.emitter().one(I, C), this;
          },
          once: function(I, C) {
            return this.emitter().one(I, C), this;
          },
          removeListener: function(I, C) {
            return this.emitter().removeListener(I, C), this;
          },
          removeAllListeners: function() {
            return this.emitter().removeAllListeners(), this;
          },
          emit: function(I, C) {
            return this.emitter().emit(I, C), this;
          }
        }), ht.eventAliasesOn(s), a = i;
      } else if (t === "renderer" && e !== "null" && e !== "base") {
        var v = Pu("renderer", "base"), d = v.prototype, g = r, y = r.prototype, p = function() {
          v.apply(this, arguments), g.apply(this, arguments);
        }, m = p.prototype;
        for (var b in d) {
          var E = d[b], M = y[b] != null;
          if (M)
            return n(b);
          m[b] = E;
        }
        for (var O in y)
          m[O] = y[O];
        d.clientFunctions.forEach(function(x) {
          m[x] = m[x] || function() {
            xt("Renderer does not implement `renderer." + x + "()` on its prototype");
          };
        }), a = p;
      } else if (t === "__proto__" || t === "constructor" || t === "prototype")
        return xt(t + " is an illegal type to be registered, possibly lead to prototype pollutions");
      return ts({
        map: Iu,
        keys: [t, e],
        value: a
      });
    }
    function Pu(t, e) {
      return rs({
        map: Iu,
        keys: [t, e]
      });
    }
    function ip(t, e, r, a, n) {
      return ts({
        map: Ru,
        keys: [t, e, r, a],
        value: n
      });
    }
    function sp(t, e, r, a) {
      return rs({
        map: Ru,
        keys: [t, e, r, a]
      });
    }
    var Xi = function() {
      if (arguments.length === 2)
        return Pu.apply(null, arguments);
      if (arguments.length === 3)
        return ku.apply(null, arguments);
      if (arguments.length === 4)
        return sp.apply(null, arguments);
      if (arguments.length === 5)
        return ip.apply(null, arguments);
      xt("Invalid extension access syntax");
    };
    Za.prototype.extension = Xi, np.forEach(function(t) {
      t.extensions.forEach(function(e) {
        ku(t.type, e.name, e.impl);
      });
    });
    var Bu = function t() {
      if (!(this instanceof t))
        return new t();
      this.length = 0;
    }, Ur = Bu.prototype;
    Ur.instanceString = function() {
      return "stylesheet";
    }, Ur.selector = function(t) {
      var e = this.length++;
      return this[e] = {
        selector: t,
        properties: []
      }, this;
    }, Ur.css = function(t, e) {
      var r = this.length - 1;
      if (ee(t))
        this[r].properties.push({
          name: t,
          value: e
        });
      else if (S(t))
        for (var a = t, n = Object.keys(a), i = 0; i < n.length; i++) {
          var s = n[i], o = a[s];
          if (o != null) {
            var l = Ft.properties[s] || Ft.properties[pt(s)];
            if (l != null) {
              var u = l.name, f = o;
              this[r].properties.push({
                name: u,
                value: f
              });
            }
          }
        }
      return this;
    }, Ur.style = Ur.css, Ur.generateStyle = function(t) {
      var e = new Ft(t);
      return this.appendToStyle(e);
    }, Ur.appendToStyle = function(t) {
      for (var e = 0; e < this.length; e++) {
        var r = this[e], a = r.selector, n = r.properties;
        t.selector(a);
        for (var i = 0; i < n.length; i++) {
          var s = n[i];
          t.css(s.name, s.value);
        }
      }
      return t;
    };
    var op = "3.23.0", Yr = function(e) {
      if (e === void 0 && (e = {}), S(e))
        return new Za(e);
      if (ee(e))
        return Xi.apply(Xi, arguments);
    };
    return Yr.use = function(t) {
      var e = Array.prototype.slice.call(arguments, 1);
      return e.unshift(Yr), t.apply(null, e), this;
    }, Yr.warnings = function(t) {
      return gs(t);
    }, Yr.version = op, Yr.stylesheet = Yr.Stylesheet = Bu, Yr;
  });
})(Xp);
const Wu = Zi;
var Qi = {}, qp = {
  get exports() {
    return Qi;
  },
  set exports(fe) {
    Qi = fe;
  }
}, ti = {}, Wp = {
  get exports() {
    return ti;
  },
  set exports(fe) {
    ti = fe;
  }
}, ri = {}, Kp = {
  get exports() {
    return ri;
  },
  set exports(fe) {
    ri = fe;
  }
}, Vu;
function Zp() {
  return Vu || (Vu = 1, function(fe, he) {
    (function(ce, Y) {
      fe.exports = Y();
    })(Ca, function() {
      return (
        /******/
        function(Q) {
          var ce = {};
          function Y(A) {
            if (ce[A])
              return ce[A].exports;
            var T = ce[A] = {
              /******/
              i: A,
              /******/
              l: !1,
              /******/
              exports: {}
              /******/
            };
            return Q[A].call(T.exports, T, T.exports, Y), T.l = !0, T.exports;
          }
          return Y.m = Q, Y.c = ce, Y.i = function(A) {
            return A;
          }, Y.d = function(A, T, w) {
            Y.o(A, T) || Object.defineProperty(A, T, {
              /******/
              configurable: !1,
              /******/
              enumerable: !0,
              /******/
              get: w
              /******/
            });
          }, Y.n = function(A) {
            var T = A && A.__esModule ? (
              /******/
              function() {
                return A.default;
              }
            ) : (
              /******/
              function() {
                return A;
              }
            );
            return Y.d(T, "a", T), T;
          }, Y.o = function(A, T) {
            return Object.prototype.hasOwnProperty.call(A, T);
          }, Y.p = "", Y(Y.s = 26);
        }([
          /* 0 */
          /***/
          function(Q, ce, Y) {
            function A() {
            }
            A.QUALITY = 1, A.DEFAULT_CREATE_BENDS_AS_NEEDED = !1, A.DEFAULT_INCREMENTAL = !1, A.DEFAULT_ANIMATION_ON_LAYOUT = !0, A.DEFAULT_ANIMATION_DURING_LAYOUT = !1, A.DEFAULT_ANIMATION_PERIOD = 50, A.DEFAULT_UNIFORM_LEAF_NODE_SIZES = !1, A.DEFAULT_GRAPH_MARGIN = 15, A.NODE_DIMENSIONS_INCLUDE_LABELS = !1, A.SIMPLE_NODE_SIZE = 40, A.SIMPLE_NODE_HALF_SIZE = A.SIMPLE_NODE_SIZE / 2, A.EMPTY_COMPOUND_NODE_SIZE = 40, A.MIN_EDGE_LENGTH = 1, A.WORLD_BOUNDARY = 1e6, A.INITIAL_WORLD_BOUNDARY = A.WORLD_BOUNDARY / 1e3, A.WORLD_CENTER_X = 1200, A.WORLD_CENTER_Y = 900, Q.exports = A;
          },
          /* 1 */
          /***/
          function(Q, ce, Y) {
            var A = Y(2), T = Y(8), w = Y(9);
            function L(U, P, K) {
              A.call(this, K), this.isOverlapingSourceAndTarget = !1, this.vGraphObject = K, this.bendpoints = [], this.source = U, this.target = P;
            }
            L.prototype = Object.create(A.prototype);
            for (var G in A)
              L[G] = A[G];
            L.prototype.getSource = function() {
              return this.source;
            }, L.prototype.getTarget = function() {
              return this.target;
            }, L.prototype.isInterGraph = function() {
              return this.isInterGraph;
            }, L.prototype.getLength = function() {
              return this.length;
            }, L.prototype.isOverlapingSourceAndTarget = function() {
              return this.isOverlapingSourceAndTarget;
            }, L.prototype.getBendpoints = function() {
              return this.bendpoints;
            }, L.prototype.getLca = function() {
              return this.lca;
            }, L.prototype.getSourceInLca = function() {
              return this.sourceInLca;
            }, L.prototype.getTargetInLca = function() {
              return this.targetInLca;
            }, L.prototype.getOtherEnd = function(U) {
              if (this.source === U)
                return this.target;
              if (this.target === U)
                return this.source;
              throw "Node is not incident with this edge";
            }, L.prototype.getOtherEndInGraph = function(U, P) {
              for (var K = this.getOtherEnd(U), D = P.getGraphManager().getRoot(); ; ) {
                if (K.getOwner() == P)
                  return K;
                if (K.getOwner() == D)
                  break;
                K = K.getOwner().getParent();
              }
              return null;
            }, L.prototype.updateLength = function() {
              var U = new Array(4);
              this.isOverlapingSourceAndTarget = T.getIntersection(this.target.getRect(), this.source.getRect(), U), this.isOverlapingSourceAndTarget || (this.lengthX = U[0] - U[2], this.lengthY = U[1] - U[3], Math.abs(this.lengthX) < 1 && (this.lengthX = w.sign(this.lengthX)), Math.abs(this.lengthY) < 1 && (this.lengthY = w.sign(this.lengthY)), this.length = Math.sqrt(this.lengthX * this.lengthX + this.lengthY * this.lengthY));
            }, L.prototype.updateLengthSimple = function() {
              this.lengthX = this.target.getCenterX() - this.source.getCenterX(), this.lengthY = this.target.getCenterY() - this.source.getCenterY(), Math.abs(this.lengthX) < 1 && (this.lengthX = w.sign(this.lengthX)), Math.abs(this.lengthY) < 1 && (this.lengthY = w.sign(this.lengthY)), this.length = Math.sqrt(this.lengthX * this.lengthX + this.lengthY * this.lengthY);
            }, Q.exports = L;
          },
          /* 2 */
          /***/
          function(Q, ce, Y) {
            function A(T) {
              this.vGraphObject = T;
            }
            Q.exports = A;
          },
          /* 3 */
          /***/
          function(Q, ce, Y) {
            var A = Y(2), T = Y(10), w = Y(13), L = Y(0), G = Y(16), U = Y(4);
            function P(D, V, _, J) {
              _ == null && J == null && (J = V), A.call(this, J), D.graphManager != null && (D = D.graphManager), this.estimatedSize = T.MIN_VALUE, this.inclusionTreeDepth = T.MAX_VALUE, this.vGraphObject = J, this.edges = [], this.graphManager = D, _ != null && V != null ? this.rect = new w(V.x, V.y, _.width, _.height) : this.rect = new w();
            }
            P.prototype = Object.create(A.prototype);
            for (var K in A)
              P[K] = A[K];
            P.prototype.getEdges = function() {
              return this.edges;
            }, P.prototype.getChild = function() {
              return this.child;
            }, P.prototype.getOwner = function() {
              return this.owner;
            }, P.prototype.getWidth = function() {
              return this.rect.width;
            }, P.prototype.setWidth = function(D) {
              this.rect.width = D;
            }, P.prototype.getHeight = function() {
              return this.rect.height;
            }, P.prototype.setHeight = function(D) {
              this.rect.height = D;
            }, P.prototype.getCenterX = function() {
              return this.rect.x + this.rect.width / 2;
            }, P.prototype.getCenterY = function() {
              return this.rect.y + this.rect.height / 2;
            }, P.prototype.getCenter = function() {
              return new U(this.rect.x + this.rect.width / 2, this.rect.y + this.rect.height / 2);
            }, P.prototype.getLocation = function() {
              return new U(this.rect.x, this.rect.y);
            }, P.prototype.getRect = function() {
              return this.rect;
            }, P.prototype.getDiagonal = function() {
              return Math.sqrt(this.rect.width * this.rect.width + this.rect.height * this.rect.height);
            }, P.prototype.getHalfTheDiagonal = function() {
              return Math.sqrt(this.rect.height * this.rect.height + this.rect.width * this.rect.width) / 2;
            }, P.prototype.setRect = function(D, V) {
              this.rect.x = D.x, this.rect.y = D.y, this.rect.width = V.width, this.rect.height = V.height;
            }, P.prototype.setCenter = function(D, V) {
              this.rect.x = D - this.rect.width / 2, this.rect.y = V - this.rect.height / 2;
            }, P.prototype.setLocation = function(D, V) {
              this.rect.x = D, this.rect.y = V;
            }, P.prototype.moveBy = function(D, V) {
              this.rect.x += D, this.rect.y += V;
            }, P.prototype.getEdgeListToNode = function(D) {
              var V = [], _ = this;
              return _.edges.forEach(function(J) {
                if (J.target == D) {
                  if (J.source != _)
                    throw "Incorrect edge source!";
                  V.push(J);
                }
              }), V;
            }, P.prototype.getEdgesBetween = function(D) {
              var V = [], _ = this;
              return _.edges.forEach(function(J) {
                if (!(J.source == _ || J.target == _))
                  throw "Incorrect edge source and/or target";
                (J.target == D || J.source == D) && V.push(J);
              }), V;
            }, P.prototype.getNeighborsList = function() {
              var D = /* @__PURE__ */ new Set(), V = this;
              return V.edges.forEach(function(_) {
                if (_.source == V)
                  D.add(_.target);
                else {
                  if (_.target != V)
                    throw "Incorrect incidency!";
                  D.add(_.source);
                }
              }), D;
            }, P.prototype.withChildren = function() {
              var D = /* @__PURE__ */ new Set(), V, _;
              if (D.add(this), this.child != null)
                for (var J = this.child.getNodes(), ne = 0; ne < J.length; ne++)
                  V = J[ne], _ = V.withChildren(), _.forEach(function(ue) {
                    D.add(ue);
                  });
              return D;
            }, P.prototype.getNoOfChildren = function() {
              var D = 0, V;
              if (this.child == null)
                D = 1;
              else
                for (var _ = this.child.getNodes(), J = 0; J < _.length; J++)
                  V = _[J], D += V.getNoOfChildren();
              return D == 0 && (D = 1), D;
            }, P.prototype.getEstimatedSize = function() {
              if (this.estimatedSize == T.MIN_VALUE)
                throw "assert failed";
              return this.estimatedSize;
            }, P.prototype.calcEstimatedSize = function() {
              return this.child == null ? this.estimatedSize = (this.rect.width + this.rect.height) / 2 : (this.estimatedSize = this.child.calcEstimatedSize(), this.rect.width = this.estimatedSize, this.rect.height = this.estimatedSize, this.estimatedSize);
            }, P.prototype.scatter = function() {
              var D, V, _ = -L.INITIAL_WORLD_BOUNDARY, J = L.INITIAL_WORLD_BOUNDARY;
              D = L.WORLD_CENTER_X + G.nextDouble() * (J - _) + _;
              var ne = -L.INITIAL_WORLD_BOUNDARY, ue = L.INITIAL_WORLD_BOUNDARY;
              V = L.WORLD_CENTER_Y + G.nextDouble() * (ue - ne) + ne, this.rect.x = D, this.rect.y = V;
            }, P.prototype.updateBounds = function() {
              if (this.getChild() == null)
                throw "assert failed";
              if (this.getChild().getNodes().length != 0) {
                var D = this.getChild();
                if (D.updateBounds(!0), this.rect.x = D.getLeft(), this.rect.y = D.getTop(), this.setWidth(D.getRight() - D.getLeft()), this.setHeight(D.getBottom() - D.getTop()), L.NODE_DIMENSIONS_INCLUDE_LABELS) {
                  var V = D.getRight() - D.getLeft(), _ = D.getBottom() - D.getTop();
                  this.labelWidth > V && (this.rect.x -= (this.labelWidth - V) / 2, this.setWidth(this.labelWidth)), this.labelHeight > _ && (this.labelPos == "center" ? this.rect.y -= (this.labelHeight - _) / 2 : this.labelPos == "top" && (this.rect.y -= this.labelHeight - _), this.setHeight(this.labelHeight));
                }
              }
            }, P.prototype.getInclusionTreeDepth = function() {
              if (this.inclusionTreeDepth == T.MAX_VALUE)
                throw "assert failed";
              return this.inclusionTreeDepth;
            }, P.prototype.transform = function(D) {
              var V = this.rect.x;
              V > L.WORLD_BOUNDARY ? V = L.WORLD_BOUNDARY : V < -L.WORLD_BOUNDARY && (V = -L.WORLD_BOUNDARY);
              var _ = this.rect.y;
              _ > L.WORLD_BOUNDARY ? _ = L.WORLD_BOUNDARY : _ < -L.WORLD_BOUNDARY && (_ = -L.WORLD_BOUNDARY);
              var J = new U(V, _), ne = D.inverseTransformPoint(J);
              this.setLocation(ne.x, ne.y);
            }, P.prototype.getLeft = function() {
              return this.rect.x;
            }, P.prototype.getRight = function() {
              return this.rect.x + this.rect.width;
            }, P.prototype.getTop = function() {
              return this.rect.y;
            }, P.prototype.getBottom = function() {
              return this.rect.y + this.rect.height;
            }, P.prototype.getParent = function() {
              return this.owner == null ? null : this.owner.getParent();
            }, Q.exports = P;
          },
          /* 4 */
          /***/
          function(Q, ce, Y) {
            function A(T, w) {
              T == null && w == null ? (this.x = 0, this.y = 0) : (this.x = T, this.y = w);
            }
            A.prototype.getX = function() {
              return this.x;
            }, A.prototype.getY = function() {
              return this.y;
            }, A.prototype.setX = function(T) {
              this.x = T;
            }, A.prototype.setY = function(T) {
              this.y = T;
            }, A.prototype.getDifference = function(T) {
              return new DimensionD(this.x - T.x, this.y - T.y);
            }, A.prototype.getCopy = function() {
              return new A(this.x, this.y);
            }, A.prototype.translate = function(T) {
              return this.x += T.width, this.y += T.height, this;
            }, Q.exports = A;
          },
          /* 5 */
          /***/
          function(Q, ce, Y) {
            var A = Y(2), T = Y(10), w = Y(0), L = Y(6), G = Y(3), U = Y(1), P = Y(13), K = Y(12), D = Y(11);
            function V(J, ne, ue) {
              A.call(this, ue), this.estimatedSize = T.MIN_VALUE, this.margin = w.DEFAULT_GRAPH_MARGIN, this.edges = [], this.nodes = [], this.isConnected = !1, this.parent = J, ne != null && ne instanceof L ? this.graphManager = ne : ne != null && ne instanceof Layout && (this.graphManager = ne.graphManager);
            }
            V.prototype = Object.create(A.prototype);
            for (var _ in A)
              V[_] = A[_];
            V.prototype.getNodes = function() {
              return this.nodes;
            }, V.prototype.getEdges = function() {
              return this.edges;
            }, V.prototype.getGraphManager = function() {
              return this.graphManager;
            }, V.prototype.getParent = function() {
              return this.parent;
            }, V.prototype.getLeft = function() {
              return this.left;
            }, V.prototype.getRight = function() {
              return this.right;
            }, V.prototype.getTop = function() {
              return this.top;
            }, V.prototype.getBottom = function() {
              return this.bottom;
            }, V.prototype.isConnected = function() {
              return this.isConnected;
            }, V.prototype.add = function(J, ne, ue) {
              if (ne == null && ue == null) {
                var j = J;
                if (this.graphManager == null)
                  throw "Graph has no graph mgr!";
                if (this.getNodes().indexOf(j) > -1)
                  throw "Node already in graph!";
                return j.owner = this, this.getNodes().push(j), j;
              } else {
                var ee = J;
                if (!(this.getNodes().indexOf(ne) > -1 && this.getNodes().indexOf(ue) > -1))
                  throw "Source or target not in graph!";
                if (!(ne.owner == ue.owner && ne.owner == this))
                  throw "Both owners must be this graph!";
                return ne.owner != ue.owner ? null : (ee.source = ne, ee.target = ue, ee.isInterGraph = !1, this.getEdges().push(ee), ne.edges.push(ee), ue != ne && ue.edges.push(ee), ee);
              }
            }, V.prototype.remove = function(J) {
              var ne = J;
              if (J instanceof G) {
                if (ne == null)
                  throw "Node is null!";
                if (!(ne.owner != null && ne.owner == this))
                  throw "Owner graph is invalid!";
                if (this.graphManager == null)
                  throw "Owner graph manager is invalid!";
                for (var ue = ne.edges.slice(), j, ee = ue.length, H = 0; H < ee; H++)
                  j = ue[H], j.isInterGraph ? this.graphManager.remove(j) : j.source.owner.remove(j);
                var te = this.nodes.indexOf(ne);
                if (te == -1)
                  throw "Node not in owner node list!";
                this.nodes.splice(te, 1);
              } else if (J instanceof U) {
                var j = J;
                if (j == null)
                  throw "Edge is null!";
                if (!(j.source != null && j.target != null))
                  throw "Source and/or target is null!";
                if (!(j.source.owner != null && j.target.owner != null && j.source.owner == this && j.target.owner == this))
                  throw "Source and/or target owner is invalid!";
                var S = j.source.edges.indexOf(j), $ = j.target.edges.indexOf(j);
                if (!(S > -1 && $ > -1))
                  throw "Source and/or target doesn't know this edge!";
                j.source.edges.splice(S, 1), j.target != j.source && j.target.edges.splice($, 1);
                var te = j.source.owner.getEdges().indexOf(j);
                if (te == -1)
                  throw "Not in owner's edge list!";
                j.source.owner.getEdges().splice(te, 1);
              }
            }, V.prototype.updateLeftTop = function() {
              for (var J = T.MAX_VALUE, ne = T.MAX_VALUE, ue, j, ee, H = this.getNodes(), te = H.length, S = 0; S < te; S++) {
                var $ = H[S];
                ue = $.getTop(), j = $.getLeft(), J > ue && (J = ue), ne > j && (ne = j);
              }
              return J == T.MAX_VALUE ? null : (H[0].getParent().paddingLeft != null ? ee = H[0].getParent().paddingLeft : ee = this.margin, this.left = ne - ee, this.top = J - ee, new K(this.left, this.top));
            }, V.prototype.updateBounds = function(J) {
              for (var ne = T.MAX_VALUE, ue = -T.MAX_VALUE, j = T.MAX_VALUE, ee = -T.MAX_VALUE, H, te, S, $, k, q = this.nodes, ve = q.length, pe = 0; pe < ve; pe++) {
                var Ae = q[pe];
                J && Ae.child != null && Ae.updateBounds(), H = Ae.getLeft(), te = Ae.getRight(), S = Ae.getTop(), $ = Ae.getBottom(), ne > H && (ne = H), ue < te && (ue = te), j > S && (j = S), ee < $ && (ee = $);
              }
              var Ne = new P(ne, j, ue - ne, ee - j);
              ne == T.MAX_VALUE && (this.left = this.parent.getLeft(), this.right = this.parent.getRight(), this.top = this.parent.getTop(), this.bottom = this.parent.getBottom()), q[0].getParent().paddingLeft != null ? k = q[0].getParent().paddingLeft : k = this.margin, this.left = Ne.x - k, this.right = Ne.x + Ne.width + k, this.top = Ne.y - k, this.bottom = Ne.y + Ne.height + k;
            }, V.calculateBounds = function(J) {
              for (var ne = T.MAX_VALUE, ue = -T.MAX_VALUE, j = T.MAX_VALUE, ee = -T.MAX_VALUE, H, te, S, $, k = J.length, q = 0; q < k; q++) {
                var ve = J[q];
                H = ve.getLeft(), te = ve.getRight(), S = ve.getTop(), $ = ve.getBottom(), ne > H && (ne = H), ue < te && (ue = te), j > S && (j = S), ee < $ && (ee = $);
              }
              var pe = new P(ne, j, ue - ne, ee - j);
              return pe;
            }, V.prototype.getInclusionTreeDepth = function() {
              return this == this.graphManager.getRoot() ? 1 : this.parent.getInclusionTreeDepth();
            }, V.prototype.getEstimatedSize = function() {
              if (this.estimatedSize == T.MIN_VALUE)
                throw "assert failed";
              return this.estimatedSize;
            }, V.prototype.calcEstimatedSize = function() {
              for (var J = 0, ne = this.nodes, ue = ne.length, j = 0; j < ue; j++) {
                var ee = ne[j];
                J += ee.calcEstimatedSize();
              }
              return J == 0 ? this.estimatedSize = w.EMPTY_COMPOUND_NODE_SIZE : this.estimatedSize = J / Math.sqrt(this.nodes.length), this.estimatedSize;
            }, V.prototype.updateConnected = function() {
              var J = this;
              if (this.nodes.length == 0) {
                this.isConnected = !0;
                return;
              }
              var ne = new D(), ue = /* @__PURE__ */ new Set(), j = this.nodes[0], ee, H, te = j.withChildren();
              for (te.forEach(function(pe) {
                ne.push(pe), ue.add(pe);
              }); ne.length !== 0; ) {
                j = ne.shift(), ee = j.getEdges();
                for (var S = ee.length, $ = 0; $ < S; $++) {
                  var k = ee[$];
                  if (H = k.getOtherEndInGraph(j, this), H != null && !ue.has(H)) {
                    var q = H.withChildren();
                    q.forEach(function(pe) {
                      ne.push(pe), ue.add(pe);
                    });
                  }
                }
              }
              if (this.isConnected = !1, ue.size >= this.nodes.length) {
                var ve = 0;
                ue.forEach(function(pe) {
                  pe.owner == J && ve++;
                }), ve == this.nodes.length && (this.isConnected = !0);
              }
            }, Q.exports = V;
          },
          /* 6 */
          /***/
          function(Q, ce, Y) {
            var A, T = Y(1);
            function w(L) {
              A = Y(5), this.layout = L, this.graphs = [], this.edges = [];
            }
            w.prototype.addRoot = function() {
              var L = this.layout.newGraph(), G = this.layout.newNode(null), U = this.add(L, G);
              return this.setRootGraph(U), this.rootGraph;
            }, w.prototype.add = function(L, G, U, P, K) {
              if (U == null && P == null && K == null) {
                if (L == null)
                  throw "Graph is null!";
                if (G == null)
                  throw "Parent node is null!";
                if (this.graphs.indexOf(L) > -1)
                  throw "Graph already in this graph mgr!";
                if (this.graphs.push(L), L.parent != null)
                  throw "Already has a parent!";
                if (G.child != null)
                  throw "Already has a child!";
                return L.parent = G, G.child = L, L;
              } else {
                K = U, P = G, U = L;
                var D = P.getOwner(), V = K.getOwner();
                if (!(D != null && D.getGraphManager() == this))
                  throw "Source not in this graph mgr!";
                if (!(V != null && V.getGraphManager() == this))
                  throw "Target not in this graph mgr!";
                if (D == V)
                  return U.isInterGraph = !1, D.add(U, P, K);
                if (U.isInterGraph = !0, U.source = P, U.target = K, this.edges.indexOf(U) > -1)
                  throw "Edge already in inter-graph edge list!";
                if (this.edges.push(U), !(U.source != null && U.target != null))
                  throw "Edge source and/or target is null!";
                if (!(U.source.edges.indexOf(U) == -1 && U.target.edges.indexOf(U) == -1))
                  throw "Edge already in source and/or target incidency list!";
                return U.source.edges.push(U), U.target.edges.push(U), U;
              }
            }, w.prototype.remove = function(L) {
              if (L instanceof A) {
                var G = L;
                if (G.getGraphManager() != this)
                  throw "Graph not in this graph mgr";
                if (!(G == this.rootGraph || G.parent != null && G.parent.graphManager == this))
                  throw "Invalid parent node!";
                var U = [];
                U = U.concat(G.getEdges());
                for (var P, K = U.length, D = 0; D < K; D++)
                  P = U[D], G.remove(P);
                var V = [];
                V = V.concat(G.getNodes());
                var _;
                K = V.length;
                for (var D = 0; D < K; D++)
                  _ = V[D], G.remove(_);
                G == this.rootGraph && this.setRootGraph(null);
                var J = this.graphs.indexOf(G);
                this.graphs.splice(J, 1), G.parent = null;
              } else if (L instanceof T) {
                if (P = L, P == null)
                  throw "Edge is null!";
                if (!P.isInterGraph)
                  throw "Not an inter-graph edge!";
                if (!(P.source != null && P.target != null))
                  throw "Source and/or target is null!";
                if (!(P.source.edges.indexOf(P) != -1 && P.target.edges.indexOf(P) != -1))
                  throw "Source and/or target doesn't know this edge!";
                var J = P.source.edges.indexOf(P);
                if (P.source.edges.splice(J, 1), J = P.target.edges.indexOf(P), P.target.edges.splice(J, 1), !(P.source.owner != null && P.source.owner.getGraphManager() != null))
                  throw "Edge owner graph or owner graph manager is null!";
                if (P.source.owner.getGraphManager().edges.indexOf(P) == -1)
                  throw "Not in owner graph manager's edge list!";
                var J = P.source.owner.getGraphManager().edges.indexOf(P);
                P.source.owner.getGraphManager().edges.splice(J, 1);
              }
            }, w.prototype.updateBounds = function() {
              this.rootGraph.updateBounds(!0);
            }, w.prototype.getGraphs = function() {
              return this.graphs;
            }, w.prototype.getAllNodes = function() {
              if (this.allNodes == null) {
                for (var L = [], G = this.getGraphs(), U = G.length, P = 0; P < U; P++)
                  L = L.concat(G[P].getNodes());
                this.allNodes = L;
              }
              return this.allNodes;
            }, w.prototype.resetAllNodes = function() {
              this.allNodes = null;
            }, w.prototype.resetAllEdges = function() {
              this.allEdges = null;
            }, w.prototype.resetAllNodesToApplyGravitation = function() {
              this.allNodesToApplyGravitation = null;
            }, w.prototype.getAllEdges = function() {
              if (this.allEdges == null) {
                var L = [], G = this.getGraphs();
                G.length;
                for (var U = 0; U < G.length; U++)
                  L = L.concat(G[U].getEdges());
                L = L.concat(this.edges), this.allEdges = L;
              }
              return this.allEdges;
            }, w.prototype.getAllNodesToApplyGravitation = function() {
              return this.allNodesToApplyGravitation;
            }, w.prototype.setAllNodesToApplyGravitation = function(L) {
              if (this.allNodesToApplyGravitation != null)
                throw "assert failed";
              this.allNodesToApplyGravitation = L;
            }, w.prototype.getRoot = function() {
              return this.rootGraph;
            }, w.prototype.setRootGraph = function(L) {
              if (L.getGraphManager() != this)
                throw "Root not in this graph mgr!";
              this.rootGraph = L, L.parent == null && (L.parent = this.layout.newNode("Root node"));
            }, w.prototype.getLayout = function() {
              return this.layout;
            }, w.prototype.isOneAncestorOfOther = function(L, G) {
              if (!(L != null && G != null))
                throw "assert failed";
              if (L == G)
                return !0;
              var U = L.getOwner(), P;
              do {
                if (P = U.getParent(), P == null)
                  break;
                if (P == G)
                  return !0;
                if (U = P.getOwner(), U == null)
                  break;
              } while (!0);
              U = G.getOwner();
              do {
                if (P = U.getParent(), P == null)
                  break;
                if (P == L)
                  return !0;
                if (U = P.getOwner(), U == null)
                  break;
              } while (!0);
              return !1;
            }, w.prototype.calcLowestCommonAncestors = function() {
              for (var L, G, U, P, K, D = this.getAllEdges(), V = D.length, _ = 0; _ < V; _++) {
                if (L = D[_], G = L.source, U = L.target, L.lca = null, L.sourceInLca = G, L.targetInLca = U, G == U) {
                  L.lca = G.getOwner();
                  continue;
                }
                for (P = G.getOwner(); L.lca == null; ) {
                  for (L.targetInLca = U, K = U.getOwner(); L.lca == null; ) {
                    if (K == P) {
                      L.lca = K;
                      break;
                    }
                    if (K == this.rootGraph)
                      break;
                    if (L.lca != null)
                      throw "assert failed";
                    L.targetInLca = K.getParent(), K = L.targetInLca.getOwner();
                  }
                  if (P == this.rootGraph)
                    break;
                  L.lca == null && (L.sourceInLca = P.getParent(), P = L.sourceInLca.getOwner());
                }
                if (L.lca == null)
                  throw "assert failed";
              }
            }, w.prototype.calcLowestCommonAncestor = function(L, G) {
              if (L == G)
                return L.getOwner();
              var U = L.getOwner();
              do {
                if (U == null)
                  break;
                var P = G.getOwner();
                do {
                  if (P == null)
                    break;
                  if (P == U)
                    return P;
                  P = P.getParent().getOwner();
                } while (!0);
                U = U.getParent().getOwner();
              } while (!0);
              return U;
            }, w.prototype.calcInclusionTreeDepths = function(L, G) {
              L == null && G == null && (L = this.rootGraph, G = 1);
              for (var U, P = L.getNodes(), K = P.length, D = 0; D < K; D++)
                U = P[D], U.inclusionTreeDepth = G, U.child != null && this.calcInclusionTreeDepths(U.child, G + 1);
            }, w.prototype.includesInvalidEdge = function() {
              for (var L, G = this.edges.length, U = 0; U < G; U++)
                if (L = this.edges[U], this.isOneAncestorOfOther(L.source, L.target))
                  return !0;
              return !1;
            }, Q.exports = w;
          },
          /* 7 */
          /***/
          function(Q, ce, Y) {
            var A = Y(0);
            function T() {
            }
            for (var w in A)
              T[w] = A[w];
            T.MAX_ITERATIONS = 2500, T.DEFAULT_EDGE_LENGTH = 50, T.DEFAULT_SPRING_STRENGTH = 0.45, T.DEFAULT_REPULSION_STRENGTH = 4500, T.DEFAULT_GRAVITY_STRENGTH = 0.4, T.DEFAULT_COMPOUND_GRAVITY_STRENGTH = 1, T.DEFAULT_GRAVITY_RANGE_FACTOR = 3.8, T.DEFAULT_COMPOUND_GRAVITY_RANGE_FACTOR = 1.5, T.DEFAULT_USE_SMART_IDEAL_EDGE_LENGTH_CALCULATION = !0, T.DEFAULT_USE_SMART_REPULSION_RANGE_CALCULATION = !0, T.DEFAULT_COOLING_FACTOR_INCREMENTAL = 0.3, T.COOLING_ADAPTATION_FACTOR = 0.33, T.ADAPTATION_LOWER_NODE_LIMIT = 1e3, T.ADAPTATION_UPPER_NODE_LIMIT = 5e3, T.MAX_NODE_DISPLACEMENT_INCREMENTAL = 100, T.MAX_NODE_DISPLACEMENT = T.MAX_NODE_DISPLACEMENT_INCREMENTAL * 3, T.MIN_REPULSION_DIST = T.DEFAULT_EDGE_LENGTH / 10, T.CONVERGENCE_CHECK_PERIOD = 100, T.PER_LEVEL_IDEAL_EDGE_LENGTH_FACTOR = 0.1, T.MIN_EDGE_LENGTH = 1, T.GRID_CALCULATION_CHECK_PERIOD = 10, Q.exports = T;
          },
          /* 8 */
          /***/
          function(Q, ce, Y) {
            var A = Y(12);
            function T() {
            }
            T.calcSeparationAmount = function(w, L, G, U) {
              if (!w.intersects(L))
                throw "assert failed";
              var P = new Array(2);
              this.decideDirectionsForOverlappingNodes(w, L, P), G[0] = Math.min(w.getRight(), L.getRight()) - Math.max(w.x, L.x), G[1] = Math.min(w.getBottom(), L.getBottom()) - Math.max(w.y, L.y), w.getX() <= L.getX() && w.getRight() >= L.getRight() ? G[0] += Math.min(L.getX() - w.getX(), w.getRight() - L.getRight()) : L.getX() <= w.getX() && L.getRight() >= w.getRight() && (G[0] += Math.min(w.getX() - L.getX(), L.getRight() - w.getRight())), w.getY() <= L.getY() && w.getBottom() >= L.getBottom() ? G[1] += Math.min(L.getY() - w.getY(), w.getBottom() - L.getBottom()) : L.getY() <= w.getY() && L.getBottom() >= w.getBottom() && (G[1] += Math.min(w.getY() - L.getY(), L.getBottom() - w.getBottom()));
              var K = Math.abs((L.getCenterY() - w.getCenterY()) / (L.getCenterX() - w.getCenterX()));
              L.getCenterY() === w.getCenterY() && L.getCenterX() === w.getCenterX() && (K = 1);
              var D = K * G[0], V = G[1] / K;
              G[0] < V ? V = G[0] : D = G[1], G[0] = -1 * P[0] * (V / 2 + U), G[1] = -1 * P[1] * (D / 2 + U);
            }, T.decideDirectionsForOverlappingNodes = function(w, L, G) {
              w.getCenterX() < L.getCenterX() ? G[0] = -1 : G[0] = 1, w.getCenterY() < L.getCenterY() ? G[1] = -1 : G[1] = 1;
            }, T.getIntersection2 = function(w, L, G) {
              var U = w.getCenterX(), P = w.getCenterY(), K = L.getCenterX(), D = L.getCenterY();
              if (w.intersects(L))
                return G[0] = U, G[1] = P, G[2] = K, G[3] = D, !0;
              var V = w.getX(), _ = w.getY(), J = w.getRight(), ne = w.getX(), ue = w.getBottom(), j = w.getRight(), ee = w.getWidthHalf(), H = w.getHeightHalf(), te = L.getX(), S = L.getY(), $ = L.getRight(), k = L.getX(), q = L.getBottom(), ve = L.getRight(), pe = L.getWidthHalf(), Ae = L.getHeightHalf(), Ne = !1, _e = !1;
              if (U === K) {
                if (P > D)
                  return G[0] = U, G[1] = _, G[2] = K, G[3] = q, !1;
                if (P < D)
                  return G[0] = U, G[1] = ue, G[2] = K, G[3] = S, !1;
              } else if (P === D) {
                if (U > K)
                  return G[0] = V, G[1] = P, G[2] = $, G[3] = D, !1;
                if (U < K)
                  return G[0] = J, G[1] = P, G[2] = te, G[3] = D, !1;
              } else {
                var tt = w.height / w.width, ct = L.height / L.width, Pe = (D - P) / (K - U), $e = void 0, Xe = void 0, rt = void 0, lt = void 0, nt = void 0, je = void 0;
                if (-tt === Pe ? U > K ? (G[0] = ne, G[1] = ue, Ne = !0) : (G[0] = J, G[1] = _, Ne = !0) : tt === Pe && (U > K ? (G[0] = V, G[1] = _, Ne = !0) : (G[0] = j, G[1] = ue, Ne = !0)), -ct === Pe ? K > U ? (G[2] = k, G[3] = q, _e = !0) : (G[2] = $, G[3] = S, _e = !0) : ct === Pe && (K > U ? (G[2] = te, G[3] = S, _e = !0) : (G[2] = ve, G[3] = q, _e = !0)), Ne && _e)
                  return !1;
                if (U > K ? P > D ? ($e = this.getCardinalDirection(tt, Pe, 4), Xe = this.getCardinalDirection(ct, Pe, 2)) : ($e = this.getCardinalDirection(-tt, Pe, 3), Xe = this.getCardinalDirection(-ct, Pe, 1)) : P > D ? ($e = this.getCardinalDirection(-tt, Pe, 1), Xe = this.getCardinalDirection(-ct, Pe, 3)) : ($e = this.getCardinalDirection(tt, Pe, 2), Xe = this.getCardinalDirection(ct, Pe, 4)), !Ne)
                  switch ($e) {
                    case 1:
                      lt = _, rt = U + -H / Pe, G[0] = rt, G[1] = lt;
                      break;
                    case 2:
                      rt = j, lt = P + ee * Pe, G[0] = rt, G[1] = lt;
                      break;
                    case 3:
                      lt = ue, rt = U + H / Pe, G[0] = rt, G[1] = lt;
                      break;
                    case 4:
                      rt = ne, lt = P + -ee * Pe, G[0] = rt, G[1] = lt;
                      break;
                  }
                if (!_e)
                  switch (Xe) {
                    case 1:
                      je = S, nt = K + -Ae / Pe, G[2] = nt, G[3] = je;
                      break;
                    case 2:
                      nt = ve, je = D + pe * Pe, G[2] = nt, G[3] = je;
                      break;
                    case 3:
                      je = q, nt = K + Ae / Pe, G[2] = nt, G[3] = je;
                      break;
                    case 4:
                      nt = k, je = D + -pe * Pe, G[2] = nt, G[3] = je;
                      break;
                  }
              }
              return !1;
            }, T.getCardinalDirection = function(w, L, G) {
              return w > L ? G : 1 + G % 4;
            }, T.getIntersection = function(w, L, G, U) {
              if (U == null)
                return this.getIntersection2(w, L, G);
              var P = w.x, K = w.y, D = L.x, V = L.y, _ = G.x, J = G.y, ne = U.x, ue = U.y, j = void 0, ee = void 0, H = void 0, te = void 0, S = void 0, $ = void 0, k = void 0, q = void 0, ve = void 0;
              return H = V - K, S = P - D, k = D * K - P * V, te = ue - J, $ = _ - ne, q = ne * J - _ * ue, ve = H * $ - te * S, ve === 0 ? null : (j = (S * q - $ * k) / ve, ee = (te * k - H * q) / ve, new A(j, ee));
            }, T.angleOfVector = function(w, L, G, U) {
              var P = void 0;
              return w !== G ? (P = Math.atan((U - L) / (G - w)), G < w ? P += Math.PI : U < L && (P += this.TWO_PI)) : U < L ? P = this.ONE_AND_HALF_PI : P = this.HALF_PI, P;
            }, T.doIntersect = function(w, L, G, U) {
              var P = w.x, K = w.y, D = L.x, V = L.y, _ = G.x, J = G.y, ne = U.x, ue = U.y, j = (D - P) * (ue - J) - (ne - _) * (V - K);
              if (j === 0)
                return !1;
              var ee = ((ue - J) * (ne - P) + (_ - ne) * (ue - K)) / j, H = ((K - V) * (ne - P) + (D - P) * (ue - K)) / j;
              return 0 < ee && ee < 1 && 0 < H && H < 1;
            }, T.HALF_PI = 0.5 * Math.PI, T.ONE_AND_HALF_PI = 1.5 * Math.PI, T.TWO_PI = 2 * Math.PI, T.THREE_PI = 3 * Math.PI, Q.exports = T;
          },
          /* 9 */
          /***/
          function(Q, ce, Y) {
            function A() {
            }
            A.sign = function(T) {
              return T > 0 ? 1 : T < 0 ? -1 : 0;
            }, A.floor = function(T) {
              return T < 0 ? Math.ceil(T) : Math.floor(T);
            }, A.ceil = function(T) {
              return T < 0 ? Math.floor(T) : Math.ceil(T);
            }, Q.exports = A;
          },
          /* 10 */
          /***/
          function(Q, ce, Y) {
            function A() {
            }
            A.MAX_VALUE = 2147483647, A.MIN_VALUE = -2147483648, Q.exports = A;
          },
          /* 11 */
          /***/
          function(Q, ce, Y) {
            var A = function() {
              function P(K, D) {
                for (var V = 0; V < D.length; V++) {
                  var _ = D[V];
                  _.enumerable = _.enumerable || !1, _.configurable = !0, "value" in _ && (_.writable = !0), Object.defineProperty(K, _.key, _);
                }
              }
              return function(K, D, V) {
                return D && P(K.prototype, D), V && P(K, V), K;
              };
            }();
            function T(P, K) {
              if (!(P instanceof K))
                throw new TypeError("Cannot call a class as a function");
            }
            var w = function(K) {
              return { value: K, next: null, prev: null };
            }, L = function(K, D, V, _) {
              return K !== null ? K.next = D : _.head = D, V !== null ? V.prev = D : _.tail = D, D.prev = K, D.next = V, _.length++, D;
            }, G = function(K, D) {
              var V = K.prev, _ = K.next;
              return V !== null ? V.next = _ : D.head = _, _ !== null ? _.prev = V : D.tail = V, K.prev = K.next = null, D.length--, K;
            }, U = function() {
              function P(K) {
                var D = this;
                T(this, P), this.length = 0, this.head = null, this.tail = null, K != null && K.forEach(function(V) {
                  return D.push(V);
                });
              }
              return A(P, [{
                key: "size",
                value: function() {
                  return this.length;
                }
              }, {
                key: "insertBefore",
                value: function(D, V) {
                  return L(V.prev, w(D), V, this);
                }
              }, {
                key: "insertAfter",
                value: function(D, V) {
                  return L(V, w(D), V.next, this);
                }
              }, {
                key: "insertNodeBefore",
                value: function(D, V) {
                  return L(V.prev, D, V, this);
                }
              }, {
                key: "insertNodeAfter",
                value: function(D, V) {
                  return L(V, D, V.next, this);
                }
              }, {
                key: "push",
                value: function(D) {
                  return L(this.tail, w(D), null, this);
                }
              }, {
                key: "unshift",
                value: function(D) {
                  return L(null, w(D), this.head, this);
                }
              }, {
                key: "remove",
                value: function(D) {
                  return G(D, this);
                }
              }, {
                key: "pop",
                value: function() {
                  return G(this.tail, this).value;
                }
              }, {
                key: "popNode",
                value: function() {
                  return G(this.tail, this);
                }
              }, {
                key: "shift",
                value: function() {
                  return G(this.head, this).value;
                }
              }, {
                key: "shiftNode",
                value: function() {
                  return G(this.head, this);
                }
              }, {
                key: "get_object_at",
                value: function(D) {
                  if (D <= this.length()) {
                    for (var V = 1, _ = this.head; V < D; )
                      _ = _.next, V++;
                    return _.value;
                  }
                }
              }, {
                key: "set_object_at",
                value: function(D, V) {
                  if (D <= this.length()) {
                    for (var _ = 1, J = this.head; _ < D; )
                      J = J.next, _++;
                    J.value = V;
                  }
                }
              }]), P;
            }();
            Q.exports = U;
          },
          /* 12 */
          /***/
          function(Q, ce, Y) {
            function A(T, w, L) {
              this.x = null, this.y = null, T == null && w == null && L == null ? (this.x = 0, this.y = 0) : typeof T == "number" && typeof w == "number" && L == null ? (this.x = T, this.y = w) : T.constructor.name == "Point" && w == null && L == null && (L = T, this.x = L.x, this.y = L.y);
            }
            A.prototype.getX = function() {
              return this.x;
            }, A.prototype.getY = function() {
              return this.y;
            }, A.prototype.getLocation = function() {
              return new A(this.x, this.y);
            }, A.prototype.setLocation = function(T, w, L) {
              T.constructor.name == "Point" && w == null && L == null ? (L = T, this.setLocation(L.x, L.y)) : typeof T == "number" && typeof w == "number" && L == null && (parseInt(T) == T && parseInt(w) == w ? this.move(T, w) : (this.x = Math.floor(T + 0.5), this.y = Math.floor(w + 0.5)));
            }, A.prototype.move = function(T, w) {
              this.x = T, this.y = w;
            }, A.prototype.translate = function(T, w) {
              this.x += T, this.y += w;
            }, A.prototype.equals = function(T) {
              if (T.constructor.name == "Point") {
                var w = T;
                return this.x == w.x && this.y == w.y;
              }
              return this == T;
            }, A.prototype.toString = function() {
              return new A().constructor.name + "[x=" + this.x + ",y=" + this.y + "]";
            }, Q.exports = A;
          },
          /* 13 */
          /***/
          function(Q, ce, Y) {
            function A(T, w, L, G) {
              this.x = 0, this.y = 0, this.width = 0, this.height = 0, T != null && w != null && L != null && G != null && (this.x = T, this.y = w, this.width = L, this.height = G);
            }
            A.prototype.getX = function() {
              return this.x;
            }, A.prototype.setX = function(T) {
              this.x = T;
            }, A.prototype.getY = function() {
              return this.y;
            }, A.prototype.setY = function(T) {
              this.y = T;
            }, A.prototype.getWidth = function() {
              return this.width;
            }, A.prototype.setWidth = function(T) {
              this.width = T;
            }, A.prototype.getHeight = function() {
              return this.height;
            }, A.prototype.setHeight = function(T) {
              this.height = T;
            }, A.prototype.getRight = function() {
              return this.x + this.width;
            }, A.prototype.getBottom = function() {
              return this.y + this.height;
            }, A.prototype.intersects = function(T) {
              return !(this.getRight() < T.x || this.getBottom() < T.y || T.getRight() < this.x || T.getBottom() < this.y);
            }, A.prototype.getCenterX = function() {
              return this.x + this.width / 2;
            }, A.prototype.getMinX = function() {
              return this.getX();
            }, A.prototype.getMaxX = function() {
              return this.getX() + this.width;
            }, A.prototype.getCenterY = function() {
              return this.y + this.height / 2;
            }, A.prototype.getMinY = function() {
              return this.getY();
            }, A.prototype.getMaxY = function() {
              return this.getY() + this.height;
            }, A.prototype.getWidthHalf = function() {
              return this.width / 2;
            }, A.prototype.getHeightHalf = function() {
              return this.height / 2;
            }, Q.exports = A;
          },
          /* 14 */
          /***/
          function(Q, ce, Y) {
            var A = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(w) {
              return typeof w;
            } : function(w) {
              return w && typeof Symbol == "function" && w.constructor === Symbol && w !== Symbol.prototype ? "symbol" : typeof w;
            };
            function T() {
            }
            T.lastID = 0, T.createID = function(w) {
              return T.isPrimitive(w) ? w : (w.uniqueID != null || (w.uniqueID = T.getString(), T.lastID++), w.uniqueID);
            }, T.getString = function(w) {
              return w == null && (w = T.lastID), "Object#" + w;
            }, T.isPrimitive = function(w) {
              var L = typeof w > "u" ? "undefined" : A(w);
              return w == null || L != "object" && L != "function";
            }, Q.exports = T;
          },
          /* 15 */
          /***/
          function(Q, ce, Y) {
            function A(_) {
              if (Array.isArray(_)) {
                for (var J = 0, ne = Array(_.length); J < _.length; J++)
                  ne[J] = _[J];
                return ne;
              } else
                return Array.from(_);
            }
            var T = Y(0), w = Y(6), L = Y(3), G = Y(1), U = Y(5), P = Y(4), K = Y(17), D = Y(27);
            function V(_) {
              D.call(this), this.layoutQuality = T.QUALITY, this.createBendsAsNeeded = T.DEFAULT_CREATE_BENDS_AS_NEEDED, this.incremental = T.DEFAULT_INCREMENTAL, this.animationOnLayout = T.DEFAULT_ANIMATION_ON_LAYOUT, this.animationDuringLayout = T.DEFAULT_ANIMATION_DURING_LAYOUT, this.animationPeriod = T.DEFAULT_ANIMATION_PERIOD, this.uniformLeafNodeSizes = T.DEFAULT_UNIFORM_LEAF_NODE_SIZES, this.edgeToDummyNodes = /* @__PURE__ */ new Map(), this.graphManager = new w(this), this.isLayoutFinished = !1, this.isSubLayout = !1, this.isRemoteUse = !1, _ != null && (this.isRemoteUse = _);
            }
            V.RANDOM_SEED = 1, V.prototype = Object.create(D.prototype), V.prototype.getGraphManager = function() {
              return this.graphManager;
            }, V.prototype.getAllNodes = function() {
              return this.graphManager.getAllNodes();
            }, V.prototype.getAllEdges = function() {
              return this.graphManager.getAllEdges();
            }, V.prototype.getAllNodesToApplyGravitation = function() {
              return this.graphManager.getAllNodesToApplyGravitation();
            }, V.prototype.newGraphManager = function() {
              var _ = new w(this);
              return this.graphManager = _, _;
            }, V.prototype.newGraph = function(_) {
              return new U(null, this.graphManager, _);
            }, V.prototype.newNode = function(_) {
              return new L(this.graphManager, _);
            }, V.prototype.newEdge = function(_) {
              return new G(null, null, _);
            }, V.prototype.checkLayoutSuccess = function() {
              return this.graphManager.getRoot() == null || this.graphManager.getRoot().getNodes().length == 0 || this.graphManager.includesInvalidEdge();
            }, V.prototype.runLayout = function() {
              this.isLayoutFinished = !1, this.tilingPreLayout && this.tilingPreLayout(), this.initParameters();
              var _;
              return this.checkLayoutSuccess() ? _ = !1 : _ = this.layout(), T.ANIMATE === "during" ? !1 : (_ && (this.isSubLayout || this.doPostLayout()), this.tilingPostLayout && this.tilingPostLayout(), this.isLayoutFinished = !0, _);
            }, V.prototype.doPostLayout = function() {
              this.incremental || this.transform(), this.update();
            }, V.prototype.update2 = function() {
              if (this.createBendsAsNeeded && (this.createBendpointsFromDummyNodes(), this.graphManager.resetAllEdges()), !this.isRemoteUse) {
                for (var _ = this.graphManager.getAllEdges(), J = 0; J < _.length; J++)
                  _[J];
                for (var ne = this.graphManager.getRoot().getNodes(), J = 0; J < ne.length; J++)
                  ne[J];
                this.update(this.graphManager.getRoot());
              }
            }, V.prototype.update = function(_) {
              if (_ == null)
                this.update2();
              else if (_ instanceof L) {
                var J = _;
                if (J.getChild() != null)
                  for (var ne = J.getChild().getNodes(), ue = 0; ue < ne.length; ue++)
                    update(ne[ue]);
                if (J.vGraphObject != null) {
                  var j = J.vGraphObject;
                  j.update(J);
                }
              } else if (_ instanceof G) {
                var ee = _;
                if (ee.vGraphObject != null) {
                  var H = ee.vGraphObject;
                  H.update(ee);
                }
              } else if (_ instanceof U) {
                var te = _;
                if (te.vGraphObject != null) {
                  var S = te.vGraphObject;
                  S.update(te);
                }
              }
            }, V.prototype.initParameters = function() {
              this.isSubLayout || (this.layoutQuality = T.QUALITY, this.animationDuringLayout = T.DEFAULT_ANIMATION_DURING_LAYOUT, this.animationPeriod = T.DEFAULT_ANIMATION_PERIOD, this.animationOnLayout = T.DEFAULT_ANIMATION_ON_LAYOUT, this.incremental = T.DEFAULT_INCREMENTAL, this.createBendsAsNeeded = T.DEFAULT_CREATE_BENDS_AS_NEEDED, this.uniformLeafNodeSizes = T.DEFAULT_UNIFORM_LEAF_NODE_SIZES), this.animationDuringLayout && (this.animationOnLayout = !1);
            }, V.prototype.transform = function(_) {
              if (_ == null)
                this.transform(new P(0, 0));
              else {
                var J = new K(), ne = this.graphManager.getRoot().updateLeftTop();
                if (ne != null) {
                  J.setWorldOrgX(_.x), J.setWorldOrgY(_.y), J.setDeviceOrgX(ne.x), J.setDeviceOrgY(ne.y);
                  for (var ue = this.getAllNodes(), j, ee = 0; ee < ue.length; ee++)
                    j = ue[ee], j.transform(J);
                }
              }
            }, V.prototype.positionNodesRandomly = function(_) {
              if (_ == null)
                this.positionNodesRandomly(this.getGraphManager().getRoot()), this.getGraphManager().getRoot().updateBounds(!0);
              else
                for (var J, ne, ue = _.getNodes(), j = 0; j < ue.length; j++)
                  J = ue[j], ne = J.getChild(), ne == null || ne.getNodes().length == 0 ? J.scatter() : (this.positionNodesRandomly(ne), J.updateBounds());
            }, V.prototype.getFlatForest = function() {
              for (var _ = [], J = !0, ne = this.graphManager.getRoot().getNodes(), ue = !0, j = 0; j < ne.length; j++)
                ne[j].getChild() != null && (ue = !1);
              if (!ue)
                return _;
              var ee = /* @__PURE__ */ new Set(), H = [], te = /* @__PURE__ */ new Map(), S = [];
              for (S = S.concat(ne); S.length > 0 && J; ) {
                for (H.push(S[0]); H.length > 0 && J; ) {
                  var $ = H[0];
                  H.splice(0, 1), ee.add($);
                  for (var k = $.getEdges(), j = 0; j < k.length; j++) {
                    var q = k[j].getOtherEnd($);
                    if (te.get($) != q)
                      if (!ee.has(q))
                        H.push(q), te.set(q, $);
                      else {
                        J = !1;
                        break;
                      }
                  }
                }
                if (!J)
                  _ = [];
                else {
                  var ve = [].concat(A(ee));
                  _.push(ve);
                  for (var j = 0; j < ve.length; j++) {
                    var pe = ve[j], Ae = S.indexOf(pe);
                    Ae > -1 && S.splice(Ae, 1);
                  }
                  ee = /* @__PURE__ */ new Set(), te = /* @__PURE__ */ new Map();
                }
              }
              return _;
            }, V.prototype.createDummyNodesForBendpoints = function(_) {
              for (var J = [], ne = _.source, ue = this.graphManager.calcLowestCommonAncestor(_.source, _.target), j = 0; j < _.bendpoints.length; j++) {
                var ee = this.newNode(null);
                ee.setRect(new Point(0, 0), new Dimension(1, 1)), ue.add(ee);
                var H = this.newEdge(null);
                this.graphManager.add(H, ne, ee), J.add(ee), ne = ee;
              }
              var H = this.newEdge(null);
              return this.graphManager.add(H, ne, _.target), this.edgeToDummyNodes.set(_, J), _.isInterGraph() ? this.graphManager.remove(_) : ue.remove(_), J;
            }, V.prototype.createBendpointsFromDummyNodes = function() {
              var _ = [];
              _ = _.concat(this.graphManager.getAllEdges()), _ = [].concat(A(this.edgeToDummyNodes.keys())).concat(_);
              for (var J = 0; J < _.length; J++) {
                var ne = _[J];
                if (ne.bendpoints.length > 0) {
                  for (var ue = this.edgeToDummyNodes.get(ne), j = 0; j < ue.length; j++) {
                    var ee = ue[j], H = new P(ee.getCenterX(), ee.getCenterY()), te = ne.bendpoints.get(j);
                    te.x = H.x, te.y = H.y, ee.getOwner().remove(ee);
                  }
                  this.graphManager.add(ne, ne.source, ne.target);
                }
              }
            }, V.transform = function(_, J, ne, ue) {
              if (ne != null && ue != null) {
                var j = J;
                if (_ <= 50) {
                  var ee = J / ne;
                  j -= (J - ee) / 50 * (50 - _);
                } else {
                  var H = J * ue;
                  j += (H - J) / 50 * (_ - 50);
                }
                return j;
              } else {
                var te, S;
                return _ <= 50 ? (te = 9 * J / 500, S = J / 10) : (te = 9 * J / 50, S = -8 * J), te * _ + S;
              }
            }, V.findCenterOfTree = function(_) {
              var J = [];
              J = J.concat(_);
              var ne = [], ue = /* @__PURE__ */ new Map(), j = !1, ee = null;
              (J.length == 1 || J.length == 2) && (j = !0, ee = J[0]);
              for (var H = 0; H < J.length; H++) {
                var te = J[H], S = te.getNeighborsList().size;
                ue.set(te, te.getNeighborsList().size), S == 1 && ne.push(te);
              }
              var $ = [];
              for ($ = $.concat(ne); !j; ) {
                var k = [];
                k = k.concat($), $ = [];
                for (var H = 0; H < J.length; H++) {
                  var te = J[H], q = J.indexOf(te);
                  q >= 0 && J.splice(q, 1);
                  var ve = te.getNeighborsList();
                  ve.forEach(function(Ne) {
                    if (ne.indexOf(Ne) < 0) {
                      var _e = ue.get(Ne), tt = _e - 1;
                      tt == 1 && $.push(Ne), ue.set(Ne, tt);
                    }
                  });
                }
                ne = ne.concat($), (J.length == 1 || J.length == 2) && (j = !0, ee = J[0]);
              }
              return ee;
            }, V.prototype.setGraphManager = function(_) {
              this.graphManager = _;
            }, Q.exports = V;
          },
          /* 16 */
          /***/
          function(Q, ce, Y) {
            function A() {
            }
            A.seed = 1, A.x = 0, A.nextDouble = function() {
              return A.x = Math.sin(A.seed++) * 1e4, A.x - Math.floor(A.x);
            }, Q.exports = A;
          },
          /* 17 */
          /***/
          function(Q, ce, Y) {
            var A = Y(4);
            function T(w, L) {
              this.lworldOrgX = 0, this.lworldOrgY = 0, this.ldeviceOrgX = 0, this.ldeviceOrgY = 0, this.lworldExtX = 1, this.lworldExtY = 1, this.ldeviceExtX = 1, this.ldeviceExtY = 1;
            }
            T.prototype.getWorldOrgX = function() {
              return this.lworldOrgX;
            }, T.prototype.setWorldOrgX = function(w) {
              this.lworldOrgX = w;
            }, T.prototype.getWorldOrgY = function() {
              return this.lworldOrgY;
            }, T.prototype.setWorldOrgY = function(w) {
              this.lworldOrgY = w;
            }, T.prototype.getWorldExtX = function() {
              return this.lworldExtX;
            }, T.prototype.setWorldExtX = function(w) {
              this.lworldExtX = w;
            }, T.prototype.getWorldExtY = function() {
              return this.lworldExtY;
            }, T.prototype.setWorldExtY = function(w) {
              this.lworldExtY = w;
            }, T.prototype.getDeviceOrgX = function() {
              return this.ldeviceOrgX;
            }, T.prototype.setDeviceOrgX = function(w) {
              this.ldeviceOrgX = w;
            }, T.prototype.getDeviceOrgY = function() {
              return this.ldeviceOrgY;
            }, T.prototype.setDeviceOrgY = function(w) {
              this.ldeviceOrgY = w;
            }, T.prototype.getDeviceExtX = function() {
              return this.ldeviceExtX;
            }, T.prototype.setDeviceExtX = function(w) {
              this.ldeviceExtX = w;
            }, T.prototype.getDeviceExtY = function() {
              return this.ldeviceExtY;
            }, T.prototype.setDeviceExtY = function(w) {
              this.ldeviceExtY = w;
            }, T.prototype.transformX = function(w) {
              var L = 0, G = this.lworldExtX;
              return G != 0 && (L = this.ldeviceOrgX + (w - this.lworldOrgX) * this.ldeviceExtX / G), L;
            }, T.prototype.transformY = function(w) {
              var L = 0, G = this.lworldExtY;
              return G != 0 && (L = this.ldeviceOrgY + (w - this.lworldOrgY) * this.ldeviceExtY / G), L;
            }, T.prototype.inverseTransformX = function(w) {
              var L = 0, G = this.ldeviceExtX;
              return G != 0 && (L = this.lworldOrgX + (w - this.ldeviceOrgX) * this.lworldExtX / G), L;
            }, T.prototype.inverseTransformY = function(w) {
              var L = 0, G = this.ldeviceExtY;
              return G != 0 && (L = this.lworldOrgY + (w - this.ldeviceOrgY) * this.lworldExtY / G), L;
            }, T.prototype.inverseTransformPoint = function(w) {
              var L = new A(this.inverseTransformX(w.x), this.inverseTransformY(w.y));
              return L;
            }, Q.exports = T;
          },
          /* 18 */
          /***/
          function(Q, ce, Y) {
            function A(D) {
              if (Array.isArray(D)) {
                for (var V = 0, _ = Array(D.length); V < D.length; V++)
                  _[V] = D[V];
                return _;
              } else
                return Array.from(D);
            }
            var T = Y(15), w = Y(7), L = Y(0), G = Y(8), U = Y(9);
            function P() {
              T.call(this), this.useSmartIdealEdgeLengthCalculation = w.DEFAULT_USE_SMART_IDEAL_EDGE_LENGTH_CALCULATION, this.idealEdgeLength = w.DEFAULT_EDGE_LENGTH, this.springConstant = w.DEFAULT_SPRING_STRENGTH, this.repulsionConstant = w.DEFAULT_REPULSION_STRENGTH, this.gravityConstant = w.DEFAULT_GRAVITY_STRENGTH, this.compoundGravityConstant = w.DEFAULT_COMPOUND_GRAVITY_STRENGTH, this.gravityRangeFactor = w.DEFAULT_GRAVITY_RANGE_FACTOR, this.compoundGravityRangeFactor = w.DEFAULT_COMPOUND_GRAVITY_RANGE_FACTOR, this.displacementThresholdPerNode = 3 * w.DEFAULT_EDGE_LENGTH / 100, this.coolingFactor = w.DEFAULT_COOLING_FACTOR_INCREMENTAL, this.initialCoolingFactor = w.DEFAULT_COOLING_FACTOR_INCREMENTAL, this.totalDisplacement = 0, this.oldTotalDisplacement = 0, this.maxIterations = w.MAX_ITERATIONS;
            }
            P.prototype = Object.create(T.prototype);
            for (var K in T)
              P[K] = T[K];
            P.prototype.initParameters = function() {
              T.prototype.initParameters.call(this, arguments), this.totalIterations = 0, this.notAnimatedIterations = 0, this.useFRGridVariant = w.DEFAULT_USE_SMART_REPULSION_RANGE_CALCULATION, this.grid = [];
            }, P.prototype.calcIdealEdgeLengths = function() {
              for (var D, V, _, J, ne, ue, j = this.getGraphManager().getAllEdges(), ee = 0; ee < j.length; ee++)
                D = j[ee], D.idealLength = this.idealEdgeLength, D.isInterGraph && (_ = D.getSource(), J = D.getTarget(), ne = D.getSourceInLca().getEstimatedSize(), ue = D.getTargetInLca().getEstimatedSize(), this.useSmartIdealEdgeLengthCalculation && (D.idealLength += ne + ue - 2 * L.SIMPLE_NODE_SIZE), V = D.getLca().getInclusionTreeDepth(), D.idealLength += w.DEFAULT_EDGE_LENGTH * w.PER_LEVEL_IDEAL_EDGE_LENGTH_FACTOR * (_.getInclusionTreeDepth() + J.getInclusionTreeDepth() - 2 * V));
            }, P.prototype.initSpringEmbedder = function() {
              var D = this.getAllNodes().length;
              this.incremental ? (D > w.ADAPTATION_LOWER_NODE_LIMIT && (this.coolingFactor = Math.max(this.coolingFactor * w.COOLING_ADAPTATION_FACTOR, this.coolingFactor - (D - w.ADAPTATION_LOWER_NODE_LIMIT) / (w.ADAPTATION_UPPER_NODE_LIMIT - w.ADAPTATION_LOWER_NODE_LIMIT) * this.coolingFactor * (1 - w.COOLING_ADAPTATION_FACTOR))), this.maxNodeDisplacement = w.MAX_NODE_DISPLACEMENT_INCREMENTAL) : (D > w.ADAPTATION_LOWER_NODE_LIMIT ? this.coolingFactor = Math.max(w.COOLING_ADAPTATION_FACTOR, 1 - (D - w.ADAPTATION_LOWER_NODE_LIMIT) / (w.ADAPTATION_UPPER_NODE_LIMIT - w.ADAPTATION_LOWER_NODE_LIMIT) * (1 - w.COOLING_ADAPTATION_FACTOR)) : this.coolingFactor = 1, this.initialCoolingFactor = this.coolingFactor, this.maxNodeDisplacement = w.MAX_NODE_DISPLACEMENT), this.maxIterations = Math.max(this.getAllNodes().length * 5, this.maxIterations), this.totalDisplacementThreshold = this.displacementThresholdPerNode * this.getAllNodes().length, this.repulsionRange = this.calcRepulsionRange();
            }, P.prototype.calcSpringForces = function() {
              for (var D = this.getAllEdges(), V, _ = 0; _ < D.length; _++)
                V = D[_], this.calcSpringForce(V, V.idealLength);
            }, P.prototype.calcRepulsionForces = function() {
              var D = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : !0, V = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, _, J, ne, ue, j = this.getAllNodes(), ee;
              if (this.useFRGridVariant)
                for (this.totalIterations % w.GRID_CALCULATION_CHECK_PERIOD == 1 && D && this.updateGrid(), ee = /* @__PURE__ */ new Set(), _ = 0; _ < j.length; _++)
                  ne = j[_], this.calculateRepulsionForceOfANode(ne, ee, D, V), ee.add(ne);
              else
                for (_ = 0; _ < j.length; _++)
                  for (ne = j[_], J = _ + 1; J < j.length; J++)
                    ue = j[J], ne.getOwner() == ue.getOwner() && this.calcRepulsionForce(ne, ue);
            }, P.prototype.calcGravitationalForces = function() {
              for (var D, V = this.getAllNodesToApplyGravitation(), _ = 0; _ < V.length; _++)
                D = V[_], this.calcGravitationalForce(D);
            }, P.prototype.moveNodes = function() {
              for (var D = this.getAllNodes(), V, _ = 0; _ < D.length; _++)
                V = D[_], V.move();
            }, P.prototype.calcSpringForce = function(D, V) {
              var _ = D.getSource(), J = D.getTarget(), ne, ue, j, ee;
              if (this.uniformLeafNodeSizes && _.getChild() == null && J.getChild() == null)
                D.updateLengthSimple();
              else if (D.updateLength(), D.isOverlapingSourceAndTarget)
                return;
              ne = D.getLength(), ne != 0 && (ue = this.springConstant * (ne - V), j = ue * (D.lengthX / ne), ee = ue * (D.lengthY / ne), _.springForceX += j, _.springForceY += ee, J.springForceX -= j, J.springForceY -= ee);
            }, P.prototype.calcRepulsionForce = function(D, V) {
              var _ = D.getRect(), J = V.getRect(), ne = new Array(2), ue = new Array(4), j, ee, H, te, S, $, k;
              if (_.intersects(J)) {
                G.calcSeparationAmount(_, J, ne, w.DEFAULT_EDGE_LENGTH / 2), $ = 2 * ne[0], k = 2 * ne[1];
                var q = D.noOfChildren * V.noOfChildren / (D.noOfChildren + V.noOfChildren);
                D.repulsionForceX -= q * $, D.repulsionForceY -= q * k, V.repulsionForceX += q * $, V.repulsionForceY += q * k;
              } else
                this.uniformLeafNodeSizes && D.getChild() == null && V.getChild() == null ? (j = J.getCenterX() - _.getCenterX(), ee = J.getCenterY() - _.getCenterY()) : (G.getIntersection(_, J, ue), j = ue[2] - ue[0], ee = ue[3] - ue[1]), Math.abs(j) < w.MIN_REPULSION_DIST && (j = U.sign(j) * w.MIN_REPULSION_DIST), Math.abs(ee) < w.MIN_REPULSION_DIST && (ee = U.sign(ee) * w.MIN_REPULSION_DIST), H = j * j + ee * ee, te = Math.sqrt(H), S = this.repulsionConstant * D.noOfChildren * V.noOfChildren / H, $ = S * j / te, k = S * ee / te, D.repulsionForceX -= $, D.repulsionForceY -= k, V.repulsionForceX += $, V.repulsionForceY += k;
            }, P.prototype.calcGravitationalForce = function(D) {
              var V, _, J, ne, ue, j, ee, H;
              V = D.getOwner(), _ = (V.getRight() + V.getLeft()) / 2, J = (V.getTop() + V.getBottom()) / 2, ne = D.getCenterX() - _, ue = D.getCenterY() - J, j = Math.abs(ne) + D.getWidth() / 2, ee = Math.abs(ue) + D.getHeight() / 2, D.getOwner() == this.graphManager.getRoot() ? (H = V.getEstimatedSize() * this.gravityRangeFactor, (j > H || ee > H) && (D.gravitationForceX = -this.gravityConstant * ne, D.gravitationForceY = -this.gravityConstant * ue)) : (H = V.getEstimatedSize() * this.compoundGravityRangeFactor, (j > H || ee > H) && (D.gravitationForceX = -this.gravityConstant * ne * this.compoundGravityConstant, D.gravitationForceY = -this.gravityConstant * ue * this.compoundGravityConstant));
            }, P.prototype.isConverged = function() {
              var D, V = !1;
              return this.totalIterations > this.maxIterations / 3 && (V = Math.abs(this.totalDisplacement - this.oldTotalDisplacement) < 2), D = this.totalDisplacement < this.totalDisplacementThreshold, this.oldTotalDisplacement = this.totalDisplacement, D || V;
            }, P.prototype.animate = function() {
              this.animationDuringLayout && !this.isSubLayout && (this.notAnimatedIterations == this.animationPeriod ? (this.update(), this.notAnimatedIterations = 0) : this.notAnimatedIterations++);
            }, P.prototype.calcNoOfChildrenForAllNodes = function() {
              for (var D, V = this.graphManager.getAllNodes(), _ = 0; _ < V.length; _++)
                D = V[_], D.noOfChildren = D.getNoOfChildren();
            }, P.prototype.calcGrid = function(D) {
              var V = 0, _ = 0;
              V = parseInt(Math.ceil((D.getRight() - D.getLeft()) / this.repulsionRange)), _ = parseInt(Math.ceil((D.getBottom() - D.getTop()) / this.repulsionRange));
              for (var J = new Array(V), ne = 0; ne < V; ne++)
                J[ne] = new Array(_);
              for (var ne = 0; ne < V; ne++)
                for (var ue = 0; ue < _; ue++)
                  J[ne][ue] = new Array();
              return J;
            }, P.prototype.addNodeToGrid = function(D, V, _) {
              var J = 0, ne = 0, ue = 0, j = 0;
              J = parseInt(Math.floor((D.getRect().x - V) / this.repulsionRange)), ne = parseInt(Math.floor((D.getRect().width + D.getRect().x - V) / this.repulsionRange)), ue = parseInt(Math.floor((D.getRect().y - _) / this.repulsionRange)), j = parseInt(Math.floor((D.getRect().height + D.getRect().y - _) / this.repulsionRange));
              for (var ee = J; ee <= ne; ee++)
                for (var H = ue; H <= j; H++)
                  this.grid[ee][H].push(D), D.setGridCoordinates(J, ne, ue, j);
            }, P.prototype.updateGrid = function() {
              var D, V, _ = this.getAllNodes();
              for (this.grid = this.calcGrid(this.graphManager.getRoot()), D = 0; D < _.length; D++)
                V = _[D], this.addNodeToGrid(V, this.graphManager.getRoot().getLeft(), this.graphManager.getRoot().getTop());
            }, P.prototype.calculateRepulsionForceOfANode = function(D, V, _, J) {
              if (this.totalIterations % w.GRID_CALCULATION_CHECK_PERIOD == 1 && _ || J) {
                var ne = /* @__PURE__ */ new Set();
                D.surrounding = new Array();
                for (var ue, j = this.grid, ee = D.startX - 1; ee < D.finishX + 2; ee++)
                  for (var H = D.startY - 1; H < D.finishY + 2; H++)
                    if (!(ee < 0 || H < 0 || ee >= j.length || H >= j[0].length)) {
                      for (var te = 0; te < j[ee][H].length; te++)
                        if (ue = j[ee][H][te], !(D.getOwner() != ue.getOwner() || D == ue) && !V.has(ue) && !ne.has(ue)) {
                          var S = Math.abs(D.getCenterX() - ue.getCenterX()) - (D.getWidth() / 2 + ue.getWidth() / 2), $ = Math.abs(D.getCenterY() - ue.getCenterY()) - (D.getHeight() / 2 + ue.getHeight() / 2);
                          S <= this.repulsionRange && $ <= this.repulsionRange && ne.add(ue);
                        }
                    }
                D.surrounding = [].concat(A(ne));
              }
              for (ee = 0; ee < D.surrounding.length; ee++)
                this.calcRepulsionForce(D, D.surrounding[ee]);
            }, P.prototype.calcRepulsionRange = function() {
              return 0;
            }, Q.exports = P;
          },
          /* 19 */
          /***/
          function(Q, ce, Y) {
            var A = Y(1), T = Y(7);
            function w(G, U, P) {
              A.call(this, G, U, P), this.idealLength = T.DEFAULT_EDGE_LENGTH;
            }
            w.prototype = Object.create(A.prototype);
            for (var L in A)
              w[L] = A[L];
            Q.exports = w;
          },
          /* 20 */
          /***/
          function(Q, ce, Y) {
            var A = Y(3);
            function T(L, G, U, P) {
              A.call(this, L, G, U, P), this.springForceX = 0, this.springForceY = 0, this.repulsionForceX = 0, this.repulsionForceY = 0, this.gravitationForceX = 0, this.gravitationForceY = 0, this.displacementX = 0, this.displacementY = 0, this.startX = 0, this.finishX = 0, this.startY = 0, this.finishY = 0, this.surrounding = [];
            }
            T.prototype = Object.create(A.prototype);
            for (var w in A)
              T[w] = A[w];
            T.prototype.setGridCoordinates = function(L, G, U, P) {
              this.startX = L, this.finishX = G, this.startY = U, this.finishY = P;
            }, Q.exports = T;
          },
          /* 21 */
          /***/
          function(Q, ce, Y) {
            function A(T, w) {
              this.width = 0, this.height = 0, T !== null && w !== null && (this.height = w, this.width = T);
            }
            A.prototype.getWidth = function() {
              return this.width;
            }, A.prototype.setWidth = function(T) {
              this.width = T;
            }, A.prototype.getHeight = function() {
              return this.height;
            }, A.prototype.setHeight = function(T) {
              this.height = T;
            }, Q.exports = A;
          },
          /* 22 */
          /***/
          function(Q, ce, Y) {
            var A = Y(14);
            function T() {
              this.map = {}, this.keys = [];
            }
            T.prototype.put = function(w, L) {
              var G = A.createID(w);
              this.contains(G) || (this.map[G] = L, this.keys.push(w));
            }, T.prototype.contains = function(w) {
              return A.createID(w), this.map[w] != null;
            }, T.prototype.get = function(w) {
              var L = A.createID(w);
              return this.map[L];
            }, T.prototype.keySet = function() {
              return this.keys;
            }, Q.exports = T;
          },
          /* 23 */
          /***/
          function(Q, ce, Y) {
            var A = Y(14);
            function T() {
              this.set = {};
            }
            T.prototype.add = function(w) {
              var L = A.createID(w);
              this.contains(L) || (this.set[L] = w);
            }, T.prototype.remove = function(w) {
              delete this.set[A.createID(w)];
            }, T.prototype.clear = function() {
              this.set = {};
            }, T.prototype.contains = function(w) {
              return this.set[A.createID(w)] == w;
            }, T.prototype.isEmpty = function() {
              return this.size() === 0;
            }, T.prototype.size = function() {
              return Object.keys(this.set).length;
            }, T.prototype.addAllTo = function(w) {
              for (var L = Object.keys(this.set), G = L.length, U = 0; U < G; U++)
                w.push(this.set[L[U]]);
            }, T.prototype.size = function() {
              return Object.keys(this.set).length;
            }, T.prototype.addAll = function(w) {
              for (var L = w.length, G = 0; G < L; G++) {
                var U = w[G];
                this.add(U);
              }
            }, Q.exports = T;
          },
          /* 24 */
          /***/
          function(Q, ce, Y) {
            var A = function() {
              function G(U, P) {
                for (var K = 0; K < P.length; K++) {
                  var D = P[K];
                  D.enumerable = D.enumerable || !1, D.configurable = !0, "value" in D && (D.writable = !0), Object.defineProperty(U, D.key, D);
                }
              }
              return function(U, P, K) {
                return P && G(U.prototype, P), K && G(U, K), U;
              };
            }();
            function T(G, U) {
              if (!(G instanceof U))
                throw new TypeError("Cannot call a class as a function");
            }
            var w = Y(11), L = function() {
              function G(U, P) {
                T(this, G), (P !== null || P !== void 0) && (this.compareFunction = this._defaultCompareFunction);
                var K = void 0;
                U instanceof w ? K = U.size() : K = U.length, this._quicksort(U, 0, K - 1);
              }
              return A(G, [{
                key: "_quicksort",
                value: function(P, K, D) {
                  if (K < D) {
                    var V = this._partition(P, K, D);
                    this._quicksort(P, K, V), this._quicksort(P, V + 1, D);
                  }
                }
              }, {
                key: "_partition",
                value: function(P, K, D) {
                  for (var V = this._get(P, K), _ = K, J = D; ; ) {
                    for (; this.compareFunction(V, this._get(P, J)); )
                      J--;
                    for (; this.compareFunction(this._get(P, _), V); )
                      _++;
                    if (_ < J)
                      this._swap(P, _, J), _++, J--;
                    else
                      return J;
                  }
                }
              }, {
                key: "_get",
                value: function(P, K) {
                  return P instanceof w ? P.get_object_at(K) : P[K];
                }
              }, {
                key: "_set",
                value: function(P, K, D) {
                  P instanceof w ? P.set_object_at(K, D) : P[K] = D;
                }
              }, {
                key: "_swap",
                value: function(P, K, D) {
                  var V = this._get(P, K);
                  this._set(P, K, this._get(P, D)), this._set(P, D, V);
                }
              }, {
                key: "_defaultCompareFunction",
                value: function(P, K) {
                  return K > P;
                }
              }]), G;
            }();
            Q.exports = L;
          },
          /* 25 */
          /***/
          function(Q, ce, Y) {
            var A = function() {
              function L(G, U) {
                for (var P = 0; P < U.length; P++) {
                  var K = U[P];
                  K.enumerable = K.enumerable || !1, K.configurable = !0, "value" in K && (K.writable = !0), Object.defineProperty(G, K.key, K);
                }
              }
              return function(G, U, P) {
                return U && L(G.prototype, U), P && L(G, P), G;
              };
            }();
            function T(L, G) {
              if (!(L instanceof G))
                throw new TypeError("Cannot call a class as a function");
            }
            var w = function() {
              function L(G, U) {
                var P = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : 1, K = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : -1, D = arguments.length > 4 && arguments[4] !== void 0 ? arguments[4] : -1;
                T(this, L), this.sequence1 = G, this.sequence2 = U, this.match_score = P, this.mismatch_penalty = K, this.gap_penalty = D, this.iMax = G.length + 1, this.jMax = U.length + 1, this.grid = new Array(this.iMax);
                for (var V = 0; V < this.iMax; V++) {
                  this.grid[V] = new Array(this.jMax);
                  for (var _ = 0; _ < this.jMax; _++)
                    this.grid[V][_] = 0;
                }
                this.tracebackGrid = new Array(this.iMax);
                for (var J = 0; J < this.iMax; J++) {
                  this.tracebackGrid[J] = new Array(this.jMax);
                  for (var ne = 0; ne < this.jMax; ne++)
                    this.tracebackGrid[J][ne] = [null, null, null];
                }
                this.alignments = [], this.score = -1, this.computeGrids();
              }
              return A(L, [{
                key: "getScore",
                value: function() {
                  return this.score;
                }
              }, {
                key: "getAlignments",
                value: function() {
                  return this.alignments;
                }
                // Main dynamic programming procedure
              }, {
                key: "computeGrids",
                value: function() {
                  for (var U = 1; U < this.jMax; U++)
                    this.grid[0][U] = this.grid[0][U - 1] + this.gap_penalty, this.tracebackGrid[0][U] = [!1, !1, !0];
                  for (var P = 1; P < this.iMax; P++)
                    this.grid[P][0] = this.grid[P - 1][0] + this.gap_penalty, this.tracebackGrid[P][0] = [!1, !0, !1];
                  for (var K = 1; K < this.iMax; K++)
                    for (var D = 1; D < this.jMax; D++) {
                      var V = void 0;
                      this.sequence1[K - 1] === this.sequence2[D - 1] ? V = this.grid[K - 1][D - 1] + this.match_score : V = this.grid[K - 1][D - 1] + this.mismatch_penalty;
                      var _ = this.grid[K - 1][D] + this.gap_penalty, J = this.grid[K][D - 1] + this.gap_penalty, ne = [V, _, J], ue = this.arrayAllMaxIndexes(ne);
                      this.grid[K][D] = ne[ue[0]], this.tracebackGrid[K][D] = [ue.includes(0), ue.includes(1), ue.includes(2)];
                    }
                  this.score = this.grid[this.iMax - 1][this.jMax - 1];
                }
                // Gets all possible valid sequence combinations
              }, {
                key: "alignmentTraceback",
                value: function() {
                  var U = [];
                  for (U.push({
                    pos: [this.sequence1.length, this.sequence2.length],
                    seq1: "",
                    seq2: ""
                  }); U[0]; ) {
                    var P = U[0], K = this.tracebackGrid[P.pos[0]][P.pos[1]];
                    K[0] && U.push({
                      pos: [P.pos[0] - 1, P.pos[1] - 1],
                      seq1: this.sequence1[P.pos[0] - 1] + P.seq1,
                      seq2: this.sequence2[P.pos[1] - 1] + P.seq2
                    }), K[1] && U.push({
                      pos: [P.pos[0] - 1, P.pos[1]],
                      seq1: this.sequence1[P.pos[0] - 1] + P.seq1,
                      seq2: "-" + P.seq2
                    }), K[2] && U.push({
                      pos: [P.pos[0], P.pos[1] - 1],
                      seq1: "-" + P.seq1,
                      seq2: this.sequence2[P.pos[1] - 1] + P.seq2
                    }), P.pos[0] === 0 && P.pos[1] === 0 && this.alignments.push({
                      sequence1: P.seq1,
                      sequence2: P.seq2
                    }), U.shift();
                  }
                  return this.alignments;
                }
                // Helper Functions
              }, {
                key: "getAllIndexes",
                value: function(U, P) {
                  for (var K = [], D = -1; (D = U.indexOf(P, D + 1)) !== -1; )
                    K.push(D);
                  return K;
                }
              }, {
                key: "arrayAllMaxIndexes",
                value: function(U) {
                  return this.getAllIndexes(U, Math.max.apply(null, U));
                }
              }]), L;
            }();
            Q.exports = w;
          },
          /* 26 */
          /***/
          function(Q, ce, Y) {
            var A = function() {
            };
            A.FDLayout = Y(18), A.FDLayoutConstants = Y(7), A.FDLayoutEdge = Y(19), A.FDLayoutNode = Y(20), A.DimensionD = Y(21), A.HashMap = Y(22), A.HashSet = Y(23), A.IGeometry = Y(8), A.IMath = Y(9), A.Integer = Y(10), A.Point = Y(12), A.PointD = Y(4), A.RandomSeed = Y(16), A.RectangleD = Y(13), A.Transform = Y(17), A.UniqueIDGeneretor = Y(14), A.Quicksort = Y(24), A.LinkedList = Y(11), A.LGraphObject = Y(2), A.LGraph = Y(5), A.LEdge = Y(1), A.LGraphManager = Y(6), A.LNode = Y(3), A.Layout = Y(15), A.LayoutConstants = Y(0), A.NeedlemanWunsch = Y(25), Q.exports = A;
          },
          /* 27 */
          /***/
          function(Q, ce, Y) {
            function A() {
              this.listeners = [];
            }
            var T = A.prototype;
            T.addListener = function(w, L) {
              this.listeners.push({
                event: w,
                callback: L
              });
            }, T.removeListener = function(w, L) {
              for (var G = this.listeners.length; G >= 0; G--) {
                var U = this.listeners[G];
                U.event === w && U.callback === L && this.listeners.splice(G, 1);
              }
            }, T.emit = function(w, L) {
              for (var G = 0; G < this.listeners.length; G++) {
                var U = this.listeners[G];
                w === U.event && U.callback(L);
              }
            }, Q.exports = A;
          }
          /******/
        ])
      );
    });
  }(Kp)), ri;
}
var _u;
function Qp() {
  return _u || (_u = 1, function(fe, he) {
    (function(ce, Y) {
      fe.exports = Y(Zp());
    })(Ca, function(Q) {
      return (
        /******/
        function(ce) {
          var Y = {};
          function A(T) {
            if (Y[T])
              return Y[T].exports;
            var w = Y[T] = {
              /******/
              i: T,
              /******/
              l: !1,
              /******/
              exports: {}
              /******/
            };
            return ce[T].call(w.exports, w, w.exports, A), w.l = !0, w.exports;
          }
          return A.m = ce, A.c = Y, A.i = function(T) {
            return T;
          }, A.d = function(T, w, L) {
            A.o(T, w) || Object.defineProperty(T, w, {
              /******/
              configurable: !1,
              /******/
              enumerable: !0,
              /******/
              get: L
              /******/
            });
          }, A.n = function(T) {
            var w = T && T.__esModule ? (
              /******/
              function() {
                return T.default;
              }
            ) : (
              /******/
              function() {
                return T;
              }
            );
            return A.d(w, "a", w), w;
          }, A.o = function(T, w) {
            return Object.prototype.hasOwnProperty.call(T, w);
          }, A.p = "", A(A.s = 7);
        }([
          /* 0 */
          /***/
          function(ce, Y) {
            ce.exports = Q;
          },
          /* 1 */
          /***/
          function(ce, Y, A) {
            var T = A(0).FDLayoutConstants;
            function w() {
            }
            for (var L in T)
              w[L] = T[L];
            w.DEFAULT_USE_MULTI_LEVEL_SCALING = !1, w.DEFAULT_RADIAL_SEPARATION = T.DEFAULT_EDGE_LENGTH, w.DEFAULT_COMPONENT_SEPERATION = 60, w.TILE = !0, w.TILING_PADDING_VERTICAL = 10, w.TILING_PADDING_HORIZONTAL = 10, w.TREE_REDUCTION_ON_INCREMENTAL = !1, ce.exports = w;
          },
          /* 2 */
          /***/
          function(ce, Y, A) {
            var T = A(0).FDLayoutEdge;
            function w(G, U, P) {
              T.call(this, G, U, P);
            }
            w.prototype = Object.create(T.prototype);
            for (var L in T)
              w[L] = T[L];
            ce.exports = w;
          },
          /* 3 */
          /***/
          function(ce, Y, A) {
            var T = A(0).LGraph;
            function w(G, U, P) {
              T.call(this, G, U, P);
            }
            w.prototype = Object.create(T.prototype);
            for (var L in T)
              w[L] = T[L];
            ce.exports = w;
          },
          /* 4 */
          /***/
          function(ce, Y, A) {
            var T = A(0).LGraphManager;
            function w(G) {
              T.call(this, G);
            }
            w.prototype = Object.create(T.prototype);
            for (var L in T)
              w[L] = T[L];
            ce.exports = w;
          },
          /* 5 */
          /***/
          function(ce, Y, A) {
            var T = A(0).FDLayoutNode, w = A(0).IMath;
            function L(U, P, K, D) {
              T.call(this, U, P, K, D);
            }
            L.prototype = Object.create(T.prototype);
            for (var G in T)
              L[G] = T[G];
            L.prototype.move = function() {
              var U = this.graphManager.getLayout();
              this.displacementX = U.coolingFactor * (this.springForceX + this.repulsionForceX + this.gravitationForceX) / this.noOfChildren, this.displacementY = U.coolingFactor * (this.springForceY + this.repulsionForceY + this.gravitationForceY) / this.noOfChildren, Math.abs(this.displacementX) > U.coolingFactor * U.maxNodeDisplacement && (this.displacementX = U.coolingFactor * U.maxNodeDisplacement * w.sign(this.displacementX)), Math.abs(this.displacementY) > U.coolingFactor * U.maxNodeDisplacement && (this.displacementY = U.coolingFactor * U.maxNodeDisplacement * w.sign(this.displacementY)), this.child == null ? this.moveBy(this.displacementX, this.displacementY) : this.child.getNodes().length == 0 ? this.moveBy(this.displacementX, this.displacementY) : this.propogateDisplacementToChildren(this.displacementX, this.displacementY), U.totalDisplacement += Math.abs(this.displacementX) + Math.abs(this.displacementY), this.springForceX = 0, this.springForceY = 0, this.repulsionForceX = 0, this.repulsionForceY = 0, this.gravitationForceX = 0, this.gravitationForceY = 0, this.displacementX = 0, this.displacementY = 0;
            }, L.prototype.propogateDisplacementToChildren = function(U, P) {
              for (var K = this.getChild().getNodes(), D, V = 0; V < K.length; V++)
                D = K[V], D.getChild() == null ? (D.moveBy(U, P), D.displacementX += U, D.displacementY += P) : D.propogateDisplacementToChildren(U, P);
            }, L.prototype.setPred1 = function(U) {
              this.pred1 = U;
            }, L.prototype.getPred1 = function() {
              return pred1;
            }, L.prototype.getPred2 = function() {
              return pred2;
            }, L.prototype.setNext = function(U) {
              this.next = U;
            }, L.prototype.getNext = function() {
              return next;
            }, L.prototype.setProcessed = function(U) {
              this.processed = U;
            }, L.prototype.isProcessed = function() {
              return processed;
            }, ce.exports = L;
          },
          /* 6 */
          /***/
          function(ce, Y, A) {
            var T = A(0).FDLayout, w = A(4), L = A(3), G = A(5), U = A(2), P = A(1), K = A(0).FDLayoutConstants, D = A(0).LayoutConstants, V = A(0).Point, _ = A(0).PointD, J = A(0).Layout, ne = A(0).Integer, ue = A(0).IGeometry, j = A(0).LGraph, ee = A(0).Transform;
            function H() {
              T.call(this), this.toBeTiled = {};
            }
            H.prototype = Object.create(T.prototype);
            for (var te in T)
              H[te] = T[te];
            H.prototype.newGraphManager = function() {
              var S = new w(this);
              return this.graphManager = S, S;
            }, H.prototype.newGraph = function(S) {
              return new L(null, this.graphManager, S);
            }, H.prototype.newNode = function(S) {
              return new G(this.graphManager, S);
            }, H.prototype.newEdge = function(S) {
              return new U(null, null, S);
            }, H.prototype.initParameters = function() {
              T.prototype.initParameters.call(this, arguments), this.isSubLayout || (P.DEFAULT_EDGE_LENGTH < 10 ? this.idealEdgeLength = 10 : this.idealEdgeLength = P.DEFAULT_EDGE_LENGTH, this.useSmartIdealEdgeLengthCalculation = P.DEFAULT_USE_SMART_IDEAL_EDGE_LENGTH_CALCULATION, this.springConstant = K.DEFAULT_SPRING_STRENGTH, this.repulsionConstant = K.DEFAULT_REPULSION_STRENGTH, this.gravityConstant = K.DEFAULT_GRAVITY_STRENGTH, this.compoundGravityConstant = K.DEFAULT_COMPOUND_GRAVITY_STRENGTH, this.gravityRangeFactor = K.DEFAULT_GRAVITY_RANGE_FACTOR, this.compoundGravityRangeFactor = K.DEFAULT_COMPOUND_GRAVITY_RANGE_FACTOR, this.prunedNodesAll = [], this.growTreeIterations = 0, this.afterGrowthIterations = 0, this.isTreeGrowing = !1, this.isGrowthFinished = !1, this.coolingCycle = 0, this.maxCoolingCycle = this.maxIterations / K.CONVERGENCE_CHECK_PERIOD, this.finalTemperature = K.CONVERGENCE_CHECK_PERIOD / this.maxIterations, this.coolingAdjuster = 1);
            }, H.prototype.layout = function() {
              var S = D.DEFAULT_CREATE_BENDS_AS_NEEDED;
              return S && (this.createBendpoints(), this.graphManager.resetAllEdges()), this.level = 0, this.classicLayout();
            }, H.prototype.classicLayout = function() {
              if (this.nodesWithGravity = this.calculateNodesToApplyGravitationTo(), this.graphManager.setAllNodesToApplyGravitation(this.nodesWithGravity), this.calcNoOfChildrenForAllNodes(), this.graphManager.calcLowestCommonAncestors(), this.graphManager.calcInclusionTreeDepths(), this.graphManager.getRoot().calcEstimatedSize(), this.calcIdealEdgeLengths(), this.incremental) {
                if (P.TREE_REDUCTION_ON_INCREMENTAL) {
                  this.reduceTrees(), this.graphManager.resetAllNodesToApplyGravitation();
                  var $ = new Set(this.getAllNodes()), k = this.nodesWithGravity.filter(function(pe) {
                    return $.has(pe);
                  });
                  this.graphManager.setAllNodesToApplyGravitation(k);
                }
              } else {
                var S = this.getFlatForest();
                if (S.length > 0)
                  this.positionNodesRadially(S);
                else {
                  this.reduceTrees(), this.graphManager.resetAllNodesToApplyGravitation();
                  var $ = new Set(this.getAllNodes()), k = this.nodesWithGravity.filter(function(q) {
                    return $.has(q);
                  });
                  this.graphManager.setAllNodesToApplyGravitation(k), this.positionNodesRandomly();
                }
              }
              return this.initSpringEmbedder(), this.runSpringEmbedder(), !0;
            }, H.prototype.tick = function() {
              if (this.totalIterations++, this.totalIterations === this.maxIterations && !this.isTreeGrowing && !this.isGrowthFinished)
                if (this.prunedNodesAll.length > 0)
                  this.isTreeGrowing = !0;
                else
                  return !0;
              if (this.totalIterations % K.CONVERGENCE_CHECK_PERIOD == 0 && !this.isTreeGrowing && !this.isGrowthFinished) {
                if (this.isConverged())
                  if (this.prunedNodesAll.length > 0)
                    this.isTreeGrowing = !0;
                  else
                    return !0;
                this.coolingCycle++, this.layoutQuality == 0 ? this.coolingAdjuster = this.coolingCycle : this.layoutQuality == 1 && (this.coolingAdjuster = this.coolingCycle / 3), this.coolingFactor = Math.max(this.initialCoolingFactor - Math.pow(this.coolingCycle, Math.log(100 * (this.initialCoolingFactor - this.finalTemperature)) / Math.log(this.maxCoolingCycle)) / 100 * this.coolingAdjuster, this.finalTemperature), this.animationPeriod = Math.ceil(this.initialAnimationPeriod * Math.sqrt(this.coolingFactor));
              }
              if (this.isTreeGrowing) {
                if (this.growTreeIterations % 10 == 0)
                  if (this.prunedNodesAll.length > 0) {
                    this.graphManager.updateBounds(), this.updateGrid(), this.growTree(this.prunedNodesAll), this.graphManager.resetAllNodesToApplyGravitation();
                    var S = new Set(this.getAllNodes()), $ = this.nodesWithGravity.filter(function(ve) {
                      return S.has(ve);
                    });
                    this.graphManager.setAllNodesToApplyGravitation($), this.graphManager.updateBounds(), this.updateGrid(), this.coolingFactor = K.DEFAULT_COOLING_FACTOR_INCREMENTAL;
                  } else
                    this.isTreeGrowing = !1, this.isGrowthFinished = !0;
                this.growTreeIterations++;
              }
              if (this.isGrowthFinished) {
                if (this.isConverged())
                  return !0;
                this.afterGrowthIterations % 10 == 0 && (this.graphManager.updateBounds(), this.updateGrid()), this.coolingFactor = K.DEFAULT_COOLING_FACTOR_INCREMENTAL * ((100 - this.afterGrowthIterations) / 100), this.afterGrowthIterations++;
              }
              var k = !this.isTreeGrowing && !this.isGrowthFinished, q = this.growTreeIterations % 10 == 1 && this.isTreeGrowing || this.afterGrowthIterations % 10 == 1 && this.isGrowthFinished;
              return this.totalDisplacement = 0, this.graphManager.updateBounds(), this.calcSpringForces(), this.calcRepulsionForces(k, q), this.calcGravitationalForces(), this.moveNodes(), this.animate(), !1;
            }, H.prototype.getPositionsData = function() {
              for (var S = this.graphManager.getAllNodes(), $ = {}, k = 0; k < S.length; k++) {
                var q = S[k].rect, ve = S[k].id;
                $[ve] = {
                  id: ve,
                  x: q.getCenterX(),
                  y: q.getCenterY(),
                  w: q.width,
                  h: q.height
                };
              }
              return $;
            }, H.prototype.runSpringEmbedder = function() {
              this.initialAnimationPeriod = 25, this.animationPeriod = this.initialAnimationPeriod;
              var S = !1;
              if (K.ANIMATE === "during")
                this.emit("layoutstarted");
              else {
                for (; !S; )
                  S = this.tick();
                this.graphManager.updateBounds();
              }
            }, H.prototype.calculateNodesToApplyGravitationTo = function() {
              var S = [], $, k = this.graphManager.getGraphs(), q = k.length, ve;
              for (ve = 0; ve < q; ve++)
                $ = k[ve], $.updateConnected(), $.isConnected || (S = S.concat($.getNodes()));
              return S;
            }, H.prototype.createBendpoints = function() {
              var S = [];
              S = S.concat(this.graphManager.getAllEdges());
              var $ = /* @__PURE__ */ new Set(), k;
              for (k = 0; k < S.length; k++) {
                var q = S[k];
                if (!$.has(q)) {
                  var ve = q.getSource(), pe = q.getTarget();
                  if (ve == pe)
                    q.getBendpoints().push(new _()), q.getBendpoints().push(new _()), this.createDummyNodesForBendpoints(q), $.add(q);
                  else {
                    var Ae = [];
                    if (Ae = Ae.concat(ve.getEdgeListToNode(pe)), Ae = Ae.concat(pe.getEdgeListToNode(ve)), !$.has(Ae[0])) {
                      if (Ae.length > 1) {
                        var Ne;
                        for (Ne = 0; Ne < Ae.length; Ne++) {
                          var _e = Ae[Ne];
                          _e.getBendpoints().push(new _()), this.createDummyNodesForBendpoints(_e);
                        }
                      }
                      Ae.forEach(function(tt) {
                        $.add(tt);
                      });
                    }
                  }
                }
                if ($.size == S.length)
                  break;
              }
            }, H.prototype.positionNodesRadially = function(S) {
              for (var $ = new V(0, 0), k = Math.ceil(Math.sqrt(S.length)), q = 0, ve = 0, pe = 0, Ae = new _(0, 0), Ne = 0; Ne < S.length; Ne++) {
                Ne % k == 0 && (pe = 0, ve = q, Ne != 0 && (ve += P.DEFAULT_COMPONENT_SEPERATION), q = 0);
                var _e = S[Ne], tt = J.findCenterOfTree(_e);
                $.x = pe, $.y = ve, Ae = H.radialLayout(_e, tt, $), Ae.y > q && (q = Math.floor(Ae.y)), pe = Math.floor(Ae.x + P.DEFAULT_COMPONENT_SEPERATION);
              }
              this.transform(new _(D.WORLD_CENTER_X - Ae.x / 2, D.WORLD_CENTER_Y - Ae.y / 2));
            }, H.radialLayout = function(S, $, k) {
              var q = Math.max(this.maxDiagonalInTree(S), P.DEFAULT_RADIAL_SEPARATION);
              H.branchRadialLayout($, null, 0, 359, 0, q);
              var ve = j.calculateBounds(S), pe = new ee();
              pe.setDeviceOrgX(ve.getMinX()), pe.setDeviceOrgY(ve.getMinY()), pe.setWorldOrgX(k.x), pe.setWorldOrgY(k.y);
              for (var Ae = 0; Ae < S.length; Ae++) {
                var Ne = S[Ae];
                Ne.transform(pe);
              }
              var _e = new _(ve.getMaxX(), ve.getMaxY());
              return pe.inverseTransformPoint(_e);
            }, H.branchRadialLayout = function(S, $, k, q, ve, pe) {
              var Ae = (q - k + 1) / 2;
              Ae < 0 && (Ae += 180);
              var Ne = (Ae + k) % 360, _e = Ne * ue.TWO_PI / 360, tt = ve * Math.cos(_e), ct = ve * Math.sin(_e);
              S.setCenter(tt, ct);
              var Pe = [];
              Pe = Pe.concat(S.getEdges());
              var $e = Pe.length;
              $ != null && $e--;
              for (var Xe = 0, rt = Pe.length, lt, nt = S.getEdgesBetween($); nt.length > 1; ) {
                var je = nt[0];
                nt.splice(0, 1);
                var pt = Pe.indexOf(je);
                pt >= 0 && Pe.splice(pt, 1), rt--, $e--;
              }
              $ != null ? lt = (Pe.indexOf(nt[0]) + 1) % rt : lt = 0;
              for (var Et = Math.abs(q - k) / $e, kt = lt; Xe != $e; kt = ++kt % rt) {
                var vt = Pe[kt].getOtherEnd(S);
                if (vt != $) {
                  var vr = (k + Xe * Et) % 360, qt = (vr + Et) % 360;
                  H.branchRadialLayout(vt, S, vr, qt, ve + pe, pe), Xe++;
                }
              }
            }, H.maxDiagonalInTree = function(S) {
              for (var $ = ne.MIN_VALUE, k = 0; k < S.length; k++) {
                var q = S[k], ve = q.getDiagonal();
                ve > $ && ($ = ve);
              }
              return $;
            }, H.prototype.calcRepulsionRange = function() {
              return 2 * (this.level + 1) * this.idealEdgeLength;
            }, H.prototype.groupZeroDegreeMembers = function() {
              var S = this, $ = {};
              this.memberGroups = {}, this.idToDummyNode = {};
              for (var k = [], q = this.graphManager.getAllNodes(), ve = 0; ve < q.length; ve++) {
                var pe = q[ve], Ae = pe.getParent();
                this.getNodeDegreeWithChildren(pe) === 0 && (Ae.id == null || !this.getToBeTiled(Ae)) && k.push(pe);
              }
              for (var ve = 0; ve < k.length; ve++) {
                var pe = k[ve], Ne = pe.getParent().id;
                typeof $[Ne] > "u" && ($[Ne] = []), $[Ne] = $[Ne].concat(pe);
              }
              Object.keys($).forEach(function(_e) {
                if ($[_e].length > 1) {
                  var tt = "DummyCompound_" + _e;
                  S.memberGroups[tt] = $[_e];
                  var ct = $[_e][0].getParent(), Pe = new G(S.graphManager);
                  Pe.id = tt, Pe.paddingLeft = ct.paddingLeft || 0, Pe.paddingRight = ct.paddingRight || 0, Pe.paddingBottom = ct.paddingBottom || 0, Pe.paddingTop = ct.paddingTop || 0, S.idToDummyNode[tt] = Pe;
                  var $e = S.getGraphManager().add(S.newGraph(), Pe), Xe = ct.getChild();
                  Xe.add(Pe);
                  for (var rt = 0; rt < $[_e].length; rt++) {
                    var lt = $[_e][rt];
                    Xe.remove(lt), $e.add(lt);
                  }
                }
              });
            }, H.prototype.clearCompounds = function() {
              var S = {}, $ = {};
              this.performDFSOnCompounds();
              for (var k = 0; k < this.compoundOrder.length; k++)
                $[this.compoundOrder[k].id] = this.compoundOrder[k], S[this.compoundOrder[k].id] = [].concat(this.compoundOrder[k].getChild().getNodes()), this.graphManager.remove(this.compoundOrder[k].getChild()), this.compoundOrder[k].child = null;
              this.graphManager.resetAllNodes(), this.tileCompoundMembers(S, $);
            }, H.prototype.clearZeroDegreeMembers = function() {
              var S = this, $ = this.tiledZeroDegreePack = [];
              Object.keys(this.memberGroups).forEach(function(k) {
                var q = S.idToDummyNode[k];
                $[k] = S.tileNodes(S.memberGroups[k], q.paddingLeft + q.paddingRight), q.rect.width = $[k].width, q.rect.height = $[k].height;
              });
            }, H.prototype.repopulateCompounds = function() {
              for (var S = this.compoundOrder.length - 1; S >= 0; S--) {
                var $ = this.compoundOrder[S], k = $.id, q = $.paddingLeft, ve = $.paddingTop;
                this.adjustLocations(this.tiledMemberPack[k], $.rect.x, $.rect.y, q, ve);
              }
            }, H.prototype.repopulateZeroDegreeMembers = function() {
              var S = this, $ = this.tiledZeroDegreePack;
              Object.keys($).forEach(function(k) {
                var q = S.idToDummyNode[k], ve = q.paddingLeft, pe = q.paddingTop;
                S.adjustLocations($[k], q.rect.x, q.rect.y, ve, pe);
              });
            }, H.prototype.getToBeTiled = function(S) {
              var $ = S.id;
              if (this.toBeTiled[$] != null)
                return this.toBeTiled[$];
              var k = S.getChild();
              if (k == null)
                return this.toBeTiled[$] = !1, !1;
              for (var q = k.getNodes(), ve = 0; ve < q.length; ve++) {
                var pe = q[ve];
                if (this.getNodeDegree(pe) > 0)
                  return this.toBeTiled[$] = !1, !1;
                if (pe.getChild() == null) {
                  this.toBeTiled[pe.id] = !1;
                  continue;
                }
                if (!this.getToBeTiled(pe))
                  return this.toBeTiled[$] = !1, !1;
              }
              return this.toBeTiled[$] = !0, !0;
            }, H.prototype.getNodeDegree = function(S) {
              S.id;
              for (var $ = S.getEdges(), k = 0, q = 0; q < $.length; q++) {
                var ve = $[q];
                ve.getSource().id !== ve.getTarget().id && (k = k + 1);
              }
              return k;
            }, H.prototype.getNodeDegreeWithChildren = function(S) {
              var $ = this.getNodeDegree(S);
              if (S.getChild() == null)
                return $;
              for (var k = S.getChild().getNodes(), q = 0; q < k.length; q++) {
                var ve = k[q];
                $ += this.getNodeDegreeWithChildren(ve);
              }
              return $;
            }, H.prototype.performDFSOnCompounds = function() {
              this.compoundOrder = [], this.fillCompexOrderByDFS(this.graphManager.getRoot().getNodes());
            }, H.prototype.fillCompexOrderByDFS = function(S) {
              for (var $ = 0; $ < S.length; $++) {
                var k = S[$];
                k.getChild() != null && this.fillCompexOrderByDFS(k.getChild().getNodes()), this.getToBeTiled(k) && this.compoundOrder.push(k);
              }
            }, H.prototype.adjustLocations = function(S, $, k, q, ve) {
              $ += q, k += ve;
              for (var pe = $, Ae = 0; Ae < S.rows.length; Ae++) {
                var Ne = S.rows[Ae];
                $ = pe;
                for (var _e = 0, tt = 0; tt < Ne.length; tt++) {
                  var ct = Ne[tt];
                  ct.rect.x = $, ct.rect.y = k, $ += ct.rect.width + S.horizontalPadding, ct.rect.height > _e && (_e = ct.rect.height);
                }
                k += _e + S.verticalPadding;
              }
            }, H.prototype.tileCompoundMembers = function(S, $) {
              var k = this;
              this.tiledMemberPack = [], Object.keys(S).forEach(function(q) {
                var ve = $[q];
                k.tiledMemberPack[q] = k.tileNodes(S[q], ve.paddingLeft + ve.paddingRight), ve.rect.width = k.tiledMemberPack[q].width, ve.rect.height = k.tiledMemberPack[q].height;
              });
            }, H.prototype.tileNodes = function(S, $) {
              var k = P.TILING_PADDING_VERTICAL, q = P.TILING_PADDING_HORIZONTAL, ve = {
                rows: [],
                rowWidth: [],
                rowHeight: [],
                width: 0,
                height: $,
                // assume minHeight equals to minWidth
                verticalPadding: k,
                horizontalPadding: q
              };
              S.sort(function(Ne, _e) {
                return Ne.rect.width * Ne.rect.height > _e.rect.width * _e.rect.height ? -1 : Ne.rect.width * Ne.rect.height < _e.rect.width * _e.rect.height ? 1 : 0;
              });
              for (var pe = 0; pe < S.length; pe++) {
                var Ae = S[pe];
                ve.rows.length == 0 ? this.insertNodeToRow(ve, Ae, 0, $) : this.canAddHorizontal(ve, Ae.rect.width, Ae.rect.height) ? this.insertNodeToRow(ve, Ae, this.getShortestRowIndex(ve), $) : this.insertNodeToRow(ve, Ae, ve.rows.length, $), this.shiftToLastRow(ve);
              }
              return ve;
            }, H.prototype.insertNodeToRow = function(S, $, k, q) {
              var ve = q;
              if (k == S.rows.length) {
                var pe = [];
                S.rows.push(pe), S.rowWidth.push(ve), S.rowHeight.push(0);
              }
              var Ae = S.rowWidth[k] + $.rect.width;
              S.rows[k].length > 0 && (Ae += S.horizontalPadding), S.rowWidth[k] = Ae, S.width < Ae && (S.width = Ae);
              var Ne = $.rect.height;
              k > 0 && (Ne += S.verticalPadding);
              var _e = 0;
              Ne > S.rowHeight[k] && (_e = S.rowHeight[k], S.rowHeight[k] = Ne, _e = S.rowHeight[k] - _e), S.height += _e, S.rows[k].push($);
            }, H.prototype.getShortestRowIndex = function(S) {
              for (var $ = -1, k = Number.MAX_VALUE, q = 0; q < S.rows.length; q++)
                S.rowWidth[q] < k && ($ = q, k = S.rowWidth[q]);
              return $;
            }, H.prototype.getLongestRowIndex = function(S) {
              for (var $ = -1, k = Number.MIN_VALUE, q = 0; q < S.rows.length; q++)
                S.rowWidth[q] > k && ($ = q, k = S.rowWidth[q]);
              return $;
            }, H.prototype.canAddHorizontal = function(S, $, k) {
              var q = this.getShortestRowIndex(S);
              if (q < 0)
                return !0;
              var ve = S.rowWidth[q];
              if (ve + S.horizontalPadding + $ <= S.width)
                return !0;
              var pe = 0;
              S.rowHeight[q] < k && q > 0 && (pe = k + S.verticalPadding - S.rowHeight[q]);
              var Ae;
              S.width - ve >= $ + S.horizontalPadding ? Ae = (S.height + pe) / (ve + $ + S.horizontalPadding) : Ae = (S.height + pe) / S.width, pe = k + S.verticalPadding;
              var Ne;
              return S.width < $ ? Ne = (S.height + pe) / $ : Ne = (S.height + pe) / S.width, Ne < 1 && (Ne = 1 / Ne), Ae < 1 && (Ae = 1 / Ae), Ae < Ne;
            }, H.prototype.shiftToLastRow = function(S) {
              var $ = this.getLongestRowIndex(S), k = S.rowWidth.length - 1, q = S.rows[$], ve = q[q.length - 1], pe = ve.width + S.horizontalPadding;
              if (S.width - S.rowWidth[k] > pe && $ != k) {
                q.splice(-1, 1), S.rows[k].push(ve), S.rowWidth[$] = S.rowWidth[$] - pe, S.rowWidth[k] = S.rowWidth[k] + pe, S.width = S.rowWidth[instance.getLongestRowIndex(S)];
                for (var Ae = Number.MIN_VALUE, Ne = 0; Ne < q.length; Ne++)
                  q[Ne].height > Ae && (Ae = q[Ne].height);
                $ > 0 && (Ae += S.verticalPadding);
                var _e = S.rowHeight[$] + S.rowHeight[k];
                S.rowHeight[$] = Ae, S.rowHeight[k] < ve.height + S.verticalPadding && (S.rowHeight[k] = ve.height + S.verticalPadding);
                var tt = S.rowHeight[$] + S.rowHeight[k];
                S.height += tt - _e, this.shiftToLastRow(S);
              }
            }, H.prototype.tilingPreLayout = function() {
              P.TILE && (this.groupZeroDegreeMembers(), this.clearCompounds(), this.clearZeroDegreeMembers());
            }, H.prototype.tilingPostLayout = function() {
              P.TILE && (this.repopulateZeroDegreeMembers(), this.repopulateCompounds());
            }, H.prototype.reduceTrees = function() {
              for (var S = [], $ = !0, k; $; ) {
                var q = this.graphManager.getAllNodes(), ve = [];
                $ = !1;
                for (var pe = 0; pe < q.length; pe++)
                  k = q[pe], k.getEdges().length == 1 && !k.getEdges()[0].isInterGraph && k.getChild() == null && (ve.push([k, k.getEdges()[0], k.getOwner()]), $ = !0);
                if ($ == !0) {
                  for (var Ae = [], Ne = 0; Ne < ve.length; Ne++)
                    ve[Ne][0].getEdges().length == 1 && (Ae.push(ve[Ne]), ve[Ne][0].getOwner().remove(ve[Ne][0]));
                  S.push(Ae), this.graphManager.resetAllNodes(), this.graphManager.resetAllEdges();
                }
              }
              this.prunedNodesAll = S;
            }, H.prototype.growTree = function(S) {
              for (var $ = S.length, k = S[$ - 1], q, ve = 0; ve < k.length; ve++)
                q = k[ve], this.findPlaceforPrunedNode(q), q[2].add(q[0]), q[2].add(q[1], q[1].source, q[1].target);
              S.splice(S.length - 1, 1), this.graphManager.resetAllNodes(), this.graphManager.resetAllEdges();
            }, H.prototype.findPlaceforPrunedNode = function(S) {
              var $, k, q = S[0];
              q == S[1].source ? k = S[1].target : k = S[1].source;
              var ve = k.startX, pe = k.finishX, Ae = k.startY, Ne = k.finishY, _e = 0, tt = 0, ct = 0, Pe = 0, $e = [_e, ct, tt, Pe];
              if (Ae > 0)
                for (var Xe = ve; Xe <= pe; Xe++)
                  $e[0] += this.grid[Xe][Ae - 1].length + this.grid[Xe][Ae].length - 1;
              if (pe < this.grid.length - 1)
                for (var Xe = Ae; Xe <= Ne; Xe++)
                  $e[1] += this.grid[pe + 1][Xe].length + this.grid[pe][Xe].length - 1;
              if (Ne < this.grid[0].length - 1)
                for (var Xe = ve; Xe <= pe; Xe++)
                  $e[2] += this.grid[Xe][Ne + 1].length + this.grid[Xe][Ne].length - 1;
              if (ve > 0)
                for (var Xe = Ae; Xe <= Ne; Xe++)
                  $e[3] += this.grid[ve - 1][Xe].length + this.grid[ve][Xe].length - 1;
              for (var rt = ne.MAX_VALUE, lt, nt, je = 0; je < $e.length; je++)
                $e[je] < rt ? (rt = $e[je], lt = 1, nt = je) : $e[je] == rt && lt++;
              if (lt == 3 && rt == 0)
                $e[0] == 0 && $e[1] == 0 && $e[2] == 0 ? $ = 1 : $e[0] == 0 && $e[1] == 0 && $e[3] == 0 ? $ = 0 : $e[0] == 0 && $e[2] == 0 && $e[3] == 0 ? $ = 3 : $e[1] == 0 && $e[2] == 0 && $e[3] == 0 && ($ = 2);
              else if (lt == 2 && rt == 0) {
                var pt = Math.floor(Math.random() * 2);
                $e[0] == 0 && $e[1] == 0 ? pt == 0 ? $ = 0 : $ = 1 : $e[0] == 0 && $e[2] == 0 ? pt == 0 ? $ = 0 : $ = 2 : $e[0] == 0 && $e[3] == 0 ? pt == 0 ? $ = 0 : $ = 3 : $e[1] == 0 && $e[2] == 0 ? pt == 0 ? $ = 1 : $ = 2 : $e[1] == 0 && $e[3] == 0 ? pt == 0 ? $ = 1 : $ = 3 : pt == 0 ? $ = 2 : $ = 3;
              } else if (lt == 4 && rt == 0) {
                var pt = Math.floor(Math.random() * 4);
                $ = pt;
              } else
                $ = nt;
              $ == 0 ? q.setCenter(k.getCenterX(), k.getCenterY() - k.getHeight() / 2 - K.DEFAULT_EDGE_LENGTH - q.getHeight() / 2) : $ == 1 ? q.setCenter(k.getCenterX() + k.getWidth() / 2 + K.DEFAULT_EDGE_LENGTH + q.getWidth() / 2, k.getCenterY()) : $ == 2 ? q.setCenter(k.getCenterX(), k.getCenterY() + k.getHeight() / 2 + K.DEFAULT_EDGE_LENGTH + q.getHeight() / 2) : q.setCenter(k.getCenterX() - k.getWidth() / 2 - K.DEFAULT_EDGE_LENGTH - q.getWidth() / 2, k.getCenterY());
            }, ce.exports = H;
          },
          /* 7 */
          /***/
          function(ce, Y, A) {
            var T = {};
            T.layoutBase = A(0), T.CoSEConstants = A(1), T.CoSEEdge = A(2), T.CoSEGraph = A(3), T.CoSEGraphManager = A(4), T.CoSELayout = A(6), T.CoSENode = A(5), ce.exports = T;
          }
          /******/
        ])
      );
    });
  }(Wp)), ti;
}
(function(fe, he) {
  (function(ce, Y) {
    fe.exports = Y(Qp());
  })(Ca, function(Q) {
    return (
      /******/
      function(ce) {
        var Y = {};
        function A(T) {
          if (Y[T])
            return Y[T].exports;
          var w = Y[T] = {
            /******/
            i: T,
            /******/
            l: !1,
            /******/
            exports: {}
            /******/
          };
          return ce[T].call(w.exports, w, w.exports, A), w.l = !0, w.exports;
        }
        return A.m = ce, A.c = Y, A.i = function(T) {
          return T;
        }, A.d = function(T, w, L) {
          A.o(T, w) || Object.defineProperty(T, w, {
            /******/
            configurable: !1,
            /******/
            enumerable: !0,
            /******/
            get: L
            /******/
          });
        }, A.n = function(T) {
          var w = T && T.__esModule ? (
            /******/
            function() {
              return T.default;
            }
          ) : (
            /******/
            function() {
              return T;
            }
          );
          return A.d(w, "a", w), w;
        }, A.o = function(T, w) {
          return Object.prototype.hasOwnProperty.call(T, w);
        }, A.p = "", A(A.s = 1);
      }([
        /* 0 */
        /***/
        function(ce, Y) {
          ce.exports = Q;
        },
        /* 1 */
        /***/
        function(ce, Y, A) {
          var T = A(0).layoutBase.LayoutConstants, w = A(0).layoutBase.FDLayoutConstants, L = A(0).CoSEConstants, G = A(0).CoSELayout, U = A(0).CoSENode, P = A(0).layoutBase.PointD, K = A(0).layoutBase.DimensionD, D = {
            // Called on `layoutready`
            ready: function() {
            },
            // Called on `layoutstop`
            stop: function() {
            },
            // 'draft', 'default' or 'proof" 
            // - 'draft' fast cooling rate 
            // - 'default' moderate cooling rate 
            // - "proof" slow cooling rate
            quality: "default",
            // include labels in node dimensions
            nodeDimensionsIncludeLabels: !1,
            // number of ticks per frame; higher is faster but more jerky
            refresh: 30,
            // Whether to fit the network view after when done
            fit: !0,
            // Padding on fit
            padding: 10,
            // Whether to enable incremental mode
            randomize: !0,
            // Node repulsion (non overlapping) multiplier
            nodeRepulsion: 4500,
            // Ideal edge (non nested) length
            idealEdgeLength: 50,
            // Divisor to compute edge forces
            edgeElasticity: 0.45,
            // Nesting factor (multiplier) to compute ideal edge length for nested edges
            nestingFactor: 0.1,
            // Gravity force (constant)
            gravity: 0.25,
            // Maximum number of iterations to perform
            numIter: 2500,
            // For enabling tiling
            tile: !0,
            // Type of layout animation. The option set is {'during', 'end', false}
            animate: "end",
            // Duration for animate:end
            animationDuration: 500,
            // Represents the amount of the vertical space to put between the zero degree members during the tiling operation(can also be a function)
            tilingPaddingVertical: 10,
            // Represents the amount of the horizontal space to put between the zero degree members during the tiling operation(can also be a function)
            tilingPaddingHorizontal: 10,
            // Gravity range (constant) for compounds
            gravityRangeCompound: 1.5,
            // Gravity force (constant) for compounds
            gravityCompound: 1,
            // Gravity range (constant)
            gravityRange: 3.8,
            // Initial cooling factor for incremental layout
            initialEnergyOnIncremental: 0.5
          };
          function V(ue, j) {
            var ee = {};
            for (var H in ue)
              ee[H] = ue[H];
            for (var H in j)
              ee[H] = j[H];
            return ee;
          }
          function _(ue) {
            this.options = V(D, ue), J(this.options);
          }
          var J = function(j) {
            j.nodeRepulsion != null && (L.DEFAULT_REPULSION_STRENGTH = w.DEFAULT_REPULSION_STRENGTH = j.nodeRepulsion), j.idealEdgeLength != null && (L.DEFAULT_EDGE_LENGTH = w.DEFAULT_EDGE_LENGTH = j.idealEdgeLength), j.edgeElasticity != null && (L.DEFAULT_SPRING_STRENGTH = w.DEFAULT_SPRING_STRENGTH = j.edgeElasticity), j.nestingFactor != null && (L.PER_LEVEL_IDEAL_EDGE_LENGTH_FACTOR = w.PER_LEVEL_IDEAL_EDGE_LENGTH_FACTOR = j.nestingFactor), j.gravity != null && (L.DEFAULT_GRAVITY_STRENGTH = w.DEFAULT_GRAVITY_STRENGTH = j.gravity), j.numIter != null && (L.MAX_ITERATIONS = w.MAX_ITERATIONS = j.numIter), j.gravityRange != null && (L.DEFAULT_GRAVITY_RANGE_FACTOR = w.DEFAULT_GRAVITY_RANGE_FACTOR = j.gravityRange), j.gravityCompound != null && (L.DEFAULT_COMPOUND_GRAVITY_STRENGTH = w.DEFAULT_COMPOUND_GRAVITY_STRENGTH = j.gravityCompound), j.gravityRangeCompound != null && (L.DEFAULT_COMPOUND_GRAVITY_RANGE_FACTOR = w.DEFAULT_COMPOUND_GRAVITY_RANGE_FACTOR = j.gravityRangeCompound), j.initialEnergyOnIncremental != null && (L.DEFAULT_COOLING_FACTOR_INCREMENTAL = w.DEFAULT_COOLING_FACTOR_INCREMENTAL = j.initialEnergyOnIncremental), j.quality == "draft" ? T.QUALITY = 0 : j.quality == "proof" ? T.QUALITY = 2 : T.QUALITY = 1, L.NODE_DIMENSIONS_INCLUDE_LABELS = w.NODE_DIMENSIONS_INCLUDE_LABELS = T.NODE_DIMENSIONS_INCLUDE_LABELS = j.nodeDimensionsIncludeLabels, L.DEFAULT_INCREMENTAL = w.DEFAULT_INCREMENTAL = T.DEFAULT_INCREMENTAL = !j.randomize, L.ANIMATE = w.ANIMATE = T.ANIMATE = j.animate, L.TILE = j.tile, L.TILING_PADDING_VERTICAL = typeof j.tilingPaddingVertical == "function" ? j.tilingPaddingVertical.call() : j.tilingPaddingVertical, L.TILING_PADDING_HORIZONTAL = typeof j.tilingPaddingHorizontal == "function" ? j.tilingPaddingHorizontal.call() : j.tilingPaddingHorizontal;
          };
          _.prototype.run = function() {
            var ue, j, ee = this.options;
            this.idToLNode = {};
            var H = this.layout = new G(), te = this;
            te.stopped = !1, this.cy = this.options.cy, this.cy.trigger({ type: "layoutstart", layout: this });
            var S = H.newGraphManager();
            this.gm = S;
            var $ = this.options.eles.nodes(), k = this.options.eles.edges();
            this.root = S.addRoot(), this.processChildrenList(this.root, this.getTopMostNodes($), H);
            for (var q = 0; q < k.length; q++) {
              var ve = k[q], pe = this.idToLNode[ve.data("source")], Ae = this.idToLNode[ve.data("target")];
              if (pe !== Ae && pe.getEdgesBetween(Ae).length == 0) {
                var Ne = S.add(H.newEdge(), pe, Ae);
                Ne.id = ve.id();
              }
            }
            var _e = function(Pe, $e) {
              typeof Pe == "number" && (Pe = $e);
              var Xe = Pe.data("id"), rt = te.idToLNode[Xe];
              return {
                x: rt.getRect().getCenterX(),
                y: rt.getRect().getCenterY()
              };
            }, tt = function ct() {
              for (var Pe = function() {
                ee.fit && ee.cy.fit(ee.eles, ee.padding), ue || (ue = !0, te.cy.one("layoutready", ee.ready), te.cy.trigger({ type: "layoutready", layout: te }));
              }, $e = te.options.refresh, Xe, rt = 0; rt < $e && !Xe; rt++)
                Xe = te.stopped || te.layout.tick();
              if (Xe) {
                H.checkLayoutSuccess() && !H.isSubLayout && H.doPostLayout(), H.tilingPostLayout && H.tilingPostLayout(), H.isLayoutFinished = !0, te.options.eles.nodes().positions(_e), Pe(), te.cy.one("layoutstop", te.options.stop), te.cy.trigger({ type: "layoutstop", layout: te }), j && cancelAnimationFrame(j), ue = !1;
                return;
              }
              var lt = te.layout.getPositionsData();
              ee.eles.nodes().positions(function(nt, je) {
                if (typeof nt == "number" && (nt = je), !nt.isParent()) {
                  for (var pt = nt.id(), Et = lt[pt], kt = nt; Et == null && (Et = lt[kt.data("parent")] || lt["DummyCompound_" + kt.data("parent")], lt[pt] = Et, kt = kt.parent()[0], kt != null); )
                    ;
                  return Et != null ? {
                    x: Et.x,
                    y: Et.y
                  } : {
                    x: nt.position("x"),
                    y: nt.position("y")
                  };
                }
              }), Pe(), j = requestAnimationFrame(ct);
            };
            return H.addListener("layoutstarted", function() {
              te.options.animate === "during" && (j = requestAnimationFrame(tt));
            }), H.runLayout(), this.options.animate !== "during" && (te.options.eles.nodes().not(":parent").layoutPositions(te, te.options, _e), ue = !1), this;
          }, _.prototype.getTopMostNodes = function(ue) {
            for (var j = {}, ee = 0; ee < ue.length; ee++)
              j[ue[ee].id()] = !0;
            var H = ue.filter(function(te, S) {
              typeof te == "number" && (te = S);
              for (var $ = te.parent()[0]; $ != null; ) {
                if (j[$.id()])
                  return !1;
                $ = $.parent()[0];
              }
              return !0;
            });
            return H;
          }, _.prototype.processChildrenList = function(ue, j, ee) {
            for (var H = j.length, te = 0; te < H; te++) {
              var S = j[te], $ = S.children(), k, q = S.layoutDimensions({
                nodeDimensionsIncludeLabels: this.options.nodeDimensionsIncludeLabels
              });
              if (S.outerWidth() != null && S.outerHeight() != null ? k = ue.add(new U(ee.graphManager, new P(S.position("x") - q.w / 2, S.position("y") - q.h / 2), new K(parseFloat(q.w), parseFloat(q.h)))) : k = ue.add(new U(this.graphManager)), k.id = S.data("id"), k.paddingLeft = parseInt(S.css("padding")), k.paddingTop = parseInt(S.css("padding")), k.paddingRight = parseInt(S.css("padding")), k.paddingBottom = parseInt(S.css("padding")), this.options.nodeDimensionsIncludeLabels && S.isParent()) {
                var ve = S.boundingBox({ includeLabels: !0, includeNodes: !1 }).w, pe = S.boundingBox({ includeLabels: !0, includeNodes: !1 }).h, Ae = S.css("text-halign");
                k.labelWidth = ve, k.labelHeight = pe, k.labelPos = Ae;
              }
              if (this.idToLNode[S.data("id")] = k, isNaN(k.rect.x) && (k.rect.x = 0), isNaN(k.rect.y) && (k.rect.y = 0), $ != null && $.length > 0) {
                var Ne;
                Ne = ee.getGraphManager().add(ee.newGraph(), k), this.processChildrenList(Ne, $, ee);
              }
            }
          }, _.prototype.stop = function() {
            return this.stopped = !0, this;
          };
          var ne = function(j) {
            j("layout", "cose-bilkent", _);
          };
          typeof cytoscape < "u" && ne(cytoscape), ce.exports = ne;
        }
        /******/
      ])
    );
  });
})(qp);
const Jp = /* @__PURE__ */ mp(Qi);
Wu.use(Jp);
function Ku(fe, he, Q, ce) {
  qu.drawNode(fe, he, Q, ce), he.children && he.children.forEach((Y, A) => {
    Ku(fe, Y, Q < 0 ? A : Q, ce);
  });
}
function jp(fe, he) {
  he.edges().map((Q, ce) => {
    const Y = Q.data();
    if (Q[0]._private.bodyBounds) {
      const A = Q[0]._private.rscratch;
      qr.trace("Edge: ", ce, Y), fe.insert("path").attr(
        "d",
        `M ${A.startX},${A.startY} L ${A.midX},${A.midY} L${A.endX},${A.endY} `
      ).attr("class", "edge section-edge-" + Y.section + " edge-depth-" + Y.depth);
    }
  });
}
function Zu(fe, he, Q, ce) {
  he.add({
    group: "nodes",
    data: {
      id: fe.id,
      labelText: fe.descr,
      height: fe.height,
      width: fe.width,
      level: ce,
      nodeId: fe.id,
      padding: fe.padding,
      type: fe.type
    },
    position: {
      x: fe.x,
      y: fe.y
    }
  }), fe.children && fe.children.forEach((Y) => {
    Zu(Y, he, Q, ce + 1), he.add({
      group: "edges",
      data: {
        id: `${fe.id}_${Y.id}`,
        source: fe.id,
        target: Y.id,
        depth: ce,
        section: Y.section
      }
    });
  });
}
function ey(fe, he) {
  return new Promise((Q) => {
    const ce = nn("body").append("div").attr("id", "cy").attr("style", "display:none"), Y = Wu({
      container: document.getElementById("cy"),
      // container to render in
      style: [
        {
          selector: "edge",
          style: {
            "curve-style": "bezier"
          }
        }
      ]
    });
    ce.remove(), Zu(fe, Y, he, 0), Y.nodes().forEach(function(A) {
      A.layoutDimensions = () => {
        const T = A.data();
        return { w: T.width, h: T.height };
      };
    }), Y.layout({
      name: "cose-bilkent",
      quality: "proof",
      // headless: true,
      styleEnabled: !1,
      animate: !1
    }).run(), Y.ready((A) => {
      qr.info("Ready", A), Q(Y);
    });
  });
}
function ty(fe) {
  fe.nodes().map((he, Q) => {
    const ce = he.data();
    ce.x = he.position().x, ce.y = he.position().y, qu.positionNode(ce);
    const Y = ji(ce.nodeId);
    qr.info("Id:", Q, "Position: (", he.position().x, ", ", he.position().y, ")", ce), Y.attr(
      "transform",
      `translate(${he.position().x - ce.width / 2}, ${he.position().y - ce.height / 2})`
    ), Y.attr("attr", `apa-${Q})`);
  });
}
const ry = async (fe, he, Q, ce) => {
  const Y = sn();
  ce.db.clear(), ce.parser.parse(fe), qr.debug(`Renering info diagram
` + fe);
  const A = sn().securityLevel;
  let T;
  A === "sandbox" && (T = nn("#i" + he));
  const L = (A === "sandbox" ? nn(T.nodes()[0].contentDocument.body) : nn("body")).select("#" + he);
  L.append("g");
  const G = ce.db.getMindmap(), U = L.append("g");
  U.attr("class", "mindmap-edges");
  const P = L.append("g");
  P.attr("class", "mindmap-nodes"), Ku(P, G, -1, Y);
  const K = await ey(G, Y);
  jp(U, K), ty(K), wp(void 0, L, Y.mindmap.padding, Y.mindmap.useMaxWidth);
}, ay = {
  draw: ry
}, ny = (fe) => {
  let he = "";
  for (let Q = 0; Q < fe.THEME_COLOR_LIMIT; Q++)
    fe["lineColor" + Q] = fe["lineColor" + Q] || fe["cScaleInv" + Q], xp(fe["lineColor" + Q]) ? fe["lineColor" + Q] = bp(fe["lineColor" + Q], 20) : fe["lineColor" + Q] = Ep(fe["lineColor" + Q], 20);
  for (let Q = 0; Q < fe.THEME_COLOR_LIMIT; Q++) {
    const ce = "" + (17 - 3 * Q);
    he += `
    .section-${Q - 1} rect, .section-${Q - 1} path, .section-${Q - 1} circle, .section-${Q - 1} polygon, .section-${Q - 1} path  {
      fill: ${fe["cScale" + Q]};
    }
    .section-${Q - 1} text {
     fill: ${fe["cScaleLabel" + Q]};
    }
    .node-icon-${Q - 1} {
      font-size: 40px;
      color: ${fe["cScaleLabel" + Q]};
    }
    .section-edge-${Q - 1}{
      stroke: ${fe["cScale" + Q]};
    }
    .edge-depth-${Q - 1}{
      stroke-width: ${ce};
    }
    .section-${Q - 1} line {
      stroke: ${fe["cScaleInv" + Q]} ;
      stroke-width: 3;
    }

    .disabled, .disabled circle, .disabled text {
      fill: lightgray;
    }
    .disabled text {
      fill: #efefef;
    }
    `;
  }
  return he;
}, iy = (fe) => `
  .edge {
    stroke-width: 3;
  }
  ${ny(fe)}
  .section-root rect, .section-root path, .section-root circle, .section-root polygon  {
    fill: ${fe.git0};
  }
  .section-root text {
    fill: ${fe.gitBranchLabel0};
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
`, sy = iy, fy = {
  db: Rp,
  renderer: ay,
  parser: Tp,
  styles: sy
};
export {
  fy as diagram
};
//# sourceMappingURL=mindmap-definition-9c087979.js.map
