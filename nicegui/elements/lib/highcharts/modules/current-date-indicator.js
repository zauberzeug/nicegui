/*
 Highcharts Gantt JS v10.3.3 (2023-01-20)

 CurrentDateIndicator

 (c) 2010-2021 Lars A. V. Cabrera

 License: www.highcharts.com/license
*/
(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/current-date-indicator",["highcharts"],function(b){a(b);a.Highcharts=b;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function b(a,d,e,b){a.hasOwnProperty(d)||(a[d]=b.apply(null,e),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:d,module:a[d]}})))}a=a?a._modules:
{};b(a,"Extensions/CurrentDateIndication.js",[a["Core/Axis/Axis.js"],a["Core/Axis/PlotLineOrBand/PlotLineOrBand.js"],a["Core/Utilities.js"]],function(a,b,e){var d=e.addEvent,f=e.merge;e=e.wrap;var g={color:"#ccd6eb",width:2,label:{format:"%a, %b %d %Y, %H:%M",formatter:function(a,c){return this.axis.chart.time.dateFormat(c||"",a)},rotation:0,style:{fontSize:"10px"}}};d(a,"afterSetOptions",function(){var a=this.options,c=a.currentDateIndicator;c&&(c="object"===typeof c?f(g,c):f(g),c.value=Date.now(),
c.className="highcharts-current-date-indicator",a.plotLines||(a.plotLines=[]),a.plotLines.push(c))});d(b,"render",function(){this.label&&this.label.attr({text:this.getLabelText(this.options.label)})});e(b.prototype,"getLabelText",function(a,c){var b=this.options;return b&&b.className&&-1!==b.className.indexOf("highcharts-current-date-indicator")&&b.label&&"function"===typeof b.label.formatter?(b.value=Date.now(),b.label.formatter.call(this,b.value,b.label.format)):a.call(this,c)})});b(a,"masters/modules/current-date-indicator.src.js",
[],function(){})});
//# sourceMappingURL=current-date-indicator.js.map