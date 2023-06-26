import { g as A, l as G, e as V, f as Ae } from "./config-e567ef17.js";
import { F as Oe, G as pe, u as Se, H as Ie } from "./utils-aa888deb.js";
import { m as Ge } from "./mermaidAPI-04b5c286.js";
import { s as Pe, g as He, a as Ne, b as De, d as Ve, e as ze, f as je } from "./commonDb-4dc3d465.js";
import "./setupGraphViewbox-a4603a92.js";
import "./errorRenderer-a3c4bedb.js";
var me = function() {
  var r = function(B, l, u, b) {
    for (u = u || {}, b = B.length; b--; u[B[b]] = l)
      ;
    return u;
  }, n = [1, 4], o = [1, 7], h = [1, 5], a = [1, 9], c = [1, 6], f = [2, 6], p = [1, 16], w = [6, 8, 14, 20, 22, 24, 25, 27, 29, 32, 37, 40, 50, 55], y = [8, 14, 20, 22, 24, 25, 27, 29, 32, 37, 40], m = [8, 13, 14, 20, 22, 24, 25, 27, 29, 32, 37, 40], d = [1, 26], _ = [6, 8, 14, 50, 55], s = [8, 14, 55], C = [1, 53], v = [1, 52], N = [8, 14, 30, 33, 35, 38, 55], x = [1, 67], g = [1, 68], k = [1, 69], P = [8, 14, 33, 35, 42, 55], ne = {
    trace: function() {
    },
    yy: {},
    symbols_: { error: 2, start: 3, eol: 4, directive: 5, GG: 6, document: 7, EOF: 8, ":": 9, DIR: 10, options: 11, body: 12, OPT: 13, NL: 14, line: 15, statement: 16, commitStatement: 17, mergeStatement: 18, cherryPickStatement: 19, acc_title: 20, acc_title_value: 21, acc_descr: 22, acc_descr_value: 23, acc_descr_multiline_value: 24, section: 25, branchStatement: 26, CHECKOUT: 27, ref: 28, BRANCH: 29, ORDER: 30, NUM: 31, CHERRY_PICK: 32, COMMIT_ID: 33, STR: 34, COMMIT_TAG: 35, EMPTYSTR: 36, MERGE: 37, COMMIT_TYPE: 38, commitType: 39, COMMIT: 40, commit_arg: 41, COMMIT_MSG: 42, NORMAL: 43, REVERSE: 44, HIGHLIGHT: 45, openDirective: 46, typeDirective: 47, closeDirective: 48, argDirective: 49, open_directive: 50, type_directive: 51, arg_directive: 52, close_directive: 53, ID: 54, ";": 55, $accept: 0, $end: 1 },
    terminals_: { 2: "error", 6: "GG", 8: "EOF", 9: ":", 10: "DIR", 13: "OPT", 14: "NL", 20: "acc_title", 21: "acc_title_value", 22: "acc_descr", 23: "acc_descr_value", 24: "acc_descr_multiline_value", 25: "section", 27: "CHECKOUT", 29: "BRANCH", 30: "ORDER", 31: "NUM", 32: "CHERRY_PICK", 33: "COMMIT_ID", 34: "STR", 35: "COMMIT_TAG", 36: "EMPTYSTR", 37: "MERGE", 38: "COMMIT_TYPE", 40: "COMMIT", 42: "COMMIT_MSG", 43: "NORMAL", 44: "REVERSE", 45: "HIGHLIGHT", 50: "open_directive", 51: "type_directive", 52: "arg_directive", 53: "close_directive", 54: "ID", 55: ";" },
    productions_: [0, [3, 2], [3, 2], [3, 3], [3, 4], [3, 5], [7, 0], [7, 2], [11, 2], [11, 1], [12, 0], [12, 2], [15, 2], [15, 1], [16, 1], [16, 1], [16, 1], [16, 2], [16, 2], [16, 1], [16, 1], [16, 1], [16, 2], [26, 2], [26, 4], [19, 3], [19, 5], [19, 5], [19, 5], [19, 5], [18, 2], [18, 4], [18, 4], [18, 4], [18, 6], [18, 6], [18, 6], [18, 6], [18, 6], [18, 6], [18, 8], [18, 8], [18, 8], [18, 8], [18, 8], [18, 8], [17, 2], [17, 3], [17, 3], [17, 5], [17, 5], [17, 3], [17, 5], [17, 5], [17, 5], [17, 5], [17, 7], [17, 7], [17, 7], [17, 7], [17, 7], [17, 7], [17, 3], [17, 5], [17, 5], [17, 5], [17, 5], [17, 5], [17, 5], [17, 7], [17, 7], [17, 7], [17, 7], [17, 7], [17, 7], [17, 7], [17, 7], [17, 7], [17, 7], [17, 7], [17, 7], [17, 7], [17, 7], [17, 7], [17, 7], [17, 7], [17, 7], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [17, 9], [41, 0], [41, 1], [39, 1], [39, 1], [39, 1], [5, 3], [5, 5], [46, 1], [47, 1], [49, 1], [48, 1], [28, 1], [28, 1], [4, 1], [4, 1], [4, 1]],
    performAction: function(l, u, b, i, E, e, W) {
      var t = e.length - 1;
      switch (E) {
        case 3:
          return e[t];
        case 4:
          return e[t - 1];
        case 5:
          return i.setDirection(e[t - 3]), e[t - 1];
        case 7:
          i.setOptions(e[t - 1]), this.$ = e[t];
          break;
        case 8:
          e[t - 1] += e[t], this.$ = e[t - 1];
          break;
        case 10:
          this.$ = [];
          break;
        case 11:
          e[t - 1].push(e[t]), this.$ = e[t - 1];
          break;
        case 12:
          this.$ = e[t - 1];
          break;
        case 17:
          this.$ = e[t].trim(), i.setAccTitle(this.$);
          break;
        case 18:
        case 19:
          this.$ = e[t].trim(), i.setAccDescription(this.$);
          break;
        case 20:
          i.addSection(e[t].substr(8)), this.$ = e[t].substr(8);
          break;
        case 22:
          i.checkout(e[t]);
          break;
        case 23:
          i.branch(e[t]);
          break;
        case 24:
          i.branch(e[t - 2], e[t]);
          break;
        case 25:
          i.cherryPick(e[t], "", void 0);
          break;
        case 26:
          i.cherryPick(e[t - 2], "", e[t]);
          break;
        case 27:
        case 29:
          i.cherryPick(e[t - 2], "", "");
          break;
        case 28:
          i.cherryPick(e[t], "", e[t - 2]);
          break;
        case 30:
          i.merge(e[t], "", "", "");
          break;
        case 31:
          i.merge(e[t - 2], e[t], "", "");
          break;
        case 32:
          i.merge(e[t - 2], "", e[t], "");
          break;
        case 33:
          i.merge(e[t - 2], "", "", e[t]);
          break;
        case 34:
          i.merge(e[t - 4], e[t], "", e[t - 2]);
          break;
        case 35:
          i.merge(e[t - 4], "", e[t], e[t - 2]);
          break;
        case 36:
          i.merge(e[t - 4], "", e[t - 2], e[t]);
          break;
        case 37:
          i.merge(e[t - 4], e[t - 2], e[t], "");
          break;
        case 38:
          i.merge(e[t - 4], e[t - 2], "", e[t]);
          break;
        case 39:
          i.merge(e[t - 4], e[t], e[t - 2], "");
          break;
        case 40:
          i.merge(e[t - 6], e[t - 4], e[t - 2], e[t]);
          break;
        case 41:
          i.merge(e[t - 6], e[t], e[t - 4], e[t - 2]);
          break;
        case 42:
          i.merge(e[t - 6], e[t - 4], e[t], e[t - 2]);
          break;
        case 43:
          i.merge(e[t - 6], e[t - 2], e[t - 4], e[t]);
          break;
        case 44:
          i.merge(e[t - 6], e[t], e[t - 2], e[t - 4]);
          break;
        case 45:
          i.merge(e[t - 6], e[t - 2], e[t], e[t - 4]);
          break;
        case 46:
          i.commit(e[t]);
          break;
        case 47:
          i.commit("", "", i.commitType.NORMAL, e[t]);
          break;
        case 48:
          i.commit("", "", e[t], "");
          break;
        case 49:
          i.commit("", "", e[t], e[t - 2]);
          break;
        case 50:
          i.commit("", "", e[t - 2], e[t]);
          break;
        case 51:
          i.commit("", e[t], i.commitType.NORMAL, "");
          break;
        case 52:
          i.commit("", e[t - 2], i.commitType.NORMAL, e[t]);
          break;
        case 53:
          i.commit("", e[t], i.commitType.NORMAL, e[t - 2]);
          break;
        case 54:
          i.commit("", e[t - 2], e[t], "");
          break;
        case 55:
          i.commit("", e[t], e[t - 2], "");
          break;
        case 56:
          i.commit("", e[t - 4], e[t - 2], e[t]);
          break;
        case 57:
          i.commit("", e[t - 4], e[t], e[t - 2]);
          break;
        case 58:
          i.commit("", e[t - 2], e[t - 4], e[t]);
          break;
        case 59:
          i.commit("", e[t], e[t - 4], e[t - 2]);
          break;
        case 60:
          i.commit("", e[t], e[t - 2], e[t - 4]);
          break;
        case 61:
          i.commit("", e[t - 2], e[t], e[t - 4]);
          break;
        case 62:
          i.commit(e[t], "", i.commitType.NORMAL, "");
          break;
        case 63:
          i.commit(e[t], "", i.commitType.NORMAL, e[t - 2]);
          break;
        case 64:
          i.commit(e[t - 2], "", i.commitType.NORMAL, e[t]);
          break;
        case 65:
          i.commit(e[t - 2], "", e[t], "");
          break;
        case 66:
          i.commit(e[t], "", e[t - 2], "");
          break;
        case 67:
          i.commit(e[t], e[t - 2], i.commitType.NORMAL, "");
          break;
        case 68:
          i.commit(e[t - 2], e[t], i.commitType.NORMAL, "");
          break;
        case 69:
          i.commit(e[t - 4], "", e[t - 2], e[t]);
          break;
        case 70:
          i.commit(e[t - 4], "", e[t], e[t - 2]);
          break;
        case 71:
          i.commit(e[t - 2], "", e[t - 4], e[t]);
          break;
        case 72:
          i.commit(e[t], "", e[t - 4], e[t - 2]);
          break;
        case 73:
          i.commit(e[t], "", e[t - 2], e[t - 4]);
          break;
        case 74:
          i.commit(e[t - 2], "", e[t], e[t - 4]);
          break;
        case 75:
          i.commit(e[t - 4], e[t], e[t - 2], "");
          break;
        case 76:
          i.commit(e[t - 4], e[t - 2], e[t], "");
          break;
        case 77:
          i.commit(e[t - 2], e[t], e[t - 4], "");
          break;
        case 78:
          i.commit(e[t], e[t - 2], e[t - 4], "");
          break;
        case 79:
          i.commit(e[t], e[t - 4], e[t - 2], "");
          break;
        case 80:
          i.commit(e[t - 2], e[t - 4], e[t], "");
          break;
        case 81:
          i.commit(e[t - 4], e[t], i.commitType.NORMAL, e[t - 2]);
          break;
        case 82:
          i.commit(e[t - 4], e[t - 2], i.commitType.NORMAL, e[t]);
          break;
        case 83:
          i.commit(e[t - 2], e[t], i.commitType.NORMAL, e[t - 4]);
          break;
        case 84:
          i.commit(e[t], e[t - 2], i.commitType.NORMAL, e[t - 4]);
          break;
        case 85:
          i.commit(e[t], e[t - 4], i.commitType.NORMAL, e[t - 2]);
          break;
        case 86:
          i.commit(e[t - 2], e[t - 4], i.commitType.NORMAL, e[t]);
          break;
        case 87:
          i.commit(e[t - 6], e[t - 4], e[t - 2], e[t]);
          break;
        case 88:
          i.commit(e[t - 6], e[t - 4], e[t], e[t - 2]);
          break;
        case 89:
          i.commit(e[t - 6], e[t - 2], e[t - 4], e[t]);
          break;
        case 90:
          i.commit(e[t - 6], e[t], e[t - 4], e[t - 2]);
          break;
        case 91:
          i.commit(e[t - 6], e[t - 2], e[t], e[t - 4]);
          break;
        case 92:
          i.commit(e[t - 6], e[t], e[t - 2], e[t - 4]);
          break;
        case 93:
          i.commit(e[t - 4], e[t - 6], e[t - 2], e[t]);
          break;
        case 94:
          i.commit(e[t - 4], e[t - 6], e[t], e[t - 2]);
          break;
        case 95:
          i.commit(e[t - 2], e[t - 6], e[t - 4], e[t]);
          break;
        case 96:
          i.commit(e[t], e[t - 6], e[t - 4], e[t - 2]);
          break;
        case 97:
          i.commit(e[t - 2], e[t - 6], e[t], e[t - 4]);
          break;
        case 98:
          i.commit(e[t], e[t - 6], e[t - 2], e[t - 4]);
          break;
        case 99:
          i.commit(e[t], e[t - 4], e[t - 2], e[t - 6]);
          break;
        case 100:
          i.commit(e[t - 2], e[t - 4], e[t], e[t - 6]);
          break;
        case 101:
          i.commit(e[t], e[t - 2], e[t - 4], e[t - 6]);
          break;
        case 102:
          i.commit(e[t - 2], e[t], e[t - 4], e[t - 6]);
          break;
        case 103:
          i.commit(e[t - 4], e[t - 2], e[t], e[t - 6]);
          break;
        case 104:
          i.commit(e[t - 4], e[t], e[t - 2], e[t - 6]);
          break;
        case 105:
          i.commit(e[t - 2], e[t - 4], e[t - 6], e[t]);
          break;
        case 106:
          i.commit(e[t], e[t - 4], e[t - 6], e[t - 2]);
          break;
        case 107:
          i.commit(e[t - 2], e[t], e[t - 6], e[t - 4]);
          break;
        case 108:
          i.commit(e[t], e[t - 2], e[t - 6], e[t - 4]);
          break;
        case 109:
          i.commit(e[t - 4], e[t - 2], e[t - 6], e[t]);
          break;
        case 110:
          i.commit(e[t - 4], e[t], e[t - 6], e[t - 2]);
          break;
        case 111:
          this.$ = "";
          break;
        case 112:
          this.$ = e[t];
          break;
        case 113:
          this.$ = i.commitType.NORMAL;
          break;
        case 114:
          this.$ = i.commitType.REVERSE;
          break;
        case 115:
          this.$ = i.commitType.HIGHLIGHT;
          break;
        case 118:
          i.parseDirective("%%{", "open_directive");
          break;
        case 119:
          i.parseDirective(e[t], "type_directive");
          break;
        case 120:
          e[t] = e[t].trim().replace(/'/g, '"'), i.parseDirective(e[t], "arg_directive");
          break;
        case 121:
          i.parseDirective("}%%", "close_directive", "gitGraph");
          break;
      }
    },
    table: [{ 3: 1, 4: 2, 5: 3, 6: n, 8: o, 14: h, 46: 8, 50: a, 55: c }, { 1: [3] }, { 3: 10, 4: 2, 5: 3, 6: n, 8: o, 14: h, 46: 8, 50: a, 55: c }, { 3: 11, 4: 2, 5: 3, 6: n, 8: o, 14: h, 46: 8, 50: a, 55: c }, { 7: 12, 8: f, 9: [1, 13], 10: [1, 14], 11: 15, 14: p }, r(w, [2, 124]), r(w, [2, 125]), r(w, [2, 126]), { 47: 17, 51: [1, 18] }, { 51: [2, 118] }, { 1: [2, 1] }, { 1: [2, 2] }, { 8: [1, 19] }, { 7: 20, 8: f, 11: 15, 14: p }, { 9: [1, 21] }, r(y, [2, 10], { 12: 22, 13: [1, 23] }), r(m, [2, 9]), { 9: [1, 25], 48: 24, 53: d }, r([9, 53], [2, 119]), { 1: [2, 3] }, { 8: [1, 27] }, { 7: 28, 8: f, 11: 15, 14: p }, { 8: [2, 7], 14: [1, 31], 15: 29, 16: 30, 17: 32, 18: 33, 19: 34, 20: [1, 35], 22: [1, 36], 24: [1, 37], 25: [1, 38], 26: 39, 27: [1, 40], 29: [1, 44], 32: [1, 43], 37: [1, 42], 40: [1, 41] }, r(m, [2, 8]), r(_, [2, 116]), { 49: 45, 52: [1, 46] }, r(_, [2, 121]), { 1: [2, 4] }, { 8: [1, 47] }, r(y, [2, 11]), { 4: 48, 8: o, 14: h, 55: c }, r(y, [2, 13]), r(s, [2, 14]), r(s, [2, 15]), r(s, [2, 16]), { 21: [1, 49] }, { 23: [1, 50] }, r(s, [2, 19]), r(s, [2, 20]), r(s, [2, 21]), { 28: 51, 34: C, 54: v }, r(s, [2, 111], { 41: 54, 33: [1, 57], 34: [1, 59], 35: [1, 55], 38: [1, 56], 42: [1, 58] }), { 28: 60, 34: C, 54: v }, { 33: [1, 61], 35: [1, 62] }, { 28: 63, 34: C, 54: v }, { 48: 64, 53: d }, { 53: [2, 120] }, { 1: [2, 5] }, r(y, [2, 12]), r(s, [2, 17]), r(s, [2, 18]), r(s, [2, 22]), r(N, [2, 122]), r(N, [2, 123]), r(s, [2, 46]), { 34: [1, 65] }, { 39: 66, 43: x, 44: g, 45: k }, { 34: [1, 70] }, { 34: [1, 71] }, r(s, [2, 112]), r(s, [2, 30], { 33: [1, 72], 35: [1, 74], 38: [1, 73] }), { 34: [1, 75] }, { 34: [1, 76], 36: [1, 77] }, r(s, [2, 23], { 30: [1, 78] }), r(_, [2, 117]), r(s, [2, 47], { 33: [1, 80], 38: [1, 79], 42: [1, 81] }), r(s, [2, 48], { 33: [1, 83], 35: [1, 82], 42: [1, 84] }), r(P, [2, 113]), r(P, [2, 114]), r(P, [2, 115]), r(s, [2, 51], { 35: [1, 85], 38: [1, 86], 42: [1, 87] }), r(s, [2, 62], { 33: [1, 90], 35: [1, 88], 38: [1, 89] }), { 34: [1, 91] }, { 39: 92, 43: x, 44: g, 45: k }, { 34: [1, 93] }, r(s, [2, 25], { 35: [1, 94] }), { 33: [1, 95] }, { 33: [1, 96] }, { 31: [1, 97] }, { 39: 98, 43: x, 44: g, 45: k }, { 34: [1, 99] }, { 34: [1, 100] }, { 34: [1, 101] }, { 34: [1, 102] }, { 34: [1, 103] }, { 34: [1, 104] }, { 39: 105, 43: x, 44: g, 45: k }, { 34: [1, 106] }, { 34: [1, 107] }, { 39: 108, 43: x, 44: g, 45: k }, { 34: [1, 109] }, r(s, [2, 31], { 35: [1, 111], 38: [1, 110] }), r(s, [2, 32], { 33: [1, 113], 35: [1, 112] }), r(s, [2, 33], { 33: [1, 114], 38: [1, 115] }), { 34: [1, 116], 36: [1, 117] }, { 34: [1, 118] }, { 34: [1, 119] }, r(s, [2, 24]), r(s, [2, 49], { 33: [1, 120], 42: [1, 121] }), r(s, [2, 53], { 38: [1, 122], 42: [1, 123] }), r(s, [2, 63], { 33: [1, 125], 38: [1, 124] }), r(s, [2, 50], { 33: [1, 126], 42: [1, 127] }), r(s, [2, 55], { 35: [1, 128], 42: [1, 129] }), r(s, [2, 66], { 33: [1, 131], 35: [1, 130] }), r(s, [2, 52], { 38: [1, 132], 42: [1, 133] }), r(s, [2, 54], { 35: [1, 134], 42: [1, 135] }), r(s, [2, 67], { 35: [1, 137], 38: [1, 136] }), r(s, [2, 64], { 33: [1, 139], 38: [1, 138] }), r(s, [2, 65], { 33: [1, 141], 35: [1, 140] }), r(s, [2, 68], { 35: [1, 143], 38: [1, 142] }), { 39: 144, 43: x, 44: g, 45: k }, { 34: [1, 145] }, { 34: [1, 146] }, { 34: [1, 147] }, { 34: [1, 148] }, { 39: 149, 43: x, 44: g, 45: k }, r(s, [2, 26]), r(s, [2, 27]), r(s, [2, 28]), r(s, [2, 29]), { 34: [1, 150] }, { 34: [1, 151] }, { 39: 152, 43: x, 44: g, 45: k }, { 34: [1, 153] }, { 39: 154, 43: x, 44: g, 45: k }, { 34: [1, 155] }, { 34: [1, 156] }, { 34: [1, 157] }, { 34: [1, 158] }, { 34: [1, 159] }, { 34: [1, 160] }, { 34: [1, 161] }, { 39: 162, 43: x, 44: g, 45: k }, { 34: [1, 163] }, { 34: [1, 164] }, { 34: [1, 165] }, { 39: 166, 43: x, 44: g, 45: k }, { 34: [1, 167] }, { 39: 168, 43: x, 44: g, 45: k }, { 34: [1, 169] }, { 34: [1, 170] }, { 34: [1, 171] }, { 39: 172, 43: x, 44: g, 45: k }, { 34: [1, 173] }, r(s, [2, 37], { 35: [1, 174] }), r(s, [2, 38], { 38: [1, 175] }), r(s, [2, 36], { 33: [1, 176] }), r(s, [2, 39], { 35: [1, 177] }), r(s, [2, 34], { 38: [1, 178] }), r(s, [2, 35], { 33: [1, 179] }), r(s, [2, 60], { 42: [1, 180] }), r(s, [2, 73], { 33: [1, 181] }), r(s, [2, 61], { 42: [1, 182] }), r(s, [2, 84], { 38: [1, 183] }), r(s, [2, 74], { 33: [1, 184] }), r(s, [2, 83], { 38: [1, 185] }), r(s, [2, 59], { 42: [1, 186] }), r(s, [2, 72], { 33: [1, 187] }), r(s, [2, 58], { 42: [1, 188] }), r(s, [2, 78], { 35: [1, 189] }), r(s, [2, 71], { 33: [1, 190] }), r(s, [2, 77], { 35: [1, 191] }), r(s, [2, 57], { 42: [1, 192] }), r(s, [2, 85], { 38: [1, 193] }), r(s, [2, 56], { 42: [1, 194] }), r(s, [2, 79], { 35: [1, 195] }), r(s, [2, 80], { 35: [1, 196] }), r(s, [2, 86], { 38: [1, 197] }), r(s, [2, 70], { 33: [1, 198] }), r(s, [2, 81], { 38: [1, 199] }), r(s, [2, 69], { 33: [1, 200] }), r(s, [2, 75], { 35: [1, 201] }), r(s, [2, 76], { 35: [1, 202] }), r(s, [2, 82], { 38: [1, 203] }), { 34: [1, 204] }, { 39: 205, 43: x, 44: g, 45: k }, { 34: [1, 206] }, { 34: [1, 207] }, { 39: 208, 43: x, 44: g, 45: k }, { 34: [1, 209] }, { 34: [1, 210] }, { 34: [1, 211] }, { 34: [1, 212] }, { 39: 213, 43: x, 44: g, 45: k }, { 34: [1, 214] }, { 39: 215, 43: x, 44: g, 45: k }, { 34: [1, 216] }, { 34: [1, 217] }, { 34: [1, 218] }, { 34: [1, 219] }, { 34: [1, 220] }, { 34: [1, 221] }, { 34: [1, 222] }, { 39: 223, 43: x, 44: g, 45: k }, { 34: [1, 224] }, { 34: [1, 225] }, { 34: [1, 226] }, { 39: 227, 43: x, 44: g, 45: k }, { 34: [1, 228] }, { 39: 229, 43: x, 44: g, 45: k }, { 34: [1, 230] }, { 34: [1, 231] }, { 34: [1, 232] }, { 39: 233, 43: x, 44: g, 45: k }, r(s, [2, 40]), r(s, [2, 42]), r(s, [2, 41]), r(s, [2, 43]), r(s, [2, 45]), r(s, [2, 44]), r(s, [2, 101]), r(s, [2, 102]), r(s, [2, 99]), r(s, [2, 100]), r(s, [2, 104]), r(s, [2, 103]), r(s, [2, 108]), r(s, [2, 107]), r(s, [2, 106]), r(s, [2, 105]), r(s, [2, 110]), r(s, [2, 109]), r(s, [2, 98]), r(s, [2, 97]), r(s, [2, 96]), r(s, [2, 95]), r(s, [2, 93]), r(s, [2, 94]), r(s, [2, 92]), r(s, [2, 91]), r(s, [2, 90]), r(s, [2, 89]), r(s, [2, 87]), r(s, [2, 88])],
    defaultActions: { 9: [2, 118], 10: [2, 1], 11: [2, 2], 19: [2, 3], 27: [2, 4], 46: [2, 120], 47: [2, 5] },
    parseError: function(l, u) {
      if (u.recoverable)
        this.trace(l);
      else {
        var b = new Error(l);
        throw b.hash = u, b;
      }
    },
    parse: function(l) {
      var u = this, b = [0], i = [], E = [null], e = [], W = this.table, t = "", Z = 0, be = 0, Re = 2, ge = 1, Ce = e.slice.call(arguments, 1), L = Object.create(this.lexer), q = { yy: {} };
      for (var ce in this.yy)
        Object.prototype.hasOwnProperty.call(this.yy, ce) && (q.yy[ce] = this.yy[ce]);
      L.setInput(l, q.yy), q.yy.lexer = L, q.yy.parser = this, typeof L.yylloc > "u" && (L.yylloc = {});
      var oe = L.yylloc;
      e.push(oe);
      var Le = L.options && L.options.ranges;
      typeof q.yy.parseError == "function" ? this.parseError = q.yy.parseError : this.parseError = Object.getPrototypeOf(this).parseError;
      function Me() {
        var j;
        return j = i.pop() || L.lex() || ge, typeof j != "number" && (j instanceof Array && (i = j, j = i.pop()), j = u.symbols_[j] || j), j;
      }
      for (var S, Y, D, le, U = {}, $, z, de, ee; ; ) {
        if (Y = b[b.length - 1], this.defaultActions[Y] ? D = this.defaultActions[Y] : ((S === null || typeof S > "u") && (S = Me()), D = W[Y] && W[Y][S]), typeof D > "u" || !D.length || !D[0]) {
          var he = "";
          ee = [];
          for ($ in W[Y])
            this.terminals_[$] && $ > Re && ee.push("'" + this.terminals_[$] + "'");
          L.showPosition ? he = "Parse error on line " + (Z + 1) + `:
` + L.showPosition() + `
Expecting ` + ee.join(", ") + ", got '" + (this.terminals_[S] || S) + "'" : he = "Parse error on line " + (Z + 1) + ": Unexpected " + (S == ge ? "end of input" : "'" + (this.terminals_[S] || S) + "'"), this.parseError(he, {
            text: L.match,
            token: this.terminals_[S] || S,
            line: L.yylineno,
            loc: oe,
            expected: ee
          });
        }
        if (D[0] instanceof Array && D.length > 1)
          throw new Error("Parse Error: multiple actions possible at state: " + Y + ", token: " + S);
        switch (D[0]) {
          case 1:
            b.push(S), E.push(L.yytext), e.push(L.yylloc), b.push(D[1]), S = null, be = L.yyleng, t = L.yytext, Z = L.yylineno, oe = L.yylloc;
            break;
          case 2:
            if (z = this.productions_[D[1]][1], U.$ = E[E.length - z], U._$ = {
              first_line: e[e.length - (z || 1)].first_line,
              last_line: e[e.length - 1].last_line,
              first_column: e[e.length - (z || 1)].first_column,
              last_column: e[e.length - 1].last_column
            }, Le && (U._$.range = [
              e[e.length - (z || 1)].range[0],
              e[e.length - 1].range[1]
            ]), le = this.performAction.apply(U, [
              t,
              be,
              Z,
              q.yy,
              D[1],
              E,
              e
            ].concat(Ce)), typeof le < "u")
              return le;
            z && (b = b.slice(0, -1 * z * 2), E = E.slice(0, -1 * z), e = e.slice(0, -1 * z)), b.push(this.productions_[D[1]][0]), E.push(U.$), e.push(U._$), de = W[b[b.length - 2]][b[b.length - 1]], b.push(de);
            break;
          case 3:
            return !0;
        }
      }
      return !0;
    }
  }, Te = function() {
    var B = {
      EOF: 1,
      parseError: function(u, b) {
        if (this.yy.parser)
          this.yy.parser.parseError(u, b);
        else
          throw new Error(u);
      },
      // resets the lexer, sets new input
      setInput: function(l, u) {
        return this.yy = u || this.yy || {}, this._input = l, this._more = this._backtrack = this.done = !1, this.yylineno = this.yyleng = 0, this.yytext = this.matched = this.match = "", this.conditionStack = ["INITIAL"], this.yylloc = {
          first_line: 1,
          first_column: 0,
          last_line: 1,
          last_column: 0
        }, this.options.ranges && (this.yylloc.range = [0, 0]), this.offset = 0, this;
      },
      // consumes and returns one char from the input
      input: function() {
        var l = this._input[0];
        this.yytext += l, this.yyleng++, this.offset++, this.match += l, this.matched += l;
        var u = l.match(/(?:\r\n?|\n).*/g);
        return u ? (this.yylineno++, this.yylloc.last_line++) : this.yylloc.last_column++, this.options.ranges && this.yylloc.range[1]++, this._input = this._input.slice(1), l;
      },
      // unshifts one char (or a string) into the input
      unput: function(l) {
        var u = l.length, b = l.split(/(?:\r\n?|\n)/g);
        this._input = l + this._input, this.yytext = this.yytext.substr(0, this.yytext.length - u), this.offset -= u;
        var i = this.match.split(/(?:\r\n?|\n)/g);
        this.match = this.match.substr(0, this.match.length - 1), this.matched = this.matched.substr(0, this.matched.length - 1), b.length - 1 && (this.yylineno -= b.length - 1);
        var E = this.yylloc.range;
        return this.yylloc = {
          first_line: this.yylloc.first_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.first_column,
          last_column: b ? (b.length === i.length ? this.yylloc.first_column : 0) + i[i.length - b.length].length - b[0].length : this.yylloc.first_column - u
        }, this.options.ranges && (this.yylloc.range = [E[0], E[0] + this.yyleng - u]), this.yyleng = this.yytext.length, this;
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
      less: function(l) {
        this.unput(this.match.slice(l));
      },
      // displays already matched input, i.e. for error messages
      pastInput: function() {
        var l = this.matched.substr(0, this.matched.length - this.match.length);
        return (l.length > 20 ? "..." : "") + l.substr(-20).replace(/\n/g, "");
      },
      // displays upcoming input, i.e. for error messages
      upcomingInput: function() {
        var l = this.match;
        return l.length < 20 && (l += this._input.substr(0, 20 - l.length)), (l.substr(0, 20) + (l.length > 20 ? "..." : "")).replace(/\n/g, "");
      },
      // displays the character position where the lexing error occurred, i.e. for error messages
      showPosition: function() {
        var l = this.pastInput(), u = new Array(l.length + 1).join("-");
        return l + this.upcomingInput() + `
` + u + "^";
      },
      // test the lexed token: return FALSE when not a match, otherwise return token
      test_match: function(l, u) {
        var b, i, E;
        if (this.options.backtrack_lexer && (E = {
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
        }, this.options.ranges && (E.yylloc.range = this.yylloc.range.slice(0))), i = l[0].match(/(?:\r\n?|\n).*/g), i && (this.yylineno += i.length), this.yylloc = {
          first_line: this.yylloc.last_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.last_column,
          last_column: i ? i[i.length - 1].length - i[i.length - 1].match(/\r?\n?/)[0].length : this.yylloc.last_column + l[0].length
        }, this.yytext += l[0], this.match += l[0], this.matches = l, this.yyleng = this.yytext.length, this.options.ranges && (this.yylloc.range = [this.offset, this.offset += this.yyleng]), this._more = !1, this._backtrack = !1, this._input = this._input.slice(l[0].length), this.matched += l[0], b = this.performAction.call(this, this.yy, this, u, this.conditionStack[this.conditionStack.length - 1]), this.done && this._input && (this.done = !1), b)
          return b;
        if (this._backtrack) {
          for (var e in E)
            this[e] = E[e];
          return !1;
        }
        return !1;
      },
      // return next match in input
      next: function() {
        if (this.done)
          return this.EOF;
        this._input || (this.done = !0);
        var l, u, b, i;
        this._more || (this.yytext = "", this.match = "");
        for (var E = this._currentRules(), e = 0; e < E.length; e++)
          if (b = this._input.match(this.rules[E[e]]), b && (!u || b[0].length > u[0].length)) {
            if (u = b, i = e, this.options.backtrack_lexer) {
              if (l = this.test_match(b, E[e]), l !== !1)
                return l;
              if (this._backtrack) {
                u = !1;
                continue;
              } else
                return !1;
            } else if (!this.options.flex)
              break;
          }
        return u ? (l = this.test_match(u, E[i]), l !== !1 ? l : !1) : this._input === "" ? this.EOF : this.parseError("Lexical error on line " + (this.yylineno + 1) + `. Unrecognized text.
` + this.showPosition(), {
          text: "",
          token: null,
          line: this.yylineno
        });
      },
      // return next match that has a token
      lex: function() {
        var u = this.next();
        return u || this.lex();
      },
      // activates a new lexer condition state (pushes the new lexer condition state onto the condition stack)
      begin: function(u) {
        this.conditionStack.push(u);
      },
      // pop the previously active lexer condition state off the condition stack
      popState: function() {
        var u = this.conditionStack.length - 1;
        return u > 0 ? this.conditionStack.pop() : this.conditionStack[0];
      },
      // produce the lexer rule set which is active for the currently active lexer condition state
      _currentRules: function() {
        return this.conditionStack.length && this.conditionStack[this.conditionStack.length - 1] ? this.conditions[this.conditionStack[this.conditionStack.length - 1]].rules : this.conditions.INITIAL.rules;
      },
      // return the currently active lexer condition state; when an index argument is provided it produces the N-th previous condition state, if available
      topState: function(u) {
        return u = this.conditionStack.length - 1 - Math.abs(u || 0), u >= 0 ? this.conditionStack[u] : "INITIAL";
      },
      // alias for begin(condition)
      pushState: function(u) {
        this.begin(u);
      },
      // return the number of states currently on the stack
      stateStackSize: function() {
        return this.conditionStack.length;
      },
      options: { "case-insensitive": !0 },
      performAction: function(u, b, i, E) {
        switch (i) {
          case 0:
            return this.begin("open_directive"), 50;
          case 1:
            return this.begin("type_directive"), 51;
          case 2:
            return this.popState(), this.begin("arg_directive"), 9;
          case 3:
            return this.popState(), this.popState(), 53;
          case 4:
            return 52;
          case 5:
            return this.begin("acc_title"), 20;
          case 6:
            return this.popState(), "acc_title_value";
          case 7:
            return this.begin("acc_descr"), 22;
          case 8:
            return this.popState(), "acc_descr_value";
          case 9:
            this.begin("acc_descr_multiline");
            break;
          case 10:
            this.popState();
            break;
          case 11:
            return "acc_descr_multiline_value";
          case 12:
            return 14;
          case 13:
            break;
          case 14:
            break;
          case 15:
            return 6;
          case 16:
            return 40;
          case 17:
            return 33;
          case 18:
            return 38;
          case 19:
            return 42;
          case 20:
            return 43;
          case 21:
            return 44;
          case 22:
            return 45;
          case 23:
            return 35;
          case 24:
            return 29;
          case 25:
            return 30;
          case 26:
            return 37;
          case 27:
            return 32;
          case 28:
            return 27;
          case 29:
            return 10;
          case 30:
            return 10;
          case 31:
            return 9;
          case 32:
            return "CARET";
          case 33:
            this.begin("options");
            break;
          case 34:
            this.popState();
            break;
          case 35:
            return 13;
          case 36:
            return 36;
          case 37:
            this.begin("string");
            break;
          case 38:
            this.popState();
            break;
          case 39:
            return 34;
          case 40:
            return 31;
          case 41:
            return 54;
          case 42:
            return 8;
        }
      },
      rules: [/^(?:%%\{)/i, /^(?:((?:(?!\}%%)[^:.])*))/i, /^(?::)/i, /^(?:\}%%)/i, /^(?:((?:(?!\}%%).|\n)*))/i, /^(?:accTitle\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*\{\s*)/i, /^(?:[\}])/i, /^(?:[^\}]*)/i, /^(?:(\r?\n)+)/i, /^(?:#[^\n]*)/i, /^(?:%[^\n]*)/i, /^(?:gitGraph\b)/i, /^(?:commit(?=\s|$))/i, /^(?:id:)/i, /^(?:type:)/i, /^(?:msg:)/i, /^(?:NORMAL\b)/i, /^(?:REVERSE\b)/i, /^(?:HIGHLIGHT\b)/i, /^(?:tag:)/i, /^(?:branch(?=\s|$))/i, /^(?:order:)/i, /^(?:merge(?=\s|$))/i, /^(?:cherry-pick(?=\s|$))/i, /^(?:checkout(?=\s|$))/i, /^(?:LR\b)/i, /^(?:BT\b)/i, /^(?::)/i, /^(?:\^)/i, /^(?:options\r?\n)/i, /^(?:[ \r\n\t]+end\b)/i, /^(?:[\s\S]+(?=[ \r\n\t]+end))/i, /^(?:["]["])/i, /^(?:["])/i, /^(?:["])/i, /^(?:[^"]*)/i, /^(?:[0-9]+(?=\s|$))/i, /^(?:\w([-\./\w]*[-\w])?)/i, /^(?:$)/i, /^(?:\s+)/i],
      conditions: { acc_descr_multiline: { rules: [10, 11], inclusive: !1 }, acc_descr: { rules: [8], inclusive: !1 }, acc_title: { rules: [6], inclusive: !1 }, close_directive: { rules: [], inclusive: !1 }, arg_directive: { rules: [3, 4], inclusive: !1 }, type_directive: { rules: [2, 3], inclusive: !1 }, open_directive: { rules: [1], inclusive: !1 }, options: { rules: [34, 35], inclusive: !1 }, string: { rules: [38, 39], inclusive: !1 }, INITIAL: { rules: [0, 5, 7, 9, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 36, 37, 40, 41, 42, 43], inclusive: !0 } }
    };
    return B;
  }();
  ne.lexer = Te;
  function ae() {
    this.yy = {};
  }
  return ae.prototype = ne, ne.Parser = ae, new ae();
}();
me.parser = me;
const Be = me;
let te = A().gitGraph.mainBranchName, qe = A().gitGraph.mainBranchOrder, R = {}, O = null, Q = {};
Q[te] = { name: te, order: qe };
let T = {};
T[te] = O;
let M = te, xe = "LR", K = 0;
function fe() {
  return Oe({ length: 7 });
}
const Ye = function(r, n, o) {
  Ge.parseDirective(this, r, n, o);
};
function Fe(r, n) {
  const o = /* @__PURE__ */ Object.create(null);
  return r.reduce((h, a) => {
    const c = n(a);
    return o[c] || (o[c] = !0, h.push(a)), h;
  }, []);
}
const Ke = function(r) {
  xe = r;
};
let ye = {};
const Ue = function(r) {
  G.debug("options str", r), r = r && r.trim(), r = r || "{}";
  try {
    ye = JSON.parse(r);
  } catch (n) {
    G.error("error while parsing gitGraph options", n.message);
  }
}, We = function() {
  return ye;
}, Je = function(r, n, o, h) {
  G.debug("Entering commit:", r, n, o, h), n = V.sanitizeText(n, A()), r = V.sanitizeText(r, A()), h = V.sanitizeText(h, A());
  const a = {
    id: n || K + "-" + fe(),
    message: r,
    seq: K++,
    type: o || X.NORMAL,
    tag: h || "",
    parents: O == null ? [] : [O.id],
    branch: M
  };
  O = a, R[a.id] = a, T[M] = a.id, G.debug("in pushCommit " + a.id);
}, Qe = function(r, n) {
  if (r = V.sanitizeText(r, A()), T[r] === void 0)
    T[r] = O != null ? O.id : null, Q[r] = { name: r, order: n ? parseInt(n, 10) : null }, Ee(r), G.debug("in createBranch");
  else {
    let o = new Error(
      'Trying to create an existing branch. (Help: Either use a new name if you want create a new branch or try using "checkout ' + r + '")'
    );
    throw o.hash = {
      text: "branch " + r,
      token: "branch " + r,
      line: "1",
      loc: { first_line: 1, last_line: 1, first_column: 1, last_column: 1 },
      expected: ['"checkout ' + r + '"']
    }, o;
  }
}, Xe = function(r, n, o, h) {
  r = V.sanitizeText(r, A()), n = V.sanitizeText(n, A());
  const a = R[T[M]], c = R[T[r]];
  if (M === r) {
    let p = new Error('Incorrect usage of "merge". Cannot merge a branch to itself');
    throw p.hash = {
      text: "merge " + r,
      token: "merge " + r,
      line: "1",
      loc: { first_line: 1, last_line: 1, first_column: 1, last_column: 1 },
      expected: ["branch abc"]
    }, p;
  } else if (a === void 0 || !a) {
    let p = new Error(
      'Incorrect usage of "merge". Current branch (' + M + ")has no commits"
    );
    throw p.hash = {
      text: "merge " + r,
      token: "merge " + r,
      line: "1",
      loc: { first_line: 1, last_line: 1, first_column: 1, last_column: 1 },
      expected: ["commit"]
    }, p;
  } else if (T[r] === void 0) {
    let p = new Error(
      'Incorrect usage of "merge". Branch to be merged (' + r + ") does not exist"
    );
    throw p.hash = {
      text: "merge " + r,
      token: "merge " + r,
      line: "1",
      loc: { first_line: 1, last_line: 1, first_column: 1, last_column: 1 },
      expected: ["branch " + r]
    }, p;
  } else if (c === void 0 || !c) {
    let p = new Error(
      'Incorrect usage of "merge". Branch to be merged (' + r + ") has no commits"
    );
    throw p.hash = {
      text: "merge " + r,
      token: "merge " + r,
      line: "1",
      loc: { first_line: 1, last_line: 1, first_column: 1, last_column: 1 },
      expected: ['"commit"']
    }, p;
  } else if (a === c) {
    let p = new Error('Incorrect usage of "merge". Both branches have same head');
    throw p.hash = {
      text: "merge " + r,
      token: "merge " + r,
      line: "1",
      loc: { first_line: 1, last_line: 1, first_column: 1, last_column: 1 },
      expected: ["branch abc"]
    }, p;
  } else if (n && R[n] !== void 0) {
    let p = new Error(
      'Incorrect usage of "merge". Commit with id:' + n + " already exists, use different custom Id"
    );
    throw p.hash = {
      text: "merge " + r + n + o + h,
      token: "merge " + r + n + o + h,
      line: "1",
      loc: { first_line: 1, last_line: 1, first_column: 1, last_column: 1 },
      expected: [
        "merge " + r + " " + n + "_UNIQUE " + o + " " + h
      ]
    }, p;
  }
  const f = {
    id: n || K + "-" + fe(),
    message: "merged branch " + r + " into " + M,
    seq: K++,
    parents: [O == null ? null : O.id, T[r]],
    branch: M,
    type: X.MERGE,
    customType: o,
    customId: !!n,
    tag: h || ""
  };
  O = f, R[f.id] = f, T[M] = f.id, G.debug(T), G.debug("in mergeBranch");
}, Ze = function(r, n, o) {
  if (G.debug("Entering cherryPick:", r, n, o), r = V.sanitizeText(r, A()), n = V.sanitizeText(n, A()), o = V.sanitizeText(o, A()), !r || R[r] === void 0) {
    let c = new Error(
      'Incorrect usage of "cherryPick". Source commit id should exist and provided'
    );
    throw c.hash = {
      text: "cherryPick " + r + " " + n,
      token: "cherryPick " + r + " " + n,
      line: "1",
      loc: { first_line: 1, last_line: 1, first_column: 1, last_column: 1 },
      expected: ["cherry-pick abc"]
    }, c;
  }
  let h = R[r], a = h.branch;
  if (h.type === X.MERGE) {
    let c = new Error(
      'Incorrect usage of "cherryPick". Source commit should not be a merge commit'
    );
    throw c.hash = {
      text: "cherryPick " + r + " " + n,
      token: "cherryPick " + r + " " + n,
      line: "1",
      loc: { first_line: 1, last_line: 1, first_column: 1, last_column: 1 },
      expected: ["cherry-pick abc"]
    }, c;
  }
  if (!n || R[n] === void 0) {
    if (a === M) {
      let p = new Error(
        'Incorrect usage of "cherryPick". Source commit is already on current branch'
      );
      throw p.hash = {
        text: "cherryPick " + r + " " + n,
        token: "cherryPick " + r + " " + n,
        line: "1",
        loc: { first_line: 1, last_line: 1, first_column: 1, last_column: 1 },
        expected: ["cherry-pick abc"]
      }, p;
    }
    const c = R[T[M]];
    if (c === void 0 || !c) {
      let p = new Error(
        'Incorrect usage of "cherry-pick". Current branch (' + M + ")has no commits"
      );
      throw p.hash = {
        text: "cherryPick " + r + " " + n,
        token: "cherryPick " + r + " " + n,
        line: "1",
        loc: { first_line: 1, last_line: 1, first_column: 1, last_column: 1 },
        expected: ["cherry-pick abc"]
      }, p;
    }
    const f = {
      id: K + "-" + fe(),
      message: "cherry-picked " + h + " into " + M,
      seq: K++,
      parents: [O == null ? null : O.id, h.id],
      branch: M,
      type: X.CHERRY_PICK,
      tag: o ?? "cherry-pick:" + h.id
    };
    O = f, R[f.id] = f, T[M] = f.id, G.debug(T), G.debug("in cherryPick");
  }
}, Ee = function(r) {
  if (r = V.sanitizeText(r, A()), T[r] === void 0) {
    let n = new Error(
      'Trying to checkout branch which is not yet created. (Help try using "branch ' + r + '")'
    );
    throw n.hash = {
      text: "checkout " + r,
      token: "checkout " + r,
      line: "1",
      loc: { first_line: 1, last_line: 1, first_column: 1, last_column: 1 },
      expected: ['"branch ' + r + '"']
    }, n;
  } else {
    M = r;
    const n = T[M];
    O = R[n];
  }
};
function ke(r, n, o) {
  const h = r.indexOf(n);
  h === -1 ? r.push(o) : r.splice(h, 1, o);
}
function we(r) {
  const n = r.reduce((a, c) => a.seq > c.seq ? a : c, r[0]);
  let o = "";
  r.forEach(function(a) {
    a === n ? o += "	*" : o += "	|";
  });
  const h = [o, n.id, n.seq];
  for (let a in T)
    T[a] === n.id && h.push(a);
  if (G.debug(h.join(" ")), n.parents && n.parents.length == 2) {
    const a = R[n.parents[0]];
    ke(r, n, a), r.push(R[n.parents[1]]);
  } else {
    if (n.parents.length == 0)
      return;
    {
      const a = R[n.parents];
      ke(r, n, a);
    }
  }
  r = Fe(r, (a) => a.id), we(r);
}
const $e = function() {
  G.debug(R);
  const r = ve()[0];
  we([r]);
}, et = function() {
  R = {}, O = null;
  let r = A().gitGraph.mainBranchName, n = A().gitGraph.mainBranchOrder;
  T = {}, T[r] = null, Q = {}, Q[r] = { name: r, order: n }, M = r, K = 0, je();
}, tt = function() {
  return Object.values(Q).map((n, o) => n.order !== null ? n : {
    ...n,
    order: parseFloat(`0.${o}`, 10)
  }).sort((n, o) => n.order - o.order).map(({ name: n }) => ({ name: n }));
}, rt = function() {
  return T;
}, it = function() {
  return R;
}, ve = function() {
  const r = Object.keys(R).map(function(n) {
    return R[n];
  });
  return r.forEach(function(n) {
    G.debug(n.id);
  }), r.sort((n, o) => n.seq - o.seq), r;
}, st = function() {
  return M;
}, nt = function() {
  return xe;
}, at = function() {
  return O;
}, X = {
  NORMAL: 0,
  REVERSE: 1,
  HIGHLIGHT: 2,
  MERGE: 3,
  CHERRY_PICK: 4
}, ct = {
  parseDirective: Ye,
  getConfig: () => A().gitGraph,
  setDirection: Ke,
  setOptions: Ue,
  getOptions: We,
  commit: Je,
  branch: Qe,
  merge: Xe,
  cherryPick: Ze,
  checkout: Ee,
  //reset,
  prettyPrint: $e,
  clear: et,
  getBranchesAsObjArray: tt,
  getBranches: rt,
  getCommits: it,
  getCommitsArray: ve,
  getCurrentBranch: st,
  getDirection: nt,
  getHead: at,
  setAccTitle: Pe,
  getAccTitle: He,
  getAccDescription: Ne,
  setAccDescription: De,
  setDiagramTitle: Ve,
  getDiagramTitle: ze,
  commitType: X
};
let J = {};
const H = {
  NORMAL: 0,
  REVERSE: 1,
  HIGHLIGHT: 2,
  MERGE: 3,
  CHERRY_PICK: 4
}, F = 8;
let I = {}, re = {}, ie = [], se = 0;
const ot = () => {
  I = {}, re = {}, J = {}, se = 0, ie = [];
}, lt = (r) => {
  const n = document.createElementNS("http://www.w3.org/2000/svg", "text");
  let o = [];
  typeof r == "string" ? o = r.split(/\\n|\n|<br\s*\/?>/gi) : Array.isArray(r) ? o = r : o = [];
  for (const h of o) {
    const a = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
    a.setAttributeNS("http://www.w3.org/XML/1998/namespace", "xml:space", "preserve"), a.setAttribute("dy", "1em"), a.setAttribute("x", "0"), a.setAttribute("class", "row"), a.textContent = h.trim(), n.appendChild(a);
  }
  return n;
}, _e = (r, n, o) => {
  const h = pe().gitGraph, a = r.append("g").attr("class", "commit-bullets"), c = r.append("g").attr("class", "commit-labels");
  let f = 0;
  Object.keys(n).sort((y, m) => n[y].seq - n[m].seq).forEach((y) => {
    const m = n[y], d = I[m.branch].pos, _ = f + 10;
    if (o) {
      let s, C = m.customType !== void 0 && m.customType !== "" ? m.customType : m.type;
      switch (C) {
        case H.NORMAL:
          s = "commit-normal";
          break;
        case H.REVERSE:
          s = "commit-reverse";
          break;
        case H.HIGHLIGHT:
          s = "commit-highlight";
          break;
        case H.MERGE:
          s = "commit-merge";
          break;
        case H.CHERRY_PICK:
          s = "commit-cherry-pick";
          break;
        default:
          s = "commit-normal";
      }
      if (C === H.HIGHLIGHT) {
        const v = a.append("rect");
        v.attr("x", _ - 10), v.attr("y", d - 10), v.attr("height", 20), v.attr("width", 20), v.attr(
          "class",
          `commit ${m.id} commit-highlight${I[m.branch].index % F} ${s}-outer`
        ), a.append("rect").attr("x", _ - 6).attr("y", d - 6).attr("height", 12).attr("width", 12).attr(
          "class",
          `commit ${m.id} commit${I[m.branch].index % F} ${s}-inner`
        );
      } else if (C === H.CHERRY_PICK)
        a.append("circle").attr("cx", _).attr("cy", d).attr("r", 10).attr("class", `commit ${m.id} ${s}`), a.append("circle").attr("cx", _ - 3).attr("cy", d + 2).attr("r", 2.75).attr("fill", "#fff").attr("class", `commit ${m.id} ${s}`), a.append("circle").attr("cx", _ + 3).attr("cy", d + 2).attr("r", 2.75).attr("fill", "#fff").attr("class", `commit ${m.id} ${s}`), a.append("line").attr("x1", _ + 3).attr("y1", d + 1).attr("x2", _).attr("y2", d - 5).attr("stroke", "#fff").attr("class", `commit ${m.id} ${s}`), a.append("line").attr("x1", _ - 3).attr("y1", d + 1).attr("x2", _).attr("y2", d - 5).attr("stroke", "#fff").attr("class", `commit ${m.id} ${s}`);
      else {
        const v = a.append("circle");
        if (v.attr("cx", _), v.attr("cy", d), v.attr("r", m.type === H.MERGE ? 9 : 10), v.attr(
          "class",
          `commit ${m.id} commit${I[m.branch].index % F}`
        ), C === H.MERGE) {
          const N = a.append("circle");
          N.attr("cx", _), N.attr("cy", d), N.attr("r", 6), N.attr(
            "class",
            `commit ${s} ${m.id} commit${I[m.branch].index % F}`
          );
        }
        C === H.REVERSE && a.append("path").attr("d", `M ${_ - 5},${d - 5}L${_ + 5},${d + 5}M${_ - 5},${d + 5}L${_ + 5},${d - 5}`).attr(
          "class",
          `commit ${s} ${m.id} commit${I[m.branch].index % F}`
        );
      }
    }
    if (re[m.id] = { x: f + 10, y: d }, o) {
      if (m.type !== H.CHERRY_PICK && (m.customId && m.type === H.MERGE || m.type !== H.MERGE) && h.showCommitLabel) {
        const v = c.append("g"), N = v.insert("rect").attr("class", "commit-label-bkg"), x = v.append("text").attr("x", f).attr("y", d + 25).attr("class", "commit-label").text(m.id);
        let g = x.node().getBBox();
        if (N.attr("x", f + 10 - g.width / 2 - 2).attr("y", d + 13.5).attr("width", g.width + 2 * 2).attr("height", g.height + 2 * 2), x.attr("x", f + 10 - g.width / 2), h.rotateCommitLabel) {
          let k = -7.5 - (g.width + 10) / 25 * 9.5, P = 10 + g.width / 25 * 8.5;
          v.attr(
            "transform",
            "translate(" + k + ", " + P + ") rotate(" + -45 + ", " + f + ", " + d + ")"
          );
        }
      }
      if (m.tag) {
        const v = c.insert("polygon"), N = c.append("circle"), x = c.append("text").attr("y", d - 16).attr("class", "tag-label").text(m.tag);
        let g = x.node().getBBox();
        x.attr("x", f + 10 - g.width / 2);
        const k = g.height / 2, P = d - 19.2;
        v.attr("class", "tag-label-bkg").attr(
          "points",
          `
          ${f - g.width / 2 - 4 / 2},${P + 2}
          ${f - g.width / 2 - 4 / 2},${P - 2}
          ${f + 10 - g.width / 2 - 4},${P - k - 2}
          ${f + 10 + g.width / 2 + 4},${P - k - 2}
          ${f + 10 + g.width / 2 + 4},${P + k + 2}
          ${f + 10 - g.width / 2 - 4},${P + k + 2}`
        ), N.attr("cx", f - g.width / 2 + 4 / 2).attr("cy", P).attr("r", 1.5).attr("class", "tag-hole");
      }
    }
    f += 50, f > se && (se = f);
  });
}, ht = (r, n, o) => Object.keys(o).filter((c) => o[c].branch === n.branch && o[c].seq > r.seq && o[c].seq < n.seq).length > 0, ue = (r, n, o = 0) => {
  const h = r + Math.abs(r - n) / 2;
  if (o > 5)
    return h;
  if (ie.every((f) => Math.abs(f - h) >= 10))
    return ie.push(h), h;
  const c = Math.abs(r - n);
  return ue(r, n - c / 5, o + 1);
}, mt = (r, n, o, h) => {
  const a = re[n.id], c = re[o.id], f = ht(n, o, h);
  let p = "", w = "", y = 0, m = 0, d = I[o.branch].index, _;
  if (f) {
    p = "A 10 10, 0, 0, 0,", w = "A 10 10, 0, 0, 1,", y = 10, m = 10, d = I[o.branch].index;
    const s = a.y < c.y ? ue(a.y, c.y) : ue(c.y, a.y);
    a.y < c.y ? _ = `M ${a.x} ${a.y} L ${a.x} ${s - y} ${p} ${a.x + m} ${s} L ${c.x - y} ${s} ${w} ${c.x} ${s + m} L ${c.x} ${c.y}` : _ = `M ${a.x} ${a.y} L ${a.x} ${s + y} ${w} ${a.x + m} ${s} L ${c.x - y} ${s} ${p} ${c.x} ${s - m} L ${c.x} ${c.y}`;
  } else
    a.y < c.y && (p = "A 20 20, 0, 0, 0,", y = 20, m = 20, d = I[o.branch].index, _ = `M ${a.x} ${a.y} L ${a.x} ${c.y - y} ${p} ${a.x + m} ${c.y} L ${c.x} ${c.y}`), a.y > c.y && (p = "A 20 20, 0, 0, 0,", y = 20, m = 20, d = I[n.branch].index, _ = `M ${a.x} ${a.y} L ${c.x - y} ${a.y} ${p} ${c.x} ${a.y - m} L ${c.x} ${c.y}`), a.y === c.y && (d = I[n.branch].index, _ = `M ${a.x} ${a.y} L ${a.x} ${c.y - y} ${p} ${a.x + m} ${c.y} L ${c.x} ${c.y}`);
  r.append("path").attr("d", _).attr("class", "arrow arrow" + d % F);
}, ut = (r, n) => {
  const o = r.append("g").attr("class", "commit-arrows");
  Object.keys(n).forEach((h) => {
    const a = n[h];
    a.parents && a.parents.length > 0 && a.parents.forEach((c) => {
      mt(o, n[c], a, n);
    });
  });
}, pt = (r, n) => {
  const o = pe().gitGraph, h = r.append("g");
  n.forEach((a, c) => {
    const f = c % F, p = I[a.name].pos, w = h.append("line");
    w.attr("x1", 0), w.attr("y1", p), w.attr("x2", se), w.attr("y2", p), w.attr("class", "branch branch" + f), ie.push(p);
    let y = a.name;
    const m = lt(y), d = h.insert("rect"), s = h.insert("g").attr("class", "branchLabel").insert("g").attr("class", "label branch-label" + f);
    s.node().appendChild(m);
    let C = m.getBBox();
    d.attr("class", "branchLabelBkg label" + f).attr("rx", 4).attr("ry", 4).attr("x", -C.width - 4 - (o.rotateCommitLabel === !0 ? 30 : 0)).attr("y", -C.height / 2 + 8).attr("width", C.width + 18).attr("height", C.height + 4), s.attr(
      "transform",
      "translate(" + (-C.width - 14 - (o.rotateCommitLabel === !0 ? 30 : 0)) + ", " + (p - C.height / 2 - 1) + ")"
    ), d.attr("transform", "translate(" + -19 + ", " + (p - C.height / 2) + ")");
  });
}, ft = function(r, n, o, h) {
  ot();
  const a = pe(), c = a.gitGraph;
  G.debug("in gitgraph renderer", r + `
`, "id:", n, o), J = h.db.getCommits();
  const f = h.db.getBranchesAsObjArray();
  let p = 0;
  f.forEach((y, m) => {
    I[y.name] = { pos: p, index: m }, p += 50 + (c.rotateCommitLabel ? 40 : 0);
  });
  const w = Ae(`[id="${n}"]`);
  _e(w, J, !1), c.showBranches && pt(w, f), ut(w, J), _e(w, J, !0), Se.insertTitle(
    w,
    "gitTitleText",
    c.titleTopMargin,
    h.db.getDiagramTitle()
  ), Ie(
    void 0,
    w,
    c.diagramPadding,
    c.useMaxWidth ?? a.useMaxWidth
  );
}, bt = {
  draw: ft
}, gt = (r) => `
  .commit-id,
  .commit-msg,
  .branch-label {
    fill: lightgrey;
    color: lightgrey;
    font-family: 'trebuchet ms', verdana, arial, sans-serif;
    font-family: var(--mermaid-font-family);
  }
  ${[0, 1, 2, 3, 4, 5, 6, 7].map(
  (n) => `
        .branch-label${n} { fill: ${r["gitBranchLabel" + n]}; }
        .commit${n} { stroke: ${r["git" + n]}; fill: ${r["git" + n]}; }
        .commit-highlight${n} { stroke: ${r["gitInv" + n]}; fill: ${r["gitInv" + n]}; }
        .label${n}  { fill: ${r["git" + n]}; }
        .arrow${n} { stroke: ${r["git" + n]}; }
        `
).join(`
`)}

  .branch {
    stroke-width: 1;
    stroke: ${r.lineColor};
    stroke-dasharray: 2;
  }
  .commit-label { font-size: ${r.commitLabelFontSize}; fill: ${r.commitLabelColor};}
  .commit-label-bkg { font-size: ${r.commitLabelFontSize}; fill: ${r.commitLabelBackground}; opacity: 0.5; }
  .tag-label { font-size: ${r.tagLabelFontSize}; fill: ${r.tagLabelColor};}
  .tag-label-bkg { fill: ${r.tagLabelBackground}; stroke: ${r.tagLabelBorder}; }
  .tag-hole { fill: ${r.textColor}; }

  .commit-merge {
    stroke: ${r.primaryColor};
    fill: ${r.primaryColor};
  }
  .commit-reverse {
    stroke: ${r.primaryColor};
    fill: ${r.primaryColor};
    stroke-width: 3;
  }
  .commit-highlight-outer {
  }
  .commit-highlight-inner {
    stroke: ${r.primaryColor};
    fill: ${r.primaryColor};
  }

  .arrow { stroke-width: 8; stroke-linecap: round; fill: none}
  .gitTitleText {
    text-anchor: middle;
    font-size: 18px;
    fill: ${r.textColor};
  }
  }
`, dt = gt, vt = {
  parser: Be,
  db: ct,
  renderer: bt,
  styles: dt
};
export {
  vt as diagram
};
//# sourceMappingURL=gitGraphDiagram-602e6108.js.map
