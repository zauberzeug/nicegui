import { g as getConfig, e as common, l as log, f as select } from "./config-b4fa35bb.js";
import { m as mermaidAPI } from "./mermaidAPI-6f22a815.js";
import { s as setAccTitle, g as getAccTitle, d as setDiagramTitle, e as getDiagramTitle, a as getAccDescription, b as setAccDescription, f as clear$1 } from "./commonDb-7f40ab5a.js";
import { c as configureSvgSize } from "./setupGraphViewbox-16a0ba81.js";
import { i as initRange } from "./init-cc95ec8e.js";
import { a as array } from "./array-b7dcf730.js";
import { c as constant } from "./constant-b644328d.js";
import { I as tau } from "./utils-872dfc50.js";
import { d as d3arc } from "./arc-7c943a40.js";
import "./errorRenderer-ebf63d74.js";
class InternMap extends Map {
  constructor(entries, key = keyof) {
    super();
    Object.defineProperties(this, { _intern: { value: /* @__PURE__ */ new Map() }, _key: { value: key } });
    if (entries != null)
      for (const [key2, value] of entries)
        this.set(key2, value);
  }
  get(key) {
    return super.get(intern_get(this, key));
  }
  has(key) {
    return super.has(intern_get(this, key));
  }
  set(key, value) {
    return super.set(intern_set(this, key), value);
  }
  delete(key) {
    return super.delete(intern_delete(this, key));
  }
}
function intern_get({ _intern, _key }, value) {
  const key = _key(value);
  return _intern.has(key) ? _intern.get(key) : value;
}
function intern_set({ _intern, _key }, value) {
  const key = _key(value);
  if (_intern.has(key))
    return _intern.get(key);
  _intern.set(key, value);
  return value;
}
function intern_delete({ _intern, _key }, value) {
  const key = _key(value);
  if (_intern.has(key)) {
    value = _intern.get(key);
    _intern.delete(key);
  }
  return value;
}
function keyof(value) {
  return value !== null && typeof value === "object" ? value.valueOf() : value;
}
const implicit = Symbol("implicit");
function ordinal() {
  var index = new InternMap(), domain = [], range = [], unknown = implicit;
  function scale(d) {
    let i = index.get(d);
    if (i === void 0) {
      if (unknown !== implicit)
        return unknown;
      index.set(d, i = domain.push(d) - 1);
    }
    return range[i % range.length];
  }
  scale.domain = function(_) {
    if (!arguments.length)
      return domain.slice();
    domain = [], index = new InternMap();
    for (const value of _) {
      if (index.has(value))
        continue;
      index.set(value, domain.push(value) - 1);
    }
    return scale;
  };
  scale.range = function(_) {
    return arguments.length ? (range = Array.from(_), scale) : range.slice();
  };
  scale.unknown = function(_) {
    return arguments.length ? (unknown = _, scale) : unknown;
  };
  scale.copy = function() {
    return ordinal(domain, range).unknown(unknown);
  };
  initRange.apply(scale, arguments);
  return scale;
}
function descending(a, b) {
  return b < a ? -1 : b > a ? 1 : b >= a ? 0 : NaN;
}
function identity(d) {
  return d;
}
function d3pie() {
  var value = identity, sortValues = descending, sort = null, startAngle = constant(0), endAngle = constant(tau), padAngle = constant(0);
  function pie(data) {
    var i, n = (data = array(data)).length, j, k, sum = 0, index = new Array(n), arcs = new Array(n), a0 = +startAngle.apply(this, arguments), da = Math.min(tau, Math.max(-tau, endAngle.apply(this, arguments) - a0)), a1, p = Math.min(Math.abs(da) / n, padAngle.apply(this, arguments)), pa = p * (da < 0 ? -1 : 1), v;
    for (i = 0; i < n; ++i) {
      if ((v = arcs[index[i] = i] = +value(data[i], i, data)) > 0) {
        sum += v;
      }
    }
    if (sortValues != null)
      index.sort(function(i2, j2) {
        return sortValues(arcs[i2], arcs[j2]);
      });
    else if (sort != null)
      index.sort(function(i2, j2) {
        return sort(data[i2], data[j2]);
      });
    for (i = 0, k = sum ? (da - n * pa) / sum : 0; i < n; ++i, a0 = a1) {
      j = index[i], v = arcs[j], a1 = a0 + (v > 0 ? v * k : 0) + pa, arcs[j] = {
        data: data[j],
        index: i,
        value: v,
        startAngle: a0,
        endAngle: a1,
        padAngle: p
      };
    }
    return arcs;
  }
  pie.value = function(_) {
    return arguments.length ? (value = typeof _ === "function" ? _ : constant(+_), pie) : value;
  };
  pie.sortValues = function(_) {
    return arguments.length ? (sortValues = _, sort = null, pie) : sortValues;
  };
  pie.sort = function(_) {
    return arguments.length ? (sort = _, sortValues = null, pie) : sort;
  };
  pie.startAngle = function(_) {
    return arguments.length ? (startAngle = typeof _ === "function" ? _ : constant(+_), pie) : startAngle;
  };
  pie.endAngle = function(_) {
    return arguments.length ? (endAngle = typeof _ === "function" ? _ : constant(+_), pie) : endAngle;
  };
  pie.padAngle = function(_) {
    return arguments.length ? (padAngle = typeof _ === "function" ? _ : constant(+_), pie) : padAngle;
  };
  return pie;
}
var parser = function() {
  var o = function(k, v, o2, l) {
    for (o2 = o2 || {}, l = k.length; l--; o2[k[l]] = v)
      ;
    return o2;
  }, $V0 = [1, 4], $V1 = [1, 5], $V2 = [1, 6], $V3 = [1, 7], $V4 = [1, 9], $V5 = [1, 11, 13, 15, 17, 19, 20, 26, 27, 28, 29], $V6 = [2, 5], $V7 = [1, 6, 11, 13, 15, 17, 19, 20, 26, 27, 28, 29], $V8 = [26, 27, 28], $V9 = [2, 8], $Va = [1, 18], $Vb = [1, 19], $Vc = [1, 20], $Vd = [1, 21], $Ve = [1, 22], $Vf = [1, 23], $Vg = [1, 28], $Vh = [6, 26, 27, 28, 29];
  var parser2 = {
    trace: function trace() {
    },
    yy: {},
    symbols_: { "error": 2, "start": 3, "eol": 4, "directive": 5, "PIE": 6, "document": 7, "showData": 8, "line": 9, "statement": 10, "txt": 11, "value": 12, "title": 13, "title_value": 14, "acc_title": 15, "acc_title_value": 16, "acc_descr": 17, "acc_descr_value": 18, "acc_descr_multiline_value": 19, "section": 20, "openDirective": 21, "typeDirective": 22, "closeDirective": 23, ":": 24, "argDirective": 25, "NEWLINE": 26, ";": 27, "EOF": 28, "open_directive": 29, "type_directive": 30, "arg_directive": 31, "close_directive": 32, "$accept": 0, "$end": 1 },
    terminals_: { 2: "error", 6: "PIE", 8: "showData", 11: "txt", 12: "value", 13: "title", 14: "title_value", 15: "acc_title", 16: "acc_title_value", 17: "acc_descr", 18: "acc_descr_value", 19: "acc_descr_multiline_value", 20: "section", 24: ":", 26: "NEWLINE", 27: ";", 28: "EOF", 29: "open_directive", 30: "type_directive", 31: "arg_directive", 32: "close_directive" },
    productions_: [0, [3, 2], [3, 2], [3, 2], [3, 3], [7, 0], [7, 2], [9, 2], [10, 0], [10, 2], [10, 2], [10, 2], [10, 2], [10, 1], [10, 1], [10, 1], [5, 3], [5, 5], [4, 1], [4, 1], [4, 1], [21, 1], [22, 1], [25, 1], [23, 1]],
    performAction: function anonymous(yytext, yyleng, yylineno, yy, yystate, $$, _$) {
      var $0 = $$.length - 1;
      switch (yystate) {
        case 4:
          yy.setShowData(true);
          break;
        case 7:
          this.$ = $$[$0 - 1];
          break;
        case 9:
          yy.addSection($$[$0 - 1], yy.cleanupValue($$[$0]));
          break;
        case 10:
          this.$ = $$[$0].trim();
          yy.setDiagramTitle(this.$);
          break;
        case 11:
          this.$ = $$[$0].trim();
          yy.setAccTitle(this.$);
          break;
        case 12:
        case 13:
          this.$ = $$[$0].trim();
          yy.setAccDescription(this.$);
          break;
        case 14:
          yy.addSection($$[$0].substr(8));
          this.$ = $$[$0].substr(8);
          break;
        case 21:
          yy.parseDirective("%%{", "open_directive");
          break;
        case 22:
          yy.parseDirective($$[$0], "type_directive");
          break;
        case 23:
          $$[$0] = $$[$0].trim().replace(/'/g, '"');
          yy.parseDirective($$[$0], "arg_directive");
          break;
        case 24:
          yy.parseDirective("}%%", "close_directive", "pie");
          break;
      }
    },
    table: [{ 3: 1, 4: 2, 5: 3, 6: $V0, 21: 8, 26: $V1, 27: $V2, 28: $V3, 29: $V4 }, { 1: [3] }, { 3: 10, 4: 2, 5: 3, 6: $V0, 21: 8, 26: $V1, 27: $V2, 28: $V3, 29: $V4 }, { 3: 11, 4: 2, 5: 3, 6: $V0, 21: 8, 26: $V1, 27: $V2, 28: $V3, 29: $V4 }, o($V5, $V6, { 7: 12, 8: [1, 13] }), o($V7, [2, 18]), o($V7, [2, 19]), o($V7, [2, 20]), { 22: 14, 30: [1, 15] }, { 30: [2, 21] }, { 1: [2, 1] }, { 1: [2, 2] }, o($V8, $V9, { 21: 8, 9: 16, 10: 17, 5: 24, 1: [2, 3], 11: $Va, 13: $Vb, 15: $Vc, 17: $Vd, 19: $Ve, 20: $Vf, 29: $V4 }), o($V5, $V6, { 7: 25 }), { 23: 26, 24: [1, 27], 32: $Vg }, o([24, 32], [2, 22]), o($V5, [2, 6]), { 4: 29, 26: $V1, 27: $V2, 28: $V3 }, { 12: [1, 30] }, { 14: [1, 31] }, { 16: [1, 32] }, { 18: [1, 33] }, o($V8, [2, 13]), o($V8, [2, 14]), o($V8, [2, 15]), o($V8, $V9, { 21: 8, 9: 16, 10: 17, 5: 24, 1: [2, 4], 11: $Va, 13: $Vb, 15: $Vc, 17: $Vd, 19: $Ve, 20: $Vf, 29: $V4 }), o($Vh, [2, 16]), { 25: 34, 31: [1, 35] }, o($Vh, [2, 24]), o($V5, [2, 7]), o($V8, [2, 9]), o($V8, [2, 10]), o($V8, [2, 11]), o($V8, [2, 12]), { 23: 36, 32: $Vg }, { 32: [2, 23] }, o($Vh, [2, 17])],
    defaultActions: { 9: [2, 21], 10: [2, 1], 11: [2, 2], 35: [2, 23] },
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
            return 29;
          case 1:
            this.begin("type_directive");
            return 30;
          case 2:
            this.popState();
            this.begin("arg_directive");
            return 24;
          case 3:
            this.popState();
            this.popState();
            return 32;
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
            this.begin("title");
            return 13;
          case 11:
            this.popState();
            return "title_value";
          case 12:
            this.begin("acc_title");
            return 15;
          case 13:
            this.popState();
            return "acc_title_value";
          case 14:
            this.begin("acc_descr");
            return 17;
          case 15:
            this.popState();
            return "acc_descr_value";
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
      conditions: { "acc_descr_multiline": { "rules": [17, 18], "inclusive": false }, "acc_descr": { "rules": [15], "inclusive": false }, "acc_title": { "rules": [13], "inclusive": false }, "close_directive": { "rules": [], "inclusive": false }, "arg_directive": { "rules": [3, 4], "inclusive": false }, "type_directive": { "rules": [2, 3], "inclusive": false }, "open_directive": { "rules": [1], "inclusive": false }, "title": { "rules": [11], "inclusive": false }, "string": { "rules": [20, 21], "inclusive": false }, "INITIAL": { "rules": [0, 5, 6, 7, 8, 9, 10, 12, 14, 16, 19, 22, 23, 24, 25], "inclusive": true } }
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
let sections = {};
let showData = false;
const parseDirective = function(statement, context, type) {
  mermaidAPI.parseDirective(this, statement, context, type);
};
const addSection = function(id, value) {
  id = common.sanitizeText(id, getConfig());
  if (sections[id] === void 0) {
    sections[id] = value;
    log.debug("Added new section :", id);
  }
};
const getSections = () => sections;
const setShowData = function(toggle) {
  showData = toggle;
};
const getShowData = function() {
  return showData;
};
const cleanupValue = function(value) {
  if (value.substring(0, 1) === ":") {
    value = value.substring(1).trim();
    return Number(value.trim());
  } else {
    return Number(value.trim());
  }
};
const clear = function() {
  sections = {};
  showData = false;
  clear$1();
};
const db = {
  parseDirective,
  getConfig: () => getConfig().pie,
  addSection,
  getSections,
  cleanupValue,
  clear,
  setAccTitle,
  getAccTitle,
  setDiagramTitle,
  getDiagramTitle,
  setShowData,
  getShowData,
  getAccDescription,
  setAccDescription
};
const getStyles = (options) => `
  .pieCircle{
    stroke: ${options.pieStrokeColor};
    stroke-width : ${options.pieStrokeWidth};
    opacity : ${options.pieOpacity};
  }
  .pieTitleText {
    text-anchor: middle;
    font-size: ${options.pieTitleTextSize};
    fill: ${options.pieTitleTextColor};
    font-family: ${options.fontFamily};
  }
  .slice {
    font-family: ${options.fontFamily};
    fill: ${options.pieSectionTextColor};
    font-size:${options.pieSectionTextSize};
    // fill: white;
  }
  .legend text {
    fill: ${options.pieLegendTextColor};
    font-family: ${options.fontFamily};
    font-size: ${options.pieLegendTextSize};
  }
`;
const styles = getStyles;
let conf = getConfig();
let width;
const height = 450;
const draw = (txt, id, _version, diagObj) => {
  try {
    conf = getConfig();
    log.debug("Rendering info diagram\n" + txt);
    const securityLevel = getConfig().securityLevel;
    let sandboxElement;
    if (securityLevel === "sandbox") {
      sandboxElement = select("#i" + id);
    }
    const root = securityLevel === "sandbox" ? select(sandboxElement.nodes()[0].contentDocument.body) : select("body");
    const doc = securityLevel === "sandbox" ? sandboxElement.nodes()[0].contentDocument : document;
    diagObj.db.clear();
    diagObj.parser.parse(txt);
    log.debug("Parsed info diagram");
    const elem = doc.getElementById(id);
    width = elem.parentElement.offsetWidth;
    if (width === void 0) {
      width = 1200;
    }
    if (conf.useWidth !== void 0) {
      width = conf.useWidth;
    }
    if (conf.pie.useWidth !== void 0) {
      width = conf.pie.useWidth;
    }
    const diagram2 = root.select("#" + id);
    configureSvgSize(diagram2, height, width, conf.pie.useMaxWidth);
    elem.setAttribute("viewBox", "0 0 " + width + " " + height);
    var margin = 40;
    var legendRectSize = 18;
    var legendSpacing = 4;
    var radius = Math.min(width, height) / 2 - margin;
    var svg = diagram2.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    var data = diagObj.db.getSections();
    var sum = 0;
    Object.keys(data).forEach(function(key) {
      sum += data[key];
    });
    const themeVariables = conf.themeVariables;
    var myGeneratedColors = [
      themeVariables.pie1,
      themeVariables.pie2,
      themeVariables.pie3,
      themeVariables.pie4,
      themeVariables.pie5,
      themeVariables.pie6,
      themeVariables.pie7,
      themeVariables.pie8,
      themeVariables.pie9,
      themeVariables.pie10,
      themeVariables.pie11,
      themeVariables.pie12
    ];
    var color = ordinal().range(myGeneratedColors);
    var pieData = Object.entries(data).map(function(el, idx) {
      return {
        order: idx,
        name: el[0],
        value: el[1]
      };
    });
    var pie = d3pie().value(function(d) {
      return d.value;
    }).sort(function(a, b) {
      return a.order - b.order;
    });
    var dataReady = pie(pieData);
    var arcGenerator = d3arc().innerRadius(0).outerRadius(radius);
    svg.selectAll("mySlices").data(dataReady).enter().append("path").attr("d", arcGenerator).attr("fill", function(d) {
      return color(d.data.name);
    }).attr("class", "pieCircle");
    svg.selectAll("mySlices").data(dataReady).enter().append("text").text(function(d) {
      return (d.data.value / sum * 100).toFixed(0) + "%";
    }).attr("transform", function(d) {
      return "translate(" + arcGenerator.centroid(d) + ")";
    }).style("text-anchor", "middle").attr("class", "slice");
    svg.append("text").text(diagObj.db.getDiagramTitle()).attr("x", 0).attr("y", -(height - 50) / 2).attr("class", "pieTitleText");
    var legend = svg.selectAll(".legend").data(color.domain()).enter().append("g").attr("class", "legend").attr("transform", function(d, i) {
      const height2 = legendRectSize + legendSpacing;
      const offset = height2 * color.domain().length / 2;
      const horizontal = 12 * legendRectSize;
      const vertical = i * height2 - offset;
      return "translate(" + horizontal + "," + vertical + ")";
    });
    legend.append("rect").attr("width", legendRectSize).attr("height", legendRectSize).style("fill", color).style("stroke", color);
    legend.data(dataReady).append("text").attr("x", legendRectSize + legendSpacing).attr("y", legendRectSize - legendSpacing).text(function(d) {
      if (diagObj.db.getShowData() || conf.showData || conf.pie.showData) {
        return d.data.name + " [" + d.data.value + "]";
      } else {
        return d.data.name;
      }
    });
  } catch (e) {
    log.error("Error while rendering info diagram");
    log.error(e);
  }
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
//# sourceMappingURL=pieDiagram-2c4efa7e.js.map
