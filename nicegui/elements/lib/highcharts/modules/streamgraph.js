/*
 Highcharts JS v10.3.3 (2023-01-20)

 Streamgraph module

 (c) 2010-2021 Torstein Honsi

 License: www.highcharts.com/license
*/
(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/streamgraph",["highcharts"],function(d){a(d);a.Highcharts=d;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function d(a,e,d,f){a.hasOwnProperty(e)||(a[e]=f.apply(null,d),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:e,module:a[e]}})))}a=a?a._modules:{};
d(a,"Series/Streamgraph/StreamgraphSeries.js",[a["Core/Series/SeriesRegistry.js"],a["Core/Utilities.js"]],function(a,e){var d=this&&this.__extends||function(){var a=function(b,c){a=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(a,c){a.__proto__=c}||function(a,c){for(var b in c)c.hasOwnProperty(b)&&(a[b]=c[b])};return a(b,c)};return function(b,c){function d(){this.constructor=b}a(b,c);b.prototype=null===c?Object.create(c):(d.prototype=c.prototype,new d)}}(),f=a.seriesTypes.areaspline,
h=e.merge;e=e.extend;var g=function(a){function b(){var c=null!==a&&a.apply(this,arguments)||this;c.data=void 0;c.points=void 0;c.options=void 0;return c}d(b,a);b.prototype.streamStacker=function(a,b,d){a[0]-=b.total/2;a[1]-=b.total/2;this.stackedYData[d]=a};b.defaultOptions=h(f.defaultOptions,{fillOpacity:1,lineWidth:0,marker:{enabled:!1},stacking:"stream"});return b}(f);e(g.prototype,{negStacks:!1});a.registerSeriesType("streamgraph",g);"";return g});d(a,"masters/modules/streamgraph.src.js",[],
function(){})});
//# sourceMappingURL=streamgraph.js.map