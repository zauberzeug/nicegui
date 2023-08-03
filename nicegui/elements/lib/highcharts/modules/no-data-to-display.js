/*
 Highcharts JS v11.1.0 (2023-06-05)

 Plugin for displaying a message when there is no data visible in chart.

 (c) 2010-2021 Highsoft AS
 Author: Oystein Moseng

 License: www.highcharts.com/license
*/
'use strict';(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/no-data-to-display",["highcharts"],function(d){a(d);a.Highcharts=d;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function d(a,e,c,f){a.hasOwnProperty(e)||(a[e]=f.apply(null,c),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:e,module:a[e]}})))}
a=a?a._modules:{};d(a,"Extensions/NoDataToDisplay.js",[a["Core/Renderer/HTML/AST.js"],a["Core/Chart/Chart.js"],a["Core/Defaults.js"],a["Core/Utilities.js"]],function(a,e,c,f){({getOptions:c}=c);const {addEvent:d,extend:g}=f;f=e.prototype;c=c();g(c.lang,{noData:"No data to display"});c.noData={attr:{zIndex:1},position:{x:0,y:0,align:"center",verticalAlign:"middle"},style:{fontWeight:"bold",fontSize:"0.8em",color:"#666666"}};f.showNoData=function(c){var b=this.options;c=c||b&&b.lang.noData||"";b=b&&
(b.noData||{});this.renderer&&(this.noDataLabel||(this.noDataLabel=this.renderer.label(c,0,0,void 0,void 0,void 0,b.useHTML,void 0,"no-data").add()),this.styledMode||this.noDataLabel.attr(a.filterUserAttributes(b.attr||{})).css(b.style||{}),this.noDataLabel.align(g(this.noDataLabel.getBBox(),b.position||{}),!1,"plotBox"))};f.hideNoData=function(){this.noDataLabel&&(this.noDataLabel=this.noDataLabel.destroy())};f.hasData=function(){let a=this.series||[],b=a.length;for(;b--;)if(a[b].hasData()&&!a[b].options.isInternal)return!0;
return this.loadingShown};d(e,"render",function(){this.hasData()?this.hideNoData():this.showNoData()})});d(a,"masters/modules/no-data-to-display.src.js",[],function(){})});
//# sourceMappingURL=no-data-to-display.js.map