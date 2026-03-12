function e(e){return e&&e.__esModule&&Object.prototype.hasOwnProperty.call(e,"default")?e.default:e}
/*!
 * is-number <https://github.com/jonschlinkert/is-number>
 *
 * Copyright (c) 2014-2018, Jon Schlinkert.
 * Released under the MIT License.
 */var r,t,n,u;function o(){return t?r:(t=1,r=function(e){var r=+e;return r-r===0&&(r===e||"string"==typeof e&&(0!==r||""!==e.trim()))})}
/*!
 * is-odd <https://github.com/jonschlinkert/is-odd>
 *
 * Copyright (c) 2015-2017, Jon Schlinkert.
 * Released under the MIT License.
 */var a=function(){if(u)return n;u=1;const e=o();return n=function(r){const t=Math.abs(r);if(!e(t))throw new TypeError("expected a number");if(!Number.isInteger(t))throw new Error("expected an integer");if(!Number.isSafeInteger(t))throw new Error("value exceeds maximum safe integer");return t%2==1}}(),i=e(a);export{i as default};
