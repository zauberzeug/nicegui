/**
 * @license Highstock JS v10.3.2 (2022-11-28)
 *
 * Data grouping module
 *
 * (c) 2010-2021 Torstein Hønsi
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/datagrouping', ['highcharts'], function (Highcharts) {
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
}));