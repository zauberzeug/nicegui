/*
 Highcharts JS v11.1.0 (2023-06-05)

 Dot plot series type for Highcharts

 (c) 2010-2021 Torstein Honsi

 License: www.highcharts.com/license
*/
'use strict';(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/dotplot",["highcharts"],function(c){a(c);a.Highcharts=c;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function c(a,e,c,x){a.hasOwnProperty(e)||(a[e]=x.apply(null,c),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:e,module:a[e]}})))}a=a?a._modules:
{};c(a,"Series/DotPlot/DotPlotSeries.js",[a["Series/Column/ColumnSeries.js"],a["Core/Series/SeriesRegistry.js"],a["Core/Utilities.js"]],function(a,c,p){const {extend:e,merge:y,pick:r}=p;class f extends a{constructor(){super(...arguments);this.points=this.options=this.data=void 0}drawPoints(){const a=this,c=a.chart.renderer,f=this.options.marker,t=this.yAxis.transA*a.options.itemPadding,u=this.borderWidth%2?.5:1;this.points.forEach(function(b){let k,l;var g=b.marker||{};let v=g.symbol||f.symbol,p=
r(g.radius,f.radius),m,n,w="rect"!==v;b.graphics=k=b.graphics||[];l=b.pointAttr?b.pointAttr[b.selected?"selected":""]||a.pointAttr[""]:a.pointAttribs(b,b.selected&&"select");delete l.r;a.chart.styledMode&&(delete l.stroke,delete l["stroke-width"]);if(null!==b.y){b.graphic||(b.graphic=c.g("point").add(a.group));n=r(b.stackY,b.y);m=Math.min(b.pointWidth,a.yAxis.transA-t);let q=Math.floor(n);for(g=n;g>n-b.y;g--,q--){var h=b.barX+(w?b.pointWidth/2-m/2:0);var d=a.yAxis.toPixels(g,!0)+t/2;a.options.crisp&&
(h=Math.round(h)-u,d=Math.round(d)+u);h={x:h,y:d,width:Math.round(w?m:b.pointWidth),height:Math.round(m),r:p};(d=k[q])?d.animate(h):d=c.symbol(v).attr(e(h,l)).add(b.graphic);d.isActive=!0;k[q]=d}}k.forEach((a,b)=>{a&&(a.isActive?a.isActive=!1:(a.destroy(),k.splice(b,1)))})})}}f.defaultOptions=y(a.defaultOptions,{itemPadding:.2,marker:{symbol:"circle",states:{hover:{},select:{}}}});e(f.prototype,{markerAttribs:void 0});c.registerSeriesType("dotplot",f);return f});c(a,"masters/modules/dotplot.src.js",
[],function(){})});
//# sourceMappingURL=dotplot.js.map