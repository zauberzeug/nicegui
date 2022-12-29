/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * Wind barb series module
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
        define('highcharts/modules/windbarb', ['highcharts'], function (Highcharts) {
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
    _registerModule(_modules, 'Series/Windbarb/WindbarbPoint.js', [_modules['Core/Utilities.js'], _modules['Series/Column/ColumnSeries.js']], function (U, ColumnSeries) {
        /* *
         *
         *  Wind barb series module
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
        var isNumber = U.isNumber;
        /* *
         *
         * Class
         *
         * */
        var WindbarbPoint = /** @class */ (function (_super) {
                __extends(WindbarbPoint, _super);
            function WindbarbPoint() {
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                /* *
                 *
                 * Properties
                 *
                 * */
                _this.beaufort = void 0;
                _this.beaufortLevel = void 0;
                _this.direction = void 0;
                _this.options = void 0;
                _this.series = void 0;
                return _this;
            }
            /* *
             *
             * Functions
             *
             * */
            WindbarbPoint.prototype.isValid = function () {
                return isNumber(this.value) && this.value >= 0;
            };
            return WindbarbPoint;
        }(ColumnSeries.prototype.pointClass));
        /* *
         *
         * Default export
         *
         * */

        return WindbarbPoint;
    });
    _registerModule(_modules, 'Series/Windbarb/WindbarbSeries.js', [_modules['Core/Animation/AnimationUtilities.js'], _modules['Extensions/DataGrouping/ApproximationRegistry.js'], _modules['Core/Globals.js'], _modules['Series/OnSeriesComposition.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js'], _modules['Series/Windbarb/WindbarbPoint.js']], function (A, ApproximationRegistry, H, OnSeriesComposition, SeriesRegistry, U, WindbarbPoint) {
        /* *
         *
         *  Wind barb series module
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
        var animObject = A.animObject;
        var Series = SeriesRegistry.series,
            ColumnSeries = SeriesRegistry.seriesTypes.column;
        var extend = U.extend,
            merge = U.merge,
            pick = U.pick;
        /**
         * @private
         * @class
         * @name Highcharts.seriesTypes.windbarb
         *
         * @augments Highcharts.Series
         */
        var WindbarbSeries = /** @class */ (function (_super) {
                __extends(WindbarbSeries, _super);
            function WindbarbSeries() {
                /* *
                 *
                 * Static properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                /* *
                 *
                 * Properties
                 *
                 * */
                _this.data = void 0;
                _this.options = void 0;
                _this.points = void 0;
                return _this;
            }
            /* *
             *
             * Static functions
             *
             * */
            // eslint-disable-next-line valid-jsdoc
            /**
             * Once off, register the windbarb approximation for data grouping. This can
             * be called anywhere (not necessarily in the translate function), but must
             * happen after the data grouping module is loaded and before the
             * wind barb series uses it.
             * @private
             */
            WindbarbSeries.registerApproximation = function () {
                if (!ApproximationRegistry.windbarb) {
                    ApproximationRegistry.windbarb = function (values, directions) {
                        var vectorX = 0,
                            vectorY = 0,
                            i,
                            len = values.length;
                        for (i = 0; i < len; i++) {
                            vectorX += values[i] * Math.cos(directions[i] * H.deg2rad);
                            vectorY += values[i] * Math.sin(directions[i] * H.deg2rad);
                        }
                        return [
                            // Wind speed
                            values.reduce(function (sum, value) {
                                return sum + value;
                            }, 0) / values.length,
                            // Wind direction
                            Math.atan2(vectorY, vectorX) / H.deg2rad
                        ];
                    };
                }
            };
            /* *
             *
             * Functions
             *
             * */
            WindbarbSeries.prototype.init = function (chart, options) {
                WindbarbSeries.registerApproximation();
                Series.prototype.init.call(this, chart, options);
            };
            // Get presentational attributes.
            WindbarbSeries.prototype.pointAttribs = function (point, state) {
                var options = this.options,
                    stroke = point.color || this.color,
                    strokeWidth = this.options.lineWidth;
                if (state) {
                    stroke = options.states[state].color || stroke;
                    strokeWidth =
                        (options.states[state].lineWidth || strokeWidth) +
                            (options.states[state].lineWidthPlus || 0);
                }
                return {
                    'stroke': stroke,
                    'stroke-width': strokeWidth
                };
            };
            // Create a single wind arrow. It is later rotated around the zero
            // centerpoint.
            WindbarbSeries.prototype.windArrow = function (point) {
                var knots = point.value * 1.943844,
                    level = point.beaufortLevel,
                    path,
                    barbs,
                    u = this.options.vectorLength / 20,
                    pos = -10;
                if (point.isNull) {
                    return [];
                }
                if (level === 0) {
                    return this.chart.renderer.symbols.circle(-10 * u, -10 * u, 20 * u, 20 * u);
                }
                // The stem and the arrow head
                path = [
                    ['M', 0, 7 * u],
                    ['L', -1.5 * u, 7 * u],
                    ['L', 0, 10 * u],
                    ['L', 1.5 * u, 7 * u],
                    ['L', 0, 7 * u],
                    ['L', 0, -10 * u] // top
                ];
                // For each full 50 knots, add a pennant
                barbs = (knots - knots % 50) / 50; // pennants
                if (barbs > 0) {
                    while (barbs--) {
                        path.push(pos === -10 ? ['L', 0, pos * u] : ['M', 0, pos * u], ['L', 5 * u, pos * u + 2], ['L', 0, pos * u + 4]);
                        // Substract from the rest and move position for next
                        knots -= 50;
                        pos += 7;
                    }
                }
                // For each full 10 knots, add a full barb
                barbs = (knots - knots % 10) / 10;
                if (barbs > 0) {
                    while (barbs--) {
                        path.push(pos === -10 ? ['L', 0, pos * u] : ['M', 0, pos * u], ['L', 7 * u, pos * u]);
                        knots -= 10;
                        pos += 3;
                    }
                }
                // For each full 5 knots, add a half barb
                barbs = (knots - knots % 5) / 5; // half barbs
                if (barbs > 0) {
                    while (barbs--) {
                        path.push(pos === -10 ? ['L', 0, pos * u] : ['M', 0, pos * u], ['L', 4 * u, pos * u]);
                        knots -= 5;
                        pos += 3;
                    }
                }
                return path;
            };
            WindbarbSeries.prototype.drawPoints = function () {
                var chart = this.chart,
                    yAxis = this.yAxis,
                    inverted = chart.inverted,
                    shapeOffset = this.options.vectorLength / 2;
                this.points.forEach(function (point) {
                    var plotX = point.plotX,
                        plotY = point.plotY;
                    // Check if it's inside the plot area, but only for the X
                    // dimension.
                    if (this.options.clip === false ||
                        chart.isInsidePlot(plotX, 0)) {
                        // Create the graphic the first time
                        if (!point.graphic) {
                            point.graphic = this.chart.renderer
                                .path()
                                .add(this.markerGroup)
                                .addClass('highcharts-point ' +
                                'highcharts-color-' +
                                pick(point.colorIndex, point.series.colorIndex));
                        }
                        // Position the graphic
                        point.graphic
                            .attr({
                            d: this.windArrow(point),
                            translateX: plotX + this.options.xOffset,
                            translateY: plotY + this.options.yOffset,
                            rotation: point.direction
                        });
                        if (!this.chart.styledMode) {
                            point.graphic
                                .attr(this.pointAttribs(point));
                        }
                    }
                    else if (point.graphic) {
                        point.graphic = point.graphic.destroy();
                    }
                    // Set the tooltip anchor position
                    point.tooltipPos = [
                        plotX + this.options.xOffset +
                            (inverted && !this.onSeries ? shapeOffset : 0),
                        plotY + this.options.yOffset -
                            (inverted ?
                                0 :
                                shapeOffset + yAxis.pos - chart.plotTop)
                    ]; // #6327
                }, this);
            };
            // Fade in the arrows on initializing series.
            WindbarbSeries.prototype.animate = function (init) {
                if (init) {
                    this.markerGroup.attr({
                        opacity: 0.01
                    });
                }
                else {
                    this.markerGroup.animate({
                        opacity: 1
                    }, animObject(this.options.animation));
                }
            };
            WindbarbSeries.prototype.markerAttribs = function (point, state) {
                return {};
            };
            WindbarbSeries.prototype.getExtremes = function () {
                return {};
            };
            WindbarbSeries.prototype.shouldShowTooltip = function (plotX, plotY, options) {
                if (options === void 0) { options = {}; }
                options.ignoreX = this.chart.inverted;
                options.ignoreY = !options.ignoreX;
                return _super.prototype.shouldShowTooltip.call(this, plotX, plotY, options);
            };
            /**
             * Wind barbs are a convenient way to represent wind speed and direction in
             * one graphical form. Wind direction is given by the stem direction, and
             * wind speed by the number and shape of barbs.
             *
             * @sample {highcharts|highstock} highcharts/demo/windbarb-series/
             *         Wind barb series
             *
             * @extends      plotOptions.column
             * @excluding    boostThreshold, marker, connectEnds, connectNulls,
             *               cropThreshold, dashStyle, dragDrop, gapSize, gapUnit,
             *               linecap, shadow, stacking, step, boostBlending
             * @since        6.0.0
             * @product      highcharts highstock
             * @requires     modules/windbarb
             * @optionparent plotOptions.windbarb
             */
            WindbarbSeries.defaultOptions = merge(ColumnSeries.defaultOptions, {
                /**
                 * Data grouping options for the wind barbs. In Highcharts, this
                 * requires the `modules/datagrouping.js` module to be loaded. In
                 * Highcharts Stock, data grouping is included.
                 *
                 * @sample  highcharts/plotoptions/windbarb-datagrouping
                 *          Wind barb with data grouping
                 *
                 * @since   7.1.0
                 * @product highcharts highstock
                 */
                dataGrouping: {
                    /**
                     * Whether to enable data grouping.
                     *
                     * @product highcharts highstock
                     */
                    enabled: true,
                    /**
                     * Approximation function for the data grouping. The default
                     * returns an average of wind speed and a vector average direction
                     * weighted by wind speed.
                     *
                     * @product highcharts highstock
                     *
                     * @type {string|Function}
                     */
                    approximation: 'windbarb',
                    /**
                     * The approximate data group width.
                     *
                     * @product highcharts highstock
                     */
                    groupPixelWidth: 30
                },
                /**
                 * The line width of the wind barb symbols.
                 */
                lineWidth: 2,
                /**
                 * The id of another series in the chart that the wind barbs are
                 * projected on. When `null`, the wind symbols are drawn on the X axis,
                 * but offset up or down by the `yOffset` setting.
                 *
                 * @sample {highcharts|highstock} highcharts/plotoptions/windbarb-onseries
                 *         Projected on area series
                 *
                 * @type {string|null}
                 */
                onSeries: null,
                states: {
                    hover: {
                        lineWidthPlus: 0
                    }
                },
                tooltip: {
                    /**
                     * The default point format for the wind barb tooltip. Note the
                     * `point.beaufort` property that refers to the Beaufort wind scale.
                     * The names can be internationalized by modifying
                     * `Highcharts.seriesTypes.windbarb.prototype.beaufortNames`.
                     */
                    pointFormat: '<span style="color:{point.color}">\u25CF</span> {series.name}: <b>{point.value}</b> ({point.beaufort})<br/>'
                },
                /**
                 * Pixel length of the stems.
                 */
                vectorLength: 20,
                /**
                 * @default   value
                 */
                colorKey: 'value',
                /**
                 * Vertical offset from the cartesian position, in pixels. The default
                 * value makes sure the symbols don't overlap the X axis when `onSeries`
                 * is `null`, and that they don't overlap the linked series when
                 * `onSeries` is given.
                 */
                yOffset: -20,
                /**
                 * Horizontal offset from the cartesian position, in pixels. When the
                 * chart is inverted, this option allows translation like
                 * [yOffset](#plotOptions.windbarb.yOffset) in non inverted charts.
                 *
                 * @since 6.1.0
                 */
                xOffset: 0
            });
            return WindbarbSeries;
        }(ColumnSeries));
        OnSeriesComposition.compose(WindbarbSeries);
        extend(WindbarbSeries.prototype, {
            beaufortFloor: [0, 0.3, 1.6, 3.4, 5.5, 8.0, 10.8, 13.9, 17.2, 20.8,
                24.5, 28.5, 32.7],
            beaufortName: ['Calm', 'Light air', 'Light breeze',
                'Gentle breeze', 'Moderate breeze', 'Fresh breeze',
                'Strong breeze', 'Near gale', 'Gale', 'Strong gale', 'Storm',
                'Violent storm', 'Hurricane'],
            invertible: false,
            parallelArrays: ['x', 'value', 'direction'],
            pointArrayMap: ['value', 'direction'],
            pointClass: WindbarbPoint,
            trackerGroups: ['markerGroup'],
            translate: function () {
                var beaufortFloor = this.beaufortFloor,
                    beaufortName = this.beaufortName;
                OnSeriesComposition.translate.call(this);
                this.points.forEach(function (point) {
                    var level = 0;
                    // Find the beaufort level (zero based)
                    for (; level < beaufortFloor.length; level++) {
                        if (beaufortFloor[level] > point.value) {
                            break;
                        }
                    }
                    point.beaufortLevel = level - 1;
                    point.beaufort = beaufortName[level - 1];
                });
            }
        });
        /* *
         *
         * Registry
         *
         * */
        WindbarbSeries.registerApproximation();
        SeriesRegistry.registerSeriesType('windbarb', WindbarbSeries);
        /* *
         *
         * Export default
         *
         * */
        /* *
         *
         * API Options
         *
         * */
        /**
         * A `windbarb` series. If the [type](#series.windbarb.type) option is not
         * specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.windbarb
         * @excluding dataParser, dataURL, boostThreshold, boostBlending
         * @product   highcharts highstock
         * @requires  modules/windbarb
         * @apioption series.windbarb
         */
        /**
         * An array of data points for the series. For the `windbarb` series type,
         * points can be given in the following ways:
         *
         * 1. An array of arrays with 3 values. In this case, the values correspond to
         *    `x,value,direction`. If the first value is a string, it is applied as the
         *    name of the point, and the `x` value is inferred.
         *    ```js
         *       data: [
         *           [Date.UTC(2017, 0, 1, 0), 3.3, 90],
         *           [Date.UTC(2017, 0, 1, 1), 12.1, 180],
         *           [Date.UTC(2017, 0, 1, 2), 11.1, 270]
         *       ]
         *    ```
         *
         * 2. An array of objects with named values. The following snippet shows only a
         *    few settings, see the complete options set below. If the total number of
         *    data points exceeds the series'
         *    [turboThreshold](#series.area.turboThreshold), this option is not
         *    available.
         *    ```js
         *       data: [{
         *           x: Date.UTC(2017, 0, 1, 0),
         *           value: 12.1,
         *           direction: 90
         *       }, {
         *           x: Date.UTC(2017, 0, 1, 1),
         *           value: 11.1,
         *           direction: 270
         *       }]
         *    ```
         *
         * @sample {highcharts} highcharts/chart/reflow-true/
         *         Numerical values
         * @sample {highcharts} highcharts/series/data-array-of-arrays/
         *         Arrays of numeric x and y
         * @sample {highcharts} highcharts/series/data-array-of-arrays-datetime/
         *         Arrays of datetime x and y
         * @sample {highcharts} highcharts/series/data-array-of-name-value/
         *         Arrays of point.name and y
         * @sample {highcharts} highcharts/series/data-array-of-objects/
         *         Config objects
         *
         * @type      {Array<Array<(number|string),number,number>|*>}
         * @extends   series.line.data
         * @product   highcharts highstock
         * @apioption series.windbarb.data
         */
        /**
         * The wind speed in meters per second.
         *
         * @type      {number|null}
         * @product   highcharts highstock
         * @apioption series.windbarb.data.value
         */
        /**
         * The wind direction in degrees, where 0 is north (pointing towards south).
         *
         * @type      {number}
         * @product   highcharts highstock
         * @apioption series.windbarb.data.direction
         */
        ''; // adds doclets above to transpiled file

        return WindbarbSeries;
    });
    _registerModule(_modules, 'masters/modules/windbarb.src.js', [], function () {


    });
}));