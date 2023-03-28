import { m as Ve } from "./mermaidAPI-04b5c286.js";
import { g as Ut, b as ve, e as le, c as je, f as Qt, l as _e } from "./config-e567ef17.js";
import { s as Ue, g as Fe, a as ze, b as Xe } from "./commonDb-4dc3d465.js";
import { s as ke, q as Yt, w as We, v as xe } from "./utils-aa888deb.js";
import { c as Qe } from "./setupGraphViewbox-a4603a92.js";
import "./errorRenderer-a3c4bedb.js";
var qt = function() {
  var e = function(Ot, _, x, m) {
    for (x = x || {}, m = Ot.length; m--; x[Ot[m]] = _)
      ;
    return x;
  }, t = [1, 6], i = [1, 7], o = [1, 8], l = [1, 9], n = [1, 16], r = [1, 11], a = [1, 12], s = [1, 13], u = [1, 14], d = [1, 15], y = [1, 27], p = [1, 33], C = [1, 34], T = [1, 35], R = [1, 36], D = [1, 37], L = [1, 72], Y = [1, 73], Q = [1, 74], H = [1, 75], q = [1, 76], G = [1, 77], K = [1, 78], J = [1, 38], Z = [1, 39], $ = [1, 40], tt = [1, 41], et = [1, 42], nt = [1, 43], it = [1, 44], st = [1, 45], at = [1, 46], rt = [1, 47], lt = [1, 48], ot = [1, 49], ct = [1, 50], ht = [1, 51], ut = [1, 52], dt = [1, 53], ft = [1, 54], pt = [1, 55], yt = [1, 56], gt = [1, 57], bt = [1, 59], _t = [1, 60], xt = [1, 61], mt = [1, 62], Et = [1, 63], vt = [1, 64], kt = [1, 65], At = [1, 66], Ct = [1, 67], wt = [1, 68], Tt = [1, 69], Nt = [24, 52], $t = [24, 44, 46, 47, 48, 49, 50, 51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84], It = [15, 24, 44, 46, 47, 48, 49, 50, 51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84], E = [1, 94], v = [1, 95], k = [1, 96], A = [1, 97], w = [15, 24, 52], fe = [7, 8, 9, 10, 18, 22, 25, 26, 27, 28], pe = [15, 24, 43, 52], zt = [15, 24, 43, 52, 86, 87, 89, 90], Dt = [15, 43], te = [44, 46, 47, 48, 49, 50, 51, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84], ee = {
    trace: function() {
    },
    yy: {},
    symbols_: { error: 2, start: 3, mermaidDoc: 4, direction: 5, directive: 6, direction_tb: 7, direction_bt: 8, direction_rl: 9, direction_lr: 10, graphConfig: 11, openDirective: 12, typeDirective: 13, closeDirective: 14, NEWLINE: 15, ":": 16, argDirective: 17, open_directive: 18, type_directive: 19, arg_directive: 20, close_directive: 21, C4_CONTEXT: 22, statements: 23, EOF: 24, C4_CONTAINER: 25, C4_COMPONENT: 26, C4_DYNAMIC: 27, C4_DEPLOYMENT: 28, otherStatements: 29, diagramStatements: 30, otherStatement: 31, title: 32, accDescription: 33, acc_title: 34, acc_title_value: 35, acc_descr: 36, acc_descr_value: 37, acc_descr_multiline_value: 38, boundaryStatement: 39, boundaryStartStatement: 40, boundaryStopStatement: 41, boundaryStart: 42, LBRACE: 43, ENTERPRISE_BOUNDARY: 44, attributes: 45, SYSTEM_BOUNDARY: 46, BOUNDARY: 47, CONTAINER_BOUNDARY: 48, NODE: 49, NODE_L: 50, NODE_R: 51, RBRACE: 52, diagramStatement: 53, PERSON: 54, PERSON_EXT: 55, SYSTEM: 56, SYSTEM_DB: 57, SYSTEM_QUEUE: 58, SYSTEM_EXT: 59, SYSTEM_EXT_DB: 60, SYSTEM_EXT_QUEUE: 61, CONTAINER: 62, CONTAINER_DB: 63, CONTAINER_QUEUE: 64, CONTAINER_EXT: 65, CONTAINER_EXT_DB: 66, CONTAINER_EXT_QUEUE: 67, COMPONENT: 68, COMPONENT_DB: 69, COMPONENT_QUEUE: 70, COMPONENT_EXT: 71, COMPONENT_EXT_DB: 72, COMPONENT_EXT_QUEUE: 73, REL: 74, BIREL: 75, REL_U: 76, REL_D: 77, REL_L: 78, REL_R: 79, REL_B: 80, REL_INDEX: 81, UPDATE_EL_STYLE: 82, UPDATE_REL_STYLE: 83, UPDATE_LAYOUT_CONFIG: 84, attribute: 85, STR: 86, STR_KEY: 87, STR_VALUE: 88, ATTRIBUTE: 89, ATTRIBUTE_EMPTY: 90, $accept: 0, $end: 1 },
    terminals_: { 2: "error", 7: "direction_tb", 8: "direction_bt", 9: "direction_rl", 10: "direction_lr", 15: "NEWLINE", 16: ":", 18: "open_directive", 19: "type_directive", 20: "arg_directive", 21: "close_directive", 22: "C4_CONTEXT", 24: "EOF", 25: "C4_CONTAINER", 26: "C4_COMPONENT", 27: "C4_DYNAMIC", 28: "C4_DEPLOYMENT", 32: "title", 33: "accDescription", 34: "acc_title", 35: "acc_title_value", 36: "acc_descr", 37: "acc_descr_value", 38: "acc_descr_multiline_value", 43: "LBRACE", 44: "ENTERPRISE_BOUNDARY", 46: "SYSTEM_BOUNDARY", 47: "BOUNDARY", 48: "CONTAINER_BOUNDARY", 49: "NODE", 50: "NODE_L", 51: "NODE_R", 52: "RBRACE", 54: "PERSON", 55: "PERSON_EXT", 56: "SYSTEM", 57: "SYSTEM_DB", 58: "SYSTEM_QUEUE", 59: "SYSTEM_EXT", 60: "SYSTEM_EXT_DB", 61: "SYSTEM_EXT_QUEUE", 62: "CONTAINER", 63: "CONTAINER_DB", 64: "CONTAINER_QUEUE", 65: "CONTAINER_EXT", 66: "CONTAINER_EXT_DB", 67: "CONTAINER_EXT_QUEUE", 68: "COMPONENT", 69: "COMPONENT_DB", 70: "COMPONENT_QUEUE", 71: "COMPONENT_EXT", 72: "COMPONENT_EXT_DB", 73: "COMPONENT_EXT_QUEUE", 74: "REL", 75: "BIREL", 76: "REL_U", 77: "REL_D", 78: "REL_L", 79: "REL_R", 80: "REL_B", 81: "REL_INDEX", 82: "UPDATE_EL_STYLE", 83: "UPDATE_REL_STYLE", 84: "UPDATE_LAYOUT_CONFIG", 86: "STR", 87: "STR_KEY", 88: "STR_VALUE", 89: "ATTRIBUTE", 90: "ATTRIBUTE_EMPTY" },
    productions_: [0, [3, 1], [3, 1], [3, 2], [5, 1], [5, 1], [5, 1], [5, 1], [4, 1], [6, 4], [6, 6], [12, 1], [13, 1], [17, 1], [14, 1], [11, 4], [11, 4], [11, 4], [11, 4], [11, 4], [23, 1], [23, 1], [23, 2], [29, 1], [29, 2], [29, 3], [31, 1], [31, 1], [31, 2], [31, 2], [31, 1], [39, 3], [40, 3], [40, 3], [40, 4], [42, 2], [42, 2], [42, 2], [42, 2], [42, 2], [42, 2], [42, 2], [41, 1], [30, 1], [30, 2], [30, 3], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 1], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [53, 2], [45, 1], [45, 2], [85, 1], [85, 2], [85, 1], [85, 1]],
    performAction: function(_, x, m, g, O, h, Vt) {
      var f = h.length - 1;
      switch (O) {
        case 4:
          g.setDirection("TB");
          break;
        case 5:
          g.setDirection("BT");
          break;
        case 6:
          g.setDirection("RL");
          break;
        case 7:
          g.setDirection("LR");
          break;
        case 11:
          g.parseDirective("%%{", "open_directive");
          break;
        case 12:
          break;
        case 13:
          h[f] = h[f].trim().replace(/'/g, '"'), g.parseDirective(h[f], "arg_directive");
          break;
        case 14:
          g.parseDirective("}%%", "close_directive", "c4Context");
          break;
        case 15:
        case 16:
        case 17:
        case 18:
        case 19:
          g.setC4Type(h[f - 3]);
          break;
        case 26:
          g.setTitle(h[f].substring(6)), this.$ = h[f].substring(6);
          break;
        case 27:
          g.setAccDescription(h[f].substring(15)), this.$ = h[f].substring(15);
          break;
        case 28:
          this.$ = h[f].trim(), g.setTitle(this.$);
          break;
        case 29:
        case 30:
          this.$ = h[f].trim(), g.setAccDescription(this.$);
          break;
        case 35:
        case 36:
          h[f].splice(2, 0, "ENTERPRISE"), g.addPersonOrSystemBoundary(...h[f]), this.$ = h[f];
          break;
        case 37:
          g.addPersonOrSystemBoundary(...h[f]), this.$ = h[f];
          break;
        case 38:
          h[f].splice(2, 0, "CONTAINER"), g.addContainerBoundary(...h[f]), this.$ = h[f];
          break;
        case 39:
          g.addDeploymentNode("node", ...h[f]), this.$ = h[f];
          break;
        case 40:
          g.addDeploymentNode("nodeL", ...h[f]), this.$ = h[f];
          break;
        case 41:
          g.addDeploymentNode("nodeR", ...h[f]), this.$ = h[f];
          break;
        case 42:
          g.popBoundaryParseStack();
          break;
        case 46:
          g.addPersonOrSystem("person", ...h[f]), this.$ = h[f];
          break;
        case 47:
          g.addPersonOrSystem("external_person", ...h[f]), this.$ = h[f];
          break;
        case 48:
          g.addPersonOrSystem("system", ...h[f]), this.$ = h[f];
          break;
        case 49:
          g.addPersonOrSystem("system_db", ...h[f]), this.$ = h[f];
          break;
        case 50:
          g.addPersonOrSystem("system_queue", ...h[f]), this.$ = h[f];
          break;
        case 51:
          g.addPersonOrSystem("external_system", ...h[f]), this.$ = h[f];
          break;
        case 52:
          g.addPersonOrSystem("external_system_db", ...h[f]), this.$ = h[f];
          break;
        case 53:
          g.addPersonOrSystem("external_system_queue", ...h[f]), this.$ = h[f];
          break;
        case 54:
          g.addContainer("container", ...h[f]), this.$ = h[f];
          break;
        case 55:
          g.addContainer("container_db", ...h[f]), this.$ = h[f];
          break;
        case 56:
          g.addContainer("container_queue", ...h[f]), this.$ = h[f];
          break;
        case 57:
          g.addContainer("external_container", ...h[f]), this.$ = h[f];
          break;
        case 58:
          g.addContainer("external_container_db", ...h[f]), this.$ = h[f];
          break;
        case 59:
          g.addContainer("external_container_queue", ...h[f]), this.$ = h[f];
          break;
        case 60:
          g.addComponent("component", ...h[f]), this.$ = h[f];
          break;
        case 61:
          g.addComponent("component_db", ...h[f]), this.$ = h[f];
          break;
        case 62:
          g.addComponent("component_queue", ...h[f]), this.$ = h[f];
          break;
        case 63:
          g.addComponent("external_component", ...h[f]), this.$ = h[f];
          break;
        case 64:
          g.addComponent("external_component_db", ...h[f]), this.$ = h[f];
          break;
        case 65:
          g.addComponent("external_component_queue", ...h[f]), this.$ = h[f];
          break;
        case 67:
          g.addRel("rel", ...h[f]), this.$ = h[f];
          break;
        case 68:
          g.addRel("birel", ...h[f]), this.$ = h[f];
          break;
        case 69:
          g.addRel("rel_u", ...h[f]), this.$ = h[f];
          break;
        case 70:
          g.addRel("rel_d", ...h[f]), this.$ = h[f];
          break;
        case 71:
          g.addRel("rel_l", ...h[f]), this.$ = h[f];
          break;
        case 72:
          g.addRel("rel_r", ...h[f]), this.$ = h[f];
          break;
        case 73:
          g.addRel("rel_b", ...h[f]), this.$ = h[f];
          break;
        case 74:
          h[f].splice(0, 1), g.addRel("rel", ...h[f]), this.$ = h[f];
          break;
        case 75:
          g.updateElStyle("update_el_style", ...h[f]), this.$ = h[f];
          break;
        case 76:
          g.updateRelStyle("update_rel_style", ...h[f]), this.$ = h[f];
          break;
        case 77:
          g.updateLayoutConfig("update_layout_config", ...h[f]), this.$ = h[f];
          break;
        case 78:
          this.$ = [h[f]];
          break;
        case 79:
          h[f].unshift(h[f - 1]), this.$ = h[f];
          break;
        case 80:
        case 82:
          this.$ = h[f].trim();
          break;
        case 81:
          let Pt = {};
          Pt[h[f - 1].trim()] = h[f].trim(), this.$ = Pt;
          break;
        case 83:
          this.$ = "";
          break;
      }
    },
    table: [{ 3: 1, 4: 2, 5: 3, 6: 4, 7: t, 8: i, 9: o, 10: l, 11: 5, 12: 10, 18: n, 22: r, 25: a, 26: s, 27: u, 28: d }, { 1: [3] }, { 1: [2, 1] }, { 1: [2, 2] }, { 3: 17, 4: 2, 5: 3, 6: 4, 7: t, 8: i, 9: o, 10: l, 11: 5, 12: 10, 18: n, 22: r, 25: a, 26: s, 27: u, 28: d }, { 1: [2, 8] }, { 1: [2, 4] }, { 1: [2, 5] }, { 1: [2, 6] }, { 1: [2, 7] }, { 13: 18, 19: [1, 19] }, { 15: [1, 20] }, { 15: [1, 21] }, { 15: [1, 22] }, { 15: [1, 23] }, { 15: [1, 24] }, { 19: [2, 11] }, { 1: [2, 3] }, { 14: 25, 16: [1, 26], 21: y }, e([16, 21], [2, 12]), { 23: 28, 29: 29, 30: 30, 31: 31, 32: p, 33: C, 34: T, 36: R, 38: D, 39: 58, 40: 70, 42: 71, 44: L, 46: Y, 47: Q, 48: H, 49: q, 50: G, 51: K, 53: 32, 54: J, 55: Z, 56: $, 57: tt, 58: et, 59: nt, 60: it, 61: st, 62: at, 63: rt, 64: lt, 65: ot, 66: ct, 67: ht, 68: ut, 69: dt, 70: ft, 71: pt, 72: yt, 73: gt, 74: bt, 75: _t, 76: xt, 77: mt, 78: Et, 79: vt, 80: kt, 81: At, 82: Ct, 83: wt, 84: Tt }, { 23: 79, 29: 29, 30: 30, 31: 31, 32: p, 33: C, 34: T, 36: R, 38: D, 39: 58, 40: 70, 42: 71, 44: L, 46: Y, 47: Q, 48: H, 49: q, 50: G, 51: K, 53: 32, 54: J, 55: Z, 56: $, 57: tt, 58: et, 59: nt, 60: it, 61: st, 62: at, 63: rt, 64: lt, 65: ot, 66: ct, 67: ht, 68: ut, 69: dt, 70: ft, 71: pt, 72: yt, 73: gt, 74: bt, 75: _t, 76: xt, 77: mt, 78: Et, 79: vt, 80: kt, 81: At, 82: Ct, 83: wt, 84: Tt }, { 23: 80, 29: 29, 30: 30, 31: 31, 32: p, 33: C, 34: T, 36: R, 38: D, 39: 58, 40: 70, 42: 71, 44: L, 46: Y, 47: Q, 48: H, 49: q, 50: G, 51: K, 53: 32, 54: J, 55: Z, 56: $, 57: tt, 58: et, 59: nt, 60: it, 61: st, 62: at, 63: rt, 64: lt, 65: ot, 66: ct, 67: ht, 68: ut, 69: dt, 70: ft, 71: pt, 72: yt, 73: gt, 74: bt, 75: _t, 76: xt, 77: mt, 78: Et, 79: vt, 80: kt, 81: At, 82: Ct, 83: wt, 84: Tt }, { 23: 81, 29: 29, 30: 30, 31: 31, 32: p, 33: C, 34: T, 36: R, 38: D, 39: 58, 40: 70, 42: 71, 44: L, 46: Y, 47: Q, 48: H, 49: q, 50: G, 51: K, 53: 32, 54: J, 55: Z, 56: $, 57: tt, 58: et, 59: nt, 60: it, 61: st, 62: at, 63: rt, 64: lt, 65: ot, 66: ct, 67: ht, 68: ut, 69: dt, 70: ft, 71: pt, 72: yt, 73: gt, 74: bt, 75: _t, 76: xt, 77: mt, 78: Et, 79: vt, 80: kt, 81: At, 82: Ct, 83: wt, 84: Tt }, { 23: 82, 29: 29, 30: 30, 31: 31, 32: p, 33: C, 34: T, 36: R, 38: D, 39: 58, 40: 70, 42: 71, 44: L, 46: Y, 47: Q, 48: H, 49: q, 50: G, 51: K, 53: 32, 54: J, 55: Z, 56: $, 57: tt, 58: et, 59: nt, 60: it, 61: st, 62: at, 63: rt, 64: lt, 65: ot, 66: ct, 67: ht, 68: ut, 69: dt, 70: ft, 71: pt, 72: yt, 73: gt, 74: bt, 75: _t, 76: xt, 77: mt, 78: Et, 79: vt, 80: kt, 81: At, 82: Ct, 83: wt, 84: Tt }, { 15: [1, 83] }, { 17: 84, 20: [1, 85] }, { 15: [2, 14] }, { 24: [1, 86] }, e(Nt, [2, 20], { 53: 32, 39: 58, 40: 70, 42: 71, 30: 87, 44: L, 46: Y, 47: Q, 48: H, 49: q, 50: G, 51: K, 54: J, 55: Z, 56: $, 57: tt, 58: et, 59: nt, 60: it, 61: st, 62: at, 63: rt, 64: lt, 65: ot, 66: ct, 67: ht, 68: ut, 69: dt, 70: ft, 71: pt, 72: yt, 73: gt, 74: bt, 75: _t, 76: xt, 77: mt, 78: Et, 79: vt, 80: kt, 81: At, 82: Ct, 83: wt, 84: Tt }), e(Nt, [2, 21]), e($t, [2, 23], { 15: [1, 88] }), e(Nt, [2, 43], { 15: [1, 89] }), e(It, [2, 26]), e(It, [2, 27]), { 35: [1, 90] }, { 37: [1, 91] }, e(It, [2, 30]), { 45: 92, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 98, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 99, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 100, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 101, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 102, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 103, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 104, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 105, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 106, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 107, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 108, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 109, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 110, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 111, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 112, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 113, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 114, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 115, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 116, 85: 93, 86: E, 87: v, 89: k, 90: A }, e(w, [2, 66]), { 45: 117, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 118, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 119, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 120, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 121, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 122, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 123, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 124, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 125, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 126, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 127, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 30: 128, 39: 58, 40: 70, 42: 71, 44: L, 46: Y, 47: Q, 48: H, 49: q, 50: G, 51: K, 53: 32, 54: J, 55: Z, 56: $, 57: tt, 58: et, 59: nt, 60: it, 61: st, 62: at, 63: rt, 64: lt, 65: ot, 66: ct, 67: ht, 68: ut, 69: dt, 70: ft, 71: pt, 72: yt, 73: gt, 74: bt, 75: _t, 76: xt, 77: mt, 78: Et, 79: vt, 80: kt, 81: At, 82: Ct, 83: wt, 84: Tt }, { 15: [1, 130], 43: [1, 129] }, { 45: 131, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 132, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 133, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 134, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 135, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 136, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 45: 137, 85: 93, 86: E, 87: v, 89: k, 90: A }, { 24: [1, 138] }, { 24: [1, 139] }, { 24: [1, 140] }, { 24: [1, 141] }, e(fe, [2, 9]), { 14: 142, 21: y }, { 21: [2, 13] }, { 1: [2, 15] }, e(Nt, [2, 22]), e($t, [2, 24], { 31: 31, 29: 143, 32: p, 33: C, 34: T, 36: R, 38: D }), e(Nt, [2, 44], { 29: 29, 30: 30, 31: 31, 53: 32, 39: 58, 40: 70, 42: 71, 23: 144, 32: p, 33: C, 34: T, 36: R, 38: D, 44: L, 46: Y, 47: Q, 48: H, 49: q, 50: G, 51: K, 54: J, 55: Z, 56: $, 57: tt, 58: et, 59: nt, 60: it, 61: st, 62: at, 63: rt, 64: lt, 65: ot, 66: ct, 67: ht, 68: ut, 69: dt, 70: ft, 71: pt, 72: yt, 73: gt, 74: bt, 75: _t, 76: xt, 77: mt, 78: Et, 79: vt, 80: kt, 81: At, 82: Ct, 83: wt, 84: Tt }), e(It, [2, 28]), e(It, [2, 29]), e(w, [2, 46]), e(pe, [2, 78], { 85: 93, 45: 145, 86: E, 87: v, 89: k, 90: A }), e(zt, [2, 80]), { 88: [1, 146] }, e(zt, [2, 82]), e(zt, [2, 83]), e(w, [2, 47]), e(w, [2, 48]), e(w, [2, 49]), e(w, [2, 50]), e(w, [2, 51]), e(w, [2, 52]), e(w, [2, 53]), e(w, [2, 54]), e(w, [2, 55]), e(w, [2, 56]), e(w, [2, 57]), e(w, [2, 58]), e(w, [2, 59]), e(w, [2, 60]), e(w, [2, 61]), e(w, [2, 62]), e(w, [2, 63]), e(w, [2, 64]), e(w, [2, 65]), e(w, [2, 67]), e(w, [2, 68]), e(w, [2, 69]), e(w, [2, 70]), e(w, [2, 71]), e(w, [2, 72]), e(w, [2, 73]), e(w, [2, 74]), e(w, [2, 75]), e(w, [2, 76]), e(w, [2, 77]), { 41: 147, 52: [1, 148] }, { 15: [1, 149] }, { 43: [1, 150] }, e(Dt, [2, 35]), e(Dt, [2, 36]), e(Dt, [2, 37]), e(Dt, [2, 38]), e(Dt, [2, 39]), e(Dt, [2, 40]), e(Dt, [2, 41]), { 1: [2, 16] }, { 1: [2, 17] }, { 1: [2, 18] }, { 1: [2, 19] }, { 15: [1, 151] }, e($t, [2, 25]), e(Nt, [2, 45]), e(pe, [2, 79]), e(zt, [2, 81]), e(w, [2, 31]), e(w, [2, 42]), e(te, [2, 32]), e(te, [2, 33], { 15: [1, 152] }), e(fe, [2, 10]), e(te, [2, 34])],
    defaultActions: { 2: [2, 1], 3: [2, 2], 5: [2, 8], 6: [2, 4], 7: [2, 5], 8: [2, 6], 9: [2, 7], 16: [2, 11], 17: [2, 3], 27: [2, 14], 85: [2, 13], 86: [2, 15], 138: [2, 16], 139: [2, 17], 140: [2, 18], 141: [2, 19] },
    parseError: function(_, x) {
      if (x.recoverable)
        this.trace(_);
      else {
        var m = new Error(_);
        throw m.hash = x, m;
      }
    },
    parse: function(_) {
      var x = this, m = [0], g = [], O = [null], h = [], Vt = this.table, f = "", Pt = 0, ye = 0, Ne = 2, ge = 1, Be = h.slice.call(arguments, 1), S = Object.create(this.lexer), Mt = { yy: {} };
      for (var ie in this.yy)
        Object.prototype.hasOwnProperty.call(this.yy, ie) && (Mt.yy[ie] = this.yy[ie]);
      S.setInput(_, Mt.yy), Mt.yy.lexer = S, Mt.yy.parser = this, typeof S.yylloc > "u" && (S.yylloc = {});
      var se = S.yylloc;
      h.push(se);
      var Ye = S.options && S.options.ranges;
      typeof Mt.yy.parseError == "function" ? this.parseError = Mt.yy.parseError : this.parseError = Object.getPrototypeOf(this).parseError;
      function Ie() {
        var X;
        return X = g.pop() || S.lex() || ge, typeof X != "number" && (X instanceof Array && (g = X, X = g.pop()), X = x.symbols_[X] || X), X;
      }
      for (var M, Lt, N, ae, Bt = {}, Xt, z, be, Wt; ; ) {
        if (Lt = m[m.length - 1], this.defaultActions[Lt] ? N = this.defaultActions[Lt] : ((M === null || typeof M > "u") && (M = Ie()), N = Vt[Lt] && Vt[Lt][M]), typeof N > "u" || !N.length || !N[0]) {
          var re = "";
          Wt = [];
          for (Xt in Vt[Lt])
            this.terminals_[Xt] && Xt > Ne && Wt.push("'" + this.terminals_[Xt] + "'");
          S.showPosition ? re = "Parse error on line " + (Pt + 1) + `:
` + S.showPosition() + `
Expecting ` + Wt.join(", ") + ", got '" + (this.terminals_[M] || M) + "'" : re = "Parse error on line " + (Pt + 1) + ": Unexpected " + (M == ge ? "end of input" : "'" + (this.terminals_[M] || M) + "'"), this.parseError(re, {
            text: S.match,
            token: this.terminals_[M] || M,
            line: S.yylineno,
            loc: se,
            expected: Wt
          });
        }
        if (N[0] instanceof Array && N.length > 1)
          throw new Error("Parse Error: multiple actions possible at state: " + Lt + ", token: " + M);
        switch (N[0]) {
          case 1:
            m.push(M), O.push(S.yytext), h.push(S.yylloc), m.push(N[1]), M = null, ye = S.yyleng, f = S.yytext, Pt = S.yylineno, se = S.yylloc;
            break;
          case 2:
            if (z = this.productions_[N[1]][1], Bt.$ = O[O.length - z], Bt._$ = {
              first_line: h[h.length - (z || 1)].first_line,
              last_line: h[h.length - 1].last_line,
              first_column: h[h.length - (z || 1)].first_column,
              last_column: h[h.length - 1].last_column
            }, Ye && (Bt._$.range = [
              h[h.length - (z || 1)].range[0],
              h[h.length - 1].range[1]
            ]), ae = this.performAction.apply(Bt, [
              f,
              ye,
              Pt,
              Mt.yy,
              N[1],
              O,
              h
            ].concat(Be)), typeof ae < "u")
              return ae;
            z && (m = m.slice(0, -1 * z * 2), O = O.slice(0, -1 * z), h = h.slice(0, -1 * z)), m.push(this.productions_[N[1]][0]), O.push(Bt.$), h.push(Bt._$), be = Vt[m[m.length - 2]][m[m.length - 1]], m.push(be);
            break;
          case 3:
            return !0;
        }
      }
      return !0;
    }
  }, Le = function() {
    var Ot = {
      EOF: 1,
      parseError: function(x, m) {
        if (this.yy.parser)
          this.yy.parser.parseError(x, m);
        else
          throw new Error(x);
      },
      // resets the lexer, sets new input
      setInput: function(_, x) {
        return this.yy = x || this.yy || {}, this._input = _, this._more = this._backtrack = this.done = !1, this.yylineno = this.yyleng = 0, this.yytext = this.matched = this.match = "", this.conditionStack = ["INITIAL"], this.yylloc = {
          first_line: 1,
          first_column: 0,
          last_line: 1,
          last_column: 0
        }, this.options.ranges && (this.yylloc.range = [0, 0]), this.offset = 0, this;
      },
      // consumes and returns one char from the input
      input: function() {
        var _ = this._input[0];
        this.yytext += _, this.yyleng++, this.offset++, this.match += _, this.matched += _;
        var x = _.match(/(?:\r\n?|\n).*/g);
        return x ? (this.yylineno++, this.yylloc.last_line++) : this.yylloc.last_column++, this.options.ranges && this.yylloc.range[1]++, this._input = this._input.slice(1), _;
      },
      // unshifts one char (or a string) into the input
      unput: function(_) {
        var x = _.length, m = _.split(/(?:\r\n?|\n)/g);
        this._input = _ + this._input, this.yytext = this.yytext.substr(0, this.yytext.length - x), this.offset -= x;
        var g = this.match.split(/(?:\r\n?|\n)/g);
        this.match = this.match.substr(0, this.match.length - 1), this.matched = this.matched.substr(0, this.matched.length - 1), m.length - 1 && (this.yylineno -= m.length - 1);
        var O = this.yylloc.range;
        return this.yylloc = {
          first_line: this.yylloc.first_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.first_column,
          last_column: m ? (m.length === g.length ? this.yylloc.first_column : 0) + g[g.length - m.length].length - m[0].length : this.yylloc.first_column - x
        }, this.options.ranges && (this.yylloc.range = [O[0], O[0] + this.yyleng - x]), this.yyleng = this.yytext.length, this;
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
      less: function(_) {
        this.unput(this.match.slice(_));
      },
      // displays already matched input, i.e. for error messages
      pastInput: function() {
        var _ = this.matched.substr(0, this.matched.length - this.match.length);
        return (_.length > 20 ? "..." : "") + _.substr(-20).replace(/\n/g, "");
      },
      // displays upcoming input, i.e. for error messages
      upcomingInput: function() {
        var _ = this.match;
        return _.length < 20 && (_ += this._input.substr(0, 20 - _.length)), (_.substr(0, 20) + (_.length > 20 ? "..." : "")).replace(/\n/g, "");
      },
      // displays the character position where the lexing error occurred, i.e. for error messages
      showPosition: function() {
        var _ = this.pastInput(), x = new Array(_.length + 1).join("-");
        return _ + this.upcomingInput() + `
` + x + "^";
      },
      // test the lexed token: return FALSE when not a match, otherwise return token
      test_match: function(_, x) {
        var m, g, O;
        if (this.options.backtrack_lexer && (O = {
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
        }, this.options.ranges && (O.yylloc.range = this.yylloc.range.slice(0))), g = _[0].match(/(?:\r\n?|\n).*/g), g && (this.yylineno += g.length), this.yylloc = {
          first_line: this.yylloc.last_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.last_column,
          last_column: g ? g[g.length - 1].length - g[g.length - 1].match(/\r?\n?/)[0].length : this.yylloc.last_column + _[0].length
        }, this.yytext += _[0], this.match += _[0], this.matches = _, this.yyleng = this.yytext.length, this.options.ranges && (this.yylloc.range = [this.offset, this.offset += this.yyleng]), this._more = !1, this._backtrack = !1, this._input = this._input.slice(_[0].length), this.matched += _[0], m = this.performAction.call(this, this.yy, this, x, this.conditionStack[this.conditionStack.length - 1]), this.done && this._input && (this.done = !1), m)
          return m;
        if (this._backtrack) {
          for (var h in O)
            this[h] = O[h];
          return !1;
        }
        return !1;
      },
      // return next match in input
      next: function() {
        if (this.done)
          return this.EOF;
        this._input || (this.done = !0);
        var _, x, m, g;
        this._more || (this.yytext = "", this.match = "");
        for (var O = this._currentRules(), h = 0; h < O.length; h++)
          if (m = this._input.match(this.rules[O[h]]), m && (!x || m[0].length > x[0].length)) {
            if (x = m, g = h, this.options.backtrack_lexer) {
              if (_ = this.test_match(m, O[h]), _ !== !1)
                return _;
              if (this._backtrack) {
                x = !1;
                continue;
              } else
                return !1;
            } else if (!this.options.flex)
              break;
          }
        return x ? (_ = this.test_match(x, O[g]), _ !== !1 ? _ : !1) : this._input === "" ? this.EOF : this.parseError("Lexical error on line " + (this.yylineno + 1) + `. Unrecognized text.
` + this.showPosition(), {
          text: "",
          token: null,
          line: this.yylineno
        });
      },
      // return next match that has a token
      lex: function() {
        var x = this.next();
        return x || this.lex();
      },
      // activates a new lexer condition state (pushes the new lexer condition state onto the condition stack)
      begin: function(x) {
        this.conditionStack.push(x);
      },
      // pop the previously active lexer condition state off the condition stack
      popState: function() {
        var x = this.conditionStack.length - 1;
        return x > 0 ? this.conditionStack.pop() : this.conditionStack[0];
      },
      // produce the lexer rule set which is active for the currently active lexer condition state
      _currentRules: function() {
        return this.conditionStack.length && this.conditionStack[this.conditionStack.length - 1] ? this.conditions[this.conditionStack[this.conditionStack.length - 1]].rules : this.conditions.INITIAL.rules;
      },
      // return the currently active lexer condition state; when an index argument is provided it produces the N-th previous condition state, if available
      topState: function(x) {
        return x = this.conditionStack.length - 1 - Math.abs(x || 0), x >= 0 ? this.conditionStack[x] : "INITIAL";
      },
      // alias for begin(condition)
      pushState: function(x) {
        this.begin(x);
      },
      // return the number of states currently on the stack
      stateStackSize: function() {
        return this.conditionStack.length;
      },
      options: {},
      performAction: function(x, m, g, O) {
        switch (g) {
          case 0:
            return this.begin("open_directive"), 18;
          case 1:
            return 7;
          case 2:
            return 8;
          case 3:
            return 9;
          case 4:
            return 10;
          case 5:
            return this.begin("type_directive"), 19;
          case 6:
            return this.popState(), this.begin("arg_directive"), 16;
          case 7:
            return this.popState(), this.popState(), 21;
          case 8:
            return 20;
          case 9:
            return 32;
          case 10:
            return 33;
          case 11:
            return this.begin("acc_title"), 34;
          case 12:
            return this.popState(), "acc_title_value";
          case 13:
            return this.begin("acc_descr"), 36;
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
            break;
          case 19:
            c;
            break;
          case 20:
            return 15;
          case 21:
            break;
          case 22:
            return 22;
          case 23:
            return 25;
          case 24:
            return 26;
          case 25:
            return 27;
          case 26:
            return 28;
          case 27:
            return this.begin("person_ext"), 55;
          case 28:
            return this.begin("person"), 54;
          case 29:
            return this.begin("system_ext_queue"), 61;
          case 30:
            return this.begin("system_ext_db"), 60;
          case 31:
            return this.begin("system_ext"), 59;
          case 32:
            return this.begin("system_queue"), 58;
          case 33:
            return this.begin("system_db"), 57;
          case 34:
            return this.begin("system"), 56;
          case 35:
            return this.begin("boundary"), 47;
          case 36:
            return this.begin("enterprise_boundary"), 44;
          case 37:
            return this.begin("system_boundary"), 46;
          case 38:
            return this.begin("container_ext_queue"), 67;
          case 39:
            return this.begin("container_ext_db"), 66;
          case 40:
            return this.begin("container_ext"), 65;
          case 41:
            return this.begin("container_queue"), 64;
          case 42:
            return this.begin("container_db"), 63;
          case 43:
            return this.begin("container"), 62;
          case 44:
            return this.begin("container_boundary"), 48;
          case 45:
            return this.begin("component_ext_queue"), 73;
          case 46:
            return this.begin("component_ext_db"), 72;
          case 47:
            return this.begin("component_ext"), 71;
          case 48:
            return this.begin("component_queue"), 70;
          case 49:
            return this.begin("component_db"), 69;
          case 50:
            return this.begin("component"), 68;
          case 51:
            return this.begin("node"), 49;
          case 52:
            return this.begin("node"), 49;
          case 53:
            return this.begin("node_l"), 50;
          case 54:
            return this.begin("node_r"), 51;
          case 55:
            return this.begin("rel"), 74;
          case 56:
            return this.begin("birel"), 75;
          case 57:
            return this.begin("rel_u"), 76;
          case 58:
            return this.begin("rel_u"), 76;
          case 59:
            return this.begin("rel_d"), 77;
          case 60:
            return this.begin("rel_d"), 77;
          case 61:
            return this.begin("rel_l"), 78;
          case 62:
            return this.begin("rel_l"), 78;
          case 63:
            return this.begin("rel_r"), 79;
          case 64:
            return this.begin("rel_r"), 79;
          case 65:
            return this.begin("rel_b"), 80;
          case 66:
            return this.begin("rel_index"), 81;
          case 67:
            return this.begin("update_el_style"), 82;
          case 68:
            return this.begin("update_rel_style"), 83;
          case 69:
            return this.begin("update_layout_config"), 84;
          case 70:
            return "EOF_IN_STRUCT";
          case 71:
            return this.begin("attribute"), "ATTRIBUTE_EMPTY";
          case 72:
            this.begin("attribute");
            break;
          case 73:
            this.popState(), this.popState();
            break;
          case 74:
            return 90;
          case 75:
            break;
          case 76:
            return 90;
          case 77:
            this.begin("string");
            break;
          case 78:
            this.popState();
            break;
          case 79:
            return "STR";
          case 80:
            this.begin("string_kv");
            break;
          case 81:
            return this.begin("string_kv_key"), "STR_KEY";
          case 82:
            this.popState(), this.begin("string_kv_value");
            break;
          case 83:
            return "STR_VALUE";
          case 84:
            this.popState(), this.popState();
            break;
          case 85:
            return "STR";
          case 86:
            return "LBRACE";
          case 87:
            return "RBRACE";
          case 88:
            return "SPACE";
          case 89:
            return "EOL";
          case 90:
            return 24;
        }
      },
      rules: [/^(?:%%\{)/, /^(?:.*direction\s+TB[^\n]*)/, /^(?:.*direction\s+BT[^\n]*)/, /^(?:.*direction\s+RL[^\n]*)/, /^(?:.*direction\s+LR[^\n]*)/, /^(?:((?:(?!\}%%)[^:.])*))/, /^(?::)/, /^(?:\}%%)/, /^(?:((?:(?!\}%%).|\n)*))/, /^(?:title\s[^#\n;]+)/, /^(?:accDescription\s[^#\n;]+)/, /^(?:accTitle\s*:\s*)/, /^(?:(?!\n||)*[^\n]*)/, /^(?:accDescr\s*:\s*)/, /^(?:(?!\n||)*[^\n]*)/, /^(?:accDescr\s*\{\s*)/, /^(?:[\}])/, /^(?:[^\}]*)/, /^(?:%%(?!\{)*[^\n]*(\r?\n?)+)/, /^(?:%%[^\n]*(\r?\n)*)/, /^(?:\s*(\r?\n)+)/, /^(?:\s+)/, /^(?:C4Context\b)/, /^(?:C4Container\b)/, /^(?:C4Component\b)/, /^(?:C4Dynamic\b)/, /^(?:C4Deployment\b)/, /^(?:Person_Ext\b)/, /^(?:Person\b)/, /^(?:SystemQueue_Ext\b)/, /^(?:SystemDb_Ext\b)/, /^(?:System_Ext\b)/, /^(?:SystemQueue\b)/, /^(?:SystemDb\b)/, /^(?:System\b)/, /^(?:Boundary\b)/, /^(?:Enterprise_Boundary\b)/, /^(?:System_Boundary\b)/, /^(?:ContainerQueue_Ext\b)/, /^(?:ContainerDb_Ext\b)/, /^(?:Container_Ext\b)/, /^(?:ContainerQueue\b)/, /^(?:ContainerDb\b)/, /^(?:Container\b)/, /^(?:Container_Boundary\b)/, /^(?:ComponentQueue_Ext\b)/, /^(?:ComponentDb_Ext\b)/, /^(?:Component_Ext\b)/, /^(?:ComponentQueue\b)/, /^(?:ComponentDb\b)/, /^(?:Component\b)/, /^(?:Deployment_Node\b)/, /^(?:Node\b)/, /^(?:Node_L\b)/, /^(?:Node_R\b)/, /^(?:Rel\b)/, /^(?:BiRel\b)/, /^(?:Rel_Up\b)/, /^(?:Rel_U\b)/, /^(?:Rel_Down\b)/, /^(?:Rel_D\b)/, /^(?:Rel_Left\b)/, /^(?:Rel_L\b)/, /^(?:Rel_Right\b)/, /^(?:Rel_R\b)/, /^(?:Rel_Back\b)/, /^(?:RelIndex\b)/, /^(?:UpdateElementStyle\b)/, /^(?:UpdateRelStyle\b)/, /^(?:UpdateLayoutConfig\b)/, /^(?:$)/, /^(?:[(][ ]*[,])/, /^(?:[(])/, /^(?:[)])/, /^(?:,,)/, /^(?:,)/, /^(?:[ ]*["]["])/, /^(?:[ ]*["])/, /^(?:["])/, /^(?:[^"]*)/, /^(?:[ ]*[\$])/, /^(?:[^=]*)/, /^(?:[=][ ]*["])/, /^(?:[^"]+)/, /^(?:["])/, /^(?:[^,]+)/, /^(?:\{)/, /^(?:\})/, /^(?:[\s]+)/, /^(?:[\n\r]+)/, /^(?:$)/],
      conditions: { acc_descr_multiline: { rules: [16, 17], inclusive: !1 }, acc_descr: { rules: [14], inclusive: !1 }, acc_title: { rules: [12], inclusive: !1 }, close_directive: { rules: [], inclusive: !1 }, arg_directive: { rules: [7, 8], inclusive: !1 }, type_directive: { rules: [6, 7], inclusive: !1 }, open_directive: { rules: [5], inclusive: !1 }, string_kv_value: { rules: [83, 84], inclusive: !1 }, string_kv_key: { rules: [82], inclusive: !1 }, string_kv: { rules: [81], inclusive: !1 }, string: { rules: [78, 79], inclusive: !1 }, attribute: { rules: [73, 74, 75, 76, 77, 80, 85], inclusive: !1 }, update_layout_config: { rules: [70, 71, 72, 73], inclusive: !1 }, update_rel_style: { rules: [70, 71, 72, 73], inclusive: !1 }, update_el_style: { rules: [70, 71, 72, 73], inclusive: !1 }, rel_b: { rules: [70, 71, 72, 73], inclusive: !1 }, rel_r: { rules: [70, 71, 72, 73], inclusive: !1 }, rel_l: { rules: [70, 71, 72, 73], inclusive: !1 }, rel_d: { rules: [70, 71, 72, 73], inclusive: !1 }, rel_u: { rules: [70, 71, 72, 73], inclusive: !1 }, rel_bi: { rules: [], inclusive: !1 }, rel: { rules: [70, 71, 72, 73], inclusive: !1 }, node_r: { rules: [70, 71, 72, 73], inclusive: !1 }, node_l: { rules: [70, 71, 72, 73], inclusive: !1 }, node: { rules: [70, 71, 72, 73], inclusive: !1 }, index: { rules: [], inclusive: !1 }, rel_index: { rules: [70, 71, 72, 73], inclusive: !1 }, component_ext_queue: { rules: [], inclusive: !1 }, component_ext_db: { rules: [70, 71, 72, 73], inclusive: !1 }, component_ext: { rules: [70, 71, 72, 73], inclusive: !1 }, component_queue: { rules: [70, 71, 72, 73], inclusive: !1 }, component_db: { rules: [70, 71, 72, 73], inclusive: !1 }, component: { rules: [70, 71, 72, 73], inclusive: !1 }, container_boundary: { rules: [70, 71, 72, 73], inclusive: !1 }, container_ext_queue: { rules: [], inclusive: !1 }, container_ext_db: { rules: [70, 71, 72, 73], inclusive: !1 }, container_ext: { rules: [70, 71, 72, 73], inclusive: !1 }, container_queue: { rules: [70, 71, 72, 73], inclusive: !1 }, container_db: { rules: [70, 71, 72, 73], inclusive: !1 }, container: { rules: [70, 71, 72, 73], inclusive: !1 }, birel: { rules: [70, 71, 72, 73], inclusive: !1 }, system_boundary: { rules: [70, 71, 72, 73], inclusive: !1 }, enterprise_boundary: { rules: [70, 71, 72, 73], inclusive: !1 }, boundary: { rules: [70, 71, 72, 73], inclusive: !1 }, system_ext_queue: { rules: [70, 71, 72, 73], inclusive: !1 }, system_ext_db: { rules: [70, 71, 72, 73], inclusive: !1 }, system_ext: { rules: [70, 71, 72, 73], inclusive: !1 }, system_queue: { rules: [70, 71, 72, 73], inclusive: !1 }, system_db: { rules: [70, 71, 72, 73], inclusive: !1 }, system: { rules: [70, 71, 72, 73], inclusive: !1 }, person_ext: { rules: [70, 71, 72, 73], inclusive: !1 }, person: { rules: [70, 71, 72, 73], inclusive: !1 }, INITIAL: { rules: [0, 1, 2, 3, 4, 9, 10, 11, 13, 15, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 86, 87, 88, 89, 90], inclusive: !0 } }
    };
    return Ot;
  }();
  ee.lexer = Le;
  function ne() {
    this.yy = {};
  }
  return ne.prototype = ee, ee.Parser = ne, new ne();
}();
qt.parser = qt;
const He = qt;
let j = [], Rt = [""], P = "global", V = "", F = [
  {
    alias: "global",
    label: { text: "global" },
    type: { text: "global" },
    tags: null,
    link: null,
    parentBoundary: ""
  }
], Ft = [], he = "", ue = !1, Gt = 4, Kt = 2;
var Ae;
const qe = function() {
  return Ae;
}, Ge = function(e) {
  Ae = ve(e, Ut());
}, Ke = function(e, t, i) {
  Ve.parseDirective(this, e, t, i);
}, Je = function(e, t, i, o, l, n, r, a, s) {
  if (e == null || t === void 0 || t === null || i === void 0 || i === null || o === void 0 || o === null)
    return;
  let u = {};
  const d = Ft.find((y) => y.from === t && y.to === i);
  if (d ? u = d : Ft.push(u), u.type = e, u.from = t, u.to = i, u.label = { text: o }, l == null)
    u.techn = { text: "" };
  else if (typeof l == "object") {
    let [y, p] = Object.entries(l)[0];
    u[y] = { text: p };
  } else
    u.techn = { text: l };
  if (n == null)
    u.descr = { text: "" };
  else if (typeof n == "object") {
    let [y, p] = Object.entries(n)[0];
    u[y] = { text: p };
  } else
    u.descr = { text: n };
  if (typeof r == "object") {
    let [y, p] = Object.entries(r)[0];
    u[y] = p;
  } else
    u.sprite = r;
  if (typeof a == "object") {
    let [y, p] = Object.entries(a)[0];
    u[y] = p;
  } else
    u.tags = a;
  if (typeof s == "object") {
    let [y, p] = Object.entries(s)[0];
    u[y] = p;
  } else
    u.link = s;
  u.wrap = St();
}, Ze = function(e, t, i, o, l, n, r) {
  if (t === null || i === null)
    return;
  let a = {};
  const s = j.find((u) => u.alias === t);
  if (s && t === s.alias ? a = s : (a.alias = t, j.push(a)), i == null ? a.label = { text: "" } : a.label = { text: i }, o == null)
    a.descr = { text: "" };
  else if (typeof o == "object") {
    let [u, d] = Object.entries(o)[0];
    a[u] = { text: d };
  } else
    a.descr = { text: o };
  if (typeof l == "object") {
    let [u, d] = Object.entries(l)[0];
    a[u] = d;
  } else
    a.sprite = l;
  if (typeof n == "object") {
    let [u, d] = Object.entries(n)[0];
    a[u] = d;
  } else
    a.tags = n;
  if (typeof r == "object") {
    let [u, d] = Object.entries(r)[0];
    a[u] = d;
  } else
    a.link = r;
  a.typeC4Shape = { text: e }, a.parentBoundary = P, a.wrap = St();
}, $e = function(e, t, i, o, l, n, r, a) {
  if (t === null || i === null)
    return;
  let s = {};
  const u = j.find((d) => d.alias === t);
  if (u && t === u.alias ? s = u : (s.alias = t, j.push(s)), i == null ? s.label = { text: "" } : s.label = { text: i }, o == null)
    s.techn = { text: "" };
  else if (typeof o == "object") {
    let [d, y] = Object.entries(o)[0];
    s[d] = { text: y };
  } else
    s.techn = { text: o };
  if (l == null)
    s.descr = { text: "" };
  else if (typeof l == "object") {
    let [d, y] = Object.entries(l)[0];
    s[d] = { text: y };
  } else
    s.descr = { text: l };
  if (typeof n == "object") {
    let [d, y] = Object.entries(n)[0];
    s[d] = y;
  } else
    s.sprite = n;
  if (typeof r == "object") {
    let [d, y] = Object.entries(r)[0];
    s[d] = y;
  } else
    s.tags = r;
  if (typeof a == "object") {
    let [d, y] = Object.entries(a)[0];
    s[d] = y;
  } else
    s.link = a;
  s.wrap = St(), s.typeC4Shape = { text: e }, s.parentBoundary = P;
}, t0 = function(e, t, i, o, l, n, r, a) {
  if (t === null || i === null)
    return;
  let s = {};
  const u = j.find((d) => d.alias === t);
  if (u && t === u.alias ? s = u : (s.alias = t, j.push(s)), i == null ? s.label = { text: "" } : s.label = { text: i }, o == null)
    s.techn = { text: "" };
  else if (typeof o == "object") {
    let [d, y] = Object.entries(o)[0];
    s[d] = { text: y };
  } else
    s.techn = { text: o };
  if (l == null)
    s.descr = { text: "" };
  else if (typeof l == "object") {
    let [d, y] = Object.entries(l)[0];
    s[d] = { text: y };
  } else
    s.descr = { text: l };
  if (typeof n == "object") {
    let [d, y] = Object.entries(n)[0];
    s[d] = y;
  } else
    s.sprite = n;
  if (typeof r == "object") {
    let [d, y] = Object.entries(r)[0];
    s[d] = y;
  } else
    s.tags = r;
  if (typeof a == "object") {
    let [d, y] = Object.entries(a)[0];
    s[d] = y;
  } else
    s.link = a;
  s.wrap = St(), s.typeC4Shape = { text: e }, s.parentBoundary = P;
}, e0 = function(e, t, i, o, l) {
  if (e === null || t === null)
    return;
  let n = {};
  const r = F.find((a) => a.alias === e);
  if (r && e === r.alias ? n = r : (n.alias = e, F.push(n)), t == null ? n.label = { text: "" } : n.label = { text: t }, i == null)
    n.type = { text: "system" };
  else if (typeof i == "object") {
    let [a, s] = Object.entries(i)[0];
    n[a] = { text: s };
  } else
    n.type = { text: i };
  if (typeof o == "object") {
    let [a, s] = Object.entries(o)[0];
    n[a] = s;
  } else
    n.tags = o;
  if (typeof l == "object") {
    let [a, s] = Object.entries(l)[0];
    n[a] = s;
  } else
    n.link = l;
  n.parentBoundary = P, n.wrap = St(), V = P, P = e, Rt.push(V);
}, n0 = function(e, t, i, o, l) {
  if (e === null || t === null)
    return;
  let n = {};
  const r = F.find((a) => a.alias === e);
  if (r && e === r.alias ? n = r : (n.alias = e, F.push(n)), t == null ? n.label = { text: "" } : n.label = { text: t }, i == null)
    n.type = { text: "container" };
  else if (typeof i == "object") {
    let [a, s] = Object.entries(i)[0];
    n[a] = { text: s };
  } else
    n.type = { text: i };
  if (typeof o == "object") {
    let [a, s] = Object.entries(o)[0];
    n[a] = s;
  } else
    n.tags = o;
  if (typeof l == "object") {
    let [a, s] = Object.entries(l)[0];
    n[a] = s;
  } else
    n.link = l;
  n.parentBoundary = P, n.wrap = St(), V = P, P = e, Rt.push(V);
}, i0 = function(e, t, i, o, l, n, r, a) {
  if (t === null || i === null)
    return;
  let s = {};
  const u = F.find((d) => d.alias === t);
  if (u && t === u.alias ? s = u : (s.alias = t, F.push(s)), i == null ? s.label = { text: "" } : s.label = { text: i }, o == null)
    s.type = { text: "node" };
  else if (typeof o == "object") {
    let [d, y] = Object.entries(o)[0];
    s[d] = { text: y };
  } else
    s.type = { text: o };
  if (l == null)
    s.descr = { text: "" };
  else if (typeof l == "object") {
    let [d, y] = Object.entries(l)[0];
    s[d] = { text: y };
  } else
    s.descr = { text: l };
  if (typeof r == "object") {
    let [d, y] = Object.entries(r)[0];
    s[d] = y;
  } else
    s.tags = r;
  if (typeof a == "object") {
    let [d, y] = Object.entries(a)[0];
    s[d] = y;
  } else
    s.link = a;
  s.nodeType = e, s.parentBoundary = P, s.wrap = St(), V = P, P = t, Rt.push(V);
}, s0 = function() {
  P = V, Rt.pop(), V = Rt.pop(), Rt.push(V);
}, a0 = function(e, t, i, o, l, n, r, a, s, u, d) {
  let y = j.find((p) => p.alias === t);
  if (!(y === void 0 && (y = F.find((p) => p.alias === t), y === void 0))) {
    if (i != null)
      if (typeof i == "object") {
        let [p, C] = Object.entries(i)[0];
        y[p] = C;
      } else
        y.bgColor = i;
    if (o != null)
      if (typeof o == "object") {
        let [p, C] = Object.entries(o)[0];
        y[p] = C;
      } else
        y.fontColor = o;
    if (l != null)
      if (typeof l == "object") {
        let [p, C] = Object.entries(l)[0];
        y[p] = C;
      } else
        y.borderColor = l;
    if (n != null)
      if (typeof n == "object") {
        let [p, C] = Object.entries(n)[0];
        y[p] = C;
      } else
        y.shadowing = n;
    if (r != null)
      if (typeof r == "object") {
        let [p, C] = Object.entries(r)[0];
        y[p] = C;
      } else
        y.shape = r;
    if (a != null)
      if (typeof a == "object") {
        let [p, C] = Object.entries(a)[0];
        y[p] = C;
      } else
        y.sprite = a;
    if (s != null)
      if (typeof s == "object") {
        let [p, C] = Object.entries(s)[0];
        y[p] = C;
      } else
        y.techn = s;
    if (u != null)
      if (typeof u == "object") {
        let [p, C] = Object.entries(u)[0];
        y[p] = C;
      } else
        y.legendText = u;
    if (d != null)
      if (typeof d == "object") {
        let [p, C] = Object.entries(d)[0];
        y[p] = C;
      } else
        y.legendSprite = d;
  }
}, r0 = function(e, t, i, o, l, n, r) {
  const a = Ft.find((s) => s.from === t && s.to === i);
  if (a !== void 0) {
    if (o != null)
      if (typeof o == "object") {
        let [s, u] = Object.entries(o)[0];
        a[s] = u;
      } else
        a.textColor = o;
    if (l != null)
      if (typeof l == "object") {
        let [s, u] = Object.entries(l)[0];
        a[s] = u;
      } else
        a.lineColor = l;
    if (n != null)
      if (typeof n == "object") {
        let [s, u] = Object.entries(n)[0];
        a[s] = parseInt(u);
      } else
        a.offsetX = parseInt(n);
    if (r != null)
      if (typeof r == "object") {
        let [s, u] = Object.entries(r)[0];
        a[s] = parseInt(u);
      } else
        a.offsetY = parseInt(r);
  }
}, l0 = function(e, t, i) {
  let o = Gt, l = Kt;
  if (typeof t == "object") {
    const n = Object.values(t)[0];
    o = parseInt(n);
  } else
    o = parseInt(t);
  if (typeof i == "object") {
    const n = Object.values(i)[0];
    l = parseInt(n);
  } else
    l = parseInt(i);
  o >= 1 && (Gt = o), l >= 1 && (Kt = l);
}, o0 = function() {
  return Gt;
}, c0 = function() {
  return Kt;
}, h0 = function() {
  return P;
}, u0 = function() {
  return V;
}, Ce = function(e) {
  return e == null ? j : j.filter((t) => t.parentBoundary === e);
}, d0 = function(e) {
  return j.find((t) => t.alias === e);
}, f0 = function(e) {
  return Object.keys(Ce(e));
}, p0 = function(e) {
  return e == null ? F : F.filter((t) => t.parentBoundary === e);
}, y0 = function() {
  return Ft;
}, g0 = function() {
  return he;
}, b0 = function(e) {
  ue = e;
}, St = function() {
  return ue;
}, _0 = function() {
  j = [], F = [
    {
      alias: "global",
      label: { text: "global" },
      type: { text: "global" },
      tags: null,
      link: null,
      parentBoundary: ""
    }
  ], V = "", P = "global", Rt = [""], Ft = [], Rt = [""], he = "", ue = !1, Gt = 4, Kt = 2;
}, x0 = {
  SOLID: 0,
  DOTTED: 1,
  NOTE: 2,
  SOLID_CROSS: 3,
  DOTTED_CROSS: 4,
  SOLID_OPEN: 5,
  DOTTED_OPEN: 6,
  LOOP_START: 10,
  LOOP_END: 11,
  ALT_START: 12,
  ALT_ELSE: 13,
  ALT_END: 14,
  OPT_START: 15,
  OPT_END: 16,
  ACTIVE_START: 17,
  ACTIVE_END: 18,
  PAR_START: 19,
  PAR_AND: 20,
  PAR_END: 21,
  RECT_START: 22,
  RECT_END: 23,
  SOLID_POINT: 24,
  DOTTED_POINT: 25
}, m0 = {
  FILLED: 0,
  OPEN: 1
}, E0 = {
  LEFTOF: 0,
  RIGHTOF: 1,
  OVER: 2
}, v0 = function(e) {
  he = ve(e, Ut());
}, we = {
  addPersonOrSystem: Ze,
  addPersonOrSystemBoundary: e0,
  addContainer: $e,
  addContainerBoundary: n0,
  addComponent: t0,
  addDeploymentNode: i0,
  popBoundaryParseStack: s0,
  addRel: Je,
  updateElStyle: a0,
  updateRelStyle: r0,
  updateLayoutConfig: l0,
  autoWrap: St,
  setWrap: b0,
  getC4ShapeArray: Ce,
  getC4Shape: d0,
  getC4ShapeKeys: f0,
  getBoundarys: p0,
  getCurrentBoundaryParse: h0,
  getParentBoundaryParse: u0,
  getRels: y0,
  getTitle: g0,
  getC4Type: qe,
  getC4ShapeInRow: o0,
  getC4BoundaryInRow: c0,
  setAccTitle: Ue,
  getAccTitle: Fe,
  getAccDescription: ze,
  setAccDescription: Xe,
  parseDirective: Ke,
  getConfig: () => Ut().c4,
  clear: _0,
  LINETYPE: x0,
  ARROWTYPE: m0,
  PLACEMENT: E0,
  setTitle: v0,
  setC4Type: Ge
  // apply,
}, de = function(e, t) {
  const i = e.append("rect");
  if (i.attr("x", t.x), i.attr("y", t.y), i.attr("fill", t.fill), i.attr("stroke", t.stroke), i.attr("width", t.width), i.attr("height", t.height), i.attr("rx", t.rx), i.attr("ry", t.ry), t.attrs !== "undefined" && t.attrs !== null)
    for (let o in t.attrs)
      i.attr(o, t.attrs[o]);
  return t.class !== "undefined" && i.attr("class", t.class), i;
}, Te = function(e, t, i, o, l, n) {
  const r = e.append("image");
  r.attr("width", t), r.attr("height", i), r.attr("x", o), r.attr("y", l);
  let a = n.startsWith("data:image/png;base64") ? n : ke(n);
  r.attr("xlink:href", a);
}, k0 = (e, t, i) => {
  const o = e.append("g");
  let l = 0;
  for (let n of t) {
    let r = n.textColor ? n.textColor : "#444444", a = n.lineColor ? n.lineColor : "#444444", s = n.offsetX ? parseInt(n.offsetX) : 0, u = n.offsetY ? parseInt(n.offsetY) : 0, d = "";
    if (l === 0) {
      let p = o.append("line");
      p.attr("x1", n.startPoint.x), p.attr("y1", n.startPoint.y), p.attr("x2", n.endPoint.x), p.attr("y2", n.endPoint.y), p.attr("stroke-width", "1"), p.attr("stroke", a), p.style("fill", "none"), n.type !== "rel_b" && p.attr("marker-end", "url(" + d + "#arrowhead)"), (n.type === "birel" || n.type === "rel_b") && p.attr("marker-start", "url(" + d + "#arrowend)"), l = -1;
    } else {
      let p = o.append("path");
      p.attr("fill", "none").attr("stroke-width", "1").attr("stroke", a).attr(
        "d",
        "Mstartx,starty Qcontrolx,controly stopx,stopy ".replaceAll("startx", n.startPoint.x).replaceAll("starty", n.startPoint.y).replaceAll(
          "controlx",
          n.startPoint.x + (n.endPoint.x - n.startPoint.x) / 2 - (n.endPoint.x - n.startPoint.x) / 4
        ).replaceAll("controly", n.startPoint.y + (n.endPoint.y - n.startPoint.y) / 2).replaceAll("stopx", n.endPoint.x).replaceAll("stopy", n.endPoint.y)
      ), n.type !== "rel_b" && p.attr("marker-end", "url(" + d + "#arrowhead)"), (n.type === "birel" || n.type === "rel_b") && p.attr("marker-start", "url(" + d + "#arrowend)");
    }
    let y = i.messageFont();
    W(i)(
      n.label.text,
      o,
      Math.min(n.startPoint.x, n.endPoint.x) + Math.abs(n.endPoint.x - n.startPoint.x) / 2 + s,
      Math.min(n.startPoint.y, n.endPoint.y) + Math.abs(n.endPoint.y - n.startPoint.y) / 2 + u,
      n.label.width,
      n.label.height,
      { fill: r },
      y
    ), n.techn && n.techn.text !== "" && (y = i.messageFont(), W(i)(
      "[" + n.techn.text + "]",
      o,
      Math.min(n.startPoint.x, n.endPoint.x) + Math.abs(n.endPoint.x - n.startPoint.x) / 2 + s,
      Math.min(n.startPoint.y, n.endPoint.y) + Math.abs(n.endPoint.y - n.startPoint.y) / 2 + i.messageFontSize + 5 + u,
      Math.max(n.label.width, n.techn.width),
      n.techn.height,
      { fill: r, "font-style": "italic" },
      y
    ));
  }
}, A0 = function(e, t, i) {
  const o = e.append("g");
  let l = t.bgColor ? t.bgColor : "none", n = t.borderColor ? t.borderColor : "#444444", r = t.fontColor ? t.fontColor : "black", a = { "stroke-width": 1, "stroke-dasharray": "7.0,7.0" };
  t.nodeType && (a = { "stroke-width": 1 });
  let s = {
    x: t.x,
    y: t.y,
    fill: l,
    stroke: n,
    width: t.width,
    height: t.height,
    rx: 2.5,
    ry: 2.5,
    attrs: a
  };
  de(o, s);
  let u = i.boundaryFont();
  u.fontWeight = "bold", u.fontSize = u.fontSize + 2, u.fontColor = r, W(i)(
    t.label.text,
    o,
    t.x,
    t.y + t.label.Y,
    t.width,
    t.height,
    { fill: "#444444" },
    u
  ), t.type && t.type.text !== "" && (u = i.boundaryFont(), u.fontColor = r, W(i)(
    t.type.text,
    o,
    t.x,
    t.y + t.type.Y,
    t.width,
    t.height,
    { fill: "#444444" },
    u
  )), t.descr && t.descr.text !== "" && (u = i.boundaryFont(), u.fontSize = u.fontSize - 2, u.fontColor = r, W(i)(
    t.descr.text,
    o,
    t.x,
    t.y + t.descr.Y,
    t.width,
    t.height,
    { fill: "#444444" },
    u
  ));
}, C0 = function(e, t, i) {
  var y;
  let o = t.bgColor ? t.bgColor : i[t.typeC4Shape.text + "_bg_color"], l = t.borderColor ? t.borderColor : i[t.typeC4Shape.text + "_border_color"], n = t.fontColor ? t.fontColor : "#FFFFFF", r = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAIAAADYYG7QAAACD0lEQVR4Xu2YoU4EMRCGT+4j8Ai8AhaH4QHgAUjQuFMECUgMIUgwJAgMhgQsAYUiJCiQIBBY+EITsjfTdme6V24v4c8vyGbb+ZjOtN0bNcvjQXmkH83WvYBWto6PLm6v7p7uH1/w2fXD+PBycX1Pv2l3IdDm/vn7x+dXQiAubRzoURa7gRZWd0iGRIiJbOnhnfYBQZNJjNbuyY2eJG8fkDE3bbG4ep6MHUAsgYxmE3nVs6VsBWJSGccsOlFPmLIViMzLOB7pCVO2AtHJMohH7Fh6zqitQK7m0rJvAVYgGcEpe//PLdDz65sM4pF9N7ICcXDKIB5Nv6j7tD0NoSdM2QrU9Gg0ewE1LqBhHR3BBdvj2vapnidjHxD/q6vd7Pvhr31AwcY8eXMTXAKECZZJFXuEq27aLgQK5uLMohCenGGuGewOxSjBvYBqeG6B+Nqiblggdjnc+ZXDy+FNFpFzw76O3UBAROuXh6FoiAcf5g9eTvUgzy0nWg6I8cXHRUpg5bOVBCo+KDpFajOf23GgPme7RSQ+lacIENUgJ6gg1k6HjgOlqnLqip4tEuhv0hNEMXUD0clyXE3p6pZA0S2nnvTlXwLJEZWlb7cTQH1+USgTN4VhAenm/wea1OCAOmqo6fE1WCb9WSKBah+rbUWPWAmE2Rvk0ApiB45eOyNAzU8xcTvj8KvkKEoOaIYeHNA3ZuygAvFMUO0AAAAASUVORK5CYII=";
  switch (t.typeC4Shape.text) {
    case "person":
      r = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAIAAADYYG7QAAACD0lEQVR4Xu2YoU4EMRCGT+4j8Ai8AhaH4QHgAUjQuFMECUgMIUgwJAgMhgQsAYUiJCiQIBBY+EITsjfTdme6V24v4c8vyGbb+ZjOtN0bNcvjQXmkH83WvYBWto6PLm6v7p7uH1/w2fXD+PBycX1Pv2l3IdDm/vn7x+dXQiAubRzoURa7gRZWd0iGRIiJbOnhnfYBQZNJjNbuyY2eJG8fkDE3bbG4ep6MHUAsgYxmE3nVs6VsBWJSGccsOlFPmLIViMzLOB7pCVO2AtHJMohH7Fh6zqitQK7m0rJvAVYgGcEpe//PLdDz65sM4pF9N7ICcXDKIB5Nv6j7tD0NoSdM2QrU9Gg0ewE1LqBhHR3BBdvj2vapnidjHxD/q6vd7Pvhr31AwcY8eXMTXAKECZZJFXuEq27aLgQK5uLMohCenGGuGewOxSjBvYBqeG6B+Nqiblggdjnc+ZXDy+FNFpFzw76O3UBAROuXh6FoiAcf5g9eTvUgzy0nWg6I8cXHRUpg5bOVBCo+KDpFajOf23GgPme7RSQ+lacIENUgJ6gg1k6HjgOlqnLqip4tEuhv0hNEMXUD0clyXE3p6pZA0S2nnvTlXwLJEZWlb7cTQH1+USgTN4VhAenm/wea1OCAOmqo6fE1WCb9WSKBah+rbUWPWAmE2Rvk0ApiB45eOyNAzU8xcTvj8KvkKEoOaIYeHNA3ZuygAvFMUO0AAAAASUVORK5CYII=";
      break;
    case "external_person":
      r = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAIAAADYYG7QAAAB6ElEQVR4Xu2YLY+EMBCG9+dWr0aj0Wg0Go1Go0+j8Xdv2uTCvv1gpt0ebHKPuhDaeW4605Z9mJvx4AdXUyTUdd08z+u6flmWZRnHsWkafk9DptAwDPu+f0eAYtu2PEaGWuj5fCIZrBAC2eLBAnRCsEkkxmeaJp7iDJ2QMDdHsLg8SxKFEJaAo8lAXnmuOFIhTMpxxKATebo4UiFknuNo4OniSIXQyRxEA3YsnjGCVEjVXD7yLUAqxBGUyPv/Y4W2beMgGuS7kVQIBycH0fD+oi5pezQETxdHKmQKGk1eQEYldK+jw5GxPfZ9z7Mk0Qnhf1W1m3w//EUn5BDmSZsbR44QQLBEqrBHqOrmSKaQAxdnLArCrxZcM7A7ZKs4ioRq8LFC+NpC3WCBJsvpVw5edm9iEXFuyNfxXAgSwfrFQ1c0iNda8AdejvUgnktOtJQQxmcfFzGglc5WVCj7oDgFqU18boeFSs52CUh8LE8BIVQDT1ABrB0HtgSEYlX5doJnCwv9TXocKCaKbnwhdDKPq4lf3SwU3HLq4V/+WYhHVMa/3b4IlfyikAduCkcBc7mQ3/z/Qq/cTuikhkzB12Ae/mcJC9U+Vo8Ej1gWAtgbeGgFsAMHr50BIWOLCbezvhpBFUdY6EJuJ/QDW0XoMX60zZ0AAAAASUVORK5CYII=";
      break;
  }
  const a = e.append("g");
  a.attr("class", "person-man");
  const s = Oe();
  switch (t.typeC4Shape.text) {
    case "person":
    case "external_person":
    case "system":
    case "external_system":
    case "container":
    case "external_container":
    case "component":
    case "external_component":
      s.x = t.x, s.y = t.y, s.fill = o, s.width = t.width, s.height = t.height, s.stroke = l, s.rx = 2.5, s.ry = 2.5, s.attrs = { "stroke-width": 0.5 }, de(a, s);
      break;
    case "system_db":
    case "external_system_db":
    case "container_db":
    case "external_container_db":
    case "component_db":
    case "external_component_db":
      a.append("path").attr("fill", o).attr("stroke-width", "0.5").attr("stroke", l).attr(
        "d",
        "Mstartx,startyc0,-10 half,-10 half,-10c0,0 half,0 half,10l0,heightc0,10 -half,10 -half,10c0,0 -half,0 -half,-10l0,-height".replaceAll("startx", t.x).replaceAll("starty", t.y).replaceAll("half", t.width / 2).replaceAll("height", t.height)
      ), a.append("path").attr("fill", "none").attr("stroke-width", "0.5").attr("stroke", l).attr(
        "d",
        "Mstartx,startyc0,10 half,10 half,10c0,0 half,0 half,-10".replaceAll("startx", t.x).replaceAll("starty", t.y).replaceAll("half", t.width / 2)
      );
      break;
    case "system_queue":
    case "external_system_queue":
    case "container_queue":
    case "external_container_queue":
    case "component_queue":
    case "external_component_queue":
      a.append("path").attr("fill", o).attr("stroke-width", "0.5").attr("stroke", l).attr(
        "d",
        "Mstartx,startylwidth,0c5,0 5,half 5,halfc0,0 0,half -5,halfl-width,0c-5,0 -5,-half -5,-halfc0,0 0,-half 5,-half".replaceAll("startx", t.x).replaceAll("starty", t.y).replaceAll("width", t.width).replaceAll("half", t.height / 2)
      ), a.append("path").attr("fill", "none").attr("stroke-width", "0.5").attr("stroke", l).attr(
        "d",
        "Mstartx,startyc-5,0 -5,half -5,halfc0,half 5,half 5,half".replaceAll("startx", t.x + t.width).replaceAll("starty", t.y).replaceAll("half", t.height / 2)
      );
      break;
  }
  let u = L0(i, t.typeC4Shape.text);
  switch (a.append("text").attr("fill", n).attr("font-family", u.fontFamily).attr("font-size", u.fontSize - 2).attr("font-style", "italic").attr("lengthAdjust", "spacing").attr("textLength", t.typeC4Shape.width).attr("x", t.x + t.width / 2 - t.typeC4Shape.width / 2).attr("y", t.y + t.typeC4Shape.Y).text("<<" + t.typeC4Shape.text + ">>"), t.typeC4Shape.text) {
    case "person":
    case "external_person":
      Te(
        a,
        48,
        48,
        t.x + t.width / 2 - 24,
        t.y + t.image.Y,
        r
      );
      break;
  }
  let d = i[t.typeC4Shape.text + "Font"]();
  return d.fontWeight = "bold", d.fontSize = d.fontSize + 2, d.fontColor = n, W(i)(
    t.label.text,
    a,
    t.x,
    t.y + t.label.Y,
    t.width,
    t.height,
    { fill: n },
    d
  ), d = i[t.typeC4Shape.text + "Font"](), d.fontColor = n, t.techn && ((y = t.techn) == null ? void 0 : y.text) !== "" ? W(i)(
    t.techn.text,
    a,
    t.x,
    t.y + t.techn.Y,
    t.width,
    t.height,
    { fill: n, "font-style": "italic" },
    d
  ) : t.type && t.type.text !== "" && W(i)(
    t.type.text,
    a,
    t.x,
    t.y + t.type.Y,
    t.width,
    t.height,
    { fill: n, "font-style": "italic" },
    d
  ), t.descr && t.descr.text !== "" && (d = i.personFont(), d.fontColor = n, W(i)(
    t.descr.text,
    a,
    t.x,
    t.y + t.descr.Y,
    t.width,
    t.height,
    { fill: n },
    d
  )), t.height;
}, w0 = function(e) {
  e.append("defs").append("symbol").attr("id", "database").attr("fill-rule", "evenodd").attr("clip-rule", "evenodd").append("path").attr("transform", "scale(.5)").attr(
    "d",
    "M12.258.001l.256.004.255.005.253.008.251.01.249.012.247.015.246.016.242.019.241.02.239.023.236.024.233.027.231.028.229.031.225.032.223.034.22.036.217.038.214.04.211.041.208.043.205.045.201.046.198.048.194.05.191.051.187.053.183.054.18.056.175.057.172.059.168.06.163.061.16.063.155.064.15.066.074.033.073.033.071.034.07.034.069.035.068.035.067.035.066.035.064.036.064.036.062.036.06.036.06.037.058.037.058.037.055.038.055.038.053.038.052.038.051.039.05.039.048.039.047.039.045.04.044.04.043.04.041.04.04.041.039.041.037.041.036.041.034.041.033.042.032.042.03.042.029.042.027.042.026.043.024.043.023.043.021.043.02.043.018.044.017.043.015.044.013.044.012.044.011.045.009.044.007.045.006.045.004.045.002.045.001.045v17l-.001.045-.002.045-.004.045-.006.045-.007.045-.009.044-.011.045-.012.044-.013.044-.015.044-.017.043-.018.044-.02.043-.021.043-.023.043-.024.043-.026.043-.027.042-.029.042-.03.042-.032.042-.033.042-.034.041-.036.041-.037.041-.039.041-.04.041-.041.04-.043.04-.044.04-.045.04-.047.039-.048.039-.05.039-.051.039-.052.038-.053.038-.055.038-.055.038-.058.037-.058.037-.06.037-.06.036-.062.036-.064.036-.064.036-.066.035-.067.035-.068.035-.069.035-.07.034-.071.034-.073.033-.074.033-.15.066-.155.064-.16.063-.163.061-.168.06-.172.059-.175.057-.18.056-.183.054-.187.053-.191.051-.194.05-.198.048-.201.046-.205.045-.208.043-.211.041-.214.04-.217.038-.22.036-.223.034-.225.032-.229.031-.231.028-.233.027-.236.024-.239.023-.241.02-.242.019-.246.016-.247.015-.249.012-.251.01-.253.008-.255.005-.256.004-.258.001-.258-.001-.256-.004-.255-.005-.253-.008-.251-.01-.249-.012-.247-.015-.245-.016-.243-.019-.241-.02-.238-.023-.236-.024-.234-.027-.231-.028-.228-.031-.226-.032-.223-.034-.22-.036-.217-.038-.214-.04-.211-.041-.208-.043-.204-.045-.201-.046-.198-.048-.195-.05-.19-.051-.187-.053-.184-.054-.179-.056-.176-.057-.172-.059-.167-.06-.164-.061-.159-.063-.155-.064-.151-.066-.074-.033-.072-.033-.072-.034-.07-.034-.069-.035-.068-.035-.067-.035-.066-.035-.064-.036-.063-.036-.062-.036-.061-.036-.06-.037-.058-.037-.057-.037-.056-.038-.055-.038-.053-.038-.052-.038-.051-.039-.049-.039-.049-.039-.046-.039-.046-.04-.044-.04-.043-.04-.041-.04-.04-.041-.039-.041-.037-.041-.036-.041-.034-.041-.033-.042-.032-.042-.03-.042-.029-.042-.027-.042-.026-.043-.024-.043-.023-.043-.021-.043-.02-.043-.018-.044-.017-.043-.015-.044-.013-.044-.012-.044-.011-.045-.009-.044-.007-.045-.006-.045-.004-.045-.002-.045-.001-.045v-17l.001-.045.002-.045.004-.045.006-.045.007-.045.009-.044.011-.045.012-.044.013-.044.015-.044.017-.043.018-.044.02-.043.021-.043.023-.043.024-.043.026-.043.027-.042.029-.042.03-.042.032-.042.033-.042.034-.041.036-.041.037-.041.039-.041.04-.041.041-.04.043-.04.044-.04.046-.04.046-.039.049-.039.049-.039.051-.039.052-.038.053-.038.055-.038.056-.038.057-.037.058-.037.06-.037.061-.036.062-.036.063-.036.064-.036.066-.035.067-.035.068-.035.069-.035.07-.034.072-.034.072-.033.074-.033.151-.066.155-.064.159-.063.164-.061.167-.06.172-.059.176-.057.179-.056.184-.054.187-.053.19-.051.195-.05.198-.048.201-.046.204-.045.208-.043.211-.041.214-.04.217-.038.22-.036.223-.034.226-.032.228-.031.231-.028.234-.027.236-.024.238-.023.241-.02.243-.019.245-.016.247-.015.249-.012.251-.01.253-.008.255-.005.256-.004.258-.001.258.001zm-9.258 20.499v.01l.001.021.003.021.004.022.005.021.006.022.007.022.009.023.01.022.011.023.012.023.013.023.015.023.016.024.017.023.018.024.019.024.021.024.022.025.023.024.024.025.052.049.056.05.061.051.066.051.07.051.075.051.079.052.084.052.088.052.092.052.097.052.102.051.105.052.11.052.114.051.119.051.123.051.127.05.131.05.135.05.139.048.144.049.147.047.152.047.155.047.16.045.163.045.167.043.171.043.176.041.178.041.183.039.187.039.19.037.194.035.197.035.202.033.204.031.209.03.212.029.216.027.219.025.222.024.226.021.23.02.233.018.236.016.24.015.243.012.246.01.249.008.253.005.256.004.259.001.26-.001.257-.004.254-.005.25-.008.247-.011.244-.012.241-.014.237-.016.233-.018.231-.021.226-.021.224-.024.22-.026.216-.027.212-.028.21-.031.205-.031.202-.034.198-.034.194-.036.191-.037.187-.039.183-.04.179-.04.175-.042.172-.043.168-.044.163-.045.16-.046.155-.046.152-.047.148-.048.143-.049.139-.049.136-.05.131-.05.126-.05.123-.051.118-.052.114-.051.11-.052.106-.052.101-.052.096-.052.092-.052.088-.053.083-.051.079-.052.074-.052.07-.051.065-.051.06-.051.056-.05.051-.05.023-.024.023-.025.021-.024.02-.024.019-.024.018-.024.017-.024.015-.023.014-.024.013-.023.012-.023.01-.023.01-.022.008-.022.006-.022.006-.022.004-.022.004-.021.001-.021.001-.021v-4.127l-.077.055-.08.053-.083.054-.085.053-.087.052-.09.052-.093.051-.095.05-.097.05-.1.049-.102.049-.105.048-.106.047-.109.047-.111.046-.114.045-.115.045-.118.044-.12.043-.122.042-.124.042-.126.041-.128.04-.13.04-.132.038-.134.038-.135.037-.138.037-.139.035-.142.035-.143.034-.144.033-.147.032-.148.031-.15.03-.151.03-.153.029-.154.027-.156.027-.158.026-.159.025-.161.024-.162.023-.163.022-.165.021-.166.02-.167.019-.169.018-.169.017-.171.016-.173.015-.173.014-.175.013-.175.012-.177.011-.178.01-.179.008-.179.008-.181.006-.182.005-.182.004-.184.003-.184.002h-.37l-.184-.002-.184-.003-.182-.004-.182-.005-.181-.006-.179-.008-.179-.008-.178-.01-.176-.011-.176-.012-.175-.013-.173-.014-.172-.015-.171-.016-.17-.017-.169-.018-.167-.019-.166-.02-.165-.021-.163-.022-.162-.023-.161-.024-.159-.025-.157-.026-.156-.027-.155-.027-.153-.029-.151-.03-.15-.03-.148-.031-.146-.032-.145-.033-.143-.034-.141-.035-.14-.035-.137-.037-.136-.037-.134-.038-.132-.038-.13-.04-.128-.04-.126-.041-.124-.042-.122-.042-.12-.044-.117-.043-.116-.045-.113-.045-.112-.046-.109-.047-.106-.047-.105-.048-.102-.049-.1-.049-.097-.05-.095-.05-.093-.052-.09-.051-.087-.052-.085-.053-.083-.054-.08-.054-.077-.054v4.127zm0-5.654v.011l.001.021.003.021.004.021.005.022.006.022.007.022.009.022.01.022.011.023.012.023.013.023.015.024.016.023.017.024.018.024.019.024.021.024.022.024.023.025.024.024.052.05.056.05.061.05.066.051.07.051.075.052.079.051.084.052.088.052.092.052.097.052.102.052.105.052.11.051.114.051.119.052.123.05.127.051.131.05.135.049.139.049.144.048.147.048.152.047.155.046.16.045.163.045.167.044.171.042.176.042.178.04.183.04.187.038.19.037.194.036.197.034.202.033.204.032.209.03.212.028.216.027.219.025.222.024.226.022.23.02.233.018.236.016.24.014.243.012.246.01.249.008.253.006.256.003.259.001.26-.001.257-.003.254-.006.25-.008.247-.01.244-.012.241-.015.237-.016.233-.018.231-.02.226-.022.224-.024.22-.025.216-.027.212-.029.21-.03.205-.032.202-.033.198-.035.194-.036.191-.037.187-.039.183-.039.179-.041.175-.042.172-.043.168-.044.163-.045.16-.045.155-.047.152-.047.148-.048.143-.048.139-.05.136-.049.131-.05.126-.051.123-.051.118-.051.114-.052.11-.052.106-.052.101-.052.096-.052.092-.052.088-.052.083-.052.079-.052.074-.051.07-.052.065-.051.06-.05.056-.051.051-.049.023-.025.023-.024.021-.025.02-.024.019-.024.018-.024.017-.024.015-.023.014-.023.013-.024.012-.022.01-.023.01-.023.008-.022.006-.022.006-.022.004-.021.004-.022.001-.021.001-.021v-4.139l-.077.054-.08.054-.083.054-.085.052-.087.053-.09.051-.093.051-.095.051-.097.05-.1.049-.102.049-.105.048-.106.047-.109.047-.111.046-.114.045-.115.044-.118.044-.12.044-.122.042-.124.042-.126.041-.128.04-.13.039-.132.039-.134.038-.135.037-.138.036-.139.036-.142.035-.143.033-.144.033-.147.033-.148.031-.15.03-.151.03-.153.028-.154.028-.156.027-.158.026-.159.025-.161.024-.162.023-.163.022-.165.021-.166.02-.167.019-.169.018-.169.017-.171.016-.173.015-.173.014-.175.013-.175.012-.177.011-.178.009-.179.009-.179.007-.181.007-.182.005-.182.004-.184.003-.184.002h-.37l-.184-.002-.184-.003-.182-.004-.182-.005-.181-.007-.179-.007-.179-.009-.178-.009-.176-.011-.176-.012-.175-.013-.173-.014-.172-.015-.171-.016-.17-.017-.169-.018-.167-.019-.166-.02-.165-.021-.163-.022-.162-.023-.161-.024-.159-.025-.157-.026-.156-.027-.155-.028-.153-.028-.151-.03-.15-.03-.148-.031-.146-.033-.145-.033-.143-.033-.141-.035-.14-.036-.137-.036-.136-.037-.134-.038-.132-.039-.13-.039-.128-.04-.126-.041-.124-.042-.122-.043-.12-.043-.117-.044-.116-.044-.113-.046-.112-.046-.109-.046-.106-.047-.105-.048-.102-.049-.1-.049-.097-.05-.095-.051-.093-.051-.09-.051-.087-.053-.085-.052-.083-.054-.08-.054-.077-.054v4.139zm0-5.666v.011l.001.02.003.022.004.021.005.022.006.021.007.022.009.023.01.022.011.023.012.023.013.023.015.023.016.024.017.024.018.023.019.024.021.025.022.024.023.024.024.025.052.05.056.05.061.05.066.051.07.051.075.052.079.051.084.052.088.052.092.052.097.052.102.052.105.051.11.052.114.051.119.051.123.051.127.05.131.05.135.05.139.049.144.048.147.048.152.047.155.046.16.045.163.045.167.043.171.043.176.042.178.04.183.04.187.038.19.037.194.036.197.034.202.033.204.032.209.03.212.028.216.027.219.025.222.024.226.021.23.02.233.018.236.017.24.014.243.012.246.01.249.008.253.006.256.003.259.001.26-.001.257-.003.254-.006.25-.008.247-.01.244-.013.241-.014.237-.016.233-.018.231-.02.226-.022.224-.024.22-.025.216-.027.212-.029.21-.03.205-.032.202-.033.198-.035.194-.036.191-.037.187-.039.183-.039.179-.041.175-.042.172-.043.168-.044.163-.045.16-.045.155-.047.152-.047.148-.048.143-.049.139-.049.136-.049.131-.051.126-.05.123-.051.118-.052.114-.051.11-.052.106-.052.101-.052.096-.052.092-.052.088-.052.083-.052.079-.052.074-.052.07-.051.065-.051.06-.051.056-.05.051-.049.023-.025.023-.025.021-.024.02-.024.019-.024.018-.024.017-.024.015-.023.014-.024.013-.023.012-.023.01-.022.01-.023.008-.022.006-.022.006-.022.004-.022.004-.021.001-.021.001-.021v-4.153l-.077.054-.08.054-.083.053-.085.053-.087.053-.09.051-.093.051-.095.051-.097.05-.1.049-.102.048-.105.048-.106.048-.109.046-.111.046-.114.046-.115.044-.118.044-.12.043-.122.043-.124.042-.126.041-.128.04-.13.039-.132.039-.134.038-.135.037-.138.036-.139.036-.142.034-.143.034-.144.033-.147.032-.148.032-.15.03-.151.03-.153.028-.154.028-.156.027-.158.026-.159.024-.161.024-.162.023-.163.023-.165.021-.166.02-.167.019-.169.018-.169.017-.171.016-.173.015-.173.014-.175.013-.175.012-.177.01-.178.01-.179.009-.179.007-.181.006-.182.006-.182.004-.184.003-.184.001-.185.001-.185-.001-.184-.001-.184-.003-.182-.004-.182-.006-.181-.006-.179-.007-.179-.009-.178-.01-.176-.01-.176-.012-.175-.013-.173-.014-.172-.015-.171-.016-.17-.017-.169-.018-.167-.019-.166-.02-.165-.021-.163-.023-.162-.023-.161-.024-.159-.024-.157-.026-.156-.027-.155-.028-.153-.028-.151-.03-.15-.03-.148-.032-.146-.032-.145-.033-.143-.034-.141-.034-.14-.036-.137-.036-.136-.037-.134-.038-.132-.039-.13-.039-.128-.041-.126-.041-.124-.041-.122-.043-.12-.043-.117-.044-.116-.044-.113-.046-.112-.046-.109-.046-.106-.048-.105-.048-.102-.048-.1-.05-.097-.049-.095-.051-.093-.051-.09-.052-.087-.052-.085-.053-.083-.053-.08-.054-.077-.054v4.153zm8.74-8.179l-.257.004-.254.005-.25.008-.247.011-.244.012-.241.014-.237.016-.233.018-.231.021-.226.022-.224.023-.22.026-.216.027-.212.028-.21.031-.205.032-.202.033-.198.034-.194.036-.191.038-.187.038-.183.04-.179.041-.175.042-.172.043-.168.043-.163.045-.16.046-.155.046-.152.048-.148.048-.143.048-.139.049-.136.05-.131.05-.126.051-.123.051-.118.051-.114.052-.11.052-.106.052-.101.052-.096.052-.092.052-.088.052-.083.052-.079.052-.074.051-.07.052-.065.051-.06.05-.056.05-.051.05-.023.025-.023.024-.021.024-.02.025-.019.024-.018.024-.017.023-.015.024-.014.023-.013.023-.012.023-.01.023-.01.022-.008.022-.006.023-.006.021-.004.022-.004.021-.001.021-.001.021.001.021.001.021.004.021.004.022.006.021.006.023.008.022.01.022.01.023.012.023.013.023.014.023.015.024.017.023.018.024.019.024.02.025.021.024.023.024.023.025.051.05.056.05.06.05.065.051.07.052.074.051.079.052.083.052.088.052.092.052.096.052.101.052.106.052.11.052.114.052.118.051.123.051.126.051.131.05.136.05.139.049.143.048.148.048.152.048.155.046.16.046.163.045.168.043.172.043.175.042.179.041.183.04.187.038.191.038.194.036.198.034.202.033.205.032.21.031.212.028.216.027.22.026.224.023.226.022.231.021.233.018.237.016.241.014.244.012.247.011.25.008.254.005.257.004.26.001.26-.001.257-.004.254-.005.25-.008.247-.011.244-.012.241-.014.237-.016.233-.018.231-.021.226-.022.224-.023.22-.026.216-.027.212-.028.21-.031.205-.032.202-.033.198-.034.194-.036.191-.038.187-.038.183-.04.179-.041.175-.042.172-.043.168-.043.163-.045.16-.046.155-.046.152-.048.148-.048.143-.048.139-.049.136-.05.131-.05.126-.051.123-.051.118-.051.114-.052.11-.052.106-.052.101-.052.096-.052.092-.052.088-.052.083-.052.079-.052.074-.051.07-.052.065-.051.06-.05.056-.05.051-.05.023-.025.023-.024.021-.024.02-.025.019-.024.018-.024.017-.023.015-.024.014-.023.013-.023.012-.023.01-.023.01-.022.008-.022.006-.023.006-.021.004-.022.004-.021.001-.021.001-.021-.001-.021-.001-.021-.004-.021-.004-.022-.006-.021-.006-.023-.008-.022-.01-.022-.01-.023-.012-.023-.013-.023-.014-.023-.015-.024-.017-.023-.018-.024-.019-.024-.02-.025-.021-.024-.023-.024-.023-.025-.051-.05-.056-.05-.06-.05-.065-.051-.07-.052-.074-.051-.079-.052-.083-.052-.088-.052-.092-.052-.096-.052-.101-.052-.106-.052-.11-.052-.114-.052-.118-.051-.123-.051-.126-.051-.131-.05-.136-.05-.139-.049-.143-.048-.148-.048-.152-.048-.155-.046-.16-.046-.163-.045-.168-.043-.172-.043-.175-.042-.179-.041-.183-.04-.187-.038-.191-.038-.194-.036-.198-.034-.202-.033-.205-.032-.21-.031-.212-.028-.216-.027-.22-.026-.224-.023-.226-.022-.231-.021-.233-.018-.237-.016-.241-.014-.244-.012-.247-.011-.25-.008-.254-.005-.257-.004-.26-.001-.26.001z"
  );
}, T0 = function(e) {
  e.append("defs").append("symbol").attr("id", "computer").attr("width", "24").attr("height", "24").append("path").attr("transform", "scale(.5)").attr(
    "d",
    "M2 2v13h20v-13h-20zm18 11h-16v-9h16v9zm-10.228 6l.466-1h3.524l.467 1h-4.457zm14.228 3h-24l2-6h2.104l-1.33 4h18.45l-1.297-4h2.073l2 6zm-5-10h-14v-7h14v7z"
  );
}, O0 = function(e) {
  e.append("defs").append("symbol").attr("id", "clock").attr("width", "24").attr("height", "24").append("path").attr("transform", "scale(.5)").attr(
    "d",
    "M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm5.848 12.459c.202.038.202.333.001.372-1.907.361-6.045 1.111-6.547 1.111-.719 0-1.301-.582-1.301-1.301 0-.512.77-5.447 1.125-7.445.034-.192.312-.181.343.014l.985 6.238 5.394 1.011z"
  );
}, R0 = function(e) {
  e.append("defs").append("marker").attr("id", "arrowhead").attr("refX", 9).attr("refY", 5).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 12).attr("markerHeight", 12).attr("orient", "auto").append("path").attr("d", "M 0 0 L 10 5 L 0 10 z");
}, S0 = function(e) {
  e.append("defs").append("marker").attr("id", "arrowend").attr("refX", 1).attr("refY", 5).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 12).attr("markerHeight", 12).attr("orient", "auto").append("path").attr("d", "M 10 0 L 0 5 L 10 10 z");
}, D0 = function(e) {
  e.append("defs").append("marker").attr("id", "filled-head").attr("refX", 18).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L14,7 L9,1 Z");
}, P0 = function(e) {
  e.append("defs").append("marker").attr("id", "sequencenumber").attr("refX", 15).attr("refY", 15).attr("markerWidth", 60).attr("markerHeight", 40).attr("orient", "auto").append("circle").attr("cx", 15).attr("cy", 15).attr("r", 6);
}, M0 = function(e) {
  const i = e.append("defs").append("marker").attr("id", "crosshead").attr("markerWidth", 15).attr("markerHeight", 8).attr("orient", "auto").attr("refX", 16).attr("refY", 4);
  i.append("path").attr("fill", "black").attr("stroke", "#000000").style("stroke-dasharray", "0, 0").attr("stroke-width", "1px").attr("d", "M 9,2 V 6 L16,4 Z"), i.append("path").attr("fill", "none").attr("stroke", "#000000").style("stroke-dasharray", "0, 0").attr("stroke-width", "1px").attr("d", "M 0,1 L 6,7 M 6,1 L 0,7");
}, Oe = function() {
  return {
    x: 0,
    y: 0,
    fill: "#EDF2AE",
    stroke: "#666",
    width: 100,
    anchor: "start",
    height: 100,
    rx: 0,
    ry: 0
  };
}, L0 = (e, t) => ({
  fontFamily: e[t + "FontFamily"],
  fontSize: e[t + "FontSize"],
  fontWeight: e[t + "FontWeight"]
}), W = function() {
  function e(l, n, r, a, s, u, d) {
    const y = n.append("text").attr("x", r + s / 2).attr("y", a + u / 2 + 5).style("text-anchor", "middle").text(l);
    o(y, d);
  }
  function t(l, n, r, a, s, u, d, y) {
    const { fontSize: p, fontFamily: C, fontWeight: T } = y, R = l.split(le.lineBreakRegex);
    for (let D = 0; D < R.length; D++) {
      const L = D * p - p * (R.length - 1) / 2, Y = n.append("text").attr("x", r + s / 2).attr("y", a).style("text-anchor", "middle").attr("dominant-baseline", "middle").style("font-size", p).style("font-weight", T).style("font-family", C);
      Y.append("tspan").attr("dy", L).text(R[D]).attr("alignment-baseline", "mathematical"), o(Y, d);
    }
  }
  function i(l, n, r, a, s, u, d, y) {
    const p = n.append("switch"), T = p.append("foreignObject").attr("x", r).attr("y", a).attr("width", s).attr("height", u).append("xhtml:div").style("display", "table").style("height", "100%").style("width", "100%");
    T.append("div").style("display", "table-cell").style("text-align", "center").style("vertical-align", "middle").text(l), t(l, p, r, a, s, u, d, y), o(T, d);
  }
  function o(l, n) {
    for (const r in n)
      n.hasOwnProperty(r) && l.attr(r, n[r]);
  }
  return function(l) {
    return l.textPlacement === "fo" ? i : l.textPlacement === "old" ? e : t;
  };
}(), U = {
  drawRect: de,
  drawBoundary: A0,
  drawC4Shape: C0,
  drawRels: k0,
  drawImage: Te,
  insertArrowHead: R0,
  insertArrowEnd: S0,
  insertArrowFilledHead: D0,
  insertDynamicNumber: P0,
  insertArrowCrossHead: M0,
  insertDatabaseIcon: w0,
  insertComputerIcon: T0,
  insertClockIcon: O0,
  getNoteRect: Oe,
  sanitizeUrl: ke
  // TODO why is this exported?
};
let Jt = 0, Zt = 0, Re = 4, oe = 2;
qt.yy = we;
let b = {};
class Se {
  constructor(t) {
    this.name = "", this.data = {}, this.data.startx = void 0, this.data.stopx = void 0, this.data.starty = void 0, this.data.stopy = void 0, this.data.widthLimit = void 0, this.nextData = {}, this.nextData.startx = void 0, this.nextData.stopx = void 0, this.nextData.starty = void 0, this.nextData.stopy = void 0, this.nextData.cnt = 0, ce(t.db.getConfig());
  }
  setData(t, i, o, l) {
    this.nextData.startx = this.data.startx = t, this.nextData.stopx = this.data.stopx = i, this.nextData.starty = this.data.starty = o, this.nextData.stopy = this.data.stopy = l;
  }
  updateVal(t, i, o, l) {
    t[i] === void 0 ? t[i] = o : t[i] = l(o, t[i]);
  }
  insert(t) {
    this.nextData.cnt = this.nextData.cnt + 1;
    let i = this.nextData.startx === this.nextData.stopx ? this.nextData.stopx + t.margin : this.nextData.stopx + t.margin * 2, o = i + t.width, l = this.nextData.starty + t.margin * 2, n = l + t.height;
    (i >= this.data.widthLimit || o >= this.data.widthLimit || this.nextData.cnt > Re) && (i = this.nextData.startx + t.margin + b.nextLinePaddingX, l = this.nextData.stopy + t.margin * 2, this.nextData.stopx = o = i + t.width, this.nextData.starty = this.nextData.stopy, this.nextData.stopy = n = l + t.height, this.nextData.cnt = 1), t.x = i, t.y = l, this.updateVal(this.data, "startx", i, Math.min), this.updateVal(this.data, "starty", l, Math.min), this.updateVal(this.data, "stopx", o, Math.max), this.updateVal(this.data, "stopy", n, Math.max), this.updateVal(this.nextData, "startx", i, Math.min), this.updateVal(this.nextData, "starty", l, Math.min), this.updateVal(this.nextData, "stopx", o, Math.max), this.updateVal(this.nextData, "stopy", n, Math.max);
  }
  init(t) {
    this.name = "", this.data = {
      startx: void 0,
      stopx: void 0,
      starty: void 0,
      stopy: void 0,
      widthLimit: void 0
    }, this.nextData = {
      startx: void 0,
      stopx: void 0,
      starty: void 0,
      stopy: void 0,
      cnt: 0
    }, ce(t.db.getConfig());
  }
  bumpLastMargin(t) {
    this.data.stopx += t, this.data.stopy += t;
  }
}
const ce = function(e) {
  je(b, e), e.fontFamily && (b.personFontFamily = b.systemFontFamily = b.messageFontFamily = e.fontFamily), e.fontSize && (b.personFontSize = b.systemFontSize = b.messageFontSize = e.fontSize), e.fontWeight && (b.personFontWeight = b.systemFontWeight = b.messageFontWeight = e.fontWeight);
}, jt = (e, t) => ({
  fontFamily: e[t + "FontFamily"],
  fontSize: e[t + "FontSize"],
  fontWeight: e[t + "FontWeight"]
}), Ht = (e) => ({
  fontFamily: e.boundaryFontFamily,
  fontSize: e.boundaryFontSize,
  fontWeight: e.boundaryFontWeight
}), N0 = (e) => ({
  fontFamily: e.messageFontFamily,
  fontSize: e.messageFontSize,
  fontWeight: e.messageFontWeight
});
function I(e, t, i, o, l) {
  if (!t[e].width)
    if (i)
      t[e].text = We(t[e].text, l, o), t[e].textLines = t[e].text.split(le.lineBreakRegex).length, t[e].width = l, t[e].height = xe(t[e].text, o);
    else {
      let n = t[e].text.split(le.lineBreakRegex);
      t[e].textLines = n.length;
      let r = 0;
      t[e].height = 0, t[e].width = 0;
      for (const a of n)
        t[e].width = Math.max(
          Yt(a, o),
          t[e].width
        ), r = xe(a, o), t[e].height = t[e].height + r;
    }
}
const De = function(e, t, i) {
  t.x = i.data.startx, t.y = i.data.starty, t.width = i.data.stopx - i.data.startx, t.height = i.data.stopy - i.data.starty, t.label.y = b.c4ShapeMargin - 35;
  let o = t.wrap && b.wrap, l = Ht(b);
  l.fontSize = l.fontSize + 2, l.fontWeight = "bold";
  let n = Yt(t.label.text, l);
  I("label", t, o, l, n), U.drawBoundary(e, t, b);
}, Pe = function(e, t, i, o) {
  let l = 0;
  for (const n of o) {
    l = 0;
    const r = i[n];
    let a = jt(b, r.typeC4Shape.text);
    switch (a.fontSize = a.fontSize - 2, r.typeC4Shape.width = Yt(
      "<<" + r.typeC4Shape.text + ">>",
      a
    ), r.typeC4Shape.height = a.fontSize + 2, r.typeC4Shape.Y = b.c4ShapePadding, l = r.typeC4Shape.Y + r.typeC4Shape.height - 4, r.image = { width: 0, height: 0, Y: 0 }, r.typeC4Shape.text) {
      case "person":
      case "external_person":
        r.image.width = 48, r.image.height = 48, r.image.Y = l, l = r.image.Y + r.image.height;
        break;
    }
    r.sprite && (r.image.width = 48, r.image.height = 48, r.image.Y = l, l = r.image.Y + r.image.height);
    let s = r.wrap && b.wrap, u = b.width - b.c4ShapePadding * 2, d = jt(b, r.typeC4Shape.text);
    if (d.fontSize = d.fontSize + 2, d.fontWeight = "bold", I("label", r, s, d, u), r.label.Y = l + 8, l = r.label.Y + r.label.height, r.type && r.type.text !== "") {
      r.type.text = "[" + r.type.text + "]";
      let C = jt(b, r.typeC4Shape.text);
      I("type", r, s, C, u), r.type.Y = l + 5, l = r.type.Y + r.type.height;
    } else if (r.techn && r.techn.text !== "") {
      r.techn.text = "[" + r.techn.text + "]";
      let C = jt(b, r.techn.text);
      I("techn", r, s, C, u), r.techn.Y = l + 5, l = r.techn.Y + r.techn.height;
    }
    let y = l, p = r.label.width;
    if (r.descr && r.descr.text !== "") {
      let C = jt(b, r.typeC4Shape.text);
      I("descr", r, s, C, u), r.descr.Y = l + 20, l = r.descr.Y + r.descr.height, p = Math.max(r.label.width, r.descr.width), y = l - r.descr.textLines * 5;
    }
    p = p + b.c4ShapePadding, r.width = Math.max(r.width || b.width, p, b.width), r.height = Math.max(r.height || b.height, y, b.height), r.margin = r.margin || b.c4ShapeMargin, e.insert(r), U.drawC4Shape(t, r, b);
  }
  e.bumpLastMargin(b.c4ShapeMargin);
};
class B {
  constructor(t, i) {
    this.x = t, this.y = i;
  }
}
let me = function(e, t) {
  let i = e.x, o = e.y, l = t.x, n = t.y, r = i + e.width / 2, a = o + e.height / 2, s = Math.abs(i - l), u = Math.abs(o - n), d = u / s, y = e.height / e.width, p = null;
  return o == n && i < l ? p = new B(i + e.width, a) : o == n && i > l ? p = new B(i, a) : i == l && o < n ? p = new B(r, o + e.height) : i == l && o > n && (p = new B(r, o)), i > l && o < n ? y >= d ? p = new B(i, a + d * e.width / 2) : p = new B(
    r - s / u * e.height / 2,
    o + e.height
  ) : i < l && o < n ? y >= d ? p = new B(i + e.width, a + d * e.width / 2) : p = new B(
    r + s / u * e.height / 2,
    o + e.height
  ) : i < l && o > n ? y >= d ? p = new B(i + e.width, a - d * e.width / 2) : p = new B(r + e.height / 2 * s / u, o) : i > l && o > n && (y >= d ? p = new B(i, a - e.width / 2 * d) : p = new B(r - e.height / 2 * s / u, o)), p;
}, B0 = function(e, t) {
  let i = { x: 0, y: 0 };
  i.x = t.x + t.width / 2, i.y = t.y + t.height / 2;
  let o = me(e, i);
  i.x = e.x + e.width / 2, i.y = e.y + e.height / 2;
  let l = me(t, i);
  return { startPoint: o, endPoint: l };
};
const Y0 = function(e, t, i, o) {
  let l = 0;
  for (let n of t) {
    l = l + 1;
    let r = n.wrap && b.wrap, a = N0(b);
    o.db.getC4Type() === "C4Dynamic" && (n.label.text = l + ": " + n.label.text);
    let u = Yt(n.label.text, a);
    I("label", n, r, a, u), n.techn && n.techn.text !== "" && (u = Yt(n.techn.text, a), I("techn", n, r, a, u)), n.descr && n.descr.text !== "" && (u = Yt(n.descr.text, a), I("descr", n, r, a, u));
    let d = i(n.from), y = i(n.to), p = B0(d, y);
    n.startPoint = p.startPoint, n.endPoint = p.endPoint;
  }
  U.drawRels(e, t, b);
};
function Me(e, t, i, o, l) {
  let n = new Se(l);
  n.data.widthLimit = i.data.widthLimit / Math.min(oe, o.length);
  for (let [r, a] of o.entries()) {
    let s = 0;
    a.image = { width: 0, height: 0, Y: 0 }, a.sprite && (a.image.width = 48, a.image.height = 48, a.image.Y = s, s = a.image.Y + a.image.height);
    let u = a.wrap && b.wrap, d = Ht(b);
    if (d.fontSize = d.fontSize + 2, d.fontWeight = "bold", I(
      "label",
      a,
      u,
      d,
      n.data.widthLimit
    ), a.label.Y = s + 8, s = a.label.Y + a.label.height, a.type && a.type.text !== "") {
      a.type.text = "[" + a.type.text + "]";
      let T = Ht(b);
      I(
        "type",
        a,
        u,
        T,
        n.data.widthLimit
      ), a.type.Y = s + 5, s = a.type.Y + a.type.height;
    }
    if (a.descr && a.descr.text !== "") {
      let T = Ht(b);
      T.fontSize = T.fontSize - 2, I(
        "descr",
        a,
        u,
        T,
        n.data.widthLimit
      ), a.descr.Y = s + 20, s = a.descr.Y + a.descr.height;
    }
    if (r == 0 || r % oe === 0) {
      let T = i.data.startx + b.diagramMarginX, R = i.data.stopy + b.diagramMarginY + s;
      n.setData(T, T, R, R);
    } else {
      let T = n.data.stopx !== n.data.startx ? n.data.stopx + b.diagramMarginX : n.data.startx, R = n.data.starty;
      n.setData(T, T, R, R);
    }
    n.name = a.alias;
    let y = l.db.getC4ShapeArray(a.alias), p = l.db.getC4ShapeKeys(a.alias);
    p.length > 0 && Pe(
      n,
      e,
      y,
      p
    ), t = a.alias;
    let C = l.db.getBoundarys(t);
    C.length > 0 && Me(
      e,
      t,
      n,
      C,
      l
    ), a.alias !== "global" && De(e, a, n), i.data.stopy = Math.max(
      n.data.stopy + b.c4ShapeMargin,
      i.data.stopy
    ), i.data.stopx = Math.max(
      n.data.stopx + b.c4ShapeMargin,
      i.data.stopx
    ), Jt = Math.max(Jt, i.data.stopx), Zt = Math.max(Zt, i.data.stopy);
  }
}
const I0 = function(e, t, i, o) {
  b = Ut().c4;
  const l = Ut().securityLevel;
  let n;
  l === "sandbox" && (n = Qt("#i" + t));
  const r = l === "sandbox" ? Qt(n.nodes()[0].contentDocument.body) : Qt("body");
  let a = o.db;
  o.db.setWrap(b.wrap), Re = a.getC4ShapeInRow(), oe = a.getC4BoundaryInRow(), _e.debug(`C:${JSON.stringify(b, null, 2)}`);
  const s = l === "sandbox" ? r.select(`[id="${t}"]`) : Qt(`[id="${t}"]`);
  U.insertComputerIcon(s), U.insertDatabaseIcon(s), U.insertClockIcon(s);
  let u = new Se(o);
  u.setData(
    b.diagramMarginX,
    b.diagramMarginX,
    b.diagramMarginY,
    b.diagramMarginY
  ), u.data.widthLimit = screen.availWidth, Jt = b.diagramMarginX, Zt = b.diagramMarginY;
  const d = o.db.getTitle();
  let y = o.db.getBoundarys("");
  Me(s, "", u, y, o), U.insertArrowHead(s), U.insertArrowEnd(s), U.insertArrowCrossHead(s), U.insertArrowFilledHead(s), Y0(s, o.db.getRels(), o.db.getC4Shape, o), u.data.stopx = Jt, u.data.stopy = Zt;
  const p = u.data;
  let T = p.stopy - p.starty + 2 * b.diagramMarginY;
  const D = p.stopx - p.startx + 2 * b.diagramMarginX;
  d && s.append("text").text(d).attr("x", (p.stopx - p.startx) / 2 - 4 * b.diagramMarginX).attr("y", p.starty + b.diagramMarginY), Qe(s, T, D, b.useMaxWidth);
  const L = d ? 60 : 0;
  s.attr(
    "viewBox",
    p.startx - b.diagramMarginX + " -" + (b.diagramMarginY + L) + " " + D + " " + (T + L)
  ), _e.debug("models:", p);
}, Ee = {
  drawPersonOrSystemArray: Pe,
  drawBoundary: De,
  setConf: ce,
  draw: I0
}, V0 = (e) => `.person {
    stroke: ${e.personBorder};
    fill: ${e.personBkg};
  }
`, j0 = V0, H0 = {
  parser: He,
  db: we,
  renderer: Ee,
  styles: j0,
  init: (e) => {
    Ee.setConf(e.c4);
  }
};
export {
  H0 as diagram
};
//# sourceMappingURL=c4Diagram-a7af8508.js.map
