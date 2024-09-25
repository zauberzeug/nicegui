import {
  __name,
  clear,
  common_default,
  configureSvgSize,
  getAccDescription,
  getAccTitle,
  getConfig2 as getConfig,
  log,
  setAccDescription,
  setAccTitle
} from "./chunk-O2AGWWWV.mjs";

// src/diagrams/requirement/parser/requirementDiagram.jison
var parser = function() {
  var o = /* @__PURE__ */ __name(function(k, v, o2, l) {
    for (o2 = o2 || {}, l = k.length; l--; o2[k[l]] = v) ;
    return o2;
  }, "o"), $V0 = [1, 3], $V1 = [1, 4], $V2 = [1, 5], $V3 = [1, 6], $V4 = [5, 6, 8, 9, 11, 13, 31, 32, 33, 34, 35, 36, 44, 62, 63], $V5 = [1, 18], $V6 = [2, 7], $V7 = [1, 22], $V8 = [1, 23], $V9 = [1, 24], $Va = [1, 25], $Vb = [1, 26], $Vc = [1, 27], $Vd = [1, 20], $Ve = [1, 28], $Vf = [1, 29], $Vg = [62, 63], $Vh = [5, 8, 9, 11, 13, 31, 32, 33, 34, 35, 36, 44, 51, 53, 62, 63], $Vi = [1, 47], $Vj = [1, 48], $Vk = [1, 49], $Vl = [1, 50], $Vm = [1, 51], $Vn = [1, 52], $Vo = [1, 53], $Vp = [53, 54], $Vq = [1, 64], $Vr = [1, 60], $Vs = [1, 61], $Vt = [1, 62], $Vu = [1, 63], $Vv = [1, 65], $Vw = [1, 69], $Vx = [1, 70], $Vy = [1, 67], $Vz = [1, 68], $VA = [5, 8, 9, 11, 13, 31, 32, 33, 34, 35, 36, 44, 62, 63];
  var parser2 = {
    trace: /* @__PURE__ */ __name(function trace() {
    }, "trace"),
    yy: {},
    symbols_: { "error": 2, "start": 3, "directive": 4, "NEWLINE": 5, "RD": 6, "diagram": 7, "EOF": 8, "acc_title": 9, "acc_title_value": 10, "acc_descr": 11, "acc_descr_value": 12, "acc_descr_multiline_value": 13, "requirementDef": 14, "elementDef": 15, "relationshipDef": 16, "requirementType": 17, "requirementName": 18, "STRUCT_START": 19, "requirementBody": 20, "ID": 21, "COLONSEP": 22, "id": 23, "TEXT": 24, "text": 25, "RISK": 26, "riskLevel": 27, "VERIFYMTHD": 28, "verifyType": 29, "STRUCT_STOP": 30, "REQUIREMENT": 31, "FUNCTIONAL_REQUIREMENT": 32, "INTERFACE_REQUIREMENT": 33, "PERFORMANCE_REQUIREMENT": 34, "PHYSICAL_REQUIREMENT": 35, "DESIGN_CONSTRAINT": 36, "LOW_RISK": 37, "MED_RISK": 38, "HIGH_RISK": 39, "VERIFY_ANALYSIS": 40, "VERIFY_DEMONSTRATION": 41, "VERIFY_INSPECTION": 42, "VERIFY_TEST": 43, "ELEMENT": 44, "elementName": 45, "elementBody": 46, "TYPE": 47, "type": 48, "DOCREF": 49, "ref": 50, "END_ARROW_L": 51, "relationship": 52, "LINE": 53, "END_ARROW_R": 54, "CONTAINS": 55, "COPIES": 56, "DERIVES": 57, "SATISFIES": 58, "VERIFIES": 59, "REFINES": 60, "TRACES": 61, "unqString": 62, "qString": 63, "$accept": 0, "$end": 1 },
    terminals_: { 2: "error", 5: "NEWLINE", 6: "RD", 8: "EOF", 9: "acc_title", 10: "acc_title_value", 11: "acc_descr", 12: "acc_descr_value", 13: "acc_descr_multiline_value", 19: "STRUCT_START", 21: "ID", 22: "COLONSEP", 24: "TEXT", 26: "RISK", 28: "VERIFYMTHD", 30: "STRUCT_STOP", 31: "REQUIREMENT", 32: "FUNCTIONAL_REQUIREMENT", 33: "INTERFACE_REQUIREMENT", 34: "PERFORMANCE_REQUIREMENT", 35: "PHYSICAL_REQUIREMENT", 36: "DESIGN_CONSTRAINT", 37: "LOW_RISK", 38: "MED_RISK", 39: "HIGH_RISK", 40: "VERIFY_ANALYSIS", 41: "VERIFY_DEMONSTRATION", 42: "VERIFY_INSPECTION", 43: "VERIFY_TEST", 44: "ELEMENT", 47: "TYPE", 49: "DOCREF", 51: "END_ARROW_L", 53: "LINE", 54: "END_ARROW_R", 55: "CONTAINS", 56: "COPIES", 57: "DERIVES", 58: "SATISFIES", 59: "VERIFIES", 60: "REFINES", 61: "TRACES", 62: "unqString", 63: "qString" },
    productions_: [0, [3, 3], [3, 2], [3, 4], [4, 2], [4, 2], [4, 1], [7, 0], [7, 2], [7, 2], [7, 2], [7, 2], [7, 2], [14, 5], [20, 5], [20, 5], [20, 5], [20, 5], [20, 2], [20, 1], [17, 1], [17, 1], [17, 1], [17, 1], [17, 1], [17, 1], [27, 1], [27, 1], [27, 1], [29, 1], [29, 1], [29, 1], [29, 1], [15, 5], [46, 5], [46, 5], [46, 2], [46, 1], [16, 5], [16, 5], [52, 1], [52, 1], [52, 1], [52, 1], [52, 1], [52, 1], [52, 1], [18, 1], [18, 1], [23, 1], [23, 1], [25, 1], [25, 1], [45, 1], [45, 1], [48, 1], [48, 1], [50, 1], [50, 1]],
    performAction: /* @__PURE__ */ __name(function anonymous(yytext, yyleng, yylineno, yy, yystate, $$, _$) {
      var $0 = $$.length - 1;
      switch (yystate) {
        case 4:
          this.$ = $$[$0].trim();
          yy.setAccTitle(this.$);
          break;
        case 5:
        case 6:
          this.$ = $$[$0].trim();
          yy.setAccDescription(this.$);
          break;
        case 7:
          this.$ = [];
          break;
        case 13:
          yy.addRequirement($$[$0 - 3], $$[$0 - 4]);
          break;
        case 14:
          yy.setNewReqId($$[$0 - 2]);
          break;
        case 15:
          yy.setNewReqText($$[$0 - 2]);
          break;
        case 16:
          yy.setNewReqRisk($$[$0 - 2]);
          break;
        case 17:
          yy.setNewReqVerifyMethod($$[$0 - 2]);
          break;
        case 20:
          this.$ = yy.RequirementType.REQUIREMENT;
          break;
        case 21:
          this.$ = yy.RequirementType.FUNCTIONAL_REQUIREMENT;
          break;
        case 22:
          this.$ = yy.RequirementType.INTERFACE_REQUIREMENT;
          break;
        case 23:
          this.$ = yy.RequirementType.PERFORMANCE_REQUIREMENT;
          break;
        case 24:
          this.$ = yy.RequirementType.PHYSICAL_REQUIREMENT;
          break;
        case 25:
          this.$ = yy.RequirementType.DESIGN_CONSTRAINT;
          break;
        case 26:
          this.$ = yy.RiskLevel.LOW_RISK;
          break;
        case 27:
          this.$ = yy.RiskLevel.MED_RISK;
          break;
        case 28:
          this.$ = yy.RiskLevel.HIGH_RISK;
          break;
        case 29:
          this.$ = yy.VerifyType.VERIFY_ANALYSIS;
          break;
        case 30:
          this.$ = yy.VerifyType.VERIFY_DEMONSTRATION;
          break;
        case 31:
          this.$ = yy.VerifyType.VERIFY_INSPECTION;
          break;
        case 32:
          this.$ = yy.VerifyType.VERIFY_TEST;
          break;
        case 33:
          yy.addElement($$[$0 - 3]);
          break;
        case 34:
          yy.setNewElementType($$[$0 - 2]);
          break;
        case 35:
          yy.setNewElementDocRef($$[$0 - 2]);
          break;
        case 38:
          yy.addRelationship($$[$0 - 2], $$[$0], $$[$0 - 4]);
          break;
        case 39:
          yy.addRelationship($$[$0 - 2], $$[$0 - 4], $$[$0]);
          break;
        case 40:
          this.$ = yy.Relationships.CONTAINS;
          break;
        case 41:
          this.$ = yy.Relationships.COPIES;
          break;
        case 42:
          this.$ = yy.Relationships.DERIVES;
          break;
        case 43:
          this.$ = yy.Relationships.SATISFIES;
          break;
        case 44:
          this.$ = yy.Relationships.VERIFIES;
          break;
        case 45:
          this.$ = yy.Relationships.REFINES;
          break;
        case 46:
          this.$ = yy.Relationships.TRACES;
          break;
      }
    }, "anonymous"),
    table: [{ 3: 1, 4: 2, 6: $V0, 9: $V1, 11: $V2, 13: $V3 }, { 1: [3] }, { 3: 8, 4: 2, 5: [1, 7], 6: $V0, 9: $V1, 11: $V2, 13: $V3 }, { 5: [1, 9] }, { 10: [1, 10] }, { 12: [1, 11] }, o($V4, [2, 6]), { 3: 12, 4: 2, 6: $V0, 9: $V1, 11: $V2, 13: $V3 }, { 1: [2, 2] }, { 4: 17, 5: $V5, 7: 13, 8: $V6, 9: $V1, 11: $V2, 13: $V3, 14: 14, 15: 15, 16: 16, 17: 19, 23: 21, 31: $V7, 32: $V8, 33: $V9, 34: $Va, 35: $Vb, 36: $Vc, 44: $Vd, 62: $Ve, 63: $Vf }, o($V4, [2, 4]), o($V4, [2, 5]), { 1: [2, 1] }, { 8: [1, 30] }, { 4: 17, 5: $V5, 7: 31, 8: $V6, 9: $V1, 11: $V2, 13: $V3, 14: 14, 15: 15, 16: 16, 17: 19, 23: 21, 31: $V7, 32: $V8, 33: $V9, 34: $Va, 35: $Vb, 36: $Vc, 44: $Vd, 62: $Ve, 63: $Vf }, { 4: 17, 5: $V5, 7: 32, 8: $V6, 9: $V1, 11: $V2, 13: $V3, 14: 14, 15: 15, 16: 16, 17: 19, 23: 21, 31: $V7, 32: $V8, 33: $V9, 34: $Va, 35: $Vb, 36: $Vc, 44: $Vd, 62: $Ve, 63: $Vf }, { 4: 17, 5: $V5, 7: 33, 8: $V6, 9: $V1, 11: $V2, 13: $V3, 14: 14, 15: 15, 16: 16, 17: 19, 23: 21, 31: $V7, 32: $V8, 33: $V9, 34: $Va, 35: $Vb, 36: $Vc, 44: $Vd, 62: $Ve, 63: $Vf }, { 4: 17, 5: $V5, 7: 34, 8: $V6, 9: $V1, 11: $V2, 13: $V3, 14: 14, 15: 15, 16: 16, 17: 19, 23: 21, 31: $V7, 32: $V8, 33: $V9, 34: $Va, 35: $Vb, 36: $Vc, 44: $Vd, 62: $Ve, 63: $Vf }, { 4: 17, 5: $V5, 7: 35, 8: $V6, 9: $V1, 11: $V2, 13: $V3, 14: 14, 15: 15, 16: 16, 17: 19, 23: 21, 31: $V7, 32: $V8, 33: $V9, 34: $Va, 35: $Vb, 36: $Vc, 44: $Vd, 62: $Ve, 63: $Vf }, { 18: 36, 62: [1, 37], 63: [1, 38] }, { 45: 39, 62: [1, 40], 63: [1, 41] }, { 51: [1, 42], 53: [1, 43] }, o($Vg, [2, 20]), o($Vg, [2, 21]), o($Vg, [2, 22]), o($Vg, [2, 23]), o($Vg, [2, 24]), o($Vg, [2, 25]), o($Vh, [2, 49]), o($Vh, [2, 50]), { 1: [2, 3] }, { 8: [2, 8] }, { 8: [2, 9] }, { 8: [2, 10] }, { 8: [2, 11] }, { 8: [2, 12] }, { 19: [1, 44] }, { 19: [2, 47] }, { 19: [2, 48] }, { 19: [1, 45] }, { 19: [2, 53] }, { 19: [2, 54] }, { 52: 46, 55: $Vi, 56: $Vj, 57: $Vk, 58: $Vl, 59: $Vm, 60: $Vn, 61: $Vo }, { 52: 54, 55: $Vi, 56: $Vj, 57: $Vk, 58: $Vl, 59: $Vm, 60: $Vn, 61: $Vo }, { 5: [1, 55] }, { 5: [1, 56] }, { 53: [1, 57] }, o($Vp, [2, 40]), o($Vp, [2, 41]), o($Vp, [2, 42]), o($Vp, [2, 43]), o($Vp, [2, 44]), o($Vp, [2, 45]), o($Vp, [2, 46]), { 54: [1, 58] }, { 5: $Vq, 20: 59, 21: $Vr, 24: $Vs, 26: $Vt, 28: $Vu, 30: $Vv }, { 5: $Vw, 30: $Vx, 46: 66, 47: $Vy, 49: $Vz }, { 23: 71, 62: $Ve, 63: $Vf }, { 23: 72, 62: $Ve, 63: $Vf }, o($VA, [2, 13]), { 22: [1, 73] }, { 22: [1, 74] }, { 22: [1, 75] }, { 22: [1, 76] }, { 5: $Vq, 20: 77, 21: $Vr, 24: $Vs, 26: $Vt, 28: $Vu, 30: $Vv }, o($VA, [2, 19]), o($VA, [2, 33]), { 22: [1, 78] }, { 22: [1, 79] }, { 5: $Vw, 30: $Vx, 46: 80, 47: $Vy, 49: $Vz }, o($VA, [2, 37]), o($VA, [2, 38]), o($VA, [2, 39]), { 23: 81, 62: $Ve, 63: $Vf }, { 25: 82, 62: [1, 83], 63: [1, 84] }, { 27: 85, 37: [1, 86], 38: [1, 87], 39: [1, 88] }, { 29: 89, 40: [1, 90], 41: [1, 91], 42: [1, 92], 43: [1, 93] }, o($VA, [2, 18]), { 48: 94, 62: [1, 95], 63: [1, 96] }, { 50: 97, 62: [1, 98], 63: [1, 99] }, o($VA, [2, 36]), { 5: [1, 100] }, { 5: [1, 101] }, { 5: [2, 51] }, { 5: [2, 52] }, { 5: [1, 102] }, { 5: [2, 26] }, { 5: [2, 27] }, { 5: [2, 28] }, { 5: [1, 103] }, { 5: [2, 29] }, { 5: [2, 30] }, { 5: [2, 31] }, { 5: [2, 32] }, { 5: [1, 104] }, { 5: [2, 55] }, { 5: [2, 56] }, { 5: [1, 105] }, { 5: [2, 57] }, { 5: [2, 58] }, { 5: $Vq, 20: 106, 21: $Vr, 24: $Vs, 26: $Vt, 28: $Vu, 30: $Vv }, { 5: $Vq, 20: 107, 21: $Vr, 24: $Vs, 26: $Vt, 28: $Vu, 30: $Vv }, { 5: $Vq, 20: 108, 21: $Vr, 24: $Vs, 26: $Vt, 28: $Vu, 30: $Vv }, { 5: $Vq, 20: 109, 21: $Vr, 24: $Vs, 26: $Vt, 28: $Vu, 30: $Vv }, { 5: $Vw, 30: $Vx, 46: 110, 47: $Vy, 49: $Vz }, { 5: $Vw, 30: $Vx, 46: 111, 47: $Vy, 49: $Vz }, o($VA, [2, 14]), o($VA, [2, 15]), o($VA, [2, 16]), o($VA, [2, 17]), o($VA, [2, 34]), o($VA, [2, 35])],
    defaultActions: { 8: [2, 2], 12: [2, 1], 30: [2, 3], 31: [2, 8], 32: [2, 9], 33: [2, 10], 34: [2, 11], 35: [2, 12], 37: [2, 47], 38: [2, 48], 40: [2, 53], 41: [2, 54], 83: [2, 51], 84: [2, 52], 86: [2, 26], 87: [2, 27], 88: [2, 28], 90: [2, 29], 91: [2, 30], 92: [2, 31], 93: [2, 32], 95: [2, 55], 96: [2, 56], 98: [2, 57], 99: [2, 58] },
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
            return "title";
            break;
          case 1:
            this.begin("acc_title");
            return 9;
            break;
          case 2:
            this.popState();
            return "acc_title_value";
            break;
          case 3:
            this.begin("acc_descr");
            return 11;
            break;
          case 4:
            this.popState();
            return "acc_descr_value";
            break;
          case 5:
            this.begin("acc_descr_multiline");
            break;
          case 6:
            this.popState();
            break;
          case 7:
            return "acc_descr_multiline_value";
            break;
          case 8:
            return 5;
            break;
          case 9:
            break;
          case 10:
            break;
          case 11:
            break;
          case 12:
            return 8;
            break;
          case 13:
            return 6;
            break;
          case 14:
            return 19;
            break;
          case 15:
            return 30;
            break;
          case 16:
            return 22;
            break;
          case 17:
            return 21;
            break;
          case 18:
            return 24;
            break;
          case 19:
            return 26;
            break;
          case 20:
            return 28;
            break;
          case 21:
            return 31;
            break;
          case 22:
            return 32;
            break;
          case 23:
            return 33;
            break;
          case 24:
            return 34;
            break;
          case 25:
            return 35;
            break;
          case 26:
            return 36;
            break;
          case 27:
            return 37;
            break;
          case 28:
            return 38;
            break;
          case 29:
            return 39;
            break;
          case 30:
            return 40;
            break;
          case 31:
            return 41;
            break;
          case 32:
            return 42;
            break;
          case 33:
            return 43;
            break;
          case 34:
            return 44;
            break;
          case 35:
            return 55;
            break;
          case 36:
            return 56;
            break;
          case 37:
            return 57;
            break;
          case 38:
            return 58;
            break;
          case 39:
            return 59;
            break;
          case 40:
            return 60;
            break;
          case 41:
            return 61;
            break;
          case 42:
            return 47;
            break;
          case 43:
            return 49;
            break;
          case 44:
            return 51;
            break;
          case 45:
            return 54;
            break;
          case 46:
            return 53;
            break;
          case 47:
            this.begin("string");
            break;
          case 48:
            this.popState();
            break;
          case 49:
            return "qString";
            break;
          case 50:
            yy_.yytext = yy_.yytext.trim();
            return 62;
            break;
        }
      }, "anonymous"),
      rules: [/^(?:title\s[^#\n;]+)/i, /^(?:accTitle\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*\{\s*)/i, /^(?:[\}])/i, /^(?:[^\}]*)/i, /^(?:(\r?\n)+)/i, /^(?:\s+)/i, /^(?:#[^\n]*)/i, /^(?:%[^\n]*)/i, /^(?:$)/i, /^(?:requirementDiagram\b)/i, /^(?:\{)/i, /^(?:\})/i, /^(?::)/i, /^(?:id\b)/i, /^(?:text\b)/i, /^(?:risk\b)/i, /^(?:verifyMethod\b)/i, /^(?:requirement\b)/i, /^(?:functionalRequirement\b)/i, /^(?:interfaceRequirement\b)/i, /^(?:performanceRequirement\b)/i, /^(?:physicalRequirement\b)/i, /^(?:designConstraint\b)/i, /^(?:low\b)/i, /^(?:medium\b)/i, /^(?:high\b)/i, /^(?:analysis\b)/i, /^(?:demonstration\b)/i, /^(?:inspection\b)/i, /^(?:test\b)/i, /^(?:element\b)/i, /^(?:contains\b)/i, /^(?:copies\b)/i, /^(?:derives\b)/i, /^(?:satisfies\b)/i, /^(?:verifies\b)/i, /^(?:refines\b)/i, /^(?:traces\b)/i, /^(?:type\b)/i, /^(?:docref\b)/i, /^(?:<-)/i, /^(?:->)/i, /^(?:-)/i, /^(?:["])/i, /^(?:["])/i, /^(?:[^"]*)/i, /^(?:[\w][^\r\n\{\<\>\-\=]*)/i],
      conditions: { "acc_descr_multiline": { "rules": [6, 7], "inclusive": false }, "acc_descr": { "rules": [4], "inclusive": false }, "acc_title": { "rules": [2], "inclusive": false }, "unqString": { "rules": [], "inclusive": false }, "token": { "rules": [], "inclusive": false }, "string": { "rules": [48, 49], "inclusive": false }, "INITIAL": { "rules": [0, 1, 3, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 50], "inclusive": true } }
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
var requirementDiagram_default = parser;

// src/diagrams/requirement/requirementDb.js
var relations = [];
var latestRequirement = {};
var requirements = /* @__PURE__ */ new Map();
var latestElement = {};
var elements = /* @__PURE__ */ new Map();
var RequirementType = {
  REQUIREMENT: "Requirement",
  FUNCTIONAL_REQUIREMENT: "Functional Requirement",
  INTERFACE_REQUIREMENT: "Interface Requirement",
  PERFORMANCE_REQUIREMENT: "Performance Requirement",
  PHYSICAL_REQUIREMENT: "Physical Requirement",
  DESIGN_CONSTRAINT: "Design Constraint"
};
var RiskLevel = {
  LOW_RISK: "Low",
  MED_RISK: "Medium",
  HIGH_RISK: "High"
};
var VerifyType = {
  VERIFY_ANALYSIS: "Analysis",
  VERIFY_DEMONSTRATION: "Demonstration",
  VERIFY_INSPECTION: "Inspection",
  VERIFY_TEST: "Test"
};
var Relationships = {
  CONTAINS: "contains",
  COPIES: "copies",
  DERIVES: "derives",
  SATISFIES: "satisfies",
  VERIFIES: "verifies",
  REFINES: "refines",
  TRACES: "traces"
};
var addRequirement = /* @__PURE__ */ __name((name, type) => {
  if (!requirements.has(name)) {
    requirements.set(name, {
      name,
      type,
      id: latestRequirement.id,
      text: latestRequirement.text,
      risk: latestRequirement.risk,
      verifyMethod: latestRequirement.verifyMethod
    });
  }
  latestRequirement = {};
  return requirements.get(name);
}, "addRequirement");
var getRequirements = /* @__PURE__ */ __name(() => requirements, "getRequirements");
var setNewReqId = /* @__PURE__ */ __name((id) => {
  if (latestRequirement !== void 0) {
    latestRequirement.id = id;
  }
}, "setNewReqId");
var setNewReqText = /* @__PURE__ */ __name((text) => {
  if (latestRequirement !== void 0) {
    latestRequirement.text = text;
  }
}, "setNewReqText");
var setNewReqRisk = /* @__PURE__ */ __name((risk) => {
  if (latestRequirement !== void 0) {
    latestRequirement.risk = risk;
  }
}, "setNewReqRisk");
var setNewReqVerifyMethod = /* @__PURE__ */ __name((verifyMethod) => {
  if (latestRequirement !== void 0) {
    latestRequirement.verifyMethod = verifyMethod;
  }
}, "setNewReqVerifyMethod");
var addElement = /* @__PURE__ */ __name((name) => {
  if (!elements.has(name)) {
    elements.set(name, {
      name,
      type: latestElement.type,
      docRef: latestElement.docRef
    });
    log.info("Added new requirement: ", name);
  }
  latestElement = {};
  return elements.get(name);
}, "addElement");
var getElements = /* @__PURE__ */ __name(() => elements, "getElements");
var setNewElementType = /* @__PURE__ */ __name((type) => {
  if (latestElement !== void 0) {
    latestElement.type = type;
  }
}, "setNewElementType");
var setNewElementDocRef = /* @__PURE__ */ __name((docRef) => {
  if (latestElement !== void 0) {
    latestElement.docRef = docRef;
  }
}, "setNewElementDocRef");
var addRelationship = /* @__PURE__ */ __name((type, src, dst) => {
  relations.push({
    type,
    src,
    dst
  });
}, "addRelationship");
var getRelationships = /* @__PURE__ */ __name(() => relations, "getRelationships");
var clear2 = /* @__PURE__ */ __name(() => {
  relations = [];
  latestRequirement = {};
  requirements = /* @__PURE__ */ new Map();
  latestElement = {};
  elements = /* @__PURE__ */ new Map();
  clear();
}, "clear");
var requirementDb_default = {
  RequirementType,
  RiskLevel,
  VerifyType,
  Relationships,
  getConfig: /* @__PURE__ */ __name(() => getConfig().req, "getConfig"),
  addRequirement,
  getRequirements,
  setNewReqId,
  setNewReqText,
  setNewReqRisk,
  setNewReqVerifyMethod,
  setAccTitle,
  getAccTitle,
  setAccDescription,
  getAccDescription,
  addElement,
  getElements,
  setNewElementType,
  setNewElementDocRef,
  addRelationship,
  getRelationships,
  clear: clear2
};

// src/diagrams/requirement/styles.js
var getStyles = /* @__PURE__ */ __name((options) => `

  marker {
    fill: ${options.relationColor};
    stroke: ${options.relationColor};
  }

  marker.cross {
    stroke: ${options.lineColor};
  }

  svg {
    font-family: ${options.fontFamily};
    font-size: ${options.fontSize};
  }

  .reqBox {
    fill: ${options.requirementBackground};
    fill-opacity: 1.0;
    stroke: ${options.requirementBorderColor};
    stroke-width: ${options.requirementBorderSize};
  }
  
  .reqTitle, .reqLabel{
    fill:  ${options.requirementTextColor};
  }
  .reqLabelBox {
    fill: ${options.relationLabelBackground};
    fill-opacity: 1.0;
  }

  .req-title-line {
    stroke: ${options.requirementBorderColor};
    stroke-width: ${options.requirementBorderSize};
  }
  .relationshipLine {
    stroke: ${options.relationColor};
    stroke-width: 1;
  }
  .relationshipLabel {
    fill: ${options.relationLabelColor};
  }

`, "getStyles");
var styles_default = getStyles;

// src/diagrams/requirement/requirementRenderer.js
import { line, select } from "d3";
import { layout as dagreLayout } from "dagre-d3-es/src/dagre/index.js";
import * as graphlib from "dagre-d3-es/src/graphlib/index.js";

// src/diagrams/requirement/requirementMarkers.js
var ReqMarkers = {
  CONTAINS: "contains",
  ARROW: "arrow"
};
var insertLineEndings = /* @__PURE__ */ __name((parentNode, conf2) => {
  let containsNode = parentNode.append("defs").append("marker").attr("id", ReqMarkers.CONTAINS + "_line_ending").attr("refX", 0).attr("refY", conf2.line_height / 2).attr("markerWidth", conf2.line_height).attr("markerHeight", conf2.line_height).attr("orient", "auto").append("g");
  containsNode.append("circle").attr("cx", conf2.line_height / 2).attr("cy", conf2.line_height / 2).attr("r", conf2.line_height / 2).attr("fill", "none");
  containsNode.append("line").attr("x1", 0).attr("x2", conf2.line_height).attr("y1", conf2.line_height / 2).attr("y2", conf2.line_height / 2).attr("stroke-width", 1);
  containsNode.append("line").attr("y1", 0).attr("y2", conf2.line_height).attr("x1", conf2.line_height / 2).attr("x2", conf2.line_height / 2).attr("stroke-width", 1);
  parentNode.append("defs").append("marker").attr("id", ReqMarkers.ARROW + "_line_ending").attr("refX", conf2.line_height).attr("refY", 0.5 * conf2.line_height).attr("markerWidth", conf2.line_height).attr("markerHeight", conf2.line_height).attr("orient", "auto").append("path").attr(
    "d",
    `M0,0
      L${conf2.line_height},${conf2.line_height / 2}
      M${conf2.line_height},${conf2.line_height / 2}
      L0,${conf2.line_height}`
  ).attr("stroke-width", 1);
}, "insertLineEndings");
var requirementMarkers_default = {
  ReqMarkers,
  insertLineEndings
};

// src/diagrams/requirement/requirementRenderer.js
var conf = {};
var relCnt = 0;
var newRectNode = /* @__PURE__ */ __name((parentNode, id) => {
  return parentNode.insert("rect", "#" + id).attr("class", "req reqBox").attr("x", 0).attr("y", 0).attr("width", conf.rect_min_width + "px").attr("height", conf.rect_min_height + "px");
}, "newRectNode");
var newTitleNode = /* @__PURE__ */ __name((parentNode, id, txts) => {
  let x = conf.rect_min_width / 2;
  let title = parentNode.append("text").attr("class", "req reqLabel reqTitle").attr("id", id).attr("x", x).attr("y", conf.rect_padding).attr("dominant-baseline", "hanging");
  let i = 0;
  txts.forEach((textStr) => {
    if (i == 0) {
      title.append("tspan").attr("text-anchor", "middle").attr("x", conf.rect_min_width / 2).attr("dy", 0).text(textStr);
    } else {
      title.append("tspan").attr("text-anchor", "middle").attr("x", conf.rect_min_width / 2).attr("dy", conf.line_height * 0.75).text(textStr);
    }
    i++;
  });
  let yPadding = 1.5 * conf.rect_padding;
  let linePadding = i * conf.line_height * 0.75;
  let totalY = yPadding + linePadding;
  parentNode.append("line").attr("class", "req-title-line").attr("x1", "0").attr("x2", conf.rect_min_width).attr("y1", totalY).attr("y2", totalY);
  return {
    titleNode: title,
    y: totalY
  };
}, "newTitleNode");
var newBodyNode = /* @__PURE__ */ __name((parentNode, id, txts, yStart) => {
  let body = parentNode.append("text").attr("class", "req reqLabel").attr("id", id).attr("x", conf.rect_padding).attr("y", yStart).attr("dominant-baseline", "hanging");
  let currentRow = 0;
  const charLimit = 30;
  let wrappedTxts = [];
  txts.forEach((textStr) => {
    let currentTextLen = textStr.length;
    while (currentTextLen > charLimit && currentRow < 3) {
      let firstPart = textStr.substring(0, charLimit);
      textStr = textStr.substring(charLimit, textStr.length);
      currentTextLen = textStr.length;
      wrappedTxts[wrappedTxts.length] = firstPart;
      currentRow++;
    }
    if (currentRow == 3) {
      let lastStr = wrappedTxts[wrappedTxts.length - 1];
      wrappedTxts[wrappedTxts.length - 1] = lastStr.substring(0, lastStr.length - 4) + "...";
    } else {
      wrappedTxts[wrappedTxts.length] = textStr;
    }
    currentRow = 0;
  });
  wrappedTxts.forEach((textStr) => {
    body.append("tspan").attr("x", conf.rect_padding).attr("dy", conf.line_height).text(textStr);
  });
  return body;
}, "newBodyNode");
var addEdgeLabel = /* @__PURE__ */ __name((parentNode, svgPath, conf2, txt) => {
  const len = svgPath.node().getTotalLength();
  const labelPoint = svgPath.node().getPointAtLength(len * 0.5);
  const labelId = "rel" + relCnt;
  relCnt++;
  const labelNode = parentNode.append("text").attr("class", "req relationshipLabel").attr("id", labelId).attr("x", labelPoint.x).attr("y", labelPoint.y).attr("text-anchor", "middle").attr("dominant-baseline", "middle").text(txt);
  const labelBBox = labelNode.node().getBBox();
  parentNode.insert("rect", "#" + labelId).attr("class", "req reqLabelBox").attr("x", labelPoint.x - labelBBox.width / 2).attr("y", labelPoint.y - labelBBox.height / 2).attr("width", labelBBox.width).attr("height", labelBBox.height).attr("fill", "white").attr("fill-opacity", "85%");
}, "addEdgeLabel");
var drawRelationshipFromLayout = /* @__PURE__ */ __name(function(svg, rel, g, insert, diagObj) {
  const edge = g.edge(elementString(rel.src), elementString(rel.dst));
  const lineFunction = line().x(function(d) {
    return d.x;
  }).y(function(d) {
    return d.y;
  });
  const svgPath = svg.insert("path", "#" + insert).attr("class", "er relationshipLine").attr("d", lineFunction(edge.points)).attr("fill", "none");
  if (rel.type == diagObj.db.Relationships.CONTAINS) {
    svgPath.attr(
      "marker-start",
      "url(" + common_default.getUrl(conf.arrowMarkerAbsolute) + "#" + rel.type + "_line_ending)"
    );
  } else {
    svgPath.attr("stroke-dasharray", "10,7");
    svgPath.attr(
      "marker-end",
      "url(" + common_default.getUrl(conf.arrowMarkerAbsolute) + "#" + requirementMarkers_default.ReqMarkers.ARROW + "_line_ending)"
    );
  }
  addEdgeLabel(svg, svgPath, conf, `<<${rel.type}>>`);
  return;
}, "drawRelationshipFromLayout");
var drawReqs = /* @__PURE__ */ __name((reqs, graph, svgNode) => {
  reqs.forEach((req, reqName) => {
    reqName = elementString(reqName);
    log.info("Added new requirement: ", reqName);
    const groupNode = svgNode.append("g").attr("id", reqName);
    const textId = "req-" + reqName;
    const rectNode = newRectNode(groupNode, textId);
    let nodes = [];
    let titleNodeInfo = newTitleNode(groupNode, reqName + "_title", [
      `<<${req.type}>>`,
      `${req.name}`
    ]);
    nodes.push(titleNodeInfo.titleNode);
    let bodyNode = newBodyNode(
      groupNode,
      reqName + "_body",
      [
        `Id: ${req.id}`,
        `Text: ${req.text}`,
        `Risk: ${req.risk}`,
        `Verification: ${req.verifyMethod}`
      ],
      titleNodeInfo.y
    );
    nodes.push(bodyNode);
    const rectBBox = rectNode.node().getBBox();
    graph.setNode(reqName, {
      width: rectBBox.width,
      height: rectBBox.height,
      shape: "rect",
      id: reqName
    });
  });
}, "drawReqs");
var drawElements = /* @__PURE__ */ __name((els, graph, svgNode) => {
  els.forEach((el, elName) => {
    const id = elementString(elName);
    const groupNode = svgNode.append("g").attr("id", id);
    const textId = "element-" + id;
    const rectNode = newRectNode(groupNode, textId);
    let nodes = [];
    let titleNodeInfo = newTitleNode(groupNode, textId + "_title", [`<<Element>>`, `${elName}`]);
    nodes.push(titleNodeInfo.titleNode);
    let bodyNode = newBodyNode(
      groupNode,
      textId + "_body",
      [`Type: ${el.type || "Not Specified"}`, `Doc Ref: ${el.docRef || "None"}`],
      titleNodeInfo.y
    );
    nodes.push(bodyNode);
    const rectBBox = rectNode.node().getBBox();
    graph.setNode(id, {
      width: rectBBox.width,
      height: rectBBox.height,
      shape: "rect",
      id
    });
  });
}, "drawElements");
var addRelationships = /* @__PURE__ */ __name((relationships, g) => {
  relationships.forEach(function(r) {
    let src = elementString(r.src);
    let dst = elementString(r.dst);
    g.setEdge(src, dst, { relationship: r });
  });
  return relationships;
}, "addRelationships");
var adjustEntities = /* @__PURE__ */ __name(function(svgNode, graph) {
  graph.nodes().forEach(function(v) {
    if (v !== void 0 && graph.node(v) !== void 0) {
      svgNode.select("#" + v);
      svgNode.select("#" + v).attr(
        "transform",
        "translate(" + (graph.node(v).x - graph.node(v).width / 2) + "," + (graph.node(v).y - graph.node(v).height / 2) + " )"
      );
    }
  });
  return;
}, "adjustEntities");
var elementString = /* @__PURE__ */ __name((str) => {
  return str.replace(/\s/g, "").replace(/\./g, "_");
}, "elementString");
var draw = /* @__PURE__ */ __name((text, id, _version, diagObj) => {
  conf = getConfig().requirement;
  const securityLevel = conf.securityLevel;
  let sandboxElement;
  if (securityLevel === "sandbox") {
    sandboxElement = select("#i" + id);
  }
  const root = securityLevel === "sandbox" ? select(sandboxElement.nodes()[0].contentDocument.body) : select("body");
  const svg = root.select(`[id='${id}']`);
  requirementMarkers_default.insertLineEndings(svg, conf);
  const g = new graphlib.Graph({
    multigraph: false,
    compound: false,
    directed: true
  }).setGraph({
    rankdir: conf.layoutDirection,
    marginx: 20,
    marginy: 20,
    nodesep: 100,
    edgesep: 100,
    ranksep: 100
  }).setDefaultEdgeLabel(function() {
    return {};
  });
  let requirements2 = diagObj.db.getRequirements();
  let elements2 = diagObj.db.getElements();
  let relationships = diagObj.db.getRelationships();
  drawReqs(requirements2, g, svg);
  drawElements(elements2, g, svg);
  addRelationships(relationships, g);
  dagreLayout(g);
  adjustEntities(svg, g);
  relationships.forEach(function(rel) {
    drawRelationshipFromLayout(svg, rel, g, id, diagObj);
  });
  const padding = conf.rect_padding;
  const svgBounds = svg.node().getBBox();
  const width = svgBounds.width + padding * 2;
  const height = svgBounds.height + padding * 2;
  configureSvgSize(svg, height, width, conf.useMaxWidth);
  svg.attr("viewBox", `${svgBounds.x - padding} ${svgBounds.y - padding} ${width} ${height}`);
}, "draw");
var requirementRenderer_default = {
  draw
};

// src/diagrams/requirement/requirementDiagram.ts
var diagram = {
  parser: requirementDiagram_default,
  db: requirementDb_default,
  renderer: requirementRenderer_default,
  styles: styles_default
};
export {
  diagram
};
