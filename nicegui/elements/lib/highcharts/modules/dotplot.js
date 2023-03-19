/*
 Highcharts JS v10.3.3 (2023-01-20)

 Dot plot series type for Highcharts

 (c) 2010-2021 Torstein Honsi

 License: www.highcharts.com/license
*/
(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/dotplot",["highcharts"],function(b){a(b);a.Highcharts=b;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function b(a,g,f,b){a.hasOwnProperty(g)||(a[g]=b.apply(null,f),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:g,module:a[g]}})))}a=a?a._modules:{};b(a,
"Series/DotPlot/DotPlotSeries.js",[a["Series/Column/ColumnSeries.js"],a["Core/Series/SeriesRegistry.js"],a["Core/Utilities.js"]],function(a,b,f){var g=this&&this.__extends||function(){var a=function(e,d){a=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(a,d){a.__proto__=d}||function(a,d){for(var e in d)d.hasOwnProperty(e)&&(a[e]=d[e])};return a(e,d)};return function(e,d){function b(){this.constructor=e}a(e,d);e.prototype=null===d?Object.create(d):(b.prototype=d.prototype,new b)}}(),
t=f.extend,n=f.merge,u=f.pick;f=function(b){function e(){var a=null!==b&&b.apply(this,arguments)||this;a.data=void 0;a.options=void 0;a.points=void 0;return a}g(e,b);e.prototype.drawPoints=function(){var a=this,b=a.chart.renderer,e=this.options.marker,f=this.yAxis.transA*a.options.itemPadding,g=this.borderWidth%2?.5:1;this.points.forEach(function(c){var d;var k=c.marker||{};var v=k.symbol||e.symbol,n=u(k.radius,e.radius),w="rect"!==v;c.graphics=d=c.graphics||[];var m=c.pointAttr?c.pointAttr[c.selected?
"selected":""]||a.pointAttr[""]:a.pointAttribs(c,c.selected&&"select");delete m.r;a.chart.styledMode&&(delete m.stroke,delete m["stroke-width"]);if(null!==c.y){c.graphic||(c.graphic=b.g("point").add(a.group));var p=u(c.stackY,c.y);var q=Math.min(c.pointWidth,a.yAxis.transA-f);var r=Math.floor(p);for(k=p;k>p-c.y;k--,r--){var l=c.barX+(w?c.pointWidth/2-q/2:0);var h=a.yAxis.toPixels(k,!0)+f/2;a.options.crisp&&(l=Math.round(l)-g,h=Math.round(h)+g);l={x:l,y:h,width:Math.round(w?q:c.pointWidth),height:Math.round(q),
r:n};(h=d[r])?h.animate(l):h=b.symbol(v).attr(t(l,m)).add(c.graphic);h.isActive=!0;d[r]=h}}d.forEach(function(a,b){a&&(a.isActive?a.isActive=!1:(a.destroy(),d.splice(b,1)))})})};e.defaultOptions=n(a.defaultOptions,{itemPadding:.2,marker:{symbol:"circle",states:{hover:{},select:{}}}});return e}(a);t(f.prototype,{markerAttribs:void 0});b.registerSeriesType("dotplot",f);return f});b(a,"masters/modules/dotplot.src.js",[],function(){})});
//# sourceMappingURL=dotplot.js.map