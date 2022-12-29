/**
 * @license Highstock JS v10.3.2 (2022-11-28)
 *
 * Highcharts Stock as a plugin for Highcharts
 *
 * (c) 2010-2021 Torstein Honsi
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/stock', ['highcharts'], function (Highcharts) {
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
    _registerModule(_modules, 'Core/Axis/BrokenAxis.js', [_modules['Core/Axis/Stacking/StackItem.js'], _modules['Core/Utilities.js']], function (StackItem, U) {
        /* *
         *
         *  (c) 2009-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var addEvent = U.addEvent,
            find = U.find,
            fireEvent = U.fireEvent,
            isArray = U.isArray,
            isNumber = U.isNumber,
            pick = U.pick;
        /* *
         *
         *  Composition
         *
         * */
        /**
         * Axis with support of broken data rows.
         * @private
         */
        var BrokenAxis;
        (function (BrokenAxis) {
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
             * Adds support for broken axes.
             * @private
             */
            function compose(AxisClass, SeriesClass) {
                if (composedClasses.indexOf(AxisClass) === -1) {
                    composedClasses.push(AxisClass);
                    AxisClass.keepProps.push('brokenAxis');
                    addEvent(AxisClass, 'init', onAxisInit);
                    addEvent(AxisClass, 'afterInit', onAxisAfterInit);
                    addEvent(AxisClass, 'afterSetTickPositions', onAxisAfterSetTickPositions);
                    addEvent(AxisClass, 'afterSetOptions', onAxisAfterSetOptions);
                }
                if (composedClasses.indexOf(SeriesClass) === -1) {
                    composedClasses.push(SeriesClass);
                    var seriesProto = SeriesClass.prototype;
                    seriesProto.drawBreaks = seriesDrawBreaks;
                    seriesProto.gappedPath = seriesGappedPath;
                    addEvent(SeriesClass, 'afterGeneratePoints', onSeriesAfterGeneratePoints);
                    addEvent(SeriesClass, 'afterRender', onSeriesAfterRender);
                }
                return AxisClass;
            }
            BrokenAxis.compose = compose;
            /**
             * @private
             */
            function onAxisAfterInit() {
                if (typeof this.brokenAxis !== 'undefined') {
                    this.brokenAxis.setBreaks(this.options.breaks, false);
                }
            }
            /**
             * Force Axis to be not-ordinal when breaks are defined.
             * @private
             */
            function onAxisAfterSetOptions() {
                var axis = this;
                if (axis.brokenAxis && axis.brokenAxis.hasBreaks) {
                    axis.options.ordinal = false;
                }
            }
            /**
             * @private
             */
            function onAxisAfterSetTickPositions() {
                var axis = this,
                    brokenAxis = axis.brokenAxis;
                if (brokenAxis &&
                    brokenAxis.hasBreaks) {
                    var tickPositions = axis.tickPositions,
                        info = axis.tickPositions.info,
                        newPositions = [];
                    for (var i = 0; i < tickPositions.length; i++) {
                        if (!brokenAxis.isInAnyBreak(tickPositions[i])) {
                            newPositions.push(tickPositions[i]);
                        }
                    }
                    axis.tickPositions = newPositions;
                    axis.tickPositions.info = info;
                }
            }
            /**
             * @private
             */
            function onAxisInit() {
                var axis = this;
                if (!axis.brokenAxis) {
                    axis.brokenAxis = new Additions(axis);
                }
            }
            /**
             * @private
             */
            function onSeriesAfterGeneratePoints() {
                var _a = this,
                    isDirty = _a.isDirty,
                    connectNulls = _a.options.connectNulls,
                    points = _a.points,
                    xAxis = _a.xAxis,
                    yAxis = _a.yAxis;
                // Set, or reset visibility of the points. Axis.setBreaks marks
                // the series as isDirty
                if (isDirty) {
                    var i = points.length;
                    while (i--) {
                        var point = points[i];
                        // Respect nulls inside the break (#4275)
                        var nullGap = point.y === null && connectNulls === false;
                        var isPointInBreak = (!nullGap && ((xAxis &&
                                xAxis.brokenAxis &&
                                xAxis.brokenAxis.isInAnyBreak(point.x,
                            true)) || (yAxis &&
                                yAxis.brokenAxis &&
                                yAxis.brokenAxis.isInAnyBreak(point.y,
                            true))));
                        // Set point.visible if in any break.
                        // If not in break, reset visible to original value.
                        point.visible = isPointInBreak ?
                            false :
                            point.options.visible !== false;
                    }
                }
            }
            /**
             * @private
             */
            function onSeriesAfterRender() {
                this.drawBreaks(this.xAxis, ['x']);
                this.drawBreaks(this.yAxis, pick(this.pointArrayMap, ['y']));
            }
            /**
             * @private
             */
            function seriesDrawBreaks(axis, keys) {
                var series = this,
                    points = series.points;
                var breaks,
                    threshold,
                    eventName,
                    y;
                if (axis && // #5950
                    axis.brokenAxis &&
                    axis.brokenAxis.hasBreaks) {
                    var brokenAxis_1 = axis.brokenAxis;
                    keys.forEach(function (key) {
                        breaks = brokenAxis_1 && brokenAxis_1.breakArray || [];
                        threshold = axis.isXAxis ?
                            axis.min :
                            pick(series.options.threshold, axis.min);
                        points.forEach(function (point) {
                            y = pick(point['stack' + key.toUpperCase()], point[key]);
                            breaks.forEach(function (brk) {
                                if (isNumber(threshold) && isNumber(y)) {
                                    eventName = false;
                                    if ((threshold < brk.from && y > brk.to) ||
                                        (threshold > brk.from && y < brk.from)) {
                                        eventName = 'pointBreak';
                                    }
                                    else if ((threshold < brk.from &&
                                        y > brk.from &&
                                        y < brk.to) || (threshold > brk.from &&
                                        y > brk.to &&
                                        y < brk.from)) {
                                        eventName = 'pointInBreak';
                                    }
                                    if (eventName) {
                                        fireEvent(axis, eventName, { point: point, brk: brk });
                                    }
                                }
                            });
                        });
                    });
                }
            }
            /**
             * Extend getGraphPath by identifying gaps in the data so that we
             * can draw a gap in the line or area. This was moved from ordinal
             * axis module to broken axis module as of #5045.
             *
             * @private
             * @function Highcharts.Series#gappedPath
             *
             * @return {Highcharts.SVGPathArray}
             * Gapped path
             */
            function seriesGappedPath() {
                var currentDataGrouping = this.currentDataGrouping,
                    groupingSize = currentDataGrouping && currentDataGrouping.gapSize,
                    points = this.points.slice(),
                    yAxis = this.yAxis;
                var gapSize = this.options.gapSize,
                    i = points.length - 1,
                    stack;
                /**
                 * Defines when to display a gap in the graph, together with the
                 * [gapUnit](plotOptions.series.gapUnit) option.
                 *
                 * In case when `dataGrouping` is enabled, points can be grouped
                 * into a larger time span. This can make the grouped points to
                 * have a greater distance than the absolute value of `gapSize`
                 * property, which will result in disappearing graph completely.
                 * To prevent this situation the mentioned distance between
                 * grouped points is used instead of previously defined
                 * `gapSize`.
                 *
                 * In practice, this option is most often used to visualize gaps
                 * in time series. In a stock chart, intraday data is available
                 * for daytime hours, while gaps will appear in nights and
                 * weekends.
                 *
                 * @see [gapUnit](plotOptions.series.gapUnit)
                 * @see [xAxis.breaks](#xAxis.breaks)
                 *
                 * @sample {highstock} stock/plotoptions/series-gapsize/
                 * Setting the gap size to 2 introduces gaps for weekends in
                 * daily datasets.
                 *
                 * @type      {number}
                 * @default   0
                 * @product   highstock
                 * @requires  modules/broken-axis
                 * @apioption plotOptions.series.gapSize
                 */
                /**
                 * Together with [gapSize](plotOptions.series.gapSize), this
                 * option defines where to draw gaps in the graph.
                 *
                 * When the `gapUnit` is `"relative"` (default), a gap size of 5
                 * means that if the distance between two points is greater than
                 * 5 times that of the two closest points, the graph will be
                 * broken.
                 *
                 * When the `gapUnit` is `"value"`, the gap is based on absolute
                 * axis values, which on a datetime axis is milliseconds. This
                 * also applies to the navigator series that inherits gap
                 * options from the base series.
                 *
                 * @see [gapSize](plotOptions.series.gapSize)
                 *
                 * @type       {string}
                 * @default    relative
                 * @since      5.0.13
                 * @product    highstock
                 * @validvalue ["relative", "value"]
                 * @requires   modules/broken-axis
                 * @apioption  plotOptions.series.gapUnit
                 */
                if (gapSize && i > 0) { // #5008
                    // Gap unit is relative
                    if (this.options.gapUnit !== 'value') {
                        gapSize *= this.basePointRange;
                    }
                    // Setting a new gapSize in case dataGrouping is enabled
                    // (#7686)
                    if (groupingSize &&
                        groupingSize > gapSize &&
                        // Except when DG is forced (e.g. from other series)
                        // and has lower granularity than actual points (#11351)
                        groupingSize >= this.basePointRange) {
                        gapSize = groupingSize;
                    }
                    // extension for ordinal breaks
                    var current = void 0,
                        next = void 0;
                    while (i--) {
                        // Reassign next if it is not visible
                        if (!(next && next.visible !== false)) {
                            next = points[i + 1];
                        }
                        current = points[i];
                        // Skip iteration if one of the points is not visible
                        if (next.visible === false || current.visible === false) {
                            continue;
                        }
                        if (next.x - current.x > gapSize) {
                            var xRange = (current.x + next.x) / 2;
                            points.splice(// insert after this one
                            i + 1, 0, {
                                isNull: true,
                                x: xRange
                            });
                            // For stacked chart generate empty stack items, #6546
                            if (yAxis.stacking && this.options.stacking) {
                                stack = yAxis.stacking.stacks[this.stackKey][xRange] = new StackItem(yAxis, yAxis.options.stackLabels, false, xRange, this.stack);
                                stack.total = 0;
                            }
                        }
                        // Assign current to next for the upcoming iteration
                        next = current;
                    }
                }
                // Call base method
                return this.getGraphPath(points);
            }
            /* *
             *
             *  Class
             *
             * */
            /**
             * Provides support for broken axes.
             * @private
             * @class
             */
            var Additions = /** @class */ (function () {
                    /* *
                     *
                     *  Constructors
                     *
                     * */
                    function Additions(axis) {
                        this.hasBreaks = false;
                    this.axis = axis;
                }
                /* *
                 *
                 *  Static Functions
                 *
                 * */
                /**
                 * @private
                 */
                Additions.isInBreak = function (brk, val) {
                    var repeat = brk.repeat || Infinity,
                        from = brk.from,
                        length = brk.to - brk.from,
                        test = (val >= from ?
                            (val - from) % repeat :
                            repeat - ((from - val) % repeat));
                    var ret;
                    if (!brk.inclusive) {
                        ret = test < length && test !== 0;
                    }
                    else {
                        ret = test <= length;
                    }
                    return ret;
                };
                /**
                 * @private
                 */
                Additions.lin2Val = function (val) {
                    var axis = this;
                    var brokenAxis = axis.brokenAxis;
                    var breakArray = brokenAxis && brokenAxis.breakArray;
                    if (!breakArray || !isNumber(val)) {
                        return val;
                    }
                    var nval = val,
                        brk,
                        i;
                    for (i = 0; i < breakArray.length; i++) {
                        brk = breakArray[i];
                        if (brk.from >= nval) {
                            break;
                        }
                        else if (brk.to < nval) {
                            nval += brk.len;
                        }
                        else if (Additions.isInBreak(brk, nval)) {
                            nval += brk.len;
                        }
                    }
                    return nval;
                };
                /**
                 * @private
                 */
                Additions.val2Lin = function (val) {
                    var axis = this;
                    var brokenAxis = axis.brokenAxis;
                    var breakArray = brokenAxis && brokenAxis.breakArray;
                    if (!breakArray || !isNumber(val)) {
                        return val;
                    }
                    var nval = val,
                        brk,
                        i;
                    for (i = 0; i < breakArray.length; i++) {
                        brk = breakArray[i];
                        if (brk.to <= val) {
                            nval -= brk.len;
                        }
                        else if (brk.from >= val) {
                            break;
                        }
                        else if (Additions.isInBreak(brk, val)) {
                            nval -= (val - brk.from);
                            break;
                        }
                    }
                    return nval;
                };
                /* *
                 *
                 *  Functions
                 *
                 * */
                /**
                 * Returns the first break found where the x is larger then break.from
                 * and smaller then break.to.
                 *
                 * @param {number} x
                 * The number which should be within a break.
                 *
                 * @param {Array<Highcharts.XAxisBreaksOptions>} breaks
                 * The array of breaks to search within.
                 *
                 * @return {Highcharts.XAxisBreaksOptions|undefined}
                 * Returns the first break found that matches, returns false if no break
                 * is found.
                 */
                Additions.prototype.findBreakAt = function (x, breaks) {
                    return find(breaks, function (b) {
                        return b.from < x && x < b.to;
                    });
                };
                /**
                 * @private
                 */
                Additions.prototype.isInAnyBreak = function (val, testKeep) {
                    var brokenAxis = this,
                        axis = brokenAxis.axis,
                        breaks = axis.options.breaks || [];
                    var i = breaks.length,
                        inbrk,
                        keep,
                        ret;
                    if (i && isNumber(val)) {
                        while (i--) {
                            if (Additions.isInBreak(breaks[i], val)) {
                                inbrk = true;
                                if (!keep) {
                                    keep = pick(breaks[i].showPoints, !axis.isXAxis);
                                }
                            }
                        }
                        if (inbrk && testKeep) {
                            ret = inbrk && !keep;
                        }
                        else {
                            ret = inbrk;
                        }
                    }
                    return ret;
                };
                /**
                 * Dynamically set or unset breaks in an axis. This function in lighter
                 * than usin Axis.update, and it also preserves animation.
                 *
                 * @private
                 * @function Highcharts.Axis#setBreaks
                 *
                 * @param {Array<Highcharts.XAxisBreaksOptions>} [breaks]
                 * The breaks to add. When `undefined` it removes existing breaks.
                 *
                 * @param {boolean} [redraw=true]
                 * Whether to redraw the chart immediately.
                 */
                Additions.prototype.setBreaks = function (breaks, redraw) {
                    var brokenAxis = this;
                    var axis = brokenAxis.axis;
                    var hasBreaks = (isArray(breaks) && !!breaks.length);
                    axis.isDirty = brokenAxis.hasBreaks !== hasBreaks;
                    brokenAxis.hasBreaks = hasBreaks;
                    axis.options.breaks = axis.userOptions.breaks = breaks;
                    axis.forceRedraw = true; // Force recalculation in setScale
                    // Recalculate series related to the axis.
                    axis.series.forEach(function (series) {
                        series.isDirty = true;
                    });
                    if (!hasBreaks && axis.val2lin === Additions.val2Lin) {
                        // Revert to prototype functions
                        delete axis.val2lin;
                        delete axis.lin2val;
                    }
                    if (hasBreaks) {
                        axis.userOptions.ordinal = false;
                        axis.lin2val = Additions.lin2Val;
                        axis.val2lin = Additions.val2Lin;
                        axis.setExtremes = function (newMin, newMax, redraw, animation, eventArguments) {
                            // If trying to set extremes inside a break, extend min to
                            // after, and max to before the break ( #3857 )
                            if (brokenAxis.hasBreaks) {
                                var breaks_1 = (this.options.breaks || []);
                                var axisBreak = void 0;
                                while ((axisBreak = brokenAxis.findBreakAt(newMin, breaks_1))) {
                                    newMin = axisBreak.to;
                                }
                                while ((axisBreak = brokenAxis.findBreakAt(newMax, breaks_1))) {
                                    newMax = axisBreak.from;
                                }
                                // If both min and max is within the same break.
                                if (newMax < newMin) {
                                    newMax = newMin;
                                }
                            }
                            axis.constructor.prototype.setExtremes.call(this, newMin, newMax, redraw, animation, eventArguments);
                        };
                        axis.setAxisTranslation = function () {
                            axis.constructor.prototype.setAxisTranslation.call(this);
                            brokenAxis.unitLength = void 0;
                            if (brokenAxis.hasBreaks) {
                                var breaks_2 = axis.options.breaks || [], 
                                    // Temporary one:
                                    breakArrayT_1 = [],
                                    breakArray_1 = [],
                                    pointRangePadding = pick(axis.pointRangePadding, 0);
                                var length_1 = 0,
                                    inBrk_1,
                                    repeat_1,
                                    min_1 = axis.userMin || axis.min,
                                    max_1 = axis.userMax || axis.max,
                                    start_1,
                                    i_1;
                                // Min & max check (#4247)
                                breaks_2.forEach(function (brk) {
                                    repeat_1 = brk.repeat || Infinity;
                                    if (isNumber(min_1) && isNumber(max_1)) {
                                        if (Additions.isInBreak(brk, min_1)) {
                                            min_1 += ((brk.to % repeat_1) -
                                                (min_1 % repeat_1));
                                        }
                                        if (Additions.isInBreak(brk, max_1)) {
                                            max_1 -= ((max_1 % repeat_1) -
                                                (brk.from % repeat_1));
                                        }
                                    }
                                });
                                // Construct an array holding all breaks in the axis
                                breaks_2.forEach(function (brk) {
                                    start_1 = brk.from;
                                    repeat_1 = brk.repeat || Infinity;
                                    if (isNumber(min_1) && isNumber(max_1)) {
                                        while (start_1 - repeat_1 > min_1) {
                                            start_1 -= repeat_1;
                                        }
                                        while (start_1 < min_1) {
                                            start_1 += repeat_1;
                                        }
                                        for (i_1 = start_1; i_1 < max_1; i_1 += repeat_1) {
                                            breakArrayT_1.push({
                                                value: i_1,
                                                move: 'in'
                                            });
                                            breakArrayT_1.push({
                                                value: i_1 + brk.to - brk.from,
                                                move: 'out',
                                                size: brk.breakSize
                                            });
                                        }
                                    }
                                });
                                breakArrayT_1.sort(function (a, b) {
                                    return ((a.value === b.value) ?
                                        ((a.move === 'in' ? 0 : 1) -
                                            (b.move === 'in' ? 0 : 1)) :
                                        a.value - b.value);
                                });
                                // Simplify the breaks
                                inBrk_1 = 0;
                                start_1 = min_1;
                                breakArrayT_1.forEach(function (brk) {
                                    inBrk_1 += (brk.move === 'in' ? 1 : -1);
                                    if (inBrk_1 === 1 && brk.move === 'in') {
                                        start_1 = brk.value;
                                    }
                                    if (inBrk_1 === 0 && isNumber(start_1)) {
                                        breakArray_1.push({
                                            from: start_1,
                                            to: brk.value,
                                            len: brk.value - start_1 - (brk.size || 0)
                                        });
                                        length_1 += (brk.value -
                                            start_1 -
                                            (brk.size || 0));
                                    }
                                });
                                brokenAxis.breakArray = breakArray_1;
                                // Used with staticScale, and below the actual axis
                                // length, when breaks are substracted.
                                if (isNumber(min_1) &&
                                    isNumber(max_1) &&
                                    isNumber(axis.min)) {
                                    brokenAxis.unitLength = max_1 - min_1 - length_1 +
                                        pointRangePadding;
                                    fireEvent(axis, 'afterBreaks');
                                    if (axis.staticScale) {
                                        axis.transA = axis.staticScale;
                                    }
                                    else if (brokenAxis.unitLength) {
                                        axis.transA *=
                                            (max_1 - axis.min + pointRangePadding) /
                                                brokenAxis.unitLength;
                                    }
                                    if (pointRangePadding) {
                                        axis.minPixelPadding =
                                            axis.transA * (axis.minPointOffset || 0);
                                    }
                                    axis.min = min_1;
                                    axis.max = max_1;
                                }
                            }
                        };
                    }
                    if (pick(redraw, true)) {
                        axis.chart.redraw();
                    }
                };
                return Additions;
            }());
            BrokenAxis.Additions = Additions;
        })(BrokenAxis || (BrokenAxis = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return BrokenAxis;
    });
    _registerModule(_modules, 'masters/modules/broken-axis.src.js', [_modules['Core/Globals.js'], _modules['Core/Axis/BrokenAxis.js']], function (Highcharts, BrokenAxis) {

        var G = Highcharts;
        // Compositions
        BrokenAxis.compose(G.Axis, G.Series);

    });
    _registerModule(_modules, 'Extensions/DataGrouping/ApproximationRegistry.js', [], function () {
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
         *  Constants
         *
         * */
        /**
         * Define the available approximation types. The data grouping
         * approximations takes an array or numbers as the first parameter. In case
         * of ohlc, four arrays are sent in as four parameters. Each array consists
         * only of numbers. In case null values belong to the group, the property
         * .hasNulls will be set to true on the array.
         *
         * @product highstock
         *
         * @private
         */
        var ApproximationRegistry = {
            // approximations added programmatically
            };
        /* *
         *
         *  Default Export
         *
         * */

        return ApproximationRegistry;
    });
    _registerModule(_modules, 'Extensions/DataGrouping/ApproximationDefaults.js', [_modules['Extensions/DataGrouping/ApproximationRegistry.js'], _modules['Core/Utilities.js']], function (ApproximationRegistry, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var arrayMax = U.arrayMax,
            arrayMin = U.arrayMin,
            correctFloat = U.correctFloat,
            extend = U.extend,
            isNumber = U.isNumber;
        /* *
         *
         *  Functions
         *
         * */
        /**
         * @private
         */
        function average(arr) {
            var len = arr.length;
            var ret = sum(arr);
            // If we have a number, return it divided by the length. If not,
            // return null or undefined based on what the sum method finds.
            if (isNumber(ret) && len) {
                ret = correctFloat(ret / len);
            }
            return ret;
        }
        /**
         * The same as average, but for series with multiple values, like area ranges.
         * @private
         */
        function averages() {
            var ret = [];
            [].forEach.call(arguments, function (arr) {
                ret.push(average(arr));
            });
            // Return undefined when first elem. is undefined and let
            // sum method handle null (#7377)
            return typeof ret[0] === 'undefined' ? void 0 : ret;
        }
        /**
         * @private
         */
        function close(arr) {
            return arr.length ?
                arr[arr.length - 1] :
                (arr.hasNulls ? null : void 0);
        }
        /**
         * @private
         */
        function high(arr) {
            return arr.length ?
                arrayMax(arr) :
                (arr.hasNulls ? null : void 0);
        }
        /**
         * HLC, OHLC and range are special cases where a multidimensional array is input
         * and an array is output.
         * @private
         */
        function hlc(high, low, close) {
            high = ApproximationRegistry.high(high);
            low = ApproximationRegistry.low(low);
            close = ApproximationRegistry.close(close);
            if (isNumber(high) ||
                isNumber(low) ||
                isNumber(close)) {
                return [high, low, close];
            }
        }
        /**
         * @private
         */
        function low(arr) {
            return arr.length ?
                arrayMin(arr) :
                (arr.hasNulls ? null : void 0);
        }
        /**
         * @private
         */
        function ohlc(open, high, low, close) {
            open = ApproximationRegistry.open(open);
            high = ApproximationRegistry.high(high);
            low = ApproximationRegistry.low(low);
            close = ApproximationRegistry.close(close);
            if (isNumber(open) ||
                isNumber(high) ||
                isNumber(low) ||
                isNumber(close)) {
                return [open, high, low, close];
            }
        }
        /**
         * @private
         */
        function open(arr) {
            return arr.length ? arr[0] : (arr.hasNulls ? null : void 0);
        }
        /**
         * @private
         */
        function range(low, high) {
            low = ApproximationRegistry.low(low);
            high = ApproximationRegistry.high(high);
            if (isNumber(low) || isNumber(high)) {
                return [low, high];
            }
            if (low === null && high === null) {
                return null;
            }
            // else, return is undefined
        }
        /**
         * @private
         */
        function sum(arr) {
            var len = arr.length,
                ret;
            // 1. it consists of nulls exclusive
            if (!len && arr.hasNulls) {
                ret = null;
                // 2. it has a length and real values
            }
            else if (len) {
                ret = 0;
                while (len--) {
                    ret += arr[len];
                }
            }
            // 3. it has zero length, so just return undefined
            // => doNothing()
            return ret;
        }
        /* *
         *
         *  Default Export
         *
         * */
        var ApproximationDefaults = {
                average: average,
                averages: averages,
                close: close,
                high: high,
                hlc: hlc,
                low: low,
                ohlc: ohlc,
                open: open,
                range: range,
                sum: sum
            };
        extend(ApproximationRegistry, ApproximationDefaults);

        return ApproximationDefaults;
    });
    _registerModule(_modules, 'Extensions/DataGrouping/DataGroupingDefaults.js', [], function () {
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
         *  Constants
         *
         * */
        /**
         * Common options
         * @private
         */
        var common = {
                // enabled: null, // (true for stock charts, false for basic),
                // forced: undefined,
                groupPixelWidth: 2,
                // the first one is the point or start value, the second is the start
                // value if we're dealing with range, the third one is the end value if
                // dealing with a range
                dateTimeLabelFormats: {
                    millisecond: [
                        '%A, %b %e, %H:%M:%S.%L',
                        '%A, %b %e, %H:%M:%S.%L',
                        '-%H:%M:%S.%L'
                    ],
                    second: [
                        '%A, %b %e, %H:%M:%S',
                        '%A, %b %e, %H:%M:%S',
                        '-%H:%M:%S'
                    ],
                    minute: [
                        '%A, %b %e, %H:%M',
                        '%A, %b %e, %H:%M',
                        '-%H:%M'
                    ],
                    hour: [
                        '%A, %b %e, %H:%M',
                        '%A, %b %e, %H:%M',
                        '-%H:%M'
                    ],
                    day: [
                        '%A, %b %e, %Y',
                        '%A, %b %e',
                        '-%A, %b %e, %Y'
                    ],
                    week: [
                        'Week from %A, %b %e, %Y',
                        '%A, %b %e',
                        '-%A, %b %e, %Y'
                    ],
                    month: [
                        '%B %Y',
                        '%B',
                        '-%B %Y'
                    ],
                    year: [
                        '%Y',
                        '%Y',
                        '-%Y'
                    ]
                }
                // smoothed = false, // enable this for navigator series only
            };
        /**
         * Extends common options
         * @private
         */
        var seriesSpecific = {
                line: {},
                spline: {},
                area: {},
                areaspline: {},
                arearange: {},
                column: {
                    groupPixelWidth: 10
                },
                columnrange: {
                    groupPixelWidth: 10
                },
                candlestick: {
                    groupPixelWidth: 10
                },
                ohlc: {
                    groupPixelWidth: 5
                },
                hlc: {
                    groupPixelWidth: 5
                    // Move to HeikinAshiSeries.ts aftre refactoring data grouping.
                },
                heikinashi: {
                    groupPixelWidth: 10
                }
            };
        /**
         * Units are defined in a separate array to allow complete overriding in
         * case of a user option.
         * @private
         */
        var units = [
                [
                    'millisecond',
                    [1, 2, 5, 10, 20, 25, 50, 100, 200, 500] // allowed multiples
                ],
            [
                    'second',
                    [1, 2, 5, 10, 15, 30]
                ],
            [
                    'minute',
                    [1, 2, 5, 10, 15, 30]
                ],
            [
                    'hour',
                    [1, 2, 3, 4, 6, 8, 12]
                ],
            [
                    'day',
                    [1]
                ],
            [
                    'week',
                    [1]
                ],
            [
                    'month',
                    [1, 3, 6]
                ],
            [
                    'year',
                    null
                ]
            ];
        /* *
         *
         *  Default Export
         *
         * */
        var DataGroupingDefaults = {
                common: common,
                seriesSpecific: seriesSpecific,
                units: units
            };

        return DataGroupingDefaults;
    });
    _registerModule(_modules, 'Extensions/DataGrouping/DataGroupingAxisComposition.js', [_modules['Extensions/DataGrouping/DataGroupingDefaults.js'], _modules['Core/Utilities.js']], function (DataGroupingDefaults, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var addEvent = U.addEvent,
            extend = U.extend,
            merge = U.merge,
            pick = U.pick;
        /* *
         *
         *  Constants
         *
         * */
        var composedMembers = [];
        /* *
         *
         *  Variables
         *
         * */
        var AxisConstructor;
        /* *
         *
         *  Functions
         *
         * */
        /**
         * Check the groupPixelWidth and apply the grouping if needed.
         * Fired only after processing the data.
         *
         * @product highstock
         *
         * @function Highcharts.Axis#applyGrouping
         */
        function applyGrouping(e) {
            var axis = this,
                series = axis.series;
            // Reset the groupPixelWidth for all series, #17141.
            series.forEach(function (series) {
                series.groupPixelWidth = void 0; // #2110
            });
            series.forEach(function (series) {
                series.groupPixelWidth = (axis.getGroupPixelWidth &&
                    axis.getGroupPixelWidth());
                if (series.groupPixelWidth) {
                    series.hasProcessed = true; // #2692
                }
                // Fire independing on series.groupPixelWidth to always set a proper
                // dataGrouping state, (#16238)
                series.applyGrouping(!!e.hasExtremesChanged);
            });
        }
        /**
         * @private
         */
        function compose(AxisClass) {
            AxisConstructor = AxisClass;
            if (composedMembers.indexOf(AxisClass) === -1) {
                composedMembers.push(AxisClass);
                addEvent(AxisClass, 'afterSetScale', onAfterSetScale);
                // When all series are processed, calculate the group pixel width and
                // then if this value is different than zero apply groupings.
                addEvent(AxisClass, 'postProcessData', applyGrouping);
                extend(AxisClass.prototype, {
                    applyGrouping: applyGrouping,
                    getGroupPixelWidth: getGroupPixelWidth,
                    setDataGrouping: setDataGrouping
                });
            }
        }
        /**
         * Get the data grouping pixel width based on the greatest defined individual
         * width of the axis' series, and if whether one of the axes need grouping.
         * @private
         */
        function getGroupPixelWidth() {
            var series = this.series;
            var i = series.length,
                groupPixelWidth = 0,
                doGrouping = false,
                dataLength,
                dgOptions;
            // If one of the series needs grouping, apply it to all (#1634)
            while (i--) {
                dgOptions = series[i].options.dataGrouping;
                if (dgOptions) { // #2692
                    // If multiple series are compared on the same x axis, give them the
                    // same group pixel width (#334)
                    groupPixelWidth = Math.max(groupPixelWidth, 
                    // Fallback to commonOptions (#9693)
                    pick(dgOptions.groupPixelWidth, DataGroupingDefaults.common.groupPixelWidth));
                    dataLength = (series[i].processedXData || series[i].data).length;
                    // Execute grouping if the amount of points is greater than the
                    // limit defined in groupPixelWidth
                    if (series[i].groupPixelWidth ||
                        (dataLength >
                            (this.chart.plotSizeX / groupPixelWidth)) ||
                        (dataLength && dgOptions.forced)) {
                        doGrouping = true;
                    }
                }
            }
            return doGrouping ? groupPixelWidth : 0;
        }
        /**
         * When resetting the scale reset the hasProccessed flag to avoid taking
         * previous data grouping of neighbour series into accound when determining
         * group pixel width (#2692).
         * @private
         */
        function onAfterSetScale() {
            this.series.forEach(function (series) {
                series.hasProcessed = false;
            });
        }
        /**
         * Highcharts Stock only. Force data grouping on all the axis' series.
         *
         * @product highstock
         *
         * @function Highcharts.Axis#setDataGrouping
         *
         * @param {boolean|Highcharts.DataGroupingOptionsObject} [dataGrouping]
         *        A `dataGrouping` configuration. Use `false` to disable data grouping
         *        dynamically.
         *
         * @param {boolean} [redraw=true]
         *        Whether to redraw the chart or wait for a later call to
         *        {@link Chart#redraw}.
         */
        function setDataGrouping(dataGrouping, redraw) {
            var axis = this;
            var i;
            redraw = pick(redraw, true);
            if (!dataGrouping) {
                dataGrouping = {
                    forced: false,
                    units: null
                };
            }
            // Axis is instantiated, update all series
            if (this instanceof AxisConstructor) {
                i = this.series.length;
                while (i--) {
                    this.series[i].update({
                        dataGrouping: dataGrouping
                    }, false);
                }
                // Axis not yet instanciated, alter series options
            }
            else {
                this.chart.options.series.forEach(function (seriesOptions) {
                    // Merging dataGrouping options with already defined options #16759
                    seriesOptions.dataGrouping = typeof dataGrouping === 'boolean' ?
                        dataGrouping :
                        merge(dataGrouping, seriesOptions.dataGrouping);
                });
            }
            // Clear ordinal slope, so we won't accidentaly use the old one (#7827)
            if (axis.ordinal) {
                axis.ordinal.slope = void 0;
            }
            if (redraw) {
                this.chart.redraw();
            }
        }
        /* *
         *
         *  Default Export
         *
         * */
        var DataGroupingAxisComposition = {
                compose: compose
            };

        return DataGroupingAxisComposition;
    });
    _registerModule(_modules, 'Extensions/DataGrouping/DataGroupingSeriesComposition.js', [_modules['Extensions/DataGrouping/ApproximationRegistry.js'], _modules['Extensions/DataGrouping/DataGroupingDefaults.js'], _modules['Core/Axis/DateTimeAxis.js'], _modules['Core/Defaults.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (ApproximationRegistry, DataGroupingDefaults, DateTimeAxis, D, SeriesRegistry, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var seriesProto = SeriesRegistry.series.prototype;
        var addEvent = U.addEvent,
            defined = U.defined,
            error = U.error,
            extend = U.extend,
            isNumber = U.isNumber,
            merge = U.merge,
            pick = U.pick;
        /* *
         *
         *  Constants
         *
         * */
        var baseGeneratePoints = seriesProto.generatePoints;
        var composedMembers = [];
        /* *
         *
         *  Functions
         *
         * */
        /**
         * @private
         */
        function adjustExtremes(xAxis, groupedXData) {
            // Make sure the X axis extends to show the first group (#2533)
            // But only for visible series (#5493, #6393)
            if (defined(groupedXData[0]) &&
                isNumber(xAxis.min) &&
                isNumber(xAxis.dataMin) &&
                groupedXData[0] < xAxis.min) {
                if ((!defined(xAxis.options.min) &&
                    xAxis.min <= xAxis.dataMin) ||
                    xAxis.min === xAxis.dataMin) {
                    xAxis.min = Math.min(groupedXData[0], xAxis.min);
                }
                xAxis.dataMin = Math.min(groupedXData[0], xAxis.dataMin);
            }
            // When the last anchor set, change the extremes that
            // the last point is visible (#12455).
            if (defined(groupedXData[groupedXData.length - 1]) &&
                isNumber(xAxis.max) &&
                isNumber(xAxis.dataMax) &&
                groupedXData[groupedXData.length - 1] > xAxis.max) {
                if ((!defined(xAxis.options.max) &&
                    isNumber(xAxis.dataMax) &&
                    xAxis.max >= xAxis.dataMax) || xAxis.max === xAxis.dataMax) {
                    xAxis.max = Math.max(groupedXData[groupedXData.length - 1], xAxis.max);
                }
                xAxis.dataMax = Math.max(groupedXData[groupedXData.length - 1], xAxis.dataMax);
            }
        }
        /**
         * @private
         */
        function anchorPoints(series, groupedXData, xMax) {
            var options = series.options,
                dataGroupingOptions = options.dataGrouping,
                totalRange = (series.currentDataGrouping && series.currentDataGrouping.gapSize);
            var i;
            // DataGrouping x-coordinates.
            if (dataGroupingOptions && series.xData && totalRange && series.groupMap) {
                var groupedDataLength = groupedXData.length - 1,
                    anchor = dataGroupingOptions.anchor,
                    firstAnchor = pick(dataGroupingOptions.firstAnchor,
                    anchor),
                    lastAnchor = pick(dataGroupingOptions.lastAnchor,
                    anchor);
                // Anchor points that are not extremes.
                if (anchor && anchor !== 'start') {
                    var shiftInterval = (totalRange *
                            { middle: 0.5,
                        end: 1 }[anchor]);
                    i = groupedXData.length - 1;
                    while (i-- && i > 0) {
                        groupedXData[i] += shiftInterval;
                    }
                }
                // Change the first point position, but only when it is
                // the first point in the data set not in the current zoom.
                if (firstAnchor &&
                    firstAnchor !== 'start' &&
                    series.xData[0] >= groupedXData[0]) {
                    var groupStart = series.groupMap[0].start,
                        groupLength = series.groupMap[0].length;
                    var firstGroupstEnd = void 0;
                    if (isNumber(groupStart) && isNumber(groupLength)) {
                        firstGroupstEnd = groupStart + (groupLength - 1);
                    }
                    groupedXData[0] = {
                        middle: groupedXData[0] + 0.5 * totalRange,
                        end: groupedXData[0] + totalRange,
                        firstPoint: series.xData[0],
                        lastPoint: firstGroupstEnd && series.xData[firstGroupstEnd]
                    }[firstAnchor];
                }
                // Change the last point position but only when it is
                // the last point in the data set not in the current zoom.
                if (lastAnchor &&
                    lastAnchor !== 'start' &&
                    totalRange &&
                    groupedXData[groupedDataLength] >= xMax - totalRange) {
                    var lastGroupStart = series.groupMap[series.groupMap.length - 1].start;
                    groupedXData[groupedDataLength] = {
                        middle: groupedXData[groupedDataLength] + 0.5 * totalRange,
                        end: groupedXData[groupedDataLength] + totalRange,
                        firstPoint: lastGroupStart && series.xData[lastGroupStart],
                        lastPoint: series.xData[series.xData.length - 1]
                    }[lastAnchor];
                }
            }
        }
        /**
         * For the processed data, calculate the grouped data if needed.
         *
         * @private
         * @function Highcharts.Series#applyGrouping
         */
        function applyGrouping(hasExtremesChanged) {
            var series = this,
                chart = series.chart,
                options = series.options,
                dataGroupingOptions = options.dataGrouping,
                groupingEnabled = series.allowDG !== false && dataGroupingOptions &&
                    pick(dataGroupingOptions.enabled,
                chart.options.isStock),
                visible = (series.visible || !chart.options.chart.ignoreHiddenSeries),
                lastDataGrouping = this.currentDataGrouping;
            var currentDataGrouping,
                croppedData,
                revertRequireSorting = false;
            // Data needs to be sorted for dataGrouping
            if (groupingEnabled && !series.requireSorting) {
                series.requireSorting = revertRequireSorting = true;
            }
            // Skip if skipDataGrouping method returns false or if grouping is disabled
            // (in that order).
            var skip = skipDataGrouping(series,
                hasExtremesChanged) === false || !groupingEnabled;
            // Revert original requireSorting value if changed
            if (revertRequireSorting) {
                series.requireSorting = false;
            }
            if (!skip) {
                series.destroyGroupedData();
                var processedXData = dataGroupingOptions.groupAll ?
                        series.xData :
                        series.processedXData,
                    processedYData = dataGroupingOptions.groupAll ?
                        series.yData :
                        series.processedYData,
                    plotSizeX = chart.plotSizeX,
                    xAxis = series.xAxis,
                    ordinal = xAxis.options.ordinal,
                    groupPixelWidth = series.groupPixelWidth;
                var i = void 0,
                    hasGroupedData = void 0;
                // Execute grouping if the amount of points is greater than the limit
                // defined in groupPixelWidth
                if (groupPixelWidth &&
                    processedXData &&
                    processedXData.length) {
                    hasGroupedData = true;
                    // Force recreation of point instances in series.translate, #5699
                    series.isDirty = true;
                    series.points = null; // #6709
                    var extremes = xAxis.getExtremes(),
                        xMin = extremes.min,
                        xMax = extremes.max,
                        groupIntervalFactor = (ordinal &&
                            xAxis.ordinal &&
                            xAxis.ordinal.getGroupIntervalFactor(xMin,
                        xMax,
                        series)) || 1,
                        interval = (groupPixelWidth * (xMax - xMin) / plotSizeX) *
                            groupIntervalFactor,
                        groupPositions = xAxis.getTimeTicks(DateTimeAxis.Additions.prototype.normalizeTimeTickInterval(interval,
                        dataGroupingOptions.units ||
                            DataGroupingDefaults.units), 
                        // Processed data may extend beyond axis (#4907)
                        Math.min(xMin,
                        processedXData[0]),
                        Math.max(xMax,
                        processedXData[processedXData.length - 1]),
                        xAxis.options.startOfWeek,
                        processedXData,
                        series.closestPointRange),
                        groupedData = seriesProto.groupData.apply(series,
                        [
                            processedXData,
                            processedYData,
                            groupPositions,
                            dataGroupingOptions.approximation
                        ]);
                    var groupedXData = groupedData.groupedXData,
                        groupedYData = groupedData.groupedYData,
                        gapSize = 0;
                    // The smoothed option is deprecated, instead, there is a fallback
                    // to the new anchoring mechanism. #12455.
                    if (dataGroupingOptions &&
                        dataGroupingOptions.smoothed &&
                        groupedXData.length) {
                        dataGroupingOptions.firstAnchor = 'firstPoint';
                        dataGroupingOptions.anchor = 'middle';
                        dataGroupingOptions.lastAnchor = 'lastPoint';
                        error(32, false, chart, {
                            'dataGrouping.smoothed': 'use dataGrouping.anchor'
                        });
                    }
                    anchorPoints(series, groupedXData, xMax);
                    // Record what data grouping values were used
                    for (i = 1; i < groupPositions.length; i++) {
                        // The grouped gapSize needs to be the largest distance between
                        // the group to capture varying group sizes like months or DST
                        // crossing (#10000). Also check that the gap is not at the
                        // start of a segment.
                        if (!groupPositions.info.segmentStarts ||
                            groupPositions.info.segmentStarts.indexOf(i) === -1) {
                            gapSize = Math.max(groupPositions[i] - groupPositions[i - 1], gapSize);
                        }
                    }
                    currentDataGrouping = groupPositions.info;
                    currentDataGrouping.gapSize = gapSize;
                    series.closestPointRange = groupPositions.info.totalRange;
                    series.groupMap = groupedData.groupMap;
                    if (visible) {
                        adjustExtremes(xAxis, groupedXData);
                    }
                    // We calculated all group positions but we should render
                    // only the ones within the visible range
                    if (dataGroupingOptions.groupAll) {
                        // Keep the reference to all grouped points
                        // for further calculation (eg. heikinashi).
                        series.allGroupedData = groupedYData;
                        croppedData = series.cropData(groupedXData, groupedYData, xAxis.min, xAxis.max, 1 // Ordinal xAxis will remove left-most points otherwise
                        );
                        groupedXData = croppedData.xData;
                        groupedYData = croppedData.yData;
                        series.cropStart = croppedData.start; // #15005
                    }
                    // Set series props
                    series.processedXData = groupedXData;
                    series.processedYData = groupedYData;
                }
                else {
                    series.groupMap = null;
                }
                series.hasGroupedData = hasGroupedData;
                series.currentDataGrouping = currentDataGrouping;
                series.preventGraphAnimation =
                    (lastDataGrouping && lastDataGrouping.totalRange) !==
                        (currentDataGrouping && currentDataGrouping.totalRange);
            }
        }
        /**
         * @private
         */
        function compose(SeriesClass) {
            var PointClass = SeriesClass.prototype.pointClass;
            if (composedMembers.indexOf(PointClass) === -1) {
                composedMembers.push(PointClass);
                // Override point prototype to throw a warning when trying to update
                // grouped points.
                addEvent(PointClass, 'update', function () {
                    if (this.dataGroup) {
                        error(24, false, this.series.chart);
                        return false;
                    }
                });
            }
            if (composedMembers.indexOf(SeriesClass) === -1) {
                composedMembers.push(SeriesClass);
                addEvent(SeriesClass, 'afterSetOptions', onAfterSetOptions);
                addEvent(SeriesClass, 'destroy', destroyGroupedData);
                extend(SeriesClass.prototype, {
                    applyGrouping: applyGrouping,
                    destroyGroupedData: destroyGroupedData,
                    generatePoints: generatePoints,
                    getDGApproximation: getDGApproximation,
                    groupData: groupData
                });
            }
        }
        /**
         * Destroy the grouped data points. #622, #740
         * @private
         */
        function destroyGroupedData() {
            // Clear previous groups
            if (this.groupedData) {
                this.groupedData.forEach(function (point, i) {
                    if (point) {
                        this.groupedData[i] = point.destroy ?
                            point.destroy() : null;
                    }
                }, this);
                // Clears all:
                // - `this.groupedData`
                // - `this.points`
                // - `preserve` object in series.update()
                this.groupedData.length = 0;
            }
        }
        /**
         * Override the generatePoints method by adding a reference to grouped data
         * @private
         */
        function generatePoints() {
            baseGeneratePoints.apply(this);
            // Record grouped data in order to let it be destroyed the next time
            // processData runs
            this.destroyGroupedData(); // #622
            this.groupedData = this.hasGroupedData ? this.points : null;
        }
        /**
         * Set default approximations to the prototypes if present. Properties are
         * inherited down. Can be overridden for individual series types.
         * @private
         */
        function getDGApproximation() {
            if (this.is('arearange')) {
                return 'range';
            }
            if (this.is('ohlc')) {
                return 'ohlc';
            }
            if (this.is('hlc')) {
                return 'hlc';
            }
            if (this.is('column')) {
                return 'sum';
            }
            return 'average';
        }
        /**
         * Highcharts Stock only. Takes parallel arrays of x and y data and groups the
         * data into intervals defined by groupPositions, a collection of starting x
         * values for each group.
         *
         * @product highstock
         *
         * @function Highcharts.Series#groupData
         * @param {Array<number>} xData
         *        Parallel array of x data.
         * @param {Array<(number|null|undefined)>|Array<Array<(number|null|undefined)>>} yData
         *        Parallel array of y data.
         * @param {Array<number>} groupPositions
         *        Group positions.
         * @param {string|Function} [approximation]
         *        Approximation to use.
         * @return {Highcharts.DataGroupingResultObject}
         *         Mapped groups.
         */
        function groupData(xData, yData, groupPositions, approximation) {
            var series = this,
                data = series.data,
                dataOptions = series.options && series.options.data,
                groupedXData = [],
                groupedYData = [],
                groupMap = [],
                dataLength = xData.length, 
                // when grouping the fake extended axis for panning,
                // we don't need to consider y
                handleYData = !!yData,
                values = [],
                pointArrayMap = series.pointArrayMap,
                pointArrayMapLength = pointArrayMap && pointArrayMap.length,
                extendedPointArrayMap = ['x'].concat(pointArrayMap || ['y']),
                groupAll = (this.options.dataGrouping &&
                    this.options.dataGrouping.groupAll);
            var pointX,
                pointY,
                groupedY,
                pos = 0,
                start = 0;
            var approximationFn = (typeof approximation === 'function' ?
                    approximation :
                    approximation && ApproximationRegistry[approximation] ?
                        ApproximationRegistry[approximation] :
                        ApproximationRegistry[(series.getDGApproximation && series.getDGApproximation() ||
                            'average')]);
            // Calculate values array size from pointArrayMap length
            if (pointArrayMapLength) {
                var len = pointArrayMap.length;
                while (len--) {
                    values.push([]);
                }
            }
            else {
                values.push([]);
            }
            var valuesLen = pointArrayMapLength || 1;
            for (var i = 0; i <= dataLength; i++) {
                // Start with the first point within the X axis range (#2696)
                if (xData[i] < groupPositions[0]) {
                    continue; // with next point
                }
                // when a new group is entered, summarize and initialize
                // the previous group
                while ((typeof groupPositions[pos + 1] !== 'undefined' &&
                    xData[i] >= groupPositions[pos + 1]) ||
                    i === dataLength) { // get the last group
                    // get group x and y
                    pointX = groupPositions[pos];
                    series.dataGroupInfo = {
                        start: groupAll ? start : (series.cropStart + start),
                        length: values[0].length
                    };
                    groupedY = approximationFn.apply(series, values);
                    // By default, let options of the first grouped point be passed over
                    // to the grouped point. This allows preserving properties like
                    // `name` and `color` or custom properties. Implementers can
                    // override this from the approximation function, where they can
                    // write custom options to `this.dataGroupInfo.options`.
                    if (series.pointClass && !defined(series.dataGroupInfo.options)) {
                        // Convert numbers and arrays into objects
                        series.dataGroupInfo.options = merge(series.pointClass.prototype
                            .optionsToObject.call({ series: series }, series.options.data[series.cropStart + start]));
                        // Make sure the raw data (x, y, open, high etc) is not copied
                        // over and overwriting approximated data.
                        extendedPointArrayMap.forEach(function (key) {
                            delete series.dataGroupInfo.options[key];
                        });
                    }
                    // push the grouped data
                    if (typeof groupedY !== 'undefined') {
                        groupedXData.push(pointX);
                        groupedYData.push(groupedY);
                        groupMap.push(series.dataGroupInfo);
                    }
                    // reset the aggregate arrays
                    start = i;
                    for (var j = 0; j < valuesLen; j++) {
                        values[j].length = 0; // faster than values[j] = []
                        values[j].hasNulls = false;
                    }
                    // Advance on the group positions
                    pos += 1;
                    // don't loop beyond the last group
                    if (i === dataLength) {
                        break;
                    }
                }
                // break out
                if (i === dataLength) {
                    break;
                }
                // for each raw data point, push it to an array that contains all values
                // for this specific group
                if (pointArrayMap) {
                    var index = (series.options.dataGrouping &&
                            series.options.dataGrouping.groupAll ?
                            i : series.cropStart + i),
                        point = (data && data[index]) ||
                            series.pointClass.prototype.applyOptions.apply({
                                series: series
                            },
                        [dataOptions[index]]);
                    var val = void 0;
                    for (var j = 0; j < pointArrayMapLength; j++) {
                        val = point[pointArrayMap[j]];
                        if (isNumber(val)) {
                            values[j].push(val);
                        }
                        else if (val === null) {
                            values[j].hasNulls = true;
                        }
                    }
                }
                else {
                    pointY = handleYData ? yData[i] : null;
                    if (isNumber(pointY)) {
                        values[0].push(pointY);
                    }
                    else if (pointY === null) {
                        values[0].hasNulls = true;
                    }
                }
            }
            return {
                groupedXData: groupedXData,
                groupedYData: groupedYData,
                groupMap: groupMap
            };
        }
        /**
         * Handle default options for data grouping. This must be set at runtime because
         * some series types are defined after this.
         * @private
         */
        function onAfterSetOptions(e) {
            var options = e.options,
                type = this.type,
                plotOptions = this.chart.options.plotOptions, 
                // External series, for example technical indicators should also inherit
                // commonOptions which are not available outside this module
                baseOptions = (this.useCommonDataGrouping &&
                    DataGroupingDefaults.common),
                seriesSpecific = DataGroupingDefaults.seriesSpecific;
            var defaultOptions = D.defaultOptions.plotOptions[type].dataGrouping;
            if (plotOptions && (seriesSpecific[type] || baseOptions)) { // #1284
                var rangeSelector = this.chart.rangeSelector;
                if (!defaultOptions) {
                    defaultOptions = merge(DataGroupingDefaults.common, seriesSpecific[type]);
                }
                options.dataGrouping = merge(baseOptions, defaultOptions, plotOptions.series && plotOptions.series.dataGrouping, // #1228
                // Set by the StockChart constructor:
                plotOptions[type].dataGrouping, this.userOptions.dataGrouping, !options.isInternal &&
                    rangeSelector &&
                    isNumber(rangeSelector.selected) &&
                    rangeSelector.buttonOptions[rangeSelector.selected].dataGrouping);
            }
        }
        /**
         * @private
         */
        function skipDataGrouping(series, force) {
            return !(series.isCartesian &&
                !series.isDirty &&
                !series.xAxis.isDirty &&
                !series.yAxis.isDirty &&
                !force);
        }
        /* *
         *
         *  Default Export
         *
         * */
        var DataGroupingSeriesComposition = {
                compose: compose,
                groupData: groupData
            };

        return DataGroupingSeriesComposition;
    });
    _registerModule(_modules, 'Extensions/DataGrouping/DataGrouping.js', [_modules['Extensions/DataGrouping/DataGroupingAxisComposition.js'], _modules['Extensions/DataGrouping/DataGroupingDefaults.js'], _modules['Extensions/DataGrouping/DataGroupingSeriesComposition.js'], _modules['Core/FormatUtilities.js'], _modules['Core/Utilities.js']], function (DataGroupingAxisComposition, DataGroupingDefaults, DataGroupingSeriesComposition, F, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var format = F.format;
        var addEvent = U.addEvent,
            extend = U.extend,
            isNumber = U.isNumber;
        /* *
         *
         *  Constants
         *
         * */
        var composedMembers = [];
        /* *
         *
         *  Functions
         *
         * */
        /**
         * @private
         */
        function compose(AxisClass, SeriesClass, TooltipClass) {
            DataGroupingAxisComposition.compose(AxisClass);
            DataGroupingSeriesComposition.compose(SeriesClass);
            if (composedMembers.indexOf(TooltipClass) === -1) {
                composedMembers.push(TooltipClass);
                addEvent(TooltipClass, 'headerFormatter', onTooltipHeaderFormatter);
            }
        }
        /**
         * Extend the original method, make the tooltip's header reflect the grouped
         * range.
         * @private
         */
        function onTooltipHeaderFormatter(e) {
            var chart = this.chart,
                time = chart.time,
                labelConfig = e.labelConfig,
                series = labelConfig.series,
                options = series.options,
                tooltipOptions = series.tooltipOptions,
                dataGroupingOptions = options.dataGrouping,
                xAxis = series.xAxis;
            var xDateFormat = tooltipOptions.xDateFormat,
                xDateFormatEnd,
                currentDataGrouping,
                dateTimeLabelFormats,
                labelFormats,
                formattedKey,
                formatString = tooltipOptions[e.isFooter ? 'footerFormat' : 'headerFormat'];
            // apply only to grouped series
            if (xAxis &&
                xAxis.options.type === 'datetime' &&
                dataGroupingOptions &&
                isNumber(labelConfig.key)) {
                // set variables
                currentDataGrouping = series.currentDataGrouping;
                dateTimeLabelFormats = dataGroupingOptions.dateTimeLabelFormats ||
                    // Fallback to commonOptions (#9693)
                    DataGroupingDefaults.common.dateTimeLabelFormats;
                // if we have grouped data, use the grouping information to get the
                // right format
                if (currentDataGrouping) {
                    labelFormats =
                        dateTimeLabelFormats[currentDataGrouping.unitName];
                    if (currentDataGrouping.count === 1) {
                        xDateFormat = labelFormats[0];
                    }
                    else {
                        xDateFormat = labelFormats[1];
                        xDateFormatEnd = labelFormats[2];
                    }
                    // if not grouped, and we don't have set the xDateFormat option, get the
                    // best fit, so if the least distance between points is one minute, show
                    // it, but if the least distance is one day, skip hours and minutes etc.
                }
                else if (!xDateFormat && dateTimeLabelFormats && xAxis.dateTime) {
                    xDateFormat = xAxis.dateTime.getXDateFormat(labelConfig.x, tooltipOptions.dateTimeLabelFormats);
                }
                // now format the key
                formattedKey = time.dateFormat(xDateFormat, labelConfig.key);
                if (xDateFormatEnd) {
                    formattedKey += time.dateFormat(xDateFormatEnd, labelConfig.key + currentDataGrouping.totalRange - 1);
                }
                // Replace default header style with class name
                if (series.chart.styledMode) {
                    formatString = this.styledModeFormat(formatString);
                }
                // return the replaced format
                e.text = format(formatString, {
                    point: extend(labelConfig.point, { key: formattedKey }),
                    series: series
                }, chart);
                e.preventDefault();
            }
        }
        /* *
         *
         *  Default Export
         *
         * */
        var DataGroupingComposition = {
                compose: compose,
                groupData: DataGroupingSeriesComposition.groupData
            };
        /* *
         *
         *  API Declarations
         *
         * */
        /**
         * @typedef {"average"|"averages"|"open"|"high"|"low"|"close"|"sum"} Highcharts.DataGroupingApproximationValue
         */
        /**
         * The position of the point inside the group.
         *
         * @typedef    {"start"|"middle"|"end"} Highcharts.DataGroupingAnchor
         */
        /**
         * The position of the first or last point in the series inside the group.
         *
         * @typedef    {"start"|"middle"|"end"|"firstPoint"|"lastPoint"} Highcharts.DataGroupingAnchorExtremes
         */
        /**
         * Highcharts Stock only.
         *
         * @product highstock
         * @interface Highcharts.DataGroupingInfoObject
         */ /**
        * @name Highcharts.DataGroupingInfoObject#length
        * @type {number}
        */ /**
        * @name Highcharts.DataGroupingInfoObject#options
        * @type {Highcharts.SeriesOptionsType|undefined}
        */ /**
        * @name Highcharts.DataGroupingInfoObject#start
        * @type {number}
        */
        /**
         * Highcharts Stock only.
         *
         * @product highstock
         * @interface Highcharts.DataGroupingResultObject
         */ /**
        * @name Highcharts.DataGroupingResultObject#groupedXData
        * @type {Array<number>}
        */ /**
        * @name Highcharts.DataGroupingResultObject#groupedYData
        * @type {Array<(number|null|undefined)>|Array<Array<(number|null|undefined)>>}
        */ /**
        * @name Highcharts.DataGroupingResultObject#groupMap
        * @type {Array<DataGroupingInfoObject>}
        */
        /**
         * Highcharts Stock only. If a point object is created by data
         * grouping, it doesn't reflect actual points in the raw
         * data. In this case, the `dataGroup` property holds
         * information that points back to the raw data.
         *
         * - `dataGroup.start` is the index of the first raw data
         *   point in the group.
         *
         * - `dataGroup.length` is the amount of points in the
         *   group.
         *
         * @sample stock/members/point-datagroup
         *         Click to inspect raw data points
         *
         * @product highstock
         *
         * @name Highcharts.Point#dataGroup
         * @type {Highcharts.DataGroupingInfoObject|undefined}
         */
        (''); // detach doclets above
        /* *
         *
         *  API Options
         *
         * */
        /**
         * Data grouping is the concept of sampling the data values into larger
         * blocks in order to ease readability and increase performance of the
         * JavaScript charts. Highcharts Stock by default applies data grouping when
         * the points become closer than a certain pixel value, determined by
         * the `groupPixelWidth` option.
         *
         * If data grouping is applied, the grouping information of grouped
         * points can be read from the [Point.dataGroup](
         * /class-reference/Highcharts.Point#dataGroup). If point options other than
         * the data itself are set, for example `name` or `color` or custom properties,
         * the grouping logic doesn't know how to group it. In this case the options of
         * the first point instance are copied over to the group point. This can be
         * altered through a custom `approximation` callback function.
         *
         * @declare   Highcharts.DataGroupingOptionsObject
         * @product   highstock
         * @requires  product:highstock
         * @requires  module:modules/datagrouping
         * @apioption plotOptions.series.dataGrouping
         */
        /**
         * Specifies how the points should be located on the X axis inside the group.
         * Points that are extremes can be set separately. Available options:
         *
         * - `start` places the point at the beginning of the group
         * (e.g. range 00:00:00 - 23:59:59 -> 00:00:00)
         *
         * - `middle` places the point in the middle of the group
         * (e.g. range 00:00:00 - 23:59:59 -> 12:00:00)
         *
         * - `end` places the point at the end of the group
         * (e.g. range 00:00:00 - 23:59:59 -> 23:59:59)
         *
         * @sample {highstock} stock/plotoptions/series-datagrouping-anchor
         *         Changing the point x-coordinate inside the group.
         *
         * @see [dataGrouping.firstAnchor](#plotOptions.series.dataGrouping.firstAnchor)
         * @see [dataGrouping.lastAnchor](#plotOptions.series.dataGrouping.lastAnchor)
         *
         * @type       {Highcharts.DataGroupingAnchor}
         * @since 9.1.0
         * @default    start
         * @apioption  plotOptions.series.dataGrouping.anchor
         */
        /**
         * The method of approximation inside a group. When for example 30 days
         * are grouped into one month, this determines what value should represent
         * the group. Possible values are "average", "averages", "open", "high",
         * "low", "close" and "sum". For OHLC and candlestick series the approximation
         * is "ohlc" by default, which finds the open, high, low and close values
         * within all the grouped data. For ranges, the approximation is "range",
         * which finds the low and high values. For multi-dimensional data,
         * like ranges and OHLC, "averages" will compute the average for each
         * dimension.
         *
         * Custom aggregate methods can be added by assigning a callback function
         * as the approximation. This function takes a numeric array as the
         * argument and should return a single numeric value or `null`. Note
         * that the numeric array will never contain null values, only true
         * numbers. Instead, if null values are present in the raw data, the
         * numeric array will have an `.hasNulls` property set to `true`. For
         * single-value data sets the data is available in the first argument
         * of the callback function. For OHLC data sets, all the open values
         * are in the first argument, all high values in the second etc.
         *
         * Since v4.2.7, grouping meta data is available in the approximation
         * callback from `this.dataGroupInfo`. It can be used to extract information
         * from the raw data.
         *
         * Defaults to `average` for line-type series, `sum` for columns, `range`
         * for range series, `hlc` for HLC, and `ohlc` for OHLC and candlestick.
         *
         * @sample {highstock} stock/plotoptions/series-datagrouping-approximation
         *         Approximation callback with custom data
         * @sample {highstock} stock/plotoptions/series-datagrouping-simple-approximation
         *         Simple approximation demo
         *
         * @type       {Highcharts.DataGroupingApproximationValue|Function}
         * @apioption  plotOptions.series.dataGrouping.approximation
         */
        /**
         * Datetime formats for the header of the tooltip in a stock chart.
         * The format can vary within a chart depending on the currently selected
         * time range and the current data grouping.
         *
         * The default formats are:
         * ```js
         * {
         *     millisecond: [
         *         '%A, %b %e, %H:%M:%S.%L', '%A, %b %e, %H:%M:%S.%L', '-%H:%M:%S.%L'
         *     ],
         *     second: ['%A, %b %e, %H:%M:%S', '%A, %b %e, %H:%M:%S', '-%H:%M:%S'],
         *     minute: ['%A, %b %e, %H:%M', '%A, %b %e, %H:%M', '-%H:%M'],
         *     hour: ['%A, %b %e, %H:%M', '%A, %b %e, %H:%M', '-%H:%M'],
         *     day: ['%A, %b %e, %Y', '%A, %b %e', '-%A, %b %e, %Y'],
         *     week: ['Week from %A, %b %e, %Y', '%A, %b %e', '-%A, %b %e, %Y'],
         *     month: ['%B %Y', '%B', '-%B %Y'],
         *     year: ['%Y', '%Y', '-%Y']
         * }
         * ```
         *
         * For each of these array definitions, the first item is the format
         * used when the active time span is one unit. For instance, if the
         * current data applies to one week, the first item of the week array
         * is used. The second and third items are used when the active time
         * span is more than two units. For instance, if the current data applies
         * to two weeks, the second and third item of the week array are used,
         *  and applied to the start and end date of the time span.
         *
         * @type      {Object}
         * @apioption plotOptions.series.dataGrouping.dateTimeLabelFormats
         */
        /**
         * Enable or disable data grouping.
         *
         * @type      {boolean}
         * @default   true
         * @apioption plotOptions.series.dataGrouping.enabled
         */
        /**
         * Specifies how the first grouped point is positioned on the xAxis.
         * If firstAnchor and/or lastAnchor are defined, then those options take
         * precedence over anchor for the first and/or last grouped points.
         * Available options:
         *
         * -`start` places the point at the beginning of the group
         * (e.g. range 00:00:00 - 23:59:59 -> 00:00:00)
         *
         * -`middle` places the point in the middle of the group
         * (e.g. range 00:00:00 - 23:59:59 -> 12:00:00)
         *
         * -`end` places the point at the end of the group
         * (e.g. range 00:00:00 - 23:59:59 -> 23:59:59)
         *
         * -`firstPoint` the first point in the group
         * (e.g. points at 00:13, 00:35, 00:59 -> 00:13)
         *
         * -`lastPoint` the last point in the group
         * (e.g. points at 00:13, 00:35, 00:59 -> 00:59)
         *
         * @sample {highstock} stock/plotoptions/series-datagrouping-first-anchor
         *         Applying first and last anchor.
         *
         * @see [dataGrouping.anchor](#plotOptions.series.dataGrouping.anchor)
         *
         * @type       {Highcharts.DataGroupingAnchorExtremes}
         * @since 9.1.0
         * @default    start
         * @apioption  plotOptions.series.dataGrouping.firstAnchor
         */
        /**
         * When data grouping is forced, it runs no matter how small the intervals
         * are. This can be handy for example when the sum should be calculated
         * for values appearing at random times within each hour.
         *
         * @type      {boolean}
         * @default   false
         * @apioption plotOptions.series.dataGrouping.forced
         */
        /**
         * The approximate pixel width of each group. If for example a series
         * with 30 points is displayed over a 600 pixel wide plot area, no grouping
         * is performed. If however the series contains so many points that
         * the spacing is less than the groupPixelWidth, Highcharts will try
         * to group it into appropriate groups so that each is more or less
         * two pixels wide. If multiple series with different group pixel widths
         * are drawn on the same x axis, all series will take the greatest width.
         * For example, line series have 2px default group width, while column
         * series have 10px. If combined, both the line and the column will
         * have 10px by default.
         *
         * @type      {number}
         * @default   2
         * @apioption plotOptions.series.dataGrouping.groupPixelWidth
         */
        /**
         * By default only points within the visible range are grouped. Enabling this
         * option will force data grouping to calculate all grouped points for a given
         * dataset. That option prevents for example a column series from calculating
         * a grouped point partially. The effect is similar to
         * [Series.getExtremesFromAll](#plotOptions.series.getExtremesFromAll) but does
         * not affect yAxis extremes.
         *
         * @sample {highstock} stock/plotoptions/series-datagrouping-groupall/
         *         Two series with the same data but different groupAll setting
         *
         * @type      {boolean}
         * @default   false
         * @since     6.1.0
         * @apioption plotOptions.series.dataGrouping.groupAll
         */
        /**
         * Specifies how the last grouped point is positioned on the xAxis.
         * If firstAnchor and/or lastAnchor are defined, then those options take
         * precedence over anchor for the first and/or last grouped points.
         * Available options:
         *
         * -`start` places the point at the beginning of the group
         * (e.g. range 00:00:00 - 23:59:59 -> 00:00:00)
         *
         * -`middle` places the point in the middle of the group
         * (e.g. range 00:00:00 - 23:59:59 -> 12:00:00)
         *
         * -`end` places the point at the end of the group
         * (e.g. range 00:00:00 - 23:59:59 -> 23:59:59)
         *
         * -`firstPoint` the first point in the group
         * (e.g. points at 00:13, 00:35, 00:59 -> 00:13)
         *
         * -`lastPoint` the last point in the group
         * (e.g. points at 00:13, 00:35, 00:59 -> 00:59)
         *
         * @sample {highstock} stock/plotoptions/series-datagrouping-first-anchor
         *         Applying first and last anchor.
         *
         * @sample {highstock} stock/plotoptions/series-datagrouping-last-anchor
         *         Applying the last anchor in the chart with live data.
         *
         * @see [dataGrouping.anchor](#plotOptions.series.dataGrouping.anchor)
         *
         * @type       {Highcharts.DataGroupingAnchorExtremes}
         * @since 9.1.0
         * @default    start
         * @apioption  plotOptions.series.dataGrouping.lastAnchor
         */
        /**
         * Normally, a group is indexed by the start of that group, so for example
         * when 30 daily values are grouped into one month, that month's x value
         * will be the 1st of the month. This apparently shifts the data to
         * the left. When the smoothed option is true, this is compensated for.
         * The data is shifted to the middle of the group, and min and max
         * values are preserved. Internally, this is used in the Navigator series.
         *
         * @type      {boolean}
         * @default   false
         * @deprecated
         * @apioption plotOptions.series.dataGrouping.smoothed
         */
        /**
         * An array determining what time intervals the data is allowed to be
         * grouped to. Each array item is an array where the first value is
         * the time unit and the second value another array of allowed multiples.
         *
         * Defaults to:
         * ```js
         * units: [[
         *     'millisecond', // unit name
         *     [1, 2, 5, 10, 20, 25, 50, 100, 200, 500] // allowed multiples
         * ], [
         *     'second',
         *     [1, 2, 5, 10, 15, 30]
         * ], [
         *     'minute',
         *     [1, 2, 5, 10, 15, 30]
         * ], [
         *     'hour',
         *     [1, 2, 3, 4, 6, 8, 12]
         * ], [
         *     'day',
         *     [1]
         * ], [
         *     'week',
         *     [1]
         * ], [
         *     'month',
         *     [1, 3, 6]
         * ], [
         *     'year',
         *     null
         * ]]
         * ```
         *
         * @type      {Array<Array<string,(Array<number>|null)>>}
         * @apioption plotOptions.series.dataGrouping.units
         */
        /**
         * The approximate pixel width of each group. If for example a series
         * with 30 points is displayed over a 600 pixel wide plot area, no grouping
         * is performed. If however the series contains so many points that
         * the spacing is less than the groupPixelWidth, Highcharts will try
         * to group it into appropriate groups so that each is more or less
         * two pixels wide. Defaults to `10`.
         *
         * @sample {highstock} stock/plotoptions/series-datagrouping-grouppixelwidth/
         *         Two series with the same data density but different groupPixelWidth
         *
         * @type      {number}
         * @default   10
         * @apioption plotOptions.column.dataGrouping.groupPixelWidth
         */
        ''; // required by JSDoc parsing

        return DataGroupingComposition;
    });
    _registerModule(_modules, 'masters/modules/datagrouping.src.js', [_modules['Core/Globals.js'], _modules['Extensions/DataGrouping/ApproximationDefaults.js'], _modules['Extensions/DataGrouping/ApproximationRegistry.js'], _modules['Extensions/DataGrouping/DataGrouping.js']], function (Highcharts, ApproximationDefaults, ApproximationRegistry, DataGrouping) {

        var G = Highcharts;
        G.dataGrouping = {
            approximationDefaults: ApproximationDefaults,
            approximations: ApproximationRegistry
        };
        DataGrouping.compose(G.Axis, G.Series, G.Tooltip);

    });
    _registerModule(_modules, 'Series/DataModifyComposition.js', [_modules['Core/Axis/Axis.js'], _modules['Core/Series/Point.js'], _modules['Core/Series/Series.js'], _modules['Core/Utilities.js']], function (Axis, Point, Series, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var pointTooltipFormatter = Point.prototype.tooltipFormatter;
        var addEvent = U.addEvent,
            arrayMax = U.arrayMax,
            arrayMin = U.arrayMin,
            correctFloat = U.correctFloat,
            defined = U.defined,
            isArray = U.isArray,
            isNumber = U.isNumber,
            isString = U.isString,
            pick = U.pick;
        /* *
         *
         *  Composition
         *
         * */
        var DataModifyComposition;
        (function (DataModifyComposition) {
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
             * Extends the series, axis and point classes with
             * compare and cumulative support.
             *
             * @private
             *
             * @param SeriesClass
             * Series class to use.
             *
             * @param AxisClass
             * Axis class to extend.
             *
             * @param PointClass
             * Point class to use.
             */
            function compose(SeriesClass, AxisClass, PointClass) {
                if (composedClasses.indexOf(SeriesClass) === -1) {
                    composedClasses.push(SeriesClass);
                    var seriesProto = SeriesClass.prototype;
                    seriesProto.setCompare = seriesSetCompare;
                    seriesProto.setCumulative = seriesSetCumulative;
                    addEvent(SeriesClass, 'afterInit', afterInit);
                    addEvent(SeriesClass, 'afterGetExtremes', afterGetExtremes);
                    addEvent(SeriesClass, 'afterProcessData', afterProcessData);
                }
                if (composedClasses.indexOf(AxisClass) === -1) {
                    composedClasses.push(AxisClass);
                    var axisProto = AxisClass.prototype;
                    axisProto.setCompare = axisSetCompare;
                    axisProto.setModifier = setModifier;
                    axisProto.setCumulative = axisSetCumulative;
                }
                if (composedClasses.indexOf(PointClass) === -1) {
                    composedClasses.push(PointClass);
                    var pointProto = PointClass.prototype;
                    pointProto.tooltipFormatter = tooltipFormatter;
                }
                return SeriesClass;
            }
            DataModifyComposition.compose = compose;
            /* ********************************************************************** *
             *  Start shared compare and cumulative logic                             *
             * ********************************************************************** */
            /**
             * Shared code for the axis.setCompare() and the axis.setCumulative()
             * methods. Inits the 'compare' or the 'cumulative' mode.
             * @private
             */
            function setModifier(mode, modeState, redraw) {
                if (!this.isXAxis) {
                    this.series.forEach(function (series) {
                        if (mode === 'compare' &&
                            typeof modeState !== 'boolean') {
                            series.setCompare(modeState, false);
                        }
                        else if (mode === 'cumulative' &&
                            !isString(modeState)) {
                            series.setCumulative(modeState, false);
                        }
                    });
                    if (pick(redraw, true)) {
                        this.chart.redraw();
                    }
                }
            }
            /**
             * Extend the tooltip formatter by adding support for the point.change
             * variable as well as the changeDecimals option.
             *
             * @ignore
             * @function Highcharts.Point#tooltipFormatter
             *
             * @param {string} pointFormat
             */
            function tooltipFormatter(pointFormat) {
                var point = this, numberFormatter = point.series.chart.numberFormatter, replace = function (value) {
                        pointFormat = pointFormat.replace('{point.' + value + '}', (point[value] > 0 && value === 'change' ? '+' : '') +
                            numberFormatter(point[value], pick(point.series.tooltipOptions.changeDecimals, 2)));
                };
                if (defined(point.change)) {
                    replace('change');
                }
                if (defined(point.cumulativeSum)) {
                    replace('cumulativeSum');
                }
                return pointTooltipFormatter.apply(this, [pointFormat]);
            }
            /**
             * Extend series.init by adding a methods to modify the y values used
             * for plotting on the y axis. For compare mode, this method is called both
             * from the axis when finding dataMin and dataMax,
             * and from the series.translate method.
             *
             * @ignore
             * @function Highcharts.Series#init
             */
            function afterInit() {
                var compare = this.options.compare;
                var dataModify;
                if (compare === 'percent' ||
                    compare === 'value' ||
                    this.options.cumulative) {
                    dataModify = new Additions(this);
                    if (compare === 'percent' || compare === 'value') {
                        // Set comparison mode
                        dataModify.initCompare(compare);
                    }
                    else {
                        // Set Cumulative Sum mode
                        dataModify.initCumulative();
                    }
                }
                this.dataModify = dataModify;
            }
            /**
             * Adjust the extremes (compare and cumulative modify the data).
             * @private
             */
            function afterGetExtremes(e) {
                var dataExtremes = e.dataExtremes,
                    activeYData = dataExtremes.activeYData;
                if (this.dataModify && dataExtremes) {
                    var extremes = void 0;
                    if (this.options.compare) {
                        extremes = [
                            this.dataModify.modifyValue(dataExtremes.dataMin),
                            this.dataModify.modifyValue(dataExtremes.dataMax)
                        ];
                    }
                    else if (this.options.cumulative &&
                        isArray(activeYData) &&
                        // If only one y visible, sum doesn't change
                        // so no need to change extremes
                        activeYData.length >= 2) {
                        extremes = Additions.getCumulativeExtremes(activeYData);
                    }
                    if (extremes) {
                        dataExtremes.dataMin = arrayMin(extremes);
                        dataExtremes.dataMax = arrayMax(extremes);
                    }
                }
            }
            /* ********************************************************************** *
             *  End shared compare and cumulative logic                               *
             * ********************************************************************** */
            /* ********************************************************************** *
             *  Start value compare logic                                             *
             * ********************************************************************** */
            /**
             * Highcharts Stock only. Set the
             * [compare](https://api.highcharts.com/highstock/plotOptions.series.compare)
             * mode of the series after render time.
             * In most cases it is more useful running
             * {@link Axis#setCompare} on the X axis to update all its series.
             *
             * @function Highcharts.Series#setCompare
             *
             * @param {string|null} [compare]
             *        Can be one of `undefined` (default), `null`, `"percent"`
             *        or `"value"`.
             *
             * @param {boolean} [redraw=true]
             *        Whether to redraw the chart or to wait for a later call to
             *        {@link Chart#redraw}.
             */
            function seriesSetCompare(compare, redraw) {
                // Survive to export, #5485 (and for options generally)
                this.options.compare = this.userOptions.compare = compare;
                // Fire series.init() that will set or delete series.dataModify
                this.update({}, pick(redraw, true));
                if (this.dataModify && (compare === 'value' || compare === 'percent')) {
                    this.dataModify.initCompare(compare);
                }
                else {
                    // When disabling, clear the points
                    this.points.forEach(function (point) {
                        delete point.change;
                    });
                }
            }
            /**
             * Extend series.processData by finding the first y value in the plot area,
             * used for comparing the following values
             *
             * @ignore
             * @function Highcharts.Series#processData
             */
            function afterProcessData() {
                var series = this;
                if (series.xAxis && // not pies
                    series.processedYData &&
                    series.dataModify) {
                    var processedXData = series.processedXData,
                        processedYData = series.processedYData,
                        length_1 = processedYData.length,
                        compareStart = series.options.compareStart === true ? 0 : 1;
                    var keyIndex = -1,
                        i = void 0;
                    // For series with more than one value (range, OHLC etc), compare
                    // against close or the pointValKey (#4922, #3112, #9854)
                    if (series.pointArrayMap) {
                        keyIndex = series.pointArrayMap.indexOf(series.options.pointValKey || series.pointValKey || 'y');
                    }
                    // find the first value for comparison
                    for (i = 0; i < length_1 - compareStart; i++) {
                        var compareValue = processedYData[i] && keyIndex > -1 ?
                                processedYData[i][keyIndex] : processedYData[i];
                        if (isNumber(compareValue) &&
                            compareValue !== 0 &&
                            processedXData[i + compareStart] >= (series.xAxis.min || 0)) {
                            series.dataModify.compareValue = compareValue;
                            break;
                        }
                    }
                }
            }
            /**
             * Highcharts Stock only. Set the compare mode on all series
             * belonging to a Y axis.
             *
             * @see [plotOptions.series.compare](https://api.highcharts.com/highstock/plotOptions.series.compare)
             *
             * @sample stock/members/axis-setcompare/
             *         Set compare
             *
             * @function Highcharts.Axis#setCompare
             *
             * @param {string|null} [compare]
             *        The compare mode. Can be one of `undefined` (default), `null`,
             *        `"value"` or `"percent"`.
             *
             * @param {boolean} [redraw=true]
             *        Whether to redraw the chart or to wait for a later call to
             *        {@link Chart#redraw}.
             */
            function axisSetCompare(compare, redraw) {
                this.setModifier('compare', compare, redraw);
            }
            /* ********************************************************************** *
             *  End value compare logic                                               *
             * ********************************************************************** */
            /* ********************************************************************** *
             *  Start Cumulative Sum logic, author: Rafal Sebestjanski                *
             * ********************************************************************** */
            /**
             * Highcharts Stock only. Set the
             * [cumulative](https://api.highcharts.com/highstock/plotOptions.series.cumulative)
             * mode of the series after render time.
             * In most cases it is more useful running
             * {@link Axis#setCumulative} on the Y axis to update all its series.
             *
             * @function Highcharts.Series#setCumulative
             *
             * @param {boolean} [cumulative=false]
             *        Either enable or disable Cumulative Sum mode.
             *        Can be one of `false` (default) or `true`.
             *
             * @param {boolean} [redraw=true]
             *        Whether to redraw the chart or to wait for a later call to
             *        {@link Chart#redraw}.
             */
            function seriesSetCumulative(cumulative, redraw) {
                // Set default value to false
                cumulative = pick(cumulative, false);
                // Survive to export, #5485 (and for options generally)
                this.options.cumulative = this.userOptions.cumulative = cumulative;
                // Fire series.init() that will set or delete series.dataModify
                this.update({}, pick(redraw, true));
                // If should, turn on the Cumulative Sum mode
                if (this.dataModify) {
                    this.dataModify.initCumulative();
                }
                else {
                    // When disabling, clear the points
                    this.points.forEach(function (point) {
                        delete point.cumulativeSum;
                    });
                }
            }
            /**
             * Highcharts Stock only. Set the cumulative mode on all series
             * belonging to a Y axis.
             *
             * @see [plotOptions.series.cumulative](https://api.highcharts.com/highstock/plotOptions.series.cumulative)
             *
             * @sample stock/members/axis-setcumulative/
             *         Set cumulative
             *
             * @function Highcharts.Axis#setCumulative
             *
             * @param {boolean} [cumulative]
             *        Whether to disable or enable the cumulative mode.
             *        Can be one of `undefined` (default, treated as `false`),
             *        `false` or `true`.
             *
             * @param {boolean} [redraw=true]
             *        Whether to redraw the chart or to wait for a later call to
             *        {@link Chart#redraw}.
             */
            function axisSetCumulative(cumulative, redraw) {
                this.setModifier('cumulative', cumulative, redraw);
            }
            /* *
             *
             *  Classes
             *
             * */
            /**
             * @private
             */
            var Additions = /** @class */ (function () {
                    /* *
                     *
                     *  Constructors
                     *
                     * */
                    /**
                     * @private
                     */
                    function Additions(series) {
                        this.series = series;
                }
                /* *
                *
                *  Functions
                *
                * */
                /**
                 * @private
                 */
                Additions.prototype.modifyValue = function () {
                    return 0;
                };
                /**
                 * @ignore
                 * @function Highcharts.Series#getCumulativeExtremes
                 *
                 * @param {Array} [activeYData]
                 *        An array cointaining all the points' y values
                 *        in a visible range.
                 */
                Additions.getCumulativeExtremes = function (activeYData) {
                    var cumulativeDataMin = Infinity,
                        cumulativeDataMax = -Infinity;
                    activeYData.reduce(function (prev, cur) {
                        var sum = prev + cur;
                        cumulativeDataMin = Math.min(cumulativeDataMin, sum, prev);
                        cumulativeDataMax = Math.max(cumulativeDataMax, sum, prev);
                        return sum;
                    });
                    return [cumulativeDataMin, cumulativeDataMax];
                };
                /**
                 * @ignore
                 * @function Highcharts.Series#initCompare
                 *
                 * @param {string} [compare]
                 *        Can be one of `"percent"` or `"value"`.
                 */
                Additions.prototype.initCompare = function (compare) {
                    // Set the modifyValue method
                    this.modifyValue = function (value, index) {
                        if (value === null) {
                            value = 0;
                        }
                        var compareValue = this.compareValue;
                        if (typeof value !== 'undefined' &&
                            typeof compareValue !== 'undefined') { // #2601, #5814
                            // Get the modified value
                            if (compare === 'value') {
                                value -= compareValue;
                                // Compare percent
                            }
                            else {
                                var compareBase = this.series.options.compareBase;
                                value = 100 * (value / compareValue) -
                                    (compareBase === 100 ? 0 : 100);
                            }
                            // record for tooltip etc.
                            if (typeof index !== 'undefined') {
                                var point = this.series.points[index];
                                if (point) {
                                    point.change = value;
                                }
                            }
                            return value;
                        }
                        return 0;
                    };
                };
                /**
                 * @ignore
                 * @function Highcharts.Series#initCumulative
                 */
                Additions.prototype.initCumulative = function () {
                    // Set the modifyValue method
                    this.modifyValue = function (value, index) {
                        if (value === null) {
                            value = 0;
                        }
                        if (value !== void 0 && index !== void 0) {
                            var prevPoint = index > 0 ?
                                    this.series.points[index - 1] : null;
                            // Get the modified value
                            if (prevPoint && prevPoint.cumulativeSum) {
                                value = correctFloat(prevPoint.cumulativeSum + value);
                            }
                            // Record for tooltip etc.
                            var point = this.series.points[index];
                            if (point) {
                                point.cumulativeSum = value;
                            }
                            return value;
                        }
                        return 0;
                    };
                };
                return Additions;
            }());
            DataModifyComposition.Additions = Additions;
        })(DataModifyComposition || (DataModifyComposition = {}));
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
         * Compare the values of the series against the first non-null, non-
         * zero value in the visible range. The y axis will show percentage
         * or absolute change depending on whether `compare` is set to `"percent"`
         * or `"value"`. When this is applied to multiple series, it allows
         * comparing the development of the series against each other. Adds
         * a `change` field to every point object.
         *
         * @see [compareBase](#plotOptions.series.compareBase)
         * @see [Axis.setCompare()](/class-reference/Highcharts.Axis#setCompare)
         * @see [Series.setCompare()](/class-reference/Highcharts.Series#setCompare)
         *
         * @sample {highstock} stock/plotoptions/series-compare-percent/
         *         Percent
         * @sample {highstock} stock/plotoptions/series-compare-value/
         *         Value
         *
         * @type      {string}
         * @since     1.0.1
         * @product   highstock
         * @validvalue ["percent", "value"]
         * @apioption plotOptions.series.compare
         */
        /**
         * Defines if comparison should start from the first point within the visible
         * range or should start from the first point **before** the range.
         *
         * In other words, this flag determines if first point within the visible range
         * will have 0% (`compareStart=true`) or should have been already calculated
         * according to the previous point (`compareStart=false`).
         *
         * @sample {highstock} stock/plotoptions/series-comparestart/
         *         Calculate compare within visible range
         *
         * @type      {boolean}
         * @default   false
         * @since     6.0.0
         * @product   highstock
         * @apioption plotOptions.series.compareStart
         */
        /**
         * When [compare](#plotOptions.series.compare) is `percent`, this option
         * dictates whether to use 0 or 100 as the base of comparison.
         *
         * @sample {highstock} stock/plotoptions/series-comparebase/
         *         Compare base is 100
         *
         * @type       {number}
         * @default    0
         * @since      5.0.6
         * @product    highstock
         * @validvalue [0, 100]
         * @apioption  plotOptions.series.compareBase
         */
        /**
         * Cumulative Sum feature replaces points' values with the following formula:
         * `sum of all previous points' values + current point's value`.
         * Works only for points in a visible range.
         * Adds the `cumulativeSum` field to each point object that can be accessed
         * e.g. in the [tooltip.pointFormat](https://api.highcharts.com/highstock/tooltip.pointFormat).
         *
         * @see [Axis.setCumulative()](/class-reference/Highcharts.Axis#setCumulative)
         * @see [Series.setCumulative()](/class-reference/Highcharts.Series#setCumulative)
         *
         * @sample {highstock} stock/plotoptions/series-cumulative-sum/
         *         Cumulative Sum
         *
         * @type      {boolean}
         * @default   false
         * @since 9.3.0
         * @product   highstock
         * @apioption plotOptions.series.cumulative
         */
        ''; // keeps doclets above in transpiled file

        return DataModifyComposition;
    });
    _registerModule(_modules, 'Core/Axis/NavigatorAxisComposition.js', [_modules['Core/Globals.js'], _modules['Core/Utilities.js']], function (H, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var isTouchDevice = H.isTouchDevice;
        var addEvent = U.addEvent,
            correctFloat = U.correctFloat,
            defined = U.defined,
            isNumber = U.isNumber,
            pick = U.pick;
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
         * @private
         */
        function onAxisInit() {
            var axis = this;
            if (!axis.navigatorAxis) {
                axis.navigatorAxis = new NavigatorAxisAdditions(axis);
            }
        }
        /**
         * For Stock charts, override selection zooming with some special features
         * because X axis zooming is already allowed by the Navigator and Range
         * selector.
         * @private
         */
        function onAxisZoom(e) {
            var axis = this,
                chart = axis.chart,
                chartOptions = chart.options,
                navigator = chartOptions.navigator,
                navigatorAxis = axis.navigatorAxis,
                pinchType = chartOptions.chart.zooming.pinchType,
                rangeSelector = chartOptions.rangeSelector,
                zoomType = chartOptions.chart.zooming.type;
            if (axis.isXAxis && ((navigator && navigator.enabled) ||
                (rangeSelector && rangeSelector.enabled))) {
                // For y only zooming, ignore the X axis completely
                if (zoomType === 'y') {
                    e.zoomed = false;
                    // For xy zooming, record the state of the zoom before zoom
                    // selection, then when the reset button is pressed, revert to
                    // this state. This should apply only if the chart is
                    // initialized with a range (#6612), otherwise zoom all the way
                    // out.
                }
                else if (((!isTouchDevice && zoomType === 'xy') ||
                    (isTouchDevice && pinchType === 'xy')) &&
                    axis.options.range) {
                    var previousZoom = navigatorAxis.previousZoom;
                    if (defined(e.newMin)) {
                        navigatorAxis.previousZoom = [axis.min, axis.max];
                    }
                    else if (previousZoom) {
                        e.newMin = previousZoom[0];
                        e.newMax = previousZoom[1];
                        navigatorAxis.previousZoom = void 0;
                    }
                }
            }
            if (typeof e.zoomed !== 'undefined') {
                e.preventDefault();
            }
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
        var NavigatorAxisAdditions = /** @class */ (function () {
                /* *
                 *
                 *  Constructors
                 *
                 * */
                function NavigatorAxisAdditions(axis) {
                    this.axis = axis;
            }
            /* *
             *
             *  Static Functions
             *
             * */
            /**
             * @private
             */
            NavigatorAxisAdditions.compose = function (AxisClass) {
                if (composedClasses.indexOf(AxisClass) === -1) {
                    composedClasses.push(AxisClass);
                    AxisClass.keepProps.push('navigatorAxis');
                    addEvent(AxisClass, 'init', onAxisInit);
                    addEvent(AxisClass, 'zoom', onAxisZoom);
                }
            };
            /* *
             *
             *  Functions
             *
             * */
            /**
             * @private
             */
            NavigatorAxisAdditions.prototype.destroy = function () {
                this.axis = void 0;
            };
            /**
             * Add logic to normalize the zoomed range in order to preserve the pressed
             * state of range selector buttons
             *
             * @private
             * @function Highcharts.Axis#toFixedRange
             */
            NavigatorAxisAdditions.prototype.toFixedRange = function (pxMin, pxMax, fixedMin, fixedMax) {
                var axis = this.axis,
                    chart = axis.chart;
                var newMin = pick(fixedMin,
                    axis.translate(pxMin,
                    true, !axis.horiz)),
                    newMax = pick(fixedMax,
                    axis.translate(pxMax,
                    true, !axis.horiz));
                var fixedRange = chart && chart.fixedRange,
                    halfPointRange = (axis.pointRange || 0) / 2,
                    changeRatio = fixedRange && (newMax - newMin) / fixedRange;
                // Add/remove half point range to/from the extremes (#1172)
                if (!defined(fixedMin)) {
                    newMin = correctFloat(newMin + halfPointRange);
                }
                if (!defined(fixedMax)) {
                    newMax = correctFloat(newMax - halfPointRange);
                }
                // If the difference between the fixed range and the actual requested
                // range is too great, the user is dragging across an ordinal gap, and
                // we need to release the range selector button.
                if (changeRatio > 0.7 && changeRatio < 1.3) {
                    if (fixedMax) {
                        newMin = newMax - fixedRange;
                    }
                    else {
                        newMax = newMin + fixedRange;
                    }
                }
                if (!isNumber(newMin) || !isNumber(newMax)) { // #1195, #7411
                    newMin = newMax = void 0;
                }
                return {
                    min: newMin,
                    max: newMax
                };
            };
            return NavigatorAxisAdditions;
        }());
        /* *
         *
         *  Default Export
         *
         * */

        return NavigatorAxisAdditions;
    });
    _registerModule(_modules, 'Stock/Navigator/NavigatorDefaults.js', [_modules['Core/Color/Color.js'], _modules['Core/Series/SeriesRegistry.js']], function (Color, SeriesRegistry) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var color = Color.parse;
        var seriesTypes = SeriesRegistry.seriesTypes;
        /* *
         *
         *  Constants
         *
         * */
        /**
         * The navigator is a small series below the main series, displaying
         * a view of the entire data set. It provides tools to zoom in and
         * out on parts of the data as well as panning across the dataset.
         *
         * @product      highstock gantt
         * @optionparent navigator
         */
        var NavigatorDefaults = {
                /**
                 * Whether the navigator and scrollbar should adapt to updated data
                 * in the base X axis. When loading data async, as in the demo below,
                 * this should be `false`. Otherwise new data will trigger navigator
                 * redraw, which will cause unwanted looping. In the demo below, the
                 * data in the navigator is set only once. On navigating, only the main
                 * chart content is updated.
                 *
                 * @sample {highstock} stock/demo/lazy-loading/
                 *         Set to false with async data loading
                 *
                 * @type      {boolean}
                 * @default   true
                 * @apioption navigator.adaptToUpdatedData
                 */
                /**
                 * An integer identifying the index to use for the base series, or a
                 * string representing the id of the series.
                 *
                 * **Note**: As of Highcharts 5.0, this is now a deprecated option.
                 * Prefer [series.showInNavigator](#plotOptions.series.showInNavigator).
                 *
                 * @see [series.showInNavigator](#plotOptions.series.showInNavigator)
                 *
                 * @deprecated
                 * @type      {number|string}
                 * @default   0
                 * @apioption navigator.baseSeries
                 */
                /**
                 * Enable or disable the navigator.
                 *
                 * @sample {highstock} stock/navigator/enabled/
                 *         Disable the navigator
                 *
                 * @type      {boolean}
                 * @default   true
                 * @apioption navigator.enabled
                 */
                /**
                 * When the chart is inverted, whether to draw the navigator on the
                 * opposite side.
                 *
                 * @type      {boolean}
                 * @default   false
                 * @since     5.0.8
                 * @apioption navigator.opposite
                 */
                /**
                 * The height of the navigator.
                 *
                 * @sample {highstock} stock/navigator/height/
                 *         A higher navigator
                 */
                height: 40,
                /**
                 * The distance from the nearest element, the X axis or X axis labels.
                 *
                 * @sample {highstock} stock/navigator/margin/
                 *         A margin of 2 draws the navigator closer to the X axis labels
                 */
                margin: 25,
                /**
                 * Whether the mask should be inside the range marking the zoomed
                 * range, or outside. In Highcharts Stock 1.x it was always `false`.
                 *
                 * @sample {highstock} stock/navigator/maskinside-false/
                 *         False, mask outside
                 *
                 * @since   2.0
                 */
                maskInside: true,
                /**
                 * Options for the handles for dragging the zoomed area.
                 *
                 * @sample {highstock} stock/navigator/handles/
                 *         Colored handles
                 */
                handles: {
                    /**
                     * Width for handles.
                     *
                     * @sample {highstock} stock/navigator/styled-handles/
                     *         Styled handles
                     *
                     * @since   6.0.0
                     */
                    width: 7,
                    /**
                     * Height for handles.
                     *
                     * @sample {highstock} stock/navigator/styled-handles/
                     *         Styled handles
                     *
                     * @since   6.0.0
                     */
                    height: 15,
                    /**
                     * Array to define shapes of handles. 0-index for left, 1-index for
                     * right.
                     *
                     * Additionally, the URL to a graphic can be given on this form:
                     * `url(graphic.png)`. Note that for the image to be applied to
                     * exported charts, its URL needs to be accessible by the export
                     * server.
                     *
                     * Custom callbacks for symbol path generation can also be added to
                     * `Highcharts.SVGRenderer.prototype.symbols`. The callback is then
                     * used by its method name, as shown in the demo.
                     *
                     * @sample {highstock} stock/navigator/styled-handles/
                     *         Styled handles
                     *
                     * @type    {Array<string>}
                     * @default ["navigator-handle", "navigator-handle"]
                     * @since   6.0.0
                     */
                    symbols: ['navigator-handle', 'navigator-handle'],
                    /**
                     * Allows to enable/disable handles.
                     *
                     * @since   6.0.0
                     */
                    enabled: true,
                    /**
                     * The width for the handle border and the stripes inside.
                     *
                     * @sample {highstock} stock/navigator/styled-handles/
                     *         Styled handles
                     *
                     * @since     6.0.0
                     * @apioption navigator.handles.lineWidth
                     */
                    lineWidth: 1,
                    /**
                     * The fill for the handle.
                     *
                     * @type    {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                     */
                    backgroundColor: "#f2f2f2" /* Palette.neutralColor5 */,
                    /**
                     * The stroke for the handle border and the stripes inside.
                     *
                     * @type    {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                     */
                    borderColor: "#999999" /* Palette.neutralColor40 */
                },
                /**
                 * The color of the mask covering the areas of the navigator series
                 * that are currently not visible in the main series. The default
                 * color is bluish with an opacity of 0.3 to see the series below.
                 *
                 * @see In styled mode, the mask is styled with the
                 *      `.highcharts-navigator-mask` and
                 *      `.highcharts-navigator-mask-inside` classes.
                 *
                 * @sample {highstock} stock/navigator/maskfill/
                 *         Blue, semi transparent mask
                 *
                 * @type    {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 * @default rgba(102,133,194,0.3)
                 */
                maskFill: color("#6685c2" /* Palette.highlightColor60 */).setOpacity(0.3).get(),
                /**
                 * The color of the line marking the currently zoomed area in the
                 * navigator.
                 *
                 * @sample {highstock} stock/navigator/outline/
                 *         2px blue outline
                 *
                 * @type    {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 * @default #cccccc
                 */
                outlineColor: "#cccccc" /* Palette.neutralColor20 */,
                /**
                 * The width of the line marking the currently zoomed area in the
                 * navigator.
                 *
                 * @see In styled mode, the outline stroke width is set with the
                 *      `.highcharts-navigator-outline` class.
                 *
                 * @sample {highstock} stock/navigator/outline/
                 *         2px blue outline
                 *
                 * @type    {number}
                 */
                outlineWidth: 1,
                /**
                 * Options for the navigator series. Available options are the same
                 * as any series, documented at [plotOptions](#plotOptions.series)
                 * and [series](#series).
                 *
                 * Unless data is explicitly defined on navigator.series, the data
                 * is borrowed from the first series in the chart.
                 *
                 * Default series options for the navigator series are:
                 * ```js
                 * series: {
                 *     type: 'areaspline',
                 *     fillOpacity: 0.05,
                 *     dataGrouping: {
                 *         smoothed: true
                 *     },
                 *     lineWidth: 1,
                 *     marker: {
                 *         enabled: false
                 *     }
                 * }
                 * ```
                 *
                 * @see In styled mode, the navigator series is styled with the
                 *      `.highcharts-navigator-series` class.
                 *
                 * @sample {highstock} stock/navigator/series-data/
                 *         Using a separate data set for the navigator
                 * @sample {highstock} stock/navigator/series/
                 *         A green navigator series
                 *
                 * @type {*|Array<*>|Highcharts.SeriesOptionsType|Array<Highcharts.SeriesOptionsType>}
                 */
                series: {
                    /**
                     * The type of the navigator series.
                     *
                     * Heads up:
                     * In column-type navigator, zooming is limited to at least one
                     * point with its `pointRange`.
                     *
                     * @sample {highstock} stock/navigator/column/
                     *         Column type navigator
                     *
                     * @type    {string}
                     * @default {highstock} `areaspline` if defined, otherwise `line`
                     * @default {gantt} gantt
                     */
                    type: (typeof seriesTypes.areaspline === 'undefined' ?
                        'line' :
                        'areaspline'),
                    /**
                     * The fill opacity of the navigator series.
                     */
                    fillOpacity: 0.05,
                    /**
                     * The pixel line width of the navigator series.
                     */
                    lineWidth: 1,
                    /**
                     * @ignore-option
                     */
                    compare: null,
                    /**
                     * Unless data is explicitly defined, the data is borrowed from the
                     * first series in the chart.
                     *
                     * @type      {Array<number|Array<number|string|null>|object|null>}
                     * @product   highstock
                     * @apioption navigator.series.data
                     */
                    /**
                     * Data grouping options for the navigator series.
                     *
                     * @extends plotOptions.series.dataGrouping
                     */
                    dataGrouping: {
                        approximation: 'average',
                        enabled: true,
                        groupPixelWidth: 2,
                        // Replace smoothed property by anchors, #12455.
                        firstAnchor: 'firstPoint',
                        anchor: 'middle',
                        lastAnchor: 'lastPoint',
                        // Day and week differs from plotOptions.series.dataGrouping
                        units: [
                            ['millisecond', [1, 2, 5, 10, 20, 25, 50, 100, 200, 500]],
                            ['second', [1, 2, 5, 10, 15, 30]],
                            ['minute', [1, 2, 5, 10, 15, 30]],
                            ['hour', [1, 2, 3, 4, 6, 8, 12]],
                            ['day', [1, 2, 3, 4]],
                            ['week', [1, 2, 3]],
                            ['month', [1, 3, 6]],
                            ['year', null]
                        ]
                    },
                    /**
                     * Data label options for the navigator series. Data labels are
                     * disabled by default on the navigator series.
                     *
                     * @extends plotOptions.series.dataLabels
                     */
                    dataLabels: {
                        enabled: false,
                        zIndex: 2 // #1839
                    },
                    id: 'highcharts-navigator-series',
                    className: 'highcharts-navigator-series',
                    /**
                     * Sets the fill color of the navigator series.
                     *
                     * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                     * @apioption navigator.series.color
                     */
                    /**
                     * Line color for the navigator series. Allows setting the color
                     * while disallowing the default candlestick setting.
                     *
                     * @type {Highcharts.ColorString|null}
                     */
                    lineColor: null,
                    marker: {
                        enabled: false
                    },
                    /**
                     * Since Highcharts Stock v8, default value is the same as default
                     * `pointRange` defined for a specific type (e.g. `null` for
                     * column type).
                     *
                     * In Highcharts Stock version < 8, defaults to 0.
                     *
                     * @extends plotOptions.series.pointRange
                     * @type {number|null}
                     * @apioption navigator.series.pointRange
                     */
                    /**
                     * The threshold option. Setting it to 0 will make the default
                     * navigator area series draw its area from the 0 value and up.
                     *
                     * @type {number|null}
                     */
                    threshold: null
                },
                /**
                 * Enable or disable navigator sticking to right, while adding new
                 * points. If `undefined`, the navigator sticks to the axis maximum only
                 * if it was already at the maximum prior to adding points.
                 *
                 * @type      {boolean}
                 * @default   undefined
                 * @since 10.2.1
                 * @sample {highstock} stock/navigator/sticktomax-false/
                 * stickToMax set to false
                 * @apioption navigator.stickToMax
                 */
                /**
                 * Options for the navigator X axis. Default series options for the
                 * navigator xAxis are:
                 * ```js
                 * xAxis: {
                 *     tickWidth: 0,
                 *     lineWidth: 0,
                 *     gridLineWidth: 1,
                 *     tickPixelInterval: 200,
                 *     labels: {
                 *            align: 'left',
                 *         style: {
                 *             color: '#888'
                 *         },
                 *         x: 3,
                 *         y: -4
                 *     }
                 * }
                 * ```
                 *
                 * @extends   xAxis
                 * @excluding linkedTo, maxZoom, minRange, opposite, range, scrollbar,
                 *            showEmpty, maxRange
                 */
                xAxis: {
                    /**
                     * Additional range on the right side of the xAxis. Works similar to
                     * xAxis.maxPadding, but value is set in milliseconds.
                     * Can be set for both, main xAxis and navigator's xAxis.
                     *
                     * @since   6.0.0
                     */
                    overscroll: 0,
                    className: 'highcharts-navigator-xaxis',
                    tickLength: 0,
                    lineWidth: 0,
                    gridLineColor: "#e6e6e6" /* Palette.neutralColor10 */,
                    gridLineWidth: 1,
                    tickPixelInterval: 200,
                    labels: {
                        align: 'left',
                        /**
                         * @type {Highcharts.CSSObject}
                         */
                        style: {
                            /** @ignore */
                            color: "#999999" /* Palette.neutralColor40 */
                        },
                        x: 3,
                        y: -4
                    },
                    crosshair: false
                },
                /**
                 * Options for the navigator Y axis. Default series options for the
                 * navigator yAxis are:
                 * ```js
                 * yAxis: {
                 *     gridLineWidth: 0,
                 *     startOnTick: false,
                 *     endOnTick: false,
                 *     minPadding: 0.1,
                 *     maxPadding: 0.1,
                 *     labels: {
                 *         enabled: false
                 *     },
                 *     title: {
                 *         text: null
                 *     },
                 *     tickWidth: 0
                 * }
                 * ```
                 *
                 * @extends   yAxis
                 * @excluding height, linkedTo, maxZoom, minRange, ordinal, range,
                 *            showEmpty, scrollbar, top, units, maxRange, minLength,
                 *            maxLength, resize
                 */
                yAxis: {
                    className: 'highcharts-navigator-yaxis',
                    gridLineWidth: 0,
                    startOnTick: false,
                    endOnTick: false,
                    minPadding: 0.1,
                    maxPadding: 0.1,
                    labels: {
                        enabled: false
                    },
                    crosshair: false,
                    title: {
                        text: null
                    },
                    tickLength: 0,
                    tickWidth: 0
                }
            };
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
         * Maximum range which can be set using the navigator's handles.
         * Opposite of [xAxis.minRange](#xAxis.minRange).
         *
         * @sample {highstock} stock/navigator/maxrange/
         *         Defined max and min range
         *
         * @type      {number}
         * @since     6.0.0
         * @product   highstock gantt
         * @apioption xAxis.maxRange
         */
        (''); // keeps doclets above in JS file

        return NavigatorDefaults;
    });
    _registerModule(_modules, 'Stock/Navigator/NavigatorSymbols.js', [], function () {
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
         *  Constants
         *
         * */
        /**
         * Draw one of the handles on the side of the zoomed range in the navigator.
         * @private
         */
        function navigatorHandle(_x, _y, width, height, options) {
            if (options === void 0) { options = {}; }
            var halfWidth = options.width ? options.width / 2 : width,
                markerPosition = Math.round(halfWidth / 3) + 0.5;
            height = options.height || height;
            return [
                ['M', -halfWidth - 1, 0.5],
                ['L', halfWidth, 0.5],
                ['L', halfWidth, height + 0.5],
                ['L', -halfWidth - 1, height + 0.5],
                ['L', -halfWidth - 1, 0.5],
                ['M', -markerPosition, 4],
                ['L', -markerPosition, height - 3],
                ['M', markerPosition - 1, 4],
                ['L', markerPosition - 1, height - 3]
            ];
        }
        /* *
         *
         *  Default Export
         *
         * */
        var NavigatorSymbols = {
                'navigator-handle': navigatorHandle
            };

        return NavigatorSymbols;
    });
    _registerModule(_modules, 'Stock/Navigator/NavigatorComposition.js', [_modules['Core/Defaults.js'], _modules['Core/Globals.js'], _modules['Core/Axis/NavigatorAxisComposition.js'], _modules['Stock/Navigator/NavigatorDefaults.js'], _modules['Stock/Navigator/NavigatorSymbols.js'], _modules['Core/Renderer/RendererRegistry.js'], _modules['Core/Utilities.js']], function (D, H, NavigatorAxisAdditions, NavigatorDefaults, NavigatorSymbols, RendererRegistry, U) {
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
        var isTouchDevice = H.isTouchDevice;
        var getRendererType = RendererRegistry.getRendererType;
        var addEvent = U.addEvent,
            extend = U.extend,
            merge = U.merge,
            pick = U.pick;
        /* *
         *
         *  Constants
         *
         * */
        var composedClasses = [];
        /* *
         *
         *  Variables
         *
         * */
        var NavigatorConstructor;
        /* *
         *
         *  Functions
         *
         * */
        /**
         * @private
         */
        function compose(AxisClass, ChartClass, NavigatorClass, SeriesClass) {
            NavigatorAxisAdditions.compose(AxisClass);
            NavigatorConstructor = NavigatorClass;
            if (composedClasses.indexOf(ChartClass) === -1) {
                composedClasses.push(ChartClass);
                var chartProto = ChartClass.prototype;
                chartProto.callbacks.push(onChartCallback);
                addEvent(ChartClass, 'afterAddSeries', onChartAfterAddSeries);
                addEvent(ChartClass, 'afterSetChartSize', onChartAfterSetChartSize);
                addEvent(ChartClass, 'afterUpdate', onChartAfterUpdate);
                addEvent(ChartClass, 'beforeRender', onChartBeforeRender);
                addEvent(ChartClass, 'beforeShowResetZoom', onChartBeforeShowResetZoom);
                addEvent(ChartClass, 'update', onChartUpdate);
            }
            if (composedClasses.indexOf(SeriesClass) === -1) {
                composedClasses.push(SeriesClass);
                addEvent(SeriesClass, 'afterUpdate', onSeriesAfterUpdate);
            }
            if (composedClasses.indexOf(getRendererType) === -1) {
                composedClasses.push(getRendererType);
                extend(getRendererType().prototype.symbols, NavigatorSymbols);
            }
            if (composedClasses.indexOf(setOptions) === -1) {
                composedClasses.push(setOptions);
                extend(defaultOptions, { navigator: NavigatorDefaults });
            }
        }
        /**
         * Handle adding new series.
         * @private
         */
        function onChartAfterAddSeries() {
            if (this.navigator) {
                // Recompute which series should be shown in navigator, and add them
                this.navigator.setBaseSeries(null, false);
            }
        }
        /**
         * For stock charts, extend the Chart.setChartSize method so that we can set the
         * final top position of the navigator once the height of the chart, including
         * the legend, is determined. #367. We can't use Chart.getMargins, because
         * labels offsets are not calculated yet.
         * @private
         */
        function onChartAfterSetChartSize() {
            var legend = this.legend,
                navigator = this.navigator;
            var scrollbarHeight,
                legendOptions,
                xAxis,
                yAxis;
            if (navigator) {
                legendOptions = legend && legend.options;
                xAxis = navigator.xAxis;
                yAxis = navigator.yAxis;
                scrollbarHeight = navigator.scrollbarHeight;
                // Compute the top position
                if (this.inverted) {
                    navigator.left = navigator.opposite ?
                        this.chartWidth - scrollbarHeight -
                            navigator.height :
                        this.spacing[3] + scrollbarHeight;
                    navigator.top = this.plotTop + scrollbarHeight;
                }
                else {
                    navigator.left = pick(xAxis.left, this.plotLeft + scrollbarHeight);
                    navigator.top = navigator.navigatorOptions.top ||
                        this.chartHeight -
                            navigator.height -
                            scrollbarHeight -
                            this.spacing[2] -
                            (this.rangeSelector && this.extraBottomMargin ?
                                this.rangeSelector.getHeight() :
                                0) -
                            ((legendOptions &&
                                legendOptions.verticalAlign === 'bottom' &&
                                legendOptions.layout !== 'proximate' && // #13392
                                legendOptions.enabled &&
                                !legendOptions.floating) ?
                                legend.legendHeight +
                                    pick(legendOptions.margin, 10) :
                                0) -
                            (this.titleOffset ? this.titleOffset[2] : 0);
                }
                if (xAxis && yAxis) { // false if navigator is disabled (#904)
                    if (this.inverted) {
                        xAxis.options.left = yAxis.options.left = navigator.left;
                    }
                    else {
                        xAxis.options.top = yAxis.options.top = navigator.top;
                    }
                    xAxis.setAxisSize();
                    yAxis.setAxisSize();
                }
            }
        }
        /**
         * Initialize navigator, if no scrolling exists yet.
         * @private
         */
        function onChartAfterUpdate(event) {
            if (!this.navigator && !this.scroller &&
                (this.options.navigator.enabled ||
                    this.options.scrollbar.enabled)) {
                this.scroller = this.navigator = new NavigatorConstructor(this);
                if (pick(event.redraw, true)) {
                    this.redraw(event.animation); // #7067
                }
            }
        }
        /**
         * Initialize navigator for stock charts
         * @private
         */
        function onChartBeforeRender() {
            var options = this.options;
            if (options.navigator.enabled ||
                options.scrollbar.enabled) {
                this.scroller = this.navigator = new NavigatorConstructor(this);
            }
        }
        /**
         * For Stock charts. For x only zooming, do not to create the zoom button
         * because X axis zooming is already allowed by the Navigator and Range
         * selector. (#9285)
         * @private
         */
        function onChartBeforeShowResetZoom() {
            var chartOptions = this.options,
                navigator = chartOptions.navigator,
                rangeSelector = chartOptions.rangeSelector;
            if (((navigator && navigator.enabled) ||
                (rangeSelector && rangeSelector.enabled)) &&
                ((!isTouchDevice &&
                    chartOptions.chart.zooming.type === 'x') ||
                    (isTouchDevice &&
                        chartOptions.chart.zooming.pinchType === 'x'))) {
                return false;
            }
        }
        /**
         * @private
         */
        function onChartCallback(chart) {
            var navigator = chart.navigator;
            // Initialize the navigator
            if (navigator && chart.xAxis[0]) {
                var extremes = chart.xAxis[0].getExtremes();
                navigator.render(extremes.min, extremes.max);
            }
        }
        /**
         * Merge options, if no scrolling exists yet
         * @private
         */
        function onChartUpdate(e) {
            var navigatorOptions = (e.options.navigator || {}),
                scrollbarOptions = (e.options.scrollbar || {});
            if (!this.navigator && !this.scroller &&
                (navigatorOptions.enabled || scrollbarOptions.enabled)) {
                merge(true, this.options.navigator, navigatorOptions);
                merge(true, this.options.scrollbar, scrollbarOptions);
                delete e.options.navigator;
                delete e.options.scrollbar;
            }
        }
        /**
         * Handle updating series
         * @private
         */
        function onSeriesAfterUpdate() {
            if (this.chart.navigator && !this.options.isInternal) {
                this.chart.navigator.setBaseSeries(null, false);
            }
        }
        /* *
         *
         *  Default Export
         *
         * */
        var NavigatorComposition = {
                compose: compose
            };

        return NavigatorComposition;
    });
    _registerModule(_modules, 'Core/Axis/ScrollbarAxis.js', [_modules['Core/Utilities.js']], function (U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var addEvent = U.addEvent,
            defined = U.defined,
            pick = U.pick;
        /* *
         *
         *  Composition
         *
         * */
        /* eslint-disable no-invalid-this, valid-jsdoc */
        /**
         * Creates scrollbars if enabled.
         * @private
         */
        var ScrollbarAxis = /** @class */ (function () {
                function ScrollbarAxis() {
                }
                /**
                 * Attaches to axis events to create scrollbars if enabled.
                 *
                 * @private
                 *
                 * @param AxisClass
                 * Axis class to extend.
                 *
                 * @param ScrollbarClass
                 * Scrollbar class to use.
                 */
                ScrollbarAxis.compose = function (AxisClass, ScrollbarClass) {
                    if (ScrollbarAxis.composed.indexOf(AxisClass) === -1) {
                        ScrollbarAxis.composed.push(AxisClass);
                }
                else {
                    return AxisClass;
                }
                var getExtremes = function (axis) {
                        var axisMin = pick(axis.options && axis.options.min,
                    axis.min);
                    var axisMax = pick(axis.options && axis.options.max,
                        axis.max);
                    return {
                        axisMin: axisMin,
                        axisMax: axisMax,
                        scrollMin: defined(axis.dataMin) ?
                            Math.min(axisMin, axis.min, axis.dataMin, pick(axis.threshold, Infinity)) : axisMin,
                        scrollMax: defined(axis.dataMax) ?
                            Math.max(axisMax, axis.max, axis.dataMax, pick(axis.threshold, -Infinity)) : axisMax
                    };
                };
                // Wrap axis initialization and create scrollbar if enabled:
                addEvent(AxisClass, 'afterInit', function () {
                    var axis = this;
                    if (axis.options &&
                        axis.options.scrollbar &&
                        axis.options.scrollbar.enabled) {
                        // Predefined options:
                        axis.options.scrollbar.vertical = !axis.horiz;
                        axis.options.startOnTick = axis.options.endOnTick = false;
                        axis.scrollbar = new ScrollbarClass(axis.chart.renderer, axis.options.scrollbar, axis.chart);
                        addEvent(axis.scrollbar, 'changed', function (e) {
                            var _a = getExtremes(axis),
                                axisMin = _a.axisMin,
                                axisMax = _a.axisMax,
                                unitedMin = _a.scrollMin,
                                unitedMax = _a.scrollMax,
                                range = unitedMax - unitedMin,
                                to,
                                from;
                            // #12834, scroll when show/hide series, wrong extremes
                            if (!defined(axisMin) || !defined(axisMax)) {
                                return;
                            }
                            if ((axis.horiz && !axis.reversed) ||
                                (!axis.horiz && axis.reversed)) {
                                to = unitedMin + range * this.to;
                                from = unitedMin + range * this.from;
                            }
                            else {
                                // y-values in browser are reversed, but this also
                                // applies for reversed horizontal axis:
                                to = unitedMin + range * (1 - this.from);
                                from = unitedMin + range * (1 - this.to);
                            }
                            if (this.shouldUpdateExtremes(e.DOMType)) {
                                axis.setExtremes(from, to, true, (e.DOMType !== 'mousemove' &&
                                    e.DOMType !== 'touchmove'), e);
                            }
                            else {
                                // When live redraw is disabled, don't change extremes
                                // Only change the position of the scollbar thumb
                                this.setRange(this.from, this.to);
                            }
                        });
                    }
                });
                // Wrap rendering axis, and update scrollbar if one is created:
                addEvent(AxisClass, 'afterRender', function () {
                    var axis = this,
                        _a = getExtremes(axis),
                        scrollMin = _a.scrollMin,
                        scrollMax = _a.scrollMax,
                        scrollbar = axis.scrollbar,
                        offset = (axis.axisTitleMargin + (axis.titleOffset || 0)),
                        scrollbarsOffsets = axis.chart.scrollbarsOffsets,
                        axisMargin = axis.options.margin || 0,
                        offsetsIndex,
                        from,
                        to;
                    if (scrollbar) {
                        if (axis.horiz) {
                            // Reserve space for labels/title
                            if (!axis.opposite) {
                                scrollbarsOffsets[1] += offset;
                            }
                            scrollbar.position(axis.left, (axis.top +
                                axis.height +
                                2 +
                                scrollbarsOffsets[1] -
                                (axis.opposite ? axisMargin : 0)), axis.width, axis.height);
                            // Next scrollbar should reserve space for margin (if set)
                            if (!axis.opposite) {
                                scrollbarsOffsets[1] += axisMargin;
                            }
                            offsetsIndex = 1;
                        }
                        else {
                            // Reserve space for labels/title
                            if (axis.opposite) {
                                scrollbarsOffsets[0] += offset;
                            }
                            var xPosition = void 0;
                            if (!scrollbar.options.opposite) {
                                xPosition = axis.opposite ? 0 : axisMargin;
                            }
                            else {
                                xPosition = axis.left +
                                    axis.width +
                                    2 +
                                    scrollbarsOffsets[0] -
                                    (axis.opposite ? 0 : axisMargin);
                            }
                            scrollbar.position(xPosition, axis.top, axis.width, axis.height);
                            // Next scrollbar should reserve space for margin (if set)
                            if (axis.opposite) {
                                scrollbarsOffsets[0] += axisMargin;
                            }
                            offsetsIndex = 0;
                        }
                        scrollbarsOffsets[offsetsIndex] += scrollbar.size +
                            scrollbar.options.margin;
                        if (isNaN(scrollMin) ||
                            isNaN(scrollMax) ||
                            !defined(axis.min) ||
                            !defined(axis.max) ||
                            axis.min === axis.max // #10733
                        ) {
                            // default action: when extremes are the same or there is
                            // not extremes on the axis, but scrollbar exists, make it
                            // full size
                            scrollbar.setRange(0, 1);
                        }
                        else {
                            from = ((axis.min - scrollMin) /
                                (scrollMax - scrollMin));
                            to = ((axis.max - scrollMin) /
                                (scrollMax - scrollMin));
                            if ((axis.horiz && !axis.reversed) ||
                                (!axis.horiz && axis.reversed)) {
                                scrollbar.setRange(from, to);
                            }
                            else {
                                // inverse vertical axis
                                scrollbar.setRange(1 - to, 1 - from);
                            }
                        }
                    }
                });
                // Make space for a scrollbar:
                addEvent(AxisClass, 'afterGetOffset', function () {
                    var axis = this,
                        opposite = axis.scrollbar && !axis.scrollbar.options.opposite,
                        index = axis.horiz ? 2 : opposite ? 3 : 1,
                        scrollbar = axis.scrollbar;
                    if (scrollbar) {
                        // reset scrollbars offsets
                        axis.chart.scrollbarsOffsets = [0, 0];
                        axis.chart.axisOffset[index] +=
                            scrollbar.size + scrollbar.options.margin;
                    }
                });
                return AxisClass;
            };
            ScrollbarAxis.composed = [];
            return ScrollbarAxis;
        }());

        return ScrollbarAxis;
    });
    _registerModule(_modules, 'Stock/Scrollbar/ScrollbarDefaults.js', [_modules['Core/Globals.js']], function (H) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var isTouchDevice = H.isTouchDevice;
        /* *
         *
         *  Constant
         *
         * */
        /**
         *
         * The scrollbar is a means of panning over the X axis of a stock chart.
         * Scrollbars can  also be applied to other types of axes.
         *
         * Another approach to scrollable charts is the [chart.scrollablePlotArea](
         * https://api.highcharts.com/highcharts/chart.scrollablePlotArea) option that
         * is especially suitable for simpler cartesian charts on mobile.
         *
         * In styled mode, all the presentational options for the
         * scrollbar are replaced by the classes `.highcharts-scrollbar-thumb`,
         * `.highcharts-scrollbar-arrow`, `.highcharts-scrollbar-button`,
         * `.highcharts-scrollbar-rifles` and `.highcharts-scrollbar-track`.
         *
         * @sample stock/yaxis/inverted-bar-scrollbar/
         *         A scrollbar on a simple bar chart
         *
         * @product highstock gantt
         * @optionparent scrollbar
         *
         * @private
         */
        var ScrollbarDefaults = {
                /**
                 * The height of the scrollbar. The height also applies to the width
                 * of the scroll arrows so that they are always squares. Defaults to
                 * 20 for touch devices and 14 for mouse devices.
                 *
                 * @sample stock/scrollbar/height/
                 *         A 30px scrollbar
                 *
                 * @type    {number}
                 * @default 20/14
                 */
                height: isTouchDevice ? 20 : 14,
                /**
                 * The border rounding radius of the bar.
                 *
                 * @sample stock/scrollbar/style/
                 *         Scrollbar styling
                 */
                barBorderRadius: 0,
                /**
                 * The corner radius of the scrollbar buttons.
                 *
                 * @sample stock/scrollbar/style/
                 *         Scrollbar styling
                 */
                buttonBorderRadius: 0,
                /**
                 * Enable or disable the scrollbar.
                 *
                 * @sample stock/scrollbar/enabled/
                 *         Disable the scrollbar,
            only use navigator
                 *
                 * @type      {boolean}
                 * @default   true
                 * @apioption scrollbar.enabled
                 */
                /**
                 * Whether to redraw the main chart as the scrollbar or the navigator
                 * zoomed window is moved. Defaults to `true` for modern browsers and
                 * `false` for legacy IE browsers as well as mobile devices.
                 *
                 * @sample stock/scrollbar/liveredraw
                 *         Setting live redraw to false
                 *
                 * @type  {boolean}
                 * @since 1.3
                 */
                liveRedraw: void 0,
                /**
                 * The margin between the scrollbar and its axis when the scrollbar is
                 * applied directly to an axis.
                 */
                margin: 10,
                /**
                 * The minimum width of the scrollbar.
                 *
                 * @since 1.2.5
                 */
                minWidth: 6,
                /** @ignore-option */
                opposite: true,
                /**
                 * Whether to show or hide the scrollbar when the scrolled content is
                 * zoomed out to it full extent.
                 *
                 * @type      {boolean}
                 * @default   true
                 * @apioption scrollbar.showFull
                 */
                step: 0.2,
                /**
                 * The z index of the scrollbar group.
                 */
                zIndex: 3,
                /**
                 * The background color of the scrollbar itself.
                 *
                 * @sample stock/scrollbar/style/
                 *         Scrollbar styling
                 *
                 * @type {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 */
                barBackgroundColor: "#cccccc" /* Palette.neutralColor20 */,
                /**
                 * The width of the bar's border.
                 *
                 * @sample stock/scrollbar/style/
                 *         Scrollbar styling
                 */
                barBorderWidth: 1,
                /**
                 * The color of the scrollbar's border.
                 *
                 * @type {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 */
                barBorderColor: "#cccccc" /* Palette.neutralColor20 */,
                /**
                 * The color of the small arrow inside the scrollbar buttons.
                 *
                 * @sample stock/scrollbar/style/
                 *         Scrollbar styling
                 *
                 * @type {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 */
                buttonArrowColor: "#333333" /* Palette.neutralColor80 */,
                /**
                 * The color of scrollbar buttons.
                 *
                 * @sample stock/scrollbar/style/
                 *         Scrollbar styling
                 *
                 * @type {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 */
                buttonBackgroundColor: "#e6e6e6" /* Palette.neutralColor10 */,
                /**
                 * The color of the border of the scrollbar buttons.
                 *
                 * @sample stock/scrollbar/style/
                 *         Scrollbar styling
                 *
                 * @type {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 */
                buttonBorderColor: "#cccccc" /* Palette.neutralColor20 */,
                /**
                 * The border width of the scrollbar buttons.
                 *
                 * @sample stock/scrollbar/style/
                 *         Scrollbar styling
                 */
                buttonBorderWidth: 1,
                /**
                 * The color of the small rifles in the middle of the scrollbar.
                 *
                 * @type {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 */
                rifleColor: "#333333" /* Palette.neutralColor80 */,
                /**
                 * The color of the track background.
                 *
                 * @sample stock/scrollbar/style/
                 *         Scrollbar styling
                 *
                 * @type {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 */
                trackBackgroundColor: "#f2f2f2" /* Palette.neutralColor5 */,
                /**
                 * The color of the border of the scrollbar track.
                 *
                 * @sample stock/scrollbar/style/
                 *         Scrollbar styling
                 *
                 * @type {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 */
                trackBorderColor: "#f2f2f2" /* Palette.neutralColor5 */,
                /**
                 * The corner radius of the border of the scrollbar track.
                 *
                 * @sample stock/scrollbar/style/
                 *         Scrollbar styling
                 *
                 * @type      {number}
                 * @default   0
                 * @apioption scrollbar.trackBorderRadius
                 */
                /**
                 * The width of the border of the scrollbar track.
                 *
                 * @sample stock/scrollbar/style/
                 *         Scrollbar styling
                 */
                trackBorderWidth: 1
            };
        /* *
         *
         *  Default Export
         *
         * */

        return ScrollbarDefaults;
    });
    _registerModule(_modules, 'Stock/Scrollbar/Scrollbar.js', [_modules['Core/Defaults.js'], _modules['Core/Globals.js'], _modules['Core/Axis/ScrollbarAxis.js'], _modules['Stock/Scrollbar/ScrollbarDefaults.js'], _modules['Core/Utilities.js']], function (D, H, ScrollbarAxis, ScrollbarDefaults, U) {
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
            correctFloat = U.correctFloat,
            defined = U.defined,
            destroyObjectProperties = U.destroyObjectProperties,
            fireEvent = U.fireEvent,
            merge = U.merge,
            pick = U.pick,
            removeEvent = U.removeEvent;
        /* *
         *
         *  Constants
         *
         * */
        /* eslint-disable no-invalid-this, valid-jsdoc */
        /**
         * A reusable scrollbar, internally used in Highcharts Stock's
         * navigator and optionally on individual axes.
         *
         * @private
         * @class
         * @name Highcharts.Scrollbar
         * @param {Highcharts.SVGRenderer} renderer
         * @param {Highcharts.ScrollbarOptions} options
         * @param {Highcharts.Chart} chart
         */
        var Scrollbar = /** @class */ (function () {
                /* *
                 *
                 *  Constructors
                 *
                 * */
                function Scrollbar(renderer, options, chart) {
                    /* *
                     *
                     *  Properties
                     *
                     * */
                    this._events = [];
                this.chart = void 0;
                this.chartX = 0;
                this.chartY = 0;
                this.from = 0;
                this.group = void 0;
                this.options = void 0;
                this.renderer = void 0;
                this.scrollbar = void 0;
                this.scrollbarButtons = [];
                this.scrollbarGroup = void 0;
                this.scrollbarLeft = 0;
                this.scrollbarRifles = void 0;
                this.scrollbarStrokeWidth = 1;
                this.scrollbarTop = 0;
                this.size = 0;
                this.to = 0;
                this.track = void 0;
                this.trackBorderWidth = 1;
                this.userOptions = void 0;
                this.x = 0;
                this.y = 0;
                this.init(renderer, options, chart);
            }
            /* *
             *
             *  Static Functions
             *
             * */
            Scrollbar.compose = function (AxisClass) {
                ScrollbarAxis.compose(AxisClass, Scrollbar);
            };
            /**
             * When we have vertical scrollbar, rifles and arrow in buttons should be
             * rotated. The same method is used in Navigator's handles, to rotate them.
             *
             * @function Highcharts.swapXY
             *
             * @param {Highcharts.SVGPathArray} path
             * Path to be rotated.
             *
             * @param {boolean} [vertical]
             * If vertical scrollbar, swap x-y values.
             *
             * @return {Highcharts.SVGPathArray}
             * Rotated path.
             *
             * @requires modules/stock
             */
            Scrollbar.swapXY = function (path, vertical) {
                if (vertical) {
                    path.forEach(function (seg) {
                        var len = seg.length;
                        var temp;
                        for (var i = 0; i < len; i += 2) {
                            temp = seg[i + 1];
                            if (typeof temp === 'number') {
                                seg[i + 1] = seg[i + 2];
                                seg[i + 2] = temp;
                            }
                        }
                    });
                }
                return path;
            };
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Set up the mouse and touch events for the Scrollbar
             *
             * @private
             * @function Highcharts.Scrollbar#addEvents
             */
            Scrollbar.prototype.addEvents = function () {
                var buttonsOrder = this.options.inverted ? [1, 0] : [0, 1],
                    buttons = this.scrollbarButtons,
                    bar = this.scrollbarGroup.element,
                    track = this.track.element,
                    mouseDownHandler = this.mouseDownHandler.bind(this),
                    mouseMoveHandler = this.mouseMoveHandler.bind(this),
                    mouseUpHandler = this.mouseUpHandler.bind(this);
                // Mouse events
                var _events = [
                        [
                            buttons[buttonsOrder[0]].element,
                            'click',
                            this.buttonToMinClick.bind(this)
                        ],
                        [
                            buttons[buttonsOrder[1]].element,
                            'click',
                            this.buttonToMaxClick.bind(this)
                        ],
                        [track, 'click',
                    this.trackClick.bind(this)],
                        [bar, 'mousedown',
                    mouseDownHandler],
                        [bar.ownerDocument, 'mousemove',
                    mouseMoveHandler],
                        [bar.ownerDocument, 'mouseup',
                    mouseUpHandler]
                    ];
                // Touch events
                if (H.hasTouch) {
                    _events.push([bar, 'touchstart', mouseDownHandler], [bar.ownerDocument, 'touchmove', mouseMoveHandler], [bar.ownerDocument, 'touchend', mouseUpHandler]);
                }
                // Add them all
                _events.forEach(function (args) {
                    addEvent.apply(null, args);
                });
                this._events = _events;
            };
            Scrollbar.prototype.buttonToMaxClick = function (e) {
                var scroller = this;
                var range = ((scroller.to - scroller.from) *
                        pick(scroller.options.step, 0.2));
                scroller.updatePosition(scroller.from + range, scroller.to + range);
                fireEvent(scroller, 'changed', {
                    from: scroller.from,
                    to: scroller.to,
                    trigger: 'scrollbar',
                    DOMEvent: e
                });
            };
            Scrollbar.prototype.buttonToMinClick = function (e) {
                var scroller = this;
                var range = correctFloat(scroller.to - scroller.from) *
                        pick(scroller.options.step, 0.2);
                scroller.updatePosition(correctFloat(scroller.from - range), correctFloat(scroller.to - range));
                fireEvent(scroller, 'changed', {
                    from: scroller.from,
                    to: scroller.to,
                    trigger: 'scrollbar',
                    DOMEvent: e
                });
            };
            /**
             * Get normalized (0-1) cursor position over the scrollbar
             *
             * @private
             * @function Highcharts.Scrollbar#cursorToScrollbarPosition
             *
             * @param  {*} normalizedEvent
             *         normalized event, with chartX and chartY values
             *
             * @return {Highcharts.Dictionary<number>}
             *         Local position {chartX, chartY}
             */
            Scrollbar.prototype.cursorToScrollbarPosition = function (normalizedEvent) {
                var scroller = this,
                    options = scroller.options,
                    minWidthDifference = options.minWidth > scroller.calculatedWidth ?
                        options.minWidth :
                        0; // minWidth distorts translation
                    return {
                        chartX: (normalizedEvent.chartX - scroller.x -
                            scroller.xOffset) /
                            (scroller.barWidth - minWidthDifference),
                        chartY: (normalizedEvent.chartY - scroller.y -
                            scroller.yOffset) /
                            (scroller.barWidth - minWidthDifference)
                    };
            };
            /**
             * Destroys allocated elements.
             *
             * @private
             * @function Highcharts.Scrollbar#destroy
             */
            Scrollbar.prototype.destroy = function () {
                var scroller = this,
                    navigator = scroller.chart.scroller;
                // Disconnect events added in addEvents
                scroller.removeEvents();
                // Destroy properties
                [
                    'track',
                    'scrollbarRifles',
                    'scrollbar',
                    'scrollbarGroup',
                    'group'
                ].forEach(function (prop) {
                    if (scroller[prop] && scroller[prop].destroy) {
                        scroller[prop] = scroller[prop].destroy();
                    }
                });
                // #6421, chart may have more scrollbars
                if (navigator && scroller === navigator.scrollbar) {
                    navigator.scrollbar = null;
                    // Destroy elements in collection
                    destroyObjectProperties(navigator.scrollbarButtons);
                }
            };
            /**
             * Draw the scrollbar buttons with arrows
             *
             * @private
             * @function Highcharts.Scrollbar#drawScrollbarButton
             * @param {number} index
             *        0 is left, 1 is right
             */
            Scrollbar.prototype.drawScrollbarButton = function (index) {
                var scroller = this,
                    renderer = scroller.renderer,
                    scrollbarButtons = scroller.scrollbarButtons,
                    options = scroller.options,
                    size = scroller.size,
                    group = renderer.g().add(scroller.group);
                var tempElem;
                scrollbarButtons.push(group);
                // Create a rectangle for the scrollbar button
                tempElem = renderer.rect()
                    .addClass('highcharts-scrollbar-button')
                    .add(group);
                // Presentational attributes
                if (!scroller.chart.styledMode) {
                    tempElem.attr({
                        stroke: options.buttonBorderColor,
                        'stroke-width': options.buttonBorderWidth,
                        fill: options.buttonBackgroundColor
                    });
                }
                // Place the rectangle based on the rendered stroke width
                tempElem.attr(tempElem.crisp({
                    x: -0.5,
                    y: -0.5,
                    width: size + 1,
                    height: size + 1,
                    r: options.buttonBorderRadius
                }, tempElem.strokeWidth()));
                // Button arrow
                tempElem = renderer
                    .path(Scrollbar.swapXY([[
                        'M',
                        size / 2 + (index ? -1 : 1),
                        size / 2 - 3
                    ], [
                        'L',
                        size / 2 + (index ? -1 : 1),
                        size / 2 + 3
                    ], [
                        'L',
                        size / 2 + (index ? 2 : -2),
                        size / 2
                    ]], options.vertical))
                    .addClass('highcharts-scrollbar-arrow')
                    .add(scrollbarButtons[index]);
                if (!scroller.chart.styledMode) {
                    tempElem.attr({
                        fill: options.buttonArrowColor
                    });
                }
            };
            /**
             * @private
             * @function Highcharts.Scrollbar#init
             * @param {Highcharts.SVGRenderer} renderer
             * @param {Highcharts.ScrollbarOptions} options
             * @param {Highcharts.Chart} chart
             */
            Scrollbar.prototype.init = function (renderer, options, chart) {
                var scroller = this;
                scroller.scrollbarButtons = [];
                scroller.renderer = renderer;
                scroller.userOptions = options;
                scroller.options = merge(ScrollbarDefaults, defaultOptions.scrollbar, options);
                scroller.chart = chart;
                // backward compatibility
                scroller.size = pick(scroller.options.size, scroller.options.height);
                // Init
                if (options.enabled) {
                    scroller.render();
                    scroller.addEvents();
                }
            };
            Scrollbar.prototype.mouseDownHandler = function (e) {
                var scroller = this,
                    normalizedEvent = scroller.chart.pointer.normalize(e),
                    mousePosition = scroller.cursorToScrollbarPosition(normalizedEvent);
                scroller.chartX = mousePosition.chartX;
                scroller.chartY = mousePosition.chartY;
                scroller.initPositions = [scroller.from, scroller.to];
                scroller.grabbedCenter = true;
            };
            /**
             * Event handler for the mouse move event.
             * @private
             */
            Scrollbar.prototype.mouseMoveHandler = function (e) {
                var scroller = this,
                    normalizedEvent = scroller.chart.pointer.normalize(e),
                    options = scroller.options,
                    direction = options.vertical ?
                        'chartY' : 'chartX',
                    initPositions = scroller.initPositions || [];
                var scrollPosition,
                    chartPosition,
                    change;
                // In iOS, a mousemove event with e.pageX === 0 is fired when
                // holding the finger down in the center of the scrollbar. This
                // should be ignored.
                if (scroller.grabbedCenter &&
                    // #4696, scrollbar failed on Android
                    (!e.touches || e.touches[0][direction] !== 0)) {
                    chartPosition = scroller.cursorToScrollbarPosition(normalizedEvent)[direction];
                    scrollPosition = scroller[direction];
                    change = chartPosition - scrollPosition;
                    scroller.hasDragged = true;
                    scroller.updatePosition(initPositions[0] + change, initPositions[1] + change);
                    if (scroller.hasDragged) {
                        fireEvent(scroller, 'changed', {
                            from: scroller.from,
                            to: scroller.to,
                            trigger: 'scrollbar',
                            DOMType: e.type,
                            DOMEvent: e
                        });
                    }
                }
            };
            /**
             * Event handler for the mouse up event.
             * @private
             */
            Scrollbar.prototype.mouseUpHandler = function (e) {
                var scroller = this;
                if (scroller.hasDragged) {
                    fireEvent(scroller, 'changed', {
                        from: scroller.from,
                        to: scroller.to,
                        trigger: 'scrollbar',
                        DOMType: e.type,
                        DOMEvent: e
                    });
                }
                scroller.grabbedCenter =
                    scroller.hasDragged =
                        scroller.chartX =
                            scroller.chartY = null;
            };
            /**
             * Position the scrollbar, method called from a parent with defined
             * dimensions.
             *
             * @private
             * @function Highcharts.Scrollbar#position
             * @param {number} x
             *        x-position on the chart
             * @param {number} y
             *        y-position on the chart
             * @param {number} width
             *        width of the scrollbar
             * @param {number} height
             *        height of the scorllbar
             */
            Scrollbar.prototype.position = function (x, y, width, height) {
                var scroller = this,
                    options = scroller.options,
                    vertical = options.vertical,
                    method = scroller.rendered ? 'animate' : 'attr';
                var xOffset = height,
                    yOffset = 0;
                // Make the scrollbar visible when it is repositioned, #15763.
                scroller.group.show();
                scroller.x = x;
                scroller.y = y + this.trackBorderWidth;
                scroller.width = width; // width with buttons
                scroller.height = height;
                scroller.xOffset = xOffset;
                scroller.yOffset = yOffset;
                // If Scrollbar is a vertical type, swap options:
                if (vertical) {
                    scroller.width = scroller.yOffset = width = yOffset = scroller.size;
                    scroller.xOffset = xOffset = 0;
                    scroller.barWidth = height - width * 2; // width without buttons
                    scroller.x = x = x + scroller.options.margin;
                }
                else {
                    scroller.height = scroller.xOffset = height = xOffset =
                        scroller.size;
                    scroller.barWidth = width - height * 2; // width without buttons
                    scroller.y = scroller.y + scroller.options.margin;
                }
                // Set general position for a group:
                scroller.group[method]({
                    translateX: x,
                    translateY: scroller.y
                });
                // Resize background/track:
                scroller.track[method]({
                    width: width,
                    height: height
                });
                // Move right/bottom button ot it's place:
                scroller.scrollbarButtons[1][method]({
                    translateX: vertical ? 0 : width - xOffset,
                    translateY: vertical ? height - yOffset : 0
                });
            };
            /**
             * Removes the event handlers attached previously with addEvents.
             *
             * @private
             * @function Highcharts.Scrollbar#removeEvents
             */
            Scrollbar.prototype.removeEvents = function () {
                this._events.forEach(function (args) {
                    removeEvent.apply(null, args);
                });
                this._events.length = 0;
            };
            /**
             * Render scrollbar with all required items.
             *
             * @private
             * @function Highcharts.Scrollbar#render
             */
            Scrollbar.prototype.render = function () {
                var scroller = this,
                    renderer = scroller.renderer,
                    options = scroller.options,
                    size = scroller.size,
                    styledMode = scroller.chart.styledMode,
                    group = renderer.g('scrollbar')
                        .attr({
                        zIndex: options.zIndex
                    })
                        .hide() // initially hide the scrollbar #15863
                        .add();
                // Draw the scrollbar group
                scroller.group = group;
                // Draw the scrollbar track:
                scroller.track = renderer.rect()
                    .addClass('highcharts-scrollbar-track')
                    .attr({
                    x: 0,
                    r: options.trackBorderRadius || 0,
                    height: size,
                    width: size
                }).add(group);
                if (!styledMode) {
                    scroller.track.attr({
                        fill: options.trackBackgroundColor,
                        stroke: options.trackBorderColor,
                        'stroke-width': options.trackBorderWidth
                    });
                }
                scroller.trackBorderWidth = scroller.track.strokeWidth();
                scroller.track.attr({
                    y: -this.trackBorderWidth % 2 / 2
                });
                // Draw the scrollbar itself
                scroller.scrollbarGroup = renderer.g().add(group);
                scroller.scrollbar = renderer.rect()
                    .addClass('highcharts-scrollbar-thumb')
                    .attr({
                    height: size,
                    width: size,
                    r: options.barBorderRadius || 0
                }).add(scroller.scrollbarGroup);
                scroller.scrollbarRifles = renderer
                    .path(Scrollbar.swapXY([
                    ['M', -3, size / 4],
                    ['L', -3, 2 * size / 3],
                    ['M', 0, size / 4],
                    ['L', 0, 2 * size / 3],
                    ['M', 3, size / 4],
                    ['L', 3, 2 * size / 3]
                ], options.vertical))
                    .addClass('highcharts-scrollbar-rifles')
                    .add(scroller.scrollbarGroup);
                if (!styledMode) {
                    scroller.scrollbar.attr({
                        fill: options.barBackgroundColor,
                        stroke: options.barBorderColor,
                        'stroke-width': options.barBorderWidth
                    });
                    scroller.scrollbarRifles.attr({
                        stroke: options.rifleColor,
                        'stroke-width': 1
                    });
                }
                scroller.scrollbarStrokeWidth = scroller.scrollbar.strokeWidth();
                scroller.scrollbarGroup.translate(-scroller.scrollbarStrokeWidth % 2 / 2, -scroller.scrollbarStrokeWidth % 2 / 2);
                // Draw the buttons:
                scroller.drawScrollbarButton(0);
                scroller.drawScrollbarButton(1);
            };
            /**
             * Set scrollbar size, with a given scale.
             *
             * @private
             * @function Highcharts.Scrollbar#setRange
             * @param {number} from
             *        scale (0-1) where bar should start
             * @param {number} to
             *        scale (0-1) where bar should end
             */
            Scrollbar.prototype.setRange = function (from, to) {
                var scroller = this,
                    options = scroller.options,
                    vertical = options.vertical,
                    minWidth = options.minWidth,
                    fullWidth = scroller.barWidth,
                    method = (this.rendered &&
                        !this.hasDragged &&
                        !(this.chart.navigator && this.chart.navigator.hasDragged)) ? 'animate' : 'attr';
                if (!defined(fullWidth)) {
                    return;
                }
                var toPX = fullWidth * Math.min(to, 1);
                var fromPX,
                    newSize;
                from = Math.max(from, 0);
                fromPX = Math.ceil(fullWidth * from);
                scroller.calculatedWidth = newSize = correctFloat(toPX - fromPX);
                // We need to recalculate position, if minWidth is used
                if (newSize < minWidth) {
                    fromPX = (fullWidth - minWidth + newSize) * from;
                    newSize = minWidth;
                }
                var newPos = Math.floor(fromPX + scroller.xOffset + scroller.yOffset);
                var newRiflesPos = newSize / 2 - 0.5; // -0.5 -> rifle line width / 2
                    // Store current position:
                    scroller.from = from;
                scroller.to = to;
                if (!vertical) {
                    scroller.scrollbarGroup[method]({
                        translateX: newPos
                    });
                    scroller.scrollbar[method]({
                        width: newSize
                    });
                    scroller.scrollbarRifles[method]({
                        translateX: newRiflesPos
                    });
                    scroller.scrollbarLeft = newPos;
                    scroller.scrollbarTop = 0;
                }
                else {
                    scroller.scrollbarGroup[method]({
                        translateY: newPos
                    });
                    scroller.scrollbar[method]({
                        height: newSize
                    });
                    scroller.scrollbarRifles[method]({
                        translateY: newRiflesPos
                    });
                    scroller.scrollbarTop = newPos;
                    scroller.scrollbarLeft = 0;
                }
                if (newSize <= 12) {
                    scroller.scrollbarRifles.hide();
                }
                else {
                    scroller.scrollbarRifles.show();
                }
                // Show or hide the scrollbar based on the showFull setting
                if (options.showFull === false) {
                    if (from <= 0 && to >= 1) {
                        scroller.group.hide();
                    }
                    else {
                        scroller.group.show();
                    }
                }
                scroller.rendered = true;
            };
            /**
             * Checks if the extremes should be updated in response to a scrollbar
             * change event.
             *
             * @private
             * @function Highcharts.Scrollbar#shouldUpdateExtremes
             */
            Scrollbar.prototype.shouldUpdateExtremes = function (eventType) {
                return (pick(this.options.liveRedraw, H.svg &&
                    !H.isTouchDevice &&
                    !this.chart.boosted) ||
                    // Mouseup always should change extremes
                    eventType === 'mouseup' ||
                    eventType === 'touchend' ||
                    // Internal events
                    !defined(eventType));
            };
            Scrollbar.prototype.trackClick = function (e) {
                var scroller = this;
                var normalizedEvent = scroller.chart.pointer.normalize(e),
                    range = scroller.to - scroller.from,
                    top = scroller.y + scroller.scrollbarTop,
                    left = scroller.x + scroller.scrollbarLeft;
                if ((scroller.options.vertical && normalizedEvent.chartY > top) ||
                    (!scroller.options.vertical && normalizedEvent.chartX > left)) {
                    // On the top or on the left side of the track:
                    scroller.updatePosition(scroller.from + range, scroller.to + range);
                }
                else {
                    // On the bottom or the right side of the track:
                    scroller.updatePosition(scroller.from - range, scroller.to - range);
                }
                fireEvent(scroller, 'changed', {
                    from: scroller.from,
                    to: scroller.to,
                    trigger: 'scrollbar',
                    DOMEvent: e
                });
            };
            /**
             * Update the scrollbar with new options
             *
             * @private
             * @function Highcharts.Scrollbar#update
             * @param  {Highcharts.ScrollbarOptions} options
             */
            Scrollbar.prototype.update = function (options) {
                this.destroy();
                this.init(this.chart.renderer, merge(true, this.options, options), this.chart);
            };
            /**
             * Update position option in the Scrollbar, with normalized 0-1 scale
             *
             * @private
             * @function Highcharts.Scrollbar#updatePosition
             * @param  {number} from
             * @param  {number} to
             */
            Scrollbar.prototype.updatePosition = function (from, to) {
                if (to > 1) {
                    from = correctFloat(1 - correctFloat(to - from));
                    to = 1;
                }
                if (from < 0) {
                    to = correctFloat(to - from);
                    from = 0;
                }
                this.from = from;
                this.to = to;
            };
            /* *
             *
             *  Static Properties
             *
             * */
            Scrollbar.defaultOptions = ScrollbarDefaults;
            return Scrollbar;
        }());
        /* *
         *
         *  Registry
         *
         * */
        defaultOptions.scrollbar = merge(true, Scrollbar.defaultOptions, defaultOptions.scrollbar);
        /* *
         *
         *  Default Export
         *
         * */

        return Scrollbar;
    });
    _registerModule(_modules, 'Stock/Navigator/Navigator.js', [_modules['Core/Axis/Axis.js'], _modules['Core/Defaults.js'], _modules['Core/Globals.js'], _modules['Core/Axis/NavigatorAxisComposition.js'], _modules['Stock/Navigator/NavigatorComposition.js'], _modules['Stock/Scrollbar/Scrollbar.js'], _modules['Core/Utilities.js']], function (Axis, D, H, NavigatorAxisAdditions, NavigatorComposition, Scrollbar, U) {
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
        var hasTouch = H.hasTouch,
            isTouchDevice = H.isTouchDevice;
        var addEvent = U.addEvent,
            clamp = U.clamp,
            correctFloat = U.correctFloat,
            defined = U.defined,
            destroyObjectProperties = U.destroyObjectProperties,
            erase = U.erase,
            extend = U.extend,
            find = U.find,
            isArray = U.isArray,
            isNumber = U.isNumber,
            merge = U.merge,
            pick = U.pick,
            removeEvent = U.removeEvent,
            splat = U.splat;
        /* *
         *
         *  Functions
         *
         * */
        /**
         * Finding the min or max of a set of variables where we don't know if they are
         * defined, is a pattern that is repeated several places in Highcharts. Consider
         * making this a global utility method.
         * @private
         */
        function numExt(extreme) {
            var args = [];
            for (var _i = 1; _i < arguments.length; _i++) {
                args[_i - 1] = arguments[_i];
            }
            var numbers = [].filter.call(args,
                isNumber);
            if (numbers.length) {
                return Math[extreme].apply(0, numbers);
            }
        }
        /* *
         *
         *  Class
         *
         * */
        /**
         * The Navigator class
         *
         * @private
         * @class
         * @name Highcharts.Navigator
         *
         * @param {Highcharts.Chart} chart
         *        Chart object
         */
        var Navigator = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function Navigator(chart) {
                    /* *
                     *
                     *  Properties
                     *
                     * */
                    this.baseSeries = void 0;
                this.chart = void 0;
                this.handles = void 0;
                this.height = void 0;
                this.left = void 0;
                this.navigatorEnabled = void 0;
                this.navigatorGroup = void 0;
                this.navigatorOptions = void 0;
                this.navigatorSeries = void 0;
                this.navigatorSize = void 0;
                this.opposite = void 0;
                this.outline = void 0;
                this.outlineHeight = void 0;
                this.range = void 0;
                this.rendered = void 0;
                this.shades = void 0;
                this.size = void 0;
                this.top = void 0;
                this.xAxis = void 0;
                this.yAxis = void 0;
                this.zoomedMax = void 0;
                this.zoomedMin = void 0;
                this.init(chart);
            }
            /* *
             *
             *  Static Functions
             *
             * */
            Navigator.compose = function (AxisClass, ChartClass, SeriesClass) {
                NavigatorComposition.compose(AxisClass, ChartClass, Navigator, SeriesClass);
            };
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Draw one of the handles on the side of the zoomed range in the navigator.
             *
             * @private
             * @function Highcharts.Navigator#drawHandle
             *
             * @param {number} x
             *        The x center for the handle
             *
             * @param {number} index
             *        0 for left and 1 for right
             *
             * @param {boolean|undefined} inverted
             *        Flag for chart.inverted
             *
             * @param {string} verb
             *        Use 'animate' or 'attr'
             */
            Navigator.prototype.drawHandle = function (x, index, inverted, verb) {
                var navigator = this,
                    height = navigator.navigatorOptions.handles.height;
                // Place it
                navigator.handles[index][verb](inverted ? {
                    translateX: Math.round(navigator.left + navigator.height / 2),
                    translateY: Math.round(navigator.top + parseInt(x, 10) + 0.5 - height)
                } : {
                    translateX: Math.round(navigator.left + parseInt(x, 10)),
                    translateY: Math.round(navigator.top + navigator.height / 2 - height / 2 - 1)
                });
            };
            /**
             * Render outline around the zoomed range
             *
             * @private
             * @function Highcharts.Navigator#drawOutline
             *
             * @param {number} zoomedMin
             *        in pixels position where zoomed range starts
             *
             * @param {number} zoomedMax
             *        in pixels position where zoomed range ends
             *
             * @param {boolean|undefined} inverted
             *        flag if chart is inverted
             *
             * @param {string} verb
             *        use 'animate' or 'attr'
             */
            Navigator.prototype.drawOutline = function (zoomedMin, zoomedMax, inverted, verb) {
                var navigator = this,
                    maskInside = navigator.navigatorOptions.maskInside,
                    outlineWidth = navigator.outline.strokeWidth(),
                    halfOutline = outlineWidth / 2,
                    outlineCorrection = (outlineWidth % 2) / 2, // #5800
                    outlineHeight = navigator.outlineHeight,
                    scrollbarHeight = navigator.scrollbarHeight || 0,
                    navigatorSize = navigator.size;
                var left = navigator.left - scrollbarHeight,
                    navigatorTop = navigator.top,
                    verticalMin,
                    path;
                if (inverted) {
                    left -= halfOutline;
                    verticalMin = navigatorTop + zoomedMax + outlineCorrection;
                    zoomedMax = navigatorTop + zoomedMin + outlineCorrection;
                    path = [
                        [
                            'M',
                            left + outlineHeight,
                            navigatorTop - scrollbarHeight - outlineCorrection
                        ],
                        // top right of zoomed range
                        ['L', left + outlineHeight, verticalMin],
                        ['L', left, verticalMin],
                        ['L', left, zoomedMax],
                        ['L', left + outlineHeight, zoomedMax],
                        [
                            'L',
                            left + outlineHeight,
                            navigatorTop + navigatorSize + scrollbarHeight
                        ]
                    ];
                    if (maskInside) {
                        path.push(
                        // upper left of zoomed range
                        ['M', left + outlineHeight, verticalMin - halfOutline], 
                        // upper right of z.r.
                        [
                            'L',
                            left + outlineHeight,
                            zoomedMax + halfOutline
                        ]);
                    }
                }
                else {
                    zoomedMin += left + scrollbarHeight - outlineCorrection;
                    zoomedMax += left + scrollbarHeight - outlineCorrection;
                    navigatorTop += halfOutline;
                    path = [
                        // left
                        ['M', left, navigatorTop],
                        // upper left of zoomed range
                        ['L', zoomedMin, navigatorTop],
                        // lower left of z.r.
                        ['L', zoomedMin, navigatorTop + outlineHeight],
                        // lower right of z.r.
                        ['L', zoomedMax, navigatorTop + outlineHeight],
                        // upper right of z.r.
                        ['L', zoomedMax, navigatorTop],
                        // right
                        ['L', left + navigatorSize + scrollbarHeight * 2, navigatorTop]
                    ];
                    if (maskInside) {
                        path.push(
                        // upper left of zoomed range
                        ['M', zoomedMin - halfOutline, navigatorTop], 
                        // upper right of z.r.
                        ['L', zoomedMax + halfOutline, navigatorTop]);
                    }
                }
                navigator.outline[verb]({
                    d: path
                });
            };
            /**
             * Render outline around the zoomed range
             *
             * @private
             * @function Highcharts.Navigator#drawMasks
             *
             * @param {number} zoomedMin
             *        in pixels position where zoomed range starts
             *
             * @param {number} zoomedMax
             *        in pixels position where zoomed range ends
             *
             * @param {boolean|undefined} inverted
             *        flag if chart is inverted
             *
             * @param {string} verb
             *        use 'animate' or 'attr'
             */
            Navigator.prototype.drawMasks = function (zoomedMin, zoomedMax, inverted, verb) {
                var navigator = this,
                    left = navigator.left,
                    top = navigator.top,
                    navigatorHeight = navigator.height;
                var height,
                    width,
                    x,
                    y;
                // Determine rectangle position & size
                // According to (non)inverted position:
                if (inverted) {
                    x = [left, left, left];
                    y = [top, top + zoomedMin, top + zoomedMax];
                    width = [navigatorHeight, navigatorHeight, navigatorHeight];
                    height = [
                        zoomedMin,
                        zoomedMax - zoomedMin,
                        navigator.size - zoomedMax
                    ];
                }
                else {
                    x = [left, left + zoomedMin, left + zoomedMax];
                    y = [top, top, top];
                    width = [
                        zoomedMin,
                        zoomedMax - zoomedMin,
                        navigator.size - zoomedMax
                    ];
                    height = [navigatorHeight, navigatorHeight, navigatorHeight];
                }
                navigator.shades.forEach(function (shade, i) {
                    shade[verb]({
                        x: x[i],
                        y: y[i],
                        width: width[i],
                        height: height[i]
                    });
                });
            };
            /**
             * Generate DOM elements for a navigator:
             *
             * - main navigator group
             *
             * - all shades
             *
             * - outline
             *
             * - handles
             *
             * @private
             * @function Highcharts.Navigator#renderElements
             */
            Navigator.prototype.renderElements = function () {
                var navigator = this,
                    navigatorOptions = navigator.navigatorOptions,
                    maskInside = navigatorOptions.maskInside,
                    chart = navigator.chart,
                    inverted = chart.inverted,
                    renderer = chart.renderer,
                    mouseCursor = {
                        cursor: inverted ? 'ns-resize' : 'ew-resize'
                    }, 
                    // Create the main navigator group
                    navigatorGroup = navigator.navigatorGroup = renderer
                        .g('navigator')
                        .attr({
                        zIndex: 8,
                        visibility: 'hidden'
                    })
                        .add();
                // Create masks, each mask will get events and fill:
                [
                    !maskInside,
                    maskInside,
                    !maskInside
                ].forEach(function (hasMask, index) {
                    var shade = renderer.rect()
                            .addClass('highcharts-navigator-mask' +
                            (index === 1 ? '-inside' : '-outside'))
                            .add(navigatorGroup);
                    if (!chart.styledMode) {
                        shade.attr({
                            fill: hasMask ?
                                navigatorOptions.maskFill :
                                'rgba(0,0,0,0)'
                        });
                        if (index === 1) {
                            shade.css(mouseCursor);
                        }
                    }
                    navigator.shades[index] = shade;
                });
                // Create the outline:
                navigator.outline = renderer.path()
                    .addClass('highcharts-navigator-outline')
                    .add(navigatorGroup);
                if (!chart.styledMode) {
                    navigator.outline.attr({
                        'stroke-width': navigatorOptions.outlineWidth,
                        stroke: navigatorOptions.outlineColor
                    });
                }
                // Create the handlers:
                if (navigatorOptions.handles && navigatorOptions.handles.enabled) {
                    var handlesOptions_1 = navigatorOptions.handles,
                        height_1 = handlesOptions_1.height,
                        width_1 = handlesOptions_1.width;
                    [0, 1].forEach(function (index) {
                        navigator.handles[index] = renderer.symbol(handlesOptions_1.symbols[index], -width_1 / 2 - 1, 0, width_1, height_1, handlesOptions_1);
                        if (chart.inverted) {
                            navigator.handles[index].attr({
                                rotation: 90,
                                rotationOriginX: Math.floor(-width_1 / 2),
                                rotationOriginY: (height_1 + width_1) / 2
                            });
                        }
                        // zIndex = 6 for right handle, 7 for left.
                        // Can't be 10, because of the tooltip in inverted chart #2908
                        navigator.handles[index].attr({ zIndex: 7 - index })
                            .addClass('highcharts-navigator-handle ' +
                            'highcharts-navigator-handle-' +
                            ['left', 'right'][index]).add(navigatorGroup);
                        if (!chart.styledMode) {
                            navigator.handles[index]
                                .attr({
                                fill: handlesOptions_1.backgroundColor,
                                stroke: handlesOptions_1.borderColor,
                                'stroke-width': handlesOptions_1.lineWidth
                            })
                                .css(mouseCursor);
                        }
                    });
                }
            };
            /**
             * Update navigator
             *
             * @private
             * @function Highcharts.Navigator#update
             *
             * @param {Highcharts.NavigatorOptions} options
             *        Options to merge in when updating navigator
             */
            Navigator.prototype.update = function (options) {
                // Remove references to old navigator series in base series
                (this.series || []).forEach(function (series) {
                    if (series.baseSeries) {
                        delete series.baseSeries.navigatorSeries;
                    }
                });
                // Destroy and rebuild navigator
                this.destroy();
                var chartOptions = this.chart.options;
                merge(true, chartOptions.navigator, options);
                this.init(this.chart);
            };
            /**
             * Render the navigator
             *
             * @private
             * @function Highcharts.Navigator#render
             * @param {number} min
             *        X axis value minimum
             * @param {number} max
             *        X axis value maximum
             * @param {number} [pxMin]
             *        Pixel value minimum
             * @param {number} [pxMax]
             *        Pixel value maximum
             */
            Navigator.prototype.render = function (min, max, pxMin, pxMax) {
                var navigator = this,
                    chart = navigator.chart,
                    xAxis = navigator.xAxis,
                    pointRange = xAxis.pointRange || 0,
                    scrollbarXAxis = xAxis.navigatorAxis.fake ? chart.xAxis[0] : xAxis,
                    navigatorEnabled = navigator.navigatorEnabled,
                    rendered = navigator.rendered,
                    inverted = chart.inverted,
                    minRange = chart.xAxis[0].minRange,
                    maxRange = chart.xAxis[0].options.maxRange;
                var navigatorWidth,
                    scrollbarLeft,
                    scrollbarTop,
                    scrollbarHeight = navigator.scrollbarHeight,
                    navigatorSize,
                    verb;
                // Don't redraw while moving the handles (#4703).
                if (this.hasDragged && !defined(pxMin)) {
                    return;
                }
                min = correctFloat(min - pointRange / 2);
                max = correctFloat(max + pointRange / 2);
                // Don't render the navigator until we have data (#486, #4202, #5172).
                if (!isNumber(min) || !isNumber(max)) {
                    // However, if navigator was already rendered, we may need to resize
                    // it. For example hidden series, but visible navigator (#6022).
                    if (rendered) {
                        pxMin = 0;
                        pxMax = pick(xAxis.width, scrollbarXAxis.width);
                    }
                    else {
                        return;
                    }
                }
                navigator.left = pick(xAxis.left, 
                // in case of scrollbar only, without navigator
                chart.plotLeft + scrollbarHeight +
                    (inverted ? chart.plotWidth : 0));
                var zoomedMax = navigator.size = navigatorSize = pick(xAxis.len, (inverted ? chart.plotHeight : chart.plotWidth) -
                        2 * scrollbarHeight);
                if (inverted) {
                    navigatorWidth = scrollbarHeight;
                }
                else {
                    navigatorWidth = navigatorSize + 2 * scrollbarHeight;
                }
                // Get the pixel position of the handles
                pxMin = pick(pxMin, xAxis.toPixels(min, true));
                pxMax = pick(pxMax, xAxis.toPixels(max, true));
                // Verify (#1851, #2238)
                if (!isNumber(pxMin) || Math.abs(pxMin) === Infinity) {
                    pxMin = 0;
                    pxMax = navigatorWidth;
                }
                // Are we below the minRange? (#2618, #6191)
                var newMin = xAxis.toValue(pxMin,
                    true),
                    newMax = xAxis.toValue(pxMax,
                    true),
                    currentRange = Math.abs(correctFloat(newMax - newMin));
                if (currentRange < minRange) {
                    if (this.grabbedLeft) {
                        pxMin = xAxis.toPixels(newMax - minRange - pointRange, true);
                    }
                    else if (this.grabbedRight) {
                        pxMax = xAxis.toPixels(newMin + minRange + pointRange, true);
                    }
                }
                else if (defined(maxRange) &&
                    correctFloat(currentRange - pointRange) > maxRange) {
                    if (this.grabbedLeft) {
                        pxMin = xAxis.toPixels(newMax - maxRange - pointRange, true);
                    }
                    else if (this.grabbedRight) {
                        pxMax = xAxis.toPixels(newMin + maxRange + pointRange, true);
                    }
                }
                // Handles are allowed to cross, but never exceed the plot area
                navigator.zoomedMax = clamp(Math.max(pxMin, pxMax), 0, zoomedMax);
                navigator.zoomedMin = clamp(navigator.fixedWidth ?
                    navigator.zoomedMax - navigator.fixedWidth :
                    Math.min(pxMin, pxMax), 0, zoomedMax);
                navigator.range = navigator.zoomedMax - navigator.zoomedMin;
                zoomedMax = Math.round(navigator.zoomedMax);
                var zoomedMin = Math.round(navigator.zoomedMin);
                if (navigatorEnabled) {
                    navigator.navigatorGroup.attr({
                        visibility: 'inherit'
                    });
                    // Place elements
                    verb = rendered && !navigator.hasDragged ? 'animate' : 'attr';
                    navigator.drawMasks(zoomedMin, zoomedMax, inverted, verb);
                    navigator.drawOutline(zoomedMin, zoomedMax, inverted, verb);
                    if (navigator.navigatorOptions.handles.enabled) {
                        navigator.drawHandle(zoomedMin, 0, inverted, verb);
                        navigator.drawHandle(zoomedMax, 1, inverted, verb);
                    }
                }
                if (navigator.scrollbar) {
                    if (inverted) {
                        scrollbarTop = navigator.top - scrollbarHeight;
                        scrollbarLeft = navigator.left - scrollbarHeight +
                            (navigatorEnabled || !scrollbarXAxis.opposite ? 0 :
                                // Multiple axes has offsets:
                                (scrollbarXAxis.titleOffset || 0) +
                                    // Self margin from the axis.title
                                    scrollbarXAxis.axisTitleMargin);
                        scrollbarHeight = navigatorSize + 2 * scrollbarHeight;
                    }
                    else {
                        scrollbarTop = navigator.top + (navigatorEnabled ?
                            navigator.height :
                            -scrollbarHeight);
                        scrollbarLeft = navigator.left - scrollbarHeight;
                    }
                    // Reposition scrollbar
                    navigator.scrollbar.position(scrollbarLeft, scrollbarTop, navigatorWidth, scrollbarHeight);
                    // Keep scale 0-1
                    navigator.scrollbar.setRange(
                    // Use real value, not rounded because range can be very small
                    // (#1716)
                    navigator.zoomedMin / (navigatorSize || 1), navigator.zoomedMax / (navigatorSize || 1));
                }
                navigator.rendered = true;
            };
            /**
             * Set up the mouse and touch events for the navigator
             *
             * @private
             * @function Highcharts.Navigator#addMouseEvents
             */
            Navigator.prototype.addMouseEvents = function () {
                var navigator = this,
                    chart = navigator.chart,
                    container = chart.container;
                var eventsToUnbind = [],
                    mouseMoveHandler,
                    mouseUpHandler;
                /**
                 * Create mouse events' handlers.
                 * Make them as separate functions to enable wrapping them:
                 */
                navigator.mouseMoveHandler = mouseMoveHandler = function (e) {
                    navigator.onMouseMove(e);
                };
                navigator.mouseUpHandler = mouseUpHandler = function (e) {
                    navigator.onMouseUp(e);
                };
                // Add shades and handles mousedown events
                eventsToUnbind = navigator.getPartsEvents('mousedown');
                // Add mouse move and mouseup events. These are bind to doc/container,
                // because Navigator.grabbedSomething flags are stored in mousedown
                // events
                eventsToUnbind.push(addEvent(chart.renderTo, 'mousemove', mouseMoveHandler), addEvent(container.ownerDocument, 'mouseup', mouseUpHandler));
                // Touch events
                if (hasTouch) {
                    eventsToUnbind.push(addEvent(chart.renderTo, 'touchmove', mouseMoveHandler), addEvent(container.ownerDocument, 'touchend', mouseUpHandler));
                    eventsToUnbind.concat(navigator.getPartsEvents('touchstart'));
                }
                navigator.eventsToUnbind = eventsToUnbind;
                // Data events
                if (navigator.series && navigator.series[0]) {
                    eventsToUnbind.push(addEvent(navigator.series[0].xAxis, 'foundExtremes', function () {
                        chart.navigator.modifyNavigatorAxisExtremes();
                    }));
                }
            };
            /**
             * Generate events for handles and masks
             *
             * @private
             * @function Highcharts.Navigator#getPartsEvents
             *
             * @param {string} eventName
             *        Event name handler, 'mousedown' or 'touchstart'
             *
             * @return {Array<Function>}
             *         An array of functions to remove navigator functions from the
             *         events again.
             */
            Navigator.prototype.getPartsEvents = function (eventName) {
                var navigator = this,
                    events = [];
                ['shades', 'handles'].forEach(function (name) {
                    navigator[name].forEach(function (navigatorItem, index) {
                        events.push(addEvent(navigatorItem.element, eventName, function (e) {
                            navigator[name + 'Mousedown'](e, index);
                        }));
                    });
                });
                return events;
            };
            /**
             * Mousedown on a shaded mask, either:
             *
             * - will be stored for future drag&drop
             *
             * - will directly shift to a new range
             *
             * @private
             * @function Highcharts.Navigator#shadesMousedown
             *
             * @param {Highcharts.PointerEventObject} e
             *        Mouse event
             *
             * @param {number} index
             *        Index of a mask in Navigator.shades array
             */
            Navigator.prototype.shadesMousedown = function (e, index) {
                e = this.chart.pointer.normalize(e);
                var navigator = this,
                    chart = navigator.chart,
                    xAxis = navigator.xAxis,
                    zoomedMin = navigator.zoomedMin,
                    navigatorSize = navigator.size,
                    range = navigator.range;
                var navigatorPosition = navigator.left,
                    chartX = e.chartX,
                    fixedMax,
                    fixedMin,
                    ext,
                    left;
                // For inverted chart, swap some options:
                if (chart.inverted) {
                    chartX = e.chartY;
                    navigatorPosition = navigator.top;
                }
                if (index === 1) {
                    // Store information for drag&drop
                    navigator.grabbedCenter = chartX;
                    navigator.fixedWidth = range;
                    navigator.dragOffset = chartX - zoomedMin;
                }
                else {
                    // Shift the range by clicking on shaded areas
                    left = chartX - navigatorPosition - range / 2;
                    if (index === 0) {
                        left = Math.max(0, left);
                    }
                    else if (index === 2 && left + range >= navigatorSize) {
                        left = navigatorSize - range;
                        if (navigator.reversedExtremes) {
                            // #7713
                            left -= range;
                            fixedMin = navigator.getUnionExtremes().dataMin;
                        }
                        else {
                            // #2293, #3543
                            fixedMax = navigator.getUnionExtremes().dataMax;
                        }
                    }
                    if (left !== zoomedMin) { // it has actually moved
                        navigator.fixedWidth = range; // #1370
                        ext = xAxis.navigatorAxis.toFixedRange(left, left + range, fixedMin, fixedMax);
                        if (defined(ext.min)) { // #7411
                            chart.xAxis[0].setExtremes(Math.min(ext.min, ext.max), Math.max(ext.min, ext.max), true, null, // auto animation
                            { trigger: 'navigator' });
                        }
                    }
                }
            };
            /**
             * Mousedown on a handle mask.
             * Will store necessary information for drag&drop.
             *
             * @private
             * @function Highcharts.Navigator#handlesMousedown
             * @param {Highcharts.PointerEventObject} e
             *        Mouse event
             * @param {number} index
             *        Index of a handle in Navigator.handles array
             */
            Navigator.prototype.handlesMousedown = function (e, index) {
                e = this.chart.pointer.normalize(e);
                var navigator = this,
                    chart = navigator.chart,
                    baseXAxis = chart.xAxis[0], 
                    // For reversed axes, min and max are changed,
                    // so the other extreme should be stored
                    reverse = navigator.reversedExtremes;
                if (index === 0) {
                    // Grab the left handle
                    navigator.grabbedLeft = true;
                    navigator.otherHandlePos = navigator.zoomedMax;
                    navigator.fixedExtreme = reverse ? baseXAxis.min : baseXAxis.max;
                }
                else {
                    // Grab the right handle
                    navigator.grabbedRight = true;
                    navigator.otherHandlePos = navigator.zoomedMin;
                    navigator.fixedExtreme = reverse ? baseXAxis.max : baseXAxis.min;
                }
                chart.fixedRange = null;
            };
            /**
             * Mouse move event based on x/y mouse position.
             *
             * @private
             * @function Highcharts.Navigator#onMouseMove
             *
             * @param {Highcharts.PointerEventObject} e
             *        Mouse event
             */
            Navigator.prototype.onMouseMove = function (e) {
                var navigator = this,
                    chart = navigator.chart,
                    navigatorSize = navigator.navigatorSize,
                    range = navigator.range,
                    dragOffset = navigator.dragOffset,
                    inverted = chart.inverted;
                var left = navigator.left,
                    chartX;
                // In iOS, a mousemove event with e.pageX === 0 is fired when holding
                // the finger down in the center of the scrollbar. This should be
                // ignored.
                if (!e.touches || e.touches[0].pageX !== 0) { // #4696
                    e = chart.pointer.normalize(e);
                    chartX = e.chartX;
                    // Swap some options for inverted chart
                    if (inverted) {
                        left = navigator.top;
                        chartX = e.chartY;
                    }
                    // Drag left handle or top handle
                    if (navigator.grabbedLeft) {
                        navigator.hasDragged = true;
                        navigator.render(0, 0, chartX - left, navigator.otherHandlePos);
                        // Drag right handle or bottom handle
                    }
                    else if (navigator.grabbedRight) {
                        navigator.hasDragged = true;
                        navigator.render(0, 0, navigator.otherHandlePos, chartX - left);
                        // Drag scrollbar or open area in navigator
                    }
                    else if (navigator.grabbedCenter) {
                        navigator.hasDragged = true;
                        if (chartX < dragOffset) { // outside left
                            chartX = dragOffset;
                            // outside right
                        }
                        else if (chartX >
                            navigatorSize + dragOffset - range) {
                            chartX = navigatorSize + dragOffset - range;
                        }
                        navigator.render(0, 0, chartX - dragOffset, chartX - dragOffset + range);
                    }
                    if (navigator.hasDragged &&
                        navigator.scrollbar &&
                        pick(navigator.scrollbar.options.liveRedraw, 
                        // By default, don't run live redraw on VML, on touch
                        // devices or if the chart is in boost.
                        H.svg &&
                            !isTouchDevice &&
                            !this.chart.boosted)) {
                        e.DOMType = e.type; // DOMType is for IE8
                        setTimeout(function () {
                            navigator.onMouseUp(e);
                        }, 0);
                    }
                }
            };
            /**
             * Mouse up event based on x/y mouse position.
             *
             * @private
             * @function Highcharts.Navigator#onMouseUp
             * @param {Highcharts.PointerEventObject} e
             *        Mouse event
             */
            Navigator.prototype.onMouseUp = function (e) {
                var navigator = this,
                    chart = navigator.chart,
                    xAxis = navigator.xAxis,
                    scrollbar = navigator.scrollbar,
                    DOMEvent = e.DOMEvent || e,
                    inverted = chart.inverted,
                    verb = navigator.rendered && !navigator.hasDragged ?
                        'animate' : 'attr';
                var zoomedMax,
                    zoomedMin,
                    unionExtremes,
                    fixedMin,
                    fixedMax,
                    ext;
                if (
                // MouseUp is called for both, navigator and scrollbar (that order),
                // which causes calling afterSetExtremes twice. Prevent first call
                // by checking if scrollbar is going to set new extremes (#6334)
                (navigator.hasDragged && (!scrollbar || !scrollbar.hasDragged)) ||
                    e.trigger === 'scrollbar') {
                    unionExtremes = navigator.getUnionExtremes();
                    // When dragging one handle, make sure the other one doesn't change
                    if (navigator.zoomedMin === navigator.otherHandlePos) {
                        fixedMin = navigator.fixedExtreme;
                    }
                    else if (navigator.zoomedMax === navigator.otherHandlePos) {
                        fixedMax = navigator.fixedExtreme;
                    }
                    // Snap to right edge (#4076)
                    if (navigator.zoomedMax === navigator.size) {
                        fixedMax = navigator.reversedExtremes ?
                            unionExtremes.dataMin :
                            unionExtremes.dataMax;
                    }
                    // Snap to left edge (#7576)
                    if (navigator.zoomedMin === 0) {
                        fixedMin = navigator.reversedExtremes ?
                            unionExtremes.dataMax :
                            unionExtremes.dataMin;
                    }
                    ext = xAxis.navigatorAxis.toFixedRange(navigator.zoomedMin, navigator.zoomedMax, fixedMin, fixedMax);
                    if (defined(ext.min)) {
                        chart.xAxis[0].setExtremes(Math.min(ext.min, ext.max), Math.max(ext.min, ext.max), true, 
                        // Run animation when clicking buttons, scrollbar track etc,
                        // but not when dragging handles or scrollbar
                        navigator.hasDragged ? false : null, {
                            trigger: 'navigator',
                            triggerOp: 'navigator-drag',
                            DOMEvent: DOMEvent // #1838
                        });
                    }
                }
                if (e.DOMType !== 'mousemove' &&
                    e.DOMType !== 'touchmove') {
                    navigator.grabbedLeft = navigator.grabbedRight =
                        navigator.grabbedCenter = navigator.fixedWidth =
                            navigator.fixedExtreme = navigator.otherHandlePos =
                                navigator.hasDragged = navigator.dragOffset = null;
                }
                // Update position of navigator shades, outline and handles (#12573)
                if (navigator.navigatorEnabled &&
                    isNumber(navigator.zoomedMin) &&
                    isNumber(navigator.zoomedMax)) {
                    zoomedMin = Math.round(navigator.zoomedMin);
                    zoomedMax = Math.round(navigator.zoomedMax);
                    if (navigator.shades) {
                        navigator.drawMasks(zoomedMin, zoomedMax, inverted, verb);
                    }
                    if (navigator.outline) {
                        navigator.drawOutline(zoomedMin, zoomedMax, inverted, verb);
                    }
                    if (navigator.navigatorOptions.handles.enabled &&
                        Object.keys(navigator.handles).length ===
                            navigator.handles.length) {
                        navigator.drawHandle(zoomedMin, 0, inverted, verb);
                        navigator.drawHandle(zoomedMax, 1, inverted, verb);
                    }
                }
            };
            /**
             * Removes the event handlers attached previously with addEvents.
             *
             * @private
             * @function Highcharts.Navigator#removeEvents
             */
            Navigator.prototype.removeEvents = function () {
                if (this.eventsToUnbind) {
                    this.eventsToUnbind.forEach(function (unbind) {
                        unbind();
                    });
                    this.eventsToUnbind = void 0;
                }
                this.removeBaseSeriesEvents();
            };
            /**
             * Remove data events.
             *
             * @private
             * @function Highcharts.Navigator#removeBaseSeriesEvents
             */
            Navigator.prototype.removeBaseSeriesEvents = function () {
                var baseSeries = this.baseSeries || [];
                if (this.navigatorEnabled && baseSeries[0]) {
                    if (this.navigatorOptions.adaptToUpdatedData !== false) {
                        baseSeries.forEach(function (series) {
                            removeEvent(series, 'updatedData', this.updatedDataHandler);
                        }, this);
                    }
                    // We only listen for extremes-events on the first baseSeries
                    if (baseSeries[0].xAxis) {
                        removeEvent(baseSeries[0].xAxis, 'foundExtremes', this.modifyBaseAxisExtremes);
                    }
                }
            };
            /**
             * Initialize the Navigator object
             *
             * @private
             * @function Highcharts.Navigator#init
             */
            Navigator.prototype.init = function (chart) {
                var chartOptions = chart.options,
                    navigatorOptions = chartOptions.navigator || {},
                    navigatorEnabled = navigatorOptions.enabled,
                    scrollbarOptions = chartOptions.scrollbar || {},
                    scrollbarEnabled = scrollbarOptions.enabled,
                    height = navigatorEnabled && navigatorOptions.height || 0,
                    scrollbarHeight = scrollbarEnabled && scrollbarOptions.height || 0;
                this.handles = [];
                this.shades = [];
                this.chart = chart;
                this.setBaseSeries();
                this.height = height;
                this.scrollbarHeight = scrollbarHeight;
                this.scrollbarEnabled = scrollbarEnabled;
                this.navigatorEnabled = navigatorEnabled;
                this.navigatorOptions = navigatorOptions;
                this.scrollbarOptions = scrollbarOptions;
                this.outlineHeight = height + scrollbarHeight;
                this.opposite = pick(navigatorOptions.opposite, Boolean(!navigatorEnabled && chart.inverted)); // #6262
                var navigator = this,
                    baseSeries = navigator.baseSeries,
                    xAxisIndex = chart.xAxis.length,
                    yAxisIndex = chart.yAxis.length,
                    baseXaxis = baseSeries && baseSeries[0] && baseSeries[0].xAxis ||
                        chart.xAxis[0] || { options: {} };
                chart.isDirtyBox = true;
                if (navigator.navigatorEnabled) {
                    // an x axis is required for scrollbar also
                    navigator.xAxis = new Axis(chart, merge({
                        // inherit base xAxis' break and ordinal options
                        breaks: baseXaxis.options.breaks,
                        ordinal: baseXaxis.options.ordinal
                    }, navigatorOptions.xAxis, {
                        id: 'navigator-x-axis',
                        yAxis: 'navigator-y-axis',
                        isX: true,
                        type: 'datetime',
                        index: xAxisIndex,
                        isInternal: true,
                        offset: 0,
                        keepOrdinalPadding: true,
                        startOnTick: false,
                        endOnTick: false,
                        minPadding: 0,
                        maxPadding: 0,
                        zoomEnabled: false
                    }, chart.inverted ? {
                        offsets: [scrollbarHeight, 0, -scrollbarHeight, 0],
                        width: height
                    } : {
                        offsets: [0, -scrollbarHeight, 0, scrollbarHeight],
                        height: height
                    }));
                    navigator.yAxis = new Axis(chart, merge(navigatorOptions.yAxis, {
                        id: 'navigator-y-axis',
                        alignTicks: false,
                        offset: 0,
                        index: yAxisIndex,
                        isInternal: true,
                        reversed: pick((navigatorOptions.yAxis &&
                            navigatorOptions.yAxis.reversed), (chart.yAxis[0] && chart.yAxis[0].reversed), false),
                        zoomEnabled: false
                    }, chart.inverted ? {
                        width: height
                    } : {
                        height: height
                    }));
                    // If we have a base series, initialize the navigator series
                    if (baseSeries || navigatorOptions.series.data) {
                        navigator.updateNavigatorSeries(false);
                        // If not, set up an event to listen for added series
                    }
                    else if (chart.series.length === 0) {
                        navigator.unbindRedraw = addEvent(chart, 'beforeRedraw', function () {
                            // We've got one, now add it as base
                            if (chart.series.length > 0 && !navigator.series) {
                                navigator.setBaseSeries();
                                navigator.unbindRedraw(); // reset
                            }
                        });
                    }
                    navigator.reversedExtremes = (chart.inverted && !navigator.xAxis.reversed) || (!chart.inverted && navigator.xAxis.reversed);
                    // Render items, so we can bind events to them:
                    navigator.renderElements();
                    // Add mouse events
                    navigator.addMouseEvents();
                    // in case of scrollbar only, fake an x axis to get translation
                }
                else {
                    navigator.xAxis = {
                        chart: chart,
                        navigatorAxis: {
                            fake: true
                        },
                        translate: function (value, reverse) {
                            var axis = chart.xAxis[0], ext = axis.getExtremes(), scrollTrackWidth = axis.len - 2 * scrollbarHeight, min = numExt('min', axis.options.min, ext.dataMin), valueRange = numExt('max', axis.options.max, ext.dataMax) - min;
                            return reverse ?
                                // from pixel to value
                                (value * valueRange / scrollTrackWidth) + min :
                                // from value to pixel
                                scrollTrackWidth * (value - min) / valueRange;
                        },
                        toPixels: function (value) {
                            return this.translate(value);
                        },
                        toValue: function (value) {
                            return this.translate(value, true);
                        }
                    };
                    navigator.xAxis.navigatorAxis.axis = navigator.xAxis;
                    navigator.xAxis.navigatorAxis.toFixedRange = (NavigatorAxisAdditions.prototype.toFixedRange.bind(navigator.xAxis.navigatorAxis));
                }
                // Initialize the scrollbar
                if (chart.options.scrollbar.enabled) {
                    chart.scrollbar = navigator.scrollbar = new Scrollbar(chart.renderer, merge(chart.options.scrollbar, {
                        margin: navigator.navigatorEnabled ? 0 : 10,
                        vertical: chart.inverted
                    }), chart);
                    addEvent(navigator.scrollbar, 'changed', function (e) {
                        var range = navigator.size,
                            to = range * this.to,
                            from = range * this.from;
                        navigator.hasDragged = navigator.scrollbar.hasDragged;
                        navigator.render(0, 0, from, to);
                        if (this.shouldUpdateExtremes(e.DOMType)) {
                            setTimeout(function () {
                                navigator.onMouseUp(e);
                            });
                        }
                    });
                }
                // Add data events
                navigator.addBaseSeriesEvents();
                // Add redraw events
                navigator.addChartEvents();
            };
            /**
             * Get the union data extremes of the chart - the outer data extremes of the
             * base X axis and the navigator axis.
             *
             * @private
             * @function Highcharts.Navigator#getUnionExtremes
             */
            Navigator.prototype.getUnionExtremes = function (returnFalseOnNoBaseSeries) {
                var baseAxis = this.chart.xAxis[0],
                    navAxis = this.xAxis,
                    navAxisOptions = navAxis.options,
                    baseAxisOptions = baseAxis.options;
                var ret;
                if (!returnFalseOnNoBaseSeries || baseAxis.dataMin !== null) {
                    ret = {
                        dataMin: pick(// #4053
                        navAxisOptions && navAxisOptions.min, numExt('min', baseAxisOptions.min, baseAxis.dataMin, navAxis.dataMin, navAxis.min)),
                        dataMax: pick(navAxisOptions && navAxisOptions.max, numExt('max', baseAxisOptions.max, baseAxis.dataMax, navAxis.dataMax, navAxis.max))
                    };
                }
                return ret;
            };
            /**
             * Set the base series and update the navigator series from this. With a bit
             * of modification we should be able to make this an API method to be called
             * from the outside
             *
             * @private
             * @function Highcharts.Navigator#setBaseSeries
             * @param {Highcharts.SeriesOptionsType} [baseSeriesOptions]
             *        Additional series options for a navigator
             * @param {boolean} [redraw]
             *        Whether to redraw after update.
             */
            Navigator.prototype.setBaseSeries = function (baseSeriesOptions, redraw) {
                var chart = this.chart,
                    baseSeries = this.baseSeries = [];
                baseSeriesOptions = (baseSeriesOptions ||
                    chart.options && chart.options.navigator.baseSeries ||
                    (chart.series.length ?
                        // Find the first non-navigator series (#8430)
                        find(chart.series, function (s) { return (!s.options.isInternal); }).index :
                        0));
                // Iterate through series and add the ones that should be shown in
                // navigator.
                (chart.series || []).forEach(function (series, i) {
                    if (
                    // Don't include existing nav series
                    !series.options.isInternal &&
                        (series.options.showInNavigator ||
                            (i === baseSeriesOptions ||
                                series.options.id === baseSeriesOptions) &&
                                series.options.showInNavigator !== false)) {
                        baseSeries.push(series);
                    }
                });
                // When run after render, this.xAxis already exists
                if (this.xAxis && !this.xAxis.navigatorAxis.fake) {
                    this.updateNavigatorSeries(true, redraw);
                }
            };
            /**
             * Update series in the navigator from baseSeries, adding new if does not
             * exist.
             *
             * @private
             * @function Highcharts.Navigator.updateNavigatorSeries
             */
            Navigator.prototype.updateNavigatorSeries = function (addEvents, redraw) {
                var navigator = this,
                    chart = navigator.chart,
                    baseSeries = navigator.baseSeries,
                    navSeriesMixin = {
                        enableMouseTracking: false,
                        index: null,
                        linkedTo: null,
                        group: 'nav',
                        padXAxis: false,
                        xAxis: 'navigator-x-axis',
                        yAxis: 'navigator-y-axis',
                        showInLegend: false,
                        stacking: void 0,
                        isInternal: true,
                        states: {
                            inactive: {
                                opacity: 1
                            }
                        }
                    }, 
                    // Remove navigator series that are no longer in the baseSeries
                    navigatorSeries = navigator.series =
                        (navigator.series || []).filter(function (navSeries) {
                            var base = navSeries.baseSeries;
                        if (baseSeries.indexOf(base) < 0) { // Not in array
                            // If there is still a base series connected to this
                            // series, remove event handler and reference.
                            if (base) {
                                removeEvent(base, 'updatedData', navigator.updatedDataHandler);
                                delete base.navigatorSeries;
                            }
                            // Kill the nav series. It may already have been
                            // destroyed (#8715).
                            if (navSeries.chart) {
                                navSeries.destroy();
                            }
                            return false;
                        }
                        return true;
                    });
                var baseOptions,
                    mergedNavSeriesOptions,
                    chartNavigatorSeriesOptions = navigator.navigatorOptions.series,
                    baseNavigatorOptions;
                // Go through each base series and merge the options to create new
                // series
                if (baseSeries && baseSeries.length) {
                    baseSeries.forEach(function (base) {
                        var linkedNavSeries = base.navigatorSeries,
                            userNavOptions = extend(
                            // Grab color and visibility from base as default
                            {
                                color: base.color,
                                visible: base.visible
                            }, !isArray(chartNavigatorSeriesOptions) ?
                                chartNavigatorSeriesOptions :
                                defaultOptions.navigator.series);
                        // Don't update if the series exists in nav and we have disabled
                        // adaptToUpdatedData.
                        if (linkedNavSeries &&
                            navigator.navigatorOptions.adaptToUpdatedData === false) {
                            return;
                        }
                        navSeriesMixin.name = 'Navigator ' + baseSeries.length;
                        baseOptions = base.options || {};
                        baseNavigatorOptions = baseOptions.navigatorOptions || {};
                        // The dataLabels options are not merged correctly
                        // if the settings are an array, #13847.
                        userNavOptions.dataLabels = splat(userNavOptions.dataLabels);
                        mergedNavSeriesOptions = merge(baseOptions, navSeriesMixin, userNavOptions, baseNavigatorOptions);
                        // Once nav series type is resolved, pick correct pointRange
                        mergedNavSeriesOptions.pointRange = pick(
                        // Stricte set pointRange in options
                        userNavOptions.pointRange, baseNavigatorOptions.pointRange, 
                        // Fallback to default values, e.g. `null` for column
                        defaultOptions.plotOptions[mergedNavSeriesOptions.type || 'line'].pointRange);
                        // Merge data separately. Do a slice to avoid mutating the
                        // navigator options from base series (#4923).
                        var navigatorSeriesData = baseNavigatorOptions.data || userNavOptions.data;
                        navigator.hasNavigatorData =
                            navigator.hasNavigatorData || !!navigatorSeriesData;
                        mergedNavSeriesOptions.data =
                            navigatorSeriesData ||
                                baseOptions.data && baseOptions.data.slice(0);
                        // Update or add the series
                        if (linkedNavSeries && linkedNavSeries.options) {
                            linkedNavSeries.update(mergedNavSeriesOptions, redraw);
                        }
                        else {
                            base.navigatorSeries = chart.initSeries(mergedNavSeriesOptions);
                            base.navigatorSeries.baseSeries = base; // Store ref
                            navigatorSeries.push(base.navigatorSeries);
                        }
                    });
                }
                // If user has defined data (and no base series) or explicitly defined
                // navigator.series as an array, we create these series on top of any
                // base series.
                if (chartNavigatorSeriesOptions.data &&
                    !(baseSeries && baseSeries.length) ||
                    isArray(chartNavigatorSeriesOptions)) {
                    navigator.hasNavigatorData = false;
                    // Allow navigator.series to be an array
                    chartNavigatorSeriesOptions =
                        splat(chartNavigatorSeriesOptions);
                    chartNavigatorSeriesOptions.forEach(function (userSeriesOptions, i) {
                        navSeriesMixin.name =
                            'Navigator ' + (navigatorSeries.length + 1);
                        mergedNavSeriesOptions = merge(defaultOptions.navigator.series, {
                            // Since we don't have a base series to pull color from,
                            // try to fake it by using color from series with same
                            // index. Otherwise pull from the colors array. We need
                            // an explicit color as otherwise updates will increment
                            // color counter and we'll get a new color for each
                            // update of the nav series.
                            color: chart.series[i] &&
                                !chart.series[i].options.isInternal &&
                                chart.series[i].color ||
                                chart.options.colors[i] ||
                                chart.options.colors[0]
                        }, navSeriesMixin, userSeriesOptions);
                        mergedNavSeriesOptions.data = userSeriesOptions.data;
                        if (mergedNavSeriesOptions.data) {
                            navigator.hasNavigatorData = true;
                            navigatorSeries.push(chart.initSeries(mergedNavSeriesOptions));
                        }
                    });
                }
                if (addEvents) {
                    this.addBaseSeriesEvents();
                }
            };
            /**
             * Add data events.
             * For example when main series is updated we need to recalculate extremes
             *
             * @private
             * @function Highcharts.Navigator#addBaseSeriesEvent
             */
            Navigator.prototype.addBaseSeriesEvents = function () {
                var _this = this;
                var navigator = this,
                    baseSeries = navigator.baseSeries || [];
                // Bind modified extremes event to first base's xAxis only.
                // In event of > 1 base-xAxes, the navigator will ignore those.
                // Adding this multiple times to the same axis is no problem, as
                // duplicates should be discarded by the browser.
                if (baseSeries[0] && baseSeries[0].xAxis) {
                    baseSeries[0].eventsToUnbind.push(addEvent(baseSeries[0].xAxis, 'foundExtremes', this.modifyBaseAxisExtremes));
                }
                baseSeries.forEach(function (base) {
                    // Link base series show/hide to navigator series visibility
                    base.eventsToUnbind.push(addEvent(base, 'show', function () {
                        if (this.navigatorSeries) {
                            this.navigatorSeries.setVisible(true, false);
                        }
                    }));
                    base.eventsToUnbind.push(addEvent(base, 'hide', function () {
                        if (this.navigatorSeries) {
                            this.navigatorSeries.setVisible(false, false);
                        }
                    }));
                    // Respond to updated data in the base series, unless explicitily
                    // not adapting to data changes.
                    if (_this.navigatorOptions.adaptToUpdatedData !== false) {
                        if (base.xAxis) {
                            base.eventsToUnbind.push(addEvent(base, 'updatedData', _this.updatedDataHandler));
                        }
                    }
                    // Handle series removal
                    base.eventsToUnbind.push(addEvent(base, 'remove', function () {
                        if (this.navigatorSeries) {
                            erase(navigator.series, this.navigatorSeries);
                            if (defined(this.navigatorSeries.options)) {
                                this.navigatorSeries.remove(false);
                            }
                            delete this.navigatorSeries;
                        }
                    }));
                });
            };
            /**
             * Get minimum from all base series connected to the navigator
             * @private
             * @param {number} currentSeriesMin
             *        Minium from the current series
             * @return {number}
             *         Minimum from all series
             */
            Navigator.prototype.getBaseSeriesMin = function (currentSeriesMin) {
                return this.baseSeries.reduce(function (min, series) {
                    // (#10193)
                    return Math.min(min, series.xData && series.xData.length ?
                        series.xData[0] : min);
                }, currentSeriesMin);
            };
            /**
             * Set the navigator x axis extremes to reflect the total. The navigator
             * extremes should always be the extremes of the union of all series in the
             * chart as well as the navigator series.
             *
             * @private
             * @function Highcharts.Navigator#modifyNavigatorAxisExtremes
             */
            Navigator.prototype.modifyNavigatorAxisExtremes = function () {
                var xAxis = this.xAxis;
                if (typeof xAxis.getExtremes !== 'undefined') {
                    var unionExtremes = this.getUnionExtremes(true);
                    if (unionExtremes &&
                        (unionExtremes.dataMin !== xAxis.min ||
                            unionExtremes.dataMax !== xAxis.max)) {
                        xAxis.min = unionExtremes.dataMin;
                        xAxis.max = unionExtremes.dataMax;
                    }
                }
            };
            /**
             * Hook to modify the base axis extremes with information from the Navigator
             *
             * @private
             * @function Highcharts.Navigator#modifyBaseAxisExtremes
             */
            Navigator.prototype.modifyBaseAxisExtremes = function () {
                var baseXAxis = this,
                    navigator = baseXAxis.chart.navigator,
                    baseExtremes = baseXAxis.getExtremes(),
                    baseMin = baseExtremes.min,
                    baseMax = baseExtremes.max,
                    baseDataMin = baseExtremes.dataMin,
                    baseDataMax = baseExtremes.dataMax,
                    range = baseMax - baseMin,
                    stickToMin = navigator.stickToMin,
                    stickToMax = navigator.stickToMax,
                    overscroll = pick(baseXAxis.options.overscroll, 0),
                    navigatorSeries = navigator.series && navigator.series[0],
                    hasSetExtremes = !!baseXAxis.setExtremes, 
                    // When the extremes have been set by range selector button, don't
                    // stick to min or max. The range selector buttons will handle the
                    // extremes. (#5489)
                    unmutable = baseXAxis.eventArgs &&
                        baseXAxis.eventArgs.trigger === 'rangeSelectorButton';
                var newMax,
                    newMin;
                if (!unmutable) {
                    // If the zoomed range is already at the min, move it to the right
                    // as new data comes in
                    if (stickToMin) {
                        newMin = baseDataMin;
                        newMax = newMin + range;
                    }
                    // If the zoomed range is already at the max, move it to the right
                    // as new data comes in
                    if (stickToMax) {
                        newMax = baseDataMax + overscroll;
                        // If stickToMin is true, the new min value is set above
                        if (!stickToMin) {
                            newMin = Math.max(baseDataMin, // don't go below data extremes (#13184)
                            newMax - range, navigator.getBaseSeriesMin(navigatorSeries && navigatorSeries.xData ?
                                navigatorSeries.xData[0] :
                                -Number.MAX_VALUE));
                        }
                    }
                    // Update the extremes
                    if (hasSetExtremes && (stickToMin || stickToMax)) {
                        if (isNumber(newMin)) {
                            baseXAxis.min = baseXAxis.userMin = newMin;
                            baseXAxis.max = baseXAxis.userMax = newMax;
                        }
                    }
                }
                // Reset
                navigator.stickToMin =
                    navigator.stickToMax = null;
            };
            /**
             * Handler for updated data on the base series. When data is modified, the
             * navigator series must reflect it. This is called from the Chart.redraw
             * function before axis and series extremes are computed.
             *
             * @private
             * @function Highcharts.Navigator#updateDataHandler
             */
            Navigator.prototype.updatedDataHandler = function () {
                var navigator = this.chart.navigator,
                    baseSeries = this,
                    navigatorSeries = this.navigatorSeries,
                    shouldStickToMax = navigator.reversedExtremes ?
                        Math.round(navigator.zoomedMin) === 0 :
                        Math.round(navigator.zoomedMax) >= Math.round(navigator.size);
                // If the scrollbar is scrolled all the way to the right, keep right as
                // new data comes in, unless user set navigator.stickToMax to false.
                navigator.stickToMax = pick(this.chart.options.navigator &&
                    this.chart.options.navigator.stickToMax, shouldStickToMax);
                navigator.stickToMin = navigator.shouldStickToMin(baseSeries, navigator);
                // Set the navigator series data to the new data of the base series
                if (navigatorSeries && !navigator.hasNavigatorData) {
                    navigatorSeries.options.pointStart = baseSeries.xData[0];
                    navigatorSeries.setData(baseSeries.options.data, false, null, false); // #5414
                }
            };
            /**
             * Detect if the zoomed area should stick to the minimum, #14742.
             *
             * @private
             * @function Highcharts.Navigator#shouldStickToMin
             */
            Navigator.prototype.shouldStickToMin = function (baseSeries, navigator) {
                var xDataMin = navigator.getBaseSeriesMin(baseSeries.xData[0]),
                    xAxis = baseSeries.xAxis,
                    max = xAxis.max,
                    min = xAxis.min,
                    range = xAxis.options.range;
                var stickToMin = true;
                if (isNumber(max) && isNumber(min)) {
                    // If range declared, stick to the minimum only if the range
                    // is smaller than the data set range.
                    if (range && max - xDataMin > 0) {
                        stickToMin = max - xDataMin < range;
                    }
                    else {
                        // If the current axis minimum falls outside the new
                        // updated dataset, we must adjust.
                        stickToMin = min <= xDataMin;
                    }
                }
                else {
                    stickToMin = false; // #15864
                }
                return stickToMin;
            };
            /**
             * Add chart events, like redrawing navigator, when chart requires that.
             *
             * @private
             * @function Highcharts.Navigator#addChartEvents
             */
            Navigator.prototype.addChartEvents = function () {
                if (!this.eventsToUnbind) {
                    this.eventsToUnbind = [];
                }
                this.eventsToUnbind.push(
                // Move the scrollbar after redraw, like after data updata even if
                // axes don't redraw
                addEvent(this.chart, 'redraw', function () {
                    var navigator = this.navigator,
                        xAxis = navigator && (navigator.baseSeries &&
                            navigator.baseSeries[0] &&
                            navigator.baseSeries[0].xAxis ||
                            this.xAxis[0]); // #5709, #13114
                        if (xAxis) {
                            navigator.render(xAxis.min,
                        xAxis.max);
                    }
                }), 
                // Make room for the navigator, can be placed around the chart:
                addEvent(this.chart, 'getMargins', function () {
                    var chart = this,
                        navigator = chart.navigator,
                        marginName = navigator.opposite ?
                            'plotTop' : 'marginBottom';
                    if (chart.inverted) {
                        marginName = navigator.opposite ?
                            'marginRight' : 'plotLeft';
                    }
                    chart[marginName] =
                        (chart[marginName] || 0) + (navigator.navigatorEnabled || !chart.inverted ?
                            navigator.outlineHeight :
                            0) + navigator.navigatorOptions.margin;
                }));
            };
            /**
             * Destroys allocated elements.
             *
             * @private
             * @function Highcharts.Navigator#destroy
             */
            Navigator.prototype.destroy = function () {
                var _this = this;
                // Disconnect events added in addEvents
                this.removeEvents();
                if (this.xAxis) {
                    erase(this.chart.xAxis, this.xAxis);
                    erase(this.chart.axes, this.xAxis);
                }
                if (this.yAxis) {
                    erase(this.chart.yAxis, this.yAxis);
                    erase(this.chart.axes, this.yAxis);
                }
                // Destroy series
                (this.series || []).forEach(function (s) {
                    if (s.destroy) {
                        s.destroy();
                    }
                });
                // Destroy properties
                [
                    'series', 'xAxis', 'yAxis', 'shades', 'outline', 'scrollbarTrack',
                    'scrollbarRifles', 'scrollbarGroup', 'scrollbar', 'navigatorGroup',
                    'rendered'
                ].forEach(function (prop) {
                    if (_this[prop] && _this[prop].destroy) {
                        _this[prop].destroy();
                    }
                    _this[prop] = null;
                });
                // Destroy elements in collection
                [this.handles].forEach(function (coll) {
                    destroyObjectProperties(coll);
                });
            };
            return Navigator;
        }());
        /* *
         *
         *  Default Export
         *
         * */

        return Navigator;
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
    _registerModule(_modules, 'Core/Axis/OrdinalAxis.js', [_modules['Core/Axis/Axis.js'], _modules['Core/Globals.js'], _modules['Core/Series/Series.js'], _modules['Core/Utilities.js']], function (Axis, H, Series, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var addEvent = U.addEvent,
            correctFloat = U.correctFloat,
            css = U.css,
            defined = U.defined,
            error = U.error,
            pick = U.pick,
            timeUnits = U.timeUnits;
        /* *
         *
         *  Constants
         *
         * */
        var composedClasses = [];
        /* eslint-disable valid-jsdoc */
        /* *
         *
         *  Composition
         *
         * */
        /**
         * Extends the axis with ordinal support.
         * @private
         */
        var OrdinalAxis;
        (function (OrdinalAxis) {
            /* *
             *
             *  Declarations
             *
             * */
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Extends the axis with ordinal support.
             *
             * @private
             *
             * @param AxisClass
             * Axis class to extend.
             *
             * @param ChartClass
             * Chart class to use.
             *
             * @param SeriesClass
             * Series class to use.
             */
            function compose(AxisClass, SeriesClass, ChartClass) {
                if (composedClasses.indexOf(AxisClass) === -1) {
                    composedClasses.push(AxisClass);
                    var axisProto = AxisClass.prototype;
                    axisProto.getTimeTicks = getTimeTicks;
                    axisProto.index2val = index2val;
                    axisProto.lin2val = lin2val;
                    axisProto.val2lin = val2lin;
                    // Record this to prevent overwriting by broken-axis module (#5979)
                    axisProto.ordinal2lin = axisProto.val2lin;
                    addEvent(AxisClass, 'afterInit', onAxisAfterInit);
                    addEvent(AxisClass, 'foundExtremes', onAxisFoundExtremes);
                    addEvent(AxisClass, 'afterSetScale', onAxisAfterSetScale);
                    addEvent(AxisClass, 'initialAxisTranslation', onAxisInitialAxisTranslation);
                }
                if (composedClasses.indexOf(ChartClass) === -1) {
                    composedClasses.push(ChartClass);
                    addEvent(ChartClass, 'pan', onChartPan);
                }
                if (composedClasses.indexOf(SeriesClass) === -1) {
                    composedClasses.push(SeriesClass);
                    addEvent(SeriesClass, 'updatedData', onSeriesUpdatedData);
                }
                /* eslint-enable no-invalid-this */
                return AxisClass;
            }
            OrdinalAxis.compose = compose;
            /**
             * In an ordinal axis, there might be areas with dense consentrations of
             * points, then large gaps between some. Creating equally distributed
             * ticks over this entire range may lead to a huge number of ticks that
             * will later be removed. So instead, break the positions up in
             * segments, find the tick positions for each segment then concatenize
             * them. This method is used from both data grouping logic and X axis
             * tick position logic.
             * @private
             */
            function getTimeTicks(normalizedInterval, min, max, startOfWeek, positions, closestDistance, findHigherRanks) {
                if (positions === void 0) { positions = []; }
                if (closestDistance === void 0) { closestDistance = 0; }
                var higherRanks = {},
                    tickPixelIntervalOption = this.options.tickPixelInterval,
                    time = this.chart.time, 
                    // Record all the start positions of a segment, to use when
                    // deciding what's a gap in the data.
                    segmentStarts = [];
                var end,
                    segmentPositions,
                    hasCrossedHigherRank,
                    info,
                    outsideMax,
                    start = 0,
                    groupPositions = [],
                    lastGroupPosition = -Number.MAX_VALUE;
                // The positions are not always defined, for example for ordinal
                // positions when data has regular interval (#1557, #2090)
                if ((!this.options.ordinal && !this.options.breaks) ||
                    !positions ||
                    positions.length < 3 ||
                    typeof min === 'undefined') {
                    return time.getTimeTicks.apply(time, arguments);
                }
                // Analyze the positions array to split it into segments on gaps
                // larger than 5 times the closest distance. The closest distance is
                // already found at this point, so we reuse that instead of
                // computing it again.
                var posLength = positions.length;
                for (end = 0; end < posLength; end++) {
                    outsideMax = end && positions[end - 1] > max;
                    if (positions[end] < min) { // Set the last position before min
                        start = end;
                    }
                    if (end === posLength - 1 ||
                        positions[end + 1] - positions[end] > closestDistance * 5 ||
                        outsideMax) {
                        // For each segment, calculate the tick positions from the
                        // getTimeTicks utility function. The interval will be the
                        // same regardless of how long the segment is.
                        if (positions[end] > lastGroupPosition) { // #1475
                            segmentPositions = time.getTimeTicks(normalizedInterval, positions[start], positions[end], startOfWeek);
                            // Prevent duplicate groups, for example for multiple
                            // segments within one larger time frame (#1475)
                            while (segmentPositions.length &&
                                segmentPositions[0] <= lastGroupPosition) {
                                segmentPositions.shift();
                            }
                            if (segmentPositions.length) {
                                lastGroupPosition =
                                    segmentPositions[segmentPositions.length - 1];
                            }
                            segmentStarts.push(groupPositions.length);
                            groupPositions = groupPositions.concat(segmentPositions);
                        }
                        // Set start of next segment
                        start = end + 1;
                    }
                    if (outsideMax) {
                        break;
                    }
                }
                // Get the grouping info from the last of the segments. The info is
                // the same for all segments.
                if (segmentPositions) {
                    info = segmentPositions.info;
                    // Optionally identify ticks with higher rank, for example
                    // when the ticks have crossed midnight.
                    if (findHigherRanks && info.unitRange <= timeUnits.hour) {
                        end = groupPositions.length - 1;
                        // Compare points two by two
                        for (start = 1; start < end; start++) {
                            if (time.dateFormat('%d', groupPositions[start]) !==
                                time.dateFormat('%d', groupPositions[start - 1])) {
                                higherRanks[groupPositions[start]] = 'day';
                                hasCrossedHigherRank = true;
                            }
                        }
                        // If the complete array has crossed midnight, we want
                        // to mark the first positions also as higher rank
                        if (hasCrossedHigherRank) {
                            higherRanks[groupPositions[0]] = 'day';
                        }
                        info.higherRanks = higherRanks;
                    }
                    // Save the info
                    info.segmentStarts = segmentStarts;
                    groupPositions.info = info;
                }
                else {
                    error(12, false, this.chart);
                }
                // Don't show ticks within a gap in the ordinal axis, where the
                // space between two points is greater than a portion of the tick
                // pixel interval
                if (findHigherRanks && defined(tickPixelIntervalOption)) {
                    var length_1 = groupPositions.length,
                        translatedArr = [],
                        distances = [];
                    var itemToRemove = void 0,
                        translated = void 0,
                        lastTranslated = void 0,
                        medianDistance = void 0,
                        distance = void 0,
                        i = length_1;
                    // Find median pixel distance in order to keep a reasonably even
                    // distance between ticks (#748)
                    while (i--) {
                        translated = this.translate(groupPositions[i]);
                        if (lastTranslated) {
                            distances[i] = lastTranslated - translated;
                        }
                        translatedArr[i] = lastTranslated = translated;
                    }
                    distances.sort();
                    medianDistance = distances[Math.floor(distances.length / 2)];
                    if (medianDistance < tickPixelIntervalOption * 0.6) {
                        medianDistance = null;
                    }
                    // Now loop over again and remove ticks where needed
                    i = groupPositions[length_1 - 1] > max ? length_1 - 1 : length_1; // #817
                    lastTranslated = void 0;
                    while (i--) {
                        translated = translatedArr[i];
                        distance = Math.abs(lastTranslated - translated);
                        // #4175 - when axis is reversed, the distance, is negative but
                        // tickPixelIntervalOption positive, so we need to compare the
                        // same values
                        // Remove ticks that are closer than 0.6 times the pixel
                        // interval from the one to the right, but not if it is close to
                        // the median distance (#748).
                        if (lastTranslated &&
                            distance < tickPixelIntervalOption * 0.8 &&
                            (medianDistance === null || distance < medianDistance * 0.8)) {
                            // Is this a higher ranked position with a normal
                            // position to the right?
                            if (higherRanks[groupPositions[i]] &&
                                !higherRanks[groupPositions[i + 1]]) {
                                // Yes: remove the lower ranked neighbour to the
                                // right
                                itemToRemove = i + 1;
                                lastTranslated = translated; // #709
                            }
                            else {
                                // No: remove this one
                                itemToRemove = i;
                            }
                            groupPositions.splice(itemToRemove, 1);
                        }
                        else {
                            lastTranslated = translated;
                        }
                    }
                }
                return groupPositions;
            }
            /**
             * Get axis position of given index of the extended ordinal positions.
             * Used only when panning an ordinal axis.
             *
             * @private
             * @function Highcharts.Axis#index2val
             * @param {number} index
             * The index value of searched point
             */
            function index2val(index) {
                var axis = this,
                    ordinal = axis.ordinal, 
                    // Context could be changed to extendedOrdinalPositions.
                    ordinalPositions = ordinal.positions;
                // The visible range contains only equally spaced values.
                if (!ordinalPositions) {
                    return index;
                }
                var i = ordinalPositions.length - 1,
                    distance;
                if (index < 0) { // out of range, in effect panning to the left
                    index = ordinalPositions[0];
                }
                else if (index > i) { // out of range, panning to the right
                    index = ordinalPositions[i];
                }
                else { // split it up
                    i = Math.floor(index);
                    distance = index - i; // the decimal
                }
                if (typeof distance !== 'undefined' &&
                    typeof ordinalPositions[i] !== 'undefined') {
                    return ordinalPositions[i] + (distance ?
                        distance *
                            (ordinalPositions[i + 1] - ordinalPositions[i]) :
                        0);
                }
                return index;
            }
            /**
             * Translate from linear (internal) to axis value.
             *
             * @private
             * @function Highcharts.Axis#lin2val
             * @param {number} val
             * The linear abstracted value.
             */
            function lin2val(val) {
                var axis = this,
                    ordinal = axis.ordinal,
                    localMin = axis.old ? axis.old.min : axis.min,
                    localA = axis.old ? axis.old.transA : axis.transA;
                var positions = ordinal.positions; // for the current visible range
                    // The visible range contains only equally spaced values.
                    if (!positions) {
                        return val;
                }
                // Convert back from modivied value to pixels. // #15970
                var pixelVal = (val - localMin) * localA +
                        axis.minPixelPadding,
                    isInside = pixelVal > 0 && pixelVal < axis.left + axis.len;
                // If the value is not inside the plot area, use the extended positions.
                // (array contains also points that are outside of the plotArea).
                if (!isInside) {
                    // When iterating for the first time,
                    // get the extended ordinal positional and assign them.
                    if (!ordinal.extendedOrdinalPositions) {
                        ordinal.extendedOrdinalPositions = (ordinal.getExtendedPositions());
                    }
                    positions = ordinal.extendedOrdinalPositions;
                }
                // In some cases (especially in early stages of the chart creation) the
                // getExtendedPositions might return undefined.
                if (positions && positions.length) {
                    var index = ordinal.getIndexOfPoint(pixelVal,
                        positions),
                        mantissa = correctFloat(index % 1);
                    // Check if the index is inside position array. If true,
                    // read/approximate value for that exact index.
                    if (index >= 0 && index < positions.length - 1) {
                        var leftNeighbour = positions[Math.floor(index)],
                            rightNeighbour = positions[Math.ceil(index)],
                            distance = rightNeighbour - leftNeighbour;
                        return positions[Math.floor(index)] + mantissa * distance;
                    }
                    // For cases when the index is not in the extended ordinal position
                    // array, like when the value we are looking for exceed the
                    // available data, approximate that value based on the calculated
                    // slope.
                    var positionsLength = positions.length,
                        firstPositionsValue = positions[0],
                        lastPositionsValue = positions[positionsLength - 1],
                        slope = (lastPositionsValue - firstPositionsValue) / (positionsLength - 1);
                    if (index < 0) {
                        return firstPositionsValue + slope * index;
                    }
                    return lastPositionsValue + slope * (index - positionsLength);
                }
                return val;
            }
            /**
             * Internal function to calculate the precise index in ordinalPositions
             * array.
             * @private
             */
            function getIndexInArray(ordinalPositions, val) {
                var index = OrdinalAxis.Additions.findIndexOf(ordinalPositions,
                    val,
                    true);
                if (ordinalPositions[index] === val) {
                    return index;
                }
                var percent = (val - ordinalPositions[index]) /
                        (ordinalPositions[index + 1] - ordinalPositions[index]);
                return index + percent;
            }
            /**
            * @private
            */
            function onAxisAfterInit() {
                var axis = this;
                if (!axis.ordinal) {
                    axis.ordinal = new OrdinalAxis.Additions(axis);
                }
            }
            /**
             * @private
             */
            function onAxisFoundExtremes() {
                var axis = this;
                if (axis.isXAxis &&
                    defined(axis.options.overscroll) &&
                    axis.max === axis.dataMax &&
                    (
                    // Panning is an execption. We don't want to apply
                    // overscroll when panning over the dataMax
                    !axis.chart.mouseIsDown ||
                        axis.isInternal) && (
                // Scrollbar buttons are the other execption:
                !axis.eventArgs ||
                    axis.eventArgs && axis.eventArgs.trigger !== 'navigator')) {
                    axis.max += axis.options.overscroll;
                    // Live data and buttons require translation for the min:
                    if (!axis.isInternal && defined(axis.userMin)) {
                        axis.min += axis.options.overscroll;
                    }
                }
            }
            /**
             * For ordinal axis, that loads data async, redraw axis after data is
             * loaded. If we don't do that, axis will have the same extremes as
             * previously, but ordinal positions won't be calculated. See #10290
             * @private
             */
            function onAxisAfterSetScale() {
                var axis = this;
                if (axis.horiz && !axis.isDirty) {
                    axis.isDirty = axis.isOrdinal &&
                        axis.chart.navigator &&
                        !axis.chart.navigator.adaptToUpdatedData;
                }
            }
            /**
             * @private
             */
            function onAxisInitialAxisTranslation() {
                var axis = this;
                if (axis.ordinal) {
                    axis.ordinal.beforeSetTickPositions();
                    axis.tickInterval = axis.ordinal.postProcessTickInterval(axis.tickInterval);
                }
            }
            /**
             * Extending the Chart.pan method for ordinal axes
             * @private
             */
            function onChartPan(e) {
                var chart = this,
                    xAxis = chart.xAxis[0],
                    overscroll = xAxis.options.overscroll,
                    chartX = e.originalEvent.chartX,
                    panning = chart.options.chart.panning;
                var runBase = false;
                if (panning &&
                    panning.type !== 'y' &&
                    xAxis.options.ordinal &&
                    xAxis.series.length) {
                    var mouseDownX = chart.mouseDownX,
                        extremes = xAxis.getExtremes(),
                        dataMax = extremes.dataMax,
                        min = extremes.min,
                        max = extremes.max,
                        hoverPoints = chart.hoverPoints,
                        closestPointRange = (xAxis.closestPointRange ||
                            (xAxis.ordinal && xAxis.ordinal.overscrollPointsRange)),
                        pointPixelWidth = (xAxis.translationSlope *
                            (xAxis.ordinal.slope || closestPointRange)), 
                        // how many ordinal units did we move?
                        movedUnits = (mouseDownX - chartX) / pointPixelWidth, 
                        // get index of all the chart's points
                        extendedOrdinalPositions = xAxis.ordinal.getExtendedPositions(),
                        extendedAxis = {
                            ordinal: {
                                positions: extendedOrdinalPositions,
                                extendedOrdinalPositions: extendedOrdinalPositions
                            }
                        },
                        index2val_1 = xAxis.index2val,
                        val2lin_1 = xAxis.val2lin;
                    var trimmedRange = void 0,
                        ordinalPositions = void 0,
                        searchAxisLeft = void 0,
                        searchAxisRight = void 0;
                    // we have an ordinal axis, but the data is equally spaced
                    if (!extendedAxis.ordinal.positions) {
                        runBase = true;
                    }
                    else if (Math.abs(movedUnits) > 1) {
                        // Remove active points for shared tooltip
                        if (hoverPoints) {
                            hoverPoints.forEach(function (point) {
                                point.setState();
                            });
                        }
                        if (movedUnits < 0) {
                            searchAxisLeft = extendedAxis;
                            searchAxisRight = xAxis.ordinal.positions ?
                                xAxis : extendedAxis;
                        }
                        else {
                            searchAxisLeft = xAxis.ordinal.positions ?
                                xAxis : extendedAxis;
                            searchAxisRight = extendedAxis;
                        }
                        // In grouped data series, the last ordinal position represents
                        // the grouped data, which is to the left of the real data max.
                        // If we don't compensate for this, we will be allowed to pan
                        // grouped data series passed the right of the plot area.
                        ordinalPositions = searchAxisRight.ordinal.positions;
                        if (dataMax >
                            ordinalPositions[ordinalPositions.length - 1]) {
                            ordinalPositions.push(dataMax);
                        }
                        // Get the new min and max values by getting the ordinal index
                        // for the current extreme, then add the moved units and
                        // translate back to values. This happens on the extended
                        // ordinal positions if the new position is out of range, else
                        // it happens on the current x axis which is smaller and faster.
                        chart.fixedRange = max - min;
                        trimmedRange = xAxis.navigatorAxis
                            .toFixedRange(void 0, void 0, index2val_1.apply(searchAxisLeft, [
                            val2lin_1.apply(searchAxisLeft, [min, true]) +
                                movedUnits
                        ]), index2val_1.apply(searchAxisRight, [
                            val2lin_1.apply(searchAxisRight, [max, true]) +
                                movedUnits
                        ]));
                        // Apply it if it is within the available data range
                        if (trimmedRange.min >= Math.min(extremes.dataMin, min) &&
                            trimmedRange.max <= Math.max(dataMax, max) +
                                overscroll) {
                            xAxis.setExtremes(trimmedRange.min, trimmedRange.max, true, false, { trigger: 'pan' });
                        }
                        chart.mouseDownX = chartX; // set new reference for next run
                        css(chart.container, { cursor: 'move' });
                    }
                }
                else {
                    runBase = true;
                }
                // revert to the linear chart.pan version
                if (runBase || (panning && /y/.test(panning.type))) {
                    if (overscroll) {
                        xAxis.max = xAxis.dataMax + overscroll;
                    }
                }
                else {
                    e.preventDefault();
                }
            }
            /**
             * @private
             */
            function onSeriesUpdatedData() {
                var xAxis = this.xAxis;
                // Destroy the extended ordinal index on updated data
                // and destroy extendedOrdinalPositions, #16055.
                if (xAxis && xAxis.options.ordinal) {
                    delete xAxis.ordinal.index;
                    delete xAxis.ordinal.extendedOrdinalPositions;
                }
            }
            /**
             * Translate from a linear axis value to the corresponding ordinal axis
             * position. If there are no gaps in the ordinal axis this will be the
             * same. The translated value is the value that the point would have if
             * the axis was linear, using the same min and max.
             *
             * @private
             * @function Highcharts.Axis#val2lin
             * @param {number} val
             * The axis value.
             * @param {boolean} [toIndex]
             * Whether to return the index in the ordinalPositions or the new value.
             */
            function val2lin(val, toIndex) {
                var axis = this,
                    ordinal = axis.ordinal,
                    ordinalPositions = ordinal.positions;
                var slope = ordinal.slope,
                    extendedOrdinalPositions = ordinal.extendedOrdinalPositions;
                if (!ordinalPositions) {
                    return val;
                }
                var ordinalLength = ordinalPositions.length;
                var ordinalIndex;
                // If the searched value is inside visible plotArea, ivastigate the
                // value basing on ordinalPositions.
                if (ordinalPositions[0] <= val &&
                    ordinalPositions[ordinalLength - 1] >= val) {
                    ordinalIndex = getIndexInArray(ordinalPositions, val);
                    // final return value is based on ordinalIndex
                }
                else {
                    if (!extendedOrdinalPositions) {
                        extendedOrdinalPositions =
                            ordinal.getExtendedPositions &&
                                ordinal.getExtendedPositions();
                        ordinal.extendedOrdinalPositions = extendedOrdinalPositions;
                    }
                    if (!(extendedOrdinalPositions && extendedOrdinalPositions.length)) {
                        return val;
                    }
                    var length_2 = extendedOrdinalPositions.length;
                    if (!slope) {
                        slope =
                            (extendedOrdinalPositions[length_2 - 1] -
                                extendedOrdinalPositions[0]) /
                                length_2;
                    }
                    // OriginalPointReference is equal to the index of
                    // first point of ordinalPositions in extendedOrdinalPositions.
                    var originalPositionsReference = getIndexInArray(extendedOrdinalPositions,
                        ordinalPositions[0]);
                    // If the searched value is outside the visiblePlotArea,
                    // check if it is inside extendedOrdinalPositions.
                    if (val >= extendedOrdinalPositions[0] &&
                        val <=
                            extendedOrdinalPositions[length_2 - 1]) {
                        // Return Value
                        ordinalIndex = getIndexInArray(extendedOrdinalPositions, val) -
                            originalPositionsReference;
                    }
                    else {
                        // Since ordinal.slope is the average distance between 2
                        // points on visible plotArea, this can be used to calculete
                        // the approximate position of the point, which is outside
                        // the extededOrdinalPositions.
                        if (val < extendedOrdinalPositions[0]) {
                            var diff = extendedOrdinalPositions[0] - val,
                                approximateIndexOffset = diff / slope;
                            ordinalIndex =
                                -originalPositionsReference -
                                    approximateIndexOffset;
                        }
                        else {
                            var diff = val -
                                    extendedOrdinalPositions[length_2 - 1],
                                approximateIndexOffset = diff / slope;
                            ordinalIndex =
                                approximateIndexOffset +
                                    length_2 -
                                    originalPositionsReference;
                        }
                    }
                }
                return toIndex ? ordinalIndex : slope * (ordinalIndex || 0) +
                    ordinal.offset;
            }
            /* *
             *
             *  Classes
             *
             * */
            /**
             * @private
             */
            var Additions = /** @class */ (function () {
                    /* *
                     *
                     *  Constructors
                     *
                     * */
                    /**
                     * @private
                     */
                    function Additions(axis) {
                        this.index = {};
                    this.axis = axis;
                }
                /* *
                *
                *  Functions
                *
                * */
                /**
                 * Calculate the ordinal positions before tick positions are calculated.
                 * @private
                 */
                Additions.prototype.beforeSetTickPositions = function () {
                    var axis = this.axis,
                        ordinal = axis.ordinal,
                        extremes = axis.getExtremes(),
                        min = extremes.min,
                        max = extremes.max,
                        hasBreaks = axis.isXAxis && !!axis.options.breaks,
                        isOrdinal = axis.options.ordinal,
                        ignoreHiddenSeries = axis.chart.options.chart.ignoreHiddenSeries;
                    var len,
                        uniqueOrdinalPositions,
                        dist,
                        minIndex,
                        maxIndex,
                        slope,
                        i,
                        ordinalPositions = [],
                        overscrollPointsRange = Number.MAX_VALUE,
                        useOrdinal = false,
                        adjustOrdinalExtremesPoints = false,
                        isBoosted = false;
                    // Apply the ordinal logic
                    if (isOrdinal || hasBreaks) { // #4167 YAxis is never ordinal ?
                        var distanceBetweenPoint_1 = 0;
                        axis.series.forEach(function (series, i) {
                            uniqueOrdinalPositions = [];
                            // For an axis with multiple series, check if the distance
                            // between points is identical throughout all series.
                            if (i > 0 &&
                                series.options.id !== 'highcharts-navigator-series' &&
                                series.processedXData.length > 1) {
                                adjustOrdinalExtremesPoints =
                                    distanceBetweenPoint_1 !== series.processedXData[1] -
                                        series.processedXData[0];
                            }
                            distanceBetweenPoint_1 =
                                series.processedXData[1] - series.processedXData[0];
                            if (series.boosted) {
                                isBoosted = series.boosted;
                            }
                            if ((!ignoreHiddenSeries || series.visible !== false) &&
                                (series
                                    .takeOrdinalPosition !== false ||
                                    hasBreaks)) {
                                // concatenate the processed X data into the existing
                                // positions, or the empty array
                                ordinalPositions = ordinalPositions.concat(series.processedXData);
                                len = ordinalPositions.length;
                                // remove duplicates (#1588)
                                ordinalPositions.sort(function (a, b) {
                                    // without a custom function it is sorted as strings
                                    return a - b;
                                });
                                overscrollPointsRange = Math.min(overscrollPointsRange, pick(
                                // Check for a single-point series:
                                series.closestPointRange, overscrollPointsRange));
                                if (len) {
                                    i = 0;
                                    while (i < len - 1) {
                                        if (ordinalPositions[i] !==
                                            ordinalPositions[i + 1]) {
                                            uniqueOrdinalPositions.push(ordinalPositions[i + 1]);
                                        }
                                        i++;
                                    }
                                    // Check first item:
                                    if (uniqueOrdinalPositions[0] !==
                                        ordinalPositions[0]) {
                                        uniqueOrdinalPositions.unshift(ordinalPositions[0]);
                                    }
                                    ordinalPositions = uniqueOrdinalPositions;
                                }
                            }
                        });
                        // If the distance between points is not identical throughout
                        // all series, remove the first and last ordinal position to
                        // avoid enabling ordinal logic when it is not needed, #17405.
                        // Only for boosted series because changes are negligible.
                        if (adjustOrdinalExtremesPoints && isBoosted) {
                            ordinalPositions.pop();
                            ordinalPositions.shift();
                        }
                        // cache the length
                        len = ordinalPositions.length;
                        // Check if we really need the overhead of mapping axis data
                        // against the ordinal positions. If the series consist of
                        // evenly spaced data any way, we don't need any ordinal logic.
                        if (len > 2) { // two points have equal distance by default
                            dist = ordinalPositions[1] - ordinalPositions[0];
                            i = len - 1;
                            while (i-- && !useOrdinal) {
                                if (ordinalPositions[i + 1] - ordinalPositions[i] !==
                                    dist) {
                                    useOrdinal = true;
                                }
                            }
                            // When zooming in on a week, prevent axis padding for
                            // weekends even though the data within the week is evenly
                            // spaced.
                            if (!axis.options.keepOrdinalPadding &&
                                (ordinalPositions[0] - min > dist ||
                                    (max -
                                        ordinalPositions[ordinalPositions.length - 1]) > dist)) {
                                useOrdinal = true;
                            }
                        }
                        else if (axis.options.overscroll) {
                            if (len === 2) {
                                // Exactly two points, distance for overscroll is fixed:
                                overscrollPointsRange =
                                    ordinalPositions[1] - ordinalPositions[0];
                            }
                            else if (len === 1) {
                                // We have just one point, closest distance is unknown.
                                // Assume then it is last point and overscrolled range:
                                overscrollPointsRange = axis.options.overscroll;
                                ordinalPositions = [
                                    ordinalPositions[0],
                                    ordinalPositions[0] + overscrollPointsRange
                                ];
                            }
                            else {
                                // In case of zooming in on overscrolled range, stick to
                                // the old range:
                                overscrollPointsRange = ordinal.overscrollPointsRange;
                            }
                        }
                        // Record the slope and offset to compute the linear values from
                        // the array index. Since the ordinal positions may exceed the
                        // current range, get the start and end positions within it
                        // (#719, #665b)
                        if (useOrdinal || axis.forceOrdinal) {
                            if (axis.options.overscroll) {
                                ordinal.overscrollPointsRange = overscrollPointsRange;
                                ordinalPositions = ordinalPositions.concat(ordinal.getOverscrollPositions());
                            }
                            // Register
                            ordinal.positions = ordinalPositions;
                            // This relies on the ordinalPositions being set. Use
                            // Math.max and Math.min to prevent padding on either sides
                            // of the data.
                            minIndex = axis.ordinal2lin(// #5979
                            Math.max(min, ordinalPositions[0]), true);
                            maxIndex = Math.max(axis.ordinal2lin(Math.min(max, ordinalPositions[ordinalPositions.length - 1]), true), 1); // #3339
                            // Set the slope and offset of the values compared to the
                            // indices in the ordinal positions
                            ordinal.slope = slope = (max - min) / (maxIndex - minIndex);
                            ordinal.offset = min - (minIndex * slope);
                        }
                        else {
                            ordinal.overscrollPointsRange = pick(axis.closestPointRange, ordinal.overscrollPointsRange);
                            ordinal.positions = axis.ordinal.slope = ordinal.offset =
                                void 0;
                        }
                    }
                    axis.isOrdinal = isOrdinal && useOrdinal; // #3818, #4196, #4926
                    ordinal.groupIntervalFactor = null; // reset for next run
                };
                /**
                 * Faster way of using the Array.indexOf method.
                 * Works for sorted arrays only with unique values.
                 *
                 * @param {Array} sortedArray
                 *        The sorted array inside which we are looking for.
                 * @param {number} key
                 *        The key to being found.
                 * @param {boolean} indirectSearch
                 *        In case of lack of the point in the array, should return
                 *        value be equal to -1 or the closest smaller index.
                 *  @private
                 */
                Additions.findIndexOf = function (sortedArray, key, indirectSearch) {
                    var start = 0,
                        end = sortedArray.length - 1,
                        middle;
                    while (start < end) {
                        middle = Math.ceil((start + end) / 2);
                        // Key found as the middle element.
                        if (sortedArray[middle] <= key) {
                            // Continue searching to the right.
                            start = middle;
                        }
                        else {
                            // Continue searching to the left.
                            end = middle - 1;
                        }
                    }
                    if (sortedArray[start] === key) {
                        return start;
                    }
                    // Key could not be found.
                    return !indirectSearch ? -1 : start;
                };
                /**
                 * Get the ordinal positions for the entire data set. This is necessary
                 * in chart panning because we need to find out what points or data
                 * groups are available outside the visible range. When a panning
                 * operation starts, if an index for the given grouping does not exists,
                 * it is created and cached. This index is deleted on updated data, so
                 * it will be regenerated the next time a panning operation starts.
                 * @private
                 */
                Additions.prototype.getExtendedPositions = function () {
                    var ordinal = this,
                        axis = ordinal.axis,
                        axisProto = axis.constructor.prototype,
                        chart = axis.chart,
                        grouping = axis.series[0].currentDataGrouping,
                        key = grouping ?
                            grouping.count + grouping.unitName :
                            'raw',
                        overscroll = axis.options.overscroll,
                        extremes = axis.getExtremes();
                    var fakeAxis,
                        fakeSeries = void 0,
                        ordinalIndex = ordinal.index;
                    // If this is the first time, or the ordinal index is deleted by
                    // updatedData,
                    // create it.
                    if (!ordinalIndex) {
                        ordinalIndex = ordinal.index = {};
                    }
                    if (!ordinalIndex[key]) {
                        // Create a fake axis object where the extended ordinal
                        // positions are emulated
                        fakeAxis = {
                            series: [],
                            chart: chart,
                            forceOrdinal: false,
                            getExtremes: function () {
                                return {
                                    min: extremes.dataMin,
                                    max: extremes.dataMax + overscroll
                                };
                            },
                            getGroupPixelWidth: axisProto.getGroupPixelWidth,
                            getTimeTicks: axisProto.getTimeTicks,
                            options: {
                                ordinal: true
                            },
                            ordinal: {
                                getGroupIntervalFactor: this.getGroupIntervalFactor
                            },
                            ordinal2lin: axisProto.ordinal2lin,
                            getIndexOfPoint: axisProto.getIndexOfPoint,
                            val2lin: axisProto.val2lin // #2590
                        };
                        fakeAxis.ordinal.axis = fakeAxis;
                        // Add the fake series to hold the full data, then apply
                        // processData to it
                        axis.series.forEach(function (series) {
                            fakeSeries = {
                                xAxis: fakeAxis,
                                xData: series.xData.slice(),
                                chart: chart,
                                destroyGroupedData: H.noop,
                                getProcessedData: Series.prototype.getProcessedData,
                                applyGrouping: Series.prototype.applyGrouping
                            };
                            fakeSeries.xData = fakeSeries.xData.concat(ordinal.getOverscrollPositions());
                            fakeSeries.options = {
                                dataGrouping: grouping ? {
                                    firstAnchor: 'firstPoint',
                                    anchor: 'middle',
                                    lastAnchor: 'lastPoint',
                                    enabled: true,
                                    forced: true,
                                    // doesn't matter which, use the fastest
                                    approximation: 'open',
                                    units: [[
                                            grouping.unitName,
                                            [grouping.count]
                                        ]]
                                } : {
                                    enabled: false
                                }
                            };
                            fakeAxis.series.push(fakeSeries);
                            series.processData.apply(fakeSeries);
                        });
                        // Force to use the ordinal when points are evenly spaced (e.g.
                        // weeks), #3825.
                        if ((fakeSeries.closestPointRange !==
                            fakeSeries.basePointRange) &&
                            fakeSeries.currentDataGrouping) {
                            fakeAxis.forceOrdinal = true;
                        }
                        // Run beforeSetTickPositions to compute the ordinalPositions
                        axis.ordinal.beforeSetTickPositions.apply({ axis: fakeAxis });
                        // Cache it
                        ordinalIndex[key] = fakeAxis.ordinal.positions;
                    }
                    return ordinalIndex[key];
                };
                /**
                 * Find the factor to estimate how wide the plot area would have been if
                 * ordinal gaps were included. This value is used to compute an imagined
                 * plot width in order to establish the data grouping interval.
                 *
                 * A real world case is the intraday-candlestick example. Without this
                 * logic, it would show the correct data grouping when viewing a range
                 * within each day, but once moving the range to include the gap between
                 * two days, the interval would include the cut-away night hours and the
                 * data grouping would be wrong. So the below method tries to compensate
                 * by identifying the most common point interval, in this case days.
                 *
                 * An opposite case is presented in issue #718. We have a long array of
                 * daily data, then one point is appended one hour after the last point.
                 * We expect the data grouping not to change.
                 *
                 * In the future, if we find cases where this estimation doesn't work
                 * optimally, we might need to add a second pass to the data grouping
                 * logic, where we do another run with a greater interval if the number
                 * of data groups is more than a certain fraction of the desired group
                 * count.
                 * @private
                 */
                Additions.prototype.getGroupIntervalFactor = function (xMin, xMax, series) {
                    var ordinal = this,
                        axis = ordinal.axis,
                        processedXData = series.processedXData,
                        len = processedXData.length,
                        distances = [];
                    var median,
                        i,
                        groupIntervalFactor = ordinal.groupIntervalFactor;
                    // Only do this computation for the first series, let the other
                    // inherit it (#2416)
                    if (!groupIntervalFactor) {
                        // Register all the distances in an array
                        for (i = 0; i < len - 1; i++) {
                            distances[i] = (processedXData[i + 1] -
                                processedXData[i]);
                        }
                        // Sort them and find the median
                        distances.sort(function (a, b) {
                            return a - b;
                        });
                        median = distances[Math.floor(len / 2)];
                        // Compensate for series that don't extend through the entire
                        // axis extent. #1675.
                        xMin = Math.max(xMin, processedXData[0]);
                        xMax = Math.min(xMax, processedXData[len - 1]);
                        ordinal.groupIntervalFactor = groupIntervalFactor =
                            (len * median) / (xMax - xMin);
                    }
                    // Return the factor needed for data grouping
                    return groupIntervalFactor;
                };
                /**
                 * Get index of point inside the ordinal positions array.
                 *
                 * @private
                 * @param {number} val
                 * The pixel value of a point.
                 *
                 * @param {Array<number>} [ordinallArray]
                 * An array of all points available on the axis for the given data set.
                 * Either ordinalPositions if the value is inside the plotArea or
                 * extendedOrdinalPositions if not.
                 */
                Additions.prototype.getIndexOfPoint = function (val, ordinalArray) {
                    var ordinal = this,
                        axis = ordinal.axis,
                        firstPointVal = ordinal.positions ? ordinal.positions[0] : 0;
                    var firstPointX = axis.series[0].points &&
                            axis.series[0].points[0] &&
                            axis.series[0].points[0].plotX ||
                            axis.minPixelPadding; // #15987
                        // When more series assign to axis, find the smallest one, #15987.
                        if (axis.series.length > 1) {
                            axis.series.forEach(function (series) {
                                if (series.points &&
                                    defined(series.points[0]) &&
                                    defined(series.points[0].plotX) &&
                                    series.points[0].plotX < firstPointX) {
                                    firstPointX = series.points[0].plotX;
                            }
                        });
                    }
                    // Distance in pixels between two points on the ordinal axis in the
                    // current zoom.
                    var ordinalPointPixelInterval = axis.translationSlope * (ordinal.slope ||
                            axis.closestPointRange ||
                            ordinal.overscrollPointsRange), 
                        // toValue for the first point.
                        shiftIndex = (val - firstPointX) / ordinalPointPixelInterval;
                    return Additions.findIndexOf(ordinalArray, firstPointVal) + shiftIndex;
                };
                /**
                 * Get ticks for an ordinal axis within a range where points don't
                 * exist. It is required when overscroll is enabled. We can't base on
                 * points, because we may not have any, so we use approximated
                 * pointRange and generate these ticks between Axis.dataMax,
                 * Axis.dataMax + Axis.overscroll evenly spaced. Used in panning and
                 * navigator scrolling.
                 * @private
                 */
                Additions.prototype.getOverscrollPositions = function () {
                    var ordinal = this,
                        axis = ordinal.axis,
                        extraRange = axis.options.overscroll,
                        distance = ordinal.overscrollPointsRange,
                        positions = [],
                        max = axis.dataMax;
                    if (defined(distance)) {
                        // Max + pointRange because we need to scroll to the last
                        while (max <= axis.dataMax + extraRange) {
                            max += distance;
                            positions.push(max);
                        }
                    }
                    return positions;
                };
                /**
                 * Make the tick intervals closer because the ordinal gaps make the
                 * ticks spread out or cluster.
                 * @private
                 */
                Additions.prototype.postProcessTickInterval = function (tickInterval) {
                    // Problem: https://jsfiddle.net/highcharts/FQm4E/1/. This is a case
                    // where this algorithm doesn't work optimally. In this case, the
                    // tick labels are spread out per week, but all the gaps reside
                    // within weeks. So we have a situation where the labels are courser
                    // than the ordinal gaps, and thus the tick interval should not be
                    // altered.
                    var ordinal = this,
                        axis = ordinal.axis,
                        ordinalSlope = ordinal.slope;
                    var ret;
                    if (ordinalSlope) {
                        if (!axis.options.breaks) {
                            ret = (tickInterval /
                                (ordinalSlope / axis.closestPointRange));
                        }
                        else {
                            ret = axis.closestPointRange || tickInterval; // #7275
                        }
                    }
                    else {
                        ret = tickInterval;
                    }
                    return ret;
                };
                return Additions;
            }());
            OrdinalAxis.Additions = Additions;
        })(OrdinalAxis || (OrdinalAxis = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return OrdinalAxis;
    });
    _registerModule(_modules, 'Series/HLC/HLCPoint.js', [_modules['Core/Series/SeriesRegistry.js']], function (SeriesRegistry) {
        /* *
         *
         *  (c) 2010-2021 Pawel Lysy
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
        var ColumnPoint = SeriesRegistry.seriesTypes.column.prototype.pointClass;
        /* *
         *
         *  Class
         *
         * */
        var HLCPoint = /** @class */ (function (_super) {
                __extends(HLCPoint, _super);
            function HLCPoint() {
                /* *
                 *
                 *  Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.close = void 0;
                _this.high = void 0;
                _this.low = void 0;
                _this.options = void 0;
                _this.plotClose = void 0;
                _this.series = void 0;
                return _this;
            }
            return HLCPoint;
        }(ColumnPoint));
        /* *
         *
         *  Default Export
         *
         * */

        return HLCPoint;
    });
    _registerModule(_modules, 'Series/HLC/HLCSeriesDefaults.js', [], function () {
        /* *
         *
         *  (c) 2010-2021 Pawel Lysy
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
         * An HLC chart is a style of financial chart used to describe price
         * movements over time. It displays high, low and close values per
         * data point.
         *
         * @sample stock/demo/hlc/
         *         HLC chart
         *
         * @extends      plotOptions.column
         * @excluding    borderColor, borderRadius, borderWidth, crisp, stacking,
         *               stack
         * @product      highstock
         * @optionparent plotOptions.hlc
         */
        var HLCSeriesDefaults = {
                /**
                 * The approximate pixel width of each group. If for example a series
                 * with 30 points is displayed over a 600 pixel wide plot area, no
                 * grouping is performed. If however the series contains so many points
                 * that the spacing is less than the groupPixelWidth, Highcharts will
                 * try to group it into appropriate groups so that each is more or less
                 * two pixels wide. Defaults to `5`.
                 *
                 * @type      {number}
                 * @default   5
                 * @product   highstock
                 * @apioption plotOptions.hlc.dataGrouping.groupPixelWidth
                 */
                /**
                 * @type      {Highcharts.DataGroupingApproximationValue|Function}
                 * @default   hlc
                 * @product   highstock
                 * @apioption plotOptions.hlc.dataGrouping.approximation
                 */
                /**
                 * @default   close
                 * @apioption plotOptions.hlc.colorKey
                 */
                /**
                 * The pixel width of the line/border. Defaults to `1`.
                 *
                 * @sample {highstock} stock/plotoptions/hlc-linewidth/
                 *         A greater line width
                 *
                 * @type    {number}
                 * @default 1
                 * @product highstock
                 *
                 * @public
                 */
                lineWidth: 1,
                tooltip: {
                    pointFormat: '<span style="color:{point.color}">\u25CF</span> ' +
                        '<b> {series.name}</b><br/>' +
                        'High: {point.high}<br/>' +
                        'Low: {point.low}<br/>' +
                        'Close: {point.close}<br/>'
                },
                /**
                 * @type {number|null}
                 */
                threshold: null,
                states: {
                    /**
                     * @extends plotOptions.column.states.hover
                     * @product highstock
                     */
                    hover: {
                        /**
                         * The pixel width of the line representing the HLC point.
                         *
                         * @type    {number}
                         * @default 3
                         * @product highstock
                         */
                        lineWidth: 3
                    }
                },
                /**
                 * Determines which one of  `high`, `low`, `close` values should
                 * be represented as `point.y`, which is later used to set dataLabel
                 * position and [compare](#plotOptions.series.compare).
                 *
                 * @sample {highstock} stock/plotoptions/hlc-pointvalkey/
                 *         Possible values
                 *
                 * @type       {string}
                 * @default    close
                 * @validvalue ["high", "low", "close"]
                 * @product    highstock
                 * @apioption  plotOptions.hlc.pointValKey
                 */
                /**
                 * @default   close
                 * @apioption plotOptions.hlc.colorKey
                 */
                stickyTracking: true
            };
        /**
         * A `hlc` series. If the [type](#series.hlc.type) option is not
         * specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.hlc
         * @excluding dataParser, dataURL
         * @product   highstock
         * @apioption series.hlc
         */
        /**
         * An array of data points for the series. For the `hlc` series type,
         * points can be given in the following ways:
         *
         * 1. An array of arrays with 4 or 3 values. In this case, the values correspond
         *    to `x,high,low,close`. If the first value is a string, it is applied
         *    as the name of the point, and the `x` value is inferred. The `x` value can
         *    also be omitted, in which case the inner arrays should be of length of 3\.
         *    Then the `x` value is automatically calculated, either starting at 0 and
         *    incremented by 1, or from `pointStart` and `pointInterval` given in the
         *    series options.
         *    ```js
         *    data: [
         *        [0, 5, 6, 7],
         *        [1, 4, 8, 2],
         *        [2, 3, 4, 10]
         *    ]
         *    ```
         *
         * 2. An array of objects with named values. The following snippet shows only a
         *    few settings, see the complete options set below. If the total number of
         *    data points exceeds the series'
         *    [turboThreshold](#series.hlc.turboThreshold), this option is not
         *    available.
         *    ```js
         *    data: [{
         *        x: 1,
         *        high: 4,
         *        low: 5,
         *        close: 2,
         *        name: "Point2",
         *        color: "#00FF00"
         *    }, {
         *        x: 1,
         *        high: 3,
         *        low: 6,
         *        close: 7,
         *        name: "Point1",
         *        color: "#FF00FF"
         *    }]
         *    ```
         *
         * @type      {Array<Array<(number|string),number,number>|Array<(number|string),number,number,number>|*>}
         * @extends   series.arearange.data
         * @excluding y, marker
         * @product   highstock
         * @apioption series.hlc.data
         */
        /**
         * The closing value of each data point.
         *
         * @type      {number}
         * @product   highstock
         * @apioption series.hlc.data.close
         */
        (''); // keeps doclets above in JS file
        /* *
         *
         *  Default Export
         *
         * */

        return HLCSeriesDefaults;
    });
    _registerModule(_modules, 'Series/HLC/HLCSeries.js', [_modules['Series/HLC/HLCPoint.js'], _modules['Series/HLC/HLCSeriesDefaults.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (HLCPoint, HLCSeriesDefaults, SeriesRegistry, U) {
        /* *
         *
         *  (c) 2010-2021 Pawel Lysy
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
        var ColumnSeries = SeriesRegistry.seriesTypes.column;
        var extend = U.extend,
            merge = U.merge;
        /* *
         *
         *  Class
         *
         * */
        /**
         * The hlc series type.
         *
         * @private
         * @class
         * @name Highcharts.seriesTypes.hlc
         *
         * @augments Highcharts.Series
         */
        var HLCSeries = /** @class */ (function (_super) {
                __extends(HLCSeries, _super);
            function HLCSeries() {
                /* *
                 *
                 *  Static Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                /* *
                 *
                 *  Properties
                 *
                 * */
                _this.data = void 0;
                _this.options = void 0;
                _this.points = void 0;
                _this.yData = void 0;
                return _this;
            }
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Extend the path if close is not between high and low.
             *
             * @param {SVGPath} path the path array of the point
             * @param {number} halfStrokeWidth
             * @param {number} value value of the point to which the stem should be extended
             */
            HLCSeries.prototype.extendStem = function (path, halfStrokeWidth, value) {
                var start = path[0];
                var end = path[1];
                // We don't need to worry about crisp - close value
                // is already crisped and halfStrokeWidth should remove it.
                if (typeof start[2] === 'number') {
                    start[2] = Math.max(value + halfStrokeWidth, start[2]);
                }
                if (typeof end[2] === 'number') {
                    end[2] = Math.min(value - halfStrokeWidth, end[2]);
                }
            };
            /**
             * Function to create SVGPath of the point based on the
             * plot positions of this point.
             * @private
             */
            HLCSeries.prototype.getPointPath = function (point, graphic) {
                // crisp vector coordinates
                var strokeWidth = graphic.strokeWidth(),
                    series = point.series,
                    crispCorr = (strokeWidth % 2) / 2, 
                    // #2596:
                    crispX = Math.round(point.plotX) - crispCorr,
                    halfWidth = Math.round(point.shapeArgs.width / 2);
                var plotClose = point.plotClose;
                // the vertical stem
                var path = [
                        ['M',
                    crispX,
                    Math.round(point.yBottom)],
                        ['L',
                    crispX,
                    Math.round(point.plotHigh)]
                    ];
                // close
                if (point.close !== null) {
                    plotClose = Math.round(point.plotClose) + crispCorr;
                    path.push(['M', crispX, plotClose], ['L', crispX + halfWidth, plotClose]);
                    series.extendStem(path, strokeWidth / 2, plotClose);
                }
                return path;
            };
            /**
             * Draw single point
             * @private
             */
            HLCSeries.prototype.drawSinglePoint = function (point) {
                var series = point.series,
                    chart = series.chart;
                var path,
                    graphic = point.graphic;
                if (typeof point.plotY !== 'undefined') {
                    // Create and/or update the graphic
                    if (!graphic) {
                        point.graphic = graphic = chart.renderer.path()
                            .add(series.group);
                    }
                    if (!chart.styledMode) {
                        graphic.attr(series.pointAttribs(point, (point.selected && 'select'))); // #3897
                    }
                    // crisp vector coordinates
                    path = series.getPointPath(point, graphic);
                    graphic[!graphic ? 'attr' : 'animate']({ d: path })
                        .addClass(point.getClassName(), true);
                }
            };
            /**
             * Draw the data points
             * @private
             */
            HLCSeries.prototype.drawPoints = function () {
                this.points.forEach(this.drawSinglePoint);
            };
            /**
             * @private
             * @function Highcharts.seriesTypes.hlc#init
             */
            HLCSeries.prototype.init = function () {
                _super.prototype.init.apply(this, arguments);
                this.options.stacking = void 0; // #8817
            };
            /**
             * Postprocess mapping between options and SVG attributes
             * @private
             */
            HLCSeries.prototype.pointAttribs = function (point, state) {
                var attribs = _super.prototype.pointAttribs.call(this,
                    point,
                    state);
                delete attribs.fill;
                return attribs;
            };
            HLCSeries.prototype.toYData = function (point) {
                // return a plain array for speedy calculation
                return [point.high, point.low, point.close];
            };
            /**
             * Translate data points from raw values x and y to plotX and plotY
             *
             * @private
             * @function Highcharts.seriesTypes.hlc#translate
             */
            HLCSeries.prototype.translate = function () {
                var series = this,
                    yAxis = series.yAxis,
                    names = (this.pointArrayMap && this.pointArrayMap.slice()) || [],
                    translated = names.map(function (name) {
                        return "plot".concat(name.charAt(0).toUpperCase() + name.slice(1));
                });
                translated.push('yBottom');
                names.push('low');
                _super.prototype.translate.apply(series);
                // Do the translation
                series.points.forEach(function (point) {
                    names.forEach(function (name, i) {
                        var value = point[name];
                        if (value !== null) {
                            if (series.dataModify) {
                                value = series.dataModify.modifyValue(value);
                            }
                            point[translated[i]] =
                                yAxis.toPixels(value, true);
                        }
                    });
                    // Align the tooltip to the high value to avoid covering the
                    // point
                    point.tooltipPos[1] =
                        point.plotHigh + yAxis.pos - series.chart.plotTop;
                });
            };
            HLCSeries.defaultOptions = merge(ColumnSeries.defaultOptions, HLCSeriesDefaults);
            return HLCSeries;
        }(ColumnSeries));
        extend(HLCSeries.prototype, {
            pointClass: HLCPoint,
            animate: null,
            directTouch: false,
            pointArrayMap: ['high', 'low', 'close'],
            pointAttrToOptions: {
                stroke: 'color',
                'stroke-width': 'lineWidth'
            },
            pointValKey: 'close'
        });
        SeriesRegistry.registerSeriesType('hlc', HLCSeries);
        /* *
         *
         *  Default Export
         *
         * */

        return HLCSeries;
    });
    _registerModule(_modules, 'Series/OHLC/OHLCPoint.js', [_modules['Core/Series/SeriesRegistry.js']], function (SeriesRegistry) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
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
        var HLCSeries = SeriesRegistry.seriesTypes.hlc;
        /* *
         *
         *  Class
         *
         * */
        var OHLCPoint = /** @class */ (function (_super) {
                __extends(OHLCPoint, _super);
            function OHLCPoint() {
                /* *
                 *
                 *  Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.open = void 0;
                _this.options = void 0;
                _this.plotOpen = void 0;
                _this.series = void 0;
                return _this;
            }
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Extend the parent method by adding up or down to the class name.
             * @private
             * @function Highcharts.seriesTypes.ohlc#getClassName
             */
            OHLCPoint.prototype.getClassName = function () {
                return _super.prototype.getClassName.call(this) +
                    (this.open < this.close ?
                        ' highcharts-point-up' :
                        ' highcharts-point-down');
            };
            /**
             * Save upColor as point color (#14826).
             * @private
             * @function Highcharts.seriesTypes.ohlc#resolveUpColor
             */
            OHLCPoint.prototype.resolveUpColor = function () {
                if (this.open < this.close &&
                    !this.options.color &&
                    this.series.options.upColor) {
                    this.color = this.series.options.upColor;
                }
            };
            /**
             * Extend the parent method by saving upColor.
             * @private
             * @function Highcharts.seriesTypes.ohlc#resolveColor
             */
            OHLCPoint.prototype.resolveColor = function () {
                _super.prototype.resolveColor.call(this);
                this.resolveUpColor();
            };
            /**
             * Extend the parent method by saving upColor.
             * @private
             * @function Highcharts.seriesTypes.ohlc#getZone
             *
             * @return {Highcharts.SeriesZonesOptionsObject}
             *         The zone item.
             */
            OHLCPoint.prototype.getZone = function () {
                var zone = _super.prototype.getZone.call(this);
                this.resolveUpColor();
                return zone;
            };
            /**
             * Extend the parent method by resolving up/down colors (#15849)
             * @private
             **/
            OHLCPoint.prototype.applyOptions = function () {
                _super.prototype.applyOptions.apply(this, arguments);
                if (this.resolveColor) {
                    this.resolveColor();
                }
                return this;
            };
            return OHLCPoint;
        }(HLCSeries.prototype.pointClass));
        /* *
         *
         *  Default Export
         *
         * */

        return OHLCPoint;
    });
    _registerModule(_modules, 'Series/OHLC/OHLCSeriesDefaults.js', [], function () {
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
         *  API Options
         *
         * */
        /**
         * An OHLC chart is a style of financial chart used to describe price
         * movements over time. It displays open, high, low and close values per
         * data point.
         *
         * @sample stock/demo/ohlc
         *         OHLC chart
         *
         * @extends      plotOptions.hlc
         * @product      highstock
         * @optionparent plotOptions.ohlc
         */
        var OHLCSeriesDefaults = {
                /**
                 * @type      {Highcharts.DataGroupingApproximationValue|Function}
                 * @default   ohlc
                 * @product   highstock
                 * @apioption plotOptions.ohlc.dataGrouping.approximation
                 */
                /**
                 * Determines which one of  `open`, `high`, `low`, `close` values should
                 * be represented as `point.y`, which is later used to set dataLabel
                 * position and [compare](#plotOptions.series.compare).
                 *
                 * @default    close
                 * @validvalue ["open", "high", "low", "close"]
                 * @product    highstock
                 * @apioption  plotOptions.ohlc.pointValKey
                 */
                /**
                 * Line color for up points.
                 *
                 * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 * @product   highstock
                 * @apioption plotOptions.ohlc.upColor
                 */
                tooltip: {
                    pointFormat: '<span style="color:{point.color}">\u25CF</span> ' +
                        '<b> {series.name}</b><br/>' +
                        'Open: {point.open}<br/>' +
                        'High: {point.high}<br/>' +
                        'Low: {point.low}<br/>' +
                        'Close: {point.close}<br/>'
                }
            };
        /**
         * The parameter allows setting line series type and use OHLC indicators.
         * Data in OHLC format is required.
         *
         * @sample {highstock} stock/indicators/use-ohlc-data
         *         Use OHLC data format to plot line chart
         *
         * @type      {boolean}
         * @product   highstock
         * @apioption plotOptions.line.useOhlcData
         */
        /**
         * A `ohlc` series. If the [type](#series.ohlc.type) option is not
         * specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.ohlc
         * @excluding dataParser, dataURL
         * @product   highstock
         * @apioption series.ohlc
         */
        /**
         * An array of data points for the series. For the `ohlc` series type,
         * points can be given in the following ways:
         *
         * 1. An array of arrays with 5 or 4 values. In this case, the values correspond
         *    to `x,open,high,low,close`. If the first value is a string, it is applied
         *    as the name of the point, and the `x` value is inferred. The `x` value can
         *    also be omitted, in which case the inner arrays should be of length 4\.
         *    Then the `x` value is automatically calculated, either starting at 0 and
         *    incremented by 1, or from `pointStart` and `pointInterval` given in the
         *    series options.
         *    ```js
         *    data: [
         *        [0, 6, 5, 6, 7],
         *        [1, 9, 4, 8, 2],
         *        [2, 6, 3, 4, 10]
         *    ]
         *    ```
         *
         * 2. An array of objects with named values. The following snippet shows only a
         *    few settings, see the complete options set below. If the total number of
         *    data points exceeds the series'
         *    [turboThreshold](#series.ohlc.turboThreshold), this option is not
         *    available.
         *    ```js
         *    data: [{
         *        x: 1,
         *        open: 3,
         *        high: 4,
         *        low: 5,
         *        close: 2,
         *        name: "Point2",
         *        color: "#00FF00"
         *    }, {
         *        x: 1,
         *        open: 4,
         *        high: 3,
         *        low: 6,
         *        close: 7,
         *        name: "Point1",
         *        color: "#FF00FF"
         *    }]
         *    ```
         *
         * @type      {Array<Array<(number|string),number,number,number>|Array<(number|string),number,number,number,number>|*>}
         * @extends   series.arearange.data
         * @excluding y, marker
         * @product   highstock
         * @apioption series.ohlc.data
         */
        /**
         * The closing value of each data point.
         *
         * @type      {number}
         * @product   highstock
         * @apioption series.ohlc.data.close
         */
        /**
         * The opening value of each data point.
         *
         * @type      {number}
         * @product   highstock
         * @apioption series.ohlc.data.open
         */
        ''; // adds doclets above to transpilat
        /* *
         *
         *  Default Export
         *
         * */

        return OHLCSeriesDefaults;
    });
    _registerModule(_modules, 'Series/OHLC/OHLCSeries.js', [_modules['Series/OHLC/OHLCPoint.js'], _modules['Series/OHLC/OHLCSeriesDefaults.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (OHLCPoint, OHLCSeriesDefaults, SeriesRegistry, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
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
        var HLCSeries = SeriesRegistry.seriesTypes.hlc;
        var addEvent = U.addEvent,
            extend = U.extend,
            merge = U.merge;
        /* *
         *
         *  Constants
         *
         * */
        var composedMembers = [];
        /* *
         *
         *  Functions
         *
         * */
        /**
         * @private
         */
        function onSeriesAfterSetOptions(e) {
            var options = e.options,
                dataGrouping = options.dataGrouping;
            if (dataGrouping &&
                options.useOhlcData &&
                options.id !== 'highcharts-navigator-series') {
                dataGrouping.approximation = 'ohlc';
            }
        }
        /**
         * Add useOhlcData option
         * @private
         */
        function onSeriesInit(eventOptions) {
            // eslint-disable-next-line no-invalid-this
            var series = this,
                options = eventOptions.options;
            if (options.useOhlcData &&
                options.id !== 'highcharts-navigator-series') {
                extend(series, {
                    pointValKey: OHLCSeries.prototype.pointValKey,
                    // keys: ohlcProto.keys, // @todo potentially nonsense
                    pointArrayMap: OHLCSeries.prototype.pointArrayMap,
                    toYData: OHLCSeries.prototype.toYData
                });
            }
        }
        /* *
         *
         *  Class
         *
         * */
        /**
         * The ohlc series type.
         *
         * @private
         * @class
         * @name Highcharts.seriesTypes.ohlc
         *
         * @augments Highcharts.Series
         */
        var OHLCSeries = /** @class */ (function (_super) {
                __extends(OHLCSeries, _super);
            function OHLCSeries() {
                /* *
                 *
                 *  Static Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                /* *
                 *
                 *  Properties
                 *
                 * */
                _this.data = void 0;
                _this.options = void 0;
                _this.points = void 0;
                return _this;
            }
            /* *
             *
             *  Static Functions
             *
             * */
            OHLCSeries.compose = function (SeriesClass) {
                var _args = [];
                for (var _i = 1; _i < arguments.length; _i++) {
                    _args[_i - 1] = arguments[_i];
                }
                if (composedMembers.indexOf(SeriesClass) === -1) {
                    composedMembers.push(SeriesClass);
                    addEvent(SeriesClass, 'afterSetOptions', onSeriesAfterSetOptions);
                    addEvent(SeriesClass, 'init', onSeriesInit);
                }
            };
            /* *
             *
             *  Functions
             *
             * */
            OHLCSeries.prototype.getPointPath = function (point, graphic) {
                var path = _super.prototype.getPointPath.call(this,
                    point,
                    graphic),
                    strokeWidth = graphic.strokeWidth(),
                    crispCorr = (strokeWidth % 2) / 2,
                    crispX = Math.round(point.plotX) - crispCorr,
                    halfWidth = Math.round(point.shapeArgs.width / 2);
                var plotOpen = point.plotOpen;
                // crisp vector coordinates
                if (point.open !== null) {
                    plotOpen = Math.round(point.plotOpen) + crispCorr;
                    path.push(['M', crispX, plotOpen], ['L', crispX - halfWidth, plotOpen]);
                    _super.prototype.extendStem.call(this, path, strokeWidth / 2, plotOpen);
                }
                return path;
            };
            /**
             * Postprocess mapping between options and SVG attributes
             * @private
             */
            OHLCSeries.prototype.pointAttribs = function (point, state) {
                var attribs = _super.prototype.pointAttribs.call(this,
                    point,
                    state),
                    options = this.options;
                delete attribs.fill;
                if (!point.options.color &&
                    options.upColor &&
                    point.open < point.close) {
                    attribs.stroke = options.upColor;
                }
                return attribs;
            };
            OHLCSeries.prototype.toYData = function (point) {
                // return a plain array for speedy calculation
                return [point.open, point.high, point.low, point.close];
            };
            OHLCSeries.defaultOptions = merge(HLCSeries.defaultOptions, OHLCSeriesDefaults);
            return OHLCSeries;
        }(HLCSeries));
        extend(OHLCSeries.prototype, {
            pointClass: OHLCPoint,
            pointArrayMap: ['open', 'high', 'low', 'close']
        });
        SeriesRegistry.registerSeriesType('ohlc', OHLCSeries);
        /* *
         *
         *  Default Export
         *
         * */

        return OHLCSeries;
    });
    _registerModule(_modules, 'Series/Candlestick/CandlestickSeriesDefaults.js', [_modules['Core/Defaults.js'], _modules['Core/Utilities.js']], function (D, U) {
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
        var merge = U.merge;
        /* *
         *
         *  API Options
         *
         * */
        /**
         * A candlestick chart is a style of financial chart used to describe
         * price movements over time.
         *
         * @sample stock/demo/candlestick/
         *         Candlestick chart
         *
         * @extends      plotOptions.ohlc
         * @excluding    borderColor,borderRadius,borderWidth
         * @product      highstock
         * @optionparent plotOptions.candlestick
         */
        var CandlestickSeriesDefaults = {
                /**
                 * The specific line color for up candle sticks. The default is to
                 * inherit the general `lineColor` setting.
                 *
                 * @sample {highstock} stock/plotoptions/candlestick-linecolor/
                 *         Candlestick line colors
                 *
                 * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 * @since     1.3.6
                 * @product   highstock
                 * @apioption plotOptions.candlestick.upLineColor
                 */
                states: {
                    /**
                     * @extends plotOptions.column.states.hover
                     * @product highstock
                     */
                    hover: {
                        /**
                         * The pixel width of the line/border around the
                         * candlestick.
                         *
                         * @product highstock
                         */
                        lineWidth: 2
                    }
                },
                /**
                 * @type    {number|null}
                 * @product highstock
                 */
                threshold: null,
                /**
                 * The color of the line/border of the candlestick.
                 *
                 * In styled mode,
            the line stroke can be set with the
                 * `.highcharts-candlestick-series .highcahrts-point` rule.
                 *
                 * @see [upLineColor](#plotOptions.candlestick.upLineColor)
                 *
                 * @sample {highstock} stock/plotoptions/candlestick-linecolor/
                 *         Candlestick line colors
                 *
                 * @type    {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 * @default #000000
                 * @product highstock
                 */
                lineColor: "#000000" /* Palette.neutralColor100 */,
                /**
                 * The pixel width of the candlestick line/border. Defaults to `1`.
                 *
                 *
                 * In styled mode,
            the line stroke width can be set with the
                 * `.highcharts-candlestick-series .highcahrts-point` rule.
                 *
                 * @product highstock
                 */
                lineWidth: 1,
                /**
                 * The fill color of the candlestick when values are rising.
                 *
                 * In styled mode,
            the up color can be set with the
                 * `.highcharts-candlestick-series .highcharts-point-up` rule.
                 *
                 * @sample {highstock} stock/plotoptions/candlestick-color/
                 *         Custom colors
                 * @sample {highstock} highcharts/css/candlestick/
                 *         Colors in styled mode
                 *
                 * @type    {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 * @default #ffffff
                 * @product highstock
                */
                upColor: "#ffffff" /* Palette.backgroundColor */,
                /**
                 * @product highstock
                 */
                stickyTracking: true
            };
        /**
         * A `candlestick` series. If the [type](#series.candlestick.type)
         * option is not specified, it is inherited from [chart.type](
         * #chart.type).
         *
         * @type      {*}
         * @extends   series,plotOptions.candlestick
         * @excluding dataParser, dataURL, marker
         * @product   highstock
         * @apioption series.candlestick
         */
        /**
         * An array of data points for the series. For the `candlestick` series
         * type, points can be given in the following ways:
         *
         * 1. An array of arrays with 5 or 4 values. In this case, the values correspond
         *    to `x,open,high,low,close`. If the first value is a string, it is applied
         *    as the name of the point, and the `x` value is inferred. The `x` value can
         *    also be omitted, in which case the inner arrays should be of length 4.
         *    Then the `x` value is automatically calculated, either starting at 0 and
         *    incremented by 1, or from `pointStart` and `pointInterval` given in the
         *    series options.
         *    ```js
         *    data: [
         *        [0, 7, 2, 0, 4],
         *        [1, 1, 4, 2, 8],
         *        [2, 3, 3, 9, 3]
         *    ]
         *    ```
         *
         * 2. An array of objects with named values. The following snippet shows only a
         *    few settings, see the complete options set below. If the total number of
         *    data points exceeds the series'
         *    [turboThreshold](#series.candlestick.turboThreshold), this option is not
         *    available.
         *    ```js
         *    data: [{
         *        x: 1,
         *        open: 9,
         *        high: 2,
         *        low: 4,
         *        close: 6,
         *        name: "Point2",
         *        color: "#00FF00"
         *    }, {
         *        x: 1,
         *        open: 1,
         *        high: 4,
         *        low: 7,
         *        close: 7,
         *        name: "Point1",
         *        color: "#FF00FF"
         *    }]
         *    ```
         *
         * @type      {Array<Array<(number|string),number,number,number>|Array<(number|string),number,number,number,number>|*>}
         * @extends   series.ohlc.data
         * @excluding y
         * @product   highstock
         * @apioption series.candlestick.data
         */
        ''; // adds doclets above to transpilat
        /* *
         *
         *  Default Export
         *
         * */

        return CandlestickSeriesDefaults;
    });
    _registerModule(_modules, 'Series/Candlestick/CandlestickSeries.js', [_modules['Series/Candlestick/CandlestickSeriesDefaults.js'], _modules['Core/Defaults.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (CandlestickSeriesDefaults, D, SeriesRegistry, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
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
        var defaultOptions = D.defaultOptions;
        var _a = SeriesRegistry.seriesTypes,
            ColumnSeries = _a.column,
            OHLCSeries = _a.ohlc;
        var merge = U.merge;
        /* *
         *
         *  Class
         *
         * */
        /**
         * The candlestick series type.
         *
         * @private
         * @class
         * @name Highcharts.seriesTypes.candlestick
         *
         * @augments Highcharts.seriesTypes.ohlc
         */
        var CandlestickSeries = /** @class */ (function (_super) {
                __extends(CandlestickSeries, _super);
            function CandlestickSeries() {
                /* *
                 *
                 *  Static Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                /* *
                 *
                 *  Properties
                 *
                 * */
                _this.data = void 0;
                _this.options = void 0;
                _this.points = void 0;
                return _this;
            }
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Postprocess mapping between options and SVG attributes
             *
             * @private
             * @function Highcharts.seriesTypes.candlestick#pointAttribs
             */
            CandlestickSeries.prototype.pointAttribs = function (point, state) {
                var attribs = ColumnSeries.prototype.pointAttribs.call(this,
                    point,
                    state),
                    options = this.options,
                    isUp = point.open < point.close,
                    stroke = options.lineColor || this.color,
                    color = point.color || this.color; // (#14826)
                    attribs['stroke-width'] = options.lineWidth;
                attribs.fill = point.options.color ||
                    (isUp ? (options.upColor || color) : color);
                attribs.stroke = point.options.lineColor ||
                    (isUp ? (options.upLineColor || stroke) : stroke);
                // Select or hover states
                if (state) {
                    var stateOptions = options.states[state];
                    attribs.fill = stateOptions.color || attribs.fill;
                    attribs.stroke = stateOptions.lineColor || attribs.stroke;
                    attribs['stroke-width'] =
                        stateOptions.lineWidth || attribs['stroke-width'];
                }
                return attribs;
            };
            /**
             * Draw the data points.
             *
             * @private
             * @function Highcharts.seriesTypes.candlestick#drawPoints
             */
            CandlestickSeries.prototype.drawPoints = function () {
                var series = this,
                    points = series.points,
                    chart = series.chart,
                    reversedYAxis = series.yAxis.reversed;
                for (var _i = 0, points_1 = points; _i < points_1.length; _i++) {
                    var point = points_1[_i];
                    var graphic = point.graphic,
                        plotOpen = void 0,
                        plotClose = void 0,
                        topBox = void 0,
                        bottomBox = void 0,
                        hasTopWhisker = void 0,
                        hasBottomWhisker = void 0,
                        crispCorr = void 0,
                        crispX = void 0,
                        path = void 0,
                        halfWidth = void 0;
                    var isNew = !graphic;
                    if (typeof point.plotY !== 'undefined') {
                        if (!graphic) {
                            point.graphic = graphic = chart.renderer.path()
                                .add(series.group);
                        }
                        if (!series.chart.styledMode) {
                            graphic
                                .attr(series.pointAttribs(point, (point.selected && 'select'))) // #3897
                                .shadow(series.options.shadow);
                        }
                        // Crisp vector coordinates
                        crispCorr = (graphic.strokeWidth() % 2) / 2;
                        // #2596:
                        crispX = Math.round(point.plotX) - crispCorr;
                        plotOpen = point.plotOpen;
                        plotClose = point.plotClose;
                        topBox = Math.min(plotOpen, plotClose);
                        bottomBox = Math.max(plotOpen, plotClose);
                        halfWidth = Math.round(point.shapeArgs.width / 2);
                        hasTopWhisker = reversedYAxis ?
                            bottomBox !== point.yBottom :
                            Math.round(topBox) !==
                                Math.round(point.plotHigh);
                        hasBottomWhisker = reversedYAxis ?
                            Math.round(topBox) !==
                                Math.round(point.plotHigh) :
                            bottomBox !== point.yBottom;
                        topBox = Math.round(topBox) + crispCorr;
                        bottomBox = Math.round(bottomBox) + crispCorr;
                        // Create the path. Due to a bug in Chrome 49, the path is
                        // first instanciated with no values, then the values
                        // pushed. For unknown reasons, instanciating the path array
                        // with all the values would lead to a crash when updating
                        // frequently (#5193).
                        path = [];
                        path.push(['M', crispX - halfWidth, bottomBox], ['L', crispX - halfWidth, topBox], ['L', crispX + halfWidth, topBox], ['L', crispX + halfWidth, bottomBox], ['Z'], // Ensure a nice rectangle #2602
                        ['M', crispX, topBox], [
                            'L',
                            // #460, #2094
                            crispX,
                            hasTopWhisker ?
                                Math.round(reversedYAxis ?
                                    point.yBottom :
                                    point.plotHigh) :
                                topBox
                        ], ['M', crispX, bottomBox], [
                            'L',
                            // #460, #2094
                            crispX,
                            hasBottomWhisker ?
                                Math.round(reversedYAxis ?
                                    point.plotHigh :
                                    point.yBottom) :
                                bottomBox
                        ]);
                        graphic[isNew ? 'attr' : 'animate']({ d: path })
                            .addClass(point.getClassName(), true);
                    }
                }
            };
            CandlestickSeries.defaultOptions = merge(OHLCSeries.defaultOptions, defaultOptions.plotOptions, { tooltip: OHLCSeries.defaultOptions.tooltip }, CandlestickSeriesDefaults);
            return CandlestickSeries;
        }(OHLCSeries));
        SeriesRegistry.registerSeriesType('candlestick', CandlestickSeries);
        /* *
         *
         *  Default Export
         *
         * */

        return CandlestickSeries;
    });
    _registerModule(_modules, 'Series/Flags/FlagsPoint.js', [_modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (SeriesRegistry, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
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
        var ColumnPoint = SeriesRegistry.seriesTypes.column.prototype.pointClass;
        var isNumber = U.isNumber;
        /* *
         *
         *  Class
         *
         * */
        var FlagsPoint = /** @class */ (function (_super) {
                __extends(FlagsPoint, _super);
            function FlagsPoint() {
                /* *
                 *
                 *  Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.options = void 0;
                _this.series = void 0;
                _this.ttBelow = false;
                return _this;
            }
            /* *
             *
             *  Functions
             *
             * */
            /**
             * @private
             */
            FlagsPoint.prototype.isValid = function () {
                // #9233 - Prevent from treating flags as null points (even if
                // they have no y values defined).
                return isNumber(this.y) || typeof this.y === 'undefined';
            };
            /**
             * @private
             */
            FlagsPoint.prototype.hasNewShapeType = function () {
                var shape = this.options.shape || this.series.options.shape;
                return this.graphic && shape && shape !== this.graphic.symbolKey;
            };
            return FlagsPoint;
        }(ColumnPoint));
        /* *
         *
         *  Default Export
         *
         * */

        return FlagsPoint;
    });
    _registerModule(_modules, 'Series/Flags/FlagsSeriesDefaults.js', [], function () {
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
         *  API Options
         *
         * */
        /**
         * Flags are used to mark events in stock charts. They can be added on the
         * timeline, or attached to a specific series.
         *
         * @sample stock/demo/flags-general/
         *         Flags on a line series
         *
         * @extends      plotOptions.column
         * @excluding    animation, borderColor, borderRadius, borderWidth,
         *               colorByPoint, cropThreshold, dataGrouping, pointPadding,
         *               pointWidth, turboThreshold
         * @product      highstock
         * @optionparent plotOptions.flags
         */
        var FlagsSeriesDefaults = {
                /**
                 * In case the flag is placed on a series, on what point key to place
                 * it. Line and columns have one key, `y`. In range or OHLC-type series,
                 * however, the flag can optionally be placed on the `open`, `high`,
                 * `low` or `close` key.
                 *
                 * @sample {highstock} stock/plotoptions/flags-onkey/
                 *         Range series, flag on high
                 *
                 * @type       {string}
                 * @default    y
                 * @since      4.2.2
                 * @product    highstock
                 * @validvalue ["y", "open", "high", "low", "close"]
                 * @apioption  plotOptions.flags.onKey
                 */
                /**
                 * The id of the series that the flags should be drawn on. If no id
                 * is given, the flags are drawn on the x axis.
                 *
                 * @sample {highstock} stock/plotoptions/flags/
                 *         Flags on series and on x axis
                 *
                 * @type      {string}
                 * @product   highstock
                 * @apioption plotOptions.flags.onSeries
                 */
                pointRange: 0,
                /**
                 * Whether the flags are allowed to overlap sideways. If `false`, the
                 * flags are moved sideways using an algorithm that seeks to place every
                 * flag as close as possible to its original position.
                 *
                 * @sample {highstock} stock/plotoptions/flags-allowoverlapx
                 *         Allow sideways overlap
                 *
                 * @since 6.0.4
                 */
                allowOverlapX: false,
                /**
                 * The shape of the marker. Can be one of "flag", "circlepin",
                 * "squarepin", or an image of the format `url(/path-to-image.jpg)`.
                 * Individual shapes can also be set for each point.
                 *
                 * @sample {highstock} stock/plotoptions/flags/
                 *         Different shapes
                 *
                 * @type    {Highcharts.FlagsShapeValue}
                 * @product highstock
                 */
                shape: 'flag',
                /**
                 * When multiple flags in the same series fall on the same value, this
                 * number determines the vertical offset between them.
                 *
                 * @sample {highstock} stock/plotoptions/flags-stackdistance/
                 *         A greater stack distance
                 *
                 * @product highstock
                 */
                stackDistance: 12,
                /**
                 * Text alignment for the text inside the flag.
                 *
                 * @since      5.0.0
                 * @product    highstock
                 * @validvalue ["left", "center", "right"]
                 */
                textAlign: 'center',
                /**
                 * Specific tooltip options for flag series. Flag series tooltips are
                 * different from most other types in that a flag doesn't have a data
                 * value, so the tooltip rather displays the `text` option for each
                 * point.
                 *
                 * @extends   plotOptions.series.tooltip
                 * @excluding changeDecimals, valueDecimals, valuePrefix, valueSuffix
                 * @product   highstock
                 */
                tooltip: {
                    pointFormat: '{point.text}'
                },
                /**
                 * @type {number|null}
                 */
                threshold: null,
                /**
                 * The text to display on each flag. This can be defined on series
                 * level, or individually for each point. Defaults to `"A"`.
                 *
                 * @type      {string}
                 * @default   A
                 * @product   highstock
                 * @apioption plotOptions.flags.title
                 */
                /**
                 * The y position of the top left corner of the flag relative to either
                 * the series (if onSeries is defined), or the x axis. Defaults to
                 * `-30`.
                 *
                 * @product highstock
                 */
                y: -30,
                /**
                 * Whether to use HTML to render the flag texts. Using HTML allows for
                 * advanced formatting, images and reliable bi-directional text
                 * rendering. Note that exported images won't respect the HTML, and that
                 * HTML won't respect Z-index settings.
                 *
                 * @type      {boolean}
                 * @default   false
                 * @since     1.3
                 * @product   highstock
                 * @apioption plotOptions.flags.useHTML
                 */
                /**
                 * Fixed width of the flag's shape. By default, width is autocalculated
                 * according to the flag's title.
                 *
                 * @sample {highstock} stock/demo/flags-shapes/
                 *         Flags with fixed width
                 *
                 * @type      {number}
                 * @product   highstock
                 * @apioption plotOptions.flags.width
                 */
                /**
                 * Fixed height of the flag's shape. By default, height is
                 * autocalculated according to the flag's title.
                 *
                 * @type      {number}
                 * @product   highstock
                 * @apioption plotOptions.flags.height
                 */
                /**
                 * The fill color for the flags.
                 *
                 * @type    {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 * @product highstock
                 */
                fillColor: "#ffffff" /* Palette.backgroundColor */,
                /**
                 * The color of the line/border of the flag.
                 *
                 * In styled mode, the stroke is set in the
                 * `.highcharts-flag-series.highcharts-point` rule.
                 *
                 * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 * @default   #000000
                 * @product   highstock
                 * @apioption plotOptions.flags.lineColor
                 */
                /**
                 * The pixel width of the flag's line/border.
                 *
                 * @product highstock
                 */
                lineWidth: 1,
                states: {
                    /**
                     * @extends plotOptions.column.states.hover
                     * @product highstock
                     */
                    hover: {
                        /**
                         * The color of the line/border of the flag.
                         *
                         * @type    {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                         * @product highstock
                         */
                        lineColor: "#000000" /* Palette.neutralColor100 */,
                        /**
                         * The fill or background color of the flag.
                         *
                         * @type    {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                         * @product highstock
                         */
                        fillColor: "#ccd6eb" /* Palette.highlightColor20 */
                    }
                },
                /**
                 * The text styles of the flag.
                 *
                 * In styled mode, the styles are set in the
                 * `.highcharts-flag-series .highcharts-point` rule.
                 *
                 * @type    {Highcharts.CSSObject}
                 * @default {"fontSize": "11px", "fontWeight": "bold"}
                 * @product highstock
                 */
                style: {
                    /** @ignore-option */
                    fontSize: '11px',
                    /** @ignore-option */
                    fontWeight: 'bold'
                }
            };
        /**
         * A `flags` series. If the [type](#series.flags.type) option is not
         * specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.flags
         * @excluding animation, borderColor, borderRadius, borderWidth, colorByPoint,
         *            connectNulls, cropThreshold, dashStyle, dataGrouping, dataParser,
         *            dataURL, gapSize, gapUnit, linecap, lineWidth, marker,
         *            pointPadding, pointWidth, step, turboThreshold, useOhlcData
         * @product   highstock
         * @apioption series.flags
         */
        /**
         * An array of data points for the series. For the `flags` series type,
         * points can be given in the following ways:
         *
         * 1. An array of objects with named values. The following snippet shows only a
         *    few settings, see the complete options set below. If the total number of
         *    data points exceeds the series'
         *    [turboThreshold](#series.flags.turboThreshold), this option is not
         *    available.
         *    ```js
         *    data: [{
         *        x: 1,
         *        title: "A",
         *        text: "First event"
         *    }, {
         *        x: 1,
         *        title: "B",
         *        text: "Second event"
         *    }]
         *    ```
         *
         * @type      {Array<*>}
         * @extends   series.line.data
         * @excluding dataLabels, marker, name, y
         * @product   highstock
         * @apioption series.flags.data
         */
        /**
         * The fill color of an individual flag. By default it inherits from
         * the series color.
         *
         * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
         * @product   highstock
         * @apioption series.flags.data.fillColor
         */
        /**
         * The longer text to be shown in the flag's tooltip.
         *
         * @type      {string}
         * @product   highstock
         * @apioption series.flags.data.text
         */
        /**
         * The short text to be shown on the flag.
         *
         * @type      {string}
         * @product   highstock
         * @apioption series.flags.data.title
         */
        ''; // keeps doclets above in transpiled file
        /* *
         *
         *  Default Export
         *
         * */

        return FlagsSeriesDefaults;
    });
    _registerModule(_modules, 'Series/Flags/FlagsSymbols.js', [_modules['Core/Renderer/RendererRegistry.js']], function (RendererRegistry) {
        /* *
         *
         *  Imports
         *
         * */
        /* *
         *
         *  Composition
         *
         * */
        var FlagsSymbols;
        (function (FlagsSymbols) {
            /* *
             *
             *  Constants
             *
             * */
            var modifiedMembers = [];
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * @private
             */
            function compose(SVGRendererClass) {
                if (modifiedMembers.indexOf(SVGRendererClass) === -1) {
                    modifiedMembers.push(SVGRendererClass);
                    var symbols = SVGRendererClass.prototype.symbols;
                    symbols.flag = flag;
                    createPinSymbol(symbols, 'circle');
                    createPinSymbol(symbols, 'square');
                }
                var RendererClass = RendererRegistry.getRendererType();
                // The symbol callbacks are generated on the SVGRenderer object in all
                // browsers. Even VML browsers need this in order to generate shapes in
                // export. Now share them with the VMLRenderer.
                if (modifiedMembers.indexOf(RendererClass)) {
                    modifiedMembers.push(RendererClass);
                    var symbols = SVGRendererClass.prototype.symbols,
                        vmlSymbols = RendererClass.prototype.symbols;
                    vmlSymbols.circlepin = symbols.circlepin;
                    vmlSymbols.flag = symbols.flag.bind(symbols);
                    vmlSymbols.squarepin = symbols.squarepin;
                }
            }
            FlagsSymbols.compose = compose;
            /**
             * Create the flag icon with anchor.
             * @private
             */
            function flag(x, y, w, h, options) {
                var anchorX = (options && options.anchorX) || x,
                    anchorY = (options && options.anchorY) || y;
                // To do: unwanted any cast because symbols.circle has wrong type, it
                // actually returns an SVGPathArray
                var path = this.circle(anchorX - 1,
                    anchorY - 1, 2, 2);
                path.push(['M', anchorX, anchorY], ['L', x, y + h], ['L', x, y], ['L', x + w, y], ['L', x + w, y + h], ['L', x, y + h], ['Z']);
                return path;
            }
            /**
             * Create the circlepin and squarepin icons with anchor.
             * @private
             */
            function createPinSymbol(symbols, shape) {
                symbols[(shape + 'pin')] = function (x, y, w, h, options) {
                    var anchorX = options && options.anchorX,
                        anchorY = options && options.anchorY;
                    var path;
                    // For single-letter flags, make sure circular flags are not taller
                    // than their width
                    if (shape === 'circle' && h > w) {
                        x -= Math.round((h - w) / 2);
                        w = h;
                    }
                    path = (symbols[shape])(x, y, w, h);
                    if (anchorX && anchorY) {
                        /**
                         * If the label is below the anchor, draw the connecting line
                         * from the top edge of the label, otherwise start drawing from
                         * the bottom edge
                         */
                        var labelX = anchorX;
                        if (shape === 'circle') {
                            labelX = x + w / 2;
                        }
                        else {
                            var startSeg = path[0];
                            var endSeg = path[1];
                            if (startSeg[0] === 'M' && endSeg[0] === 'L') {
                                labelX = (startSeg[1] + endSeg[1]) / 2;
                            }
                        }
                        var labelY = (y > anchorY) ? y : y + h;
                        path.push([
                            'M',
                            labelX,
                            labelY
                        ], [
                            'L',
                            anchorX,
                            anchorY
                        ]);
                        path = path.concat(symbols.circle(anchorX - 1, anchorY - 1, 2, 2));
                    }
                    return path;
                };
            }
        })(FlagsSymbols || (FlagsSymbols = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return FlagsSymbols;
    });
    _registerModule(_modules, 'Series/OnSeriesComposition.js', [_modules['Series/Column/ColumnSeries.js'], _modules['Core/Series/Series.js'], _modules['Core/Utilities.js']], function (ColumnSeries, Series, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var columnProto = ColumnSeries.prototype;
        var seriesProto = Series.prototype;
        var defined = U.defined,
            stableSort = U.stableSort;
        /* *
         *
         *  Composition
         *
         * */
        var OnSeriesComposition;
        (function (OnSeriesComposition) {
            /* *
             *
             *  Declarations
             *
             * */
            /* *
             *
             *  Properties
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
                    var seriesProto_1 = SeriesClass.prototype;
                    seriesProto_1.getPlotBox = getPlotBox;
                    seriesProto_1.translate = translate;
                }
                return SeriesClass;
            }
            OnSeriesComposition.compose = compose;
            /**
             * Override getPlotBox. If the onSeries option is valid, return the plot box
             * of the onSeries, otherwise proceed as usual.
             *
             * @private
             */
            function getPlotBox(name) {
                return seriesProto.getPlotBox.call((this.options.onSeries &&
                    this.chart.get(this.options.onSeries)) || this, name);
            }
            OnSeriesComposition.getPlotBox = getPlotBox;
            /**
             * Extend the translate method by placing the point on the related series
             *
             * @private
             */
            function translate() {
                columnProto.translate.apply(this);
                var series = this,
                    options = series.options,
                    chart = series.chart,
                    points = series.points,
                    optionsOnSeries = options.onSeries,
                    onSeries = (optionsOnSeries &&
                        chart.get(optionsOnSeries)),
                    step = onSeries && onSeries.options.step,
                    onData = (onSeries && onSeries.points),
                    inverted = chart.inverted,
                    xAxis = series.xAxis,
                    yAxis = series.yAxis;
                var cursor = points.length - 1,
                    point,
                    lastPoint,
                    onKey = options.onKey || 'y',
                    i = onData && onData.length,
                    xOffset = 0,
                    leftPoint,
                    lastX,
                    rightPoint,
                    currentDataGrouping,
                    distanceRatio;
                // relate to a master series
                if (onSeries && onSeries.visible && i) {
                    xOffset = (onSeries.pointXOffset || 0) + (onSeries.barW || 0) / 2;
                    currentDataGrouping = onSeries.currentDataGrouping;
                    lastX = (onData[i - 1].x +
                        (currentDataGrouping ? currentDataGrouping.totalRange : 0)); // #2374
                    // sort the data points
                    stableSort(points, function (a, b) { return (a.x - b.x); });
                    onKey = 'plot' + onKey[0].toUpperCase() + onKey.substr(1);
                    while (i-- && points[cursor]) {
                        leftPoint = onData[i];
                        point = points[cursor];
                        point.y = leftPoint.y;
                        if (leftPoint.x <= point.x &&
                            typeof leftPoint[onKey] !== 'undefined') {
                            if (point.x <= lastX) { // #803
                                point.plotY = leftPoint[onKey];
                                // interpolate between points, #666
                                if (leftPoint.x < point.x &&
                                    !step) {
                                    rightPoint = onData[i + 1];
                                    if (rightPoint &&
                                        typeof rightPoint[onKey] !== 'undefined') {
                                        // the distance ratio, between 0 and 1
                                        distanceRatio =
                                            (point.x - leftPoint.x) /
                                                (rightPoint.x - leftPoint.x);
                                        point.plotY +=
                                            distanceRatio *
                                                // the plotY distance
                                                (rightPoint[onKey] - leftPoint[onKey]);
                                        point.y +=
                                            distanceRatio *
                                                (rightPoint.y - leftPoint.y);
                                    }
                                }
                            }
                            cursor--;
                            i++; // check again for points in the same x position
                            if (cursor < 0) {
                                break;
                            }
                        }
                    }
                }
                // Add plotY position and handle stacking
                points.forEach(function (point, i) {
                    var stackIndex;
                    point.plotX += xOffset; // #2049
                    // Undefined plotY means the point is either on axis, outside series
                    // range or hidden series. If the series is outside the range of the
                    // x axis it should fall through with an undefined plotY, but then
                    // we must remove the shapeArgs (#847). For inverted charts, we need
                    // to calculate position anyway, because series.invertGroups is not
                    // defined
                    if (typeof point.plotY === 'undefined' || inverted) {
                        if (point.plotX >= 0 &&
                            point.plotX <= xAxis.len) {
                            // We're inside xAxis range
                            if (inverted) {
                                point.plotY = xAxis.translate(point.x, 0, 1, 0, 1);
                                point.plotX = defined(point.y) ?
                                    yAxis.translate(point.y, 0, 0, 0, 1) :
                                    0;
                            }
                            else {
                                point.plotY = (xAxis.opposite ? 0 : series.yAxis.len) +
                                    xAxis.offset; // For the windbarb demo
                            }
                        }
                        else {
                            point.shapeArgs = {}; // 847
                        }
                    }
                    // if multiple flags appear at the same x, order them into a stack
                    lastPoint = points[i - 1];
                    if (lastPoint && lastPoint.plotX === point.plotX) {
                        if (typeof lastPoint.stackIndex === 'undefined') {
                            lastPoint.stackIndex = 0;
                        }
                        stackIndex = lastPoint.stackIndex + 1;
                    }
                    point.stackIndex = stackIndex; // #3639
                });
                this.onSeries = onSeries;
            }
            OnSeriesComposition.translate = translate;
        })(OnSeriesComposition || (OnSeriesComposition = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return OnSeriesComposition;
    });
    _registerModule(_modules, 'Series/Flags/FlagsSeries.js', [_modules['Series/Flags/FlagsPoint.js'], _modules['Series/Flags/FlagsSeriesDefaults.js'], _modules['Series/Flags/FlagsSymbols.js'], _modules['Core/Globals.js'], _modules['Series/OnSeriesComposition.js'], _modules['Core/Renderer/RendererUtilities.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Renderer/SVG/SVGElement.js'], _modules['Core/Utilities.js']], function (FlagsPoint, FlagsSeriesDefaults, FlagsSymbols, H, OnSeriesComposition, R, SeriesRegistry, SVGElement, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
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
        var noop = H.noop;
        var distribute = R.distribute;
        var Series = SeriesRegistry.series,
            ColumnSeries = SeriesRegistry.seriesTypes.column;
        var addEvent = U.addEvent,
            defined = U.defined,
            extend = U.extend,
            merge = U.merge,
            objectEach = U.objectEach,
            wrap = U.wrap;
        /* *
         *
         *  Classes
         *
         * */
        /**
         * The Flags series.
         *
         * @private
         * @class
         * @name Highcharts.seriesTypes.flags
         *
         * @augments Highcharts.Series
         */
        var FlagsSeries = /** @class */ (function (_super) {
                __extends(FlagsSeries, _super);
            function FlagsSeries() {
                /* *
                 *
                 *  Static Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                /* *
                 *
                 *  Properties
                 *
                 * */
                _this.data = void 0;
                _this.options = void 0;
                _this.points = void 0;
                return _this;
            }
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Disable animation, but keep clipping (#8546).
             * @private
             */
            FlagsSeries.prototype.animate = function (init) {
                if (init) {
                    this.setClip();
                }
            };
            /**
             * Draw the markers.
             * @private
             */
            FlagsSeries.prototype.drawPoints = function () {
                var series = this,
                    points = series.points,
                    chart = series.chart,
                    renderer = chart.renderer,
                    inverted = chart.inverted,
                    options = series.options,
                    optionsY = options.y,
                    yAxis = series.yAxis,
                    boxesMap = {},
                    boxes = [];
                var plotX,
                    plotY,
                    shape,
                    i,
                    point,
                    graphic,
                    stackIndex,
                    anchorY,
                    attribs,
                    outsideRight,
                    centered;
                i = points.length;
                while (i--) {
                    point = points[i];
                    outsideRight =
                        (inverted ? point.plotY : point.plotX) >
                            series.xAxis.len;
                    plotX = point.plotX;
                    stackIndex = point.stackIndex;
                    shape = point.options.shape || options.shape;
                    plotY = point.plotY;
                    if (typeof plotY !== 'undefined') {
                        plotY = point.plotY + optionsY -
                            (typeof stackIndex !== 'undefined' &&
                                (stackIndex * options.stackDistance));
                    }
                    // skip connectors for higher level stacked points
                    point.anchorX = stackIndex ? void 0 : point.plotX;
                    anchorY = stackIndex ? void 0 : point.plotY;
                    centered = shape !== 'flag';
                    graphic = point.graphic;
                    // Only draw the point if y is defined and the flag is within
                    // the visible area
                    if (typeof plotY !== 'undefined' &&
                        plotX >= 0 &&
                        !outsideRight) {
                        // #15384
                        if (graphic && point.hasNewShapeType()) {
                            graphic = graphic.destroy();
                        }
                        // Create the flag
                        if (!graphic) {
                            graphic = point.graphic = renderer.label('', null, null, shape, null, null, options.useHTML)
                                .addClass('highcharts-point')
                                .add(series.markerGroup);
                            // Add reference to the point for tracker (#6303)
                            if (point.graphic.div) {
                                point.graphic.div.point = point;
                            }
                            graphic.isNew = true;
                        }
                        graphic.attr({
                            align: centered ? 'center' : 'left',
                            width: options.width,
                            height: options.height,
                            'text-align': options.textAlign
                        });
                        if (!chart.styledMode) {
                            graphic
                                .attr(series.pointAttribs(point))
                                .css(merge(options.style, point.style))
                                .shadow(options.shadow);
                        }
                        if (plotX > 0) { // #3119
                            plotX -= graphic.strokeWidth() % 2; // #4285
                        }
                        // Plant the flag
                        attribs = {
                            y: plotY,
                            anchorY: anchorY
                        };
                        if (options.allowOverlapX) {
                            attribs.x = plotX;
                            attribs.anchorX = point.anchorX;
                        }
                        graphic.attr({
                            text: point.options.title || options.title || 'A'
                        })[graphic.isNew ? 'attr' : 'animate'](attribs);
                        // Rig for the distribute function
                        if (!options.allowOverlapX) {
                            if (!boxesMap[point.plotX]) {
                                boxesMap[point.plotX] = {
                                    align: centered ? 0.5 : 0,
                                    size: graphic.width,
                                    target: plotX,
                                    anchorX: plotX
                                };
                            }
                            else {
                                boxesMap[point.plotX].size = Math.max(boxesMap[point.plotX].size, graphic.width);
                            }
                        }
                        // Set the tooltip anchor position
                        point.tooltipPos = [
                            plotX,
                            plotY + yAxis.pos - chart.plotTop
                        ]; // #6327
                    }
                    else if (graphic) {
                        point.graphic = graphic.destroy();
                    }
                }
                // Handle X-dimension overlapping
                if (!options.allowOverlapX) {
                    var maxDistance_1 = 100;
                    objectEach(boxesMap, function (box) {
                        box.plotX = box.anchorX;
                        boxes.push(box);
                        maxDistance_1 = Math.max(box.size, maxDistance_1);
                    });
                    // If necessary (for overlapping or long labels)  distribute it
                    // depending on the label width or a hardcoded value, #16041.
                    distribute(boxes, inverted ? yAxis.len : this.xAxis.len, maxDistance_1);
                    for (var _i = 0, points_1 = points; _i < points_1.length; _i++) {
                        var point_1 = points_1[_i];
                        var plotX_1 = point_1.plotX,
                            graphic_1 = point_1.graphic,
                            box = graphic_1 && boxesMap[plotX_1];
                        if (box && graphic_1) {
                            // Hide flag when its box position is not specified
                            // (#8573, #9299)
                            if (!defined(box.pos)) {
                                graphic_1.hide().isNew = true;
                            }
                            else {
                                graphic_1[graphic_1.isNew ? 'attr' : 'animate']({
                                    x: box.pos + (box.align || 0) * box.size,
                                    anchorX: point_1.anchorX
                                }).show().isNew = false;
                            }
                        }
                    }
                }
                // Can be a mix of SVG and HTML and we need events for both (#6303)
                if (options.useHTML && series.markerGroup) {
                    wrap(series.markerGroup, 'on', function (proceed) {
                        return SVGElement.prototype.on.apply(
                        // for HTML
                        // eslint-disable-next-line no-invalid-this
                        proceed.apply(this, [].slice.call(arguments, 1)), 
                        // and for SVG
                        [].slice.call(arguments, 1));
                    });
                }
            };
            /**
             * Extend the column trackers with listeners to expand and contract
             * stacks.
             * @private
             */
            FlagsSeries.prototype.drawTracker = function () {
                var series = this,
                    points = series.points;
                _super.prototype.drawTracker.call(this);
                var _loop_1 = function (point) {
                        var graphic = point.graphic;
                    if (graphic) {
                        if (point.unbindMouseOver) {
                            point.unbindMouseOver();
                        }
                        point.unbindMouseOver = addEvent(graphic.element, 'mouseover', function () {
                            // Raise this point
                            if (point.stackIndex > 0 &&
                                !point.raised) {
                                point._y = graphic.y;
                                graphic.attr({
                                    y: point._y - 8
                                });
                                point.raised = true;
                            }
                            // Revert other raised points
                            for (var _i = 0, points_3 = points; _i < points_3.length; _i++) {
                                var otherPoint = points_3[_i];
                                if (otherPoint !== point &&
                                    otherPoint.raised &&
                                    otherPoint.graphic) {
                                    otherPoint.graphic.attr({
                                        y: otherPoint._y
                                    });
                                    otherPoint.raised = false;
                                }
                            }
                        });
                    }
                };
                /* *
                * Bring each stacked flag up on mouse over, this allows readability
                * of vertically stacked elements as well as tight points on the x
                * axis. #1924.
                */
                for (var _i = 0, points_2 = points; _i < points_2.length; _i++) {
                    var point = points_2[_i];
                    _loop_1(point);
                }
            };
            /**
             * Get presentational attributes
             * @private
             */
            FlagsSeries.prototype.pointAttribs = function (point, state) {
                var options = this.options,
                    color = (point && point.color) || this.color;
                var lineColor = options.lineColor,
                    lineWidth = (point && point.lineWidth),
                    fill = (point && point.fillColor) || options.fillColor;
                if (state) {
                    fill = options.states[state].fillColor;
                    lineColor = options.states[state].lineColor;
                    lineWidth = options.states[state].lineWidth;
                }
                return {
                    fill: fill || color,
                    stroke: lineColor || color,
                    'stroke-width': lineWidth || options.lineWidth || 0
                };
            };
            /**
             * @private
             */
            FlagsSeries.prototype.setClip = function () {
                Series.prototype.setClip.apply(this, arguments);
                if (this.options.clip !== false &&
                    this.sharedClipKey &&
                    this.markerGroup) {
                    this.markerGroup.clip(this.chart.sharedClips[this.sharedClipKey]);
                }
            };
            FlagsSeries.compose = FlagsSymbols.compose;
            FlagsSeries.defaultOptions = merge(ColumnSeries.defaultOptions, FlagsSeriesDefaults);
            return FlagsSeries;
        }(ColumnSeries));
        OnSeriesComposition.compose(FlagsSeries);
        extend(FlagsSeries.prototype, {
            allowDG: false,
            forceCrop: true,
            invertible: false,
            noSharedTooltip: true,
            pointClass: FlagsPoint,
            sorted: false,
            takeOrdinalPosition: false,
            trackerGroups: ['markerGroup'],
            buildKDTree: noop,
            /**
             * Inherit the initialization from base Series.
             * @private
             */
            init: Series.prototype.init
        });
        SeriesRegistry.registerSeriesType('flags', FlagsSeries);
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
         * @typedef {"circlepin"|"flag"|"squarepin"} Highcharts.FlagsShapeValue
         */
        ''; // detach doclets above

        return FlagsSeries;
    });
    _registerModule(_modules, 'Core/Chart/StockChart.js', [_modules['Core/Axis/Axis.js'], _modules['Core/Chart/Chart.js'], _modules['Core/FormatUtilities.js'], _modules['Core/Defaults.js'], _modules['Stock/Navigator/NavigatorDefaults.js'], _modules['Stock/RangeSelector/RangeSelectorDefaults.js'], _modules['Stock/Scrollbar/ScrollbarDefaults.js'], _modules['Core/Series/Series.js'], _modules['Core/Renderer/SVG/SVGRenderer.js'], _modules['Core/Utilities.js']], function (Axis, Chart, F, D, NavigatorDefaults, RangeSelectorDefaults, ScrollbarDefaults, Series, SVGRenderer, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
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
        var format = F.format;
        var getOptions = D.getOptions;
        var addEvent = U.addEvent,
            clamp = U.clamp,
            defined = U.defined,
            extend = U.extend,
            find = U.find,
            isNumber = U.isNumber,
            isString = U.isString,
            merge = U.merge,
            pick = U.pick,
            splat = U.splat;
        /* *
         *
         *  Class
         *
         * */
        /**
         * Stock-optimized chart. Use {@link Highcharts.Chart|Chart} for common charts.
         *
         * @requires modules/stock
         *
         * @class
         * @name Highcharts.StockChart
         * @extends Highcharts.Chart
         */
        var StockChart = /** @class */ (function (_super) {
                __extends(StockChart, _super);
            function StockChart() {
                return _super !== null && _super.apply(this, arguments) || this;
            }
            /**
             * Initializes the chart. The constructor's arguments are passed on
             * directly.
             *
             * @function Highcharts.StockChart#init
             *
             * @param {Highcharts.Options} userOptions
             *        Custom options.
             *
             * @param {Function} [callback]
             *        Function to run when the chart has loaded and and all external
             *        images are loaded.
             *
             *
             * @emits Highcharts.StockChart#event:init
             * @emits Highcharts.StockChart#event:afterInit
             */
            StockChart.prototype.init = function (userOptions, callback) {
                var defaultOptions = getOptions(),
                    xAxisOptions = userOptions.xAxis,
                    yAxisOptions = userOptions.yAxis, 
                    // Always disable startOnTick:true on the main axis when the
                    // navigator is enabled (#1090)
                    navigatorEnabled = pick(userOptions.navigator && userOptions.navigator.enabled,
                    NavigatorDefaults.enabled,
                    true);
                // Avoid doing these twice
                userOptions.xAxis = userOptions.yAxis = void 0;
                var options = merge({
                        chart: {
                            panning: {
                                enabled: true,
                                type: 'x'
                            },
                            zooming: {
                                pinchType: 'x'
                            }
                        },
                        navigator: {
                            enabled: navigatorEnabled
                        },
                        scrollbar: {
                            // #4988 - check if setOptions was called
                            enabled: pick(ScrollbarDefaults.enabled,
                    true)
                        },
                        rangeSelector: {
                            // #4988 - check if setOptions was called
                            enabled: pick(RangeSelectorDefaults.rangeSelector.enabled,
                    true)
                        },
                        title: {
                            text: null
                        },
                        tooltip: {
                            split: pick(defaultOptions.tooltip.split,
                    true),
                            crosshairs: true
                        },
                        legend: {
                            enabled: false
                        }
                    },
                    userOptions, // user's options
                    {
                        isStock: true // internal flag
                    });
                userOptions.xAxis = xAxisOptions;
                userOptions.yAxis = yAxisOptions;
                // apply X axis options to both single and multi y axes
                options.xAxis = splat(userOptions.xAxis || {}).map(function (xAxisOptions, i) {
                    return merge(getDefaultAxisOptions('xAxis', xAxisOptions), defaultOptions.xAxis, // #3802
                    // #7690
                    defaultOptions.xAxis && defaultOptions.xAxis[i], xAxisOptions, // user options
                    getForcedAxisOptions('xAxis', userOptions));
                });
                // apply Y axis options to both single and multi y axes
                options.yAxis = splat(userOptions.yAxis || {}).map(function (yAxisOptions, i) {
                    return merge(getDefaultAxisOptions('yAxis', yAxisOptions), defaultOptions.yAxis, // #3802
                    // #7690
                    defaultOptions.yAxis && defaultOptions.yAxis[i], yAxisOptions // user options
                    );
                });
                _super.prototype.init.call(this, options, callback);
            };
            /**
             * Factory for creating different axis types.
             * Extended to add stock defaults.
             *
             * @private
             * @function Highcharts.StockChart#createAxis
             * @param {string} type
             * An axis type.
             * @param {Chart.CreateAxisOptionsObject} options
             * The axis creation options.
             */
            StockChart.prototype.createAxis = function (type, options) {
                options.axis = merge(getDefaultAxisOptions(type, options.axis), options.axis, getForcedAxisOptions(type, this.userOptions));
                return _super.prototype.createAxis.call(this, type, options);
            };
            return StockChart;
        }(Chart));
        /* eslint-disable no-invalid-this, valid-jsdoc */
        (function (StockChart) {
            /**
             * Factory function for creating new stock charts. Creates a new
             * {@link Highcharts.StockChart|StockChart} object with different default
             * options than the basic Chart.
             *
             * @example
             * let chart = Highcharts.stockChart('container', {
             *     series: [{
             *         data: [1, 2, 3, 4, 5, 6, 7, 8, 9],
             *         pointInterval: 24 * 60 * 60 * 1000
             *     }]
             * });
             *
             * @function Highcharts.stockChart
             *
             * @param {string|Highcharts.HTMLDOMElement} [renderTo]
             *        The DOM element to render to, or its id.
             *
             * @param {Highcharts.Options} options
             *        The chart options structure as described in the
             *        [options reference](https://api.highcharts.com/highstock).
             *
             * @param {Highcharts.ChartCallbackFunction} [callback]
             *        A function to execute when the chart object is finished loading
             *        and rendering. In most cases the chart is built in one thread,
             *        but in Internet Explorer version 8 or less the chart is sometimes
             *        initialized before the document is ready, and in these cases the
             *        chart object will not be finished synchronously. As a
             *        consequence, code that relies on the newly built Chart object
             *        should always run in the callback. Defining a
             *        [chart.events.load](https://api.highcharts.com/highstock/chart.events.load)
             *        handler is equivalent.
             *
             * @return {Highcharts.StockChart}
             *         The chart object.
             */
            function stockChart(a, b, c) {
                return new StockChart(a, b, c);
            }
            StockChart.stockChart = stockChart;
        })(StockChart || (StockChart = {}));
        /**
         * Get stock-specific default axis options.
         *
         * @private
         * @function getDefaultAxisOptions
         */
        function getDefaultAxisOptions(type, options) {
            if (type === 'xAxis') {
                return {
                    minPadding: 0,
                    maxPadding: 0,
                    overscroll: 0,
                    ordinal: true,
                    title: {
                        text: null
                    },
                    labels: {
                        overflow: 'justify'
                    },
                    showLastLabel: true
                };
            }
            if (type === 'yAxis') {
                return {
                    labels: {
                        y: -2
                    },
                    opposite: pick(options.opposite, true),
                    showLastLabel: !!(
                    // #6104, show last label by default for category axes
                    options.categories ||
                        options.type === 'category'),
                    title: {
                        text: null
                    }
                };
            }
            return {};
        }
        /**
         * Get stock-specific forced axis options.
         *
         * @private
         * @function getForcedAxisOptions
         */
        function getForcedAxisOptions(type, chartOptions) {
            if (type === 'xAxis') {
                // Always disable startOnTick:true on the main axis when the navigator
                // is enabled (#1090)
                var navigatorEnabled = pick(chartOptions.navigator && chartOptions.navigator.enabled,
                    NavigatorDefaults.enabled,
                    true);
                var axisOptions = {
                        type: 'datetime',
                        categories: void 0
                    };
                if (navigatorEnabled) {
                    axisOptions.startOnTick = false;
                    axisOptions.endOnTick = false;
                }
                return axisOptions;
            }
            return {};
        }
        /* *
         *
         *  Compositions
         *
         * */
        // Handle som Stock-specific series defaults, override the plotOptions before
        // series options are handled.
        addEvent(Series, 'setOptions', function (e) {
            var overrides;
            if (this.chart.options.isStock) {
                if (this.is('column') || this.is('columnrange')) {
                    overrides = {
                        borderWidth: 0,
                        shadow: false
                    };
                }
                else if (!this.is('scatter') && !this.is('sma')) {
                    overrides = {
                        marker: {
                            enabled: false,
                            radius: 2
                        }
                    };
                }
                if (overrides) {
                    e.plotOptions[this.type] = merge(e.plotOptions[this.type], overrides);
                }
            }
        });
        // Override the automatic label alignment so that the first Y axis' labels
        // are drawn on top of the grid line, and subsequent axes are drawn outside
        addEvent(Axis, 'autoLabelAlign', function (e) {
            var chart = this.chart,
                options = this.options,
                panes = chart._labelPanes = chart._labelPanes || {},
                key,
                labelOptions = this.options.labels;
            if (this.chart.options.isStock && this.coll === 'yAxis') {
                key = options.top + ',' + options.height;
                // do it only for the first Y axis of each pane
                if (!panes[key] && labelOptions.enabled) {
                    if (labelOptions.x === 15) { // default
                        labelOptions.x = 0;
                    }
                    if (typeof labelOptions.align === 'undefined') {
                        labelOptions.align = 'right';
                    }
                    panes[key] = this;
                    e.align = 'right';
                    e.preventDefault();
                }
            }
        });
        // Clear axis from label panes (#6071)
        addEvent(Axis, 'destroy', function () {
            var chart = this.chart, key = this.options && (this.options.top + ',' + this.options.height);
            if (key && chart._labelPanes && chart._labelPanes[key] === this) {
                delete chart._labelPanes[key];
            }
        });
        // Override getPlotLinePath to allow for multipane charts
        addEvent(Axis, 'getPlotLinePath', function (e) {
            var axis = this,
                series = (this.isLinked && !this.series ?
                    this.linkedParent.series :
                    this.series),
                chart = axis.chart,
                renderer = chart.renderer,
                axisLeft = axis.left,
                axisTop = axis.top,
                x1,
                y1,
                x2,
                y2,
                result = [],
                axes = [], // #3416 need a default array
                axes2,
                uniqueAxes,
                translatedValue = e.translatedValue,
                value = e.value,
                force = e.force,
                transVal;
            /**
             * Return the other axis based on either the axis option or on related
             * series.
             * @private
             */
            function getAxis(coll) {
                var otherColl = coll === 'xAxis' ? 'yAxis' : 'xAxis',
                    opt = axis.options[otherColl];
                // Other axis indexed by number
                if (isNumber(opt)) {
                    return [chart[otherColl][opt]];
                }
                // Other axis indexed by id (like navigator)
                if (isString(opt)) {
                    return [chart.get(opt)];
                }
                // Auto detect based on existing series
                return series.map(function (s) {
                    return s[otherColl];
                });
            }
            if ( // For stock chart, by default render paths across the panes
            // except the case when `acrossPanes` is disabled by user (#6644)
            (chart.options.isStock && e.acrossPanes !== false) &&
                // Ignore in case of colorAxis or zAxis. #3360, #3524, #6720
                axis.coll === 'xAxis' || axis.coll === 'yAxis') {
                e.preventDefault();
                // Get the related axes based on series
                axes = getAxis(axis.coll);
                // Get the related axes based options.*Axis setting #2810
                axes2 = (axis.isXAxis ? chart.yAxis : chart.xAxis);
                axes2.forEach(function (A) {
                    if (defined(A.options.id) ?
                        A.options.id.indexOf('navigator') === -1 :
                        true) {
                        var a = (A.isXAxis ? 'yAxis' : 'xAxis'),
                            rax = (defined(A.options[a]) ?
                                chart[a][A.options[a]] :
                                chart[a][0]);
                        if (axis === rax) {
                            axes.push(A);
                        }
                    }
                });
                // Remove duplicates in the axes array. If there are no axes in the axes
                // array, we are adding an axis without data, so we need to populate
                // this with grid lines (#2796).
                uniqueAxes = axes.length ?
                    [] :
                    [axis.isXAxis ? chart.yAxis[0] : chart.xAxis[0]]; // #3742
                axes.forEach(function (axis2) {
                    if (uniqueAxes.indexOf(axis2) === -1 &&
                        // Do not draw on axis which overlap completely. #5424
                        !find(uniqueAxes, function (unique) {
                            return unique.pos === axis2.pos && unique.len === axis2.len;
                        })) {
                        uniqueAxes.push(axis2);
                    }
                });
                transVal = pick(translatedValue, axis.translate(value, void 0, void 0, e.old));
                if (isNumber(transVal)) {
                    if (axis.horiz) {
                        uniqueAxes.forEach(function (axis2) {
                            var skip;
                            y1 = axis2.pos;
                            y2 = y1 + axis2.len;
                            x1 = x2 = Math.round(transVal + axis.transB);
                            // outside plot area
                            if (force !== 'pass' &&
                                (x1 < axisLeft || x1 > axisLeft + axis.width)) {
                                if (force) {
                                    x1 = x2 = clamp(x1, axisLeft, axisLeft + axis.width);
                                }
                                else {
                                    skip = true;
                                }
                            }
                            if (!skip) {
                                result.push(['M', x1, y1], ['L', x2, y2]);
                            }
                        });
                    }
                    else {
                        uniqueAxes.forEach(function (axis2) {
                            var skip;
                            x1 = axis2.pos;
                            x2 = x1 + axis2.len;
                            y1 = y2 = Math.round(axisTop + axis.height - transVal);
                            // outside plot area
                            if (force !== 'pass' &&
                                (y1 < axisTop || y1 > axisTop + axis.height)) {
                                if (force) {
                                    y1 = y2 = clamp(y1, axisTop, axisTop + axis.height);
                                }
                                else {
                                    skip = true;
                                }
                            }
                            if (!skip) {
                                result.push(['M', x1, y1], ['L', x2, y2]);
                            }
                        });
                    }
                }
                e.path = result.length > 0 ?
                    renderer.crispPolyLine(result, e.lineWidth || 1) :
                    // #3557 getPlotLinePath in regular Highcharts also returns null
                    null;
            }
        });
        /**
         * Function to crisp a line with multiple segments
         *
         * @private
         * @function Highcharts.SVGRenderer#crispPolyLine
         */
        SVGRenderer.prototype.crispPolyLine = function (points, width) {
            // points format: [['M', 0, 0], ['L', 100, 0]]
            // normalize to a crisp line
            for (var i = 0; i < points.length; i = i + 2) {
                var start = points[i],
                    end = points[i + 1];
                if (start[1] === end[1]) {
                    // Substract due to #1129. Now bottom and left axis gridlines behave
                    // the same.
                    start[1] = end[1] =
                        Math.round(start[1]) - (width % 2 / 2);
                }
                if (start[2] === end[2]) {
                    start[2] = end[2] =
                        Math.round(start[2]) + (width % 2 / 2);
                }
            }
            return points;
        };
        // Wrapper to hide the label
        addEvent(Axis, 'afterHideCrosshair', function () {
            if (this.crossLabel) {
                this.crossLabel = this.crossLabel.hide();
            }
        });
        // Extend crosshairs to also draw the label
        addEvent(Axis, 'afterDrawCrosshair', function (event) {
            // Check if the label has to be drawn
            if (!this.crosshair ||
                !this.crosshair.label ||
                !this.crosshair.label.enabled ||
                !this.cross ||
                !isNumber(this.min) ||
                !isNumber(this.max)) {
                return;
            }
            var chart = this.chart, log = this.logarithmic, options = this.crosshair.label, // the label's options
                horiz = this.horiz, // axis orientation
                opposite = this.opposite, // axis position
                left = this.left, // left position
                top = this.top, // top position
                crossLabel = this.crossLabel, // the svgElement
                posx, posy, crossBox, formatOption = options.format, formatFormat = '', limit, align, tickInside = this.options.tickPosition === 'inside', snap = this.crosshair.snap !== false, offset = 0, 
                // Use last available event (#5287)
                e = event.e || (this.cross && this.cross.e), point = event.point, min = this.min, max = this.max;
            if (log) {
                min = log.lin2log(min);
                max = log.lin2log(max);
            }
            align = (horiz ? 'center' : opposite ?
                (this.labelAlign === 'right' ? 'right' : 'left') :
                (this.labelAlign === 'left' ? 'left' : 'center'));
            // If the label does not exist yet, create it.
            if (!crossLabel) {
                crossLabel = this.crossLabel = chart.renderer
                    .label('', 0, void 0, options.shape || 'callout')
                    .addClass('highcharts-crosshair-label highcharts-color-' + (point && point.series ?
                    point.series.colorIndex :
                    this.series[0] && this.series[0].colorIndex))
                    .attr({
                    align: options.align || align,
                    padding: pick(options.padding, 8),
                    r: pick(options.borderRadius, 3),
                    zIndex: 2
                })
                    .add(this.labelGroup);
                // Presentational
                if (!chart.styledMode) {
                    crossLabel
                        .attr({
                        fill: options.backgroundColor ||
                            point && point.series && point.series.color || // #14888
                            "#666666" /* Palette.neutralColor60 */,
                        stroke: options.borderColor || '',
                        'stroke-width': options.borderWidth || 0
                    })
                        .css(extend({
                        color: "#ffffff" /* Palette.backgroundColor */,
                        fontWeight: 'normal',
                        fontSize: '11px',
                        textAlign: 'center'
                    }, options.style || {}));
                }
            }
            if (horiz) {
                posx = snap ? (point.plotX || 0) + left : e.chartX;
                posy = top + (opposite ? 0 : this.height);
            }
            else {
                posx = opposite ? this.width + left : 0;
                posy = snap ? (point.plotY || 0) + top : e.chartY;
            }
            if (!formatOption && !options.formatter) {
                if (this.dateTime) {
                    formatFormat = '%b %d, %Y';
                }
                formatOption =
                    '{value' + (formatFormat ? ':' + formatFormat : '') + '}';
            }
            // Show the label
            var value = snap ?
                    (this.isXAxis ? point.x : point.y) :
                    this.toValue(horiz ? e.chartX : e.chartY);
            // Crosshair should be rendered within Axis range (#7219). Also, the point
            // of currentPriceIndicator should be inside the plot area, #14879.
            var isInside = point && point.series ?
                    point.series.isPointInside(point) :
                    (isNumber(value) && value > min && value < max);
            var text = '';
            if (formatOption) {
                text = format(formatOption, { value: value }, chart);
            }
            else if (options.formatter && isNumber(value)) {
                text = options.formatter.call(this, value);
            }
            crossLabel.attr({
                text: text,
                x: posx,
                y: posy,
                visibility: isInside ? 'inherit' : 'hidden'
            });
            crossBox = crossLabel.getBBox();
            // now it is placed we can correct its position
            if (isNumber(crossLabel.y)) {
                if (horiz) {
                    if ((tickInside && !opposite) || (!tickInside && opposite)) {
                        posy = crossLabel.y - crossBox.height;
                    }
                }
                else {
                    posy = crossLabel.y - (crossBox.height / 2);
                }
            }
            // check the edges
            if (horiz) {
                limit = {
                    left: left - crossBox.x,
                    right: left + this.width - crossBox.x
                };
            }
            else {
                limit = {
                    left: this.labelAlign === 'left' ? left : 0,
                    right: this.labelAlign === 'right' ?
                        left + this.width :
                        chart.chartWidth
                };
            }
            // left edge
            if (crossLabel.translateX < limit.left) {
                offset = limit.left - crossLabel.translateX;
            }
            // right edge
            if (crossLabel.translateX + crossBox.width >= limit.right) {
                offset = -(crossLabel.translateX + crossBox.width - limit.right);
            }
            // show the crosslabel
            crossLabel.attr({
                x: posx + offset,
                y: posy,
                // First set x and y, then anchorX and anchorY, when box is actually
                // calculated, #5702
                anchorX: horiz ?
                    posx :
                    (this.opposite ? 0 : chart.chartWidth),
                anchorY: horiz ?
                    (this.opposite ? chart.chartHeight : 0) :
                    posy + crossBox.height / 2
            });
        });
        /**
         * Based on the data grouping options decides whether
         * the data should be cropped while processing.
         *
         * @ignore
         * @function Highcharts.Series#forceCropping
         */
        Series.prototype.forceCropping = function () {
            var chart = this.chart,
                options = this.options,
                dataGroupingOptions = options.dataGrouping,
                groupingEnabled = this.allowDG !== false && dataGroupingOptions &&
                    pick(dataGroupingOptions.enabled,
                chart.options.isStock);
            return groupingEnabled;
        };
        addEvent(Chart, 'update', function (e) {
            var options = e.options;
            // Use case: enabling scrollbar from a disabled state.
            // Scrollbar needs to be initialized from a controller, Navigator in this
            // case (#6615)
            if ('scrollbar' in options && this.navigator) {
                merge(true, this.options.scrollbar, options.scrollbar);
                this.navigator.update({});
                delete options.scrollbar;
            }
        });
        /* *
         *
         *  Default Export
         *
         * */

        return StockChart;
    });
    _registerModule(_modules, 'masters/modules/stock.src.js', [_modules['Core/Globals.js'], _modules['Series/DataModifyComposition.js'], _modules['Stock/Navigator/Navigator.js'], _modules['Stock/RangeSelector/RangeSelector.js'], _modules['Stock/Scrollbar/Scrollbar.js'], _modules['Core/Axis/OrdinalAxis.js'], _modules['Series/OHLC/OHLCSeries.js'], _modules['Series/Flags/FlagsSeries.js'], _modules['Core/Chart/StockChart.js']], function (Highcharts, DataModifyComposition, Navigator, RangeSelector, Scrollbar, OrdinalAxis, OHLCSeries, FlagsSeries, StockChart) {

        var G = Highcharts;
        // Classes
        G.Navigator = Navigator;
        G.RangeSelector = RangeSelector;
        G.Scrollbar = Scrollbar;
        G.StockChart = G.stockChart = StockChart.stockChart;
        // Compositions
        DataModifyComposition.compose(G.Series, G.Axis, G.Point);
        FlagsSeries.compose(G.Renderer);
        Navigator.compose(G.Axis, G.Chart, G.Series);
        OHLCSeries.compose(G.Series);
        OrdinalAxis.compose(G.Axis, G.Series, G.Chart);
        RangeSelector.compose(G.Axis, G.Chart);
        Scrollbar.compose(G.Axis);

    });
}));