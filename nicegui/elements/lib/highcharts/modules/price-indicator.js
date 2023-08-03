/*
 Highstock JS v11.1.0 (2023-06-05)

 Advanced Highcharts Stock tools

 (c) 2010-2021 Highsoft AS
 Author: Torstein Honsi

 License: www.highcharts.com/license
*/
'use strict';(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/price-indicator",["highcharts","highcharts/modules/stock"],function(c){a(c);a.Highcharts=c;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function c(a,d,c,h){a.hasOwnProperty(d)||(a[d]=h.apply(null,c),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:d,
module:a[d]}})))}a=a?a._modules:{};c(a,"Extensions/PriceIndication.js",[a["Core/Series/Series.js"],a["Core/Utilities.js"]],function(a,c){const {addEvent:d,isArray:h,merge:m}=c;d(a,"afterRender",function(){var a=this.options;const c=a.lastVisiblePrice;var e=a.lastPrice;if((c||e)&&"highcharts-navigator-series"!==a.id){let d=this.xAxis,b=this.yAxis,n=b.crosshair,p=b.cross,q=b.crossLabel,f=this.points,g=f.length,l=this.xData[this.xData.length-1],k=this.yData[this.yData.length-1];e&&e.enabled&&(b.crosshair=
b.options.crosshair=a.lastPrice,!this.chart.styledMode&&b.crosshair&&b.options.crosshair&&a.lastPrice&&(b.crosshair.color=b.options.crosshair.color=a.lastPrice.color||this.color),b.cross=this.lastPrice,e=h(k)?k[3]:k,this.lastPriceLabel&&this.lastPriceLabel.destroy(),delete b.crossLabel,b.drawCrosshair(null,{x:l,y:e,plotX:d.toPixels(l,!0),plotY:b.toPixels(e,!0)}),this.yAxis.cross&&(this.lastPrice=this.yAxis.cross,this.lastPrice.addClass("highcharts-color-"+this.colorIndex),this.lastPrice.y=e),this.lastPriceLabel=
b.crossLabel);c&&c.enabled&&0<g&&(b.crosshair=b.options.crosshair=m({color:"transparent"},a.lastVisiblePrice),b.cross=this.lastVisiblePrice,a=f[g-1].isInside?f[g-1]:f[g-2],this.lastVisiblePriceLabel&&this.lastVisiblePriceLabel.destroy(),delete b.crossLabel,b.drawCrosshair(null,a),b.cross&&(this.lastVisiblePrice=b.cross,a&&"number"===typeof a.y&&(this.lastVisiblePrice.y=a.y)),this.lastVisiblePriceLabel=b.crossLabel);b.crosshair=b.options.crosshair=n;b.cross=p;b.crossLabel=q}})});c(a,"masters/modules/price-indicator.src.js",
[],function(){})});
//# sourceMappingURL=price-indicator.js.map