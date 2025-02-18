import{m as Ct}from"./chunk-AC3VT7B7.mjs";import{a as Qt}from"./chunk-TI4EEUUG.mjs";import{L as it,M as rt,P as st,Q as at,R as ot,S as ct,T as lt,U as ut,V as dt,X as ee,a as nt,b as ce,ba as ft,ca as ht,da as mt,ea as kt,fa as fe,ga as yt,ja as pt,ka as Ee,la as Me,ma as Ae,na as Le,oa as Ie,pa as gt,qa as bt,ra as xt,sa as Tt,ta as vt,ua as wt,va as _t,wa as Ye,xa as We,ya as Dt}from"./chunk-NQURTBEV.mjs";import"./chunk-6BY5RJGC.mjs";import{a as o,b as Se,e as oe}from"./chunk-GTKDMUJJ.mjs";var Et=Se((Ve,Oe)=>{"use strict";(function(e,t){typeof Ve=="object"&&typeof Oe<"u"?Oe.exports=t():typeof define=="function"&&define.amd?define(t):(e=typeof globalThis<"u"?globalThis:e||self).dayjs_plugin_isoWeek=t()})(Ve,function(){"use strict";var e="day";return function(t,r,i){var a=o(function(T){return T.add(4-T.isoWeekday(),e)},"a"),f=r.prototype;f.isoWeekYear=function(){return a(this).year()},f.isoWeek=function(T){if(!this.$utils().u(T))return this.add(7*(T-this.isoWeek()),e);var W,A,E,F,j=a(this),y=(W=this.isoWeekYear(),A=this.$u,E=(A?i.utc:i)().year(W).startOf("year"),F=4-E.isoWeekday(),E.isoWeekday()>4&&(F+=7),E.add(F,e));return j.diff(y,"week")+1},f.isoWeekday=function(T){return this.$utils().u(T)?this.day()||7:this.day(this.day()%7?T:T-7)};var m=f.startOf;f.startOf=function(T,W){var A=this.$utils(),E=!!A.u(W)||W;return A.p(T)==="isoweek"?E?this.date(this.date()-(this.isoWeekday()-1)).startOf("day"):this.date(this.date()-1-(this.isoWeekday()-1)+7).endOf("day"):m.bind(this)(T,W)}}})});var Mt=Se((Pe,ze)=>{"use strict";(function(e,t){typeof Pe=="object"&&typeof ze<"u"?ze.exports=t():typeof define=="function"&&define.amd?define(t):(e=typeof globalThis<"u"?globalThis:e||self).dayjs_plugin_customParseFormat=t()})(Pe,function(){"use strict";var e={LTS:"h:mm:ss A",LT:"h:mm A",L:"MM/DD/YYYY",LL:"MMMM D, YYYY",LLL:"MMMM D, YYYY h:mm A",LLLL:"dddd, MMMM D, YYYY h:mm A"},t=/(\[[^[]*\])|([-_:/.,()\s]+)|(A|a|YYYY|YY?|MM?M?M?|Do|DD?|hh?|HH?|mm?|ss?|S{1,3}|z|ZZ?)/g,r=/\d\d/,i=/\d\d?/,a=/\d*[^-_:/,()\s\d]+/,f={},m=o(function(y){return(y=+y)+(y>68?1900:2e3)},"s"),T=o(function(y){return function(_){this[y]=+_}},"a"),W=[/[+-]\d\d:?(\d\d)?|Z/,function(y){(this.zone||(this.zone={})).offset=function(_){if(!_||_==="Z")return 0;var g=_.match(/([+-]|\d\d)/g),I=60*g[1]+(+g[2]||0);return I===0?0:g[0]==="+"?-I:I}(y)}],A=o(function(y){var _=f[y];return _&&(_.indexOf?_:_.s.concat(_.f))},"h"),E=o(function(y,_){var g,I=f.meridiem;if(I){for(var z=1;z<=24;z+=1)if(y.indexOf(I(z,0,_))>-1){g=z>12;break}}else g=y===(_?"pm":"PM");return g},"u"),F={A:[a,function(y){this.afternoon=E(y,!1)}],a:[a,function(y){this.afternoon=E(y,!0)}],S:[/\d/,function(y){this.milliseconds=100*+y}],SS:[r,function(y){this.milliseconds=10*+y}],SSS:[/\d{3}/,function(y){this.milliseconds=+y}],s:[i,T("seconds")],ss:[i,T("seconds")],m:[i,T("minutes")],mm:[i,T("minutes")],H:[i,T("hours")],h:[i,T("hours")],HH:[i,T("hours")],hh:[i,T("hours")],D:[i,T("day")],DD:[r,T("day")],Do:[a,function(y){var _=f.ordinal,g=y.match(/\d+/);if(this.day=g[0],_)for(var I=1;I<=31;I+=1)_(I).replace(/\[|\]/g,"")===y&&(this.day=I)}],M:[i,T("month")],MM:[r,T("month")],MMM:[a,function(y){var _=A("months"),g=(A("monthsShort")||_.map(function(I){return I.slice(0,3)})).indexOf(y)+1;if(g<1)throw new Error;this.month=g%12||g}],MMMM:[a,function(y){var _=A("months").indexOf(y)+1;if(_<1)throw new Error;this.month=_%12||_}],Y:[/[+-]?\d+/,T("year")],YY:[r,function(y){this.year=m(y)}],YYYY:[/\d{4}/,T("year")],Z:W,ZZ:W};function j(y){var _,g;_=y,g=f&&f.formats;for(var I=(y=_.replace(/(\[[^\]]+])|(LTS?|l{1,4}|L{1,4})/g,function(q,p,v){var b=v&&v.toUpperCase();return p||g[v]||e[v]||g[b].replace(/(\[[^\]]+])|(MMMM|MM|DD|dddd)/g,function(w,k,D){return k||D.slice(1)})})).match(t),z=I.length,N=0;N<z;N+=1){var Q=I[N],X=F[Q],R=X&&X[0],B=X&&X[1];I[N]=B?{regex:R,parser:B}:Q.replace(/^\[|\]$/g,"")}return function(q){for(var p={},v=0,b=0;v<z;v+=1){var w=I[v];if(typeof w=="string")b+=w.length;else{var k=w.regex,D=w.parser,c=q.slice(b),l=k.exec(c)[0];D.call(p,l),q=q.replace(l,"")}}return function(h){var u=h.afternoon;if(u!==void 0){var x=h.hours;u?x<12&&(h.hours+=12):x===12&&(h.hours=0),delete h.afternoon}}(p),p}}return o(j,"c"),function(y,_,g){g.p.customParseFormat=!0,y&&y.parseTwoDigitYear&&(m=y.parseTwoDigitYear);var I=_.prototype,z=I.parse;I.parse=function(N){var Q=N.date,X=N.utc,R=N.args;this.$u=X;var B=R[1];if(typeof B=="string"){var q=R[2]===!0,p=R[3]===!0,v=q||p,b=R[2];p&&(b=R[2]),f=this.$locale(),!q&&b&&(f=g.Ls[b]),this.$d=function(c,l,h){try{if(["x","X"].indexOf(l)>-1)return new Date((l==="X"?1e3:1)*c);var u=j(l)(c),x=u.year,s=u.month,d=u.day,n=u.hours,M=u.minutes,C=u.seconds,S=u.milliseconds,O=u.zone,L=new Date,te=d||(x||s?1:L.getDate()),Y=x||L.getFullYear(),U=0;x&&!s||(U=s>0?s-1:L.getMonth());var ne=n||0,ie=M||0,de=C||0,ye=S||0;return O?new Date(Date.UTC(Y,U,te,ne,ie,de,ye+60*O.offset*1e3)):h?new Date(Date.UTC(Y,U,te,ne,ie,de,ye)):new Date(Y,U,te,ne,ie,de,ye)}catch{return new Date("")}}(Q,B,X),this.init(),b&&b!==!0&&(this.$L=this.locale(b).$L),v&&Q!=this.format(B)&&(this.$d=new Date("")),f={}}else if(B instanceof Array)for(var w=B.length,k=1;k<=w;k+=1){R[1]=B[k-1];var D=g.apply(this,R);if(D.isValid()){this.$d=D.$d,this.$L=D.$L,this.init();break}k===w&&(this.$d=new Date(""))}else z.call(this,N)}}})});var At=Se((Ne,Re)=>{"use strict";(function(e,t){typeof Ne=="object"&&typeof Re<"u"?Re.exports=t():typeof define=="function"&&define.amd?define(t):(e=typeof globalThis<"u"?globalThis:e||self).dayjs_plugin_advancedFormat=t()})(Ne,function(){"use strict";return function(e,t){var r=t.prototype,i=r.format;r.format=function(a){var f=this,m=this.$locale();if(!this.isValid())return i.bind(this)(a);var T=this.$utils(),W=(a||"YYYY-MM-DDTHH:mm:ssZ").replace(/\[([^\]]+)]|Q|wo|ww|w|WW|W|zzz|z|gggg|GGGG|Do|X|x|k{1,2}|S/g,function(A){switch(A){case"Q":return Math.ceil((f.$M+1)/3);case"Do":return m.ordinal(f.$D);case"gggg":return f.weekYear();case"GGGG":return f.isoWeekYear();case"wo":return m.ordinal(f.week(),"W");case"w":case"ww":return T.s(f.week(),A==="w"?1:2,"0");case"W":case"WW":return T.s(f.isoWeek(),A==="W"?1:2,"0");case"k":case"kk":return T.s(String(f.$H===0?24:f.$H),A==="k"?1:2,"0");case"X":return Math.floor(f.$d.getTime()/1e3);case"x":return f.$d.getTime();case"z":return"["+f.offsetName()+"]";case"zzz":return"["+f.offsetName("long")+"]";default:return A}});return i.bind(this)(W)}}})});var Fe=function(){var e=o(function(D,c,l,h){for(l=l||{},h=D.length;h--;l[D[h]]=c);return l},"o"),t=[6,8,10,12,13,14,15,16,17,18,20,21,22,23,24,25,26,27,28,29,30,31,33,35,36,38,40],r=[1,26],i=[1,27],a=[1,28],f=[1,29],m=[1,30],T=[1,31],W=[1,32],A=[1,33],E=[1,34],F=[1,9],j=[1,10],y=[1,11],_=[1,12],g=[1,13],I=[1,14],z=[1,15],N=[1,16],Q=[1,19],X=[1,20],R=[1,21],B=[1,22],q=[1,23],p=[1,25],v=[1,35],b={trace:o(function(){},"trace"),yy:{},symbols_:{error:2,start:3,gantt:4,document:5,EOF:6,line:7,SPACE:8,statement:9,NL:10,weekday:11,weekday_monday:12,weekday_tuesday:13,weekday_wednesday:14,weekday_thursday:15,weekday_friday:16,weekday_saturday:17,weekday_sunday:18,weekend:19,weekend_friday:20,weekend_saturday:21,dateFormat:22,inclusiveEndDates:23,topAxis:24,axisFormat:25,tickInterval:26,excludes:27,includes:28,todayMarker:29,title:30,acc_title:31,acc_title_value:32,acc_descr:33,acc_descr_value:34,acc_descr_multiline_value:35,section:36,clickStatement:37,taskTxt:38,taskData:39,click:40,callbackname:41,callbackargs:42,href:43,clickStatementDebug:44,$accept:0,$end:1},terminals_:{2:"error",4:"gantt",6:"EOF",8:"SPACE",10:"NL",12:"weekday_monday",13:"weekday_tuesday",14:"weekday_wednesday",15:"weekday_thursday",16:"weekday_friday",17:"weekday_saturday",18:"weekday_sunday",20:"weekend_friday",21:"weekend_saturday",22:"dateFormat",23:"inclusiveEndDates",24:"topAxis",25:"axisFormat",26:"tickInterval",27:"excludes",28:"includes",29:"todayMarker",30:"title",31:"acc_title",32:"acc_title_value",33:"acc_descr",34:"acc_descr_value",35:"acc_descr_multiline_value",36:"section",38:"taskTxt",39:"taskData",40:"click",41:"callbackname",42:"callbackargs",43:"href"},productions_:[0,[3,3],[5,0],[5,2],[7,2],[7,1],[7,1],[7,1],[11,1],[11,1],[11,1],[11,1],[11,1],[11,1],[11,1],[19,1],[19,1],[9,1],[9,1],[9,1],[9,1],[9,1],[9,1],[9,1],[9,1],[9,1],[9,1],[9,1],[9,2],[9,2],[9,1],[9,1],[9,1],[9,2],[37,2],[37,3],[37,3],[37,4],[37,3],[37,4],[37,2],[44,2],[44,3],[44,3],[44,4],[44,3],[44,4],[44,2]],performAction:o(function(c,l,h,u,x,s,d){var n=s.length-1;switch(x){case 1:return s[n-1];case 2:this.$=[];break;case 3:s[n-1].push(s[n]),this.$=s[n-1];break;case 4:case 5:this.$=s[n];break;case 6:case 7:this.$=[];break;case 8:u.setWeekday("monday");break;case 9:u.setWeekday("tuesday");break;case 10:u.setWeekday("wednesday");break;case 11:u.setWeekday("thursday");break;case 12:u.setWeekday("friday");break;case 13:u.setWeekday("saturday");break;case 14:u.setWeekday("sunday");break;case 15:u.setWeekend("friday");break;case 16:u.setWeekend("saturday");break;case 17:u.setDateFormat(s[n].substr(11)),this.$=s[n].substr(11);break;case 18:u.enableInclusiveEndDates(),this.$=s[n].substr(18);break;case 19:u.TopAxis(),this.$=s[n].substr(8);break;case 20:u.setAxisFormat(s[n].substr(11)),this.$=s[n].substr(11);break;case 21:u.setTickInterval(s[n].substr(13)),this.$=s[n].substr(13);break;case 22:u.setExcludes(s[n].substr(9)),this.$=s[n].substr(9);break;case 23:u.setIncludes(s[n].substr(9)),this.$=s[n].substr(9);break;case 24:u.setTodayMarker(s[n].substr(12)),this.$=s[n].substr(12);break;case 27:u.setDiagramTitle(s[n].substr(6)),this.$=s[n].substr(6);break;case 28:this.$=s[n].trim(),u.setAccTitle(this.$);break;case 29:case 30:this.$=s[n].trim(),u.setAccDescription(this.$);break;case 31:u.addSection(s[n].substr(8)),this.$=s[n].substr(8);break;case 33:u.addTask(s[n-1],s[n]),this.$="task";break;case 34:this.$=s[n-1],u.setClickEvent(s[n-1],s[n],null);break;case 35:this.$=s[n-2],u.setClickEvent(s[n-2],s[n-1],s[n]);break;case 36:this.$=s[n-2],u.setClickEvent(s[n-2],s[n-1],null),u.setLink(s[n-2],s[n]);break;case 37:this.$=s[n-3],u.setClickEvent(s[n-3],s[n-2],s[n-1]),u.setLink(s[n-3],s[n]);break;case 38:this.$=s[n-2],u.setClickEvent(s[n-2],s[n],null),u.setLink(s[n-2],s[n-1]);break;case 39:this.$=s[n-3],u.setClickEvent(s[n-3],s[n-1],s[n]),u.setLink(s[n-3],s[n-2]);break;case 40:this.$=s[n-1],u.setLink(s[n-1],s[n]);break;case 41:case 47:this.$=s[n-1]+" "+s[n];break;case 42:case 43:case 45:this.$=s[n-2]+" "+s[n-1]+" "+s[n];break;case 44:case 46:this.$=s[n-3]+" "+s[n-2]+" "+s[n-1]+" "+s[n];break}},"anonymous"),table:[{3:1,4:[1,2]},{1:[3]},e(t,[2,2],{5:3}),{6:[1,4],7:5,8:[1,6],9:7,10:[1,8],11:17,12:r,13:i,14:a,15:f,16:m,17:T,18:W,19:18,20:A,21:E,22:F,23:j,24:y,25:_,26:g,27:I,28:z,29:N,30:Q,31:X,33:R,35:B,36:q,37:24,38:p,40:v},e(t,[2,7],{1:[2,1]}),e(t,[2,3]),{9:36,11:17,12:r,13:i,14:a,15:f,16:m,17:T,18:W,19:18,20:A,21:E,22:F,23:j,24:y,25:_,26:g,27:I,28:z,29:N,30:Q,31:X,33:R,35:B,36:q,37:24,38:p,40:v},e(t,[2,5]),e(t,[2,6]),e(t,[2,17]),e(t,[2,18]),e(t,[2,19]),e(t,[2,20]),e(t,[2,21]),e(t,[2,22]),e(t,[2,23]),e(t,[2,24]),e(t,[2,25]),e(t,[2,26]),e(t,[2,27]),{32:[1,37]},{34:[1,38]},e(t,[2,30]),e(t,[2,31]),e(t,[2,32]),{39:[1,39]},e(t,[2,8]),e(t,[2,9]),e(t,[2,10]),e(t,[2,11]),e(t,[2,12]),e(t,[2,13]),e(t,[2,14]),e(t,[2,15]),e(t,[2,16]),{41:[1,40],43:[1,41]},e(t,[2,4]),e(t,[2,28]),e(t,[2,29]),e(t,[2,33]),e(t,[2,34],{42:[1,42],43:[1,43]}),e(t,[2,40],{41:[1,44]}),e(t,[2,35],{43:[1,45]}),e(t,[2,36]),e(t,[2,38],{42:[1,46]}),e(t,[2,37]),e(t,[2,39])],defaultActions:{},parseError:o(function(c,l){if(l.recoverable)this.trace(c);else{var h=new Error(c);throw h.hash=l,h}},"parseError"),parse:o(function(c){var l=this,h=[0],u=[],x=[null],s=[],d=this.table,n="",M=0,C=0,S=0,O=2,L=1,te=s.slice.call(arguments,1),Y=Object.create(this.lexer),U={yy:{}};for(var ne in this.yy)Object.prototype.hasOwnProperty.call(this.yy,ne)&&(U.yy[ne]=this.yy[ne]);Y.setInput(c,U.yy),U.yy.lexer=Y,U.yy.parser=this,typeof Y.yylloc>"u"&&(Y.yylloc={});var ie=Y.yylloc;s.push(ie);var de=Y.options&&Y.options.ranges;typeof U.yy.parseError=="function"?this.parseError=U.yy.parseError:this.parseError=Object.getPrototypeOf(this).parseError;function ye(G){h.length=h.length-2*G,x.length=x.length-G,s.length=s.length-G}o(ye,"popStack");function et(){var G;return G=u.pop()||Y.lex()||L,typeof G!="number"&&(G instanceof Array&&(u=G,G=u.pop()),G=l.symbols_[G]||G),G}o(et,"lex");for(var P,_e,re,Z,On,De,ae={},pe,J,tt,ge;;){if(re=h[h.length-1],this.defaultActions[re]?Z=this.defaultActions[re]:((P===null||typeof P>"u")&&(P=et()),Z=d[re]&&d[re][P]),typeof Z>"u"||!Z.length||!Z[0]){var Ce="";ge=[];for(pe in d[re])this.terminals_[pe]&&pe>O&&ge.push("'"+this.terminals_[pe]+"'");Y.showPosition?Ce="Parse error on line "+(M+1)+`:
`+Y.showPosition()+`
Expecting `+ge.join(", ")+", got '"+(this.terminals_[P]||P)+"'":Ce="Parse error on line "+(M+1)+": Unexpected "+(P==L?"end of input":"'"+(this.terminals_[P]||P)+"'"),this.parseError(Ce,{text:Y.match,token:this.terminals_[P]||P,line:Y.yylineno,loc:ie,expected:ge})}if(Z[0]instanceof Array&&Z.length>1)throw new Error("Parse Error: multiple actions possible at state: "+re+", token: "+P);switch(Z[0]){case 1:h.push(P),x.push(Y.yytext),s.push(Y.yylloc),h.push(Z[1]),P=null,_e?(P=_e,_e=null):(C=Y.yyleng,n=Y.yytext,M=Y.yylineno,ie=Y.yylloc,S>0&&S--);break;case 2:if(J=this.productions_[Z[1]][1],ae.$=x[x.length-J],ae._$={first_line:s[s.length-(J||1)].first_line,last_line:s[s.length-1].last_line,first_column:s[s.length-(J||1)].first_column,last_column:s[s.length-1].last_column},de&&(ae._$.range=[s[s.length-(J||1)].range[0],s[s.length-1].range[1]]),De=this.performAction.apply(ae,[n,C,M,U.yy,Z[1],x,s].concat(te)),typeof De<"u")return De;J&&(h=h.slice(0,-1*J*2),x=x.slice(0,-1*J),s=s.slice(0,-1*J)),h.push(this.productions_[Z[1]][0]),x.push(ae.$),s.push(ae._$),tt=d[h[h.length-2]][h[h.length-1]],h.push(tt);break;case 3:return!0}}return!0},"parse")},w=function(){var D={EOF:1,parseError:o(function(l,h){if(this.yy.parser)this.yy.parser.parseError(l,h);else throw new Error(l)},"parseError"),setInput:o(function(c,l){return this.yy=l||this.yy||{},this._input=c,this._more=this._backtrack=this.done=!1,this.yylineno=this.yyleng=0,this.yytext=this.matched=this.match="",this.conditionStack=["INITIAL"],this.yylloc={first_line:1,first_column:0,last_line:1,last_column:0},this.options.ranges&&(this.yylloc.range=[0,0]),this.offset=0,this},"setInput"),input:o(function(){var c=this._input[0];this.yytext+=c,this.yyleng++,this.offset++,this.match+=c,this.matched+=c;var l=c.match(/(?:\r\n?|\n).*/g);return l?(this.yylineno++,this.yylloc.last_line++):this.yylloc.last_column++,this.options.ranges&&this.yylloc.range[1]++,this._input=this._input.slice(1),c},"input"),unput:o(function(c){var l=c.length,h=c.split(/(?:\r\n?|\n)/g);this._input=c+this._input,this.yytext=this.yytext.substr(0,this.yytext.length-l),this.offset-=l;var u=this.match.split(/(?:\r\n?|\n)/g);this.match=this.match.substr(0,this.match.length-1),this.matched=this.matched.substr(0,this.matched.length-1),h.length-1&&(this.yylineno-=h.length-1);var x=this.yylloc.range;return this.yylloc={first_line:this.yylloc.first_line,last_line:this.yylineno+1,first_column:this.yylloc.first_column,last_column:h?(h.length===u.length?this.yylloc.first_column:0)+u[u.length-h.length].length-h[0].length:this.yylloc.first_column-l},this.options.ranges&&(this.yylloc.range=[x[0],x[0]+this.yyleng-l]),this.yyleng=this.yytext.length,this},"unput"),more:o(function(){return this._more=!0,this},"more"),reject:o(function(){if(this.options.backtrack_lexer)this._backtrack=!0;else return this.parseError("Lexical error on line "+(this.yylineno+1)+`. You can only invoke reject() in the lexer when the lexer is of the backtracking persuasion (options.backtrack_lexer = true).
`+this.showPosition(),{text:"",token:null,line:this.yylineno});return this},"reject"),less:o(function(c){this.unput(this.match.slice(c))},"less"),pastInput:o(function(){var c=this.matched.substr(0,this.matched.length-this.match.length);return(c.length>20?"...":"")+c.substr(-20).replace(/\n/g,"")},"pastInput"),upcomingInput:o(function(){var c=this.match;return c.length<20&&(c+=this._input.substr(0,20-c.length)),(c.substr(0,20)+(c.length>20?"...":"")).replace(/\n/g,"")},"upcomingInput"),showPosition:o(function(){var c=this.pastInput(),l=new Array(c.length+1).join("-");return c+this.upcomingInput()+`
`+l+"^"},"showPosition"),test_match:o(function(c,l){var h,u,x;if(this.options.backtrack_lexer&&(x={yylineno:this.yylineno,yylloc:{first_line:this.yylloc.first_line,last_line:this.last_line,first_column:this.yylloc.first_column,last_column:this.yylloc.last_column},yytext:this.yytext,match:this.match,matches:this.matches,matched:this.matched,yyleng:this.yyleng,offset:this.offset,_more:this._more,_input:this._input,yy:this.yy,conditionStack:this.conditionStack.slice(0),done:this.done},this.options.ranges&&(x.yylloc.range=this.yylloc.range.slice(0))),u=c[0].match(/(?:\r\n?|\n).*/g),u&&(this.yylineno+=u.length),this.yylloc={first_line:this.yylloc.last_line,last_line:this.yylineno+1,first_column:this.yylloc.last_column,last_column:u?u[u.length-1].length-u[u.length-1].match(/\r?\n?/)[0].length:this.yylloc.last_column+c[0].length},this.yytext+=c[0],this.match+=c[0],this.matches=c,this.yyleng=this.yytext.length,this.options.ranges&&(this.yylloc.range=[this.offset,this.offset+=this.yyleng]),this._more=!1,this._backtrack=!1,this._input=this._input.slice(c[0].length),this.matched+=c[0],h=this.performAction.call(this,this.yy,this,l,this.conditionStack[this.conditionStack.length-1]),this.done&&this._input&&(this.done=!1),h)return h;if(this._backtrack){for(var s in x)this[s]=x[s];return!1}return!1},"test_match"),next:o(function(){if(this.done)return this.EOF;this._input||(this.done=!0);var c,l,h,u;this._more||(this.yytext="",this.match="");for(var x=this._currentRules(),s=0;s<x.length;s++)if(h=this._input.match(this.rules[x[s]]),h&&(!l||h[0].length>l[0].length)){if(l=h,u=s,this.options.backtrack_lexer){if(c=this.test_match(h,x[s]),c!==!1)return c;if(this._backtrack){l=!1;continue}else return!1}else if(!this.options.flex)break}return l?(c=this.test_match(l,x[u]),c!==!1?c:!1):this._input===""?this.EOF:this.parseError("Lexical error on line "+(this.yylineno+1)+`. Unrecognized text.
`+this.showPosition(),{text:"",token:null,line:this.yylineno})},"next"),lex:o(function(){var l=this.next();return l||this.lex()},"lex"),begin:o(function(l){this.conditionStack.push(l)},"begin"),popState:o(function(){var l=this.conditionStack.length-1;return l>0?this.conditionStack.pop():this.conditionStack[0]},"popState"),_currentRules:o(function(){return this.conditionStack.length&&this.conditionStack[this.conditionStack.length-1]?this.conditions[this.conditionStack[this.conditionStack.length-1]].rules:this.conditions.INITIAL.rules},"_currentRules"),topState:o(function(l){return l=this.conditionStack.length-1-Math.abs(l||0),l>=0?this.conditionStack[l]:"INITIAL"},"topState"),pushState:o(function(l){this.begin(l)},"pushState"),stateStackSize:o(function(){return this.conditionStack.length},"stateStackSize"),options:{"case-insensitive":!0},performAction:o(function(l,h,u,x){var s=x;switch(u){case 0:return this.begin("open_directive"),"open_directive";break;case 1:return this.begin("acc_title"),31;break;case 2:return this.popState(),"acc_title_value";break;case 3:return this.begin("acc_descr"),33;break;case 4:return this.popState(),"acc_descr_value";break;case 5:this.begin("acc_descr_multiline");break;case 6:this.popState();break;case 7:return"acc_descr_multiline_value";case 8:break;case 9:break;case 10:break;case 11:return 10;case 12:break;case 13:break;case 14:this.begin("href");break;case 15:this.popState();break;case 16:return 43;case 17:this.begin("callbackname");break;case 18:this.popState();break;case 19:this.popState(),this.begin("callbackargs");break;case 20:return 41;case 21:this.popState();break;case 22:return 42;case 23:this.begin("click");break;case 24:this.popState();break;case 25:return 40;case 26:return 4;case 27:return 22;case 28:return 23;case 29:return 24;case 30:return 25;case 31:return 26;case 32:return 28;case 33:return 27;case 34:return 29;case 35:return 12;case 36:return 13;case 37:return 14;case 38:return 15;case 39:return 16;case 40:return 17;case 41:return 18;case 42:return 20;case 43:return 21;case 44:return"date";case 45:return 30;case 46:return"accDescription";case 47:return 36;case 48:return 38;case 49:return 39;case 50:return":";case 51:return 6;case 52:return"INVALID"}},"anonymous"),rules:[/^(?:%%\{)/i,/^(?:accTitle\s*:\s*)/i,/^(?:(?!\n||)*[^\n]*)/i,/^(?:accDescr\s*:\s*)/i,/^(?:(?!\n||)*[^\n]*)/i,/^(?:accDescr\s*\{\s*)/i,/^(?:[\}])/i,/^(?:[^\}]*)/i,/^(?:%%(?!\{)*[^\n]*)/i,/^(?:[^\}]%%*[^\n]*)/i,/^(?:%%*[^\n]*[\n]*)/i,/^(?:[\n]+)/i,/^(?:\s+)/i,/^(?:%[^\n]*)/i,/^(?:href[\s]+["])/i,/^(?:["])/i,/^(?:[^"]*)/i,/^(?:call[\s]+)/i,/^(?:\([\s]*\))/i,/^(?:\()/i,/^(?:[^(]*)/i,/^(?:\))/i,/^(?:[^)]*)/i,/^(?:click[\s]+)/i,/^(?:[\s\n])/i,/^(?:[^\s\n]*)/i,/^(?:gantt\b)/i,/^(?:dateFormat\s[^#\n;]+)/i,/^(?:inclusiveEndDates\b)/i,/^(?:topAxis\b)/i,/^(?:axisFormat\s[^#\n;]+)/i,/^(?:tickInterval\s[^#\n;]+)/i,/^(?:includes\s[^#\n;]+)/i,/^(?:excludes\s[^#\n;]+)/i,/^(?:todayMarker\s[^\n;]+)/i,/^(?:weekday\s+monday\b)/i,/^(?:weekday\s+tuesday\b)/i,/^(?:weekday\s+wednesday\b)/i,/^(?:weekday\s+thursday\b)/i,/^(?:weekday\s+friday\b)/i,/^(?:weekday\s+saturday\b)/i,/^(?:weekday\s+sunday\b)/i,/^(?:weekend\s+friday\b)/i,/^(?:weekend\s+saturday\b)/i,/^(?:\d\d\d\d-\d\d-\d\d\b)/i,/^(?:title\s[^\n]+)/i,/^(?:accDescription\s[^#\n;]+)/i,/^(?:section\s[^\n]+)/i,/^(?:[^:\n]+)/i,/^(?::[^#\n;]+)/i,/^(?::)/i,/^(?:$)/i,/^(?:.)/i],conditions:{acc_descr_multiline:{rules:[6,7],inclusive:!1},acc_descr:{rules:[4],inclusive:!1},acc_title:{rules:[2],inclusive:!1},callbackargs:{rules:[21,22],inclusive:!1},callbackname:{rules:[18,19,20],inclusive:!1},href:{rules:[15,16],inclusive:!1},click:{rules:[24,25],inclusive:!1},INITIAL:{rules:[0,1,3,5,8,9,10,11,12,13,14,17,23,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52],inclusive:!0}}};return D}();b.lexer=w;function k(){this.yy={}}return o(k,"Parser"),k.prototype=b,b.Parser=k,new k}();Fe.parser=Fe;var St=Fe;var Yt=oe(Qt(),1),H=oe(nt(),1),Wt=oe(Et(),1),Ft=oe(Mt(),1),Vt=oe(At(),1);H.default.extend(Wt.default);H.default.extend(Ft.default);H.default.extend(Vt.default);var Lt={friday:5,saturday:6},K="",He="",Xe,qe="",he=[],me=[],Ue=new Map,Ze=[],Te=[],ue="",Qe="",Ot=["active","done","crit","milestone"],Ke=[],ke=!1,Je=!1,$e="sunday",ve="saturday",Be=0,Kt=o(function(){Ze=[],Te=[],ue="",Ke=[],be=0,Ge=void 0,xe=void 0,V=[],K="",He="",Qe="",Xe=void 0,qe="",he=[],me=[],ke=!1,Je=!1,Be=0,Ue=new Map,st(),$e="sunday",ve="saturday"},"clear"),Jt=o(function(e){He=e},"setAxisFormat"),$t=o(function(){return He},"getAxisFormat"),en=o(function(e){Xe=e},"setTickInterval"),tn=o(function(){return Xe},"getTickInterval"),nn=o(function(e){qe=e},"setTodayMarker"),rn=o(function(){return qe},"getTodayMarker"),sn=o(function(e){K=e},"setDateFormat"),an=o(function(){ke=!0},"enableInclusiveEndDates"),on=o(function(){return ke},"endDatesAreInclusive"),cn=o(function(){Je=!0},"enableTopAxis"),ln=o(function(){return Je},"topAxisEnabled"),un=o(function(e){Qe=e},"setDisplayMode"),dn=o(function(){return Qe},"getDisplayMode"),fn=o(function(){return K},"getDateFormat"),hn=o(function(e){he=e.toLowerCase().split(/[\s,]+/)},"setIncludes"),mn=o(function(){return he},"getIncludes"),kn=o(function(e){me=e.toLowerCase().split(/[\s,]+/)},"setExcludes"),yn=o(function(){return me},"getExcludes"),pn=o(function(){return Ue},"getLinks"),gn=o(function(e){ue=e,Ze.push(e)},"addSection"),bn=o(function(){return Ze},"getSections"),xn=o(function(){let e=It(),t=10,r=0;for(;!e&&r<t;)e=It(),r++;return Te=V,Te},"getTasks"),Pt=o(function(e,t,r,i){return i.includes(e.format(t.trim()))?!1:r.includes("weekends")&&(e.isoWeekday()===Lt[ve]||e.isoWeekday()===Lt[ve]+1)||r.includes(e.format("dddd").toLowerCase())?!0:r.includes(e.format(t.trim()))},"isInvalidDate"),Tn=o(function(e){$e=e},"setWeekday"),vn=o(function(){return $e},"getWeekday"),wn=o(function(e){ve=e},"setWeekend"),zt=o(function(e,t,r,i){if(!r.length||e.manualEndTime)return;let a;e.startTime instanceof Date?a=(0,H.default)(e.startTime):a=(0,H.default)(e.startTime,t,!0),a=a.add(1,"d");let f;e.endTime instanceof Date?f=(0,H.default)(e.endTime):f=(0,H.default)(e.endTime,t,!0);let[m,T]=_n(a,f,t,r,i);e.endTime=m.toDate(),e.renderEndTime=T},"checkTaskDates"),_n=o(function(e,t,r,i,a){let f=!1,m=null;for(;e<=t;)f||(m=t.toDate()),f=Pt(e,r,i,a),f&&(t=t.add(1,"d")),e=e.add(1,"d");return[t,m]},"fixTaskDates"),je=o(function(e,t,r){r=r.trim();let a=/^after\s+(?<ids>[\d\w- ]+)/.exec(r);if(a!==null){let m=null;for(let W of a.groups.ids.split(" ")){let A=se(W);A!==void 0&&(!m||A.endTime>m.endTime)&&(m=A)}if(m)return m.endTime;let T=new Date;return T.setHours(0,0,0,0),T}let f=(0,H.default)(r,t.trim(),!0);if(f.isValid())return f.toDate();{ce.debug("Invalid date:"+r),ce.debug("With date format:"+t.trim());let m=new Date(r);if(m===void 0||isNaN(m.getTime())||m.getFullYear()<-1e4||m.getFullYear()>1e4)throw new Error("Invalid date:"+r);return m}},"getStartDate"),Nt=o(function(e){let t=/^(\d+(?:\.\d+)?)([Mdhmswy]|ms)$/.exec(e.trim());return t!==null?[Number.parseFloat(t[1]),t[2]]:[NaN,"ms"]},"parseDuration"),Rt=o(function(e,t,r,i=!1){r=r.trim();let f=/^until\s+(?<ids>[\d\w- ]+)/.exec(r);if(f!==null){let E=null;for(let j of f.groups.ids.split(" ")){let y=se(j);y!==void 0&&(!E||y.startTime<E.startTime)&&(E=y)}if(E)return E.startTime;let F=new Date;return F.setHours(0,0,0,0),F}let m=(0,H.default)(r,t.trim(),!0);if(m.isValid())return i&&(m=m.add(1,"d")),m.toDate();let T=(0,H.default)(e),[W,A]=Nt(r);if(!Number.isNaN(W)){let E=T.add(W,A);E.isValid()&&(T=E)}return T.toDate()},"getEndDate"),be=0,le=o(function(e){return e===void 0?(be=be+1,"task"+be):e},"parseId"),Dn=o(function(e,t){let r;t.substr(0,1)===":"?r=t.substr(1,t.length):r=t;let i=r.split(","),a={};Xt(i,a,Ot);for(let m=0;m<i.length;m++)i[m]=i[m].trim();let f="";switch(i.length){case 1:a.id=le(),a.startTime=e.endTime,f=i[0];break;case 2:a.id=le(),a.startTime=je(void 0,K,i[0]),f=i[1];break;case 3:a.id=le(i[0]),a.startTime=je(void 0,K,i[1]),f=i[2];break;default:}return f&&(a.endTime=Rt(a.startTime,K,f,ke),a.manualEndTime=(0,H.default)(f,"YYYY-MM-DD",!0).isValid(),zt(a,K,me,he)),a},"compileData"),Cn=o(function(e,t){let r;t.substr(0,1)===":"?r=t.substr(1,t.length):r=t;let i=r.split(","),a={};Xt(i,a,Ot);for(let f=0;f<i.length;f++)i[f]=i[f].trim();switch(i.length){case 1:a.id=le(),a.startTime={type:"prevTaskEnd",id:e},a.endTime={data:i[0]};break;case 2:a.id=le(),a.startTime={type:"getStartDate",startData:i[0]},a.endTime={data:i[1]};break;case 3:a.id=le(i[0]),a.startTime={type:"getStartDate",startData:i[1]},a.endTime={data:i[2]};break;default:}return a},"parseData"),Ge,xe,V=[],Bt={},Sn=o(function(e,t){let r={section:ue,type:ue,processed:!1,manualEndTime:!1,renderEndTime:null,raw:{data:t},task:e,classes:[]},i=Cn(xe,t);r.raw.startTime=i.startTime,r.raw.endTime=i.endTime,r.id=i.id,r.prevTaskId=xe,r.active=i.active,r.done=i.done,r.crit=i.crit,r.milestone=i.milestone,r.order=Be,Be++;let a=V.push(r);xe=r.id,Bt[r.id]=a-1},"addTask"),se=o(function(e){let t=Bt[e];return V[t]},"findTaskById"),En=o(function(e,t){let r={section:ue,type:ue,description:e,task:e,classes:[]},i=Dn(Ge,t);r.startTime=i.startTime,r.endTime=i.endTime,r.id=i.id,r.active=i.active,r.done=i.done,r.crit=i.crit,r.milestone=i.milestone,Ge=r,Te.push(r)},"addTaskOrg"),It=o(function(){let e=o(function(r){let i=V[r],a="";switch(V[r].raw.startTime.type){case"prevTaskEnd":{let f=se(i.prevTaskId);i.startTime=f.endTime;break}case"getStartDate":a=je(void 0,K,V[r].raw.startTime.startData),a&&(V[r].startTime=a);break}return V[r].startTime&&(V[r].endTime=Rt(V[r].startTime,K,V[r].raw.endTime.data,ke),V[r].endTime&&(V[r].processed=!0,V[r].manualEndTime=(0,H.default)(V[r].raw.endTime.data,"YYYY-MM-DD",!0).isValid(),zt(V[r],K,me,he))),V[r].processed},"compileTask"),t=!0;for(let[r,i]of V.entries())e(r),t=t&&i.processed;return t},"compileTasks"),Mn=o(function(e,t){let r=t;ee().securityLevel!=="loose"&&(r=(0,Yt.sanitizeUrl)(t)),e.split(",").forEach(function(i){se(i)!==void 0&&(Gt(i,()=>{window.open(r,"_self")}),Ue.set(i,r))}),jt(e,"clickable")},"setLink"),jt=o(function(e,t){e.split(",").forEach(function(r){let i=se(r);i!==void 0&&i.classes.push(t)})},"setClass"),An=o(function(e,t,r){if(ee().securityLevel!=="loose"||t===void 0)return;let i=[];if(typeof r=="string"){i=r.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/);for(let f=0;f<i.length;f++){let m=i[f].trim();m.startsWith('"')&&m.endsWith('"')&&(m=m.substr(1,m.length-2)),i[f]=m}}i.length===0&&i.push(e),se(e)!==void 0&&Gt(e,()=>{Ct.runFunc(t,...i)})},"setClickFun"),Gt=o(function(e,t){Ke.push(function(){let r=document.querySelector(`[id="${e}"]`);r!==null&&r.addEventListener("click",function(){t()})},function(){let r=document.querySelector(`[id="${e}-text"]`);r!==null&&r.addEventListener("click",function(){t()})})},"pushFun"),Ln=o(function(e,t,r){e.split(",").forEach(function(i){An(i,t,r)}),jt(e,"clickable")},"setClickEvent"),In=o(function(e){Ke.forEach(function(t){t(e)})},"bindFunctions"),Ht={getConfig:o(()=>ee().gantt,"getConfig"),clear:Kt,setDateFormat:sn,getDateFormat:fn,enableInclusiveEndDates:an,endDatesAreInclusive:on,enableTopAxis:cn,topAxisEnabled:ln,setAxisFormat:Jt,getAxisFormat:$t,setTickInterval:en,getTickInterval:tn,setTodayMarker:nn,getTodayMarker:rn,setAccTitle:at,getAccTitle:ot,setDiagramTitle:ut,getDiagramTitle:dt,setDisplayMode:un,getDisplayMode:dn,setAccDescription:ct,getAccDescription:lt,addSection:gn,getSections:bn,getTasks:xn,addTask:Sn,findTaskById:se,addTaskOrg:En,setIncludes:hn,getIncludes:mn,setExcludes:kn,getExcludes:yn,setClickEvent:Ln,setLink:Mn,getLinks:pn,bindFunctions:In,parseDuration:Nt,isInvalidDate:Pt,setWeekday:Tn,getWeekday:vn,setWeekend:wn};function Xt(e,t,r){let i=!0;for(;i;)i=!1,r.forEach(function(a){let f="^\\s*"+a+"\\s*$",m=new RegExp(f);e[0].match(m)&&(t[a]=!0,e.shift(1),i=!0)})}o(Xt,"getTaskTags");var we=oe(nt(),1);var Yn=o(function(){ce.debug("Something is calling, setConf, remove the call")},"setConf"),qt={monday:bt,tuesday:xt,wednesday:Tt,thursday:vt,friday:wt,saturday:_t,sunday:gt},Wn=o((e,t)=>{let r=[...e].map(()=>-1/0),i=[...e].sort((f,m)=>f.startTime-m.startTime||f.order-m.order),a=0;for(let f of i)for(let m=0;m<r.length;m++)if(f.startTime>=r[m]){r[m]=f.endTime,f.order=m+t,m>a&&(a=m);break}return a},"getMaxIntersections"),$,Fn=o(function(e,t,r,i){let a=ee().gantt,f=ee().securityLevel,m;f==="sandbox"&&(m=fe("#i"+t));let T=f==="sandbox"?fe(m.nodes()[0].contentDocument.body):fe("body"),W=f==="sandbox"?m.nodes()[0].contentDocument:document,A=W.getElementById(t);$=A.parentElement.offsetWidth,$===void 0&&($=1200),a.useWidth!==void 0&&($=a.useWidth);let E=i.db.getTasks(),F=[];for(let p of E)F.push(p.type);F=q(F);let j={},y=2*a.topPadding;if(i.db.getDisplayMode()==="compact"||a.displayMode==="compact"){let p={};for(let b of E)p[b.section]===void 0?p[b.section]=[b]:p[b.section].push(b);let v=0;for(let b of Object.keys(p)){let w=Wn(p[b],v)+1;v+=w,y+=w*(a.barHeight+a.barGap),j[b]=w}}else{y+=E.length*(a.barHeight+a.barGap);for(let p of F)j[p]=E.filter(v=>v.type===p).length}A.setAttribute("viewBox","0 0 "+$+" "+y);let _=T.select(`[id="${t}"]`),g=Dt().domain([ht(E,function(p){return p.startTime}),ft(E,function(p){return p.endTime})]).rangeRound([0,$-a.leftPadding-a.rightPadding]);function I(p,v){let b=p.startTime,w=v.startTime,k=0;return b>w?k=1:b<w&&(k=-1),k}o(I,"taskCompare"),E.sort(I),z(E,$,y),rt(_,y,$,a.useMaxWidth),_.append("text").text(i.db.getDiagramTitle()).attr("x",$/2).attr("y",a.titleTopMargin).attr("class","titleText");function z(p,v,b){let w=a.barHeight,k=w+a.barGap,D=a.topPadding,c=a.leftPadding,l=pt().domain([0,F.length]).range(["#00B9FA","#F95002"]).interpolate(yt);Q(k,D,c,v,b,p,i.db.getExcludes(),i.db.getIncludes()),X(c,D,v,b),N(p,k,D,c,w,l,v,b),R(k,D,c,w,l),B(c,D,v,b)}o(z,"makeGantt");function N(p,v,b,w,k,D,c){let h=[...new Set(p.map(d=>d.order))].map(d=>p.find(n=>n.order===d));_.append("g").selectAll("rect").data(h).enter().append("rect").attr("x",0).attr("y",function(d,n){return n=d.order,n*v+b-2}).attr("width",function(){return c-a.rightPadding/2}).attr("height",v).attr("class",function(d){for(let[n,M]of F.entries())if(d.type===M)return"section section"+n%a.numberSectionStyles;return"section section0"});let u=_.append("g").selectAll("rect").data(p).enter(),x=i.db.getLinks();if(u.append("rect").attr("id",function(d){return d.id}).attr("rx",3).attr("ry",3).attr("x",function(d){return d.milestone?g(d.startTime)+w+.5*(g(d.endTime)-g(d.startTime))-.5*k:g(d.startTime)+w}).attr("y",function(d,n){return n=d.order,n*v+b}).attr("width",function(d){return d.milestone?k:g(d.renderEndTime||d.endTime)-g(d.startTime)}).attr("height",k).attr("transform-origin",function(d,n){return n=d.order,(g(d.startTime)+w+.5*(g(d.endTime)-g(d.startTime))).toString()+"px "+(n*v+b+.5*k).toString()+"px"}).attr("class",function(d){let n="task",M="";d.classes.length>0&&(M=d.classes.join(" "));let C=0;for(let[O,L]of F.entries())d.type===L&&(C=O%a.numberSectionStyles);let S="";return d.active?d.crit?S+=" activeCrit":S=" active":d.done?d.crit?S=" doneCrit":S=" done":d.crit&&(S+=" crit"),S.length===0&&(S=" task"),d.milestone&&(S=" milestone "+S),S+=C,S+=" "+M,n+S}),u.append("text").attr("id",function(d){return d.id+"-text"}).text(function(d){return d.task}).attr("font-size",a.fontSize).attr("x",function(d){let n=g(d.startTime),M=g(d.renderEndTime||d.endTime);d.milestone&&(n+=.5*(g(d.endTime)-g(d.startTime))-.5*k),d.milestone&&(M=n+k);let C=this.getBBox().width;return C>M-n?M+C+1.5*a.leftPadding>c?n+w-5:M+w+5:(M-n)/2+n+w}).attr("y",function(d,n){return n=d.order,n*v+a.barHeight/2+(a.fontSize/2-2)+b}).attr("text-height",k).attr("class",function(d){let n=g(d.startTime),M=g(d.endTime);d.milestone&&(M=n+k);let C=this.getBBox().width,S="";d.classes.length>0&&(S=d.classes.join(" "));let O=0;for(let[te,Y]of F.entries())d.type===Y&&(O=te%a.numberSectionStyles);let L="";return d.active&&(d.crit?L="activeCritText"+O:L="activeText"+O),d.done?d.crit?L=L+" doneCritText"+O:L=L+" doneText"+O:d.crit&&(L=L+" critText"+O),d.milestone&&(L+=" milestoneText"),C>M-n?M+C+1.5*a.leftPadding>c?S+" taskTextOutsideLeft taskTextOutside"+O+" "+L:S+" taskTextOutsideRight taskTextOutside"+O+" "+L+" width-"+C:S+" taskText taskText"+O+" "+L+" width-"+C}),ee().securityLevel==="sandbox"){let d;d=fe("#i"+t);let n=d.nodes()[0].contentDocument;u.filter(function(M){return x.has(M.id)}).each(function(M){var C=n.querySelector("#"+M.id),S=n.querySelector("#"+M.id+"-text");let O=C.parentNode;var L=n.createElement("a");L.setAttribute("xlink:href",x.get(M.id)),L.setAttribute("target","_top"),O.appendChild(L),L.appendChild(C),L.appendChild(S)})}}o(N,"drawRects");function Q(p,v,b,w,k,D,c,l){if(c.length===0&&l.length===0)return;let h,u;for(let{startTime:C,endTime:S}of D)(h===void 0||C<h)&&(h=C),(u===void 0||S>u)&&(u=S);if(!h||!u)return;if((0,we.default)(u).diff((0,we.default)(h),"year")>5){ce.warn("The difference between the min and max time is more than 5 years. This will cause performance issues. Skipping drawing exclude days.");return}let x=i.db.getDateFormat(),s=[],d=null,n=(0,we.default)(h);for(;n.valueOf()<=u;)i.db.isInvalidDate(n,x,c,l)?d?d.end=n:d={start:n,end:n}:d&&(s.push(d),d=null),n=n.add(1,"d");_.append("g").selectAll("rect").data(s).enter().append("rect").attr("id",function(C){return"exclude-"+C.start.format("YYYY-MM-DD")}).attr("x",function(C){return g(C.start)+b}).attr("y",a.gridLineStartPadding).attr("width",function(C){let S=C.end.add(1,"day");return g(S)-g(C.start)}).attr("height",k-v-a.gridLineStartPadding).attr("transform-origin",function(C,S){return(g(C.start)+b+.5*(g(C.end)-g(C.start))).toString()+"px "+(S*p+.5*k).toString()+"px"}).attr("class","exclude-range")}o(Q,"drawExcludeDays");function X(p,v,b,w){let k=kt(g).tickSize(-w+v+a.gridLineStartPadding).tickFormat(We(i.db.getAxisFormat()||a.axisFormat||"%Y-%m-%d")),c=/^([1-9]\d*)(millisecond|second|minute|hour|day|week|month)$/.exec(i.db.getTickInterval()||a.tickInterval);if(c!==null){let l=c[1],h=c[2],u=i.db.getWeekday()||a.weekday;switch(h){case"millisecond":k.ticks(Ee.every(l));break;case"second":k.ticks(Me.every(l));break;case"minute":k.ticks(Ae.every(l));break;case"hour":k.ticks(Le.every(l));break;case"day":k.ticks(Ie.every(l));break;case"week":k.ticks(qt[u].every(l));break;case"month":k.ticks(Ye.every(l));break}}if(_.append("g").attr("class","grid").attr("transform","translate("+p+", "+(w-50)+")").call(k).selectAll("text").style("text-anchor","middle").attr("fill","#000").attr("stroke","none").attr("font-size",10).attr("dy","1em"),i.db.topAxisEnabled()||a.topAxis){let l=mt(g).tickSize(-w+v+a.gridLineStartPadding).tickFormat(We(i.db.getAxisFormat()||a.axisFormat||"%Y-%m-%d"));if(c!==null){let h=c[1],u=c[2],x=i.db.getWeekday()||a.weekday;switch(u){case"millisecond":l.ticks(Ee.every(h));break;case"second":l.ticks(Me.every(h));break;case"minute":l.ticks(Ae.every(h));break;case"hour":l.ticks(Le.every(h));break;case"day":l.ticks(Ie.every(h));break;case"week":l.ticks(qt[x].every(h));break;case"month":l.ticks(Ye.every(h));break}}_.append("g").attr("class","grid").attr("transform","translate("+p+", "+v+")").call(l).selectAll("text").style("text-anchor","middle").attr("fill","#000").attr("stroke","none").attr("font-size",10)}}o(X,"makeGrid");function R(p,v){let b=0,w=Object.keys(j).map(k=>[k,j[k]]);_.append("g").selectAll("text").data(w).enter().append(function(k){let D=k[0].split(it.lineBreakRegex),c=-(D.length-1)/2,l=W.createElementNS("http://www.w3.org/2000/svg","text");l.setAttribute("dy",c+"em");for(let[h,u]of D.entries()){let x=W.createElementNS("http://www.w3.org/2000/svg","tspan");x.setAttribute("alignment-baseline","central"),x.setAttribute("x","10"),h>0&&x.setAttribute("dy","1em"),x.textContent=u,l.appendChild(x)}return l}).attr("x",10).attr("y",function(k,D){if(D>0)for(let c=0;c<D;c++)return b+=w[D-1][1],k[1]*p/2+b*p+v;else return k[1]*p/2+v}).attr("font-size",a.sectionFontSize).attr("class",function(k){for(let[D,c]of F.entries())if(k[0]===c)return"sectionTitle sectionTitle"+D%a.numberSectionStyles;return"sectionTitle"})}o(R,"vertLabels");function B(p,v,b,w){let k=i.db.getTodayMarker();if(k==="off")return;let D=_.append("g").attr("class","today"),c=new Date,l=D.append("line");l.attr("x1",g(c)+p).attr("x2",g(c)+p).attr("y1",a.titleTopMargin).attr("y2",w-a.titleTopMargin).attr("class","today"),k!==""&&l.attr("style",k.replace(/,/g,";"))}o(B,"drawToday");function q(p){let v={},b=[];for(let w=0,k=p.length;w<k;++w)Object.prototype.hasOwnProperty.call(v,p[w])||(v[p[w]]=!0,b.push(p[w]));return b}o(q,"checkUnique")},"draw"),Ut={setConf:Yn,draw:Fn};var Vn=o(e=>`
  .mermaid-main-font {
    font-family: var(--mermaid-font-family, "trebuchet ms", verdana, arial, sans-serif);
  }

  .exclude-range {
    fill: ${e.excludeBkgColor};
  }

  .section {
    stroke: none;
    opacity: 0.2;
  }

  .section0 {
    fill: ${e.sectionBkgColor};
  }

  .section2 {
    fill: ${e.sectionBkgColor2};
  }

  .section1,
  .section3 {
    fill: ${e.altSectionBkgColor};
    opacity: 0.2;
  }

  .sectionTitle0 {
    fill: ${e.titleColor};
  }

  .sectionTitle1 {
    fill: ${e.titleColor};
  }

  .sectionTitle2 {
    fill: ${e.titleColor};
  }

  .sectionTitle3 {
    fill: ${e.titleColor};
  }

  .sectionTitle {
    text-anchor: start;
    font-family: var(--mermaid-font-family, "trebuchet ms", verdana, arial, sans-serif);
  }


  /* Grid and axis */

  .grid .tick {
    stroke: ${e.gridColor};
    opacity: 0.8;
    shape-rendering: crispEdges;
  }

  .grid .tick text {
    font-family: ${e.fontFamily};
    fill: ${e.textColor};
  }

  .grid path {
    stroke-width: 0;
  }


  /* Today line */

  .today {
    fill: none;
    stroke: ${e.todayLineColor};
    stroke-width: 2px;
  }


  /* Task styling */

  /* Default task */

  .task {
    stroke-width: 2;
  }

  .taskText {
    text-anchor: middle;
    font-family: var(--mermaid-font-family, "trebuchet ms", verdana, arial, sans-serif);
  }

  .taskTextOutsideRight {
    fill: ${e.taskTextDarkColor};
    text-anchor: start;
    font-family: var(--mermaid-font-family, "trebuchet ms", verdana, arial, sans-serif);
  }

  .taskTextOutsideLeft {
    fill: ${e.taskTextDarkColor};
    text-anchor: end;
  }


  /* Special case clickable */

  .task.clickable {
    cursor: pointer;
  }

  .taskText.clickable {
    cursor: pointer;
    fill: ${e.taskTextClickableColor} !important;
    font-weight: bold;
  }

  .taskTextOutsideLeft.clickable {
    cursor: pointer;
    fill: ${e.taskTextClickableColor} !important;
    font-weight: bold;
  }

  .taskTextOutsideRight.clickable {
    cursor: pointer;
    fill: ${e.taskTextClickableColor} !important;
    font-weight: bold;
  }


  /* Specific task settings for the sections*/

  .taskText0,
  .taskText1,
  .taskText2,
  .taskText3 {
    fill: ${e.taskTextColor};
  }

  .task0,
  .task1,
  .task2,
  .task3 {
    fill: ${e.taskBkgColor};
    stroke: ${e.taskBorderColor};
  }

  .taskTextOutside0,
  .taskTextOutside2
  {
    fill: ${e.taskTextOutsideColor};
  }

  .taskTextOutside1,
  .taskTextOutside3 {
    fill: ${e.taskTextOutsideColor};
  }


  /* Active task */

  .active0,
  .active1,
  .active2,
  .active3 {
    fill: ${e.activeTaskBkgColor};
    stroke: ${e.activeTaskBorderColor};
  }

  .activeText0,
  .activeText1,
  .activeText2,
  .activeText3 {
    fill: ${e.taskTextDarkColor} !important;
  }


  /* Completed task */

  .done0,
  .done1,
  .done2,
  .done3 {
    stroke: ${e.doneTaskBorderColor};
    fill: ${e.doneTaskBkgColor};
    stroke-width: 2;
  }

  .doneText0,
  .doneText1,
  .doneText2,
  .doneText3 {
    fill: ${e.taskTextDarkColor} !important;
  }


  /* Tasks on the critical line */

  .crit0,
  .crit1,
  .crit2,
  .crit3 {
    stroke: ${e.critBorderColor};
    fill: ${e.critBkgColor};
    stroke-width: 2;
  }

  .activeCrit0,
  .activeCrit1,
  .activeCrit2,
  .activeCrit3 {
    stroke: ${e.critBorderColor};
    fill: ${e.activeTaskBkgColor};
    stroke-width: 2;
  }

  .doneCrit0,
  .doneCrit1,
  .doneCrit2,
  .doneCrit3 {
    stroke: ${e.critBorderColor};
    fill: ${e.doneTaskBkgColor};
    stroke-width: 2;
    cursor: pointer;
    shape-rendering: crispEdges;
  }

  .milestone {
    transform: rotate(45deg) scale(0.8,0.8);
  }

  .milestoneText {
    font-style: italic;
  }
  .doneCritText0,
  .doneCritText1,
  .doneCritText2,
  .doneCritText3 {
    fill: ${e.taskTextDarkColor} !important;
  }

  .activeCritText0,
  .activeCritText1,
  .activeCritText2,
  .activeCritText3 {
    fill: ${e.taskTextDarkColor} !important;
  }

  .titleText {
    text-anchor: middle;
    font-size: 18px;
    fill: ${e.titleColor||e.textColor};
    font-family: var(--mermaid-font-family, "trebuchet ms", verdana, arial, sans-serif);
  }
`,"getStyles"),Zt=Vn;var oi={parser:St,db:Ht,renderer:Ut,styles:Zt};export{oi as diagram};
