/*
 Highcharts JS v10.3.3 (2023-01-20)

 Highcharts 3D funnel module

 (c) 2010-2021 Kacper Madej

 License: www.highcharts.com/license
*/
(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/pyramid3d",["highcharts","highcharts/highcharts-3d","highcharts/modules/cylinder","highcharts/modules/funnel3d"],function(b){a(b);a.Highcharts=b;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function b(a,c,b,e){a.hasOwnProperty(c)||(a[c]=e.apply(null,b),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",
{detail:{path:c,module:a[c]}})))}a=a?a._modules:{};b(a,"Series/Pyramid3D/Pyramid3DSeries.js",[a["Core/Series/SeriesRegistry.js"],a["Core/Utilities.js"]],function(a,c){var b=this&&this.__extends||function(){var a=function(b,d){a=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(a,b){a.__proto__=b}||function(a,b){for(var d in b)b.hasOwnProperty(d)&&(a[d]=b[d])};return a(b,d)};return function(b,d){function c(){this.constructor=b}a(b,d);b.prototype=null===d?Object.create(d):(c.prototype=
d.prototype,new c)}}(),e=a.seriesTypes.funnel3d,f=c.merge;c=function(a){function c(){var b=null!==a&&a.apply(this,arguments)||this;b.data=void 0;b.options=void 0;b.points=void 0;return b}b(c,a);c.defaultOptions=f(e.defaultOptions,{reversed:!0,neckHeight:0,neckWidth:0,dataLabels:{verticalAlign:"top"}});return c}(e);a.registerSeriesType("pyramid3d",c);"";return c});b(a,"masters/modules/pyramid3d.src.js",[],function(){})});
//# sourceMappingURL=pyramid3d.js.map