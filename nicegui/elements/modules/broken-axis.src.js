/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * (c) 2009-2021 Torstein Honsi
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/broken-axis', ['highcharts'], function (Highcharts) {
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
}));