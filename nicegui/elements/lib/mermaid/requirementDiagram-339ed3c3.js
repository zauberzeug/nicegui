import { g as getConfig, l as log, f as select, e as common } from "./config-b4fa35bb.js";
import { m as mermaidAPI } from "./mermaidAPI-6f22a815.js";
import { s as setAccTitle, g as getAccTitle, b as setAccDescription, a as getAccDescription, f as clear$1 } from "./commonDb-7f40ab5a.js";
import { G as Graph, l as layout } from "./layout-4663fc19.js";
import { c as configureSvgSize } from "./setupGraphViewbox-16a0ba81.js";
import { l as line } from "./isPlainObject-91dd8bc9.js";
import "./utils-872dfc50.js";
import "./errorRenderer-ebf63d74.js";
import "./array-b7dcf730.js";
import "./constant-b644328d.js";
var parser = function() {
  var o = function(k, v, o2, l) {
    for (o2 = o2 || {}, l = k.length; l--; o2[k[l]] = v)
      ;
    return o2;
  }, $V0 = [1, 3], $V1 = [1, 5], $V2 = [1, 6], $V3 = [1, 7], $V4 = [1, 8], $V5 = [5, 6, 8, 14, 16, 18, 19, 40, 41, 42, 43, 44, 45, 53, 71, 72], $V6 = [1, 22], $V7 = [2, 13], $V8 = [1, 26], $V9 = [1, 27], $Va = [1, 28], $Vb = [1, 29], $Vc = [1, 30], $Vd = [1, 31], $Ve = [1, 24], $Vf = [1, 32], $Vg = [1, 33], $Vh = [1, 36], $Vi = [71, 72], $Vj = [5, 8, 14, 16, 18, 19, 40, 41, 42, 43, 44, 45, 53, 60, 62, 71, 72], $Vk = [1, 56], $Vl = [1, 57], $Vm = [1, 58], $Vn = [1, 59], $Vo = [1, 60], $Vp = [1, 61], $Vq = [1, 62], $Vr = [62, 63], $Vs = [1, 74], $Vt = [1, 70], $Vu = [1, 71], $Vv = [1, 72], $Vw = [1, 73], $Vx = [1, 75], $Vy = [1, 79], $Vz = [1, 80], $VA = [1, 77], $VB = [1, 78], $VC = [5, 8, 14, 16, 18, 19, 40, 41, 42, 43, 44, 45, 53, 71, 72];
  var parser2 = {
    trace: function trace() {
    },
    yy: {},
    symbols_: { "error": 2, "start": 3, "directive": 4, "NEWLINE": 5, "RD": 6, "diagram": 7, "EOF": 8, "openDirective": 9, "typeDirective": 10, "closeDirective": 11, ":": 12, "argDirective": 13, "acc_title": 14, "acc_title_value": 15, "acc_descr": 16, "acc_descr_value": 17, "acc_descr_multiline_value": 18, "open_directive": 19, "type_directive": 20, "arg_directive": 21, "close_directive": 22, "requirementDef": 23, "elementDef": 24, "relationshipDef": 25, "requirementType": 26, "requirementName": 27, "STRUCT_START": 28, "requirementBody": 29, "ID": 30, "COLONSEP": 31, "id": 32, "TEXT": 33, "text": 34, "RISK": 35, "riskLevel": 36, "VERIFYMTHD": 37, "verifyType": 38, "STRUCT_STOP": 39, "REQUIREMENT": 40, "FUNCTIONAL_REQUIREMENT": 41, "INTERFACE_REQUIREMENT": 42, "PERFORMANCE_REQUIREMENT": 43, "PHYSICAL_REQUIREMENT": 44, "DESIGN_CONSTRAINT": 45, "LOW_RISK": 46, "MED_RISK": 47, "HIGH_RISK": 48, "VERIFY_ANALYSIS": 49, "VERIFY_DEMONSTRATION": 50, "VERIFY_INSPECTION": 51, "VERIFY_TEST": 52, "ELEMENT": 53, "elementName": 54, "elementBody": 55, "TYPE": 56, "type": 57, "DOCREF": 58, "ref": 59, "END_ARROW_L": 60, "relationship": 61, "LINE": 62, "END_ARROW_R": 63, "CONTAINS": 64, "COPIES": 65, "DERIVES": 66, "SATISFIES": 67, "VERIFIES": 68, "REFINES": 69, "TRACES": 70, "unqString": 71, "qString": 72, "$accept": 0, "$end": 1 },
    terminals_: { 2: "error", 5: "NEWLINE", 6: "RD", 8: "EOF", 12: ":", 14: "acc_title", 15: "acc_title_value", 16: "acc_descr", 17: "acc_descr_value", 18: "acc_descr_multiline_value", 19: "open_directive", 20: "type_directive", 21: "arg_directive", 22: "close_directive", 28: "STRUCT_START", 30: "ID", 31: "COLONSEP", 33: "TEXT", 35: "RISK", 37: "VERIFYMTHD", 39: "STRUCT_STOP", 40: "REQUIREMENT", 41: "FUNCTIONAL_REQUIREMENT", 42: "INTERFACE_REQUIREMENT", 43: "PERFORMANCE_REQUIREMENT", 44: "PHYSICAL_REQUIREMENT", 45: "DESIGN_CONSTRAINT", 46: "LOW_RISK", 47: "MED_RISK", 48: "HIGH_RISK", 49: "VERIFY_ANALYSIS", 50: "VERIFY_DEMONSTRATION", 51: "VERIFY_INSPECTION", 52: "VERIFY_TEST", 53: "ELEMENT", 56: "TYPE", 58: "DOCREF", 60: "END_ARROW_L", 62: "LINE", 63: "END_ARROW_R", 64: "CONTAINS", 65: "COPIES", 66: "DERIVES", 67: "SATISFIES", 68: "VERIFIES", 69: "REFINES", 70: "TRACES", 71: "unqString", 72: "qString" },
    productions_: [0, [3, 3], [3, 2], [3, 4], [4, 3], [4, 5], [4, 2], [4, 2], [4, 1], [9, 1], [10, 1], [13, 1], [11, 1], [7, 0], [7, 2], [7, 2], [7, 2], [7, 2], [7, 2], [23, 5], [29, 5], [29, 5], [29, 5], [29, 5], [29, 2], [29, 1], [26, 1], [26, 1], [26, 1], [26, 1], [26, 1], [26, 1], [36, 1], [36, 1], [36, 1], [38, 1], [38, 1], [38, 1], [38, 1], [24, 5], [55, 5], [55, 5], [55, 2], [55, 1], [25, 5], [25, 5], [61, 1], [61, 1], [61, 1], [61, 1], [61, 1], [61, 1], [61, 1], [27, 1], [27, 1], [32, 1], [32, 1], [34, 1], [34, 1], [54, 1], [54, 1], [57, 1], [57, 1], [59, 1], [59, 1]],
    performAction: function anonymous(yytext, yyleng, yylineno, yy, yystate, $$, _$) {
      var $0 = $$.length - 1;
      switch (yystate) {
        case 6:
          this.$ = $$[$0].trim();
          yy.setAccTitle(this.$);
          break;
        case 7:
        case 8:
          this.$ = $$[$0].trim();
          yy.setAccDescription(this.$);
          break;
        case 9:
          yy.parseDirective("%%{", "open_directive");
          break;
        case 10:
          yy.parseDirective($$[$0], "type_directive");
          break;
        case 11:
          $$[$0] = $$[$0].trim().replace(/'/g, '"');
          yy.parseDirective($$[$0], "arg_directive");
          break;
        case 12:
          yy.parseDirective("}%%", "close_directive", "pie");
          break;
        case 13:
          this.$ = [];
          break;
        case 19:
          yy.addRequirement($$[$0 - 3], $$[$0 - 4]);
          break;
        case 20:
          yy.setNewReqId($$[$0 - 2]);
          break;
        case 21:
          yy.setNewReqText($$[$0 - 2]);
          break;
        case 22:
          yy.setNewReqRisk($$[$0 - 2]);
          break;
        case 23:
          yy.setNewReqVerifyMethod($$[$0 - 2]);
          break;
        case 26:
          this.$ = yy.RequirementType.REQUIREMENT;
          break;
        case 27:
          this.$ = yy.RequirementType.FUNCTIONAL_REQUIREMENT;
          break;
        case 28:
          this.$ = yy.RequirementType.INTERFACE_REQUIREMENT;
          break;
        case 29:
          this.$ = yy.RequirementType.PERFORMANCE_REQUIREMENT;
          break;
        case 30:
          this.$ = yy.RequirementType.PHYSICAL_REQUIREMENT;
          break;
        case 31:
          this.$ = yy.RequirementType.DESIGN_CONSTRAINT;
          break;
        case 32:
          this.$ = yy.RiskLevel.LOW_RISK;
          break;
        case 33:
          this.$ = yy.RiskLevel.MED_RISK;
          break;
        case 34:
          this.$ = yy.RiskLevel.HIGH_RISK;
          break;
        case 35:
          this.$ = yy.VerifyType.VERIFY_ANALYSIS;
          break;
        case 36:
          this.$ = yy.VerifyType.VERIFY_DEMONSTRATION;
          break;
        case 37:
          this.$ = yy.VerifyType.VERIFY_INSPECTION;
          break;
        case 38:
          this.$ = yy.VerifyType.VERIFY_TEST;
          break;
        case 39:
          yy.addElement($$[$0 - 3]);
          break;
        case 40:
          yy.setNewElementType($$[$0 - 2]);
          break;
        case 41:
          yy.setNewElementDocRef($$[$0 - 2]);
          break;
        case 44:
          yy.addRelationship($$[$0 - 2], $$[$0], $$[$0 - 4]);
          break;
        case 45:
          yy.addRelationship($$[$0 - 2], $$[$0 - 4], $$[$0]);
          break;
        case 46:
          this.$ = yy.Relationships.CONTAINS;
          break;
        case 47:
          this.$ = yy.Relationships.COPIES;
          break;
        case 48:
          this.$ = yy.Relationships.DERIVES;
          break;
        case 49:
          this.$ = yy.Relationships.SATISFIES;
          break;
        case 50:
          this.$ = yy.Relationships.VERIFIES;
          break;
        case 51:
          this.$ = yy.Relationships.REFINES;
          break;
        case 52:
          this.$ = yy.Relationships.TRACES;
          break;
      }
    },
    table: [{ 3: 1, 4: 2, 6: $V0, 9: 4, 14: $V1, 16: $V2, 18: $V3, 19: $V4 }, { 1: [3] }, { 3: 10, 4: 2, 5: [1, 9], 6: $V0, 9: 4, 14: $V1, 16: $V2, 18: $V3, 19: $V4 }, { 5: [1, 11] }, { 10: 12, 20: [1, 13] }, { 15: [1, 14] }, { 17: [1, 15] }, o($V5, [2, 8]), { 20: [2, 9] }, { 3: 16, 4: 2, 6: $V0, 9: 4, 14: $V1, 16: $V2, 18: $V3, 19: $V4 }, { 1: [2, 2] }, { 4: 21, 5: $V6, 7: 17, 8: $V7, 9: 4, 14: $V1, 16: $V2, 18: $V3, 19: $V4, 23: 18, 24: 19, 25: 20, 26: 23, 32: 25, 40: $V8, 41: $V9, 42: $Va, 43: $Vb, 44: $Vc, 45: $Vd, 53: $Ve, 71: $Vf, 72: $Vg }, { 11: 34, 12: [1, 35], 22: $Vh }, o([12, 22], [2, 10]), o($V5, [2, 6]), o($V5, [2, 7]), { 1: [2, 1] }, { 8: [1, 37] }, { 4: 21, 5: $V6, 7: 38, 8: $V7, 9: 4, 14: $V1, 16: $V2, 18: $V3, 19: $V4, 23: 18, 24: 19, 25: 20, 26: 23, 32: 25, 40: $V8, 41: $V9, 42: $Va, 43: $Vb, 44: $Vc, 45: $Vd, 53: $Ve, 71: $Vf, 72: $Vg }, { 4: 21, 5: $V6, 7: 39, 8: $V7, 9: 4, 14: $V1, 16: $V2, 18: $V3, 19: $V4, 23: 18, 24: 19, 25: 20, 26: 23, 32: 25, 40: $V8, 41: $V9, 42: $Va, 43: $Vb, 44: $Vc, 45: $Vd, 53: $Ve, 71: $Vf, 72: $Vg }, { 4: 21, 5: $V6, 7: 40, 8: $V7, 9: 4, 14: $V1, 16: $V2, 18: $V3, 19: $V4, 23: 18, 24: 19, 25: 20, 26: 23, 32: 25, 40: $V8, 41: $V9, 42: $Va, 43: $Vb, 44: $Vc, 45: $Vd, 53: $Ve, 71: $Vf, 72: $Vg }, { 4: 21, 5: $V6, 7: 41, 8: $V7, 9: 4, 14: $V1, 16: $V2, 18: $V3, 19: $V4, 23: 18, 24: 19, 25: 20, 26: 23, 32: 25, 40: $V8, 41: $V9, 42: $Va, 43: $Vb, 44: $Vc, 45: $Vd, 53: $Ve, 71: $Vf, 72: $Vg }, { 4: 21, 5: $V6, 7: 42, 8: $V7, 9: 4, 14: $V1, 16: $V2, 18: $V3, 19: $V4, 23: 18, 24: 19, 25: 20, 26: 23, 32: 25, 40: $V8, 41: $V9, 42: $Va, 43: $Vb, 44: $Vc, 45: $Vd, 53: $Ve, 71: $Vf, 72: $Vg }, { 27: 43, 71: [1, 44], 72: [1, 45] }, { 54: 46, 71: [1, 47], 72: [1, 48] }, { 60: [1, 49], 62: [1, 50] }, o($Vi, [2, 26]), o($Vi, [2, 27]), o($Vi, [2, 28]), o($Vi, [2, 29]), o($Vi, [2, 30]), o($Vi, [2, 31]), o($Vj, [2, 55]), o($Vj, [2, 56]), o($V5, [2, 4]), { 13: 51, 21: [1, 52] }, o($V5, [2, 12]), { 1: [2, 3] }, { 8: [2, 14] }, { 8: [2, 15] }, { 8: [2, 16] }, { 8: [2, 17] }, { 8: [2, 18] }, { 28: [1, 53] }, { 28: [2, 53] }, { 28: [2, 54] }, { 28: [1, 54] }, { 28: [2, 59] }, { 28: [2, 60] }, { 61: 55, 64: $Vk, 65: $Vl, 66: $Vm, 67: $Vn, 68: $Vo, 69: $Vp, 70: $Vq }, { 61: 63, 64: $Vk, 65: $Vl, 66: $Vm, 67: $Vn, 68: $Vo, 69: $Vp, 70: $Vq }, { 11: 64, 22: $Vh }, { 22: [2, 11] }, { 5: [1, 65] }, { 5: [1, 66] }, { 62: [1, 67] }, o($Vr, [2, 46]), o($Vr, [2, 47]), o($Vr, [2, 48]), o($Vr, [2, 49]), o($Vr, [2, 50]), o($Vr, [2, 51]), o($Vr, [2, 52]), { 63: [1, 68] }, o($V5, [2, 5]), { 5: $Vs, 29: 69, 30: $Vt, 33: $Vu, 35: $Vv, 37: $Vw, 39: $Vx }, { 5: $Vy, 39: $Vz, 55: 76, 56: $VA, 58: $VB }, { 32: 81, 71: $Vf, 72: $Vg }, { 32: 82, 71: $Vf, 72: $Vg }, o($VC, [2, 19]), { 31: [1, 83] }, { 31: [1, 84] }, { 31: [1, 85] }, { 31: [1, 86] }, { 5: $Vs, 29: 87, 30: $Vt, 33: $Vu, 35: $Vv, 37: $Vw, 39: $Vx }, o($VC, [2, 25]), o($VC, [2, 39]), { 31: [1, 88] }, { 31: [1, 89] }, { 5: $Vy, 39: $Vz, 55: 90, 56: $VA, 58: $VB }, o($VC, [2, 43]), o($VC, [2, 44]), o($VC, [2, 45]), { 32: 91, 71: $Vf, 72: $Vg }, { 34: 92, 71: [1, 93], 72: [1, 94] }, { 36: 95, 46: [1, 96], 47: [1, 97], 48: [1, 98] }, { 38: 99, 49: [1, 100], 50: [1, 101], 51: [1, 102], 52: [1, 103] }, o($VC, [2, 24]), { 57: 104, 71: [1, 105], 72: [1, 106] }, { 59: 107, 71: [1, 108], 72: [1, 109] }, o($VC, [2, 42]), { 5: [1, 110] }, { 5: [1, 111] }, { 5: [2, 57] }, { 5: [2, 58] }, { 5: [1, 112] }, { 5: [2, 32] }, { 5: [2, 33] }, { 5: [2, 34] }, { 5: [1, 113] }, { 5: [2, 35] }, { 5: [2, 36] }, { 5: [2, 37] }, { 5: [2, 38] }, { 5: [1, 114] }, { 5: [2, 61] }, { 5: [2, 62] }, { 5: [1, 115] }, { 5: [2, 63] }, { 5: [2, 64] }, { 5: $Vs, 29: 116, 30: $Vt, 33: $Vu, 35: $Vv, 37: $Vw, 39: $Vx }, { 5: $Vs, 29: 117, 30: $Vt, 33: $Vu, 35: $Vv, 37: $Vw, 39: $Vx }, { 5: $Vs, 29: 118, 30: $Vt, 33: $Vu, 35: $Vv, 37: $Vw, 39: $Vx }, { 5: $Vs, 29: 119, 30: $Vt, 33: $Vu, 35: $Vv, 37: $Vw, 39: $Vx }, { 5: $Vy, 39: $Vz, 55: 120, 56: $VA, 58: $VB }, { 5: $Vy, 39: $Vz, 55: 121, 56: $VA, 58: $VB }, o($VC, [2, 20]), o($VC, [2, 21]), o($VC, [2, 22]), o($VC, [2, 23]), o($VC, [2, 40]), o($VC, [2, 41])],
    defaultActions: { 8: [2, 9], 10: [2, 2], 16: [2, 1], 37: [2, 3], 38: [2, 14], 39: [2, 15], 40: [2, 16], 41: [2, 17], 42: [2, 18], 44: [2, 53], 45: [2, 54], 47: [2, 59], 48: [2, 60], 52: [2, 11], 93: [2, 57], 94: [2, 58], 96: [2, 32], 97: [2, 33], 98: [2, 34], 100: [2, 35], 101: [2, 36], 102: [2, 37], 103: [2, 38], 105: [2, 61], 106: [2, 62], 108: [2, 63], 109: [2, 64] },
    parseError: function parseError(str, hash) {
      if (hash.recoverable) {
        this.trace(str);
      } else {
        var error = new Error(str);
        error.hash = hash;
        throw error;
      }
    },
    parse: function parse(input) {
      var self = this, stack = [0], tstack = [], vstack = [null], lstack = [], table = this.table, yytext = "", yylineno = 0, yyleng = 0, TERROR = 2, EOF = 1;
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
      var symbol, state, action, r, yyval = {}, p, len, newState, expected;
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
            {
              yyleng = lexer2.yyleng;
              yytext = lexer2.yytext;
              yylineno = lexer2.yylineno;
              yyloc = lexer2.yylloc;
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
    }
  };
  var lexer = function() {
    var lexer2 = {
      EOF: 1,
      parseError: function parseError(str, hash) {
        if (this.yy.parser) {
          this.yy.parser.parseError(str, hash);
        } else {
          throw new Error(str);
        }
      },
      // resets the lexer, sets new input
      setInput: function(input, yy) {
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
      },
      // consumes and returns one char from the input
      input: function() {
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
      },
      // unshifts one char (or a string) into the input
      unput: function(ch) {
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
      },
      // When called from action, caches matched text and appends it on next action
      more: function() {
        this._more = true;
        return this;
      },
      // When called from action, signals the lexer that this rule fails to match the input, so the next matching rule (regex) should be tested instead.
      reject: function() {
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
      },
      // retain first n characters of the match
      less: function(n) {
        this.unput(this.match.slice(n));
      },
      // displays already matched input, i.e. for error messages
      pastInput: function() {
        var past = this.matched.substr(0, this.matched.length - this.match.length);
        return (past.length > 20 ? "..." : "") + past.substr(-20).replace(/\n/g, "");
      },
      // displays upcoming input, i.e. for error messages
      upcomingInput: function() {
        var next = this.match;
        if (next.length < 20) {
          next += this._input.substr(0, 20 - next.length);
        }
        return (next.substr(0, 20) + (next.length > 20 ? "..." : "")).replace(/\n/g, "");
      },
      // displays the character position where the lexing error occurred, i.e. for error messages
      showPosition: function() {
        var pre = this.pastInput();
        var c = new Array(pre.length + 1).join("-");
        return pre + this.upcomingInput() + "\n" + c + "^";
      },
      // test the lexed token: return FALSE when not a match, otherwise return token
      test_match: function(match, indexed_rule) {
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
      },
      // return next match in input
      next: function() {
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
      },
      // return next match that has a token
      lex: function lex() {
        var r = this.next();
        if (r) {
          return r;
        } else {
          return this.lex();
        }
      },
      // activates a new lexer condition state (pushes the new lexer condition state onto the condition stack)
      begin: function begin(condition) {
        this.conditionStack.push(condition);
      },
      // pop the previously active lexer condition state off the condition stack
      popState: function popState() {
        var n = this.conditionStack.length - 1;
        if (n > 0) {
          return this.conditionStack.pop();
        } else {
          return this.conditionStack[0];
        }
      },
      // produce the lexer rule set which is active for the currently active lexer condition state
      _currentRules: function _currentRules() {
        if (this.conditionStack.length && this.conditionStack[this.conditionStack.length - 1]) {
          return this.conditions[this.conditionStack[this.conditionStack.length - 1]].rules;
        } else {
          return this.conditions["INITIAL"].rules;
        }
      },
      // return the currently active lexer condition state; when an index argument is provided it produces the N-th previous condition state, if available
      topState: function topState(n) {
        n = this.conditionStack.length - 1 - Math.abs(n || 0);
        if (n >= 0) {
          return this.conditionStack[n];
        } else {
          return "INITIAL";
        }
      },
      // alias for begin(condition)
      pushState: function pushState(condition) {
        this.begin(condition);
      },
      // return the number of states currently on the stack
      stateStackSize: function stateStackSize() {
        return this.conditionStack.length;
      },
      options: { "case-insensitive": true },
      performAction: function anonymous(yy, yy_, $avoiding_name_collisions, YY_START) {
        switch ($avoiding_name_collisions) {
          case 0:
            this.begin("open_directive");
            return 19;
          case 1:
            this.begin("type_directive");
            return 20;
          case 2:
            this.popState();
            this.begin("arg_directive");
            return 12;
          case 3:
            this.popState();
            this.popState();
            return 22;
          case 4:
            return 21;
          case 5:
            return "title";
          case 6:
            this.begin("acc_title");
            return 14;
          case 7:
            this.popState();
            return "acc_title_value";
          case 8:
            this.begin("acc_descr");
            return 16;
          case 9:
            this.popState();
            return "acc_descr_value";
          case 10:
            this.begin("acc_descr_multiline");
            break;
          case 11:
            this.popState();
            break;
          case 12:
            return "acc_descr_multiline_value";
          case 13:
            return 5;
          case 14:
            break;
          case 15:
            break;
          case 16:
            break;
          case 17:
            return 8;
          case 18:
            return 6;
          case 19:
            return 28;
          case 20:
            return 39;
          case 21:
            return 31;
          case 22:
            return 30;
          case 23:
            return 33;
          case 24:
            return 35;
          case 25:
            return 37;
          case 26:
            return 40;
          case 27:
            return 41;
          case 28:
            return 42;
          case 29:
            return 43;
          case 30:
            return 44;
          case 31:
            return 45;
          case 32:
            return 46;
          case 33:
            return 47;
          case 34:
            return 48;
          case 35:
            return 49;
          case 36:
            return 50;
          case 37:
            return 51;
          case 38:
            return 52;
          case 39:
            return 53;
          case 40:
            return 64;
          case 41:
            return 65;
          case 42:
            return 66;
          case 43:
            return 67;
          case 44:
            return 68;
          case 45:
            return 69;
          case 46:
            return 70;
          case 47:
            return 56;
          case 48:
            return 58;
          case 49:
            return 60;
          case 50:
            return 63;
          case 51:
            return 62;
          case 52:
            this.begin("string");
            break;
          case 53:
            this.popState();
            break;
          case 54:
            return "qString";
          case 55:
            yy_.yytext = yy_.yytext.trim();
            return 71;
        }
      },
      rules: [/^(?:%%\{)/i, /^(?:((?:(?!\}%%)[^:.])*))/i, /^(?::)/i, /^(?:\}%%)/i, /^(?:((?:(?!\}%%).|\n)*))/i, /^(?:title\s[^#\n;]+)/i, /^(?:accTitle\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*\{\s*)/i, /^(?:[\}])/i, /^(?:[^\}]*)/i, /^(?:(\r?\n)+)/i, /^(?:\s+)/i, /^(?:#[^\n]*)/i, /^(?:%[^\n]*)/i, /^(?:$)/i, /^(?:requirementDiagram\b)/i, /^(?:\{)/i, /^(?:\})/i, /^(?::)/i, /^(?:id\b)/i, /^(?:text\b)/i, /^(?:risk\b)/i, /^(?:verifyMethod\b)/i, /^(?:requirement\b)/i, /^(?:functionalRequirement\b)/i, /^(?:interfaceRequirement\b)/i, /^(?:performanceRequirement\b)/i, /^(?:physicalRequirement\b)/i, /^(?:designConstraint\b)/i, /^(?:low\b)/i, /^(?:medium\b)/i, /^(?:high\b)/i, /^(?:analysis\b)/i, /^(?:demonstration\b)/i, /^(?:inspection\b)/i, /^(?:test\b)/i, /^(?:element\b)/i, /^(?:contains\b)/i, /^(?:copies\b)/i, /^(?:derives\b)/i, /^(?:satisfies\b)/i, /^(?:verifies\b)/i, /^(?:refines\b)/i, /^(?:traces\b)/i, /^(?:type\b)/i, /^(?:docref\b)/i, /^(?:<-)/i, /^(?:->)/i, /^(?:-)/i, /^(?:["])/i, /^(?:["])/i, /^(?:[^"]*)/i, /^(?:[\w][^\r\n\{\<\>\-\=]*)/i],
      conditions: { "acc_descr_multiline": { "rules": [11, 12], "inclusive": false }, "acc_descr": { "rules": [9], "inclusive": false }, "acc_title": { "rules": [7], "inclusive": false }, "close_directive": { "rules": [], "inclusive": false }, "arg_directive": { "rules": [3, 4], "inclusive": false }, "type_directive": { "rules": [2, 3], "inclusive": false }, "open_directive": { "rules": [1], "inclusive": false }, "unqString": { "rules": [], "inclusive": false }, "token": { "rules": [], "inclusive": false }, "string": { "rules": [53, 54], "inclusive": false }, "INITIAL": { "rules": [0, 5, 6, 8, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 55], "inclusive": true } }
    };
    return lexer2;
  }();
  parser2.lexer = lexer;
  function Parser() {
    this.yy = {};
  }
  Parser.prototype = parser2;
  parser2.Parser = Parser;
  return new Parser();
}();
parser.parser = parser;
const parser$1 = parser;
let relations = [];
let latestRequirement = {};
let requirements = {};
let latestElement = {};
let elements = {};
const RequirementType = {
  REQUIREMENT: "Requirement",
  FUNCTIONAL_REQUIREMENT: "Functional Requirement",
  INTERFACE_REQUIREMENT: "Interface Requirement",
  PERFORMANCE_REQUIREMENT: "Performance Requirement",
  PHYSICAL_REQUIREMENT: "Physical Requirement",
  DESIGN_CONSTRAINT: "Design Constraint"
};
const RiskLevel = {
  LOW_RISK: "Low",
  MED_RISK: "Medium",
  HIGH_RISK: "High"
};
const VerifyType = {
  VERIFY_ANALYSIS: "Analysis",
  VERIFY_DEMONSTRATION: "Demonstration",
  VERIFY_INSPECTION: "Inspection",
  VERIFY_TEST: "Test"
};
const Relationships = {
  CONTAINS: "contains",
  COPIES: "copies",
  DERIVES: "derives",
  SATISFIES: "satisfies",
  VERIFIES: "verifies",
  REFINES: "refines",
  TRACES: "traces"
};
const parseDirective = function(statement, context, type) {
  mermaidAPI.parseDirective(this, statement, context, type);
};
const addRequirement = (name, type) => {
  if (requirements[name] === void 0) {
    requirements[name] = {
      name,
      type,
      id: latestRequirement.id,
      text: latestRequirement.text,
      risk: latestRequirement.risk,
      verifyMethod: latestRequirement.verifyMethod
    };
  }
  latestRequirement = {};
  return requirements[name];
};
const getRequirements = () => requirements;
const setNewReqId = (id) => {
  if (latestRequirement !== void 0) {
    latestRequirement.id = id;
  }
};
const setNewReqText = (text) => {
  if (latestRequirement !== void 0) {
    latestRequirement.text = text;
  }
};
const setNewReqRisk = (risk) => {
  if (latestRequirement !== void 0) {
    latestRequirement.risk = risk;
  }
};
const setNewReqVerifyMethod = (verifyMethod) => {
  if (latestRequirement !== void 0) {
    latestRequirement.verifyMethod = verifyMethod;
  }
};
const addElement = (name) => {
  if (elements[name] === void 0) {
    elements[name] = {
      name,
      type: latestElement.type,
      docRef: latestElement.docRef
    };
    log.info("Added new requirement: ", name);
  }
  latestElement = {};
  return elements[name];
};
const getElements = () => elements;
const setNewElementType = (type) => {
  if (latestElement !== void 0) {
    latestElement.type = type;
  }
};
const setNewElementDocRef = (docRef) => {
  if (latestElement !== void 0) {
    latestElement.docRef = docRef;
  }
};
const addRelationship = (type, src, dst) => {
  relations.push({
    type,
    src,
    dst
  });
};
const getRelationships = () => relations;
const clear = () => {
  relations = [];
  latestRequirement = {};
  requirements = {};
  latestElement = {};
  elements = {};
  clear$1();
};
const db = {
  RequirementType,
  RiskLevel,
  VerifyType,
  Relationships,
  parseDirective,
  getConfig: () => getConfig().req,
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
  clear
};
const getStyles = (options) => `

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
    fill-opacity: 100%;
    stroke: ${options.requirementBorderColor};
    stroke-width: ${options.requirementBorderSize};
  }
  
  .reqTitle, .reqLabel{
    fill:  ${options.requirementTextColor};
  }
  .reqLabelBox {
    fill: ${options.relationLabelBackground};
    fill-opacity: 100%;
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

`;
const styles = getStyles;
const ReqMarkers = {
  CONTAINS: "contains",
  ARROW: "arrow"
};
const insertLineEndings = (parentNode, conf2) => {
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
};
const markers = {
  ReqMarkers,
  insertLineEndings
};
let conf = {};
let relCnt = 0;
const newRectNode = (parentNode, id) => {
  return parentNode.insert("rect", "#" + id).attr("class", "req reqBox").attr("x", 0).attr("y", 0).attr("width", conf.rect_min_width + "px").attr("height", conf.rect_min_height + "px");
};
const newTitleNode = (parentNode, id, txts) => {
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
};
const newBodyNode = (parentNode, id, txts, yStart) => {
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
};
const addEdgeLabel = (parentNode, svgPath, conf2, txt) => {
  const len = svgPath.node().getTotalLength();
  const labelPoint = svgPath.node().getPointAtLength(len * 0.5);
  const labelId = "rel" + relCnt;
  relCnt++;
  const labelNode = parentNode.append("text").attr("class", "req relationshipLabel").attr("id", labelId).attr("x", labelPoint.x).attr("y", labelPoint.y).attr("text-anchor", "middle").attr("dominant-baseline", "middle").text(txt);
  const labelBBox = labelNode.node().getBBox();
  parentNode.insert("rect", "#" + labelId).attr("class", "req reqLabelBox").attr("x", labelPoint.x - labelBBox.width / 2).attr("y", labelPoint.y - labelBBox.height / 2).attr("width", labelBBox.width).attr("height", labelBBox.height).attr("fill", "white").attr("fill-opacity", "85%");
};
const drawRelationshipFromLayout = function(svg, rel, g, insert, diagObj) {
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
      "url(" + common.getUrl(conf.arrowMarkerAbsolute) + "#" + rel.type + "_line_ending)"
    );
  } else {
    svgPath.attr("stroke-dasharray", "10,7");
    svgPath.attr(
      "marker-end",
      "url(" + common.getUrl(conf.arrowMarkerAbsolute) + "#" + markers.ReqMarkers.ARROW + "_line_ending)"
    );
  }
  addEdgeLabel(svg, svgPath, conf, `<<${rel.type}>>`);
  return;
};
const drawReqs = (reqs, graph, svgNode) => {
  Object.keys(reqs).forEach((reqName) => {
    let req = reqs[reqName];
    reqName = elementString(reqName);
    log.info("Added new requirement: ", reqName);
    const groupNode = svgNode.append("g").attr("id", reqName);
    const textId = "req-" + reqName;
    const rectNode = newRectNode(groupNode, textId);
    let titleNodeInfo = newTitleNode(groupNode, reqName + "_title", [
      `<<${req.type}>>`,
      `${req.name}`
    ]);
    newBodyNode(
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
    const rectBBox = rectNode.node().getBBox();
    graph.setNode(reqName, {
      width: rectBBox.width,
      height: rectBBox.height,
      shape: "rect",
      id: reqName
    });
  });
};
const drawElements = (els, graph, svgNode) => {
  Object.keys(els).forEach((elName) => {
    let el = els[elName];
    const id = elementString(elName);
    const groupNode = svgNode.append("g").attr("id", id);
    const textId = "element-" + id;
    const rectNode = newRectNode(groupNode, textId);
    let titleNodeInfo = newTitleNode(groupNode, textId + "_title", [`<<Element>>`, `${elName}`]);
    newBodyNode(
      groupNode,
      textId + "_body",
      [`Type: ${el.type || "Not Specified"}`, `Doc Ref: ${el.docRef || "None"}`],
      titleNodeInfo.y
    );
    const rectBBox = rectNode.node().getBBox();
    graph.setNode(id, {
      width: rectBBox.width,
      height: rectBBox.height,
      shape: "rect",
      id
    });
  });
};
const addRelationships = (relationships, g) => {
  relationships.forEach(function(r) {
    let src = elementString(r.src);
    let dst = elementString(r.dst);
    g.setEdge(src, dst, { relationship: r });
  });
  return relationships;
};
const adjustEntities = function(svgNode, graph) {
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
};
const elementString = (str) => {
  return str.replace(/\s/g, "").replace(/\./g, "_");
};
const draw = (text, id, _version, diagObj) => {
  conf = getConfig().requirement;
  diagObj.db.clear();
  diagObj.parser.parse(text);
  const securityLevel = conf.securityLevel;
  let sandboxElement;
  if (securityLevel === "sandbox") {
    sandboxElement = select("#i" + id);
  }
  const root = securityLevel === "sandbox" ? select(sandboxElement.nodes()[0].contentDocument.body) : select("body");
  const svg = root.select(`[id='${id}']`);
  markers.insertLineEndings(svg, conf);
  const g = new Graph({
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
  layout(g);
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
};
const renderer = {
  draw
};
const diagram = {
  parser: parser$1,
  db,
  renderer,
  styles
};
export {
  diagram
};
//# sourceMappingURL=requirementDiagram-339ed3c3.js.map
