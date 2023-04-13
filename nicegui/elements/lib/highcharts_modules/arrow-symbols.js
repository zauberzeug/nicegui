/*
 Highcharts JS v10.3.3 (2023-01-20)

 Arrow Symbols

 (c) 2017-2021 Lars A. V. Cabrera

 License: www.highcharts.com/license
*/
(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/arrow-symbols",["highcharts"],function(b){a(b);a.Highcharts=b;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function b(a,f,b,g){a.hasOwnProperty(f)||(a[f]=g.apply(null,b),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:f,module:a[f]}})))}a=a?a._modules:{};
b(a,"Extensions/ArrowSymbols.js",[a["Core/Renderer/SVG/SVGRenderer.js"]],function(a){function b(a,d,b,c){return[["M",a,d+c/2],["L",a+b,d],["L",a,d+c/2],["L",a+b,d+c]]}function h(a,b,e,c){return[["M",a+e,b],["L",a,b+c/2],["L",a+e,b+c],["Z"]]}function g(a,b,e,c){return h(a,b,e/2,c)}a=a.prototype.symbols;a.arrow=b;a["arrow-filled"]=h;a["arrow-filled-half"]=g;a["arrow-half"]=function(a,d,e,c){return b(a,d,e/2,c)};a["triangle-left"]=h;a["triangle-left-half"]=g;return a});b(a,"masters/modules/arrow-symbols.src.js",
[],function(){})});
//# sourceMappingURL=arrow-symbols.js.map