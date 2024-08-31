import{a as z}from"./chunk-4KE642ED.mjs";import{a as v}from"./chunk-YFFLADYN.mjs";import"./chunk-VRGDDFRA.mjs";import"./chunk-E4AWDUZE.mjs";import{a as G}from"./chunk-WVHPJQMP.mjs";import{l as u}from"./chunk-AC3VT7B7.mjs";import"./chunk-TI4EEUUG.mjs";import{A as x,M as C,P as B,Q as S,R as $,S as w,T as W,U as F,V as j,b,s as h}from"./chunk-NQURTBEV.mjs";import"./chunk-C7NU23FD.mjs";import"./chunk-DZFIHE2J.mjs";import"./chunk-D3PZO57J.mjs";import"./chunk-BKDDFIKN.mjs";import"./chunk-YPUTD6PB.mjs";import"./chunk-6BY5RJGC.mjs";import{a}from"./chunk-GTKDMUJJ.mjs";var T={packet:[]},D=structuredClone(T),q=h.packet,V=a(()=>{let t=u({...q,...x().packet});return t.showBits&&(t.paddingY+=10),t},"getConfig"),L=a(()=>D.packet,"getPacket"),N=a(t=>{t.length>0&&D.packet.push(t)},"pushWord"),I=a(()=>{B(),D=structuredClone(T)},"clear"),d={pushWord:N,getPacket:L,getConfig:V,clear:I,setAccTitle:S,getAccTitle:$,setDiagramTitle:F,getDiagramTitle:j,getAccDescription:W,setAccDescription:w};var M=1e4,Y=a(t=>{z(t,d);let e=-1,i=[],s=1,{bitsPerRow:c}=d.getConfig();for(let{start:r,end:o,label:m}of t.blocks){if(o&&o<r)throw new Error(`Packet block ${r} - ${o} is invalid. End must be greater than start.`);if(r!==e+1)throw new Error(`Packet block ${r} - ${o??r} is not contiguous. It should start from ${e+1}.`);for(e=o??r,b.debug(`Packet block ${r} - ${e} with label ${m}`);i.length<=c+1&&d.getPacket().length<M;){let[y,l]=U({start:r,end:o,label:m},s,c);if(i.push(y),y.end+1===s*c&&(d.pushWord(i),i=[],s++),!l)break;({start:r,end:o,label:m}=l)}}d.pushWord(i)},"populate"),U=a((t,e,i)=>{if(t.end===void 0&&(t.end=t.start),t.start>t.end)throw new Error(`Block start ${t.start} is greater than block end ${t.end}.`);return t.end+1<=e*i?[t,void 0]:[{start:t.start,end:e*i-1,label:t.label},{start:e*i,end:t.end,label:t.label}]},"getNextFittingBlock"),A={parse:a(async t=>{let e=await v("packet",t);b.debug(e),Y(e)},"parse")};var H=a((t,e,i,s)=>{let c=s.db,r=c.getConfig(),{rowHeight:o,paddingY:m,bitWidth:y,bitsPerRow:l}=r,P=c.getPacket(),n=c.getDiagramTitle(),f=o+m,p=f*(P.length+1)-(n?0:o),k=y*l+2,g=G(e);g.attr("viewbox",`0 0 ${k} ${p}`),C(g,p,k,r.useMaxWidth);for(let[O,_]of P.entries())K(g,_,O,r);g.append("text").text(n).attr("x",k/2).attr("y",p-f/2).attr("dominant-baseline","middle").attr("text-anchor","middle").attr("class","packetTitle")},"draw"),K=a((t,e,i,{rowHeight:s,paddingX:c,paddingY:r,bitWidth:o,bitsPerRow:m,showBits:y})=>{let l=t.append("g"),P=i*(s+r)+r;for(let n of e){let f=n.start%m*o+1,p=(n.end-n.start+1)*o-c;if(l.append("rect").attr("x",f).attr("y",P).attr("width",p).attr("height",s).attr("class","packetBlock"),l.append("text").attr("x",f+p/2).attr("y",P+s/2).attr("class","packetLabel").attr("dominant-baseline","middle").attr("text-anchor","middle").text(n.label),!y)continue;let k=n.end===n.start,g=P-2;l.append("text").attr("x",f+(k?p/2:0)).attr("y",g).attr("class","packetByte start").attr("dominant-baseline","auto").attr("text-anchor",k?"middle":"start").text(n.start),k||l.append("text").attr("x",f+p).attr("y",g).attr("class","packetByte end").attr("dominant-baseline","auto").attr("text-anchor","end").text(n.end)}},"drawWord"),E={draw:H};var X={byteFontSize:"10px",startByteColor:"black",endByteColor:"black",labelColor:"black",labelFontSize:"12px",titleColor:"black",titleFontSize:"14px",blockStrokeColor:"black",blockStrokeWidth:"1",blockFillColor:"#efefef"},R=a(({packet:t}={})=>{let e=u(X,t);return`
	.packetByte {
		font-size: ${e.byteFontSize};
	}
	.packetByte.start {
		fill: ${e.startByteColor};
	}
	.packetByte.end {
		fill: ${e.endByteColor};
	}
	.packetLabel {
		fill: ${e.labelColor};
		font-size: ${e.labelFontSize};
	}
	.packetTitle {
		fill: ${e.titleColor};
		font-size: ${e.titleFontSize};
	}
	.packetBlock {
		stroke: ${e.blockStrokeColor};
		stroke-width: ${e.blockStrokeWidth};
		fill: ${e.blockFillColor};
	}
	`},"styles");var Dt={parser:A,db:d,renderer:E,styles:R};export{Dt as diagram};
