/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * Streamgraph module
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
        define('highcharts/modules/streamgraph', ['highcharts'], function (Highcharts) {
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
    _registerModule(_modules, 'Series/Streamgraph/StreamgraphSeries.js', [_modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (SeriesRegistry, U) {
        /* *
         *
         *  Streamgraph module
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
        var AreaSplineSeries = SeriesRegistry.seriesTypes.areaspline;
        var merge = U.merge,
            extend = U.extend;
        /**
         * Streamgraph series type
         *
         * @private
         * @class
         * @name Highcharts.seriesTypes.streamgraph
         *
         * @augments Highcharts.Series
         */
        var StreamgraphSeries = /** @class */ (function (_super) {
                __extends(StreamgraphSeries, _super);
            function StreamgraphSeries() {
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
            // Modifier function for stream stacks. It simply moves the point up or
            // down in order to center the full stack vertically.
            StreamgraphSeries.prototype.streamStacker = function (pointExtremes, stack, i) {
                // Y bottom value
                pointExtremes[0] -= stack.total / 2;
                // Y value
                pointExtremes[1] -= stack.total / 2;
                // Record the Y data for use when getting axis extremes
                this.stackedYData[i] = pointExtremes;
            };
            /**
             * A streamgraph is a type of stacked area graph which is displaced around a
             * central axis, resulting in a flowing, organic shape.
             *
             * @sample {highcharts|highstock} highcharts/demo/streamgraph/
             *         Streamgraph
             *
             * @extends      plotOptions.areaspline
             * @since        6.0.0
             * @product      highcharts highstock
             * @requires     modules/streamgraph
             * @optionparent plotOptions.streamgraph
             */
            StreamgraphSeries.defaultOptions = merge(AreaSplineSeries.defaultOptions, {
                /**
                 * @see [fillColor](#plotOptions.streamgraph.fillColor)
                 * @see [fillOpacity](#plotOptions.streamgraph.fillOpacity)
                 *
                 * @apioption plotOptions.streamgraph.color
                 */
                /**
                 * @see [color](#plotOptions.streamgraph.color)
                 * @see [fillOpacity](#plotOptions.streamgraph.fillOpacity)
                 *
                 * @apioption plotOptions.streamgraph.fillColor
                 */
                /**
                 * @see [color](#plotOptions.streamgraph.color)
                 * @see [fillColor](#plotOptions.streamgraph.fillColor)
                 *
                 * @apioption plotOptions.streamgraph.fillOpacity
                 */
                fillOpacity: 1,
                lineWidth: 0,
                marker: {
                    enabled: false
                },
                stacking: 'stream'
            });
            return StreamgraphSeries;
        }(AreaSplineSeries));
        extend(StreamgraphSeries.prototype, {
            negStacks: false
        });
        SeriesRegistry.registerSeriesType('streamgraph', StreamgraphSeries);
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
         * A `streamgraph` series. If the [type](#series.streamgraph.type) option is not
         * specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.streamgraph
         * @excluding dataParser, dataURL, step, boostThreshold, boostBlending
         * @product   highcharts highstock
         * @requires  modules/streamgraph
         * @apioption series.streamgraph
         */
        /**
         * @see [fillColor](#series.streamgraph.fillColor)
         * @see [fillOpacity](#series.streamgraph.fillOpacity)
         *
         * @apioption series.streamgraph.color
         */
        /**
         * An array of data points for the series. For the `streamgraph` series type,
         * points can be given in the following ways:
         *
         * 1. An array of numerical values. In this case, the numerical values will be
         *    interpreted as `y` options. The `x` values will be automatically
         *    calculated, either starting at 0 and incremented by 1, or from
         *    `pointStart` and `pointInterval` given in the series options. If the axis
         *    has categories, these will be used. Example:
         *    ```js
         *    data: [0, 5, 3, 5]
         *    ```
         *
         * 2. An array of arrays with 2 values. In this case, the values correspond to
         *    `x,y`. If the first value is a string, it is applied as the name of the
         *    point, and the `x` value is inferred.
         *    ```js
         *        data: [
         *            [0, 9],
         *            [1, 7],
         *            [2, 6]
         *        ]
         *    ```
         *
         * 3. An array of objects with named values. The following snippet shows only a
         *    few settings, see the complete options set below. If the total number of
         *    data points exceeds the series'
         *    [turboThreshold](#series.area.turboThreshold),
         *    this option is not available.
         *    ```js
         *        data: [{
         *            x: 1,
         *            y: 9,
         *            name: "Point2",
         *            color: "#00FF00"
         *        }, {
         *            x: 1,
         *            y: 6,
         *            name: "Point1",
         *            color: "#FF00FF"
         *        }]
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
         * @type      {Array<number|Array<(number|string),(number|null)>|null|*>}
         * @extends   series.line.data
         * @product   highcharts highstock
         * @apioption series.streamgraph.data
         */
        /**
         * @see [color](#series.streamgraph.color)
         * @see [fillOpacity](#series.streamgraph.fillOpacity)
         *
         * @apioption series.streamgraph.fillColor
         */
        /**
         * @see [color](#series.streamgraph.color)
         * @see [fillColor](#series.streamgraph.fillColor)
         *
         * @type      {number}
         * @default   1
         * @apioption series.streamgraph.fillOpacity
         */
        ''; // adds doclets above to transpiled file

        return StreamgraphSeries;
    });
    _registerModule(_modules, 'masters/modules/streamgraph.src.js', [], function () {


    });
}));