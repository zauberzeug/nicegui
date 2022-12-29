/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * Accessibility module
 *
 * (c) 2010-2021 Highsoft AS
 * Author: Oystein Moseng
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/accessibility', ['highcharts'], function (Highcharts) {
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
    _registerModule(_modules, 'Accessibility/Utils/HTMLUtilities.js', [_modules['Core/Globals.js'], _modules['Core/Utilities.js']], function (H, U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Utility functions for accessibility module.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var doc = H.doc,
            win = H.win;
        var css = U.css;
        /* *
         *
         *  Constants
         *
         * */
        var simulatedEventTarget = win.EventTarget && new win.EventTarget() || 'none';
        /* *
         *
         *  Functions
         *
         * */
        /* eslint-disable valid-jsdoc */
        /**
         * @private
         * @param {Highcharts.HTMLDOMElement} el
         * @param {string} className
         * @return {void}
         */
        function addClass(el, className) {
            if (el.classList) {
                el.classList.add(className);
            }
            else if (el.className.indexOf(className) < 0) {
                // Note: Dumb check for class name exists, should be fine for practical
                // use cases, but will return false positives if the element has a class
                // that contains the className.
                el.className += ' ' + className;
            }
        }
        /**
         * @private
         * @param {Highcharts.HTMLDOMElement} el
         * @param {string} className
         * @return {void}
         */
        function removeClass(el, className) {
            if (el.classList) {
                el.classList.remove(className);
            }
            else {
                // Note: Dumb logic that will break if the element has a class name that
                // consists of className plus something else.
                el.className = el.className.replace(new RegExp(className, 'g'), '');
            }
        }
        /**
         * Utility function to clone a mouse event for re-dispatching.
         * @private
         */
        function cloneMouseEvent(e) {
            if (typeof win.MouseEvent === 'function') {
                return new win.MouseEvent(e.type, e);
            }
            // No MouseEvent support, try using initMouseEvent
            if (doc.createEvent) {
                var evt = doc.createEvent('MouseEvent');
                if (evt.initMouseEvent) {
                    evt.initMouseEvent(e.type, e.bubbles, // #10561, #12161
                    e.cancelable, e.view || win, e.detail, e.screenX, e.screenY, e.clientX, e.clientY, e.ctrlKey, e.altKey, e.shiftKey, e.metaKey, e.button, e.relatedTarget);
                    return evt;
                }
            }
            return getFakeMouseEvent(e.type);
        }
        /**
         * Utility function to clone a touch event for re-dispatching.
         * @private
         */
        function cloneTouchEvent(e) {
            var touchListToTouchArray = function (l) {
                    var touchArray = [];
                for (var i = 0; i < l.length; ++i) {
                    var item = l.item(i);
                    if (item) {
                        touchArray.push(item);
                    }
                }
                return touchArray;
            };
            if (typeof win.TouchEvent === 'function') {
                var newEvent = new win.TouchEvent(e.type, {
                        touches: touchListToTouchArray(e.touches),
                        targetTouches: touchListToTouchArray(e.targetTouches),
                        changedTouches: touchListToTouchArray(e.changedTouches),
                        ctrlKey: e.ctrlKey,
                        shiftKey: e.shiftKey,
                        altKey: e.altKey,
                        metaKey: e.metaKey,
                        bubbles: e.bubbles,
                        cancelable: e.cancelable,
                        composed: e.composed,
                        detail: e.detail,
                        view: e.view
                    });
                if (e.defaultPrevented) {
                    newEvent.preventDefault();
                }
                return newEvent;
            }
            var fakeEvt = cloneMouseEvent(e);
            fakeEvt.touches = e.touches;
            fakeEvt.changedTouches = e.changedTouches;
            fakeEvt.targetTouches = e.targetTouches;
            return fakeEvt;
        }
        /**
         * @private
         */
        function escapeStringForHTML(str) {
            return str
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#x27;')
                .replace(/\//g, '&#x2F;');
        }
        /**
         * Get an element by ID
         * @private
         */
        function getElement(id) {
            return doc.getElementById(id);
        }
        /**
         * Get a fake mouse event of a given type. If relatedTarget is not given,
         * it will point to simulatedEventTarget, as an indicator that the event
         * is fake.
         * @private
         */
        function getFakeMouseEvent(type, position, relatedTarget) {
            var pos = position || {
                    x: 0,
                    y: 0
                };
            if (typeof win.MouseEvent === 'function') {
                return new win.MouseEvent(type, {
                    bubbles: true,
                    cancelable: true,
                    composed: true,
                    button: 0,
                    buttons: 1,
                    relatedTarget: relatedTarget || simulatedEventTarget,
                    view: win,
                    detail: type === 'click' ? 1 : 0,
                    screenX: pos.x,
                    screenY: pos.y,
                    clientX: pos.x,
                    clientY: pos.y
                });
            }
            // No MouseEvent support, try using initMouseEvent
            if (doc.createEvent) {
                var evt = doc.createEvent('MouseEvent');
                if (evt.initMouseEvent) {
                    evt.initMouseEvent(type, true, // Bubble
                    true, // Cancel
                    win, // View
                    type === 'click' ? 1 : 0, // Detail
                    // Coords
                    pos.x, pos.y, pos.x, pos.y, 
                    // Pressed keys
                    false, false, false, false, 0, // button
                    null // related target
                    );
                    return evt;
                }
            }
            return { type: type };
        }
        /**
         * Get an appropriate heading level for an element. Corresponds to the
         * heading level below the previous heading in the DOM.
         *
         * Note: Only detects previous headings in the DOM that are siblings,
         * ancestors, or previous siblings of ancestors. Headings that are nested below
         * siblings of ancestors (cousins et.al) are not picked up. This is because it
         * is ambiguous whether or not the nesting is for layout purposes or indicates a
         * separate section.
         *
         * @private
         * @param {Highcharts.HTMLDOMElement} [element]
         * @return {string} The heading tag name (h1, h2 etc).
         * If no nearest heading is found, "p" is returned.
         */
        function getHeadingTagNameForElement(element) {
            var getIncreasedHeadingLevel = function (tagName) {
                    var headingLevel = parseInt(tagName.slice(1), 10),
                newLevel = Math.min(6,
                headingLevel + 1);
                return 'h' + newLevel;
            };
            var isHeading = function (tagName) { return /H[1-6]/.test(tagName); };
            var getPreviousSiblingsHeading = function (el) {
                    var sibling = el;
                while (sibling = sibling.previousSibling) { // eslint-disable-line
                    var tagName = sibling.tagName || '';
                    if (isHeading(tagName)) {
                        return tagName;
                    }
                }
                return '';
            };
            var getHeadingRecursive = function (el) {
                    var prevSiblingsHeading = getPreviousSiblingsHeading(el);
                if (prevSiblingsHeading) {
                    return getIncreasedHeadingLevel(prevSiblingsHeading);
                }
                // No previous siblings are headings, try parent node
                var parent = el.parentElement;
                if (!parent) {
                    return 'p';
                }
                var parentTagName = parent.tagName;
                if (isHeading(parentTagName)) {
                    return getIncreasedHeadingLevel(parentTagName);
                }
                return getHeadingRecursive(parent);
            };
            return getHeadingRecursive(element);
        }
        /**
         * Remove an element from the DOM.
         * @private
         * @param {Highcharts.HTMLDOMElement|Highcharts.SVGDOMElement} [element]
         * @return {void}
         */
        function removeElement(element) {
            if (element && element.parentNode) {
                element.parentNode.removeChild(element);
            }
        }
        /**
         * Remove all child nodes from an element.
         * @private
         * @param {Highcharts.HTMLDOMElement|Highcharts.SVGDOMElement} [element]
         * @return {void}
         */
        function removeChildNodes(element) {
            while (element.lastChild) {
                element.removeChild(element.lastChild);
            }
        }
        /**
         * Utility function. Reverses child nodes of a DOM element.
         * @private
         */
        function reverseChildNodes(node) {
            var i = node.childNodes.length;
            while (i--) {
                node.appendChild(node.childNodes[i]);
            }
        }
        /**
         * Used for aria-label attributes, painting on a canvas will fail if the
         * text contains tags.
         * @private
         */
        function stripHTMLTagsFromString(str) {
            return typeof str === 'string' ?
                str.replace(/<\/?[^>]+(>|$)/g, '') : str;
        }
        /**
         * Utility function for hiding an element visually, but still keeping it
         * available to screen reader users.
         * @private
         */
        function visuallyHideElement(element) {
            css(element, {
                position: 'absolute',
                width: '1px',
                height: '1px',
                overflow: 'hidden',
                whiteSpace: 'nowrap',
                clip: 'rect(1px, 1px, 1px, 1px)',
                marginTop: '-3px',
                '-ms-filter': 'progid:DXImageTransform.Microsoft.Alpha(Opacity=1)',
                filter: 'alpha(opacity=1)',
                opacity: 0.01
            });
        }
        /* *
         *
         *  Default Export
         *
         * */
        var HTMLUtilities = {
                addClass: addClass,
                cloneMouseEvent: cloneMouseEvent,
                cloneTouchEvent: cloneTouchEvent,
                escapeStringForHTML: escapeStringForHTML,
                getElement: getElement,
                getFakeMouseEvent: getFakeMouseEvent,
                getHeadingTagNameForElement: getHeadingTagNameForElement,
                removeChildNodes: removeChildNodes,
                removeClass: removeClass,
                removeElement: removeElement,
                reverseChildNodes: reverseChildNodes,
                simulatedEventTarget: simulatedEventTarget,
                stripHTMLTagsFromString: stripHTMLTagsFromString,
                visuallyHideElement: visuallyHideElement
            };

        return HTMLUtilities;
    });
    _registerModule(_modules, 'Accessibility/A11yI18n.js', [_modules['Core/FormatUtilities.js'], _modules['Core/Utilities.js']], function (F, U) {
        /* *
         *
         *  Accessibility module - internationalization support
         *
         *  (c) 2010-2021 Highsoft AS
         *  Author: Øystein Moseng
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var format = F.format;
        var getNestedProperty = U.getNestedProperty,
            pick = U.pick;
        /* *
         *
         *  Composition
         *
         * */
        var A11yI18nComposition;
        (function (A11yI18nComposition) {
            /* *
             *
             *  Declarations
             *
             * */
            /* *
             *
             *  Constants
             *
             * */
            var composedClasses = [];
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * @private
             */
            function compose(ChartClass) {
                if (composedClasses.indexOf(ChartClass) === -1) {
                    composedClasses.push(ChartClass);
                    var chartProto = ChartClass.prototype;
                    chartProto.langFormat = langFormat;
                }
                return ChartClass;
            }
            A11yI18nComposition.compose = compose;
            /**
             * i18n utility function.  Format a single array or plural statement in a
             * format string.  If the statement is not an array or plural statement,
             * returns the statement within brackets.  Invalid array statements return
             * an empty string.
             *
             * @private
             * @function formatExtendedStatement
             * @param {string} statement
             * @param {Highcharts.Dictionary<*>} ctx
             * Context to apply to the format string.
             */
            function formatExtendedStatement(statement, ctx) {
                var eachStart = statement.indexOf('#each('), pluralStart = statement.indexOf('#plural('), indexStart = statement.indexOf('['), indexEnd = statement.indexOf(']');
                var arr,
                    result;
                // Dealing with an each-function?
                if (eachStart > -1) {
                    var eachEnd = statement.slice(eachStart).indexOf(')') + eachStart, preEach = statement.substring(0, eachStart), postEach = statement.substring(eachEnd + 1), eachStatement = statement.substring(eachStart + 6, eachEnd), eachArguments = eachStatement.split(',');
                    var lenArg = Number(eachArguments[1]),
                        len = void 0;
                    result = '';
                    arr = getNestedProperty(eachArguments[0], ctx);
                    if (arr) {
                        lenArg = isNaN(lenArg) ? arr.length : lenArg;
                        len = lenArg < 0 ?
                            arr.length + lenArg :
                            Math.min(lenArg, arr.length); // Overshoot
                        // Run through the array for the specified length
                        for (var i = 0; i < len; ++i) {
                            result += preEach + arr[i] + postEach;
                        }
                    }
                    return result.length ? result : '';
                }
                // Dealing with a plural-function?
                if (pluralStart > -1) {
                    var pluralEnd = (statement.slice(pluralStart).indexOf(')') + pluralStart), pluralStatement = statement.substring(pluralStart + 8, pluralEnd), pluralArguments = pluralStatement.split(','), num = Number(getNestedProperty(pluralArguments[0], ctx));
                    switch (num) {
                        case 0:
                            result = pick(pluralArguments[4], pluralArguments[1]);
                            break;
                        case 1:
                            result = pick(pluralArguments[2], pluralArguments[1]);
                            break;
                        case 2:
                            result = pick(pluralArguments[3], pluralArguments[1]);
                            break;
                        default:
                            result = pluralArguments[1];
                    }
                    return result ? stringTrim(result) : '';
                }
                // Array index
                if (indexStart > -1) {
                    var arrayName = statement.substring(0,
                        indexStart),
                        ix = Number(statement.substring(indexStart + 1,
                        indexEnd));
                    var val = void 0;
                    arr = getNestedProperty(arrayName, ctx);
                    if (!isNaN(ix) && arr) {
                        if (ix < 0) {
                            val = arr[arr.length + ix];
                            // Handle negative overshoot
                            if (typeof val === 'undefined') {
                                val = arr[0];
                            }
                        }
                        else {
                            val = arr[ix];
                            // Handle positive overshoot
                            if (typeof val === 'undefined') {
                                val = arr[arr.length - 1];
                            }
                        }
                    }
                    return typeof val !== 'undefined' ? val : '';
                }
                // Standard substitution, delegate to format or similar
                return '{' + statement + '}';
            }
            /* eslint-disable max-len */
            /**
             * i18n formatting function.  Extends Highcharts.format() functionality by
             * also handling arrays and plural conditionals.  Arrays can be indexed as
             * follows:
             *
             * - Format: 'This is the first index: {myArray[0]}. The last: {myArray[-1]}.'
             *
             * - Context: { myArray: [0, 1, 2, 3, 4, 5] }
             *
             * - Result: 'This is the first index: 0. The last: 5.'
             *
             *
             * They can also be iterated using the #each() function.  This will repeat
             * the contents of the bracket expression for each element.  Example:
             *
             * - Format: 'List contains: {#each(myArray)cm }'
             *
             * - Context: { myArray: [0, 1, 2] }
             *
             * - Result: 'List contains: 0cm 1cm 2cm '
             *
             *
             * The #each() function optionally takes a length parameter.  If positive,
             * this parameter specifies the max number of elements to iterate through.
             * If negative, the function will subtract the number from the length of the
             * array.  Use this to stop iterating before the array ends.  Example:
             *
             * - Format: 'List contains: {#each(myArray, -1) }and {myArray[-1]}.'
             *
             * - Context: { myArray: [0, 1, 2, 3] }
             *
             * - Result: 'List contains: 0, 1, 2, and 3.'
             *
             *
             * Use the #plural() function to pick a string depending on whether or not a
             * context object is 1.  Arguments are #plural(obj, plural, singular).
             * Example:
             *
             * - Format: 'Has {numPoints} {#plural(numPoints, points, point}.'
             *
             * - Context: { numPoints: 5 }
             *
             * - Result: 'Has 5 points.'
             *
             *
             * Optionally there are additional parameters for dual and none:
             * #plural(obj, plural, singular, dual, none).  Example:
             *
             * - Format: 'Has {#plural(numPoints, many points, one point, two points,
             *   none}.'
             *
             * - Context: { numPoints: 2 }
             *
             * - Result: 'Has two points.'
             *
             *
             * The dual or none parameters will take precedence if they are supplied.
             *
             * @requires modules/accessibility
             *
             * @function Highcharts.i18nFormat
             *
             * @param {string} formatString
             * The string to format.
             *
             * @param {Highcharts.Dictionary<*>} context
             * Context to apply to the format string.
             *
             * @param {Highcharts.Chart} chart
             * A `Chart` instance with a time object and numberFormatter, passed on to
             * format().
             *
             * @return {string}
             * The formatted string.
             */
            function i18nFormat(formatString, context, chart) {
                var getFirstBracketStatement = function (sourceStr, offset) {
                        var str = sourceStr.slice(offset || 0), startBracket = str.indexOf('{'), endBracket = str.indexOf('}');
                    if (startBracket > -1 && endBracket > startBracket) {
                        return {
                            statement: str.substring(startBracket + 1, endBracket),
                            begin: offset + startBracket + 1,
                            end: offset + endBracket
                        };
                    }
                }, tokens = [];
                var bracketRes,
                    constRes,
                    cursor = 0;
                // Tokenize format string into bracket statements and constants
                do {
                    bracketRes = getFirstBracketStatement(formatString, cursor);
                    constRes = formatString.substring(cursor, bracketRes && bracketRes.begin - 1);
                    // If we have constant content before this bracket statement, add it
                    if (constRes.length) {
                        tokens.push({
                            value: constRes,
                            type: 'constant'
                        });
                    }
                    // Add the bracket statement
                    if (bracketRes) {
                        tokens.push({
                            value: bracketRes.statement,
                            type: 'statement'
                        });
                    }
                    cursor = bracketRes ? bracketRes.end + 1 : cursor + 1;
                } while (bracketRes);
                // Perform the formatting.  The formatArrayStatement function returns
                // the statement in brackets if it is not an array statement, which
                // means it gets picked up by format below.
                tokens.forEach(function (token) {
                    if (token.type === 'statement') {
                        token.value = formatExtendedStatement(token.value, context);
                    }
                });
                // Join string back together and pass to format to pick up non-array
                // statements.
                return format(tokens.reduce(function (acc, cur) { return acc + cur.value; }, ''), context, chart);
            }
            A11yI18nComposition.i18nFormat = i18nFormat;
            /* eslint-enable max-len */
            /**
             * Apply context to a format string from lang options of the chart.
             *
             * @requires modules/accessibility
             *
             * @function Highcharts.Chart#langFormat
             *
             * @param {string} langKey
             * Key (using dot notation) into lang option structure.
             *
             * @param {Highcharts.Dictionary<*>} context
             * Context to apply to the format string.
             *
             * @return {string}
             * The formatted string.
             */
            function langFormat(langKey, context) {
                var keys = langKey.split('.');
                var formatString = this.options.lang,
                    i = 0;
                for (; i < keys.length; ++i) {
                    formatString = formatString && formatString[keys[i]];
                }
                return typeof formatString === 'string' ?
                    i18nFormat(formatString, context, this) : '';
            }
            /**
             * String trim that works for IE6-8 as well.
             *
             * @private
             * @function stringTrim
             *
             * @param {string} str
             * The input string
             *
             * @return {string}
             * The trimmed string
             */
            function stringTrim(str) {
                return str.trim && str.trim() || str.replace(/^\s+|\s+$/g, '');
            }
        })(A11yI18nComposition || (A11yI18nComposition = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return A11yI18nComposition;
    });
    _registerModule(_modules, 'Accessibility/Utils/ChartUtilities.js', [_modules['Core/Globals.js'], _modules['Accessibility/Utils/HTMLUtilities.js'], _modules['Core/Utilities.js']], function (H, HU, U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Utils for dealing with charts.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var doc = H.doc;
        var stripHTMLTags = HU.stripHTMLTagsFromString;
        var defined = U.defined,
            find = U.find,
            fireEvent = U.fireEvent;
        /* *
         *
         *  Functions
         *
         * */
        /* eslint-disable valid-jsdoc */
        /**
         * Fire an event on an element that is either wrapped by Highcharts,
         * or a DOM element.
         * @private
         */
        function fireEventOnWrappedOrUnwrappedElement(el, eventObject) {
            var type = eventObject.type;
            var hcEvents = el.hcEvents;
            if ((doc.createEvent) &&
                (el.dispatchEvent || el.fireEvent)) {
                if (el.dispatchEvent) {
                    el.dispatchEvent(eventObject);
                }
                else {
                    el.fireEvent(type, eventObject);
                }
            }
            else if (hcEvents && hcEvents[type]) {
                fireEvent(el, type, eventObject);
            }
            else if (el.element) {
                fireEventOnWrappedOrUnwrappedElement(el.element, eventObject);
            }
        }
        /**
         * @private
         */
        function getChartTitle(chart) {
            return stripHTMLTags(chart.options.title.text ||
                chart.langFormat('accessibility.defaultChartTitle', { chart: chart }));
        }
        /**
         * Return string with the axis name/title.
         * @private
         */
        function getAxisDescription(axis) {
            return axis && (axis.userOptions && axis.userOptions.accessibility &&
                axis.userOptions.accessibility.description ||
                axis.axisTitle && axis.axisTitle.textStr ||
                axis.options.id ||
                axis.categories && 'categories' ||
                axis.dateTime && 'Time' ||
                'values');
        }
        /**
         * Return string with text description of the axis range.
         * @private
         * @param {Highcharts.Axis} axis
         * The axis to get range desc of.
         * @return {string}
         * A string with the range description for the axis.
         */
        function getAxisRangeDescription(axis) {
            var axisOptions = axis.options || {};
            // Handle overridden range description
            if (axisOptions.accessibility &&
                typeof axisOptions.accessibility.rangeDescription !== 'undefined') {
                return axisOptions.accessibility.rangeDescription;
            }
            // Handle category axes
            if (axis.categories) {
                return getCategoryAxisRangeDesc(axis);
            }
            // Use time range, not from-to?
            if (axis.dateTime && (axis.min === 0 || axis.dataMin === 0)) {
                return getAxisTimeLengthDesc(axis);
            }
            // Just use from and to.
            // We have the range and the unit to use, find the desc format
            return getAxisFromToDescription(axis);
        }
        /**
         * Describe the range of a category axis.
         * @private
         */
        function getCategoryAxisRangeDesc(axis) {
            var chart = axis.chart;
            if (axis.dataMax && axis.dataMin) {
                return chart.langFormat('accessibility.axis.rangeCategories', {
                    chart: chart,
                    axis: axis,
                    numCategories: axis.dataMax - axis.dataMin + 1
                });
            }
            return '';
        }
        /**
         * Describe the length of the time window shown on an axis.
         * @private
         */
        function getAxisTimeLengthDesc(axis) {
            var chart = axis.chart,
                range = {},
                min = axis.dataMin || axis.min || 0,
                max = axis.dataMax || axis.max || 0;
            var rangeUnit = 'Seconds';
            range.Seconds = (max - min) / 1000;
            range.Minutes = range.Seconds / 60;
            range.Hours = range.Minutes / 60;
            range.Days = range.Hours / 24;
            ['Minutes', 'Hours', 'Days'].forEach(function (unit) {
                if (range[unit] > 2) {
                    rangeUnit = unit;
                }
            });
            var rangeValue = range[rangeUnit].toFixed(rangeUnit !== 'Seconds' &&
                    rangeUnit !== 'Minutes' ? 1 : 0 // Use decimals for days/hours
                );
            // We have the range and the unit to use, find the desc format
            return chart.langFormat('accessibility.axis.timeRange' + rangeUnit, {
                chart: chart,
                axis: axis,
                range: rangeValue.replace('.0', '')
            });
        }
        /**
         * Describe an axis from-to range.
         * @private
         */
        function getAxisFromToDescription(axis) {
            var chart = axis.chart,
                options = chart.options,
                dateRangeFormat = (options &&
                    options.accessibility &&
                    options.accessibility.screenReaderSection.axisRangeDateFormat ||
                    ''),
                extremes = {
                    min: axis.dataMin || axis.min || 0,
                    max: axis.dataMax || axis.max || 0
                },
                format = function (key) {
                    return axis.dateTime ?
                        chart.time.dateFormat(dateRangeFormat,
                extremes[key]) :
                        extremes[key].toString();
            };
            return chart.langFormat('accessibility.axis.rangeFromTo', {
                chart: chart,
                axis: axis,
                rangeFrom: format('min'),
                rangeTo: format('max')
            });
        }
        /**
         * Get the DOM element for the first point in the series.
         * @private
         * @param {Highcharts.Series} series
         * The series to get element for.
         * @return {Highcharts.HTMLDOMElement|Highcharts.SVGDOMElement|undefined}
         * The DOM element for the point.
         */
        function getSeriesFirstPointElement(series) {
            if (series.points && series.points.length) {
                var firstPointWithGraphic = find(series.points,
                    function (p) { return !!p.graphic; });
                return (firstPointWithGraphic &&
                    firstPointWithGraphic.graphic &&
                    firstPointWithGraphic.graphic.element);
            }
        }
        /**
         * Get the DOM element for the series that we put accessibility info on.
         * @private
         * @param {Highcharts.Series} series
         * The series to get element for.
         * @return {Highcharts.HTMLDOMElement|Highcharts.SVGDOMElement|undefined}
         * The DOM element for the series
         */
        function getSeriesA11yElement(series) {
            var firstPointEl = getSeriesFirstPointElement(series);
            return (firstPointEl &&
                firstPointEl.parentNode || series.graph &&
                series.graph.element || series.group &&
                series.group.element); // Could be tracker series depending on series type
        }
        /**
         * Remove aria-hidden from element. Also unhides parents of the element, and
         * hides siblings that are not explicitly unhidden.
         * @private
         */
        function unhideChartElementFromAT(chart, element) {
            element.setAttribute('aria-hidden', false);
            if (element === chart.renderTo ||
                !element.parentNode ||
                element.parentNode === doc.body // #16126: Full screen printing
            ) {
                return;
            }
            // Hide siblings unless their hidden state is already explicitly set
            Array.prototype.forEach.call(element.parentNode.childNodes, function (node) {
                if (!node.hasAttribute('aria-hidden')) {
                    node.setAttribute('aria-hidden', true);
                }
            });
            // Repeat for parent
            unhideChartElementFromAT(chart, element.parentNode);
        }
        /**
         * Hide series from screen readers.
         * @private
         */
        function hideSeriesFromAT(series) {
            var seriesEl = getSeriesA11yElement(series);
            if (seriesEl) {
                seriesEl.setAttribute('aria-hidden', true);
            }
        }
        /**
         * Get series objects by series name.
         * @private
         */
        function getSeriesFromName(chart, name) {
            if (!name) {
                return chart.series;
            }
            return (chart.series || []).filter(function (s) {
                return s.name === name;
            });
        }
        /**
         * Get point in a series from x/y values.
         * @private
         */
        function getPointFromXY(series, x, y) {
            var i = series.length,
                res;
            while (i--) {
                res = find(series[i].points || [], function (p) {
                    return p.x === x && p.y === y;
                });
                if (res) {
                    return res;
                }
            }
        }
        /**
         * Get relative position of point on an x/y axis from 0 to 1.
         * @private
         */
        function getRelativePointAxisPosition(axis, point) {
            if (!defined(axis.dataMin) || !defined(axis.dataMax)) {
                return 0;
            }
            var axisStart = axis.toPixels(axis.dataMin),
                axisEnd = axis.toPixels(axis.dataMax), 
                // We have to use pixel position because of axis breaks, log axis etc.
                positionProp = axis.coll === 'xAxis' ? 'x' : 'y',
                pointPos = axis.toPixels(point[positionProp] || 0);
            return (pointPos - axisStart) / (axisEnd - axisStart);
        }
        /**
         * Get relative position of point on an x/y axis from 0 to 1.
         * @private
         */
        function scrollToPoint(point) {
            var xAxis = point.series.xAxis,
                yAxis = point.series.yAxis,
                axis = (xAxis && xAxis.scrollbar ? xAxis : yAxis),
                scrollbar = (axis && axis.scrollbar);
            if (scrollbar && defined(scrollbar.to) && defined(scrollbar.from)) {
                var range = scrollbar.to - scrollbar.from;
                var pos = getRelativePointAxisPosition(axis,
                    point);
                scrollbar.updatePosition(pos - range / 2, pos + range / 2);
                fireEvent(scrollbar, 'changed', {
                    from: scrollbar.from,
                    to: scrollbar.to,
                    trigger: 'scrollbar',
                    DOMEvent: null
                });
            }
        }
        /* *
         *
         *  Default Export
         *
         * */
        var ChartUtilities = {
                fireEventOnWrappedOrUnwrappedElement: fireEventOnWrappedOrUnwrappedElement,
                getChartTitle: getChartTitle,
                getAxisDescription: getAxisDescription,
                getAxisRangeDescription: getAxisRangeDescription,
                getPointFromXY: getPointFromXY,
                getSeriesFirstPointElement: getSeriesFirstPointElement,
                getSeriesFromName: getSeriesFromName,
                getSeriesA11yElement: getSeriesA11yElement,
                unhideChartElementFromAT: unhideChartElementFromAT,
                hideSeriesFromAT: hideSeriesFromAT,
                scrollToPoint: scrollToPoint
            };

        return ChartUtilities;
    });
    _registerModule(_modules, 'Accessibility/Utils/DOMElementProvider.js', [_modules['Core/Globals.js'], _modules['Accessibility/Utils/HTMLUtilities.js']], function (H, HU) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Class that can keep track of elements added to DOM and clean them up on
         *  destroy.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var doc = H.doc;
        var removeElement = HU.removeElement;
        /* *
         *
         *  Class
         *
         * */
        /**
         * @private
         */
        var DOMElementProvider = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function DOMElementProvider() {
                    this.elements = [];
            }
            /**
             * Create an element and keep track of it for later removal.
             * Same args as document.createElement
             * @private
             */
            DOMElementProvider.prototype.createElement = function () {
                var el = doc.createElement.apply(doc,
                    arguments);
                this.elements.push(el);
                return el;
            };
            /**
             * Destroy all created elements, removing them from the DOM.
             * @private
             */
            DOMElementProvider.prototype.destroyCreatedElements = function () {
                this.elements.forEach(function (element) {
                    removeElement(element);
                });
                this.elements = [];
            };
            return DOMElementProvider;
        }());
        /* *
         *
         *  Default Export
         *
         * */

        return DOMElementProvider;
    });
    _registerModule(_modules, 'Accessibility/Utils/EventProvider.js', [_modules['Core/Globals.js'], _modules['Core/Utilities.js']], function (H, U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Class that can keep track of events added, and clean them up on destroy.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var addEvent = U.addEvent;
        /* *
         *
         *  Class
         *
         * */
        /**
         * @private
         */
        var EventProvider = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function EventProvider() {
                    this.eventRemovers = [];
            }
            /**
             * Add an event to an element and keep track of it for later removal.
             * Same args as Highcharts.addEvent.
             * @private
             */
            EventProvider.prototype.addEvent = function () {
                var remover = addEvent.apply(H,
                    arguments);
                this.eventRemovers.push(remover);
                return remover;
            };
            /**
             * Remove all added events.
             * @private
             */
            EventProvider.prototype.removeAddedEvents = function () {
                this.eventRemovers.forEach(function (remover) { return remover(); });
                this.eventRemovers = [];
            };
            return EventProvider;
        }());
        /* *
         *
         *  Default Export
         *
         * */

        return EventProvider;
    });
    _registerModule(_modules, 'Accessibility/AccessibilityComponent.js', [_modules['Accessibility/Utils/ChartUtilities.js'], _modules['Accessibility/Utils/DOMElementProvider.js'], _modules['Accessibility/Utils/EventProvider.js'], _modules['Accessibility/Utils/HTMLUtilities.js'], _modules['Core/Utilities.js']], function (CU, DOMElementProvider, EventProvider, HU, U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Accessibility component class definition
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var fireEventOnWrappedOrUnwrappedElement = CU.fireEventOnWrappedOrUnwrappedElement;
        var getFakeMouseEvent = HU.getFakeMouseEvent;
        var extend = U.extend;
        /* *
         *
         *  Class
         *
         * */
        /**
         * The AccessibilityComponent base class, representing a part of the chart that
         * has accessibility logic connected to it. This class can be inherited from to
         * create a custom accessibility component for a chart.
         *
         * Components should take care to destroy added elements and unregister event
         * handlers on destroy. This is handled automatically if using this.addEvent and
         * this.createElement.
         *
         * @sample highcharts/accessibility/custom-component
         *         Custom accessibility component
         *
         * @requires module:modules/accessibility
         * @class
         * @name Highcharts.AccessibilityComponent
         */
        var AccessibilityComponent = /** @class */ (function () {
                function AccessibilityComponent() {
                    /* *
                     *
                     *  Properties
                     *
                     * */
                    this.chart = void 0;
                this.domElementProvider = void 0;
                this.eventProvider = void 0;
                this.keyCodes = void 0;
                this.proxyProvider = void 0;
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Initialize the class
             * @private
             * @param {Highcharts.Chart} chart The chart object
             * @param {Highcharts.ProxyProvider} proxyProvider The proxy provider of the accessibility module
             */
            AccessibilityComponent.prototype.initBase = function (chart, proxyProvider) {
                this.chart = chart;
                this.eventProvider = new EventProvider();
                this.domElementProvider = new DOMElementProvider();
                this.proxyProvider = proxyProvider;
                // Key code enum for common keys
                this.keyCodes = {
                    left: 37,
                    right: 39,
                    up: 38,
                    down: 40,
                    enter: 13,
                    space: 32,
                    esc: 27,
                    tab: 9,
                    pageUp: 33,
                    pageDown: 34,
                    end: 35,
                    home: 36
                };
            };
            /**
             * Add an event to an element and keep track of it for later removal.
             * See EventProvider for details.
             * @private
             */
            AccessibilityComponent.prototype.addEvent = function (el, type, fn, options) {
                return this.eventProvider.addEvent(el, type, fn, options);
            };
            /**
             * Create an element and keep track of it for later removal.
             * See DOMElementProvider for details.
             * @private
             */
            AccessibilityComponent.prototype.createElement = function (tagName, options) {
                return this.domElementProvider.createElement(tagName, options);
            };
            /**
             * Fire a fake click event on an element. It is useful to have this on
             * AccessibilityComponent for users of custom components.
             */
            AccessibilityComponent.prototype.fakeClickEvent = function (el) {
                var fakeEvent = getFakeMouseEvent('click');
                fireEventOnWrappedOrUnwrappedElement(el, fakeEvent);
            };
            /**
             * Remove traces of the component.
             * @private
             */
            AccessibilityComponent.prototype.destroyBase = function () {
                this.domElementProvider.destroyCreatedElements();
                this.eventProvider.removeAddedEvents();
            };
            return AccessibilityComponent;
        }());
        extend(AccessibilityComponent.prototype, 
        /** @lends Highcharts.AccessibilityComponent */
        {
            /**
             * Called on component initialization.
             */
            init: function () { },
            /**
             * Get keyboard navigation handler for this component.
             * @private
             */
            getKeyboardNavigation: function () { },
            /**
             * Called on updates to the chart, including options changes.
             * Note that this is also called on first render of chart.
             */
            onChartUpdate: function () { },
            /**
             * Called on every chart render.
             */
            onChartRender: function () { },
            /**
             * Called when accessibility is disabled or chart is destroyed.
             */
            destroy: function () { }
        });
        /* *
         *
         *  Default Export
         *
         * */

        return AccessibilityComponent;
    });
    _registerModule(_modules, 'Accessibility/KeyboardNavigationHandler.js', [_modules['Core/Utilities.js']], function (U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Keyboard navigation handler base class definition
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var find = U.find;
        /* *
         *
         *  Class
         *
         * */
        /**
         * Define a keyboard navigation handler for use with a
         * Highcharts.AccessibilityComponent instance. This functions as an abstraction
         * layer for keyboard navigation, and defines a map of keyCodes to handler
         * functions.
         *
         * @requires module:modules/accessibility
         *
         * @sample highcharts/accessibility/custom-component
         *         Custom accessibility component
         *
         * @class
         * @name Highcharts.KeyboardNavigationHandler
         *
         * @param {Highcharts.Chart} chart
         * The chart this module should act on.
         *
         * @param {Highcharts.KeyboardNavigationHandlerOptionsObject} options
         * Options for the keyboard navigation handler.
         */
        var KeyboardNavigationHandler = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function KeyboardNavigationHandler(chart, options) {
                    this.chart = chart;
                this.keyCodeMap = options.keyCodeMap || [];
                this.validate = options.validate;
                this.init = options.init;
                this.terminate = options.terminate;
                // Response enum
                this.response = {
                    success: 1,
                    prev: 2,
                    next: 3,
                    noHandler: 4,
                    fail: 5 // Handler failed
                };
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Find handler function(s) for key code in the keyCodeMap and run it.
             *
             * @function KeyboardNavigationHandler#run
             * @param {global.KeyboardEvent} e
             * @return {number} Returns a response code indicating whether the run was
             *      a success/fail/unhandled, or if we should move to next/prev module.
             */
            KeyboardNavigationHandler.prototype.run = function (e) {
                var keyCode = e.which || e.keyCode;
                var response = this.response.noHandler;
                var handlerCodeSet = find(this.keyCodeMap,
                    function (codeSet) {
                        return codeSet[0].indexOf(keyCode) > -1;
                });
                if (handlerCodeSet) {
                    response = handlerCodeSet[1].call(this, keyCode, e);
                }
                else if (keyCode === 9) {
                    // Default tab handler, move to next/prev module
                    response = this.response[e.shiftKey ? 'prev' : 'next'];
                }
                return response;
            };
            return KeyboardNavigationHandler;
        }());
        /* *
         *
         *  Default Export
         *
         * */
        /* *
         *
         *  API Declarations
         *
         * */
        /**
         * Options for the keyboard navigation handler.
         *
         * @interface Highcharts.KeyboardNavigationHandlerOptionsObject
         */ /**
        * An array containing pairs of an array of keycodes, mapped to a handler
        * function. When the keycode is received, the handler is called with the
        * keycode as parameter.
        * @name Highcharts.KeyboardNavigationHandlerOptionsObject#keyCodeMap
        * @type {Array<Array<Array<number>, Function>>}
        */ /**
        * Function to run on initialization of module.
        * @name Highcharts.KeyboardNavigationHandlerOptionsObject#init
        * @type {Function}
        */ /**
        * Function to run before moving to next/prev module. Receives moving direction
        * as parameter: +1 for next, -1 for previous.
        * @name Highcharts.KeyboardNavigationHandlerOptionsObject#terminate
        * @type {Function|undefined}
        */ /**
        * Function to run to validate module. Should return false if module should not
        * run, true otherwise. Receives chart as parameter.
        * @name Highcharts.KeyboardNavigationHandlerOptionsObject#validate
        * @type {Function|undefined}
        */
        (''); // keeps doclets above in JS file

        return KeyboardNavigationHandler;
    });
    _registerModule(_modules, 'Accessibility/Components/ContainerComponent.js', [_modules['Accessibility/AccessibilityComponent.js'], _modules['Accessibility/KeyboardNavigationHandler.js'], _modules['Accessibility/Utils/ChartUtilities.js'], _modules['Core/Globals.js'], _modules['Accessibility/Utils/HTMLUtilities.js']], function (AccessibilityComponent, KeyboardNavigationHandler, CU, H, HU) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Accessibility component for chart container.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var __extends = (this && this.__extends) || (function () {
                var extendStatics = function (d,
            b) {
                    extendStatics = Object.setPrototypeOf ||
                        ({ __proto__: [] } instanceof Array && function (d,
            b) { d.__proto__ = b; }) ||
                        function (d,
            b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
                return extendStatics(d, b);
            };
            return function (d, b) {
                extendStatics(d, b);
                function __() { this.constructor = d; }
                d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
            };
        })();
        var unhideChartElementFromAT = CU.unhideChartElementFromAT,
            getChartTitle = CU.getChartTitle;
        var doc = H.doc;
        var stripHTMLTags = HU.stripHTMLTagsFromString;
        /**
         * The ContainerComponent class
         *
         * @private
         * @class
         * @name Highcharts.ContainerComponent
         */
        var ContainerComponent = /** @class */ (function (_super) {
                __extends(ContainerComponent, _super);
            function ContainerComponent() {
                return _super !== null && _super.apply(this, arguments) || this;
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Called on first render/updates to the chart, including options changes.
             */
            ContainerComponent.prototype.onChartUpdate = function () {
                this.handleSVGTitleElement();
                this.setSVGContainerLabel();
                this.setGraphicContainerAttrs();
                this.setRenderToAttrs();
                this.makeCreditsAccessible();
            };
            /**
             * @private
             */
            ContainerComponent.prototype.handleSVGTitleElement = function () {
                var chart = this.chart, titleId = 'highcharts-title-' + chart.index, titleContents = stripHTMLTags(chart.langFormat('accessibility.svgContainerTitle', {
                        chartTitle: getChartTitle(chart)
                    }));
                if (titleContents.length) {
                    var titleElement = this.svgTitleElement =
                            this.svgTitleElement || doc.createElementNS('http://www.w3.org/2000/svg', 'title');
                    titleElement.textContent = titleContents;
                    titleElement.id = titleId;
                    chart.renderTo.insertBefore(titleElement, chart.renderTo.firstChild);
                }
            };
            /**
             * @private
             */
            ContainerComponent.prototype.setSVGContainerLabel = function () {
                var chart = this.chart,
                    svgContainerLabel = chart.langFormat('accessibility.svgContainerLabel', {
                        chartTitle: getChartTitle(chart)
                    });
                if (chart.renderer.box && svgContainerLabel.length) {
                    chart.renderer.box.setAttribute('aria-label', svgContainerLabel);
                }
            };
            /**
             * @private
             */
            ContainerComponent.prototype.setGraphicContainerAttrs = function () {
                var chart = this.chart,
                    label = chart.langFormat('accessibility.graphicContainerLabel', {
                        chartTitle: getChartTitle(chart)
                    });
                if (label.length) {
                    chart.container.setAttribute('aria-label', label);
                }
            };
            /**
             * Set attributes on the chart container element.
             * @private
             */
            ContainerComponent.prototype.setRenderToAttrs = function () {
                var chart = this.chart, shouldHaveLandmark = chart.options.accessibility
                        .landmarkVerbosity !== 'disabled', containerLabel = chart.langFormat('accessibility.chartContainerLabel', {
                        title: getChartTitle(chart),
                        chart: chart
                    });
                if (containerLabel) {
                    chart.renderTo.setAttribute('role', shouldHaveLandmark ? 'region' : 'group');
                    chart.renderTo.setAttribute('aria-label', containerLabel);
                }
            };
            /**
             * @private
             */
            ContainerComponent.prototype.makeCreditsAccessible = function () {
                var chart = this.chart,
                    credits = chart.credits;
                if (credits) {
                    if (credits.textStr) {
                        credits.element.setAttribute('aria-label', chart.langFormat('accessibility.credits', { creditsStr: stripHTMLTags(credits.textStr) }));
                    }
                    unhideChartElementFromAT(chart, credits.element);
                }
            };
            /**
             * Empty handler to just set focus on chart
             * @private
             */
            ContainerComponent.prototype.getKeyboardNavigation = function () {
                var chart = this.chart;
                return new KeyboardNavigationHandler(chart, {
                    keyCodeMap: [],
                    validate: function () {
                        return true;
                    },
                    init: function () {
                        var a11y = chart.accessibility;
                        if (a11y) {
                            a11y.keyboardNavigation.tabindexContainer.focus();
                        }
                    }
                });
            };
            /**
             * Accessibility disabled/chart destroyed.
             */
            ContainerComponent.prototype.destroy = function () {
                this.chart.renderTo.setAttribute('aria-hidden', true);
            };
            return ContainerComponent;
        }(AccessibilityComponent));
        /* *
         *
         *  Default Export
         *
         * */

        return ContainerComponent;
    });
    _registerModule(_modules, 'Accessibility/FocusBorder.js', [_modules['Core/Renderer/SVG/SVGLabel.js'], _modules['Core/Utilities.js']], function (SVGLabel, U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Extend SVG and Chart classes with focus border capabilities.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var addEvent = U.addEvent,
            pick = U.pick;
        /* *
         *
         *  Composition
         *
         * */
        var FocusBorderComposition;
        (function (FocusBorderComposition) {
            /* *
             *
             *  Declarations
             *
             * */
            /* *
             *
             *  Constants
             *
             * */
            var composedClasses = [];
            // Attributes that trigger a focus border update
            var svgElementBorderUpdateTriggers = [
                    'x', 'y', 'transform', 'width', 'height', 'r', 'd', 'stroke-width'
                ];
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * @private
             */
            function compose(ChartClass, SVGElementClass) {
                if (composedClasses.indexOf(ChartClass) === -1) {
                    composedClasses.push(ChartClass);
                    var chartProto = ChartClass.prototype;
                    chartProto.renderFocusBorder = chartRenderFocusBorder;
                    chartProto.setFocusToElement = chartSetFocusToElement;
                }
                if (composedClasses.indexOf(SVGElementClass) === -1) {
                    composedClasses.push(SVGElementClass);
                    var svgElementProto = SVGElementClass.prototype;
                    svgElementProto.addFocusBorder = svgElementAddFocusBorder;
                    svgElementProto.removeFocusBorder = svgElementRemoveFocusBorder;
                }
            }
            FocusBorderComposition.compose = compose;
            /**
             * Redraws the focus border on the currently focused element.
             *
             * @private
             * @function Highcharts.Chart#renderFocusBorder
             */
            function chartRenderFocusBorder() {
                var focusElement = this.focusElement,
                    focusBorderOptions = this.options.accessibility.keyboardNavigation.focusBorder;
                if (focusElement) {
                    focusElement.removeFocusBorder();
                    if (focusBorderOptions.enabled) {
                        focusElement.addFocusBorder(focusBorderOptions.margin, {
                            stroke: focusBorderOptions.style.color,
                            strokeWidth: focusBorderOptions.style.lineWidth,
                            r: focusBorderOptions.style.borderRadius
                        });
                    }
                }
            }
            /**
             * Set chart's focus to an SVGElement. Calls focus() on it, and draws the
             * focus border. This is used by multiple components.
             *
             * @private
             * @function Highcharts.Chart#setFocusToElement
             *
             * @param {Highcharts.SVGElement} svgElement
             * Element to draw the border around.
             *
             * @param {SVGDOMElement|HTMLDOMElement} [focusElement]
             * If supplied, it draws the border around svgElement and sets the focus to
             * focusElement.
             */
            function chartSetFocusToElement(svgElement, focusElement) {
                var focusBorderOptions = this.options.accessibility.keyboardNavigation.focusBorder,
                    browserFocusElement = focusElement || svgElement.element;
                // Set browser focus if possible
                if (browserFocusElement &&
                    browserFocusElement.focus) {
                    // If there is no focusin-listener, add one to work around Edge
                    // where Narrator is not reading out points despite calling focus().
                    if (!(browserFocusElement.hcEvents &&
                        browserFocusElement.hcEvents.focusin)) {
                        addEvent(browserFocusElement, 'focusin', function () { });
                    }
                    browserFocusElement.focus();
                    // Hide default focus ring
                    if (focusBorderOptions.hideBrowserFocusOutline) {
                        browserFocusElement.style.outline = 'none';
                    }
                }
                if (this.focusElement) {
                    this.focusElement.removeFocusBorder();
                }
                this.focusElement = svgElement;
                this.renderFocusBorder();
            }
            /**
             * Add hook to destroy focus border if SVG element is destroyed, unless
             * hook already exists.
             * @private
             * @param el Element to add destroy hook to
             */
            function svgElementAddDestroyFocusBorderHook(el) {
                if (el.focusBorderDestroyHook) {
                    return;
                }
                var origDestroy = el.destroy;
                el.destroy = function () {
                    if (el.focusBorder && el.focusBorder.destroy) {
                        el.focusBorder.destroy();
                    }
                    return origDestroy.apply(el, arguments);
                };
                el.focusBorderDestroyHook = origDestroy;
            }
            /**
             * Add focus border functionality to SVGElements. Draws a new rect on top of
             * element around its bounding box. This is used by multiple components.
             *
             * @private
             * @function Highcharts.SVGElement#addFocusBorder
             *
             * @param {number} margin
             *
             * @param {SVGAttributes} attribs
             */
            function svgElementAddFocusBorder(margin, attribs) {
                // Allow updating by just adding new border
                if (this.focusBorder) {
                    this.removeFocusBorder();
                }
                // Add the border rect
                var bb = this.getBBox(),
                    pad = pick(margin, 3),
                    parent = this.parentGroup,
                    scaleX = this.scaleX || parent && parent.scaleX,
                    scaleY = this.scaleY || parent && parent.scaleY,
                    oneDefined = scaleX ? !scaleY : scaleY,
                    scaleBoth = oneDefined ? Math.abs(scaleX || scaleY || 1) :
                        (Math.abs(scaleX || 1) + Math.abs(scaleY || 1)) / 2;
                bb.x += this.translateX ? this.translateX : 0;
                bb.y += this.translateY ? this.translateY : 0;
                var borderPosX = bb.x - pad,
                    borderPosY = bb.y - pad,
                    borderWidth = bb.width + 2 * pad,
                    borderHeight = bb.height + 2 * pad;
                /**
                 * For text elements, apply x and y offset, #11397.
                 * @private
                 */
                function getTextAnchorCorrection(text) {
                    var posXCorrection = 0,
                        posYCorrection = 0;
                    if (text.attr('text-anchor') === 'middle') {
                        posXCorrection = posYCorrection = 0.5;
                    }
                    else if (!text.rotation) {
                        posYCorrection = 0.75;
                    }
                    else {
                        posXCorrection = 0.25;
                    }
                    return {
                        x: posXCorrection,
                        y: posYCorrection
                    };
                }
                var isLabel = this instanceof SVGLabel;
                if (this.element.nodeName === 'text' || isLabel) {
                    var isRotated = !!this.rotation;
                    var correction = !isLabel ? getTextAnchorCorrection(this) :
                            {
                                x: isRotated ? 1 : 0,
                                y: 0
                            };
                    var attrX = +this.attr('x');
                    var attrY = +this.attr('y');
                    if (!isNaN(attrX)) {
                        borderPosX = attrX - (bb.width * correction.x) - pad;
                    }
                    if (!isNaN(attrY)) {
                        borderPosY = attrY - (bb.height * correction.y) - pad;
                    }
                    if (isLabel && isRotated) {
                        var temp = borderWidth;
                        borderWidth = borderHeight;
                        borderHeight = temp;
                        if (!isNaN(attrX)) {
                            borderPosX = attrX - (bb.height * correction.x) - pad;
                        }
                        if (!isNaN(attrY)) {
                            borderPosY = attrY - (bb.width * correction.y) - pad;
                        }
                    }
                }
                this.focusBorder = this.renderer.rect(borderPosX, borderPosY, borderWidth, borderHeight, parseInt((attribs && attribs.r || 0).toString(), 10) / scaleBoth)
                    .addClass('highcharts-focus-border')
                    .attr({
                    zIndex: 99
                })
                    .add(parent);
                if (!this.renderer.styledMode) {
                    this.focusBorder.attr({
                        stroke: attribs && attribs.stroke,
                        'stroke-width': (attribs && attribs.strokeWidth || 0) / scaleBoth
                    });
                }
                avgElementAddUpdateFocusBorderHooks(this, margin, attribs);
                svgElementAddDestroyFocusBorderHook(this);
            }
            /**
             * Add hooks to update the focus border of an element when the element
             * size/position is updated, unless already added.
             * @private
             * @param el Element to add update hooks to
             * @param updateParams Parameters to pass through to addFocusBorder when updating.
             */
            function avgElementAddUpdateFocusBorderHooks(el) {
                var updateParams = [];
                for (var _i = 1; _i < arguments.length; _i++) {
                    updateParams[_i - 1] = arguments[_i];
                }
                if (el.focusBorderUpdateHooks) {
                    return;
                }
                el.focusBorderUpdateHooks = {};
                svgElementBorderUpdateTriggers.forEach(function (trigger) {
                    var setterKey = trigger + 'Setter';
                    var origSetter = el[setterKey] || el._defaultSetter;
                    el.focusBorderUpdateHooks[setterKey] = origSetter;
                    el[setterKey] = function () {
                        var ret = origSetter.apply(el,
                            arguments);
                        el.addFocusBorder.apply(el, updateParams);
                        return ret;
                    };
                });
            }
            /**
             * Remove hook from SVG element added by addDestroyFocusBorderHook, if
             * existing.
             * @private
             * @param el Element to remove destroy hook from
             */
            function svgElementRemoveDestroyFocusBorderHook(el) {
                if (!el.focusBorderDestroyHook) {
                    return;
                }
                el.destroy = el.focusBorderDestroyHook;
                delete el.focusBorderDestroyHook;
            }
            /**
             * Add focus border functionality to SVGElements. Draws a new rect on top of
             * element around its bounding box. This is used by multiple components.
             * @private
             * @function Highcharts.SVGElement#removeFocusBorder
             */
            function svgElementRemoveFocusBorder() {
                svgElementRemoveUpdateFocusBorderHooks(this);
                svgElementRemoveDestroyFocusBorderHook(this);
                if (this.focusBorder) {
                    this.focusBorder.destroy();
                    delete this.focusBorder;
                }
            }
            /**
             * Remove hooks from SVG element added by addUpdateFocusBorderHooks, if
             * existing.
             * @private
             * @param el Element to remove update hooks from
             */
            function svgElementRemoveUpdateFocusBorderHooks(el) {
                if (!el.focusBorderUpdateHooks) {
                    return;
                }
                Object.keys(el.focusBorderUpdateHooks).forEach(function (setterKey) {
                    var origSetter = el.focusBorderUpdateHooks[setterKey];
                    if (origSetter === el._defaultSetter) {
                        delete el[setterKey];
                    }
                    else {
                        el[setterKey] = origSetter;
                    }
                });
                delete el.focusBorderUpdateHooks;
            }
        })(FocusBorderComposition || (FocusBorderComposition = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return FocusBorderComposition;
    });
    _registerModule(_modules, 'Accessibility/Utils/Announcer.js', [_modules['Core/Renderer/HTML/AST.js'], _modules['Accessibility/Utils/DOMElementProvider.js'], _modules['Core/Globals.js'], _modules['Accessibility/Utils/HTMLUtilities.js'], _modules['Core/Utilities.js']], function (AST, DOMElementProvider, H, HU, U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Create announcer to speak messages to screen readers and other AT.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var doc = H.doc;
        var addClass = HU.addClass,
            visuallyHideElement = HU.visuallyHideElement;
        var attr = U.attr;
        /* *
         *
         *  Class
         *
         * */
        var Announcer = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function Announcer(chart, type) {
                    this.chart = chart;
                this.domElementProvider = new DOMElementProvider();
                this.announceRegion = this.addAnnounceRegion(type);
            }
            /* *
             *
             *  Functions
             *
             * */
            Announcer.prototype.destroy = function () {
                this.domElementProvider.destroyCreatedElements();
            };
            Announcer.prototype.announce = function (message) {
                var _this = this;
                AST.setElementHTML(this.announceRegion, message);
                // Delete contents after a little while to avoid user finding the live
                // region in the DOM.
                if (this.clearAnnouncementRegionTimer) {
                    clearTimeout(this.clearAnnouncementRegionTimer);
                }
                this.clearAnnouncementRegionTimer = setTimeout(function () {
                    _this.announceRegion.innerHTML = AST.emptyHTML;
                    delete _this.clearAnnouncementRegionTimer;
                }, 1000);
            };
            Announcer.prototype.addAnnounceRegion = function (type) {
                var chartContainer = (this.chart.announcerContainer || this.createAnnouncerContainer()),
                    div = this.domElementProvider.createElement('div');
                attr(div, {
                    'aria-hidden': false,
                    'aria-live': type
                });
                if (this.chart.styledMode) {
                    addClass(div, 'highcharts-visually-hidden');
                }
                else {
                    visuallyHideElement(div);
                }
                chartContainer.appendChild(div);
                return div;
            };
            Announcer.prototype.createAnnouncerContainer = function () {
                var chart = this.chart,
                    container = doc.createElement('div');
                attr(container, {
                    'aria-hidden': false,
                    'class': 'highcharts-announcer-container'
                });
                container.style.position = 'relative';
                chart.renderTo.insertBefore(container, chart.renderTo.firstChild);
                chart.announcerContainer = container;
                return container;
            };
            return Announcer;
        }());
        /* *
         *
         *  Default Export
         *
         * */

        return Announcer;
    });
    _registerModule(_modules, 'Accessibility/Components/AnnotationsA11y.js', [_modules['Accessibility/Utils/HTMLUtilities.js']], function (HTMLUtilities) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Annotations accessibility code.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var escapeStringForHTML = HTMLUtilities.escapeStringForHTML,
            stripHTMLTagsFromString = HTMLUtilities.stripHTMLTagsFromString;
        /* *
         *
         *  Functions
         *
         * */
        /**
         * Get list of all annotation labels in the chart.
         *
         * @private
         * @param {Highcharts.Chart} chart The chart to get annotation info on.
         * @return {Array<object>} The labels, or empty array if none.
         */
        function getChartAnnotationLabels(chart) {
            var annotations = chart.annotations || [];
            return annotations.reduce(function (acc, cur) {
                if (cur.options &&
                    cur.options.visible !== false) {
                    acc = acc.concat(cur.labels);
                }
                return acc;
            }, []);
        }
        /**
         * Get the text of an annotation label.
         *
         * @private
         * @param {Object} label The annotation label object
         * @return {string} The text in the label.
         */
        function getLabelText(label) {
            return ((label.options &&
                label.options.accessibility &&
                label.options.accessibility.description) ||
                (label.graphic &&
                    label.graphic.text &&
                    label.graphic.text.textStr) ||
                '');
        }
        /**
         * Describe an annotation label.
         *
         * @private
         * @param {Object} label The annotation label object to describe
         * @return {string} The description for the label.
         */
        function getAnnotationLabelDescription(label) {
            var a11yDesc = (label.options &&
                    label.options.accessibility &&
                    label.options.accessibility.description);
            if (a11yDesc) {
                return a11yDesc;
            }
            var chart = label.chart;
            var labelText = getLabelText(label);
            var points = label.points;
            var getAriaLabel = function (point) { return (point.graphic &&
                    point.graphic.element &&
                    point.graphic.element.getAttribute('aria-label') ||
                    ''); };
            var getValueDesc = function (point) {
                    var valDesc = (point.accessibility &&
                        point.accessibility.valueDescription ||
                        getAriaLabel(point));
                var seriesName = (point &&
                        point.series.name ||
                        '');
                return (seriesName ? seriesName + ', ' : '') + 'data point ' + valDesc;
            };
            var pointValueDescriptions = points
                    .filter(function (p) { return !!p.graphic; }) // Filter out mock points
                    .map(getValueDesc)
                    // Filter out points we can't describe
                    .filter(function (desc) { return !!desc; });
            var numPoints = pointValueDescriptions.length;
            var pointsSelector = numPoints > 1 ?
                    'MultiplePoints' : numPoints ?
                    'SinglePoint' : 'NoPoints';
            var langFormatStr = ('accessibility.screenReaderSection.annotations.description' +
                    pointsSelector);
            var context = {
                    annotationText: labelText,
                    annotation: label,
                    numPoints: numPoints,
                    annotationPoint: pointValueDescriptions[0],
                    additionalAnnotationPoints: pointValueDescriptions.slice(1)
                };
            return chart.langFormat(langFormatStr, context);
        }
        /**
         * Return array of HTML strings for each annotation label in the chart.
         *
         * @private
         * @param {Highcharts.Chart} chart The chart to get annotation info on.
         * @return {Array<string>} Array of strings with HTML content for each annotation label.
         */
        function getAnnotationListItems(chart) {
            var labels = getChartAnnotationLabels(chart);
            return labels.map(function (label) {
                var desc = escapeStringForHTML(stripHTMLTagsFromString(getAnnotationLabelDescription(label)));
                return desc ? "<li>".concat(desc, "</li>") : '';
            });
        }
        /**
         * Return the annotation info for a chart as string.
         *
         * @private
         * @param {Highcharts.Chart} chart The chart to get annotation info on.
         * @return {string} String with HTML content or empty string if no annotations.
         */
        function getAnnotationsInfoHTML(chart) {
            var annotations = chart.annotations;
            if (!(annotations && annotations.length)) {
                return '';
            }
            var annotationItems = getAnnotationListItems(chart);
            return "<ul style=\"list-style-type: none\">".concat(annotationItems.join(' '), "</ul>");
        }
        /**
         * Return the texts for the annotation(s) connected to a point, or empty array
         * if none.
         *
         * @private
         * @param {Highcharts.Point} point The data point to get the annotation info from.
         * @return {Array<string>} Annotation texts
         */
        function getPointAnnotationTexts(point) {
            var labels = getChartAnnotationLabels(point.series.chart);
            var pointLabels = labels
                    .filter(function (label) { return label.points.indexOf(point) > -1; });
            if (!pointLabels.length) {
                return [];
            }
            return pointLabels.map(function (label) { return "".concat(getLabelText(label)); });
        }
        /* *
         *
         *  Default Export
         *
         * */
        var AnnotationsA11y = {
                getAnnotationsInfoHTML: getAnnotationsInfoHTML,
                getAnnotationLabelDescription: getAnnotationLabelDescription,
                getAnnotationListItems: getAnnotationListItems,
                getPointAnnotationTexts: getPointAnnotationTexts
            };

        return AnnotationsA11y;
    });
    _registerModule(_modules, 'Accessibility/Components/InfoRegionsComponent.js', [_modules['Accessibility/A11yI18n.js'], _modules['Accessibility/AccessibilityComponent.js'], _modules['Accessibility/Utils/Announcer.js'], _modules['Accessibility/Components/AnnotationsA11y.js'], _modules['Core/Renderer/HTML/AST.js'], _modules['Accessibility/Utils/ChartUtilities.js'], _modules['Core/FormatUtilities.js'], _modules['Core/Globals.js'], _modules['Accessibility/Utils/HTMLUtilities.js'], _modules['Core/Utilities.js']], function (A11yI18n, AccessibilityComponent, Announcer, AnnotationsA11y, AST, CU, F, H, HU, U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Accessibility component for chart info region and table.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var __extends = (this && this.__extends) || (function () {
                var extendStatics = function (d,
            b) {
                    extendStatics = Object.setPrototypeOf ||
                        ({ __proto__: [] } instanceof Array && function (d,
            b) { d.__proto__ = b; }) ||
                        function (d,
            b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
                return extendStatics(d, b);
            };
            return function (d, b) {
                extendStatics(d, b);
                function __() { this.constructor = d; }
                d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
            };
        })();
        var getAnnotationsInfoHTML = AnnotationsA11y.getAnnotationsInfoHTML;
        var getAxisDescription = CU.getAxisDescription,
            getAxisRangeDescription = CU.getAxisRangeDescription,
            getChartTitle = CU.getChartTitle,
            unhideChartElementFromAT = CU.unhideChartElementFromAT;
        var format = F.format;
        var doc = H.doc;
        var addClass = HU.addClass,
            getElement = HU.getElement,
            getHeadingTagNameForElement = HU.getHeadingTagNameForElement,
            stripHTMLTagsFromString = HU.stripHTMLTagsFromString,
            visuallyHideElement = HU.visuallyHideElement;
        var attr = U.attr,
            pick = U.pick;
        /* *
         *
         *  Functions
         *
         * */
        /* eslint-disable valid-jsdoc */
        /**
         * @private
         */
        function getTableSummary(chart) {
            return chart.langFormat('accessibility.table.tableSummary', { chart: chart });
        }
        /**
         * @private
         */
        function getTypeDescForMapChart(chart, formatContext) {
            return formatContext.mapTitle ?
                chart.langFormat('accessibility.chartTypes.mapTypeDescription', formatContext) :
                chart.langFormat('accessibility.chartTypes.unknownMap', formatContext);
        }
        /**
         * @private
         */
        function getTypeDescForCombinationChart(chart, formatContext) {
            return chart.langFormat('accessibility.chartTypes.combinationChart', formatContext);
        }
        /**
         * @private
         */
        function getTypeDescForEmptyChart(chart, formatContext) {
            return chart.langFormat('accessibility.chartTypes.emptyChart', formatContext);
        }
        /**
         * @private
         */
        function buildTypeDescriptionFromSeries(chart, types, context) {
            var firstType = types[0], typeExplaination = chart.langFormat('accessibility.seriesTypeDescriptions.' + firstType, context), multi = chart.series && chart.series.length < 2 ? 'Single' : 'Multiple';
            return (chart.langFormat('accessibility.chartTypes.' + firstType + multi, context) ||
                chart.langFormat('accessibility.chartTypes.default' + multi, context)) + (typeExplaination ? ' ' + typeExplaination : '');
        }
        /**
         * Return simplified explaination of chart type. Some types will not be
         * familiar to most users, but in those cases we try to add an explaination
         * of the type.
         *
         * @private
         * @function Highcharts.Chart#getTypeDescription
         * @param {Array<string>} types The series types in this chart.
         * @return {string} The text description of the chart type.
         */
        function getTypeDescription(chart, types) {
            var firstType = types[0],
                firstSeries = chart.series && chart.series[0] || {},
                mapTitle = chart.mapView && chart.mapView.geoMap &&
                    chart.mapView.geoMap.title,
                formatContext = {
                    numSeries: chart.series.length,
                    numPoints: firstSeries.points && firstSeries.points.length,
                    chart: chart,
                    mapTitle: mapTitle
                };
            if (!firstType) {
                return getTypeDescForEmptyChart(chart, formatContext);
            }
            if (firstType === 'map') {
                return getTypeDescForMapChart(chart, formatContext);
            }
            if (chart.types.length > 1) {
                return getTypeDescForCombinationChart(chart, formatContext);
            }
            return buildTypeDescriptionFromSeries(chart, types, formatContext);
        }
        /**
         * @private
         */
        function stripEmptyHTMLTags(str) {
            return str.replace(/<(\w+)[^>]*?>\s*<\/\1>/g, '');
        }
        /* *
         *
         *  Class
         *
         * */
        /**
         * The InfoRegionsComponent class
         *
         * @private
         * @class
         * @name Highcharts.InfoRegionsComponent
         */
        var InfoRegionsComponent = /** @class */ (function (_super) {
                __extends(InfoRegionsComponent, _super);
            function InfoRegionsComponent() {
                /* *
                 *
                 *  Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.announcer = void 0;
                _this.screenReaderSections = {};
                return _this;
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Init the component
             * @private
             */
            InfoRegionsComponent.prototype.init = function () {
                var chart = this.chart;
                var component = this;
                this.initRegionsDefinitions();
                this.addEvent(chart, 'aftergetTableAST', function (e) {
                    component.onDataTableCreated(e);
                });
                this.addEvent(chart, 'afterViewData', function (e) {
                    if (e.wasHidden) {
                        component.dataTableDiv = e.element;
                        // Use a small delay to give browsers & AT time to
                        // register the new table.
                        setTimeout(function () {
                            component.focusDataTable();
                        }, 300);
                    }
                });
                this.announcer = new Announcer(chart, 'assertive');
            };
            /**
             * @private
             */
            InfoRegionsComponent.prototype.initRegionsDefinitions = function () {
                var component = this;
                this.screenReaderSections = {
                    before: {
                        element: null,
                        buildContent: function (chart) {
                            var formatter = chart.options.accessibility
                                    .screenReaderSection.beforeChartFormatter;
                            return formatter ? formatter(chart) :
                                component.defaultBeforeChartFormatter(chart);
                        },
                        insertIntoDOM: function (el, chart) {
                            chart.renderTo.insertBefore(el, chart.renderTo.firstChild);
                        },
                        afterInserted: function () {
                            if (typeof component.sonifyButtonId !== 'undefined') {
                                component.initSonifyButton(component.sonifyButtonId);
                            }
                            if (typeof component.dataTableButtonId !== 'undefined') {
                                component.initDataTableButton(component.dataTableButtonId);
                            }
                        }
                    },
                    after: {
                        element: null,
                        buildContent: function (chart) {
                            var formatter = chart.options.accessibility
                                    .screenReaderSection
                                    .afterChartFormatter;
                            return formatter ? formatter(chart) :
                                component.defaultAfterChartFormatter();
                        },
                        insertIntoDOM: function (el, chart) {
                            chart.renderTo.insertBefore(el, chart.container.nextSibling);
                        },
                        afterInserted: function () {
                            if (component.chart.accessibility) {
                                component.chart.accessibility
                                    .keyboardNavigation.updateExitAnchor(); // #15986
                            }
                        }
                    }
                };
            };
            /**
             * Called on chart render. Have to update the sections on render, in order
             * to get a11y info from series.
             */
            InfoRegionsComponent.prototype.onChartRender = function () {
                var component = this;
                this.linkedDescriptionElement = this.getLinkedDescriptionElement();
                this.setLinkedDescriptionAttrs();
                Object.keys(this.screenReaderSections).forEach(function (regionKey) {
                    component.updateScreenReaderSection(regionKey);
                });
            };
            /**
             * @private
             */
            InfoRegionsComponent.prototype.getLinkedDescriptionElement = function () {
                var chartOptions = this.chart.options,
                    linkedDescOption = chartOptions.accessibility.linkedDescription;
                if (!linkedDescOption) {
                    return;
                }
                if (typeof linkedDescOption !== 'string') {
                    return linkedDescOption;
                }
                var query = format(linkedDescOption,
                    this.chart),
                    queryMatch = doc.querySelectorAll(query);
                if (queryMatch.length === 1) {
                    return queryMatch[0];
                }
            };
            /**
             * @private
             */
            InfoRegionsComponent.prototype.setLinkedDescriptionAttrs = function () {
                var el = this.linkedDescriptionElement;
                if (el) {
                    el.setAttribute('aria-hidden', 'true');
                    addClass(el, 'highcharts-linked-description');
                }
            };
            /**
             * @private
             * @param {string} regionKey
             * The name/key of the region to update
             */
            InfoRegionsComponent.prototype.updateScreenReaderSection = function (regionKey) {
                var chart = this.chart;
                var region = this.screenReaderSections[regionKey];
                var content = region.buildContent(chart);
                var sectionDiv = region.element = (region.element || this.createElement('div'));
                var hiddenDiv = (sectionDiv.firstChild || this.createElement('div'));
                if (content) {
                    this.setScreenReaderSectionAttribs(sectionDiv, regionKey);
                    AST.setElementHTML(hiddenDiv, content);
                    sectionDiv.appendChild(hiddenDiv);
                    region.insertIntoDOM(sectionDiv, chart);
                    if (chart.styledMode) {
                        addClass(hiddenDiv, 'highcharts-visually-hidden');
                    }
                    else {
                        visuallyHideElement(hiddenDiv);
                    }
                    unhideChartElementFromAT(chart, hiddenDiv);
                    if (region.afterInserted) {
                        region.afterInserted();
                    }
                }
                else {
                    if (sectionDiv.parentNode) {
                        sectionDiv.parentNode.removeChild(sectionDiv);
                    }
                    region.element = null;
                }
            };
            /**
             * Apply a11y attributes to a screen reader info section
             * @private
             * @param {Highcharts.HTMLDOMElement} sectionDiv The section element
             * @param {string} regionKey Name/key of the region we are setting attrs for
             */
            InfoRegionsComponent.prototype.setScreenReaderSectionAttribs = function (sectionDiv, regionKey) {
                var chart = this.chart, labelText = chart.langFormat('accessibility.screenReaderSection.' + regionKey +
                        'RegionLabel', { chart: chart, chartTitle: getChartTitle(chart) }), sectionId = "highcharts-screen-reader-region-".concat(regionKey, "-").concat(chart.index);
                attr(sectionDiv, {
                    id: sectionId,
                    'aria-label': labelText || void 0
                });
                // Sections are wrapped to be positioned relatively to chart in case
                // elements inside are tabbed to.
                sectionDiv.style.position = 'relative';
                if (labelText) {
                    sectionDiv.setAttribute('role', chart.options.accessibility.landmarkVerbosity === 'all' ?
                        'region' : 'group');
                }
            };
            /**
             * @private
             */
            InfoRegionsComponent.prototype.defaultBeforeChartFormatter = function () {
                var chart = this.chart,
                    format = chart.options.accessibility.screenReaderSection
                        .beforeChartFormat;
                if (!format) {
                    return '';
                }
                var axesDesc = this.getAxesDescription(),
                    shouldHaveSonifyBtn = (chart.sonify &&
                        chart.options.sonification &&
                        chart.options.sonification.enabled),
                    sonifyButtonId = 'highcharts-a11y-sonify-data-btn-' +
                        chart.index,
                    dataTableButtonId = 'hc-linkto-highcharts-data-table-' +
                        chart.index,
                    annotationsList = getAnnotationsInfoHTML(chart),
                    annotationsTitleStr = chart.langFormat('accessibility.screenReaderSection.annotations.heading', { chart: chart }),
                    context = {
                        headingTagName: getHeadingTagNameForElement(chart.renderTo),
                        chartTitle: getChartTitle(chart),
                        typeDescription: this.getTypeDescriptionText(),
                        chartSubtitle: this.getSubtitleText(),
                        chartLongdesc: this.getLongdescText(),
                        xAxisDescription: axesDesc.xAxis,
                        yAxisDescription: axesDesc.yAxis,
                        playAsSoundButton: shouldHaveSonifyBtn ?
                            this.getSonifyButtonText(sonifyButtonId) : '',
                        viewTableButton: chart.getCSV ?
                            this.getDataTableButtonText(dataTableButtonId) : '',
                        annotationsTitle: annotationsList ? annotationsTitleStr : '',
                        annotationsList: annotationsList
                    },
                    formattedString = A11yI18n.i18nFormat(format,
                    context,
                    chart);
                this.dataTableButtonId = dataTableButtonId;
                this.sonifyButtonId = sonifyButtonId;
                return stripEmptyHTMLTags(formattedString);
            };
            /**
             * @private
             */
            InfoRegionsComponent.prototype.defaultAfterChartFormatter = function () {
                var chart = this.chart;
                var format = chart.options.accessibility.screenReaderSection
                        .afterChartFormat;
                if (!format) {
                    return '';
                }
                var context = { endOfChartMarker: this.getEndOfChartMarkerText() };
                var formattedString = A11yI18n.i18nFormat(format,
                    context,
                    chart);
                return stripEmptyHTMLTags(formattedString);
            };
            /**
             * @private
             */
            InfoRegionsComponent.prototype.getLinkedDescription = function () {
                var el = this.linkedDescriptionElement,
                    content = el && el.innerHTML || '';
                return stripHTMLTagsFromString(content);
            };
            /**
             * @private
             */
            InfoRegionsComponent.prototype.getLongdescText = function () {
                var chartOptions = this.chart.options,
                    captionOptions = chartOptions.caption,
                    captionText = captionOptions && captionOptions.text,
                    linkedDescription = this.getLinkedDescription();
                return (chartOptions.accessibility.description ||
                    linkedDescription ||
                    captionText ||
                    '');
            };
            /**
             * @private
             */
            InfoRegionsComponent.prototype.getTypeDescriptionText = function () {
                var chart = this.chart;
                return chart.types ?
                    chart.options.accessibility.typeDescription ||
                        getTypeDescription(chart, chart.types) : '';
            };
            /**
             * @private
             */
            InfoRegionsComponent.prototype.getDataTableButtonText = function (buttonId) {
                var chart = this.chart,
                    buttonText = chart.langFormat('accessibility.table.viewAsDataTableButtonText', { chart: chart,
                    chartTitle: getChartTitle(chart) });
                return '<button id="' + buttonId + '">' + buttonText + '</button>';
            };
            /**
             * @private
             */
            InfoRegionsComponent.prototype.getSonifyButtonText = function (buttonId) {
                var chart = this.chart;
                if (chart.options.sonification &&
                    chart.options.sonification.enabled === false) {
                    return '';
                }
                var buttonText = chart.langFormat('accessibility.sonification.playAsSoundButtonText', { chart: chart,
                    chartTitle: getChartTitle(chart) });
                return '<button id="' + buttonId + '">' + buttonText + '</button>';
            };
            /**
             * @private
             */
            InfoRegionsComponent.prototype.getSubtitleText = function () {
                var subtitle = (this.chart.options.subtitle);
                return stripHTMLTagsFromString(subtitle && subtitle.text || '');
            };
            /**
             * @private
             */
            InfoRegionsComponent.prototype.getEndOfChartMarkerText = function () {
                var chart = this.chart, markerText = chart.langFormat('accessibility.screenReaderSection.endOfChartMarker', { chart: chart }), id = 'highcharts-end-of-chart-marker-' + chart.index;
                return '<div id="' + id + '">' + markerText + '</div>';
            };
            /**
             * @private
             * @param {Highcharts.Dictionary<string>} e
             */
            InfoRegionsComponent.prototype.onDataTableCreated = function (e) {
                var chart = this.chart;
                if (chart.options.accessibility.enabled) {
                    if (this.viewDataTableButton) {
                        this.viewDataTableButton.setAttribute('aria-expanded', 'true');
                    }
                    var attributes = e.tree.attributes || {};
                    attributes.tabindex = -1;
                    attributes.summary = getTableSummary(chart);
                    e.tree.attributes = attributes;
                }
            };
            /**
             * @private
             */
            InfoRegionsComponent.prototype.focusDataTable = function () {
                var tableDiv = this.dataTableDiv,
                    table = tableDiv && tableDiv.getElementsByTagName('table')[0];
                if (table && table.focus) {
                    table.focus();
                }
            };
            /**
             * @private
             * @param {string} sonifyButtonId
             */
            InfoRegionsComponent.prototype.initSonifyButton = function (sonifyButtonId) {
                var _this = this;
                var el = this.sonifyButton = getElement(sonifyButtonId);
                var chart = this.chart;
                var defaultHandler = function (e) {
                        if (el) {
                            el.setAttribute('aria-hidden', 'true');
                        el.setAttribute('aria-label', '');
                    }
                    e.preventDefault();
                    e.stopPropagation();
                    var announceMsg = chart.langFormat('accessibility.sonification.playAsSoundClickAnnouncement', { chart: chart });
                    _this.announcer.announce(announceMsg);
                    setTimeout(function () {
                        if (el) {
                            el.removeAttribute('aria-hidden');
                            el.removeAttribute('aria-label');
                        }
                        if (chart.sonify) {
                            chart.sonify();
                        }
                    }, 1000); // Delay to let screen reader speak the button press
                };
                if (el && chart) {
                    el.setAttribute('tabindex', -1);
                    el.onclick = function (e) {
                        var onPlayAsSoundClick = (chart.options.accessibility &&
                                chart.options.accessibility.screenReaderSection
                                    .onPlayAsSoundClick);
                        (onPlayAsSoundClick || defaultHandler).call(this, e, chart);
                    };
                }
            };
            /**
             * Set attribs and handlers for default viewAsDataTable button if exists.
             * @private
             * @param {string} tableButtonId
             */
            InfoRegionsComponent.prototype.initDataTableButton = function (tableButtonId) {
                var el = this.viewDataTableButton = getElement(tableButtonId), chart = this.chart, tableId = tableButtonId.replace('hc-linkto-', '');
                if (el) {
                    attr(el, {
                        tabindex: -1,
                        'aria-expanded': !!getElement(tableId)
                    });
                    el.onclick = chart.options.accessibility
                        .screenReaderSection.onViewDataTableClick ||
                        function () {
                            chart.viewData();
                        };
                }
            };
            /**
             * Return object with text description of each of the chart's axes.
             * @private
             */
            InfoRegionsComponent.prototype.getAxesDescription = function () {
                var chart = this.chart,
                    shouldDescribeColl = function (collectionKey,
                    defaultCondition) {
                        var axes = chart[collectionKey];
                    return axes.length > 1 || axes[0] &&
                        pick(axes[0].options.accessibility &&
                            axes[0].options.accessibility.enabled, defaultCondition);
                }, hasNoMap = !!chart.types &&
                    chart.types.indexOf('map') < 0 &&
                    chart.types.indexOf('treemap') < 0 &&
                    chart.types.indexOf('tilemap') < 0, hasCartesian = !!chart.hasCartesianSeries, showXAxes = shouldDescribeColl('xAxis', !chart.angular && hasCartesian && hasNoMap), showYAxes = shouldDescribeColl('yAxis', hasCartesian && hasNoMap), desc = {};
                if (showXAxes) {
                    desc.xAxis = this.getAxisDescriptionText('xAxis');
                }
                if (showYAxes) {
                    desc.yAxis = this.getAxisDescriptionText('yAxis');
                }
                return desc;
            };
            /**
             * @private
             */
            InfoRegionsComponent.prototype.getAxisDescriptionText = function (collectionKey) {
                var chart = this.chart;
                var axes = chart[collectionKey];
                return chart.langFormat('accessibility.axis.' + collectionKey + 'Description' + (axes.length > 1 ? 'Plural' : 'Singular'), {
                    chart: chart,
                    names: axes.map(function (axis) {
                        return getAxisDescription(axis);
                    }),
                    ranges: axes.map(function (axis) {
                        return getAxisRangeDescription(axis);
                    }),
                    numAxes: axes.length
                });
            };
            /**
             * Remove component traces
             */
            InfoRegionsComponent.prototype.destroy = function () {
                if (this.announcer) {
                    this.announcer.destroy();
                }
            };
            return InfoRegionsComponent;
        }(AccessibilityComponent));
        /* *
         *
         *  Default Export
         *
         * */

        return InfoRegionsComponent;
    });
    _registerModule(_modules, 'Accessibility/Components/MenuComponent.js', [_modules['Core/Chart/Chart.js'], _modules['Core/Utilities.js'], _modules['Accessibility/AccessibilityComponent.js'], _modules['Accessibility/KeyboardNavigationHandler.js'], _modules['Accessibility/Utils/ChartUtilities.js'], _modules['Accessibility/Utils/HTMLUtilities.js']], function (Chart, U, AccessibilityComponent, KeyboardNavigationHandler, ChartUtilities, HTMLUtilities) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Accessibility component for exporting menu.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var __extends = (this && this.__extends) || (function () {
                var extendStatics = function (d,
            b) {
                    extendStatics = Object.setPrototypeOf ||
                        ({ __proto__: [] } instanceof Array && function (d,
            b) { d.__proto__ = b; }) ||
                        function (d,
            b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
                return extendStatics(d, b);
            };
            return function (d, b) {
                extendStatics(d, b);
                function __() { this.constructor = d; }
                d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
            };
        })();
        var attr = U.attr;
        var getChartTitle = ChartUtilities.getChartTitle,
            unhideChartElementFromAT = ChartUtilities.unhideChartElementFromAT;
        var getFakeMouseEvent = HTMLUtilities.getFakeMouseEvent;
        /* *
         *
         *  Functions
         *
         * */
        /* eslint-disable valid-jsdoc */
        /**
         * Get the wrapped export button element of a chart.
         * @private
         */
        function getExportMenuButtonElement(chart) {
            return chart.exportSVGElements && chart.exportSVGElements[0];
        }
        /**
         * @private
         */
        function exportingShouldHaveA11y(chart) {
            var exportingOpts = chart.options.exporting,
                exportButton = getExportMenuButtonElement(chart);
            return !!(exportingOpts &&
                exportingOpts.enabled !== false &&
                exportingOpts.accessibility &&
                exportingOpts.accessibility.enabled &&
                exportButton &&
                exportButton.element);
        }
        /* *
         *
         *  Class
         *
         * */
        /**
         * The MenuComponent class
         *
         * @private
         * @class
         * @name Highcharts.MenuComponent
         */
        var MenuComponent = /** @class */ (function (_super) {
                __extends(MenuComponent, _super);
            function MenuComponent() {
                return _super !== null && _super.apply(this, arguments) || this;
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Init the component
             */
            MenuComponent.prototype.init = function () {
                var chart = this.chart,
                    component = this;
                this.addEvent(chart, 'exportMenuShown', function () {
                    component.onMenuShown();
                });
                this.addEvent(chart, 'exportMenuHidden', function () {
                    component.onMenuHidden();
                });
                this.createProxyGroup();
            };
            /**
             * @private
             */
            MenuComponent.prototype.onMenuHidden = function () {
                var menu = this.chart.exportContextMenu;
                if (menu) {
                    menu.setAttribute('aria-hidden', 'true');
                }
                this.setExportButtonExpandedState('false');
            };
            /**
             * @private
             */
            MenuComponent.prototype.onMenuShown = function () {
                var chart = this.chart,
                    menu = chart.exportContextMenu;
                if (menu) {
                    this.addAccessibleContextMenuAttribs();
                    unhideChartElementFromAT(chart, menu);
                }
                this.setExportButtonExpandedState('true');
            };
            /**
             * @private
             * @param {string} stateStr
             */
            MenuComponent.prototype.setExportButtonExpandedState = function (stateStr) {
                if (this.exportButtonProxy) {
                    this.exportButtonProxy.buttonElement.setAttribute('aria-expanded', stateStr);
                }
            };
            /**
             * Called on each render of the chart. We need to update positioning of the
             * proxy overlay.
             */
            MenuComponent.prototype.onChartRender = function () {
                var chart = this.chart,
                    focusEl = chart.focusElement,
                    a11y = chart.accessibility;
                this.proxyProvider.clearGroup('chartMenu');
                this.proxyMenuButton();
                if (this.exportButtonProxy &&
                    focusEl &&
                    focusEl === chart.exportingGroup) {
                    if (focusEl.focusBorder) {
                        chart.setFocusToElement(focusEl, this.exportButtonProxy.buttonElement);
                    }
                    else if (a11y) {
                        a11y.keyboardNavigation.tabindexContainer.focus();
                    }
                }
            };
            /**
             * @private
             */
            MenuComponent.prototype.proxyMenuButton = function () {
                var chart = this.chart;
                var proxyProvider = this.proxyProvider;
                var buttonEl = getExportMenuButtonElement(chart);
                if (exportingShouldHaveA11y(chart) && buttonEl) {
                    this.exportButtonProxy = proxyProvider.addProxyElement('chartMenu', { click: buttonEl }, {
                        'aria-label': chart.langFormat('accessibility.exporting.menuButtonLabel', {
                            chart: chart,
                            chartTitle: getChartTitle(chart)
                        }),
                        'aria-expanded': false,
                        title: chart.options.lang.contextButtonTitle || null
                    });
                }
            };
            /**
             * @private
             */
            MenuComponent.prototype.createProxyGroup = function () {
                var chart = this.chart;
                if (chart && this.proxyProvider) {
                    this.proxyProvider.addGroup('chartMenu', 'div');
                }
            };
            /**
             * @private
             */
            MenuComponent.prototype.addAccessibleContextMenuAttribs = function () {
                var chart = this.chart,
                    exportList = chart.exportDivElements;
                if (exportList && exportList.length) {
                    // Set tabindex on the menu items to allow focusing by script
                    // Set role to give screen readers a chance to pick up the contents
                    exportList.forEach(function (item) {
                        if (item) {
                            if (item.tagName === 'LI' &&
                                !(item.children && item.children.length)) {
                                item.setAttribute('tabindex', -1);
                            }
                            else {
                                item.setAttribute('aria-hidden', 'true');
                            }
                        }
                    });
                    // Set accessibility properties on parent div
                    var parentDiv = (exportList[0] && exportList[0].parentNode);
                    if (parentDiv) {
                        attr(parentDiv, {
                            'aria-hidden': void 0,
                            'aria-label': chart.langFormat('accessibility.exporting.chartMenuLabel', { chart: chart }),
                            role: 'list' // Needed for webkit/VO
                        });
                    }
                }
            };
            /**
             * Get keyboard navigation handler for this component.
             * @private
             */
            MenuComponent.prototype.getKeyboardNavigation = function () {
                var keys = this.keyCodes,
                    chart = this.chart,
                    component = this;
                return new KeyboardNavigationHandler(chart, {
                    keyCodeMap: [
                        // Arrow prev handler
                        [
                            [keys.left, keys.up],
                            function () {
                                return component.onKbdPrevious(this);
                            }
                        ],
                        // Arrow next handler
                        [
                            [keys.right, keys.down],
                            function () {
                                return component.onKbdNext(this);
                            }
                        ],
                        // Click handler
                        [
                            [keys.enter, keys.space],
                            function () {
                                return component.onKbdClick(this);
                            }
                        ]
                    ],
                    // Only run exporting navigation if exporting support exists and is
                    // enabled on chart
                    validate: function () {
                        return !!chart.exporting &&
                            chart.options.exporting.enabled !== false &&
                            chart.options.exporting.accessibility.enabled !==
                                false;
                    },
                    // Focus export menu button
                    init: function () {
                        var proxy = component.exportButtonProxy;
                        var svgEl = component.chart.exportingGroup;
                        if (proxy && svgEl) {
                            chart.setFocusToElement(svgEl, proxy.buttonElement);
                        }
                    },
                    // Hide the menu
                    terminate: function () {
                        chart.hideExportMenu();
                    }
                });
            };
            /**
             * @private
             * @param {Highcharts.KeyboardNavigationHandler} keyboardNavigationHandler
             * @return {number} Response code
             */
            MenuComponent.prototype.onKbdPrevious = function (keyboardNavigationHandler) {
                var chart = this.chart;
                var a11yOptions = chart.options.accessibility;
                var response = keyboardNavigationHandler.response;
                // Try to highlight prev item in list. Highlighting e.g.
                // separators will fail.
                var i = chart.highlightedExportItemIx || 0;
                while (i--) {
                    if (chart.highlightExportItem(i)) {
                        return response.success;
                    }
                }
                // We failed, so wrap around or move to prev module
                if (a11yOptions.keyboardNavigation.wrapAround) {
                    chart.highlightLastExportItem();
                    return response.success;
                }
                return response.prev;
            };
            /**
             * @private
             * @param {Highcharts.KeyboardNavigationHandler} keyboardNavigationHandler
             * @return {number} Response code
             */
            MenuComponent.prototype.onKbdNext = function (keyboardNavigationHandler) {
                var chart = this.chart;
                var a11yOptions = chart.options.accessibility;
                var response = keyboardNavigationHandler.response;
                // Try to highlight next item in list. Highlighting e.g.
                // separators will fail.
                for (var i = (chart.highlightedExportItemIx || 0) + 1; i < chart.exportDivElements.length; ++i) {
                    if (chart.highlightExportItem(i)) {
                        return response.success;
                    }
                }
                // We failed, so wrap around or move to next module
                if (a11yOptions.keyboardNavigation.wrapAround) {
                    chart.highlightExportItem(0);
                    return response.success;
                }
                return response.next;
            };
            /**
             * @private
             * @param {Highcharts.KeyboardNavigationHandler} keyboardNavigationHandler
             * @return {number} Response code
             */
            MenuComponent.prototype.onKbdClick = function (keyboardNavigationHandler) {
                var chart = this.chart;
                var curHighlightedItem = chart.exportDivElements[chart.highlightedExportItemIx];
                var exportButtonElement = getExportMenuButtonElement(chart).element;
                if (chart.openMenu) {
                    this.fakeClickEvent(curHighlightedItem);
                }
                else {
                    this.fakeClickEvent(exportButtonElement);
                    chart.highlightExportItem(0);
                }
                return keyboardNavigationHandler.response.success;
            };
            return MenuComponent;
        }(AccessibilityComponent));
        /* *
         *
         *  Class Namespace
         *
         * */
        (function (MenuComponent) {
            /* *
             *
             *  Declarations
             *
             * */
            /* *
             *
             *  Constants
             *
             * */
            var composedClasses = [];
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * @private
             */
            function compose(ChartClass) {
                if (composedClasses.indexOf(ChartClass) === -1) {
                    composedClasses.push(ChartClass);
                    var chartProto = Chart.prototype;
                    chartProto.hideExportMenu = chartHideExportMenu;
                    chartProto.highlightExportItem = chartHighlightExportItem;
                    chartProto.highlightLastExportItem = chartHighlightLastExportItem;
                    chartProto.showExportMenu = chartShowExportMenu;
                }
            }
            MenuComponent.compose = compose;
            /**
             * Show the export menu and focus the first item (if exists).
             *
             * @private
             * @function Highcharts.Chart#showExportMenu
             */
            function chartShowExportMenu() {
                var exportButton = getExportMenuButtonElement(this);
                if (exportButton) {
                    var el = exportButton.element;
                    if (el.onclick) {
                        el.onclick(getFakeMouseEvent('click'));
                    }
                }
            }
            /**
             * @private
             * @function Highcharts.Chart#hideExportMenu
             */
            function chartHideExportMenu() {
                var chart = this,
                    exportList = chart.exportDivElements;
                if (exportList && chart.exportContextMenu && chart.openMenu) {
                    // Reset hover states etc.
                    exportList.forEach(function (el) {
                        if (el &&
                            el.className === 'highcharts-menu-item' &&
                            el.onmouseout) {
                            el.onmouseout(getFakeMouseEvent('mouseout'));
                        }
                    });
                    chart.highlightedExportItemIx = 0;
                    // Hide the menu div
                    chart.exportContextMenu.hideMenu();
                    // Make sure the chart has focus and can capture keyboard events
                    chart.container.focus();
                }
            }
            /**
             * Highlight export menu item by index.
             *
             * @private
             * @function Highcharts.Chart#highlightExportItem
             */
            function chartHighlightExportItem(ix) {
                var listItem = this.exportDivElements && this.exportDivElements[ix];
                var curHighlighted = this.exportDivElements &&
                        this.exportDivElements[this.highlightedExportItemIx];
                if (listItem &&
                    listItem.tagName === 'LI' &&
                    !(listItem.children && listItem.children.length)) {
                    // Test if we have focus support for SVG elements
                    var hasSVGFocusSupport = !!(this.renderTo.getElementsByTagName('g')[0] || {}).focus;
                    // Only focus if we can set focus back to the elements after
                    // destroying the menu (#7422)
                    if (listItem.focus && hasSVGFocusSupport) {
                        listItem.focus();
                    }
                    if (curHighlighted && curHighlighted.onmouseout) {
                        curHighlighted.onmouseout(getFakeMouseEvent('mouseout'));
                    }
                    if (listItem.onmouseover) {
                        listItem.onmouseover(getFakeMouseEvent('mouseover'));
                    }
                    this.highlightedExportItemIx = ix;
                    return true;
                }
                return false;
            }
            /**
             * Try to highlight the last valid export menu item.
             *
             * @private
             * @function Highcharts.Chart#highlightLastExportItem
             */
            function chartHighlightLastExportItem() {
                var chart = this;
                if (chart.exportDivElements) {
                    var i = chart.exportDivElements.length;
                    while (i--) {
                        if (chart.highlightExportItem(i)) {
                            return true;
                        }
                    }
                }
                return false;
            }
        })(MenuComponent || (MenuComponent = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return MenuComponent;
    });
    _registerModule(_modules, 'Accessibility/KeyboardNavigation.js', [_modules['Core/Globals.js'], _modules['Accessibility/Components/MenuComponent.js'], _modules['Core/Utilities.js'], _modules['Accessibility/Utils/EventProvider.js'], _modules['Accessibility/Utils/HTMLUtilities.js']], function (H, MenuComponent, U, EventProvider, HTMLUtilities) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Main keyboard navigation handling.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var doc = H.doc,
            win = H.win;
        var addEvent = U.addEvent,
            fireEvent = U.fireEvent;
        var getElement = HTMLUtilities.getElement,
            simulatedEventTarget = HTMLUtilities.simulatedEventTarget;
        /* *
         *
         *  Class
         *
         * */
        /**
         * The KeyboardNavigation class, containing the overall keyboard navigation
         * logic for the chart.
         *
         * @requires module:modules/accessibility
         *
         * @private
         * @class
         * @param {Highcharts.Chart} chart
         *        Chart object
         * @param {Object} components
         *        Map of component names to AccessibilityComponent objects.
         * @name Highcharts.KeyboardNavigation
         */
        var KeyboardNavigation = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function KeyboardNavigation(chart, components) {
                    /* *
                     *
                     *  Properties
                     *
                     * */
                    this.chart = void 0;
                this.components = void 0;
                this.currentModuleIx = NaN;
                this.eventProvider = void 0;
                this.exitAnchor = void 0;
                this.modules = [];
                this.tabindexContainer = void 0;
                this.init(chart, components);
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Initialize the class
             * @private
             * @param {Highcharts.Chart} chart
             *        Chart object
             * @param {Object} components
             *        Map of component names to AccessibilityComponent objects.
             */
            KeyboardNavigation.prototype.init = function (chart, components) {
                var _this = this;
                var ep = this.eventProvider = new EventProvider();
                this.chart = chart;
                this.components = components;
                this.modules = [];
                this.currentModuleIx = 0;
                this.update();
                ep.addEvent(this.tabindexContainer, 'keydown', function (e) { return _this.onKeydown(e); });
                ep.addEvent(this.tabindexContainer, 'focus', function (e) { return _this.onFocus(e); });
                ['mouseup', 'touchend'].forEach(function (eventName) {
                    return ep.addEvent(doc, eventName, function (e) { return _this.onMouseUp(e); });
                });
                ['mousedown', 'touchstart'].forEach(function (eventName) {
                    return ep.addEvent(chart.renderTo, eventName, function () {
                        _this.isClickingChart = true;
                    });
                });
                ep.addEvent(chart.renderTo, 'mouseover', function () {
                    _this.pointerIsOverChart = true;
                });
                ep.addEvent(chart.renderTo, 'mouseout', function () {
                    _this.pointerIsOverChart = false;
                });
            };
            /**
             * Update the modules for the keyboard navigation.
             * @param {Array<string>} [order]
             *        Array specifying the tab order of the components.
             */
            KeyboardNavigation.prototype.update = function (order) {
                var a11yOptions = this.chart.options.accessibility,
                    keyboardOptions = a11yOptions && a11yOptions.keyboardNavigation,
                    components = this.components;
                this.updateContainerTabindex();
                if (keyboardOptions &&
                    keyboardOptions.enabled &&
                    order &&
                    order.length) {
                    // We (still) have keyboard navigation. Update module list
                    this.modules = order.reduce(function (modules, componentName) {
                        var navModules = components[componentName]
                                .getKeyboardNavigation();
                        return modules.concat(navModules);
                    }, []);
                    this.updateExitAnchor();
                }
                else {
                    this.modules = [];
                    this.currentModuleIx = 0;
                    this.removeExitAnchor();
                }
            };
            /**
             * We use an exit anchor to move focus out of chart whenever we want, by
             * setting focus to this div and not preventing the default tab action. We
             * also use this when users come back into the chart by tabbing back, in
             * order to navigate from the end of the chart.
             * @private
             */
            KeyboardNavigation.prototype.updateExitAnchor = function () {
                var endMarkerId = "highcharts-end-of-chart-marker-".concat(this.chart.index),
                    endMarker = getElement(endMarkerId);
                this.removeExitAnchor();
                if (endMarker) {
                    this.makeElementAnExitAnchor(endMarker);
                    this.exitAnchor = endMarker;
                }
                else {
                    this.createExitAnchor();
                }
            };
            /**
             * Move to prev/next module.
             * @private
             * @param {number} direction
             * Direction to move. +1 for next, -1 for prev.
             * @return {boolean}
             * True if there was a valid module in direction.
             */
            KeyboardNavigation.prototype.move = function (direction) {
                var curModule = this.modules && this.modules[this.currentModuleIx];
                if (curModule && curModule.terminate) {
                    curModule.terminate(direction);
                }
                // Remove existing focus border if any
                if (this.chart.focusElement) {
                    this.chart.focusElement.removeFocusBorder();
                }
                this.currentModuleIx += direction;
                var newModule = this.modules && this.modules[this.currentModuleIx];
                if (newModule) {
                    if (newModule.validate && !newModule.validate()) {
                        return this.move(direction); // Invalid module, recurse
                    }
                    if (newModule.init) {
                        newModule.init(direction); // Valid module, init it
                        return true;
                    }
                }
                // No module
                this.currentModuleIx = 0; // Reset counter
                // Set focus to chart or exit anchor depending on direction
                this.exiting = true;
                if (direction > 0) {
                    this.exitAnchor && this.exitAnchor.focus();
                }
                else {
                    this.tabindexContainer.focus();
                }
                return false;
            };
            /**
             * Function to run on container focus
             * @private
             * @param {global.FocusEvent} e Browser focus event.
             */
            KeyboardNavigation.prototype.onFocus = function (e) {
                var chart = this.chart;
                var focusComesFromChart = (e.relatedTarget &&
                        chart.container.contains(e.relatedTarget));
                // Init keyboard nav if tabbing into chart
                if (!this.exiting &&
                    !this.tabbingInBackwards &&
                    !this.isClickingChart &&
                    !focusComesFromChart) {
                    var ix = this.getFirstValidModuleIx();
                    if (ix !== null) {
                        this.currentModuleIx = ix;
                        this.modules[ix].init(1);
                    }
                }
                this.exiting = false;
            };
            /**
             * Reset chart navigation state if we mouse click and it's not already
             * reset. Reset fully if outside the chart, otherwise just hide focus
             * indicator.
             * @private
             */
            KeyboardNavigation.prototype.onMouseUp = function (e) {
                delete this.isClickingChart;
                if (!this.keyboardReset &&
                    e.relatedTarget !== simulatedEventTarget) {
                    var chart = this.chart;
                    if (!this.pointerIsOverChart) {
                        var curMod = this.modules &&
                                this.modules[this.currentModuleIx || 0];
                        if (curMod && curMod.terminate) {
                            curMod.terminate();
                        }
                        this.currentModuleIx = 0;
                    }
                    if (chart.focusElement) {
                        chart.focusElement.removeFocusBorder();
                        delete chart.focusElement;
                    }
                    this.keyboardReset = true;
                }
            };
            /**
             * Function to run on keydown
             * @private
             * @param {global.KeyboardEvent} ev Browser keydown event.
             */
            KeyboardNavigation.prototype.onKeydown = function (ev) {
                var e = ev || win.event,
                    curNavModule = (this.modules &&
                        this.modules.length &&
                        this.modules[this.currentModuleIx]);
                var preventDefault;
                // Used for resetting nav state when clicking outside chart
                this.keyboardReset = false;
                // Used for sending focus out of the chart by the modules.
                this.exiting = false;
                // If there is a nav module for the current index, run it.
                // Otherwise, we are outside of the chart in some direction.
                if (curNavModule) {
                    var response = curNavModule.run(e);
                    if (response === curNavModule.response.success) {
                        preventDefault = true;
                    }
                    else if (response === curNavModule.response.prev) {
                        preventDefault = this.move(-1);
                    }
                    else if (response === curNavModule.response.next) {
                        preventDefault = this.move(1);
                    }
                    if (preventDefault) {
                        e.preventDefault();
                        e.stopPropagation();
                    }
                }
            };
            /**
             * Chart container should have tabindex if navigation is enabled.
             * @private
             */
            KeyboardNavigation.prototype.updateContainerTabindex = function () {
                var a11yOptions = this.chart.options.accessibility,
                    keyboardOptions = a11yOptions && a11yOptions.keyboardNavigation,
                    shouldHaveTabindex = !(keyboardOptions && keyboardOptions.enabled === false),
                    chart = this.chart,
                    container = chart.container;
                var tabindexContainer;
                if (chart.renderTo.hasAttribute('tabindex')) {
                    container.removeAttribute('tabindex');
                    tabindexContainer = chart.renderTo;
                }
                else {
                    tabindexContainer = container;
                }
                this.tabindexContainer = tabindexContainer;
                var curTabindex = tabindexContainer.getAttribute('tabindex');
                if (shouldHaveTabindex && !curTabindex) {
                    tabindexContainer.setAttribute('tabindex', '0');
                }
                else if (!shouldHaveTabindex) {
                    chart.container.removeAttribute('tabindex');
                }
            };
            /**
             * Add new exit anchor to the chart.
             * @private
             */
            KeyboardNavigation.prototype.createExitAnchor = function () {
                var chart = this.chart,
                    exitAnchor = this.exitAnchor = doc.createElement('div');
                chart.renderTo.appendChild(exitAnchor);
                this.makeElementAnExitAnchor(exitAnchor);
            };
            /**
             * Add attributes and events to an element to make it function as an
             * exit anchor.
             * @private
             */
            KeyboardNavigation.prototype.makeElementAnExitAnchor = function (el) {
                var chartTabindex = this.tabindexContainer.getAttribute('tabindex') || 0;
                el.setAttribute('class', 'highcharts-exit-anchor');
                el.setAttribute('tabindex', chartTabindex);
                el.setAttribute('aria-hidden', false);
                // Handle focus
                this.addExitAnchorEventsToEl(el);
            };
            /**
             * Destroy the exit anchor and remove from DOM.
             * @private
             */
            KeyboardNavigation.prototype.removeExitAnchor = function () {
                if (this.exitAnchor && this.exitAnchor.parentNode) {
                    this.exitAnchor.parentNode.removeChild(this.exitAnchor);
                    delete this.exitAnchor;
                }
            };
            /**
             * Add focus handler to exit anchor element.
             * @private
             */
            KeyboardNavigation.prototype.addExitAnchorEventsToEl = function (element) {
                var chart = this.chart,
                    keyboardNavigation = this;
                this.eventProvider.addEvent(element, 'focus', function (ev) {
                    var e = ev || win.event,
                        focusComesFromChart = (e.relatedTarget &&
                            chart.container.contains(e.relatedTarget)),
                        comingInBackwards = !(focusComesFromChart || keyboardNavigation.exiting);
                    if (chart.focusElement) {
                        delete chart.focusElement;
                    }
                    if (comingInBackwards) {
                        // Focus the container instead
                        keyboardNavigation.tabbingInBackwards = true;
                        keyboardNavigation.tabindexContainer.focus();
                        delete keyboardNavigation.tabbingInBackwards;
                        e.preventDefault();
                        // Move to last valid keyboard nav module
                        // Note the we don't run it, just set the index
                        if (keyboardNavigation.modules &&
                            keyboardNavigation.modules.length) {
                            keyboardNavigation.currentModuleIx =
                                keyboardNavigation.modules.length - 1;
                            var curModule = keyboardNavigation.modules[keyboardNavigation.currentModuleIx];
                            // Validate the module
                            if (curModule &&
                                curModule.validate && !curModule.validate()) {
                                // Invalid. Try moving backwards to find next valid.
                                keyboardNavigation.move(-1);
                            }
                            else if (curModule) {
                                // We have a valid module, init it
                                curModule.init(-1);
                            }
                        }
                    }
                    else {
                        // Don't skip the next focus, we only skip once.
                        keyboardNavigation.exiting = false;
                    }
                });
            };
            /**
             * Get the ix of the first module that either does not require validation or
             * validates positively.
             * @private
             */
            KeyboardNavigation.prototype.getFirstValidModuleIx = function () {
                var len = this.modules.length;
                for (var i = 0; i < len; ++i) {
                    var mod = this.modules[i];
                    if (!mod.validate || mod.validate()) {
                        return i;
                    }
                }
                return null;
            };
            /**
             * Remove all traces of keyboard navigation.
             * @private
             */
            KeyboardNavigation.prototype.destroy = function () {
                this.removeExitAnchor();
                this.eventProvider.removeAddedEvents();
                this.chart.container.removeAttribute('tabindex');
            };
            return KeyboardNavigation;
        }());
        /* *
         *
         *  Class Namespace
         *
         * */
        (function (KeyboardNavigation) {
            /* *
             *
             *  Declarations
             *
             * */
            /* *
             *
             *  Construction
             *
             * */
            var composedItems = [];
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Composition function.
             * @private
             */
            function compose(ChartClass) {
                MenuComponent.compose(ChartClass);
                if (composedItems.indexOf(ChartClass) === -1) {
                    composedItems.push(ChartClass);
                    var chartProto = ChartClass.prototype;
                    chartProto.dismissPopupContent = chartDismissPopupContent;
                }
                if (composedItems.indexOf(doc) === -1) {
                    composedItems.push(doc);
                    addEvent(doc, 'keydown', documentOnKeydown);
                }
                return ChartClass;
            }
            KeyboardNavigation.compose = compose;
            /**
             * Dismiss popup content in chart, including export menu and tooltip.
             * @private
             */
            function chartDismissPopupContent() {
                var chart = this;
                fireEvent(this, 'dismissPopupContent', {}, function () {
                    if (chart.tooltip) {
                        chart.tooltip.hide(0);
                    }
                    chart.hideExportMenu();
                });
            }
            /**
             * Add event listener to document to detect ESC key press and dismiss
             * hover/popup content.
             * @private
             */
            function documentOnKeydown(e) {
                var keycode = e.which || e.keyCode;
                var esc = 27;
                if (keycode === esc && H.charts) {
                    H.charts.forEach(function (chart) {
                        if (chart && chart.dismissPopupContent) {
                            chart.dismissPopupContent();
                        }
                    });
                }
            }
        })(KeyboardNavigation || (KeyboardNavigation = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return KeyboardNavigation;
    });
    _registerModule(_modules, 'Accessibility/Components/LegendComponent.js', [_modules['Core/Animation/AnimationUtilities.js'], _modules['Core/Globals.js'], _modules['Core/Legend/Legend.js'], _modules['Core/Utilities.js'], _modules['Accessibility/AccessibilityComponent.js'], _modules['Accessibility/KeyboardNavigationHandler.js'], _modules['Accessibility/Utils/ChartUtilities.js'], _modules['Accessibility/Utils/HTMLUtilities.js']], function (A, H, Legend, U, AccessibilityComponent, KeyboardNavigationHandler, CU, HU) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Accessibility component for chart legend.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var __extends = (this && this.__extends) || (function () {
                var extendStatics = function (d,
            b) {
                    extendStatics = Object.setPrototypeOf ||
                        ({ __proto__: [] } instanceof Array && function (d,
            b) { d.__proto__ = b; }) ||
                        function (d,
            b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
                return extendStatics(d, b);
            };
            return function (d, b) {
                extendStatics(d, b);
                function __() { this.constructor = d; }
                d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
            };
        })();
        var animObject = A.animObject;
        var doc = H.doc;
        var addEvent = U.addEvent,
            fireEvent = U.fireEvent,
            isNumber = U.isNumber,
            pick = U.pick,
            syncTimeout = U.syncTimeout;
        var getChartTitle = CU.getChartTitle;
        var stripHTMLTags = HU.stripHTMLTagsFromString,
            addClass = HU.addClass,
            removeClass = HU.removeClass;
        /* *
         *
         *  Functions
         *
         * */
        /**
         * @private
         */
        function scrollLegendToItem(legend, itemIx) {
            var itemPage = (legend.allItems[itemIx].legendItem || {}).pageIx,
                curPage = legend.currentPage;
            if (typeof itemPage !== 'undefined' && itemPage + 1 !== curPage) {
                legend.scroll(1 + itemPage - curPage);
            }
        }
        /**
         * @private
         */
        function shouldDoLegendA11y(chart) {
            var items = chart.legend && chart.legend.allItems,
                legendA11yOptions = (chart.options.legend.accessibility || {}),
                unsupportedColorAxis = chart.colorAxis && chart.colorAxis.some(function (c) { return !c.dataClasses || !c.dataClasses.length; });
            return !!(items && items.length &&
                !unsupportedColorAxis &&
                legendA11yOptions.enabled !== false);
        }
        /**
         * @private
         */
        function setLegendItemHoverState(hoverActive, item) {
            var legendItem = item.legendItem || {};
            item.setState(hoverActive ? 'hover' : '', true);
            for (var _i = 0, _a = ['group', 'label', 'symbol']; _i < _a.length; _i++) {
                var key = _a[_i];
                var svgElement = legendItem[key];
                var element = svgElement && svgElement.element || svgElement;
                if (element) {
                    fireEvent(element, hoverActive ? 'mouseover' : 'mouseout');
                }
            }
        }
        /* *
         *
         *  Class
         *
         * */
        /**
         * The LegendComponent class
         *
         * @private
         * @class
         * @name Highcharts.LegendComponent
         */
        var LegendComponent = /** @class */ (function (_super) {
                __extends(LegendComponent, _super);
            function LegendComponent() {
                /* *
                 *
                 *  Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.highlightedLegendItemIx = NaN;
                _this.proxyGroup = null;
                return _this;
            }
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Init the component
             * @private
             */
            LegendComponent.prototype.init = function () {
                var component = this;
                this.recreateProxies();
                // Note: Chart could create legend dynamically, so events cannot be
                // tied to the component's chart's current legend.
                // @todo 1. attach component to created legends
                // @todo 2. move listeners to composition and access `this.component`
                this.addEvent(Legend, 'afterScroll', function () {
                    if (this.chart === component.chart) {
                        component.proxyProvider.updateGroupProxyElementPositions('legend');
                        component.updateLegendItemProxyVisibility();
                        if (component.highlightedLegendItemIx > -1) {
                            this.chart.highlightLegendItem(component.highlightedLegendItemIx);
                        }
                    }
                });
                this.addEvent(Legend, 'afterPositionItem', function (e) {
                    if (this.chart === component.chart && this.chart.renderer) {
                        component.updateProxyPositionForItem(e.item);
                    }
                });
                this.addEvent(Legend, 'afterRender', function () {
                    if (this.chart === component.chart &&
                        this.chart.renderer &&
                        component.recreateProxies()) {
                        syncTimeout(function () { return component.proxyProvider
                            .updateGroupProxyElementPositions('legend'); }, animObject(pick(this.chart.renderer.globalAnimation, true)).duration);
                    }
                });
            };
            /**
             * Update visibility of legend items when using paged legend
             * @private
             */
            LegendComponent.prototype.updateLegendItemProxyVisibility = function () {
                var chart = this.chart;
                var legend = chart.legend;
                var items = legend.allItems || [];
                var curPage = legend.currentPage || 1;
                var clipHeight = legend.clipHeight || 0;
                var legendItem;
                items.forEach(function (item) {
                    if (item.a11yProxyElement) {
                        var hasPages = legend.pages && legend.pages.length;
                        var proxyEl = item.a11yProxyElement.element;
                        var hide = false;
                        legendItem = item.legendItem || {};
                        if (hasPages) {
                            var itemPage = legendItem.pageIx || 0;
                            var y = legendItem.y || 0;
                            var h = legendItem.label ?
                                    Math.round(legendItem.label.getBBox().height) :
                                    0;
                            hide = y + h - legend.pages[itemPage] > clipHeight ||
                                itemPage !== curPage - 1;
                        }
                        if (hide) {
                            if (chart.styledMode) {
                                addClass(proxyEl, 'highcharts-a11y-invisible');
                            }
                            else {
                                proxyEl.style.visibility = 'hidden';
                            }
                        }
                        else {
                            removeClass(proxyEl, 'highcharts-a11y-invisible');
                            proxyEl.style.visibility = '';
                        }
                    }
                });
            };
            /**
             * @private
             */
            LegendComponent.prototype.onChartRender = function () {
                if (!shouldDoLegendA11y(this.chart)) {
                    this.removeProxies();
                }
            };
            /**
             * @private
             */
            LegendComponent.prototype.highlightAdjacentLegendPage = function (direction) {
                var chart = this.chart;
                var legend = chart.legend;
                var curPageIx = legend.currentPage || 1;
                var newPageIx = curPageIx + direction;
                var pages = legend.pages || [];
                if (newPageIx > 0 && newPageIx <= pages.length) {
                    var i = 0,
                        res = void 0;
                    for (var _i = 0, _a = legend.allItems; _i < _a.length; _i++) {
                        var item = _a[_i];
                        if (((item.legendItem || {}).pageIx || 0) + 1 === newPageIx) {
                            res = chart.highlightLegendItem(i);
                            if (res) {
                                this.highlightedLegendItemIx = i;
                            }
                        }
                        ++i;
                    }
                }
            };
            /**
             * @private
             */
            LegendComponent.prototype.updateProxyPositionForItem = function (item) {
                if (item.a11yProxyElement) {
                    item.a11yProxyElement.refreshPosition();
                }
            };
            /**
             * Returns false if legend a11y is disabled and proxies were not created,
             * true otherwise.
             * @private
             */
            LegendComponent.prototype.recreateProxies = function () {
                var focusedElement = doc.activeElement;
                var proxyGroup = this.proxyGroup;
                var shouldRestoreFocus = focusedElement && proxyGroup &&
                        proxyGroup.contains(focusedElement);
                this.removeProxies();
                if (shouldDoLegendA11y(this.chart)) {
                    this.addLegendProxyGroup();
                    this.proxyLegendItems();
                    this.updateLegendItemProxyVisibility();
                    this.updateLegendTitle();
                    if (shouldRestoreFocus) {
                        this.chart.highlightLegendItem(this.highlightedLegendItemIx);
                    }
                    return true;
                }
                return false;
            };
            /**
             * @private
             */
            LegendComponent.prototype.removeProxies = function () {
                this.proxyProvider.removeGroup('legend');
            };
            /**
             * @private
             */
            LegendComponent.prototype.updateLegendTitle = function () {
                var chart = this.chart;
                var legendTitle = stripHTMLTags((chart.legend &&
                        chart.legend.options.title &&
                        chart.legend.options.title.text ||
                        '').replace(/<br ?\/?>/g, ' '));
                var legendLabel = chart.langFormat('accessibility.legend.legendLabel' + (legendTitle ? '' : 'NoTitle'), {
                        chart: chart,
                        legendTitle: legendTitle,
                        chartTitle: getChartTitle(chart)
                    });
                this.proxyProvider.updateGroupAttrs('legend', {
                    'aria-label': legendLabel
                });
            };
            /**
             * @private
             */
            LegendComponent.prototype.addLegendProxyGroup = function () {
                var a11yOptions = this.chart.options.accessibility;
                var groupRole = a11yOptions.landmarkVerbosity === 'all' ?
                        'region' : null;
                this.proxyGroup = this.proxyProvider.addGroup('legend', 'ul', {
                    // Filled by updateLegendTitle, to keep up to date without
                    // recreating group
                    'aria-label': '_placeholder_',
                    role: groupRole
                });
            };
            /**
             * @private
             */
            LegendComponent.prototype.proxyLegendItems = function () {
                var component = this,
                    items = (this.chart.legend || {}).allItems || [];
                var legendItem;
                items.forEach(function (item) {
                    legendItem = item.legendItem || {};
                    if (legendItem.label && legendItem.label.element) {
                        component.proxyLegendItem(item);
                    }
                });
            };
            /**
             * @private
             * @param {Highcharts.BubbleLegendItem|Point|Highcharts.Series} item
             */
            LegendComponent.prototype.proxyLegendItem = function (item) {
                var legendItem = item.legendItem || {};
                if (!legendItem.label || !legendItem.group) {
                    return;
                }
                var itemLabel = this.chart.langFormat('accessibility.legend.legendItem', {
                        chart: this.chart,
                        itemName: stripHTMLTags(item.name),
                        item: item
                    });
                var attribs = {
                        tabindex: -1,
                        'aria-pressed': item.visible,
                        'aria-label': itemLabel
                    };
                // Considers useHTML
                var proxyPositioningElement = legendItem.group.div ?
                        legendItem.label :
                        legendItem.group;
                item.a11yProxyElement = this.proxyProvider.addProxyElement('legend', {
                    click: legendItem.label,
                    visual: proxyPositioningElement.element
                }, attribs);
            };
            /**
             * Get keyboard navigation handler for this component.
             * @private
             */
            LegendComponent.prototype.getKeyboardNavigation = function () {
                var keys = this.keyCodes,
                    component = this,
                    chart = this.chart;
                return new KeyboardNavigationHandler(chart, {
                    keyCodeMap: [
                        [
                            [keys.left, keys.right, keys.up, keys.down],
                            function (keyCode) {
                                return component.onKbdArrowKey(this, keyCode);
                            }
                        ],
                        [
                            [keys.enter, keys.space],
                            function () {
                                return component.onKbdClick(this);
                            }
                        ],
                        [
                            [keys.pageDown, keys.pageUp],
                            function (keyCode) {
                                var direction = keyCode === keys.pageDown ? 1 : -1;
                                component.highlightAdjacentLegendPage(direction);
                                return this.response.success;
                            }
                        ]
                    ],
                    validate: function () {
                        return component.shouldHaveLegendNavigation();
                    },
                    init: function () {
                        chart.highlightLegendItem(0);
                        component.highlightedLegendItemIx = 0;
                    },
                    terminate: function () {
                        component.highlightedLegendItemIx = -1;
                        chart.legend.allItems.forEach(function (item) { return setLegendItemHoverState(false, item); });
                    }
                });
            };
            /**
             * Arrow key navigation
             * @private
             */
            LegendComponent.prototype.onKbdArrowKey = function (keyboardNavigationHandler, keyCode) {
                var keys = this.keyCodes,
                    response = keyboardNavigationHandler.response,
                    chart = this.chart,
                    a11yOptions = chart.options.accessibility,
                    numItems = chart.legend.allItems.length,
                    direction = (keyCode === keys.left || keyCode === keys.up) ? -1 : 1;
                var res = chart.highlightLegendItem(this.highlightedLegendItemIx + direction);
                if (res) {
                    this.highlightedLegendItemIx += direction;
                    return response.success;
                }
                if (numItems > 1 &&
                    a11yOptions.keyboardNavigation.wrapAround) {
                    keyboardNavigationHandler.init(direction);
                    return response.success;
                }
                return response.success;
            };
            /**
             * @private
             * @param {Highcharts.KeyboardNavigationHandler} keyboardNavigationHandler
             * @return {number} Response code
             */
            LegendComponent.prototype.onKbdClick = function (keyboardNavigationHandler) {
                var legendItem = this.chart.legend.allItems[this.highlightedLegendItemIx];
                if (legendItem && legendItem.a11yProxyElement) {
                    legendItem.a11yProxyElement.click();
                }
                return keyboardNavigationHandler.response.success;
            };
            /**
             * @private
             */
            LegendComponent.prototype.shouldHaveLegendNavigation = function () {
                if (!shouldDoLegendA11y(this.chart)) {
                    return false;
                }
                var chart = this.chart,
                    legendOptions = chart.options.legend || {},
                    legendA11yOptions = (legendOptions.accessibility || {});
                return !!(chart.legend.display &&
                    legendA11yOptions.keyboardNavigation &&
                    legendA11yOptions.keyboardNavigation.enabled);
            };
            return LegendComponent;
        }(AccessibilityComponent));
        /* *
         *
         *  Class Namespace
         *
         * */
        (function (LegendComponent) {
            /* *
             *
             *  Declarations
             *
             * */
            /* *
             *
             *  Constants
             *
             * */
            var composedClasses = [];
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Highlight legend item by index.
             * @private
             */
            function chartHighlightLegendItem(ix) {
                var items = this.legend.allItems;
                var oldIx = this.accessibility &&
                        this.accessibility.components.legend.highlightedLegendItemIx;
                var itemToHighlight = items[ix],
                    legendItem = itemToHighlight.legendItem || {};
                if (itemToHighlight) {
                    if (isNumber(oldIx) && items[oldIx]) {
                        setLegendItemHoverState(false, items[oldIx]);
                    }
                    scrollLegendToItem(this.legend, ix);
                    var legendItemProp = legendItem.label;
                    var proxyBtn = itemToHighlight.a11yProxyElement &&
                            itemToHighlight.a11yProxyElement.buttonElement;
                    if (legendItemProp && legendItemProp.element && proxyBtn) {
                        this.setFocusToElement(legendItemProp, proxyBtn);
                    }
                    setLegendItemHoverState(true, itemToHighlight);
                    return true;
                }
                return false;
            }
            /**
             * @private
             */
            function compose(ChartClass, LegendClass) {
                if (composedClasses.indexOf(ChartClass) === -1) {
                    composedClasses.push(ChartClass);
                    var chartProto = ChartClass.prototype;
                    chartProto.highlightLegendItem = chartHighlightLegendItem;
                }
                if (composedClasses.indexOf(LegendClass) === -1) {
                    composedClasses.push(LegendClass);
                    addEvent(LegendClass, 'afterColorizeItem', legendOnAfterColorizeItem);
                }
            }
            LegendComponent.compose = compose;
            /**
             * Keep track of pressed state for legend items.
             * @private
             */
            function legendOnAfterColorizeItem(e) {
                var chart = this.chart,
                    a11yOptions = chart.options.accessibility,
                    legendItem = e.item;
                if (a11yOptions.enabled && legendItem && legendItem.a11yProxyElement) {
                    legendItem.a11yProxyElement.buttonElement.setAttribute('aria-pressed', e.visible ? 'true' : 'false');
                }
            }
        })(LegendComponent || (LegendComponent = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return LegendComponent;
    });
    _registerModule(_modules, 'Accessibility/Components/SeriesComponent/SeriesDescriber.js', [_modules['Accessibility/Components/AnnotationsA11y.js'], _modules['Accessibility/Utils/ChartUtilities.js'], _modules['Core/FormatUtilities.js'], _modules['Accessibility/Utils/HTMLUtilities.js'], _modules['Core/Utilities.js']], function (AnnotationsA11y, ChartUtilities, F, HTMLUtilities, U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Place desriptions on a series and its points.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var getPointAnnotationTexts = AnnotationsA11y.getPointAnnotationTexts;
        var getAxisDescription = ChartUtilities.getAxisDescription,
            getSeriesFirstPointElement = ChartUtilities.getSeriesFirstPointElement,
            getSeriesA11yElement = ChartUtilities.getSeriesA11yElement,
            unhideChartElementFromAT = ChartUtilities.unhideChartElementFromAT;
        var format = F.format,
            numberFormat = F.numberFormat;
        var reverseChildNodes = HTMLUtilities.reverseChildNodes,
            stripHTMLTags = HTMLUtilities.stripHTMLTagsFromString;
        var find = U.find,
            isNumber = U.isNumber,
            pick = U.pick,
            defined = U.defined;
        /* *
         *
         *  Functions
         *
         * */
        /* eslint-disable valid-jsdoc */
        /**
         * @private
         */
        function findFirstPointWithGraphic(point) {
            var sourcePointIndex = point.index;
            if (!point.series || !point.series.data || !defined(sourcePointIndex)) {
                return null;
            }
            return find(point.series.data, function (p) {
                return !!(p &&
                    typeof p.index !== 'undefined' &&
                    p.index > sourcePointIndex &&
                    p.graphic &&
                    p.graphic.element);
            }) || null;
        }
        /**
         * Whether or not we should add a mock point element in
         * order to describe a point that has no graphic.
         * @private
         */
        function shouldAddMockPoint(point) {
            // Note: Sunburst series use isNull for hidden points on drilldown.
            // Ignore these.
            var series = point.series,
                chart = series && series.chart,
                isSunburst = series && series.is('sunburst'),
                isNull = point.isNull,
                shouldDescribeNull = chart &&
                    chart
                        .options.accessibility.point.describeNull;
            return isNull && !isSunburst && shouldDescribeNull;
        }
        /**
         * @private
         */
        function makeMockElement(point, pos) {
            var renderer = point.series.chart.renderer,
                mock = renderer.rect(pos.x,
                pos.y, 1, 1);
            mock.attr({
                'class': 'highcharts-a11y-mock-point',
                fill: 'none',
                opacity: 0,
                'fill-opacity': 0,
                'stroke-opacity': 0
            });
            return mock;
        }
        /**
         * @private
         */
        function addMockPointElement(point) {
            var series = point.series,
                firstPointWithGraphic = findFirstPointWithGraphic(point),
                firstGraphic = firstPointWithGraphic && firstPointWithGraphic.graphic,
                parentGroup = firstGraphic ?
                    firstGraphic.parentGroup :
                    series.graph || series.group,
                mockPos = firstPointWithGraphic ? {
                    x: pick(point.plotX,
                firstPointWithGraphic.plotX, 0),
                    y: pick(point.plotY,
                firstPointWithGraphic.plotY, 0)
                } : {
                    x: pick(point.plotX, 0),
                    y: pick(point.plotY, 0)
                },
                mockElement = makeMockElement(point,
                mockPos);
            if (parentGroup && parentGroup.element) {
                point.graphic = mockElement;
                point.hasMockGraphic = true;
                mockElement.add(parentGroup);
                // Move to correct pos in DOM
                parentGroup.element.insertBefore(mockElement.element, firstGraphic ? firstGraphic.element : null);
                return mockElement.element;
            }
        }
        /**
         * @private
         */
        function hasMorePointsThanDescriptionThreshold(series) {
            var chartA11yOptions = series.chart.options.accessibility,
                threshold = (chartA11yOptions.series.pointDescriptionEnabledThreshold);
            return !!(threshold !== false &&
                series.points &&
                series.points.length >= threshold);
        }
        /**
         * @private
         */
        function shouldSetScreenReaderPropsOnPoints(series) {
            var seriesA11yOptions = series.options.accessibility || {};
            return !hasMorePointsThanDescriptionThreshold(series) &&
                !seriesA11yOptions.exposeAsGroupOnly;
        }
        /**
         * @private
         */
        function shouldSetKeyboardNavPropsOnPoints(series) {
            var chartA11yOptions = series.chart.options.accessibility,
                seriesNavOptions = chartA11yOptions.keyboardNavigation.seriesNavigation;
            return !!(series.points && (series.points.length <
                seriesNavOptions.pointNavigationEnabledThreshold ||
                seriesNavOptions.pointNavigationEnabledThreshold === false));
        }
        /**
         * @private
         */
        function shouldDescribeSeriesElement(series) {
            var chart = series.chart,
                chartOptions = chart.options.chart,
                chartHas3d = chartOptions.options3d && chartOptions.options3d.enabled,
                hasMultipleSeries = chart.series.length > 1,
                describeSingleSeriesOption = chart.options.accessibility.series.describeSingleSeries,
                exposeAsGroupOnlyOption = (series.options.accessibility || {}).exposeAsGroupOnly,
                noDescribe3D = chartHas3d && hasMultipleSeries;
            return !noDescribe3D && (hasMultipleSeries || describeSingleSeriesOption ||
                exposeAsGroupOnlyOption || hasMorePointsThanDescriptionThreshold(series));
        }
        /**
         * @private
         */
        function pointNumberToString(point, value) {
            var series = point.series,
                chart = series.chart,
                a11yPointOptions = chart.options.accessibility.point || {},
                seriesA11yPointOptions = series.options.accessibility &&
                    series.options.accessibility.point || {},
                tooltipOptions = series.tooltipOptions || {},
                lang = chart.options.lang;
            if (isNumber(value)) {
                return numberFormat(value, seriesA11yPointOptions.valueDecimals ||
                    a11yPointOptions.valueDecimals ||
                    tooltipOptions.valueDecimals ||
                    -1, lang.decimalPoint, lang.accessibility.thousandsSep || lang.thousandsSep);
            }
            return value;
        }
        /**
         * @private
         */
        function getSeriesDescriptionText(series) {
            var seriesA11yOptions = series.options.accessibility || {},
                descOpt = seriesA11yOptions.description;
            return descOpt && series.chart.langFormat('accessibility.series.description', {
                description: descOpt,
                series: series
            }) || '';
        }
        /**
         * @private
         */
        function getSeriesAxisDescriptionText(series, axisCollection) {
            var axis = series[axisCollection];
            return series.chart.langFormat('accessibility.series.' + axisCollection + 'Description', {
                name: getAxisDescription(axis),
                series: series
            });
        }
        /**
         * Get accessible time description for a point on a datetime axis.
         *
         * @private
         */
        function getPointA11yTimeDescription(point) {
            var series = point.series,
                chart = series.chart,
                seriesA11yOptions = series.options.accessibility &&
                    series.options.accessibility.point || {},
                a11yOptions = chart.options.accessibility.point || {},
                dateXAxis = series.xAxis && series.xAxis.dateTime;
            if (dateXAxis) {
                var tooltipDateFormat = dateXAxis.getXDateFormat(point.x || 0,
                    chart.options.tooltip.dateTimeLabelFormats),
                    dateFormat = seriesA11yOptions.dateFormatter &&
                        seriesA11yOptions.dateFormatter(point) ||
                        a11yOptions.dateFormatter && a11yOptions.dateFormatter(point) ||
                        seriesA11yOptions.dateFormat ||
                        a11yOptions.dateFormat ||
                        tooltipDateFormat;
                return chart.time.dateFormat(dateFormat, point.x || 0, void 0);
            }
        }
        /**
         * @private
         */
        function getPointXDescription(point) {
            var timeDesc = getPointA11yTimeDescription(point), xAxis = point.series.xAxis || {}, pointCategory = xAxis.categories && defined(point.category) &&
                    ('' + point.category).replace('<br/>', ' '), canUseId = defined(point.id) &&
                    ('' + point.id).indexOf('highcharts-') < 0, fallback = 'x, ' + point.x;
            return point.name || timeDesc || pointCategory ||
                (canUseId ? point.id : fallback);
        }
        /**
         * @private
         */
        function getPointArrayMapValueDescription(point, prefix, suffix) {
            var pre = prefix || '', suf = suffix || '', keyToValStr = function (key) {
                    var num = pointNumberToString(point, pick(point[key], point.options[key]));
                return key + ': ' + pre + num + suf;
            }, pointArrayMap = point.series.pointArrayMap;
            return pointArrayMap.reduce(function (desc, key) {
                return desc + (desc.length ? ', ' : '') + keyToValStr(key);
            }, '');
        }
        /**
         * @private
         */
        function getPointValue(point) {
            var series = point.series,
                a11yPointOpts = series.chart.options.accessibility.point || {},
                seriesA11yPointOpts = series.chart.options.accessibility &&
                    series.chart.options.accessibility.point || {},
                tooltipOptions = series.tooltipOptions || {},
                valuePrefix = seriesA11yPointOpts.valuePrefix ||
                    a11yPointOpts.valuePrefix ||
                    tooltipOptions.valuePrefix ||
                    '',
                valueSuffix = seriesA11yPointOpts.valueSuffix ||
                    a11yPointOpts.valueSuffix ||
                    tooltipOptions.valueSuffix ||
                    '',
                fallbackKey = (typeof point.value !==
                    'undefined' ?
                    'value' : 'y'),
                fallbackDesc = pointNumberToString(point,
                point[fallbackKey]);
            if (point.isNull) {
                return series.chart.langFormat('accessibility.series.nullPointValue', {
                    point: point
                });
            }
            if (series.pointArrayMap) {
                return getPointArrayMapValueDescription(point, valuePrefix, valueSuffix);
            }
            return valuePrefix + fallbackDesc + valueSuffix;
        }
        /**
         * Return the description for the annotation(s) connected to a point, or
         * empty string if none.
         *
         * @private
         * @param {Highcharts.Point} point
         * The data point to get the annotation info from.
         * @return {string}
         * Annotation description
         */
        function getPointAnnotationDescription(point) {
            var chart = point.series.chart;
            var langKey = 'accessibility.series.pointAnnotationsDescription';
            var annotations = getPointAnnotationTexts(point);
            var context = { point: point,
                annotations: annotations };
            return annotations.length ? chart.langFormat(langKey, context) : '';
        }
        /**
         * Return string with information about point.
         * @private
         */
        function getPointValueDescription(point) {
            var series = point.series, chart = series.chart, seriesA11yOptions = series.options.accessibility, seriesValueDescFormat = seriesA11yOptions && seriesA11yOptions.point &&
                    seriesA11yOptions.point.valueDescriptionFormat, pointValueDescriptionFormat = seriesValueDescFormat ||
                    chart.options.accessibility.point.valueDescriptionFormat, showXDescription = pick(series.xAxis &&
                    series.xAxis.options.accessibility &&
                    series.xAxis.options.accessibility.enabled, !chart.angular), xDesc = showXDescription ? getPointXDescription(point) : '', context = {
                    point: point,
                    index: defined(point.index) ? (point.index + 1) : '',
                    xDescription: xDesc,
                    value: getPointValue(point),
                    separator: showXDescription ? ', ' : ''
                };
            return format(pointValueDescriptionFormat, context, chart);
        }
        /**
         * Return string with information about point.
         * @private
         */
        function defaultPointDescriptionFormatter(point) {
            var series = point.series, shouldExposeSeriesName = series.chart.series.length > 1 ||
                    series.options.name, valText = getPointValueDescription(point), description = point.options && point.options.accessibility &&
                    point.options.accessibility.description, userDescText = description ? ' ' + description : '', seriesNameText = shouldExposeSeriesName ? ' ' + series.name + '.' : '', annotationsDesc = getPointAnnotationDescription(point), pointAnnotationsText = annotationsDesc ? ' ' + annotationsDesc : '';
            point.accessibility = point.accessibility || {};
            point.accessibility.valueDescription = valText;
            return valText + userDescText + seriesNameText + pointAnnotationsText;
        }
        /**
         * Set a11y props on a point element
         * @private
         * @param {Highcharts.Point} point
         * @param {Highcharts.HTMLDOMElement|Highcharts.SVGDOMElement} pointElement
         */
        function setPointScreenReaderAttribs(point, pointElement) {
            var series = point.series,
                a11yPointOptions = series.chart.options.accessibility.point || {},
                seriesPointA11yOptions = series.options.accessibility &&
                    series.options.accessibility.point || {},
                label = stripHTMLTags(seriesPointA11yOptions.descriptionFormatter &&
                    seriesPointA11yOptions.descriptionFormatter(point) ||
                    a11yPointOptions.descriptionFormatter &&
                        a11yPointOptions.descriptionFormatter(point) ||
                    defaultPointDescriptionFormatter(point));
            pointElement.setAttribute('role', 'img');
            pointElement.setAttribute('aria-label', label);
        }
        /**
         * Add accessible info to individual point elements of a series
         * @private
         * @param {Highcharts.Series} series
         */
        function describePointsInSeries(series) {
            var setScreenReaderProps = shouldSetScreenReaderPropsOnPoints(series),
                setKeyboardProps = shouldSetKeyboardNavPropsOnPoints(series),
                shouldDescribeNullPoints = series.chart.options.accessibility
                    .point.describeNull;
            if (setScreenReaderProps || setKeyboardProps) {
                series.points.forEach(function (point) {
                    var pointEl = point.graphic && point.graphic.element ||
                            shouldAddMockPoint(point) && addMockPointElement(point),
                        pointA11yDisabled = (point.options &&
                            point.options.accessibility &&
                            point.options.accessibility.enabled === false);
                    if (pointEl) {
                        if (point.isNull && !shouldDescribeNullPoints) {
                            pointEl.setAttribute('aria-hidden', true);
                            return;
                        }
                        // We always set tabindex, as long as we are setting props.
                        // When setting tabindex, also remove default outline to
                        // avoid ugly border on click.
                        pointEl.setAttribute('tabindex', '-1');
                        if (!series.chart.styledMode) {
                            pointEl.style.outline = 'none';
                        }
                        if (setScreenReaderProps && !pointA11yDisabled) {
                            setPointScreenReaderAttribs(point, pointEl);
                        }
                        else {
                            pointEl.setAttribute('aria-hidden', true);
                        }
                    }
                });
            }
        }
        /**
         * Return string with information about series.
         * @private
         */
        function defaultSeriesDescriptionFormatter(series) {
            var chart = series.chart,
                chartTypes = chart.types || [],
                description = getSeriesDescriptionText(series),
                shouldDescribeAxis = function (coll) {
                    return chart[coll] && chart[coll].length > 1 && series[coll];
            }, seriesNumber = series.index + 1, xAxisInfo = getSeriesAxisDescriptionText(series, 'xAxis'), yAxisInfo = getSeriesAxisDescriptionText(series, 'yAxis'), summaryContext = {
                seriesNumber: seriesNumber,
                series: series,
                chart: chart
            }, combinationSuffix = chartTypes.length > 1 ? 'Combination' : '', summary = chart.langFormat('accessibility.series.summary.' + series.type + combinationSuffix, summaryContext) || chart.langFormat('accessibility.series.summary.default' + combinationSuffix, summaryContext), axisDescription = (shouldDescribeAxis('yAxis') ? ' ' + yAxisInfo + '.' : '') + (shouldDescribeAxis('xAxis') ? ' ' + xAxisInfo + '.' : ''), formatStr = chart.options.accessibility.series.descriptionFormat || '';
            return format(formatStr, {
                seriesDescription: summary,
                authorDescription: (description ? ' ' + description : ''),
                axisDescription: axisDescription,
                series: series,
                chart: chart,
                seriesNumber: seriesNumber
            }, void 0);
        }
        /**
         * Set a11y props on a series element
         * @private
         * @param {Highcharts.Series} series
         * @param {Highcharts.HTMLDOMElement|Highcharts.SVGDOMElement} seriesElement
         */
        function describeSeriesElement(series, seriesElement) {
            var seriesA11yOptions = series.options.accessibility || {},
                a11yOptions = series.chart.options.accessibility,
                landmarkVerbosity = a11yOptions.landmarkVerbosity;
            // Handle role attribute
            if (seriesA11yOptions.exposeAsGroupOnly) {
                seriesElement.setAttribute('role', 'img');
            }
            else if (landmarkVerbosity === 'all') {
                seriesElement.setAttribute('role', 'region');
            }
            else {
                seriesElement.setAttribute('role', 'group');
            }
            seriesElement.setAttribute('tabindex', '-1');
            if (!series.chart.styledMode) {
                // Don't show browser outline on click, despite tabindex
                seriesElement.style.outline = 'none';
            }
            seriesElement.setAttribute('aria-label', stripHTMLTags(a11yOptions.series.descriptionFormatter &&
                a11yOptions.series.descriptionFormatter(series) ||
                defaultSeriesDescriptionFormatter(series)));
        }
        /**
         * Put accessible info on series and points of a series.
         * @param {Highcharts.Series} series The series to add info on.
         */
        function describeSeries(series) {
            var chart = series.chart,
                firstPointEl = getSeriesFirstPointElement(series),
                seriesEl = getSeriesA11yElement(series),
                is3d = chart.is3d && chart.is3d();
            if (seriesEl) {
                // For some series types the order of elements do not match the
                // order of points in series. In that case we have to reverse them
                // in order for AT to read them out in an understandable order.
                // Due to z-index issues we cannot do this for 3D charts.
                if (seriesEl.lastChild === firstPointEl && !is3d) {
                    reverseChildNodes(seriesEl);
                }
                describePointsInSeries(series);
                unhideChartElementFromAT(chart, seriesEl);
                if (shouldDescribeSeriesElement(series)) {
                    describeSeriesElement(series, seriesEl);
                }
                else {
                    seriesEl.removeAttribute('aria-label');
                }
            }
        }
        /* *
         *
         *  Default Export
         *
         * */
        var SeriesDescriber = {
                defaultPointDescriptionFormatter: defaultPointDescriptionFormatter,
                defaultSeriesDescriptionFormatter: defaultSeriesDescriptionFormatter,
                describeSeries: describeSeries
            };

        return SeriesDescriber;
    });
    _registerModule(_modules, 'Accessibility/Components/SeriesComponent/NewDataAnnouncer.js', [_modules['Core/Globals.js'], _modules['Core/Utilities.js'], _modules['Accessibility/Utils/Announcer.js'], _modules['Accessibility/Utils/ChartUtilities.js'], _modules['Accessibility/Utils/EventProvider.js'], _modules['Accessibility/Components/SeriesComponent/SeriesDescriber.js']], function (H, U, Announcer, ChartUtilities, EventProvider, SeriesDescriber) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Handle announcing new data for a chart.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var addEvent = U.addEvent,
            defined = U.defined;
        var getChartTitle = ChartUtilities.getChartTitle;
        var defaultPointDescriptionFormatter = SeriesDescriber.defaultPointDescriptionFormatter,
            defaultSeriesDescriptionFormatter = SeriesDescriber.defaultSeriesDescriptionFormatter;
        /* *
         *
         *  Functions
         *
         * */
        /* eslint-disable valid-jsdoc */
        /**
         * @private
         */
        function chartHasAnnounceEnabled(chart) {
            return !!chart.options.accessibility.announceNewData.enabled;
        }
        /**
         * @private
         */
        function findPointInDataArray(point) {
            var candidates = point.series.data.filter(function (candidate) { return (point.x === candidate.x && point.y === candidate.y); });
            return candidates.length === 1 ? candidates[0] : point;
        }
        /**
         * Get array of unique series from two arrays
         * @private
         */
        function getUniqueSeries(arrayA, arrayB) {
            var uniqueSeries = (arrayA || []).concat(arrayB || []).reduce(function (acc,
                cur) {
                    acc[cur.name + cur.index] = cur;
                return acc;
            }, {});
            return Object
                .keys(uniqueSeries)
                .map(function (ix) { return uniqueSeries[ix]; });
        }
        /* *
         *
         *  Class
         *
         * */
        /**
         * @private
         * @class
         */
        var NewDataAnnouncer = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function NewDataAnnouncer(chart) {
                    /* *
                     *
                     *  Public
                     *
                     * */
                    this.announcer = void 0;
                this.dirty = {
                    allSeries: {}
                };
                this.eventProvider = void 0;
                this.lastAnnouncementTime = 0;
                this.chart = chart;
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Initialize the new data announcer.
             * @private
             */
            NewDataAnnouncer.prototype.init = function () {
                var chart = this.chart;
                var announceOptions = (chart.options.accessibility.announceNewData);
                var announceType = announceOptions.interruptUser ?
                        'assertive' : 'polite';
                this.lastAnnouncementTime = 0;
                this.dirty = {
                    allSeries: {}
                };
                this.eventProvider = new EventProvider();
                this.announcer = new Announcer(chart, announceType);
                this.addEventListeners();
            };
            /**
             * Remove traces of announcer.
             * @private
             */
            NewDataAnnouncer.prototype.destroy = function () {
                this.eventProvider.removeAddedEvents();
                this.announcer.destroy();
            };
            /**
             * Add event listeners for the announcer
             * @private
             */
            NewDataAnnouncer.prototype.addEventListeners = function () {
                var announcer = this,
                    chart = this.chart,
                    e = this.eventProvider;
                e.addEvent(chart, 'afterApplyDrilldown', function () {
                    announcer.lastAnnouncementTime = 0;
                });
                e.addEvent(chart, 'afterAddSeries', function (e) {
                    announcer.onSeriesAdded(e.series);
                });
                e.addEvent(chart, 'redraw', function () {
                    announcer.announceDirtyData();
                });
            };
            /**
             * On new data series added, update dirty list.
             * @private
             * @param {Highcharts.Series} series
             */
            NewDataAnnouncer.prototype.onSeriesAdded = function (series) {
                if (chartHasAnnounceEnabled(this.chart)) {
                    this.dirty.hasDirty = true;
                    this.dirty.allSeries[series.name + series.index] = series;
                    // Add it to newSeries storage unless we already have one
                    this.dirty.newSeries = defined(this.dirty.newSeries) ?
                        void 0 : series;
                }
            };
            /**
             * Gather what we know and announce the data to user.
             * @private
             */
            NewDataAnnouncer.prototype.announceDirtyData = function () {
                var chart = this.chart,
                    announcer = this;
                if (chart.options.accessibility.announceNewData &&
                    this.dirty.hasDirty) {
                    var newPoint = this.dirty.newPoint;
                    // If we have a single new point, see if we can find it in the
                    // data array. Otherwise we can only pass through options to
                    // the description builder, and it is a bit sparse in info.
                    if (newPoint) {
                        newPoint = findPointInDataArray(newPoint);
                    }
                    this.queueAnnouncement(Object
                        .keys(this.dirty.allSeries)
                        .map(function (ix) {
                        return announcer.dirty.allSeries[ix];
                    }), this.dirty.newSeries, newPoint);
                    // Reset
                    this.dirty = {
                        allSeries: {}
                    };
                }
            };
            /**
             * Announce to user that there is new data.
             * @private
             * @param {Array<Highcharts.Series>} dirtySeries
             *          Array of series with new data.
             * @param {Highcharts.Series} [newSeries]
             *          If a single new series was added, a reference to this series.
             * @param {Highcharts.Point} [newPoint]
             *          If a single point was added, a reference to this point.
             */
            NewDataAnnouncer.prototype.queueAnnouncement = function (dirtySeries, newSeries, newPoint) {
                var _this = this;
                var chart = this.chart;
                var annOptions = chart.options.accessibility.announceNewData;
                if (annOptions.enabled) {
                    var now = +new Date();
                    var dTime = now - this.lastAnnouncementTime;
                    var time = Math.max(0,
                        annOptions.minAnnounceInterval - dTime);
                    // Add series from previously queued announcement.
                    var allSeries = getUniqueSeries(this.queuedAnnouncement && this.queuedAnnouncement.series,
                        dirtySeries);
                    // Build message and announce
                    var message = this.buildAnnouncementMessage(allSeries,
                        newSeries,
                        newPoint);
                    if (message) {
                        // Is there already one queued?
                        if (this.queuedAnnouncement) {
                            clearTimeout(this.queuedAnnouncementTimer);
                        }
                        // Build the announcement
                        this.queuedAnnouncement = {
                            time: now,
                            message: message,
                            series: allSeries
                        };
                        // Queue the announcement
                        this.queuedAnnouncementTimer = setTimeout(function () {
                            if (_this && _this.announcer) {
                                _this.lastAnnouncementTime = +new Date();
                                _this.announcer.announce(_this.queuedAnnouncement.message);
                                delete _this.queuedAnnouncement;
                                delete _this.queuedAnnouncementTimer;
                            }
                        }, time);
                    }
                }
            };
            /**
             * Get announcement message for new data.
             * @private
             * @param {Array<Highcharts.Series>} dirtySeries
             *          Array of series with new data.
             * @param {Highcharts.Series} [newSeries]
             *          If a single new series was added, a reference to this series.
             * @param {Highcharts.Point} [newPoint]
             *          If a single point was added, a reference to this point.
             *
             * @return {string|null}
             * The announcement message to give to user.
             */
            NewDataAnnouncer.prototype.buildAnnouncementMessage = function (dirtySeries, newSeries, newPoint) {
                var chart = this.chart,
                    annOptions = chart.options.accessibility.announceNewData;
                // User supplied formatter?
                if (annOptions.announcementFormatter) {
                    var formatterRes = annOptions.announcementFormatter(dirtySeries,
                        newSeries,
                        newPoint);
                    if (formatterRes !== false) {
                        return formatterRes.length ? formatterRes : null;
                    }
                }
                // Default formatter - use lang options
                var multiple = H.charts && H.charts.length > 1 ?
                        'Multiple' : 'Single', langKey = newSeries ? 'newSeriesAnnounce' + multiple :
                        newPoint ? 'newPointAnnounce' + multiple : 'newDataAnnounce', chartTitle = getChartTitle(chart);
                return chart.langFormat('accessibility.announceNewData.' + langKey, {
                    chartTitle: chartTitle,
                    seriesDesc: newSeries ?
                        defaultSeriesDescriptionFormatter(newSeries) :
                        null,
                    pointDesc: newPoint ?
                        defaultPointDescriptionFormatter(newPoint) :
                        null,
                    point: newPoint,
                    series: newSeries
                });
            };
            return NewDataAnnouncer;
        }());
        /* *
         *
         *  Class Namespace
         *
         * */
        (function (NewDataAnnouncer) {
            /* *
             *
             *  Declarations
             *
             * */
            /* *
             *
             *  Static Properties
             *
             * */
            NewDataAnnouncer.composedClasses = [];
            /* *
             *
             *  Static Functions
             *
             * */
            /**
             * @private
             */
            function compose(SeriesClass) {
                if (NewDataAnnouncer.composedClasses.indexOf(SeriesClass) === -1) {
                    NewDataAnnouncer.composedClasses.push(SeriesClass);
                    addEvent(SeriesClass, 'addPoint', seriesOnAddPoint);
                    addEvent(SeriesClass, 'updatedData', seriesOnUpdatedData);
                }
            }
            NewDataAnnouncer.compose = compose;
            /**
             * On new point added, update dirty list.
             * @private
             * @param {Highcharts.Point} point
             */
            function seriesOnAddPoint(e) {
                var chart = this.chart,
                    newDataAnnouncer = this.newDataAnnouncer;
                if (newDataAnnouncer &&
                    newDataAnnouncer.chart === chart &&
                    chartHasAnnounceEnabled(chart)) {
                    // Add it to newPoint storage unless we already have one
                    newDataAnnouncer.dirty.newPoint = (defined(newDataAnnouncer.dirty.newPoint) ?
                        void 0 :
                        e.point);
                }
            }
            /**
             * On new data in the series, make sure we add it to the dirty list.
             * @private
             * @param {Highcharts.Series} series
             */
            function seriesOnUpdatedData() {
                var chart = this.chart,
                    newDataAnnouncer = this.newDataAnnouncer;
                if (newDataAnnouncer &&
                    newDataAnnouncer.chart === chart &&
                    chartHasAnnounceEnabled(chart)) {
                    newDataAnnouncer.dirty.hasDirty = true;
                    newDataAnnouncer.dirty.allSeries[this.name + this.index] = this;
                }
            }
        })(NewDataAnnouncer || (NewDataAnnouncer = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return NewDataAnnouncer;
    });
    _registerModule(_modules, 'Accessibility/ProxyElement.js', [_modules['Core/Globals.js'], _modules['Core/Utilities.js'], _modules['Accessibility/Utils/EventProvider.js'], _modules['Accessibility/Utils/ChartUtilities.js'], _modules['Accessibility/Utils/HTMLUtilities.js']], function (H, U, EventProvider, ChartUtilities, HTMLUtilities) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Proxy elements are used to shadow SVG elements in HTML for assistive
         *  technology, such as screen readers or voice input software.
         *
         *  The ProxyElement class represents such an element, and deals with
         *  overlay positioning and mirroring events for the target.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var doc = H.doc;
        var attr = U.attr,
            css = U.css,
            merge = U.merge;
        var fireEventOnWrappedOrUnwrappedElement = ChartUtilities.fireEventOnWrappedOrUnwrappedElement;
        var cloneMouseEvent = HTMLUtilities.cloneMouseEvent,
            cloneTouchEvent = HTMLUtilities.cloneTouchEvent,
            getFakeMouseEvent = HTMLUtilities.getFakeMouseEvent,
            removeElement = HTMLUtilities.removeElement;
        /* *
         *
         *  Class
         *
         * */
        /**
         * Represents a proxy element that overlays a target and relays events
         * to its target.
         *
         * @private
         * @class
         */
        var ProxyElement = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function ProxyElement(chart, target, groupType, attributes) {
                    this.chart = chart;
                this.target = target;
                this.groupType = groupType;
                var isListItem = groupType === 'ul';
                this.eventProvider = new EventProvider();
                var wrapperEl = isListItem ? doc.createElement('li') : null;
                var btnEl = this.buttonElement = doc.createElement('button');
                if (!chart.styledMode) {
                    this.hideButtonVisually(btnEl);
                }
                if (wrapperEl) {
                    if (isListItem && !chart.styledMode) {
                        wrapperEl.style.listStyle = 'none';
                    }
                    wrapperEl.appendChild(btnEl);
                    this.element = wrapperEl;
                }
                else {
                    this.element = btnEl;
                }
                this.updateTarget(target, attributes);
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Fake a click event on the target.
             */
            ProxyElement.prototype.click = function () {
                var pos = this.getTargetPosition();
                pos.x += pos.width / 2;
                pos.y += pos.height / 2;
                var fakeEventObject = getFakeMouseEvent('click',
                    pos);
                fireEventOnWrappedOrUnwrappedElement(this.target.click, fakeEventObject);
            };
            /**
             * Update the target to be proxied. The position and events are updated to
             * match the new target.
             * @param target The new target definition
             * @param attributes New HTML attributes to apply to the button. Set an
             * attribute to null to remove.
             */
            ProxyElement.prototype.updateTarget = function (target, attributes) {
                this.target = target;
                this.updateCSSClassName();
                var attrs = attributes || {};
                Object.keys(attrs).forEach(function (a) {
                    if (attrs[a] === null) {
                        delete attrs[a];
                    }
                });
                attr(this.buttonElement, merge({
                    'aria-label': this.getTargetAttr(target.click, 'aria-label')
                }, attrs));
                this.eventProvider.removeAddedEvents();
                this.addProxyEventsToButton(this.buttonElement, target.click);
                this.refreshPosition();
            };
            /**
             * Refresh the position of the proxy element to match the current target
             */
            ProxyElement.prototype.refreshPosition = function () {
                var bBox = this.getTargetPosition();
                css(this.buttonElement, {
                    width: (bBox.width || 1) + 'px',
                    height: (bBox.height || 1) + 'px',
                    left: (Math.round(bBox.x) || 0) + 'px',
                    top: (Math.round(bBox.y) || 0) + 'px'
                });
            };
            /**
             * Remove button from DOM, and clear events.
             */
            ProxyElement.prototype.remove = function () {
                this.eventProvider.removeAddedEvents();
                removeElement(this.element);
            };
            // -------------------------- private ------------------------------------
            /**
             * Update the CSS class name to match target
             */
            ProxyElement.prototype.updateCSSClassName = function () {
                var stringHasNoTooltip = function (s) { return (s.indexOf('highcharts-no-tooltip') > -1); };
                var legend = this.chart.legend;
                var groupDiv = legend.group && legend.group.div;
                var noTooltipOnGroup = stringHasNoTooltip(groupDiv && groupDiv.className || '');
                var targetClassName = this.getTargetAttr(this.target.click, 'class') || '';
                var noTooltipOnTarget = stringHasNoTooltip(targetClassName);
                this.buttonElement.className = noTooltipOnGroup || noTooltipOnTarget ?
                    'highcharts-a11y-proxy-button highcharts-no-tooltip' :
                    'highcharts-a11y-proxy-button';
            };
            /**
             * Mirror events for a proxy button to a target
             */
            ProxyElement.prototype.addProxyEventsToButton = function (button, target) {
                var _this = this;
                [
                    'click', 'touchstart', 'touchend', 'touchcancel', 'touchmove',
                    'mouseover', 'mouseenter', 'mouseleave', 'mouseout'
                ].forEach(function (evtType) {
                    var isTouchEvent = evtType.indexOf('touch') === 0;
                    _this.eventProvider.addEvent(button, evtType, function (e) {
                        var clonedEvent = isTouchEvent ?
                                cloneTouchEvent(e) :
                                cloneMouseEvent(e);
                        if (target) {
                            fireEventOnWrappedOrUnwrappedElement(target, clonedEvent);
                        }
                        e.stopPropagation();
                        // #9682, #15318: Touch scrolling didnt work when touching
                        // proxy
                        if (!isTouchEvent) {
                            e.preventDefault();
                        }
                    }, { passive: false });
                });
            };
            /**
             * Set visually hidden style on a proxy button
             */
            ProxyElement.prototype.hideButtonVisually = function (button) {
                css(button, {
                    borderWidth: 0,
                    backgroundColor: 'transparent',
                    cursor: 'pointer',
                    outline: 'none',
                    opacity: 0.001,
                    filter: 'alpha(opacity=1)',
                    zIndex: 999,
                    overflow: 'hidden',
                    padding: 0,
                    margin: 0,
                    display: 'block',
                    position: 'absolute',
                    '-ms-filter': 'progid:DXImageTransform.Microsoft.Alpha(Opacity=1)'
                });
            };
            /**
             * Get the position relative to chart container for the target
             */
            ProxyElement.prototype.getTargetPosition = function () {
                var clickTarget = this.target.click;
                // We accept both DOM elements and wrapped elements as click targets.
                var clickTargetElement = clickTarget.element ?
                        clickTarget.element :
                        clickTarget;
                var posElement = this.target.visual || clickTargetElement;
                var chartDiv = this.chart.renderTo;
                if (chartDiv && posElement && posElement.getBoundingClientRect) {
                    var rectEl = posElement.getBoundingClientRect(),
                        chartPos = this.chart.pointer.getChartPosition();
                    return {
                        x: (rectEl.left - chartPos.left) / chartPos.scaleX,
                        y: (rectEl.top - chartPos.top) / chartPos.scaleY,
                        width: rectEl.right / chartPos.scaleX -
                            rectEl.left / chartPos.scaleX,
                        height: rectEl.bottom / chartPos.scaleY -
                            rectEl.top / chartPos.scaleY
                    };
                }
                return { x: 0, y: 0, width: 1, height: 1 };
            };
            /**
             * Get an attribute value of a target
             */
            ProxyElement.prototype.getTargetAttr = function (target, key) {
                if (target.element) {
                    return target.element.getAttribute(key);
                }
                return target.getAttribute(key);
            };
            return ProxyElement;
        }());
        /* *
         *
         *  Default Export
         *
         * */

        return ProxyElement;
    });
    _registerModule(_modules, 'Accessibility/ProxyProvider.js', [_modules['Core/Globals.js'], _modules['Core/Utilities.js'], _modules['Accessibility/Utils/ChartUtilities.js'], _modules['Accessibility/Utils/DOMElementProvider.js'], _modules['Accessibility/Utils/HTMLUtilities.js'], _modules['Accessibility/ProxyElement.js']], function (H, U, CU, DOMElementProvider, HU, ProxyElement) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Proxy elements are used to shadow SVG elements in HTML for assistive
         *  technology, such as screen readers or voice input software.
         *
         *  The ProxyProvider keeps track of all proxy elements of the a11y module,
         *  and updating their order and positioning.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var doc = H.doc;
        var attr = U.attr,
            css = U.css;
        var unhideChartElementFromAT = CU.unhideChartElementFromAT;
        var removeElement = HU.removeElement,
            removeChildNodes = HU.removeChildNodes;
        /* *
         *
         *  Class
         *
         * */
        /**
         * Keeps track of all proxy elements and proxy groups.
         *
         * @private
         * @class
         */
        var ProxyProvider = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function ProxyProvider(chart) {
                    this.chart = chart;
                this.domElementProvider = new DOMElementProvider();
                this.groups = {};
                this.groupOrder = [];
                this.beforeChartProxyPosContainer = this.createProxyPosContainer('before');
                this.afterChartProxyPosContainer = this.createProxyPosContainer('after');
                this.update();
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable */
            /**
             * Add a new proxy element to a group, proxying a target control.
             */
            ProxyProvider.prototype.addProxyElement = function (groupKey, target, attributes) {
                var group = this.groups[groupKey];
                if (!group) {
                    throw new Error('ProxyProvider.addProxyElement: Invalid group key ' + groupKey);
                }
                var proxy = new ProxyElement(this.chart,
                    target,
                    group.type,
                    attributes);
                group.proxyContainerElement.appendChild(proxy.element);
                group.proxyElements.push(proxy);
                return proxy;
            };
            /**
             * Create a group that will contain proxy elements. The group order is
             * automatically updated according to the last group order keys.
             *
             * Returns the added group.
             */
            ProxyProvider.prototype.addGroup = function (groupKey, groupType, attributes) {
                var existingGroup = this.groups[groupKey];
                if (existingGroup) {
                    return existingGroup.groupElement;
                }
                var proxyContainer = this.domElementProvider.createElement(groupType);
                // If we want to add a role to the group, and still use e.g.
                // a list group, we need a wrapper div.
                var groupElement;
                if (attributes && attributes.role && groupType !== 'div') {
                    groupElement = this.domElementProvider.createElement('div');
                    groupElement.appendChild(proxyContainer);
                }
                else {
                    groupElement = proxyContainer;
                }
                groupElement.className = 'highcharts-a11y-proxy-group highcharts-a11y-proxy-group-' +
                    groupKey.replace(/\W/g, '-');
                this.groups[groupKey] = {
                    proxyContainerElement: proxyContainer,
                    groupElement: groupElement,
                    type: groupType,
                    proxyElements: []
                };
                attr(groupElement, attributes || {});
                if (groupType === 'ul') {
                    proxyContainer.setAttribute('role', 'list'); // Needed for webkit
                }
                // Add the group to the end by default, and perhaps then we
                // won't have to reorder the whole set of groups.
                this.afterChartProxyPosContainer.appendChild(groupElement);
                this.updateGroupOrder(this.groupOrder);
                return groupElement;
            };
            /**
             * Update HTML attributes of a group.
             */
            ProxyProvider.prototype.updateGroupAttrs = function (groupKey, attributes) {
                var group = this.groups[groupKey];
                if (!group) {
                    throw new Error('ProxyProvider.updateGroupAttrs: Invalid group key ' + groupKey);
                }
                attr(group.groupElement, attributes);
            };
            /**
             * Reorder the proxy groups.
             *
             * The group key "series" refers to the chart's data points / <svg> element.
             * This is so that the keyboardNavigation.order option can be used to
             * determine the proxy group order.
             */
            ProxyProvider.prototype.updateGroupOrder = function (groupKeys) {
                var _this = this;
                // Store so that we can update order when a new group is created
                this.groupOrder = groupKeys.slice();
                // Don't unnecessarily reorder, because keyboard focus is lost
                if (this.isDOMOrderGroupOrder()) {
                    return;
                }
                var seriesIx = groupKeys.indexOf('series');
                var beforeKeys = seriesIx > -1 ? groupKeys.slice(0,
                    seriesIx) : groupKeys;
                var afterKeys = seriesIx > -1 ? groupKeys.slice(seriesIx + 1) : [];
                // Store focused element since it will be lost when reordering
                var activeElement = doc.activeElement;
                // Add groups to correct container
                ['before', 'after'].forEach(function (pos) {
                    var posContainer = _this[pos === 'before' ?
                            'beforeChartProxyPosContainer' :
                            'afterChartProxyPosContainer'];
                    var keys = pos === 'before' ? beforeKeys : afterKeys;
                    removeChildNodes(posContainer);
                    keys.forEach(function (groupKey) {
                        var group = _this.groups[groupKey];
                        if (group) {
                            posContainer.appendChild(group.groupElement);
                        }
                    });
                });
                // Attempt to restore focus after reordering, but note that this may
                // cause screen readers re-announcing the button.
                if ((this.beforeChartProxyPosContainer.contains(activeElement) ||
                    this.afterChartProxyPosContainer.contains(activeElement)) &&
                    activeElement && activeElement.focus) {
                    activeElement.focus();
                }
            };
            /**
             * Remove all proxy elements in a group
             */
            ProxyProvider.prototype.clearGroup = function (groupKey) {
                var group = this.groups[groupKey];
                if (!group) {
                    throw new Error('ProxyProvider.clearGroup: Invalid group key ' + groupKey);
                }
                removeChildNodes(group.proxyContainerElement);
            };
            /**
             * Remove a group from the DOM and from the proxy provider's group list.
             * All child elements are removed.
             * If the group does not exist, nothing happens.
             */
            ProxyProvider.prototype.removeGroup = function (groupKey) {
                var group = this.groups[groupKey];
                if (group) {
                    removeElement(group.groupElement);
                    delete this.groups[groupKey];
                }
            };
            /**
             * Update the position and order of all proxy groups and elements
             */
            ProxyProvider.prototype.update = function () {
                this.updatePosContainerPositions();
                this.updateGroupOrder(this.groupOrder);
                this.updateProxyElementPositions();
            };
            /**
             * Update all proxy element positions
             */
            ProxyProvider.prototype.updateProxyElementPositions = function () {
                Object.keys(this.groups).forEach(this.updateGroupProxyElementPositions.bind(this));
            };
            /**
             * Update a group's proxy elements' positions.
             * If the group does not exist, nothing happens.
             */
            ProxyProvider.prototype.updateGroupProxyElementPositions = function (groupKey) {
                var group = this.groups[groupKey];
                if (group) {
                    group.proxyElements.forEach(function (el) { return el.refreshPosition(); });
                }
            };
            /**
             * Remove all added elements
             */
            ProxyProvider.prototype.destroy = function () {
                this.domElementProvider.destroyCreatedElements();
            };
            // -------------------------- private ------------------------------------
            /**
             * Create and return a pos container element (the overall containers for
             * the proxy groups).
             */
            ProxyProvider.prototype.createProxyPosContainer = function (classNamePostfix) {
                var el = this.domElementProvider.createElement('div');
                el.setAttribute('aria-hidden', 'false');
                el.className = 'highcharts-a11y-proxy-container' + (classNamePostfix ? '-' + classNamePostfix : '');
                css(el, {
                    top: '0',
                    left: '0'
                });
                if (!this.chart.styledMode) {
                    el.style.whiteSpace = 'nowrap';
                    el.style.position = 'absolute';
                }
                return el;
            };
            /**
             * Get an array of group keys that corresponds to the current group order
             * in the DOM.
             */
            ProxyProvider.prototype.getCurrentGroupOrderInDOM = function () {
                var _this = this;
                var getGroupKeyFromElement = function (el) {
                        var allGroups = Object.keys(_this.groups);
                    var i = allGroups.length;
                    while (i--) {
                        var groupKey = allGroups[i];
                        var group = _this.groups[groupKey];
                        if (group && el === group.groupElement) {
                            return groupKey;
                        }
                    }
                };
                var getChildrenGroupOrder = function (el) {
                        var childrenOrder = [];
                    var children = el.children;
                    for (var i = 0; i < children.length; ++i) {
                        var groupKey = getGroupKeyFromElement(children[i]);
                        if (groupKey) {
                            childrenOrder.push(groupKey);
                        }
                    }
                    return childrenOrder;
                };
                var before = getChildrenGroupOrder(this.beforeChartProxyPosContainer);
                var after = getChildrenGroupOrder(this.afterChartProxyPosContainer);
                before.push('series');
                return before.concat(after);
            };
            /**
             * Check if the current DOM order matches the current group order, so that
             * a reordering/update is unnecessary.
             */
            ProxyProvider.prototype.isDOMOrderGroupOrder = function () {
                var _this = this;
                var domOrder = this.getCurrentGroupOrderInDOM();
                var groupOrderWithGroups = this.groupOrder.filter(function (x) { return x === 'series' || !!_this.groups[x]; });
                var i = domOrder.length;
                if (i !== groupOrderWithGroups.length) {
                    return false;
                }
                while (i--) {
                    if (domOrder[i] !== groupOrderWithGroups[i]) {
                        return false;
                    }
                }
                return true;
            };
            /**
             * Update the DOM positions of the before/after proxy
             * positioning containers for the groups.
             */
            ProxyProvider.prototype.updatePosContainerPositions = function () {
                var chart = this.chart;
                // If exporting, don't add these containers to the DOM.
                if (chart.renderer.forExport) {
                    return;
                }
                var rendererSVGEl = chart.renderer.box;
                chart.container.insertBefore(this.afterChartProxyPosContainer, rendererSVGEl.nextSibling);
                chart.container.insertBefore(this.beforeChartProxyPosContainer, rendererSVGEl);
                unhideChartElementFromAT(this.chart, this.afterChartProxyPosContainer);
                unhideChartElementFromAT(this.chart, this.beforeChartProxyPosContainer);
            };
            return ProxyProvider;
        }());
        /* *
         *
         *  Export Default
         *
         * */

        return ProxyProvider;
    });
    _registerModule(_modules, 'Stock/RangeSelector/RangeSelectorDefaults.js', [], function () {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /* *
         *
         *  Declarations
         *
         * */
        /**
         * Language object. The language object is global and it can't be set
         * on each chart initialization. Instead, use `Highcharts.setOptions` to
         * set it before any chart is initialized.
         *
         * ```js
         * Highcharts.setOptions({
         *     lang: {
         *         months: [
         *             'Janvier', 'Février', 'Mars', 'Avril',
         *             'Mai', 'Juin', 'Juillet', 'Août',
         *             'Septembre', 'Octobre', 'Novembre', 'Décembre'
         *         ],
         *         weekdays: [
         *             'Dimanche', 'Lundi', 'Mardi', 'Mercredi',
         *             'Jeudi', 'Vendredi', 'Samedi'
         *         ]
         *     }
         * });
         * ```
         *
         * @optionparent lang
         */
        var lang = {
                /**
                 * The text for the label for the range selector buttons.
                 *
                 * @product highstock gantt
                 */
                rangeSelectorZoom: 'Zoom',
                /**
                 * The text for the label for the "from" input box in the range
                 * selector. Since v9.0,
            this string is empty as the label is not
                 * rendered by default.
                 *
                 * @product highstock gantt
                 */
                rangeSelectorFrom: '',
                /**
                 * The text for the label for the "to" input box in the range selector.
                 *
                 * @product highstock gantt
                 */
                rangeSelectorTo: '→'
            };
        /**
         * The range selector is a tool for selecting ranges to display within
         * the chart. It provides buttons to select preconfigured ranges in
         * the chart, like 1 day, 1 week, 1 month etc. It also provides input
         * boxes where min and max dates can be manually input.
         *
         * @product      highstock gantt
         * @optionparent rangeSelector
         */
        var rangeSelector = {
                /**
                 * Whether to enable all buttons from the start. By default buttons are
                 * only enabled if the corresponding time range exists on the X axis,
                 * but enabling all buttons allows for dynamically loading different
                 * time ranges.
                 *
                 * @sample {highstock} stock/rangeselector/allbuttonsenabled-true/
                 *         All buttons enabled
                 *
                 * @since     2.0.3
                 */
                allButtonsEnabled: false,
                /**
                 * An array of configuration objects for the buttons.
                 *
                 * Defaults to:
                 * ```js
                 * buttons: [{
                 *     type: 'month',
                 *     count: 1,
                 *     text: '1m',
                 *     title: 'View 1 month'
                 * }, {
                 *     type: 'month',
                 *     count: 3,
                 *     text: '3m',
                 *     title: 'View 3 months'
                 * }, {
                 *     type: 'month',
                 *     count: 6,
                 *     text: '6m',
                 *     title: 'View 6 months'
                 * }, {
                 *     type: 'ytd',
                 *     text: 'YTD',
                 *     title: 'View year to date'
                 * }, {
                 *     type: 'year',
                 *     count: 1,
                 *     text: '1y',
                 *     title: 'View 1 year'
                 * }, {
                 *     type: 'all',
                 *     text: 'All',
                 *     title: 'View all'
                 * }]
                 * ```
                 *
                 * @sample {highstock} stock/rangeselector/datagrouping/
                 *         Data grouping by buttons
                 *
                 * @type      {Array<*>}
                 */
                buttons: void 0,
                /**
                 * How many units of the defined type the button should span. If `type`
                 * is "month" and `count` is 3,
            the button spans three months.
                 *
                 * @type      {number}
                 * @default   1
                 * @apioption rangeSelector.buttons.count
                 */
                /**
                 * Fires when clicking on the rangeSelector button. One parameter,
                 * event,
            is passed to the function,
            containing common event
                 * information.
                 *
                 * ```js
                 * click: function(e) {
                 *   console.log(this);
             * }
             * ```
             *
             * Return false to stop default button's click action.
             *
             * @sample {highstock} stock/rangeselector/button-click/
             *         Click event on the button
             *
             * @type      {Highcharts.RangeSelectorClickCallbackFunction}
             * @apioption rangeSelector.buttons.events.click
             */
            /**
             * Additional range (in milliseconds) added to the end of the calculated
             * time span.
             *
             * @sample {highstock} stock/rangeselector/min-max-offsets/
             *         Button offsets
             *
             * @type      {number}
             * @default   0
             * @since     6.0.0
             * @apioption rangeSelector.buttons.offsetMax
             */
            /**
             * Additional range (in milliseconds) added to the start of the
             * calculated time span.
             *
             * @sample {highstock} stock/rangeselector/min-max-offsets/
             *         Button offsets
             *
             * @type      {number}
             * @default   0
             * @since     6.0.0
             * @apioption rangeSelector.buttons.offsetMin
             */
            /**
             * When buttons apply dataGrouping on a series, by default zooming
             * in/out will deselect buttons and unset dataGrouping. Enable this
             * option to keep buttons selected when extremes change.
             *
             * @sample {highstock} stock/rangeselector/preserve-datagrouping/
             *         Different preserveDataGrouping settings
             *
             * @type      {boolean}
             * @default   false
             * @since     6.1.2
             * @apioption rangeSelector.buttons.preserveDataGrouping
             */
            /**
             * A custom data grouping object for each button.
             *
             * @see [series.dataGrouping](#plotOptions.series.dataGrouping)
             *
             * @sample {highstock} stock/rangeselector/datagrouping/
             *         Data grouping by range selector buttons
             *
             * @type      {*}
             * @extends   plotOptions.series.dataGrouping
             * @apioption rangeSelector.buttons.dataGrouping
             */
            /**
             * The text for the button itself.
             *
             * @type      {string}
             * @apioption rangeSelector.buttons.text
             */
            /**
             * Explanation for the button, shown as a tooltip on hover, and used by
             * assistive technology.
             *
             * @type      {string}
             * @apioption rangeSelector.buttons.title
             */
            /**
             * Defined the time span for the button. Can be one of `millisecond`,
             * `second`, `minute`, `hour`, `day`, `week`, `month`, `year`, `ytd`,
             * and `all`.
             *
             * @type       {Highcharts.RangeSelectorButtonTypeValue}
             * @apioption  rangeSelector.buttons.type
             */
            /**
             * The space in pixels between the buttons in the range selector.
             */
            buttonSpacing: 5,
            /**
             * Whether to collapse the range selector buttons into a dropdown when
             * there is not enough room to show everything in a single row, instead
             * of dividing the range selector into multiple rows.
             * Can be one of the following:
             *  - `always`: Always collapse
             *  - `responsive`: Only collapse when there is not enough room
             *  - `never`: Never collapse
             *
             * @sample {highstock} stock/rangeselector/dropdown/
             *         Dropdown option
             *
             * @validvalue ["always", "responsive", "never"]
             * @since 9.0.0
             */
            dropdown: 'responsive',
            /**
             * Enable or disable the range selector. Default to `true` for stock
             * charts, using the `stockChart` factory.
             *
             * @sample {highstock} stock/rangeselector/enabled/
             *         Disable the range selector
             *
             * @type {boolean|undefined}
             * @default {highstock} true
             */
            enabled: void 0,
            /**
             * The vertical alignment of the rangeselector box. Allowed properties
             * are `top`, `middle`, `bottom`.
             *
             * @sample {highstock} stock/rangeselector/vertical-align-middle/
             *         Middle
             * @sample {highstock} stock/rangeselector/vertical-align-bottom/
             *         Bottom
             *
             * @type  {Highcharts.VerticalAlignValue}
             * @since 6.0.0
             */
            verticalAlign: 'top',
            /**
             * A collection of attributes for the buttons. The object takes SVG
             * attributes like `fill`, `stroke`, `stroke-width`, as well as `style`,
             * a collection of CSS properties for the text.
             *
             * The object can also be extended with states, so you can set
             * presentational options for `hover`, `select` or `disabled` button
             * states.
             *
             * CSS styles for the text label.
             *
             * In styled mode, the buttons are styled by the
             * `.highcharts-range-selector-buttons .highcharts-button` rule with its
             * different states.
             *
             * @sample {highstock} stock/rangeselector/styling/
             *         Styling the buttons and inputs
             *
             * @type {Highcharts.SVGAttributes}
             */
            buttonTheme: {
                /** @ignore */
                width: 28,
                /** @ignore */
                height: 18,
                /** @ignore */
                padding: 2,
                /** @ignore */
                zIndex: 7 // #484, #852
            },
            /**
             * When the rangeselector is floating, the plot area does not reserve
             * space for it. This opens for positioning anywhere on the chart.
             *
             * @sample {highstock} stock/rangeselector/floating/
             *         Placing the range selector between the plot area and the
             *         navigator
             *
             * @since 6.0.0
             */
            floating: false,
            /**
             * The x offset of the range selector relative to its horizontal
             * alignment within `chart.spacingLeft` and `chart.spacingRight`.
             *
             * @since 6.0.0
             */
            x: 0,
            /**
             * The y offset of the range selector relative to its horizontal
             * alignment within `chart.spacingLeft` and `chart.spacingRight`.
             *
             * @since 6.0.0
             */
            y: 0,
            /**
             * Deprecated. The height of the range selector. Currently it is
             * calculated dynamically.
             *
             * @deprecated
             * @type  {number|undefined}
             * @since 2.1.9
             */
            height: void 0,
            /**
             * The border color of the date input boxes.
             *
             * @sample {highstock} stock/rangeselector/styling/
             *         Styling the buttons and inputs
             *
             * @type      {Highcharts.ColorString}
             * @since     1.3.7
             */
            inputBoxBorderColor: 'none',
            /**
             * The pixel height of the date input boxes.
             *
             * @sample {highstock} stock/rangeselector/styling/
             *         Styling the buttons and inputs
             *
             * @since     1.3.7
             */
            inputBoxHeight: 17,
            /**
             * The pixel width of the date input boxes. When `undefined`, the width
             * is fitted to the rendered content.
             *
             * @sample {highstock} stock/rangeselector/styling/
             *         Styling the buttons and inputs
             *
             * @type   {number|undefined}
             * @since  1.3.7
             */
            inputBoxWidth: void 0,
            /**
             * The date format in the input boxes when not selected for editing.
             * Defaults to `%b %e, %Y`.
             *
             * This is used to determine which type of input to show,
             * `datetime-local`, `date` or `time` and falling back to `text` when
             * the browser does not support the input type or the format contains
             * milliseconds.
             *
             * @sample {highstock} stock/rangeselector/input-type/
             *         Input types
             * @sample {highstock} stock/rangeselector/input-format/
             *         Milliseconds in the range selector
             *
             */
            inputDateFormat: '%b %e, %Y',
            /**
             * A custom callback function to parse values entered in the input boxes
             * and return a valid JavaScript time as milliseconds since 1970.
             * The first argument passed is a value to parse,
             * second is a boolean indicating use of the UTC time.
             *
             * This will only get called for inputs of type `text`. Since v8.2.3,
             * the input type is dynamically determined based on the granularity
             * of the `inputDateFormat` and the browser support.
             *
             * @sample {highstock} stock/rangeselector/input-format/
             *         Milliseconds in the range selector
             *
             * @type      {Highcharts.RangeSelectorParseCallbackFunction}
             * @since     1.3.3
             */
            inputDateParser: void 0,
            /**
             * The date format in the input boxes when they are selected for
             * editing. This must be a format that is recognized by JavaScript
             * Date.parse.
             *
             * This will only be used for inputs of type `text`. Since v8.2.3,
             * the input type is dynamically determined based on the granularity
             * of the `inputDateFormat` and the browser support.
             *
             * @sample {highstock} stock/rangeselector/input-format/
             *         Milliseconds in the range selector
             *
             */
            inputEditDateFormat: '%Y-%m-%d',
            /**
             * Enable or disable the date input boxes.
             */
            inputEnabled: true,
            /**
             * Positioning for the input boxes. Allowed properties are `align`,
             *  `x` and `y`.
             *
             * @since 1.2.4
             */
            inputPosition: {
                /**
                 * The alignment of the input box. Allowed properties are `left`,
                 * `center`, `right`.
                 *
                 * @sample {highstock} stock/rangeselector/input-button-position/
                 *         Alignment
                 *
                 * @type  {Highcharts.AlignValue}
                 * @since 6.0.0
                 */
                align: 'right',
                /**
                 * X offset of the input row.
                 */
                x: 0,
                /**
                 * Y offset of the input row.
                 */
                y: 0
            },
            /**
             * The space in pixels between the labels and the date input boxes in
             * the range selector.
             *
             * @since 9.0.0
             */
            inputSpacing: 5,
            /**
             * The index of the button to appear pre-selected.
             *
             * @type      {number}
             */
            selected: void 0,
            /**
             * Positioning for the button row.
             *
             * @since 1.2.4
             */
            buttonPosition: {
                /**
                 * The alignment of the input box. Allowed properties are `left`,
                 * `center`, `right`.
                 *
                 * @sample {highstock} stock/rangeselector/input-button-position/
                 *         Alignment
                 *
                 * @type  {Highcharts.AlignValue}
                 * @since 6.0.0
                 */
                align: 'left',
                /**
                 * X offset of the button row.
                 */
                x: 0,
                /**
                 * Y offset of the button row.
                 */
                y: 0
            },
            /**
             * CSS for the HTML inputs in the range selector.
             *
             * In styled mode, the inputs are styled by the
             * `.highcharts-range-input text` rule in SVG mode, and
             * `input.highcharts-range-selector` when active.
             *
             * @sample {highstock} stock/rangeselector/styling/
             *         Styling the buttons and inputs
             *
             * @type      {Highcharts.CSSObject}
             * @apioption rangeSelector.inputStyle
             */
            inputStyle: {
                /** @ignore */
                color: "#335cad" /* Palette.highlightColor80 */,
                /** @ignore */
                cursor: 'pointer'
            },
            /**
             * CSS styles for the labels - the Zoom, From and To texts.
             *
             * In styled mode, the labels are styled by the
             * `.highcharts-range-label` class.
             *
             * @sample {highstock} stock/rangeselector/styling/
             *         Styling the buttons and inputs
             *
             * @type {Highcharts.CSSObject}
             */
            labelStyle: {
                /** @ignore */
                color: "#666666" /* Palette.neutralColor60 */
            }
        };
        /* *
         *
         *  Default Export
         *
         * */
        var RangeSelectorDefaults = {
                lang: lang,
                rangeSelector: rangeSelector
            };

        return RangeSelectorDefaults;
    });
    _registerModule(_modules, 'Stock/RangeSelector/RangeSelectorComposition.js', [_modules['Core/Defaults.js'], _modules['Stock/RangeSelector/RangeSelectorDefaults.js'], _modules['Core/Utilities.js']], function (D, RangeSelectorDefaults, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var defaultOptions = D.defaultOptions,
            setOptions = D.setOptions;
        var addEvent = U.addEvent,
            defined = U.defined,
            extend = U.extend,
            find = U.find,
            isNumber = U.isNumber,
            merge = U.merge,
            pick = U.pick;
        /* *
         *
         *  Constants
         *
         * */
        var chartDestroyEvents = [];
        var composedMembers = [];
        /* *
         *
         *  Variables
         *
         * */
        var RangeSelectorConstructor;
        /* *
         *
         *  Functions
         *
         * */
        /**
         * Get the axis min value based on the range option and the current max. For
         * stock charts this is extended via the {@link RangeSelector} so that if the
         * selected range is a multiple of months or years, it is compensated for
         * various month lengths.
         *
         * @private
         * @function Highcharts.Axis#minFromRange
         * @return {number|undefined}
         *         The new minimum value.
         */
        function axisMinFromRange() {
            var rangeOptions = this.range,
                type = rangeOptions.type,
                max = this.max,
                time = this.chart.time, 
                // Get the true range from a start date
                getTrueRange = function (base,
                count) {
                    var timeName = type === 'year' ?
                        'FullYear' : 'Month';
                var date = new time.Date(base);
                var basePeriod = time.get(timeName,
                    date);
                time.set(timeName, date, basePeriod + count);
                if (basePeriod === time.get(timeName, date)) {
                    time.set('Date', date, 0); // #6537
                }
                return date.getTime() - base;
            };
            var min,
                range;
            if (isNumber(rangeOptions)) {
                min = max - rangeOptions;
                range = rangeOptions;
            }
            else if (rangeOptions) {
                min = max + getTrueRange(max, -(rangeOptions.count || 1));
                // Let the fixedRange reflect initial settings (#5930)
                if (this.chart) {
                    this.chart.fixedRange = max - min;
                }
            }
            var dataMin = pick(this.dataMin,
                Number.MIN_VALUE);
            if (!isNumber(min)) {
                min = dataMin;
            }
            if (min <= dataMin) {
                min = dataMin;
                if (typeof range === 'undefined') { // #4501
                    range = getTrueRange(min, rangeOptions.count);
                }
                this.newMax = Math.min(min + range, pick(this.dataMax, Number.MAX_VALUE));
            }
            if (!isNumber(max)) {
                min = void 0;
            }
            else if (!isNumber(rangeOptions) &&
                rangeOptions &&
                rangeOptions._offsetMin) {
                min += rangeOptions._offsetMin;
            }
            return min;
        }
        /**
         * @private
         */
        function compose(AxisClass, ChartClass, RangeSelectorClass) {
            RangeSelectorConstructor = RangeSelectorClass;
            if (composedMembers.indexOf(AxisClass) === -1) {
                composedMembers.push(AxisClass);
                AxisClass.prototype.minFromRange = axisMinFromRange;
            }
            if (composedMembers.indexOf(ChartClass) === -1) {
                composedMembers.push(ChartClass);
                addEvent(ChartClass, 'afterGetContainer', onChartAfterGetContainer);
                addEvent(ChartClass, 'beforeRender', onChartBeforeRender);
                addEvent(ChartClass, 'destroy', onChartDestroy);
                addEvent(ChartClass, 'getMargins', onChartGetMargins);
                addEvent(ChartClass, 'render', onChartRender);
                addEvent(ChartClass, 'update', onChartUpdate);
                var chartProto = ChartClass.prototype;
                chartProto.callbacks.push(onChartCallback);
            }
            if (composedMembers.indexOf(setOptions) === -1) {
                extend(defaultOptions, { rangeSelector: RangeSelectorDefaults.rangeSelector });
                extend(defaultOptions.lang, RangeSelectorDefaults.lang);
            }
        }
        /**
         * Initialize rangeselector for stock charts
         * @private
         */
        function onChartAfterGetContainer() {
            if (this.options.rangeSelector &&
                this.options.rangeSelector.enabled) {
                this.rangeSelector = new RangeSelectorConstructor(this);
            }
        }
        /**
         * @private
         */
        function onChartBeforeRender() {
            var chart = this,
                axes = chart.axes,
                rangeSelector = chart.rangeSelector;
            if (rangeSelector) {
                if (isNumber(rangeSelector.deferredYTDClick)) {
                    rangeSelector.clickButton(rangeSelector.deferredYTDClick);
                    delete rangeSelector.deferredYTDClick;
                }
                axes.forEach(function (axis) {
                    axis.updateNames();
                    axis.setScale();
                });
                chart.getAxisMargins();
                rangeSelector.render();
                var verticalAlign = rangeSelector.options.verticalAlign;
                if (!rangeSelector.options.floating) {
                    if (verticalAlign === 'bottom') {
                        this.extraBottomMargin = true;
                    }
                    else if (verticalAlign !== 'middle') {
                        this.extraTopMargin = true;
                    }
                }
            }
        }
        /**
         * @private
         */
        function onChartCallback(chart) {
            var extremes,
                legend,
                alignTo,
                verticalAlign;
            var rangeSelector = chart.rangeSelector,
                redraw = function () {
                    if (rangeSelector) {
                        extremes = chart.xAxis[0].getExtremes();
                    legend = chart.legend;
                    verticalAlign = (rangeSelector &&
                        rangeSelector.options.verticalAlign);
                    if (isNumber(extremes.min)) {
                        rangeSelector.render(extremes.min, extremes.max);
                    }
                    // Re-align the legend so that it's below the rangeselector
                    if (legend.display &&
                        verticalAlign === 'top' &&
                        verticalAlign === legend.options.verticalAlign) {
                        // Create a new alignment box for the legend.
                        alignTo = merge(chart.spacingBox);
                        if (legend.options.layout === 'vertical') {
                            alignTo.y = chart.plotTop;
                        }
                        else {
                            alignTo.y += rangeSelector.getHeight();
                        }
                        legend.group.placed = false; // Don't animate the alignment.
                        legend.align(alignTo);
                    }
                }
            };
            if (rangeSelector) {
                var events = find(chartDestroyEvents,
                    function (e) { return e[0] === chart; });
                if (!events) {
                    chartDestroyEvents.push([chart, [
                            // redraw the scroller on setExtremes
                            addEvent(chart.xAxis[0], 'afterSetExtremes', function (e) {
                                if (rangeSelector) {
                                    rangeSelector.render(e.min, e.max);
                                }
                            }),
                            // redraw the scroller chart resize
                            addEvent(chart, 'redraw', redraw)
                        ]]);
                }
                // do it now
                redraw();
            }
        }
        /**
         * Remove resize/afterSetExtremes at chart destroy.
         * @private
         */
        function onChartDestroy() {
            for (var i = 0, iEnd = chartDestroyEvents.length; i < iEnd; ++i) {
                var events = chartDestroyEvents[i];
                if (events[0] === this) {
                    events[1].forEach(function (unbind) { return unbind(); });
                    chartDestroyEvents.splice(i, 1);
                    return;
                }
            }
        }
        function onChartGetMargins() {
            var rangeSelector = this.rangeSelector;
            if (rangeSelector) {
                var rangeSelectorHeight = rangeSelector.getHeight();
                if (this.extraTopMargin) {
                    this.plotTop += rangeSelectorHeight;
                }
                if (this.extraBottomMargin) {
                    this.marginBottom += rangeSelectorHeight;
                }
            }
        }
        /**
         * @private
         */
        function onChartRender() {
            var chart = this,
                rangeSelector = chart.rangeSelector;
            if (rangeSelector && !rangeSelector.options.floating) {
                rangeSelector.render();
                var verticalAlign = rangeSelector.options.verticalAlign;
                if (verticalAlign === 'bottom') {
                    this.extraBottomMargin = true;
                }
                else if (verticalAlign !== 'middle') {
                    this.extraTopMargin = true;
                }
            }
        }
        /**
         * @private
         */
        function onChartUpdate(e) {
            var chart = this,
                options = e.options,
                optionsRangeSelector = options.rangeSelector,
                extraBottomMarginWas = this.extraBottomMargin,
                extraTopMarginWas = this.extraTopMargin;
            var rangeSelector = chart.rangeSelector;
            if (optionsRangeSelector &&
                optionsRangeSelector.enabled &&
                !defined(rangeSelector) &&
                this.options.rangeSelector) {
                this.options.rangeSelector.enabled = true;
                this.rangeSelector = rangeSelector = new RangeSelectorConstructor(this);
            }
            this.extraBottomMargin = false;
            this.extraTopMargin = false;
            if (rangeSelector) {
                onChartCallback(this);
                var verticalAlign = (optionsRangeSelector &&
                        optionsRangeSelector.verticalAlign) || (rangeSelector.options && rangeSelector.options.verticalAlign);
                if (!rangeSelector.options.floating) {
                    if (verticalAlign === 'bottom') {
                        this.extraBottomMargin = true;
                    }
                    else if (verticalAlign !== 'middle') {
                        this.extraTopMargin = true;
                    }
                }
                if (this.extraBottomMargin !== extraBottomMarginWas ||
                    this.extraTopMargin !== extraTopMarginWas) {
                    this.isDirtyBox = true;
                }
            }
        }
        /* *
         *
         *  Default Export
         *
         * */
        var RangeSelectorComposition = {
                compose: compose
            };

        return RangeSelectorComposition;
    });
    _registerModule(_modules, 'Stock/RangeSelector/RangeSelector.js', [_modules['Core/Axis/Axis.js'], _modules['Core/Defaults.js'], _modules['Core/Globals.js'], _modules['Stock/RangeSelector/RangeSelectorComposition.js'], _modules['Core/Renderer/SVG/SVGElement.js'], _modules['Core/Utilities.js']], function (Axis, D, H, RangeSelectorComposition, SVGElement, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var defaultOptions = D.defaultOptions;
        var addEvent = U.addEvent,
            createElement = U.createElement,
            css = U.css,
            defined = U.defined,
            destroyObjectProperties = U.destroyObjectProperties,
            discardElement = U.discardElement,
            extend = U.extend,
            fireEvent = U.fireEvent,
            isNumber = U.isNumber,
            merge = U.merge,
            objectEach = U.objectEach,
            pad = U.pad,
            pick = U.pick,
            pInt = U.pInt,
            splat = U.splat;
        /* *
         *
         *  Functions
         *
         * */
        /**
         * Get the preferred input type based on a date format string.
         *
         * @private
         * @function preferredInputType
         */
        function preferredInputType(format) {
            var ms = format.indexOf('%L') !== -1;
            if (ms) {
                return 'text';
            }
            var date = ['a', 'A', 'd', 'e', 'w', 'b', 'B', 'm', 'o', 'y', 'Y']
                    .some(function (char) { return format.indexOf('%' + char) !== -1; });
            var time = ['H', 'k', 'I', 'l', 'M', 'S']
                    .some(function (char) { return format.indexOf('%' + char) !== -1; });
            if (date && time) {
                return 'datetime-local';
            }
            if (date) {
                return 'date';
            }
            if (time) {
                return 'time';
            }
            return 'text';
        }
        /* *
         *
         *  Class
         *
         * */
        /**
         * The range selector.
         *
         * @private
         * @class
         * @name Highcharts.RangeSelector
         * @param {Highcharts.Chart} chart
         */
        var RangeSelector = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function RangeSelector(chart) {
                    /* *
                     *
                     *  Properties
                     *
                     * */
                    this.buttons = void 0;
                this.buttonOptions = RangeSelector.prototype.defaultButtons;
                this.initialButtonGroupWidth = 0;
                this.options = void 0;
                this.chart = chart;
                this.init(chart);
            }
            /* *
             *
             *  Static Functions
             *
             * */
            /**
             * @private
             */
            RangeSelector.compose = function (AxisClass, ChartClass) {
                RangeSelectorComposition.compose(AxisClass, ChartClass, RangeSelector);
            };
            /* *
             *
             *  Functions
             *
             * */
            /**
             * The method to run when one of the buttons in the range selectors is
             * clicked
             *
             * @private
             * @function Highcharts.RangeSelector#clickButton
             * @param {number} i
             *        The index of the button
             * @param {boolean} [redraw]
             */
            RangeSelector.prototype.clickButton = function (i, redraw) {
                var rangeSelector = this,
                    chart = rangeSelector.chart,
                    rangeOptions = rangeSelector.buttonOptions[i],
                    baseAxis = chart.xAxis[0],
                    unionExtremes = (chart.scroller && chart.scroller.getUnionExtremes()) || baseAxis || {},
                    type = rangeOptions.type,
                    dataGrouping = rangeOptions.dataGrouping;
                var dataMin = unionExtremes.dataMin,
                    dataMax = unionExtremes.dataMax,
                    newMin,
                    newMax = baseAxis && Math.round(Math.min(baseAxis.max,
                    pick(dataMax,
                    baseAxis.max))), // #1568
                    baseXAxisOptions,
                    range = rangeOptions._range,
                    rangeMin,
                    minSetting,
                    rangeSetting,
                    ctx,
                    ytdExtremes,
                    addOffsetMin = true;
                // chart has no data, base series is removed
                if (dataMin === null || dataMax === null) {
                    return;
                }
                // Set the fixed range before range is altered
                chart.fixedRange = range;
                rangeSelector.setSelected(i);
                // Apply dataGrouping associated to button
                if (dataGrouping) {
                    this.forcedDataGrouping = true;
                    Axis.prototype.setDataGrouping.call(baseAxis || { chart: this.chart }, dataGrouping, false);
                    this.frozenStates = rangeOptions.preserveDataGrouping;
                }
                // Apply range
                if (type === 'month' || type === 'year') {
                    if (!baseAxis) {
                        // This is set to the user options and picked up later when the
                        // axis is instantiated so that we know the min and max.
                        range = rangeOptions;
                    }
                    else {
                        ctx = {
                            range: rangeOptions,
                            max: newMax,
                            chart: chart,
                            dataMin: dataMin,
                            dataMax: dataMax
                        };
                        newMin = baseAxis.minFromRange.call(ctx);
                        if (isNumber(ctx.newMax)) {
                            newMax = ctx.newMax;
                        }
                        // #15799: offsetMin is added in minFromRange so that it works
                        // with pre-selected buttons as well
                        addOffsetMin = false;
                    }
                    // Fixed times like minutes, hours, days
                }
                else if (range) {
                    newMin = Math.max(newMax - range, dataMin);
                    newMax = Math.min(newMin + range, dataMax);
                    addOffsetMin = false;
                }
                else if (type === 'ytd') {
                    // On user clicks on the buttons, or a delayed action running from
                    // the beforeRender event (below), the baseAxis is defined.
                    if (baseAxis) {
                        // When "ytd" is the pre-selected button for the initial view,
                        // its calculation is delayed and rerun in the beforeRender
                        // event (below). When the series are initialized, but before
                        // the chart is rendered, we have access to the xData array
                        // (#942).
                        if (typeof dataMax === 'undefined' ||
                            typeof dataMin === 'undefined') {
                            dataMin = Number.MAX_VALUE;
                            dataMax = Number.MIN_VALUE;
                            chart.series.forEach(function (series) {
                                // reassign it to the last item
                                var xData = series.xData;
                                if (xData) {
                                    dataMin = Math.min(xData[0], dataMin);
                                    dataMax = Math.max(xData[xData.length - 1], dataMax);
                                }
                            });
                            redraw = false;
                        }
                        ytdExtremes = rangeSelector.getYTDExtremes(dataMax, dataMin, chart.time.useUTC);
                        newMin = rangeMin = ytdExtremes.min;
                        newMax = ytdExtremes.max;
                        // "ytd" is pre-selected. We don't yet have access to processed
                        // point and extremes data (things like pointStart and pointInterval
                        // are missing), so we delay the process (#942)
                    }
                    else {
                        rangeSelector.deferredYTDClick = i;
                        return;
                    }
                }
                else if (type === 'all' && baseAxis) {
                    // If the navigator exist and the axis range is declared reset that
                    // range and from now on only use the range set by a user, #14742.
                    if (chart.navigator && chart.navigator.baseSeries[0]) {
                        chart.navigator.baseSeries[0].xAxis.options.range = void 0;
                    }
                    newMin = dataMin;
                    newMax = dataMax;
                }
                if (addOffsetMin && rangeOptions._offsetMin && defined(newMin)) {
                    newMin += rangeOptions._offsetMin;
                }
                if (rangeOptions._offsetMax && defined(newMax)) {
                    newMax += rangeOptions._offsetMax;
                }
                if (this.dropdown) {
                    this.dropdown.selectedIndex = i + 1;
                }
                // Update the chart
                if (!baseAxis) {
                    // Axis not yet instanciated. Temporarily set min and range
                    // options and remove them on chart load (#4317).
                    baseXAxisOptions = splat(chart.options.xAxis)[0];
                    rangeSetting = baseXAxisOptions.range;
                    baseXAxisOptions.range = range;
                    minSetting = baseXAxisOptions.min;
                    baseXAxisOptions.min = rangeMin;
                    addEvent(chart, 'load', function resetMinAndRange() {
                        baseXAxisOptions.range = rangeSetting;
                        baseXAxisOptions.min = minSetting;
                    });
                }
                else {
                    // Existing axis object. Set extremes after render time.
                    baseAxis.setExtremes(newMin, newMax, pick(redraw, true), void 0, // auto animation
                    {
                        trigger: 'rangeSelectorButton',
                        rangeSelectorButton: rangeOptions
                    });
                }
                fireEvent(this, 'afterBtnClick');
            };
            /**
             * Set the selected option. This method only sets the internal flag, it
             * doesn't update the buttons or the actual zoomed range.
             *
             * @private
             * @function Highcharts.RangeSelector#setSelected
             * @param {number} [selected]
             */
            RangeSelector.prototype.setSelected = function (selected) {
                this.selected = this.options.selected = selected;
            };
            /**
             * Initialize the range selector
             *
             * @private
             * @function Highcharts.RangeSelector#init
             * @param {Highcharts.Chart} chart
             */
            RangeSelector.prototype.init = function (chart) {
                var rangeSelector = this,
                    options = chart.options.rangeSelector,
                    buttonOptions = (options.buttons || rangeSelector.defaultButtons.slice()),
                    selectedOption = options.selected,
                    blurInputs = function () {
                        var minInput = rangeSelector.minInput,
                    maxInput = rangeSelector.maxInput;
                    // #3274 in some case blur is not defined
                    if (minInput && (minInput.blur)) {
                        fireEvent(minInput, 'blur');
                    }
                    if (maxInput && (maxInput.blur)) {
                        fireEvent(maxInput, 'blur');
                    }
                };
                rangeSelector.chart = chart;
                rangeSelector.options = options;
                rangeSelector.buttons = [];
                rangeSelector.buttonOptions = buttonOptions;
                this.eventsToUnbind = [];
                this.eventsToUnbind.push(addEvent(chart.container, 'mousedown', blurInputs));
                this.eventsToUnbind.push(addEvent(chart, 'resize', blurInputs));
                // Extend the buttonOptions with actual range
                buttonOptions.forEach(rangeSelector.computeButtonRange);
                // zoomed range based on a pre-selected button index
                if (typeof selectedOption !== 'undefined' &&
                    buttonOptions[selectedOption]) {
                    this.clickButton(selectedOption, false);
                }
                this.eventsToUnbind.push(addEvent(chart, 'load', function () {
                    // If a data grouping is applied to the current button, release it
                    // when extremes change
                    if (chart.xAxis && chart.xAxis[0]) {
                        addEvent(chart.xAxis[0], 'setExtremes', function (e) {
                            if (this.max - this.min !==
                                chart.fixedRange &&
                                e.trigger !== 'rangeSelectorButton' &&
                                e.trigger !== 'updatedData' &&
                                rangeSelector.forcedDataGrouping &&
                                !rangeSelector.frozenStates) {
                                this.setDataGrouping(false, false);
                            }
                        });
                    }
                }));
            };
            /**
             * Dynamically update the range selector buttons after a new range has been
             * set
             *
             * @private
             * @function Highcharts.RangeSelector#updateButtonStates
             */
            RangeSelector.prototype.updateButtonStates = function () {
                var rangeSelector = this,
                    chart = this.chart,
                    dropdown = this.dropdown,
                    baseAxis = chart.xAxis[0],
                    actualRange = Math.round(baseAxis.max - baseAxis.min),
                    hasNoData = !baseAxis.hasVisibleSeries,
                    day = 24 * 36e5, // A single day in milliseconds
                    unionExtremes = (chart.scroller &&
                        chart.scroller.getUnionExtremes()) || baseAxis,
                    dataMin = unionExtremes.dataMin,
                    dataMax = unionExtremes.dataMax,
                    ytdExtremes = rangeSelector.getYTDExtremes(dataMax,
                    dataMin,
                    chart.time.useUTC),
                    ytdMin = ytdExtremes.min,
                    ytdMax = ytdExtremes.max,
                    selected = rangeSelector.selected,
                    allButtonsEnabled = rangeSelector.options.allButtonsEnabled,
                    buttons = rangeSelector.buttons;
                var selectedExists = isNumber(selected);
                rangeSelector.buttonOptions.forEach(function (rangeOptions, i) {
                    var range = rangeOptions._range,
                        type = rangeOptions.type,
                        count = rangeOptions.count || 1,
                        button = buttons[i],
                        offsetRange = rangeOptions._offsetMax -
                            rangeOptions._offsetMin,
                        isSelected = i === selected, 
                        // Disable buttons where the range exceeds what is allowed in
                        // the current view
                        isTooGreatRange = range >
                            dataMax - dataMin, 
                        // Disable buttons where the range is smaller than the minimum
                        // range
                        isTooSmallRange = range < baseAxis.minRange;
                    var state = 0, 
                        // Do not select the YTD button if not explicitly told so
                        isYTDButNotSelected = false, 
                        // Disable the All button if we're already showing all
                        isAllButAlreadyShowingAll = false,
                        isSameRange = range === actualRange;
                    // Months and years have a variable range so we check the extremes
                    if ((type === 'month' || type === 'year') &&
                        (actualRange + 36e5 >=
                            { month: 28, year: 365 }[type] * day * count - offsetRange) &&
                        (actualRange - 36e5 <=
                            { month: 31, year: 366 }[type] * day * count + offsetRange)) {
                        isSameRange = true;
                    }
                    else if (type === 'ytd') {
                        isSameRange = (ytdMax - ytdMin + offsetRange) === actualRange;
                        isYTDButNotSelected = !isSelected;
                    }
                    else if (type === 'all') {
                        isSameRange = (baseAxis.max - baseAxis.min >=
                            dataMax - dataMin);
                        isAllButAlreadyShowingAll = (!isSelected &&
                            selectedExists &&
                            isSameRange);
                    }
                    // The new zoom area happens to match the range for a button - mark
                    // it selected. This happens when scrolling across an ordinal gap.
                    // It can be seen in the intraday demos when selecting 1h and scroll
                    // across the night gap.
                    var disable = (!allButtonsEnabled &&
                            (isTooGreatRange ||
                                isTooSmallRange ||
                                isAllButAlreadyShowingAll ||
                                hasNoData));
                    var select = ((isSelected && isSameRange) ||
                            (isSameRange && !selectedExists && !isYTDButNotSelected) ||
                            (isSelected && rangeSelector.frozenStates));
                    if (disable) {
                        state = 3;
                    }
                    else if (select) {
                        selectedExists = true; // Only one button can be selected
                        state = 2;
                    }
                    // If state has changed, update the button
                    if (button.state !== state) {
                        button.setState(state);
                        if (dropdown) {
                            dropdown.options[i + 1].disabled = disable;
                            if (state === 2) {
                                dropdown.selectedIndex = i + 1;
                            }
                        }
                        // Reset (#9209)
                        if (state === 0 && selected === i) {
                            rangeSelector.setSelected();
                        }
                    }
                });
            };
            /**
             * Compute and cache the range for an individual button
             *
             * @private
             * @function Highcharts.RangeSelector#computeButtonRange
             * @param {Highcharts.RangeSelectorButtonsOptions} rangeOptions
             */
            RangeSelector.prototype.computeButtonRange = function (rangeOptions) {
                var type = rangeOptions.type,
                    count = rangeOptions.count || 1, 
                    // these time intervals have a fixed number of milliseconds, as
                    // opposed to month, ytd and year
                    fixedTimes = {
                        millisecond: 1,
                        second: 1000,
                        minute: 60 * 1000,
                        hour: 3600 * 1000,
                        day: 24 * 3600 * 1000,
                        week: 7 * 24 * 3600 * 1000
                    };
                // Store the range on the button object
                if (fixedTimes[type]) {
                    rangeOptions._range = fixedTimes[type] * count;
                }
                else if (type === 'month' || type === 'year') {
                    rangeOptions._range = {
                        month: 30,
                        year: 365
                    }[type] * 24 * 36e5 * count;
                }
                rangeOptions._offsetMin = pick(rangeOptions.offsetMin, 0);
                rangeOptions._offsetMax = pick(rangeOptions.offsetMax, 0);
                rangeOptions._range +=
                    rangeOptions._offsetMax - rangeOptions._offsetMin;
            };
            /**
             * Get the unix timestamp of a HTML input for the dates
             *
             * @private
             * @function Highcharts.RangeSelector#getInputValue
             */
            RangeSelector.prototype.getInputValue = function (name) {
                var input = name === 'min' ? this.minInput : this.maxInput;
                var options = this.chart.options
                        .rangeSelector;
                var time = this.chart.time;
                if (input) {
                    return ((input.type === 'text' && options.inputDateParser) ||
                        this.defaultInputDateParser)(input.value, time.useUTC, time);
                }
                return 0;
            };
            /**
             * Set the internal and displayed value of a HTML input for the dates
             *
             * @private
             * @function Highcharts.RangeSelector#setInputValue
             */
            RangeSelector.prototype.setInputValue = function (name, inputTime) {
                var options = this.options, time = this.chart.time, input = name === 'min' ? this.minInput : this.maxInput, dateBox = name === 'min' ? this.minDateBox : this.maxDateBox;
                if (input) {
                    var hcTimeAttr = input.getAttribute('data-hc-time');
                    var updatedTime = defined(hcTimeAttr) ? Number(hcTimeAttr) : void 0;
                    if (defined(inputTime)) {
                        var previousTime = updatedTime;
                        if (defined(previousTime)) {
                            input.setAttribute('data-hc-time-previous', previousTime);
                        }
                        input.setAttribute('data-hc-time', inputTime);
                        updatedTime = inputTime;
                    }
                    input.value = time.dateFormat((this.inputTypeFormats[input.type] ||
                        options.inputEditDateFormat), updatedTime);
                    if (dateBox) {
                        dateBox.attr({
                            text: time.dateFormat(options.inputDateFormat, updatedTime)
                        });
                    }
                }
            };
            /**
             * Set the min and max value of a HTML input for the dates
             *
             * @private
             * @function Highcharts.RangeSelector#setInputExtremes
             */
            RangeSelector.prototype.setInputExtremes = function (name, min, max) {
                var input = name === 'min' ? this.minInput : this.maxInput;
                if (input) {
                    var format = this.inputTypeFormats[input.type];
                    var time = this.chart.time;
                    if (format) {
                        var newMin = time.dateFormat(format,
                            min);
                        if (input.min !== newMin) {
                            input.min = newMin;
                        }
                        var newMax = time.dateFormat(format,
                            max);
                        if (input.max !== newMax) {
                            input.max = newMax;
                        }
                    }
                }
            };
            /**
             * @private
             * @function Highcharts.RangeSelector#showInput
             * @param {string} name
             */
            RangeSelector.prototype.showInput = function (name) {
                var dateBox = name === 'min' ? this.minDateBox : this.maxDateBox;
                var input = name === 'min' ? this.minInput : this.maxInput;
                if (input && dateBox && this.inputGroup) {
                    var isTextInput = input.type === 'text';
                    var _a = this.inputGroup,
                        translateX = _a.translateX,
                        translateY = _a.translateY;
                    var inputBoxWidth = this.options.inputBoxWidth;
                    css(input, {
                        width: isTextInput ?
                            ((dateBox.width + (inputBoxWidth ? -2 : 20)) + 'px') :
                            'auto',
                        height: isTextInput ? ((dateBox.height - 2) + 'px') : 'auto',
                        border: '2px solid silver'
                    });
                    if (isTextInput && inputBoxWidth) {
                        css(input, {
                            left: (translateX + dateBox.x) + 'px',
                            top: translateY + 'px'
                        });
                        // Inputs of types date, time or datetime-local should be centered
                        // on top of the dateBox
                    }
                    else {
                        css(input, {
                            left: Math.min(Math.round(dateBox.x +
                                translateX -
                                (input.offsetWidth - dateBox.width) / 2), this.chart.chartWidth - input.offsetWidth) + 'px',
                            top: (translateY - (input.offsetHeight - dateBox.height) / 2) + 'px'
                        });
                    }
                }
            };
            /**
             * @private
             * @function Highcharts.RangeSelector#hideInput
             * @param {string} name
             */
            RangeSelector.prototype.hideInput = function (name) {
                var input = name === 'min' ? this.minInput : this.maxInput;
                if (input) {
                    css(input, {
                        top: '-9999em',
                        border: 0,
                        width: '1px',
                        height: '1px'
                    });
                }
            };
            /**
             * @private
             * @function Highcharts.RangeSelector#defaultInputDateParser
             */
            RangeSelector.prototype.defaultInputDateParser = function (inputDate, useUTC, time) {
                var hasTimezone = function (str) {
                        return str.length > 6 &&
                            (str.lastIndexOf('-') === str.length - 6 ||
                                str.lastIndexOf('+') === str.length - 6);
                };
                var input = inputDate.split('/').join('-').split(' ').join('T');
                if (input.indexOf('T') === -1) {
                    input += 'T00:00';
                }
                if (useUTC) {
                    input += 'Z';
                }
                else if (H.isSafari && !hasTimezone(input)) {
                    var offset = new Date(input).getTimezoneOffset() / 60;
                    input += offset <= 0 ? "+".concat(pad(-offset), ":00") : "-".concat(pad(offset), ":00");
                }
                var date = Date.parse(input);
                // If the value isn't parsed directly to a value by the
                // browser's Date.parse method, like YYYY-MM-DD in IE8, try
                // parsing it a different way
                if (!isNumber(date)) {
                    var parts = inputDate.split('-');
                    date = Date.UTC(pInt(parts[0]), pInt(parts[1]) - 1, pInt(parts[2]));
                }
                if (time && useUTC && isNumber(date)) {
                    date += time.getTimezoneOffset(date);
                }
                return date;
            };
            /**
             * Draw either the 'from' or the 'to' HTML input box of the range selector
             *
             * @private
             * @function Highcharts.RangeSelector#drawInput
             */
            RangeSelector.prototype.drawInput = function (name) {
                var _a = this,
                    chart = _a.chart,
                    div = _a.div,
                    inputGroup = _a.inputGroup;
                var rangeSelector = this,
                    chartStyle = chart.renderer.style || {},
                    renderer = chart.renderer,
                    options = chart.options.rangeSelector,
                    lang = defaultOptions.lang,
                    isMin = name === 'min';
                /**
                 * @private
                 */
                function updateExtremes() {
                    var maxInput = rangeSelector.maxInput,
                        minInput = rangeSelector.minInput,
                        chartAxis = chart.xAxis[0],
                        dataAxis = chart.scroller && chart.scroller.xAxis ?
                            chart.scroller.xAxis :
                            chartAxis,
                        dataMin = dataAxis.dataMin,
                        dataMax = dataAxis.dataMax;
                    var value = rangeSelector.getInputValue(name);
                    if (value !== Number(input.getAttribute('data-hc-time-previous')) &&
                        isNumber(value)) {
                        input.setAttribute('data-hc-time-previous', value);
                        // Validate the extremes. If it goes beyound the data min or
                        // max, use the actual data extreme (#2438).
                        if (isMin && maxInput && isNumber(dataMin)) {
                            if (value > Number(maxInput.getAttribute('data-hc-time'))) {
                                value = void 0;
                            }
                            else if (value < dataMin) {
                                value = dataMin;
                            }
                        }
                        else if (minInput && isNumber(dataMax)) {
                            if (value < Number(minInput.getAttribute('data-hc-time'))) {
                                value = void 0;
                            }
                            else if (value > dataMax) {
                                value = dataMax;
                            }
                        }
                        // Set the extremes
                        if (typeof value !== 'undefined') { // @todo typof undefined
                            chartAxis.setExtremes(isMin ? value : chartAxis.min, isMin ? chartAxis.max : value, void 0, void 0, { trigger: 'rangeSelectorInput' });
                        }
                    }
                }
                // Create the text label
                var text = lang[isMin ? 'rangeSelectorFrom' : 'rangeSelectorTo'] || '';
                var label = renderer
                        .label(text, 0)
                        .addClass('highcharts-range-label')
                        .attr({
                        padding: text ? 2 : 0,
                        height: text ? options.inputBoxHeight : 0
                    })
                        .add(inputGroup);
                // Create an SVG label that shows updated date ranges and and records
                // click events that bring in the HTML input.
                var dateBox = renderer
                        .label('', 0)
                        .addClass('highcharts-range-input')
                        .attr({
                        padding: 2,
                        width: options.inputBoxWidth,
                        height: options.inputBoxHeight,
                        'text-align': 'center'
                    })
                        .on('click',
                    function () {
                        // If it is already focused, the onfocus event doesn't fire
                        // (#3713)
                        rangeSelector.showInput(name);
                    rangeSelector[name + 'Input'].focus();
                });
                if (!chart.styledMode) {
                    dateBox.attr({
                        stroke: options.inputBoxBorderColor,
                        'stroke-width': 1
                    });
                }
                dateBox.add(inputGroup);
                // Create the HTML input element. This is rendered as 1x1 pixel then set
                // to the right size when focused.
                var input = createElement('input', {
                        name: name,
                        className: 'highcharts-range-selector'
                    },
                    void 0,
                    div);
                // #14788: Setting input.type to an unsupported type throws in IE, so
                // we need to use setAttribute instead
                input.setAttribute('type', preferredInputType(options.inputDateFormat || '%b %e, %Y'));
                if (!chart.styledMode) {
                    // Styles
                    label.css(merge(chartStyle, options.labelStyle));
                    dateBox.css(merge({
                        color: "#333333" /* Palette.neutralColor80 */
                    }, chartStyle, options.inputStyle));
                    css(input, extend({
                        position: 'absolute',
                        border: 0,
                        boxShadow: '0 0 15px rgba(0,0,0,0.3)',
                        width: '1px',
                        height: '1px',
                        padding: 0,
                        textAlign: 'center',
                        fontSize: chartStyle.fontSize,
                        fontFamily: chartStyle.fontFamily,
                        top: '-9999em' // #4798
                    }, options.inputStyle));
                }
                // Blow up the input box
                input.onfocus = function () {
                    rangeSelector.showInput(name);
                };
                // Hide away the input box
                input.onblur = function () {
                    // update extermes only when inputs are active
                    if (input === H.doc.activeElement) { // Only when focused
                        // Update also when no `change` event is triggered, like when
                        // clicking inside the SVG (#4710)
                        updateExtremes();
                    }
                    // #10404 - move hide and blur outside focus
                    rangeSelector.hideInput(name);
                    rangeSelector.setInputValue(name);
                    input.blur(); // #4606
                };
                var keyDown = false;
                // handle changes in the input boxes
                input.onchange = function () {
                    // Update extremes and blur input when clicking date input calendar
                    if (!keyDown) {
                        updateExtremes();
                        rangeSelector.hideInput(name);
                        input.blur();
                    }
                };
                input.onkeypress = function (event) {
                    // IE does not fire onchange on enter
                    if (event.keyCode === 13) {
                        updateExtremes();
                    }
                };
                input.onkeydown = function (event) {
                    keyDown = true;
                    // Arrow keys
                    if (event.keyCode === 38 || event.keyCode === 40) {
                        updateExtremes();
                    }
                };
                input.onkeyup = function () {
                    keyDown = false;
                };
                return { dateBox: dateBox, input: input, label: label };
            };
            /**
             * Get the position of the range selector buttons and inputs. This can be
             * overridden from outside for custom positioning.
             *
             * @private
             * @function Highcharts.RangeSelector#getPosition
             */
            RangeSelector.prototype.getPosition = function () {
                var chart = this.chart,
                    options = chart.options.rangeSelector,
                    top = options.verticalAlign === 'top' ?
                        chart.plotTop - chart.axisOffset[0] :
                        0; // set offset only for varticalAlign top
                    return {
                        buttonTop: top + options.buttonPosition.y,
                        inputTop: top + options.inputPosition.y - 10
                    };
            };
            /**
             * Get the extremes of YTD. Will choose dataMax if its value is lower than
             * the current timestamp. Will choose dataMin if its value is higher than
             * the timestamp for the start of current year.
             *
             * @private
             * @function Highcharts.RangeSelector#getYTDExtremes
             * @return {*}
             * Returns min and max for the YTD
             */
            RangeSelector.prototype.getYTDExtremes = function (dataMax, dataMin, useUTC) {
                var time = this.chart.time,
                    now = new time.Date(dataMax),
                    year = time.get('FullYear',
                    now),
                    startOfYear = useUTC ?
                        time.Date.UTC(year, 0, 1) : // eslint-disable-line new-cap
                        +new time.Date(year, 0, 1),
                    min = Math.max(dataMin,
                    startOfYear),
                    ts = now.getTime();
                return {
                    max: Math.min(dataMax || ts, ts),
                    min: min
                };
            };
            /**
             * Render the range selector including the buttons and the inputs. The first
             * time render is called, the elements are created and positioned. On
             * subsequent calls, they are moved and updated.
             *
             * @private
             * @function Highcharts.RangeSelector#render
             * @param {number} [min]
             *        X axis minimum
             * @param {number} [max]
             *        X axis maximum
             */
            RangeSelector.prototype.render = function (min, max) {
                var chart = this.chart,
                    renderer = chart.renderer,
                    container = chart.container,
                    chartOptions = chart.options,
                    options = chartOptions.rangeSelector, 
                    // Place inputs above the container
                    inputsZIndex = pick(chartOptions.chart.style &&
                        chartOptions.chart.style.zIndex, 0) + 1,
                    inputEnabled = options.inputEnabled,
                    rendered = this.rendered;
                if (options.enabled === false) {
                    return;
                }
                // create the elements
                if (!rendered) {
                    this.group = renderer.g('range-selector-group')
                        .attr({
                        zIndex: 7
                    })
                        .add();
                    this.div = createElement('div', void 0, {
                        position: 'relative',
                        height: 0,
                        zIndex: inputsZIndex
                    });
                    if (this.buttonOptions.length) {
                        this.renderButtons();
                    }
                    // First create a wrapper outside the container in order to make
                    // the inputs work and make export correct
                    if (container.parentNode) {
                        container.parentNode.insertBefore(this.div, container);
                    }
                    if (inputEnabled) {
                        // Create the group to keep the inputs
                        this.inputGroup = renderer.g('input-group').add(this.group);
                        var minElems = this.drawInput('min');
                        this.minDateBox = minElems.dateBox;
                        this.minLabel = minElems.label;
                        this.minInput = minElems.input;
                        var maxElems = this.drawInput('max');
                        this.maxDateBox = maxElems.dateBox;
                        this.maxLabel = maxElems.label;
                        this.maxInput = maxElems.input;
                    }
                }
                if (inputEnabled) {
                    // Set or reset the input values
                    this.setInputValue('min', min);
                    this.setInputValue('max', max);
                    var unionExtremes = (chart.scroller && chart.scroller.getUnionExtremes()) || chart.xAxis[0] || {};
                    if (defined(unionExtremes.dataMin) &&
                        defined(unionExtremes.dataMax)) {
                        var minRange = chart.xAxis[0].minRange || 0;
                        this.setInputExtremes('min', unionExtremes.dataMin, Math.min(unionExtremes.dataMax, this.getInputValue('max')) - minRange);
                        this.setInputExtremes('max', Math.max(unionExtremes.dataMin, this.getInputValue('min')) + minRange, unionExtremes.dataMax);
                    }
                    // Reflow
                    if (this.inputGroup) {
                        var x_1 = 0;
                        [
                            this.minLabel,
                            this.minDateBox,
                            this.maxLabel,
                            this.maxDateBox
                        ].forEach(function (label) {
                            if (label) {
                                var width = label.getBBox().width;
                                if (width) {
                                    label.attr({ x: x_1 });
                                    x_1 += width + options.inputSpacing;
                                }
                            }
                        });
                    }
                }
                this.alignElements();
                this.rendered = true;
            };
            /**
             * Render the range buttons. This only runs the first time, later the
             * positioning is laid out in alignElements.
             *
             * @private
             * @function Highcharts.RangeSelector#renderButtons
             */
            RangeSelector.prototype.renderButtons = function () {
                var _this = this;
                var _a = this,
                    buttons = _a.buttons,
                    chart = _a.chart,
                    options = _a.options;
                var lang = defaultOptions.lang;
                var renderer = chart.renderer;
                var buttonTheme = merge(options.buttonTheme);
                var states = buttonTheme && buttonTheme.states;
                // Prevent the button from resetting the width when the button state
                // changes since we need more control over the width when collapsing
                // the buttons
                var width = buttonTheme.width || 28;
                delete buttonTheme.width;
                delete buttonTheme.states;
                this.buttonGroup = renderer.g('range-selector-buttons').add(this.group);
                var dropdown = this.dropdown = createElement('select',
                    void 0, {
                        position: 'absolute',
                        width: '1px',
                        height: '1px',
                        padding: 0,
                        border: 0,
                        top: '-9999em',
                        cursor: 'pointer',
                        opacity: 0.0001
                    },
                    this.div);
                // Prevent page zoom on iPhone
                addEvent(dropdown, 'touchstart', function () {
                    dropdown.style.fontSize = '16px';
                });
                // Forward events from select to button
                [
                    [H.isMS ? 'mouseover' : 'mouseenter'],
                    [H.isMS ? 'mouseout' : 'mouseleave'],
                    ['change', 'click']
                ].forEach(function (_a) {
                    var from = _a[0],
                        to = _a[1];
                    addEvent(dropdown, from, function () {
                        var button = buttons[_this.currentButtonIndex()];
                        if (button) {
                            fireEvent(button.element, to || from);
                        }
                    });
                });
                this.zoomText = renderer
                    .label((lang && lang.rangeSelectorZoom) || '', 0)
                    .attr({
                    padding: options.buttonTheme.padding,
                    height: options.buttonTheme.height,
                    paddingLeft: 0,
                    paddingRight: 0
                })
                    .add(this.buttonGroup);
                if (!this.chart.styledMode) {
                    this.zoomText.css(options.labelStyle);
                    buttonTheme['stroke-width'] = pick(buttonTheme['stroke-width'], 0);
                }
                createElement('option', {
                    textContent: this.zoomText.textStr,
                    disabled: true
                }, void 0, dropdown);
                this.buttonOptions.forEach(function (rangeOptions, i) {
                    createElement('option', {
                        textContent: rangeOptions.title || rangeOptions.text
                    }, void 0, dropdown);
                    buttons[i] = renderer
                        .button(rangeOptions.text, 0, 0, function (e) {
                        // extract events from button object and call
                        var buttonEvents = (rangeOptions.events && rangeOptions.events.click);
                        var callDefaultEvent;
                        if (buttonEvents) {
                            callDefaultEvent =
                                buttonEvents.call(rangeOptions, e);
                        }
                        if (callDefaultEvent !== false) {
                            _this.clickButton(i);
                        }
                        _this.isActive = true;
                    }, buttonTheme, states && states.hover, states && states.select, states && states.disabled)
                        .attr({
                        'text-align': 'center',
                        width: width
                    })
                        .add(_this.buttonGroup);
                    if (rangeOptions.title) {
                        buttons[i].attr('title', rangeOptions.title);
                    }
                });
            };
            /**
             * Align the elements horizontally and vertically.
             *
             * @private
             * @function Highcharts.RangeSelector#alignElements
             */
            RangeSelector.prototype.alignElements = function () {
                var _this = this;
                var _a = this,
                    buttonGroup = _a.buttonGroup,
                    buttons = _a.buttons,
                    chart = _a.chart,
                    group = _a.group,
                    inputGroup = _a.inputGroup,
                    options = _a.options,
                    zoomText = _a.zoomText;
                var chartOptions = chart.options;
                var navButtonOptions = (chartOptions.exporting &&
                        chartOptions.exporting.enabled !== false &&
                        chartOptions.navigation &&
                        chartOptions.navigation.buttonOptions);
                var buttonPosition = options.buttonPosition,
                    inputPosition = options.inputPosition,
                    verticalAlign = options.verticalAlign;
                // Get the X offset required to avoid overlapping with the exporting
                // button. This is is used both by the buttonGroup and the inputGroup.
                var getXOffsetForExportButton = function (group,
                    position) {
                        if (navButtonOptions &&
                            _this.titleCollision(chart) &&
                            verticalAlign === 'top' &&
                            position.align === 'right' && ((position.y -
                            group.getBBox().height - 12) <
                            ((navButtonOptions.y || 0) +
                                (navButtonOptions.height || 0) +
                                chart.spacing[0]))) {
                            return -40;
                    }
                    return 0;
                };
                var plotLeft = chart.plotLeft;
                if (group && buttonPosition && inputPosition) {
                    var translateX = buttonPosition.x - chart.spacing[3];
                    if (buttonGroup) {
                        this.positionButtons();
                        if (!this.initialButtonGroupWidth) {
                            var width_1 = 0;
                            if (zoomText) {
                                width_1 += zoomText.getBBox().width + 5;
                            }
                            buttons.forEach(function (button, i) {
                                width_1 += button.width;
                                if (i !== buttons.length - 1) {
                                    width_1 += options.buttonSpacing;
                                }
                            });
                            this.initialButtonGroupWidth = width_1;
                        }
                        plotLeft -= chart.spacing[3];
                        this.updateButtonStates();
                        // Detect collision between button group and exporting
                        var xOffsetForExportButton_1 = getXOffsetForExportButton(buttonGroup,
                            buttonPosition);
                        this.alignButtonGroup(xOffsetForExportButton_1);
                        // Skip animation
                        group.placed = buttonGroup.placed = chart.hasLoaded;
                    }
                    var xOffsetForExportButton = 0;
                    if (inputGroup) {
                        // Detect collision between the input group and exporting button
                        xOffsetForExportButton = getXOffsetForExportButton(inputGroup, inputPosition);
                        if (inputPosition.align === 'left') {
                            translateX = plotLeft;
                        }
                        else if (inputPosition.align === 'right') {
                            translateX = -Math.max(chart.axisOffset[1], -xOffsetForExportButton);
                        }
                        // Update the alignment to the updated spacing box
                        inputGroup.align({
                            y: inputPosition.y,
                            width: inputGroup.getBBox().width,
                            align: inputPosition.align,
                            // fix wrong getBBox() value on right align
                            x: inputPosition.x + translateX - 2
                        }, true, chart.spacingBox);
                        // Skip animation
                        inputGroup.placed = chart.hasLoaded;
                    }
                    this.handleCollision(xOffsetForExportButton);
                    // Vertical align
                    group.align({
                        verticalAlign: verticalAlign
                    }, true, chart.spacingBox);
                    var alignTranslateY = group.alignAttr.translateY;
                    // Set position
                    var groupHeight = group.getBBox().height + 20; // # 20 padding
                        var translateY = 0;
                    // Calculate bottom position
                    if (verticalAlign === 'bottom') {
                        var legendOptions = chart.legend && chart.legend.options;
                        var legendHeight = (legendOptions &&
                                legendOptions.verticalAlign === 'bottom' &&
                                legendOptions.enabled &&
                                !legendOptions.floating ?
                                (chart.legend.legendHeight +
                                    pick(legendOptions.margin, 10)) :
                                0);
                        groupHeight = groupHeight + legendHeight - 20;
                        translateY = (alignTranslateY -
                            groupHeight -
                            (options.floating ? 0 : options.y) -
                            (chart.titleOffset ? chart.titleOffset[2] : 0) -
                            10 // 10 spacing
                        );
                    }
                    if (verticalAlign === 'top') {
                        if (options.floating) {
                            translateY = 0;
                        }
                        if (chart.titleOffset && chart.titleOffset[0]) {
                            translateY = chart.titleOffset[0];
                        }
                        translateY += ((chart.margin[0] - chart.spacing[0]) || 0);
                    }
                    else if (verticalAlign === 'middle') {
                        if (inputPosition.y === buttonPosition.y) {
                            translateY = alignTranslateY;
                        }
                        else if (inputPosition.y || buttonPosition.y) {
                            if (inputPosition.y < 0 ||
                                buttonPosition.y < 0) {
                                translateY -= Math.min(inputPosition.y, buttonPosition.y);
                            }
                            else {
                                translateY = alignTranslateY - groupHeight;
                            }
                        }
                    }
                    group.translate(options.x, options.y + Math.floor(translateY));
                    // Translate HTML inputs
                    var _b = this,
                        minInput = _b.minInput,
                        maxInput = _b.maxInput,
                        dropdown = _b.dropdown;
                    if (options.inputEnabled && minInput && maxInput) {
                        minInput.style.marginTop = group.translateY + 'px';
                        maxInput.style.marginTop = group.translateY + 'px';
                    }
                    if (dropdown) {
                        dropdown.style.marginTop = group.translateY + 'px';
                    }
                }
            };
            /**
             * Align the button group horizontally and vertically.
             *
             * @private
             * @function Highcharts.RangeSelector#alignButtonGroup
             * @param {number} xOffsetForExportButton
             * @param {number} [width]
             */
            RangeSelector.prototype.alignButtonGroup = function (xOffsetForExportButton, width) {
                var _a = this,
                    chart = _a.chart,
                    options = _a.options,
                    buttonGroup = _a.buttonGroup,
                    buttons = _a.buttons;
                var buttonPosition = options.buttonPosition;
                var plotLeft = chart.plotLeft - chart.spacing[3];
                var translateX = buttonPosition.x - chart.spacing[3];
                if (buttonPosition.align === 'right') {
                    translateX += xOffsetForExportButton - plotLeft; // #13014
                }
                else if (buttonPosition.align === 'center') {
                    translateX -= plotLeft / 2;
                }
                if (buttonGroup) {
                    // Align button group
                    buttonGroup.align({
                        y: buttonPosition.y,
                        width: pick(width, this.initialButtonGroupWidth),
                        align: buttonPosition.align,
                        x: translateX
                    }, true, chart.spacingBox);
                }
            };
            /**
             * @private
             * @function Highcharts.RangeSelector#positionButtons
             */
            RangeSelector.prototype.positionButtons = function () {
                var _a = this,
                    buttons = _a.buttons,
                    chart = _a.chart,
                    options = _a.options,
                    zoomText = _a.zoomText;
                var verb = chart.hasLoaded ? 'animate' : 'attr';
                var buttonPosition = options.buttonPosition;
                var plotLeft = chart.plotLeft;
                var buttonLeft = plotLeft;
                if (zoomText && zoomText.visibility !== 'hidden') {
                    // #8769, allow dynamically updating margins
                    zoomText[verb]({
                        x: pick(plotLeft + buttonPosition.x, plotLeft)
                    });
                    // Button start position
                    buttonLeft += buttonPosition.x +
                        zoomText.getBBox().width + 5;
                }
                for (var i = 0, iEnd = this.buttonOptions.length; i < iEnd; ++i) {
                    if (buttons[i].visibility !== 'hidden') {
                        buttons[i][verb]({ x: buttonLeft });
                        // increase button position for the next button
                        buttonLeft += buttons[i].width + options.buttonSpacing;
                    }
                    else {
                        buttons[i][verb]({ x: plotLeft });
                    }
                }
            };
            /**
             * Handle collision between the button group and the input group
             *
             * @private
             * @function Highcharts.RangeSelector#handleCollision
             *
             * @param  {number} xOffsetForExportButton
             *                  The X offset of the group required to make room for the
             *                  exporting button
             */
            RangeSelector.prototype.handleCollision = function (xOffsetForExportButton) {
                var _this = this;
                var _a = this,
                    chart = _a.chart,
                    buttonGroup = _a.buttonGroup,
                    inputGroup = _a.inputGroup;
                var _b = this.options,
                    buttonPosition = _b.buttonPosition,
                    dropdown = _b.dropdown,
                    inputPosition = _b.inputPosition;
                var maxButtonWidth = function () {
                        var buttonWidth = 0;
                    _this.buttons.forEach(function (button) {
                        var bBox = button.getBBox();
                        if (bBox.width > buttonWidth) {
                            buttonWidth = bBox.width;
                        }
                    });
                    return buttonWidth;
                };
                var groupsOverlap = function (buttonGroupWidth) {
                        if (inputGroup && buttonGroup) {
                            var inputGroupX = (inputGroup.alignAttr.translateX +
                                inputGroup.alignOptions.x -
                                xOffsetForExportButton +
                                // getBBox for detecing left margin
                                inputGroup.getBBox().x +
                                // 2px padding to not overlap input and label
                                2);
                        var inputGroupWidth = inputGroup.alignOptions.width;
                        var buttonGroupX = buttonGroup.alignAttr.translateX +
                                buttonGroup.getBBox().x;
                        return (buttonGroupX + buttonGroupWidth > inputGroupX) &&
                            (inputGroupX + inputGroupWidth > buttonGroupX) &&
                            (buttonPosition.y <
                                (inputPosition.y +
                                    inputGroup.getBBox().height));
                    }
                    return false;
                };
                var moveInputsDown = function () {
                        if (inputGroup && buttonGroup) {
                            inputGroup.attr({
                                translateX: inputGroup.alignAttr.translateX + (chart.axisOffset[1] >= -xOffsetForExportButton ?
                                    0 :
                                    -xOffsetForExportButton),
                                translateY: inputGroup.alignAttr.translateY +
                                    buttonGroup.getBBox().height + 10
                            });
                    }
                };
                if (buttonGroup) {
                    if (dropdown === 'always') {
                        this.collapseButtons(xOffsetForExportButton);
                        if (groupsOverlap(maxButtonWidth())) {
                            // Move the inputs down if there is still a collision
                            // after collapsing the buttons
                            moveInputsDown();
                        }
                        return;
                    }
                    if (dropdown === 'never') {
                        this.expandButtons();
                    }
                }
                // Detect collision
                if (inputGroup && buttonGroup) {
                    if ((inputPosition.align === buttonPosition.align) ||
                        // 20 is minimal spacing between elements
                        groupsOverlap(this.initialButtonGroupWidth + 20)) {
                        if (dropdown === 'responsive') {
                            this.collapseButtons(xOffsetForExportButton);
                            if (groupsOverlap(maxButtonWidth())) {
                                moveInputsDown();
                            }
                        }
                        else {
                            moveInputsDown();
                        }
                    }
                    else if (dropdown === 'responsive') {
                        this.expandButtons();
                    }
                }
                else if (buttonGroup && dropdown === 'responsive') {
                    if (this.initialButtonGroupWidth > chart.plotWidth) {
                        this.collapseButtons(xOffsetForExportButton);
                    }
                    else {
                        this.expandButtons();
                    }
                }
            };
            /**
             * Collapse the buttons and put the select element on top.
             *
             * @private
             * @function Highcharts.RangeSelector#collapseButtons
             * @param {number} xOffsetForExportButton
             */
            RangeSelector.prototype.collapseButtons = function (xOffsetForExportButton) {
                var _a = this,
                    buttons = _a.buttons,
                    buttonOptions = _a.buttonOptions,
                    chart = _a.chart,
                    dropdown = _a.dropdown,
                    options = _a.options,
                    zoomText = _a.zoomText;
                var userButtonTheme = (chart.userOptions.rangeSelector &&
                        chart.userOptions.rangeSelector.buttonTheme) || {};
                var getAttribs = function (text) { return ({
                        text: text ? "" + text + " \u25BE" : '▾',
                        width: 'auto',
                        paddingLeft: pick(options.buttonTheme.paddingLeft,
                    userButtonTheme.padding, 8),
                        paddingRight: pick(options.buttonTheme.paddingRight,
                    userButtonTheme.padding, 8)
                    }); };
                if (zoomText) {
                    zoomText.hide();
                }
                var hasActiveButton = false;
                buttonOptions.forEach(function (rangeOptions, i) {
                    var button = buttons[i];
                    if (button.state !== 2) {
                        button.hide();
                    }
                    else {
                        button.show();
                        button.attr(getAttribs(rangeOptions.text));
                        hasActiveButton = true;
                    }
                });
                if (!hasActiveButton) {
                    if (dropdown) {
                        dropdown.selectedIndex = 0;
                    }
                    buttons[0].show();
                    buttons[0].attr(getAttribs(this.zoomText && this.zoomText.textStr));
                }
                var align = options.buttonPosition.align;
                this.positionButtons();
                if (align === 'right' || align === 'center') {
                    this.alignButtonGroup(xOffsetForExportButton, buttons[this.currentButtonIndex()].getBBox().width);
                }
                this.showDropdown();
            };
            /**
             * Show all the buttons and hide the select element.
             *
             * @private
             * @function Highcharts.RangeSelector#expandButtons
             */
            RangeSelector.prototype.expandButtons = function () {
                var _a = this,
                    buttons = _a.buttons,
                    buttonOptions = _a.buttonOptions,
                    options = _a.options,
                    zoomText = _a.zoomText;
                this.hideDropdown();
                if (zoomText) {
                    zoomText.show();
                }
                buttonOptions.forEach(function (rangeOptions, i) {
                    var button = buttons[i];
                    button.show();
                    button.attr({
                        text: rangeOptions.text,
                        width: options.buttonTheme.width || 28,
                        paddingLeft: pick(options.buttonTheme.paddingLeft, 'unset'),
                        paddingRight: pick(options.buttonTheme.paddingRight, 'unset')
                    });
                    if (button.state < 2) {
                        button.setState(0);
                    }
                });
                this.positionButtons();
            };
            /**
             * Get the index of the visible button when the buttons are collapsed.
             *
             * @private
             * @function Highcharts.RangeSelector#currentButtonIndex
             */
            RangeSelector.prototype.currentButtonIndex = function () {
                var dropdown = this.dropdown;
                if (dropdown && dropdown.selectedIndex > 0) {
                    return dropdown.selectedIndex - 1;
                }
                return 0;
            };
            /**
             * Position the select element on top of the button.
             *
             * @private
             * @function Highcharts.RangeSelector#showDropdown
             */
            RangeSelector.prototype.showDropdown = function () {
                var _a = this,
                    buttonGroup = _a.buttonGroup,
                    buttons = _a.buttons,
                    chart = _a.chart,
                    dropdown = _a.dropdown;
                if (buttonGroup && dropdown) {
                    var translateX = buttonGroup.translateX,
                        translateY = buttonGroup.translateY;
                    var bBox = buttons[this.currentButtonIndex()].getBBox();
                    css(dropdown, {
                        left: (chart.plotLeft + translateX) + 'px',
                        top: (translateY + 0.5) + 'px',
                        width: bBox.width + 'px',
                        height: bBox.height + 'px'
                    });
                    this.hasVisibleDropdown = true;
                }
            };
            /**
             * @private
             * @function Highcharts.RangeSelector#hideDropdown
             */
            RangeSelector.prototype.hideDropdown = function () {
                var dropdown = this.dropdown;
                if (dropdown) {
                    css(dropdown, {
                        top: '-9999em',
                        width: '1px',
                        height: '1px'
                    });
                    this.hasVisibleDropdown = false;
                }
            };
            /**
             * Extracts height of range selector
             *
             * @private
             * @function Highcharts.RangeSelector#getHeight
             * @return {number}
             * Returns rangeSelector height
             */
            RangeSelector.prototype.getHeight = function () {
                var rangeSelector = this,
                    options = rangeSelector.options,
                    rangeSelectorGroup = rangeSelector.group,
                    inputPosition = options.inputPosition,
                    buttonPosition = options.buttonPosition,
                    yPosition = options.y,
                    buttonPositionY = buttonPosition.y,
                    inputPositionY = inputPosition.y;
                var rangeSelectorHeight = 0;
                if (options.height) {
                    return options.height;
                }
                // Align the elements before we read the height in case we're switching
                // between wrapped and non-wrapped layout
                this.alignElements();
                rangeSelectorHeight = rangeSelectorGroup ?
                    // 13px to keep back compatibility
                    (rangeSelectorGroup.getBBox(true).height) + 13 +
                        yPosition :
                    0;
                var minPosition = Math.min(inputPositionY,
                    buttonPositionY);
                if ((inputPositionY < 0 && buttonPositionY < 0) ||
                    (inputPositionY > 0 && buttonPositionY > 0)) {
                    rangeSelectorHeight += Math.abs(minPosition);
                }
                return rangeSelectorHeight;
            };
            /**
             * Detect collision with title or subtitle
             *
             * @private
             * @function Highcharts.RangeSelector#titleCollision
             * @return {boolean}
             * Returns collision status
             */
            RangeSelector.prototype.titleCollision = function (chart) {
                return !(chart.options.title.text ||
                    chart.options.subtitle.text);
            };
            /**
             * Update the range selector with new options
             *
             * @private
             * @function Highcharts.RangeSelector#update
             * @param {Highcharts.RangeSelectorOptions} options
             */
            RangeSelector.prototype.update = function (options) {
                var chart = this.chart;
                merge(true, chart.options.rangeSelector, options);
                this.destroy();
                this.init(chart);
                this.render();
            };
            /**
             * Destroys allocated elements.
             *
             * @private
             * @function Highcharts.RangeSelector#destroy
             */
            RangeSelector.prototype.destroy = function () {
                var rSelector = this,
                    minInput = rSelector.minInput,
                    maxInput = rSelector.maxInput;
                if (rSelector.eventsToUnbind) {
                    rSelector.eventsToUnbind.forEach(function (unbind) { return unbind(); });
                    rSelector.eventsToUnbind = void 0;
                }
                // Destroy elements in collections
                destroyObjectProperties(rSelector.buttons);
                // Clear input element events
                if (minInput) {
                    minInput.onfocus = minInput.onblur = minInput.onchange = null;
                }
                if (maxInput) {
                    maxInput.onfocus = maxInput.onblur = maxInput.onchange = null;
                }
                // Destroy HTML and SVG elements
                objectEach(rSelector, function (val, key) {
                    if (val && key !== 'chart') {
                        if (val instanceof SVGElement) {
                            // SVGElement
                            val.destroy();
                        }
                        else if (val instanceof window.HTMLElement) {
                            // HTML element
                            discardElement(val);
                        }
                    }
                    if (val !== RangeSelector.prototype[key]) {
                        rSelector[key] = null;
                    }
                }, this);
            };
            return RangeSelector;
        }());
        extend(RangeSelector.prototype, {
            /**
             * The default buttons for pre-selecting time frames.
             * @private
             */
            defaultButtons: [{
                    type: 'month',
                    count: 1,
                    text: '1m',
                    title: 'View 1 month'
                }, {
                    type: 'month',
                    count: 3,
                    text: '3m',
                    title: 'View 3 months'
                }, {
                    type: 'month',
                    count: 6,
                    text: '6m',
                    title: 'View 6 months'
                }, {
                    type: 'ytd',
                    text: 'YTD',
                    title: 'View year to date'
                }, {
                    type: 'year',
                    count: 1,
                    text: '1y',
                    title: 'View 1 year'
                }, {
                    type: 'all',
                    text: 'All',
                    title: 'View all'
                }],
            /**
             * The date formats to use when setting min, max and value on date inputs.
             * @private
             */
            inputTypeFormats: {
                'datetime-local': '%Y-%m-%dT%H:%M:%S',
                'date': '%Y-%m-%d',
                'time': '%H:%M:%S'
            }
        });
        /* *
         *
         *  Default Export
         *
         * */
        /* *
         *
         *  API Options
         *
         * */
        /**
         * Define the time span for the button
         *
         * @typedef {"all"|"day"|"hour"|"millisecond"|"minute"|"month"|"second"|"week"|"year"|"ytd"} Highcharts.RangeSelectorButtonTypeValue
         */
        /**
         * Callback function to react on button clicks.
         *
         * @callback Highcharts.RangeSelectorClickCallbackFunction
         *
         * @param {global.Event} e
         *        Event arguments.
         *
         * @param {boolean|undefined}
         *        Return false to cancel the default button event.
         */
        /**
         * Callback function to parse values entered in the input boxes and return a
         * valid JavaScript time as milliseconds since 1970.
         *
         * @callback Highcharts.RangeSelectorParseCallbackFunction
         *
         * @param {string} value
         *        Input value to parse.
         *
         * @return {number}
         *         Parsed JavaScript time value.
         */
        (''); // keeps doclets above in JS file

        return RangeSelector;
    });
    _registerModule(_modules, 'Accessibility/Components/RangeSelectorComponent.js', [_modules['Stock/RangeSelector/RangeSelector.js'], _modules['Accessibility/AccessibilityComponent.js'], _modules['Accessibility/Utils/ChartUtilities.js'], _modules['Accessibility/Utils/Announcer.js'], _modules['Accessibility/KeyboardNavigationHandler.js'], _modules['Core/Utilities.js']], function (RangeSelector, AccessibilityComponent, ChartUtilities, Announcer, KeyboardNavigationHandler, U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Accessibility component for the range selector.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var __extends = (this && this.__extends) || (function () {
                var extendStatics = function (d,
            b) {
                    extendStatics = Object.setPrototypeOf ||
                        ({ __proto__: [] } instanceof Array && function (d,
            b) { d.__proto__ = b; }) ||
                        function (d,
            b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
                return extendStatics(d, b);
            };
            return function (d, b) {
                extendStatics(d, b);
                function __() { this.constructor = d; }
                d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
            };
        })();
        var unhideChartElementFromAT = ChartUtilities.unhideChartElementFromAT,
            getAxisRangeDescription = ChartUtilities.getAxisRangeDescription;
        var addEvent = U.addEvent,
            attr = U.attr;
        /* *
         *
         *  Functions
         *
         * */
        /* eslint-disable valid-jsdoc */
        /**
         * @private
         */
        function shouldRunInputNavigation(chart) {
            return Boolean(chart.rangeSelector &&
                chart.rangeSelector.inputGroup &&
                chart.rangeSelector.inputGroup.element.style.visibility !== 'hidden' &&
                chart.options.rangeSelector.inputEnabled !== false &&
                chart.rangeSelector.minInput &&
                chart.rangeSelector.maxInput);
        }
        /* *
         *
         *  Class
         *
         * */
        /**
         * The RangeSelectorComponent class
         *
         * @private
         * @class
         * @name Highcharts.RangeSelectorComponent
         */
        var RangeSelectorComponent = /** @class */ (function (_super) {
                __extends(RangeSelectorComponent, _super);
            function RangeSelectorComponent() {
                /* *
                 *
                 *  Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.announcer = void 0;
                return _this;
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Init the component
             * @private
             */
            RangeSelectorComponent.prototype.init = function () {
                var chart = this.chart;
                this.announcer = new Announcer(chart, 'polite');
            };
            /**
             * Called on first render/updates to the chart, including options changes.
             */
            RangeSelectorComponent.prototype.onChartUpdate = function () {
                var chart = this.chart,
                    component = this,
                    rangeSelector = chart.rangeSelector;
                if (!rangeSelector) {
                    return;
                }
                this.updateSelectorVisibility();
                this.setDropdownAttrs();
                if (rangeSelector.buttons &&
                    rangeSelector.buttons.length) {
                    rangeSelector.buttons.forEach(function (button) {
                        component.setRangeButtonAttrs(button);
                    });
                }
                // Make sure input boxes are accessible and focusable
                if (rangeSelector.maxInput && rangeSelector.minInput) {
                    ['minInput', 'maxInput'].forEach(function (key, i) {
                        var input = rangeSelector[key];
                        if (input) {
                            unhideChartElementFromAT(chart, input);
                            component.setRangeInputAttrs(input, 'accessibility.rangeSelector.' + (i ? 'max' : 'min') +
                                'InputLabel');
                        }
                    });
                }
            };
            /**
             * Hide buttons from AT when showing dropdown, and vice versa.
             * @private
             */
            RangeSelectorComponent.prototype.updateSelectorVisibility = function () {
                var chart = this.chart;
                var rangeSelector = chart.rangeSelector;
                var dropdown = (rangeSelector &&
                        rangeSelector.dropdown);
                var buttons = (rangeSelector &&
                        rangeSelector.buttons ||
                        []);
                var hideFromAT = function (el) { return el.setAttribute('aria-hidden',
                    true); };
                if (rangeSelector &&
                    rangeSelector.hasVisibleDropdown &&
                    dropdown) {
                    unhideChartElementFromAT(chart, dropdown);
                    buttons.forEach(function (btn) { return hideFromAT(btn.element); });
                }
                else {
                    if (dropdown) {
                        hideFromAT(dropdown);
                    }
                    buttons.forEach(function (btn) { return unhideChartElementFromAT(chart, btn.element); });
                }
            };
            /**
             * Set accessibility related attributes on dropdown element.
             * @private
             */
            RangeSelectorComponent.prototype.setDropdownAttrs = function () {
                var chart = this.chart;
                var dropdown = (chart.rangeSelector &&
                        chart.rangeSelector.dropdown);
                if (dropdown) {
                    var label = chart.langFormat('accessibility.rangeSelector.dropdownLabel', { rangeTitle: chart.options.lang.rangeSelectorZoom });
                    dropdown.setAttribute('aria-label', label);
                    dropdown.setAttribute('tabindex', -1);
                }
            };
            /**
             * @private
             * @param {Highcharts.SVGElement} button
             */
            RangeSelectorComponent.prototype.setRangeButtonAttrs = function (button) {
                attr(button.element, {
                    tabindex: -1,
                    role: 'button'
                });
            };
            /**
             * @private
             */
            RangeSelectorComponent.prototype.setRangeInputAttrs = function (input, langKey) {
                var chart = this.chart;
                attr(input, {
                    tabindex: -1,
                    'aria-label': chart.langFormat(langKey, { chart: chart })
                });
            };
            /**
             * @private
             * @param {Highcharts.KeyboardNavigationHandler} keyboardNavigationHandler
             * @param {number} keyCode
             * @return {number} Response code
             */
            RangeSelectorComponent.prototype.onButtonNavKbdArrowKey = function (keyboardNavigationHandler, keyCode) {
                var response = keyboardNavigationHandler.response,
                    keys = this.keyCodes,
                    chart = this.chart,
                    wrapAround = chart.options.accessibility
                        .keyboardNavigation.wrapAround,
                    direction = (keyCode === keys.left || keyCode === keys.up) ? -1 : 1,
                    didHighlight = chart.highlightRangeSelectorButton(chart.highlightedRangeSelectorItemIx + direction);
                if (!didHighlight) {
                    if (wrapAround) {
                        keyboardNavigationHandler.init(direction);
                        return response.success;
                    }
                    return response[direction > 0 ? 'next' : 'prev'];
                }
                return response.success;
            };
            /**
             * @private
             */
            RangeSelectorComponent.prototype.onButtonNavKbdClick = function (keyboardNavigationHandler) {
                var response = keyboardNavigationHandler.response,
                    chart = this.chart,
                    wasDisabled = chart.oldRangeSelectorItemState === 3;
                if (!wasDisabled) {
                    this.fakeClickEvent(chart.rangeSelector.buttons[chart.highlightedRangeSelectorItemIx].element);
                }
                return response.success;
            };
            /**
             * Called whenever a range selector button has been clicked, either by
             * mouse, touch, or kbd/voice/other.
             * @private
             */
            RangeSelectorComponent.prototype.onAfterBtnClick = function () {
                var chart = this.chart;
                var axisRangeDescription = getAxisRangeDescription(chart.xAxis[0]);
                var announcement = chart.langFormat('accessibility.rangeSelector.clickButtonAnnouncement', { chart: chart,
                    axisRangeDescription: axisRangeDescription });
                if (announcement) {
                    this.announcer.announce(announcement);
                }
            };
            /**
             * @private
             */
            RangeSelectorComponent.prototype.onInputKbdMove = function (direction) {
                var chart = this.chart;
                var rangeSel = chart.rangeSelector;
                var newIx = chart.highlightedInputRangeIx = (chart.highlightedInputRangeIx || 0) + direction;
                var newIxOutOfRange = newIx > 1 || newIx < 0;
                if (newIxOutOfRange) {
                    if (chart.accessibility) {
                        chart.accessibility.keyboardNavigation.tabindexContainer
                            .focus();
                        chart.accessibility.keyboardNavigation.move(direction);
                    }
                }
                else if (rangeSel) {
                    var svgEl = rangeSel[newIx ? 'maxDateBox' : 'minDateBox'];
                    var inputEl = rangeSel[newIx ? 'maxInput' : 'minInput'];
                    if (svgEl && inputEl) {
                        chart.setFocusToElement(svgEl, inputEl);
                    }
                }
            };
            /**
             * @private
             * @param {number} direction
             */
            RangeSelectorComponent.prototype.onInputNavInit = function (direction) {
                var _this = this;
                var component = this;
                var chart = this.chart;
                var buttonIxToHighlight = direction > 0 ? 0 : 1;
                var rangeSel = chart.rangeSelector;
                var svgEl = (rangeSel &&
                        rangeSel[buttonIxToHighlight ? 'maxDateBox' : 'minDateBox']);
                var minInput = (rangeSel && rangeSel.minInput);
                var maxInput = (rangeSel && rangeSel.maxInput);
                var inputEl = buttonIxToHighlight ? maxInput : minInput;
                chart.highlightedInputRangeIx = buttonIxToHighlight;
                if (svgEl && minInput && maxInput) {
                    chart.setFocusToElement(svgEl, inputEl);
                    // Tab-press with the input focused does not propagate to chart
                    // automatically, so we manually catch and handle it when relevant.
                    if (this.removeInputKeydownHandler) {
                        this.removeInputKeydownHandler();
                    }
                    var keydownHandler = function (e) {
                            var isTab = (e.which || e.keyCode) === _this.keyCodes.tab;
                        if (isTab) {
                            e.preventDefault();
                            e.stopPropagation();
                            component.onInputKbdMove(e.shiftKey ? -1 : 1);
                        }
                    };
                    var minRemover_1 = addEvent(minInput, 'keydown',
                        keydownHandler);
                    var maxRemover_1 = addEvent(maxInput, 'keydown',
                        keydownHandler);
                    this.removeInputKeydownHandler = function () {
                        minRemover_1();
                        maxRemover_1();
                    };
                }
            };
            /**
             * @private
             */
            RangeSelectorComponent.prototype.onInputNavTerminate = function () {
                var rangeSel = (this.chart.rangeSelector || {});
                if (rangeSel.maxInput) {
                    rangeSel.hideInput('max');
                }
                if (rangeSel.minInput) {
                    rangeSel.hideInput('min');
                }
                if (this.removeInputKeydownHandler) {
                    this.removeInputKeydownHandler();
                    delete this.removeInputKeydownHandler;
                }
            };
            /**
             * @private
             */
            RangeSelectorComponent.prototype.initDropdownNav = function () {
                var _this = this;
                var chart = this.chart;
                var rangeSelector = chart.rangeSelector;
                var dropdown = (rangeSelector && rangeSelector.dropdown);
                if (rangeSelector && dropdown) {
                    chart.setFocusToElement(rangeSelector.buttonGroup, dropdown);
                    if (this.removeDropdownKeydownHandler) {
                        this.removeDropdownKeydownHandler();
                    }
                    // Tab-press with dropdown focused does not propagate to chart
                    // automatically, so we manually catch and handle it when relevant.
                    this.removeDropdownKeydownHandler = addEvent(dropdown, 'keydown', function (e) {
                        var isTab = (e.which || e.keyCode) === _this.keyCodes.tab,
                            a11y = chart.accessibility;
                        if (isTab) {
                            e.preventDefault();
                            e.stopPropagation();
                            if (a11y) {
                                a11y.keyboardNavigation.tabindexContainer.focus();
                                a11y.keyboardNavigation.move(e.shiftKey ? -1 : 1);
                            }
                        }
                    });
                }
            };
            /**
             * Get navigation for the range selector buttons.
             * @private
             * @return {Highcharts.KeyboardNavigationHandler} The module object.
             */
            RangeSelectorComponent.prototype.getRangeSelectorButtonNavigation = function () {
                var chart = this.chart;
                var keys = this.keyCodes;
                var component = this;
                return new KeyboardNavigationHandler(chart, {
                    keyCodeMap: [
                        [
                            [keys.left, keys.right, keys.up, keys.down],
                            function (keyCode) {
                                return component.onButtonNavKbdArrowKey(this, keyCode);
                            }
                        ],
                        [
                            [keys.enter, keys.space],
                            function () {
                                return component.onButtonNavKbdClick(this);
                            }
                        ]
                    ],
                    validate: function () {
                        return !!(chart.rangeSelector &&
                            chart.rangeSelector.buttons &&
                            chart.rangeSelector.buttons.length);
                    },
                    init: function (direction) {
                        var rangeSelector = chart.rangeSelector;
                        if (rangeSelector && rangeSelector.hasVisibleDropdown) {
                            component.initDropdownNav();
                        }
                        else if (rangeSelector) {
                            var lastButtonIx = rangeSelector.buttons.length - 1;
                            chart.highlightRangeSelectorButton(direction > 0 ? 0 : lastButtonIx);
                        }
                    },
                    terminate: function () {
                        if (component.removeDropdownKeydownHandler) {
                            component.removeDropdownKeydownHandler();
                            delete component.removeDropdownKeydownHandler;
                        }
                    }
                });
            };
            /**
             * Get navigation for the range selector input boxes.
             * @private
             * @return {Highcharts.KeyboardNavigationHandler}
             *         The module object.
             */
            RangeSelectorComponent.prototype.getRangeSelectorInputNavigation = function () {
                var chart = this.chart;
                var component = this;
                return new KeyboardNavigationHandler(chart, {
                    keyCodeMap: [],
                    validate: function () {
                        return shouldRunInputNavigation(chart);
                    },
                    init: function (direction) {
                        component.onInputNavInit(direction);
                    },
                    terminate: function () {
                        component.onInputNavTerminate();
                    }
                });
            };
            /**
             * Get keyboard navigation handlers for this component.
             * @return {Array<Highcharts.KeyboardNavigationHandler>}
             *         List of module objects.
             */
            RangeSelectorComponent.prototype.getKeyboardNavigation = function () {
                return [
                    this.getRangeSelectorButtonNavigation(),
                    this.getRangeSelectorInputNavigation()
                ];
            };
            /**
             * Remove component traces
             */
            RangeSelectorComponent.prototype.destroy = function () {
                if (this.removeDropdownKeydownHandler) {
                    this.removeDropdownKeydownHandler();
                }
                if (this.removeInputKeydownHandler) {
                    this.removeInputKeydownHandler();
                }
                if (this.announcer) {
                    this.announcer.destroy();
                }
            };
            return RangeSelectorComponent;
        }(AccessibilityComponent));
        /* *
         *
         *  Class Namespace
         *
         * */
        (function (RangeSelectorComponent) {
            /* *
             *
             *  Declarations
             *
             * */
            /* *
             *
             *  Constants
             *
             * */
            var composedClasses = [];
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Highlight range selector button by index.
             *
             * @private
             * @function Highcharts.Chart#highlightRangeSelectorButton
             */
            function chartHighlightRangeSelectorButton(ix) {
                var buttons = (this.rangeSelector &&
                        this.rangeSelector.buttons ||
                        []);
                var curHighlightedIx = this.highlightedRangeSelectorItemIx;
                var curSelectedIx = (this.rangeSelector &&
                        this.rangeSelector.selected);
                // Deselect old
                if (typeof curHighlightedIx !== 'undefined' &&
                    buttons[curHighlightedIx] &&
                    curHighlightedIx !== curSelectedIx) {
                    buttons[curHighlightedIx].setState(this.oldRangeSelectorItemState || 0);
                }
                // Select new
                this.highlightedRangeSelectorItemIx = ix;
                if (buttons[ix]) {
                    this.setFocusToElement(buttons[ix].box, buttons[ix].element);
                    if (ix !== curSelectedIx) {
                        this.oldRangeSelectorItemState = buttons[ix].state;
                        buttons[ix].setState(1);
                    }
                    return true;
                }
                return false;
            }
            /**
             * @private
             */
            function compose(ChartClass, RangeSelectorClass) {
                if (composedClasses.indexOf(ChartClass) === -1) {
                    composedClasses.push(ChartClass);
                    var chartProto = ChartClass.prototype;
                    chartProto.highlightRangeSelectorButton = (chartHighlightRangeSelectorButton);
                }
                if (composedClasses.indexOf(RangeSelectorClass) === -1) {
                    composedClasses.push(RangeSelectorClass);
                    addEvent(RangeSelector, 'afterBtnClick', rangeSelectorAfterBtnClick);
                }
            }
            RangeSelectorComponent.compose = compose;
            /**
             * Range selector does not have destroy-setup for class instance events - so
             * we set it on the class and call the component from here.
             * @private
             */
            function rangeSelectorAfterBtnClick() {
                var a11y = this.chart.accessibility;
                if (a11y && a11y.components.rangeSelector) {
                    return a11y.components.rangeSelector.onAfterBtnClick();
                }
            }
        })(RangeSelectorComponent || (RangeSelectorComponent = {}));
        /* *
         *
         *  Export Default
         *
         * */

        return RangeSelectorComponent;
    });
    _registerModule(_modules, 'Accessibility/Components/SeriesComponent/ForcedMarkers.js', [_modules['Core/Utilities.js']], function (U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Handle forcing series markers.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var addEvent = U.addEvent,
            merge = U.merge;
        /* *
         *
         *  Composition
         *
         * */
        var ForcedMarkersComposition;
        (function (ForcedMarkersComposition) {
            /* *
             *
             *  Declarations
             *
             * */
            /* *
             *
             *  Compositions
             *
             * */
            var composedClasses = [];
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * @private
             */
            function compose(SeriesClass) {
                if (composedClasses.indexOf(SeriesClass) === -1) {
                    composedClasses.push(SeriesClass);
                    addEvent(SeriesClass, 'afterSetOptions', seriesOnAfterSetOptions);
                    addEvent(SeriesClass, 'render', seriesOnRender);
                    addEvent(SeriesClass, 'afterRender', seriesOnAfterRender);
                }
            }
            ForcedMarkersComposition.compose = compose;
            /**
             * @private
             */
            function forceZeroOpacityMarkerOptions(options) {
                merge(true, options, {
                    marker: {
                        enabled: true,
                        states: {
                            normal: {
                                opacity: 0
                            }
                        }
                    }
                });
            }
            /**
             * @private
             */
            function getPointMarkerOpacity(pointOptions) {
                return pointOptions.marker.states &&
                    pointOptions.marker.states.normal &&
                    pointOptions.marker.states.normal.opacity;
            }
            /**
             * @private
             */
            function handleForcePointMarkers(series) {
                var i = series.points.length;
                while (i--) {
                    var point = series.points[i];
                    var pointOptions = point.options;
                    var hadForcedMarker = point.hasForcedA11yMarker;
                    delete point.hasForcedA11yMarker;
                    if (pointOptions.marker) {
                        var isStillForcedMarker = hadForcedMarker &&
                                getPointMarkerOpacity(pointOptions) === 0;
                        if (pointOptions.marker.enabled && !isStillForcedMarker) {
                            unforcePointMarkerOptions(pointOptions);
                            point.hasForcedA11yMarker = false;
                        }
                        else if (pointOptions.marker.enabled === false) {
                            forceZeroOpacityMarkerOptions(pointOptions);
                            point.hasForcedA11yMarker = true;
                        }
                    }
                }
            }
            /**
             * @private
             */
            function hasIndividualPointMarkerOptions(series) {
                return !!(series._hasPointMarkers &&
                    series.points &&
                    series.points.length);
            }
            /**
             * @private
             */
            function isWithinDescriptionThreshold(series) {
                var a11yOptions = series.chart.options.accessibility;
                return series.points.length <
                    a11yOptions.series.pointDescriptionEnabledThreshold ||
                    a11yOptions.series
                        .pointDescriptionEnabledThreshold === false;
            }
            /**
             * Process marker graphics after render
             * @private
             */
            function seriesOnAfterRender() {
                var series = this;
                // For styled mode the rendered graphic does not reflect the style
                // options, and we need to add/remove classes to achieve the same.
                if (series.chart.styledMode) {
                    if (series.markerGroup) {
                        series.markerGroup[series.a11yMarkersForced ? 'addClass' : 'removeClass']('highcharts-a11y-markers-hidden');
                    }
                    // Do we need to handle individual points?
                    if (hasIndividualPointMarkerOptions(series)) {
                        series.points.forEach(function (point) {
                            if (point.graphic) {
                                point.graphic[point.hasForcedA11yMarker ?
                                    'addClass' : 'removeClass']('highcharts-a11y-marker-hidden');
                                point.graphic[point.hasForcedA11yMarker === false ?
                                    'addClass' :
                                    'removeClass']('highcharts-a11y-marker-visible');
                            }
                        });
                    }
                }
            }
            /**
             * Keep track of options to reset markers to if no longer forced.
             * @private
             */
            function seriesOnAfterSetOptions(e) {
                this.resetA11yMarkerOptions = merge(e.options.marker || {}, this.userOptions.marker || {});
            }
            /**
             * Keep track of forcing markers.
             * @private
             */
            function seriesOnRender() {
                var series = this,
                    options = series.options;
                if (shouldForceMarkers(series)) {
                    if (options.marker && options.marker.enabled === false) {
                        series.a11yMarkersForced = true;
                        forceZeroOpacityMarkerOptions(series.options);
                    }
                    if (hasIndividualPointMarkerOptions(series)) {
                        handleForcePointMarkers(series);
                    }
                }
                else if (series.a11yMarkersForced) {
                    delete series.a11yMarkersForced;
                    unforceSeriesMarkerOptions(series);
                    delete series.resetA11yMarkerOptions;
                }
            }
            /**
             * @private
             */
            function shouldForceMarkers(series) {
                var chart = series.chart,
                    chartA11yEnabled = chart.options.accessibility.enabled,
                    seriesA11yEnabled = (series.options.accessibility &&
                        series.options.accessibility.enabled) !== false;
                return (chartA11yEnabled &&
                    seriesA11yEnabled &&
                    isWithinDescriptionThreshold(series));
            }
            /**
             * @private
             */
            function unforcePointMarkerOptions(pointOptions) {
                merge(true, pointOptions.marker, {
                    states: {
                        normal: {
                            opacity: getPointMarkerOpacity(pointOptions) || 1
                        }
                    }
                });
            }
            /**
             * Reset markers to normal
             * @private
             */
            function unforceSeriesMarkerOptions(series) {
                var resetMarkerOptions = series.resetA11yMarkerOptions;
                if (resetMarkerOptions) {
                    var originalOpactiy = resetMarkerOptions.states &&
                            resetMarkerOptions.states.normal &&
                            resetMarkerOptions.states.normal.opacity;
                    series.update({
                        marker: {
                            enabled: resetMarkerOptions.enabled,
                            states: {
                                normal: { opacity: originalOpactiy }
                            }
                        }
                    });
                }
            }
        })(ForcedMarkersComposition || (ForcedMarkersComposition = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return ForcedMarkersComposition;
    });
    _registerModule(_modules, 'Accessibility/Components/SeriesComponent/SeriesKeyboardNavigation.js', [_modules['Core/Series/Point.js'], _modules['Core/Series/Series.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Globals.js'], _modules['Core/Utilities.js'], _modules['Accessibility/KeyboardNavigationHandler.js'], _modules['Accessibility/Utils/EventProvider.js'], _modules['Accessibility/Utils/ChartUtilities.js']], function (Point, Series, SeriesRegistry, H, U, KeyboardNavigationHandler, EventProvider, ChartUtilities) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Handle keyboard navigation for series.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var seriesTypes = SeriesRegistry.seriesTypes;
        var doc = H.doc;
        var defined = U.defined,
            fireEvent = U.fireEvent;
        var getPointFromXY = ChartUtilities.getPointFromXY,
            getSeriesFromName = ChartUtilities.getSeriesFromName,
            scrollToPoint = ChartUtilities.scrollToPoint;
        /* *
         *
         *  Functions
         *
         * */
        /* eslint-disable valid-jsdoc */
        /**
         * Get the index of a point in a series. This is needed when using e.g. data
         * grouping.
         *
         * @private
         * @function getPointIndex
         * @param {Highcharts.AccessibilityPoint} point
         * The point to find index of.
         * @return {number|undefined}
         * The index in the series.points array of the point.
         */
        function getPointIndex(point) {
            var index = point.index,
                points = point.series.points;
            var i = points.length;
            if (points[index] !== point) {
                while (i--) {
                    if (points[i] === point) {
                        return i;
                    }
                }
            }
            else {
                return index;
            }
        }
        /**
         * Determine if series navigation should be skipped
         * @private
         */
        function isSkipSeries(series) {
            var a11yOptions = series.chart.options.accessibility,
                seriesNavOptions = a11yOptions.keyboardNavigation.seriesNavigation,
                seriesA11yOptions = series.options.accessibility || {},
                seriesKbdNavOptions = seriesA11yOptions.keyboardNavigation;
            return seriesKbdNavOptions && seriesKbdNavOptions.enabled === false ||
                seriesA11yOptions.enabled === false ||
                series.options.enableMouseTracking === false || // #8440
                !series.visible ||
                // Skip all points in a series where pointNavigationEnabledThreshold is
                // reached
                (seriesNavOptions.pointNavigationEnabledThreshold &&
                    seriesNavOptions.pointNavigationEnabledThreshold <=
                        series.points.length);
        }
        /**
         * Determine if navigation for a point should be skipped
         * @private
         */
        function isSkipPoint(point) {
            var a11yOptions = point.series.chart.options.accessibility;
            var pointA11yDisabled = (point.options.accessibility &&
                    point.options.accessibility.enabled === false);
            return point.isNull &&
                a11yOptions.keyboardNavigation.seriesNavigation.skipNullPoints ||
                point.visible === false ||
                point.isInside === false ||
                pointA11yDisabled ||
                isSkipSeries(point.series);
        }
        /**
         * Get the first point that is not a skip point in this series.
         * @private
         */
        function getFirstValidPointInSeries(series) {
            var points = series.points || [],
                len = points.length;
            for (var i = 0; i < len; ++i) {
                if (!isSkipPoint(points[i])) {
                    return points[i];
                }
            }
            return null;
        }
        /**
         * Get the first point that is not a skip point in this chart.
         * @private
         */
        function getFirstValidPointInChart(chart) {
            var series = chart.series || [],
                len = series.length;
            for (var i = 0; i < len; ++i) {
                if (!isSkipSeries(series[i])) {
                    var point = getFirstValidPointInSeries(series[i]);
                    if (point) {
                        return point;
                    }
                }
            }
            return null;
        }
        /**
         * @private
         */
        function highlightLastValidPointInChart(chart) {
            var numSeries = chart.series.length;
            var i = numSeries,
                res = false;
            while (i--) {
                chart.highlightedPoint = chart.series[i].points[chart.series[i].points.length - 1];
                // Highlight first valid point in the series will also
                // look backwards. It always starts from currently
                // highlighted point.
                res = chart.series[i].highlightNextValidPoint();
                if (res) {
                    break;
                }
            }
            return res;
        }
        /**
         * After drilling down/up, we need to set focus to the first point for
         * screen readers and keyboard nav.
         * @private
         */
        function updateChartFocusAfterDrilling(chart) {
            var point = getFirstValidPointInChart(chart);
            if (point) {
                point.highlight(false); // Do not visually highlight
            }
        }
        /**
         * Highlight the first point in chart that is not a skip point
         * @private
         */
        function highlightFirstValidPointInChart(chart) {
            delete chart.highlightedPoint;
            var point = getFirstValidPointInChart(chart);
            return point ? point.highlight() : false;
        }
        /* *
         *
         *  Class
         *
         * */
        /**
         * @private
         * @class
         * @name Highcharts.SeriesKeyboardNavigation
         */
        var SeriesKeyboardNavigation = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function SeriesKeyboardNavigation(chart, keyCodes) {
                    this.keyCodes = keyCodes;
                this.chart = chart;
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Init the keyboard navigation
             */
            SeriesKeyboardNavigation.prototype.init = function () {
                var keyboardNavigation = this,
                    chart = this.chart,
                    e = this.eventProvider = new EventProvider();
                e.addEvent(Series, 'destroy', function () {
                    return keyboardNavigation.onSeriesDestroy(this);
                });
                e.addEvent(chart, 'afterApplyDrilldown', function () {
                    updateChartFocusAfterDrilling(this);
                });
                e.addEvent(chart, 'drilldown', function (e) {
                    var point = e.point,
                        series = point.series;
                    keyboardNavigation.lastDrilledDownPoint = {
                        x: point.x,
                        y: point.y,
                        seriesName: series ? series.name : ''
                    };
                });
                e.addEvent(chart, 'drillupall', function () {
                    setTimeout(function () {
                        keyboardNavigation.onDrillupAll();
                    }, 10);
                });
                // Heatmaps et al. alter z-index in setState, causing elements
                // to lose focus
                e.addEvent(Point, 'afterSetState', function () {
                    var point = this;
                    var pointEl = point.graphic && point.graphic.element;
                    var focusedElement = doc.activeElement;
                    // VO brings focus with it to container, causing series nav to run.
                    // If then navigating with virtual cursor, it is possible to leave
                    // keyboard nav module state on the data points and still activate
                    // proxy buttons.
                    var focusedElClassName = (focusedElement && focusedElement.getAttribute('class'));
                    var isProxyFocused = focusedElClassName &&
                            focusedElClassName.indexOf('highcharts-a11y-proxy-button') > -1;
                    if (chart.highlightedPoint === point &&
                        focusedElement !== pointEl &&
                        !isProxyFocused &&
                        pointEl &&
                        pointEl.focus) {
                        pointEl.focus();
                    }
                });
            };
            /**
             * After drillup we want to find the point that was drilled down to and
             * highlight it.
             * @private
             */
            SeriesKeyboardNavigation.prototype.onDrillupAll = function () {
                var last = this.lastDrilledDownPoint,
                    chart = this.chart,
                    series = last && getSeriesFromName(chart,
                    last.seriesName);
                var point;
                if (last && series && defined(last.x) && defined(last.y)) {
                    point = getPointFromXY(series, last.x, last.y);
                }
                point = point || getFirstValidPointInChart(chart);
                // Container focus can be lost on drillup due to deleted elements.
                if (chart.container) {
                    chart.container.focus();
                }
                if (point && point.highlight) {
                    point.highlight(false); // Do not visually highlight
                }
            };
            /**
             * @private
             */
            SeriesKeyboardNavigation.prototype.getKeyboardNavigationHandler = function () {
                var keyboardNavigation = this,
                    keys = this.keyCodes,
                    chart = this.chart,
                    inverted = chart.inverted;
                return new KeyboardNavigationHandler(chart, {
                    keyCodeMap: [
                        [inverted ? [keys.up, keys.down] : [keys.left, keys.right],
                            function (keyCode) {
                                return keyboardNavigation.onKbdSideways(this, keyCode);
                            }],
                        [inverted ? [keys.left, keys.right] : [keys.up, keys.down],
                            function (keyCode) {
                                return keyboardNavigation.onKbdVertical(this, keyCode);
                            }],
                        [[keys.enter, keys.space],
                            function (keyCode, event) {
                                var point = chart.highlightedPoint;
                                if (point) {
                                    event.point = point;
                                    fireEvent(point.series, 'click', event);
                                    point.firePointEvent('click');
                                }
                                return this.response.success;
                            }],
                        [[keys.home],
                            function () {
                                highlightFirstValidPointInChart(chart);
                                return this.response.success;
                            }],
                        [[keys.end],
                            function () {
                                highlightLastValidPointInChart(chart);
                                return this.response.success;
                            }],
                        [[keys.pageDown, keys.pageUp],
                            function (keyCode) {
                                chart.highlightAdjacentSeries(keyCode === keys.pageDown);
                                return this.response.success;
                            }]
                    ],
                    init: function () {
                        return keyboardNavigation.onHandlerInit(this);
                    },
                    validate: function () {
                        return !!getFirstValidPointInChart(chart);
                    },
                    terminate: function () {
                        return keyboardNavigation.onHandlerTerminate();
                    }
                });
            };
            /**
             * @private
             * @param {Highcharts.KeyboardNavigationHandler} handler
             * @param {number} keyCode
             * @return {number}
             * response
             */
            SeriesKeyboardNavigation.prototype.onKbdSideways = function (handler, keyCode) {
                var keys = this.keyCodes,
                    isNext = keyCode === keys.right || keyCode === keys.down;
                return this.attemptHighlightAdjacentPoint(handler, isNext);
            };
            /**
             * When keyboard navigation inits.
             * @private
             * @param {Highcharts.KeyboardNavigationHandler} handler The handler object
             * @return {number}
             * response
             */
            SeriesKeyboardNavigation.prototype.onHandlerInit = function (handler) {
                var chart = this.chart,
                    kbdNavOptions = chart.options.accessibility.keyboardNavigation;
                if (kbdNavOptions.seriesNavigation.rememberPointFocus &&
                    chart.highlightedPoint) {
                    chart.highlightedPoint.highlight();
                }
                else {
                    highlightFirstValidPointInChart(chart);
                }
                return handler.response.success;
            };
            /**
             * @private
             * @param {Highcharts.KeyboardNavigationHandler} handler
             * @param {number} keyCode
             * @return {number}
             * response
             */
            SeriesKeyboardNavigation.prototype.onKbdVertical = function (handler, keyCode) {
                var chart = this.chart,
                    keys = this.keyCodes,
                    isNext = keyCode === keys.down || keyCode === keys.right,
                    navOptions = chart.options.accessibility.keyboardNavigation
                        .seriesNavigation;
                // Handle serialized mode, act like left/right
                if (navOptions.mode && navOptions.mode === 'serialize') {
                    return this.attemptHighlightAdjacentPoint(handler, isNext);
                }
                // Normal mode, move between series
                var highlightMethod = (chart.highlightedPoint &&
                        chart.highlightedPoint.series.keyboardMoveVertical) ?
                        'highlightAdjacentPointVertical' :
                        'highlightAdjacentSeries';
                chart[highlightMethod](isNext);
                return handler.response.success;
            };
            /**
             * @private
             */
            SeriesKeyboardNavigation.prototype.onHandlerTerminate = function () {
                var chart = this.chart,
                    kbdNavOptions = chart.options.accessibility.keyboardNavigation;
                if (chart.tooltip) {
                    chart.tooltip.hide(0);
                }
                var hoverSeries = (chart.highlightedPoint && chart.highlightedPoint.series);
                if (hoverSeries && hoverSeries.onMouseOut) {
                    hoverSeries.onMouseOut();
                }
                if (chart.highlightedPoint && chart.highlightedPoint.onMouseOut) {
                    chart.highlightedPoint.onMouseOut();
                }
                if (!kbdNavOptions.seriesNavigation.rememberPointFocus) {
                    delete chart.highlightedPoint;
                }
            };
            /**
             * Function that attempts to highlight next/prev point. Handles wrap around.
             * @private
             */
            SeriesKeyboardNavigation.prototype.attemptHighlightAdjacentPoint = function (handler, directionIsNext) {
                var chart = this.chart,
                    wrapAround = chart.options.accessibility.keyboardNavigation
                        .wrapAround,
                    highlightSuccessful = chart.highlightAdjacentPoint(directionIsNext);
                if (!highlightSuccessful) {
                    if (wrapAround && (directionIsNext ?
                        highlightFirstValidPointInChart(chart) :
                        highlightLastValidPointInChart(chart))) {
                        return handler.response.success;
                    }
                    return handler.response[directionIsNext ? 'next' : 'prev'];
                }
                return handler.response.success;
            };
            /**
             * @private
             */
            SeriesKeyboardNavigation.prototype.onSeriesDestroy = function (series) {
                var chart = this.chart,
                    currentHighlightedPointDestroyed = chart.highlightedPoint &&
                        chart.highlightedPoint.series === series;
                if (currentHighlightedPointDestroyed) {
                    delete chart.highlightedPoint;
                    if (chart.focusElement) {
                        chart.focusElement.removeFocusBorder();
                    }
                }
            };
            /**
             * @private
             */
            SeriesKeyboardNavigation.prototype.destroy = function () {
                this.eventProvider.removeAddedEvents();
            };
            return SeriesKeyboardNavigation;
        }());
        /* *
         *
         *  Class Namespace
         *
         * */
        (function (SeriesKeyboardNavigation) {
            /* *
             *
             *  Declarations
             *
             * */
            /* *
             *
             *  Constants
             *
             * */
            var composedClasses = [];
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Function to highlight next/previous point in chart.
             *
             * @private
             * @function Highcharts.Chart#highlightAdjacentPoint
             *
             * @param {boolean} next
             * Flag for the direction.
             *
             * @return {Highcharts.Point|boolean}
             * Returns highlighted point on success, false on failure (no adjacent point
             * to highlight in chosen direction).
             */
            function chartHighlightAdjacentPoint(next) {
                var chart = this,
                    series = chart.series,
                    curPoint = chart.highlightedPoint,
                    curPointIndex = curPoint && getPointIndex(curPoint) || 0,
                    curPoints = curPoint && curPoint.series.points || [],
                    lastSeries = chart.series && chart.series[chart.series.length - 1],
                    lastPoint = lastSeries &&
                        lastSeries.points &&
                        lastSeries.points[lastSeries.points.length - 1];
                var newSeries,
                    newPoint;
                // If no points, return false
                if (!series[0] || !series[0].points) {
                    return false;
                }
                if (!curPoint) {
                    // No point is highlighted yet. Try first/last point depending on
                    // move direction
                    newPoint = next ? series[0].points[0] : lastPoint;
                }
                else {
                    // We have a highlighted point. Grab next/prev point & series.
                    newSeries = series[curPoint.series.index + (next ? 1 : -1)];
                    newPoint = curPoints[curPointIndex + (next ? 1 : -1)];
                    if (!newPoint && newSeries) {
                        // Done with this series, try next one
                        newPoint = newSeries.points[next ? 0 : newSeries.points.length - 1];
                    }
                    // If there is no adjacent point, we return false
                    if (!newPoint) {
                        return false;
                    }
                }
                // Recursively skip points
                if (isSkipPoint(newPoint)) {
                    // If we skip this whole series, move to the end of the series
                    // before we recurse, just to optimize
                    newSeries = newPoint.series;
                    if (isSkipSeries(newSeries)) {
                        chart.highlightedPoint = next ?
                            newSeries.points[newSeries.points.length - 1] :
                            newSeries.points[0];
                    }
                    else {
                        // Otherwise, just move one point
                        chart.highlightedPoint = newPoint;
                    }
                    // Retry
                    return chart.highlightAdjacentPoint(next);
                }
                // There is an adjacent point, highlight it
                return newPoint.highlight();
            }
            /**
             * Highlight the closest point vertically.
             * @private
             */
            function chartHighlightAdjacentPointVertical(down) {
                var curPoint = this.highlightedPoint;
                var minDistance = Infinity,
                    bestPoint;
                if (!defined(curPoint.plotX) || !defined(curPoint.plotY)) {
                    return false;
                }
                this.series.forEach(function (series) {
                    if (isSkipSeries(series)) {
                        return;
                    }
                    series.points.forEach(function (point) {
                        if (!defined(point.plotY) || !defined(point.plotX) ||
                            point === curPoint) {
                            return;
                        }
                        var yDistance = point.plotY - curPoint.plotY;
                        var width = Math.abs(point.plotX - curPoint.plotX),
                            distance = Math.abs(yDistance) * Math.abs(yDistance) +
                                width * width * 4; // Weigh horizontal distance highly
                            // Reverse distance number if axis is reversed
                            if (series.yAxis && series.yAxis.reversed) {
                                yDistance *= -1;
                        }
                        if (yDistance <= 0 && down || yDistance >= 0 && !down ||
                            distance < 5 || // Points in same spot => infinite loop
                            isSkipPoint(point)) {
                            return;
                        }
                        if (distance < minDistance) {
                            minDistance = distance;
                            bestPoint = point;
                        }
                    });
                });
                return bestPoint ? bestPoint.highlight() : false;
            }
            /**
             * Highlight next/previous series in chart. Returns false if no adjacent
             * series in the direction, otherwise returns new highlighted point.
             * @private
             */
            function chartHighlightAdjacentSeries(down) {
                var chart = this,
                    curPoint = chart.highlightedPoint,
                    lastSeries = chart.series && chart.series[chart.series.length - 1],
                    lastPoint = lastSeries && lastSeries.points &&
                        lastSeries.points[lastSeries.points.length - 1];
                var newSeries,
                    newPoint,
                    adjacentNewPoint;
                // If no point is highlighted, highlight the first/last point
                if (!chart.highlightedPoint) {
                    newSeries = down ? (chart.series && chart.series[0]) : lastSeries;
                    newPoint = down ?
                        (newSeries && newSeries.points && newSeries.points[0]) :
                        lastPoint;
                    return newPoint ? newPoint.highlight() : false;
                }
                newSeries = (chart.series[curPoint.series.index + (down ? -1 : 1)]);
                if (!newSeries) {
                    return false;
                }
                // We have a new series in this direction, find the right point
                // Weigh xDistance as counting much higher than Y distance
                newPoint = getClosestPoint(curPoint, newSeries, 4);
                if (!newPoint) {
                    return false;
                }
                // New series and point exists, but we might want to skip it
                if (isSkipSeries(newSeries)) {
                    // Skip the series
                    newPoint.highlight();
                    // Try recurse
                    adjacentNewPoint = chart.highlightAdjacentSeries(down);
                    if (!adjacentNewPoint) {
                        // Recurse failed
                        curPoint.highlight();
                        return false;
                    }
                    // Recurse succeeded
                    return adjacentNewPoint;
                }
                // Highlight the new point or any first valid point back or forwards
                // from it
                newPoint.highlight();
                return newPoint.series.highlightNextValidPoint();
            }
            /**
             * @private
             */
            function compose(ChartClass, PointClass, SeriesClass) {
                if (composedClasses.indexOf(ChartClass) === -1) {
                    composedClasses.push(ChartClass);
                    var chartProto = ChartClass.prototype;
                    chartProto.highlightAdjacentPoint = chartHighlightAdjacentPoint;
                    chartProto.highlightAdjacentPointVertical = (chartHighlightAdjacentPointVertical);
                    chartProto.highlightAdjacentSeries = chartHighlightAdjacentSeries;
                }
                if (composedClasses.indexOf(PointClass) === -1) {
                    composedClasses.push(PointClass);
                    var pointProto = PointClass.prototype;
                    pointProto.highlight = pointHighlight;
                }
                if (composedClasses.indexOf(SeriesClass) === -1) {
                    composedClasses.push(SeriesClass);
                    var seriesProto = SeriesClass.prototype;
                    /**
                     * Set for which series types it makes sense to move to the closest
                     * point with up/down arrows, and which series types should just
                     * move to next series.
                     * @private
                     */
                    seriesProto.keyboardMoveVertical = true;
                    [
                        'column',
                        'gantt',
                        'pie'
                    ].forEach(function (type) {
                        if (seriesTypes[type]) {
                            seriesTypes[type].prototype.keyboardMoveVertical = false;
                        }
                    });
                    seriesProto.highlightNextValidPoint = (seriesHighlightNextValidPoint);
                }
            }
            SeriesKeyboardNavigation.compose = compose;
            /**
             * Get the point in a series that is closest (in pixel distance) to a
             * reference point. Optionally supply weight factors for x and y directions.
             * @private
             */
            function getClosestPoint(point, series, xWeight, yWeight) {
                var minDistance = Infinity,
                    dPoint,
                    minIx,
                    distance,
                    i = series.points.length;
                var hasUndefinedPosition = function (point) { return (!(defined(point.plotX) && defined(point.plotY))); };
                if (hasUndefinedPosition(point)) {
                    return;
                }
                while (i--) {
                    dPoint = series.points[i];
                    if (hasUndefinedPosition(dPoint)) {
                        continue;
                    }
                    distance = (point.plotX - dPoint.plotX) *
                        (point.plotX - dPoint.plotX) *
                        (xWeight || 1) +
                        (point.plotY - dPoint.plotY) *
                            (point.plotY - dPoint.plotY) *
                            (yWeight || 1);
                    if (distance < minDistance) {
                        minDistance = distance;
                        minIx = i;
                    }
                }
                return defined(minIx) ? series.points[minIx] : void 0;
            }
            /**
             * Highlights a point (show tooltip, display hover state, focus element).
             *
             * @private
             * @function Highcharts.Point#highlight
             *
             * @return {Highcharts.Point}
             *         This highlighted point.
             */
            function pointHighlight(highlightVisually) {
                if (highlightVisually === void 0) { highlightVisually = true; }
                var chart = this.series.chart;
                if (!this.isNull && highlightVisually) {
                    this.onMouseOver(); // Show the hover marker and tooltip
                }
                else {
                    if (chart.tooltip) {
                        chart.tooltip.hide(0);
                    }
                    // Do not call blur on the element, as it messes up the focus of the
                    // div element of the chart
                }
                scrollToPoint(this);
                // We focus only after calling onMouseOver because the state change can
                // change z-index and mess up the element.
                if (this.graphic) {
                    chart.setFocusToElement(this.graphic);
                    if (!highlightVisually && chart.focusElement) {
                        chart.focusElement.removeFocusBorder();
                    }
                }
                chart.highlightedPoint = this;
                return this;
            }
            /**
             * Highlight first valid point in a series. Returns the point if
             * successfully highlighted, otherwise false. If there is a highlighted
             * point in the series, use that as starting point.
             *
             * @private
             * @function Highcharts.Series#highlightNextValidPoint
             */
            function seriesHighlightNextValidPoint() {
                var curPoint = this.chart.highlightedPoint,
                    start = (curPoint && curPoint.series) === this ?
                        getPointIndex(curPoint) :
                        0,
                    points = this.points,
                    len = points.length;
                if (points && len) {
                    for (var i = start; i < len; ++i) {
                        if (!isSkipPoint(points[i])) {
                            return points[i].highlight();
                        }
                    }
                    for (var j = start; j >= 0; --j) {
                        if (!isSkipPoint(points[j])) {
                            return points[j].highlight();
                        }
                    }
                }
                return false;
            }
        })(SeriesKeyboardNavigation || (SeriesKeyboardNavigation = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return SeriesKeyboardNavigation;
    });
    _registerModule(_modules, 'Accessibility/Components/SeriesComponent/SeriesComponent.js', [_modules['Accessibility/AccessibilityComponent.js'], _modules['Accessibility/Utils/ChartUtilities.js'], _modules['Accessibility/Components/SeriesComponent/ForcedMarkers.js'], _modules['Accessibility/Components/SeriesComponent/NewDataAnnouncer.js'], _modules['Accessibility/Components/SeriesComponent/SeriesDescriber.js'], _modules['Accessibility/Components/SeriesComponent/SeriesKeyboardNavigation.js'], _modules['Core/Tooltip.js']], function (AccessibilityComponent, ChartUtilities, ForcedMarkers, NewDataAnnouncer, SeriesDescriber, SeriesKeyboardNavigation, Tooltip) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Accessibility component for series and points.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var __extends = (this && this.__extends) || (function () {
                var extendStatics = function (d,
            b) {
                    extendStatics = Object.setPrototypeOf ||
                        ({ __proto__: [] } instanceof Array && function (d,
            b) { d.__proto__ = b; }) ||
                        function (d,
            b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
                return extendStatics(d, b);
            };
            return function (d, b) {
                extendStatics(d, b);
                function __() { this.constructor = d; }
                d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
            };
        })();
        var hideSeriesFromAT = ChartUtilities.hideSeriesFromAT;
        var describeSeries = SeriesDescriber.describeSeries;
        /* *
         *
         *  Class
         *
         * */
        /**
         * The SeriesComponent class
         *
         * @private
         * @class
         * @name Highcharts.SeriesComponent
         */
        var SeriesComponent = /** @class */ (function (_super) {
                __extends(SeriesComponent, _super);
            function SeriesComponent() {
                return _super !== null && _super.apply(this, arguments) || this;
            }
            /* *
             *
             *  Static Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * @private
             */
            SeriesComponent.compose = function (ChartClass, PointClass, SeriesClass) {
                NewDataAnnouncer.compose(SeriesClass);
                ForcedMarkers.compose(SeriesClass);
                SeriesKeyboardNavigation.compose(ChartClass, PointClass, SeriesClass);
            };
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Init the component.
             */
            SeriesComponent.prototype.init = function () {
                this.newDataAnnouncer = new NewDataAnnouncer(this.chart);
                this.newDataAnnouncer.init();
                this.keyboardNavigation = new SeriesKeyboardNavigation(this.chart, this.keyCodes);
                this.keyboardNavigation.init();
                this.hideTooltipFromATWhenShown();
                this.hideSeriesLabelsFromATWhenShown();
            };
            /**
             * @private
             */
            SeriesComponent.prototype.hideTooltipFromATWhenShown = function () {
                var component = this;
                this.addEvent(Tooltip, 'refresh', function () {
                    if (this.chart === component.chart &&
                        this.label &&
                        this.label.element) {
                        this.label.element.setAttribute('aria-hidden', true);
                    }
                });
            };
            /**
             * @private
             */
            SeriesComponent.prototype.hideSeriesLabelsFromATWhenShown = function () {
                this.addEvent(this.chart, 'afterDrawSeriesLabels', function () {
                    this.series.forEach(function (series) {
                        if (series.labelBySeries) {
                            series.labelBySeries.attr('aria-hidden', true);
                        }
                    });
                });
            };
            /**
             * Called on chart render. It is necessary to do this for render in case
             * markers change on zoom/pixel density.
             */
            SeriesComponent.prototype.onChartRender = function () {
                var chart = this.chart;
                chart.series.forEach(function (series) {
                    var shouldDescribeSeries = (series.options.accessibility &&
                            series.options.accessibility.enabled) !== false &&
                            series.visible;
                    if (shouldDescribeSeries) {
                        describeSeries(series);
                    }
                    else {
                        hideSeriesFromAT(series);
                    }
                });
            };
            /**
             * Get keyboard navigation handler for this component.
             * @private
             */
            SeriesComponent.prototype.getKeyboardNavigation = function () {
                return this.keyboardNavigation.getKeyboardNavigationHandler();
            };
            /**
             * Remove traces
             * @private
             */
            SeriesComponent.prototype.destroy = function () {
                this.newDataAnnouncer.destroy();
                this.keyboardNavigation.destroy();
            };
            return SeriesComponent;
        }(AccessibilityComponent));
        /* *
         *
         *  Default Export
         *
         * */

        return SeriesComponent;
    });
    _registerModule(_modules, 'Accessibility/Components/ZoomComponent.js', [_modules['Accessibility/AccessibilityComponent.js'], _modules['Accessibility/Utils/ChartUtilities.js'], _modules['Accessibility/Utils/HTMLUtilities.js'], _modules['Accessibility/KeyboardNavigationHandler.js'], _modules['Core/Utilities.js']], function (AccessibilityComponent, CU, HU, KeyboardNavigationHandler, U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Accessibility component for chart zoom.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var __extends = (this && this.__extends) || (function () {
                var extendStatics = function (d,
            b) {
                    extendStatics = Object.setPrototypeOf ||
                        ({ __proto__: [] } instanceof Array && function (d,
            b) { d.__proto__ = b; }) ||
                        function (d,
            b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
                return extendStatics(d, b);
            };
            return function (d, b) {
                extendStatics(d, b);
                function __() { this.constructor = d; }
                d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
            };
        })();
        var unhideChartElementFromAT = CU.unhideChartElementFromAT;
        var getFakeMouseEvent = HU.getFakeMouseEvent;
        var attr = U.attr,
            pick = U.pick;
        /* *
         *
         *  Functions
         *
         * */
        /**
         * @private
         */
        function chartHasMapZoom(chart) {
            return !!((chart.mapView) &&
                chart.mapNavigation &&
                chart.mapNavigation.navButtons.length);
        }
        /* *
         *
         *  Class
         *
         * */
        /**
         * The ZoomComponent class
         *
         * @private
         * @class
         * @name Highcharts.ZoomComponent
         */
        var ZoomComponent = /** @class */ (function (_super) {
                __extends(ZoomComponent, _super);
            function ZoomComponent() {
                /* *
                 *
                 *  Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.focusedMapNavButtonIx = -1;
                return _this;
            }
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Initialize the component
             */
            ZoomComponent.prototype.init = function () {
                var component = this,
                    chart = this.chart;
                this.proxyProvider.addGroup('zoom', 'div');
                [
                    'afterShowResetZoom', 'afterApplyDrilldown', 'drillupall'
                ].forEach(function (eventType) {
                    component.addEvent(chart, eventType, function () {
                        component.updateProxyOverlays();
                    });
                });
            };
            /**
             * Called when chart is updated
             */
            ZoomComponent.prototype.onChartUpdate = function () {
                var chart = this.chart,
                    component = this;
                // Make map zoom buttons accessible
                if (chart.mapNavigation) {
                    chart.mapNavigation.navButtons.forEach(function (button, i) {
                        unhideChartElementFromAT(chart, button.element);
                        component.setMapNavButtonAttrs(button.element, 'accessibility.zoom.mapZoom' + (i ? 'Out' : 'In'));
                    });
                }
            };
            /**
             * @private
             * @param {Highcharts.HTMLDOMElement|Highcharts.SVGDOMElement} button
             * @param {string} labelFormatKey
             */
            ZoomComponent.prototype.setMapNavButtonAttrs = function (button, labelFormatKey) {
                var chart = this.chart,
                    label = chart.langFormat(labelFormatKey, { chart: chart });
                attr(button, {
                    tabindex: -1,
                    role: 'button',
                    'aria-label': label
                });
            };
            /**
             * Update the proxy overlays on every new render to ensure positions are
             * correct.
             */
            ZoomComponent.prototype.onChartRender = function () {
                this.updateProxyOverlays();
            };
            /**
             * Update proxy overlays, recreating the buttons.
             */
            ZoomComponent.prototype.updateProxyOverlays = function () {
                var chart = this.chart;
                // Always start with a clean slate
                this.proxyProvider.clearGroup('zoom');
                if (chart.resetZoomButton) {
                    this.createZoomProxyButton(chart.resetZoomButton, 'resetZoomProxyButton', chart.langFormat('accessibility.zoom.resetZoomButton', { chart: chart }));
                }
                if (chart.drillUpButton &&
                    chart.breadcrumbs &&
                    chart.breadcrumbs.list) {
                    var lastBreadcrumb = chart.breadcrumbs.list[chart.breadcrumbs.list.length - 1];
                    this.createZoomProxyButton(chart.drillUpButton, 'drillUpProxyButton', chart.langFormat('accessibility.drillUpButton', {
                        chart: chart,
                        buttonText: chart.breadcrumbs.getButtonText(lastBreadcrumb)
                    }));
                }
            };
            /**
             * @private
             * @param {Highcharts.SVGElement} buttonEl
             * @param {string} buttonProp
             * @param {string} label
             */
            ZoomComponent.prototype.createZoomProxyButton = function (buttonEl, buttonProp, label) {
                this[buttonProp] = this.proxyProvider.addProxyElement('zoom', {
                    click: buttonEl
                }, {
                    'aria-label': label,
                    tabindex: -1
                });
            };
            /**
             * Get keyboard navigation handler for map zoom.
             * @private
             * @return {Highcharts.KeyboardNavigationHandler} The module object
             */
            ZoomComponent.prototype.getMapZoomNavigation = function () {
                var keys = this.keyCodes,
                    chart = this.chart,
                    component = this;
                return new KeyboardNavigationHandler(chart, {
                    keyCodeMap: [
                        [
                            [keys.up, keys.down, keys.left, keys.right],
                            function (keyCode) {
                                return component.onMapKbdArrow(this, keyCode);
                            }
                        ],
                        [
                            [keys.tab],
                            function (_keyCode, e) {
                                return component.onMapKbdTab(this, e);
                            }
                        ],
                        [
                            [keys.space, keys.enter],
                            function () {
                                return component.onMapKbdClick(this);
                            }
                        ]
                    ],
                    validate: function () {
                        return chartHasMapZoom(chart);
                    },
                    init: function (direction) {
                        return component.onMapNavInit(direction);
                    }
                });
            };
            /**
             * Arrow key panning for maps.
             * @private
             * @param {Highcharts.KeyboardNavigationHandler} keyboardNavigationHandler The handler context.
             * @param {number} keyCode Key pressed.
             * @return {number} Response code
             */
            ZoomComponent.prototype.onMapKbdArrow = function (keyboardNavigationHandler, keyCode) {
                var chart = this.chart,
                    keys = this.keyCodes,
                    target = chart.container,
                    isY = keyCode === keys.up || keyCode === keys.down,
                    stepDirection = (keyCode === keys.left || keyCode === keys.up) ?
                        1 : -1,
                    granularity = 10,
                    diff = (isY ? chart.plotHeight : chart.plotWidth) /
                        granularity * stepDirection, 
                    // Randomize since same mousedown coords twice is ignored in MapView
                    r = Math.random() * 10,
                    startPos = {
                        x: target.offsetLeft + chart.plotLeft + chart.plotWidth / 2 + r,
                        y: target.offsetTop + chart.plotTop + chart.plotHeight / 2 + r
                    },
                    endPos = isY ? { x: startPos.x,
                    y: startPos.y + diff } :
                        { x: startPos.x + diff,
                    y: startPos.y };
                [
                    getFakeMouseEvent('mousedown', startPos),
                    getFakeMouseEvent('mousemove', endPos),
                    getFakeMouseEvent('mouseup', endPos)
                ].forEach(function (e) { return target.dispatchEvent(e); });
                return keyboardNavigationHandler.response.success;
            };
            /**
             * @private
             * @param {Highcharts.KeyboardNavigationHandler} keyboardNavigationHandler
             * @param {global.KeyboardEvent} event
             * @return {number} Response code
             */
            ZoomComponent.prototype.onMapKbdTab = function (keyboardNavigationHandler, event) {
                var chart = this.chart;
                var response = keyboardNavigationHandler.response;
                var isBackwards = event.shiftKey;
                var isMoveOutOfRange = isBackwards && !this.focusedMapNavButtonIx ||
                        !isBackwards && this.focusedMapNavButtonIx;
                // Deselect old
                chart.mapNavigation.navButtons[this.focusedMapNavButtonIx].setState(0);
                if (isMoveOutOfRange) {
                    if (chart.mapView) {
                        chart.mapView.zoomBy(); // Reset zoom
                    }
                    return response[isBackwards ? 'prev' : 'next'];
                }
                // Select other button
                this.focusedMapNavButtonIx += isBackwards ? -1 : 1;
                var button = chart.mapNavigation.navButtons[this.focusedMapNavButtonIx];
                chart.setFocusToElement(button.box, button.element);
                button.setState(2);
                return response.success;
            };
            /**
             * Called on map button click.
             * @private
             * @param {Highcharts.KeyboardNavigationHandler} keyboardNavigationHandler The handler context object
             * @return {number} Response code
             */
            ZoomComponent.prototype.onMapKbdClick = function (keyboardNavigationHandler) {
                var el = this.chart.mapNavigation.navButtons[this.focusedMapNavButtonIx].element;
                this.fakeClickEvent(el);
                return keyboardNavigationHandler.response.success;
            };
            /**
             * @private
             * @param {number} direction
             */
            ZoomComponent.prototype.onMapNavInit = function (direction) {
                var chart = this.chart,
                    zoomIn = chart.mapNavigation.navButtons[0],
                    zoomOut = chart.mapNavigation.navButtons[1],
                    initialButton = direction > 0 ? zoomIn : zoomOut;
                chart.setFocusToElement(initialButton.box, initialButton.element);
                initialButton.setState(2);
                this.focusedMapNavButtonIx = direction > 0 ? 0 : 1;
            };
            /**
             * Get keyboard navigation handler for a simple chart button. Provide the
             * button reference for the chart, and a function to call on click.
             *
             * @private
             * @param {string} buttonProp The property on chart referencing the button.
             * @return {Highcharts.KeyboardNavigationHandler} The module object
             */
            ZoomComponent.prototype.simpleButtonNavigation = function (buttonProp, proxyProp, onClick) {
                var keys = this.keyCodes,
                    component = this,
                    chart = this.chart;
                return new KeyboardNavigationHandler(chart, {
                    keyCodeMap: [
                        [
                            [keys.tab, keys.up, keys.down, keys.left, keys.right],
                            function (keyCode, e) {
                                var isBackwards = (keyCode === keys.tab && e.shiftKey ||
                                        keyCode === keys.left ||
                                        keyCode === keys.up);
                                // Arrow/tab => just move
                                return this.response[isBackwards ? 'prev' : 'next'];
                            }
                        ],
                        [
                            [keys.space, keys.enter],
                            function () {
                                var res = onClick(this,
                                    chart);
                                return pick(res, this.response.success);
                            }
                        ]
                    ],
                    validate: function () {
                        var hasButton = (chart[buttonProp] &&
                                chart[buttonProp].box &&
                                component[proxyProp].buttonElement);
                        return hasButton;
                    },
                    init: function () {
                        chart.setFocusToElement(chart[buttonProp].box, component[proxyProp].buttonElement);
                    }
                });
            };
            /**
             * Get keyboard navigation handlers for this component.
             * @return {Array<Highcharts.KeyboardNavigationHandler>}
             *         List of module objects
             */
            ZoomComponent.prototype.getKeyboardNavigation = function () {
                return [
                    this.simpleButtonNavigation('resetZoomButton', 'resetZoomProxyButton', function (_handler, chart) {
                        chart.zoomOut();
                    }),
                    this.simpleButtonNavigation('drillUpButton', 'drillUpProxyButton', function (handler, chart) {
                        chart.drillUp();
                        return handler.response.prev;
                    }),
                    this.getMapZoomNavigation()
                ];
            };
            return ZoomComponent;
        }(AccessibilityComponent));
        /* *
         *
         *  Default Export
         *
         * */

        return ZoomComponent;
    });
    _registerModule(_modules, 'Accessibility/HighContrastMode.js', [_modules['Core/Globals.js']], function (H) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Handling for Windows High Contrast Mode.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var doc = H.doc,
            isMS = H.isMS,
            win = H.win;
        /* *
         *
         *  Functions
         *
         * */
        /**
         * Detect WHCM in the browser.
         *
         * @function Highcharts#isHighContrastModeActive
         * @private
         * @return {boolean} Returns true if the browser is in High Contrast mode.
         */
        function isHighContrastModeActive() {
            // Use media query on Edge, but not on IE
            var isEdge = /(Edg)/.test(win.navigator.userAgent);
            if (win.matchMedia && isEdge) {
                return win.matchMedia('(-ms-high-contrast: active)').matches;
            }
            // Test BG image for IE
            if (isMS && win.getComputedStyle) {
                var testDiv = doc.createElement('div');
                var imageSrc = 'data:image/gif;base64,' +
                        'R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
                testDiv.style.backgroundImage = "url(".concat(imageSrc, ")"); // #13071
                doc.body.appendChild(testDiv);
                var bi = (testDiv.currentStyle ||
                        win.getComputedStyle(testDiv)).backgroundImage;
                doc.body.removeChild(testDiv);
                return bi === 'none';
            }
            // Other browsers use the forced-colors standard
            return win.matchMedia && win.matchMedia('(forced-colors: active)').matches;
        }
        /**
         * Force high contrast theme for the chart. The default theme is defined in
         * a separate file.
         *
         * @function Highcharts#setHighContrastTheme
         * @private
         * @param {Highcharts.AccessibilityChart} chart The chart to set the theme of.
         * @return {void}
         */
        function setHighContrastTheme(chart) {
            // We might want to add additional functionality here in the future for
            // storing the old state so that we can reset the theme if HC mode is
            // disabled. For now, the user will have to reload the page.
            chart.highContrastModeActive = true;
            // Apply theme to chart
            var theme = (chart.options.accessibility.highContrastTheme);
            chart.update(theme, false);
            // Force series colors (plotOptions is not enough)
            chart.series.forEach(function (s) {
                var plotOpts = theme.plotOptions[s.type] || {};
                s.update({
                    color: plotOpts.color || 'windowText',
                    colors: [plotOpts.color || 'windowText'],
                    borderColor: plotOpts.borderColor || 'window'
                });
                // Force point colors if existing
                s.points.forEach(function (p) {
                    if (p.options && p.options.color) {
                        p.update({
                            color: plotOpts.color || 'windowText',
                            borderColor: plotOpts.borderColor || 'window'
                        }, false);
                    }
                });
            });
            // The redraw for each series and after is required for 3D pie
            // (workaround)
            chart.redraw();
        }
        /* *
         *
         *  Default Export
         *
         * */
        var whcm = {
                isHighContrastModeActive: isHighContrastModeActive,
                setHighContrastTheme: setHighContrastTheme
            };

        return whcm;
    });
    _registerModule(_modules, 'Accessibility/HighContrastTheme.js', [], function () {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Default theme for Windows High Contrast Mode.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /* *
         *
         *  Theme
         *
         * */
        var theme = {
                chart: {
                    backgroundColor: 'window'
                },
                title: {
                    style: {
                        color: 'windowText'
                    }
                },
                subtitle: {
                    style: {
                        color: 'windowText'
                    }
                },
                colorAxis: {
                    minColor: 'windowText',
                    maxColor: 'windowText',
                    stops: []
                },
                colors: ['windowText'],
                xAxis: {
                    gridLineColor: 'windowText',
                    labels: {
                        style: {
                            color: 'windowText'
                        }
                    },
                    lineColor: 'windowText',
                    minorGridLineColor: 'windowText',
                    tickColor: 'windowText',
                    title: {
                        style: {
                            color: 'windowText'
                        }
                    }
                },
                yAxis: {
                    gridLineColor: 'windowText',
                    labels: {
                        style: {
                            color: 'windowText'
                        }
                    },
                    lineColor: 'windowText',
                    minorGridLineColor: 'windowText',
                    tickColor: 'windowText',
                    title: {
                        style: {
                            color: 'windowText'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'window',
                    borderColor: 'windowText',
                    style: {
                        color: 'windowText'
                    }
                },
                plotOptions: {
                    series: {
                        lineColor: 'windowText',
                        fillColor: 'window',
                        borderColor: 'windowText',
                        edgeColor: 'windowText',
                        borderWidth: 1,
                        dataLabels: {
                            connectorColor: 'windowText',
                            color: 'windowText',
                            style: {
                                color: 'windowText',
                                textOutline: 'none'
                            }
                        },
                        marker: {
                            lineColor: 'windowText',
                            fillColor: 'windowText'
                        }
                    },
                    pie: {
                        color: 'window',
                        colors: ['window'],
                        borderColor: 'windowText',
                        borderWidth: 1
                    },
                    boxplot: {
                        fillColor: 'window'
                    },
                    candlestick: {
                        lineColor: 'windowText',
                        fillColor: 'window'
                    },
                    errorbar: {
                        fillColor: 'window'
                    }
                },
                legend: {
                    backgroundColor: 'window',
                    itemStyle: {
                        color: 'windowText'
                    },
                    itemHoverStyle: {
                        color: 'windowText'
                    },
                    itemHiddenStyle: {
                        color: '#555'
                    },
                    title: {
                        style: {
                            color: 'windowText'
                        }
                    }
                },
                credits: {
                    style: {
                        color: 'windowText'
                    }
                },
                labels: {
                    style: {
                        color: 'windowText'
                    }
                },
                drilldown: {
                    activeAxisLabelStyle: {
                        color: 'windowText'
                    },
                    activeDataLabelStyle: {
                        color: 'windowText'
                    }
                },
                navigation: {
                    buttonOptions: {
                        symbolStroke: 'windowText',
                        theme: {
                            fill: 'window'
                        }
                    }
                },
                rangeSelector: {
                    buttonTheme: {
                        fill: 'window',
                        stroke: 'windowText',
                        style: {
                            color: 'windowText'
                        },
                        states: {
                            hover: {
                                fill: 'window',
                                stroke: 'windowText',
                                style: {
                                    color: 'windowText'
                                }
                            },
                            select: {
                                fill: '#444',
                                stroke: 'windowText',
                                style: {
                                    color: 'windowText'
                                }
                            }
                        }
                    },
                    inputBoxBorderColor: 'windowText',
                    inputStyle: {
                        backgroundColor: 'window',
                        color: 'windowText'
                    },
                    labelStyle: {
                        color: 'windowText'
                    }
                },
                navigator: {
                    handles: {
                        backgroundColor: 'window',
                        borderColor: 'windowText'
                    },
                    outlineColor: 'windowText',
                    maskFill: 'transparent',
                    series: {
                        color: 'windowText',
                        lineColor: 'windowText'
                    },
                    xAxis: {
                        gridLineColor: 'windowText'
                    }
                },
                scrollbar: {
                    barBackgroundColor: '#444',
                    barBorderColor: 'windowText',
                    buttonArrowColor: 'windowText',
                    buttonBackgroundColor: 'window',
                    buttonBorderColor: 'windowText',
                    rifleColor: 'windowText',
                    trackBackgroundColor: 'window',
                    trackBorderColor: 'windowText'
                }
            };
        /* *
         *
         *  Default Export
         *
         * */

        return theme;
    });
    _registerModule(_modules, 'Accessibility/Options/A11yDefaults.js', [], function () {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Default options for accessibility.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /* *
         *
         *  API Options
         *
         * */
        /**
         * Formatter callback for the accessibility announcement.
         *
         * @callback Highcharts.AccessibilityAnnouncementFormatter
         *
         * @param {Array<Highcharts.Series>} updatedSeries
         * Array of all series that received updates. If an announcement is already
         * queued, the series that received updates for that announcement are also
         * included in this array.
         *
         * @param {Highcharts.Series} [addedSeries]
         * This is provided if {@link Highcharts.Chart#addSeries} was called, and there
         * is a new series. In that case, this argument is a reference to the new
         * series.
         *
         * @param {Highcharts.Point} [addedPoint]
         * This is provided if {@link Highcharts.Series#addPoint} was called, and there
         * is a new point. In that case, this argument is a reference to the new point.
         *
         * @return {false|string}
         * The function should return a string with the text to announce to the user.
         * Return empty string to not announce anything. Return `false` to use the
         * default announcement format.
         */
        /**
         * @interface Highcharts.PointAccessibilityOptionsObject
         */ /**
        * Provide a description of the data point, announced to screen readers.
        * @name Highcharts.PointAccessibilityOptionsObject#description
        * @type {string|undefined}
        * @requires modules/accessibility
        * @since 7.1.0
        */ /**
        * Enable or disable exposing the point to assistive technology
        * @name Highcharts.PointAccessibilityOptionsObject#enabled
        * @type {boolean|undefined}
        * @requires modules/accessibility
        * @since 9.0.1
        */
        /* *
         * @interface Highcharts.PointOptionsObject in parts/Point.ts
         */ /**
        * @name Highcharts.PointOptionsObject#accessibility
        * @type {Highcharts.PointAccessibilityOptionsObject|undefined}
        * @requires modules/accessibility
        * @since 7.1.0
        */
        /**
         * @callback Highcharts.ScreenReaderClickCallbackFunction
         *
         * @param {global.MouseEvent} evt
         *        Mouse click event
         *
         * @return {void}
         */
        /**
         * Creates a formatted string for the screen reader module.
         *
         * @callback Highcharts.ScreenReaderFormatterCallbackFunction<T>
         *
         * @param {T} context
         *        Context to format
         *
         * @return {string}
         *         Formatted string for the screen reader module.
         */
        var Options = {
                /**
                 * Options for configuring accessibility for the chart. Requires the
                 * [accessibility module](https://code.highcharts.com/modules/accessibility.js)
                 * to be loaded. For a description of the module and information
                 * on its features, see
                 * [Highcharts Accessibility](https://www.highcharts.com/docs/accessibility/accessibility-module).
                 *
                 * @since        5.0.0
                 * @requires     modules/accessibility
                 * @optionparent accessibility
                 */
                accessibility: {
                    /**
                     * Enable accessibility functionality for the chart. For more
                     * information on how to include these features, and why this is
                     * recommended, see [Highcharts Accessibility](https://www.highcharts.com/docs/accessibility/accessibility-module).
                     *
                     * Highcharts will by default emit a warning to the console if
                     * the [accessibility module](https://code.highcharts.com/modules/accessibility.js)
                     * is not loaded. Setting this option to `false` will override
                     * and silence the warning.
                     *
                     * Once the module is loaded, setting this option to `false`
                     * will disable the module for this chart.
                     *
                     * @since 5.0.0
                     */
                    enabled: true,
                    /**
                     * Accessibility options for the screen reader information sections
                     * added before and after the chart.
                     *
                     * @since 8.0.0
                     */
                    screenReaderSection: {
                        /**
                         * Function to run upon clicking the "View as Data Table" link in
                         * the screen reader region.
                         *
                         * By default Highcharts will insert and set focus to a data table
                         * representation of the chart.
                         *
                         * @type      {Highcharts.ScreenReaderClickCallbackFunction}
                         * @since 8.0.0
                         * @apioption accessibility.screenReaderSection.onViewDataTableClick
                         */
                        /**
                         * Function to run upon clicking the "Play as sound" button in
                         * the screen reader region.
                         *
                         * By default Highcharts will call the `chart.sonify` function.
                         *
                         * @type      {Highcharts.ScreenReaderClickCallbackFunction}
                         * @since 8.0.1
                         * @apioption accessibility.screenReaderSection.onPlayAsSoundClick
                         */
                        /**
                         * A formatter function to create the HTML contents of the hidden
                         * screen reader information region before the chart. Receives one
                         * argument, `chart`, referring to the chart object. Should return a
                         * string with the HTML content of the region. By default this
                         * returns an automatic description of the chart based on
                         * [beforeChartFormat](#accessibility.screenReaderSection.beforeChartFormat).
                         *
                         * @type      {Highcharts.ScreenReaderFormatterCallbackFunction<Highcharts.Chart>}
                         * @since 8.0.0
                         * @apioption accessibility.screenReaderSection.beforeChartFormatter
                         */
                        /**
                         * Format for the screen reader information region before the chart.
                         * Supported HTML tags are `<h1-6>`, `<p>`, `<div>`, `<a>`, `<ul>`,
                         * `<ol>`, `<li>`, and `<button>`. Attributes are not supported,
                         * except for id on `<div>`, `<a>`, and `<button>`. Id is required
                         * on `<a>` and `<button>` in the format `<tag id="abcd">`. Numbers,
                         * lower- and uppercase letters, "-" and "#" are valid characters in
                         * IDs.
                         *
                         * The headingTagName is an auto-detected heading (h1-h6) that
                         * corresponds to the heading level below the previous heading in
                         * the DOM.
                         *
                         * Set to empty string to remove the region altogether.
                         *
                         * @since 8.0.0
                         */
                        beforeChartFormat: '<{headingTagName}>{chartTitle}</{headingTagName}>' +
                            '<div>{typeDescription}</div>' +
                            '<div>{chartSubtitle}</div>' +
                            '<div>{chartLongdesc}</div>' +
                            '<div>{playAsSoundButton}</div>' +
                            '<div>{viewTableButton}</div>' +
                            '<div>{xAxisDescription}</div>' +
                            '<div>{yAxisDescription}</div>' +
                            '<div>{annotationsTitle}{annotationsList}</div>',
                        /**
                         * A formatter function to create the HTML contents of the hidden
                         * screen reader information region after the chart. Analogous to
                         * [beforeChartFormatter](#accessibility.screenReaderSection.beforeChartFormatter).
                         *
                         * @type      {Highcharts.ScreenReaderFormatterCallbackFunction<Highcharts.Chart>}
                         * @since 8.0.0
                         * @apioption accessibility.screenReaderSection.afterChartFormatter
                         */
                        /**
                         * Format for the screen reader information region after the chart.
                         * Analogous to [beforeChartFormat](#accessibility.screenReaderSection.beforeChartFormat).
                         *
                         * @since 8.0.0
                         */
                        afterChartFormat: '{endOfChartMarker}',
                        /**
                         * Date format to use to describe range of datetime axes.
                         *
                         * For an overview of the replacement codes, see
                         * [dateFormat](/class-reference/Highcharts.Time#dateFormat).
                         *
                         * @see [point.dateFormat](#accessibility.point.dateFormat)
                         *
                         * @since 8.0.0
                         */
                        axisRangeDateFormat: '%Y-%m-%d %H:%M:%S'
                    },
                    /**
                     * Accessibility options global to all data series. Individual series
                     * can also have specific [accessibility options](#plotOptions.series.accessibility)
                     * set.
                     *
                     * @since 8.0.0
                     */
                    series: {
                        /**
                         * Formatter function to use instead of the default for series
                         * descriptions. Receives one argument, `series`, referring to the
                         * series to describe. Should return a string with the description
                         * of the series for a screen reader user. If `false` is returned,
                         * the default formatter will be used for that series.
                         *
                         * @see [series.descriptionFormat](#accessibility.series.descriptionFormat)
                         * @see [series.description](#plotOptions.series.description)
                         *
                         * @type      {Highcharts.ScreenReaderFormatterCallbackFunction<Highcharts.Series>}
                         * @since 8.0.0
                         * @apioption accessibility.series.descriptionFormatter
                         */
                        /**
                         * Format to use for describing the data series group to assistive
                         * technology - including screen readers.
                         *
                         * The series context and its subproperties are available under the
                         * variable `{series}`, for example `{series.name}` for the series
                         * name, and `{series.points.length}` for the number of data points.
                         *
                         * The chart context and its subproperties are available under the
                         * variable `{chart}`, for example `{chart.series.length}` for the
                         * number of series in the chart.
                         *
                         * `{seriesDescription}` refers to the automatic description of the
                         * series type and number of points added by Highcharts by default.
                         * `{authorDescription}` refers to the description added in
                         * [series.description](#plotOptions.series.description) if one is
                         * present. `{axisDescription}` refers to the description added if
                         * the chart has multiple X or Y axes.
                         *
                         * Note that if [series.descriptionFormatter](#accessibility.series.descriptionFormatter)
                         * is declared it will take precedence, and this option will be
                         * overridden.
                         *
                         * @sample highcharts/accessibility/advanced-accessible
                         *  Accessible low-medium-high chart
                         *
                         * @type      {string}
                         * @since 10.1.0
                         */
                        descriptionFormat: '{seriesDescription}{authorDescription}{axisDescription}',
                        /**
                         * Whether or not to add series descriptions to charts with a single
                         * series.
                         *
                         * @since 8.0.0
                         */
                        describeSingleSeries: false,
                        /**
                         * When a series contains more points than this, we no longer expose
                         * information about individual points to screen readers.
                         *
                         * Set to `false` to disable.
                         *
                         * @type  {boolean|number}
                         * @since 8.0.0
                         */
                        pointDescriptionEnabledThreshold: 200
                    },
                    /**
                     * Options for descriptions of individual data points.
                     *
                     * @since 8.0.0
                     */
                    point: {
                        /**
                         * Date format to use for points on datetime axes when describing
                         * them to screen reader users.
                         *
                         * Defaults to the same format as in tooltip.
                         *
                         * For an overview of the replacement codes, see
                         * [dateFormat](/class-reference/Highcharts.Time#dateFormat).
                         *
                         * @see [dateFormatter](#accessibility.point.dateFormatter)
                         *
                         * @type      {string}
                         * @since 8.0.0
                         * @apioption accessibility.point.dateFormat
                         */
                        /**
                         * Formatter function to determine the date/time format used with
                         * points on datetime axes when describing them to screen reader
                         * users. Receives one argument, `point`, referring to the point
                         * to describe. Should return a date format string compatible with
                         * [dateFormat](/class-reference/Highcharts.Time#dateFormat).
                         *
                         * @see [dateFormat](#accessibility.point.dateFormat)
                         *
                         * @type      {Highcharts.ScreenReaderFormatterCallbackFunction<Highcharts.Point>}
                         * @since 8.0.0
                         * @apioption accessibility.point.dateFormatter
                         */
                        /**
                         * Prefix to add to the values in the point descriptions. Uses
                         * [tooltip.valuePrefix](#tooltip.valuePrefix) if not defined.
                         *
                         * @type        {string}
                         * @since 8.0.0
                         * @apioption   accessibility.point.valuePrefix
                         */
                        /**
                         * Suffix to add to the values in the point descriptions. Uses
                         * [tooltip.valueSuffix](#tooltip.valueSuffix) if not defined.
                         *
                         * @type        {string}
                         * @since 8.0.0
                         * @apioption   accessibility.point.valueSuffix
                         */
                        /**
                         * Decimals to use for the values in the point descriptions. Uses
                         * [tooltip.valueDecimals](#tooltip.valueDecimals) if not defined.
                         *
                         * @type        {number}
                         * @since 8.0.0
                         * @apioption   accessibility.point.valueDecimals
                         */
                        /**
                         * Formatter function to use instead of the default for point
                         * descriptions.
                         *
                         * Receives one argument, `point`, referring to the point to
                         * describe. Should return a string with the description of the
                         * point for a screen reader user. If `false` is returned, the
                         * default formatter will be used for that point.
                         *
                         * Note: Prefer using [accessibility.point.valueDescriptionFormat](#accessibility.point.valueDescriptionFormat)
                         * instead if possible, as default functionality such as describing
                         * annotations will be preserved.
                         *
                         * @see [accessibility.point.valueDescriptionFormat](#accessibility.point.valueDescriptionFormat)
                         * @see [point.accessibility.description](#series.line.data.accessibility.description)
                         *
                         * @type      {Highcharts.ScreenReaderFormatterCallbackFunction<Highcharts.Point>}
                         * @since 8.0.0
                         * @apioption accessibility.point.descriptionFormatter
                         */
                        /**
                         * Format to use for describing the values of data points
                         * to assistive technology - including screen readers.
                         * The point context is available as `{point}`.
                         *
                         * Other available context variables include `{index}`, `{value}`, and `{xDescription}`.
                         *
                         * Additionally, the series name, annotation info, and
                         * description added in `point.accessibility.description`
                         * is added by default if relevant. To override this, use the
                         * [accessibility.point.descriptionFormatter](#accessibility.point.descriptionFormatter)
                         * option.
                         *
                         * @see [point.accessibility.description](#series.line.data.accessibility.description)
                         * @see [accessibility.point.descriptionFormatter](#accessibility.point.descriptionFormatter)
                         *
                         * @type      {string}
                         * @since 8.0.1
                         */
                        valueDescriptionFormat: '{xDescription}{separator}{value}.',
                        /**
                         * Whether or not to describe points with the value `null` to
                         * assistive technology, such as screen readers.
                         *
                         * @sample {highmaps} maps/demo/all-areas-as-null
                         *         Accessible map with null points
                         *
                         * @type      {boolean}
                         * @since 10.1.0
                         */
                        describeNull: true
                    },
                    /**
                     * Amount of landmarks/regions to create for screen reader users. More
                     * landmarks can make navigation with screen readers easier, but can
                     * be distracting if there are lots of charts on the page. Three modes
                     * are available:
                     *  - `all`: Adds regions for all series, legend, information
                     *      region.
                     *  - `one`: Adds a single landmark per chart.
                     *  - `disabled`: No landmarks are added.
                     *
                     * @since 7.1.0
                     * @validvalue ["all", "one", "disabled"]
                     */
                    landmarkVerbosity: 'all',
                    /**
                     * Link the chart to an HTML element describing the contents of the
                     * chart.
                     *
                     * It is always recommended to describe charts using visible text, to
                     * improve SEO as well as accessibility for users with disabilities.
                     * This option lets an HTML element with a description be linked to the
                     * chart, so that screen reader users can connect the two.
                     *
                     * By setting this option to a string, Highcharts runs the string as an
                     * HTML selector query on the entire document. If there is only a single
                     * match, this element is linked to the chart. The content of the linked
                     * element will be included in the chart description for screen reader
                     * users.
                     *
                     * By default, the chart looks for an adjacent sibling element with the
                     * `highcharts-description` class.
                     *
                     * The feature can be disabled by setting the option to an empty string,
                     * or overridden by providing the
                     * [accessibility.description](#accessibility.description) option.
                     * Alternatively, the HTML element to link can be passed in directly as
                     * an HTML node.
                     *
                     * If you need the description to be part of the exported image,
                     * consider using the [caption](#caption) feature.
                     *
                     * If you need the description to be hidden visually, use the
                     * [accessibility.description](#accessibility.description) option.
                     *
                     * @see [caption](#caption)
                     * @see [description](#accessibility.description)
                     * @see [typeDescription](#accessibility.typeDescription)
                     *
                     * @sample highcharts/accessibility/accessible-line
                     *         Accessible line chart
                     *
                     * @type  {string|Highcharts.HTMLDOMElement}
                     * @since 8.0.0
                     */
                    linkedDescription: '*[data-highcharts-chart="{index}"] + .highcharts-description',
                    /**
                     * A hook for adding custom components to the accessibility module.
                     * Should be an object mapping component names to instances of classes
                     * inheriting from the Highcharts.AccessibilityComponent base class.
                     * Remember to add the component to the
                     * [keyboardNavigation.order](#accessibility.keyboardNavigation.order)
                     * for the keyboard navigation to be usable.
                     *
                     * @sample highcharts/accessibility/custom-component
                     *         Custom accessibility component
                     *
                     * @type      {*}
                     * @since     7.1.0
                     * @apioption accessibility.customComponents
                     */
                    /**
                     * Theme to apply to the chart when Windows High Contrast Mode is
                     * detected. By default, a high contrast theme matching the high
                     * contrast system system colors is used.
                     *
                     * @type      {*}
                     * @since     7.1.3
                     * @apioption accessibility.highContrastTheme
                     */
                    /**
                     * A text description of the chart.
                     *
                     * **Note: Prefer using [linkedDescription](#accessibility.linkedDescription)
                     * or [caption](#caption.text) instead.**
                     *
                     * If the Accessibility module is loaded, this option is included by
                     * default as a long description of the chart in the hidden screen
                     * reader information region.
                     *
                     * Note: Since Highcharts now supports captions and linked descriptions,
                     * it is preferred to define the description using those methods, as a
                     * visible caption/description benefits all users. If the
                     * `accessibility.description` option is defined, the linked description
                     * is ignored, and the caption is hidden from screen reader users.
                     *
                     * @see [linkedDescription](#accessibility.linkedDescription)
                     * @see [caption](#caption)
                     * @see [typeDescription](#accessibility.typeDescription)
                     *
                     * @type      {string}
                     * @since     5.0.0
                     * @apioption accessibility.description
                     */
                    /**
                     * A text description of the chart type.
                     *
                     * If the Accessibility module is loaded, this will be included in the
                     * description of the chart in the screen reader information region.
                     *
                     * Highcharts will by default attempt to guess the chart type, but for
                     * more complex charts it is recommended to specify this property for
                     * clarity.
                     *
                     * @type      {string}
                     * @since     5.0.0
                     * @apioption accessibility.typeDescription
                     */
                    /**
                     * Options for keyboard navigation.
                     *
                     * @declare Highcharts.KeyboardNavigationOptionsObject
                     * @since   5.0.0
                     */
                    keyboardNavigation: {
                        /**
                         * Enable keyboard navigation for the chart.
                         *
                         * @since 5.0.0
                         */
                        enabled: true,
                        /**
                         * Options for the focus border drawn around elements while
                         * navigating through them.
                         *
                         * @sample highcharts/accessibility/custom-focus
                         *         Custom focus ring
                         *
                         * @declare Highcharts.KeyboardNavigationFocusBorderOptionsObject
                         * @since   6.0.3
                         */
                        focusBorder: {
                            /**
                             * Enable/disable focus border for chart.
                             *
                             * @since 6.0.3
                             */
                            enabled: true,
                            /**
                             * Hide the browser's default focus indicator.
                             *
                             * @since 6.0.4
                             */
                            hideBrowserFocusOutline: true,
                            /**
                             * Style options for the focus border drawn around elements
                             * while navigating through them. Note that some browsers in
                             * addition draw their own borders for focused elements. These
                             * automatic borders cannot be styled by Highcharts.
                             *
                             * In styled mode, the border is given the
                             * `.highcharts-focus-border` class.
                             *
                             * @type    {Highcharts.CSSObject}
                             * @since   6.0.3
                             */
                            style: {
                                /** @internal */
                                color: "#335cad" /* Palette.highlightColor80 */,
                                /** @internal */
                                lineWidth: 2,
                                /** @internal */
                                borderRadius: 3
                            },
                            /**
                             * Focus border margin around the elements.
                             *
                             * @since 6.0.3
                             */
                            margin: 2
                        },
                        /**
                         * Order of tab navigation in the chart. Determines which elements
                         * are tabbed to first. Available elements are: `series`, `zoom`,
                         * `rangeSelector`, `chartMenu`, `legend` and `container`. In
                         * addition, any custom components can be added here. Adding
                         * `container` first in order will make the keyboard focus stop on
                         * the chart container first, requiring the user to tab again to
                         * enter the chart.
                         *
                         * @type  {Array<string>}
                         * @since 7.1.0
                         */
                        order: ['series', 'zoom', 'rangeSelector', 'legend', 'chartMenu'],
                        /**
                         * Whether or not to wrap around when reaching the end of arrow-key
                         * navigation for an element in the chart.
                         * @since 7.1.0
                         */
                        wrapAround: true,
                        /**
                         * Options for the keyboard navigation of data points and series.
                         *
                         * @declare Highcharts.KeyboardNavigationSeriesNavigationOptionsObject
                         * @since 8.0.0
                         */
                        seriesNavigation: {
                            /**
                             * Set the keyboard navigation mode for the chart. Can be
                             * "normal" or "serialize". In normal mode, left/right arrow
                             * keys move between points in a series, while up/down arrow
                             * keys move between series. Up/down navigation acts
                             * intelligently to figure out which series makes sense to move
                             * to from any given point.
                             *
                             * In "serialize" mode, points are instead navigated as a single
                             * list. Left/right behaves as in "normal" mode. Up/down arrow
                             * keys will behave like left/right. This can be useful for
                             * unifying navigation behavior with/without screen readers
                             * enabled.
                             *
                             * @type       {string}
                             * @default    normal
                             * @since 8.0.0
                             * @validvalue ["normal", "serialize"]
                             * @apioption  accessibility.keyboardNavigation.seriesNavigation.mode
                             */
                            /**
                             * Skip null points when navigating through points with the
                             * keyboard.
                             *
                             * @since 8.0.0
                             */
                            skipNullPoints: true,
                            /**
                             * When a series contains more points than this, we no longer
                             * allow keyboard navigation for it.
                             *
                             * Set to `false` to disable.
                             *
                             * @type  {boolean|number}
                             * @since 8.0.0
                             */
                            pointNavigationEnabledThreshold: false,
                            /**
                             * Remember which point was focused even after navigating away
                             * from the series, so that when navigating back to the series
                             * you start at the last focused point.
                             *
                             * @type  {boolean}
                             * @since 10.1.0
                             */
                            rememberPointFocus: false
                        }
                    },
                    /**
                     * Options for announcing new data to screen reader users. Useful
                     * for dynamic data applications and drilldown.
                     *
                     * Keep in mind that frequent announcements will not be useful to
                     * users, as they won't have time to explore the new data. For these
                     * applications, consider making snapshots of the data accessible, and
                     * do the announcements in batches.
                     *
                     * @declare Highcharts.AccessibilityAnnounceNewDataOptionsObject
                     * @since   7.1.0
                     */
                    announceNewData: {
                        /**
                         * Optional formatter callback for the announcement. Receives
                         * up to three arguments. The first argument is always an array
                         * of all series that received updates. If an announcement is
                         * already queued, the series that received updates for that
                         * announcement are also included in this array. The second
                         * argument is provided if `chart.addSeries` was called, and
                         * there is a new series. In that case, this argument is a
                         * reference to the new series. The third argument, similarly,
                         * is provided if `series.addPoint` was called, and there is a
                         * new point. In that case, this argument is a reference to the
                         * new point.
                         *
                         * The function should return a string with the text to announce
                         * to the user. Return empty string to not announce anything.
                         * Return `false` to use the default announcement format.
                         *
                         * @sample highcharts/accessibility/custom-dynamic
                         *         High priority live alerts
                         *
                         * @type      {Highcharts.AccessibilityAnnouncementFormatter}
                         * @apioption accessibility.announceNewData.announcementFormatter
                         */
                        /**
                         * Enable announcing new data to screen reader users
                         * @sample highcharts/accessibility/accessible-dynamic
                         *         Dynamic data accessible
                         */
                        enabled: false,
                        /**
                         * Minimum interval between announcements in milliseconds. If
                         * new data arrives before this amount of time has passed, it is
                         * queued for announcement. If another new data event happens
                         * while an announcement is queued, the queued announcement is
                         * dropped, and the latest announcement is queued instead. Set
                         * to 0 to allow all announcements, but be warned that frequent
                         * announcements are disturbing to users.
                         */
                        minAnnounceInterval: 5000,
                        /**
                         * Choose whether or not the announcements should interrupt the
                         * screen reader. If not enabled, the user will be notified once
                         * idle. It is recommended not to enable this setting unless
                         * there is a specific reason to do so.
                         */
                        interruptUser: false
                    }
                },
                /**
                 * Accessibility options for a data point.
                 *
                 * @declare   Highcharts.PointAccessibilityOptionsObject
                 * @since     7.1.0
                 * @apioption series.line.data.accessibility
                 */
                /**
                 * Provide a description of the data point, announced to screen readers.
                 *
                 * @type      {string}
                 * @since     7.1.0
                 * @apioption series.line.data.accessibility.description
                 */
                /**
                 * Set to false to disable accessibility functionality for a specific point.
                 * The point will not be included in keyboard navigation, and will not be
                 * exposed to assistive technology.
                 *
                 * @type      {boolean}
                 * @since 9.0.1
                 * @apioption series.line.data.accessibility.enabled
                 */
                /**
                 * Accessibility options for a series.
                 *
                 * @declare    Highcharts.SeriesAccessibilityOptionsObject
                 * @since      7.1.0
                 * @requires   modules/accessibility
                 * @apioption  plotOptions.series.accessibility
                 */
                /**
                 * Enable/disable accessibility functionality for a specific series.
                 *
                 * @type       {boolean}
                 * @since      7.1.0
                 * @apioption  plotOptions.series.accessibility.enabled
                 */
                /**
                 * Provide a description of the series, announced to screen readers.
                 *
                 * @type       {string}
                 * @since      7.1.0
                 * @apioption  plotOptions.series.accessibility.description
                 */
                /**
                 * Expose only the series element to screen readers, not its points.
                 *
                 * @type       {boolean}
                 * @since      7.1.0
                 * @apioption  plotOptions.series.accessibility.exposeAsGroupOnly
                 */
                /**
                 * Point accessibility options for a series.
                 *
                 * @extends    accessibility.point
                 * @since 9.3.0
                 * @requires   modules/accessibility
                 * @apioption  plotOptions.series.accessibility.point
                 */
                /**
                 * Formatter function to use instead of the default for point
                 * descriptions. Same as `accessibility.point.descriptionFormatter`, but
                 * applies to a series instead of the whole chart.
                 *
                 * Note: Prefer using [accessibility.point.valueDescriptionFormat](#plotOptions.series.accessibility.point.valueDescriptionFormat)
                 * instead if possible, as default functionality such as describing
                 * annotations will be preserved.
                 *
                 * @see [accessibility.point.valueDescriptionFormat](#plotOptions.series.accessibility.point.valueDescriptionFormat)
                 * @see [point.accessibility.description](#series.line.data.accessibility.description)
                 * @see [accessibility.point.descriptionFormatter](#accessibility.point.descriptionFormatter)
                 *
                 * @type      {Highcharts.ScreenReaderFormatterCallbackFunction<Highcharts.Point>}
                 * @since 9.3.0
                 * @apioption plotOptions.series.accessibility.point.descriptionFormatter
                 */
                /**
                 * Keyboard navigation for a series
                 *
                 * @declare    Highcharts.SeriesAccessibilityKeyboardNavigationOptionsObject
                 * @since      7.1.0
                 * @apioption  plotOptions.series.accessibility.keyboardNavigation
                 */
                /**
                 * Enable/disable keyboard navigation support for a specific series.
                 *
                 * @type       {boolean}
                 * @since      7.1.0
                 * @apioption  plotOptions.series.accessibility.keyboardNavigation.enabled
                 */
                /**
                 * Accessibility options for an annotation label.
                 *
                 * @declare    Highcharts.AnnotationLabelAccessibilityOptionsObject
                 * @since 8.0.1
                 * @requires   modules/accessibility
                 * @apioption  annotations.labelOptions.accessibility
                 */
                /**
                 * Description of an annotation label for screen readers and other assistive
                 * technology.
                 *
                 * @type       {string}
                 * @since 8.0.1
                 * @apioption  annotations.labelOptions.accessibility.description
                 */
                /**
                 * Accessibility options for an axis. Requires the accessibility module.
                 *
                 * @declare    Highcharts.AxisAccessibilityOptionsObject
                 * @since      7.1.0
                 * @requires   modules/accessibility
                 * @apioption  xAxis.accessibility
                 */
                /**
                 * Enable axis accessibility features, including axis information in the
                 * screen reader information region. If this is disabled on the xAxis, the
                 * x values are not exposed to screen readers for the individual data points
                 * by default.
                 *
                 * @type       {boolean}
                 * @since      7.1.0
                 * @apioption  xAxis.accessibility.enabled
                 */
                /**
                 * Description for an axis to expose to screen reader users.
                 *
                 * @type       {string}
                 * @since      7.1.0
                 * @apioption  xAxis.accessibility.description
                 */
                /**
                 * Range description for an axis. Overrides the default range description.
                 * Set to empty to disable range description for this axis.
                 *
                 * @type       {string}
                 * @since      7.1.0
                 * @apioption  xAxis.accessibility.rangeDescription
                 */
                /**
                 * @optionparent legend
                 */
                legend: {
                    /**
                     * Accessibility options for the legend. Requires the Accessibility
                     * module.
                     *
                     * @since     7.1.0
                     * @requires  modules/accessibility
                     */
                    accessibility: {
                        /**
                         * Enable accessibility support for the legend.
                         *
                         * @since  7.1.0
                         */
                        enabled: true,
                        /**
                         * Options for keyboard navigation for the legend.
                         *
                         * @since     7.1.0
                         * @requires  modules/accessibility
                         */
                        keyboardNavigation: {
                            /**
                             * Enable keyboard navigation for the legend.
                             *
                             * @see [accessibility.keyboardNavigation](#accessibility.keyboardNavigation.enabled)
                             *
                             * @since  7.1.0
                             */
                            enabled: true
                        }
                    }
                },
                /**
                 * @optionparent exporting
                 */
                exporting: {
                    /**
                     * Accessibility options for the exporting menu. Requires the
                     * Accessibility module.
                     *
                     * @since    7.1.0
                     * @requires modules/accessibility
                     */
                    accessibility: {
                        /**
                         * Enable accessibility support for the export menu.
                         *
                         * @since 7.1.0
                         */
                        enabled: true
                    }
                }
            };

        return Options;
    });
    _registerModule(_modules, 'Accessibility/Options/LangDefaults.js', [], function () {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Default lang/i18n options for accessibility.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /* *
         *
         *  API Options
         *
         * */
        var langOptions = {
                /**
                 * Configure the accessibility strings in the chart. Requires the
                 * [accessibility module](https://code.highcharts.com/modules/accessibility.js)
                 * to be loaded. For a description of the module and information on its
                 * features, see
                 * [Highcharts Accessibility](https://www.highcharts.com/docs/chart-concepts/accessibility).
                 *
                 * For more dynamic control over the accessibility functionality, see
                 * [accessibility.point.descriptionFormatter](#accessibility.point.descriptionFormatter),
                 * [accessibility.series.descriptionFormatter](#accessibility.series.descriptionFormatter),
                 * and
                 * [accessibility.screenReaderSection.beforeChartFormatter](#accessibility.screenReaderSection.beforeChartFormatter).
                 *
                 * @since        6.0.6
                 * @optionparent lang.accessibility
                 */
                accessibility: {
                    /**
                     * @deprecated 10.2.1
                     * @apioption  lang.accessibility.resetZoomButton
                     */
                    defaultChartTitle: 'Chart',
                    chartContainerLabel: '{title}. Highcharts interactive chart.',
                    svgContainerLabel: 'Interactive chart',
                    drillUpButton: '{buttonText}',
                    credits: 'Chart credits: {creditsStr}',
                    /**
                     * Thousands separator to use when formatting numbers for screen
                     * readers. Note that many screen readers will not handle space as a
                     * thousands separator, and will consider "11 700" as two numbers.
                     *
                     * Set to `null` to use the separator defined in
                     * [lang.thousandsSep](lang.thousandsSep).
                     *
                     * @since 7.1.0
                     */
                    thousandsSep: ',',
                    /**
                     * Title element text for the chart SVG element. Leave this
                     * empty to disable adding the title element. Browsers will display
                     * this content when hovering over elements in the chart. Assistive
                     * technology may use this element to label the chart.
                     *
                     * @since 6.0.8
                     */
                    svgContainerTitle: '',
                    /**
                     * Set a label on the container wrapping the SVG.
                     *
                     * @see [chartContainerLabel](#lang.accessibility.chartContainerLabel)
                     *
                     * @since 8.0.0
                     */
                    graphicContainerLabel: '',
                    /**
                     * Language options for the screen reader information sections added
                     * before and after the charts.
                     *
                     * @since 8.0.0
                     */
                    screenReaderSection: {
                        beforeRegionLabel: '',
                        afterRegionLabel: '',
                        /**
                         * Language options for annotation descriptions.
                         *
                         * @since 8.0.1
                         */
                        annotations: {
                            heading: 'Chart annotations summary',
                            descriptionSinglePoint: ('{annotationText}. Related to {annotationPoint}'),
                            descriptionMultiplePoints: ('{annotationText}. Related to {annotationPoint}' +
                                '{ Also related to, #each(additionalAnnotationPoints)}'),
                            descriptionNoPoints: '{annotationText}'
                        },
                        /**
                         * Label for the end of the chart. Announced by screen readers.
                         *
                         * @since 8.0.0
                         */
                        endOfChartMarker: 'End of interactive chart.'
                    },
                    /**
                     * Language options for sonification.
                     *
                     * @since 8.0.1
                     */
                    sonification: {
                        playAsSoundButtonText: 'Play as sound, {chartTitle}',
                        playAsSoundClickAnnouncement: 'Play'
                    },
                    /**
                     * Language options for accessibility of the legend.
                     *
                     * @since 8.0.0
                     */
                    legend: {
                        legendLabelNoTitle: 'Toggle series visibility, {chartTitle}',
                        legendLabel: 'Chart legend: {legendTitle}',
                        legendItem: 'Show {itemName}'
                    },
                    /**
                     * Chart and map zoom accessibility language options.
                     *
                     * @since 8.0.0
                     */
                    zoom: {
                        mapZoomIn: 'Zoom chart',
                        mapZoomOut: 'Zoom out chart',
                        resetZoomButton: 'Reset zoom'
                    },
                    /**
                     * Range selector language options for accessibility.
                     *
                     * @since 8.0.0
                     */
                    rangeSelector: {
                        dropdownLabel: '{rangeTitle}',
                        minInputLabel: 'Select start date.',
                        maxInputLabel: 'Select end date.',
                        clickButtonAnnouncement: 'Viewing {axisRangeDescription}'
                    },
                    /**
                     * Accessibility language options for the data table.
                     *
                     * @since 8.0.0
                     */
                    table: {
                        viewAsDataTableButtonText: 'View as data table, {chartTitle}',
                        tableSummary: 'Table representation of chart.'
                    },
                    /**
                     * Default announcement for new data in charts. If addPoint or
                     * addSeries is used, and only one series/point is added, the
                     * `newPointAnnounce` and `newSeriesAnnounce` strings are used.
                     * The `...Single` versions will be used if there is only one chart
                     * on the page, and the `...Multiple` versions will be used if there
                     * are multiple charts on the page. For all other new data events,
                     * the `newDataAnnounce` string will be used.
                     *
                     * @since 7.1.0
                     */
                    announceNewData: {
                        newDataAnnounce: 'Updated data for chart {chartTitle}',
                        newSeriesAnnounceSingle: 'New data series: {seriesDesc}',
                        newPointAnnounceSingle: 'New data point: {pointDesc}',
                        newSeriesAnnounceMultiple: 'New data series in chart {chartTitle}: {seriesDesc}',
                        newPointAnnounceMultiple: 'New data point in chart {chartTitle}: {pointDesc}'
                    },
                    /**
                     * Descriptions of lesser known series types. The relevant
                     * description is added to the screen reader information region
                     * when these series types are used.
                     *
                     * @since 6.0.6
                     */
                    seriesTypeDescriptions: {
                        boxplot: 'Box plot charts are typically used to display ' +
                            'groups of statistical data. Each data point in the ' +
                            'chart can have up to 5 values: minimum, lower quartile, ' +
                            'median, upper quartile, and maximum.',
                        arearange: 'Arearange charts are line charts displaying a ' +
                            'range between a lower and higher value for each point.',
                        areasplinerange: 'These charts are line charts displaying a ' +
                            'range between a lower and higher value for each point.',
                        bubble: 'Bubble charts are scatter charts where each data ' +
                            'point also has a size value.',
                        columnrange: 'Columnrange charts are column charts ' +
                            'displaying a range between a lower and higher value for ' +
                            'each point.',
                        errorbar: 'Errorbar series are used to display the ' +
                            'variability of the data.',
                        funnel: 'Funnel charts are used to display reduction of data ' +
                            'in stages.',
                        pyramid: 'Pyramid charts consist of a single pyramid with ' +
                            'item heights corresponding to each point value.',
                        waterfall: 'A waterfall chart is a column chart where each ' +
                            'column contributes towards a total end value.'
                    },
                    /**
                     * Chart type description strings. This is added to the chart
                     * information region.
                     *
                     * If there is only a single series type used in the chart, we use
                     * the format string for the series type, or default if missing.
                     * There is one format string for cases where there is only a single
                     * series in the chart, and one for multiple series of the same
                     * type.
                     *
                     * @since 6.0.6
                     */
                    chartTypes: {
                        /* eslint-disable max-len */
                        emptyChart: 'Empty chart',
                        mapTypeDescription: 'Map of {mapTitle} with {numSeries} data series.',
                        unknownMap: 'Map of unspecified region with {numSeries} data series.',
                        combinationChart: 'Combination chart with {numSeries} data series.',
                        defaultSingle: 'Chart with {numPoints} data {#plural(numPoints, points, point)}.',
                        defaultMultiple: 'Chart with {numSeries} data series.',
                        splineSingle: 'Line chart with {numPoints} data {#plural(numPoints, points, point)}.',
                        splineMultiple: 'Line chart with {numSeries} lines.',
                        lineSingle: 'Line chart with {numPoints} data {#plural(numPoints, points, point)}.',
                        lineMultiple: 'Line chart with {numSeries} lines.',
                        columnSingle: 'Bar chart with {numPoints} {#plural(numPoints, bars, bar)}.',
                        columnMultiple: 'Bar chart with {numSeries} data series.',
                        barSingle: 'Bar chart with {numPoints} {#plural(numPoints, bars, bar)}.',
                        barMultiple: 'Bar chart with {numSeries} data series.',
                        pieSingle: 'Pie chart with {numPoints} {#plural(numPoints, slices, slice)}.',
                        pieMultiple: 'Pie chart with {numSeries} pies.',
                        scatterSingle: 'Scatter chart with {numPoints} {#plural(numPoints, points, point)}.',
                        scatterMultiple: 'Scatter chart with {numSeries} data series.',
                        boxplotSingle: 'Boxplot with {numPoints} {#plural(numPoints, boxes, box)}.',
                        boxplotMultiple: 'Boxplot with {numSeries} data series.',
                        bubbleSingle: 'Bubble chart with {numPoints} {#plural(numPoints, bubbles, bubble)}.',
                        bubbleMultiple: 'Bubble chart with {numSeries} data series.'
                    },
                    /**
                     * Axis description format strings.
                     *
                     * @since 6.0.6
                     */
                    axis: {
                        /* eslint-disable max-len */
                        xAxisDescriptionSingular: 'The chart has 1 X axis displaying {names[0]}. {ranges[0]}',
                        xAxisDescriptionPlural: 'The chart has {numAxes} X axes displaying {#each(names, -1) }and {names[-1]}.',
                        yAxisDescriptionSingular: 'The chart has 1 Y axis displaying {names[0]}. {ranges[0]}',
                        yAxisDescriptionPlural: 'The chart has {numAxes} Y axes displaying {#each(names, -1) }and {names[-1]}.',
                        timeRangeDays: 'Data range: {range} days.',
                        timeRangeHours: 'Data range: {range} hours.',
                        timeRangeMinutes: 'Data range: {range} minutes.',
                        timeRangeSeconds: 'Data range: {range} seconds.',
                        rangeFromTo: 'Data ranges from {rangeFrom} to {rangeTo}.',
                        rangeCategories: 'Data range: {numCategories} categories.'
                    },
                    /**
                     * Exporting menu format strings for accessibility module.
                     *
                     * @since 6.0.6
                     */
                    exporting: {
                        chartMenuLabel: 'Chart menu',
                        menuButtonLabel: 'View chart menu, {chartTitle}'
                    },
                    /**
                     * Lang configuration for different series types. For more dynamic
                     * control over the series element descriptions, see
                     * [accessibility.seriesDescriptionFormatter](#accessibility.seriesDescriptionFormatter).
                     *
                     * @since 6.0.6
                     */
                    series: {
                        /**
                         * Lang configuration for the series main summary. Each series
                         * type has two modes:
                         *
                         * 1. This series type is the only series type used in the
                         *    chart
                         *
                         * 2. This is a combination chart with multiple series types
                         *
                         * If a definition does not exist for the specific series type
                         * and mode, the 'default' lang definitions are used.
                         *
                         * Chart and its subproperties can be accessed with the `{chart}` variable.
                         * The series and its subproperties can be accessed with the `{series}` variable.
                         *
                         * The series index (starting from 1) can be accessed with the `{seriesNumber}` variable.
                         *
                         * @since 6.0.6
                         */
                        summary: {
                            /* eslint-disable max-len */
                            'default': '{series.name}, series {seriesNumber} of {chart.series.length} with {series.points.length} data {#plural(series.points.length, points, point)}.',
                            defaultCombination: '{series.name}, series {seriesNumber} of {chart.series.length} with {series.points.length} data {#plural(series.points.length, points, point)}.',
                            line: '{series.name}, line {seriesNumber} of {chart.series.length} with {series.points.length} data {#plural(series.points.length, points, point)}.',
                            lineCombination: '{series.name}, series {seriesNumber} of {chart.series.length}. Line with {series.points.length} data {#plural(series.points.length, points, point)}.',
                            spline: '{series.name}, line {seriesNumber} of {chart.series.length} with {series.points.length} data {#plural(series.points.length, points, point)}.',
                            splineCombination: '{series.name}, series {seriesNumber} of {chart.series.length}. Line with {series.points.length} data {#plural(series.points.length, points, point)}.',
                            column: '{series.name}, bar series {seriesNumber} of {chart.series.length} with {series.points.length} {#plural(series.points.length, bars, bar)}.',
                            columnCombination: '{series.name}, series {seriesNumber} of {chart.series.length}. Bar series with {series.points.length} {#plural(series.points.length, bars, bar)}.',
                            bar: '{series.name}, bar series {seriesNumber} of {chart.series.length} with {series.points.length} {#plural(series.points.length, bars, bar)}.',
                            barCombination: '{series.name}, series {seriesNumber} of {chart.series.length}. Bar series with {series.points.length} {#plural(series.points.length, bars, bar)}.',
                            pie: '{series.name}, pie {seriesNumber} of {chart.series.length} with {series.points.length} {#plural(series.points.length, slices, slice)}.',
                            pieCombination: '{series.name}, series {seriesNumber} of {chart.series.length}. Pie with {series.points.length} {#plural(series.points.length, slices, slice)}.',
                            scatter: '{series.name}, scatter plot {seriesNumber} of {chart.series.length} with {series.points.length} {#plural(series.points.length, points, point)}.',
                            scatterCombination: '{series.name}, series {seriesNumber} of {chart.series.length}, scatter plot with {series.points.length} {#plural(series.points.length, points, point)}.',
                            boxplot: '{series.name}, boxplot {seriesNumber} of {chart.series.length} with {series.points.length} {#plural(series.points.length, boxes, box)}.',
                            boxplotCombination: '{series.name}, series {seriesNumber} of {chart.series.length}. Boxplot with {series.points.length} {#plural(series.points.length, boxes, box)}.',
                            bubble: '{series.name}, bubble series {seriesNumber} of {chart.series.length} with {series.points.length} {#plural(series.points.length, bubbles, bubble)}.',
                            bubbleCombination: '{series.name}, series {seriesNumber} of {chart.series.length}. Bubble series with {series.points.length} {#plural(series.points.length, bubbles, bubble)}.',
                            map: '{series.name}, map {seriesNumber} of {chart.series.length} with {series.points.length} {#plural(series.points.length, areas, area)}.',
                            mapCombination: '{series.name}, series {seriesNumber} of {chart.series.length}. Map with {series.points.length} {#plural(series.points.length, areas, area)}.',
                            mapline: '{series.name}, line {seriesNumber} of {chart.series.length} with {series.points.length} data {#plural(series.points.length, points, point)}.',
                            maplineCombination: '{series.name}, series {seriesNumber} of {chart.series.length}. Line with {series.points.length} data {#plural(series.points.length, points, point)}.',
                            mapbubble: '{series.name}, bubble series {seriesNumber} of {chart.series.length} with {series.points.length} {#plural(series.points.length, bubbles, bubble)}.',
                            mapbubbleCombination: '{series.name}, series {seriesNumber} of {chart.series.length}. Bubble series with {series.points.length} {#plural(series.points.length, bubbles, bubble)}.'
                        },
                        /**
                         * User supplied description text. This is added in the point
                         * comment description by default if present.
                         *
                         * @since 6.0.6
                         */
                        description: '{description}',
                        /**
                         * xAxis description for series if there are multiple xAxes in
                         * the chart.
                         *
                         * @since 6.0.6
                         */
                        xAxisDescription: 'X axis, {name}',
                        /**
                         * yAxis description for series if there are multiple yAxes in
                         * the chart.
                         *
                         * @since 6.0.6
                         */
                        yAxisDescription: 'Y axis, {name}',
                        /**
                         * Description for the value of null points.
                         *
                         * @since 8.0.0
                         */
                        nullPointValue: 'No value',
                        /**
                         * Description for annotations on a point, as it is made available
                         * to assistive technology.
                         *
                         * @since 8.0.1
                         */
                        pointAnnotationsDescription: '{Annotation: #each(annotations). }'
                    }
                }
            };
        /* *
         *
         *  Default Export
         *
         * */

        return langOptions;
    });
    _registerModule(_modules, 'Accessibility/Options/DeprecatedOptions.js', [_modules['Core/Utilities.js']], function (U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Default options for accessibility.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /* eslint-disable max-len */
        /*
         *  List of deprecated options:
         *
         *  chart.description -> accessibility.description
         *  chart.typeDescription -> accessibility.typeDescription
         *  series.description -> series.accessibility.description
         *  series.exposeElementToA11y -> series.accessibility.exposeAsGroupOnly
         *  series.pointDescriptionFormatter ->
         *      series.accessibility.pointDescriptionFormatter
         *  series.accessibility.pointDescriptionFormatter ->
         *      series.accessibility.point.descriptionFormatter
         *  series.skipKeyboardNavigation ->
         *      series.accessibility.keyboardNavigation.enabled
         *  point.description -> point.accessibility.description !!!! WARNING: No longer deprecated and handled, removed for HC8.
         *  axis.description -> axis.accessibility.description
         *
         *  accessibility.pointDateFormat -> accessibility.point.dateFormat
         *  accessibility.addTableShortcut -> Handled by screenReaderSection.beforeChartFormat
         *  accessibility.pointDateFormatter -> accessibility.point.dateFormatter
         *  accessibility.pointDescriptionFormatter -> accessibility.point.descriptionFormatter
         *  accessibility.pointDescriptionThreshold -> accessibility.series.pointDescriptionEnabledThreshold
         *  accessibility.pointNavigationThreshold -> accessibility.keyboardNavigation.seriesNavigation.pointNavigationEnabledThreshold
         *  accessibility.pointValueDecimals -> accessibility.point.valueDecimals
         *  accessibility.pointValuePrefix -> accessibility.point.valuePrefix
         *  accessibility.pointValueSuffix -> accessibility.point.valueSuffix
         *  accessibility.screenReaderSectionFormatter -> accessibility.screenReaderSection.beforeChartFormatter
         *  accessibility.describeSingleSeries -> accessibility.series.describeSingleSeries
         *  accessibility.seriesDescriptionFormatter -> accessibility.series.descriptionFormatter
         *  accessibility.onTableAnchorClick -> accessibility.screenReaderSection.onViewDataTableClick
         *  accessibility.axisRangeDateFormat -> accessibility.screenReaderSection.axisRangeDateFormat
         *  accessibility.keyboardNavigation.skipNullPoints -> accessibility.keyboardNavigation.seriesNavigation.skipNullPoints
         *  accessibility.keyboardNavigation.mode -> accessibility.keyboardNavigation.seriesNavigation.mode
         *
         *  lang.accessibility.chartHeading -> no longer used, remove
         *  lang.accessibility.legendItem -> lang.accessibility.legend.legendItem
         *  lang.accessibility.legendLabel -> lang.accessibility.legend.legendLabel
         *  lang.accessibility.mapZoomIn -> lang.accessibility.zoom.mapZoomIn
         *  lang.accessibility.mapZoomOut -> lang.accessibility.zoom.mapZoomOut
         *  lang.accessibility.resetZoomButton -> lang.accessibility.zoom.resetZoomButton
         *  lang.accessibility.screenReaderRegionLabel -> lang.accessibility.screenReaderSection.beforeRegionLabel
         *  lang.accessibility.rangeSelectorButton -> lang.accessibility.rangeSelector.buttonText
         *  lang.accessibility.rangeSelectorMaxInput -> lang.accessibility.rangeSelector.maxInputLabel
         *  lang.accessibility.rangeSelectorMinInput -> lang.accessibility.rangeSelector.minInputLabel
         *  lang.accessibility.svgContainerEnd -> lang.accessibility.screenReaderSection.endOfChartMarker
         *  lang.accessibility.viewAsDataTable -> lang.accessibility.table.viewAsDataTableButtonText
         *  lang.accessibility.tableSummary -> lang.accessibility.table.tableSummary
         *
         */
        /* eslint-enable max-len */
        var error = U.error,
            pick = U.pick;
        /* *
         *
         *  Functions
         *
         * */
        /* eslint-disable valid-jsdoc */
        /**
         * Set a new option on a root prop, where the option is defined as an array of
         * suboptions.
         * @private
         * @param root
         * @param {Array<string>} optionAsArray
         * @param {*} val
         * @return {void}
         */
        function traverseSetOption(root, optionAsArray, val) {
            var opt = root,
                prop,
                i = 0;
            for (; i < optionAsArray.length - 1; ++i) {
                prop = optionAsArray[i];
                opt = opt[prop] = pick(opt[prop], {});
            }
            opt[optionAsArray[optionAsArray.length - 1]] = val;
        }
        /**
         * If we have a clear root option node for old and new options and a mapping
         * between, we can use this generic function for the copy and warn logic.
         */
        function deprecateFromOptionsMap(chart, rootOldAsArray, rootNewAsArray, mapToNewOptions) {
            /**
             * @private
             */
            function getChildProp(root, propAsArray) {
                return propAsArray.reduce(function (acc, cur) {
                    return acc[cur];
                }, root);
            }
            var rootOld = getChildProp(chart.options,
                rootOldAsArray),
                rootNew = getChildProp(chart.options,
                rootNewAsArray);
            Object.keys(mapToNewOptions).forEach(function (oldOptionKey) {
                var _a;
                var val = rootOld[oldOptionKey];
                if (typeof val !== 'undefined') {
                    traverseSetOption(rootNew, mapToNewOptions[oldOptionKey], val);
                    error(32, false, chart, (_a = {},
                        _a[rootOldAsArray.join('.') + '.' + oldOptionKey] = (rootNewAsArray.join('.') + '.' +
                            mapToNewOptions[oldOptionKey].join('.')),
                        _a));
                }
            });
        }
        /**
         * @private
         */
        function copyDeprecatedChartOptions(chart) {
            var chartOptions = chart.options.chart,
                a11yOptions = chart.options.accessibility || {};
            ['description', 'typeDescription'].forEach(function (prop) {
                var _a;
                if (chartOptions[prop]) {
                    a11yOptions[prop] = chartOptions[prop];
                    error(32, false, chart, (_a = {}, _a["chart.".concat(prop)] = "use accessibility.".concat(prop), _a));
                }
            });
        }
        /**
         * @private
         */
        function copyDeprecatedAxisOptions(chart) {
            chart.axes.forEach(function (axis) {
                var opts = axis.options;
                if (opts && opts.description) {
                    opts.accessibility = opts.accessibility || {};
                    opts.accessibility.description = opts.description;
                    error(32, false, chart, {
                        'axis.description': 'use axis.accessibility.description'
                    });
                }
            });
        }
        /**
         * @private
         */
        function copyDeprecatedSeriesOptions(chart) {
            // Map of deprecated series options. New options are defined as
            // arrays of paths under series.options.
            var oldToNewSeriesOptions = {
                    description: ['accessibility', 'description'],
                    exposeElementToA11y: ['accessibility', 'exposeAsGroupOnly'],
                    pointDescriptionFormatter: [
                        'accessibility', 'point', 'descriptionFormatter'
                    ],
                    skipKeyboardNavigation: [
                        'accessibility', 'keyboardNavigation', 'enabled'
                    ],
                    'accessibility.pointDescriptionFormatter': [
                        'accessibility', 'point', 'descriptionFormatter'
                    ]
                };
            chart.series.forEach(function (series) {
                // Handle series wide options
                Object.keys(oldToNewSeriesOptions).forEach(function (oldOption) {
                    var _a;
                    var optionVal = series.options[oldOption];
                    // Special case
                    if (oldOption === 'accessibility.pointDescriptionFormatter') {
                        optionVal = (series.options.accessibility &&
                            series.options.accessibility
                                .pointDescriptionFormatter);
                    }
                    if (typeof optionVal !== 'undefined') {
                        // Set the new option
                        traverseSetOption(series.options, oldToNewSeriesOptions[oldOption], 
                        // Note that skipKeyboardNavigation has inverted option
                        // value, since we set enabled rather than disabled
                        oldOption === 'skipKeyboardNavigation' ?
                            !optionVal : optionVal);
                        error(32, false, chart, (_a = {},
                            _a["series.".concat(oldOption)] = ('series.' +
                                oldToNewSeriesOptions[oldOption].join('.')),
                            _a));
                    }
                });
            });
        }
        /**
         * @private
         */
        function copyDeprecatedTopLevelAccessibilityOptions(chart) {
            deprecateFromOptionsMap(chart, ['accessibility'], ['accessibility'], {
                pointDateFormat: ['point', 'dateFormat'],
                pointDateFormatter: ['point', 'dateFormatter'],
                pointDescriptionFormatter: ['point', 'descriptionFormatter'],
                pointDescriptionThreshold: ['series',
                    'pointDescriptionEnabledThreshold'],
                pointNavigationThreshold: ['keyboardNavigation', 'seriesNavigation',
                    'pointNavigationEnabledThreshold'],
                pointValueDecimals: ['point', 'valueDecimals'],
                pointValuePrefix: ['point', 'valuePrefix'],
                pointValueSuffix: ['point', 'valueSuffix'],
                screenReaderSectionFormatter: ['screenReaderSection',
                    'beforeChartFormatter'],
                describeSingleSeries: ['series', 'describeSingleSeries'],
                seriesDescriptionFormatter: ['series', 'descriptionFormatter'],
                onTableAnchorClick: ['screenReaderSection', 'onViewDataTableClick'],
                axisRangeDateFormat: ['screenReaderSection', 'axisRangeDateFormat']
            });
        }
        /**
         * @private
         */
        function copyDeprecatedKeyboardNavigationOptions(chart) {
            deprecateFromOptionsMap(chart, ['accessibility', 'keyboardNavigation'], ['accessibility', 'keyboardNavigation', 'seriesNavigation'], {
                skipNullPoints: ['skipNullPoints'],
                mode: ['mode']
            });
        }
        /**
         * @private
         */
        function copyDeprecatedLangOptions(chart) {
            deprecateFromOptionsMap(chart, ['lang', 'accessibility'], ['lang', 'accessibility'], {
                legendItem: ['legend', 'legendItem'],
                legendLabel: ['legend', 'legendLabel'],
                mapZoomIn: ['zoom', 'mapZoomIn'],
                mapZoomOut: ['zoom', 'mapZoomOut'],
                resetZoomButton: ['zoom', 'resetZoomButton'],
                screenReaderRegionLabel: ['screenReaderSection',
                    'beforeRegionLabel'],
                rangeSelectorButton: ['rangeSelector', 'buttonText'],
                rangeSelectorMaxInput: ['rangeSelector', 'maxInputLabel'],
                rangeSelectorMinInput: ['rangeSelector', 'minInputLabel'],
                svgContainerEnd: ['screenReaderSection', 'endOfChartMarker'],
                viewAsDataTable: ['table', 'viewAsDataTableButtonText'],
                tableSummary: ['table', 'tableSummary']
            });
        }
        /**
         * Copy options that are deprecated over to new options. Logs warnings to
         * console if deprecated options are used.
         *
         * @private
         */
        function copyDeprecatedOptions(chart) {
            copyDeprecatedChartOptions(chart);
            copyDeprecatedAxisOptions(chart);
            if (chart.series) {
                copyDeprecatedSeriesOptions(chart);
            }
            copyDeprecatedTopLevelAccessibilityOptions(chart);
            copyDeprecatedKeyboardNavigationOptions(chart);
            copyDeprecatedLangOptions(chart);
        }
        /* *
         *
         *  Default Export
         *
         * */

        return copyDeprecatedOptions;
    });
    _registerModule(_modules, 'Accessibility/Accessibility.js', [_modules['Core/Defaults.js'], _modules['Core/Globals.js'], _modules['Core/Utilities.js'], _modules['Accessibility/Utils/HTMLUtilities.js'], _modules['Accessibility/A11yI18n.js'], _modules['Accessibility/Components/ContainerComponent.js'], _modules['Accessibility/FocusBorder.js'], _modules['Accessibility/Components/InfoRegionsComponent.js'], _modules['Accessibility/KeyboardNavigation.js'], _modules['Accessibility/Components/LegendComponent.js'], _modules['Accessibility/Components/MenuComponent.js'], _modules['Accessibility/Components/SeriesComponent/NewDataAnnouncer.js'], _modules['Accessibility/ProxyProvider.js'], _modules['Accessibility/Components/RangeSelectorComponent.js'], _modules['Accessibility/Components/SeriesComponent/SeriesComponent.js'], _modules['Accessibility/Components/ZoomComponent.js'], _modules['Accessibility/HighContrastMode.js'], _modules['Accessibility/HighContrastTheme.js'], _modules['Accessibility/Options/A11yDefaults.js'], _modules['Accessibility/Options/LangDefaults.js'], _modules['Accessibility/Options/DeprecatedOptions.js']], function (D, H, U, HU, A11yI18n, ContainerComponent, FocusBorder, InfoRegionsComponent, KeyboardNavigation, LegendComponent, MenuComponent, NewDataAnnouncer, ProxyProvider, RangeSelectorComponent, SeriesComponent, ZoomComponent, whcm, highContrastTheme, defaultOptionsA11Y, defaultLangOptions, copyDeprecatedOptions) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Accessibility module for Highcharts
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var defaultOptions = D.defaultOptions;
        var doc = H.doc;
        var addEvent = U.addEvent,
            extend = U.extend,
            fireEvent = U.fireEvent,
            merge = U.merge;
        var removeElement = HU.removeElement;
        /* *
         *
         *  Class
         *
         * */
        /**
         * The Accessibility class
         *
         * @private
         * @requires module:modules/accessibility
         *
         * @class
         * @name Highcharts.Accessibility
         *
         * @param {Highcharts.Chart} chart
         * Chart object
         */
        var Accessibility = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function Accessibility(chart) {
                    /* *
                     *
                     *  Properties
                     *
                     * */
                    this.chart = void 0;
                this.components = void 0;
                this.keyboardNavigation = void 0;
                this.proxyProvider = void 0;
                this.init(chart);
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Initialize the accessibility class
             * @private
             * @param {Highcharts.Chart} chart
             *        Chart object
             */
            Accessibility.prototype.init = function (chart) {
                this.chart = chart;
                // Abort on old browsers
                if (!doc.addEventListener || !chart.renderer.isSVG) {
                    this.zombie = true;
                    this.components = {};
                    chart.renderTo.setAttribute('aria-hidden', true);
                    return;
                }
                // Copy over any deprecated options that are used. We could do this on
                // every update, but it is probably not needed.
                copyDeprecatedOptions(chart);
                this.proxyProvider = new ProxyProvider(this.chart);
                this.initComponents();
                this.keyboardNavigation = new KeyboardNavigation(chart, this.components);
            };
            /**
             * @private
             */
            Accessibility.prototype.initComponents = function () {
                var chart = this.chart;
                var proxyProvider = this.proxyProvider;
                var a11yOptions = chart.options.accessibility;
                this.components = {
                    container: new ContainerComponent(),
                    infoRegions: new InfoRegionsComponent(),
                    legend: new LegendComponent(),
                    chartMenu: new MenuComponent(),
                    rangeSelector: new RangeSelectorComponent(),
                    series: new SeriesComponent(),
                    zoom: new ZoomComponent()
                };
                if (a11yOptions.customComponents) {
                    extend(this.components, a11yOptions.customComponents);
                }
                var components = this.components;
                this.getComponentOrder().forEach(function (componentName) {
                    components[componentName].initBase(chart, proxyProvider);
                    components[componentName].init();
                });
            };
            /**
             * Get order to update components in.
             * @private
             */
            Accessibility.prototype.getComponentOrder = function () {
                if (!this.components) {
                    return []; // For zombie accessibility object on old browsers
                }
                if (!this.components.series) {
                    return Object.keys(this.components);
                }
                var componentsExceptSeries = Object.keys(this.components)
                        .filter(function (c) { return c !== 'series'; });
                // Update series first, so that other components can read accessibility
                // info on points.
                return ['series'].concat(componentsExceptSeries);
            };
            /**
             * Update all components.
             */
            Accessibility.prototype.update = function () {
                var components = this.components,
                    chart = this.chart,
                    a11yOptions = chart.options.accessibility;
                fireEvent(chart, 'beforeA11yUpdate');
                // Update the chart type list as this is used by multiple modules
                chart.types = this.getChartTypes();
                // Update proxies. We don't update proxy positions since most likely we
                // need to recreate the proxies on update.
                var kbdNavOrder = a11yOptions.keyboardNavigation.order;
                this.proxyProvider.updateGroupOrder(kbdNavOrder);
                // Update markup
                this.getComponentOrder().forEach(function (componentName) {
                    components[componentName].onChartUpdate();
                    fireEvent(chart, 'afterA11yComponentUpdate', {
                        name: componentName,
                        component: components[componentName]
                    });
                });
                // Update keyboard navigation
                this.keyboardNavigation.update(kbdNavOrder);
                // Handle high contrast mode
                if (!chart.highContrastModeActive && // Only do this once
                    whcm.isHighContrastModeActive()) {
                    whcm.setHighContrastTheme(chart);
                }
                fireEvent(chart, 'afterA11yUpdate', {
                    accessibility: this
                });
            };
            /**
             * Destroy all elements.
             */
            Accessibility.prototype.destroy = function () {
                var chart = this.chart || {};
                // Destroy components
                var components = this.components;
                Object.keys(components).forEach(function (componentName) {
                    components[componentName].destroy();
                    components[componentName].destroyBase();
                });
                // Destroy proxy provider
                if (this.proxyProvider) {
                    this.proxyProvider.destroy();
                }
                // Remove announcer container
                if (chart.announcerContainer) {
                    removeElement(chart.announcerContainer);
                }
                // Kill keyboard nav
                if (this.keyboardNavigation) {
                    this.keyboardNavigation.destroy();
                }
                // Hide container from screen readers if it exists
                if (chart.renderTo) {
                    chart.renderTo.setAttribute('aria-hidden', true);
                }
                // Remove focus border if it exists
                if (chart.focusElement) {
                    chart.focusElement.removeFocusBorder();
                }
            };
            /**
             * Return a list of the types of series we have in the chart.
             * @private
             */
            Accessibility.prototype.getChartTypes = function () {
                var types = {};
                this.chart.series.forEach(function (series) {
                    types[series.type] = 1;
                });
                return Object.keys(types);
            };
            return Accessibility;
        }());
        /* *
         *
         *  Class Namespace
         *
         * */
        (function (Accessibility) {
            /* *
             *
             *  Declarations
             *
             * */
            /* *
             *
             *  Constants
             *
             * */
            var composedClasses = [];
            Accessibility.i18nFormat = A11yI18n.i18nFormat;
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Destroy with chart.
             * @private
             */
            function chartOnDestroy() {
                if (this.accessibility) {
                    this.accessibility.destroy();
                }
            }
            /**
             * Handle updates to the module and send render updates to components.
             * @private
             */
            function chartOnRender() {
                // Update/destroy
                if (this.a11yDirty && this.renderTo) {
                    delete this.a11yDirty;
                    this.updateA11yEnabled();
                }
                var a11y = this.accessibility;
                if (a11y && !a11y.zombie) {
                    a11y.proxyProvider.updateProxyElementPositions();
                    a11y.getComponentOrder().forEach(function (componentName) {
                        a11y.components[componentName].onChartRender();
                    });
                }
            }
            /**
             * Update with chart/series/point updates.
             * @private
             */
            function chartOnUpdate(e) {
                // Merge new options
                var newOptions = e.options.accessibility;
                if (newOptions) {
                    // Handle custom component updating specifically
                    if (newOptions.customComponents) {
                        this.options.accessibility.customComponents =
                            newOptions.customComponents;
                        delete newOptions.customComponents;
                    }
                    merge(true, this.options.accessibility, newOptions);
                    // Recreate from scratch
                    if (this.accessibility && this.accessibility.destroy) {
                        this.accessibility.destroy();
                        delete this.accessibility;
                    }
                }
                // Mark dirty for update
                this.a11yDirty = true;
            }
            /**
             * @private
             */
            function chartUpdateA11yEnabled() {
                var a11y = this.accessibility;
                var accessibilityOptions = this.options.accessibility;
                if (accessibilityOptions && accessibilityOptions.enabled) {
                    if (a11y && !a11y.zombie) {
                        a11y.update();
                    }
                    else {
                        this.accessibility = a11y = new Accessibility(this);
                        if (a11y && !a11y.zombie) {
                            a11y.update();
                        }
                    }
                }
                else if (a11y) {
                    // Destroy if after update we have a11y and it is disabled
                    if (a11y.destroy) {
                        a11y.destroy();
                    }
                    delete this.accessibility;
                }
                else {
                    // Just hide container
                    this.renderTo.setAttribute('aria-hidden', true);
                }
            }
            /**
             * @private
             */
            function compose(ChartClass, LegendClass, PointClass, SeriesClass, SVGElementClass, RangeSelectorClass) {
                // ordered:
                KeyboardNavigation.compose(ChartClass);
                NewDataAnnouncer.compose(SeriesClass);
                LegendComponent.compose(ChartClass, LegendClass);
                MenuComponent.compose(ChartClass);
                SeriesComponent.compose(ChartClass, PointClass, SeriesClass);
                // RangeSelector
                A11yI18n.compose(ChartClass);
                FocusBorder.compose(ChartClass, SVGElementClass);
                if (RangeSelectorClass) {
                    RangeSelectorComponent.compose(ChartClass, RangeSelectorClass);
                }
                if (composedClasses.indexOf(ChartClass) === -1) {
                    composedClasses.push(ChartClass);
                    var chartProto = ChartClass.prototype;
                    chartProto.updateA11yEnabled = chartUpdateA11yEnabled;
                    addEvent(ChartClass, 'destroy', chartOnDestroy);
                    addEvent(ChartClass, 'render', chartOnRender);
                    addEvent(ChartClass, 'update', chartOnUpdate);
                    // Mark dirty for update
                    ['addSeries', 'init'].forEach(function (event) {
                        addEvent(ChartClass, event, function () {
                            this.a11yDirty = true;
                        });
                    });
                    // Direct updates (events happen after render)
                    ['afterApplyDrilldown', 'drillupall'].forEach(function (event) {
                        addEvent(ChartClass, event, function chartOnAfterDrilldown() {
                            var a11y = this.accessibility;
                            if (a11y && !a11y.zombie) {
                                a11y.update();
                            }
                        });
                    });
                }
                if (composedClasses.indexOf(PointClass) === -1) {
                    composedClasses.push(PointClass);
                    addEvent(PointClass, 'update', pointOnUpdate);
                }
                if (composedClasses.indexOf(SeriesClass) === -1) {
                    composedClasses.push(SeriesClass);
                    // Mark dirty for update
                    ['update', 'updatedData', 'remove'].forEach(function (event) {
                        addEvent(SeriesClass, event, function () {
                            if (this.chart.accessibility) {
                                this.chart.a11yDirty = true;
                            }
                        });
                    });
                }
            }
            Accessibility.compose = compose;
            /**
             * Mark dirty for update.
             * @private
             */
            function pointOnUpdate() {
                if (this.series.chart.accessibility) {
                    this.series.chart.a11yDirty = true;
                }
            }
        })(Accessibility || (Accessibility = {}));
        /* *
         *
         *  Registry
         *
         * */
        // Add default options
        merge(true, defaultOptions, defaultOptionsA11Y, {
            accessibility: {
                highContrastTheme: highContrastTheme
            },
            lang: defaultLangOptions
        });
        /* *
         *
         *  Default Export
         *
         * */

        return Accessibility;
    });
    _registerModule(_modules, 'masters/modules/accessibility.src.js', [_modules['Core/Globals.js'], _modules['Accessibility/Accessibility.js'], _modules['Accessibility/AccessibilityComponent.js'], _modules['Accessibility/Utils/ChartUtilities.js'], _modules['Accessibility/Utils/HTMLUtilities.js'], _modules['Accessibility/KeyboardNavigationHandler.js'], _modules['Accessibility/Components/SeriesComponent/SeriesDescriber.js']], function (Highcharts, Accessibility, AccessibilityComponent, ChartUtilities, HTMLUtilities, KeyboardNavigationHandler, SeriesDescriber) {

        var G = Highcharts;
        G.i18nFormat = Accessibility.i18nFormat;
        G.A11yChartUtilities = ChartUtilities;
        G.A11yHTMLUtilities = HTMLUtilities;
        G.AccessibilityComponent = AccessibilityComponent;
        G.KeyboardNavigationHandler = KeyboardNavigationHandler;
        G.SeriesAccessibilityDescriber = SeriesDescriber;
        Accessibility.compose(G.Chart, G.Legend, G.Point, G.Series, G.SVGElement, G.RangeSelector);

    });
}));