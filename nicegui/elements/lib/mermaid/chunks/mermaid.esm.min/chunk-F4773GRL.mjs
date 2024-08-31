import{a as pe,b as de}from"./chunk-4SRTBRON.mjs";import{b as fe}from"./chunk-CBSWTUHP.mjs";import{e as ue,m as he}from"./chunk-AC3VT7B7.mjs";import{L as O,P as re,Q as ie,R as ne,S as ae,T as oe,U as ce,V as le,X as x,b as g}from"./chunk-NQURTBEV.mjs";import{a as s}from"./chunk-GTKDMUJJ.mjs";var Pt=function(){var t=s(function(w,c,u,a){for(u=u||{},a=w.length;a--;u[w[a]]=c);return u},"o"),e=[1,2],l=[1,3],n=[1,4],p=[2,4],i=[1,9],d=[1,11],E=[1,16],o=[1,17],_=[1,18],k=[1,19],N=[1,32],I=[1,20],f=[1,21],L=[1,22],R=[1,23],F=[1,24],B=[1,26],P=[1,27],G=[1,28],rt=[1,29],it=[1,30],nt=[1,31],at=[1,34],ot=[1,35],ct=[1,36],lt=[1,37],Q=[1,33],S=[1,4,5,16,17,19,21,22,24,25,26,27,28,29,33,35,37,38,42,45,48,49,50,51,54],ut=[1,4,5,14,15,16,17,19,21,22,24,25,26,27,28,29,33,35,37,38,42,45,48,49,50,51,54],ee=[4,5,16,17,19,21,22,24,25,26,27,28,29,33,35,37,38,42,45,48,49,50,51,54],Ct={trace:s(function(){},"trace"),yy:{},symbols_:{error:2,start:3,SPACE:4,NL:5,SD:6,document:7,line:8,statement:9,classDefStatement:10,styleStatement:11,cssClassStatement:12,idStatement:13,DESCR:14,"-->":15,HIDE_EMPTY:16,scale:17,WIDTH:18,COMPOSIT_STATE:19,STRUCT_START:20,STRUCT_STOP:21,STATE_DESCR:22,AS:23,ID:24,FORK:25,JOIN:26,CHOICE:27,CONCURRENT:28,note:29,notePosition:30,NOTE_TEXT:31,direction:32,acc_title:33,acc_title_value:34,acc_descr:35,acc_descr_value:36,acc_descr_multiline_value:37,classDef:38,CLASSDEF_ID:39,CLASSDEF_STYLEOPTS:40,DEFAULT:41,style:42,STYLE_IDS:43,STYLEDEF_STYLEOPTS:44,class:45,CLASSENTITY_IDS:46,STYLECLASS:47,direction_tb:48,direction_bt:49,direction_rl:50,direction_lr:51,eol:52,";":53,EDGE_STATE:54,STYLE_SEPARATOR:55,left_of:56,right_of:57,$accept:0,$end:1},terminals_:{2:"error",4:"SPACE",5:"NL",6:"SD",14:"DESCR",15:"-->",16:"HIDE_EMPTY",17:"scale",18:"WIDTH",19:"COMPOSIT_STATE",20:"STRUCT_START",21:"STRUCT_STOP",22:"STATE_DESCR",23:"AS",24:"ID",25:"FORK",26:"JOIN",27:"CHOICE",28:"CONCURRENT",29:"note",31:"NOTE_TEXT",33:"acc_title",34:"acc_title_value",35:"acc_descr",36:"acc_descr_value",37:"acc_descr_multiline_value",38:"classDef",39:"CLASSDEF_ID",40:"CLASSDEF_STYLEOPTS",41:"DEFAULT",42:"style",43:"STYLE_IDS",44:"STYLEDEF_STYLEOPTS",45:"class",46:"CLASSENTITY_IDS",47:"STYLECLASS",48:"direction_tb",49:"direction_bt",50:"direction_rl",51:"direction_lr",53:";",54:"EDGE_STATE",55:"STYLE_SEPARATOR",56:"left_of",57:"right_of"},productions_:[0,[3,2],[3,2],[3,2],[7,0],[7,2],[8,2],[8,1],[8,1],[9,1],[9,1],[9,1],[9,1],[9,2],[9,3],[9,4],[9,1],[9,2],[9,1],[9,4],[9,3],[9,6],[9,1],[9,1],[9,1],[9,1],[9,4],[9,4],[9,1],[9,2],[9,2],[9,1],[10,3],[10,3],[11,3],[12,3],[32,1],[32,1],[32,1],[32,1],[52,1],[52,1],[13,1],[13,1],[13,3],[13,3],[30,1],[30,1]],performAction:s(function(c,u,a,y,T,r,Z){var h=r.length-1;switch(T){case 3:return y.setRootDoc(r[h]),r[h];break;case 4:this.$=[];break;case 5:r[h]!="nl"&&(r[h-1].push(r[h]),this.$=r[h-1]);break;case 6:case 7:this.$=r[h];break;case 8:this.$="nl";break;case 12:this.$=r[h];break;case 13:let ht=r[h-1];ht.description=y.trimColon(r[h]),this.$=ht;break;case 14:this.$={stmt:"relation",state1:r[h-2],state2:r[h]};break;case 15:let pt=y.trimColon(r[h]);this.$={stmt:"relation",state1:r[h-3],state2:r[h-1],description:pt};break;case 19:this.$={stmt:"state",id:r[h-3],type:"default",description:"",doc:r[h-1]};break;case 20:var M=r[h],z=r[h-2].trim();if(r[h].match(":")){var tt=r[h].split(":");M=tt[0],z=[z,tt[1]]}this.$={stmt:"state",id:M,type:"default",description:z};break;case 21:this.$={stmt:"state",id:r[h-3],type:"default",description:r[h-5],doc:r[h-1]};break;case 22:this.$={stmt:"state",id:r[h],type:"fork"};break;case 23:this.$={stmt:"state",id:r[h],type:"join"};break;case 24:this.$={stmt:"state",id:r[h],type:"choice"};break;case 25:this.$={stmt:"state",id:y.getDividerId(),type:"divider"};break;case 26:this.$={stmt:"state",id:r[h-1].trim(),note:{position:r[h-2].trim(),text:r[h].trim()}};break;case 29:this.$=r[h].trim(),y.setAccTitle(this.$);break;case 30:case 31:this.$=r[h].trim(),y.setAccDescription(this.$);break;case 32:case 33:this.$={stmt:"classDef",id:r[h-1].trim(),classes:r[h].trim()};break;case 34:this.$={stmt:"style",id:r[h-1].trim(),styleClass:r[h].trim()};break;case 35:this.$={stmt:"applyClass",id:r[h-1].trim(),styleClass:r[h].trim()};break;case 36:y.setDirection("TB"),this.$={stmt:"dir",value:"TB"};break;case 37:y.setDirection("BT"),this.$={stmt:"dir",value:"BT"};break;case 38:y.setDirection("RL"),this.$={stmt:"dir",value:"RL"};break;case 39:y.setDirection("LR"),this.$={stmt:"dir",value:"LR"};break;case 42:case 43:this.$={stmt:"state",id:r[h].trim(),type:"default",description:""};break;case 44:this.$={stmt:"state",id:r[h-2].trim(),classes:[r[h].trim()],type:"default",description:""};break;case 45:this.$={stmt:"state",id:r[h-2].trim(),classes:[r[h].trim()],type:"default",description:""};break}},"anonymous"),table:[{3:1,4:e,5:l,6:n},{1:[3]},{3:5,4:e,5:l,6:n},{3:6,4:e,5:l,6:n},t([1,4,5,16,17,19,22,24,25,26,27,28,29,33,35,37,38,42,45,48,49,50,51,54],p,{7:7}),{1:[2,1]},{1:[2,2]},{1:[2,3],4:i,5:d,8:8,9:10,10:12,11:13,12:14,13:15,16:E,17:o,19:_,22:k,24:N,25:I,26:f,27:L,28:R,29:F,32:25,33:B,35:P,37:G,38:rt,42:it,45:nt,48:at,49:ot,50:ct,51:lt,54:Q},t(S,[2,5]),{9:38,10:12,11:13,12:14,13:15,16:E,17:o,19:_,22:k,24:N,25:I,26:f,27:L,28:R,29:F,32:25,33:B,35:P,37:G,38:rt,42:it,45:nt,48:at,49:ot,50:ct,51:lt,54:Q},t(S,[2,7]),t(S,[2,8]),t(S,[2,9]),t(S,[2,10]),t(S,[2,11]),t(S,[2,12],{14:[1,39],15:[1,40]}),t(S,[2,16]),{18:[1,41]},t(S,[2,18],{20:[1,42]}),{23:[1,43]},t(S,[2,22]),t(S,[2,23]),t(S,[2,24]),t(S,[2,25]),{30:44,31:[1,45],56:[1,46],57:[1,47]},t(S,[2,28]),{34:[1,48]},{36:[1,49]},t(S,[2,31]),{39:[1,50],41:[1,51]},{43:[1,52]},{46:[1,53]},t(ut,[2,42],{55:[1,54]}),t(ut,[2,43],{55:[1,55]}),t(S,[2,36]),t(S,[2,37]),t(S,[2,38]),t(S,[2,39]),t(S,[2,6]),t(S,[2,13]),{13:56,24:N,54:Q},t(S,[2,17]),t(ee,p,{7:57}),{24:[1,58]},{24:[1,59]},{23:[1,60]},{24:[2,46]},{24:[2,47]},t(S,[2,29]),t(S,[2,30]),{40:[1,61]},{40:[1,62]},{44:[1,63]},{47:[1,64]},{24:[1,65]},{24:[1,66]},t(S,[2,14],{14:[1,67]}),{4:i,5:d,8:8,9:10,10:12,11:13,12:14,13:15,16:E,17:o,19:_,21:[1,68],22:k,24:N,25:I,26:f,27:L,28:R,29:F,32:25,33:B,35:P,37:G,38:rt,42:it,45:nt,48:at,49:ot,50:ct,51:lt,54:Q},t(S,[2,20],{20:[1,69]}),{31:[1,70]},{24:[1,71]},t(S,[2,32]),t(S,[2,33]),t(S,[2,34]),t(S,[2,35]),t(ut,[2,44]),t(ut,[2,45]),t(S,[2,15]),t(S,[2,19]),t(ee,p,{7:72}),t(S,[2,26]),t(S,[2,27]),{4:i,5:d,8:8,9:10,10:12,11:13,12:14,13:15,16:E,17:o,19:_,21:[1,73],22:k,24:N,25:I,26:f,27:L,28:R,29:F,32:25,33:B,35:P,37:G,38:rt,42:it,45:nt,48:at,49:ot,50:ct,51:lt,54:Q},t(S,[2,21])],defaultActions:{5:[2,1],6:[2,2],46:[2,46],47:[2,47]},parseError:s(function(c,u){if(u.recoverable)this.trace(c);else{var a=new Error(c);throw a.hash=u,a}},"parseError"),parse:s(function(c){var u=this,a=[0],y=[],T=[null],r=[],Z=this.table,h="",M=0,z=0,tt=0,ht=2,pt=1,ze=r.slice.call(arguments,1),b=Object.create(this.lexer),V={yy:{}};for(var It in this.yy)Object.prototype.hasOwnProperty.call(this.yy,It)&&(V.yy[It]=this.yy[It]);b.setInput(c,V.yy),V.yy.lexer=b,V.yy.parser=this,typeof b.yylloc>"u"&&(b.yylloc={});var Rt=b.yylloc;r.push(Rt);var We=b.options&&b.options.ranges;typeof V.yy.parseError=="function"?this.parseError=V.yy.parseError:this.parseError=Object.getPrototypeOf(this).parseError;function Cs(A){a.length=a.length-2*A,T.length=T.length-A,r.length=r.length-A}s(Cs,"popStack");function Xe(){var A;return A=y.pop()||b.lex()||pt,typeof A!="number"&&(A instanceof Array&&(y=A,A=y.pop()),A=u.symbols_[A]||A),A}s(Xe,"lex");for(var m,vt,U,C,Ls,Ot,W={},ft,v,se,dt;;){if(U=a[a.length-1],this.defaultActions[U]?C=this.defaultActions[U]:((m===null||typeof m>"u")&&(m=Xe()),C=Z[U]&&Z[U][m]),typeof C>"u"||!C.length||!C[0]){var Nt="";dt=[];for(ft in Z[U])this.terminals_[ft]&&ft>ht&&dt.push("'"+this.terminals_[ft]+"'");b.showPosition?Nt="Parse error on line "+(M+1)+`:
`+b.showPosition()+`
Expecting `+dt.join(", ")+", got '"+(this.terminals_[m]||m)+"'":Nt="Parse error on line "+(M+1)+": Unexpected "+(m==pt?"end of input":"'"+(this.terminals_[m]||m)+"'"),this.parseError(Nt,{text:b.match,token:this.terminals_[m]||m,line:b.yylineno,loc:Rt,expected:dt})}if(C[0]instanceof Array&&C.length>1)throw new Error("Parse Error: multiple actions possible at state: "+U+", token: "+m);switch(C[0]){case 1:a.push(m),T.push(b.yytext),r.push(b.yylloc),a.push(C[1]),m=null,vt?(m=vt,vt=null):(z=b.yyleng,h=b.yytext,M=b.yylineno,Rt=b.yylloc,tt>0&&tt--);break;case 2:if(v=this.productions_[C[1]][1],W.$=T[T.length-v],W._$={first_line:r[r.length-(v||1)].first_line,last_line:r[r.length-1].last_line,first_column:r[r.length-(v||1)].first_column,last_column:r[r.length-1].last_column},We&&(W._$.range=[r[r.length-(v||1)].range[0],r[r.length-1].range[1]]),Ot=this.performAction.apply(W,[h,z,M,V.yy,C[1],T,r].concat(ze)),typeof Ot<"u")return Ot;v&&(a=a.slice(0,-1*v*2),T=T.slice(0,-1*v),r=r.slice(0,-1*v)),a.push(this.productions_[C[1]][0]),T.push(W.$),r.push(W._$),se=Z[a[a.length-2]][a[a.length-1]],a.push(se);break;case 3:return!0}}return!0},"parse")},je=function(){var w={EOF:1,parseError:s(function(u,a){if(this.yy.parser)this.yy.parser.parseError(u,a);else throw new Error(u)},"parseError"),setInput:s(function(c,u){return this.yy=u||this.yy||{},this._input=c,this._more=this._backtrack=this.done=!1,this.yylineno=this.yyleng=0,this.yytext=this.matched=this.match="",this.conditionStack=["INITIAL"],this.yylloc={first_line:1,first_column:0,last_line:1,last_column:0},this.options.ranges&&(this.yylloc.range=[0,0]),this.offset=0,this},"setInput"),input:s(function(){var c=this._input[0];this.yytext+=c,this.yyleng++,this.offset++,this.match+=c,this.matched+=c;var u=c.match(/(?:\r\n?|\n).*/g);return u?(this.yylineno++,this.yylloc.last_line++):this.yylloc.last_column++,this.options.ranges&&this.yylloc.range[1]++,this._input=this._input.slice(1),c},"input"),unput:s(function(c){var u=c.length,a=c.split(/(?:\r\n?|\n)/g);this._input=c+this._input,this.yytext=this.yytext.substr(0,this.yytext.length-u),this.offset-=u;var y=this.match.split(/(?:\r\n?|\n)/g);this.match=this.match.substr(0,this.match.length-1),this.matched=this.matched.substr(0,this.matched.length-1),a.length-1&&(this.yylineno-=a.length-1);var T=this.yylloc.range;return this.yylloc={first_line:this.yylloc.first_line,last_line:this.yylineno+1,first_column:this.yylloc.first_column,last_column:a?(a.length===y.length?this.yylloc.first_column:0)+y[y.length-a.length].length-a[0].length:this.yylloc.first_column-u},this.options.ranges&&(this.yylloc.range=[T[0],T[0]+this.yyleng-u]),this.yyleng=this.yytext.length,this},"unput"),more:s(function(){return this._more=!0,this},"more"),reject:s(function(){if(this.options.backtrack_lexer)this._backtrack=!0;else return this.parseError("Lexical error on line "+(this.yylineno+1)+`. You can only invoke reject() in the lexer when the lexer is of the backtracking persuasion (options.backtrack_lexer = true).
`+this.showPosition(),{text:"",token:null,line:this.yylineno});return this},"reject"),less:s(function(c){this.unput(this.match.slice(c))},"less"),pastInput:s(function(){var c=this.matched.substr(0,this.matched.length-this.match.length);return(c.length>20?"...":"")+c.substr(-20).replace(/\n/g,"")},"pastInput"),upcomingInput:s(function(){var c=this.match;return c.length<20&&(c+=this._input.substr(0,20-c.length)),(c.substr(0,20)+(c.length>20?"...":"")).replace(/\n/g,"")},"upcomingInput"),showPosition:s(function(){var c=this.pastInput(),u=new Array(c.length+1).join("-");return c+this.upcomingInput()+`
`+u+"^"},"showPosition"),test_match:s(function(c,u){var a,y,T;if(this.options.backtrack_lexer&&(T={yylineno:this.yylineno,yylloc:{first_line:this.yylloc.first_line,last_line:this.last_line,first_column:this.yylloc.first_column,last_column:this.yylloc.last_column},yytext:this.yytext,match:this.match,matches:this.matches,matched:this.matched,yyleng:this.yyleng,offset:this.offset,_more:this._more,_input:this._input,yy:this.yy,conditionStack:this.conditionStack.slice(0),done:this.done},this.options.ranges&&(T.yylloc.range=this.yylloc.range.slice(0))),y=c[0].match(/(?:\r\n?|\n).*/g),y&&(this.yylineno+=y.length),this.yylloc={first_line:this.yylloc.last_line,last_line:this.yylineno+1,first_column:this.yylloc.last_column,last_column:y?y[y.length-1].length-y[y.length-1].match(/\r?\n?/)[0].length:this.yylloc.last_column+c[0].length},this.yytext+=c[0],this.match+=c[0],this.matches=c,this.yyleng=this.yytext.length,this.options.ranges&&(this.yylloc.range=[this.offset,this.offset+=this.yyleng]),this._more=!1,this._backtrack=!1,this._input=this._input.slice(c[0].length),this.matched+=c[0],a=this.performAction.call(this,this.yy,this,u,this.conditionStack[this.conditionStack.length-1]),this.done&&this._input&&(this.done=!1),a)return a;if(this._backtrack){for(var r in T)this[r]=T[r];return!1}return!1},"test_match"),next:s(function(){if(this.done)return this.EOF;this._input||(this.done=!0);var c,u,a,y;this._more||(this.yytext="",this.match="");for(var T=this._currentRules(),r=0;r<T.length;r++)if(a=this._input.match(this.rules[T[r]]),a&&(!u||a[0].length>u[0].length)){if(u=a,y=r,this.options.backtrack_lexer){if(c=this.test_match(a,T[r]),c!==!1)return c;if(this._backtrack){u=!1;continue}else return!1}else if(!this.options.flex)break}return u?(c=this.test_match(u,T[y]),c!==!1?c:!1):this._input===""?this.EOF:this.parseError("Lexical error on line "+(this.yylineno+1)+`. Unrecognized text.
`+this.showPosition(),{text:"",token:null,line:this.yylineno})},"next"),lex:s(function(){var u=this.next();return u||this.lex()},"lex"),begin:s(function(u){this.conditionStack.push(u)},"begin"),popState:s(function(){var u=this.conditionStack.length-1;return u>0?this.conditionStack.pop():this.conditionStack[0]},"popState"),_currentRules:s(function(){return this.conditionStack.length&&this.conditionStack[this.conditionStack.length-1]?this.conditions[this.conditionStack[this.conditionStack.length-1]].rules:this.conditions.INITIAL.rules},"_currentRules"),topState:s(function(u){return u=this.conditionStack.length-1-Math.abs(u||0),u>=0?this.conditionStack[u]:"INITIAL"},"topState"),pushState:s(function(u){this.begin(u)},"pushState"),stateStackSize:s(function(){return this.conditionStack.length},"stateStackSize"),options:{"case-insensitive":!0},performAction:s(function(u,a,y,T){var r=T;switch(y){case 0:return 41;case 1:return 48;case 2:return 49;case 3:return 50;case 4:return 51;case 5:break;case 6:break;case 7:return 5;case 8:break;case 9:break;case 10:break;case 11:break;case 12:return this.pushState("SCALE"),17;break;case 13:return 18;case 14:this.popState();break;case 15:return this.begin("acc_title"),33;break;case 16:return this.popState(),"acc_title_value";break;case 17:return this.begin("acc_descr"),35;break;case 18:return this.popState(),"acc_descr_value";break;case 19:this.begin("acc_descr_multiline");break;case 20:this.popState();break;case 21:return"acc_descr_multiline_value";case 22:return this.pushState("CLASSDEF"),38;break;case 23:return this.popState(),this.pushState("CLASSDEFID"),"DEFAULT_CLASSDEF_ID";break;case 24:return this.popState(),this.pushState("CLASSDEFID"),39;break;case 25:return this.popState(),40;break;case 26:return this.pushState("CLASS"),45;break;case 27:return this.popState(),this.pushState("CLASS_STYLE"),46;break;case 28:return this.popState(),47;break;case 29:return this.pushState("STYLE"),42;break;case 30:return this.popState(),this.pushState("STYLEDEF_STYLES"),43;break;case 31:return this.popState(),44;break;case 32:return this.pushState("SCALE"),17;break;case 33:return 18;case 34:this.popState();break;case 35:this.pushState("STATE");break;case 36:return this.popState(),a.yytext=a.yytext.slice(0,-8).trim(),25;break;case 37:return this.popState(),a.yytext=a.yytext.slice(0,-8).trim(),26;break;case 38:return this.popState(),a.yytext=a.yytext.slice(0,-10).trim(),27;break;case 39:return this.popState(),a.yytext=a.yytext.slice(0,-8).trim(),25;break;case 40:return this.popState(),a.yytext=a.yytext.slice(0,-8).trim(),26;break;case 41:return this.popState(),a.yytext=a.yytext.slice(0,-10).trim(),27;break;case 42:return 48;case 43:return 49;case 44:return 50;case 45:return 51;case 46:this.pushState("STATE_STRING");break;case 47:return this.pushState("STATE_ID"),"AS";break;case 48:return this.popState(),"ID";break;case 49:this.popState();break;case 50:return"STATE_DESCR";case 51:return 19;case 52:this.popState();break;case 53:return this.popState(),this.pushState("struct"),20;break;case 54:break;case 55:return this.popState(),21;break;case 56:break;case 57:return this.begin("NOTE"),29;break;case 58:return this.popState(),this.pushState("NOTE_ID"),56;break;case 59:return this.popState(),this.pushState("NOTE_ID"),57;break;case 60:this.popState(),this.pushState("FLOATING_NOTE");break;case 61:return this.popState(),this.pushState("FLOATING_NOTE_ID"),"AS";break;case 62:break;case 63:return"NOTE_TEXT";case 64:return this.popState(),"ID";break;case 65:return this.popState(),this.pushState("NOTE_TEXT"),24;break;case 66:return this.popState(),a.yytext=a.yytext.substr(2).trim(),31;break;case 67:return this.popState(),a.yytext=a.yytext.slice(0,-8).trim(),31;break;case 68:return 6;case 69:return 6;case 70:return 16;case 71:return 54;case 72:return 24;case 73:return a.yytext=a.yytext.trim(),14;break;case 74:return 15;case 75:return 28;case 76:return 55;case 77:return 5;case 78:return"INVALID"}},"anonymous"),rules:[/^(?:default\b)/i,/^(?:.*direction\s+TB[^\n]*)/i,/^(?:.*direction\s+BT[^\n]*)/i,/^(?:.*direction\s+RL[^\n]*)/i,/^(?:.*direction\s+LR[^\n]*)/i,/^(?:%%(?!\{)[^\n]*)/i,/^(?:[^\}]%%[^\n]*)/i,/^(?:[\n]+)/i,/^(?:[\s]+)/i,/^(?:((?!\n)\s)+)/i,/^(?:#[^\n]*)/i,/^(?:%[^\n]*)/i,/^(?:scale\s+)/i,/^(?:\d+)/i,/^(?:\s+width\b)/i,/^(?:accTitle\s*:\s*)/i,/^(?:(?!\n||)*[^\n]*)/i,/^(?:accDescr\s*:\s*)/i,/^(?:(?!\n||)*[^\n]*)/i,/^(?:accDescr\s*\{\s*)/i,/^(?:[\}])/i,/^(?:[^\}]*)/i,/^(?:classDef\s+)/i,/^(?:DEFAULT\s+)/i,/^(?:\w+\s+)/i,/^(?:[^\n]*)/i,/^(?:class\s+)/i,/^(?:(\w+)+((,\s*\w+)*))/i,/^(?:[^\n]*)/i,/^(?:style\s+)/i,/^(?:[\w,]+\s+)/i,/^(?:[^\n]*)/i,/^(?:scale\s+)/i,/^(?:\d+)/i,/^(?:\s+width\b)/i,/^(?:state\s+)/i,/^(?:.*<<fork>>)/i,/^(?:.*<<join>>)/i,/^(?:.*<<choice>>)/i,/^(?:.*\[\[fork\]\])/i,/^(?:.*\[\[join\]\])/i,/^(?:.*\[\[choice\]\])/i,/^(?:.*direction\s+TB[^\n]*)/i,/^(?:.*direction\s+BT[^\n]*)/i,/^(?:.*direction\s+RL[^\n]*)/i,/^(?:.*direction\s+LR[^\n]*)/i,/^(?:["])/i,/^(?:\s*as\s+)/i,/^(?:[^\n\{]*)/i,/^(?:["])/i,/^(?:[^"]*)/i,/^(?:[^\n\s\{]+)/i,/^(?:\n)/i,/^(?:\{)/i,/^(?:%%(?!\{)[^\n]*)/i,/^(?:\})/i,/^(?:[\n])/i,/^(?:note\s+)/i,/^(?:left of\b)/i,/^(?:right of\b)/i,/^(?:")/i,/^(?:\s*as\s*)/i,/^(?:["])/i,/^(?:[^"]*)/i,/^(?:[^\n]*)/i,/^(?:\s*[^:\n\s\-]+)/i,/^(?:\s*:[^:\n;]+)/i,/^(?:[\s\S]*?end note\b)/i,/^(?:stateDiagram\s+)/i,/^(?:stateDiagram-v2\s+)/i,/^(?:hide empty description\b)/i,/^(?:\[\*\])/i,/^(?:[^:\n\s\-\{]+)/i,/^(?:\s*:[^:\n;]+)/i,/^(?:-->)/i,/^(?:--)/i,/^(?::::)/i,/^(?:$)/i,/^(?:.)/i],conditions:{LINE:{rules:[9,10],inclusive:!1},struct:{rules:[9,10,22,26,29,35,42,43,44,45,54,55,56,57,71,72,73,74,75],inclusive:!1},FLOATING_NOTE_ID:{rules:[64],inclusive:!1},FLOATING_NOTE:{rules:[61,62,63],inclusive:!1},NOTE_TEXT:{rules:[66,67],inclusive:!1},NOTE_ID:{rules:[65],inclusive:!1},NOTE:{rules:[58,59,60],inclusive:!1},STYLEDEF_STYLEOPTS:{rules:[],inclusive:!1},STYLEDEF_STYLES:{rules:[31],inclusive:!1},STYLE_IDS:{rules:[],inclusive:!1},STYLE:{rules:[30],inclusive:!1},CLASS_STYLE:{rules:[28],inclusive:!1},CLASS:{rules:[27],inclusive:!1},CLASSDEFID:{rules:[25],inclusive:!1},CLASSDEF:{rules:[23,24],inclusive:!1},acc_descr_multiline:{rules:[20,21],inclusive:!1},acc_descr:{rules:[18],inclusive:!1},acc_title:{rules:[16],inclusive:!1},SCALE:{rules:[13,14,33,34],inclusive:!1},ALIAS:{rules:[],inclusive:!1},STATE_ID:{rules:[48],inclusive:!1},STATE_STRING:{rules:[49,50],inclusive:!1},FORK_STATE:{rules:[],inclusive:!1},STATE:{rules:[9,10,36,37,38,39,40,41,46,47,51,52,53],inclusive:!1},ID:{rules:[9,10],inclusive:!1},INITIAL:{rules:[0,1,2,3,4,5,6,7,8,10,11,12,15,17,19,22,26,29,32,35,53,57,68,69,70,71,72,73,74,76,77,78],inclusive:!0}}};return w}();Ct.lexer=je;function Lt(){this.yy={}}return s(Lt,"Parser"),Lt.prototype=Ct,Ct.Parser=Lt,new Lt}();Pt.parser=Pt;var Is=Pt;var Se="LR",St="TB",X="state",et="relation",ye="classDef",Ee="style",Te="applyClass",H="default",yt="divider",Gt="fill:none",wt="fill: #333",$t="c",Yt="text",Ft="normal",Et="rect",Tt="rectWithTitle",_e="stateStart",ge="stateEnd",Bt="divider",Mt="roundedWithTitle",be="note",ke="noteGroup",K="statediagram",Ke="state",me=`${K}-${Ke}`,Vt="transition",Je="note",qe="note-edge",xe=`${Vt} ${qe}`,De=`${K}-${Je}`,Qe="cluster",Ae=`${K}-${Qe}`,Ze="cluster-alt",Ce=`${K}-${Ze}`,Ut="parent",Ht="note",Le="state",_t="----",Ie=`${_t}${Ht}`,jt=`${_t}${Ut}`;var zt=s((t,e=St)=>{if(!t.doc)return e;let l=e;for(let n of t.doc)n.stmt==="dir"&&(l=n.value);return l},"getDir"),ts=s(function(t,e){return e.db.extract(e.db.getRootDocV2()),e.db.getClasses()},"getClasses"),es=s(async function(t,e,l,n){g.info("REF0:"),g.info("Drawing state diagram (v2)",e);let{securityLevel:p,state:i,layout:d}=x();n.db.extract(n.db.getRootDocV2());let E=n.db.getData(),o=pe(e,p);E.type=n.type,E.layoutAlgorithm=d,E.nodeSpacing=i?.nodeSpacing||50,E.rankSpacing=i?.rankSpacing||50,E.markers=["barb"],E.diagramId=e,await fe(E,o);let _=8;he.insertTitle(o,"statediagramTitleText",i?.titleTopMargin??25,n.db.getDiagramTitle()),de(o,_,K,i?.useMaxWidth??!0)},"draw"),Bs={getClasses:ts,draw:es,getDir:zt};var bt=new Map,$=0;function Wt(t="",e=0,l="",n=_t){let p=l!==null&&l.length>0?`${n}${l}`:"";return`${Le}-${t}${p}-${e}`}s(Wt,"stateDomId");var ss=s((t,e,l,n,p,i,d,E)=>{g.trace("items",e),e.forEach(o=>{switch(o.stmt){case X:J(t,o,l,n,p,i,d,E);break;case H:J(t,o,l,n,p,i,d,E);break;case et:{J(t,o.state1,l,n,p,i,d,E),J(t,o.state2,l,n,p,i,d,E);let _={id:"edge"+$,start:o.state1.id,end:o.state2.id,arrowhead:"normal",arrowTypeEnd:"arrow_barb",style:Gt,labelStyle:"",label:O.sanitizeText(o.description,x()),arrowheadStyle:wt,labelpos:$t,labelType:Yt,thickness:Ft,classes:Vt,look:d};p.push(_),$++}break}})},"setupDoc"),Re=s((t,e=St)=>{let l=e;if(t.doc)for(let n of t.doc)n.stmt==="dir"&&(l=n.value);return l},"getDir");function gt(t,e,l){if(!e.id||e.id==="</join></fork>"||e.id==="</choice>")return;e.cssClasses&&(Array.isArray(e.cssCompiledStyles)||(e.cssCompiledStyles=[]),e.cssClasses.split(" ").forEach(p=>{if(l.get(p)){let i=l.get(p);e.cssCompiledStyles=[...e.cssCompiledStyles,...i.styles]}}));let n=t.find(p=>p.id===e.id);n?Object.assign(n,e):t.push(e)}s(gt,"insertOrUpdateNode");function rs(t){return t?.classes?.join(" ")??""}s(rs,"getClassesFromDbInfo");function is(t){return t?.styles??[]}s(is,"getStylesFromDbInfo");var J=s((t,e,l,n,p,i,d,E)=>{let o=e.id,_=l.get(o),k=rs(_),N=is(_);if(g.info("dataFetcher parsedItem",e,_,N),o!=="root"){let I=Et;e.start===!0?I=_e:e.start===!1&&(I=ge),e.type!==H&&(I=e.type),bt.get(o)||bt.set(o,{id:o,shape:I,description:O.sanitizeText(o,x()),cssClasses:`${k} ${me}`,cssStyles:N});let f=bt.get(o);e.description&&(Array.isArray(f.description)?(f.shape=Tt,f.description.push(e.description)):f.description?.length>0?(f.shape=Tt,f.description===o?f.description=[e.description]:f.description=[f.description,e.description]):(f.shape=Et,f.description=e.description),f.description=O.sanitizeTextOrArray(f.description,x())),f.description?.length===1&&f.shape===Tt&&(f.type==="group"?f.shape=Mt:f.shape=Et),!f.type&&e.doc&&(g.info("Setting cluster for XCX",o,Re(e)),f.type="group",f.isGroup=!0,f.dir=Re(e),f.shape=e.type===yt?Bt:Mt,f.cssClasses=`${f.cssClasses} ${Ae} ${i?Ce:""}`);let L={labelStyle:"",shape:f.shape,label:f.description,cssClasses:f.cssClasses,cssCompiledStyles:[],cssStyles:f.cssStyles,id:o,dir:f.dir,domId:Wt(o,$),type:f.type,isGroup:f.type==="group",padding:8,rx:10,ry:10,look:d};if(L.shape===Bt&&(L.label=""),t&&t.id!=="root"&&(g.trace("Setting node ",o," to be child of its parent ",t.id),L.parentId=t.id),L.centerLabel=!0,e.note){let R={labelStyle:"",shape:be,label:e.note.text,cssClasses:De,cssStyles:[],cssCompilesStyles:[],id:o+Ie+"-"+$,domId:Wt(o,$,Ht),type:f.type,isGroup:f.type==="group",padding:x().flowchart.padding,look:d,position:e.note.position},F=o+jt,B={labelStyle:"",shape:ke,label:e.note.text,cssClasses:f.cssClasses,cssStyles:[],id:o+jt,domId:Wt(o,$,Ut),type:"group",isGroup:!0,padding:16,look:d,position:e.note.position};$++,B.id=F,R.parentId=F,gt(n,B,E),gt(n,R,E),gt(n,L,E);let P=o,G=R.id;e.note.position==="left of"&&(P=R.id,G=o),p.push({id:P+"-"+G,start:P,end:G,arrowhead:"none",arrowTypeEnd:"",style:Gt,labelStyle:"",classes:xe,arrowheadStyle:wt,labelpos:$t,labelType:Yt,thickness:Ft,look:d})}else gt(n,L,E)}e.doc&&(g.trace("Adding nodes children "),ss(e,e.doc,l,n,p,!i,d,E))},"dataFetcher"),ve=s(()=>{bt.clear(),$=0},"reset");var qt="[*]",Ge="start",we=qt,$e="end",Oe="color",Ne="fill",ns="bgFill",as=",";function Ye(){return new Map}s(Ye,"newClassesList");var xt=[],Qt=[],Fe=Se,Dt=[],q=Ye(),Be=s(()=>({relations:[],states:new Map,documents:{}}),"newDoc"),At={root:Be()},D=At.root,st=0,Pe=0,os={LINE:0,DOTTED_LINE:1},cs={AGGREGATION:0,EXTENSION:1,COMPOSITION:2,DEPENDENCY:3},kt=s(t=>JSON.parse(JSON.stringify(t)),"clone"),ls=s(t=>{g.info("Setting root doc",t),Dt=t},"setRootDoc"),us=s(()=>Dt,"getRootDoc"),mt=s((t,e,l)=>{if(e.stmt===et)mt(t,e.state1,!0),mt(t,e.state2,!1);else if(e.stmt===X&&(e.id==="[*]"?(e.id=l?t.id+"_start":t.id+"_end",e.start=l):e.id=e.id.trim()),e.doc){let n=[],p=[],i;for(i=0;i<e.doc.length;i++)if(e.doc[i].type===yt){let d=kt(e.doc[i]);d.doc=kt(p),n.push(d),p=[]}else p.push(e.doc[i]);if(n.length>0&&p.length>0){let d={stmt:X,id:ue(),type:"divider",doc:kt(p)};n.push(kt(d)),e.doc=n}e.doc.forEach(d=>mt(e,d,!0))}},"docTranslator"),Zt=s(()=>(mt({id:"root"},{id:"root",doc:Dt},!0),{id:"root",doc:Dt}),"getRootDocV2"),hs=s(t=>{let e;t.doc?e=t.doc:e=t,g.info(e),Me(!0),g.info("Extract initial document:",e),e.forEach(i=>{switch(g.warn("Statement",i.stmt),i.stmt){case X:Y(i.id.trim(),i.type,i.doc,i.description,i.note,i.classes,i.styles,i.textStyles);break;case et:Ue(i.state1,i.state2,i.description);break;case ye:He(i.id.trim(),i.classes);break;case Ee:{let d=i.id.trim().split(","),E=i.styleClass.split(",");d.forEach(o=>{let _=j(o);if(_===void 0){let k=o.trim();Y(k),_=j(k)}_.styles=E.map(k=>k.replace(/;/g,"")?.trim())})}break;case Te:te(i.id.trim(),i.styleClass);break}});let l=Ve(),p=x().look;ve(),J(void 0,Zt(),l,xt,Qt,!0,p,q),xt.forEach(i=>{if(Array.isArray(i.label)){if(i.description=i.label.slice(1),i.isGroup&&i.description.length>0)throw new Error("Group nodes can only have label. Remove the additional description for node ["+i.id+"]");i.label=i.label[0]}})},"extract"),Y=s(function(t,e=H,l=null,n=null,p=null,i=null,d=null,E=null){let o=t?.trim();if(D.states.has(o)?(D.states.get(o).doc||(D.states.get(o).doc=l),D.states.get(o).type||(D.states.get(o).type=e)):(g.info("Adding state ",o,n),D.states.set(o,{id:o,descriptions:[],type:e,doc:l,note:p,classes:[],styles:[],textStyles:[]})),n&&(g.info("Setting state description",o,n),typeof n=="string"&&Jt(o,n.trim()),typeof n=="object"&&n.forEach(_=>Jt(o,_.trim()))),p){let _=D.states.get(o);_.note=p,_.note.text=O.sanitizeText(_.note.text,x())}i&&(g.info("Setting state classes",o,i),(typeof i=="string"?[i]:i).forEach(k=>te(o,k.trim()))),d&&(g.info("Setting state styles",o,d),(typeof d=="string"?[d]:d).forEach(k=>gs(o,k.trim()))),E&&(g.info("Setting state styles",o,d),(typeof E=="string"?[E]:E).forEach(k=>bs(o,k.trim())))},"addState"),Me=s(function(t){xt=[],Qt=[],At={root:Be()},D=At.root,st=0,q=Ye(),t||re()},"clear"),j=s(function(t){return D.states.get(t)},"getState"),Ve=s(function(){return D.states},"getStates"),ps=s(function(){g.info("Documents = ",At)},"logDocuments"),fs=s(function(){return D.relations},"getRelations");function Xt(t=""){let e=t;return t===qt&&(st++,e=`${Ge}${st}`),e}s(Xt,"startIdIfNeeded");function Kt(t="",e=H){return t===qt?Ge:e}s(Kt,"startTypeIfNeeded");function ds(t=""){let e=t;return t===we&&(st++,e=`${$e}${st}`),e}s(ds,"endIdIfNeeded");function Ss(t="",e=H){return t===we?$e:e}s(Ss,"endTypeIfNeeded");function ys(t,e,l){let n=Xt(t.id.trim()),p=Kt(t.id.trim(),t.type),i=Xt(e.id.trim()),d=Kt(e.id.trim(),e.type);Y(n,p,t.doc,t.description,t.note,t.classes,t.styles,t.textStyles),Y(i,d,e.doc,e.description,e.note,e.classes,e.styles,e.textStyles),D.relations.push({id1:n,id2:i,relationTitle:O.sanitizeText(l,x())})}s(ys,"addRelationObjs");var Ue=s(function(t,e,l){if(typeof t=="object")ys(t,e,l);else{let n=Xt(t.trim()),p=Kt(t),i=ds(e.trim()),d=Ss(e);Y(n,p),Y(i,d),D.relations.push({id1:n,id2:i,title:O.sanitizeText(l,x())})}},"addRelation"),Jt=s(function(t,e){let l=D.states.get(t),n=e.startsWith(":")?e.replace(":","").trim():e;l.descriptions.push(O.sanitizeText(n,x()))},"addDescription"),Es=s(function(t){return t.substring(0,1)===":"?t.substr(2).trim():t.trim()},"cleanupLabel"),Ts=s(()=>(Pe++,"divider-id-"+Pe),"getDividerId"),He=s(function(t,e=""){q.has(t)||q.set(t,{id:t,styles:[],textStyles:[]});let l=q.get(t);e?.split(as).forEach(n=>{let p=n.replace(/([^;]*);/,"$1").trim();if(RegExp(Oe).exec(n)){let d=p.replace(Ne,ns).replace(Oe,Ne);l.textStyles.push(d)}l.styles.push(p)})},"addStyleClass"),_s=s(function(){return q},"getClasses"),te=s(function(t,e){t.split(",").forEach(function(l){let n=j(l);if(n===void 0){let p=l.trim();Y(p),n=j(p)}n.classes.push(e)})},"setCssClass"),gs=s(function(t,e){let l=j(t);l!==void 0&&l.styles.push(e)},"setStyle"),bs=s(function(t,e){let l=j(t);l!==void 0&&l.textStyles.push(e)},"setTextStyle"),ks=s(()=>Fe,"getDirection"),ms=s(t=>{Fe=t},"setDirection"),xs=s(t=>t&&t[0]===":"?t.substr(1).trim():t.trim(),"trimColon"),Ds=s(()=>{let t=x();return{nodes:xt,edges:Qt,other:{},config:t,direction:zt(Zt())}},"getData"),rr={getConfig:s(()=>x().state,"getConfig"),getData:Ds,addState:Y,clear:Me,getState:j,getStates:Ve,getRelations:fs,getClasses:_s,getDirection:ks,addRelation:Ue,getDividerId:Ts,setDirection:ms,cleanupLabel:Es,lineType:os,relationType:cs,logDocuments:ps,getRootDoc:us,setRootDoc:ls,getRootDocV2:Zt,extract:hs,trimColon:xs,getAccTitle:ne,setAccTitle:ie,getAccDescription:oe,setAccDescription:ae,addStyleClass:He,setCssClass:te,addDescription:Jt,setDiagramTitle:ce,getDiagramTitle:le};var As=s(t=>`
defs #statediagram-barbEnd {
    fill: ${t.transitionColor};
    stroke: ${t.transitionColor};
  }
g.stateGroup text {
  fill: ${t.nodeBorder};
  stroke: none;
  font-size: 10px;
}
g.stateGroup text {
  fill: ${t.textColor};
  stroke: none;
  font-size: 10px;

}
g.stateGroup .state-title {
  font-weight: bolder;
  fill: ${t.stateLabelColor};
}

g.stateGroup rect {
  fill: ${t.mainBkg};
  stroke: ${t.nodeBorder};
}

g.stateGroup line {
  stroke: ${t.lineColor};
  stroke-width: 1;
}

.transition {
  stroke: ${t.transitionColor};
  stroke-width: 1;
  fill: none;
}

.stateGroup .composit {
  fill: ${t.background};
  border-bottom: 1px
}

.stateGroup .alt-composit {
  fill: #e0e0e0;
  border-bottom: 1px
}

.state-note {
  stroke: ${t.noteBorderColor};
  fill: ${t.noteBkgColor};

  text {
    fill: ${t.noteTextColor};
    stroke: none;
    font-size: 10px;
  }
}

.stateLabel .box {
  stroke: none;
  stroke-width: 0;
  fill: ${t.mainBkg};
  opacity: 0.5;
}

.edgeLabel .label rect {
  fill: ${t.labelBackgroundColor};
  opacity: 0.5;
}
.edgeLabel {
  background-color: ${t.edgeLabelBackground};
  p {
    background-color: ${t.edgeLabelBackground};
  }
  rect {
    opacity: 0.5;
    background-color: ${t.edgeLabelBackground};
    fill: ${t.edgeLabelBackground};
  }
  text-align: center;
}
.edgeLabel .label text {
  fill: ${t.transitionLabelColor||t.tertiaryTextColor};
}
.label div .edgeLabel {
  color: ${t.transitionLabelColor||t.tertiaryTextColor};
}

.stateLabel text {
  fill: ${t.stateLabelColor};
  font-size: 10px;
  font-weight: bold;
}

.node circle.state-start {
  fill: ${t.specialStateColor};
  stroke: ${t.specialStateColor};
}

.node .fork-join {
  fill: ${t.specialStateColor};
  stroke: ${t.specialStateColor};
}

.node circle.state-end {
  fill: ${t.innerEndBackground};
  stroke: ${t.background};
  stroke-width: 1.5
}
.end-state-inner {
  fill: ${t.compositeBackground||t.background};
  // stroke: ${t.background};
  stroke-width: 1.5
}

.node rect {
  fill: ${t.stateBkg||t.mainBkg};
  stroke: ${t.stateBorder||t.nodeBorder};
  stroke-width: 1px;
}
.node polygon {
  fill: ${t.mainBkg};
  stroke: ${t.stateBorder||t.nodeBorder};;
  stroke-width: 1px;
}
#statediagram-barbEnd {
  fill: ${t.lineColor};
}

.statediagram-cluster rect {
  fill: ${t.compositeTitleBackground};
  stroke: ${t.stateBorder||t.nodeBorder};
  stroke-width: 1px;
}

.cluster-label, .nodeLabel {
  color: ${t.stateLabelColor};
  // line-height: 1;
}

.statediagram-cluster rect.outer {
  rx: 5px;
  ry: 5px;
}
.statediagram-state .divider {
  stroke: ${t.stateBorder||t.nodeBorder};
}

.statediagram-state .title-state {
  rx: 5px;
  ry: 5px;
}
.statediagram-cluster.statediagram-cluster .inner {
  fill: ${t.compositeBackground||t.background};
}
.statediagram-cluster.statediagram-cluster-alt .inner {
  fill: ${t.altBackground?t.altBackground:"#efefef"};
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
  fill: ${t.altBackground?t.altBackground:"#efefef"};
}

.note-edge {
  stroke-dasharray: 5;
}

.statediagram-note rect {
  fill: ${t.noteBkgColor};
  stroke: ${t.noteBorderColor};
  stroke-width: 1px;
  rx: 0;
  ry: 0;
}
.statediagram-note rect {
  fill: ${t.noteBkgColor};
  stroke: ${t.noteBorderColor};
  stroke-width: 1px;
  rx: 0;
  ry: 0;
}

.statediagram-note text {
  fill: ${t.noteTextColor};
}

.statediagram-note .nodeLabel {
  color: ${t.noteTextColor};
}
.statediagram .edgeLabel {
  color: red; // ${t.noteTextColor};
}

#dependencyStart, #dependencyEnd {
  fill: ${t.lineColor};
  stroke: ${t.lineColor};
  stroke-width: 1;
}

.statediagramTitleText {
  text-anchor: middle;
  font-size: 18px;
  fill: ${t.textColor};
}
`,"getStyles"),ar=As;export{Is as a,Bs as b,rr as c,ar as d};
