/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * Pareto series type for Highcharts
 *
 * (c) 2010-2021 Sebastian Bochan
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/pareto', ['highcharts'], function (Highcharts) {
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
    _registerModule(_modules, 'Series/DerivedComposition.js', [_modules['Core/Globals.js'], _modules['Core/Series/Series.js'], _modules['Core/Utilities.js']], function (H, Series, U) {
        /* *
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var noop = H.noop;
        var addEvent = U.addEvent,
            defined = U.defined;
        /* *
         *
         *  Composition
         *
         * */
        /**
         * Provides methods for auto setting/updating series data based on the based
         * series data.
         * @private
         */
        var DerivedComposition;
        (function (DerivedComposition) {
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
            DerivedComposition.hasDerivedData = true;
            /**
             * Method to be implemented - inside the method the series has already
             * access to the base series via m `this.baseSeries` and the bases data is
             * initialised. It should return data in the format accepted by
             * `Series.setData()` method
             * @private
             */
            DerivedComposition.setDerivedData = noop;
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
                    var seriesProto = SeriesClass.prototype;
                    seriesProto.addBaseSeriesEvents = addBaseSeriesEvents;
                    seriesProto.addEvents = addEvents;
                    seriesProto.destroy = destroy;
                    seriesProto.init = init;
                    seriesProto.setBaseSeries = setBaseSeries;
                }
                return SeriesClass;
            }
            DerivedComposition.compose = compose;
            /**
             * Initialise series
             * @private
             */
            function init() {
                Series.prototype.init.apply(this, arguments);
                this.initialised = false;
                this.baseSeries = null;
                this.eventRemovers = [];
                this.addEvents();
            }
            DerivedComposition.init = init;
            /**
             * Sets base series for the series
             * @private
             */
            function setBaseSeries() {
                var chart = this.chart,
                    baseSeriesOptions = this.options.baseSeries,
                    baseSeries = (defined(baseSeriesOptions) &&
                        (chart.series[baseSeriesOptions] ||
                            chart.get(baseSeriesOptions)));
                this.baseSeries = baseSeries || null;
            }
            DerivedComposition.setBaseSeries = setBaseSeries;
            /**
             * Adds events for the series
             * @private
             */
            function addEvents() {
                var _this = this;
                this.eventRemovers.push(addEvent(this.chart, 'afterLinkSeries', function () {
                    _this.setBaseSeries();
                    if (_this.baseSeries && !_this.initialised) {
                        _this.setDerivedData();
                        _this.addBaseSeriesEvents();
                        _this.initialised = true;
                    }
                }));
            }
            DerivedComposition.addEvents = addEvents;
            /**
             * Adds events to the base series - it required for recalculating the data
             * in the series if the base series is updated / removed / etc.
             * @private
             */
            function addBaseSeriesEvents() {
                var _this = this;
                this.eventRemovers.push(addEvent(this.baseSeries, 'updatedData', function () {
                    _this.setDerivedData();
                }), addEvent(this.baseSeries, 'destroy', function () {
                    _this.baseSeries = null;
                    _this.initialised = false;
                }));
            }
            DerivedComposition.addBaseSeriesEvents = addBaseSeriesEvents;
            /**
             * Destroys the series
             * @private
             */
            function destroy() {
                this.eventRemovers.forEach(function (remover) {
                    remover();
                });
                Series.prototype.destroy.apply(this, arguments);
            }
            DerivedComposition.destroy = destroy;
        })(DerivedComposition || (DerivedComposition = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return DerivedComposition;
    });
    _registerModule(_modules, 'Series/ParetoSeries/ParetoSeries.js', [_modules['Series/DerivedComposition.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (DerivedComposition, SeriesRegistry, U) {
        /* *
         *
         *  (c) 2010-2021 Sebastian Bochan
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
        var LineSeries = SeriesRegistry.seriesTypes.line;
        var correctFloat = U.correctFloat,
            merge = U.merge,
            extend = U.extend;
        /* *
         *
         *  Class
         *
         * */
        /**
         * The pareto series type.
         *
         * @private
         * @class
         * @name Highcharts.seriesTypes.pareto
         *
         * @augments Highcharts.Series
         */
        var ParetoSeries = /** @class */ (function (_super) {
                __extends(ParetoSeries, _super);
            function ParetoSeries() {
                /* *
                 *
                 *  Static properties
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
                _this.points = void 0;
                _this.options = void 0;
                return _this;
            }
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Calculate y sum and each percent point.
             *
             * @private
             * @function Highcharts.Series#sumPointsPercents
             *
             * @param {Array<number>} yValues
             * Y values
             *
             * @param {Array<number>} xValues
             * X values
             *
             * @param {number} sum
             * Sum of all y values
             *
             * @param {boolean} [isSum]
             * Declares if calculate sum of all points
             *
             * @return {number|Array<number,number>}
             * Returns sum of points or array of points [x,sum]
             *
             * @requires modules/pareto
             */
            ParetoSeries.prototype.sumPointsPercents = function (yValues, xValues, sum, isSum) {
                var sumY = 0,
                    sumPercent = 0,
                    percentPoints = [],
                    percentPoint;
                yValues.forEach(function (point, i) {
                    if (point !== null) {
                        if (isSum) {
                            sumY += point;
                        }
                        else {
                            percentPoint = (point / sum) * 100;
                            percentPoints.push([
                                xValues[i],
                                correctFloat(sumPercent + percentPoint)
                            ]);
                            sumPercent += percentPoint;
                        }
                    }
                });
                return (isSum ? sumY : percentPoints);
            };
            /**
             * Calculate sum and return percent points.
             *
             * @private
             * @function Highcharts.Series#setDerivedData
             * @requires modules/pareto
             */
            ParetoSeries.prototype.setDerivedData = function () {
                var xValues = this.baseSeries.xData,
                    yValues = this.baseSeries.yData,
                    sum = this.sumPointsPercents(yValues,
                    xValues,
                    null,
                    true);
                this.setData(this.sumPointsPercents(yValues, xValues, sum, false), false);
            };
            /**
             * A pareto diagram is a type of chart that contains both bars and a line
             * graph, where individual values are represented in descending order by
             * bars, and the cumulative total is represented by the line.
             *
             * @sample {highcharts} highcharts/demo/pareto/
             *         Pareto diagram
             *
             * @extends      plotOptions.line
             * @since        6.0.0
             * @product      highcharts
             * @excluding    allAreas, boostThreshold, borderColor, borderRadius,
             *               borderWidth, crisp, colorAxis, depth, data, dragDrop,
             *               edgeColor, edgeWidth, findNearestPointBy, gapSize, gapUnit,
             *               grouping, groupPadding, groupZPadding, maxPointWidth, keys,
             *               negativeColor, pointInterval, pointIntervalUnit,
             *               pointPadding, pointPlacement, pointRange, pointStart,
             *               pointWidth, shadow, step, softThreshold, stacking,
             *               threshold, zoneAxis, zones, boostBlending
             * @requires     modules/pareto
             * @optionparent plotOptions.pareto
             */
            ParetoSeries.defaultOptions = merge(LineSeries.defaultOptions, {
                /**
                 * Higher zIndex than column series to draw line above shapes.
                 */
                zIndex: 3
            });
            return ParetoSeries;
        }(LineSeries));
        extend(ParetoSeries.prototype, {
            hasDerivedData: DerivedComposition.hasDerivedData
        });
        DerivedComposition.compose(ParetoSeries);
        SeriesRegistry.registerSeriesType('pareto', ParetoSeries);
        /* *
         *
         *  Default export
         *
         * */
        /* *
         *
         *  API options
         *
         * */
        /**
         * A `pareto` series. If the [type](#series.pareto.type) option is not
         * specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.pareto
         * @since     6.0.0
         * @product   highcharts
         * @excluding data, dataParser, dataURL, boostThreshold, boostBlending
         * @requires  modules/pareto
         * @apioption series.pareto
         */
        /**
         * An integer identifying the index to use for the base series, or a string
         * representing the id of the series.
         *
         * @type      {number|string}
         * @default   undefined
         * @apioption series.pareto.baseSeries
         */
        /**
         * An array of data points for the series. For the `pareto` series type,
         * points are calculated dynamically.
         *
         * @type      {Array<Array<number|string>|*>}
         * @extends   series.column.data
         * @since     6.0.0
         * @product   highcharts
         * @apioption series.pareto.data
         */
        ''; // adds the doclets above to the transpiled file

        return ParetoSeries;
    });
    _registerModule(_modules, 'masters/modules/pareto.src.js', [], function () {


    });
}));