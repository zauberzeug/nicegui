/*
 Highcharts Gantt JS v11.1.0 (2023-06-05)

 StaticScale

 (c) 2016-2021 Torstein Honsi, Lars A. V. Cabrera

 License: www.highcharts.com/license
*/
'use strict';(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/static-scale",["highcharts"],function(d){a(d);a.Highcharts=d;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function d(a,b,d,f){a.hasOwnProperty(b)||(a[b]=f.apply(null,d),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:b,module:a[b]}})))}a=a?
a._modules:{};d(a,"Extensions/StaticScale.js",[a["Core/Axis/Axis.js"],a["Core/Chart/Chart.js"],a["Core/Utilities.js"]],function(a,b,d){const {addEvent:f,defined:g,isNumber:h,pick:k}=d;f(a,"afterSetOptions",function(){const a=this.chart.options.chart;!this.horiz&&h(this.options.staticScale)&&(!a.height||a.scrollablePlotArea&&a.scrollablePlotArea.minHeight)&&(this.staticScale=this.options.staticScale)});b.prototype.adjustHeight=function(){"adjustHeight"!==this.redrawTrigger&&((this.axes||[]).forEach(function(a){let c=
a.chart,d=!!c.initiatedScale&&c.options.animation;var b=a.options.staticScale;let e;a.staticScale&&g(a.min)&&(e=k(a.brokenAxis&&a.brokenAxis.unitLength,a.max+a.tickInterval-a.min)*b,e=Math.max(e,b),b=e-c.plotHeight,!c.scrollablePixelsY&&1<=Math.abs(b)&&(c.plotHeight=e,c.redrawTrigger="adjustHeight",c.setSize(void 0,c.chartHeight+b,d)),a.series.forEach(function(a){(a=a.sharedClipKey&&c.sharedClips[a.sharedClipKey])&&a.attr(c.inverted?{width:c.plotHeight}:{height:c.plotHeight})}))}),this.initiatedScale=
!0);this.redrawTrigger=null};f(b,"render",b.prototype.adjustHeight)});d(a,"masters/modules/static-scale.src.js",[],function(){})});
//# sourceMappingURL=static-scale.js.map