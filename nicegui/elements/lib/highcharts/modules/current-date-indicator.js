/*
 Highcharts Gantt JS v11.1.0 (2023-06-05)

 CurrentDateIndicator

 (c) 2010-2021 Lars A. V. Cabrera

 License: www.highcharts.com/license
*/
'use strict';(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/current-date-indicator",["highcharts"],function(b){a(b);a.Highcharts=b;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function b(a,d,b,f){a.hasOwnProperty(d)||(a[d]=f.apply(null,b),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:d,module:a[d]}})))}
a=a?a._modules:{};b(a,"Extensions/CurrentDateIndication.js",[a["Core/Utilities.js"]],function(a){function d(){const a=this.options;var c=a.currentDateIndicator;c&&(c="object"===typeof c?e(h,c):e(h),c.value=Date.now(),c.className="highcharts-current-date-indicator",a.plotLines||(a.plotLines=[]),a.plotLines.push(c))}function b(){this.label&&this.label.attr({text:this.getLabelText(this.options.label)})}function f(a,c){const b=this.options;return b&&b.className&&-1!==b.className.indexOf("highcharts-current-date-indicator")&&
b.label&&"function"===typeof b.label.formatter?(b.value=Date.now(),b.label.formatter.call(this,b.value,b.label.format)):a.call(this,c)}const {addEvent:g,merge:e,wrap:l}=a,k=[],h={color:"#ccd3ff",width:2,label:{format:"%a, %b %d %Y, %H:%M",formatter:function(a,b){return this.axis.chart.time.dateFormat(b||"",a)},rotation:0,style:{fontSize:"0.7em"}}};return{compose:function(e,c){a.pushUnique(k,e)&&g(e,"afterSetOptions",d);a.pushUnique(k,c)&&(g(c,"render",b),l(c.prototype,"getLabelText",f))}}});b(a,"masters/modules/current-date-indicator.src.js",
[a["Core/Globals.js"],a["Extensions/CurrentDateIndication.js"]],function(a,b){b.compose(a.Axis,a.PlotLineOrBand)})});
//# sourceMappingURL=current-date-indicator.js.map