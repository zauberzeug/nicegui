/*
 Highcharts JS v10.3.2 (2022-11-28)

 Dot plot series type for Highcharts

 (c) 2010-2021 Torstein Honsi

 License: www.highcharts.com/license
*/
(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/dotplot",["highcharts"],function(b){a(b);a.Highcharts=b;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function b(a,g,f,b){a.hasOwnProperty(g)||(a[g]=b.apply(null,f),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:g,module:a[g]}})))}a=a?a._modules:{};b(a,
"Series/DotPlot/DotPlotSeries.js",[a["Series/Column/ColumnSeries.js"],a["Core/Series/SeriesRegistry.js"],a["Core/Utilities.js"]],function(a,b,f){var g=this&&this.__extends||function(){var a=function(e,c){a=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(a,c){a.__proto__=c}||function(a,c){for(var e in c)c.hasOwnProperty(e)&&(a[e]=c[e])};return a(e,c)};return function(e,c){function b(){this.constructor=e}a(e,c);e.prototype=null===c?Object.create(c):(b.prototype=c.prototype,new b)}}(),
t=f.extend,n=f.merge,u=f.pick;f=function(b){function e(){var a=null!==b&&b.apply(this,arguments)||this;a.data=void 0;a.options=void 0;a.points=void 0;return a}g(e,b);e.prototype.drawPoints=function(){var a=this,b=a.chart.renderer,e=this.options.marker,f=this.yAxis.transA*a.options.itemPadding,g=this.borderWidth%2?.5:1;this.points.forEach(function(d){var c;var h=d.marker||{};var v=h.symbol||e.symbol,n=u(h.radius,e.radius),w="rect"!==v;d.graphics=c=d.graphics||[];var m=d.pointAttr?d.pointAttr[d.selected?
"selected":""]||a.pointAttr[""]:a.pointAttribs(d,d.selected&&"select");delete m.r;a.chart.styledMode&&(delete m.stroke,delete m["stroke-width"]);if(null!==d.y){d.graphic||(d.graphic=b.g("point").add(a.group));var p=u(d.stackY,d.y);var q=Math.min(d.pointWidth,a.yAxis.transA-f);var l=Math.floor(p);for(h=p;h>p-d.y;h--,l--){var k=d.barX+(w?d.pointWidth/2-q/2:0);var r=a.yAxis.toPixels(h,!0)+f/2;a.options.crisp&&(k=Math.round(k)-g,r=Math.round(r)+g);k={x:k,y:r,width:Math.round(w?q:d.pointWidth),height:Math.round(q),
r:n};c[l]?c[l].animate(k):c[l]=b.symbol(v).attr(t(k,m)).add(d.graphic);c[l].isActive=!0}}c.forEach(function(a,b){a.isActive?a.isActive=!1:(a.destroy(),c.splice(b,1))})})};e.defaultOptions=n(a.defaultOptions,{itemPadding:.2,marker:{symbol:"circle",states:{hover:{},select:{}}}});return e}(a);t(f.prototype,{markerAttribs:void 0});b.registerSeriesType("dotplot",f);return f});b(a,"masters/modules/dotplot.src.js",[],function(){})});
//# sourceMappingURL=dotplot.js.map