/*
 Highcharts JS v11.1.0 (2023-06-05)

 (c) 2009-2022

 License: www.highcharts.com/license
*/
'use strict';(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/geoheatmap",["highcharts"],function(c){a(c);a.Highcharts=c;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function c(a,b,c,d){a.hasOwnProperty(b)||(a[b]=d.apply(null,c),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:b,module:a[b]}})))}a=a?a._modules:
{};c(a,"Series/GeoHeatmap/GeoHeatmapPoint.js",[a["Core/Utilities.js"],a["Core/Series/SeriesRegistry.js"]],function(a,b){({map:{prototype:{pointClass:b}}}=b.seriesTypes);const {isNumber:c}=a;class d extends b{constructor(){super(...arguments);this.series=this.options=void 0}applyOptions(a,b){a=super.applyOptions.call(this,a,b);const {lat:e,lon:d}=a.options;if(c(d)&&c(e)){const {colsize:c=1,rowsize:g=1}=this.series.options;b=d-c/2;const f=e-g/2;a.geometry=a.options.geometry={type:"Polygon",coordinates:[[[b,
f],[b+c,f],[b+c,f+g],[b,f+g],[b,f]]]}}return a}}return d});c(a,"Series/GeoHeatmap/GeoHeatmapSeries.js",[a["Core/Series/SeriesRegistry.js"],a["Series/GeoHeatmap/GeoHeatmapPoint.js"],a["Core/Utilities.js"]],function(a,b,c){const {seriesTypes:{map:d}}=a,{extend:k,merge:h}=c;class e extends d{constructor(){super(...arguments);this.points=this.data=this.options=void 0}update(){this.options=h(this.options,arguments[0]);super.update.apply(this,arguments)}}e.defaultOptions=h(d.defaultOptions,{nullColor:"transparent",
tooltip:{pointFormat:"Lat: {point.lat}, Lon: {point.lon}, Value: {point.value}<br/>"},borderWidth:0,colsize:1,rowsize:1});k(e.prototype,{type:"geoheatmap",pointClass:b,pointArrayMap:["lon","lat","value"]});a.registerSeriesType("geoheatmap",e);"";return e});c(a,"masters/modules/geoheatmap.src.js",[],function(){})});
//# sourceMappingURL=geoheatmap.js.map