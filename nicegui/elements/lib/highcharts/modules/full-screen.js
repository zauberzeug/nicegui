/*
 Highstock JS v11.1.0 (2023-06-05)

 Advanced Highcharts Stock tools

 (c) 2010-2021 Highsoft AS
 Author: Torstein Honsi

 License: www.highcharts.com/license
*/
'use strict';(function(b){"object"===typeof module&&module.exports?(b["default"]=b,module.exports=b):"function"===typeof define&&define.amd?define("highcharts/modules/full-screen",["highcharts"],function(c){b(c);b.Highcharts=c;return b}):b("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(b){function c(b,e,c,f){b.hasOwnProperty(e)||(b[e]=f.apply(null,c),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:e,module:b[e]}})))}b=b?b._modules:
{};c(b,"Extensions/Exporting/Fullscreen.js",[b["Core/Renderer/HTML/AST.js"],b["Core/Utilities.js"]],function(b,e){function c(){this.fullscreen=new h(this)}const {addEvent:f,fireEvent:g}=e,k=[];class h{static compose(a){e.pushUnique(k,a)&&f(a,"beforeRender",c)}constructor(a){this.chart=a;this.isOpen=!1;a=a.renderTo;this.browserProps||("function"===typeof a.requestFullscreen?this.browserProps={fullscreenChange:"fullscreenchange",requestFullscreen:"requestFullscreen",exitFullscreen:"exitFullscreen"}:
a.mozRequestFullScreen?this.browserProps={fullscreenChange:"mozfullscreenchange",requestFullscreen:"mozRequestFullScreen",exitFullscreen:"mozCancelFullScreen"}:a.webkitRequestFullScreen?this.browserProps={fullscreenChange:"webkitfullscreenchange",requestFullscreen:"webkitRequestFullScreen",exitFullscreen:"webkitExitFullscreen"}:a.msRequestFullscreen&&(this.browserProps={fullscreenChange:"MSFullscreenChange",requestFullscreen:"msRequestFullscreen",exitFullscreen:"msExitFullscreen"}))}close(){const a=
this,b=a.chart,d=b.options.chart;g(b,"fullscreenClose",null,function(){if(a.isOpen&&a.browserProps&&b.container.ownerDocument instanceof Document)b.container.ownerDocument[a.browserProps.exitFullscreen]();a.unbindFullscreenEvent&&(a.unbindFullscreenEvent=a.unbindFullscreenEvent());b.setSize(a.origWidth,a.origHeight,!1);a.origWidth=void 0;a.origHeight=void 0;d.width=a.origWidthOption;d.height=a.origHeightOption;a.origWidthOption=void 0;a.origHeightOption=void 0;a.isOpen=!1;a.setButtonText()})}open(){const a=
this,b=a.chart,d=b.options.chart;g(b,"fullscreenOpen",null,function(){d&&(a.origWidthOption=d.width,a.origHeightOption=d.height);a.origWidth=b.chartWidth;a.origHeight=b.chartHeight;if(a.browserProps){const d=f(b.container.ownerDocument,a.browserProps.fullscreenChange,function(){a.isOpen?(a.isOpen=!1,a.close()):(b.setSize(null,null,!1),a.isOpen=!0,a.setButtonText())}),e=f(b,"destroy",d);a.unbindFullscreenEvent=()=>{d();e()};const c=b.renderTo[a.browserProps.requestFullscreen]();if(c)c["catch"](function(){alert("Full screen is not supported inside a frame.")})}})}setButtonText(){var a=
this.chart,c=a.exportDivElements;const d=a.options.exporting,e=d&&d.buttons&&d.buttons.contextButton.menuItems;a=a.options.lang;d&&d.menuItemDefinitions&&a&&a.exitFullscreen&&a.viewFullscreen&&e&&c&&(c=c[e.indexOf("viewFullscreen")])&&b.setElementHTML(c,this.isOpen?a.exitFullscreen:d.menuItemDefinitions.viewFullscreen.text||a.viewFullscreen)}toggle(){this.isOpen?this.close():this.open()}}"";"";return h});c(b,"masters/modules/full-screen.src.js",[b["Core/Globals.js"],b["Extensions/Exporting/Fullscreen.js"]],
function(b,c){b.Fullscreen=c;c.compose(b.Chart)})});
//# sourceMappingURL=full-screen.js.map