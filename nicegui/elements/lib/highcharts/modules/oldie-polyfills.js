/*
 Highcharts JS v10.3.3 (2023-01-20)

 Old IE (v6, v7, v8) array polyfills for Highcharts v7+.

 (c) 2010-2021 Highsoft AS
 Author: Torstein Honsi

 License: www.highcharts.com/license
*/
(function(b){"object"===typeof module&&module.exports?(b["default"]=b,module.exports=b):"function"===typeof define&&define.amd?define("highcharts/modules/oldie-polyfills",["highcharts"],function(e){b(e);b.Highcharts=e;return b}):b("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(b){function e(b,d,c,a){b.hasOwnProperty(d)||(b[d]=a.apply(null,c),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:d,module:b[d]}})))}b=b?b._modules:
{};e(b,"Extensions/OldiePolyfills.js",[],function(){String.prototype.trim||(String.prototype.trim=function(){return this.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,"")});Array.prototype.forEach||(Array.prototype.forEach=function(d,c){for(var a=0,b=this.length;a<b;a++)if("undefined"!==typeof this[a]&&!1===d.call(c,this[a],a,this))return a});Array.prototype.map||(Array.prototype.map=function(d){for(var c=[],a=0,b=this.length;a<b;a++)c[a]=d.call(this[a],this[a],a,this);return c});Array.prototype.indexOf||
(Array.prototype.indexOf=function(d,c){var a=c||0;if(this)for(c=this.length;a<c;a++)if(this[a]===d)return a;return-1});Array.prototype.filter||(Array.prototype.filter=function(d){for(var c=[],a=0,b=this.length;a<b;a++)d(this[a],a)&&c.push(this[a]);return c});Array.prototype.some||(Array.prototype.some=function(d,c){for(var a=0,b=this.length;a<b;a++)if(!0===d.call(c,this[a],a,this))return!0;return!1});Array.prototype.reduce||(Array.prototype.reduce=function(d,c){for(var a=1<arguments.length?0:1,b=
1<arguments.length?c:this[0],e=this.length;a<e;++a)b=d.call(this,b,this[a],a,this);return b});Function.prototype.bind||(Function.prototype.bind=function(){var d=this,c=arguments[0],a=Array.prototype.slice.call(arguments,1);if("function"!==typeof d)throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");return function(){var b=a.concat(Array.prototype.slice.call(arguments));return d.apply(c,b)}});Object.getPrototypeOf||(Object.getPrototypeOf="object"===typeof"test".__proto__?
function(b){return b.__proto__}:function(b){var c=b.constructor.prototype;return c===b?{}.constructor.prototype:c});Object.keys||(Object.keys=function(b){var c=[],a;for(a in b)Object.hasOwnProperty.call(b,a)&&c.push(a);return c});if(!document.getElementsByClassName){var b=function(b){var c=document,a,d=[];if(c.querySelectorAll)return c.querySelectorAll("."+b);if(c.evaluate)for(c=c.evaluate(".//*[contains(concat(' ', @class, ' '), ' "+b+" ')]",c,null,0,null);a=c.iterateNext();)d.push(a);else for(c=
c.getElementsByTagName("*"),b=new RegExp("(^|\\s)"+b+"(\\s|$)"),a=0;a<c.length;a++)b.test(c[a].className)&&d.push(c[a]);return d};document.getElementsByClassName=b;Element.prototype.getElementsByClassName=b}});e(b,"masters/modules/oldie-polyfills.src.js",[],function(){})});
//# sourceMappingURL=oldie-polyfills.js.map