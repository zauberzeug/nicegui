import{a as H}from"./chunk-4KE642ED.mjs";import{a as Z}from"./chunk-YFFLADYN.mjs";import"./chunk-VRGDDFRA.mjs";import"./chunk-E4AWDUZE.mjs";import{a as J}from"./chunk-WVHPJQMP.mjs";import{k as V,l as U}from"./chunk-AC3VT7B7.mjs";import"./chunk-TI4EEUUG.mjs";import{Aa as C,Da as N,M as O,P as j,Q as _,R as z,S as B,T as M,U as W,V as I,X as L,b as m,ha as q,s as F}from"./chunk-NQURTBEV.mjs";import"./chunk-C7NU23FD.mjs";import"./chunk-DZFIHE2J.mjs";import"./chunk-D3PZO57J.mjs";import"./chunk-BKDDFIKN.mjs";import"./chunk-YPUTD6PB.mjs";import"./chunk-6BY5RJGC.mjs";import{a as t}from"./chunk-GTKDMUJJ.mjs";var K=F.pie,A={sections:new Map,showData:!1,config:K},u=A.sections,w=A.showData,ce=structuredClone(K),pe=t(()=>structuredClone(ce),"getConfig"),me=t(()=>{u=new Map,w=A.showData,j()},"clear"),le=t(({label:e,value:i})=>{u.has(e)||(u.set(e,i),m.debug(`added new section: ${e}, with value: ${i}`))},"addSection"),de=t(()=>u,"getSections"),fe=t(e=>{w=e},"setShowData"),ge=t(()=>w,"getShowData"),S={getConfig:pe,clear:me,setDiagramTitle:W,getDiagramTitle:I,setAccTitle:_,getAccTitle:z,setAccDescription:B,getAccDescription:M,addSection:le,getSections:de,setShowData:fe,getShowData:ge};var De=t((e,i)=>{H(e,i),i.setShowData(e.showData),e.sections.map(i.addSection)},"populateDb"),Q={parse:t(async e=>{let i=await Z("pie",e);m.debug(i),De(i,S)},"parse")};var ue=t(e=>`
  .pieCircle{
    stroke: ${e.pieStrokeColor};
    stroke-width : ${e.pieStrokeWidth};
    opacity : ${e.pieOpacity};
  }
  .pieOuterCircle{
    stroke: ${e.pieOuterStrokeColor};
    stroke-width: ${e.pieOuterStrokeWidth};
    fill: none;
  }
  .pieTitleText {
    text-anchor: middle;
    font-size: ${e.pieTitleTextSize};
    fill: ${e.pieTitleTextColor};
    font-family: ${e.fontFamily};
  }
  .slice {
    font-family: ${e.fontFamily};
    fill: ${e.pieSectionTextColor};
    font-size:${e.pieSectionTextSize};
    // fill: white;
  }
  .legend text {
    fill: ${e.pieLegendTextColor};
    font-family: ${e.fontFamily};
    font-size: ${e.pieLegendTextSize};
  }
`,"getStyles"),X=ue;var Se=t(e=>{let i=[...e.entries()].map(n=>({label:n[0],value:n[1]})).sort((n,s)=>s.value-n.value);return N().value(n=>n.value)(i)},"createPieArcs"),ye=t((e,i,ee,n)=>{m.debug(`rendering pie chart
`+e);let s=n.db,T=L(),b=U(s.getConfig(),T.pie),v=40,a=18,d=4,c=450,y=c,P=J(i),p=P.append("g");p.attr("transform","translate("+y/2+","+c/2+")");let{themeVariables:r}=T,[$]=V(r.pieOuterStrokeWidth);$??=2;let G=b.textPosition,f=Math.min(y,c)/2-v,te=C().innerRadius(0).outerRadius(f),ie=C().innerRadius(f*G).outerRadius(f*G);p.append("circle").attr("cx",0).attr("cy",0).attr("r",f+$/2).attr("class","pieOuterCircle");let k=s.getSections(),h=Se(k),re=[r.pie1,r.pie2,r.pie3,r.pie4,r.pie5,r.pie6,r.pie7,r.pie8,r.pie9,r.pie10,r.pie11,r.pie12],l=q(re);p.selectAll("mySlices").data(h).enter().append("path").attr("d",te).attr("fill",o=>l(o.data.label)).attr("class","pieCircle");let E=0;k.forEach(o=>{E+=o}),p.selectAll("mySlices").data(h).enter().append("text").text(o=>(o.data.value/E*100).toFixed(0)+"%").attr("transform",o=>"translate("+ie.centroid(o)+")").style("text-anchor","middle").attr("class","slice"),p.append("text").text(s.getDiagramTitle()).attr("x",0).attr("y",-(c-50)/2).attr("class","pieTitleText");let x=p.selectAll(".legend").data(l.domain()).enter().append("g").attr("class","legend").attr("transform",(o,g)=>{let D=a+d,ne=D*l.domain().length/2,ae=12*a,se=g*D-ne;return"translate("+ae+","+se+")"});x.append("rect").attr("width",a).attr("height",a).style("fill",l).style("stroke",l),x.data(h).append("text").attr("x",a+d).attr("y",a-d).text(o=>{let{label:g,value:D}=o.data;return s.getShowData()?`${g} [${D}]`:g});let oe=Math.max(...x.selectAll("text").nodes().map(o=>o?.getBoundingClientRect().width??0)),R=y+v+a+d+oe;P.attr("viewBox",`0 0 ${R} ${c}`),O(P,c,R,b.useMaxWidth)},"draw"),Y={draw:ye};var Ne={parser:Q,db:S,renderer:Y,styles:X};export{Ne as diagram};
