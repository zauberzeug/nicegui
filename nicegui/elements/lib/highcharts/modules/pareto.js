/*
 Highcharts JS v11.1.0 (2023-06-05)

 Pareto series type for Highcharts

 (c) 2010-2021 Sebastian Bochan

 License: www.highcharts.com/license
*/
'use strict';(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/pareto",["highcharts"],function(b){a(b);a.Highcharts=b;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function b(a,c,b,m){a.hasOwnProperty(c)||(a[c]=m.apply(null,b),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:c,module:a[c]}})))}a=a?a._modules:
{};b(a,"Series/DerivedComposition.js",[a["Core/Globals.js"],a["Core/Series/Series.js"],a["Core/Utilities.js"]],function(a,c,b){const {noop:m}=a,{addEvent:g,defined:n}=b;var e;(function(a){function h(){c.prototype.init.apply(this,arguments);this.initialised=!1;this.baseSeries=null;this.eventRemovers=[];this.addEvents()}function k(){const a=this.chart,d=this.options.baseSeries;this.baseSeries=n(d)&&(a.series[d]||a.get(d))||null}function l(){this.eventRemovers.push(g(this.chart,"afterLinkSeries",()=>
{this.setBaseSeries();this.baseSeries&&!this.initialised&&(this.setDerivedData(),this.addBaseSeriesEvents(),this.initialised=!0)}))}function e(){this.eventRemovers.push(g(this.baseSeries,"updatedData",()=>{this.setDerivedData()}),g(this.baseSeries,"destroy",()=>{this.baseSeries=null;this.initialised=!1}))}function f(){this.eventRemovers.forEach(a=>{a()});c.prototype.destroy.apply(this,arguments)}const q=[];a.hasDerivedData=!0;a.setDerivedData=m;a.compose=function(a){if(b.pushUnique(q,a)){const d=
a.prototype;d.addBaseSeriesEvents=e;d.addEvents=l;d.destroy=f;d.init=h;d.setBaseSeries=k}return a};a.init=h;a.setBaseSeries=k;a.addEvents=l;a.addBaseSeriesEvents=e;a.destroy=f})(e||(e={}));return e});b(a,"Series/ParetoSeries/ParetoSeries.js",[a["Series/DerivedComposition.js"],a["Core/Series/SeriesRegistry.js"],a["Core/Utilities.js"]],function(a,b,p){const {seriesTypes:{line:c}}=b,{correctFloat:g,merge:n,extend:e}=p;class f extends c{constructor(){super(...arguments);this.options=this.points=this.data=
void 0}sumPointsPercents(a,b,c,e){let f=0,h=0,k=[],d;a.forEach(function(a,l){null!==a&&(e?f+=a:(d=a/c*100,k.push([b[l],g(h+d)]),h+=d))});return e?f:k}setDerivedData(){const a=this.baseSeries.xData,b=this.baseSeries.yData,c=this.sumPointsPercents(b,a,null,!0);this.setData(this.sumPointsPercents(b,a,c,!1),!1)}}f.defaultOptions=n(c.defaultOptions,{zIndex:3});e(f.prototype,{hasDerivedData:a.hasDerivedData});a.compose(f);b.registerSeriesType("pareto",f);"";return f});b(a,"masters/modules/pareto.src.js",
[],function(){})});
//# sourceMappingURL=pareto.js.map