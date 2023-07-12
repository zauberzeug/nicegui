/*
 Highcharts JS v11.1.0 (2023-06-05)

 Vector plot series module

 (c) 2010-2021 Torstein Honsi

 License: www.highcharts.com/license
*/
'use strict';(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/vector",["highcharts"],function(c){a(c);a.Highcharts=c;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function c(a,d,c,f){a.hasOwnProperty(d)||(a[d]=f.apply(null,c),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:d,module:a[d]}})))}a=a?a._modules:
{};c(a,"Series/Vector/VectorSeries.js",[a["Core/Animation/AnimationUtilities.js"],a["Core/Globals.js"],a["Core/Series/SeriesRegistry.js"],a["Core/Utilities.js"]],function(a,d,c,f){const {animObject:h}=a,{series:k,seriesTypes:{scatter:g}}=c,{arrayMax:l,extend:m,merge:n,pick:p}=f;class e extends g{constructor(){super(...arguments);this.points=this.options=this.lengthMax=this.data=void 0}animate(a){a?this.markerGroup.attr({opacity:.01}):this.markerGroup.animate({opacity:1},h(this.options.animation))}arrow(a){a=
a.length/this.lengthMax*this.options.vectorLength/20;let b={start:10*a,center:0,end:-10*a}[this.options.rotationOrigin]||0;return[["M",0,7*a+b],["L",-1.5*a,7*a+b],["L",0,10*a+b],["L",1.5*a,7*a+b],["L",0,7*a+b],["L",0,-10*a+b]]}drawPoints(){const a=this.chart;this.points.forEach(function(b){const c=b.plotX,d=b.plotY;!1===this.options.clip||a.isInsidePlot(c,d,{inverted:a.inverted})?(b.graphic||(b.graphic=this.chart.renderer.path().add(this.markerGroup).addClass("highcharts-point highcharts-color-"+
p(b.colorIndex,b.series.colorIndex))),b.graphic.attr({d:this.arrow(b),translateX:c,translateY:d,rotation:b.direction}),this.chart.styledMode||b.graphic.attr(this.pointAttribs(b))):b.graphic&&(b.graphic=b.graphic.destroy())},this)}pointAttribs(a,b){let c=this.options;a=a.color||this.color;let d=this.options.lineWidth;b&&(a=c.states[b].color||a,d=(c.states[b].lineWidth||d)+(c.states[b].lineWidthPlus||0));return{stroke:a,"stroke-width":d}}translate(){k.prototype.translate.call(this);this.lengthMax=l(this.lengthData)}}
e.defaultOptions=n(g.defaultOptions,{lineWidth:2,rotationOrigin:"center",states:{hover:{lineWidthPlus:1}},tooltip:{pointFormat:"<b>[{point.x}, {point.y}]</b><br/>Length: <b>{point.length}</b><br/>Direction: <b>{point.direction}\u00b0</b><br/>"},vectorLength:20},{marker:null});m(e.prototype,{drawGraph:d.noop,getSymbol:d.noop,markerAttribs:d.noop,parallelArrays:["x","y","length","direction"],pointArrayMap:["y","length","direction"]});c.registerSeriesType("vector",e);"";return e});c(a,"masters/modules/vector.src.js",
[],function(){})});
//# sourceMappingURL=vector.js.map