/**
 * @license Highcharts Gantt JS v10.3.2 (2022-11-28)
 *
 * Gantt series
 *
 * (c) 2016-2021 Lars A. V. Cabrera
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/gantt', ['highcharts'], function (Highcharts) {
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
    _registerModule(_modules, 'Series/XRange/XRangeSeriesDefaults.js', [_modules['Core/Utilities.js']], function (U) {
        /* *
         *
         *  X-range series module
         *
         *  (c) 2010-2021 Torstein Honsi, Lars A. V. Cabrera
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var correctFloat = U.correctFloat,
            isNumber = U.isNumber,
            isObject = U.isObject;
        /* *
         *
         *  Constants
         *
         * */
        /**
         * The X-range series displays ranges on the X axis, typically time
         * intervals with a start and end date.
         *
         * @sample {highcharts} highcharts/demo/x-range/
         *         X-range
         * @sample {highcharts} highcharts/css/x-range/
         *         Styled mode X-range
         * @sample {highcharts} highcharts/chart/inverted-xrange/
         *         Inverted X-range
         *
         * @extends      plotOptions.column
         * @since        6.0.0
         * @product      highcharts highstock gantt
         * @excluding    boostThreshold, crisp, cropThreshold, depth, edgeColor,
         *               edgeWidth, findNearestPointBy, getExtremesFromAll,
         *               negativeColor, pointInterval, pointIntervalUnit,
         *               pointPlacement, pointRange, pointStart, softThreshold,
         *               stacking, threshold, data, dataSorting, boostBlending
         * @requires     modules/xrange
         * @optionparent plotOptions.xrange
         */
        var XRangeSeriesDefaults = {
                /**
                 * A partial fill for each point,
            typically used to visualize how much
                 * of a task is performed. The partial fill object can be set either on
                 * series or point level.
                 *
                 * @sample {highcharts} highcharts/demo/x-range
                 *         X-range with partial fill
                 *
                 * @product   highcharts highstock gantt
                 * @apioption plotOptions.xrange.partialFill
                 */
                /**
                 * The fill color to be used for partial fills. Defaults to a darker
                 * shade of the point color.
                 *
                 * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 * @product   highcharts highstock gantt
                 * @apioption plotOptions.xrange.partialFill.fill
                 */
                /**
                 * A partial fill for each point,
            typically used to visualize how much
                 * of a task is performed. See [completed](series.gantt.data.completed).
                 *
                 * @sample gantt/demo/progress-indicator
                 *         Gantt with progress indicator
                 *
                 * @product   gantt
                 * @apioption plotOptions.gantt.partialFill
                 */
                /**
                 * In an X-range series,
            this option makes all points of the same Y-axis
                 * category the same color.
                 */
                colorByPoint: true,
                dataLabels: {
                    formatter: function () {
                        var point = this.point,
            amount = point.partialFill;
                    if (isObject(amount)) {
                        amount = amount.amount;
                    }
                    if (isNumber(amount) && amount > 0) {
                        return correctFloat(amount * 100) + '%';
                    }
                },
                inside: true,
                verticalAlign: 'middle'
            },
            tooltip: {
                headerFormat: '<span style="font-size: 10px">{point.x} - {point.x2}</span><br/>',
                pointFormat: '<span style="color:{point.color}">\u25CF</span> {series.name}: <b>{point.yCategory}</b><br/>'
            },
            borderRadius: 3,
            pointRange: 0
        };
        /* *
         *
         *  Export Default
         *
         * */
        /* *
         *
         * API Options
         *
         * */
        /**
         * An `xrange` series. If the [type](#series.xrange.type) option is not
         * specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.xrange
         * @excluding boostThreshold, crisp, cropThreshold, depth, edgeColor, edgeWidth,
         *            findNearestPointBy, getExtremesFromAll, negativeColor,
         *            pointInterval, pointIntervalUnit, pointPlacement, pointRange,
         *            pointStart, softThreshold, stacking, threshold, dataSorting,
         *            boostBlending
         * @product   highcharts highstock gantt
         * @requires  modules/xrange
         * @apioption series.xrange
         */
        /**
         * An array of data points for the series. For the `xrange` series type,
         * points can be given in the following ways:
         *
         * 1. An array of objects with named values. The objects are point configuration
         *    objects as seen below.
         *    ```js
         *    data: [{
         *        x: Date.UTC(2017, 0, 1),
         *        x2: Date.UTC(2017, 0, 3),
         *        name: "Test",
         *        y: 0,
         *        color: "#00FF00"
         *    }, {
         *        x: Date.UTC(2017, 0, 4),
         *        x2: Date.UTC(2017, 0, 5),
         *        name: "Deploy",
         *        y: 1,
         *        color: "#FF0000"
         *    }]
         *    ```
         *
         * @sample {highcharts} highcharts/series/data-array-of-objects/
         *         Config objects
         *
         * @declare   Highcharts.XrangePointOptionsObject
         * @type      {Array<*>}
         * @extends   series.line.data
         * @product   highcharts highstock gantt
         * @apioption series.xrange.data
         */
        /**
         * The starting X value of the range point.
         *
         * @sample {highcharts} highcharts/demo/x-range
         *         X-range
         *
         * @type      {number}
         * @product   highcharts highstock gantt
         * @apioption series.xrange.data.x
         */
        /**
         * The ending X value of the range point.
         *
         * @sample {highcharts} highcharts/demo/x-range
         *         X-range
         *
         * @type      {number}
         * @product   highcharts highstock gantt
         * @apioption series.xrange.data.x2
         */
        /**
         * The Y value of the range point.
         *
         * @sample {highcharts} highcharts/demo/x-range
         *         X-range
         *
         * @type      {number}
         * @product   highcharts highstock gantt
         * @apioption series.xrange.data.y
         */
        /**
         * A partial fill for each point, typically used to visualize how much of
         * a task is performed. The partial fill object can be set either on series
         * or point level.
         *
         * @sample {highcharts} highcharts/demo/x-range
         *         X-range with partial fill
         *
         * @declare   Highcharts.XrangePointPartialFillOptionsObject
         * @product   highcharts highstock gantt
         * @apioption series.xrange.data.partialFill
         */
        /**
         * The amount of the X-range point to be filled. Values can be 0-1 and are
         * converted to percentages in the default data label formatter.
         *
         * @type      {number}
         * @product   highcharts highstock gantt
         * @apioption series.xrange.data.partialFill.amount
         */
        /**
         * The fill color to be used for partial fills. Defaults to a darker shade
         * of the point color.
         *
         * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
         * @product   highcharts highstock gantt
         * @apioption series.xrange.data.partialFill.fill
         */
        (''); // adds doclets above to transpiled file

        return XRangeSeriesDefaults;
    });
    _registerModule(_modules, 'Series/XRange/XRangePoint.js', [_modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (SeriesRegistry, U) {
        /* *
         *
         *  X-range series module
         *
         *  (c) 2010-2021 Torstein Honsi, Lars A. V. Cabrera
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
        var pointProto = SeriesRegistry.series.prototype.pointClass.prototype,
            ColumnPoint = SeriesRegistry.seriesTypes.column.prototype.pointClass;
        var extend = U.extend;
        /* *
         *
         *  Class
         *
         * */
        var XRangePoint = /** @class */ (function (_super) {
                __extends(XRangePoint, _super);
            function XRangePoint() {
                /* *
                 *
                 *  Static Functions
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                /* *
                 *
                 *  Properties
                 *
                 * */
                _this.options = void 0;
                _this.series = void 0;
                return _this;
            }
            /**
             * Return color of a point based on its category.
             *
             * @private
             * @function getColorByCategory
             *
             * @param {object} series
             *        The series which the point belongs to.
             *
             * @param {object} point
             *        The point to calculate its color for.
             *
             * @return {object}
             *         Returns an object containing the properties color and colorIndex.
             */
            XRangePoint.getColorByCategory = function (series, point) {
                var colors = series.options.colors || series.chart.options.colors,
                    colorCount = colors ?
                        colors.length :
                        series.chart.options.chart.colorCount,
                    colorIndex = point.y % colorCount,
                    color = colors && colors[colorIndex];
                return {
                    colorIndex: colorIndex,
                    color: color
                };
            };
            /* *
             *
             *  Functions
             *
             * */
            /**
             * @private
             */
            XRangePoint.prototype.resolveColor = function () {
                var series = this.series;
                if (series.options.colorByPoint && !this.options.color) {
                    var colorByPoint = XRangePoint.getColorByCategory(series,
                        this);
                    if (!series.chart.styledMode) {
                        this.color = colorByPoint.color;
                    }
                    if (!this.options.colorIndex) {
                        this.colorIndex = colorByPoint.colorIndex;
                    }
                }
                else if (!this.color) {
                    this.color = series.color;
                }
            };
            /**
             * Extend init to have y default to 0.
             *
             * @private
             */
            XRangePoint.prototype.init = function () {
                pointProto.init.apply(this, arguments);
                if (!this.y) {
                    this.y = 0;
                }
                return this;
            };
            /**
             * @private
             */
            XRangePoint.prototype.setState = function () {
                pointProto.setState.apply(this, arguments);
                this.series.drawPoint(this, this.series.getAnimationVerb());
            };
            /**
             * Add x2 and yCategory to the available properties for tooltip formats.
             *
             * @private
             */
            XRangePoint.prototype.getLabelConfig = function () {
                var cfg = pointProto.getLabelConfig.call(this),
                    yCats = this.series.yAxis.categories;
                cfg.x2 = this.x2;
                cfg.yCategory = this.yCategory = yCats && yCats[this.y];
                return cfg;
            };
            /**
             * @private
             */
            XRangePoint.prototype.isValid = function () {
                return typeof this.x === 'number' &&
                    typeof this.x2 === 'number';
            };
            return XRangePoint;
        }(ColumnPoint));
        extend(XRangePoint.prototype, {
            ttBelow: false,
            tooltipDateKeys: ['x', 'x2']
        });
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
         * The ending X value of the range point.
         * @name Highcharts.Point#x2
         * @type {number|undefined}
         * @requires modules/xrange
         */
        /**
         * Extend applyOptions so that `colorByPoint` for x-range means that one
         * color is applied per Y axis category.
         *
         * @private
         * @function Highcharts.Point#applyOptions
         *
         * @return {Highcharts.Series}
         */
        /**
         * @interface Highcharts.PointOptionsObject in parts/Point.ts
         */ /**
        * The ending X value of the range point.
        * @name Highcharts.PointOptionsObject#x2
        * @type {number|undefined}
        * @requires modules/xrange
        */
        (''); // keeps doclets above in JS file

        return XRangePoint;
    });
    _registerModule(_modules, 'Series/XRange/XRangeSeries.js', [_modules['Core/Globals.js'], _modules['Core/Color/Color.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js'], _modules['Series/XRange/XRangeSeriesDefaults.js'], _modules['Series/XRange/XRangePoint.js']], function (H, Color, SeriesRegistry, U, XRangeSeriesDefaults, XRangePoint) {
        /* *
         *
         *  X-range series module
         *
         *  (c) 2010-2021 Torstein Honsi, Lars A. V. Cabrera
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
        var color = Color.parse;
        var seriesProto = SeriesRegistry.series.prototype,
            ColumnSeries = SeriesRegistry.seriesTypes.column;
        var addEvent = U.addEvent,
            clamp = U.clamp,
            defined = U.defined,
            extend = U.extend,
            find = U.find,
            isNumber = U.isNumber,
            isObject = U.isObject,
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
         *  Functions
         *
         * */
        /**
         * Max x2 should be considered in xAxis extremes
         * @private
         */
        function onAxisAfterGetSeriesExtremes() {
            var dataMax,
                modMax;
            if (this.isXAxis) {
                dataMax = pick(this.dataMax, -Number.MAX_VALUE);
                for (var _i = 0, _a = this.series; _i < _a.length; _i++) {
                    var series = _a[_i];
                    if (series.x2Data) {
                        for (var _b = 0, _c = series.x2Data; _b < _c.length; _b++) {
                            var val = _c[_b];
                            if (val && val > dataMax) {
                                dataMax = val;
                                modMax = true;
                            }
                        }
                    }
                }
                if (modMax) {
                    this.dataMax = dataMax;
                }
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
         * @name Highcharts.seriesTypes.xrange
         *
         * @augments Highcharts.Series
         */
        var XRangeSeries = /** @class */ (function (_super) {
                __extends(XRangeSeries, _super);
            function XRangeSeries() {
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
                /*
                // Override to remove stroke from points. For partial fill.
                pointAttribs: function () {
                    let series = this,
                        retVal = columnType.prototype.pointAttribs
                            .apply(series, arguments);
    
                    //retVal['stroke-width'] = 0;
                    return retVal;
                }
                //*/
                /* eslint-enable valid-jsdoc */
            }
            /* *
             *
             *  Static Functions
             *
             * */
            XRangeSeries.compose = function (AxisClass) {
                if (composedClasses.indexOf(AxisClass) === -1) {
                    composedClasses.push(AxisClass);
                    addEvent(AxisClass, 'afterGetSeriesExtremes', onAxisAfterGetSeriesExtremes);
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
            XRangeSeries.prototype.init = function () {
                _super.prototype.init.apply(this, arguments);
                this.options.stacking = void 0; // #13161
            };
            /**
             * Borrow the column series metrics, but with swapped axes. This gives
             * free access to features like groupPadding, grouping, pointWidth etc.
             * @private
             */
            XRangeSeries.prototype.getColumnMetrics = function () {
                var _this = this;
                var swapAxes = function () {
                        for (var _i = 0,
                    _a = _this.chart.series; _i < _a.length; _i++) {
                            var series = _a[_i];
                        var xAxis = series.xAxis;
                        series.xAxis = series.yAxis;
                        series.yAxis = xAxis;
                    }
                };
                swapAxes();
                var metrics = _super.prototype.getColumnMetrics.call(this);
                swapAxes();
                return metrics;
            };
            /**
             * Override cropData to show a point where x or x2 is outside visible range,
             * but one of them is inside.
             * @private
             */
            XRangeSeries.prototype.cropData = function (xData, yData, min, max) {
                // Replace xData with x2Data to find the appropriate cropStart
                var crop = seriesProto.cropData.call(this,
                    this.x2Data,
                    yData,
                    min,
                    max);
                // Re-insert the cropped xData
                crop.xData = xData.slice(crop.start, crop.end);
                return crop;
            };
            /**
             * Finds the index of an existing point that matches the given point
             * options.
             *
             * @private
             *
             * @param {Highcharts.XRangePointOptions} options
             *        The options of the point.
             *
             * @return {number|undefined}
             *         Returns index of a matching point, or undefined if no match is
             *         found.
             */
            XRangeSeries.prototype.findPointIndex = function (options) {
                var _a = this,
                    cropStart = _a.cropStart,
                    points = _a.points;
                var id = options.id;
                var pointIndex;
                if (id) {
                    var point = find(points,
                        function (point) { return point.id === id; });
                    pointIndex = point ? point.index : void 0;
                }
                if (typeof pointIndex === 'undefined') {
                    var point = find(points,
                        function (point) { return (point.x === options.x &&
                            point.x2 === options.x2 &&
                            !point.touched); });
                    pointIndex = point ? point.index : void 0;
                }
                // Reduce pointIndex if data is cropped
                if (this.cropped &&
                    isNumber(pointIndex) &&
                    isNumber(cropStart) &&
                    pointIndex >= cropStart) {
                    pointIndex -= cropStart;
                }
                return pointIndex;
            };
            XRangeSeries.prototype.alignDataLabel = function (point) {
                var oldPlotX = point.plotX;
                point.plotX = pick(point.dlBox && point.dlBox.centerX, point.plotX);
                _super.prototype.alignDataLabel.apply(this, arguments);
                point.plotX = oldPlotX;
            };
            /**
             * @private
             */
            XRangeSeries.prototype.translatePoint = function (point) {
                var xAxis = this.xAxis,
                    yAxis = this.yAxis,
                    metrics = this.columnMetrics,
                    options = this.options,
                    minPointLength = options.minPointLength || 0,
                    oldColWidth = (point.shapeArgs && point.shapeArgs.width || 0) / 2,
                    seriesXOffset = this.pointXOffset = metrics.offset,
                    posX = pick(point.x2,
                    point.x + (point.len || 0));
                var plotX = point.plotX,
                    plotX2 = xAxis.translate(posX, 0, 0, 0, 1);
                var length = Math.abs(plotX2 - plotX),
                    inverted = this.chart.inverted,
                    borderWidth = pick(options.borderWidth, 1),
                    crisper = borderWidth % 2 / 2;
                var widthDifference,
                    partialFill,
                    yOffset = metrics.offset,
                    pointHeight = Math.round(metrics.width),
                    dlLeft,
                    dlRight,
                    dlWidth,
                    clipRectWidth;
                if (minPointLength) {
                    widthDifference = minPointLength - length;
                    if (widthDifference < 0) {
                        widthDifference = 0;
                    }
                    plotX -= widthDifference / 2;
                    plotX2 += widthDifference / 2;
                }
                plotX = Math.max(plotX, -10);
                plotX2 = clamp(plotX2, -10, xAxis.len + 10);
                // Handle individual pointWidth
                if (defined(point.options.pointWidth)) {
                    yOffset -= ((Math.ceil(point.options.pointWidth) - pointHeight) / 2);
                    pointHeight = Math.ceil(point.options.pointWidth);
                }
                // Apply pointPlacement to the Y axis
                if (options.pointPlacement &&
                    isNumber(point.plotY) &&
                    yAxis.categories) {
                    point.plotY = yAxis.translate(point.y, 0, 1, 0, 1, options.pointPlacement);
                }
                var x = Math.floor(Math.min(plotX,
                    plotX2)) + crisper;
                var x2 = Math.floor(Math.max(plotX,
                    plotX2)) + crisper;
                var shapeArgs = {
                        x: x,
                        y: Math.floor(point.plotY + yOffset) + crisper,
                        width: x2 - x,
                        height: pointHeight,
                        r: this.options.borderRadius
                    };
                point.shapeArgs = shapeArgs;
                // Move tooltip to default position
                if (!inverted) {
                    point.tooltipPos[0] -= oldColWidth +
                        seriesXOffset -
                        shapeArgs.width / 2;
                }
                else {
                    point.tooltipPos[1] += seriesXOffset +
                        oldColWidth;
                }
                // Align data labels inside the shape and inside the plot area
                dlLeft = shapeArgs.x;
                dlRight = dlLeft + shapeArgs.width;
                if (dlLeft < 0 || dlRight > xAxis.len) {
                    dlLeft = clamp(dlLeft, 0, xAxis.len);
                    dlRight = clamp(dlRight, 0, xAxis.len);
                    dlWidth = dlRight - dlLeft;
                    point.dlBox = merge(shapeArgs, {
                        x: dlLeft,
                        width: dlRight - dlLeft,
                        centerX: dlWidth ? dlWidth / 2 : null
                    });
                }
                else {
                    point.dlBox = null;
                }
                // Tooltip position
                var tooltipPos = point.tooltipPos;
                var xIndex = !inverted ? 0 : 1;
                var yIndex = !inverted ? 1 : 0;
                var tooltipYOffset = (this.columnMetrics ?
                        this.columnMetrics.offset :
                        -metrics.width / 2);
                // Centering tooltip position (#14147)
                if (!inverted) {
                    tooltipPos[xIndex] += (xAxis.reversed ? -1 : 0) * shapeArgs.width;
                }
                else {
                    tooltipPos[xIndex] += shapeArgs.width / 2;
                }
                tooltipPos[yIndex] = clamp(tooltipPos[yIndex] + ((inverted ? -1 : 1) * tooltipYOffset), 0, yAxis.len - 1);
                // Add a partShapeArgs to the point, based on the shapeArgs property
                partialFill = point.partialFill;
                if (partialFill) {
                    // Get the partial fill amount
                    if (isObject(partialFill)) {
                        partialFill = partialFill.amount;
                    }
                    // If it was not a number, assume 0
                    if (!isNumber(partialFill)) {
                        partialFill = 0;
                    }
                    point.partShapeArgs = merge(shapeArgs, {
                        r: this.options.borderRadius
                    });
                    clipRectWidth = Math.max(Math.round(length * partialFill + point.plotX -
                        plotX), 0);
                    point.clipRectArgs = {
                        x: xAxis.reversed ? // #10717
                            shapeArgs.x + length - clipRectWidth :
                            shapeArgs.x,
                        y: shapeArgs.y,
                        width: clipRectWidth,
                        height: shapeArgs.height
                    };
                }
            };
            /**
             * @private
             */
            XRangeSeries.prototype.translate = function () {
                _super.prototype.translate.apply(this, arguments);
                for (var _i = 0, _a = this.points; _i < _a.length; _i++) {
                    var point = _a[_i];
                    this.translatePoint(point);
                }
            };
            /**
             * Draws a single point in the series. Needed for partial fill.
             *
             * This override turns point.graphic into a group containing the
             * original graphic and an overlay displaying the partial fill.
             *
             * @private
             *
             * @param {Highcharts.Point} point
             *        An instance of Point in the series.
             *
             * @param {"animate"|"attr"} verb
             *        'animate' (animates changes) or 'attr' (sets options)
             */
            XRangeSeries.prototype.drawPoint = function (point, verb) {
                var seriesOpts = this.options,
                    renderer = this.chart.renderer,
                    type = point.shapeType,
                    shapeArgs = point.shapeArgs,
                    partShapeArgs = point.partShapeArgs,
                    clipRectArgs = point.clipRectArgs,
                    cutOff = seriesOpts.stacking && !seriesOpts.borderRadius,
                    pointState = point.state,
                    stateOpts = (seriesOpts.states[pointState || 'normal'] ||
                        {}),
                    pointStateVerb = typeof pointState === 'undefined' ?
                        'attr' : verb,
                    pointAttr = this.pointAttribs(point,
                    pointState),
                    animation = pick(this.chart.options.chart.animation,
                    stateOpts.animation);
                var graphic = point.graphic,
                    pfOptions = point.partialFill;
                if (!point.isNull && point.visible !== false) {
                    // Original graphic
                    if (graphic) { // update
                        graphic.rect[verb](shapeArgs);
                    }
                    else {
                        point.graphic = graphic = renderer.g('point')
                            .addClass(point.getClassName())
                            .add(point.group || this.group);
                        graphic.rect = renderer[type](merge(shapeArgs))
                            .addClass(point.getClassName())
                            .addClass('highcharts-partfill-original')
                            .add(graphic);
                    }
                    // Partial fill graphic
                    if (partShapeArgs) {
                        if (graphic.partRect) {
                            graphic.partRect[verb](merge(partShapeArgs));
                            graphic.partialClipRect[verb](merge(clipRectArgs));
                        }
                        else {
                            graphic.partialClipRect = renderer.clipRect(clipRectArgs.x, clipRectArgs.y, clipRectArgs.width, clipRectArgs.height);
                            graphic.partRect =
                                renderer[type](partShapeArgs)
                                    .addClass('highcharts-partfill-overlay')
                                    .add(graphic)
                                    .clip(graphic.partialClipRect);
                        }
                    }
                    // Presentational
                    if (!this.chart.styledMode) {
                        graphic
                            .rect[verb](pointAttr, animation)
                            .shadow(seriesOpts.shadow, null, cutOff);
                        if (partShapeArgs) {
                            // Ensure pfOptions is an object
                            if (!isObject(pfOptions)) {
                                pfOptions = {};
                            }
                            if (isObject(seriesOpts.partialFill)) {
                                pfOptions = merge(seriesOpts.partialFill, pfOptions);
                            }
                            var fill = (pfOptions.fill ||
                                    color(pointAttr.fill).brighten(-0.3).get() ||
                                    color(point.color || this.color)
                                        .brighten(-0.3).get());
                            pointAttr.fill = fill;
                            graphic
                                .partRect[pointStateVerb](pointAttr, animation)
                                .shadow(seriesOpts.shadow, null, cutOff);
                        }
                    }
                }
                else if (graphic) {
                    point.graphic = graphic.destroy(); // #1269
                }
            };
            /**
             * @private
             */
            XRangeSeries.prototype.drawPoints = function () {
                var verb = this.getAnimationVerb();
                // Draw the columns
                for (var _i = 0, _a = this.points; _i < _a.length; _i++) {
                    var point = _a[_i];
                    this.drawPoint(point, verb);
                }
            };
            /**
             * Returns "animate", or "attr" if the number of points is above the
             * animation limit.
             *
             * @private
             */
            XRangeSeries.prototype.getAnimationVerb = function () {
                return (this.chart.pointCount < (this.options.animationLimit || 250) ?
                    'animate' :
                    'attr');
            };
            /**
             * @private
             */
            XRangeSeries.prototype.isPointInside = function (point) {
                var shapeArgs = point.shapeArgs,
                    plotX = point.plotX,
                    plotY = point.plotY;
                if (!shapeArgs) {
                    return _super.prototype.isPointInside.apply(this, arguments);
                }
                var isInside = typeof plotX !== 'undefined' &&
                        typeof plotY !== 'undefined' &&
                        plotY >= 0 &&
                        plotY <= this.yAxis.len &&
                        (shapeArgs.x || 0) + (shapeArgs.width || 0) >= 0 &&
                        plotX <= this.xAxis.len;
                return isInside;
            };
            XRangeSeries.defaultOptions = merge(ColumnSeries.defaultOptions, XRangeSeriesDefaults);
            return XRangeSeries;
        }(ColumnSeries));
        extend(XRangeSeries.prototype, {
            pointClass: XRangePoint,
            cropShoulder: 1,
            getExtremesFromAll: true,
            parallelArrays: ['x', 'x2', 'y'],
            requireSorting: false,
            type: 'xrange',
            animate: seriesProto.animate,
            autoIncrement: noop,
            buildKDTree: noop
        });
        SeriesRegistry.registerSeriesType('xrange', XRangeSeries);
        /* *
         *
         * Default Export
         *
         * */

        return XRangeSeries;
    });
    _registerModule(_modules, 'Series/Gantt/GanttPoint.js', [_modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (SeriesRegistry, U) {
        /* *
         *
         *  (c) 2016-2021 Highsoft AS
         *
         *  Author: Lars A. V. Cabrera
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
        var XRangePoint = SeriesRegistry.seriesTypes.xrange.prototype.pointClass;
        var pick = U.pick;
        /* *
         *
         *  Class
         *
         * */
        var GanttPoint = /** @class */ (function (_super) {
                __extends(GanttPoint, _super);
            function GanttPoint() {
                /* *
                 *
                 *  Static Functions
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.options = void 0;
                _this.series = void 0;
                return _this;
                /* eslint-enable valid-jsdoc */
            }
            /* eslint-disable valid-jsdoc */
            /**
             * @private
             */
            GanttPoint.setGanttPointAliases = function (options) {
                /**
                 * Add a value to options if the value exists.
                 * @private
                 */
                function addIfExists(prop, val) {
                    if (typeof val !== 'undefined') {
                        options[prop] = val;
                    }
                }
                addIfExists('x', pick(options.start, options.x));
                addIfExists('x2', pick(options.end, options.x2));
                addIfExists('partialFill', pick(options.completed, options.partialFill));
            };
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Applies the options containing the x and y data and possible some
             * extra properties. This is called on point init or from point.update.
             *
             * @private
             * @function Highcharts.Point#applyOptions
             *
             * @param {Object} options
             *        The point options
             *
             * @param {number} x
             *        The x value
             *
             * @return {Highcharts.Point}
             *         The Point instance
             */
            GanttPoint.prototype.applyOptions = function (options, x) {
                var point = this,
                    ganttPoint;
                ganttPoint = _super.prototype.applyOptions.call(point, options, x);
                GanttPoint.setGanttPointAliases(ganttPoint);
                return ganttPoint;
            };
            GanttPoint.prototype.isValid = function () {
                return ((typeof this.start === 'number' ||
                    typeof this.x === 'number') &&
                    (typeof this.end === 'number' ||
                        typeof this.x2 === 'number' ||
                        this.milestone));
            };
            return GanttPoint;
        }(XRangePoint));
        /* *
         *
         *  Default Export
         *
         * */

        return GanttPoint;
    });
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
    _registerModule(_modules, 'Core/Axis/GridAxis.js', [_modules['Core/Axis/Axis.js'], _modules['Core/Axis/AxisDefaults.js'], _modules['Core/Globals.js'], _modules['Core/Utilities.js']], function (Axis, AxisDefaults, H, U) {
        /* *
         *
         *  (c) 2016 Highsoft AS
         *  Authors: Lars A. V. Cabrera
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var dateFormats = H.dateFormats;
        var addEvent = U.addEvent,
            defined = U.defined,
            erase = U.erase,
            find = U.find,
            isArray = U.isArray,
            isNumber = U.isNumber,
            merge = U.merge,
            pick = U.pick,
            timeUnits = U.timeUnits,
            wrap = U.wrap;
        /* *
         *
         *  Enums
         *
         * */
        /**
         * Enum for which side the axis is on. Maps to axis.side.
         * @private
         */
        var GridAxisSide;
        (function (GridAxisSide) {
            GridAxisSide[GridAxisSide["top"] = 0] = "top";
            GridAxisSide[GridAxisSide["right"] = 1] = "right";
            GridAxisSide[GridAxisSide["bottom"] = 2] = "bottom";
            GridAxisSide[GridAxisSide["left"] = 3] = "left";
        })(GridAxisSide || (GridAxisSide = {}));
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
        function argsToArray(args) {
            return Array.prototype.slice.call(args, 1);
        }
        /**
         * @private
         */
        function isObject(x) {
            // Always use strict mode
            return U.isObject(x, true);
        }
        /**
         * @private
         */
        function applyGridOptions(axis) {
            var options = axis.options;
            // Center-align by default
            /*
            if (!options.labels) {
                options.labels = {};
            }
            */
            options.labels.align = pick(options.labels.align, 'center');
            // @todo: Check against tickLabelPlacement between/on etc
            /* Prevents adding the last tick label if the axis is not a category
               axis.
               Since numeric labels are normally placed at starts and ends of a
               range of value, and this module makes the label point at the value,
               an "extra" label would appear. */
            if (!axis.categories) {
                options.showLastLabel = false;
            }
            // Prevents rotation of labels when squished, as rotating them would not
            // help.
            axis.labelRotation = 0;
            options.labels.rotation = 0;
        }
        /**
         * Extends axis class with grid support.
         * @private
         */
        function compose(AxisClass, ChartClass, TickClass) {
            if (composedClasses.indexOf(AxisClass) === -1) {
                composedClasses.push(AxisClass);
                AxisClass.keepProps.push('grid');
                AxisClass.prototype.getMaxLabelDimensions = getMaxLabelDimensions;
                wrap(AxisClass.prototype, 'unsquish', wrapUnsquish);
                // Add event handlers
                addEvent(AxisClass, 'init', onInit);
                addEvent(AxisClass, 'afterGetOffset', onAfterGetOffset);
                addEvent(AxisClass, 'afterGetTitlePosition', onAfterGetTitlePosition);
                addEvent(AxisClass, 'afterInit', onAfterInit);
                addEvent(AxisClass, 'afterRender', onAfterRender);
                addEvent(AxisClass, 'afterSetAxisTranslation', onAfterSetAxisTranslation);
                addEvent(AxisClass, 'afterSetOptions', onAfterSetOptions);
                addEvent(AxisClass, 'afterSetOptions', onAfterSetOptions2);
                addEvent(AxisClass, 'afterSetScale', onAfterSetScale);
                addEvent(AxisClass, 'afterTickSize', onAfterTickSize);
                addEvent(AxisClass, 'trimTicks', onTrimTicks);
                addEvent(AxisClass, 'destroy', onDestroy);
            }
            if (composedClasses.indexOf(ChartClass) === -1) {
                addEvent(ChartClass, 'afterSetChartSize', onChartAfterSetChartSize);
            }
            if (composedClasses.indexOf(TickClass) === -1) {
                addEvent(TickClass, 'afterGetLabelPosition', onTickAfterGetLabelPosition);
                addEvent(TickClass, 'labelFormat', onTickLabelFormat);
            }
            return AxisClass;
        }
        /**
         * Get the largest label width and height.
         *
         * @private
         * @function Highcharts.Axis#getMaxLabelDimensions
         *
         * @param {Highcharts.Dictionary<Highcharts.Tick>} ticks
         * All the ticks on one axis.
         *
         * @param {Array<number|string>} tickPositions
         * All the tick positions on one axis.
         *
         * @return {Highcharts.SizeObject}
         * Object containing the properties height and width.
         *
         * @todo Move this to the generic axis implementation, as it is used there.
         */
        function getMaxLabelDimensions(ticks, tickPositions) {
            var dimensions = {
                    width: 0,
                    height: 0
                };
            tickPositions.forEach(function (pos) {
                var tick = ticks[pos];
                var labelHeight = 0,
                    labelWidth = 0,
                    label;
                if (isObject(tick)) {
                    label = isObject(tick.label) ? tick.label : {};
                    // Find width and height of label
                    labelHeight = label.getBBox ? label.getBBox().height : 0;
                    if (label.textStr && !isNumber(label.textPxLength)) {
                        label.textPxLength = label.getBBox().width;
                    }
                    labelWidth = isNumber(label.textPxLength) ?
                        // Math.round ensures crisp lines
                        Math.round(label.textPxLength) :
                        0;
                    if (label.textStr) {
                        // Set the tickWidth same as the label width after ellipsis
                        // applied #10281
                        labelWidth = Math.round(label.getBBox().width);
                    }
                    // Update the result if width and/or height are larger
                    dimensions.height = Math.max(labelHeight, dimensions.height);
                    dimensions.width = Math.max(labelWidth, dimensions.width);
                }
            });
            // For tree grid, add indentation
            if (this.options.type === 'treegrid' &&
                this.treeGrid &&
                this.treeGrid.mapOfPosToGridNode) {
                var treeDepth = this.treeGrid.mapOfPosToGridNode[-1].height || 0;
                dimensions.width += (this.options.labels.indentation *
                    (treeDepth - 1));
            }
            return dimensions;
        }
        /**
         * Handle columns and getOffset.
         * @private
         */
        function onAfterGetOffset() {
            var grid = this.grid;
            (grid && grid.columns || []).forEach(function (column) {
                column.getOffset();
            });
        }
        /**
         * @private
         */
        function onAfterGetTitlePosition(e) {
            var axis = this;
            var options = axis.options;
            var gridOptions = options.grid || {};
            if (gridOptions.enabled === true) {
                // compute anchor points for each of the title align options
                var axisTitle = axis.axisTitle,
                    axisHeight = axis.height,
                    horiz = axis.horiz,
                    axisLeft = axis.left,
                    offset = axis.offset,
                    opposite = axis.opposite,
                    options_1 = axis.options,
                    axisTop = axis.top,
                    axisWidth = axis.width;
                var tickSize = axis.tickSize();
                var titleWidth = axisTitle && axisTitle.getBBox().width;
                var xOption = options_1.title.x;
                var yOption = options_1.title.y;
                var titleMargin = pick(options_1.title.margin,
                    horiz ? 5 : 10);
                var titleFontSize = axis.chart.renderer.fontMetrics(options_1.title.style.fontSize,
                    axisTitle).f;
                var crispCorr = tickSize ? tickSize[0] / 2 : 0;
                // TODO account for alignment
                // the position in the perpendicular direction of the axis
                var offAxis = ((horiz ? axisTop + axisHeight : axisLeft) +
                        (horiz ? 1 : -1) * // horizontal axis reverses the margin
                            (opposite ? -1 : 1) * // so does opposite axes
                            crispCorr +
                        (axis.side === GridAxisSide.bottom ? titleFontSize : 0));
                e.titlePosition.x = horiz ?
                    axisLeft - (titleWidth || 0) / 2 - titleMargin + xOption :
                    offAxis + (opposite ? axisWidth : 0) + offset + xOption;
                e.titlePosition.y = horiz ?
                    (offAxis -
                        (opposite ? axisHeight : 0) +
                        (opposite ? titleFontSize : -titleFontSize) / 2 +
                        offset +
                        yOption) :
                    axisTop - titleMargin + yOption;
            }
        }
        /**
         * @private
         */
        function onAfterInit() {
            var axis = this;
            var chart = axis.chart,
                _a = axis.options.grid,
                gridOptions = _a === void 0 ? {} : _a,
                userOptions = axis.userOptions;
            if (gridOptions.enabled) {
                applyGridOptions(axis);
            }
            if (gridOptions.columns) {
                var columns = axis.grid.columns = [];
                var columnIndex = axis.grid.columnIndex = 0;
                // Handle columns, each column is a grid axis
                while (++columnIndex < gridOptions.columns.length) {
                    var columnOptions = merge(userOptions,
                        gridOptions.columns[gridOptions.columns.length - columnIndex - 1], {
                            linkedTo: 0,
                            // Force to behave like category axis
                            type: 'category',
                            // Disable by default the scrollbar on the grid axis
                            scrollbar: {
                                enabled: false
                            }
                        });
                    delete columnOptions.grid.columns; // Prevent recursion
                    var column = new Axis(axis.chart,
                        columnOptions);
                    column.grid.isColumn = true;
                    column.grid.columnIndex = columnIndex;
                    // Remove column axis from chart axes array, and place it
                    // in the columns array.
                    erase(chart.axes, column);
                    erase(chart[axis.coll], column);
                    columns.push(column);
                }
            }
        }
        /**
         * Draw an extra line on the far side of the outermost axis,
         * creating floor/roof/wall of a grid. And some padding.
         * ```
         * Make this:
         *             (axis.min) __________________________ (axis.max)
         *                           |    |    |    |    |
         * Into this:
         *             (axis.min) __________________________ (axis.max)
         *                        ___|____|____|____|____|__
         * ```
         * @private
         */
        function onAfterRender() {
            var axis = this,
                grid = axis.grid,
                options = axis.options,
                gridOptions = options.grid || {};
            if (gridOptions.enabled === true) {
                var min = axis.min || 0,
                    max = axis.max || 0;
                // @todo acutual label padding (top, bottom, left, right)
                axis.maxLabelDimensions = axis.getMaxLabelDimensions(axis.ticks, axis.tickPositions);
                // Remove right wall before rendering if updating
                if (axis.rightWall) {
                    axis.rightWall.destroy();
                }
                /*
                Draw an extra axis line on outer axes
                            >
                Make this:    |______|______|______|___

                            > _________________________
                Into this:    |______|______|______|__|
                                                        */
                if (axis.grid && axis.grid.isOuterAxis() && axis.axisLine) {
                    var lineWidth = options.lineWidth;
                    if (lineWidth) {
                        var linePath = axis.getLinePath(lineWidth),
                            startPoint = linePath[0],
                            endPoint = linePath[1], 
                            // Negate distance if top or left axis
                            // Subtract 1px to draw the line at the end of the tick
                            tickLength = (axis.tickSize('tick') || [1])[0],
                            distance = (tickLength - 1) * ((axis.side === GridAxisSide.top ||
                                axis.side === GridAxisSide.left) ? -1 : 1);
                        // If axis is horizontal, reposition line path vertically
                        if (startPoint[0] === 'M' && endPoint[0] === 'L') {
                            if (axis.horiz) {
                                startPoint[2] += distance;
                                endPoint[2] += distance;
                            }
                            else {
                                startPoint[1] += distance;
                                endPoint[1] += distance;
                            }
                        }
                        // If it doesn't exist, add an upper and lower border
                        // for the vertical grid axis.
                        if (!axis.horiz && axis.chart.marginRight) {
                            var upperBorderStartPoint = startPoint,
                                upperBorderEndPoint = [
                                    'L',
                                    axis.left,
                                    startPoint[2] || 0
                                ],
                                upperBorderPath = [
                                    upperBorderStartPoint,
                                    upperBorderEndPoint
                                ],
                                lowerBorderEndPoint = [
                                    'L',
                                    axis.chart.chartWidth - axis.chart.marginRight,
                                    axis.toPixels(max + axis.tickmarkOffset)
                                ],
                                lowerBorderStartPoint = [
                                    'M',
                                    endPoint[1] || 0,
                                    axis.toPixels(max + axis.tickmarkOffset)
                                ],
                                lowerBorderPath = [
                                    lowerBorderStartPoint,
                                    lowerBorderEndPoint
                                ];
                            if (!axis.grid.upperBorder && min % 1 !== 0) {
                                axis.grid.upperBorder = axis.grid.renderBorder(upperBorderPath);
                            }
                            if (axis.grid.upperBorder) {
                                axis.grid.upperBorder.attr({
                                    stroke: options.lineColor,
                                    'stroke-width': options.lineWidth
                                });
                                axis.grid.upperBorder.animate({
                                    d: upperBorderPath
                                });
                            }
                            if (!axis.grid.lowerBorder && max % 1 !== 0) {
                                axis.grid.lowerBorder = axis.grid.renderBorder(lowerBorderPath);
                            }
                            if (axis.grid.lowerBorder) {
                                axis.grid.lowerBorder.attr({
                                    stroke: options.lineColor,
                                    'stroke-width': options.lineWidth
                                });
                                axis.grid.lowerBorder.animate({
                                    d: lowerBorderPath
                                });
                            }
                        }
                        // Render an extra line parallel to the existing axes, to
                        // close the grid.
                        if (!axis.grid.axisLineExtra) {
                            axis.grid.axisLineExtra = axis.grid.renderBorder(linePath);
                        }
                        else {
                            axis.grid.axisLineExtra.attr({
                                stroke: options.lineColor,
                                'stroke-width': options.lineWidth
                            });
                            axis.grid.axisLineExtra.animate({
                                d: linePath
                            });
                        }
                        // show or hide the line depending on options.showEmpty
                        axis.axisLine[axis.showAxis ? 'show' : 'hide']();
                    }
                }
                (grid && grid.columns || []).forEach(function (column) { return column.render(); });
                // Manipulate the tick mark visibility
                // based on the axis.max- allows smooth scrolling.
                if (!axis.horiz &&
                    axis.chart.hasRendered &&
                    (axis.scrollbar ||
                        (axis.linkedParent && axis.linkedParent.scrollbar))) {
                    var tickmarkOffset = axis.tickmarkOffset,
                        lastTick = axis.tickPositions[axis.tickPositions.length - 1],
                        firstTick = axis.tickPositions[0];
                    var label = void 0,
                        tickMark = void 0;
                    while ((label = axis.hiddenLabels.pop()) && label.element) {
                        label.show(); // #15453
                    }
                    while ((tickMark = axis.hiddenMarks.pop()) &&
                        tickMark.element) {
                        tickMark.show(); // #16439
                    }
                    // Hide/show firts tick label.
                    label = axis.ticks[firstTick].label;
                    if (label) {
                        if (min - firstTick > tickmarkOffset) {
                            axis.hiddenLabels.push(label.hide());
                        }
                        else {
                            label.show();
                        }
                    }
                    // Hide/show last tick mark/label.
                    label = axis.ticks[lastTick].label;
                    if (label) {
                        if (lastTick - max > tickmarkOffset) {
                            axis.hiddenLabels.push(label.hide());
                        }
                        else {
                            label.show();
                        }
                    }
                    var mark = axis.ticks[lastTick].mark;
                    if (mark &&
                        lastTick - max < tickmarkOffset &&
                        lastTick - max > 0 && axis.ticks[lastTick].isLast) {
                        axis.hiddenMarks.push(mark.hide());
                    }
                }
            }
        }
        /**
         * @private
         */
        function onAfterSetAxisTranslation() {
            var axis = this;
            var tickInfo = axis.tickPositions && axis.tickPositions.info;
            var options = axis.options;
            var gridOptions = options.grid || {};
            var userLabels = axis.userOptions.labels || {};
            // Fire this only for the Gantt type chart, #14868.
            if (gridOptions.enabled) {
                if (axis.horiz) {
                    axis.series.forEach(function (series) {
                        series.options.pointRange = 0;
                    });
                    // Lower level time ticks, like hours or minutes, represent
                    // points in time and not ranges. These should be aligned
                    // left in the grid cell by default. The same applies to
                    // years of higher order.
                    if (tickInfo &&
                        options.dateTimeLabelFormats &&
                        options.labels &&
                        !defined(userLabels.align) &&
                        (options.dateTimeLabelFormats[tickInfo.unitName]
                            .range === false ||
                            tickInfo.count > 1 // years
                        )) {
                        options.labels.align = 'left';
                        if (!defined(userLabels.x)) {
                            options.labels.x = 3;
                        }
                    }
                }
                else {
                    // Don't trim ticks which not in min/max range but
                    // they are still in the min/max plus tickInterval.
                    if (this.options.type !== 'treegrid' &&
                        axis.grid &&
                        axis.grid.columns) {
                        this.minPointOffset = this.tickInterval;
                    }
                }
            }
        }
        /**
         * Creates a left and right wall on horizontal axes:
         * - Places leftmost tick at the start of the axis, to create a left
         *   wall
         * - Ensures that the rightmost tick is at the end of the axis, to
         *   create a right wall.
         * @private
         */
        function onAfterSetOptions(e) {
            var options = this.options,
                userOptions = e.userOptions,
                gridOptions = ((options && isObject(options.grid)) ? options.grid : {});
            var gridAxisOptions;
            if (gridOptions.enabled === true) {
                // Merge the user options into default grid axis options so
                // that when a user option is set, it takes presedence.
                gridAxisOptions = merge(true, {
                    className: ('highcharts-grid-axis ' + (userOptions.className || '')),
                    dateTimeLabelFormats: {
                        hour: {
                            list: ['%H:%M', '%H']
                        },
                        day: {
                            list: ['%A, %e. %B', '%a, %e. %b', '%E']
                        },
                        week: {
                            list: ['Week %W', 'W%W']
                        },
                        month: {
                            list: ['%B', '%b', '%o']
                        }
                    },
                    grid: {
                        borderWidth: 1
                    },
                    labels: {
                        padding: 2,
                        style: {
                            fontSize: '13px'
                        }
                    },
                    margin: 0,
                    title: {
                        text: null,
                        reserveSpace: false,
                        rotation: 0
                    },
                    // In a grid axis, only allow one unit of certain types,
                    // for example we shouln't have one grid cell spanning
                    // two days.
                    units: [[
                            'millisecond',
                            [1, 10, 100]
                        ], [
                            'second',
                            [1, 10]
                        ], [
                            'minute',
                            [1, 5, 15]
                        ], [
                            'hour',
                            [1, 6]
                        ], [
                            'day',
                            [1]
                        ], [
                            'week',
                            [1]
                        ], [
                            'month',
                            [1]
                        ], [
                            'year',
                            null
                        ]]
                }, userOptions);
                // X-axis specific options
                if (this.coll === 'xAxis') {
                    // For linked axes, tickPixelInterval is used only if
                    // the tickPositioner below doesn't run or returns
                    // undefined (like multiple years)
                    if (defined(userOptions.linkedTo) &&
                        !defined(userOptions.tickPixelInterval)) {
                        gridAxisOptions.tickPixelInterval = 350;
                    }
                    // For the secondary grid axis, use the primary axis'
                    // tick intervals and return ticks one level higher.
                    if (
                    // Check for tick pixel interval in options
                    !defined(userOptions.tickPixelInterval) &&
                        // Only for linked axes
                        defined(userOptions.linkedTo) &&
                        !defined(userOptions.tickPositioner) &&
                        !defined(userOptions.tickInterval)) {
                        gridAxisOptions.tickPositioner = function (min, max) {
                            var parentInfo = (this.linkedParent &&
                                    this.linkedParent.tickPositions &&
                                    this.linkedParent.tickPositions.info);
                            if (parentInfo) {
                                var units = (gridAxisOptions.units || []);
                                var unitIdx = void 0,
                                    count = 1,
                                    unitName = 'year';
                                for (var i = 0; i < units.length; i++) {
                                    var unit_1 = units[i];
                                    if (unit_1 && unit_1[0] === parentInfo.unitName) {
                                        unitIdx = i;
                                        break;
                                    }
                                }
                                // Get the first allowed count on the next unit.
                                var unit = (isNumber(unitIdx) && units[unitIdx + 1]);
                                if (unit) {
                                    unitName = unit[0] || 'year';
                                    var counts = unit[1];
                                    count = counts && counts[0] || 1;
                                    // In case the base X axis shows years, make the
                                    // secondary axis show ten times the years (#11427)
                                }
                                else if (parentInfo.unitName === 'year') {
                                    // unitName is 'year'
                                    count = parentInfo.count * 10;
                                }
                                var unitRange = timeUnits[unitName];
                                this.tickInterval = unitRange * count;
                                return this.chart.time.getTimeTicks({ unitRange: unitRange, count: count, unitName: unitName }, min, max, this.options.startOfWeek);
                            }
                        };
                    }
                }
                // Now merge the combined options into the axis options
                merge(true, this.options, gridAxisOptions);
                if (this.horiz) {
                    /*               _________________________
                    Make this:    ___|_____|_____|_____|__|
                                    ^                     ^
                                    _________________________
                    Into this:    |_____|_____|_____|_____|
                                        ^                 ^    */
                    options.minPadding = pick(userOptions.minPadding, 0);
                    options.maxPadding = pick(userOptions.maxPadding, 0);
                }
                // If borderWidth is set, then use its value for tick and
                // line width.
                if (isNumber(options.grid.borderWidth)) {
                    options.tickWidth = options.lineWidth =
                        gridOptions.borderWidth;
                }
            }
        }
        /**
         * @private
         */
        function onAfterSetOptions2(e) {
            var axis = this;
            var userOptions = e.userOptions;
            var gridOptions = userOptions && userOptions.grid || {};
            var columns = gridOptions.columns;
            // Add column options to the parent axis. Children has their column
            // options set on init in onGridAxisAfterInit.
            if (gridOptions.enabled && columns) {
                merge(true, axis.options, columns[columns.length - 1]);
            }
        }
        /**
         * Handle columns and setScale.
         * @private
         */
        function onAfterSetScale() {
            var axis = this;
            (axis.grid.columns || []).forEach(function (column) { return column.setScale(); });
        }
        /**
         * Draw vertical axis ticks extra long to create cell floors and roofs.
         * Overrides the tickLength for vertical axes.
         * @private
         */
        function onAfterTickSize(e) {
            var defaultLeftAxisOptions = AxisDefaults.defaultLeftAxisOptions;
            var _a = this,
                horiz = _a.horiz,
                maxLabelDimensions = _a.maxLabelDimensions,
                _b = _a.options.grid,
                gridOptions = _b === void 0 ? {} : _b;
            if (gridOptions.enabled && maxLabelDimensions) {
                var labelPadding = (Math.abs(defaultLeftAxisOptions.labels.x) * 2);
                var distance = horiz ?
                        (gridOptions.cellHeight ||
                            labelPadding + maxLabelDimensions.height) :
                        labelPadding + maxLabelDimensions.width;
                if (isArray(e.tickSize)) {
                    e.tickSize[0] = distance;
                }
                else {
                    e.tickSize = [distance, 0];
                }
            }
        }
        /**
         * @private
         */
        function onChartAfterSetChartSize() {
            this.axes.forEach(function (axis) {
                (axis.grid && axis.grid.columns || []).forEach(function (column) {
                    column.setAxisSize();
                    column.setAxisTranslation();
                });
            });
        }
        /**
         * @private
         */
        function onDestroy(e) {
            var grid = this.grid;
            (grid.columns || []).forEach(function (column) { return column.destroy(e.keepEvents); });
            grid.columns = void 0;
        }
        /**
         * Wraps axis init to draw cell walls on vertical axes.
         * @private
         */
        function onInit(e) {
            var axis = this;
            var userOptions = e.userOptions || {};
            var gridOptions = userOptions.grid || {};
            if (gridOptions.enabled && defined(gridOptions.borderColor)) {
                userOptions.tickColor = userOptions.lineColor = (gridOptions.borderColor);
            }
            if (!axis.grid) {
                axis.grid = new GridAxisAdditions(axis);
            }
            axis.hiddenLabels = [];
            axis.hiddenMarks = [];
        }
        /**
         * Center tick labels in cells.
         * @private
         */
        function onTickAfterGetLabelPosition(e) {
            var tick = this,
                label = tick.label,
                axis = tick.axis,
                reversed = axis.reversed,
                chart = axis.chart,
                options = axis.options,
                gridOptions = options.grid || {},
                labelOpts = axis.options.labels,
                align = labelOpts.align, 
                // verticalAlign is currently not supported for axis.labels.
                verticalAlign = 'middle', // labelOpts.verticalAlign,
                side = GridAxisSide[axis.side],
                tickmarkOffset = e.tickmarkOffset,
                tickPositions = axis.tickPositions,
                tickPos = tick.pos - tickmarkOffset,
                nextTickPos = (isNumber(tickPositions[e.index + 1]) ?
                    tickPositions[e.index + 1] - tickmarkOffset :
                    (axis.max || 0) + tickmarkOffset),
                tickSize = axis.tickSize('tick'),
                tickWidth = tickSize ? tickSize[0] : 0,
                crispCorr = tickSize ? tickSize[1] / 2 : 0;
            var labelHeight,
                lblMetrics,
                lines,
                bottom,
                top,
                left,
                right;
            // Only center tick labels in grid axes
            if (gridOptions.enabled === true) {
                // Calculate top and bottom positions of the cell.
                if (side === 'top') {
                    bottom = axis.top + axis.offset;
                    top = bottom - tickWidth;
                }
                else if (side === 'bottom') {
                    top = chart.chartHeight - axis.bottom + axis.offset;
                    bottom = top + tickWidth;
                }
                else {
                    bottom = axis.top + axis.len - (axis.translate(reversed ? nextTickPos : tickPos) || 0);
                    top = axis.top + axis.len - (axis.translate(reversed ? tickPos : nextTickPos) || 0);
                }
                // Calculate left and right positions of the cell.
                if (side === 'right') {
                    left = chart.chartWidth - axis.right + axis.offset;
                    right = left + tickWidth;
                }
                else if (side === 'left') {
                    right = axis.left + axis.offset;
                    left = right - tickWidth;
                }
                else {
                    left = Math.round(axis.left + (axis.translate(reversed ? nextTickPos : tickPos) || 0)) - crispCorr;
                    right = Math.min(// #15742
                    Math.round(axis.left + (axis.translate(reversed ? tickPos : nextTickPos) || 0)) - crispCorr, axis.left + axis.len);
                }
                tick.slotWidth = right - left;
                // Calculate the positioning of the label based on
                // alignment.
                e.pos.x = (align === 'left' ?
                    left :
                    align === 'right' ?
                        right :
                        left + ((right - left) / 2) // default to center
                );
                e.pos.y = (verticalAlign === 'top' ?
                    top :
                    verticalAlign === 'bottom' ?
                        bottom :
                        top + ((bottom - top) / 2) // default to middle
                );
                lblMetrics = chart.renderer.fontMetrics(labelOpts.style.fontSize, label && label.element);
                labelHeight = label ? label.getBBox().height : 0;
                // Adjustment to y position to align the label correctly.
                // Would be better to have a setter or similar for this.
                if (!labelOpts.useHTML) {
                    lines = Math.round(labelHeight / lblMetrics.h);
                    e.pos.y += (
                    // Center the label
                    // TODO: why does this actually center the label?
                    ((lblMetrics.b - (lblMetrics.h - lblMetrics.f)) / 2) +
                        // Adjust for height of additional lines.
                        -(((lines - 1) * lblMetrics.h) / 2));
                }
                else {
                    e.pos.y += (
                    // Readjust yCorr in htmlUpdateTransform
                    lblMetrics.b +
                        // Adjust for height of html label
                        -(labelHeight / 2));
                }
                e.pos.x += (axis.horiz && labelOpts.x) || 0;
            }
        }
        /**
         * @private
         */
        function onTickLabelFormat(ctx) {
            var axis = ctx.axis,
                value = ctx.value;
            if (axis.options.grid &&
                axis.options.grid.enabled) {
                var tickPos = axis.tickPositions;
                var series = (axis.linkedParent || axis).series[0];
                var isFirst = value === tickPos[0];
                var isLast = value === tickPos[tickPos.length - 1];
                var point = series && find(series.options.data,
                    function (p) {
                        return p[axis.isXAxis ? 'x' : 'y'] === value;
                });
                var pointCopy = void 0;
                if (point && series.is('gantt')) {
                    // For the Gantt set point aliases to the pointCopy
                    // to do not change the original point
                    pointCopy = merge(point);
                    H.seriesTypes.gantt.prototype.pointClass
                        .setGanttPointAliases(pointCopy);
                }
                // Make additional properties available for the
                // formatter
                ctx.isFirst = isFirst;
                ctx.isLast = isLast;
                ctx.point = pointCopy;
            }
        }
        /**
         * Makes tick labels which are usually ignored in a linked axis
         * displayed if they are within range of linkedParent.min.
         * ```
         *                        _____________________________
         *                        |   |       |       |       |
         * Make this:             |   |   2   |   3   |   4   |
         *                        |___|_______|_______|_______|
         *                          ^
         *                        _____________________________
         *                        |   |       |       |       |
         * Into this:             | 1 |   2   |   3   |   4   |
         *                        |___|_______|_______|_______|
         *                          ^
         * ```
         * @private
         * @todo Does this function do what the drawing says? Seems to affect
         *       ticks and not the labels directly?
         */
        function onTrimTicks() {
            var axis = this;
            var options = axis.options;
            var gridOptions = options.grid || {};
            var categoryAxis = axis.categories;
            var tickPositions = axis.tickPositions;
            var firstPos = tickPositions[0];
            var lastPos = tickPositions[tickPositions.length - 1];
            var linkedMin = axis.linkedParent && axis.linkedParent.min;
            var linkedMax = axis.linkedParent && axis.linkedParent.max;
            var min = linkedMin || axis.min;
            var max = linkedMax || axis.max;
            var tickInterval = axis.tickInterval;
            var endMoreThanMin = (firstPos < min &&
                    firstPos + tickInterval > min);
            var startLessThanMax = (lastPos > max &&
                    lastPos - tickInterval < max);
            if (gridOptions.enabled === true &&
                !categoryAxis &&
                (axis.horiz || axis.isLinked)) {
                if (endMoreThanMin && !options.startOnTick) {
                    tickPositions[0] = min;
                }
                if (startLessThanMax && !options.endOnTick) {
                    tickPositions[tickPositions.length - 1] = max;
                }
            }
        }
        /**
         * Avoid altering tickInterval when reserving space.
         * @private
         */
        function wrapUnsquish(proceed) {
            var axis = this;
            var _a = axis.options.grid,
                gridOptions = _a === void 0 ? {} : _a;
            if (gridOptions.enabled === true && axis.categories) {
                return axis.tickInterval;
            }
            return proceed.apply(axis, argsToArray(arguments));
        }
        /* *
         *
         *  Class
         *
         * */
        /**
         * Additions for grid axes.
         * @private
         * @class
         */
        var GridAxisAdditions = /** @class */ (function () {
                /* *
                *
                *  Constructors
                *
                * */
                function GridAxisAdditions(axis) {
                    this.axis = axis;
            }
            /* *
            *
            *  Functions
            *
            * */
            /**
             * Checks if an axis is the outer axis in its dimension. Since
             * axes are placed outwards in order, the axis with the highest
             * index is the outermost axis.
             *
             * Example: If there are multiple x-axes at the top of the chart,
             * this function returns true if the axis supplied is the last
             * of the x-axes.
             *
             * @private
             *
             * @return {boolean}
             * True if the axis is the outermost axis in its dimension; false if
             * not.
             */
            GridAxisAdditions.prototype.isOuterAxis = function () {
                var axis = this.axis;
                var chart = axis.chart;
                var columnIndex = axis.grid.columnIndex;
                var columns = (axis.linkedParent && axis.linkedParent.grid.columns ||
                        axis.grid.columns);
                var parentAxis = columnIndex ? axis.linkedParent : axis;
                var thisIndex = -1,
                    lastIndex = 0;
                (chart[axis.coll] || []).forEach(function (otherAxis, index) {
                    if (otherAxis.side === axis.side &&
                        !otherAxis.options.isInternal) {
                        lastIndex = index;
                        if (otherAxis === parentAxis) {
                            // Get the index of the axis in question
                            thisIndex = index;
                        }
                    }
                });
                return (lastIndex === thisIndex &&
                    (isNumber(columnIndex) ?
                        columns.length === columnIndex :
                        true));
            };
            /**
             * Add extra border based on the provided path.
             * @private
             * @param {SVGPath} path
             * The path of the border.
             * @return {Highcharts.SVGElement}
             * Border
             */
            GridAxisAdditions.prototype.renderBorder = function (path) {
                var axis = this.axis,
                    renderer = axis.chart.renderer,
                    options = axis.options,
                    extraBorderLine = renderer.path(path)
                        .addClass('highcharts-axis-line')
                        .add(axis.axisBorder);
                if (!renderer.styledMode) {
                    extraBorderLine.attr({
                        stroke: options.lineColor,
                        'stroke-width': options.lineWidth,
                        zIndex: 7
                    });
                }
                return extraBorderLine;
            };
            return GridAxisAdditions;
        }());
        /* *
         *
         *  Registry
         *
         * */
        // First letter of the day of the week, e.g. 'M' for 'Monday'.
        dateFormats.E = function (timestamp) {
            return this.dateFormat('%a', timestamp, true).charAt(0);
        };
        // Adds week date format
        dateFormats.W = function (timestamp) {
            var time = this, d = new this.Date(timestamp), unitsToOmit = ['Hours', 'Milliseconds', 'Minutes', 'Seconds'];
            unitsToOmit.forEach(function (format) {
                time.set(format, d, 0);
            });
            var firstDay = (this.get('Day',
                d) + 6) % 7;
            var thursday = new this.Date(d.valueOf());
            this.set('Date', thursday, this.get('Date', d) - firstDay + 3);
            var firstThursday = new this.Date(this.get('FullYear',
                thursday), 0, 1);
            if (this.get('Day', firstThursday) !== 4) {
                this.set('Month', d, 0);
                this.set('Date', d, 1 + (11 - this.get('Day', firstThursday)) % 7);
            }
            return (1 +
                Math.floor((thursday.valueOf() - firstThursday.valueOf()) / 604800000)).toString();
        };
        /* *
         *
         *  Default Export
         *
         * */
        var GridAxis = {
                compose: compose
            };
        /* *
         *
         *  API Options
         *
         * */
        /**
         * @productdesc {gantt}
         * For grid axes (like in Gantt charts),
         * it is possible to declare as a list to provide different
         * formats depending on available space.
         *
         * Defaults to:
         * ```js
         * {
         *     hour: { list: ['%H:%M', '%H'] },
         *     day: { list: ['%A, %e. %B', '%a, %e. %b', '%E'] },
         *     week: { list: ['Week %W', 'W%W'] },
         *     month: { list: ['%B', '%b', '%o'] }
         * }
         * ```
         *
         * @sample {gantt} gantt/grid-axis/date-time-label-formats
         *         Gantt chart with custom axis date format.
         *
         * @apioption xAxis.dateTimeLabelFormats
         */
        /**
         * Set grid options for the axis labels. Requires Highcharts Gantt.
         *
         * @since     6.2.0
         * @product   gantt
         * @apioption xAxis.grid
         */
        /**
         * Enable grid on the axis labels. Defaults to true for Gantt charts.
         *
         * @type      {boolean}
         * @default   true
         * @since     6.2.0
         * @product   gantt
         * @apioption xAxis.grid.enabled
         */
        /**
         * Set specific options for each column (or row for horizontal axes) in the
         * grid. Each extra column/row is its own axis, and the axis options can be set
         * here.
         *
         * @sample gantt/demo/left-axis-table
         *         Left axis as a table
         *
         * @type      {Array<Highcharts.XAxisOptions>}
         * @apioption xAxis.grid.columns
         */
        /**
         * Set border color for the label grid lines.
         *
         * @type      {Highcharts.ColorString}
         * @apioption xAxis.grid.borderColor
         */
        /**
         * Set border width of the label grid lines.
         *
         * @type      {number}
         * @default   1
         * @apioption xAxis.grid.borderWidth
         */
        /**
         * Set cell height for grid axis labels. By default this is calculated from font
         * size. This option only applies to horizontal axes.
         *
         * @sample gantt/grid-axis/cellheight
         *         Gant chart with custom cell height
         * @type      {number}
         * @apioption xAxis.grid.cellHeight
         */
        ''; // keeps doclets above in JS file

        return GridAxis;
    });
    _registerModule(_modules, 'Gantt/Tree.js', [_modules['Core/Utilities.js']], function (U) {
        /* *
         *
         *  (c) 2016-2021 Highsoft AS
         *
         *  Authors: Jon Arild Nygard
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /* eslint no-console: 0 */
        var extend = U.extend,
            isNumber = U.isNumber,
            pick = U.pick;
        /**
         * Creates an object map from parent id to childrens index.
         *
         * @private
         * @function Highcharts.Tree#getListOfParents
         *
         * @param {Array<*>} data
         *        List of points set in options. `Array.parent` is parent id of point.
         *
         * @param {Array<string>} ids
         *        List of all point ids.
         *
         * @return {Highcharts.Dictionary<Array<*>>}
         *         Map from parent id to children index in data
         */
        var getListOfParents = function (data,
            ids) {
                var listOfParents = data.reduce(function (prev,
            curr) {
                    var parent = pick(curr.parent, '');
                if (typeof prev[parent] === 'undefined') {
                    prev[parent] = [];
                }
                prev[parent].push(curr);
                return prev;
            }, {}), parents = Object.keys(listOfParents);
            // If parent does not exist, hoist parent to root of tree.
            parents.forEach(function (parent, list) {
                var children = listOfParents[parent];
                if ((parent !== '') && (ids.indexOf(parent) === -1)) {
                    children.forEach(function (child) {
                        list[''].push(child);
                    });
                    delete list[parent];
                }
            });
            return listOfParents;
        };
        var getNode = function (id,
            parent,
            level,
            data,
            mapOfIdToChildren,
            options) {
                var descendants = 0,
            height = 0,
            after = options && options.after,
            before = options && options.before,
            node = {
                    data: data,
                    depth: level - 1,
                    id: id,
                    level: level,
                    parent: parent
                },
            start,
            end,
            children;
            // Allow custom logic before the children has been created.
            if (typeof before === 'function') {
                before(node, options);
            }
            // Call getNode recursively on the children. Calulate the height of the
            // node, and the number of descendants.
            children = ((mapOfIdToChildren[id] || [])).map(function (child) {
                var node = getNode(child.id,
                    id, (level + 1),
                    child,
                    mapOfIdToChildren,
                    options),
                    childStart = child.start,
                    childEnd = (child.milestone === true ?
                        childStart :
                        child.end);
                // Start should be the lowest child.start.
                start = ((!isNumber(start) || childStart < start) ?
                    childStart :
                    start);
                // End should be the largest child.end.
                // If child is milestone, then use start as end.
                end = ((!isNumber(end) || childEnd > end) ?
                    childEnd :
                    end);
                descendants = descendants + 1 + node.descendants;
                height = Math.max(node.height + 1, height);
                return node;
            });
            // Calculate start and end for point if it is not already explicitly set.
            if (data) {
                data.start = pick(data.start, start);
                data.end = pick(data.end, end);
            }
            extend(node, {
                children: children,
                descendants: descendants,
                height: height
            });
            // Allow custom logic after the children has been created.
            if (typeof after === 'function') {
                after(node, options);
            }
            return node;
        };
        var getTree = function (data,
            options) {
                var ids = data.map(function (d) {
                    return d.id;
            }), mapOfIdToChildren = getListOfParents(data, ids);
            return getNode('', null, 1, null, mapOfIdToChildren, options);
        };
        var Tree = {
                getListOfParents: getListOfParents,
                getNode: getNode,
                getTree: getTree
            };

        return Tree;
    });
    _registerModule(_modules, 'Core/Axis/TreeGrid/TreeGridTick.js', [_modules['Core/Utilities.js']], function (U) {
        /* *
         *
         *  (c) 2016 Highsoft AS
         *  Authors: Jon Arild Nygard
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var addEvent = U.addEvent,
            isObject = U.isObject,
            isNumber = U.isNumber,
            pick = U.pick,
            wrap = U.wrap;
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
        function onTickInit() {
            var tick = this;
            if (!tick.treeGrid) {
                tick.treeGrid = new TreeGridTickAdditions(tick);
            }
        }
        /**
         * @private
         */
        function onTickHover(label) {
            label.addClass('highcharts-treegrid-node-active');
            if (!label.renderer.styledMode) {
                label.css({
                    textDecoration: 'underline'
                });
            }
        }
        /**
         * @private
         */
        function onTickHoverExit(label, options) {
            var css = isObject(options.style) ? options.style : {};
            label.removeClass('highcharts-treegrid-node-active');
            if (!label.renderer.styledMode) {
                label.css({ textDecoration: css.textDecoration });
            }
        }
        /**
         * @private
         */
        function renderLabelIcon(tick, params) {
            var treeGrid = tick.treeGrid,
                isNew = !treeGrid.labelIcon,
                renderer = params.renderer,
                labelBox = params.xy,
                options = params.options,
                width = options.width || 0,
                height = options.height || 0,
                iconCenter = {
                    x: labelBox.x - (width / 2) - (options.padding || 0),
                    y: labelBox.y - (height / 2)
                },
                rotation = params.collapsed ? 90 : 180,
                shouldRender = params.show && isNumber(iconCenter.y);
            var icon = treeGrid.labelIcon;
            if (!icon) {
                treeGrid.labelIcon = icon = renderer
                    .path(renderer.symbols[options.type](options.x || 0, options.y || 0, width, height))
                    .addClass('highcharts-label-icon')
                    .add(params.group);
            }
            // Set the new position, and show or hide
            icon[shouldRender ? 'show' : 'hide'](); // #14904, #1338
            // Presentational attributes
            if (!renderer.styledMode) {
                icon
                    .attr({
                    cursor: 'pointer',
                    'fill': pick(params.color, "#666666" /* Palette.neutralColor60 */),
                    'stroke-width': 1,
                    stroke: options.lineColor,
                    strokeWidth: options.lineWidth || 0
                });
            }
            // Update the icon positions
            icon[isNew ? 'attr' : 'animate']({
                translateX: iconCenter.x,
                translateY: iconCenter.y,
                rotation: rotation
            });
        }
        /**
         * @private
         */
        function wrapGetLabelPosition(proceed, x, y, label, horiz, labelOptions, tickmarkOffset, index, step) {
            var tick = this,
                lbOptions = pick(tick.options && tick.options.labels,
                labelOptions),
                pos = tick.pos,
                axis = tick.axis,
                options = axis.options,
                isTreeGrid = options.type === 'treegrid',
                result = proceed.apply(tick,
                [x,
                y,
                label,
                horiz,
                lbOptions,
                tickmarkOffset,
                index,
                step]);
            var symbolOptions,
                indentation,
                mapOfPosToGridNode,
                node,
                level;
            if (isTreeGrid) {
                symbolOptions = (lbOptions && isObject(lbOptions.symbol, true) ?
                    lbOptions.symbol :
                    {});
                indentation = (lbOptions && isNumber(lbOptions.indentation) ?
                    lbOptions.indentation :
                    0);
                mapOfPosToGridNode = axis.treeGrid.mapOfPosToGridNode;
                node = mapOfPosToGridNode && mapOfPosToGridNode[pos];
                level = (node && node.depth) || 1;
                result.x += (
                // Add space for symbols
                ((symbolOptions.width || 0) +
                    ((symbolOptions.padding || 0) * 2)) +
                    // Apply indentation
                    ((level - 1) * indentation));
            }
            return result;
        }
        /**
         * @private
         */
        function wrapRenderLabel(proceed) {
            var tick = this, pos = tick.pos, axis = tick.axis, label = tick.label, mapOfPosToGridNode = axis.treeGrid.mapOfPosToGridNode, options = axis.options, labelOptions = pick(tick.options && tick.options.labels, options && options.labels), symbolOptions = (labelOptions && isObject(labelOptions.symbol, true) ?
                    labelOptions.symbol :
                    {}), node = mapOfPosToGridNode && mapOfPosToGridNode[pos], level = node && node.depth, isTreeGrid = options.type === 'treegrid', shouldRender = axis.tickPositions.indexOf(pos) > -1, prefixClassName = 'highcharts-treegrid-node-', styledMode = axis.chart.styledMode;
            var collapsed,
                addClassName,
                removeClassName;
            if (isTreeGrid && node) {
                // Add class name for hierarchical styling.
                if (label &&
                    label.element) {
                    label.addClass(prefixClassName + 'level-' + level);
                }
            }
            proceed.apply(tick, Array.prototype.slice.call(arguments, 1));
            if (isTreeGrid &&
                label &&
                label.element &&
                node &&
                node.descendants &&
                node.descendants > 0) {
                collapsed = axis.treeGrid.isCollapsed(node);
                renderLabelIcon(tick, {
                    color: (!styledMode &&
                        label.styles &&
                        label.styles.color ||
                        ''),
                    collapsed: collapsed,
                    group: label.parentGroup,
                    options: symbolOptions,
                    renderer: label.renderer,
                    show: shouldRender,
                    xy: label.xy
                });
                // Add class name for the node.
                addClassName = prefixClassName +
                    (collapsed ? 'collapsed' : 'expanded');
                removeClassName = prefixClassName +
                    (collapsed ? 'expanded' : 'collapsed');
                label
                    .addClass(addClassName)
                    .removeClass(removeClassName);
                if (!styledMode) {
                    label.css({
                        cursor: 'pointer'
                    });
                }
                // Add events to both label text and icon
                [label, tick.treeGrid.labelIcon].forEach(function (object) {
                    if (object && !object.attachedTreeGridEvents) {
                        // On hover
                        addEvent(object.element, 'mouseover', function () {
                            onTickHover(label);
                        });
                        // On hover out
                        addEvent(object.element, 'mouseout', function () {
                            onTickHoverExit(label, labelOptions);
                        });
                        addEvent(object.element, 'click', function () {
                            tick.treeGrid.toggleCollapse();
                        });
                        object.attachedTreeGridEvents = true;
                    }
                });
            }
        }
        /* *
         *
         *  Classes
         *
         * */
        /**
         * @private
         * @class
         */
        var TreeGridTickAdditions = /** @class */ (function () {
                /* *
                 *
                 *  Constructors
                 *
                 * */
                /**
                 * @private
                 */
                function TreeGridTickAdditions(tick) {
                    this.tick = tick;
            }
            /* *
             *
             *  Static Functions
             *
             * */
            /**
             * @private
             */
            TreeGridTickAdditions.compose = function (TickClass) {
                if (composedClasses.indexOf(TickClass) === -1) {
                    composedClasses.push(TickClass);
                    addEvent(TickClass, 'init', onTickInit);
                    wrap(TickClass.prototype, 'getLabelPosition', wrapGetLabelPosition);
                    wrap(TickClass.prototype, 'renderLabel', wrapRenderLabel);
                    // backwards compatibility
                    TickClass.prototype.collapse = function (redraw) {
                        this.treeGrid.collapse(redraw);
                    };
                    TickClass.prototype.expand = function (redraw) {
                        this.treeGrid.expand(redraw);
                    };
                    TickClass.prototype.toggleCollapse = function (redraw) {
                        this.treeGrid.toggleCollapse(redraw);
                    };
                }
            };
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Collapse the grid cell. Used when axis is of type treegrid.
             *
             * @see gantt/treegrid-axis/collapsed-dynamically/demo.js
             *
             * @private
             * @function Highcharts.Tick#collapse
             *
             * @param {boolean} [redraw=true]
             * Whether to redraw the chart or wait for an explicit call to
             * {@link Highcharts.Chart#redraw}
             */
            TreeGridTickAdditions.prototype.collapse = function (redraw) {
                var tick = this.tick,
                    axis = tick.axis,
                    brokenAxis = axis.brokenAxis;
                if (brokenAxis &&
                    axis.treeGrid.mapOfPosToGridNode) {
                    var pos = tick.pos,
                        node = axis.treeGrid.mapOfPosToGridNode[pos],
                        breaks = axis.treeGrid.collapse(node);
                    brokenAxis.setBreaks(breaks, pick(redraw, true));
                }
            };
            /**
             * Destroy remaining labelIcon if exist.
             *
             * @private
             * @function Highcharts.Tick#destroy
             */
            TreeGridTickAdditions.prototype.destroy = function () {
                if (this.labelIcon) {
                    this.labelIcon.destroy();
                }
            };
            /**
             * Expand the grid cell. Used when axis is of type treegrid.
             *
             * @see gantt/treegrid-axis/collapsed-dynamically/demo.js
             *
             * @private
             * @function Highcharts.Tick#expand
             *
             * @param {boolean} [redraw=true]
             * Whether to redraw the chart or wait for an explicit call to
             * {@link Highcharts.Chart#redraw}
             */
            TreeGridTickAdditions.prototype.expand = function (redraw) {
                var tick = this.tick,
                    axis = tick.axis,
                    brokenAxis = axis.brokenAxis;
                if (brokenAxis &&
                    axis.treeGrid.mapOfPosToGridNode) {
                    var pos = tick.pos,
                        node = axis.treeGrid.mapOfPosToGridNode[pos],
                        breaks = axis.treeGrid.expand(node);
                    brokenAxis.setBreaks(breaks, pick(redraw, true));
                }
            };
            /**
             * Toggle the collapse/expand state of the grid cell. Used when axis is
             * of type treegrid.
             *
             * @see gantt/treegrid-axis/collapsed-dynamically/demo.js
             *
             * @private
             * @function Highcharts.Tick#toggleCollapse
             *
             * @param {boolean} [redraw=true]
             * Whether to redraw the chart or wait for an explicit call to
             * {@link Highcharts.Chart#redraw}
             */
            TreeGridTickAdditions.prototype.toggleCollapse = function (redraw) {
                var tick = this.tick,
                    axis = tick.axis,
                    brokenAxis = axis.brokenAxis;
                if (brokenAxis &&
                    axis.treeGrid.mapOfPosToGridNode) {
                    var pos = tick.pos,
                        node = axis.treeGrid.mapOfPosToGridNode[pos],
                        breaks = axis.treeGrid.toggleCollapse(node);
                    brokenAxis.setBreaks(breaks, pick(redraw, true));
                }
            };
            return TreeGridTickAdditions;
        }());
        /* *
         *
         *  Default Export
         *
         * */

        return TreeGridTickAdditions;
    });
    _registerModule(_modules, 'Series/TreeUtilities.js', [_modules['Core/Color/Color.js'], _modules['Core/Utilities.js']], function (Color, U) {
        /* *
         *
         *  (c) 2014-2021 Highsoft AS
         *
         *  Authors: Jon Arild Nygard / Oystein Moseng
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var extend = U.extend,
            isArray = U.isArray,
            isNumber = U.isNumber,
            isObject = U.isObject,
            merge = U.merge,
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
        function getColor(node, options) {
            var index = options.index,
                mapOptionsToLevel = options.mapOptionsToLevel,
                parentColor = options.parentColor,
                parentColorIndex = options.parentColorIndex,
                series = options.series,
                colors = options.colors,
                siblings = options.siblings,
                points = series.points,
                chartOptionsChart = series.chart.options.chart;
            var getColorByPoint,
                point,
                level,
                colorByPoint,
                colorIndexByPoint,
                color,
                colorIndex;
            /**
             * @private
             */
            var variateColor = function (color) {
                    var colorVariation = level && level.colorVariation;
                if (colorVariation &&
                    colorVariation.key === 'brightness' &&
                    index &&
                    siblings) {
                    return Color.parse(color).brighten(colorVariation.to * (index / siblings)).get();
                }
                return color;
            };
            if (node) {
                point = points[node.i];
                level = mapOptionsToLevel[node.level] || {};
                getColorByPoint = point && level.colorByPoint;
                if (getColorByPoint) {
                    colorIndexByPoint = point.index % (colors ?
                        colors.length :
                        chartOptionsChart.colorCount);
                    colorByPoint = colors && colors[colorIndexByPoint];
                }
                // Select either point color, level color or inherited color.
                if (!series.chart.styledMode) {
                    color = pick(point && point.options.color, level && level.color, colorByPoint, parentColor && variateColor(parentColor), series.color);
                }
                colorIndex = pick(point && point.options.colorIndex, level && level.colorIndex, colorIndexByPoint, parentColorIndex, options.colorIndex);
            }
            return {
                color: color,
                colorIndex: colorIndex
            };
        }
        /**
         * Creates a map from level number to its given options.
         *
         * @private
         *
         * @param {Object} params
         * Object containing parameters.
         * - `defaults` Object containing default options. The default options are
         *   merged with the userOptions to get the final options for a specific
         *   level.
         * - `from` The lowest level number.
         * - `levels` User options from series.levels.
         * - `to` The highest level number.
         *
         * @return {Highcharts.Dictionary<object>|null}
         * Returns a map from level number to its given options.
         */
        function getLevelOptions(params) {
            var result = {},
                defaults,
                converted,
                i,
                from,
                to,
                levels;
            if (isObject(params)) {
                from = isNumber(params.from) ? params.from : 1;
                levels = params.levels;
                converted = {};
                defaults = isObject(params.defaults) ? params.defaults : {};
                if (isArray(levels)) {
                    converted = levels.reduce(function (obj, item) {
                        var level,
                            levelIsConstant,
                            options;
                        if (isObject(item) && isNumber(item.level)) {
                            options = merge({}, item);
                            levelIsConstant = pick(options.levelIsConstant, defaults.levelIsConstant);
                            // Delete redundant properties.
                            delete options.levelIsConstant;
                            delete options.level;
                            // Calculate which level these options apply to.
                            level = item.level + (levelIsConstant ? 0 : from - 1);
                            if (isObject(obj[level])) {
                                merge(true, obj[level], options); // #16329
                            }
                            else {
                                obj[level] = options;
                            }
                        }
                        return obj;
                    }, {});
                }
                to = isNumber(params.to) ? params.to : 1;
                for (i = 0; i <= to; i++) {
                    result[i] = merge({}, defaults, isObject(converted[i]) ? converted[i] : {});
                }
            }
            return result;
        }
        /**
         * @private
         * @todo Combine buildTree and buildNode with setTreeValues
         * @todo Remove logic from Treemap and make it utilize this mixin.
         */
        function setTreeValues(tree, options) {
            var before = options.before,
                idRoot = options.idRoot,
                mapIdToNode = options.mapIdToNode,
                nodeRoot = mapIdToNode[idRoot],
                levelIsConstant = (options.levelIsConstant !== false),
                points = options.points,
                point = points[tree.i],
                optionsPoint = point && point.options || {},
                children = [];
            var childrenTotal = 0;
            tree.levelDynamic = tree.level - (levelIsConstant ? 0 : nodeRoot.level);
            tree.name = pick(point && point.name, '');
            tree.visible = (idRoot === tree.id ||
                options.visible === true);
            if (typeof before === 'function') {
                tree = before(tree, options);
            }
            // First give the children some values
            tree.children.forEach(function (child, i) {
                var newOptions = extend({},
                    options);
                extend(newOptions, {
                    index: i,
                    siblings: tree.children.length,
                    visible: tree.visible
                });
                child = setTreeValues(child, newOptions);
                children.push(child);
                if (child.visible) {
                    childrenTotal += child.val;
                }
            });
            // Set the values
            var value = pick(optionsPoint.value,
                childrenTotal);
            tree.visible = value >= 0 && (childrenTotal > 0 || tree.visible);
            tree.children = children;
            tree.childrenTotal = childrenTotal;
            tree.isLeaf = tree.visible && !childrenTotal;
            tree.val = value;
            return tree;
        }
        /**
         * Update the rootId property on the series. Also makes sure that it is
         * accessible to exporting.
         *
         * @private
         *
         * @param {Object} series
         * The series to operate on.
         *
         * @return {string}
         * Returns the resulting rootId after update.
         */
        function updateRootId(series) {
            var rootId,
                options;
            if (isObject(series)) {
                // Get the series options.
                options = isObject(series.options) ? series.options : {};
                // Calculate the rootId.
                rootId = pick(series.rootNode, options.rootId, '');
                // Set rootId on series.userOptions to pick it up in exporting.
                if (isObject(series.userOptions)) {
                    series.userOptions.rootId = rootId;
                }
                // Set rootId on series to pick it up on next update.
                series.rootNode = rootId;
            }
            return rootId;
        }
        /* *
         *
         *  Default Export
         *
         * */
        var TreeUtilities = {
                getColor: getColor,
                getLevelOptions: getLevelOptions,
                setTreeValues: setTreeValues,
                updateRootId: updateRootId
            };

        return TreeUtilities;
    });
    _registerModule(_modules, 'Core/Axis/TreeGrid/TreeGridAxis.js', [_modules['Core/Axis/BrokenAxis.js'], _modules['Core/Axis/GridAxis.js'], _modules['Gantt/Tree.js'], _modules['Core/Axis/TreeGrid/TreeGridTick.js'], _modules['Series/TreeUtilities.js'], _modules['Core/Utilities.js']], function (BrokenAxis, GridAxis, Tree, TreeGridTick, TU, U) {
        /* *
         *
         *  (c) 2016 Highsoft AS
         *  Authors: Jon Arild Nygard
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var getLevelOptions = TU.getLevelOptions;
        var addEvent = U.addEvent,
            find = U.find,
            fireEvent = U.fireEvent,
            isArray = U.isArray,
            isObject = U.isObject,
            isString = U.isString,
            merge = U.merge,
            pick = U.pick,
            wrap = U.wrap;
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
        var TickConstructor;
        /* *
         *
         *  Functions
         *
         * */
        /**
         * @private
         */
        function getBreakFromNode(node, max) {
            var to = node.collapseEnd || 0;
            var from = node.collapseStart || 0;
            // In broken-axis, the axis.max is minimized until it is not within a
            // break. Therefore, if break.to is larger than axis.max, the axis.to
            // should not add the 0.5 axis.tickMarkOffset, to avoid adding a break
            // larger than axis.max.
            // TODO consider simplifying broken-axis and this might solve itself
            if (to >= max) {
                from -= 0.5;
            }
            return {
                from: from,
                to: to,
                showPoints: false
            };
        }
        /**
         * Creates a tree structure of the data, and the treegrid. Calculates
         * categories, and y-values of points based on the tree.
         *
         * @private
         * @function getTreeGridFromData
         *
         * @param {Array<Highcharts.GanttPointOptions>} data
         * All the data points to display in the axis.
         *
         * @param {boolean} uniqueNames
         * Whether or not the data node with the same name should share grid cell. If
         * true they do share cell. False by default.
         *
         * @param {number} numberOfSeries
         *
         * @return {Object}
         * Returns an object containing categories, mapOfIdToNode,
         * mapOfPosToGridNode, and tree.
         *
         * @todo There should be only one point per line.
         * @todo It should be optional to have one category per point, or merge
         *       cells
         * @todo Add unit-tests.
         */
        function getTreeGridFromData(data, uniqueNames, numberOfSeries) {
            var categories = [],
                collapsedNodes = [],
                mapOfIdToNode = {},
                uniqueNamesEnabled = typeof uniqueNames === 'boolean' ?
                    uniqueNames : false;
            var mapOfPosToGridNode = {},
                posIterator = -1;
            // Build the tree from the series data.
            var treeParams = {
                    // After the children has been created.
                    after: function (node) {
                        var gridNode = mapOfPosToGridNode[node.pos];
                    var height = 0,
                        descendants = 0;
                    gridNode.children.forEach(function (child) {
                        descendants += (child.descendants || 0) + 1;
                        height = Math.max((child.height || 0) + 1, height);
                    });
                    gridNode.descendants = descendants;
                    gridNode.height = height;
                    if (gridNode.collapsed) {
                        collapsedNodes.push(gridNode);
                    }
                },
                // Before the children has been created.
                before: function (node) {
                    var data = isObject(node.data,
                        true) ?
                            node.data :
                            {},
                        name = isString(data.name) ? data.name : '',
                        parentNode = mapOfIdToNode[node.parent],
                        parentGridNode = (isObject(parentNode,
                        true) ?
                            mapOfPosToGridNode[parentNode.pos] :
                            null),
                        hasSameName = function (x) {
                            return x.name === name;
                    };
                    var gridNode,
                        pos;
                    // If not unique names, look for sibling node with the same name
                    if (uniqueNamesEnabled &&
                        isObject(parentGridNode, true) &&
                        !!(gridNode = find(parentGridNode.children, hasSameName))) {
                        // If there is a gridNode with the same name, reuse position
                        pos = gridNode.pos;
                        // Add data node to list of nodes in the grid node.
                        gridNode.nodes.push(node);
                    }
                    else {
                        // If it is a new grid node, increment position.
                        pos = posIterator++;
                    }
                    // Add new grid node to map.
                    if (!mapOfPosToGridNode[pos]) {
                        mapOfPosToGridNode[pos] = gridNode = {
                            depth: parentGridNode ? parentGridNode.depth + 1 : 0,
                            name: name,
                            id: data.id,
                            nodes: [node],
                            children: [],
                            pos: pos
                        };
                        // If not root, then add name to categories.
                        if (pos !== -1) {
                            categories.push(name);
                        }
                        // Add name to list of children.
                        if (isObject(parentGridNode, true)) {
                            parentGridNode.children.push(gridNode);
                        }
                    }
                    // Add data node to map
                    if (isString(node.id)) {
                        mapOfIdToNode[node.id] = node;
                    }
                    // If one of the points are collapsed, then start the grid node
                    // in collapsed state.
                    if (gridNode &&
                        data.collapsed === true) {
                        gridNode.collapsed = true;
                    }
                    // Assign pos to data node
                    node.pos = pos;
                }
            };
            var updateYValuesAndTickPos = function (map,
                numberOfSeries) {
                    var setValues = function (gridNode,
                start,
                result) {
                        var nodes = gridNode.nodes,
                padding = 0.5;
                    var end = start + (start === -1 ? 0 : numberOfSeries - 1);
                    var diff = (end - start) / 2,
                        pos = start + diff;
                    nodes.forEach(function (node) {
                        var data = node.data;
                        if (isObject(data, true)) {
                            // Update point
                            data.y = start + (data.seriesIndex || 0);
                            // Remove the property once used
                            delete data.seriesIndex;
                        }
                        node.pos = pos;
                    });
                    result[pos] = gridNode;
                    gridNode.pos = pos;
                    gridNode.tickmarkOffset = diff + padding;
                    gridNode.collapseStart = end + padding;
                    gridNode.children.forEach(function (child) {
                        setValues(child, end + 1, result);
                        end = (child.collapseEnd || 0) - padding;
                    });
                    // Set collapseEnd to the end of the last child node.
                    gridNode.collapseEnd = end + padding;
                    return result;
                };
                return setValues(map['-1'], -1, {});
            };
            // Create tree from data
            var tree = Tree.getTree(data,
                treeParams);
            // Update y values of data, and set calculate tick positions.
            mapOfPosToGridNode = updateYValuesAndTickPos(mapOfPosToGridNode, numberOfSeries);
            // Return the resulting data.
            return {
                categories: categories,
                mapOfIdToNode: mapOfIdToNode,
                mapOfPosToGridNode: mapOfPosToGridNode,
                collapsedNodes: collapsedNodes,
                tree: tree
            };
        }
        /**
         * Builds the tree of categories and calculates its positions.
         * @private
         * @param {Object} e Event object
         * @param {Object} e.target The chart instance which the event was fired on.
         * @param {object[]} e.target.axes The axes of the chart.
         */
        function onBeforeRender(e) {
            var chart = e.target,
                axes = chart.axes;
            axes.filter(function (axis) {
                return axis.options.type === 'treegrid';
            }).forEach(function (axis) {
                var options = axis.options || {},
                    labelOptions = options.labels,
                    uniqueNames = options.uniqueNames,
                    max = options.max, 
                    // Check whether any of series is rendering for the first
                    // time, visibility has changed, or its data is dirty, and
                    // only then update. #10570, #10580. Also check if
                    // mapOfPosToGridNode exists. #10887
                    isDirty = (!axis.treeGrid.mapOfPosToGridNode ||
                        axis.series.some(function (series) {
                            return !series.hasRendered ||
                                series.isDirtyData ||
                                series.isDirty;
                    }));
                var numberOfSeries = 0,
                    data,
                    treeGrid;
                if (isDirty) {
                    // Concatenate data from all series assigned to this axis.
                    data = axis.series.reduce(function (arr, s) {
                        if (s.visible) {
                            // Push all data to array
                            (s.options.data || []).forEach(function (data) {
                                // For using keys - rebuild the data structure
                                if (s.options.keys && s.options.keys.length) {
                                    data = s.pointClass.prototype
                                        .optionsToObject
                                        .call({ series: s }, data);
                                    s.pointClass.setGanttPointAliases(data);
                                }
                                if (isObject(data, true)) {
                                    // Set series index on data. Removed again
                                    // after use.
                                    data.seriesIndex = (numberOfSeries);
                                    arr.push(data);
                                }
                            });
                            // Increment series index
                            if (uniqueNames === true) {
                                numberOfSeries++;
                            }
                        }
                        return arr;
                    }, []);
                    // If max is higher than set data - add a
                    // dummy data to render categories #10779
                    if (max && data.length < max) {
                        for (var i = data.length; i <= max; i++) {
                            data.push({
                                // Use the zero-width character
                                // to avoid conflict with uniqueNames
                                name: i + '\u200B'
                            });
                        }
                    }
                    // setScale is fired after all the series is initialized,
                    // which is an ideal time to update the axis.categories.
                    treeGrid = getTreeGridFromData(data, uniqueNames || false, (uniqueNames === true) ? numberOfSeries : 1);
                    // Assign values to the axis.
                    axis.categories = treeGrid.categories;
                    axis.treeGrid.mapOfPosToGridNode = (treeGrid.mapOfPosToGridNode);
                    axis.hasNames = true;
                    axis.treeGrid.tree = treeGrid.tree;
                    // Update yData now that we have calculated the y values
                    axis.series.forEach(function (series) {
                        var axisData = (series.options.data || []).map(function (d) {
                                if (isArray(d) &&
                                    series.options.keys &&
                                    series.options.keys.length) {
                                    // Get the axisData from the data array used to
                                    // build the treeGrid where has been modified
                                    data.forEach(function (point) {
                                        if (d.indexOf(point.x) >= 0 &&
                                            d.indexOf(point.x2) >= 0) {
                                            d = point;
                                    }
                                });
                            }
                            return isObject(d, true) ? merge(d) : d;
                        });
                        // Avoid destroying points when series is not visible
                        if (series.visible) {
                            series.setData(axisData, false);
                        }
                    });
                    // Calculate the label options for each level in the tree.
                    axis.treeGrid.mapOptionsToLevel =
                        getLevelOptions({
                            defaults: labelOptions,
                            from: 1,
                            levels: labelOptions && labelOptions.levels,
                            to: axis.treeGrid.tree && axis.treeGrid.tree.height
                        });
                    // Setting initial collapsed nodes
                    if (e.type === 'beforeRender') {
                        axis.treeGrid.collapsedNodes = treeGrid.collapsedNodes;
                    }
                }
            });
        }
        /**
         * Generates a tick for initial positioning.
         *
         * @private
         * @function Highcharts.GridAxis#generateTick
         *
         * @param {Function} proceed
         * The original generateTick function.
         *
         * @param {number} pos
         * The tick position in axis values.
         */
        function wrapGenerateTick(proceed, pos) {
            var axis = this,
                mapOptionsToLevel = axis.treeGrid.mapOptionsToLevel || {},
                isTreeGrid = axis.options.type === 'treegrid',
                ticks = axis.ticks;
            var tick = ticks[pos],
                levelOptions,
                options,
                gridNode;
            if (isTreeGrid &&
                axis.treeGrid.mapOfPosToGridNode) {
                gridNode = axis.treeGrid.mapOfPosToGridNode[pos];
                levelOptions = mapOptionsToLevel[gridNode.depth];
                if (levelOptions) {
                    options = {
                        labels: levelOptions
                    };
                }
                if (!tick &&
                    TickConstructor) {
                    ticks[pos] = tick =
                        new TickConstructor(axis, pos, void 0, void 0, {
                            category: gridNode.name,
                            tickmarkOffset: gridNode.tickmarkOffset,
                            options: options
                        });
                }
                else {
                    // update labels depending on tick interval
                    tick.parameters.category = gridNode.name;
                    tick.options = options;
                    tick.addLabel();
                }
            }
            else {
                proceed.apply(axis, Array.prototype.slice.call(arguments, 1));
            }
        }
        /**
         * @private
         */
        function wrapInit(proceed, chart, userOptions) {
            var axis = this,
                isTreeGrid = userOptions.type === 'treegrid';
            if (!axis.treeGrid) {
                axis.treeGrid = new TreeGridAxisAdditions(axis);
            }
            // Set default and forced options for TreeGrid
            if (isTreeGrid) {
                // Add event for updating the categories of a treegrid.
                // NOTE Preferably these events should be set on the axis.
                addEvent(chart, 'beforeRender', onBeforeRender);
                addEvent(chart, 'beforeRedraw', onBeforeRender);
                // Add new collapsed nodes on addseries
                addEvent(chart, 'addSeries', function (e) {
                    if (e.options.data) {
                        var treeGrid = getTreeGridFromData(e.options.data,
                            userOptions.uniqueNames || false, 1);
                        axis.treeGrid.collapsedNodes = (axis.treeGrid.collapsedNodes || []).concat(treeGrid.collapsedNodes);
                    }
                });
                // Collapse all nodes in axis.treegrid.collapsednodes
                // where collapsed equals true.
                addEvent(axis, 'foundExtremes', function () {
                    if (axis.treeGrid.collapsedNodes) {
                        axis.treeGrid.collapsedNodes.forEach(function (node) {
                            var breaks = axis.treeGrid.collapse(node);
                            if (axis.brokenAxis) {
                                axis.brokenAxis.setBreaks(breaks, false);
                                // remove the node from the axis collapsedNodes
                                if (axis.treeGrid.collapsedNodes) {
                                    axis.treeGrid.collapsedNodes = axis.treeGrid
                                        .collapsedNodes
                                        .filter(function (n) { return ((node.collapseStart !==
                                        n.collapseStart) ||
                                        node.collapseEnd !== n.collapseEnd); });
                                }
                            }
                        });
                    }
                });
                // If staticScale is not defined on the yAxis
                // and chart height is set, set axis.isDirty
                // to ensure collapsing works (#12012)
                addEvent(axis, 'afterBreaks', function () {
                    if (axis.coll === 'yAxis' &&
                        !axis.staticScale &&
                        axis.chart.options.chart.height) {
                        axis.isDirty = true;
                    }
                });
                userOptions = merge({
                    // Default options
                    grid: {
                        enabled: true
                    },
                    // TODO: add support for align in treegrid.
                    labels: {
                        align: 'left',
                        /**
                        * Set options on specific levels in a tree grid axis. Takes
                        * precedence over labels options.
                        *
                        * @sample {gantt} gantt/treegrid-axis/labels-levels
                        *         Levels on TreeGrid Labels
                        *
                        * @type      {Array<*>}
                        * @product   gantt
                        * @apioption yAxis.labels.levels
                        *
                        * @private
                        */
                        levels: [{
                                /**
                                * Specify the level which the options within this object
                                * applies to.
                                *
                                * @type      {number}
                                * @product   gantt
                                * @apioption yAxis.labels.levels.level
                                *
                                * @private
                                */
                                level: void 0
                            }, {
                                level: 1,
                                /**
                                 * @type      {Highcharts.CSSObject}
                                 * @product   gantt
                                 * @apioption yAxis.labels.levels.style
                                 *
                                 * @private
                                 */
                                style: {
                                    /** @ignore-option */
                                    fontWeight: 'bold'
                                }
                            }],
                        /**
                         * The symbol for the collapse and expand icon in a
                         * treegrid.
                         *
                         * @product      gantt
                         * @optionparent yAxis.labels.symbol
                         *
                         * @private
                         */
                        symbol: {
                            /**
                             * The symbol type. Points to a definition function in
                             * the `Highcharts.Renderer.symbols` collection.
                             *
                             * @type {Highcharts.SymbolKeyValue}
                             *
                             * @private
                             */
                            type: 'triangle',
                            x: -5,
                            y: -5,
                            height: 10,
                            width: 10,
                            padding: 5
                        }
                    },
                    uniqueNames: false
                }, userOptions, {
                    // Forced options
                    reversed: true,
                    // grid.columns is not supported in treegrid
                    grid: {
                        columns: void 0
                    }
                });
            }
            // Now apply the original function with the original arguments,
            // which are sliced off this function's arguments
            proceed.apply(axis, [chart, userOptions]);
            if (isTreeGrid) {
                axis.hasNames = true;
                axis.options.showLastLabel = true;
            }
        }
        /**
         * Set the tick positions, tickInterval, axis min and max.
         *
         * @private
         * @function Highcharts.GridAxis#setTickInterval
         *
         * @param {Function} proceed
         * The original setTickInterval function.
         */
        function wrapSetTickInterval(proceed) {
            var axis = this,
                options = axis.options,
                isTreeGrid = options.type === 'treegrid';
            if (isTreeGrid) {
                axis.min = pick(axis.userMin, options.min, axis.dataMin);
                axis.max = pick(axis.userMax, options.max, axis.dataMax);
                fireEvent(axis, 'foundExtremes');
                // setAxisTranslation modifies the min and max according to
                // axis breaks.
                axis.setAxisTranslation();
                axis.tickmarkOffset = 0.5;
                axis.tickInterval = 1;
                axis.tickPositions = axis.treeGrid.mapOfPosToGridNode ?
                    axis.treeGrid.getTickPositions() :
                    [];
            }
            else {
                proceed.apply(axis, Array.prototype.slice.call(arguments, 1));
            }
        }
        /* *
         *
         *  Classes
         *
         * */
        /**
         * @private
         * @class
         */
        var TreeGridAxisAdditions = /** @class */ (function () {
                /* *
                 *
                 *  Constructors
                 *
                 * */
                /**
                 * @private
                 */
                function TreeGridAxisAdditions(axis) {
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
            TreeGridAxisAdditions.compose = function (AxisClass, ChartClass, SeriesClass, TickClass) {
                if (composedClasses.indexOf(AxisClass) === -1) {
                    composedClasses.push(AxisClass);
                    if (AxisClass.keepProps.indexOf('treeGrid') === -1) {
                        AxisClass.keepProps.push('treeGrid');
                    }
                    var axisProps = AxisClass.prototype;
                    wrap(axisProps, 'generateTick', wrapGenerateTick);
                    wrap(axisProps, 'init', wrapInit);
                    wrap(axisProps, 'setTickInterval', wrapSetTickInterval);
                    // Make utility functions available for testing.
                    axisProps.utils = {
                        getNode: Tree.getNode
                    };
                }
                if (composedClasses.indexOf(TickClass) === -1) {
                    composedClasses.push(TickClass);
                    if (!TickConstructor) {
                        TickConstructor = TickClass;
                    }
                }
                GridAxis.compose(AxisClass, ChartClass, TickClass);
                BrokenAxis.compose(AxisClass, SeriesClass);
                TreeGridTick.compose(TickClass);
                return AxisClass;
            };
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Set the collapse status.
             *
             * @private
             *
             * @param {Highcharts.Axis} axis
             * The axis to check against.
             *
             * @param {Highcharts.GridNode} node
             * The node to collapse.
             */
            TreeGridAxisAdditions.prototype.setCollapsedStatus = function (node) {
                var axis = this.axis,
                    chart = axis.chart;
                axis.series.forEach(function (series) {
                    var data = series.options.data;
                    if (node.id && data) {
                        var point = chart.get(node.id),
                            dataPoint = data[series.data.indexOf(point)];
                        if (point && dataPoint) {
                            point.collapsed = node.collapsed;
                            dataPoint.collapsed = node.collapsed;
                        }
                    }
                });
            };
            /**
             * Calculates the new axis breaks to collapse a node.
             *
             * @private
             *
             * @param {Highcharts.Axis} axis
             * The axis to check against.
             *
             * @param {Highcharts.GridNode} node
             * The node to collapse.
             *
             * @param {number} pos
             * The tick position to collapse.
             *
             * @return {Array<object>}
             * Returns an array of the new breaks for the axis.
             */
            TreeGridAxisAdditions.prototype.collapse = function (node) {
                var axis = this.axis,
                    breaks = (axis.options.breaks || []),
                    obj = getBreakFromNode(node,
                    axis.max);
                breaks.push(obj);
                // Change the collapsed flag #13838
                node.collapsed = true;
                axis.treeGrid.setCollapsedStatus(node);
                return breaks;
            };
            /**
             * Calculates the new axis breaks to expand a node.
             *
             * @private
             *
             * @param {Highcharts.Axis} axis
             * The axis to check against.
             *
             * @param {Highcharts.GridNode} node
             * The node to expand.
             *
             * @param {number} pos
             * The tick position to expand.
             *
             * @return {Array<object>}
             * Returns an array of the new breaks for the axis.
             */
            TreeGridAxisAdditions.prototype.expand = function (node) {
                var axis = this.axis,
                    breaks = (axis.options.breaks || []),
                    obj = getBreakFromNode(node,
                    axis.max);
                // Change the collapsed flag #13838
                node.collapsed = false;
                axis.treeGrid.setCollapsedStatus(node);
                // Remove the break from the axis breaks array.
                return breaks.reduce(function (arr, b) {
                    if (b.to !== obj.to || b.from !== obj.from) {
                        arr.push(b);
                    }
                    return arr;
                }, []);
            };
            /**
             * Creates a list of positions for the ticks on the axis. Filters out
             * positions that are outside min and max, or is inside an axis break.
             *
             * @private
             *
             * @return {Array<number>}
             * List of positions.
             */
            TreeGridAxisAdditions.prototype.getTickPositions = function () {
                var axis = this.axis,
                    roundedMin = Math.floor(axis.min / axis.tickInterval) * axis.tickInterval,
                    roundedMax = Math.ceil(axis.max / axis.tickInterval) * axis.tickInterval;
                return Object.keys(axis.treeGrid.mapOfPosToGridNode || {}).reduce(function (arr, key) {
                    var pos = +key;
                    if (pos >= roundedMin &&
                        pos <= roundedMax &&
                        !(axis.brokenAxis && axis.brokenAxis.isInAnyBreak(pos))) {
                        arr.push(pos);
                    }
                    return arr;
                }, []);
            };
            /**
             * Check if a node is collapsed.
             *
             * @private
             *
             * @param {Highcharts.Axis} axis
             * The axis to check against.
             *
             * @param {Object} node
             * The node to check if is collapsed.
             *
             * @param {number} pos
             * The tick position to collapse.
             *
             * @return {boolean}
             * Returns true if collapsed, false if expanded.
             */
            TreeGridAxisAdditions.prototype.isCollapsed = function (node) {
                var axis = this.axis,
                    breaks = (axis.options.breaks || []),
                    obj = getBreakFromNode(node,
                    axis.max);
                return breaks.some(function (b) {
                    return b.from === obj.from && b.to === obj.to;
                });
            };
            /**
             * Calculates the new axis breaks after toggling the collapse/expand
             * state of a node. If it is collapsed it will be expanded, and if it is
             * exapended it will be collapsed.
             *
             * @private
             *
             * @param {Highcharts.Axis} axis
             * The axis to check against.
             *
             * @param {Highcharts.GridNode} node
             * The node to toggle.
             *
             * @return {Array<object>}
             * Returns an array of the new breaks for the axis.
             */
            TreeGridAxisAdditions.prototype.toggleCollapse = function (node) {
                return (this.isCollapsed(node) ?
                    this.expand(node) :
                    this.collapse(node));
            };
            return TreeGridAxisAdditions;
        }());
        /* *
         *
         *  Default Export
         *
         * */

        return TreeGridAxisAdditions;
    });
    _registerModule(_modules, 'Extensions/CurrentDateIndication.js', [_modules['Core/Axis/Axis.js'], _modules['Core/Axis/PlotLineOrBand/PlotLineOrBand.js'], _modules['Core/Utilities.js']], function (Axis, PlotLineOrBand, U) {
        /* *
         *
         *  (c) 2016-2021 Highsoft AS
         *
         *  Author: Lars A. V. Cabrera
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var addEvent = U.addEvent,
            merge = U.merge,
            wrap = U.wrap;
        /**
         * Show an indicator on the axis for the current date and time. Can be a
         * boolean or a configuration object similar to
         * [xAxis.plotLines](#xAxis.plotLines).
         *
         * @sample gantt/current-date-indicator/demo
         *         Current date indicator enabled
         * @sample gantt/current-date-indicator/object-config
         *         Current date indicator with custom options
         *
         * @declare   Highcharts.CurrentDateIndicatorOptions
         * @type      {boolean|CurrentDateIndicatorOptions}
         * @default   true
         * @extends   xAxis.plotLines
         * @excluding value
         * @product   gantt
         * @apioption xAxis.currentDateIndicator
         */
        var defaultOptions = {
                color: "#ccd6eb" /* Palette.highlightColor20 */,
                width: 2,
                /**
                 * @declare Highcharts.AxisCurrentDateIndicatorLabelOptions
                 */
                label: {
                    /**
                     * Format of the label. This options is passed as the fist argument to
                     * [dateFormat](/class-reference/Highcharts.Time#dateFormat) function.
                     *
                     * @type      {string}
                     * @default   %a, %b %d %Y, %H:%M
                     * @product   gantt
                     * @apioption xAxis.currentDateIndicator.label.format
                     */
                    format: '%a, %b %d %Y, %H:%M',
                    formatter: function (value, format) {
                        return this.axis.chart.time.dateFormat(format || '', value);
                },
                rotation: 0,
                /**
                 * @type {Highcharts.CSSObject}
                 */
                style: {
                    /** @internal */
                    fontSize: '10px'
                }
            }
        };
        /* eslint-disable no-invalid-this */
        addEvent(Axis, 'afterSetOptions', function () {
            var options = this.options,
                cdiOptions = options.currentDateIndicator;
            if (cdiOptions) {
                var plotLineOptions = typeof cdiOptions === 'object' ?
                        merge(defaultOptions,
                    cdiOptions) :
                        merge(defaultOptions);
                plotLineOptions.value = Date.now();
                plotLineOptions.className = 'highcharts-current-date-indicator';
                if (!options.plotLines) {
                    options.plotLines = [];
                }
                options.plotLines.push(plotLineOptions);
            }
        });
        addEvent(PlotLineOrBand, 'render', function () {
            // If the label already exists, update its text
            if (this.label) {
                this.label.attr({
                    text: this.getLabelText(this.options.label)
                });
            }
        });
        wrap(PlotLineOrBand.prototype, 'getLabelText', function (defaultMethod, defaultLabelOptions) {
            var options = this.options;
            if (options &&
                options.className &&
                options.className.indexOf('highcharts-current-date-indicator') !== -1 &&
                options.label &&
                typeof options.label.formatter === 'function') {
                options.value = Date.now();
                return options.label.formatter
                    .call(this, options.value, options.label.format);
            }
            return defaultMethod.call(this, defaultLabelOptions);
        });

    });
    _registerModule(_modules, 'Extensions/StaticScale.js', [_modules['Core/Axis/Axis.js'], _modules['Core/Chart/Chart.js'], _modules['Core/Utilities.js']], function (Axis, Chart, U) {
        /* *
         *
         *  (c) 2016-2021 Torstein Honsi, Lars Cabrera
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var addEvent = U.addEvent,
            defined = U.defined,
            isNumber = U.isNumber,
            pick = U.pick;
        /* eslint-disable no-invalid-this */
        /**
         * For vertical axes only. Setting the static scale ensures that each tick unit
         * is translated into a fixed pixel height. For example, setting the static
         * scale to 24 results in each Y axis category taking up 24 pixels, and the
         * height of the chart adjusts. Adding or removing items will make the chart
         * resize.
         *
         * @sample gantt/xrange-series/demo/
         *         X-range series with static scale
         *
         * @type      {number}
         * @default   50
         * @since     6.2.0
         * @product   gantt
         * @apioption yAxis.staticScale
         */
        addEvent(Axis, 'afterSetOptions', function () {
            var chartOptions = this.chart.options.chart;
            if (!this.horiz &&
                isNumber(this.options.staticScale) &&
                (!chartOptions.height ||
                    (chartOptions.scrollablePlotArea &&
                        chartOptions.scrollablePlotArea.minHeight))) {
                this.staticScale = this.options.staticScale;
            }
        });
        Chart.prototype.adjustHeight = function () {
            if (this.redrawTrigger !== 'adjustHeight') {
                (this.axes || []).forEach(function (axis) {
                    var chart = axis.chart,
                        animate = !!chart.initiatedScale &&
                            chart.options.animation,
                        staticScale = axis.options.staticScale,
                        height,
                        diff;
                    if (axis.staticScale && defined(axis.min)) {
                        height = pick(axis.brokenAxis && axis.brokenAxis.unitLength, axis.max + axis.tickInterval - axis.min) * staticScale;
                        // Minimum height is 1 x staticScale.
                        height = Math.max(height, staticScale);
                        diff = height - chart.plotHeight;
                        if (!chart.scrollablePixelsY && Math.abs(diff) >= 1) {
                            chart.plotHeight = height;
                            chart.redrawTrigger = 'adjustHeight';
                            chart.setSize(void 0, chart.chartHeight + diff, animate);
                        }
                        // Make sure clip rects have the right height before initial
                        // animation.
                        axis.series.forEach(function (series) {
                            var clipRect = series.sharedClipKey &&
                                    chart.sharedClips[series.sharedClipKey];
                            if (clipRect) {
                                clipRect.attr(chart.inverted ? {
                                    width: chart.plotHeight
                                } : {
                                    height: chart.plotHeight
                                });
                            }
                        });
                    }
                });
                this.initiatedScale = true;
            }
            this.redrawTrigger = null;
        };
        addEvent(Chart, 'render', Chart.prototype.adjustHeight);

    });
    _registerModule(_modules, 'Extensions/ArrowSymbols.js', [_modules['Core/Renderer/SVG/SVGRenderer.js']], function (SVGRenderer) {
        /* *
         *
         *  (c) 2017 Highsoft AS
         *  Authors: Lars A. V. Cabrera
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var symbols = SVGRenderer.prototype.symbols;
        /* *
         *
         *  Functions
         *
         * */
        /**
         * Creates an arrow symbol. Like a triangle, except not filled.
         * ```
         *                   o
         *             o
         *       o
         * o
         *       o
         *             o
         *                   o
         * ```
         *
         * @private
         * @function
         *
         * @param {number} x
         *        x position of the arrow
         *
         * @param {number} y
         *        y position of the arrow
         *
         * @param {number} w
         *        width of the arrow
         *
         * @param {number} h
         *        height of the arrow
         *
         * @return {Highcharts.SVGPathArray}
         *         Path array
         */
        function arrow(x, y, w, h) {
            return [
                ['M', x, y + h / 2],
                ['L', x + w, y],
                ['L', x, y + h / 2],
                ['L', x + w, y + h]
            ];
        }
        /**
         * Creates a half-width arrow symbol. Like a triangle, except not filled.
         * ```
         *       o
         *    o
         * o
         *    o
         *       o
         * ```
         *
         * @private
         * @function
         *
         * @param {number} x
         *        x position of the arrow
         *
         * @param {number} y
         *        y position of the arrow
         *
         * @param {number} w
         *        width of the arrow
         *
         * @param {number} h
         *        height of the arrow
         *
         * @return {Highcharts.SVGPathArray}
         *         Path array
         */
        function arrowHalf(x, y, w, h) {
            return arrow(x, y, w / 2, h);
        }
        /**
         * Creates a left-oriented triangle.
         * ```
         *             o
         *       ooooooo
         * ooooooooooooo
         *       ooooooo
         *             o
         * ```
         *
         * @private
         * @function
         *
         * @param {number} x
         *        x position of the triangle
         *
         * @param {number} y
         *        y position of the triangle
         *
         * @param {number} w
         *        width of the triangle
         *
         * @param {number} h
         *        height of the triangle
         *
         * @return {Highcharts.SVGPathArray}
         *         Path array
         */
        function triangleLeft(x, y, w, h) {
            return [
                ['M', x + w, y],
                ['L', x, y + h / 2],
                ['L', x + w, y + h],
                ['Z']
            ];
        }
        /**
         * Creates a half-width, left-oriented triangle.
         * ```
         *       o
         *    oooo
         * ooooooo
         *    oooo
         *       o
         * ```
         *
         * @private
         * @function
         *
         * @param {number} x
         *        x position of the triangle
         *
         * @param {number} y
         *        y position of the triangle
         *
         * @param {number} w
         *        width of the triangle
         *
         * @param {number} h
         *        height of the triangle
         *
         * @return {Highcharts.SVGPathArray}
         *         Path array
         */
        function triangleLeftHalf(x, y, w, h) {
            return triangleLeft(x, y, w / 2, h);
        }
        symbols.arrow = arrow;
        symbols['arrow-filled'] = triangleLeft;
        symbols['arrow-filled-half'] = triangleLeftHalf;
        symbols['arrow-half'] = arrowHalf;
        symbols['triangle-left'] = triangleLeft;
        symbols['triangle-left-half'] = triangleLeftHalf;
        /* *
         *
         *  Default Export
         *
         * */

        return symbols;
    });
    _registerModule(_modules, 'Gantt/Connection.js', [_modules['Core/Defaults.js'], _modules['Core/Globals.js'], _modules['Core/Series/Point.js'], _modules['Core/Utilities.js']], function (D, H, Point, U) {
        /* *
         *
         *  (c) 2016 Highsoft AS
         *  Authors: Øystein Moseng, Lars A. V. Cabrera
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var defaultOptions = D.defaultOptions;
        var defined = U.defined,
            error = U.error,
            extend = U.extend,
            merge = U.merge,
            objectEach = U.objectEach,
            pick = U.pick;
        /**
         * The default pathfinder algorithm to use for a chart. It is possible to define
         * your own algorithms by adding them to the
         * `Highcharts.Pathfinder.prototype.algorithms`
         * object before the chart has been created.
         *
         * The default algorithms are as follows:
         *
         * `straight`:      Draws a straight line between the connecting
         *                  points. Does not avoid other points when drawing.
         *
         * `simpleConnect`: Finds a path between the points using right angles
         *                  only. Takes only starting/ending points into
         *                  account, and will not avoid other points.
         *
         * `fastAvoid`:     Finds a path between the points using right angles
         *                  only. Will attempt to avoid other points, but its
         *                  focus is performance over accuracy. Works well with
         *                  less dense datasets.
         *
         * @typedef {"fastAvoid"|"simpleConnect"|"straight"|string} Highcharts.PathfinderTypeValue
         */
        ''; // detach doclets above
        var deg2rad = H.deg2rad,
            max = Math.max,
            min = Math.min;
        /*
         @todo:
             - Document how to write your own algorithms
             - Consider adding a Point.pathTo method that wraps creating a connection
               and rendering it
        */
        // Set default Pathfinder options
        extend(defaultOptions, {
            /**
             * The Pathfinder module allows you to define connections between any two
             * points, represented as lines - optionally with markers for the start
             * and/or end points. Multiple algorithms are available for calculating how
             * the connecting lines are drawn.
             *
             * Connector functionality requires Highcharts Gantt to be loaded. In Gantt
             * charts, the connectors are used to draw dependencies between tasks.
             *
             * @see [dependency](series.gantt.data.dependency)
             *
             * @sample gantt/pathfinder/demo
             *         Pathfinder connections
             *
             * @declare      Highcharts.ConnectorsOptions
             * @product      gantt
             * @optionparent connectors
             */
            connectors: {
                /**
                 * Enable connectors for this chart. Requires Highcharts Gantt.
                 *
                 * @type      {boolean}
                 * @default   true
                 * @since     6.2.0
                 * @apioption connectors.enabled
                 */
                /**
                 * Set the default dash style for this chart's connecting lines.
                 *
                 * @type      {string}
                 * @default   solid
                 * @since     6.2.0
                 * @apioption connectors.dashStyle
                 */
                /**
                 * Set the default color for this chart's Pathfinder connecting lines.
                 * Defaults to the color of the point being connected.
                 *
                 * @type      {Highcharts.ColorString}
                 * @since     6.2.0
                 * @apioption connectors.lineColor
                 */
                /**
                 * Set the default pathfinder margin to use, in pixels. Some Pathfinder
                 * algorithms attempt to avoid obstacles, such as other points in the
                 * chart. These algorithms use this margin to determine how close lines
                 * can be to an obstacle. The default is to compute this automatically
                 * from the size of the obstacles in the chart.
                 *
                 * To draw connecting lines close to existing points, set this to a low
                 * number. For more space around existing points, set this number
                 * higher.
                 *
                 * @sample gantt/pathfinder/algorithm-margin
                 *         Small algorithmMargin
                 *
                 * @type      {number}
                 * @since     6.2.0
                 * @apioption connectors.algorithmMargin
                 */
                /**
                 * Set the default pathfinder algorithm to use for this chart. It is
                 * possible to define your own algorithms by adding them to the
                 * Highcharts.Pathfinder.prototype.algorithms object before the chart
                 * has been created.
                 *
                 * The default algorithms are as follows:
                 *
                 * `straight`:      Draws a straight line between the connecting
                 *                  points. Does not avoid other points when drawing.
                 *
                 * `simpleConnect`: Finds a path between the points using right angles
                 *                  only. Takes only starting/ending points into
                 *                  account, and will not avoid other points.
                 *
                 * `fastAvoid`:     Finds a path between the points using right angles
                 *                  only. Will attempt to avoid other points, but its
                 *                  focus is performance over accuracy. Works well with
                 *                  less dense datasets.
                 *
                 * Default value: `straight` is used as default for most series types,
                 * while `simpleConnect` is used as default for Gantt series, to show
                 * dependencies between points.
                 *
                 * @sample gantt/pathfinder/demo
                 *         Different types used
                 *
                 * @type    {Highcharts.PathfinderTypeValue}
                 * @default undefined
                 * @since   6.2.0
                 */
                type: 'straight',
                /**
                 * Set the default pixel width for this chart's Pathfinder connecting
                 * lines.
                 *
                 * @since 6.2.0
                 */
                lineWidth: 1,
                /**
                 * Marker options for this chart's Pathfinder connectors. Note that
                 * this option is overridden by the `startMarker` and `endMarker`
                 * options.
                 *
                 * @declare Highcharts.ConnectorsMarkerOptions
                 * @since   6.2.0
                 */
                marker: {
                    /**
                     * Set the radius of the connector markers. The default is
                     * automatically computed based on the algorithmMargin setting.
                     *
                     * Setting marker.width and marker.height will override this
                     * setting.
                     *
                     * @type      {number}
                     * @since     6.2.0
                     * @apioption connectors.marker.radius
                     */
                    /**
                     * Set the width of the connector markers. If not supplied, this
                     * is inferred from the marker radius.
                     *
                     * @type      {number}
                     * @since     6.2.0
                     * @apioption connectors.marker.width
                     */
                    /**
                     * Set the height of the connector markers. If not supplied, this
                     * is inferred from the marker radius.
                     *
                     * @type      {number}
                     * @since     6.2.0
                     * @apioption connectors.marker.height
                     */
                    /**
                     * Set the color of the connector markers. By default this is the
                     * same as the connector color.
                     *
                     * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                     * @since     6.2.0
                     * @apioption connectors.marker.color
                     */
                    /**
                     * Set the line/border color of the connector markers. By default
                     * this is the same as the marker color.
                     *
                     * @type      {Highcharts.ColorString}
                     * @since     6.2.0
                     * @apioption connectors.marker.lineColor
                     */
                    /**
                     * Enable markers for the connectors.
                     */
                    enabled: false,
                    /**
                     * Horizontal alignment of the markers relative to the points.
                     *
                     * @type {Highcharts.AlignValue}
                     */
                    align: 'center',
                    /**
                     * Vertical alignment of the markers relative to the points.
                     *
                     * @type {Highcharts.VerticalAlignValue}
                     */
                    verticalAlign: 'middle',
                    /**
                     * Whether or not to draw the markers inside the points.
                     */
                    inside: false,
                    /**
                     * Set the line/border width of the pathfinder markers.
                     */
                    lineWidth: 1
                },
                /**
                 * Marker options specific to the start markers for this chart's
                 * Pathfinder connectors. Overrides the generic marker options.
                 *
                 * @declare Highcharts.ConnectorsStartMarkerOptions
                 * @extends connectors.marker
                 * @since   6.2.0
                 */
                startMarker: {
                    /**
                     * Set the symbol of the connector start markers.
                     */
                    symbol: 'diamond'
                },
                /**
                 * Marker options specific to the end markers for this chart's
                 * Pathfinder connectors. Overrides the generic marker options.
                 *
                 * @declare Highcharts.ConnectorsEndMarkerOptions
                 * @extends connectors.marker
                 * @since   6.2.0
                 */
                endMarker: {
                    /**
                     * Set the symbol of the connector end markers.
                     */
                    symbol: 'arrow-filled'
                }
            }
        });
        /**
         * Override Pathfinder connector options for a series. Requires Highcharts Gantt
         * to be loaded.
         *
         * @declare   Highcharts.SeriesConnectorsOptionsObject
         * @extends   connectors
         * @since     6.2.0
         * @excluding enabled, algorithmMargin
         * @product   gantt
         * @apioption plotOptions.series.connectors
         */
        /**
         * Connect to a point. This option can be either a string, referring to the ID
         * of another point, or an object, or an array of either. If the option is an
         * array, each element defines a connection.
         *
         * @sample gantt/pathfinder/demo
         *         Different connection types
         *
         * @declare   Highcharts.XrangePointConnectorsOptionsObject
         * @type      {string|Array<string|*>|*}
         * @extends   plotOptions.series.connectors
         * @since     6.2.0
         * @excluding enabled
         * @product   gantt
         * @requires  highcharts-gantt
         * @apioption series.xrange.data.connect
         */
        /**
         * The ID of the point to connect to.
         *
         * @type      {string}
         * @since     6.2.0
         * @product   gantt
         * @apioption series.xrange.data.connect.to
         */
        /**
         * Get point bounding box using plotX/plotY and shapeArgs. If using
         * graphic.getBBox() directly, the bbox will be affected by animation.
         *
         * @private
         * @function
         *
         * @param {Highcharts.Point} point
         *        The point to get BB of.
         *
         * @return {Highcharts.Dictionary<number>|null}
         *         Result xMax, xMin, yMax, yMin.
         */
        function getPointBB(point) {
            var shapeArgs = point.shapeArgs,
                bb;
            // Prefer using shapeArgs (columns)
            if (shapeArgs) {
                return {
                    xMin: shapeArgs.x || 0,
                    xMax: (shapeArgs.x || 0) + (shapeArgs.width || 0),
                    yMin: shapeArgs.y || 0,
                    yMax: (shapeArgs.y || 0) + (shapeArgs.height || 0)
                };
            }
            // Otherwise use plotX/plotY and bb
            bb = point.graphic && point.graphic.getBBox();
            return bb ? {
                xMin: point.plotX - bb.width / 2,
                xMax: point.plotX + bb.width / 2,
                yMin: point.plotY - bb.height / 2,
                yMax: point.plotY + bb.height / 2
            } : null;
        }
        /**
         * Calculate margin to place around obstacles for the pathfinder in pixels.
         * Returns a minimum of 1 pixel margin.
         *
         * @private
         * @function
         *
         * @param {Array<object>} obstacles
         *        Obstacles to calculate margin from.
         *
         * @return {number}
         *         The calculated margin in pixels. At least 1.
         */
        function calculateObstacleMargin(obstacles) {
            var len = obstacles.length,
                i = 0,
                j,
                obstacleDistance,
                distances = [], 
                // Compute smallest distance between two rectangles
                distance = function (a,
                b,
                bbMargin) {
                    // Count the distance even if we are slightly off
                    var margin = pick(bbMargin, 10),
                yOverlap = a.yMax + margin > b.yMin - margin &&
                        a.yMin - margin < b.yMax + margin,
                xOverlap = a.xMax + margin > b.xMin - margin &&
                        a.xMin - margin < b.xMax + margin,
                xDistance = yOverlap ? (a.xMin > b.xMax ? a.xMin - b.xMax : b.xMin - a.xMax) : Infinity,
                yDistance = xOverlap ? (a.yMin > b.yMax ? a.yMin - b.yMax : b.yMin - a.yMax) : Infinity;
                // If the rectangles collide, try recomputing with smaller margin.
                // If they collide anyway, discard the obstacle.
                if (xOverlap && yOverlap) {
                    return (margin ?
                        distance(a, b, Math.floor(margin / 2)) :
                        Infinity);
                }
                return min(xDistance, yDistance);
            };
            // Go over all obstacles and compare them to the others.
            for (; i < len; ++i) {
                // Compare to all obstacles ahead. We will already have compared this
                // obstacle to the ones before.
                for (j = i + 1; j < len; ++j) {
                    obstacleDistance = distance(obstacles[i], obstacles[j]);
                    // TODO: Magic number 80
                    if (obstacleDistance < 80) { // Ignore large distances
                        distances.push(obstacleDistance);
                    }
                }
            }
            // Ensure we always have at least one value, even in very spaceous charts
            distances.push(80);
            return max(Math.floor(distances.sort(function (a, b) {
                return (a - b);
            })[
            // Discard first 10% of the relevant distances, and then grab
            // the smallest one.
            Math.floor(distances.length / 10)] / 2 - 1 // Divide the distance by 2 and subtract 1.
            ), 1 // 1 is the minimum margin
            );
        }
        /* eslint-disable no-invalid-this, valid-jsdoc */
        /**
         * The Connection class. Used internally to represent a connection between two
         * points.
         *
         * @private
         * @class
         * @name Highcharts.Connection
         *
         * @param {Highcharts.Point} from
         *        Connection runs from this Point.
         *
         * @param {Highcharts.Point} to
         *        Connection runs to this Point.
         *
         * @param {Highcharts.ConnectorsOptions} [options]
         *        Connection options.
         */
        var Connection = /** @class */ (function () {
                function Connection(from, to, options) {
                    /* *
                    *
                    * Properties
                    *
                    * */
                    this.chart = void 0;
                this.fromPoint = void 0;
                this.graphics = void 0;
                this.pathfinder = void 0;
                this.toPoint = void 0;
                this.init(from, to, options);
            }
            /**
             * Initialize the Connection object. Used as constructor only.
             *
             * @function Highcharts.Connection#init
             *
             * @param {Highcharts.Point} from
             *        Connection runs from this Point.
             *
             * @param {Highcharts.Point} to
             *        Connection runs to this Point.
             *
             * @param {Highcharts.ConnectorsOptions} [options]
             *        Connection options.
             */
            Connection.prototype.init = function (from, to, options) {
                this.fromPoint = from;
                this.toPoint = to;
                this.options = options;
                this.chart = from.series.chart;
                this.pathfinder = this.chart.pathfinder;
            };
            /**
             * Add (or update) this connection's path on chart. Stores reference to the
             * created element on this.graphics.path.
             *
             * @function Highcharts.Connection#renderPath
             *
             * @param {Highcharts.SVGPathArray} path
             *        Path to render, in array format. E.g. ['M', 0, 0, 'L', 10, 10]
             *
             * @param {Highcharts.SVGAttributes} [attribs]
             *        SVG attributes for the path.
             *
             * @param {Partial<Highcharts.AnimationOptionsObject>} [animation]
             *        Animation options for the rendering.
             */
            Connection.prototype.renderPath = function (path, attribs, animation) {
                var connection = this,
                    chart = this.chart,
                    styledMode = chart.styledMode,
                    pathfinder = chart.pathfinder,
                    animate = !chart.options.chart.forExport && animation !== false,
                    pathGraphic = connection.graphics && connection.graphics.path,
                    anim;
                // Add the SVG element of the pathfinder group if it doesn't exist
                if (!pathfinder.group) {
                    pathfinder.group = chart.renderer.g()
                        .addClass('highcharts-pathfinder-group')
                        .attr({ zIndex: -1 })
                        .add(chart.seriesGroup);
                }
                // Shift the group to compensate for plot area.
                // Note: Do this always (even when redrawing a path) to avoid issues
                // when updating chart in a way that changes plot metrics.
                pathfinder.group.translate(chart.plotLeft, chart.plotTop);
                // Create path if does not exist
                if (!(pathGraphic && pathGraphic.renderer)) {
                    pathGraphic = chart.renderer.path()
                        .add(pathfinder.group);
                    if (!styledMode) {
                        pathGraphic.attr({
                            opacity: 0
                        });
                    }
                }
                // Set path attribs and animate to the new path
                pathGraphic.attr(attribs);
                anim = { d: path };
                if (!styledMode) {
                    anim.opacity = 1;
                }
                pathGraphic[animate ? 'animate' : 'attr'](anim, animation);
                // Store reference on connection
                this.graphics = this.graphics || {};
                this.graphics.path = pathGraphic;
            };
            /**
             * Calculate and add marker graphics for connection to the chart. The
             * created/updated elements are stored on this.graphics.start and
             * this.graphics.end.
             *
             * @function Highcharts.Connection#addMarker
             *
             * @param {string} type
             *        Marker type, either 'start' or 'end'.
             *
             * @param {Highcharts.ConnectorsMarkerOptions} options
             *        All options for this marker. Not calculated or merged with other
             *        options.
             *
             * @param {Highcharts.SVGPathArray} path
             *        Connection path in array format. This is used to calculate the
             *        rotation angle of the markers.
             */
            Connection.prototype.addMarker = function (type, options, path) {
                var connection = this,
                    chart = connection.fromPoint.series.chart,
                    pathfinder = chart.pathfinder,
                    renderer = chart.renderer,
                    point = (type === 'start' ?
                        connection.fromPoint :
                        connection.toPoint),
                    anchor = point.getPathfinderAnchorPoint(options),
                    markerVector,
                    radians,
                    rotation,
                    box,
                    width,
                    height,
                    pathVector,
                    segment;
                if (!options.enabled) {
                    return;
                }
                // Last vector before start/end of path, used to get angle
                if (type === 'start') {
                    segment = path[1];
                }
                else { // 'end'
                    segment = path[path.length - 2];
                }
                if (segment && segment[0] === 'M' || segment[0] === 'L') {
                    pathVector = {
                        x: segment[1],
                        y: segment[2]
                    };
                    // Get angle between pathVector and anchor point and use it to
                    // create marker position.
                    radians = point.getRadiansToVector(pathVector, anchor);
                    markerVector = point.getMarkerVector(radians, options.radius, anchor);
                    // Rotation of marker is calculated from angle between pathVector
                    // and markerVector.
                    // (Note:
                    //  Used to recalculate radians between markerVector and pathVector,
                    //  but this should be the same as between pathVector and anchor.)
                    rotation = -radians / deg2rad;
                    if (options.width && options.height) {
                        width = options.width;
                        height = options.height;
                    }
                    else {
                        width = height = options.radius * 2;
                    }
                    // Add graphics object if it does not exist
                    connection.graphics = connection.graphics || {};
                    box = {
                        x: markerVector.x - (width / 2),
                        y: markerVector.y - (height / 2),
                        width: width,
                        height: height,
                        rotation: rotation,
                        rotationOriginX: markerVector.x,
                        rotationOriginY: markerVector.y
                    };
                    if (!connection.graphics[type]) {
                        // Create new marker element
                        connection.graphics[type] = renderer
                            .symbol(options.symbol)
                            .addClass('highcharts-point-connecting-path-' + type + '-marker')
                            .attr(box)
                            .add(pathfinder.group);
                        if (!renderer.styledMode) {
                            connection.graphics[type].attr({
                                fill: options.color || connection.fromPoint.color,
                                stroke: options.lineColor,
                                'stroke-width': options.lineWidth,
                                opacity: 0
                            })
                                .animate({
                                opacity: 1
                            }, point.series.options.animation);
                        }
                    }
                    else {
                        connection.graphics[type].animate(box);
                    }
                }
            };
            /**
             * Calculate and return connection path.
             * Note: Recalculates chart obstacles on demand if they aren't calculated.
             *
             * @function Highcharts.Connection#getPath
             *
             * @param {Highcharts.ConnectorsOptions} options
             *        Connector options. Not calculated or merged with other options.
             *
             * @return {object|undefined}
             *         Calculated SVG path data in array format.
             */
            Connection.prototype.getPath = function (options) {
                var pathfinder = this.pathfinder,
                    chart = this.chart,
                    algorithm = pathfinder.algorithms[options.type],
                    chartObstacles = pathfinder.chartObstacles;
                if (typeof algorithm !== 'function') {
                    error('"' + options.type + '" is not a Pathfinder algorithm.');
                    return {
                        path: [],
                        obstacles: []
                    };
                }
                // This function calculates obstacles on demand if they don't exist
                if (algorithm.requiresObstacles && !chartObstacles) {
                    chartObstacles =
                        pathfinder.chartObstacles =
                            pathfinder.getChartObstacles(options);
                    // If the algorithmMargin was computed, store the result in default
                    // options.
                    chart.options.connectors.algorithmMargin =
                        options.algorithmMargin;
                    // Cache some metrics too
                    pathfinder.chartObstacleMetrics =
                        pathfinder.getObstacleMetrics(chartObstacles);
                }
                // Get the SVG path
                return algorithm(
                // From
                this.fromPoint.getPathfinderAnchorPoint(options.startMarker), 
                // To
                this.toPoint.getPathfinderAnchorPoint(options.endMarker), merge({
                    chartObstacles: chartObstacles,
                    lineObstacles: pathfinder.lineObstacles || [],
                    obstacleMetrics: pathfinder.chartObstacleMetrics,
                    hardBounds: {
                        xMin: 0,
                        xMax: chart.plotWidth,
                        yMin: 0,
                        yMax: chart.plotHeight
                    },
                    obstacleOptions: {
                        margin: options.algorithmMargin
                    },
                    startDirectionX: pathfinder.getAlgorithmStartDirection(options.startMarker)
                }, options));
            };
            /**
             * (re)Calculate and (re)draw the connection.
             *
             * @function Highcharts.Connection#render
             */
            Connection.prototype.render = function () {
                var connection = this,
                    fromPoint = connection.fromPoint,
                    series = fromPoint.series,
                    chart = series.chart,
                    pathfinder = chart.pathfinder,
                    pathResult,
                    path,
                    options = merge(chart.options.connectors,
                    series.options.connectors,
                    fromPoint.options.connectors,
                    connection.options),
                    attribs = {};
                // Set path attribs
                if (!chart.styledMode) {
                    attribs.stroke = options.lineColor || fromPoint.color;
                    attribs['stroke-width'] = options.lineWidth;
                    if (options.dashStyle) {
                        attribs.dashstyle = options.dashStyle;
                    }
                }
                attribs['class'] = // eslint-disable-line dot-notation
                    'highcharts-point-connecting-path ' +
                        'highcharts-color-' + fromPoint.colorIndex;
                options = merge(attribs, options);
                // Set common marker options
                if (!defined(options.marker.radius)) {
                    options.marker.radius = min(max(Math.ceil((options.algorithmMargin || 8) / 2) - 1, 1), 5);
                }
                // Get the path
                pathResult = connection.getPath(options);
                path = pathResult.path;
                // Always update obstacle storage with obstacles from this path.
                // We don't know if future calls will need this for their algorithm.
                if (pathResult.obstacles) {
                    pathfinder.lineObstacles =
                        pathfinder.lineObstacles || [];
                    pathfinder.lineObstacles =
                        pathfinder.lineObstacles.concat(pathResult.obstacles);
                }
                // Add the calculated path to the pathfinder group
                connection.renderPath(path, attribs, series.options.animation);
                // Render the markers
                connection.addMarker('start', merge(options.marker, options.startMarker), path);
                connection.addMarker('end', merge(options.marker, options.endMarker), path);
            };
            /**
             * Destroy connection by destroying the added graphics elements.
             *
             * @function Highcharts.Connection#destroy
             */
            Connection.prototype.destroy = function () {
                if (this.graphics) {
                    objectEach(this.graphics, function (val) {
                        val.destroy();
                    });
                    delete this.graphics;
                }
            };
            return Connection;
        }());
        // Add to Highcharts namespace
        H.Connection = Connection;
        // Add pathfinding capabilities to Points
        extend(Point.prototype, /** @lends Point.prototype */ {
            /**
             * Get coordinates of anchor point for pathfinder connection.
             *
             * @private
             * @function Highcharts.Point#getPathfinderAnchorPoint
             *
             * @param {Highcharts.ConnectorsMarkerOptions} markerOptions
             *        Connection options for position on point.
             *
             * @return {Highcharts.PositionObject}
             *         An object with x/y properties for the position. Coordinates are
             *         in plot values, not relative to point.
             */
            getPathfinderAnchorPoint: function (markerOptions) {
                var bb = getPointBB(this),
                    x,
                    y;
                switch (markerOptions.align) { // eslint-disable-line default-case
                    case 'right':
                        x = 'xMax';
                        break;
                    case 'left':
                        x = 'xMin';
                }
                switch (markerOptions.verticalAlign) { // eslint-disable-line default-case
                    case 'top':
                        y = 'yMin';
                        break;
                    case 'bottom':
                        y = 'yMax';
                }
                return {
                    x: x ? bb[x] : (bb.xMin + bb.xMax) / 2,
                    y: y ? bb[y] : (bb.yMin + bb.yMax) / 2
                };
            },
            /**
             * Utility to get the angle from one point to another.
             *
             * @private
             * @function Highcharts.Point#getRadiansToVector
             *
             * @param {Highcharts.PositionObject} v1
             *        The first vector, as an object with x/y properties.
             *
             * @param {Highcharts.PositionObject} v2
             *        The second vector, as an object with x/y properties.
             *
             * @return {number}
             *         The angle in degrees
             */
            getRadiansToVector: function (v1, v2) {
                var box;
                if (!defined(v2)) {
                    box = getPointBB(this);
                    if (box) {
                        v2 = {
                            x: (box.xMin + box.xMax) / 2,
                            y: (box.yMin + box.yMax) / 2
                        };
                    }
                }
                return Math.atan2(v2.y - v1.y, v1.x - v2.x);
            },
            /**
             * Utility to get the position of the marker, based on the path angle and
             * the marker's radius.
             *
             * @private
             * @function Highcharts.Point#getMarkerVector
             *
             * @param {number} radians
             *        The angle in radians from the point center to another vector.
             *
             * @param {number} markerRadius
             *        The radius of the marker, to calculate the additional distance to
             *        the center of the marker.
             *
             * @param {Object} anchor
             *        The anchor point of the path and marker as an object with x/y
             *        properties.
             *
             * @return {Object}
             *         The marker vector as an object with x/y properties.
             */
            getMarkerVector: function (radians, markerRadius, anchor) {
                var twoPI = Math.PI * 2.0,
                    theta = radians,
                    bb = getPointBB(this),
                    rectWidth = bb.xMax - bb.xMin,
                    rectHeight = bb.yMax - bb.yMin,
                    rAtan = Math.atan2(rectHeight,
                    rectWidth),
                    tanTheta = 1,
                    leftOrRightRegion = false,
                    rectHalfWidth = rectWidth / 2.0,
                    rectHalfHeight = rectHeight / 2.0,
                    rectHorizontalCenter = bb.xMin + rectHalfWidth,
                    rectVerticalCenter = bb.yMin + rectHalfHeight,
                    edgePoint = {
                        x: rectHorizontalCenter,
                        y: rectVerticalCenter
                    },
                    xFactor = 1,
                    yFactor = 1;
                while (theta < -Math.PI) {
                    theta += twoPI;
                }
                while (theta > Math.PI) {
                    theta -= twoPI;
                }
                tanTheta = Math.tan(theta);
                if ((theta > -rAtan) && (theta <= rAtan)) {
                    // Right side
                    yFactor = -1;
                    leftOrRightRegion = true;
                }
                else if (theta > rAtan && theta <= (Math.PI - rAtan)) {
                    // Top side
                    yFactor = -1;
                }
                else if (theta > (Math.PI - rAtan) || theta <= -(Math.PI - rAtan)) {
                    // Left side
                    xFactor = -1;
                    leftOrRightRegion = true;
                }
                else {
                    // Bottom side
                    xFactor = -1;
                }
                // Correct the edgePoint according to the placement of the marker
                if (leftOrRightRegion) {
                    edgePoint.x += xFactor * (rectHalfWidth);
                    edgePoint.y += yFactor * (rectHalfWidth) * tanTheta;
                }
                else {
                    edgePoint.x += xFactor * (rectHeight / (2.0 * tanTheta));
                    edgePoint.y += yFactor * (rectHalfHeight);
                }
                if (anchor.x !== rectHorizontalCenter) {
                    edgePoint.x = anchor.x;
                }
                if (anchor.y !== rectVerticalCenter) {
                    edgePoint.y = anchor.y;
                }
                return {
                    x: edgePoint.x + (markerRadius * Math.cos(theta)),
                    y: edgePoint.y - (markerRadius * Math.sin(theta))
                };
            }
        });
        /**
         * Warn if using legacy options. Copy the options over. Note that this will
         * still break if using the legacy options in chart.update, addSeries etc.
         * @private
         */
        function warnLegacy(chart) {
            if (chart.options.pathfinder ||
                chart.series.reduce(function (acc, series) {
                    if (series.options) {
                        merge(true, (series.options.connectors = series.options.connectors ||
                            {}), series.options.pathfinder);
                    }
                    return acc || series.options && series.options.pathfinder;
                }, false)) {
                merge(true, (chart.options.connectors = chart.options.connectors || {}), chart.options.pathfinder);
                error('WARNING: Pathfinder options have been renamed. ' +
                    'Use "chart.connectors" or "series.connectors" instead.');
            }
        }

        return Connection;
    });
    _registerModule(_modules, 'Gantt/PathfinderAlgorithms.js', [_modules['Core/Utilities.js']], function (U) {
        /* *
         *
         *  (c) 2016 Highsoft AS
         *  Author: Øystein Moseng
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var extend = U.extend,
            pick = U.pick;
        var min = Math.min,
            max = Math.max,
            abs = Math.abs;
        /**
         * Get index of last obstacle before xMin. Employs a type of binary search, and
         * thus requires that obstacles are sorted by xMin value.
         *
         * @private
         * @function findLastObstacleBefore
         *
         * @param {Array<object>} obstacles
         *        Array of obstacles to search in.
         *
         * @param {number} xMin
         *        The xMin threshold.
         *
         * @param {number} [startIx]
         *        Starting index to search from. Must be within array range.
         *
         * @return {number}
         *         The index of the last obstacle element before xMin.
         */
        function findLastObstacleBefore(obstacles, xMin, startIx) {
            var left = startIx || 0, // left limit
                right = obstacles.length - 1, // right limit
                min = xMin - 0.0000001, // Make sure we include all obstacles at xMin
                cursor,
                cmp;
            while (left <= right) {
                cursor = (right + left) >> 1;
                cmp = min - obstacles[cursor].xMin;
                if (cmp > 0) {
                    left = cursor + 1;
                }
                else if (cmp < 0) {
                    right = cursor - 1;
                }
                else {
                    return cursor;
                }
            }
            return left > 0 ? left - 1 : 0;
        }
        /**
         * Test if a point lays within an obstacle.
         *
         * @private
         * @function pointWithinObstacle
         *
         * @param {Object} obstacle
         *        Obstacle to test.
         *
         * @param {Highcharts.Point} point
         *        Point with x/y props.
         *
         * @return {boolean}
         *         Whether point is within the obstacle or not.
         */
        function pointWithinObstacle(obstacle, point) {
            return (point.x <= obstacle.xMax &&
                point.x >= obstacle.xMin &&
                point.y <= obstacle.yMax &&
                point.y >= obstacle.yMin);
        }
        /**
         * Find the index of an obstacle that wraps around a point.
         * Returns -1 if not found.
         *
         * @private
         * @function findObstacleFromPoint
         *
         * @param {Array<object>} obstacles
         *        Obstacles to test.
         *
         * @param {Highcharts.Point} point
         *        Point with x/y props.
         *
         * @return {number}
         *         Ix of the obstacle in the array, or -1 if not found.
         */
        function findObstacleFromPoint(obstacles, point) {
            var i = findLastObstacleBefore(obstacles,
                point.x + 1) + 1;
            while (i--) {
                if (obstacles[i].xMax >= point.x &&
                    // optimization using lazy evaluation
                    pointWithinObstacle(obstacles[i], point)) {
                    return i;
                }
            }
            return -1;
        }
        /**
         * Get SVG path array from array of line segments.
         *
         * @private
         * @function pathFromSegments
         *
         * @param {Array<object>} segments
         *        The segments to build the path from.
         *
         * @return {Highcharts.SVGPathArray}
         *         SVG path array as accepted by the SVG Renderer.
         */
        function pathFromSegments(segments) {
            var path = [];
            if (segments.length) {
                path.push(['M', segments[0].start.x, segments[0].start.y]);
                for (var i = 0; i < segments.length; ++i) {
                    path.push(['L', segments[i].end.x, segments[i].end.y]);
                }
            }
            return path;
        }
        /**
         * Limits obstacle max/mins in all directions to bounds. Modifies input
         * obstacle.
         *
         * @private
         * @function limitObstacleToBounds
         *
         * @param {Object} obstacle
         *        Obstacle to limit.
         *
         * @param {Object} bounds
         *        Bounds to use as limit.
         *
         * @return {void}
         */
        function limitObstacleToBounds(obstacle, bounds) {
            obstacle.yMin = max(obstacle.yMin, bounds.yMin);
            obstacle.yMax = min(obstacle.yMax, bounds.yMax);
            obstacle.xMin = max(obstacle.xMin, bounds.xMin);
            obstacle.xMax = min(obstacle.xMax, bounds.xMax);
        }
        /**
         * Get an SVG path from a starting coordinate to an ending coordinate.
         * Draws a straight line.
         *
         * @function Highcharts.Pathfinder.algorithms.straight
         *
         * @param {Highcharts.PositionObject} start
         *        Starting coordinate, object with x/y props.
         *
         * @param {Highcharts.PositionObject} end
         *        Ending coordinate, object with x/y props.
         *
         * @return {Object}
         *         An object with the SVG path in Array form as accepted by the SVG
         *         renderer, as well as an array of new obstacles making up this
         *         path.
         */
        function straight(start, end) {
            return {
                path: [
                    ['M', start.x, start.y],
                    ['L', end.x, end.y]
                ],
                obstacles: [{ start: start, end: end }]
            };
        }
        /**
         * Find a path from a starting coordinate to an ending coordinate, using
         * right angles only, and taking only starting/ending obstacle into
         * consideration.
         *
         * @function Highcharts.Pathfinder.algorithms.simpleConnect
         *
         * @param {Highcharts.PositionObject} start
         *        Starting coordinate, object with x/y props.
         *
         * @param {Highcharts.PositionObject} end
         *        Ending coordinate, object with x/y props.
         *
         * @param {Object} options
         *        Options for the algorithm:
         *        - chartObstacles: Array of chart obstacles to avoid
         *        - startDirectionX: Optional. True if starting in the X direction.
         *          If not provided, the algorithm starts in the direction that is
         *          the furthest between start/end.
         *
         * @return {Object}
         *         An object with the SVG path in Array form as accepted by the SVG
         *         renderer, as well as an array of new obstacles making up this
         *         path.
         */
        var simpleConnect = function (start,
            end,
            options) {
                var segments = [],
            endSegment,
            dir = pick(options.startDirectionX,
            abs(end.x - start.x) > abs(end.y - start.y)) ? 'x' : 'y',
            chartObstacles = options.chartObstacles,
            startObstacleIx = findObstacleFromPoint(chartObstacles,
            start),
            endObstacleIx = findObstacleFromPoint(chartObstacles,
            end),
            startObstacle,
            endObstacle,
            prevWaypoint,
            waypoint,
            waypoint2,
            useMax,
            endPoint;
            // eslint-disable-next-line valid-jsdoc
            /**
             * Return a clone of a point with a property set from a target object,
             * optionally with an offset
             * @private
             */
            function copyFromPoint(from, fromKey, to, toKey, offset) {
                var point = {
                        x: from.x,
                        y: from.y
                    };
                point[fromKey] = to[toKey || fromKey] + (offset || 0);
                return point;
            }
            // eslint-disable-next-line valid-jsdoc
            /**
             * Return waypoint outside obstacle.
             * @private
             */
            function getMeOut(obstacle, point, direction) {
                var useMax = abs(point[direction] - obstacle[direction + 'Min']) >
                        abs(point[direction] - obstacle[direction + 'Max']);
                return copyFromPoint(point, direction, obstacle, direction + (useMax ? 'Max' : 'Min'), useMax ? 1 : -1);
            }
            // Pull out end point
            if (endObstacleIx > -1) {
                endObstacle = chartObstacles[endObstacleIx];
                waypoint = getMeOut(endObstacle, end, dir);
                endSegment = {
                    start: waypoint,
                    end: end
                };
                endPoint = waypoint;
            }
            else {
                endPoint = end;
            }
            // If an obstacle envelops the start point, add a segment to get out,
            // and around it.
            if (startObstacleIx > -1) {
                startObstacle = chartObstacles[startObstacleIx];
                waypoint = getMeOut(startObstacle, start, dir);
                segments.push({
                    start: start,
                    end: waypoint
                });
                // If we are going back again, switch direction to get around start
                // obstacle.
                if (
                // Going towards max from start:
                waypoint[dir] >= start[dir] ===
                    // Going towards min to end:
                    waypoint[dir] >= endPoint[dir]) {
                    dir = dir === 'y' ? 'x' : 'y';
                    useMax = start[dir] < end[dir];
                    segments.push({
                        start: waypoint,
                        end: copyFromPoint(waypoint, dir, startObstacle, dir + (useMax ? 'Max' : 'Min'), useMax ? 1 : -1)
                    });
                    // Switch direction again
                    dir = dir === 'y' ? 'x' : 'y';
                }
            }
            // We are around the start obstacle. Go towards the end in one
            // direction.
            prevWaypoint = segments.length ?
                segments[segments.length - 1].end :
                start;
            waypoint = copyFromPoint(prevWaypoint, dir, endPoint);
            segments.push({
                start: prevWaypoint,
                end: waypoint
            });
            // Final run to end point in the other direction
            dir = dir === 'y' ? 'x' : 'y';
            waypoint2 = copyFromPoint(waypoint, dir, endPoint);
            segments.push({
                start: waypoint,
                end: waypoint2
            });
            // Finally add the endSegment
            segments.push(endSegment);
            return {
                path: pathFromSegments(segments),
                obstacles: segments
            };
        };
        simpleConnect.requiresObstacles = true;
        /**
         * Find a path from a starting coordinate to an ending coordinate, taking
         * obstacles into consideration. Might not always find the optimal path,
         * but is fast, and usually good enough.
         *
         * @function Highcharts.Pathfinder.algorithms.fastAvoid
         *
         * @param {Highcharts.PositionObject} start
         *        Starting coordinate, object with x/y props.
         *
         * @param {Highcharts.PositionObject} end
         *        Ending coordinate, object with x/y props.
         *
         * @param {Object} options
         *        Options for the algorithm.
         *        - chartObstacles:  Array of chart obstacles to avoid
         *        - lineObstacles:   Array of line obstacles to jump over
         *        - obstacleMetrics: Object with metrics of chartObstacles cached
         *        - hardBounds:      Hard boundaries to not cross
         *        - obstacleOptions: Options for the obstacles, including margin
         *        - startDirectionX: Optional. True if starting in the X direction.
         *                           If not provided, the algorithm starts in the
         *                           direction that is the furthest between
         *                           start/end.
         *
         * @return {Object}
         *         An object with the SVG path in Array form as accepted by the SVG
         *         renderer, as well as an array of new obstacles making up this
         *         path.
         */
        var fastAvoid = function (start,
            end,
            options) {
                /*
                    Algorithm rules/description
                    - Find initial direction
                    - Determine soft/hard max for each direction.
                    - Move along initial direction until obstacle.
                    - Change direction.
                    - If hitting obstacle,
            first try to change length of previous line
                        before changing direction again.
    
                    Soft min/max x = start/destination x +/- widest obstacle + margin
                    Soft min/max y = start/destination y +/- tallest obstacle + margin
    
                    @todo:
                        - Make retrospective,
            try changing prev segment to reduce
                            corners
                        - Fix logic for breaking out of end-points - not always picking
                            the best direction currently
                        - When going around the end obstacle we should not always go the
                            shortest route,
            rather pick the one closer to the end point
                */
                var dirIsX = pick(options.startDirectionX,
            abs(end.x - start.x) > abs(end.y - start.y)),
            dir = dirIsX ? 'x' : 'y',
            segments,
            useMax,
            extractedEndPoint,
            endSegments = [],
            forceObstacleBreak = false, // Used in clearPathTo to keep track of
                // when to force break through an obstacle.
                // Boundaries to stay within. If beyond soft boundary, prefer to
                // change direction ASAP. If at hard max, always change immediately.
                metrics = options.obstacleMetrics,
            softMinX = min(start.x,
            end.x) - metrics.maxWidth - 10,
            softMaxX = max(start.x,
            end.x) + metrics.maxWidth + 10,
            softMinY = min(start.y,
            end.y) - metrics.maxHeight - 10,
            softMaxY = max(start.y,
            end.y) + metrics.maxHeight + 10, 
                // Obstacles
                chartObstacles = options.chartObstacles,
            startObstacleIx = findLastObstacleBefore(chartObstacles,
            softMinX),
            endObstacleIx = findLastObstacleBefore(chartObstacles,
            softMaxX);
            // eslint-disable-next-line valid-jsdoc
            /**
             * How far can you go between two points before hitting an obstacle?
             * Does not work for diagonal lines (because it doesn't have to).
             * @private
             */
            function pivotPoint(fromPoint, toPoint, directionIsX) {
                var firstPoint,
                    lastPoint,
                    highestPoint,
                    lowestPoint,
                    i,
                    searchDirection = fromPoint.x < toPoint.x ? 1 : -1;
                if (fromPoint.x < toPoint.x) {
                    firstPoint = fromPoint;
                    lastPoint = toPoint;
                }
                else {
                    firstPoint = toPoint;
                    lastPoint = fromPoint;
                }
                if (fromPoint.y < toPoint.y) {
                    lowestPoint = fromPoint;
                    highestPoint = toPoint;
                }
                else {
                    lowestPoint = toPoint;
                    highestPoint = fromPoint;
                }
                // Go through obstacle range in reverse if toPoint is before
                // fromPoint in the X-dimension.
                i = searchDirection < 0 ?
                    // Searching backwards, start at last obstacle before last point
                    min(findLastObstacleBefore(chartObstacles, lastPoint.x), chartObstacles.length - 1) :
                    // Forwards. Since we're not sorted by xMax, we have to look
                    // at all obstacles.
                    0;
                // Go through obstacles in this X range
                while (chartObstacles[i] && (searchDirection > 0 && chartObstacles[i].xMin <= lastPoint.x ||
                    searchDirection < 0 && chartObstacles[i].xMax >= firstPoint.x)) {
                    // If this obstacle is between from and to points in a straight
                    // line, pivot at the intersection.
                    if (chartObstacles[i].xMin <= lastPoint.x &&
                        chartObstacles[i].xMax >= firstPoint.x &&
                        chartObstacles[i].yMin <= highestPoint.y &&
                        chartObstacles[i].yMax >= lowestPoint.y) {
                        if (directionIsX) {
                            return {
                                y: fromPoint.y,
                                x: fromPoint.x < toPoint.x ?
                                    chartObstacles[i].xMin - 1 :
                                    chartObstacles[i].xMax + 1,
                                obstacle: chartObstacles[i]
                            };
                        }
                        // else ...
                        return {
                            x: fromPoint.x,
                            y: fromPoint.y < toPoint.y ?
                                chartObstacles[i].yMin - 1 :
                                chartObstacles[i].yMax + 1,
                            obstacle: chartObstacles[i]
                        };
                    }
                    i += searchDirection;
                }
                return toPoint;
            }
            /**
             * Decide in which direction to dodge or get out of an obstacle.
             * Considers desired direction, which way is shortest, soft and hard
             * bounds.
             *
             * (? Returns a string, either xMin, xMax, yMin or yMax.)
             *
             * @private
             * @function
             *
             * @param {Object} obstacle
             *        Obstacle to dodge/escape.
             *
             * @param {Object} fromPoint
             *        Point with x/y props that's dodging/escaping.
             *
             * @param {Object} toPoint
             *        Goal point.
             *
             * @param {boolean} dirIsX
             *        Dodge in X dimension.
             *
             * @param {Object} bounds
             *        Hard and soft boundaries.
             *
             * @return {boolean}
             *         Use max or not.
             */
            function getDodgeDirection(obstacle, fromPoint, toPoint, dirIsX, bounds) {
                var softBounds = bounds.soft, hardBounds = bounds.hard, dir = dirIsX ? 'x' : 'y', toPointMax = { x: fromPoint.x, y: fromPoint.y }, toPointMin = { x: fromPoint.x, y: fromPoint.y }, minPivot, maxPivot, maxOutOfSoftBounds = obstacle[dir + 'Max'] >=
                        softBounds[dir + 'Max'], minOutOfSoftBounds = obstacle[dir + 'Min'] <=
                        softBounds[dir + 'Min'], maxOutOfHardBounds = obstacle[dir + 'Max'] >=
                        hardBounds[dir + 'Max'], minOutOfHardBounds = obstacle[dir + 'Min'] <=
                        hardBounds[dir + 'Min'], 
                    // Find out if we should prefer one direction over the other if
                    // we can choose freely
                    minDistance = abs(obstacle[dir + 'Min'] - fromPoint[dir]), maxDistance = abs(obstacle[dir + 'Max'] - fromPoint[dir]), 
                    // If it's a small difference, pick the one leading towards dest
                    // point. Otherwise pick the shortest distance
                    useMax = abs(minDistance - maxDistance) < 10 ?
                        fromPoint[dir] < toPoint[dir] :
                        maxDistance < minDistance;
                // Check if we hit any obstacles trying to go around in either
                // direction.
                toPointMin[dir] = obstacle[dir + 'Min'];
                toPointMax[dir] = obstacle[dir + 'Max'];
                minPivot = pivotPoint(fromPoint, toPointMin, dirIsX)[dir] !==
                    toPointMin[dir];
                maxPivot = pivotPoint(fromPoint, toPointMax, dirIsX)[dir] !==
                    toPointMax[dir];
                useMax = minPivot ?
                    (maxPivot ? useMax : true) :
                    (maxPivot ? false : useMax);
                // useMax now contains our preferred choice, bounds not taken into
                // account. If both or neither direction is out of bounds we want to
                // use this.
                // Deal with soft bounds
                useMax = minOutOfSoftBounds ?
                    (maxOutOfSoftBounds ? useMax : true) : // Out on min
                    (maxOutOfSoftBounds ? false : useMax); // Not out on min
                // Deal with hard bounds
                useMax = minOutOfHardBounds ?
                    (maxOutOfHardBounds ? useMax : true) : // Out on min
                    (maxOutOfHardBounds ? false : useMax); // Not out on min
                return useMax;
            }
            // eslint-disable-next-line valid-jsdoc
            /**
             * Find a clear path between point.
             * @private
             */
            function clearPathTo(fromPoint, toPoint, dirIsX) {
                // Don't waste time if we've hit goal
                if (fromPoint.x === toPoint.x && fromPoint.y === toPoint.y) {
                    return [];
                }
                var dir = dirIsX ? 'x' : 'y',
                    pivot,
                    segments,
                    waypoint,
                    waypointUseMax,
                    envelopingObstacle,
                    secondEnvelopingObstacle,
                    envelopWaypoint,
                    obstacleMargin = options.obstacleOptions.margin,
                    bounds = {
                        soft: {
                            xMin: softMinX,
                            xMax: softMaxX,
                            yMin: softMinY,
                            yMax: softMaxY
                        },
                        hard: options.hardBounds
                    };
                // If fromPoint is inside an obstacle we have a problem. Break out
                // by just going to the outside of this obstacle. We prefer to go to
                // the nearest edge in the chosen direction.
                envelopingObstacle =
                    findObstacleFromPoint(chartObstacles, fromPoint);
                if (envelopingObstacle > -1) {
                    envelopingObstacle = chartObstacles[envelopingObstacle];
                    waypointUseMax = getDodgeDirection(envelopingObstacle, fromPoint, toPoint, dirIsX, bounds);
                    // Cut obstacle to hard bounds to make sure we stay within
                    limitObstacleToBounds(envelopingObstacle, options.hardBounds);
                    envelopWaypoint = dirIsX ? {
                        y: fromPoint.y,
                        x: envelopingObstacle[waypointUseMax ? 'xMax' : 'xMin'] +
                            (waypointUseMax ? 1 : -1)
                    } : {
                        x: fromPoint.x,
                        y: envelopingObstacle[waypointUseMax ? 'yMax' : 'yMin'] +
                            (waypointUseMax ? 1 : -1)
                    };
                    // If we crashed into another obstacle doing this, we put the
                    // waypoint between them instead
                    secondEnvelopingObstacle = findObstacleFromPoint(chartObstacles, envelopWaypoint);
                    if (secondEnvelopingObstacle > -1) {
                        secondEnvelopingObstacle = chartObstacles[secondEnvelopingObstacle];
                        // Cut obstacle to hard bounds
                        limitObstacleToBounds(secondEnvelopingObstacle, options.hardBounds);
                        // Modify waypoint to lay between obstacles
                        envelopWaypoint[dir] = waypointUseMax ? max(envelopingObstacle[dir + 'Max'] - obstacleMargin + 1, (secondEnvelopingObstacle[dir + 'Min'] +
                            envelopingObstacle[dir + 'Max']) / 2) :
                            min((envelopingObstacle[dir + 'Min'] + obstacleMargin - 1), ((secondEnvelopingObstacle[dir + 'Max'] +
                                envelopingObstacle[dir + 'Min']) / 2));
                        // We are not going anywhere. If this happens for the first
                        // time, do nothing. Otherwise, try to go to the extreme of
                        // the obstacle pair in the current direction.
                        if (fromPoint.x === envelopWaypoint.x &&
                            fromPoint.y === envelopWaypoint.y) {
                            if (forceObstacleBreak) {
                                envelopWaypoint[dir] = waypointUseMax ?
                                    max(envelopingObstacle[dir + 'Max'], secondEnvelopingObstacle[dir + 'Max']) + 1 :
                                    min(envelopingObstacle[dir + 'Min'], secondEnvelopingObstacle[dir + 'Min']) - 1;
                            }
                            // Toggle on if off, and the opposite
                            forceObstacleBreak = !forceObstacleBreak;
                        }
                        else {
                            // This point is not identical to previous.
                            // Clear break trigger.
                            forceObstacleBreak = false;
                        }
                    }
                    segments = [{
                            start: fromPoint,
                            end: envelopWaypoint
                        }];
                }
                else { // If not enveloping, use standard pivot calculation
                    pivot = pivotPoint(fromPoint, {
                        x: dirIsX ? toPoint.x : fromPoint.x,
                        y: dirIsX ? fromPoint.y : toPoint.y
                    }, dirIsX);
                    segments = [{
                            start: fromPoint,
                            end: {
                                x: pivot.x,
                                y: pivot.y
                            }
                        }];
                    // Pivot before goal, use a waypoint to dodge obstacle
                    if (pivot[dirIsX ? 'x' : 'y'] !== toPoint[dirIsX ? 'x' : 'y']) {
                        // Find direction of waypoint
                        waypointUseMax = getDodgeDirection(pivot.obstacle, pivot, toPoint, !dirIsX, bounds);
                        // Cut waypoint to hard bounds
                        limitObstacleToBounds(pivot.obstacle, options.hardBounds);
                        waypoint = {
                            x: dirIsX ?
                                pivot.x :
                                pivot.obstacle[waypointUseMax ? 'xMax' : 'xMin'] +
                                    (waypointUseMax ? 1 : -1),
                            y: dirIsX ?
                                pivot.obstacle[waypointUseMax ? 'yMax' : 'yMin'] +
                                    (waypointUseMax ? 1 : -1) :
                                pivot.y
                        };
                        // We're changing direction here, store that to make sure we
                        // also change direction when adding the last segment array
                        // after handling waypoint.
                        dirIsX = !dirIsX;
                        segments = segments.concat(clearPathTo({
                            x: pivot.x,
                            y: pivot.y
                        }, waypoint, dirIsX));
                    }
                }
                // Get segments for the other direction too
                // Recursion is our friend
                segments = segments.concat(clearPathTo(segments[segments.length - 1].end, toPoint, !dirIsX));
                return segments;
            }
            // eslint-disable-next-line valid-jsdoc
            /**
             * Extract point to outside of obstacle in whichever direction is
             * closest. Returns new point outside obstacle.
             * @private
             */
            function extractFromObstacle(obstacle, point, goalPoint) {
                var dirIsX = min(obstacle.xMax - point.x,
                    point.x - obstacle.xMin) <
                        min(obstacle.yMax - point.y,
                    point.y - obstacle.yMin),
                    bounds = {
                        soft: options.hardBounds,
                        hard: options.hardBounds
                    },
                    useMax = getDodgeDirection(obstacle,
                    point,
                    goalPoint,
                    dirIsX,
                    bounds);
                return dirIsX ? {
                    y: point.y,
                    x: obstacle[useMax ? 'xMax' : 'xMin'] + (useMax ? 1 : -1)
                } : {
                    x: point.x,
                    y: obstacle[useMax ? 'yMax' : 'yMin'] + (useMax ? 1 : -1)
                };
            }
            // Cut the obstacle array to soft bounds for optimization in large
            // datasets.
            chartObstacles =
                chartObstacles.slice(startObstacleIx, endObstacleIx + 1);
            // If an obstacle envelops the end point, move it out of there and add
            // a little segment to where it was.
            if ((endObstacleIx = findObstacleFromPoint(chartObstacles, end)) > -1) {
                extractedEndPoint = extractFromObstacle(chartObstacles[endObstacleIx], end, start);
                endSegments.push({
                    end: end,
                    start: extractedEndPoint
                });
                end = extractedEndPoint;
            }
            // If it's still inside one or more obstacles, get out of there by
            // force-moving towards the start point.
            while ((endObstacleIx = findObstacleFromPoint(chartObstacles, end)) > -1) {
                useMax = end[dir] - start[dir] < 0;
                extractedEndPoint = {
                    x: end.x,
                    y: end.y
                };
                extractedEndPoint[dir] = chartObstacles[endObstacleIx][useMax ? dir + 'Max' : dir + 'Min'] + (useMax ? 1 : -1);
                endSegments.push({
                    end: end,
                    start: extractedEndPoint
                });
                end = extractedEndPoint;
            }
            // Find the path
            segments = clearPathTo(start, end, dirIsX);
            // Add the end-point segments
            segments = segments.concat(endSegments.reverse());
            return {
                path: pathFromSegments(segments),
                obstacles: segments
            };
        };
        fastAvoid.requiresObstacles = true;
        // Define the available pathfinding algorithms.
        // Algorithms take up to 3 arguments: starting point, ending point, and an
        // options object.
        var algorithms = {
                fastAvoid: fastAvoid,
                straight: straight,
                simpleConnect: simpleConnect
            };

        return algorithms;
    });
    _registerModule(_modules, 'Gantt/Pathfinder.js', [_modules['Gantt/Connection.js'], _modules['Core/Chart/Chart.js'], _modules['Core/Defaults.js'], _modules['Core/Globals.js'], _modules['Core/Series/Point.js'], _modules['Core/Utilities.js'], _modules['Gantt/PathfinderAlgorithms.js']], function (Connection, Chart, D, H, Point, U, pathfinderAlgorithms) {
        /* *
         *
         *  (c) 2016 Highsoft AS
         *  Authors: Øystein Moseng, Lars A. V. Cabrera
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var defaultOptions = D.defaultOptions;
        var addEvent = U.addEvent,
            defined = U.defined,
            error = U.error,
            extend = U.extend,
            merge = U.merge,
            pick = U.pick,
            splat = U.splat;
        /**
         * The default pathfinder algorithm to use for a chart. It is possible to define
         * your own algorithms by adding them to the
         * `Highcharts.Pathfinder.prototype.algorithms`
         * object before the chart has been created.
         *
         * The default algorithms are as follows:
         *
         * `straight`:      Draws a straight line between the connecting
         *                  points. Does not avoid other points when drawing.
         *
         * `simpleConnect`: Finds a path between the points using right angles
         *                  only. Takes only starting/ending points into
         *                  account, and will not avoid other points.
         *
         * `fastAvoid`:     Finds a path between the points using right angles
         *                  only. Will attempt to avoid other points, but its
         *                  focus is performance over accuracy. Works well with
         *                  less dense datasets.
         *
         * @typedef {"fastAvoid"|"simpleConnect"|"straight"|string} Highcharts.PathfinderTypeValue
         */
        ''; // detach doclets above
        var max = Math.max,
            min = Math.min;
        /*
         @todo:
             - Document how to write your own algorithms
             - Consider adding a Point.pathTo method that wraps creating a connection
               and rendering it
        */
        // Set default Pathfinder options
        extend(defaultOptions, {
            /**
             * The Pathfinder module allows you to define connections between any two
             * points, represented as lines - optionally with markers for the start
             * and/or end points. Multiple algorithms are available for calculating how
             * the connecting lines are drawn.
             *
             * Connector functionality requires Highcharts Gantt to be loaded. In Gantt
             * charts, the connectors are used to draw dependencies between tasks.
             *
             * @see [dependency](series.gantt.data.dependency)
             *
             * @sample gantt/pathfinder/demo
             *         Pathfinder connections
             *
             * @declare      Highcharts.ConnectorsOptions
             * @product      gantt
             * @optionparent connectors
             */
            connectors: {
                /**
                 * Enable connectors for this chart. Requires Highcharts Gantt.
                 *
                 * @type      {boolean}
                 * @default   true
                 * @since     6.2.0
                 * @apioption connectors.enabled
                 */
                /**
                 * Set the default dash style for this chart's connecting lines.
                 *
                 * @type      {string}
                 * @default   solid
                 * @since     6.2.0
                 * @apioption connectors.dashStyle
                 */
                /**
                 * Set the default color for this chart's Pathfinder connecting lines.
                 * Defaults to the color of the point being connected.
                 *
                 * @type      {Highcharts.ColorString}
                 * @since     6.2.0
                 * @apioption connectors.lineColor
                 */
                /**
                 * Set the default pathfinder margin to use, in pixels. Some Pathfinder
                 * algorithms attempt to avoid obstacles, such as other points in the
                 * chart. These algorithms use this margin to determine how close lines
                 * can be to an obstacle. The default is to compute this automatically
                 * from the size of the obstacles in the chart.
                 *
                 * To draw connecting lines close to existing points, set this to a low
                 * number. For more space around existing points, set this number
                 * higher.
                 *
                 * @sample gantt/pathfinder/algorithm-margin
                 *         Small algorithmMargin
                 *
                 * @type      {number}
                 * @since     6.2.0
                 * @apioption connectors.algorithmMargin
                 */
                /**
                 * Set the default pathfinder algorithm to use for this chart. It is
                 * possible to define your own algorithms by adding them to the
                 * Highcharts.Pathfinder.prototype.algorithms object before the chart
                 * has been created.
                 *
                 * The default algorithms are as follows:
                 *
                 * `straight`:      Draws a straight line between the connecting
                 *                  points. Does not avoid other points when drawing.
                 *
                 * `simpleConnect`: Finds a path between the points using right angles
                 *                  only. Takes only starting/ending points into
                 *                  account, and will not avoid other points.
                 *
                 * `fastAvoid`:     Finds a path between the points using right angles
                 *                  only. Will attempt to avoid other points, but its
                 *                  focus is performance over accuracy. Works well with
                 *                  less dense datasets.
                 *
                 * Default value: `straight` is used as default for most series types,
                 * while `simpleConnect` is used as default for Gantt series, to show
                 * dependencies between points.
                 *
                 * @sample gantt/pathfinder/demo
                 *         Different types used
                 *
                 * @type    {Highcharts.PathfinderTypeValue}
                 * @default undefined
                 * @since   6.2.0
                 */
                type: 'straight',
                /**
                 * Set the default pixel width for this chart's Pathfinder connecting
                 * lines.
                 *
                 * @since 6.2.0
                 */
                lineWidth: 1,
                /**
                 * Marker options for this chart's Pathfinder connectors. Note that
                 * this option is overridden by the `startMarker` and `endMarker`
                 * options.
                 *
                 * @declare Highcharts.ConnectorsMarkerOptions
                 * @since   6.2.0
                 */
                marker: {
                    /**
                     * Set the radius of the connector markers. The default is
                     * automatically computed based on the algorithmMargin setting.
                     *
                     * Setting marker.width and marker.height will override this
                     * setting.
                     *
                     * @type      {number}
                     * @since     6.2.0
                     * @apioption connectors.marker.radius
                     */
                    /**
                     * Set the width of the connector markers. If not supplied, this
                     * is inferred from the marker radius.
                     *
                     * @type      {number}
                     * @since     6.2.0
                     * @apioption connectors.marker.width
                     */
                    /**
                     * Set the height of the connector markers. If not supplied, this
                     * is inferred from the marker radius.
                     *
                     * @type      {number}
                     * @since     6.2.0
                     * @apioption connectors.marker.height
                     */
                    /**
                     * Set the color of the connector markers. By default this is the
                     * same as the connector color.
                     *
                     * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                     * @since     6.2.0
                     * @apioption connectors.marker.color
                     */
                    /**
                     * Set the line/border color of the connector markers. By default
                     * this is the same as the marker color.
                     *
                     * @type      {Highcharts.ColorString}
                     * @since     6.2.0
                     * @apioption connectors.marker.lineColor
                     */
                    /**
                     * Enable markers for the connectors.
                     */
                    enabled: false,
                    /**
                     * Horizontal alignment of the markers relative to the points.
                     *
                     * @type {Highcharts.AlignValue}
                     */
                    align: 'center',
                    /**
                     * Vertical alignment of the markers relative to the points.
                     *
                     * @type {Highcharts.VerticalAlignValue}
                     */
                    verticalAlign: 'middle',
                    /**
                     * Whether or not to draw the markers inside the points.
                     */
                    inside: false,
                    /**
                     * Set the line/border width of the pathfinder markers.
                     */
                    lineWidth: 1
                },
                /**
                 * Marker options specific to the start markers for this chart's
                 * Pathfinder connectors. Overrides the generic marker options.
                 *
                 * @declare Highcharts.ConnectorsStartMarkerOptions
                 * @extends connectors.marker
                 * @since   6.2.0
                 */
                startMarker: {
                    /**
                     * Set the symbol of the connector start markers.
                     */
                    symbol: 'diamond'
                },
                /**
                 * Marker options specific to the end markers for this chart's
                 * Pathfinder connectors. Overrides the generic marker options.
                 *
                 * @declare Highcharts.ConnectorsEndMarkerOptions
                 * @extends connectors.marker
                 * @since   6.2.0
                 */
                endMarker: {
                    /**
                     * Set the symbol of the connector end markers.
                     */
                    symbol: 'arrow-filled'
                }
            }
        });
        /**
         * Override Pathfinder connector options for a series. Requires Highcharts Gantt
         * to be loaded.
         *
         * @declare   Highcharts.SeriesConnectorsOptionsObject
         * @extends   connectors
         * @since     6.2.0
         * @excluding enabled, algorithmMargin
         * @product   gantt
         * @apioption plotOptions.series.connectors
         */
        /**
         * Connect to a point. This option can be either a string, referring to the ID
         * of another point, or an object, or an array of either. If the option is an
         * array, each element defines a connection.
         *
         * @sample gantt/pathfinder/demo
         *         Different connection types
         *
         * @declare   Highcharts.XrangePointConnectorsOptionsObject
         * @type      {string|Array<string|*>|*}
         * @extends   plotOptions.series.connectors
         * @since     6.2.0
         * @excluding enabled
         * @product   gantt
         * @requires  highcharts-gantt
         * @apioption series.xrange.data.connect
         */
        /**
         * The ID of the point to connect to.
         *
         * @type      {string}
         * @since     6.2.0
         * @product   gantt
         * @apioption series.xrange.data.connect.to
         */
        /**
         * Get point bounding box using plotX/plotY and shapeArgs. If using
         * graphic.getBBox() directly, the bbox will be affected by animation.
         *
         * @private
         * @function
         *
         * @param {Highcharts.Point} point
         *        The point to get BB of.
         *
         * @return {Highcharts.Dictionary<number>|null}
         *         Result xMax, xMin, yMax, yMin.
         */
        function getPointBB(point) {
            var shapeArgs = point.shapeArgs,
                bb;
            // Prefer using shapeArgs (columns)
            if (shapeArgs) {
                return {
                    xMin: shapeArgs.x || 0,
                    xMax: (shapeArgs.x || 0) + (shapeArgs.width || 0),
                    yMin: shapeArgs.y || 0,
                    yMax: (shapeArgs.y || 0) + (shapeArgs.height || 0)
                };
            }
            // Otherwise use plotX/plotY and bb
            bb = point.graphic && point.graphic.getBBox();
            return bb ? {
                xMin: point.plotX - bb.width / 2,
                xMax: point.plotX + bb.width / 2,
                yMin: point.plotY - bb.height / 2,
                yMax: point.plotY + bb.height / 2
            } : null;
        }
        /**
         * Calculate margin to place around obstacles for the pathfinder in pixels.
         * Returns a minimum of 1 pixel margin.
         *
         * @private
         * @function
         *
         * @param {Array<object>} obstacles
         *        Obstacles to calculate margin from.
         *
         * @return {number}
         *         The calculated margin in pixels. At least 1.
         */
        function calculateObstacleMargin(obstacles) {
            var len = obstacles.length,
                i = 0,
                j,
                obstacleDistance,
                distances = [], 
                // Compute smallest distance between two rectangles
                distance = function (a,
                b,
                bbMargin) {
                    // Count the distance even if we are slightly off
                    var margin = pick(bbMargin, 10),
                yOverlap = a.yMax + margin > b.yMin - margin &&
                        a.yMin - margin < b.yMax + margin,
                xOverlap = a.xMax + margin > b.xMin - margin &&
                        a.xMin - margin < b.xMax + margin,
                xDistance = yOverlap ? (a.xMin > b.xMax ? a.xMin - b.xMax : b.xMin - a.xMax) : Infinity,
                yDistance = xOverlap ? (a.yMin > b.yMax ? a.yMin - b.yMax : b.yMin - a.yMax) : Infinity;
                // If the rectangles collide, try recomputing with smaller margin.
                // If they collide anyway, discard the obstacle.
                if (xOverlap && yOverlap) {
                    return (margin ?
                        distance(a, b, Math.floor(margin / 2)) :
                        Infinity);
                }
                return min(xDistance, yDistance);
            };
            // Go over all obstacles and compare them to the others.
            for (; i < len; ++i) {
                // Compare to all obstacles ahead. We will already have compared this
                // obstacle to the ones before.
                for (j = i + 1; j < len; ++j) {
                    obstacleDistance = distance(obstacles[i], obstacles[j]);
                    // TODO: Magic number 80
                    if (obstacleDistance < 80) { // Ignore large distances
                        distances.push(obstacleDistance);
                    }
                }
            }
            // Ensure we always have at least one value, even in very spaceous charts
            distances.push(80);
            return max(Math.floor(distances.sort(function (a, b) {
                return (a - b);
            })[
            // Discard first 10% of the relevant distances, and then grab
            // the smallest one.
            Math.floor(distances.length / 10)] / 2 - 1 // Divide the distance by 2 and subtract 1.
            ), 1 // 1 is the minimum margin
            );
        }
        /* eslint-disable no-invalid-this, valid-jsdoc */
        /**
         * The Pathfinder class.
         *
         * @private
         * @class
         * @name Highcharts.Pathfinder
         *
         * @param {Highcharts.Chart} chart
         *        The chart to operate on.
         */
        var Pathfinder = /** @class */ (function () {
                function Pathfinder(chart) {
                    /* *
                     *
                     * Properties
                     *
                     * */
                    this.chart = void 0;
                this.chartObstacles = void 0;
                this.chartObstacleMetrics = void 0;
                this.connections = void 0;
                this.group = void 0;
                this.lineObstacles = void 0;
                this.init(chart);
            }
            /**
             * @name Highcharts.Pathfinder#algorithms
             * @type {Highcharts.Dictionary<Function>}
             */
            /**
             * Initialize the Pathfinder object.
             *
             * @function Highcharts.Pathfinder#init
             *
             * @param {Highcharts.Chart} chart
             *        The chart context.
             */
            Pathfinder.prototype.init = function (chart) {
                // Initialize pathfinder with chart context
                this.chart = chart;
                // Init connection reference list
                this.connections = [];
                // Recalculate paths/obstacles on chart redraw
                addEvent(chart, 'redraw', function () {
                    this.pathfinder.update();
                });
            };
            /**
             * Update Pathfinder connections from scratch.
             *
             * @function Highcharts.Pathfinder#update
             *
             * @param {boolean} [deferRender]
             *        Whether or not to defer rendering of connections until
             *        series.afterAnimate event has fired. Used on first render.
             */
            Pathfinder.prototype.update = function (deferRender) {
                var chart = this.chart,
                    pathfinder = this,
                    oldConnections = pathfinder.connections;
                // Rebuild pathfinder connections from options
                pathfinder.connections = [];
                chart.series.forEach(function (series) {
                    if (series.visible && !series.options.isInternal) {
                        series.points.forEach(function (point) {
                            var ganttPointOptions = point.options;
                            // For Gantt series the connect could be
                            // defined as a dependency
                            if (ganttPointOptions && ganttPointOptions.dependency) {
                                ganttPointOptions.connect = ganttPointOptions
                                    .dependency;
                            }
                            var to,
                                connects = (point.options &&
                                    point.options.connect &&
                                    splat(point.options.connect));
                            if (point.visible && point.isInside !== false && connects) {
                                connects.forEach(function (connect) {
                                    to = chart.get(typeof connect === 'string' ?
                                        connect : connect.to);
                                    if (to instanceof Point &&
                                        to.series.visible &&
                                        to.visible &&
                                        to.isInside !== false) {
                                        // Add new connection
                                        pathfinder.connections.push(new Connection(point, // from
                                        to, typeof connect === 'string' ?
                                            {} :
                                            connect));
                                    }
                                });
                            }
                        });
                    }
                });
                // Clear connections that should not be updated, and move old info over
                // to new connections.
                for (var j = 0, k = void 0, found = void 0, lenOld = oldConnections.length, lenNew = pathfinder.connections.length; j < lenOld; ++j) {
                    found = false;
                    var oldCon = oldConnections[j];
                    for (k = 0; k < lenNew; ++k) {
                        var newCon = pathfinder.connections[k];
                        if ((oldCon.options && oldCon.options.type) ===
                            (newCon.options && newCon.options.type) &&
                            oldCon.fromPoint === newCon.fromPoint &&
                            oldCon.toPoint === newCon.toPoint) {
                            newCon.graphics = oldCon.graphics;
                            found = true;
                            break;
                        }
                    }
                    if (!found) {
                        oldCon.destroy();
                    }
                }
                // Clear obstacles to force recalculation. This must be done on every
                // redraw in case positions have changed. Recalculation is handled in
                // Connection.getPath on demand.
                delete this.chartObstacles;
                delete this.lineObstacles;
                // Draw the pending connections
                pathfinder.renderConnections(deferRender);
            };
            /**
             * Draw the chart's connecting paths.
             *
             * @function Highcharts.Pathfinder#renderConnections
             *
             * @param {boolean} [deferRender]
             *        Whether or not to defer render until series animation is finished.
             *        Used on first render.
             */
            Pathfinder.prototype.renderConnections = function (deferRender) {
                if (deferRender) {
                    // Render after series are done animating
                    this.chart.series.forEach(function (series) {
                        var render = function () {
                                // Find pathfinder connections belonging to this series
                                // that haven't rendered, and render them now.
                                var pathfinder = series.chart.pathfinder,
                            conns = pathfinder && pathfinder.connections || [];
                            conns.forEach(function (connection) {
                                if (connection.fromPoint &&
                                    connection.fromPoint.series === series) {
                                    connection.render();
                                }
                            });
                            if (series.pathfinderRemoveRenderEvent) {
                                series.pathfinderRemoveRenderEvent();
                                delete series.pathfinderRemoveRenderEvent;
                            }
                        };
                        if (series.options.animation === false) {
                            render();
                        }
                        else {
                            series.pathfinderRemoveRenderEvent = addEvent(series, 'afterAnimate', render);
                        }
                    });
                }
                else {
                    // Go through connections and render them
                    this.connections.forEach(function (connection) {
                        connection.render();
                    });
                }
            };
            /**
             * Get obstacles for the points in the chart. Does not include connecting
             * lines from Pathfinder. Applies algorithmMargin to the obstacles.
             *
             * @function Highcharts.Pathfinder#getChartObstacles
             *
             * @param {Object} options
             *        Options for the calculation. Currenlty only
             *        options.algorithmMargin.
             *
             * @return {Array<object>}
             *         An array of calculated obstacles. Each obstacle is defined as an
             *         object with xMin, xMax, yMin and yMax properties.
             */
            Pathfinder.prototype.getChartObstacles = function (options) {
                var obstacles = [],
                    series = this.chart.series,
                    margin = pick(options.algorithmMargin, 0),
                    calculatedMargin;
                for (var i = 0, sLen = series.length; i < sLen; ++i) {
                    if (series[i].visible && !series[i].options.isInternal) {
                        for (var j = 0, pLen = series[i].points.length, bb = void 0, point = void 0; j < pLen; ++j) {
                            point = series[i].points[j];
                            if (point.visible) {
                                bb = getPointBB(point);
                                if (bb) {
                                    obstacles.push({
                                        xMin: bb.xMin - margin,
                                        xMax: bb.xMax + margin,
                                        yMin: bb.yMin - margin,
                                        yMax: bb.yMax + margin
                                    });
                                }
                            }
                        }
                    }
                }
                // Sort obstacles by xMin for optimization
                obstacles = obstacles.sort(function (a, b) {
                    return a.xMin - b.xMin;
                });
                // Add auto-calculated margin if the option is not defined
                if (!defined(options.algorithmMargin)) {
                    calculatedMargin =
                        options.algorithmMargin =
                            calculateObstacleMargin(obstacles);
                    obstacles.forEach(function (obstacle) {
                        obstacle.xMin -= calculatedMargin;
                        obstacle.xMax += calculatedMargin;
                        obstacle.yMin -= calculatedMargin;
                        obstacle.yMax += calculatedMargin;
                    });
                }
                return obstacles;
            };
            /**
             * Utility function to get metrics for obstacles:
             * - Widest obstacle width
             * - Tallest obstacle height
             *
             * @function Highcharts.Pathfinder#getObstacleMetrics
             *
             * @param {Array<object>} obstacles
             *        An array of obstacles to inspect.
             *
             * @return {Object}
             *         The calculated metrics, as an object with maxHeight and maxWidth
             *         properties.
             */
            Pathfinder.prototype.getObstacleMetrics = function (obstacles) {
                var maxWidth = 0,
                    maxHeight = 0,
                    width,
                    height,
                    i = obstacles.length;
                while (i--) {
                    width = obstacles[i].xMax - obstacles[i].xMin;
                    height = obstacles[i].yMax - obstacles[i].yMin;
                    if (maxWidth < width) {
                        maxWidth = width;
                    }
                    if (maxHeight < height) {
                        maxHeight = height;
                    }
                }
                return {
                    maxHeight: maxHeight,
                    maxWidth: maxWidth
                };
            };
            /**
             * Utility to get which direction to start the pathfinding algorithm
             * (X vs Y), calculated from a set of marker options.
             *
             * @function Highcharts.Pathfinder#getAlgorithmStartDirection
             *
             * @param {Highcharts.ConnectorsMarkerOptions} markerOptions
             *        Marker options to calculate from.
             *
             * @return {boolean}
             *         Returns true for X, false for Y, and undefined for autocalculate.
             */
            Pathfinder.prototype.getAlgorithmStartDirection = function (markerOptions) {
                var xCenter = markerOptions.align !== 'left' &&
                        markerOptions.align !== 'right', yCenter = markerOptions.verticalAlign !== 'top' &&
                        markerOptions.verticalAlign !== 'bottom', undef;
                return xCenter ?
                    (yCenter ? undef : false) : // x is centered
                    (yCenter ? true : undef); // x is off-center
            };
            return Pathfinder;
        }());
        Pathfinder.prototype.algorithms = pathfinderAlgorithms;
        // Add to Highcharts namespace
        H.Pathfinder = Pathfinder;
        // Add pathfinding capabilities to Points
        extend(Point.prototype, /** @lends Point.prototype */ {
            /**
             * Get coordinates of anchor point for pathfinder connection.
             *
             * @private
             * @function Highcharts.Point#getPathfinderAnchorPoint
             *
             * @param {Highcharts.ConnectorsMarkerOptions} markerOptions
             *        Connection options for position on point.
             *
             * @return {Highcharts.PositionObject}
             *         An object with x/y properties for the position. Coordinates are
             *         in plot values, not relative to point.
             */
            getPathfinderAnchorPoint: function (markerOptions) {
                var bb = getPointBB(this),
                    x,
                    y;
                switch (markerOptions.align) { // eslint-disable-line default-case
                    case 'right':
                        x = 'xMax';
                        break;
                    case 'left':
                        x = 'xMin';
                }
                switch (markerOptions.verticalAlign) { // eslint-disable-line default-case
                    case 'top':
                        y = 'yMin';
                        break;
                    case 'bottom':
                        y = 'yMax';
                }
                return {
                    x: x ? bb[x] : (bb.xMin + bb.xMax) / 2,
                    y: y ? bb[y] : (bb.yMin + bb.yMax) / 2
                };
            },
            /**
             * Utility to get the angle from one point to another.
             *
             * @private
             * @function Highcharts.Point#getRadiansToVector
             *
             * @param {Highcharts.PositionObject} v1
             *        The first vector, as an object with x/y properties.
             *
             * @param {Highcharts.PositionObject} v2
             *        The second vector, as an object with x/y properties.
             *
             * @return {number}
             *         The angle in degrees
             */
            getRadiansToVector: function (v1, v2) {
                var box;
                if (!defined(v2)) {
                    box = getPointBB(this);
                    if (box) {
                        v2 = {
                            x: (box.xMin + box.xMax) / 2,
                            y: (box.yMin + box.yMax) / 2
                        };
                    }
                }
                return Math.atan2(v2.y - v1.y, v1.x - v2.x);
            },
            /**
             * Utility to get the position of the marker, based on the path angle and
             * the marker's radius.
             *
             * @private
             * @function Highcharts.Point#getMarkerVector
             *
             * @param {number} radians
             *        The angle in radians from the point center to another vector.
             *
             * @param {number} markerRadius
             *        The radius of the marker, to calculate the additional distance to
             *        the center of the marker.
             *
             * @param {Object} anchor
             *        The anchor point of the path and marker as an object with x/y
             *        properties.
             *
             * @return {Object}
             *         The marker vector as an object with x/y properties.
             */
            getMarkerVector: function (radians, markerRadius, anchor) {
                var twoPI = Math.PI * 2.0,
                    theta = radians,
                    bb = getPointBB(this),
                    rectWidth = bb.xMax - bb.xMin,
                    rectHeight = bb.yMax - bb.yMin,
                    rAtan = Math.atan2(rectHeight,
                    rectWidth),
                    tanTheta = 1,
                    leftOrRightRegion = false,
                    rectHalfWidth = rectWidth / 2.0,
                    rectHalfHeight = rectHeight / 2.0,
                    rectHorizontalCenter = bb.xMin + rectHalfWidth,
                    rectVerticalCenter = bb.yMin + rectHalfHeight,
                    edgePoint = {
                        x: rectHorizontalCenter,
                        y: rectVerticalCenter
                    },
                    xFactor = 1,
                    yFactor = 1;
                while (theta < -Math.PI) {
                    theta += twoPI;
                }
                while (theta > Math.PI) {
                    theta -= twoPI;
                }
                tanTheta = Math.tan(theta);
                if ((theta > -rAtan) && (theta <= rAtan)) {
                    // Right side
                    yFactor = -1;
                    leftOrRightRegion = true;
                }
                else if (theta > rAtan && theta <= (Math.PI - rAtan)) {
                    // Top side
                    yFactor = -1;
                }
                else if (theta > (Math.PI - rAtan) || theta <= -(Math.PI - rAtan)) {
                    // Left side
                    xFactor = -1;
                    leftOrRightRegion = true;
                }
                else {
                    // Bottom side
                    xFactor = -1;
                }
                // Correct the edgePoint according to the placement of the marker
                if (leftOrRightRegion) {
                    edgePoint.x += xFactor * (rectHalfWidth);
                    edgePoint.y += yFactor * (rectHalfWidth) * tanTheta;
                }
                else {
                    edgePoint.x += xFactor * (rectHeight / (2.0 * tanTheta));
                    edgePoint.y += yFactor * (rectHalfHeight);
                }
                if (anchor.x !== rectHorizontalCenter) {
                    edgePoint.x = anchor.x;
                }
                if (anchor.y !== rectVerticalCenter) {
                    edgePoint.y = anchor.y;
                }
                return {
                    x: edgePoint.x + (markerRadius * Math.cos(theta)),
                    y: edgePoint.y - (markerRadius * Math.sin(theta))
                };
            }
        });
        /**
         * Warn if using legacy options. Copy the options over. Note that this will
         * still break if using the legacy options in chart.update, addSeries etc.
         * @private
         */
        function warnLegacy(chart) {
            if (chart.options.pathfinder ||
                chart.series.reduce(function (acc, series) {
                    if (series.options) {
                        merge(true, (series.options.connectors = series.options.connectors ||
                            {}), series.options.pathfinder);
                    }
                    return acc || series.options && series.options.pathfinder;
                }, false)) {
                merge(true, (chart.options.connectors = chart.options.connectors || {}), chart.options.pathfinder);
                error('WARNING: Pathfinder options have been renamed. ' +
                    'Use "chart.connectors" or "series.connectors" instead.');
            }
        }
        // Initialize Pathfinder for charts
        Chart.prototype.callbacks.push(function (chart) {
            var options = chart.options;
            if (options.connectors.enabled !== false) {
                warnLegacy(chart);
                this.pathfinder = new Pathfinder(this);
                this.pathfinder.update(true); // First draw, defer render
            }
        });

        return Pathfinder;
    });
    _registerModule(_modules, 'Series/Gantt/GanttSeries.js', [_modules['Core/Axis/Axis.js'], _modules['Core/Chart/Chart.js'], _modules['Series/Gantt/GanttPoint.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Axis/Tick.js'], _modules['Core/Utilities.js'], _modules['Core/Axis/TreeGrid/TreeGridAxis.js']], function (Axis, Chart, GanttPoint, SeriesRegistry, Tick, U, TreeGridAxis) {
        /* *
         *
         *  (c) 2016-2021 Highsoft AS
         *
         *  Author: Lars A. V. Cabrera
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
        var Series = SeriesRegistry.series,
            XRangeSeries = SeriesRegistry.seriesTypes.xrange;
        var extend = U.extend,
            isNumber = U.isNumber,
            merge = U.merge,
            splat = U.splat;
        TreeGridAxis.compose(Axis, Chart, Series, Tick);
        /* *
         *
         *  Class
         *
         * */
        /**
         * @private
         * @class
         * @name Highcharts.seriesTypes.gantt
         *
         * @augments Highcharts.Series
         */
        var GanttSeries = /** @class */ (function (_super) {
                __extends(GanttSeries, _super);
            function GanttSeries() {
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
                /* eslint-enable valid-jsdoc */
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Draws a single point in the series.
             *
             * This override draws the point as a diamond if point.options.milestone
             * is true, and uses the original drawPoint() if it is false or not set.
             *
             * @requires highcharts-gantt
             *
             * @private
             * @function Highcharts.seriesTypes.gantt#drawPoint
             *
             * @param {Highcharts.Point} point
             *        An instance of Point in the series
             *
             * @param {"animate"|"attr"} verb
             *        'animate' (animates changes) or 'attr' (sets options)
             */
            GanttSeries.prototype.drawPoint = function (point, verb) {
                var series = this,
                    seriesOpts = series.options,
                    renderer = series.chart.renderer,
                    shapeArgs = point.shapeArgs,
                    plotY = point.plotY,
                    graphic = point.graphic,
                    state = point.selected && 'select',
                    cutOff = seriesOpts.stacking && !seriesOpts.borderRadius,
                    diamondShape;
                if (point.options.milestone) {
                    if (isNumber(plotY) &&
                        point.y !== null &&
                        point.visible !== false) {
                        diamondShape = renderer.symbols.diamond(shapeArgs.x || 0, shapeArgs.y || 0, shapeArgs.width || 0, shapeArgs.height || 0);
                        if (graphic) {
                            graphic[verb]({
                                d: diamondShape
                            });
                        }
                        else {
                            point.graphic = graphic = renderer.path(diamondShape)
                                .addClass(point.getClassName(), true)
                                .add(point.group || series.group);
                        }
                        // Presentational
                        if (!series.chart.styledMode) {
                            point.graphic
                                .attr(series.pointAttribs(point, state))
                                .shadow(seriesOpts.shadow, null, cutOff);
                        }
                    }
                    else if (graphic) {
                        point.graphic = graphic.destroy(); // #1269
                    }
                }
                else {
                    XRangeSeries.prototype.drawPoint.call(series, point, verb);
                }
            };
            /**
             * Handle milestones, as they have no x2.
             * @private
             */
            GanttSeries.prototype.translatePoint = function (point) {
                var series = this,
                    shapeArgs,
                    size;
                XRangeSeries.prototype.translatePoint.call(series, point);
                if (point.options.milestone) {
                    shapeArgs = point.shapeArgs;
                    size = shapeArgs.height || 0;
                    point.shapeArgs = {
                        x: (shapeArgs.x || 0) - (size / 2),
                        y: shapeArgs.y,
                        width: size,
                        height: size
                    };
                }
            };
            /**
             * A `gantt` series. If the [type](#series.gantt.type) option is not specified,
             * it is inherited from [chart.type](#chart.type).
             *
             * @extends      plotOptions.xrange
             * @product      gantt
             * @requires     highcharts-gantt
             * @optionparent plotOptions.gantt
             */
            GanttSeries.defaultOptions = merge(XRangeSeries.defaultOptions, {
                // options - default options merged with parent
                grouping: false,
                dataLabels: {
                    enabled: true
                },
                tooltip: {
                    headerFormat: '<span style="font-size: 10px">{series.name}</span><br/>',
                    pointFormat: null,
                    pointFormatter: function () {
                        var point = this,
                            series = point.series,
                            xAxis = series.xAxis,
                            formats = series.tooltipOptions.dateTimeLabelFormats,
                            startOfWeek = xAxis.options.startOfWeek,
                            ttOptions = series.tooltipOptions,
                            format = ttOptions.xDateFormat,
                            start,
                            end,
                            milestone = point.options.milestone,
                            retVal = '<b>' + (point.name || point.yCategory) + '</b>';
                        if (ttOptions.pointFormat) {
                            return point.tooltipFormatter(ttOptions.pointFormat);
                        }
                        if (!format && isNumber(point.start)) {
                            format = series.chart.time.getDateFormat(xAxis.closestPointRange, point.start, startOfWeek, formats || {});
                        }
                        start = series.chart.time.dateFormat(format, point.start);
                        end = series.chart.time.dateFormat(format, point.end);
                        retVal += '<br/>';
                        if (!milestone) {
                            retVal += 'Start: ' + start + '<br/>';
                            retVal += 'End: ' + end + '<br/>';
                        }
                        else {
                            retVal += start + '<br/>';
                        }
                        return retVal;
                    }
                },
                connectors: {
                    type: 'simpleConnect',
                    /**
                     * @declare Highcharts.ConnectorsAnimationOptionsObject
                     */
                    animation: {
                        reversed: true // Dependencies go from child to parent
                    },
                    startMarker: {
                        enabled: true,
                        symbol: 'arrow-filled',
                        radius: 4,
                        fill: '#fa0',
                        align: 'left'
                    },
                    endMarker: {
                        enabled: false,
                        align: 'right'
                    }
                }
            });
            return GanttSeries;
        }(XRangeSeries));
        extend(GanttSeries.prototype, {
            pointArrayMap: ['start', 'end', 'y'],
            pointClass: GanttPoint,
            setData: Series.prototype.setData
        });
        SeriesRegistry.registerSeriesType('gantt', GanttSeries);
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
         * A `gantt` series.
         *
         * @extends   series,plotOptions.gantt
         * @excluding boostThreshold, connectors, dashStyle, findNearestPointBy,
         *            getExtremesFromAll, marker, negativeColor, pointInterval,
         *            pointIntervalUnit, pointPlacement, pointStart
         * @product   gantt
         * @requires  highcharts-gantt
         * @apioption series.gantt
         */
        /**
         * Data for a Gantt series.
         *
         * @declare   Highcharts.GanttPointOptionsObject
         * @type      {Array<*>}
         * @extends   series.xrange.data
         * @excluding className, connect, dataLabels, events,
         *            partialFill, selected, x, x2
         * @product   gantt
         * @apioption series.gantt.data
         */
        /**
         * Whether the grid node belonging to this point should start as collapsed. Used
         * in axes of type treegrid.
         *
         * @sample {gantt} gantt/treegrid-axis/collapsed/
         *         Start as collapsed
         *
         * @type      {boolean}
         * @default   false
         * @product   gantt
         * @apioption series.gantt.data.collapsed
         */
        /**
         * The start time of a task.
         *
         * @type      {number}
         * @product   gantt
         * @apioption series.gantt.data.start
         */
        /**
         * The end time of a task.
         *
         * @type      {number}
         * @product   gantt
         * @apioption series.gantt.data.end
         */
        /**
         * The Y value of a task.
         *
         * @type      {number}
         * @product   gantt
         * @apioption series.gantt.data.y
         */
        /**
         * The name of a task. If a `treegrid` y-axis is used (default in Gantt charts),
         * this will be picked up automatically, and used to calculate the y-value.
         *
         * @type      {string}
         * @product   gantt
         * @apioption series.gantt.data.name
         */
        /**
         * Progress indicator, how much of the task completed. If it is a number, the
         * `fill` will be applied automatically.
         *
         * @sample {gantt} gantt/demo/progress-indicator
         *         Progress indicator
         *
         * @type      {number|*}
         * @extends   series.xrange.data.partialFill
         * @product   gantt
         * @apioption series.gantt.data.completed
         */
        /**
         * The amount of the progress indicator, ranging from 0 (not started) to 1
         * (finished).
         *
         * @type      {number}
         * @default   0
         * @apioption series.gantt.data.completed.amount
         */
        /**
         * The fill of the progress indicator. Defaults to a darkened variety of the
         * main color.
         *
         * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
         * @apioption series.gantt.data.completed.fill
         */
        /**
         * The ID of the point (task) that this point depends on in Gantt charts.
         * Aliases [connect](series.xrange.data.connect). Can also be an object,
         * specifying further connecting [options](series.gantt.connectors) between the
         * points. Multiple connections can be specified by providing an array.
         *
         * @sample gantt/demo/project-management
         *         Dependencies
         * @sample gantt/pathfinder/demo
         *         Different connection types
         *
         * @type      {string|Array<string|*>|*}
         * @extends   series.xrange.data.connect
         * @since     6.2.0
         * @product   gantt
         * @apioption series.gantt.data.dependency
         */
        /**
         * Whether this point is a milestone. If so, only the `start` option is handled,
         * while `end` is ignored.
         *
         * @sample gantt/gantt/milestones
         *         Milestones
         *
         * @type      {boolean}
         * @since     6.2.0
         * @product   gantt
         * @apioption series.gantt.data.milestone
         */
        /**
         * The ID of the parent point (task) of this point in Gantt charts.
         *
         * @sample gantt/demo/subtasks
         *         Gantt chart with subtasks
         *
         * @type      {string}
         * @since     6.2.0
         * @product   gantt
         * @apioption series.gantt.data.parent
         */
        /**
         * @excluding afterAnimate
         * @apioption series.gantt.events
         */
        ''; // adds doclets above to the transpiled file

        return GanttSeries;
    });
    _registerModule(_modules, 'Core/Chart/GanttChart.js', [_modules['Core/Chart/Chart.js'], _modules['Core/Defaults.js'], _modules['Core/Utilities.js']], function (Chart, D, U) {
        /* *
         *
         *  (c) 2016-2021 Highsoft AS
         *
         *  Author: Lars A. V. Cabrera
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
        var getOptions = D.getOptions;
        var isArray = U.isArray,
            merge = U.merge,
            splat = U.splat;
        /* *
         *
         *  Class
         *
         * */
        /**
         * Gantt-optimized chart. Use {@link Highcharts.Chart|Chart} for common charts.
         *
         * @requires modules/gantt
         *
         * @class
         * @name Highcharts.GanttChart
         * @extends Highcharts.Chart
         */
        var GanttChart = /** @class */ (function (_super) {
                __extends(GanttChart, _super);
            function GanttChart() {
                return _super !== null && _super.apply(this, arguments) || this;
            }
            /**
             * Initializes the chart. The constructor's arguments are passed on
             * directly.
             *
             * @function Highcharts.GanttChart#init
             *
             * @param {Highcharts.Options} userOptions
             *        Custom options.
             *
             * @param {Function} [callback]
             *        Function to run when the chart has loaded and and all external
             *        images are loaded.
             *
             *
             * @emits Highcharts.GanttChart#event:init
             * @emits Highcharts.GanttChart#event:afterInit
             */
            GanttChart.prototype.init = function (userOptions, callback) {
                var defaultOptions = getOptions(),
                    xAxisOptions = userOptions.xAxis,
                    yAxisOptions = userOptions.yAxis;
                var defaultLinkedTo;
                // Avoid doing these twice
                userOptions.xAxis = userOptions.yAxis = void 0;
                var options = merge(true, {
                        chart: {
                            type: 'gantt'
                        },
                        title: {
                            text: null
                        },
                        legend: {
                            enabled: false
                        },
                        navigator: {
                            series: { type: 'gantt' },
                            // Bars were clipped, #14060.
                            yAxis: {
                                type: 'category'
                            }
                        }
                    },
                    userOptions, // user's options
                    // forced options
                    {
                        isGantt: true
                    });
                userOptions.xAxis = xAxisOptions;
                userOptions.yAxis = yAxisOptions;
                // apply X axis options to both single and multi x axes
                // If user hasn't defined axes as array, make it into an array and add a
                // second axis by default.
                options.xAxis = (!isArray(userOptions.xAxis) ?
                    [userOptions.xAxis || {}, {}] :
                    userOptions.xAxis).map(function (xAxisOptions, i) {
                    if (i === 1) { // Second xAxis
                        defaultLinkedTo = 0;
                    }
                    return merge(defaultOptions.xAxis, {
                        grid: {
                            enabled: true
                        },
                        opposite: true,
                        linkedTo: defaultLinkedTo
                    }, xAxisOptions, // user options
                    {
                        type: 'datetime'
                    });
                });
                // apply Y axis options to both single and multi y axes
                options.yAxis = (splat(userOptions.yAxis || {})).map(function (yAxisOptions) {
                    return merge(defaultOptions.yAxis, // #3802
                    {
                        grid: {
                            enabled: true
                        },
                        staticScale: 50,
                        reversed: true,
                        // Set default type treegrid, but only if 'categories' is
                        // undefined
                        type: yAxisOptions.categories ?
                            yAxisOptions.type : 'treegrid'
                    }, yAxisOptions // user options
                    );
                });
                _super.prototype.init.call(this, options, callback);
            };
            return GanttChart;
        }(Chart));
        /* eslint-disable valid-jsdoc */
        (function (GanttChart) {
            /**
             * The factory function for creating new gantt charts. Creates a new {@link
             * Highcharts.GanttChart|GanttChart} object with different default options
             * than the basic Chart.
             *
             * @example
             * // Render a chart in to div#container
             * let chart = Highcharts.ganttChart('container', {
             *     title: {
             *         text: 'My chart'
             *     },
             *     series: [{
             *         data: ...
             *     }]
             * });
             *
             * @function Highcharts.ganttChart
             *
             * @param {string|Highcharts.HTMLDOMElement} renderTo
             *        The DOM element to render to, or its id.
             *
             * @param {Highcharts.Options} options
             *        The chart options structure.
             *
             * @param {Highcharts.ChartCallbackFunction} [callback]
             *        Function to run when the chart has loaded and and all external
             *        images are loaded. Defining a
             *        [chart.events.load](https://api.highcharts.com/highcharts/chart.events.load)
             *        handler is equivalent.
             *
             * @return {Highcharts.GanttChart}
             *         Returns the Chart object.
             */
            function ganttChart(a, b, c) {
                return new GanttChart(a, b, c);
            }
            GanttChart.ganttChart = ganttChart;
        })(GanttChart || (GanttChart = {}));

        return GanttChart;
    });
    _registerModule(_modules, 'masters/modules/gantt.src.js', [_modules['Core/Globals.js'], _modules['Stock/Navigator/Navigator.js'], _modules['Stock/Scrollbar/Scrollbar.js'], _modules['Stock/RangeSelector/RangeSelector.js'], _modules['Series/XRange/XRangeSeries.js'], _modules['Core/Chart/GanttChart.js']], function (Highcharts, Navigator, Scrollbar, RangeSelector, XRangeSeries, GanttChart) {

        var G = Highcharts;
        // Classes
        G.GanttChart = GanttChart;
        G.ganttChart = GanttChart.ganttChart;
        G.Navigator = Navigator;
        G.RangeSelector = RangeSelector;
        G.Scrollbar = Scrollbar;
        // Compositions
        Navigator.compose(G.Axis, G.Chart, G.Series);
        RangeSelector.compose(G.Axis, G.Chart);
        Scrollbar.compose(G.Axis);
        XRangeSeries.compose(G.Axis);

    });
}));