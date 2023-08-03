/*
 Highcharts JS v11.1.0 (2023-06-05)

 Highcharts 3D funnel module

 (c) 2010-2021 Kacper Madej

 License: www.highcharts.com/license
*/
'use strict';(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/pyramid3d",["highcharts","highcharts/highcharts-3d","highcharts/modules/cylinder","highcharts/modules/funnel3d"],function(b){a(b);a.Highcharts=b;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function b(a,c,b,d){a.hasOwnProperty(c)||(a[c]=d.apply(null,b),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",
{detail:{path:c,module:a[c]}})))}a=a?a._modules:{};b(a,"Series/Pyramid3D/Pyramid3DSeries.js",[a["Core/Series/SeriesRegistry.js"],a["Core/Utilities.js"]],function(a,c){const {seriesTypes:{funnel3d:b}}=a;({merge:c}=c);class d extends b{constructor(){super(...arguments);this.points=this.options=this.data=void 0}}d.defaultOptions=c(b.defaultOptions,{reversed:!0,neckHeight:0,neckWidth:0,dataLabels:{verticalAlign:"top"}});a.registerSeriesType("pyramid3d",d);"";return d});b(a,"masters/modules/pyramid3d.src.js",
[],function(){})});
//# sourceMappingURL=pyramid3d.js.map