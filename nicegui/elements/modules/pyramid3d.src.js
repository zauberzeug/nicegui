/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * Highcharts 3D funnel module
 *
 * (c) 2010-2021 Kacper Madej
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/pyramid3d', ['highcharts', 'highcharts/highcharts-3d', 'highcharts/modules/cylinder', 'highcharts/modules/funnel3d'], function (Highcharts) {
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
    _registerModule(_modules, 'Series/Pyramid3D/Pyramid3DSeries.js', [_modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (SeriesRegistry, U) {
        /* *
         *
         *  Highcharts pyramid3d series module
         *
         *  (c) 2010-2021 Highsoft AS
         *  Author: Kacper Madej
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
        var Funnel3DSeries = SeriesRegistry.seriesTypes.funnel3d;
        var merge = U.merge;
        /* *
         *
         *  Class
         *
         * */
        /**
         * The pyramid3d series type.
         *
         * @class
         * @name Highcharts.seriesTypes.pyramid3d
         * @augments seriesTypes.funnel3d
         * @requires highcharts-3d
         * @requires modules/cylinder
         * @requires modules/funnel3d
         * @requires modules/pyramid3d
         */
        var Pyramid3DSeries = /** @class */ (function (_super) {
                __extends(Pyramid3DSeries, _super);
            function Pyramid3DSeries() {
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
            /**
             * A pyramid3d is a 3d version of pyramid series type. Pyramid charts are
             * a type of chart often used to visualize stages in a sales project,
             * where the top are the initial stages with the most clients.
             *
             * @sample highcharts/demo/pyramid3d/
             *         Pyramid3d
             *
             * @extends      plotOptions.funnel3d
             * @excluding    neckHeight, neckWidth, dataSorting
             * @product      highcharts
             * @since        7.1.0
             * @requires     highcharts-3d
             * @requires     modules/cylinder
             * @requires     modules/funnel3d
             * @requires     modules/pyramid3d
             * @optionparent plotOptions.pyramid3d
             */
            Pyramid3DSeries.defaultOptions = merge(Funnel3DSeries.defaultOptions, {
                /**
                 * A reversed pyramid3d is funnel3d, but the latter supports neck
                 * related options: neckHeight and neckWidth
                 *
                 * @product highcharts
                 */
                reversed: true,
                neckHeight: 0,
                neckWidth: 0,
                dataLabels: {
                    verticalAlign: 'top'
                }
            });
            return Pyramid3DSeries;
        }(Funnel3DSeries));
        SeriesRegistry.registerSeriesType('pyramid3d', Pyramid3DSeries);
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
         * A `pyramid3d` series. If the [type](#series.pyramid3d.type) option is
         * not specified, it is inherited from [chart.type](#chart.type).
         *
         * @since     7.1.0
         * @extends   series.pyramid,plotOptions.pyramid3d
         * @excluding allAreas,boostThreshold,colorAxis,compare,compareBase,dataSorting
         * @product   highcharts
         * @sample    {highcharts} highcharts/demo/pyramid3d/ Pyramid3d
         * @requires  modules/pyramid3d
         * @apioption series.pyramid3d
         */
        /**
         * An array of data points for the series. For the `pyramid3d` series
         * type, points can be given in the following ways:
         *
         * 1.  An array of numerical values. In this case, the numerical values
         * will be interpreted as `y` options. The `x` values will be automatically
         * calculated, either starting at 0 and incremented by 1, or from `pointStart`
         * and `pointInterval` given in the series options. If the axis has
         * categories, these will be used. Example:
         *
         *  ```js
         *  data: [0, 5, 3, 5]
         *  ```
         *
         * 2.  An array of objects with named values. The following snippet shows only a
         * few settings, see the complete options set below. If the total number of data
         * points exceeds the series'
         * [turboThreshold](#series.pyramid3d.turboThreshold),
         * this option is not available.
         *
         *  ```js
         *     data: [{
         *         y: 2,
         *         name: "Point2",
         *         color: "#00FF00"
         *     }, {
         *         y: 4,
         *         name: "Point1",
         *         color: "#FF00FF"
         *     }]
         *  ```
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
         * @type      {Array<number|Array<number>|*>}
         * @extends   series.funnel3d.data
         * @product   highcharts
         * @apioption series.pyramid3d.data
         */
        ''; // adds doclets above to the transpiled file

        return Pyramid3DSeries;
    });
    _registerModule(_modules, 'masters/modules/pyramid3d.src.js', [], function () {


    });
}));