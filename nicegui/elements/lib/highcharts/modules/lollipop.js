/*
 Highcharts JS v11.1.0 (2023-06-05)

 (c) 2009-2021 Sebastian Bochan, Rafal Sebestjanski

 License: www.highcharts.com/license
*/
'use strict';(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/lollipop",["highcharts"],function(b){a(b);a.Highcharts=b;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function b(a,c,b,e){a.hasOwnProperty(c)||(a[c]=e.apply(null,b),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:c,module:a[c]}})))}a=a?a._modules:
{};b(a,"Series/Lollipop/LollipopPoint.js",[a["Core/Series/SeriesRegistry.js"],a["Core/Utilities.js"]],function(a,c){const {series:{prototype:{pointClass:b}},seriesTypes:{scatter:{prototype:{pointClass:e}},dumbbell:{prototype:{pointClass:d}}}}=a;({extend:a}=c);class h extends b{constructor(){super(...arguments);this.plotX=this.series=this.options=void 0}}a(h.prototype,{destroy:d.prototype.destroy,pointSetState:e.prototype.setState,setState:d.prototype.setState});return h});b(a,"Series/Lollipop/LollipopSeries.js",
[a["Series/Lollipop/LollipopPoint.js"],a["Core/Series/SeriesRegistry.js"],a["Core/Series/Series.js"],a["Core/Utilities.js"]],function(a,b,g,e){const {seriesTypes:{column:{prototype:d},dumbbell:{prototype:c}}}=b,{extend:k,merge:l}=e;class f extends g{constructor(){super(...arguments);this.points=this.options=this.data=void 0}drawPoints(){const a=this.points.length;let b=0,c;for(super.drawPoints.apply(this,arguments);b<a;)c=this.points[b],this.drawConnector(c),b++}}f.defaultOptions=l(g.defaultOptions,
{threshold:0,connectorWidth:1,groupPadding:.2,pointPadding:.1,states:{hover:{lineWidthPlus:0,connectorWidthPlus:1,halo:!1}},lineWidth:0,dataLabels:{align:void 0,verticalAlign:void 0},pointRange:1});k(f.prototype,{alignDataLabel:d.alignDataLabel,crispCol:d.crispCol,drawConnector:c.drawConnector,drawDataLabels:d.drawDataLabels,getColumnMetrics:d.getColumnMetrics,getConnectorAttribs:c.getConnectorAttribs,pointClass:a,translate:d.translate});b.registerSeriesType("lollipop",f);"";return f});b(a,"masters/modules/lollipop.src.js",
[],function(){})});
//# sourceMappingURL=lollipop.js.map