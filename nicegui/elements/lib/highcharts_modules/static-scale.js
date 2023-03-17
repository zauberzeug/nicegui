/*
 Highcharts Gantt JS v10.3.3 (2023-01-20)

 StaticScale

 (c) 2016-2021 Torstein Honsi, Lars A. V. Cabrera

 License: www.highcharts.com/license
*/
(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/static-scale",["highcharts"],function(b){a(b);a.Highcharts=b;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function b(a,c,f,b){a.hasOwnProperty(c)||(a[c]=b.apply(null,f),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:c,module:a[c]}})))}a=a?a._modules:{};
b(a,"Extensions/StaticScale.js",[a["Core/Axis/Axis.js"],a["Core/Chart/Chart.js"],a["Core/Utilities.js"]],function(a,c,b){var g=b.addEvent,f=b.defined,h=b.isNumber,k=b.pick;g(a,"afterSetOptions",function(){var a=this.chart.options.chart;!this.horiz&&h(this.options.staticScale)&&(!a.height||a.scrollablePlotArea&&a.scrollablePlotArea.minHeight)&&(this.staticScale=this.options.staticScale)});c.prototype.adjustHeight=function(){"adjustHeight"!==this.redrawTrigger&&((this.axes||[]).forEach(function(a){var b=
a.chart,c=!!b.initiatedScale&&b.options.animation,d=a.options.staticScale;if(a.staticScale&&f(a.min)){var e=k(a.brokenAxis&&a.brokenAxis.unitLength,a.max+a.tickInterval-a.min)*d;e=Math.max(e,d);d=e-b.plotHeight;!b.scrollablePixelsY&&1<=Math.abs(d)&&(b.plotHeight=e,b.redrawTrigger="adjustHeight",b.setSize(void 0,b.chartHeight+d,c));a.series.forEach(function(a){(a=a.sharedClipKey&&b.sharedClips[a.sharedClipKey])&&a.attr(b.inverted?{width:b.plotHeight}:{height:b.plotHeight})})}}),this.initiatedScale=
!0);this.redrawTrigger=null};g(c,"render",c.prototype.adjustHeight)});b(a,"masters/modules/static-scale.src.js",[],function(){})});
//# sourceMappingURL=static-scale.js.map