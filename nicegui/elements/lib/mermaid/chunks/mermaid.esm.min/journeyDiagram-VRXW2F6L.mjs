import{a as ft,b as pt,c as dt,f as H}from"./chunk-6IZS222M.mjs";import"./chunk-TI4EEUUG.mjs";import{Aa as G,M as st,P as at,Q as ot,R as lt,S as ct,T as ht,U as ut,V as yt,X as $,fa as z}from"./chunk-NQURTBEV.mjs";import{a as r}from"./chunk-GTKDMUJJ.mjs";var U=function(){var t=r(function(g,n,a,o){for(a=a||{},o=g.length;o--;a[g[o]]=n);return a},"o"),e=[6,8,10,11,12,14,16,17,18],s=[1,9],c=[1,10],i=[1,11],u=[1,12],h=[1,13],d=[1,14],f={trace:r(function(){},"trace"),yy:{},symbols_:{error:2,start:3,journey:4,document:5,EOF:6,line:7,SPACE:8,statement:9,NEWLINE:10,title:11,acc_title:12,acc_title_value:13,acc_descr:14,acc_descr_value:15,acc_descr_multiline_value:16,section:17,taskName:18,taskData:19,$accept:0,$end:1},terminals_:{2:"error",4:"journey",6:"EOF",8:"SPACE",10:"NEWLINE",11:"title",12:"acc_title",13:"acc_title_value",14:"acc_descr",15:"acc_descr_value",16:"acc_descr_multiline_value",17:"section",18:"taskName",19:"taskData"},productions_:[0,[3,3],[5,0],[5,2],[7,2],[7,1],[7,1],[7,1],[9,1],[9,2],[9,2],[9,1],[9,1],[9,2]],performAction:r(function(n,a,o,y,p,l,M){var _=l.length-1;switch(p){case 1:return l[_-1];case 2:this.$=[];break;case 3:l[_-1].push(l[_]),this.$=l[_-1];break;case 4:case 5:this.$=l[_];break;case 6:case 7:this.$=[];break;case 8:y.setDiagramTitle(l[_].substr(6)),this.$=l[_].substr(6);break;case 9:this.$=l[_].trim(),y.setAccTitle(this.$);break;case 10:case 11:this.$=l[_].trim(),y.setAccDescription(this.$);break;case 12:y.addSection(l[_].substr(8)),this.$=l[_].substr(8);break;case 13:y.addTask(l[_-1],l[_]),this.$="task";break}},"anonymous"),table:[{3:1,4:[1,2]},{1:[3]},t(e,[2,2],{5:3}),{6:[1,4],7:5,8:[1,6],9:7,10:[1,8],11:s,12:c,14:i,16:u,17:h,18:d},t(e,[2,7],{1:[2,1]}),t(e,[2,3]),{9:15,11:s,12:c,14:i,16:u,17:h,18:d},t(e,[2,5]),t(e,[2,6]),t(e,[2,8]),{13:[1,16]},{15:[1,17]},t(e,[2,11]),t(e,[2,12]),{19:[1,18]},t(e,[2,4]),t(e,[2,9]),t(e,[2,10]),t(e,[2,13])],defaultActions:{},parseError:r(function(n,a){if(a.recoverable)this.trace(n);else{var o=new Error(n);throw o.hash=a,o}},"parseError"),parse:r(function(n){var a=this,o=[0],y=[],p=[null],l=[],M=this.table,_="",N=0,et=0,nt=0,Tt=2,rt=1,Mt=l.slice.call(arguments,1),k=Object.create(this.lexer),C={yy:{}};for(var O in this.yy)Object.prototype.hasOwnProperty.call(this.yy,O)&&(C.yy[O]=this.yy[O]);k.setInput(n,C.yy),C.yy.lexer=k,C.yy.parser=this,typeof k.yylloc>"u"&&(k.yylloc={});var q=k.yylloc;l.push(q);var St=k.options&&k.options.ranges;typeof C.yy.parseError=="function"?this.parseError=C.yy.parseError:this.parseError=Object.getPrototypeOf(this).parseError;function Gt(v){o.length=o.length-2*v,p.length=p.length-v,l.length=l.length-v}r(Gt,"popStack");function $t(){var v;return v=y.pop()||k.lex()||rt,typeof v!="number"&&(v instanceof Array&&(y=v,v=y.pop()),v=a.symbols_[v]||v),v}r($t,"lex");for(var b,D,P,w,Ht,W,A={},B,S,it,j;;){if(P=o[o.length-1],this.defaultActions[P]?w=this.defaultActions[P]:((b===null||typeof b>"u")&&(b=$t()),w=M[P]&&M[P][b]),typeof w>"u"||!w.length||!w[0]){var X="";j=[];for(B in M[P])this.terminals_[B]&&B>Tt&&j.push("'"+this.terminals_[B]+"'");k.showPosition?X="Parse error on line "+(N+1)+`:
`+k.showPosition()+`
Expecting `+j.join(", ")+", got '"+(this.terminals_[b]||b)+"'":X="Parse error on line "+(N+1)+": Unexpected "+(b==rt?"end of input":"'"+(this.terminals_[b]||b)+"'"),this.parseError(X,{text:k.match,token:this.terminals_[b]||b,line:k.yylineno,loc:q,expected:j})}if(w[0]instanceof Array&&w.length>1)throw new Error("Parse Error: multiple actions possible at state: "+P+", token: "+b);switch(w[0]){case 1:o.push(b),p.push(k.yytext),l.push(k.yylloc),o.push(w[1]),b=null,D?(b=D,D=null):(et=k.yyleng,_=k.yytext,N=k.yylineno,q=k.yylloc,nt>0&&nt--);break;case 2:if(S=this.productions_[w[1]][1],A.$=p[p.length-S],A._$={first_line:l[l.length-(S||1)].first_line,last_line:l[l.length-1].last_line,first_column:l[l.length-(S||1)].first_column,last_column:l[l.length-1].last_column},St&&(A._$.range=[l[l.length-(S||1)].range[0],l[l.length-1].range[1]]),W=this.performAction.apply(A,[_,et,N,C.yy,w[1],p,l].concat(Mt)),typeof W<"u")return W;S&&(o=o.slice(0,-1*S*2),p=p.slice(0,-1*S),l=l.slice(0,-1*S)),o.push(this.productions_[w[1]][0]),p.push(A.$),l.push(A._$),it=M[o[o.length-2]][o[o.length-1]],o.push(it);break;case 3:return!0}}return!0},"parse")},x=function(){var g={EOF:1,parseError:r(function(a,o){if(this.yy.parser)this.yy.parser.parseError(a,o);else throw new Error(a)},"parseError"),setInput:r(function(n,a){return this.yy=a||this.yy||{},this._input=n,this._more=this._backtrack=this.done=!1,this.yylineno=this.yyleng=0,this.yytext=this.matched=this.match="",this.conditionStack=["INITIAL"],this.yylloc={first_line:1,first_column:0,last_line:1,last_column:0},this.options.ranges&&(this.yylloc.range=[0,0]),this.offset=0,this},"setInput"),input:r(function(){var n=this._input[0];this.yytext+=n,this.yyleng++,this.offset++,this.match+=n,this.matched+=n;var a=n.match(/(?:\r\n?|\n).*/g);return a?(this.yylineno++,this.yylloc.last_line++):this.yylloc.last_column++,this.options.ranges&&this.yylloc.range[1]++,this._input=this._input.slice(1),n},"input"),unput:r(function(n){var a=n.length,o=n.split(/(?:\r\n?|\n)/g);this._input=n+this._input,this.yytext=this.yytext.substr(0,this.yytext.length-a),this.offset-=a;var y=this.match.split(/(?:\r\n?|\n)/g);this.match=this.match.substr(0,this.match.length-1),this.matched=this.matched.substr(0,this.matched.length-1),o.length-1&&(this.yylineno-=o.length-1);var p=this.yylloc.range;return this.yylloc={first_line:this.yylloc.first_line,last_line:this.yylineno+1,first_column:this.yylloc.first_column,last_column:o?(o.length===y.length?this.yylloc.first_column:0)+y[y.length-o.length].length-o[0].length:this.yylloc.first_column-a},this.options.ranges&&(this.yylloc.range=[p[0],p[0]+this.yyleng-a]),this.yyleng=this.yytext.length,this},"unput"),more:r(function(){return this._more=!0,this},"more"),reject:r(function(){if(this.options.backtrack_lexer)this._backtrack=!0;else return this.parseError("Lexical error on line "+(this.yylineno+1)+`. You can only invoke reject() in the lexer when the lexer is of the backtracking persuasion (options.backtrack_lexer = true).
`+this.showPosition(),{text:"",token:null,line:this.yylineno});return this},"reject"),less:r(function(n){this.unput(this.match.slice(n))},"less"),pastInput:r(function(){var n=this.matched.substr(0,this.matched.length-this.match.length);return(n.length>20?"...":"")+n.substr(-20).replace(/\n/g,"")},"pastInput"),upcomingInput:r(function(){var n=this.match;return n.length<20&&(n+=this._input.substr(0,20-n.length)),(n.substr(0,20)+(n.length>20?"...":"")).replace(/\n/g,"")},"upcomingInput"),showPosition:r(function(){var n=this.pastInput(),a=new Array(n.length+1).join("-");return n+this.upcomingInput()+`
`+a+"^"},"showPosition"),test_match:r(function(n,a){var o,y,p;if(this.options.backtrack_lexer&&(p={yylineno:this.yylineno,yylloc:{first_line:this.yylloc.first_line,last_line:this.last_line,first_column:this.yylloc.first_column,last_column:this.yylloc.last_column},yytext:this.yytext,match:this.match,matches:this.matches,matched:this.matched,yyleng:this.yyleng,offset:this.offset,_more:this._more,_input:this._input,yy:this.yy,conditionStack:this.conditionStack.slice(0),done:this.done},this.options.ranges&&(p.yylloc.range=this.yylloc.range.slice(0))),y=n[0].match(/(?:\r\n?|\n).*/g),y&&(this.yylineno+=y.length),this.yylloc={first_line:this.yylloc.last_line,last_line:this.yylineno+1,first_column:this.yylloc.last_column,last_column:y?y[y.length-1].length-y[y.length-1].match(/\r?\n?/)[0].length:this.yylloc.last_column+n[0].length},this.yytext+=n[0],this.match+=n[0],this.matches=n,this.yyleng=this.yytext.length,this.options.ranges&&(this.yylloc.range=[this.offset,this.offset+=this.yyleng]),this._more=!1,this._backtrack=!1,this._input=this._input.slice(n[0].length),this.matched+=n[0],o=this.performAction.call(this,this.yy,this,a,this.conditionStack[this.conditionStack.length-1]),this.done&&this._input&&(this.done=!1),o)return o;if(this._backtrack){for(var l in p)this[l]=p[l];return!1}return!1},"test_match"),next:r(function(){if(this.done)return this.EOF;this._input||(this.done=!0);var n,a,o,y;this._more||(this.yytext="",this.match="");for(var p=this._currentRules(),l=0;l<p.length;l++)if(o=this._input.match(this.rules[p[l]]),o&&(!a||o[0].length>a[0].length)){if(a=o,y=l,this.options.backtrack_lexer){if(n=this.test_match(o,p[l]),n!==!1)return n;if(this._backtrack){a=!1;continue}else return!1}else if(!this.options.flex)break}return a?(n=this.test_match(a,p[y]),n!==!1?n:!1):this._input===""?this.EOF:this.parseError("Lexical error on line "+(this.yylineno+1)+`. Unrecognized text.
`+this.showPosition(),{text:"",token:null,line:this.yylineno})},"next"),lex:r(function(){var a=this.next();return a||this.lex()},"lex"),begin:r(function(a){this.conditionStack.push(a)},"begin"),popState:r(function(){var a=this.conditionStack.length-1;return a>0?this.conditionStack.pop():this.conditionStack[0]},"popState"),_currentRules:r(function(){return this.conditionStack.length&&this.conditionStack[this.conditionStack.length-1]?this.conditions[this.conditionStack[this.conditionStack.length-1]].rules:this.conditions.INITIAL.rules},"_currentRules"),topState:r(function(a){return a=this.conditionStack.length-1-Math.abs(a||0),a>=0?this.conditionStack[a]:"INITIAL"},"topState"),pushState:r(function(a){this.begin(a)},"pushState"),stateStackSize:r(function(){return this.conditionStack.length},"stateStackSize"),options:{"case-insensitive":!0},performAction:r(function(a,o,y,p){var l=p;switch(y){case 0:break;case 1:break;case 2:return 10;case 3:break;case 4:break;case 5:return 4;case 6:return 11;case 7:return this.begin("acc_title"),12;break;case 8:return this.popState(),"acc_title_value";break;case 9:return this.begin("acc_descr"),14;break;case 10:return this.popState(),"acc_descr_value";break;case 11:this.begin("acc_descr_multiline");break;case 12:this.popState();break;case 13:return"acc_descr_multiline_value";case 14:return 17;case 15:return 18;case 16:return 19;case 17:return":";case 18:return 6;case 19:return"INVALID"}},"anonymous"),rules:[/^(?:%(?!\{)[^\n]*)/i,/^(?:[^\}]%%[^\n]*)/i,/^(?:[\n]+)/i,/^(?:\s+)/i,/^(?:#[^\n]*)/i,/^(?:journey\b)/i,/^(?:title\s[^#\n;]+)/i,/^(?:accTitle\s*:\s*)/i,/^(?:(?!\n||)*[^\n]*)/i,/^(?:accDescr\s*:\s*)/i,/^(?:(?!\n||)*[^\n]*)/i,/^(?:accDescr\s*\{\s*)/i,/^(?:[\}])/i,/^(?:[^\}]*)/i,/^(?:section\s[^#:\n;]+)/i,/^(?:[^#:\n;]+)/i,/^(?::[^#\n;]+)/i,/^(?::)/i,/^(?:$)/i,/^(?:.)/i],conditions:{acc_descr_multiline:{rules:[12,13],inclusive:!1},acc_descr:{rules:[10],inclusive:!1},acc_title:{rules:[8],inclusive:!1},INITIAL:{rules:[0,1,2,3,4,5,6,7,9,11,14,15,16,17,18,19],inclusive:!0}}};return g}();f.lexer=x;function m(){this.yy={}}return r(m,"Parser"),m.prototype=f,f.Parser=m,new m}();U.parser=U;var gt=U;var V="",Z=[],L=[],R=[],Et=r(function(){Z.length=0,L.length=0,V="",R.length=0,at()},"clear"),Ct=r(function(t){V=t,Z.push(t)},"addSection"),Pt=r(function(){return Z},"getSections"),It=r(function(){let t=mt(),e=100,s=0;for(;!t&&s<e;)t=mt(),s++;return L.push(...R),L},"getTasks"),At=r(function(){let t=[];return L.forEach(s=>{s.people&&t.push(...s.people)}),[...new Set(t)].sort()},"updateActors"),Vt=r(function(t,e){let s=e.substr(1).split(":"),c=0,i=[];s.length===1?(c=Number(s[0]),i=[]):(c=Number(s[0]),i=s[1].split(","));let u=i.map(d=>d.trim()),h={section:V,type:V,people:u,task:t,score:c};R.push(h)},"addTask"),Ft=r(function(t){let e={section:V,type:V,description:t,task:t,classes:[]};L.push(e)},"addTaskOrg"),mt=r(function(){let t=r(function(s){return R[s].processed},"compileTask"),e=!0;for(let[s,c]of R.entries())t(s),e=e&&c.processed;return e},"compileTasks"),Lt=r(function(){return At()},"getActors"),J={getConfig:r(()=>$().journey,"getConfig"),clear:Et,setDiagramTitle:ut,getDiagramTitle:yt,setAccTitle:ot,getAccTitle:lt,setAccDescription:ct,getAccDescription:ht,addSection:Ct,getSections:Pt,getTasks:It,addTask:Vt,addTaskOrg:Ft,getActors:Lt};var Rt=r(t=>`.label {
    font-family: 'trebuchet ms', verdana, arial, sans-serif;
    font-family: var(--mermaid-font-family);
    color: ${t.textColor};
  }
  .mouth {
    stroke: #666;
  }

  line {
    stroke: ${t.textColor}
  }

  .legend {
    fill: ${t.textColor};
  }

  .label text {
    fill: #333;
  }
  .label {
    color: ${t.textColor}
  }

  .face {
    ${t.faceColor?`fill: ${t.faceColor}`:"fill: #FFF8DC"};
    stroke: #999;
  }

  .node rect,
  .node circle,
  .node ellipse,
  .node polygon,
  .node path {
    fill: ${t.mainBkg};
    stroke: ${t.nodeBorder};
    stroke-width: 1px;
  }

  .node .label {
    text-align: center;
  }
  .node.clickable {
    cursor: pointer;
  }

  .arrowheadPath {
    fill: ${t.arrowheadColor};
  }

  .edgePath .path {
    stroke: ${t.lineColor};
    stroke-width: 1.5px;
  }

  .flowchart-link {
    stroke: ${t.lineColor};
    fill: none;
  }

  .edgeLabel {
    background-color: ${t.edgeLabelBackground};
    rect {
      opacity: 0.5;
    }
    text-align: center;
  }

  .cluster rect {
  }

  .cluster text {
    fill: ${t.titleColor};
  }

  div.mermaidTooltip {
    position: absolute;
    text-align: center;
    max-width: 200px;
    padding: 2px;
    font-family: 'trebuchet ms', verdana, arial, sans-serif;
    font-family: var(--mermaid-font-family);
    font-size: 12px;
    background: ${t.tertiaryColor};
    border: 1px solid ${t.border2};
    border-radius: 2px;
    pointer-events: none;
    z-index: 100;
  }

  .task-type-0, .section-type-0  {
    ${t.fillType0?`fill: ${t.fillType0}`:""};
  }
  .task-type-1, .section-type-1  {
    ${t.fillType0?`fill: ${t.fillType1}`:""};
  }
  .task-type-2, .section-type-2  {
    ${t.fillType0?`fill: ${t.fillType2}`:""};
  }
  .task-type-3, .section-type-3  {
    ${t.fillType0?`fill: ${t.fillType3}`:""};
  }
  .task-type-4, .section-type-4  {
    ${t.fillType0?`fill: ${t.fillType4}`:""};
  }
  .task-type-5, .section-type-5  {
    ${t.fillType0?`fill: ${t.fillType5}`:""};
  }
  .task-type-6, .section-type-6  {
    ${t.fillType0?`fill: ${t.fillType6}`:""};
  }
  .task-type-7, .section-type-7  {
    ${t.fillType0?`fill: ${t.fillType7}`:""};
  }

  .actor-0 {
    ${t.actor0?`fill: ${t.actor0}`:""};
  }
  .actor-1 {
    ${t.actor1?`fill: ${t.actor1}`:""};
  }
  .actor-2 {
    ${t.actor2?`fill: ${t.actor2}`:""};
  }
  .actor-3 {
    ${t.actor3?`fill: ${t.actor3}`:""};
  }
  .actor-4 {
    ${t.actor4?`fill: ${t.actor4}`:""};
  }
  .actor-5 {
    ${t.actor5?`fill: ${t.actor5}`:""};
  }
`,"getStyles"),xt=Rt;var K=r(function(t,e){return ft(t,e)},"drawRect"),Nt=r(function(t,e){let c=t.append("circle").attr("cx",e.cx).attr("cy",e.cy).attr("class","face").attr("r",15).attr("stroke-width",2).attr("overflow","visible"),i=t.append("g");i.append("circle").attr("cx",e.cx-15/3).attr("cy",e.cy-15/3).attr("r",1.5).attr("stroke-width",2).attr("fill","#666").attr("stroke","#666"),i.append("circle").attr("cx",e.cx+15/3).attr("cy",e.cy-15/3).attr("r",1.5).attr("stroke-width",2).attr("fill","#666").attr("stroke","#666");function u(f){let x=G().startAngle(Math.PI/2).endAngle(3*(Math.PI/2)).innerRadius(7.5).outerRadius(6.8181818181818175);f.append("path").attr("class","mouth").attr("d",x).attr("transform","translate("+e.cx+","+(e.cy+2)+")")}r(u,"smile");function h(f){let x=G().startAngle(3*Math.PI/2).endAngle(5*(Math.PI/2)).innerRadius(7.5).outerRadius(6.8181818181818175);f.append("path").attr("class","mouth").attr("d",x).attr("transform","translate("+e.cx+","+(e.cy+7)+")")}r(h,"sad");function d(f){f.append("line").attr("class","mouth").attr("stroke",2).attr("x1",e.cx-5).attr("y1",e.cy+7).attr("x2",e.cx+5).attr("y2",e.cy+7).attr("class","mouth").attr("stroke-width","1px").attr("stroke","#666")}return r(d,"ambivalent"),e.score>3?u(i):e.score<3?h(i):d(i),c},"drawFace"),_t=r(function(t,e){let s=t.append("circle");return s.attr("cx",e.cx),s.attr("cy",e.cy),s.attr("class","actor-"+e.pos),s.attr("fill",e.fill),s.attr("stroke",e.stroke),s.attr("r",e.r),s.class!==void 0&&s.attr("class",s.class),e.title!==void 0&&s.append("title").text(e.title),s},"drawCircle"),bt=r(function(t,e){return dt(t,e)},"drawText"),Bt=r(function(t,e){function s(i,u,h,d,f){return i+","+u+" "+(i+h)+","+u+" "+(i+h)+","+(u+d-f)+" "+(i+h-f*1.2)+","+(u+d)+" "+i+","+(u+d)}r(s,"genPoints");let c=t.append("polygon");c.attr("points",s(e.x,e.y,50,20,7)),c.attr("class","labelBox"),e.y=e.y+e.labelMargin,e.x=e.x+.5*e.labelMargin,bt(t,e)},"drawLabel"),jt=r(function(t,e,s){let c=t.append("g"),i=H();i.x=e.x,i.y=e.y,i.fill=e.fill,i.width=s.width*e.taskCount+s.diagramMarginX*(e.taskCount-1),i.height=s.height,i.class="journey-section section-type-"+e.num,i.rx=3,i.ry=3,K(c,i),vt(s)(e.text,c,i.x,i.y,i.width,i.height,{class:"journey-section section-type-"+e.num},s,e.colour)},"drawSection"),kt=-1,zt=r(function(t,e,s){let c=e.x+s.width/2,i=t.append("g");kt++;let u=300+5*30;i.append("line").attr("id","task"+kt).attr("x1",c).attr("y1",e.y).attr("x2",c).attr("y2",u).attr("class","task-line").attr("stroke-width","1px").attr("stroke-dasharray","4 2").attr("stroke","#666"),Nt(i,{cx:c,cy:300+(5-e.score)*30,score:e.score});let h=H();h.x=e.x,h.y=e.y,h.fill=e.fill,h.width=s.width,h.height=s.height,h.class="task task-type-"+e.num,h.rx=3,h.ry=3,K(i,h);let d=e.x+14;e.people.forEach(f=>{let x=e.actors[f].color,m={cx:d,cy:e.y,r:7,fill:x,stroke:"#000",title:f,pos:e.actors[f].position};_t(i,m),d+=10}),vt(s)(e.task,i,h.x,h.y,h.width,h.height,{class:"task"},s,e.colour)},"drawTask"),Yt=r(function(t,e){pt(t,e)},"drawBackgroundRect"),vt=function(){function t(i,u,h,d,f,x,m,g){let n=u.append("text").attr("x",h+f/2).attr("y",d+x/2+5).style("font-color",g).style("text-anchor","middle").text(i);c(n,m)}r(t,"byText");function e(i,u,h,d,f,x,m,g,n){let{taskFontSize:a,taskFontFamily:o}=g,y=i.split(/<br\s*\/?>/gi);for(let p=0;p<y.length;p++){let l=p*a-a*(y.length-1)/2,M=u.append("text").attr("x",h+f/2).attr("y",d).attr("fill",n).style("text-anchor","middle").style("font-size",a).style("font-family",o);M.append("tspan").attr("x",h+f/2).attr("dy",l).text(y[p]),M.attr("y",d+x/2).attr("dominant-baseline","central").attr("alignment-baseline","central"),c(M,m)}}r(e,"byTspan");function s(i,u,h,d,f,x,m,g){let n=u.append("switch"),o=n.append("foreignObject").attr("x",h).attr("y",d).attr("width",f).attr("height",x).attr("position","fixed").append("xhtml:div").style("display","table").style("height","100%").style("width","100%");o.append("div").attr("class","label").style("display","table-cell").style("text-align","center").style("vertical-align","middle").text(i),e(i,n,h,d,f,x,m,g),c(o,m)}r(s,"byFo");function c(i,u){for(let h in u)h in u&&i.attr(h,u[h])}return r(c,"_setTextAttrs"),function(i){return i.textPlacement==="fo"?s:i.textPlacement==="old"?t:e}}(),Ot=r(function(t){t.append("defs").append("marker").attr("id","arrowhead").attr("refX",5).attr("refY",2).attr("markerWidth",6).attr("markerHeight",4).attr("orient","auto").append("path").attr("d","M 0,0 V 4 L6,2 Z")},"initGraphics"),F={drawRect:K,drawCircle:_t,drawSection:jt,drawText:bt,drawLabel:Bt,drawTask:zt,drawBackgroundRect:Yt,initGraphics:Ot};var qt=r(function(t){Object.keys(t).forEach(function(s){Y[s]=t[s]})},"setConf"),E={};function Dt(t){let e=$().journey,s=60;Object.keys(E).forEach(c=>{let i=E[c].color,u={cx:20,cy:s,r:7,fill:i,stroke:"#000",pos:E[c].position};F.drawCircle(t,u);let h={x:40,y:s+7,fill:"#666",text:c,textMargin:e.boxTextMargin|5};F.drawText(t,h),s+=20})}r(Dt,"drawActorLegend");var Y=$().journey,I=Y.leftMargin,Wt=r(function(t,e,s,c){let i=$().journey,u=$().securityLevel,h;u==="sandbox"&&(h=z("#i"+e));let d=u==="sandbox"?z(h.nodes()[0].contentDocument.body):z("body");T.init();let f=d.select("#"+e);F.initGraphics(f);let x=c.db.getTasks(),m=c.db.getDiagramTitle(),g=c.db.getActors();for(let l in E)delete E[l];let n=0;g.forEach(l=>{E[l]={color:i.actorColours[n%i.actorColours.length],position:n},n++}),Dt(f),T.insert(0,0,I,Object.keys(E).length*50),Xt(f,x,0);let a=T.getBounds();m&&f.append("text").text(m).attr("x",I).attr("font-size","4ex").attr("font-weight","bold").attr("y",25);let o=a.stopy-a.starty+2*i.diagramMarginY,y=I+a.stopx+2*i.diagramMarginX;st(f,o,y,i.useMaxWidth),f.append("line").attr("x1",I).attr("y1",i.height*4).attr("x2",y-I-4).attr("y2",i.height*4).attr("stroke-width",4).attr("stroke","black").attr("marker-end","url(#arrowhead)");let p=m?70:0;f.attr("viewBox",`${a.startx} -25 ${y} ${o+p}`),f.attr("preserveAspectRatio","xMinYMin meet"),f.attr("height",o+p+25)},"draw"),T={data:{startx:void 0,stopx:void 0,starty:void 0,stopy:void 0},verticalPos:0,sequenceItems:[],init:r(function(){this.sequenceItems=[],this.data={startx:void 0,stopx:void 0,starty:void 0,stopy:void 0},this.verticalPos=0},"init"),updateVal:r(function(t,e,s,c){t[e]===void 0?t[e]=s:t[e]=c(s,t[e])},"updateVal"),updateBounds:r(function(t,e,s,c){let i=$().journey,u=this,h=0;function d(f){return r(function(m){h++;let g=u.sequenceItems.length-h+1;u.updateVal(m,"starty",e-g*i.boxMargin,Math.min),u.updateVal(m,"stopy",c+g*i.boxMargin,Math.max),u.updateVal(T.data,"startx",t-g*i.boxMargin,Math.min),u.updateVal(T.data,"stopx",s+g*i.boxMargin,Math.max),f!=="activation"&&(u.updateVal(m,"startx",t-g*i.boxMargin,Math.min),u.updateVal(m,"stopx",s+g*i.boxMargin,Math.max),u.updateVal(T.data,"starty",e-g*i.boxMargin,Math.min),u.updateVal(T.data,"stopy",c+g*i.boxMargin,Math.max))},"updateItemBounds")}r(d,"updateFn"),this.sequenceItems.forEach(d())},"updateBounds"),insert:r(function(t,e,s,c){let i=Math.min(t,s),u=Math.max(t,s),h=Math.min(e,c),d=Math.max(e,c);this.updateVal(T.data,"startx",i,Math.min),this.updateVal(T.data,"starty",h,Math.min),this.updateVal(T.data,"stopx",u,Math.max),this.updateVal(T.data,"stopy",d,Math.max),this.updateBounds(i,h,u,d)},"insert"),bumpVerticalPos:r(function(t){this.verticalPos=this.verticalPos+t,this.data.stopy=this.verticalPos},"bumpVerticalPos"),getVerticalPos:r(function(){return this.verticalPos},"getVerticalPos"),getBounds:r(function(){return this.data},"getBounds")},Q=Y.sectionFills,wt=Y.sectionColours,Xt=r(function(t,e,s){let c=$().journey,i="",u=c.height*2+c.diagramMarginY,h=s+u,d=0,f="#CCC",x="black",m=0;for(let[g,n]of e.entries()){if(i!==n.section){f=Q[d%Q.length],m=d%Q.length,x=wt[d%wt.length];let o=0,y=n.section;for(let l=g;l<e.length&&e[l].section==y;l++)o=o+1;let p={x:g*c.taskMargin+g*c.width+I,y:50,text:n.section,fill:f,num:m,colour:x,taskCount:o};F.drawSection(t,p,c),i=n.section,d++}let a=n.people.reduce((o,y)=>(E[y]&&(o[y]=E[y]),o),{});n.x=g*c.taskMargin+g*c.width+I,n.y=h,n.width=c.diagramMarginX,n.height=c.diagramMarginY,n.colour=x,n.fill=f,n.num=m,n.actors=a,F.drawTask(t,n,c),T.insert(n.x,n.y,n.x+n.width+c.taskMargin,300+5*30)}},"drawTasks"),tt={setConf:qt,draw:Wt};var me={parser:gt,db:J,renderer:tt,styles:xt,init:r(t=>{tt.setConf(t.journey),J.clear()},"init")};export{me as diagram};
