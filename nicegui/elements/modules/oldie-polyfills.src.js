/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * Old IE (v6, v7, v8) array polyfills for Highcharts v7+.
 *
 * (c) 2010-2021 Highsoft AS
 * Author: Torstein Honsi
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/oldie-polyfills', ['highcharts'], function (Highcharts) {
            factory(Highcharts);
            factory.Highcharts = Highcharts;
            return factory;
        });
    } else {
        factory(typeof Highcharts !== 'undefined' ? Highcharts : undefined);
    }
}(function (Highcharts) {
    'use strict';
    var _modules = Highcharts ? Highcharts._modules : {};
    function _registerModule(obj, path, args, fn) {
        if (!obj.hasOwnProperty(path)) {
            obj[path] = fn.apply(null, args);

            if (typeof CustomEvent === 'function') {
                window.dispatchEvent(
                    new CustomEvent(
                        'HighchartsModuleLoaded',
                        { detail: { path: path, module: obj[path] }
                    })
                );
            }
        }
    }
    _registerModule(_modules, 'Extensions/OldiePolyfills.js', [], function () {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  Simple polyfills for array functions in old IE browsers (6, 7 and 8) in
         *  Highcharts v7+. These polyfills are sufficient for Highcharts to work, but
         *  for fully compatible polyfills, see MDN.
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /* global document */
        /* eslint-disable no-extend-native */
        if (!String.prototype.trim) {
            String.prototype.trim = function () {
                return this.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, '');
            };
        }
        if (!Array.prototype.forEach) {
            Array.prototype.forEach = function (fn, thisArg) {
                var i = 0,
                    len = this.length;
                for (; i < len; i++) {
                    if (typeof this[i] !== 'undefined' && // added check
                        fn.call(thisArg, this[i], i, this) === false) {
                        return i;
                    }
                }
            };
        }
        if (!Array.prototype.map) {
            Array.prototype.map = function (fn
            // @todo support optional ctx
            ) {
                var results = [],
                    i = 0,
                    len = this.length;
                for (; i < len; i++) {
                    results[i] = fn.call(this[i], this[i], i, this);
                }
                return results;
            };
        }
        if (!Array.prototype.indexOf) {
            Array.prototype.indexOf = function (member, fromIndex) {
                var arr = this, // #8874
                    len,
                    i = fromIndex || 0; // #8346
                    if (arr) {
                        len = arr.length;
                    for (; i < len; i++) {
                        if (arr[i] === member) {
                            return i;
                        }
                    }
                }
                return -1;
            };
        }
        if (!Array.prototype.filter) {
            Array.prototype.filter = function (fn
            // @todo support optional ctx
            ) {
                var ret = [],
                    i = 0,
                    length = this.length;
                for (; i < length; i++) {
                    if (fn(this[i], i)) {
                        ret.push(this[i]);
                    }
                }
                return ret;
            };
        }
        if (!Array.prototype.some) {
            Array.prototype.some = function (fn, thisArg) {
                var i = 0,
                    len = this.length;
                for (; i < len; i++) {
                    if (fn.call(thisArg, this[i], i, this) === true) {
                        return true;
                    }
                }
                return false;
            };
        }
        if (!Array.prototype.reduce) {
            Array.prototype.reduce = function (func, initialValue) {
                var context = this,
                    i = arguments.length > 1 ? 0 : 1,
                    accumulator = arguments.length > 1 ? initialValue : this[0],
                    len = this.length;
                for (; i < len; ++i) {
                    accumulator = func.call(context, accumulator, this[i], i, this);
                }
                return accumulator;
            };
        }
        if (!Function.prototype.bind) {
            Function.prototype.bind = function () {
                var thatFunc = this;
                var thatArg = arguments[0];
                var args = Array.prototype.slice.call(arguments, 1);
                if (typeof thatFunc !== 'function') {
                    // closest thing possible to the ECMAScript 5
                    // internal IsCallable function
                    throw new TypeError('Function.prototype.bind - ' +
                        'what is trying to be bound is not callable');
                }
                return function () {
                    var funcArgs = args.concat(Array.prototype.slice.call(arguments));
                    return thatFunc.apply(thatArg, funcArgs);
                };
            };
        }
        // Adapted from https://johnresig.com/blog/objectgetprototypeof/
        if (!Object.getPrototypeOf) {
            if (typeof 'test'.__proto__ === 'object') { // eslint-disable-line no-proto
                Object.getPrototypeOf = function (object) {
                    return object.__proto__; // eslint-disable-line no-proto
                };
            }
            else {
                Object.getPrototypeOf = function (object) {
                    var proto = object.constructor.prototype;
                    if (proto === object) {
                        return {}.constructor.prototype;
                    }
                    // May break if the constructor has been tampered with
                    return proto;
                };
            }
        }
        if (!Object.keys) {
            Object.keys = function (obj) {
                var result = [],
                    prop;
                for (prop in obj) {
                    if (Object.hasOwnProperty.call(obj, prop)) {
                        result.push(prop);
                    }
                }
                return result;
            };
        }
        // Add a getElementsByClassName function if the browser doesn't have one
        // Limitation: only works with one class name
        // Copyright: Eike Send https://eike.se/nd
        // License: MIT License
        if (!document.getElementsByClassName) {
            var getElementsByClassNamePolyfill = function (search) {
                    var d = document,
                elements,
                pattern,
                i,
                results = [];
                if (d.querySelectorAll) { // IE8
                    return d.querySelectorAll('.' + search);
                }
                if (d.evaluate) { // IE6, IE7
                    pattern = './/*[contains(concat(\' \', @class, \' \'), \' ' +
                        search + ' \')]';
                    elements = d.evaluate(pattern, d, null, 0, null);
                    while ((i = elements.iterateNext())) {
                        results.push(i);
                    }
                }
                else {
                    elements = d.getElementsByTagName('*');
                    pattern = new RegExp('(^|\\s)' + search + '(\\s|$)');
                    for (i = 0; i < elements.length; i++) {
                        if (pattern.test(elements[i].className)) {
                            results.push(elements[i]);
                        }
                    }
                }
                return results;
            };
            document.getElementsByClassName = getElementsByClassNamePolyfill;
            Element.prototype.getElementsByClassName = getElementsByClassNamePolyfill;
        }

    });
    _registerModule(_modules, 'masters/modules/oldie-polyfills.src.js', [], function () {


    });
}));