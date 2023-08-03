/*
 Highstock JS v11.1.0 (2023-06-05)

 HeikinAshi series type for Highcharts Stock

 (c) 2010-2021 Karol Kolodziej

 License: www.highcharts.com/license
*/
'use strict';(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/heikinashi",["highcharts","highcharts/modules/stock"],function(c){a(c);a.Highcharts=c;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function c(a,b,c,e){a.hasOwnProperty(b)||(a[b]=e.apply(null,c),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:b,
module:a[b]}})))}a=a?a._modules:{};c(a,"Series/HeikinAshi/HeikinAshiPoint.js",[a["Core/Series/SeriesRegistry.js"]],function(a){const {candlestick:{prototype:{pointClass:b}},hlc:{prototype:{pointClass:c}}}=a.seriesTypes;class e extends b{constructor(){super(...arguments);this.resolveColor=c.prototype.resolveColor}}return e});c(a,"Series/HeikinAshi/HeikinAshiSeriesDefaults.js",[],function(){"";return{dataGrouping:{groupAll:!0}}});c(a,"Series/HeikinAshi/HeikinAshiSeries.js",[a["Series/HeikinAshi/HeikinAshiPoint.js"],
a["Series/HeikinAshi/HeikinAshiSeriesDefaults.js"],a["Core/Series/SeriesRegistry.js"],a["Core/Utilities.js"]],function(a,c,l,e){function b(){this.series.forEach(a=>{a.is("heikinashi")&&(a.heikiashiData.length=0,a.getHeikinashiData())})}function n(){const a=this.points,p=this.heikiashiData,c=this.cropStart||0;this.processedYData.length=0;for(let d=0;d<a.length;d++){const b=a[d],g=p[d+c];b.open=g[0];b.high=g[1];b.low=g[2];b.close=g[3];this.processedYData.push([b.open,b.high,b.low,b.close])}}function q(){this.heikiashiData.length&&
(this.heikiashiData.length=0)}const {candlestick:h}=l.seriesTypes,{addEvent:k,merge:r}=e,m=[];class f extends h{constructor(){super(...arguments);this.data=void 0;this.heikiashiData=[];this.processedYData=this.yData=this.points=this.options=void 0}static compose(a,c,...g){h.compose(a);e.pushUnique(m,c)&&k(c,"postProcessData",b);e.pushUnique(m,f)&&(k(f,"afterTranslate",n),k(f,"updatedData",q))}getHeikinashiData(){const a=this.allGroupedData||this.yData,b=this.heikiashiData;if(!b.length&&a&&a.length){this.modifyFirstPointValue(a[0]);
for(let d=1;d<a.length;d++)this.modifyDataPoint(a[d],b[d-1])}this.heikiashiData=b}init(){super.init.apply(this,arguments);this.heikiashiData=[]}modifyFirstPointValue(a){this.heikiashiData.push([(a[0]+a[1]+a[2]+a[3])/4,a[1],a[2],(a[0]+a[3])/2])}modifyDataPoint(a,b){b=(b[0]+b[3])/2;const c=(a[0]+a[1]+a[2]+a[3])/4;this.heikiashiData.push([b,Math.max(a[1],c,b),Math.min(a[2],c,b),c])}}f.defaultOptions=r(h.defaultOptions,c);f.prototype.pointClass=a;l.registerSeriesType("heikinashi",f);return f});c(a,"masters/modules/heikinashi.src.js",
[a["Core/Globals.js"],a["Series/HeikinAshi/HeikinAshiSeries.js"]],function(a,b){b.compose(a.Series,a.Axis)})});
//# sourceMappingURL=heikinashi.js.map