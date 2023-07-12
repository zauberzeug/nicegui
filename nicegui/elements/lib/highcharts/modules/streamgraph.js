/*
 Highcharts JS v11.1.0 (2023-06-05)

 Streamgraph module

 (c) 2010-2021 Torstein Honsi

 License: www.highcharts.com/license
*/
'use strict';(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/streamgraph",["highcharts"],function(b){a(b);a.Highcharts=b;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function b(a,c,b,e){a.hasOwnProperty(c)||(a[c]=e.apply(null,b),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:c,module:a[c]}})))}a=a?a._modules:
{};b(a,"Series/Streamgraph/StreamgraphSeries.js",[a["Core/Series/SeriesRegistry.js"],a["Core/Utilities.js"]],function(a,b){const {seriesTypes:{areaspline:c}}=a,{merge:e,extend:f}=b;class d extends c{constructor(){super(...arguments);this.options=this.points=this.data=void 0}streamStacker(a,b,c){a[0]-=b.total/2;a[1]-=b.total/2;this.stackedYData[c]=a}}d.defaultOptions=e(c.defaultOptions,{fillOpacity:1,lineWidth:0,marker:{enabled:!1},stacking:"stream"});f(d.prototype,{negStacks:!1});a.registerSeriesType("streamgraph",
d);"";return d});b(a,"masters/modules/streamgraph.src.js",[],function(){})});
//# sourceMappingURL=streamgraph.js.map