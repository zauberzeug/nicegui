import {
  getDiagramElement,
  setupViewPortForSVG
} from "./chunk-GVMN75T7.mjs";
import {
  render
} from "./chunk-M7N4Q5GZ.mjs";
import {
  generateId,
  utils_default
} from "./chunk-I7ZFS43C.mjs";
import {
  clear,
  common_default,
  getAccDescription,
  getAccTitle,
  getConfig2 as getConfig,
  getDiagramTitle,
  log,
  setAccDescription,
  setAccTitle,
  setDiagramTitle
} from "./chunk-DD37ZF33.mjs";
import {
  __name
} from "./chunk-DLQEHMXD.mjs";

// src/diagrams/state/parser/stateDiagram.jison
var parser = function() {
  var o = /* @__PURE__ */ __name(function(k, v, o2, l) {
    for (o2 = o2 || {}, l = k.length; l--; o2[k[l]] = v) ;
    return o2;
  }, "o"), $V0 = [1, 2], $V1 = [1, 3], $V2 = [1, 4], $V3 = [2, 4], $V4 = [1, 9], $V5 = [1, 11], $V6 = [1, 16], $V7 = [1, 17], $V8 = [1, 18], $V9 = [1, 19], $Va = [1, 32], $Vb = [1, 20], $Vc = [1, 21], $Vd = [1, 22], $Ve = [1, 23], $Vf = [1, 24], $Vg = [1, 26], $Vh = [1, 27], $Vi = [1, 28], $Vj = [1, 29], $Vk = [1, 30], $Vl = [1, 31], $Vm = [1, 34], $Vn = [1, 35], $Vo = [1, 36], $Vp = [1, 37], $Vq = [1, 33], $Vr = [1, 4, 5, 16, 17, 19, 21, 22, 24, 25, 26, 27, 28, 29, 33, 35, 37, 38, 42, 45, 48, 49, 50, 51, 54], $Vs = [1, 4, 5, 14, 15, 16, 17, 19, 21, 22, 24, 25, 26, 27, 28, 29, 33, 35, 37, 38, 42, 45, 48, 49, 50, 51, 54], $Vt = [4, 5, 16, 17, 19, 21, 22, 24, 25, 26, 27, 28, 29, 33, 35, 37, 38, 42, 45, 48, 49, 50, 51, 54];
  var parser2 = {
    trace: /* @__PURE__ */ __name(function trace() {
    }, "trace"),
    yy: {},
    symbols_: { "error": 2, "start": 3, "SPACE": 4, "NL": 5, "SD": 6, "document": 7, "line": 8, "statement": 9, "classDefStatement": 10, "styleStatement": 11, "cssClassStatement": 12, "idStatement": 13, "DESCR": 14, "-->": 15, "HIDE_EMPTY": 16, "scale": 17, "WIDTH": 18, "COMPOSIT_STATE": 19, "STRUCT_START": 20, "STRUCT_STOP": 21, "STATE_DESCR": 22, "AS": 23, "ID": 24, "FORK": 25, "JOIN": 26, "CHOICE": 27, "CONCURRENT": 28, "note": 29, "notePosition": 30, "NOTE_TEXT": 31, "direction": 32, "acc_title": 33, "acc_title_value": 34, "acc_descr": 35, "acc_descr_value": 36, "acc_descr_multiline_value": 37, "classDef": 38, "CLASSDEF_ID": 39, "CLASSDEF_STYLEOPTS": 40, "DEFAULT": 41, "style": 42, "STYLE_IDS": 43, "STYLEDEF_STYLEOPTS": 44, "class": 45, "CLASSENTITY_IDS": 46, "STYLECLASS": 47, "direction_tb": 48, "direction_bt": 49, "direction_rl": 50, "direction_lr": 51, "eol": 52, ";": 53, "EDGE_STATE": 54, "STYLE_SEPARATOR": 55, "left_of": 56, "right_of": 57, "$accept": 0, "$end": 1 },
    terminals_: { 2: "error", 4: "SPACE", 5: "NL", 6: "SD", 14: "DESCR", 15: "-->", 16: "HIDE_EMPTY", 17: "scale", 18: "WIDTH", 19: "COMPOSIT_STATE", 20: "STRUCT_START", 21: "STRUCT_STOP", 22: "STATE_DESCR", 23: "AS", 24: "ID", 25: "FORK", 26: "JOIN", 27: "CHOICE", 28: "CONCURRENT", 29: "note", 31: "NOTE_TEXT", 33: "acc_title", 34: "acc_title_value", 35: "acc_descr", 36: "acc_descr_value", 37: "acc_descr_multiline_value", 38: "classDef", 39: "CLASSDEF_ID", 40: "CLASSDEF_STYLEOPTS", 41: "DEFAULT", 42: "style", 43: "STYLE_IDS", 44: "STYLEDEF_STYLEOPTS", 45: "class", 46: "CLASSENTITY_IDS", 47: "STYLECLASS", 48: "direction_tb", 49: "direction_bt", 50: "direction_rl", 51: "direction_lr", 53: ";", 54: "EDGE_STATE", 55: "STYLE_SEPARATOR", 56: "left_of", 57: "right_of" },
    productions_: [0, [3, 2], [3, 2], [3, 2], [7, 0], [7, 2], [8, 2], [8, 1], [8, 1], [9, 1], [9, 1], [9, 1], [9, 1], [9, 2], [9, 3], [9, 4], [9, 1], [9, 2], [9, 1], [9, 4], [9, 3], [9, 6], [9, 1], [9, 1], [9, 1], [9, 1], [9, 4], [9, 4], [9, 1], [9, 2], [9, 2], [9, 1], [10, 3], [10, 3], [11, 3], [12, 3], [32, 1], [32, 1], [32, 1], [32, 1], [52, 1], [52, 1], [13, 1], [13, 1], [13, 3], [13, 3], [30, 1], [30, 1]],
    performAction: /* @__PURE__ */ __name(function anonymous(yytext, yyleng, yylineno, yy, yystate, $$, _$) {
      var $0 = $$.length - 1;
      switch (yystate) {
        case 3:
          yy.setRootDoc($$[$0]);
          return $$[$0];
          break;
        case 4:
          this.$ = [];
          break;
        case 5:
          if ($$[$0] != "nl") {
            $$[$0 - 1].push($$[$0]);
            this.$ = $$[$0 - 1];
          }
          break;
        case 6:
        case 7:
          this.$ = $$[$0];
          break;
        case 8:
          this.$ = "nl";
          break;
        case 12:
          this.$ = $$[$0];
          break;
        case 13:
          const stateStmt = $$[$0 - 1];
          stateStmt.description = yy.trimColon($$[$0]);
          this.$ = stateStmt;
          break;
        case 14:
          this.$ = { stmt: "relation", state1: $$[$0 - 2], state2: $$[$0] };
          break;
        case 15:
          const relDescription = yy.trimColon($$[$0]);
          this.$ = { stmt: "relation", state1: $$[$0 - 3], state2: $$[$0 - 1], description: relDescription };
          break;
        case 19:
          this.$ = { stmt: "state", id: $$[$0 - 3], type: "default", description: "", doc: $$[$0 - 1] };
          break;
        case 20:
          var id = $$[$0];
          var description = $$[$0 - 2].trim();
          if ($$[$0].match(":")) {
            var parts = $$[$0].split(":");
            id = parts[0];
            description = [description, parts[1]];
          }
          this.$ = { stmt: "state", id, type: "default", description };
          break;
        case 21:
          this.$ = { stmt: "state", id: $$[$0 - 3], type: "default", description: $$[$0 - 5], doc: $$[$0 - 1] };
          break;
        case 22:
          this.$ = { stmt: "state", id: $$[$0], type: "fork" };
          break;
        case 23:
          this.$ = { stmt: "state", id: $$[$0], type: "join" };
          break;
        case 24:
          this.$ = { stmt: "state", id: $$[$0], type: "choice" };
          break;
        case 25:
          this.$ = { stmt: "state", id: yy.getDividerId(), type: "divider" };
          break;
        case 26:
          this.$ = { stmt: "state", id: $$[$0 - 1].trim(), note: { position: $$[$0 - 2].trim(), text: $$[$0].trim() } };
          break;
        case 29:
          this.$ = $$[$0].trim();
          yy.setAccTitle(this.$);
          break;
        case 30:
        case 31:
          this.$ = $$[$0].trim();
          yy.setAccDescription(this.$);
          break;
        case 32:
        case 33:
          this.$ = { stmt: "classDef", id: $$[$0 - 1].trim(), classes: $$[$0].trim() };
          break;
        case 34:
          this.$ = { stmt: "style", id: $$[$0 - 1].trim(), styleClass: $$[$0].trim() };
          break;
        case 35:
          this.$ = { stmt: "applyClass", id: $$[$0 - 1].trim(), styleClass: $$[$0].trim() };
          break;
        case 36:
          yy.setDirection("TB");
          this.$ = { stmt: "dir", value: "TB" };
          break;
        case 37:
          yy.setDirection("BT");
          this.$ = { stmt: "dir", value: "BT" };
          break;
        case 38:
          yy.setDirection("RL");
          this.$ = { stmt: "dir", value: "RL" };
          break;
        case 39:
          yy.setDirection("LR");
          this.$ = { stmt: "dir", value: "LR" };
          break;
        case 42:
        case 43:
          this.$ = { stmt: "state", id: $$[$0].trim(), type: "default", description: "" };
          break;
        case 44:
          this.$ = { stmt: "state", id: $$[$0 - 2].trim(), classes: [$$[$0].trim()], type: "default", description: "" };
          break;
        case 45:
          this.$ = { stmt: "state", id: $$[$0 - 2].trim(), classes: [$$[$0].trim()], type: "default", description: "" };
          break;
      }
    }, "anonymous"),
    table: [{ 3: 1, 4: $V0, 5: $V1, 6: $V2 }, { 1: [3] }, { 3: 5, 4: $V0, 5: $V1, 6: $V2 }, { 3: 6, 4: $V0, 5: $V1, 6: $V2 }, o([1, 4, 5, 16, 17, 19, 22, 24, 25, 26, 27, 28, 29, 33, 35, 37, 38, 42, 45, 48, 49, 50, 51, 54], $V3, { 7: 7 }), { 1: [2, 1] }, { 1: [2, 2] }, { 1: [2, 3], 4: $V4, 5: $V5, 8: 8, 9: 10, 10: 12, 11: 13, 12: 14, 13: 15, 16: $V6, 17: $V7, 19: $V8, 22: $V9, 24: $Va, 25: $Vb, 26: $Vc, 27: $Vd, 28: $Ve, 29: $Vf, 32: 25, 33: $Vg, 35: $Vh, 37: $Vi, 38: $Vj, 42: $Vk, 45: $Vl, 48: $Vm, 49: $Vn, 50: $Vo, 51: $Vp, 54: $Vq }, o($Vr, [2, 5]), { 9: 38, 10: 12, 11: 13, 12: 14, 13: 15, 16: $V6, 17: $V7, 19: $V8, 22: $V9, 24: $Va, 25: $Vb, 26: $Vc, 27: $Vd, 28: $Ve, 29: $Vf, 32: 25, 33: $Vg, 35: $Vh, 37: $Vi, 38: $Vj, 42: $Vk, 45: $Vl, 48: $Vm, 49: $Vn, 50: $Vo, 51: $Vp, 54: $Vq }, o($Vr, [2, 7]), o($Vr, [2, 8]), o($Vr, [2, 9]), o($Vr, [2, 10]), o($Vr, [2, 11]), o($Vr, [2, 12], { 14: [1, 39], 15: [1, 40] }), o($Vr, [2, 16]), { 18: [1, 41] }, o($Vr, [2, 18], { 20: [1, 42] }), { 23: [1, 43] }, o($Vr, [2, 22]), o($Vr, [2, 23]), o($Vr, [2, 24]), o($Vr, [2, 25]), { 30: 44, 31: [1, 45], 56: [1, 46], 57: [1, 47] }, o($Vr, [2, 28]), { 34: [1, 48] }, { 36: [1, 49] }, o($Vr, [2, 31]), { 39: [1, 50], 41: [1, 51] }, { 43: [1, 52] }, { 46: [1, 53] }, o($Vs, [2, 42], { 55: [1, 54] }), o($Vs, [2, 43], { 55: [1, 55] }), o($Vr, [2, 36]), o($Vr, [2, 37]), o($Vr, [2, 38]), o($Vr, [2, 39]), o($Vr, [2, 6]), o($Vr, [2, 13]), { 13: 56, 24: $Va, 54: $Vq }, o($Vr, [2, 17]), o($Vt, $V3, { 7: 57 }), { 24: [1, 58] }, { 24: [1, 59] }, { 23: [1, 60] }, { 24: [2, 46] }, { 24: [2, 47] }, o($Vr, [2, 29]), o($Vr, [2, 30]), { 40: [1, 61] }, { 40: [1, 62] }, { 44: [1, 63] }, { 47: [1, 64] }, { 24: [1, 65] }, { 24: [1, 66] }, o($Vr, [2, 14], { 14: [1, 67] }), { 4: $V4, 5: $V5, 8: 8, 9: 10, 10: 12, 11: 13, 12: 14, 13: 15, 16: $V6, 17: $V7, 19: $V8, 21: [1, 68], 22: $V9, 24: $Va, 25: $Vb, 26: $Vc, 27: $Vd, 28: $Ve, 29: $Vf, 32: 25, 33: $Vg, 35: $Vh, 37: $Vi, 38: $Vj, 42: $Vk, 45: $Vl, 48: $Vm, 49: $Vn, 50: $Vo, 51: $Vp, 54: $Vq }, o($Vr, [2, 20], { 20: [1, 69] }), { 31: [1, 70] }, { 24: [1, 71] }, o($Vr, [2, 32]), o($Vr, [2, 33]), o($Vr, [2, 34]), o($Vr, [2, 35]), o($Vs, [2, 44]), o($Vs, [2, 45]), o($Vr, [2, 15]), o($Vr, [2, 19]), o($Vt, $V3, { 7: 72 }), o($Vr, [2, 26]), o($Vr, [2, 27]), { 4: $V4, 5: $V5, 8: 8, 9: 10, 10: 12, 11: 13, 12: 14, 13: 15, 16: $V6, 17: $V7, 19: $V8, 21: [1, 73], 22: $V9, 24: $Va, 25: $Vb, 26: $Vc, 27: $Vd, 28: $Ve, 29: $Vf, 32: 25, 33: $Vg, 35: $Vh, 37: $Vi, 38: $Vj, 42: $Vk, 45: $Vl, 48: $Vm, 49: $Vn, 50: $Vo, 51: $Vp, 54: $Vq }, o($Vr, [2, 21])],
    defaultActions: { 5: [2, 1], 6: [2, 2], 46: [2, 46], 47: [2, 47] },
    parseError: /* @__PURE__ */ __name(function parseError(str, hash) {
      if (hash.recoverable) {
        this.trace(str);
      } else {
        var error = new Error(str);
        error.hash = hash;
        throw error;
      }
    }, "parseError"),
    parse: /* @__PURE__ */ __name(function parse(input) {
      var self = this, stack = [0], tstack = [], vstack = [null], lstack = [], table = this.table, yytext = "", yylineno = 0, yyleng = 0, recovering = 0, TERROR = 2, EOF = 1;
      var args = lstack.slice.call(arguments, 1);
      var lexer2 = Object.create(this.lexer);
      var sharedState = { yy: {} };
      for (var k in this.yy) {
        if (Object.prototype.hasOwnProperty.call(this.yy, k)) {
          sharedState.yy[k] = this.yy[k];
        }
      }
      lexer2.setInput(input, sharedState.yy);
      sharedState.yy.lexer = lexer2;
      sharedState.yy.parser = this;
      if (typeof lexer2.yylloc == "undefined") {
        lexer2.yylloc = {};
      }
      var yyloc = lexer2.yylloc;
      lstack.push(yyloc);
      var ranges = lexer2.options && lexer2.options.ranges;
      if (typeof sharedState.yy.parseError === "function") {
        this.parseError = sharedState.yy.parseError;
      } else {
        this.parseError = Object.getPrototypeOf(this).parseError;
      }
      function popStack(n) {
        stack.length = stack.length - 2 * n;
        vstack.length = vstack.length - n;
        lstack.length = lstack.length - n;
      }
      __name(popStack, "popStack");
      function lex() {
        var token;
        token = tstack.pop() || lexer2.lex() || EOF;
        if (typeof token !== "number") {
          if (token instanceof Array) {
            tstack = token;
            token = tstack.pop();
          }
          token = self.symbols_[token] || token;
        }
        return token;
      }
      __name(lex, "lex");
      var symbol, preErrorSymbol, state, action, a, r, yyval = {}, p, len, newState, expected;
      while (true) {
        state = stack[stack.length - 1];
        if (this.defaultActions[state]) {
          action = this.defaultActions[state];
        } else {
          if (symbol === null || typeof symbol == "undefined") {
            symbol = lex();
          }
          action = table[state] && table[state][symbol];
        }
        if (typeof action === "undefined" || !action.length || !action[0]) {
          var errStr = "";
          expected = [];
          for (p in table[state]) {
            if (this.terminals_[p] && p > TERROR) {
              expected.push("'" + this.terminals_[p] + "'");
            }
          }
          if (lexer2.showPosition) {
            errStr = "Parse error on line " + (yylineno + 1) + ":\n" + lexer2.showPosition() + "\nExpecting " + expected.join(", ") + ", got '" + (this.terminals_[symbol] || symbol) + "'";
          } else {
            errStr = "Parse error on line " + (yylineno + 1) + ": Unexpected " + (symbol == EOF ? "end of input" : "'" + (this.terminals_[symbol] || symbol) + "'");
          }
          this.parseError(errStr, {
            text: lexer2.match,
            token: this.terminals_[symbol] || symbol,
            line: lexer2.yylineno,
            loc: yyloc,
            expected
          });
        }
        if (action[0] instanceof Array && action.length > 1) {
          throw new Error("Parse Error: multiple actions possible at state: " + state + ", token: " + symbol);
        }
        switch (action[0]) {
          case 1:
            stack.push(symbol);
            vstack.push(lexer2.yytext);
            lstack.push(lexer2.yylloc);
            stack.push(action[1]);
            symbol = null;
            if (!preErrorSymbol) {
              yyleng = lexer2.yyleng;
              yytext = lexer2.yytext;
              yylineno = lexer2.yylineno;
              yyloc = lexer2.yylloc;
              if (recovering > 0) {
                recovering--;
              }
            } else {
              symbol = preErrorSymbol;
              preErrorSymbol = null;
            }
            break;
          case 2:
            len = this.productions_[action[1]][1];
            yyval.$ = vstack[vstack.length - len];
            yyval._$ = {
              first_line: lstack[lstack.length - (len || 1)].first_line,
              last_line: lstack[lstack.length - 1].last_line,
              first_column: lstack[lstack.length - (len || 1)].first_column,
              last_column: lstack[lstack.length - 1].last_column
            };
            if (ranges) {
              yyval._$.range = [
                lstack[lstack.length - (len || 1)].range[0],
                lstack[lstack.length - 1].range[1]
              ];
            }
            r = this.performAction.apply(yyval, [
              yytext,
              yyleng,
              yylineno,
              sharedState.yy,
              action[1],
              vstack,
              lstack
            ].concat(args));
            if (typeof r !== "undefined") {
              return r;
            }
            if (len) {
              stack = stack.slice(0, -1 * len * 2);
              vstack = vstack.slice(0, -1 * len);
              lstack = lstack.slice(0, -1 * len);
            }
            stack.push(this.productions_[action[1]][0]);
            vstack.push(yyval.$);
            lstack.push(yyval._$);
            newState = table[stack[stack.length - 2]][stack[stack.length - 1]];
            stack.push(newState);
            break;
          case 3:
            return true;
        }
      }
      return true;
    }, "parse")
  };
  var lexer = /* @__PURE__ */ function() {
    var lexer2 = {
      EOF: 1,
      parseError: /* @__PURE__ */ __name(function parseError(str, hash) {
        if (this.yy.parser) {
          this.yy.parser.parseError(str, hash);
        } else {
          throw new Error(str);
        }
      }, "parseError"),
      // resets the lexer, sets new input
      setInput: /* @__PURE__ */ __name(function(input, yy) {
        this.yy = yy || this.yy || {};
        this._input = input;
        this._more = this._backtrack = this.done = false;
        this.yylineno = this.yyleng = 0;
        this.yytext = this.matched = this.match = "";
        this.conditionStack = ["INITIAL"];
        this.yylloc = {
          first_line: 1,
          first_column: 0,
          last_line: 1,
          last_column: 0
        };
        if (this.options.ranges) {
          this.yylloc.range = [0, 0];
        }
        this.offset = 0;
        return this;
      }, "setInput"),
      // consumes and returns one char from the input
      input: /* @__PURE__ */ __name(function() {
        var ch = this._input[0];
        this.yytext += ch;
        this.yyleng++;
        this.offset++;
        this.match += ch;
        this.matched += ch;
        var lines = ch.match(/(?:\r\n?|\n).*/g);
        if (lines) {
          this.yylineno++;
          this.yylloc.last_line++;
        } else {
          this.yylloc.last_column++;
        }
        if (this.options.ranges) {
          this.yylloc.range[1]++;
        }
        this._input = this._input.slice(1);
        return ch;
      }, "input"),
      // unshifts one char (or a string) into the input
      unput: /* @__PURE__ */ __name(function(ch) {
        var len = ch.length;
        var lines = ch.split(/(?:\r\n?|\n)/g);
        this._input = ch + this._input;
        this.yytext = this.yytext.substr(0, this.yytext.length - len);
        this.offset -= len;
        var oldLines = this.match.split(/(?:\r\n?|\n)/g);
        this.match = this.match.substr(0, this.match.length - 1);
        this.matched = this.matched.substr(0, this.matched.length - 1);
        if (lines.length - 1) {
          this.yylineno -= lines.length - 1;
        }
        var r = this.yylloc.range;
        this.yylloc = {
          first_line: this.yylloc.first_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.first_column,
          last_column: lines ? (lines.length === oldLines.length ? this.yylloc.first_column : 0) + oldLines[oldLines.length - lines.length].length - lines[0].length : this.yylloc.first_column - len
        };
        if (this.options.ranges) {
          this.yylloc.range = [r[0], r[0] + this.yyleng - len];
        }
        this.yyleng = this.yytext.length;
        return this;
      }, "unput"),
      // When called from action, caches matched text and appends it on next action
      more: /* @__PURE__ */ __name(function() {
        this._more = true;
        return this;
      }, "more"),
      // When called from action, signals the lexer that this rule fails to match the input, so the next matching rule (regex) should be tested instead.
      reject: /* @__PURE__ */ __name(function() {
        if (this.options.backtrack_lexer) {
          this._backtrack = true;
        } else {
          return this.parseError("Lexical error on line " + (this.yylineno + 1) + ". You can only invoke reject() in the lexer when the lexer is of the backtracking persuasion (options.backtrack_lexer = true).\n" + this.showPosition(), {
            text: "",
            token: null,
            line: this.yylineno
          });
        }
        return this;
      }, "reject"),
      // retain first n characters of the match
      less: /* @__PURE__ */ __name(function(n) {
        this.unput(this.match.slice(n));
      }, "less"),
      // displays already matched input, i.e. for error messages
      pastInput: /* @__PURE__ */ __name(function() {
        var past = this.matched.substr(0, this.matched.length - this.match.length);
        return (past.length > 20 ? "..." : "") + past.substr(-20).replace(/\n/g, "");
      }, "pastInput"),
      // displays upcoming input, i.e. for error messages
      upcomingInput: /* @__PURE__ */ __name(function() {
        var next = this.match;
        if (next.length < 20) {
          next += this._input.substr(0, 20 - next.length);
        }
        return (next.substr(0, 20) + (next.length > 20 ? "..." : "")).replace(/\n/g, "");
      }, "upcomingInput"),
      // displays the character position where the lexing error occurred, i.e. for error messages
      showPosition: /* @__PURE__ */ __name(function() {
        var pre = this.pastInput();
        var c = new Array(pre.length + 1).join("-");
        return pre + this.upcomingInput() + "\n" + c + "^";
      }, "showPosition"),
      // test the lexed token: return FALSE when not a match, otherwise return token
      test_match: /* @__PURE__ */ __name(function(match, indexed_rule) {
        var token, lines, backup;
        if (this.options.backtrack_lexer) {
          backup = {
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
          };
          if (this.options.ranges) {
            backup.yylloc.range = this.yylloc.range.slice(0);
          }
        }
        lines = match[0].match(/(?:\r\n?|\n).*/g);
        if (lines) {
          this.yylineno += lines.length;
        }
        this.yylloc = {
          first_line: this.yylloc.last_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.last_column,
          last_column: lines ? lines[lines.length - 1].length - lines[lines.length - 1].match(/\r?\n?/)[0].length : this.yylloc.last_column + match[0].length
        };
        this.yytext += match[0];
        this.match += match[0];
        this.matches = match;
        this.yyleng = this.yytext.length;
        if (this.options.ranges) {
          this.yylloc.range = [this.offset, this.offset += this.yyleng];
        }
        this._more = false;
        this._backtrack = false;
        this._input = this._input.slice(match[0].length);
        this.matched += match[0];
        token = this.performAction.call(this, this.yy, this, indexed_rule, this.conditionStack[this.conditionStack.length - 1]);
        if (this.done && this._input) {
          this.done = false;
        }
        if (token) {
          return token;
        } else if (this._backtrack) {
          for (var k in backup) {
            this[k] = backup[k];
          }
          return false;
        }
        return false;
      }, "test_match"),
      // return next match in input
      next: /* @__PURE__ */ __name(function() {
        if (this.done) {
          return this.EOF;
        }
        if (!this._input) {
          this.done = true;
        }
        var token, match, tempMatch, index;
        if (!this._more) {
          this.yytext = "";
          this.match = "";
        }
        var rules = this._currentRules();
        for (var i = 0; i < rules.length; i++) {
          tempMatch = this._input.match(this.rules[rules[i]]);
          if (tempMatch && (!match || tempMatch[0].length > match[0].length)) {
            match = tempMatch;
            index = i;
            if (this.options.backtrack_lexer) {
              token = this.test_match(tempMatch, rules[i]);
              if (token !== false) {
                return token;
              } else if (this._backtrack) {
                match = false;
                continue;
              } else {
                return false;
              }
            } else if (!this.options.flex) {
              break;
            }
          }
        }
        if (match) {
          token = this.test_match(match, rules[index]);
          if (token !== false) {
            return token;
          }
          return false;
        }
        if (this._input === "") {
          return this.EOF;
        } else {
          return this.parseError("Lexical error on line " + (this.yylineno + 1) + ". Unrecognized text.\n" + this.showPosition(), {
            text: "",
            token: null,
            line: this.yylineno
          });
        }
      }, "next"),
      // return next match that has a token
      lex: /* @__PURE__ */ __name(function lex() {
        var r = this.next();
        if (r) {
          return r;
        } else {
          return this.lex();
        }
      }, "lex"),
      // activates a new lexer condition state (pushes the new lexer condition state onto the condition stack)
      begin: /* @__PURE__ */ __name(function begin(condition) {
        this.conditionStack.push(condition);
      }, "begin"),
      // pop the previously active lexer condition state off the condition stack
      popState: /* @__PURE__ */ __name(function popState() {
        var n = this.conditionStack.length - 1;
        if (n > 0) {
          return this.conditionStack.pop();
        } else {
          return this.conditionStack[0];
        }
      }, "popState"),
      // produce the lexer rule set which is active for the currently active lexer condition state
      _currentRules: /* @__PURE__ */ __name(function _currentRules() {
        if (this.conditionStack.length && this.conditionStack[this.conditionStack.length - 1]) {
          return this.conditions[this.conditionStack[this.conditionStack.length - 1]].rules;
        } else {
          return this.conditions["INITIAL"].rules;
        }
      }, "_currentRules"),
      // return the currently active lexer condition state; when an index argument is provided it produces the N-th previous condition state, if available
      topState: /* @__PURE__ */ __name(function topState(n) {
        n = this.conditionStack.length - 1 - Math.abs(n || 0);
        if (n >= 0) {
          return this.conditionStack[n];
        } else {
          return "INITIAL";
        }
      }, "topState"),
      // alias for begin(condition)
      pushState: /* @__PURE__ */ __name(function pushState(condition) {
        this.begin(condition);
      }, "pushState"),
      // return the number of states currently on the stack
      stateStackSize: /* @__PURE__ */ __name(function stateStackSize() {
        return this.conditionStack.length;
      }, "stateStackSize"),
      options: { "case-insensitive": true },
      performAction: /* @__PURE__ */ __name(function anonymous(yy, yy_, $avoiding_name_collisions, YY_START) {
        var YYSTATE = YY_START;
        switch ($avoiding_name_collisions) {
          case 0:
            return 41;
            break;
          case 1:
            return 48;
            break;
          case 2:
            return 49;
            break;
          case 3:
            return 50;
            break;
          case 4:
            return 51;
            break;
          case 5:
            break;
          case 6:
            {
            }
            break;
          case 7:
            return 5;
            break;
          case 8:
            break;
          case 9:
            break;
          case 10:
            break;
          case 11:
            break;
          case 12:
            this.pushState("SCALE");
            return 17;
            break;
          case 13:
            return 18;
            break;
          case 14:
            this.popState();
            break;
          case 15:
            this.begin("acc_title");
            return 33;
            break;
          case 16:
            this.popState();
            return "acc_title_value";
            break;
          case 17:
            this.begin("acc_descr");
            return 35;
            break;
          case 18:
            this.popState();
            return "acc_descr_value";
            break;
          case 19:
            this.begin("acc_descr_multiline");
            break;
          case 20:
            this.popState();
            break;
          case 21:
            return "acc_descr_multiline_value";
            break;
          case 22:
            this.pushState("CLASSDEF");
            return 38;
            break;
          case 23:
            this.popState();
            this.pushState("CLASSDEFID");
            return "DEFAULT_CLASSDEF_ID";
            break;
          case 24:
            this.popState();
            this.pushState("CLASSDEFID");
            return 39;
            break;
          case 25:
            this.popState();
            return 40;
            break;
          case 26:
            this.pushState("CLASS");
            return 45;
            break;
          case 27:
            this.popState();
            this.pushState("CLASS_STYLE");
            return 46;
            break;
          case 28:
            this.popState();
            return 47;
            break;
          case 29:
            this.pushState("STYLE");
            return 42;
            break;
          case 30:
            this.popState();
            this.pushState("STYLEDEF_STYLES");
            return 43;
            break;
          case 31:
            this.popState();
            return 44;
            break;
          case 32:
            this.pushState("SCALE");
            return 17;
            break;
          case 33:
            return 18;
            break;
          case 34:
            this.popState();
            break;
          case 35:
            this.pushState("STATE");
            break;
          case 36:
            this.popState();
            yy_.yytext = yy_.yytext.slice(0, -8).trim();
            return 25;
            break;
          case 37:
            this.popState();
            yy_.yytext = yy_.yytext.slice(0, -8).trim();
            return 26;
            break;
          case 38:
            this.popState();
            yy_.yytext = yy_.yytext.slice(0, -10).trim();
            return 27;
            break;
          case 39:
            this.popState();
            yy_.yytext = yy_.yytext.slice(0, -8).trim();
            return 25;
            break;
          case 40:
            this.popState();
            yy_.yytext = yy_.yytext.slice(0, -8).trim();
            return 26;
            break;
          case 41:
            this.popState();
            yy_.yytext = yy_.yytext.slice(0, -10).trim();
            return 27;
            break;
          case 42:
            return 48;
            break;
          case 43:
            return 49;
            break;
          case 44:
            return 50;
            break;
          case 45:
            return 51;
            break;
          case 46:
            this.pushState("STATE_STRING");
            break;
          case 47:
            this.pushState("STATE_ID");
            return "AS";
            break;
          case 48:
            this.popState();
            return "ID";
            break;
          case 49:
            this.popState();
            break;
          case 50:
            return "STATE_DESCR";
            break;
          case 51:
            return 19;
            break;
          case 52:
            this.popState();
            break;
          case 53:
            this.popState();
            this.pushState("struct");
            return 20;
            break;
          case 54:
            break;
          case 55:
            this.popState();
            return 21;
            break;
          case 56:
            break;
          case 57:
            this.begin("NOTE");
            return 29;
            break;
          case 58:
            this.popState();
            this.pushState("NOTE_ID");
            return 56;
            break;
          case 59:
            this.popState();
            this.pushState("NOTE_ID");
            return 57;
            break;
          case 60:
            this.popState();
            this.pushState("FLOATING_NOTE");
            break;
          case 61:
            this.popState();
            this.pushState("FLOATING_NOTE_ID");
            return "AS";
            break;
          case 62:
            break;
          case 63:
            return "NOTE_TEXT";
            break;
          case 64:
            this.popState();
            return "ID";
            break;
          case 65:
            this.popState();
            this.pushState("NOTE_TEXT");
            return 24;
            break;
          case 66:
            this.popState();
            yy_.yytext = yy_.yytext.substr(2).trim();
            return 31;
            break;
          case 67:
            this.popState();
            yy_.yytext = yy_.yytext.slice(0, -8).trim();
            return 31;
            break;
          case 68:
            return 6;
            break;
          case 69:
            return 6;
            break;
          case 70:
            return 16;
            break;
          case 71:
            return 54;
            break;
          case 72:
            return 24;
            break;
          case 73:
            yy_.yytext = yy_.yytext.trim();
            return 14;
            break;
          case 74:
            return 15;
            break;
          case 75:
            return 28;
            break;
          case 76:
            return 55;
            break;
          case 77:
            return 5;
            break;
          case 78:
            return "INVALID";
            break;
        }
      }, "anonymous"),
      rules: [/^(?:default\b)/i, /^(?:.*direction\s+TB[^\n]*)/i, /^(?:.*direction\s+BT[^\n]*)/i, /^(?:.*direction\s+RL[^\n]*)/i, /^(?:.*direction\s+LR[^\n]*)/i, /^(?:%%(?!\{)[^\n]*)/i, /^(?:[^\}]%%[^\n]*)/i, /^(?:[\n]+)/i, /^(?:[\s]+)/i, /^(?:((?!\n)\s)+)/i, /^(?:#[^\n]*)/i, /^(?:%[^\n]*)/i, /^(?:scale\s+)/i, /^(?:\d+)/i, /^(?:\s+width\b)/i, /^(?:accTitle\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*\{\s*)/i, /^(?:[\}])/i, /^(?:[^\}]*)/i, /^(?:classDef\s+)/i, /^(?:DEFAULT\s+)/i, /^(?:\w+\s+)/i, /^(?:[^\n]*)/i, /^(?:class\s+)/i, /^(?:(\w+)+((,\s*\w+)*))/i, /^(?:[^\n]*)/i, /^(?:style\s+)/i, /^(?:[\w,]+\s+)/i, /^(?:[^\n]*)/i, /^(?:scale\s+)/i, /^(?:\d+)/i, /^(?:\s+width\b)/i, /^(?:state\s+)/i, /^(?:.*<<fork>>)/i, /^(?:.*<<join>>)/i, /^(?:.*<<choice>>)/i, /^(?:.*\[\[fork\]\])/i, /^(?:.*\[\[join\]\])/i, /^(?:.*\[\[choice\]\])/i, /^(?:.*direction\s+TB[^\n]*)/i, /^(?:.*direction\s+BT[^\n]*)/i, /^(?:.*direction\s+RL[^\n]*)/i, /^(?:.*direction\s+LR[^\n]*)/i, /^(?:["])/i, /^(?:\s*as\s+)/i, /^(?:[^\n\{]*)/i, /^(?:["])/i, /^(?:[^"]*)/i, /^(?:[^\n\s\{]+)/i, /^(?:\n)/i, /^(?:\{)/i, /^(?:%%(?!\{)[^\n]*)/i, /^(?:\})/i, /^(?:[\n])/i, /^(?:note\s+)/i, /^(?:left of\b)/i, /^(?:right of\b)/i, /^(?:")/i, /^(?:\s*as\s*)/i, /^(?:["])/i, /^(?:[^"]*)/i, /^(?:[^\n]*)/i, /^(?:\s*[^:\n\s\-]+)/i, /^(?:\s*:[^:\n;]+)/i, /^(?:[\s\S]*?end note\b)/i, /^(?:stateDiagram\s+)/i, /^(?:stateDiagram-v2\s+)/i, /^(?:hide empty description\b)/i, /^(?:\[\*\])/i, /^(?:[^:\n\s\-\{]+)/i, /^(?:\s*:[^:\n;]+)/i, /^(?:-->)/i, /^(?:--)/i, /^(?::::)/i, /^(?:$)/i, /^(?:.)/i],
      conditions: { "LINE": { "rules": [9, 10], "inclusive": false }, "struct": { "rules": [9, 10, 22, 26, 29, 35, 42, 43, 44, 45, 54, 55, 56, 57, 71, 72, 73, 74, 75], "inclusive": false }, "FLOATING_NOTE_ID": { "rules": [64], "inclusive": false }, "FLOATING_NOTE": { "rules": [61, 62, 63], "inclusive": false }, "NOTE_TEXT": { "rules": [66, 67], "inclusive": false }, "NOTE_ID": { "rules": [65], "inclusive": false }, "NOTE": { "rules": [58, 59, 60], "inclusive": false }, "STYLEDEF_STYLEOPTS": { "rules": [], "inclusive": false }, "STYLEDEF_STYLES": { "rules": [31], "inclusive": false }, "STYLE_IDS": { "rules": [], "inclusive": false }, "STYLE": { "rules": [30], "inclusive": false }, "CLASS_STYLE": { "rules": [28], "inclusive": false }, "CLASS": { "rules": [27], "inclusive": false }, "CLASSDEFID": { "rules": [25], "inclusive": false }, "CLASSDEF": { "rules": [23, 24], "inclusive": false }, "acc_descr_multiline": { "rules": [20, 21], "inclusive": false }, "acc_descr": { "rules": [18], "inclusive": false }, "acc_title": { "rules": [16], "inclusive": false }, "SCALE": { "rules": [13, 14, 33, 34], "inclusive": false }, "ALIAS": { "rules": [], "inclusive": false }, "STATE_ID": { "rules": [48], "inclusive": false }, "STATE_STRING": { "rules": [49, 50], "inclusive": false }, "FORK_STATE": { "rules": [], "inclusive": false }, "STATE": { "rules": [9, 10, 36, 37, 38, 39, 40, 41, 46, 47, 51, 52, 53], "inclusive": false }, "ID": { "rules": [9, 10], "inclusive": false }, "INITIAL": { "rules": [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 15, 17, 19, 22, 26, 29, 32, 35, 53, 57, 68, 69, 70, 71, 72, 73, 74, 76, 77, 78], "inclusive": true } }
    };
    return lexer2;
  }();
  parser2.lexer = lexer;
  function Parser() {
    this.yy = {};
  }
  __name(Parser, "Parser");
  Parser.prototype = parser2;
  parser2.Parser = Parser;
  return new Parser();
}();
parser.parser = parser;
var stateDiagram_default = parser;

// src/diagrams/state/stateCommon.ts
var DEFAULT_DIAGRAM_DIRECTION = "LR";
var DEFAULT_NESTED_DOC_DIR = "TB";
var STMT_STATE = "state";
var STMT_RELATION = "relation";
var STMT_CLASSDEF = "classDef";
var STMT_STYLEDEF = "style";
var STMT_APPLYCLASS = "applyClass";
var DEFAULT_STATE_TYPE = "default";
var DIVIDER_TYPE = "divider";
var G_EDGE_STYLE = "fill:none";
var G_EDGE_ARROWHEADSTYLE = "fill: #333";
var G_EDGE_LABELPOS = "c";
var G_EDGE_LABELTYPE = "text";
var G_EDGE_THICKNESS = "normal";
var SHAPE_STATE = "rect";
var SHAPE_STATE_WITH_DESC = "rectWithTitle";
var SHAPE_START = "stateStart";
var SHAPE_END = "stateEnd";
var SHAPE_DIVIDER = "divider";
var SHAPE_GROUP = "roundedWithTitle";
var SHAPE_NOTE = "note";
var SHAPE_NOTEGROUP = "noteGroup";
var CSS_DIAGRAM = "statediagram";
var CSS_STATE = "state";
var CSS_DIAGRAM_STATE = `${CSS_DIAGRAM}-${CSS_STATE}`;
var CSS_EDGE = "transition";
var CSS_NOTE = "note";
var CSS_NOTE_EDGE = "note-edge";
var CSS_EDGE_NOTE_EDGE = `${CSS_EDGE} ${CSS_NOTE_EDGE}`;
var CSS_DIAGRAM_NOTE = `${CSS_DIAGRAM}-${CSS_NOTE}`;
var CSS_CLUSTER = "cluster";
var CSS_DIAGRAM_CLUSTER = `${CSS_DIAGRAM}-${CSS_CLUSTER}`;
var CSS_CLUSTER_ALT = "cluster-alt";
var CSS_DIAGRAM_CLUSTER_ALT = `${CSS_DIAGRAM}-${CSS_CLUSTER_ALT}`;
var PARENT = "parent";
var NOTE = "note";
var DOMID_STATE = "state";
var DOMID_TYPE_SPACER = "----";
var NOTE_ID = `${DOMID_TYPE_SPACER}${NOTE}`;
var PARENT_ID = `${DOMID_TYPE_SPACER}${PARENT}`;

// src/diagrams/state/stateRenderer-v3-unified.ts
var getDir = /* @__PURE__ */ __name((parsedItem, defaultDir = DEFAULT_NESTED_DOC_DIR) => {
  if (!parsedItem.doc) {
    return defaultDir;
  }
  let dir = defaultDir;
  for (const parsedItemDoc of parsedItem.doc) {
    if (parsedItemDoc.stmt === "dir") {
      dir = parsedItemDoc.value;
    }
  }
  return dir;
}, "getDir");
var getClasses = /* @__PURE__ */ __name(function(text, diagramObj) {
  diagramObj.db.extract(diagramObj.db.getRootDocV2());
  return diagramObj.db.getClasses();
}, "getClasses");
var draw = /* @__PURE__ */ __name(async function(text, id, _version, diag) {
  log.info("REF0:");
  log.info("Drawing state diagram (v2)", id);
  const { securityLevel, state: conf, layout } = getConfig();
  diag.db.extract(diag.db.getRootDocV2());
  const data4Layout = diag.db.getData();
  const svg = getDiagramElement(id, securityLevel);
  data4Layout.type = diag.type;
  data4Layout.layoutAlgorithm = layout;
  data4Layout.nodeSpacing = conf?.nodeSpacing || 50;
  data4Layout.rankSpacing = conf?.rankSpacing || 50;
  data4Layout.markers = ["barb"];
  data4Layout.diagramId = id;
  await render(data4Layout, svg);
  const padding = 8;
  utils_default.insertTitle(
    svg,
    "statediagramTitleText",
    conf?.titleTopMargin ?? 25,
    diag.db.getDiagramTitle()
  );
  setupViewPortForSVG(svg, padding, CSS_DIAGRAM, conf?.useMaxWidth ?? true);
}, "draw");
var stateRenderer_v3_unified_default = {
  getClasses,
  draw,
  getDir
};

// src/diagrams/state/dataFetcher.js
var nodeDb = /* @__PURE__ */ new Map();
var graphItemCount = 0;
function stateDomId(itemId = "", counter = 0, type = "", typeSpacer = DOMID_TYPE_SPACER) {
  const typeStr = type !== null && type.length > 0 ? `${typeSpacer}${type}` : "";
  return `${DOMID_STATE}-${itemId}${typeStr}-${counter}`;
}
__name(stateDomId, "stateDomId");
var setupDoc = /* @__PURE__ */ __name((parentParsedItem, doc, diagramStates, nodes2, edges2, altFlag, look, classes2) => {
  log.trace("items", doc);
  doc.forEach((item) => {
    switch (item.stmt) {
      case STMT_STATE:
        dataFetcher(parentParsedItem, item, diagramStates, nodes2, edges2, altFlag, look, classes2);
        break;
      case DEFAULT_STATE_TYPE:
        dataFetcher(parentParsedItem, item, diagramStates, nodes2, edges2, altFlag, look, classes2);
        break;
      case STMT_RELATION:
        {
          dataFetcher(
            parentParsedItem,
            item.state1,
            diagramStates,
            nodes2,
            edges2,
            altFlag,
            look,
            classes2
          );
          dataFetcher(
            parentParsedItem,
            item.state2,
            diagramStates,
            nodes2,
            edges2,
            altFlag,
            look,
            classes2
          );
          const edgeData = {
            id: "edge" + graphItemCount,
            start: item.state1.id,
            end: item.state2.id,
            arrowhead: "normal",
            arrowTypeEnd: "arrow_barb",
            style: G_EDGE_STYLE,
            labelStyle: "",
            label: common_default.sanitizeText(item.description, getConfig()),
            arrowheadStyle: G_EDGE_ARROWHEADSTYLE,
            labelpos: G_EDGE_LABELPOS,
            labelType: G_EDGE_LABELTYPE,
            thickness: G_EDGE_THICKNESS,
            classes: CSS_EDGE,
            look
          };
          edges2.push(edgeData);
          graphItemCount++;
        }
        break;
    }
  });
}, "setupDoc");
var getDir2 = /* @__PURE__ */ __name((parsedItem, defaultDir = DEFAULT_NESTED_DOC_DIR) => {
  let dir = defaultDir;
  if (parsedItem.doc) {
    for (const parsedItemDoc of parsedItem.doc) {
      if (parsedItemDoc.stmt === "dir") {
        dir = parsedItemDoc.value;
      }
    }
  }
  return dir;
}, "getDir");
function insertOrUpdateNode(nodes2, nodeData, classes2) {
  if (!nodeData.id || nodeData.id === "</join></fork>" || nodeData.id === "</choice>") {
    return;
  }
  if (nodeData.cssClasses) {
    if (!Array.isArray(nodeData.cssCompiledStyles)) {
      nodeData.cssCompiledStyles = [];
    }
    nodeData.cssClasses.split(" ").forEach((cssClass) => {
      if (classes2.get(cssClass)) {
        const classDef = classes2.get(cssClass);
        nodeData.cssCompiledStyles = [...nodeData.cssCompiledStyles, ...classDef.styles];
      }
    });
  }
  const existingNodeData = nodes2.find((node) => node.id === nodeData.id);
  if (existingNodeData) {
    Object.assign(existingNodeData, nodeData);
  } else {
    nodes2.push(nodeData);
  }
}
__name(insertOrUpdateNode, "insertOrUpdateNode");
function getClassesFromDbInfo(dbInfoItem) {
  return dbInfoItem?.classes?.join(" ") ?? "";
}
__name(getClassesFromDbInfo, "getClassesFromDbInfo");
function getStylesFromDbInfo(dbInfoItem) {
  return dbInfoItem?.styles ?? [];
}
__name(getStylesFromDbInfo, "getStylesFromDbInfo");
var dataFetcher = /* @__PURE__ */ __name((parent, parsedItem, diagramStates, nodes2, edges2, altFlag, look, classes2) => {
  const itemId = parsedItem.id;
  const dbState = diagramStates.get(itemId);
  const classStr = getClassesFromDbInfo(dbState);
  const style = getStylesFromDbInfo(dbState);
  log.info("dataFetcher parsedItem", parsedItem, dbState, style);
  if (itemId !== "root") {
    let shape = SHAPE_STATE;
    if (parsedItem.start === true) {
      shape = SHAPE_START;
    } else if (parsedItem.start === false) {
      shape = SHAPE_END;
    }
    if (parsedItem.type !== DEFAULT_STATE_TYPE) {
      shape = parsedItem.type;
    }
    if (!nodeDb.get(itemId)) {
      nodeDb.set(itemId, {
        id: itemId,
        shape,
        description: common_default.sanitizeText(itemId, getConfig()),
        cssClasses: `${classStr} ${CSS_DIAGRAM_STATE}`,
        cssStyles: style
      });
    }
    const newNode = nodeDb.get(itemId);
    if (parsedItem.description) {
      if (Array.isArray(newNode.description)) {
        newNode.shape = SHAPE_STATE_WITH_DESC;
        newNode.description.push(parsedItem.description);
      } else {
        if (newNode.description?.length > 0) {
          newNode.shape = SHAPE_STATE_WITH_DESC;
          if (newNode.description === itemId) {
            newNode.description = [parsedItem.description];
          } else {
            newNode.description = [newNode.description, parsedItem.description];
          }
        } else {
          newNode.shape = SHAPE_STATE;
          newNode.description = parsedItem.description;
        }
      }
      newNode.description = common_default.sanitizeTextOrArray(newNode.description, getConfig());
    }
    if (newNode.description?.length === 1 && newNode.shape === SHAPE_STATE_WITH_DESC) {
      if (newNode.type === "group") {
        newNode.shape = SHAPE_GROUP;
      } else {
        newNode.shape = SHAPE_STATE;
      }
    }
    if (!newNode.type && parsedItem.doc) {
      log.info("Setting cluster for XCX", itemId, getDir2(parsedItem));
      newNode.type = "group";
      newNode.isGroup = true;
      newNode.dir = getDir2(parsedItem);
      newNode.shape = parsedItem.type === DIVIDER_TYPE ? SHAPE_DIVIDER : SHAPE_GROUP;
      newNode.cssClasses = `${newNode.cssClasses} ${CSS_DIAGRAM_CLUSTER} ${altFlag ? CSS_DIAGRAM_CLUSTER_ALT : ""}`;
    }
    const nodeData = {
      labelStyle: "",
      shape: newNode.shape,
      label: newNode.description,
      cssClasses: newNode.cssClasses,
      cssCompiledStyles: [],
      cssStyles: newNode.cssStyles,
      id: itemId,
      dir: newNode.dir,
      domId: stateDomId(itemId, graphItemCount),
      type: newNode.type,
      isGroup: newNode.type === "group",
      padding: 8,
      rx: 10,
      ry: 10,
      look
    };
    if (nodeData.shape === SHAPE_DIVIDER) {
      nodeData.label = "";
    }
    if (parent && parent.id !== "root") {
      log.trace("Setting node ", itemId, " to be child of its parent ", parent.id);
      nodeData.parentId = parent.id;
    }
    nodeData.centerLabel = true;
    if (parsedItem.note) {
      const noteData = {
        labelStyle: "",
        shape: SHAPE_NOTE,
        label: parsedItem.note.text,
        cssClasses: CSS_DIAGRAM_NOTE,
        // useHtmlLabels: false,
        cssStyles: [],
        cssCompilesStyles: [],
        id: itemId + NOTE_ID + "-" + graphItemCount,
        domId: stateDomId(itemId, graphItemCount, NOTE),
        type: newNode.type,
        isGroup: newNode.type === "group",
        padding: getConfig().flowchart.padding,
        look,
        position: parsedItem.note.position
      };
      const parentNodeId = itemId + PARENT_ID;
      const groupData = {
        labelStyle: "",
        shape: SHAPE_NOTEGROUP,
        label: parsedItem.note.text,
        cssClasses: newNode.cssClasses,
        cssStyles: [],
        id: itemId + PARENT_ID,
        domId: stateDomId(itemId, graphItemCount, PARENT),
        type: "group",
        isGroup: true,
        padding: 16,
        //getConfig().flowchart.padding
        look,
        position: parsedItem.note.position
      };
      graphItemCount++;
      groupData.id = parentNodeId;
      noteData.parentId = parentNodeId;
      insertOrUpdateNode(nodes2, groupData, classes2);
      insertOrUpdateNode(nodes2, noteData, classes2);
      insertOrUpdateNode(nodes2, nodeData, classes2);
      let from = itemId;
      let to = noteData.id;
      if (parsedItem.note.position === "left of") {
        from = noteData.id;
        to = itemId;
      }
      edges2.push({
        id: from + "-" + to,
        start: from,
        end: to,
        arrowhead: "none",
        arrowTypeEnd: "",
        style: G_EDGE_STYLE,
        labelStyle: "",
        classes: CSS_EDGE_NOTE_EDGE,
        arrowheadStyle: G_EDGE_ARROWHEADSTYLE,
        labelpos: G_EDGE_LABELPOS,
        labelType: G_EDGE_LABELTYPE,
        thickness: G_EDGE_THICKNESS,
        look
      });
    } else {
      insertOrUpdateNode(nodes2, nodeData, classes2);
    }
  }
  if (parsedItem.doc) {
    log.trace("Adding nodes children ");
    setupDoc(parsedItem, parsedItem.doc, diagramStates, nodes2, edges2, !altFlag, look, classes2);
  }
}, "dataFetcher");
var reset = /* @__PURE__ */ __name(() => {
  nodeDb.clear();
  graphItemCount = 0;
}, "reset");

// src/diagrams/state/stateDb.js
var START_NODE = "[*]";
var START_TYPE = "start";
var END_NODE = START_NODE;
var END_TYPE = "end";
var COLOR_KEYWORD = "color";
var FILL_KEYWORD = "fill";
var BG_FILL = "bgFill";
var STYLECLASS_SEP = ",";
function newClassesList() {
  return /* @__PURE__ */ new Map();
}
__name(newClassesList, "newClassesList");
var nodes = [];
var edges = [];
var direction = DEFAULT_DIAGRAM_DIRECTION;
var rootDoc = [];
var classes = newClassesList();
var newDoc = /* @__PURE__ */ __name(() => {
  return {
    /** @type {{ id1: string, id2: string, relationTitle: string }[]} */
    relations: [],
    states: /* @__PURE__ */ new Map(),
    documents: {}
  };
}, "newDoc");
var documents = {
  root: newDoc()
};
var currentDocument = documents.root;
var startEndCount = 0;
var dividerCnt = 0;
var lineType = {
  LINE: 0,
  DOTTED_LINE: 1
};
var relationType = {
  AGGREGATION: 0,
  EXTENSION: 1,
  COMPOSITION: 2,
  DEPENDENCY: 3
};
var clone = /* @__PURE__ */ __name((o) => JSON.parse(JSON.stringify(o)), "clone");
var setRootDoc = /* @__PURE__ */ __name((o) => {
  log.info("Setting root doc", o);
  rootDoc = o;
}, "setRootDoc");
var getRootDoc = /* @__PURE__ */ __name(() => rootDoc, "getRootDoc");
var docTranslator = /* @__PURE__ */ __name((parent, node, first) => {
  if (node.stmt === STMT_RELATION) {
    docTranslator(parent, node.state1, true);
    docTranslator(parent, node.state2, false);
  } else {
    if (node.stmt === STMT_STATE) {
      if (node.id === "[*]") {
        node.id = first ? parent.id + "_start" : parent.id + "_end";
        node.start = first;
      } else {
        node.id = node.id.trim();
      }
    }
    if (node.doc) {
      const doc = [];
      let currentDoc = [];
      let i;
      for (i = 0; i < node.doc.length; i++) {
        if (node.doc[i].type === DIVIDER_TYPE) {
          const newNode = clone(node.doc[i]);
          newNode.doc = clone(currentDoc);
          doc.push(newNode);
          currentDoc = [];
        } else {
          currentDoc.push(node.doc[i]);
        }
      }
      if (doc.length > 0 && currentDoc.length > 0) {
        const newNode = {
          stmt: STMT_STATE,
          id: generateId(),
          type: "divider",
          doc: clone(currentDoc)
        };
        doc.push(clone(newNode));
        node.doc = doc;
      }
      node.doc.forEach((docNode) => docTranslator(node, docNode, true));
    }
  }
}, "docTranslator");
var getRootDocV2 = /* @__PURE__ */ __name(() => {
  docTranslator({ id: "root" }, { id: "root", doc: rootDoc }, true);
  return { id: "root", doc: rootDoc };
}, "getRootDocV2");
var extract = /* @__PURE__ */ __name((_doc) => {
  let doc;
  if (_doc.doc) {
    doc = _doc.doc;
  } else {
    doc = _doc;
  }
  log.info(doc);
  clear2(true);
  log.info("Extract initial document:", doc);
  doc.forEach((item) => {
    log.warn("Statement", item.stmt);
    switch (item.stmt) {
      case STMT_STATE:
        addState(
          item.id.trim(),
          item.type,
          item.doc,
          item.description,
          item.note,
          item.classes,
          item.styles,
          item.textStyles
        );
        break;
      case STMT_RELATION:
        addRelation(item.state1, item.state2, item.description);
        break;
      case STMT_CLASSDEF:
        addStyleClass(item.id.trim(), item.classes);
        break;
      case STMT_STYLEDEF:
        {
          const ids = item.id.trim().split(",");
          const styles = item.styleClass.split(",");
          ids.forEach((id) => {
            let foundState = getState(id);
            if (foundState === void 0) {
              const trimmedId = id.trim();
              addState(trimmedId);
              foundState = getState(trimmedId);
            }
            foundState.styles = styles.map((s) => s.replace(/;/g, "")?.trim());
          });
        }
        break;
      case STMT_APPLYCLASS:
        setCssClass(item.id.trim(), item.styleClass);
        break;
    }
  });
  const diagramStates = getStates();
  const config = getConfig();
  const look = config.look;
  reset();
  dataFetcher(void 0, getRootDocV2(), diagramStates, nodes, edges, true, look, classes);
  nodes.forEach((node) => {
    if (Array.isArray(node.label)) {
      node.description = node.label.slice(1);
      if (node.isGroup && node.description.length > 0) {
        throw new Error(
          "Group nodes can only have label. Remove the additional description for node [" + node.id + "]"
        );
      }
      node.label = node.label[0];
    }
  });
}, "extract");
var addState = /* @__PURE__ */ __name(function(id, type = DEFAULT_STATE_TYPE, doc = null, descr = null, note = null, classes2 = null, styles = null, textStyles = null) {
  const trimmedId = id?.trim();
  if (!currentDocument.states.has(trimmedId)) {
    log.info("Adding state ", trimmedId, descr);
    currentDocument.states.set(trimmedId, {
      id: trimmedId,
      descriptions: [],
      type,
      doc,
      note,
      classes: [],
      styles: [],
      textStyles: []
    });
  } else {
    if (!currentDocument.states.get(trimmedId).doc) {
      currentDocument.states.get(trimmedId).doc = doc;
    }
    if (!currentDocument.states.get(trimmedId).type) {
      currentDocument.states.get(trimmedId).type = type;
    }
  }
  if (descr) {
    log.info("Setting state description", trimmedId, descr);
    if (typeof descr === "string") {
      addDescription(trimmedId, descr.trim());
    }
    if (typeof descr === "object") {
      descr.forEach((des) => addDescription(trimmedId, des.trim()));
    }
  }
  if (note) {
    const doc2 = currentDocument.states.get(trimmedId);
    doc2.note = note;
    doc2.note.text = common_default.sanitizeText(doc2.note.text, getConfig());
  }
  if (classes2) {
    log.info("Setting state classes", trimmedId, classes2);
    const classesList = typeof classes2 === "string" ? [classes2] : classes2;
    classesList.forEach((cssClass) => setCssClass(trimmedId, cssClass.trim()));
  }
  if (styles) {
    log.info("Setting state styles", trimmedId, styles);
    const stylesList = typeof styles === "string" ? [styles] : styles;
    stylesList.forEach((style) => setStyle(trimmedId, style.trim()));
  }
  if (textStyles) {
    log.info("Setting state styles", trimmedId, styles);
    const textStylesList = typeof textStyles === "string" ? [textStyles] : textStyles;
    textStylesList.forEach((textStyle) => setTextStyle(trimmedId, textStyle.trim()));
  }
}, "addState");
var clear2 = /* @__PURE__ */ __name(function(saveCommon) {
  nodes = [];
  edges = [];
  documents = {
    root: newDoc()
  };
  currentDocument = documents.root;
  startEndCount = 0;
  classes = newClassesList();
  if (!saveCommon) {
    clear();
  }
}, "clear");
var getState = /* @__PURE__ */ __name(function(id) {
  return currentDocument.states.get(id);
}, "getState");
var getStates = /* @__PURE__ */ __name(function() {
  return currentDocument.states;
}, "getStates");
var logDocuments = /* @__PURE__ */ __name(function() {
  log.info("Documents = ", documents);
}, "logDocuments");
var getRelations = /* @__PURE__ */ __name(function() {
  return currentDocument.relations;
}, "getRelations");
function startIdIfNeeded(id = "") {
  let fixedId = id;
  if (id === START_NODE) {
    startEndCount++;
    fixedId = `${START_TYPE}${startEndCount}`;
  }
  return fixedId;
}
__name(startIdIfNeeded, "startIdIfNeeded");
function startTypeIfNeeded(id = "", type = DEFAULT_STATE_TYPE) {
  return id === START_NODE ? START_TYPE : type;
}
__name(startTypeIfNeeded, "startTypeIfNeeded");
function endIdIfNeeded(id = "") {
  let fixedId = id;
  if (id === END_NODE) {
    startEndCount++;
    fixedId = `${END_TYPE}${startEndCount}`;
  }
  return fixedId;
}
__name(endIdIfNeeded, "endIdIfNeeded");
function endTypeIfNeeded(id = "", type = DEFAULT_STATE_TYPE) {
  return id === END_NODE ? END_TYPE : type;
}
__name(endTypeIfNeeded, "endTypeIfNeeded");
function addRelationObjs(item1, item2, relationTitle) {
  let id1 = startIdIfNeeded(item1.id.trim());
  let type1 = startTypeIfNeeded(item1.id.trim(), item1.type);
  let id2 = startIdIfNeeded(item2.id.trim());
  let type2 = startTypeIfNeeded(item2.id.trim(), item2.type);
  addState(
    id1,
    type1,
    item1.doc,
    item1.description,
    item1.note,
    item1.classes,
    item1.styles,
    item1.textStyles
  );
  addState(
    id2,
    type2,
    item2.doc,
    item2.description,
    item2.note,
    item2.classes,
    item2.styles,
    item2.textStyles
  );
  currentDocument.relations.push({
    id1,
    id2,
    relationTitle: common_default.sanitizeText(relationTitle, getConfig())
  });
}
__name(addRelationObjs, "addRelationObjs");
var addRelation = /* @__PURE__ */ __name(function(item1, item2, title) {
  if (typeof item1 === "object") {
    addRelationObjs(item1, item2, title);
  } else {
    const id1 = startIdIfNeeded(item1.trim());
    const type1 = startTypeIfNeeded(item1);
    const id2 = endIdIfNeeded(item2.trim());
    const type2 = endTypeIfNeeded(item2);
    addState(id1, type1);
    addState(id2, type2);
    currentDocument.relations.push({
      id1,
      id2,
      title: common_default.sanitizeText(title, getConfig())
    });
  }
}, "addRelation");
var addDescription = /* @__PURE__ */ __name(function(id, descr) {
  const theState = currentDocument.states.get(id);
  const _descr = descr.startsWith(":") ? descr.replace(":", "").trim() : descr;
  theState.descriptions.push(common_default.sanitizeText(_descr, getConfig()));
}, "addDescription");
var cleanupLabel = /* @__PURE__ */ __name(function(label) {
  if (label.substring(0, 1) === ":") {
    return label.substr(2).trim();
  } else {
    return label.trim();
  }
}, "cleanupLabel");
var getDividerId = /* @__PURE__ */ __name(() => {
  dividerCnt++;
  return "divider-id-" + dividerCnt;
}, "getDividerId");
var addStyleClass = /* @__PURE__ */ __name(function(id, styleAttributes = "") {
  if (!classes.has(id)) {
    classes.set(id, { id, styles: [], textStyles: [] });
  }
  const foundClass = classes.get(id);
  if (styleAttributes !== void 0 && styleAttributes !== null) {
    styleAttributes.split(STYLECLASS_SEP).forEach((attrib) => {
      const fixedAttrib = attrib.replace(/([^;]*);/, "$1").trim();
      if (RegExp(COLOR_KEYWORD).exec(attrib)) {
        const newStyle1 = fixedAttrib.replace(FILL_KEYWORD, BG_FILL);
        const newStyle2 = newStyle1.replace(COLOR_KEYWORD, FILL_KEYWORD);
        foundClass.textStyles.push(newStyle2);
      }
      foundClass.styles.push(fixedAttrib);
    });
  }
}, "addStyleClass");
var getClasses2 = /* @__PURE__ */ __name(function() {
  return classes;
}, "getClasses");
var setCssClass = /* @__PURE__ */ __name(function(itemIds, cssClassName) {
  itemIds.split(",").forEach(function(id) {
    let foundState = getState(id);
    if (foundState === void 0) {
      const trimmedId = id.trim();
      addState(trimmedId);
      foundState = getState(trimmedId);
    }
    foundState.classes.push(cssClassName);
  });
}, "setCssClass");
var setStyle = /* @__PURE__ */ __name(function(itemId, styleText) {
  const item = getState(itemId);
  if (item !== void 0) {
    item.styles.push(styleText);
  }
}, "setStyle");
var setTextStyle = /* @__PURE__ */ __name(function(itemId, cssClassName) {
  const item = getState(itemId);
  if (item !== void 0) {
    item.textStyles.push(cssClassName);
  }
}, "setTextStyle");
var getDirection = /* @__PURE__ */ __name(() => direction, "getDirection");
var setDirection = /* @__PURE__ */ __name((dir) => {
  direction = dir;
}, "setDirection");
var trimColon = /* @__PURE__ */ __name((str) => str && str[0] === ":" ? str.substr(1).trim() : str.trim(), "trimColon");
var getData = /* @__PURE__ */ __name(() => {
  const config = getConfig();
  return { nodes, edges, other: {}, config, direction: getDir(getRootDocV2()) };
}, "getData");
var stateDb_default = {
  getConfig: /* @__PURE__ */ __name(() => getConfig().state, "getConfig"),
  getData,
  addState,
  clear: clear2,
  getState,
  getStates,
  getRelations,
  getClasses: getClasses2,
  getDirection,
  addRelation,
  getDividerId,
  setDirection,
  cleanupLabel,
  lineType,
  relationType,
  logDocuments,
  getRootDoc,
  setRootDoc,
  getRootDocV2,
  extract,
  trimColon,
  getAccTitle,
  setAccTitle,
  getAccDescription,
  setAccDescription,
  addStyleClass,
  setCssClass,
  addDescription,
  setDiagramTitle,
  getDiagramTitle
};

// src/diagrams/state/styles.js
var getStyles = /* @__PURE__ */ __name((options) => `
defs #statediagram-barbEnd {
    fill: ${options.transitionColor};
    stroke: ${options.transitionColor};
  }
g.stateGroup text {
  fill: ${options.nodeBorder};
  stroke: none;
  font-size: 10px;
}
g.stateGroup text {
  fill: ${options.textColor};
  stroke: none;
  font-size: 10px;

}
g.stateGroup .state-title {
  font-weight: bolder;
  fill: ${options.stateLabelColor};
}

g.stateGroup rect {
  fill: ${options.mainBkg};
  stroke: ${options.nodeBorder};
}

g.stateGroup line {
  stroke: ${options.lineColor};
  stroke-width: 1;
}

.transition {
  stroke: ${options.transitionColor};
  stroke-width: 1;
  fill: none;
}

.stateGroup .composit {
  fill: ${options.background};
  border-bottom: 1px
}

.stateGroup .alt-composit {
  fill: #e0e0e0;
  border-bottom: 1px
}

.state-note {
  stroke: ${options.noteBorderColor};
  fill: ${options.noteBkgColor};

  text {
    fill: ${options.noteTextColor};
    stroke: none;
    font-size: 10px;
  }
}

.stateLabel .box {
  stroke: none;
  stroke-width: 0;
  fill: ${options.mainBkg};
  opacity: 0.5;
}

.edgeLabel .label rect {
  fill: ${options.labelBackgroundColor};
  opacity: 0.5;
}
.edgeLabel {
  background-color: ${options.edgeLabelBackground};
  p {
    background-color: ${options.edgeLabelBackground};
  }
  rect {
    opacity: 0.5;
    background-color: ${options.edgeLabelBackground};
    fill: ${options.edgeLabelBackground};
  }
  text-align: center;
}
.edgeLabel .label text {
  fill: ${options.transitionLabelColor || options.tertiaryTextColor};
}
.label div .edgeLabel {
  color: ${options.transitionLabelColor || options.tertiaryTextColor};
}

.stateLabel text {
  fill: ${options.stateLabelColor};
  font-size: 10px;
  font-weight: bold;
}

.node circle.state-start {
  fill: ${options.specialStateColor};
  stroke: ${options.specialStateColor};
}

.node .fork-join {
  fill: ${options.specialStateColor};
  stroke: ${options.specialStateColor};
}

.node circle.state-end {
  fill: ${options.innerEndBackground};
  stroke: ${options.background};
  stroke-width: 1.5
}
.end-state-inner {
  fill: ${options.compositeBackground || options.background};
  // stroke: ${options.background};
  stroke-width: 1.5
}

.node rect {
  fill: ${options.stateBkg || options.mainBkg};
  stroke: ${options.stateBorder || options.nodeBorder};
  stroke-width: 1px;
}
.node polygon {
  fill: ${options.mainBkg};
  stroke: ${options.stateBorder || options.nodeBorder};;
  stroke-width: 1px;
}
#statediagram-barbEnd {
  fill: ${options.lineColor};
}

.statediagram-cluster rect {
  fill: ${options.compositeTitleBackground};
  stroke: ${options.stateBorder || options.nodeBorder};
  stroke-width: 1px;
}

.cluster-label, .nodeLabel {
  color: ${options.stateLabelColor};
  // line-height: 1;
}

.statediagram-cluster rect.outer {
  rx: 5px;
  ry: 5px;
}
.statediagram-state .divider {
  stroke: ${options.stateBorder || options.nodeBorder};
}

.statediagram-state .title-state {
  rx: 5px;
  ry: 5px;
}
.statediagram-cluster.statediagram-cluster .inner {
  fill: ${options.compositeBackground || options.background};
}
.statediagram-cluster.statediagram-cluster-alt .inner {
  fill: ${options.altBackground ? options.altBackground : "#efefef"};
}

.statediagram-cluster .inner {
  rx:0;
  ry:0;
}

.statediagram-state rect.basic {
  rx: 5px;
  ry: 5px;
}
.statediagram-state rect.divider {
  stroke-dasharray: 10,10;
  fill: ${options.altBackground ? options.altBackground : "#efefef"};
}

.note-edge {
  stroke-dasharray: 5;
}

.statediagram-note rect {
  fill: ${options.noteBkgColor};
  stroke: ${options.noteBorderColor};
  stroke-width: 1px;
  rx: 0;
  ry: 0;
}
.statediagram-note rect {
  fill: ${options.noteBkgColor};
  stroke: ${options.noteBorderColor};
  stroke-width: 1px;
  rx: 0;
  ry: 0;
}

.statediagram-note text {
  fill: ${options.noteTextColor};
}

.statediagram-note .nodeLabel {
  color: ${options.noteTextColor};
}
.statediagram .edgeLabel {
  color: red; // ${options.noteTextColor};
}

#dependencyStart, #dependencyEnd {
  fill: ${options.lineColor};
  stroke: ${options.lineColor};
  stroke-width: 1;
}

.statediagramTitleText {
  text-anchor: middle;
  font-size: 18px;
  fill: ${options.textColor};
}
`, "getStyles");
var styles_default = getStyles;

export {
  stateDiagram_default,
  stateRenderer_v3_unified_default,
  stateDb_default,
  styles_default
};
