/*
 Highcharts JS v11.1.0 (2023-06-05)

 Arrow Symbols

 (c) 2017-2021 Lars A. V. Cabrera

 License: www.highcharts.com/license
*/
'use strict';(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/arrow-symbols",["highcharts"],function(b){a(b);a.Highcharts=b;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function b(a,c,b,f){a.hasOwnProperty(c)||(a[c]=f.apply(null,b),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:c,module:a[c]}})))}a=a?
a._modules:{};b(a,"Extensions/ArrowSymbols.js",[a["Core/Utilities.js"]],function(a){function c(a,g,b,d){return[["M",a,g+d/2],["L",a+b,g],["L",a,g+d/2],["L",a+b,g+d]]}function b(a,b,l,d){return c(a,b,l/2,d)}function f(a,b,c,d){return[["M",a+c,b],["L",a,b+d/2],["L",a+c,b+d],["Z"]]}function h(a,b,c,d){return f(a,b,c/2,d)}const k=[];return{compose:function(e){a.pushUnique(k,e)&&(e=e.prototype.symbols,e.arrow=c,e["arrow-filled"]=f,e["arrow-filled-half"]=h,e["arrow-half"]=b,e["triangle-left"]=f,e["triangle-left-half"]=
h)}}});b(a,"masters/modules/arrow-symbols.src.js",[a["Core/Globals.js"],a["Extensions/ArrowSymbols.js"]],function(a,b){b.compose(a.SVGRenderer)})});
//# sourceMappingURL=arrow-symbols.js.map